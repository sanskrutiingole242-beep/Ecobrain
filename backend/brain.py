import datetime

# This is your 'Filing Cabinet'
seven_day_data = []

def add_pollution_reading(value, location):
    """Adds a new reading and keeps only the last 7 days"""
    now = datetime.datetime.now()
    seven_day_data.append({"time": now, "aqi": value, "loc": location})
    
    # Remove anything older than 7 days (604800 seconds)
    cutoff = now - datetime.timedelta(days=7)
    global seven_day_data
    seven_day_data = [d for d in seven_day_data if d['time'] > cutoff]

def get_chat_summary():
    """Tells the Chatbot exactly what happened this week"""
    if not seven_day_data:
        return "No data yet."
        
    values = [d['aqi'] for d in seven_day_data]
    highest = max(values)
    lowest = min(values)
    avg = sum(values) / len(values)
    
    # This is the 'Simple Fact Sheet' for the Bot
    return {
        "max_pollution": highest,
        "min_pollution": lowest,
        "average": round(avg, 1),
        "status": "Getting Worse" if values[-1] > avg else "Improving"
    }