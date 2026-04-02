import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FinPulse · Zorvyn Market Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Master CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Clash+Display:wght@400;500;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;700&display=swap');

:root {
    --bg:        #03050a;
    --bg2:       #06090f;
    --surface:   #090d16;
    --surface2:  #0d1420;
    --border:    #111d30;
    --border2:   #1a2d4a;
    --accent:    #3b82f6;
    --accent2:   #60a5fa;
    --green:     #10b981;
    --green2:    #34d399;
    --red:       #ef4444;
    --red2:      #f87171;
    --gold:      #f59e0b;
    --gold2:     #fbbf24;
    --purple:    #8b5cf6;
    --text:      #e2e8f0;
    --text2:     #94a3b8;
    --muted:     #334155;
    --inr:       #ff6b35;
    --inr2:      #ff8c5a;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"]      { background: transparent !important; display: none; }
[data-testid="stSidebar"]     { background: var(--bg2) !important; border-right: 1px solid var(--border); }
[data-testid="stToolbar"]     { display: none; }
#MainMenu, footer             { visibility: hidden; }
.block-container              { padding: 1.5rem 2rem 3rem !important; max-width: 1400px; margin: auto; }

/* ── Animated grid background ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(59,130,246,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(59,130,246,0.03) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
    z-index: 0;
}

/* ── HERO ── */
.hero-wrap {
    position: relative;
    padding: 3rem 3.5rem 2.5rem;
    margin-bottom: 0.5rem;
    border-radius: 20px;
    background: linear-gradient(135deg, #06090f 0%, #0a1628 50%, #06090f 100%);
    border: 1px solid var(--border2);
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), var(--green), var(--inr), transparent);
}
.hero-wrap::after {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(59,130,246,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    color: var(--accent2);
    text-transform: uppercase;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.live-badge {
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.3);
    color: var(--green2);
    padding: 0.15rem 0.6rem;
    border-radius: 20px;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
}
.live-dot {
    width: 6px; height: 6px;
    background: var(--green2);
    border-radius: 50%;
    display: inline-block;
    animation: blink 1.4s ease-in-out infinite;
}
@keyframes blink {
    0%,100% { opacity:1; box-shadow: 0 0 6px var(--green2); }
    50%      { opacity:0.3; box-shadow: none; }
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 5.5rem;
    letter-spacing: 0.05em;
    line-height: 0.9;
    background: linear-gradient(135deg, #ffffff 0%, var(--accent2) 50%, var(--green2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.75rem;
}
.hero-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: var(--text2);
    letter-spacing: 0.05em;
}
.hero-sub span { color: var(--text); }
.inr-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(255,107,53,0.1);
    border: 1px solid rgba(255,107,53,0.25);
    color: var(--inr2);
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.6rem;
    letter-spacing: 0.12em;
    margin-left: 0.75rem;
    font-family: 'DM Mono', monospace;
    text-transform: uppercase;
}

