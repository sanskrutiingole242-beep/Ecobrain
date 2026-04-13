import streamlit as st
import pandas as pd
import requests
import sqlite3
import hashlib
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np
from google import genai
from air_quality_map import show_india_map

# =========================
# SESSION INIT (IMPORTANT FIX)
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
# //////////////////////////now
if "has_anomaly" not in st.session_state:
    st.session_state.has_anomaly = False

if "latest_aqi" not in st.session_state:
    st.session_state.latest_aqi = 0
    # ////
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    # ///////////
if "user" not in st.session_state:
    st.session_state.user = ""

# =========================
# UI STYLE (NEXT LEVEL)
# =========================
st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at top, #0f172a, #020617);
    color: #e2e8f0;
}

.glass-panel {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(18px);
    border-radius: 16px;
    padding: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 10px 40px rgba(0,0,0,0.6);
    transition: 0.3s;
}

.glass-panel:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 50px rgba(0,255,170,0.15);
}

h2,h3,h4 {
    color: #38bdf8;
}

.block-container {
    padding-top: 1.2rem;
}

.stButton button {
    background: linear-gradient(135deg, #3B82F6, #00ffaa) !important;
    color: white !important;
    border-radius: 8px;
    font-weight: 600;
}
            
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.03); }
    100% { transform: scale(1); }
}

</style>
""", unsafe_allow_html=True)

# =========================
# DATABASE
# =========================
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)")
    conn.commit()
    conn.close()

def hash_pw(p): return hashlib.sha256(p.encode()).hexdigest()

def add_user(u, p):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users VALUES (?,?)", (u, hash_pw(p)))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(u, p):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (u, hash_pw(p)))
    data = c.fetchone()
    conn.close()
    return data

init_db()

# =========================
# API
# =========================
def fetch_live_aqi(city):
    try:
        token = st.secrets["WAQI_TOKEN"]
        url = f"https://api.waqi.info/feed/{city}/?token={token}"
        res = requests.get(url).json()
        if res["status"] == "ok":
            d = res["data"]
            forecast = d.get("forecast", {}).get("daily", {}).get("pm25", [])
            return d, forecast
    except:
        return None, None
    return None, None


def ask_ai(prompt):
    prompt = prompt.lower()

    if "aqi" in prompt:
        return f"AQI is {st.session_state.latest_aqi}. Stay careful if above 100."

    elif "safe" in prompt or "health" in prompt:
        v = st.session_state.latest_aqi
        if v < 50:
            return "Air is GOOD 😊 Safe for outdoor activity."
        elif v < 100:
            return "Moderate air 😐 Sensitive people should be careful."
        else:
            return "Poor air 😷 Avoid outdoor activity."

    elif "pollution" in prompt:
        return f"Current pollution level is {st.session_state.latest_aqi}."

    else:
        return "Ask me about AQI, pollution, or health impact."
# =========================
# LOGIN PAGE
# =========================
if not st.session_state.logged_in:

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.markdown("""
        <div class="glass-panel" style="margin-top:80px; text-align:center;">
            <h2>🌍 EcoBrain</h2>
            <p style="color:#94a3b8;">AI Environmental Command System</p>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            u = st.text_input("User ID")
            p = st.text_input("Password", type="password")

            if st.button("Login"):
                if login_user(u, p):
                    st.session_state.logged_in = True
                    st.session_state.user = u
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        with tab2:
            nu = st.text_input("New ID")
            np = st.text_input("New Password", type="password")

            if st.button("Create Account"):
                if add_user(nu, np):
                    st.success("Account created!")
                else:
                    st.error("User exists")

