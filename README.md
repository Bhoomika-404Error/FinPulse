# ⚡ FinPulse — Zorvyn Market Intelligence Dashboard

> A real-time fintech analytics dashboard built with Python, Streamlit & Plotly.

![Python](https://img.shields.io/badge/Python-3.10+-00d4ff?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-ff3b6b?style=flat-square&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-00ff88?style=flat-square&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-f0c040?style=flat-square)

---

## 🔥 Live Demo

👉 **[View Live Dashboard →](your-streamlit-app-url-here)**

---

## 📊 Features

| Feature | Description |
|---|---|
| 📈 **Live Price Charts** | 30-day BTC & ETH price history with area charts |
| 🌍 **Global Market KPIs** | Total market cap, volume, BTC dominance, active assets |
| 📻 **Live Ticker Tape** | Auto-scrolling real-time price ticker for top 10 assets |
| 😨 **Fear & Greed Index** | 14-day sentiment bar chart with color-coded zones |
| 🍩 **Market Dominance** | Interactive donut chart of top asset market share |
| ⚡ **Sparklines** | 7-day mini trend charts for top 5 assets |
| 📋 **Top 10 Table** | Color-coded data table with 1h / 24h / 7d performance |
| 🎯 **Risk vs Return** | Scatter plot — volume vs 24h change, bubble-sized by market cap |

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit + custom CSS (dark fintech aesthetic)
- **Charts**: Plotly (interactive, hover-enabled)
- **Data**: CoinGecko API + Alternative.me Fear & Greed API (both free, no API key needed)
- **Caching**: Streamlit `@st.cache_data` with 5-min TTL for rate limit safety

---

## 🚀 Run Locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/finpulse-zorvyn.git
cd finpulse-zorvyn

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

---

## 📁 Project Structure

```
finpulse-zorvyn/
├── app.py              # Main Streamlit dashboard
├── requirements.txt    # Python dependencies
└── README.md           # You're here!
```

---

## 🔌 APIs Used

| API | Endpoint | Rate Limit |
|---|---|---|
| CoinGecko | `/coins/markets` | 30 req/min (free) |
| CoinGecko | `/coins/{id}/market_chart` | 30 req/min (free) |
| CoinGecko | `/global` | 30 req/min (free) |
| Alternative.me | `/fng/` | Unlimited (free) |

> No API keys required — all free public endpoints.

---

## 💡 Design Decisions

- **Dark fintech aesthetic** — inspired by Bloomberg Terminal & modern trading UIs
- **Space Mono + Syne** — technical monospace + modern sans pairing
- **5-minute cache TTL** — balances freshness vs API rate limits
- **Zero dependencies on paid APIs** — fully reproducible for anyone

---

## 👩‍💻 Built By

**Bhoomika S** — Data Analyst Intern applicant @ Zorvyn FinTech  
*This project was built as a demonstration of real-world data analytics & dashboard engineering skills.*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat-square&logo=linkedin)](your-linkedin-url)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat-square&logo=github)](your-github-url)

---

*Data refreshes every 5 minutes. Built with ❤️ and way too much caffeine.*