/* ── TICKER ── */
.ticker-outer {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.55rem 0;
    overflow: hidden;
    margin: 1.5rem 0;
    position: relative;
}
.ticker-outer::before, .ticker-outer::after {
    content: '';
    position: absolute;
    top: 0; bottom: 0;
    width: 80px;
    z-index: 2;
    pointer-events: none;
}
.ticker-outer::before { left: 0;  background: linear-gradient(90deg, var(--surface), transparent); }
.ticker-outer::after  { right: 0; background: linear-gradient(-90deg, var(--surface), transparent); }
.ticker-scroll {
    display: inline-flex;
    animation: ticker-move 40s linear infinite;
    white-space: nowrap;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    gap: 0;
}
@keyframes ticker-move {
    0%   { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
.tick-item { padding: 0 2rem; display: inline-flex; align-items: center; gap: 0.5rem; border-right: 1px solid var(--border); }
.tick-sym  { color: var(--text2); font-size: 0.65rem; }
.tick-up   { color: var(--green2); }
.tick-dn   { color: var(--red2); }
.tick-inr  { color: var(--inr2); font-size: 0.65rem; }
.tick-div  { color: var(--border2); }

/* ── CURRENCY TOGGLE ── */
.toggle-wrap {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.5rem 1rem;
    margin-bottom: 1.5rem;
    width: fit-content;
}
.toggle-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    color: var(--text2);
    text-transform: uppercase;
}

/* ── KPI CARDS ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1rem;
    margin-bottom: 0.5rem;
}
.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem 1.5rem 1.2rem;
    position: relative;
    overflow: hidden;
    transition: all 0.25s ease;
    cursor: default;
}
.kpi-card:hover {
    border-color: var(--border2);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 0 0 1px rgba(59,130,246,0.1);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
}
.kpi-card.blue::before   { background: linear-gradient(90deg, transparent, var(--accent), transparent); }
.kpi-card.green::before  { background: linear-gradient(90deg, transparent, var(--green), transparent); }
.kpi-card.gold::before   { background: linear-gradient(90deg, transparent, var(--gold), transparent); }
.kpi-card.red::before    { background: linear-gradient(90deg, transparent, var(--red), transparent); }
.kpi-card.purple::before { background: linear-gradient(90deg, transparent, var(--purple), transparent); }
.kpi-card.inr::before    { background: linear-gradient(90deg, transparent, var(--inr), transparent); }

.kpi-icon {
    font-size: 1.4rem;
    margin-bottom: 0.75rem;
    display: block;
}
.kpi-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.2em;
    color: var(--text2);
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.kpi-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    letter-spacing: 0.03em;
    color: #fff;
    line-height: 1;
    margin-bottom: 0.35rem;
}
.kpi-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: var(--text2);
    margin-bottom: 0.2rem;
}
.kpi-up   { color: var(--green2); font-family: 'DM Mono', monospace; font-size: 0.72rem; }
.kpi-dn   { color: var(--red2);   font-family: 'DM Mono', monospace; font-size: 0.72rem; }
.kpi-neu  { color: var(--text2);  font-family: 'DM Mono', monospace; font-size: 0.72rem; }

.kpi-glow {
    position: absolute;
    bottom: -30px; right: -30px;
    width: 100px; height: 100px;
    border-radius: 50%;
    opacity: 0.06;
    pointer-events: none;
}

/* ── SECTION HEADERS ── */
.sec-head {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.25em;
    color: var(--accent2);
    text-transform: uppercase;
    margin: 2.5rem 0 1.25rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.sec-head::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border2), transparent);
}
.sec-badge {
    background: rgba(59,130,246,0.08);
    border: 1px solid rgba(59,130,246,0.15);
    color: var(--accent2);
    padding: 0.15rem 0.6rem;
    border-radius: 4px;
    font-size: 0.55rem;
    letter-spacing: 0.1em;
}

/* ── INDIA SECTION ── */
.india-card {
    background: linear-gradient(135deg, #0d0a00 0%, #140c00 100%);
    border: 1px solid rgba(255,107,53,0.2);
    border-radius: 14px;
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
}
.india-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--inr), transparent);
}
.india-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    color: var(--inr2);
    text-transform: uppercase;
    margin-bottom: 1rem;
}

/* ── CHART CONTAINERS ── */
.chart-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.25rem;
    margin-bottom: 1rem;
}

/* ── FOOTER ── */
.footer {
    margin-top: 3rem;
    padding: 1.5rem 0 0;
    border-top: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    color: var(--muted);
}
.footer-brand { color: var(--accent2); }
.footer-flag  { color: var(--inr2); }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DATA FETCHING
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=300)
def get_usd_to_inr():
    """Fetch live USD/INR exchange rate."""
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=inr,usd",
            timeout=8
        )
        data = r.json()
        inr_per_usdt = data.get("tether", {}).get("inr", 83.5)
        usd_per_usdt = data.get("tether", {}).get("usd", 1.0)
        return inr_per_usdt / usd_per_usdt
    except Exception:
        return 83.5  # fallback


@st.cache_data(ttl=300)
def fetch_coins_inr():
    try:
        url = ("https://api.coingecko.com/api/v3/coins/markets"
               "?vs_currency=inr&order=market_cap_desc&per_page=10&page=1"
               "&sparkline=true&price_change_percentage=1h,24h,7d")
        r = requests.get(url, timeout=10)
        data = r.json()
        # CoinGecko returns a dict on error (rate limit etc) — must be a list
        return data if isinstance(data, list) and len(data) > 0 else None
    except Exception:
        return None


@st.cache_data(ttl=300)
def fetch_coins_usd():
    try:
        url = ("https://api.coingecko.com/api/v3/coins/markets"
               "?vs_currency=usd&order=market_cap_desc&per_page=10&page=1"
               "&sparkline=true&price_change_percentage=1h,24h,7d")
        r = requests.get(url, timeout=10)
        data = r.json()
        return data if isinstance(data, list) and len(data) > 0 else None
    except Exception:
        return None


