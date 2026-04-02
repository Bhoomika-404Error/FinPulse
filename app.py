import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FinPulse · Zorvyn Market Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

:root {
    --bg:       #020408;
    --surface:  #080e18;
    --border:   #0f2040;
    --accent:   #00d4ff;
    --green:    #00ff88;
    --red:      #ff3b6b;
    --gold:     #f0c040;
    --text:     #c8e0f4;
    --muted:    #4a6580;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { background: var(--surface) !important; }

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #020408 0%, #040d1a 40%, #020408 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -1px; left: -1px; right: -1px; bottom: -1px;
    border-radius: 16px;
    background: linear-gradient(90deg, var(--accent), transparent, var(--green));
    z-index: -1;
    opacity: 0.4;
}
.hero-tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.hero-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #ffffff, var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
    margin: 0;
}
.hero-sub {
    color: var(--muted);
    font-size: 0.95rem;
    margin-top: 0.75rem;
    font-family: 'Space Mono', monospace;
}
.live-dot {
    display: inline-block;
    width: 8px; height: 8px;
    background: var(--green);
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(1.4); }
}

/* ── KPI cards ── */
.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.kpi-card:hover { border-color: var(--accent); }
.kpi-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.18em;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 800;
    line-height: 1;
    color: #fff;
}
.kpi-change-up   { color: var(--green); font-family: 'Space Mono', monospace; font-size: 0.8rem; }
.kpi-change-down { color: var(--red);   font-family: 'Space Mono', monospace; font-size: 0.8rem; }
.kpi-accent-bar {
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    border-radius: 12px 0 0 12px;
}

/* ── Section headers ── */
.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: var(--accent);
    text-transform: uppercase;
    margin: 2rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Table styling ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    overflow: hidden;
}

/* ── Ticker tape ── */
.ticker-wrap {
    background: var(--surface);
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    padding: 0.6rem 0;
    overflow: hidden;
    margin-bottom: 2rem;
    white-space: nowrap;
}
.ticker-content {
    display: inline-block;
    animation: scroll-left 30s linear infinite;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
}
@keyframes scroll-left {
    0%   { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
.tick-up   { color: var(--green); margin: 0 1.5rem; }
.tick-down { color: var(--red);   margin: 0 1.5rem; }
.tick-name { color: var(--muted); margin-right: 0.4rem; }

/* ── Footer ── */
.footer {
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.footer-brand { color: var(--accent); font-weight: 700; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DATA FETCHING
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=300)
def fetch_crypto():
    """Fetch top crypto prices from CoinGecko (free, no key needed)."""
    try:
        url = ("https://api.coingecko.com/api/v3/coins/markets"
               "?vs_currency=usd&order=market_cap_desc&per_page=10&page=1"
               "&sparkline=true&price_change_percentage=1h,24h,7d")
        r = requests.get(url, timeout=10)
        return r.json()
    except Exception:
        return None


@st.cache_data(ttl=300)
def fetch_crypto_history(coin_id="bitcoin", days=30):
    try:
        url = (f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
               f"?vs_currency=usd&days={days}")
        r = requests.get(url, timeout=10)
        data = r.json()
        prices = data.get("prices", [])
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=300)
def fetch_fear_greed():
    try:
        r = requests.get("https://api.alternative.me/fng/?limit=30", timeout=8)
        data = r.json()["data"]
        df = pd.DataFrame(data)
        df["value"] = df["value"].astype(int)
        df["timestamp"] = pd.to_datetime(df["timestamp"].astype(int), unit="s")
        return df
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=300)
def fetch_global_market():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/global", timeout=8)
        return r.json().get("data", {})
    except Exception:
        return {}


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def fmt_large(n):
    if n is None: return "N/A"
    if n >= 1e12: return f"${n/1e12:.2f}T"
    if n >= 1e9:  return f"${n/1e9:.2f}B"
    if n >= 1e6:  return f"${n/1e6:.2f}M"
    return f"${n:,.0f}"

def color_change(val):
    if val is None: return "—"
    arrow = "▲" if val >= 0 else "▼"
    cls   = "kpi-change-up" if val >= 0 else "kpi-change-down"
    return f'<span class="{cls}">{arrow} {abs(val):.2f}%</span>'

def plotly_dark_layout():
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Space Mono", color="#4a6580", size=10),
        xaxis=dict(gridcolor="#0f2040", showgrid=True, zeroline=False),
        yaxis=dict(gridcolor="#0f2040", showgrid=True, zeroline=False),
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#0f2040"),
        hovermode="x unified",
    )


# ══════════════════════════════════════════════════════════════════════════════
# LAYOUT
# ══════════════════════════════════════════════════════════════════════════════

# ── Hero ───────────────────────────────────────────────────────────────────────
now = datetime.utcnow().strftime("%d %b %Y · %H:%M UTC")
st.markdown(f"""
<div class="hero">
    <div class="hero-tag">⚡ Zorvyn FinTech · Market Intelligence Platform</div>
    <h1 class="hero-title">FinPulse</h1>
    <p class="hero-sub">
        <span class="live-dot"></span>LIVE DATA &nbsp;·&nbsp; {now} &nbsp;·&nbsp;
        Crypto Markets &amp; Sentiment Analytics
    </p>
</div>
""", unsafe_allow_html=True)

