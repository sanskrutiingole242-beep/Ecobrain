# from backend.preprocess import load_data
# from backend.model import train_trend_model
# from backend.anomaly import detect_anomalies
# from backend.cause_detection import detect_cause
# import requests  # New: To talk to the internet
# import pandas as pd

# import requests # Make sure this is at the top of main.py

# import requests
# import pandas as pd
# from backend.preprocess import load_data
# from backend.model import train_trend_model
# from backend.anomaly import detect_anomalies
# from backend.cause_detection import detect_cause

# # IMPORTANT: Added 'fetch_live=False' inside the parentheses
# def process_data(fetch_live=False):
#     if fetch_live:
#         # 1. Fetch from API
#         TOKEN = "demo" # REPLACE THIS with your real token from aqicn.org later
#         cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Jaipur", "Lucknow", "Pune", "Ahmedabad"]
#         live_list = []
        
#         for c in cities:
#             try:
#                 url = f"https://api.waqi.info/feed/{c}/?token={TOKEN}"
#                 res = requests.get(url).json()
#                 if res['status'] == 'ok':
#                     live_list.append({
#                         "city": c,
#                         "date": res['data']['time']['s'],
#                         "PM2.5": res['data']['iaqi'].get('pm25', {}).get('v', 0)
#                     })
#             except Exception as e:
#                 print(f"Error fetching {c}: {e}")
        
#         df = pd.DataFrame(live_list)
#         if df.empty:
#             df = load_data() # Fallback to CSV if API fails
#     else:
#         # 1. Load from CSV (Original Logic)
#         df = load_data()

#     # 2. Run your existing ML Pipeline
#     # Ensure these functions exist in your backend files!
#     df, model = train_trend_model(df)
#     df = detect_anomalies(df)
    
#     # Initialize cause column
#     df['cause'] = "Normal"
#     mask = df['anomaly'] == -1
#     if mask.any():
#         df.loc[mask, 'cause'] = df[mask].apply(detect_cause, axis=1)

#     # 3. Prepare Outputs for app.py
#     anomalies = df[df['anomaly'] == -1]
    
#     # Simple trend string logic
#     if fetch_live:
#         trend_status = "Real-Time Monitoring"
#     else:
#         trend_status = "Historical Analysis"

#     return df, anomalies, trend_status

#     # --- REST OF YOUR PROCESSING ---
#     # (Keep your existing calls to train_trend_model, detect_anomalies, etc. here)
    
#     # Example (Adjust based on your actual backend functions):
#     # df, model = train_trend_model(df)
#     # df = detect_anomalies(df)
#     # anomalies = df[df['anomaly'] == -1]
#     # trend_status = "Stable" # Or your trend logic
    
#     # FOR NOW, let's ensure it returns what app.py wants:
#     anomalies = df[df.get('anomaly', 0) == -1]
#     trend_status = "Live Data" if fetch_live else "Historical"
    
#     return df, anomalies, trend_status
#     # ... keep the rest of your model training/anomaly detection code here ...
#     # ... return df, anomalies, trend_status
# # This part only runs if you play main.py directly (for testing)
# if __name__ == "__main__":
#     df, anomalies, trend = process_data()
#     print("===== SAMPLE OUTPUT =====")
#     print(df.head())
#     print(f"\nOverall Trend: {trend}")
#     print(f"Total Anomalies Found: {len(anomalies)}")
import pandas as pd
import requests
from backend.preprocess import load_data
from backend.model import train_trend_model
from backend.anomaly import detect_anomalies
from backend.cause_detection import detect_cause

def process_data(fetch_live=False):
    """
    Main backend engine. 
    If fetch_live is True, it hits the WAQI API.
    If fetch_live is False, it loads your local CSV.
    """
    if fetch_live:
        # --- LIVE API LOGIC ---
        # Note: Replace "demo" with your real token from aqicn.org for full India coverage
        TOKEN = "demo" 
        cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Jaipur", "Lucknow", "Pune", "Ahmedabad"]
        live_list = []
        
        for c in cities:
            try:
                url = f"https://api.waqi.info/feed/{c}/?token={TOKEN}"
                res = requests.get(url).json()
                if res['status'] == 'ok':
                    live_list.append({
                        "city": c,
                        "date": res['data']['time']['s'],
                        "PM2.5": res['data']['iaqi'].get('pm25', {}).get('v', 0)
                    })
            except Exception as e:
                print(f"Error fetching {c}: {e}")
        
        df = pd.DataFrame(live_list)
        
        # If API fails or returns nothing, fallback to CSV so the app doesn't crash
        if df.empty:
            df = load_data()
    else:
        # --- LOCAL CSV LOGIC ---
        df = load_data()

    # --- ML PIPELINE (Works for both Live and CSV) ---
    
    # 1. Trend Analysis
    df, model = train_trend_model(df)
    
    # 2. Anomaly Detection
    df = detect_anomalies(df)
    
    # 3. Cause Detection (Only for anomalies)
    df['cause'] = "Normal"
    mask = df['anomaly'] == -1
    if mask.any():
        # Using lambda to ensure 'row' is passed correctly
        df.loc[mask, 'cause'] = df[mask].apply(lambda row: detect_cause(row), axis=1)

    # 4. Prepare Final Variables for Frontend
    anomalies = df[df['anomaly'] == -1]
    
    if fetch_live:
        trend_status = "Live Monitoring Active"
    else:
        # Simple trend calculation for the CSV data
        recent_avg = df['PM2.5'].iloc[-10:].mean()
        past_avg = df['PM2.5'].iloc[-20:-10].mean()
        trend_status = "Increasing 📈" if recent_avg > past_avg else "Decreasing 📉"

    return df, anomalies, trend_status

# For testing main.py independently
if __name__ == "__main__":
    df, anom, trend = process_data(fetch_live=False)
    print("Backend test successful!")
    print(df.head())