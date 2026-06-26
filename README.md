# 🌿 EcoBot — AI-Powered Air Quality Monitor

A live AI-powered real-time Air Quality Index (AQI) monitoring 
web app for Indian cities — built from scratch by a B.Tech 
AI & Data Science student.

## 🚀 Live Demo
👉 [Click here to open EcoBot](https://ecobot-aqi-monitor-1.streamlit.app)

## ✨ Features
- 🌫️ Real-time AQI data for Indian cities
- 🌡️ Temperature, Humidity & Wind speed
- 📊 Pollutants breakdown chart (PM2.5, PM10, NO2, SO2, CO, O3)
- 📈 7-day AQI forecast using ML (Linear Regression)
- 🗺️ Interactive city map (OpenStreetMap)
- 🤖 AI Chatbot with conversation history (Groq + Llama 3.3)
- ⚠️ Stale data detection — warns if sensor is offline
- 🏙️ Multi-city support (Jaipur, Delhi, Agra, Mumbai)

## 🛠️ Tech Stack
| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Web app frontend |
| WAQI API | Real-time AQI data |
| Plotly | Interactive charts |
| Scikit-learn | ML AQI prediction |
| NumPy | Data processing |
| Groq API (Llama 3.3-70b) | AI chatbot |
| OpenStreetMap | City map |
| Streamlit Cloud | Deployment |
| GitHub | Version control |

## 📊 AQI Scale
| AQI Range | Category | Action |
|-----------|----------|--------|
| 0-50 | Good ✅ | Safe to go out |
| 51-100 | Moderate 🟡 | Sensitive groups be careful |
| 101-150 | Unhealthy 🟠 | Limit outdoor activity |
| 150+ | Dangerous 🔴 | Stay indoors |

## ⚙️ Local Setup
1. Clone this repo
git clone https://github.com/tanishqueagrawal/Ecobot-aqi-monitor
2. Install dependencies
pip install streamlit requests groq plotly scikit-learn numpy
3. Set API keys in `.env` or directly in code
4. Run the app
streamlit run app.py

## 🔑 API Keys Required
- [WAQI API](https://aqicn.org/data-platform/token/) — Free
- [Groq API](https://console.groq.com) — Free

## 👨‍💻 Developer
**Tanishque Agrawal**
B.Tech AI & Data Science — Arya College of Engineering, Jaipur
🔗 [Credly Profile](https://www.credly.com/users/tanishque-agarwal.267d0757)
