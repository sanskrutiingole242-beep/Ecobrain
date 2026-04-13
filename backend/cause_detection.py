from backend.festival_data import festival_dates

def get_festival(date):
    for fest, dates in festival_dates.items():
        if str(date)[:10] in dates:
            return fest
    return None

def detect_cause(row):

    fest = get_festival(row['date'])

    if fest and row['PM2.5'] > 150:
        return f"Festival Impact ({fest}) 🎆"

    elif row['NO2'] > 80:
        return "Traffic Pollution 🚗"

    elif row['PM10'] > 200:
        return "Dust / Construction 🏗️"

    else:
        return "Normal"
