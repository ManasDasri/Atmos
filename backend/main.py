from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os
from pathlib import Path
import sys

# Add current directory to Python path
sys.path.append(str(Path(__file__).parent))

# Import optimization and WAQI service
try:
    from optimize import run_milp_optimization as optimize_hybrid_model
    from waqi_service import fetch_live_aqi, BENGALURU_ZONES
    from traffic_service import fetch_zone_traffic_live
except ImportError as e:
    print(f"Import warning: {e}")
    
    # Fallback functions
    def optimize_hybrid_model():
        return {"error": "Backend modules not available"}
    
    def fetch_live_aqi():
        return {"error": "WAQI service not available"}
    
    def fetch_zone_traffic_live(zones):
        return zones

app = FastAPI(title="Atmos")

# FIXED: Setup paths - frontend is at same level as backend, not inside
BASE_DIR = Path(__file__).resolve().parent  # backend directory
PROJECT_ROOT = BASE_DIR.parent  # hybrid directory (parent of backend)
FRONTEND_DIR = PROJECT_ROOT / "frontend"  # frontend directory at project root
DATA_DIR = BASE_DIR / "data"  # data directory inside backend

# Create data directory if it doesn't exist
try:
    DATA_DIR.mkdir(exist_ok=True)
except Exception as e:
    print(f"Warning: Could not create data directory: {e}")

# Verify frontend directory exists
if not FRONTEND_DIR.exists():
    print(f"ERROR: Frontend directory not found at {FRONTEND_DIR}")
    print(f"Current directory structure:")
    print(f"  BASE_DIR: {BASE_DIR}")
    print(f"  PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"  FRONTEND_DIR: {FRONTEND_DIR}")
    raise RuntimeError(f"Frontend directory does not exist: {FRONTEND_DIR}")

# Verify static and templates directories exist
STATIC_DIR = FRONTEND_DIR / "static"
TEMPLATES_DIR = FRONTEND_DIR / "templates"

if not STATIC_DIR.exists():
    raise RuntimeError(f"Static directory does not exist: {STATIC_DIR}")
if not TEMPLATES_DIR.exists():
    raise RuntimeError(f"Templates directory does not exist: {TEMPLATES_DIR}")

print(f"✓ Frontend directory found: {FRONTEND_DIR}")
print(f"✓ Static directory: {STATIC_DIR}")
print(f"✓ Templates directory: {TEMPLATES_DIR}")

# Mount static files and templates
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Model file path
MODEL_FILE = DATA_DIR / "hybrid_model.json"

def initialize_model():
    """Initialize the hybrid model if it doesn't exist"""
    if not MODEL_FILE.exists():
        print("Generating initial hybrid model...")
        try:
            optimize_hybrid_model()
        except Exception as e:
            print(f"Error initializing model: {e}")
    else:
        print("Hybrid model already exists")

# Initialize on startup
@app.on_event("startup")
async def startup_event():
    initialize_model()

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request})

@app.get("/compare", response_class=HTMLResponse)
async def compare(request: Request):
    return templates.TemplateResponse(request=request, name="compare.html", context={"request": request})

@app.get("/coverage", response_class=HTMLResponse)
async def coverage(request: Request):
    return templates.TemplateResponse(request=request, name="coverage.html", context={"request": request})

@app.get("/deployment", response_class=HTMLResponse)
async def deployment(request: Request):
    return templates.TemplateResponse(request=request, name="deployment.html", context={"request": request})

@app.get("/query", response_class=HTMLResponse)
async def query(request: Request):
    return templates.TemplateResponse(request=request, name="query.html", context={"request": request})

@app.get("/info", response_class=HTMLResponse)
async def info(request: Request):
    return templates.TemplateResponse(request=request, name="info.html", context={"request": request})

@app.get("/contrast", response_class=HTMLResponse)
async def contrast(request: Request):
    return templates.TemplateResponse(request=request, name="contrast.html", context={"request": request})

# API Endpoints
@app.get("/api/model")
async def get_model():
    """Get the current hybrid model data"""
    try:
        if not MODEL_FILE.exists():
            return JSONResponse(content={"error": "Model not found. Run optimization first."}, status_code=404)
            
        with open(MODEL_FILE, 'r') as f:
            data = json.load(f)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/api/waqi/live")