@st.cache_data(ttl=300)
def fetch_history(coin_id, currency="inr", days=30):
    try:
        url = (f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
               f"?vs_currency={currency}&days={days}")
        r = requests.get(url, timeout=10)
        data = r.json()
        df = pd.DataFrame(data.get("prices", []), columns=["ts", "price"])
        df["date"] = pd.to_datetime(df["ts"], unit="ms")
        return df
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=300)
def fetch_global():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/global", timeout=8)
        return r.json().get("data", {})
    except Exception:
        return {}


@st.cache_data(ttl=300)
def fetch_fear_greed():
    try:
        r = requests.get("https://api.alternative.me/fng/?limit=30", timeout=8)
        df = pd.DataFrame(r.json()["data"])
        df["value"] = df["value"].astype(int)
        df["timestamp"] = pd.to_datetime(df["timestamp"].astype(int), unit="s")
        return df
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=300)
def fetch_trending():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/search/trending", timeout=8)
        return r.json().get("coins", [])[:7]
    except Exception:
        return []


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def fmt_inr(n):
    if n is None: return "N/A"
    if n >= 1e12: return f"₹{n/1e12:.2f}L Cr"   # lakh crore
    if n >= 1e7:  return f"₹{n/1e7:.2f}Cr"       # crore
    if n >= 1e5:  return f"₹{n/1e5:.2f}L"        # lakh
    return f"₹{n:,.0f}"

def fmt_usd(n):
    if n is None: return "N/A"
    if n >= 1e12: return f"${n/1e12:.2f}T"
    if n >= 1e9:  return f"${n/1e9:.2f}B"
    if n >= 1e6:  return f"${n/1e6:.2f}M"
    return f"${n:,.0f}"

def fmt_price_inr(p):
    if p is None: return "—"
    if p >= 1e7: return f"₹{p/1e7:.2f}Cr"
    if p >= 1e5: return f"₹{p/1e5:.2f}L"
    if p >= 1:   return f"₹{p:,.2f}"
    return f"₹{p:.6f}"

def fmt_price_usd(p):
    if p is None: return "—"
    return f"${p:,.4f}" if p < 1 else f"${p:,.2f}"

def chg_html(val):
    if val is None: return '<span class="kpi-neu">—</span>'
    arrow = "▲" if val >= 0 else "▼"
    cls   = "kpi-up" if val >= 0 else "kpi-dn"
    return f'<span class="{cls}">{arrow} {abs(val):.2f}%</span>'

def chart_layout(title="", height=320):
    return dict(
        title=dict(text=title, font=dict(family="DM Mono", size=11, color="#94a3b8"),
                   x=0.01, y=0.97),
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Mono", color="#475569", size=10),
        xaxis=dict(gridcolor="#111d30", showgrid=True, zeroline=False,
                   tickfont=dict(size=9, color="#475569")),
        yaxis=dict(gridcolor="#111d30", showgrid=True, zeroline=False,
                   tickfont=dict(size=9, color="#475569")),
        margin=dict(l=10, r=10, t=35, b=10),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#0d1420", bordercolor="#1a2d4a",
                        font=dict(family="DM Mono", size=10)),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#111d30",
                    font=dict(family="DM Mono", size=9)),
    )


# ══════════════════════════════════════════════════════════════════════════════
# FETCH ALL DATA
# ══════════════════════════════════════════════════════════════════════════════

with st.spinner(""):
    inr_rate  = get_usd_to_inr()
    coins_inr = fetch_coins_inr()
    coins_usd = fetch_coins_usd()
    glbl      = fetch_global()
    fg_df     = fetch_fear_greed()
    trending  = fetch_trending()
    btc_inr   = fetch_history("bitcoin",  "inr", 30)
    eth_inr   = fetch_history("ethereum", "inr", 30)
    btc_usd   = fetch_history("bitcoin",  "usd", 30)
    eth_usd   = fetch_history("ethereum", "usd", 30)

now_ist = datetime.utcnow()
now_str = now_ist.strftime("%d %b %Y · %H:%M UTC")

