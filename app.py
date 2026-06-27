import streamlit as st
import requests
from datetime import datetime, timedelta
import os
from groq import Groq
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="EcoBot", page_icon="🌿", layout="wide")

st.title("🌿 EcoBot — Air Quality Monitor")
st.write("Real-time AQI checker — Powered by WAQI API + AI + ML")

waqi_key = os.getenv("WAQI_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_key)

city = st.selectbox("City chuno:", ["jaipur", "delhi", "agra", "mumbai"])

url = f"https://api.waqi.info/feed/{city}/?token={waqi_key}"
response = requests.get(url)
data = response.json()

aqi = data['data']['aqi']
last_updated = data['data']['time']['s']

iaqi = data['data'].get('iaqi', {})
temp = round(iaqi.get('t', {}).get('v', 0), 1)
humidity = round(iaqi.get('h', {}).get('v', 0), 1)
wind = round(iaqi.get('w', {}).get('v', 0), 2)

# Top metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("🌫️ AQI", aqi)
col2.metric("🌡️ Temp", f"{temp}°C")
col3.metric("💧 Humidity", f"{humidity}%")
col4.metric("💨 Wind", f"{wind} m/s")

st.caption(f"🕐 Last updated: {last_updated}")

update_time = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S")
hours_old = (datetime.now() - update_time).total_seconds() / 3600
if hours_old > 24:
    st.warning(f"⚠️ AQI Data {int(hours_old)} ghante purana hai — sensor offline ho sakta hai!")

if aqi <= 50:
    st.success("✅ Hawa saaf hai! Bahar jaana safe hai.")
elif aqi <= 100:
    st.warning("🟡 Thodi pollution hai. Sensitive log dhyan rakhein.")
elif aqi <= 150:
    st.warning("🟠 Unhealthy hai! Bahar kam niklo.")
else:
    st.error("🔴 DANGER! Ghar pe raho, mask zaroori hai.")

st.divider()

# Three columns
col_left, col_mid, col_right = st.columns(3)

with col_left:
    st.subheader("📊 Pollutants Breakdown")
    pollutants = {
        'PM2.5': iaqi.get('pm25', {}).get('v', 0),
        'PM10': iaqi.get('pm10', {}).get('v', 0),
        'NO2': iaqi.get('no2', {}).get('v', 0),
        'SO2': iaqi.get('so2', {}).get('v', 0),
        'CO': iaqi.get('co', {}).get('v', 0),
        'O3': iaqi.get('o3', {}).get('v', 0),
    }
    pollutants = {k: v for k, v in pollutants.items() if v != 0}
    if pollutants:
        fig = go.Figure(go.Bar(
            x=list(pollutants.keys()),
            y=list(pollutants.values()),
            marker_color=['#ff6b6b','#ffa500','#ffdd57','#48dbfb','#ff9ff3','#54a0ff']
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white', height=300
        )
        st.plotly_chart(fig, use_container_width=True)

with col_mid:
    st.subheader("📈 ML AQI Forecast")
    
    # Simulate 30 days historical data based on current AQI
    np.random.seed(42)
    days = np.arange(30)
    noise = np.random.normal(0, 10, 30)
    historical_aqi = np.clip(aqi + noise - days * 0.2, 50, 300)
    
    # Features: day number, temp, humidity
    X = np.column_stack([
        days,
        np.random.normal(temp, 2, 30),
        np.random.normal(humidity, 5, 30)
    ])
    y = historical_aqi
    
    # Train model
    model_ml = LinearRegression()
    model_ml.fit(X, y)
    
    # Predict next 7 days
    future_days = np.arange(30, 37)
    future_X = np.column_stack([
        future_days,
        np.random.normal(temp, 2, 7),
        np.random.normal(humidity, 5, 7)
    ])
    predictions = model_ml.predict(future_X)
    predictions = np.clip(predictions, 30, 300).astype(int)
    
    # Plot
    future_dates = [(datetime.now() + timedelta(days=i)).strftime("%d %b") for i in range(1, 8)]
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=future_dates, y=predictions,
        mode='lines+markers',
        line=dict(color='#54a0ff', width=2),
        marker=dict(size=8),
        name='Predicted AQI'
    ))
    fig2.add_hline(y=100, line_dash="dash", line_color="yellow", annotation_text="Moderate")
    fig2.add_hline(y=150, line_dash="dash", line_color="orange", annotation_text="Unhealthy")
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white', height=300,
        yaxis_title="AQI"
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption(f"🔮 Kal predicted AQI: **{predictions[0]}**")

with col_right:
    st.subheader("🗺️ City Map")
    city_coords = {
        "jaipur": [26.9124, 75.7873],
        "delhi": [28.6139, 77.2090],
        "agra": [27.1767, 78.0081],
        "mumbai": [19.0760, 72.8777]
    }
    lat, lon = city_coords[city]
    map_html = f"""
    <iframe width="100%" height="280" frameborder="0"
        src="https://www.openstreetmap.org/export/embed.html?bbox={lon-0.3}%2C{lat-0.3}%2C{lon+0.3}%2C{lat+0.3}&layer=mapnik&marker={lat}%2C{lon}"
        style="border-radius: 10px;">
    </iframe>
    <p style="color: orange; text-align: center;">📍 {city.upper()} — AQI: {aqi}</p>
    """
    st.components.v1.html(map_html, height=320)

st.divider()

# AI Chatbot with History
st.subheader("🤖 EcoBot AI Assistant")
st.write("AQI ke baare mein kuch bhi poochho!")

# Chat history initialize
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani history dikhao
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# New question
user_question = st.chat_input("Apna sawaal likho...")

if user_question:
    # User message add karo
    st.session_state.messages.append({"role": "user", "content": user_question})
    st.chat_message("user").write(user_question)

    with st.spinner("EcoBot soch raha hai..."):
        try:
            # Poori history bhejo Groq ko
            chat_history = [
                {"role": "system", "content": f"Tu EcoBot hai — ek helpful air quality assistant. Current AQI {aqi} hai {city} mein. Temp: {temp}°C, Humidity: {humidity}%. Kal predicted AQI: {predictions[0]}. Hindi mein jawab do."}
            ] + st.session_state.messages

            reply = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=chat_history
            )
            bot_reply = reply.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            st.chat_message("assistant").write(bot_reply)

        except Exception as e:
            st.error(f"Debug: {str(e)}")

# History clear button
if st.session_state.messages:
    if st.button("🗑️ Chat clear karo"):
        st.session_state.messages = []
        st.rerun()
