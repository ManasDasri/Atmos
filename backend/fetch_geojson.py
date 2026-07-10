import requests
import json
from pathlib import Path

def fetch_bangalore_boundary():
    print("Fetching Bangalore BBMP Boundary from datameet github...")
    url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/bangalore.geojson"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        geojson = response.json()
        print("Successfully fetched from github.")
    except Exception as e:
        print(f"Error fetching: {e}. Using fallback square.")
        coordinates = [
            [77.45, 12.85],
            [77.75, 12.85],
            [77.75, 13.15],
            [77.45, 13.15],
            [77.45, 12.85]
        ]
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Bengaluru",
                        "type": "city_boundary"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [coordinates]
                    }
                }
            ]
        }
    
    output_dir = Path(__file__).resolve().parent.parent / "frontend" / "static"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "bangalore.geojson"
    
    with open(output_file, "w") as f:
        json.dump(geojson, f)
        
    print(f"Successfully saved boundary to {output_file}")

if __name__ == "__main__":
    fetch_bangalore_boundary()
