import streamlit as st
import requests
from datetime import datetime
import os
from groq import Groq
import plotly.graph_objects as go

st.set_page_config(page_title="EcoBot", page_icon="🌿", layout="wide")

st.title("🌿 EcoBot — Air Quality Monitor")
st.write("Real-time AQI checker — Powered by WAQI API + AI")

waqi_key = os.getenv("WAQI_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_key)

city = st.selectbox("City chuno:", ["jaipur", "delhi", "agra", "mumbai"])

url = f"https://api.waqi.info/feed/{city}/?token={waqi_key}"
response = requests.get(url)
data = response.json()

aqi = data['data']['aqi']
last_updated = data['data']['time']['s']

# Temperature aur Humidity
iaqi = data['data'].get('iaqi', {})
temp = round(iaqi.get('t', {}).get('v', 0), 1)
humidity = round(iaqi.get('h', {}).get('v', 0), 1)
wind = round(iaqi.get('w', {}).get('v', 0), 2)
# Top metrics row
col1, col2, col3, col4 = st.columns(4)
col1.metric("🌫️ AQI", aqi)
col2.metric("🌡️ Temperature", f"{temp}°C" if temp != 'N/A' else "N/A")
col3.metric("💧 Humidity", f"{humidity}%" if humidity != 'N/A' else "N/A")
col4.metric("💨 Wind", f"{wind} m/s" if wind != 'N/A' else "N/A")

st.caption(f"🕐 Last updated: {last_updated}")

# Stale data check
update_time = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S")
hours_old = (datetime.now() - update_time).total_seconds() / 3600
if hours_old > 24:
    st.warning(f"⚠️ Data {int(hours_old)} ghante purana hai — sensor offline ho sakta hai!")

# Health advice
if aqi <= 50:
    st.success("✅ Hawa saaf hai! Bahar jaana safe hai.")
elif aqi <= 100:
    st.warning("🟡 Thodi pollution hai. Sensitive log dhyan rakhein.")
elif aqi <= 150:
    st.warning("🟠 Unhealthy hai! Bahar kam niklo.")
else:
    st.error("🔴 DANGER! Ghar pe raho, mask zaroori hai.")

st.divider()

# Two columns — Graph + Map
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 AQI Pollutants Breakdown")
    
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
            marker_color=['#ff6b6b', '#ffa500', '#ffdd57', '#48dbfb', '#ff9ff3', '#54a0ff']
        ))
        fig.update_layout(
            title=f"{city.upper()} Pollutants",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Pollutant data available nahi hai is city ke liye.")

with col_right:
    st.subheader("🗺️ City Location Map")
    
    city_coords = {
        "jaipur": [26.9124, 75.7873],
        "delhi": [28.6139, 77.2090],
        "agra": [27.1767, 78.0081],
        "mumbai": [19.0760, 72.8777]
    }
    
    lat, lon = city_coords[city]
    
    # AQI color
    if aqi <= 50:
        color = "green"
    elif aqi <= 100:
        color = "yellow"
    elif aqi <= 150:
        color = "orange"
    else:
        color = "red"
    
    map_html = f"""
    <iframe
        width="100%"
        height="350"
        frameborder="0"
        src="https://www.openstreetmap.org/export/embed.html?bbox={lon-0.5}%2C{lat-0.5}%2C{lon+0.5}%2C{lat+0.5}&layer=mapnik&marker={lat}%2C{lon}"
        style="border-radius: 10px;">
    </iframe>
    <p style="color: {color}; text-align: center; font-size: 18px;">
        📍 {city.upper()} — AQI: {aqi}
    </p>
    """
    st.components.v1.html(map_html, height=400)

st.divider()

# AI Chatbot
st.subheader("🤖 EcoBot AI Assistant")
st.write("AQI ke baare mein kuch bhi poochho!")

user_question = st.text_input("Apna sawaal likho:")

if user_question:
    with st.spinner("EcoBot soch raha hai..."):
        try:
            prompt = f"Current AQI {aqi} hai {city} mein. Temp: {temp}°C, Humidity: {humidity}%. User ka sawaal: {user_question}. Hindi mein short helpful jawab do."
            reply = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            st.success(f"🤖 EcoBot: {reply.choices[0].message.content}")
        except Exception as e:
            st.error(f"Debug: {str(e)}")