# Show warning if API rate-limited
if not coins_inr and not coins_usd:
    st.warning("⚠️ CoinGecko API is rate-limiting (free tier limit). Wait 1-2 min and refresh. Dashboard will auto-retry.", icon="⏳")


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0 0.5rem; font-family:'DM Mono',monospace; font-size:0.6rem;
         letter-spacing:0.2em; color:#3b82f6; text-transform:uppercase;">
         ⚡ FinPulse Controls
    </div>""", unsafe_allow_html=True)

    currency_mode = st.radio(
        "Display Currency",
        ["🇮🇳 INR (₹)", "🌐 USD ($)", "🔀 Both"],
        index=0,
        help="Switch between Indian Rupee and US Dollar display"
    )

    st.markdown("---")
    st.markdown(f"""
    <div style="font-family:'DM Mono',monospace; font-size:0.65rem; color:#475569;">
    <div style="color:#94a3b8; margin-bottom:0.5rem;">LIVE RATES</div>
    <div style="color:#ff8c5a; font-size:0.9rem; font-weight:600;">
        1 USD = ₹{inr_rate:.2f}
    </div>
    <div style="color:#334155; margin-top:0.25rem;">Auto-refreshes every 5 min</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if trending:
        st.markdown("""
        <div style="font-family:'DM Mono',monospace; font-size:0.6rem;
             letter-spacing:0.2em; color:#3b82f6; text-transform:uppercase;
             margin-bottom:0.75rem;">🔥 Trending Now</div>
        """, unsafe_allow_html=True)
        for t in trending[:5]:
            item = t.get("item", {})
            name = item.get("name", "")
            sym  = item.get("symbol", "").upper()
            rank = item.get("market_cap_rank", "—")
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center;
                 padding:0.4rem 0; border-bottom:1px solid #111d30;
                 font-family:'DM Mono',monospace; font-size:0.65rem;">
                <span style="color:#e2e8f0;">{sym}</span>
                <span style="color:#475569; font-size:0.6rem;">#{rank}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-family:'DM Mono',monospace; font-size:0.58rem; color:#334155;
         line-height:1.6;">
    Data: CoinGecko · Alternative.me<br>
    Built for Zorvyn FinTech Pvt. Ltd.<br>
    🇮🇳 Made in India
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════

fg_now  = int(fg_df.iloc[0]["value"]) if not fg_df.empty else "—"
fg_cls  = fg_df.iloc[0]["value_classification"] if not fg_df.empty else "—"

st.markdown(f"""
<div class="hero-wrap">
    <div class="hero-eyebrow">
        <span class="live-badge"><span class="live-dot"></span> LIVE DATA</span>
        &nbsp;·&nbsp; {now_str}
        <span class="inr-badge">🇮🇳 INR ENABLED · 1 USD = ₹{inr_rate:.2f}</span>
    </div>
    <div class="hero-title">FINPULSE</div>
    <div class="hero-sub">
        <span>Zorvyn FinTech Market Intelligence</span> ·
        Crypto · Sentiment · Risk · India Markets
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TICKER TAPE
# ══════════════════════════════════════════════════════════════════════════════

coins = coins_inr if "INR" in currency_mode else coins_usd
sym   = "₹" if "INR" in currency_mode else "$"

if coins:
    items = ""
    for c in coins:
        chg  = c.get("price_change_percentage_24h") or 0
        cls  = "tick-up" if chg >= 0 else "tick-dn"
        arr  = "▲" if chg >= 0 else "▼"
        p    = c.get("current_price", 0)
        p_fmt = fmt_price_inr(p) if "INR" in currency_mode else fmt_price_usd(p)
        if currency_mode == "🔀 Both":
            p_inr = fmt_price_inr(p * inr_rate) if "USD" in currency_mode else fmt_price_inr(p)
            items += f'<span class="tick-item"><span class="tick-sym">{c.get("symbol", "?").upper()}</span><span class="{cls}">{p_fmt} {arr}{abs(chg):.1f}%</span></span>'
        else:
            items += f'<span class="tick-item"><span class="tick-sym">{c.get("symbol", "?").upper()}</span><span class="{cls}">{p_fmt} {arr}{abs(chg):.1f}%</span></span>'

    st.markdown(f"""
    <div class="ticker-outer">
        <div class="ticker-scroll">{items * 3}</div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="sec-head">Global Market Snapshot <span class="sec-badge">LIVE</span></div>',
            unsafe_allow_html=True)

total_mcap = glbl.get("total_market_cap", {})
total_vol  = glbl.get("total_volume", {})
btc_dom    = glbl.get("market_cap_percentage", {}).get("btc")
mcap_chg   = glbl.get("market_cap_change_percentage_24h_usd")
active_c   = glbl.get("active_cryptocurrencies")

