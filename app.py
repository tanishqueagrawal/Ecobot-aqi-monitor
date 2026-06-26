import streamlit as st
import requests
from datetime import datetime
import os
from groq import Groq

st.title("🌿 EcoBot — Air Quality Monitor")
st.write("Real-time AQI checker — Powered by WAQI API + AI")

waqi_key = os.getenv("WAQI_API_KEY", "d222ab8a9905d4afba60a409ccaa662b21f8cdb4")
groq_key = os.getenv("GROQ_API_KEY", "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")

client = Groq(api_key=groq_key)

city = st.selectbox("City chuno:", ["jaipur", "delhi", "agra", "mumbai"])

url = f"https://api.waqi.info/feed/{city}/?token={waqi_key}"
response = requests.get(url)
data = response.json()

aqi = data['data']['aqi']
last_updated = data['data']['time']['s']

st.metric(label=f"{city.upper()} AQI", value=aqi)
st.caption(f"🕐 Last updated: {last_updated}")

update_time = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S")
hours_old = (datetime.now() - update_time).total_seconds() / 3600
if hours_old > 24:
    st.warning(f"⚠️ Data {int(hours_old)} ghante purana hai — sensor offline ho sakta hai!")

if aqi <= 50:
    st.success("✅ Hawa saaf hai! Bahar jaana safe hai.")
elif aqi <= 100:
    st.warning("🟡 Thodi pollution hai. Sensitive log dhyan rakhein.")
elif aqi <= 150:
    st.warning("🟠 Unhealthy hai! Bahar kam niklo.")
else:
    st.error("🔴 DANGER! Ghar pe raho, mask zaroori hai.")

st.divider()
st.subheader("🤖 EcoBot AI Assistant")
st.write("AQI ke baare mein kuch bhi poochho!")

user_question = st.text_input("Apna sawaal likho:")

if user_question:
    with st.spinner("EcoBot soch raha hai..."):
        try:
            prompt = f"Current AQI {aqi} hai {city} mein. User ka sawaal: {user_question}. Hindi mein short helpful jawab do."
            reply = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}]
            )
            st.success(f"🤖 EcoBot: {reply.choices[0].message.content}")
        except Exception as e:
            st.error(f"Debug: {str(e)}")
