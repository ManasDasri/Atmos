import json
import math
from pathlib import Path
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, value
from shapely.geometry import shape, Point
import pyproj
from shapely.ops import transform
from waqi_service import BENGALURU_ZONES
from ml_model import predict_urbanization

# Budget and Costs
TOTAL_BUDGET = 6000000  # ₹60 Lakhs
REF_SENSOR_COST = 200000
MON_SENSOR_COST = 50000

# Geographic bounds and grid size
GRID_SPACING_KM = 2.5

def get_bangalore_polygon_and_area():
    geojson_path = Path(__file__).resolve().parent.parent / "frontend" / "static" / "bangalore.geojson"
    with open(geojson_path, "r") as f:
        data = json.load(f)
        
    polygon = shape(data["features"][0]["geometry"])
    
    # Calculate exact area using pyproj
    wgs84 = pyproj.CRS('EPSG:4326')
    utm = pyproj.CRS('EPSG:32643') # UTM zone 43N for Bangalore
    project = pyproj.Transformer.from_crs(wgs84, utm, always_xy=True).transform
    projected_polygon = transform(project, polygon)
    area_km2 = projected_polygon.area / 1e6
    
    return polygon, area_km2

def generate_grid_candidates(polygon):
    minx, miny, maxx, maxy = polygon.bounds
    
    # Approx degrees for 1.5km
    step_deg = GRID_SPACING_KM / 111.0 
    
    candidates = []
    
    lon = minx
    while lon <= maxx:
        lat = miny
        while lat <= maxy:
            pt = Point(lon, lat)
            if polygon.contains(pt):
                # Interpolate properties from nearest known zones
                min_dist = float('inf')
                nearest_zone = None
                for z in BENGALURU_ZONES:
                    z_lat, z_lon = z["center"]
                    dist = math.sqrt((lat - z_lat)**2 + (lon - z_lon)**2) * 111
                    if dist < min_dist:
                        min_dist = dist
                        nearest_zone = z
                
                traffic_str = nearest_zone["traffic"]
                traffic_val = {"High": 0.9, "Medium": 0.6, "Low": 0.3}.get(traffic_str, 0.5)
                
                # Decay factor based on distance
                decay = max(0.2, 1.0 - (min_dist / 15.0))
                
                simulated_pm25 = int((100 * decay) + 20) # Dummy PM2.5 based on distance
                simulated_pop_density = int((20000 * decay) + 1000)
                
                urban_score = predict_urbanization(lat, lon, simulated_pop_density, traffic_val)
                
                candidates.append({
                    "id": f"Grid_{round(lat, 3)}_{round(lon, 3)}",
                    "lat": lat,
                    "lon": lon,
                    "pm25": simulated_pm25,
                    "traffic": traffic_str,
                    "pop_density": simulated_pop_density,
                    "urbanization_score": urban_score,
                    "nearest_zone": nearest_zone["name"]
                })
                
            lat += step_deg
        lon += step_deg
        
    return candidates