# =========================
# DASHBOARD
# =========================
else:

    # SIDEBAR
    with st.sidebar:
        st.markdown(f"## 👨‍🚀 {st.session_state.user}")
        page = st.radio("Navigation", ["Dashboard", "Analytics", "AI Insight"])

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    # HEADER
    st.markdown("""
    <div class="glass-panel">
        <h2>🌍 EcoBrain Command Center</h2>
        <p style="color:#94a3b8;">Real-time Environmental Intelligence Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    # INPUTS
    cities = ["Mumbai", "Delhi", "Bengaluru", "Chennai", "Hyderabad", "Kolkata", "Pune", "Nagpur"]
    pollutants = ["PM2.5", "PM10", "NO2", "CO", "SO2", "O3"]

    c1, c2, c3 = st.columns([1.5,1.5,3])

    with c1:
        city = st.selectbox("City", cities)

    with c2:
        pol = st.selectbox("Pollutant", pollutants)

    data, forecast = fetch_live_aqi(city)

    if data:

        iaqi = data.get("iaqi", {})
        map_key = {"PM2.5":"pm25","PM10":"pm10","NO2":"no2","CO":"co","SO2":"so2","O3":"o3"}

        value = iaqi.get(map_key[pol], {}).get("v", 0)

        st.markdown(f"""
        <div class="glass-panel" style="text-align:center;">
            <h3>🌍 Live Environmental Status</h3>
            <h2 style="color:#00ffaa;">{city} • AQI {value}</h2>
            <p style="color:#94a3b8;">
                {'🟢 Safe' if value < 50 else '🟡 Moderate' if value < 100 else '🔴 Unhealthy'} •
            AI Monitoring Active
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.session_state.latest_aqi = value


        st.markdown(f"""
        <div class="glass-panel">
            <h4>🧠 AI Insight</h4>
        <p>
            {city} air quality is currently {value}.<br>
            {'Good for outdoor activities.' if value < 50 else
            'Moderate caution required.' if value < 100 else
            'High pollution risk. Avoid outdoor exposure.'}
        </p>
    </div>
    """, unsafe_allow_html=True)

        # SIMPLE REAL-TIME ALERT LOGIC
        if value > 150:
            st.session_state.has_anomaly = True
        else:
            st.session_state.has_anomaly = False
        # //////////////////////////////now
        st.session_state.latest_aqi = value

        # KPI CARDS
        k1,k2,k3,k4 = st.columns(4)


        risk_score = min(100, int(value * 0.8))

        st.markdown(f"""
        <div class="glass-panel">
            <h4>⚠️ City Risk Score</h4>
            <h2 style="color:#ff4d4d;">{risk_score}/100</h2>
            <p>Higher score = higher health risk</p>
        </div>
        """, unsafe_allow_html=True)


        # ////////////////////////////////////////now
        if st.session_state.has_anomaly:
            st.markdown("""
            <div style="
                background: rgba(255,0,0,0.12);
                border: 1px solid #ff4d4d;
                padding: 14px;
                border-radius: 12px;
                color: #ff4d4d;
                font-weight: bold;
            ">
            🚨 ALERT: Sudden Pollution Spike Detected
            </div>
            """, unsafe_allow_html=True)


        k1.metric("Sensor Value", value)
        k2.metric("Status", "Good" if value<50 else "Moderate" if value<100 else "Poor")
        k3.metric("City", city)
        k4.metric("Mode", "Live")

        

        # MAP
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        show_india_map(pol)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("### 📊 Live City AQI Comparison")

        cities = ["Mumbai", "Delhi", "Bengaluru", "Chennai", "Hyderabad", "Kolkata", "Pune", "Nagpur"]

        aqi_values = []

        for c in cities:
            try:
                url = f"https://api.waqi.info/feed/{c}/?token={st.secrets['WAQI_TOKEN']}"
                res = requests.get(url).json()

                if res["status"] == "ok":
                    aqi_values.append(res["data"]["aqi"])
                else:
                    aqi_values.append(0)

            except:
                aqi_values.append(0)

        compare_df = pd.DataFrame({
            "City": cities,
            "AQI": aqi_values
        })

        st.bar_chart(compare_df.set_index("City"))

        # =========================
        # DASHBOARD PAGE
        # =========================
        if page == "Dashboard":

            st.markdown("### 📊 Live Monitoring")

        # =========================
        # ANALYTICS
        # =========================
        elif page == "Analytics" and forecast:

            df = pd.DataFrame(forecast)
            df["day"] = pd.to_datetime(df["day"])

            df["z_score"] = (df["avg"] - df["avg"].mean()) / df["avg"].std()
            df["anomaly"] = df["z_score"].abs() > 2

            st.session_state.has_anomaly = df["anomaly"].any()
            # import numpy as np

            # df["z_score"] = (df["avg"] - df["avg"].mean()) / df["avg"].std()
            # df["anomaly"] = df["z_score"].abs() > 2

            # has_anomaly = df["anomaly"].any()

            col1, col2 = st.columns(2)

            with col1:
                st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
                st.subheader("7-Day Trend")
                st.line_chart(df.set_index("day")["avg"])
                st.markdown("</div>", unsafe_allow_html=True)

            from prophet import Prophet

            with col2:
                st.markdown('<div class="glass-panel">', unsafe_allow_html=True)

                st.subheader("🧠 AI Forecast (Prophet Model)")

                # Prepare data for Prophet
                df_prophet = df[['day', 'avg']].copy()
                df_prophet.columns = ['ds', 'y']

                # Train model
                model = Prophet(
                    daily_seasonality=False,
                    weekly_seasonality=True,
                    yearly_seasonality=True
                )

                model.fit(df_prophet)

                # Future dates (5 days ahead)
                future = model.make_future_dataframe(periods=5)
                forecast = model.predict(future)

                # Plot results
                fig = go.Figure()

                # Actual
                fig.add_trace(go.Scatter(
                x=df_prophet['ds'],
                y=df_prophet['y'],
                name="Actual",
                line=dict(color="#1b6fce", width=3)
                ))

                # Forecast line
                fig.add_trace(go.Scatter(
                    x=forecast['ds'],
                    y=forecast['yhat'],
                    name="Forecast",
                    line=dict(color="#00ffaa", width=3)
                ))

                # Upper confidence
                fig.add_trace(go.Scatter(
                    x=forecast['ds'],
                    y=forecast['yhat_upper'],
                    fill=None,
                    mode="lines",
                    line=dict(width=0),
                    showlegend=False
                ))

                # Lower confidence (fill area)
                fig.add_trace(go.Scatter(
                    x=forecast['ds'],
                    y=forecast['yhat_lower'],
                    fill='tonexty',
                    mode="lines",
                    line=dict(width=0),
                    name="Confidence Range",
                    fillcolor="rgba(0,255,170,0.1)"
                ))

                fig.update_layout(
                    template="plotly_dark",
                    height=350,
                margin=dict(l=0, r=0, t=20, b=0),
                hovermode="x unified"
                )

                st.plotly_chart(fig, use_container_width=True)

                st.markdown('</div>', unsafe_allow_html=True)



        # =========================
        # AI INSIGHT
        # =========================
        # =========================

        elif page == "AI Insight":

            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            st.subheader("🧠 EcoBrain AI Assistant")

        # show history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_input = st.chat_input("Ask about air quality...")

        if user_input:

            st.session_state.chat_history.append({"role": "user", "content": user_input})

            with st.chat_message("user"):
                st.markdown(user_input)

            # AI RESPONSE (SAFE + FAST)
            try:
                context = f"City: {city}, AQI: {st.session_state.latest_aqi}, Question: {user_input}"
                ai_reply = ask_ai(context)

            except:
                ai_reply = "⚠️ AI error, using fallback response."

            st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})

            with st.chat_message("assistant"):
                st.markdown(ai_reply)

        st.markdown('</div>', unsafe_allow_html=True)