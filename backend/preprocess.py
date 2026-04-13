import pandas as pd

def load_data():
    
    df = pd.read_csv("data/city_day.csv")
    
    df['Date'] = pd.to_datetime(df['Date'])
    
    df = df[['Date', 'City', 'PM2.5', 'PM10', 'NO2']]
    
    df.columns = ['date', 'city', 'PM2.5', 'PM10', 'NO2']
    
    df = df.dropna()
    
    # 🔥 IMPORTANT: group by day
    df = df.groupby(['date', 'city']).mean().reset_index()
    
    return df
