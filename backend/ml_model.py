import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
from pathlib import Path
import math

MODEL_PATH = Path(__file__).resolve().parent / "urbanization_model.pkl"

def generate_synthetic_historical_data():
    """
    Generates synthetic historical data mimicking real urban sprawl in Bangalore over the last 10 years.
    Central cores (lat: 12.97, lon: 77.59) grew fast but saturated.
    Outskirts with high traffic (like ORR, Electronic City, Whitefield) are growing rapidly.
    """
    print("🌿 ATMOS - Generating synthetic historical dataset for ML training...")
    np.random.seed(42)
    
    n_samples = 2000
    
    # Bangalore approximate center
    center_lat, center_lon = 12.9716, 77.5946
    
    lats = np.random.uniform(12.78, 13.16, n_samples)
    lons = np.random.uniform(77.46, 77.78, n_samples)
    
    # Features
    distances_to_center = np.sqrt((lats - center_lat)**2 + (lons - center_lon)**2) * 111 # Approx distance in km
    
    historical_population_density = np.where(distances_to_center < 5, 
                                             np.random.uniform(15000, 30000, n_samples), # High core density
                                             np.random.uniform(2000, 10000, n_samples))  # Lower outskirt density
    
    historical_traffic_index = np.where(distances_to_center < 10,
                                        np.random.uniform(0.6, 1.0, n_samples),
                                        np.random.uniform(0.1, 0.7, n_samples))
    
    historical_pm25_trend = np.random.uniform(-0.5, 2.5, n_samples) # Annual PM2.5 growth %
    
    # Target Variable: Urbanization Growth Rate (0 to 1)
    # The hypothesis: Mid-distance areas (5-15km) with high traffic grow the fastest. Cores are saturated.
    urbanization_rate = np.zeros(n_samples)
    for i in range(n_samples):
        d = distances_to_center[i]
        t = historical_traffic_index[i]
        p = historical_population_density[i]
        
        if d < 4:
            # Saturated core
            growth = 0.1 + np.random.uniform(0, 0.1)
        elif 4 <= d <= 15:
            # Rapid sprawl zone, depends heavily on traffic/connectivity
            growth = 0.4 + (t * 0.4) + np.random.uniform(0, 0.2)
        else:
            # Far outskirts
            growth = 0.1 + (t * 0.3) + np.random.uniform(0, 0.1)
            
        urbanization_rate[i] = min(max(growth, 0.0), 1.0)
        
    df = pd.DataFrame({
        'lat': lats,
        'lon': lons,
        'distance_to_center': distances_to_center,
        'historical_pop_density': historical_population_density,
        'historical_traffic_index': historical_traffic_index,
        'historical_pm25_trend': historical_pm25_trend,
        'urbanization_rate': urbanization_rate
    })
    
    return df

def train_model():
    df = generate_synthetic_historical_data()
    
    X = df[['distance_to_center', 'historical_pop_density', 'historical_traffic_index', 'historical_pm25_trend']]
    y = df['urbanization_rate']
    
    print("🌿 ATMOS - Training Random Forest Regressor on historical data...")
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X, y)
    
    joblib.dump(model, MODEL_PATH)
    print(f"🌿 ATMOS - ML Model successfully trained and saved to {MODEL_PATH}")
    return model

_CACHED_MODEL = None

def load_or_train_model():
    global _CACHED_MODEL
    if _CACHED_MODEL is not None:
        return _CACHED_MODEL
        
    if not MODEL_PATH.exists():
        _CACHED_MODEL = train_model()
    else:
        _CACHED_MODEL = joblib.load(MODEL_PATH)
        
    return _CACHED_MODEL

def predict_urbanization(lat, lon, pop_density, traffic_index, pm25_trend=1.0):
    """
    Predicts the future urbanization potential (0.0 to 1.0) for a specific coordinate.
    """
    model = load_or_train_model()
    
    center_lat, center_lon = 12.9716, 77.5946
    distance = math.sqrt((lat - center_lat)**2 + (lon - center_lon)**2) * 111
    
    X_pred = pd.DataFrame({
        'distance_to_center': [distance],
        'historical_pop_density': [pop_density],
        'historical_traffic_index': [traffic_index],
        'historical_pm25_trend': [pm25_trend]
    })
    
    score = model.predict(X_pred)[0]
    return score

if __name__ == "__main__":
    train_model()
