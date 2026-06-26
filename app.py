import streamlit as st
import requests
from datetime import datetime
import os
import google.generativeai as genai

st.title("🌿 EcoBot — Air Quality Monitor")
st.write("Real-time AQI checker — Powered by WAQI API + Gemini AI")

# API Keys
waqi_key = os.getenv("WAQI_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

# Gemini setup
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# City selector
city = st.selectbox("City chuno:", ["jaipur", "delhi", "agra", "mumbai"])

# AQI fetch
url = f"https://api.waqi.info/feed/{city}/?token={waqi_key}"
response = requests.get(url)
data = response.json()

aqi = data['data']['aqi']
last_updated = data['data']['time']['s']

# AQI display
st.metric(label=f"{city.upper()} AQI", value=aqi)
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

# Gemini Chatbot
st.divider()
st.subheader("🤖 EcoBot AI Assistant")
st.write("AQI ke baare mein kuch bhi poochho!")

user_question = st.text_input("Apna sawaal likho:")

if user_question:
    with st.spinner("EcoBot soch raha hai..."):
        prompt = f"""
        Jaipur/India ka current AQI {aqi} hai ({city} city).
        User ka sawaal: {user_question}
        
        Hindi mein short aur helpful jawab do — health advice focus karo.
        """
        reply = model.generate_content(prompt)
        st.success(f"🤖 EcoBot: {reply.text}")