mcap_usd = total_mcap.get("usd")
vol_usd  = total_vol.get("usd")
mcap_inr = mcap_usd * inr_rate if mcap_usd else None
vol_inr  = vol_usd  * inr_rate if vol_usd  else None

if "INR" in currency_mode:
    mcap_val = fmt_inr(mcap_inr)
    vol_val  = fmt_inr(vol_inr)
    mcap_sub = f"≈ {fmt_usd(mcap_usd)}"
    vol_sub  = f"≈ {fmt_usd(vol_usd)}"
elif "USD" in currency_mode:
    mcap_val = fmt_usd(mcap_usd)
    vol_val  = fmt_usd(vol_usd)
    mcap_sub = f"≈ {fmt_inr(mcap_inr)}"
    vol_sub  = f"≈ {fmt_inr(vol_inr)}"
else:
    mcap_val = fmt_usd(mcap_usd)
    vol_val  = fmt_usd(vol_usd)
    mcap_sub = fmt_inr(mcap_inr)
    vol_sub  = fmt_inr(vol_inr)

fg_color = "#10b981" if fg_now != "—" and int(str(fg_now)) >= 60 else \
           "#f59e0b" if fg_now != "—" and int(str(fg_now)) >= 40 else "#ef4444"

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
    <div class="kpi-card blue">
        <span class="kpi-icon">🌐</span>
        <div class="kpi-label">Total Market Cap</div>
        <div class="kpi-value">{mcap_val}</div>
        <div class="kpi-sub">{mcap_sub}</div>
        {chg_html(mcap_chg)}
        <div class="kpi-glow" style="background:#3b82f6;"></div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card green">
        <span class="kpi-icon">📊</span>
        <div class="kpi-label">24h Trading Volume</div>
        <div class="kpi-value">{vol_val}</div>
        <div class="kpi-sub">{vol_sub}</div>
        <span class="kpi-neu">rolling 24h</span>
        <div class="kpi-glow" style="background:#10b981;"></div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card gold">
        <span class="kpi-icon">₿</span>
        <div class="kpi-label">BTC Dominance</div>
        <div class="kpi-value">{f'{btc_dom:.1f}%' if btc_dom else '—'}</div>
        <div class="kpi-sub">of total market cap</div>
        <span class="kpi-neu">market share</span>
        <div class="kpi-glow" style="background:#f59e0b;"></div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card {'green' if fg_now != '—' and int(str(fg_now)) >= 60 else 'red' if fg_now != '—' and int(str(fg_now)) < 40 else 'gold'}">
        <span class="kpi-icon">🧠</span>
        <div class="kpi-label">Fear & Greed Index</div>
        <div class="kpi-value" style="color:{fg_color};">{fg_now}</div>
        <div class="kpi-sub">{fg_cls}</div>
        <span class="kpi-neu">market sentiment</span>
        <div class="kpi-glow" style="background:{fg_color};"></div>
    </div>""", unsafe_allow_html=True)

with c5:
    btc_price_coins = coins_inr if "INR" in currency_mode else coins_usd
    btc_live = next((c for c in (btc_price_coins or []) if c.get("id") == "bitcoin" or c.get("symbol", "").lower() == "btc"), None)
    btc_p = fmt_price_inr(btc_live["current_price"]) if btc_live and "INR" in currency_mode \
            else fmt_price_usd(btc_live["current_price"]) if btc_live else "—"
    btc_chg = btc_live.get("price_change_percentage_24h") if btc_live else None
    st.markdown(f"""
    <div class="kpi-card inr">
        <span class="kpi-icon">🇮🇳</span>
        <div class="kpi-label">Bitcoin Live Price</div>
        <div class="kpi-value" style="font-size:1.5rem;">{btc_p}</div>
        <div class="kpi-sub">1 USD = ₹{inr_rate:.2f}</div>
        {chg_html(btc_chg)}
        <div class="kpi-glow" style="background:#ff6b35;"></div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PRICE CHARTS — BTC & ETH
# ══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="sec-head">Price History · 30 Days</div>', unsafe_allow_html=True)

use_inr = "USD" not in currency_mode
btc_df = btc_inr if use_inr else btc_usd
eth_df = eth_inr if use_inr else eth_usd
c_sym  = "₹" if use_inr else "$"