# ── Fetch data ─────────────────────────────────────────────────────────────────
with st.spinner("Fetching live market data…"):
    coins   = fetch_crypto()
    glbl    = fetch_global_market()
    fg_df   = fetch_fear_greed()
    btc_df  = fetch_crypto_history("bitcoin", 30)
    eth_df  = fetch_crypto_history("ethereum", 30)

# ── Ticker tape ───────────────────────────────────────────────────────────────
if coins:
    tickers = ""
    for c in coins[:10]:
        chg = c.get("price_change_percentage_24h") or 0
        cls = "tick-up" if chg >= 0 else "tick-down"
        arrow = "▲" if chg >= 0 else "▼"
        tickers += (f'<span class="{cls}">'
                    f'<span class="tick-name">{c["symbol"].upper()}</span>'
                    f'${c["current_price"]:,.2f} {arrow}{abs(chg):.2f}%'
                    f'</span>')
    double = tickers * 2   # seamless loop
    st.markdown(f'<div class="ticker-wrap"><div class="ticker-content">{double}</div></div>',
                unsafe_allow_html=True)

# ── Global KPIs ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Global Market Overview</div>', unsafe_allow_html=True)

total_mcap  = glbl.get("total_market_cap", {}).get("usd")
total_vol   = glbl.get("total_volume",     {}).get("usd")
btc_dom     = glbl.get("market_cap_percentage", {}).get("btc")
active_c    = glbl.get("active_cryptocurrencies")
mcap_chg    = glbl.get("market_cap_change_percentage_24h_usd")

fg_latest   = int(fg_df.iloc[0]["value"]) if not fg_df.empty else None
fg_class    = fg_df.iloc[0]["value_classification"] if not fg_df.empty else "—"

kpis = [
    ("Total Market Cap",   fmt_large(total_mcap), mcap_chg,  "#00d4ff"),
    ("24h Volume",         fmt_large(total_vol),  None,       "#00ff88"),
    ("BTC Dominance",      f"{btc_dom:.1f}%" if btc_dom else "—", None, "#f0c040"),
    ("Fear & Greed Index", str(fg_latest) if fg_latest else "—", None, "#ff3b6b"),
    ("Active Assets",      f"{active_c:,}" if active_c else "—", None, "#a78bfa"),
]

