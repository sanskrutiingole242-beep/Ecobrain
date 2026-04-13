import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static 
import os

def show_india_map(selected_pollutant):
    # --- 1. SMART PATH SETUP (THE FIX) ---
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define possible places where the file might be
    paths_to_check = [
        os.path.join(current_dir, "city_day.csv"),          # Right next to this file
        os.path.join(current_dir, "data", "city_day.csv"),   # In a subfolder called data
        os.path.join(os.path.dirname(current_dir), "data", "city_day.csv") # Root data folder
    ]
    
    city_day_path = None
    for path in paths_to_check:
        if os.path.exists(path):
            city_day_path = path
            break
            
    if city_day_path is None:
        st.error("📍 Map Error: 'city_day.csv' not found. Please place it in the same folder as app.py")
        return

    # 2. COORDINATES
    city_coords = {
        "Delhi": [28.61, 77.21], "Mumbai": [19.07, 72.87], "Bengaluru": [12.97, 77.59],
        "Chennai": [13.08, 80.27], "Hyderabad": [17.38, 78.48], "Kolkata": [22.57, 88.36],
        "Ahmedabad": [23.02, 72.57], "Jaipur": [26.91, 75.78], "Lucknow": [26.84, 80.94],
        "Patna": [25.59, 85.13], "Bhopal": [23.25, 77.41], "Gurugram": [28.45, 77.02],
        "Visakhapatnam": [17.68, 83.21], "Amritsar": [31.63, 74.87], "Kanpur": [26.44, 80.33]
    }

    try:
        # 3. LOAD DATA
        df = pd.read_csv(city_day_path)
        df['lat'] = df['City'].map(lambda x: city_coords.get(x, [None, None])[0])
        df['lon'] = df['City'].map(lambda x: city_coords.get(x, [None, None])[1])
        
        map_df = df.dropna(subset=['lat', 'lon', selected_pollutant])
        latest_df = map_df.sort_values('Date').groupby('City').last().reset_index()

        # 4. CREATE MAP
        m = folium.Map(location=[20.59, 78.96], zoom_start=5, tiles="CartoDB dark_matter")

        # 5. ADD DOTS
        for _, row in latest_df.iterrows():
            val = row[selected_pollutant]
            c = '#00ff44' if val <= 50 else '#ffaa00' if val <= 100 else '#ff4444'
            
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=10,
                color='white',
                weight=2,
                fill=True,
                fill_color=c,
                fill_opacity=0.9,
                popup=f"{row['City']}: {val}"
            ).add_to(m)

        # 6. RENDER
        # --- RENDER (FORCED LARGE) ---
        # width=1200 or 1400 ensures it fills the dashboard width
        # height=500 or 600 makes it tall enough to see clearly
        folium_static(m, width=1300, height=550)

    except Exception as e:
        st.error(f"Map Logic Error: {e}")

if __name__ == "__main__":
    show_india_map('PM2.5')