ch1, ch2 = st.columns(2)

with ch1:
    if not btc_df.empty:
        mn, mx = btc_df["price"].min(), btc_df["price"].max()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=btc_df["date"], y=btc_df["price"],
            mode="lines",
            line=dict(color="#3b82f6", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(59,130,246,0.07)",
            name=f"BTC/{c_sym}",
            hovertemplate=f"{c_sym}%{{y:,.0f}}<extra>Bitcoin</extra>",
        ))
        # Add min/max annotations
        fig.add_annotation(x=btc_df.loc[btc_df["price"].idxmax(), "date"],
                           y=mx, text=f"H: {c_sym}{mx:,.0f}",
                           font=dict(size=9, color="#60a5fa", family="DM Mono"),
                           showarrow=False, yshift=12)
        fig.add_annotation(x=btc_df.loc[btc_df["price"].idxmin(), "date"],
                           y=mn, text=f"L: {c_sym}{mn:,.0f}",
                           font=dict(size=9, color="#f87171", family="DM Mono"),
                           showarrow=False, yshift=-14)
        fig.update_layout(**chart_layout("BITCOIN (BTC) · 30D"))
        st.plotly_chart(fig, use_container_width=True)

with ch2:
    if not eth_df.empty:
        mn2, mx2 = eth_df["price"].min(), eth_df["price"].max()
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=eth_df["date"], y=eth_df["price"],
            mode="lines",
            line=dict(color="#10b981", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(16,185,129,0.07)",
            name=f"ETH/{c_sym}",
            hovertemplate=f"{c_sym}%{{y:,.0f}}<extra>Ethereum</extra>",
        ))
        fig2.add_annotation(x=eth_df.loc[eth_df["price"].idxmax(), "date"],
                            y=mx2, text=f"H: {c_sym}{mx2:,.0f}",
                            font=dict(size=9, color="#34d399", family="DM Mono"),
                            showarrow=False, yshift=12)
        fig2.add_annotation(x=eth_df.loc[eth_df["price"].idxmin(), "date"],
                            y=mn2, text=f"L: {c_sym}{mn2:,.0f}",
                            font=dict(size=9, color="#f87171", family="DM Mono"),
                            showarrow=False, yshift=-14)
        fig2.update_layout(**chart_layout("ETHEREUM (ETH) · 30D"))
        st.plotly_chart(fig2, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# INDIA MARKET SPOTLIGHT
# ══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="sec-head">🇮🇳 India Market Spotlight <span class="sec-badge">INR FOCUS</span></div>',
            unsafe_allow_html=True)

ia, ib, ic = st.columns(3)

if coins_inr:
    top3 = coins_inr[:3]
    for col, c in zip([ia, ib, ic], top3):
        with col:
            p_inr = c.get("current_price", 0)
            p_usd = p_inr / inr_rate
            chg24 = c.get("price_change_percentage_24h") or 0
            chg7d = c.get("price_change_percentage_7d_in_currency") or 0
            color = "#10b981" if chg24 >= 0 else "#ef4444"
            spark = c.get("sparkline_in_7d", {}).get("price", [])

            fig_s = go.Figure()
            if spark:
                fig_s.add_trace(go.Scatter(
                    y=spark, mode="lines",
                    line=dict(color=color, width=2),
                    fill="tozeroy",
                    fillcolor=f"rgba({'16,185,129' if chg24>=0 else '239,68,68'},0.08)",
                ))
            fig_s.update_layout(
                height=80, showlegend=False,
                margin=dict(l=0,r=0,t=0,b=0),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(visible=False), yaxis=dict(visible=False),
            )

            arr = "▲" if chg24 >= 0 else "▼"
            st.markdown(f"""
            <div class="india-card">
                <div class="india-title">{c['symbol'].upper()} · {c['name']}</div>
                <div style="font-family:'Bebas Neue',sans-serif; font-size:2rem;
                     color:#fff; line-height:1; margin-bottom:0.2rem;">
                     {fmt_price_inr(p_inr)}
                </div>
                <div style="font-family:'DM Mono',monospace; font-size:0.65rem;
                     color:#475569; margin-bottom:0.5rem;">
                     ≈ {fmt_price_usd(p_usd)}
                </div>
                <div style="font-family:'DM Mono',monospace; font-size:0.75rem;
                     color:{color};">{arr} {abs(chg24):.2f}% (24h) &nbsp;·&nbsp; {arr} {abs(chg7d):.2f}% (7d)</div>
            </div>""", unsafe_allow_html=True)
            st.plotly_chart(fig_s, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# FEAR & GREED + DOMINANCE
# ══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="sec-head">Sentiment & Market Structure</div>', unsafe_allow_html=True)

s1, s2 = st.columns([3, 2])

with s1:
    if not fg_df.empty:
        disp = fg_df.head(21).sort_values("timestamp")
        bar_colors = [
            "#ef4444" if v < 25 else
            "#f97316" if v < 40 else
            "#f59e0b" if v < 60 else
            "#84cc16" if v < 75 else
            "#10b981"
            for v in disp["value"]
        ]
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=disp["timestamp"], y=disp["value"],
            marker=dict(color=bar_colors, opacity=0.9,
                        line=dict(color="rgba(0,0,0,0)", width=0)),
            hovertemplate="%{y} — %{x|%d %b}<extra>%{text}</extra>",
            text=disp["value_classification"],
        ))
        fig3.add_hline(y=25, line_dash="dot", line_color="#334155",
                       annotation_text="Extreme Fear", annotation_font=dict(size=8, color="#334155"))
        fig3.add_hline(y=75, line_dash="dot", line_color="#334155",
                       annotation_text="Extreme Greed", annotation_font=dict(size=8, color="#334155"))
        fig3.update_layout(**chart_layout("CRYPTO FEAR & GREED INDEX · 21 DAYS", height=300))
        st.plotly_chart(fig3, use_container_width=True)