cols = st.columns(5)
for col, (label, value, chg, accent) in zip(cols, kpis):
    with col:
        chg_html = color_change(chg) if chg is not None else ""
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-accent-bar" style="background:{accent}"></div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div style="margin-top:0.4rem">{chg_html}</div>
        </div>""", unsafe_allow_html=True)

# ── Price Charts ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Price History · 30 Days</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    if not btc_df.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=btc_df["date"], y=btc_df["price"],
            mode="lines",
            line=dict(color="#00d4ff", width=2),
            fill="tozeroy",
            fillcolor="rgba(0,212,255,0.06)",
            name="BTC/USD",
            hovertemplate="$%{y:,.0f}<extra>BTC</extra>",
        ))
        fig.update_layout(title="Bitcoin (BTC)", **plotly_dark_layout())
        st.plotly_chart(fig, use_container_width=True)

with c2:
    if not eth_df.empty:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=eth_df["date"], y=eth_df["price"],
            mode="lines",
            line=dict(color="#00ff88", width=2),
            fill="tozeroy",
            fillcolor="rgba(0,255,136,0.06)",
            name="ETH/USD",
            hovertemplate="$%{y:,.2f}<extra>ETH</extra>",
        ))
        fig2.update_layout(title="Ethereum (ETH)", **plotly_dark_layout())
        st.plotly_chart(fig2, use_container_width=True)

# ── Fear & Greed + Market Dominance ───────────────────────────────────────────
st.markdown('<div class="section-header">Sentiment & Dominance</div>', unsafe_allow_html=True)

c3, c4 = st.columns([3, 2])

with c3:
    if not fg_df.empty:
        display_df = fg_df.head(14).sort_values("timestamp")
        bar_colors = ["#ff3b6b" if v < 40 else "#f0c040" if v < 60 else "#00ff88"
                      for v in display_df["value"]]
        fig3 = go.Figure(go.Bar(
            x=display_df["timestamp"],
            y=display_df["value"],
            marker_color=bar_colors,
            hovertemplate="%{y} · %{x|%d %b}<extra></extra>",
        ))
        fig3.add_hline(y=50, line_dash="dot", line_color="#4a6580", annotation_text="Neutral")
        fig3.update_layout(title="Fear & Greed Index · 14 Days", **plotly_dark_layout())
        st.plotly_chart(fig3, use_container_width=True)

with c4:
    if glbl:
        dom = glbl.get("market_cap_percentage", {})
        top = dict(sorted(dom.items(), key=lambda x: x[1], reverse=True)[:7])
        fig4 = go.Figure(go.Pie(
            labels=[k.upper() for k in top],
            values=list(top.values()),
            hole=0.55,
            marker=dict(colors=["#00d4ff","#00ff88","#f0c040","#ff3b6b",
                                 "#a78bfa","#fb923c","#4a6580"]),
            textfont=dict(family="Space Mono", size=10),
            hovertemplate="%{label}: %{value:.1f}%<extra></extra>",
        ))
        fig4.update_layout(
            title="Market Cap Dominance",
            showlegend=True,
            **{**plotly_dark_layout(),
               "legend": dict(bgcolor="rgba(0,0,0,0)", font=dict(size=9, family="Space Mono"))}
        )
        st.plotly_chart(fig4, use_container_width=True)

# ── Top 10 Table ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Top 10 Assets by Market Cap</div>', unsafe_allow_html=True)

if coins:
    rows = []
    for c in coins:
        rows.append({
            "Rank":       c.get("market_cap_rank", "—"),
            "Asset":      f'{c["name"]} ({c["symbol"].upper()})',
            "Price (USD)":f'${c["current_price"]:,.4f}' if c["current_price"] < 1
                           else f'${c["current_price"]:,.2f}',
            "1h %":       round(c.get("price_change_percentage_1h_in_currency") or 0, 2),
            "24h %":      round(c.get("price_change_percentage_24h") or 0, 2),
            "7d %":       round(c.get("price_change_percentage_7d_in_currency") or 0, 2),
            "Market Cap": fmt_large(c.get("market_cap")),
            "Volume 24h": fmt_large(c.get("total_volume")),
            "ATH":        f'${c.get("ath", 0):,.2f}',
        })
    df_table = pd.DataFrame(rows)

    def color_pct(val):
        color = "#00ff88" if val > 0 else "#ff3b6b" if val < 0 else "#4a6580"
        return f"color: {color}"

    styled = (df_table.style
              .applymap(color_pct, subset=["1h %", "24h %", "7d %"])
              .set_properties(**{"background-color": "#080e18", "color": "#c8e0f4",
                                 "border-color": "#0f2040"})
              .set_table_styles([
                  {"selector": "th",
                   "props": [("background-color", "#020408"),
                              ("color", "#00d4ff"),
                              ("font-family", "Space Mono"),
                              ("font-size", "0.65rem"),
                              ("text-transform", "uppercase"),
                              ("border-color", "#0f2040")]},
              ]))
    st.dataframe(styled, use_container_width=True, height=380)

# ── Volatility Scatter ─────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Risk vs Return · 24h Snapshot</div>', unsafe_allow_html=True)

if coins:
    scatter_data = [{
        "name":   c["symbol"].upper(),
        "chg24":  c.get("price_change_percentage_24h") or 0,
        "mcap":   c.get("market_cap") or 0,
        "vol":    c.get("total_volume") or 0,
        "price":  c.get("current_price") or 0,
    } for c in coins]
    sdf = pd.DataFrame(scatter_data)

    fig5 = px.scatter(
        sdf, x="vol", y="chg24", size="mcap", text="name",
        color="chg24",
        color_continuous_scale=[[0,"#ff3b6b"],[0.5,"#f0c040"],[1,"#00ff88"]],
        labels={"vol":"24h Volume (USD)","chg24":"24h Change (%)","mcap":"Market Cap"},
        hover_data={"price": True, "name": False},
    )
    fig5.update_traces(textposition="top center",
                       textfont=dict(family="Space Mono", size=9, color="#c8e0f4"))
    fig5.update_layout(
        coloraxis_showscale=False,
        **plotly_dark_layout()
    )
    st.plotly_chart(fig5, use_container_width=True)

# ── Sparklines row ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">7-Day Sparklines</div>', unsafe_allow_html=True)

if coins:
    spark_cols = st.columns(5)
    for i, (col, c) in enumerate(zip(spark_cols, coins[:5])):
        spark = c.get("sparkline_in_7d", {}).get("price", [])
        with col:
            if spark:
                chg = ((spark[-1] - spark[0]) / spark[0]) * 100
                clr = "#00ff88" if chg >= 0 else "#ff3b6b"
                fig_s = go.Figure(go.Scatter(
                    y=spark, mode="lines",
                    line=dict(color=clr, width=1.5),
                    fill="tozeroy", fillcolor=f"rgba({','.join(['0,255,136' if chg>=0 else '255,59,107'])},0.08)",
                ))
                fig_s.update_layout(
                    title=dict(text=f'{c["symbol"].upper()} · {chg:+.1f}%',
                               font=dict(size=11, family="Space Mono", color=clr)),
                    height=120,
                    showlegend=False,
                    margin=dict(l=0,r=0,t=30,b=0),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(visible=False),
                    yaxis=dict(visible=False),
                )
                st.plotly_chart(fig_s, use_container_width=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
    <div>Built for <span class="footer-brand">Zorvyn FinTech Pvt. Ltd.</span> ·
    Data via CoinGecko &amp; Alternative.me APIs</div>
    <div>Last refreshed: {now} · Auto-refreshes every 5 min</div>
</div>
""", unsafe_allow_html=True)

# Auto-refresh every 5 minutes
time.sleep(0)