def run_milp_optimization():
    print("🌿 ATMOS - Starting Grid-Based MILP + ML Optimization...")
    polygon, area_km2 = get_bangalore_polygon_and_area()
    print(f"🌍 Exact Calculated Area of Bangalore: {area_km2:.2f} km²")
    
    candidates = generate_grid_candidates(polygon)
    print(f"🎯 Generated {len(candidates)} grid candidate locations inside boundary.")
    
    prob = LpProblem("Atmos_Sensor_Deployment", LpMaximize)
    
    # Variables
    ref_vars = {c["id"]: LpVariable(f"ref_{c['id']}", cat='Binary') for c in candidates}
    mon_vars = {c["id"]: LpVariable(f"mon_{c['id']}", cat='Binary') for c in candidates}
    
    # Objective Function: Maximize coverage priority
    # Priority uses PM2.5, Pop Density, Traffic, AND the ML Urbanization Score!
    priority = {}
    for c in candidates:
        t_mult = {"High": 1.5, "Medium": 1.0, "Low": 0.5}.get(c["traffic"], 1.0)
        # ML Score acts as a massive future-proofing multiplier (up to 2x priority)
        ml_multiplier = 1.0 + c["urbanization_score"] 
        priority[c["id"]] = (c["pm25"] * 0.4 + (c["pop_density"]/100) * 0.4 + (t_mult * 50) * 0.2) * ml_multiplier
        
    # Maximize sum of priority * sensors
    prob += lpSum([priority[c["id"]] * (ref_vars[c["id"]] * 1.5 + mon_vars[c["id"]]) for c in candidates])
    
    # Constraint 1: Budget limit
    prob += lpSum([ref_vars[c["id"]] * REF_SENSOR_COST + mon_vars[c["id"]] * MON_SENSOR_COST for c in candidates]) <= TOTAL_BUDGET
    
    # Constraint 2: Min/Max sensors
    prob += lpSum([ref_vars[c["id"]] for c in candidates]) >= 4 # At least 4 reference
    prob += lpSum([mon_vars[c["id"]] for c in candidates]) >= 10 # At least 10 monitors
    
    # Solve
    prob.solve()
    
    if LpStatus[prob.status] != 'Optimal':
        print("❌ Could not find optimal solution.")
        return
        
    deployed_sensors = []
    total_cost = 0
    ref_count = 0
    mon_count = 0
    
    for c in candidates:
        if value(ref_vars[c["id"]]) == 1.0:
            c["type"] = "reference"
            c["range_km"] = 4
            deployed_sensors.append(c)
            total_cost += REF_SENSOR_COST
            ref_count += 1
        elif value(mon_vars[c["id"]]) == 1.0:
            c["type"] = "monitoring"
            c["range_km"] = 3
            deployed_sensors.append(c)
            total_cost += MON_SENSOR_COST
            mon_count += 1
            
    print(f"✅ Optimization Complete! Deployed {ref_count} Ref, {mon_count} Mon. Total Cost: ₹{total_cost}")
    
    # Calculate Coverage
    effective_coverage = (ref_count * math.pi * 4**2) + (mon_count * math.pi * 3**2)
    # Factor in overlap
    overlap_penalty = 0.85
    actual_coverage = effective_coverage * overlap_penalty
    coverage_percentage = min(100.0, (actual_coverage / area_km2) * 100)
    
    # Aggregate into zones for frontend compatibility
    zone_dict = {}
    for s in deployed_sensors:
        zn = s["nearest_zone"]
        if zn not in zone_dict:
            zone_dict[zn] = {
                "name": zn,
                "pm25": 0,
                "traffic": s["traffic"],
                "total_sensors": 0,
                "reference_sensors": 0,
                "monitoring_sensors": 0,
                "has_reference_sensor": False,
                "center": [s["lat"], s["lon"]]
            }
        
        zone_dict[zn]["pm25"] = max(zone_dict[zn]["pm25"], s["pm25"])
        zone_dict[zn]["total_sensors"] += 1
        if s["type"] == "reference":
            zone_dict[zn]["reference_sensors"] += 1
            zone_dict[zn]["has_reference_sensor"] = True
        else:
            zone_dict[zn]["monitoring_sensors"] += 1

    zones_list = list(zone_dict.values())
    
    avg_pm25 = sum(s["pm25"] for s in deployed_sensors) / len(deployed_sensors)
    
    output = {
        "status": "optimized",
        "total_cost": total_cost,
        "total_sensors": len(deployed_sensors),
        "reference_sensors": ref_count,
        "monitoring_sensors": mon_count,
        "total_zones": len(zones_list),
        "average_aqi": avg_pm25,
        "effective_coverage_km2": actual_coverage,
        "theoretical_coverage_km2": effective_coverage,
        "overlap_percentage": (1.0 - overlap_penalty) * 100,
        "coverage_percentage": coverage_percentage,
        "city_total_area_km2": area_km2,
        "worst_zone": {"name": "Central", "aqi": max(s["pm25"] for s in deployed_sensors)},
        "best_zone": {"name": "Outskirts", "aqi": min(s["pm25"] for s in deployed_sensors)},
        "all_sensors": deployed_sensors,
        "zones": zones_list
    }
    
    output_path = Path(__file__).resolve().parent.parent / "frontend" / "data" / "optimized_sensors.json"
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(output, f, indent=4)

if __name__ == "__main__":
    run_milp_optimization()