with s2:
    if glbl:
        dom = glbl.get("market_cap_percentage", {})
        top = dict(sorted(dom.items(), key=lambda x: x[1], reverse=True)[:8])
        fig4 = go.Figure(go.Pie(
            labels=[k.upper() for k in top],
            values=list(top.values()),
            hole=0.6,
            marker=dict(
                colors=["#3b82f6","#10b981","#f59e0b","#ef4444",
                        "#8b5cf6","#ec4899","#06b6d4","#334155"],
                line=dict(color="#03050a", width=2),
            ),
            textfont=dict(family="DM Mono", size=9),
            hovertemplate="%{label}: %{value:.1f}%<extra></extra>",
        ))
        fig4.update_layout(
            **{**chart_layout("MARKET CAP DOMINANCE", height=300),
               "showlegend": True,
               "legend": dict(bgcolor="rgba(0,0,0,0)",
                              font=dict(size=8, family="DM Mono", color="#94a3b8"))},
        )
        st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TOP 10 TABLE
# ══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="sec-head">Top 10 Assets · Full Breakdown</div>', unsafe_allow_html=True)

active_coins = coins_inr if use_inr else coins_usd

if active_coins:
    rows = []
    for c in active_coins:
        p     = c.get("current_price", 0)
        p_inr = p if use_inr else p * inr_rate
        p_usd = p / inr_rate if use_inr else p
        rows.append({
            "#":          c.get("market_cap_rank", "—"),
            "Asset":      f'{c.get("name", "Unknown")} ({c.get("symbol", "?").upper()})',
            "Price (₹)":  fmt_price_inr(p_inr),
            "Price ($)":  fmt_price_usd(p_usd),
            "1h %":       round(c.get("price_change_percentage_1h_in_currency") or 0, 2),
            "24h %":      round(c.get("price_change_percentage_24h") or 0, 2),
            "7d %":       round(c.get("price_change_percentage_7d_in_currency") or 0, 2),
            "Mkt Cap":    fmt_inr(c.get("market_cap", 0)) if use_inr else fmt_usd(c.get("market_cap", 0)),
            "Vol 24h":    fmt_inr(c.get("total_volume", 0)) if use_inr else fmt_usd(c.get("total_volume", 0)),
        })

    df_t = pd.DataFrame(rows)

    def style_pct(v):
        return f"color: #34d399" if v > 0 else f"color: #f87171" if v < 0 else "color: #475569"

    styled = (df_t.style
              .map(style_pct, subset=["1h %", "24h %", "7d %"])
              .set_properties(**{
                  "background-color": "#090d16",
                  "color": "#e2e8f0",
                  "border-color": "#111d30",
                  "font-family": "DM Mono, monospace",
                  "font-size": "0.75rem",
              })
              .set_table_styles([
                  {"selector": "th", "props": [
                      ("background-color", "#06090f"),
                      ("color", "#3b82f6"),
                      ("font-family", "DM Mono, monospace"),
                      ("font-size", "0.6rem"),
                      ("text-transform", "uppercase"),
                      ("letter-spacing", "0.1em"),
                      ("border-color", "#111d30"),
                      ("padding", "0.6rem 0.75rem"),
                  ]},
                  {"selector": "td", "props": [
                      ("padding", "0.55rem 0.75rem"),
                      ("border-color", "#111d30"),
                  ]},
              ]))
    st.dataframe(styled, use_container_width=True, height=390)