async def get_live_aqi():
    """Get live AQI data from WAQI"""
    try:
        data = fetch_live_aqi()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/api/zone/{zone_name}")
async def get_zone_data(zone_name: str):
    """Get data for a specific zone"""
    try:
        if not MODEL_FILE.exists():
            return JSONResponse(content={"error": "Model not found"}, status_code=404)
            
        with open(MODEL_FILE, 'r') as f:
            model = json.load(f)
        
        zone = next((z for z in model['zones'] if z['name'].lower() == zone_name.lower()), None)
        if zone:
            return JSONResponse(content=zone)
        return JSONResponse(content={"error": "Zone not found"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/api/optimize")
async def trigger_optimization():
    """Trigger a new optimization run"""
    try:
        result = optimize_hybrid_model()
        if "error" in result:
            return JSONResponse(content={"error": result["error"]}, status_code=500)
            
        with open(MODEL_FILE, 'r') as f:
            data = json.load(f)
        return JSONResponse(content={"success": True, "model": data})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/api/stats")
async def get_statistics():
    """Get overall statistics - FIXED VERSION"""
    try:
        if not MODEL_FILE.exists():
            return JSONResponse(content={"error": "Model not found"}, status_code=404)
            
        with open(MODEL_FILE, 'r') as f:
            model = json.load(f)
        
        zones = model['zones']
        total_sensors = model.get('total_sensors', 67)
        avg_aqi = sum(z.get('pm25', 0) for z in zones) / len(zones) if zones else 0
        worst_zone = max(zones, key=lambda z: z.get('pm25', 0)) if zones else {"name": "N/A", "pm25": 0}
        best_zone = min(zones, key=lambda z: z.get('pm25', 0)) if zones else {"name": "N/A", "pm25": 0}
        
        # FIX: Use correct field names from model
        stats = {
            "total_sensors": total_sensors,
            "reference_sensors": model.get('reference_sensors', 4),
            "monitoring_sensors": model.get('monitoring_sensors', total_sensors - 4),
            "total_zones": len(zones),
            "average_aqi": round(avg_aqi, 1),
            "worst_zone": {"name": worst_zone['name'], "aqi": worst_zone.get('pm25', 0)},
            "best_zone": {"name": best_zone['name'], "aqi": best_zone.get('pm25', 0)},
            "total_cost": model.get('total_cost', 2490000),
            "budget": model.get('budget', 2500000),
            "coverage_percentage": model.get('coverage_percentage', 0),
            # FIX: Use correct field name from model
            "coverage_area_km2": model.get('effective_coverage_km2', 0),  # Changed from coverage_area_km2
            "theoretical_coverage_km2": model.get('theoretical_coverage_km2', 0),
            "overlap_percentage": model.get('overlap_percentage', 0)
        }
        return JSONResponse(content=stats)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/api/zone/{zone_name}/sensors")
async def get_zone_sensor_locations(zone_name: str):
    """Get detailed sensor locations for a specific zone"""
    try:
        if not MODEL_FILE.exists():
            return JSONResponse(content={"error": "Model not found"}, status_code=404)
            
        with open(MODEL_FILE, 'r') as f:
            model = json.load(f)
        
        # Get zone from model
        zone = next((z for z in model['zones'] if z['name'].lower() == zone_name.lower()), None)
        if not zone:
            return JSONResponse(content={"error": "Zone not found"}, status_code=404)
        
        # Get sensor locations from zone data
        sensor_locations = zone.get('sensor_locations', [])
        
        result = {
            "zone_name": zone['name'],
            "total_sensors": zone['sensors'],
            "has_reference_sensor": zone.get('has_reference_sensor', False),
            "monitoring_sensors": zone.get('monitoring_sensors', zone['sensors']),
            "pm25": zone['pm25'],
            "traffic": zone['traffic'],
            "center": zone.get('center', [12.9716, 77.5946]),
            "sensor_placements": sensor_locations[:zone['sensors']]
        }
        
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🌿 ATMOS - Starting Server")
    print("="*60)
    print(f"Backend: {BASE_DIR}")
    print(f"Frontend: {FRONTEND_DIR}")
    print(f"Data: {DATA_DIR}")
    print("="*60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)