import streamlit as st
import requests
from datetime import datetime

st.title("🌿 EcoBot — Air Quality Monitor")
st.write("Real-time AQI checker — Powered by WAQI API")

import os
api_key = os.getenv("WAQI_API_KEY", "your_api_key_here")

# City select karne do user ko
city = st.selectbox("City chuno:", ["jaipur", "delhi", "agra", "mumbai"])

url = f"https://api.waqi.info/feed/{city}/?token={api_key}"
response = requests.get(url)
data = response.json()

aqi = data['data']['aqi']
last_updated = data['data']['time']['s']

# AQI dikhao
st.metric(label=f"{city.upper()} AQI", value=aqi)

# Last update time dikhao
st.caption(f"🕐 Last updated: {last_updated}")

# Check karo data fresh hai ya nahi
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
