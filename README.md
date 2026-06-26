# 🌿 EcoBot — AI-Powered Air Quality Monitor

A live AI-powered real-time Air Quality Index (AQI) monitoring web app for Indian cities.

## 🚀 Live Demo
👉 [Click here to open EcoBot](https://ecobot-aqi-monitor-1.streamlit.app)

## 🤖 Features
- Real-time AQI data for Indian cities (Jaipur, Delhi, Agra, Mumbai)
- Smart health recommendations based on AQI levels
- AI Chatbot — ask anything about air quality in Hindi
- Data freshness indicator — warns if sensor data is outdated
- City selector dropdown

## 🛠️ Tech Stack
| Tool | Use |
|------|-----|
| Python | Core language |
| Streamlit | Web app frontend |
| WAQI API | Real-time AQI data |
| Groq API (Llama 3.3) | AI chatbot responses |
| Streamlit Cloud | Deployment |
| GitHub | Version control |

## 📊 AQI Scale
| AQI Range | Status |
|-----------|--------|
| 0-50 | Good ✅ |
| 51-100 | Moderate 🟡 |
| 101-150 | Unhealthy 🟠 |
| 150+ | Dangerous 🔴 |

## ⚙️ Setup
1. Clone this repo
2. Install: `pip install streamlit requests groq`
3. Set your API keys (WAQI + Groq)
4. Run: `streamlit run app.py`

## 👨‍💻 Developer
Tanishque Agrawal
B.Tech AI & Data Science — Arya College, Jaipur
