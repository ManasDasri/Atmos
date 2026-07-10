import requests
import os
from typing import Dict, List
from datetime import datetime
import random

# TomTom API Key
TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY", "f5aqsYFWVP830rKyIshCi4PtO3EKxTMH")

def get_tomtom_traffic(lat: float, lon: float) -> Dict:
    """
    Fetch real-time traffic data from TomTom API
    Returns traffic flow data including current speed, free flow speed, and congestion
    """
    # Check if API key is available and not empty
    if not TOMTOM_API_KEY or TOMTOM_API_KEY.strip() == "":
        return None
        
    try:
        # TomTom Traffic Flow API endpoint
        url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
        
        params = {
            'key': TOMTOM_API_KEY,
            'point': f"{lat},{lon}",
            'unit': 'KMPH'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            flow_data = data.get('flowSegmentData', {})
            
            current_speed = flow_data.get('currentSpeed', 0)
            free_flow_speed = flow_data.get('freeFlowSpeed', 60)
            confidence = flow_data.get('confidence', 0.5)
            
            # Calculate congestion level
            if free_flow_speed > 0:
                speed_ratio = current_speed / free_flow_speed
            else:
                speed_ratio = 1.0
            
            # Classify traffic based on speed ratio
            if speed_ratio >= 0.8:
                traffic_level = "Low"
            elif speed_ratio >= 0.5:
                traffic_level = "Medium"
            else:
                traffic_level = "High"
            
            return {
                'traffic_level': traffic_level,
                'current_speed': round(current_speed, 1),
                'free_flow_speed': round(free_flow_speed, 1),
                'congestion_ratio': round((1 - speed_ratio) * 100, 1),
                'confidence': round(confidence, 2),
                'source': 'tomtom_live'
            }
        elif response.status_code == 403:
            print(f"⚠ TomTom API: Invalid or expired API key")
            return None
        else:
            print(f"⚠ TomTom API returned status {response.status_code}")
            return None
    
    except requests.exceptions.Timeout:
        print(f"⚠ TomTom API timeout")
        return None
    except requests.exceptions.RequestException as e:
        print(f"⚠ Traffic API request error: {e}")
        return None
    except Exception as e:
        print(f"⚠ Traffic API error: {e}")
        return None

def get_heuristic_traffic(zone_name: str) -> Dict:
    """
    Fallback: Use historical traffic patterns and time of day
    """
    # High traffic zones during peak hours
    high_traffic_zones = [
        'Silk Board', 'Hebbal', 'Marathahalli', 'Whitefield', 
        'HSR Layout', 'Koramangala', 'Indiranagar', 'BTM Layout'
    ]
    
    # Medium traffic zones
    medium_traffic_zones = [
        'Electronic City', 'Jayanagar', 'Banashankari', 
        'Peenya', 'Rajajinagar', 'Malleshwaram', 'Yelahanka'
    ]
    
    current_hour = datetime.now().hour
    is_peak_hour = (7 <= current_hour <= 10) or (17 <= current_hour <= 20)
    
    if zone_name in high_traffic_zones:
        traffic_level = "High" if is_peak_hour else "Medium"
        congestion = random.randint(65, 85) if is_peak_hour else random.randint(40, 60)
    elif zone_name in medium_traffic_zones:
        traffic_level = "Medium" if is_peak_hour else "Low"
        congestion = random.randint(40, 60) if is_peak_hour else random.randint(15, 35)
    else:
        traffic_level = "Low"
        congestion = random.randint(10, 25)
    
    # Add some realistic speed variations
    if traffic_level == "High":
        current_speed = random.uniform(15, 25)
    elif traffic_level == "Medium":
        current_speed = random.uniform(25, 40)
    else:
        current_speed = random.uniform(40, 55)
    
    return {
        'traffic_level': traffic_level,
        'current_speed': round(current_speed, 1),
        'free_flow_speed': 60,
        'congestion_ratio': congestion,
        'source': 'heuristic_time_based',
        'is_peak_hour': is_peak_hour
    }

def fetch_zone_traffic_live(zones: List[Dict]) -> List[Dict]:
    """
    Fetch live traffic data for all zones
    Falls back to heuristic if API fails
    """
    print("🚦 Fetching live traffic data...")
    
    zones_with_traffic = []
    api_success_count = 0
    
    for zone in zones:
        center = zone.get('center', [12.9716, 77.5946])
        
        # Try TomTom API
        traffic_data = get_tomtom_traffic(center[0], center[1])
        
        # Fallback to heuristic if API fails
        if not traffic_data:
            traffic_data = get_heuristic_traffic(zone['name'])
        else:
            api_success_count += 1
        
        zone_copy = zone.copy()
        zone_copy['traffic'] = traffic_data['traffic_level']
        zone_copy['traffic_data'] = traffic_data
        zones_with_traffic.append(zone_copy)
        
        source_icon = "🌐" if traffic_data['source'] == 'tomtom_live' else "🕐"
        print(f"  {source_icon} {zone['name']}: {traffic_data['traffic_level']} traffic ({traffic_data['congestion_ratio']:.0f}% congestion)")
    
    if api_success_count > 0:
        print(f"\n✓ Traffic data fetched: {api_success_count} live, {len(zones) - api_success_count} heuristic")
    else:
        print(f"\n✓ Traffic data fetched: All heuristic (API key not configured or unavailable)")
    
    return zones_with_traffic

if __name__ == "__main__":
    # Test traffic service
    print("Testing TomTom Traffic Service...\n")
    
    if not TOMTOM_API_KEY:
        print("⚠ TOMTOM_API_KEY environment variable not set")
        print("Using heuristic fallback mode\n")
    
    # Test Silk Board (notorious traffic hotspot)
    test_locations = [
        {'name': 'Silk Board', 'center': [12.9180, 77.6229]},
        {'name': 'Hebbal Flyover', 'center': [13.0358, 77.5970]},
        {'name': 'Whitefield', 'center': [12.9698, 77.7499]}
    ]
    
    for location in test_locations:
        print(f"Testing: {location['name']}")
        traffic = get_tomtom_traffic(location['center'][0], location['center'][1])
        
        if traffic and traffic['source'] == 'tomtom_live':
            print(f"  ✓ Live data:")
            print(f"    Traffic Level: {traffic['traffic_level']}")
            print(f"    Current Speed: {traffic['current_speed']} km/h")
            print(f"    Free Flow: {traffic['free_flow_speed']} km/h")
            print(f"    Congestion: {traffic['congestion_ratio']}%")
        else:
            print(f"  ⚠ Using heuristic fallback")
            traffic = get_heuristic_traffic(location['name'])
            print(f"    Traffic Level: {traffic['traffic_level']}")
            print(f"    Congestion: {traffic['congestion_ratio']}%")
        print()