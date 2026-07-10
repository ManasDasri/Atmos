# Atmos – Hybrid Air Quality Monitoring

## Overview

Atmos is a Python + FastAPI project that simulates and optimizes air quality sensor placement across the city. The system combines real-time WAQI data, traffic-weighted zone analysis, and optimization algorithms to propose an efficient sensor network that is cheaper and more effective than the existing CAAQMS stations.

**Key features:**
* Fetch live PM2.5 and AQI readings for Bengaluru from WAQI API.
* Generate fallback realistic data if API fails.
* Hybrid model optimization:
  * Bounding Phase Method
  * Golden Ratio Search
* Proportional sensor allocation based on pollution and traffic.
* Interactive web interface (FastAPI + Jinja2 templates):
  * Home map showing sensor coverage and PM2.5 per zone.
  * Compare current government network vs optimized hybrid model.
  * Query AQI per neighborhood.
  * Statistics and zone-wise coverage.
  * Educational info about PM2.5 and air quality safety.

---

## Project Structure

```text
hybrid/
├── backend/
│   ├── __init__.py
│   ├── main.py            # FastAPI server
│   ├── optimize.py        # Hybrid sensor optimization
│   └── waqi_service.py    # WAQI API integration & fallback
│
├── frontend/
│   ├── templates/         # HTML templates
│   └── static/            # CSS/JS assets
│
├── data/                  # Generated hybrid_model.json
├── venv1/                 # Virtual environment
└── README.md
```

---

## Requirements

* Python 3.13+
* FastAPI
* Uvicorn
* Requests
* Numpy

**Install dependencies:**

```bash
source venv1/bin/activate
pip install fastapi uvicorn requests numpy jinja2
```

---

## Setup

1. **Clone the repository to your machine:**
   ```bash
   git clone <repo-url>
   cd hybrid
   ```

2. **Activate virtual environment:**
   ```bash
   source venv1/bin/activate
   ```

3. **Set your WAQI API key:**
   ```bash
   export WAQI_API_KEY="YOUR_API_KEY_HERE"
   ```
   > Get your WAQI token at: https://aqicn.org/data-platform/token/

4. **Ensure `backend/__init__.py` exists (empty is fine).**

---

## Run the Server

```bash
python -m uvicorn backend.main:app --reload
```

* Open your browser at http://127.0.0.1:8000 to access the app.

---

## Testing Imports (Optional)

To verify that imports work correctly:

```bash
python -c "from backend.optimize import optimize_hybrid_model; print('optimize works!')"
python -c "from backend.waqi_service import fetch_live_aqi; print('WAQI works!')"
```

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/model` | GET | Returns current hybrid sensor allocation JSON |
| `/api/waqi/live` | GET | Fetches live AQI data from WAQI |
| `/api/zone/{zone_name}` | GET | Returns data for a specific zone |
| `/api/optimize` | POST | Trigger a new hybrid optimization run |
| `/api/stats` | GET | Returns statistics (total sensors, average AQI, worst/best zone) |

---

## Frontend Pages

* `/` → Home page with interactive map of sensors and PM2.5 per zone.
* `/compare` → Compare hybrid model vs existing 14 CAAQMS stations.
* `/coverage` → Visual representation of sensor coverage.
* `/query` → Input zone name to get live AQI.
* `/info` → PM2.5 explanation, health advice, and safety measures.
* `/contrast` → Compare the worst and best polluted zones.

---

## Notes

* Hybrid model uses mid-grade sensors (~₹30k each) to cover more areas efficiently under a budget of ₹25 lakh.
* Fallback data is generated when WAQI API is unavailable.
* The project is designed as a demonstration/prototype; it is not deployed to production.

---

## Author

**MD** – Engineering student