# ══════════════════════════════════════════════════════════════════════════════
# RISK vs RETURN SCATTER
# ══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="sec-head">Risk vs Return · 24h Snapshot</div>', unsafe_allow_html=True)

if active_coins:
    sdf = pd.DataFrame([{
        "coin":  c.get("symbol", "?").upper(),
        "chg":   c.get("price_change_percentage_24h") or 0,
        "vol":   c.get("total_volume") or 0,
        "mcap":  c.get("market_cap") or 0,
        "chg7d": c.get("price_change_percentage_7d_in_currency") or 0,
    } for c in active_coins])

    fig5 = go.Figure()
    fig5.add_shape(type="line", x0=sdf["vol"].min(), x1=sdf["vol"].max(),
                   y0=0, y1=0, line=dict(color="#334155", width=1, dash="dot"))
    fig5.add_trace(go.Scatter(
        x=sdf["vol"], y=sdf["chg"],
        mode="markers+text",
        text=sdf["coin"],
        textposition="top center",
        textfont=dict(family="DM Mono", size=9, color="#94a3b8"),
        marker=dict(
            size=[max(14, min(50, m / sdf["mcap"].max() * 60)) for m in sdf["mcap"]],
            color=sdf["chg"],
            colorscale=[[0,"#ef4444"],[0.5,"#f59e0b"],[1,"#10b981"]],
            opacity=0.85,
            line=dict(color="#03050a", width=2),
            showscale=False,
        ),
        hovertemplate=(
            "<b>%{text}</b><br>"
            "24h Change: %{y:.2f}%<br>"
            f"Volume: {c_sym}%{{x:,.0f}}<extra></extra>"
        ),
    ))
    fig5.update_layout(
        **chart_layout("VOLUME vs 24H RETURN · BUBBLE SIZE = MARKET CAP", height=380),
        xaxis_title="24h Trading Volume",
        yaxis_title="24h Return (%)",
    )
    st.plotly_chart(fig5, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# 7-DAY SPARKLINES
# ══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="sec-head">7-Day Sparklines · Top 5</div>', unsafe_allow_html=True)

if active_coins:
    sp_cols = st.columns(5)
    for col, c in zip(sp_cols, active_coins[:5]):
        spark = c.get("sparkline_in_7d", {}).get("price", [])
        with col:
            if spark:
                chg = ((spark[-1] - spark[0]) / spark[0]) * 100
                clr = "#10b981" if chg >= 0 else "#ef4444"
                fig_s = go.Figure(go.Scatter(
                    y=spark, mode="lines",
                    line=dict(color=clr, width=2),
                    fill="tozeroy",
                    fillcolor=f"rgba({'16,185,129' if chg>=0 else '239,68,68'},0.07)",
                ))
                fig_s.update_layout(
                    title=dict(
                        text=f'<span style="color:#94a3b8">{c.get("symbol", "?").upper()}</span> '
                             f'<span style="color:{clr};font-size:10px">{"▲" if chg>=0 else "▼"}{abs(chg):.1f}%</span>',
                        font=dict(size=11, family="DM Mono"),
                        x=0.05, y=0.95,
                    ),
                    height=130, showlegend=False,
                    margin=dict(l=0, r=0, t=28, b=0),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(visible=False), yaxis=dict(visible=False),
                )
                st.plotly_chart(fig_s, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════

st.markdown(f"""
<div class="footer">
    <div>
        <span class="footer-brand">⚡ FinPulse</span> · Built for
        <span class="footer-brand">Zorvyn FinTech Pvt. Ltd.</span> ·
        Data: CoinGecko API &amp; Alternative.me
    </div>
    <div>
        <span class="footer-flag">🇮🇳 Made in India</span> ·
        1 USD = ₹{inr_rate:.2f} · Refreshed: {now_str}
    </div>
</div>
""", unsafe_allow_html=True)
