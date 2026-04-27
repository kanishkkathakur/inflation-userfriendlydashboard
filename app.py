"""
Price Watch Dashboard — Essential Commodities
Redesigned for households and shopkeepers. Simple, bright, and clear.
Uses real datasets: vegetable_inflation_dataset.csv, merged_grocery_dataset.csv, fuel_by_date.csv
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import warnings
import os
warnings.filterwarnings("ignore")

# ─── RESOLVE DATA PATHS ──────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VEG_CSV   = os.path.join(BASE_DIR, "vegetable_inflation_dataset.csv")
GROC_CSV  = os.path.join(BASE_DIR, "merged_grocery_dataset.csv")
FUEL_CSV  = os.path.join(BASE_DIR, "fuel_by_date.csv")

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Price Watch 🛒 Commodities Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── BRIGHT THEME CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
    background-color: #FFFFFF !important;
}
.main { background: #FFFFFF !important; }
.block-container {
    padding: 1.2rem 2rem 2rem 2rem !important;
    max-width: 100% !important;
    background: #FFFFFF !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #F0F7FF 0%, #EEF2FF 100%) !important;
    border-right: 2px solid #E0E7FF !important;
}
[data-testid="stSidebar"] * { color: #1E293B !important; }

/* ── TOP BANNER ── */
.top-banner {
    background: linear-gradient(135deg, #3B82F6 0%, #6366F1 50%, #8B5CF6 100%);
    border-radius: 20px;
    padding: 1.6rem 2.2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(99,102,241,0.25);
    color: white;
}
.banner-title { font-size: 2rem; font-weight: 900; margin: 0; letter-spacing: -0.5px; }
.banner-sub { font-size: 1rem; font-weight: 600; opacity: 0.88; margin: 0.3rem 0 0 0; }

/* ── PRICE CARD ── */
.price-card {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 1.3rem 1.4rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    border: 2px solid transparent;
    margin-bottom: 0.5rem;
}
.card-emoji { font-size: 2rem; margin-bottom: 0.3rem; }
.card-name { font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; color: #64748B; margin-bottom: 0.2rem; }
.card-price { font-size: 2rem; font-weight: 900; line-height: 1.1; margin-bottom: 0.3rem; }
.card-change { font-size: 0.88rem; font-weight: 700; padding: 0.25rem 0.65rem; border-radius: 30px; display: inline-block; }
.card-advice { font-size: 0.82rem; font-weight: 700; margin-top: 0.5rem; padding: 0.35rem 0.7rem; border-radius: 10px; display: inline-block; }

/* ── SIGNAL BOXES ── */
.signal-green { background: #ECFDF5; border: 2px solid #6EE7B7; color: #065F46; }
.signal-red { background: #FEF2F2; border: 2px solid #FCA5A5; color: #991B1B; }
.signal-orange { background: #FFF7ED; border: 2px solid #FED7AA; color: #92400E; }
.signal-blue { background: #EFF6FF; border: 2px solid #BFDBFE; color: #1E40AF; }

/* ── BIG INSIGHT BOX ── */
.insight-big { border-radius: 16px; padding: 1.1rem 1.4rem; margin: 0.5rem 0; font-size: 1rem; font-weight: 700; }

/* ── SECTION HEADER ── */
.sec-header { font-size: 1.5rem; font-weight: 900; margin: 1.4rem 0 0.8rem 0; display: flex; align-items: center; gap: 0.5rem; }

/* ── CHART TIP ── */
.chart-tip {
    background: #F8FAFC;
    border-left: 5px solid #6366F1;
    border-radius: 0 10px 10px 0;
    padding: 0.7rem 1rem;
    font-size: 0.9rem;
    font-weight: 600;
    color: #334155;
    margin: 0.5rem 0 1rem 0;
}

/* ── SUMMARY TABLE ── */
.sum-table { width: 100%; border-collapse: collapse; border-radius: 14px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }
.sum-table th { background: #6366F1; color: white; padding: 0.75rem 1rem; font-size: 0.85rem; font-weight: 700; text-align: left; }
.sum-table td { padding: 0.65rem 1rem; font-size: 0.88rem; border-bottom: 1px solid #F1F5F9; color: #1E293B; font-weight: 600; }
.sum-table tr:nth-child(even) td { background: #F8FAFC; }

/* ── DIVIDER ── */
.bright-divider { height: 3px; background: linear-gradient(90deg, #3B82F6, #8B5CF6, #EC4899); border-radius: 3px; margin: 1.5rem 0; }

/* ── Streamlit tab override ── */
.stTabs [data-baseweb="tab-list"] { gap: 0.4rem; background: #F1F5F9; padding: 0.35rem; border-radius: 14px; border: 2px solid #E2E8F0; }
.stTabs [data-baseweb="tab"] { font-family: 'Nunito', sans-serif; font-size: 0.95rem; font-weight: 700; padding: 0.5rem 1.2rem; border-radius: 10px; color: #64748B; }
.stTabs [aria-selected="true"] { background: #FFFFFF !important; color: #1E293B !important; font-weight: 800; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }

button[kind="primary"] { background: linear-gradient(135deg, #3B82F6, #6366F1) !important; border-radius: 12px !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)


# ─── DATA LOADING ────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    # Load vegetables (monthly)
    veg = pd.read_csv(VEG_CSV, parse_dates=["Date"])
    veg = veg.set_index("Date").sort_index()
    veg.index = veg.index.to_period("M").to_timestamp()

    # Load grocery (daily → resample to monthly)
    groc = pd.read_csv(GROC_CSV, parse_dates=["Date"])
    groc = groc.set_index("Date").sort_index()
    groc = groc.resample("MS").mean()

    # Load fuel (daily → resample to monthly)
    fuel = pd.read_csv(FUEL_CSV, parse_dates=["Date"])
    fuel = fuel.set_index("Date").sort_index()
    fuel = fuel.resample("MS").mean()
    fuel.columns = ["Fuel"]

    # ── Commodity groupings ──────────────────────────────────────────────────
    # Vegetables: use Average_Price, Onion, Potato, Tomato
    veg_items = {
        "🥬 Vegetables (Avg)":   veg["Average_Price"],
        "🧅 Onion":              veg["Onion_Price"],
        "🥔 Potato":             veg["Potato_Price"],
        "🍅 Tomato":             veg["Tomato_Price"],
    }

    # Grocery: Tea, Milk, Sugar, Mustard Oil, Tur Dal, Moong Dal
    groc_items = {
        "🍵 Tea":                groc["Tea"],
        "🥛 Milk":               groc["Milk"],
        "🍬 Sugar":              groc["Sugar"],
        "🫙 Mustard Oil":        groc["Mustard"],
        "🫘 Tur Dal":            groc["Tur"],
        "🌿 Moong Dal":          groc["Moong"],
    }

    # Fuel
    fuel_items = {
        "⛽ Fuel":               fuel["Fuel"],
    }

    # Combine into one master frame (monthly, intersect date range)
    all_series = {**veg_items, **groc_items, **fuel_items}
    master = pd.DataFrame(all_series)
    master = master.interpolate(method="time").ffill().bfill()
    master = master.dropna(how="all")

    return master, list(veg_items.keys()), list(groc_items.keys()), list(fuel_items.keys())


master, veg_keys, groc_keys, fuel_keys = load_data()
ALL_ITEMS = list(master.columns)

# ─── THEME MAPS ──────────────────────────────────────────────────────────────
def item_color(name):
    if any(k in name for k in ["🥬","🧅","🥔","🍅"]):
        return "#22C55E"
    if "⛽" in name:
        return "#F97316"
    if "🍵" in name or "🥛" in name or "🍬" in name:
        return "#3B82F6"
    return "#A855F7"

def item_bg(name):
    c = item_color(name)
    mapping = {
        "#22C55E": ("#F0FDF4", "#BBF7D0", "#14532D"),
        "#F97316": ("#FFF7ED", "#FED7AA", "#7C2D12"),
        "#3B82F6": ("#EFF6FF", "#BFDBFE", "#1E3A8A"),
        "#A855F7": ("#FAF5FF", "#E9D5FF", "#581C87"),
    }
    return mapping.get(c, ("#F8FAFC", "#E2E8F0", "#1E293B"))

def color_fill(name):
    c = item_color(name)
    return c.replace("#","rgba(") + ",0.12)".replace("rgba(","rgba(") if False else f"rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},0.12)"

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#FAFBFF",
    font=dict(family="Nunito, sans-serif", size=12, color="#1E293B"),
    margin=dict(l=10, r=10, t=44, b=10),
    legend=dict(
        orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
        font=dict(size=11, family="Nunito"),
        bgcolor="rgba(255,255,255,0.9)", bordercolor="#E2E8F0", borderwidth=1,
    ),
    xaxis=dict(showgrid=True, gridcolor="#EEF2FF", gridwidth=1, showline=True, linecolor="#E2E8F0", zeroline=False),
    yaxis=dict(showgrid=True, gridcolor="#EEF2FF", gridwidth=1, showline=False, zeroline=False),
    hovermode="x unified",
)


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1rem 0 0.5rem 0;'>
        <p style='font-size:1.5rem;font-weight:900;color:#1E293B;margin:0;'>⚙️ Settings</p>
        <p style='font-size:0.85rem;color:#64748B;margin:0.2rem 0 0 0;font-weight:600;'>Adjust filters below</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("**🛍️ Primary Item (for detailed view)**")
    primary_item = st.selectbox("Select Item", ALL_ITEMS, label_visibility="collapsed")

    st.markdown("**📦 Compare Items**")
    selected_items = st.multiselect("Select Items", ALL_ITEMS, default=ALL_ITEMS[:6], label_visibility="collapsed")
    if not selected_items:
        selected_items = ALL_ITEMS[:6]

    st.markdown("**📅 Date Range**")
    min_date, max_date = master.index[0], master.index[-1]
    date_start, date_end = st.select_slider(
        "Date Range", options=master.index.tolist(),
        value=(min_date, max_date),
        format_func=lambda x: x.strftime("%b %Y"),
        label_visibility="collapsed",
    )

    st.markdown("**🔮 Months to Predict**")
    forecast_horizon = st.slider("Forecast Months", 3, 12, 6, label_visibility="collapsed")

    st.markdown("---")
    st.markdown("""
    <div style='background:#EFF6FF;border-radius:12px;padding:0.8rem;'>
        <p style='font-size:0.78rem;color:#1E40AF;font-weight:700;margin:0;'>ℹ️ Real data from Indian markets (2019–2023)</p>
    </div>
    """, unsafe_allow_html=True)


# ─── FILTER ──────────────────────────────────────────────────────────────────
df_filt = master.loc[date_start:date_end, [c for c in selected_items if c in master.columns]]
df_inflation = df_filt.pct_change(12) * 100


# ─── TOP BANNER ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="top-banner">
    <p class="banner-title">🛒 Price Watch Dashboard</p>
    <p class="banner-sub">Know today's prices · Plan your shopping · Manage your stock</p>
</div>
""", unsafe_allow_html=True)


# ─── MAIN TABS ───────────────────────────────────────────────────────────────
tabs = st.tabs(["🏠 Household Dashboard", "🏪 Shopkeeper Dashboard", "📊 Market Overview"])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — HOUSEHOLD DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="sec-header">🏠 Your Shopping Guide</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#64748B;font-size:1rem;font-weight:600;margin-top:-0.5rem;margin-bottom:1rem;'>"
        "See today's prices and decide the best time to buy</p>", unsafe_allow_html=True
    )

    # ── Price Cards ──────────────────────────────────────────────────────────
    show_items = [c for c in selected_items if c in df_filt.columns][:5]
    cols = st.columns(len(show_items)) if show_items else st.columns(1)

    for i, item in enumerate(show_items):
        s = df_filt[item].dropna()
        if len(s) < 2:
            continue
        latest  = s.iloc[-1]
        prev_12 = s.iloc[-13] if len(s) > 13 else s.iloc[0]
        prev_1  = s.iloc[-2]
        yoy = ((latest / prev_12) - 1) * 100 if prev_12 > 0 else 0
        mom = ((latest / prev_1)  - 1) * 100 if prev_1 > 0 else 0

        is_rising = yoy > 3
        bg, border, text_c = item_bg(item)
        clr = item_color(item)

        with cols[i]:
            st.markdown(f"""
            <div class="price-card" style="background:{bg};border:2px solid {border};">
                <div class="card-name">{item}</div>
                <div class="card-price" style="color:{text_c};">₹{latest:.1f}</div>
                <span class="card-change {'signal-red' if yoy > 3 else 'signal-green'}">
                    {'📈 +' if yoy > 0 else '📉 '}{yoy:.1f}% vs last year
                </span><br>
                <div class="card-advice {'signal-red' if is_rising else 'signal-green'}" style="margin-top:0.5rem;">
                    {'🔴 Prices Increasing' if is_rising else '🟢 Prices Decreasing'}
                </div>
                <div style="font-size:0.82rem;font-weight:700;color:{'#991B1B' if is_rising else '#065F46'};
                    background:{'#FEF2F2' if is_rising else '#ECFDF5'};
                    border-radius:10px;padding:0.3rem 0.6rem;margin-top:0.4rem;display:inline-block;">
                    {'⏳ Wait before buying' if is_rising else '✅ Good time to buy!'}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="bright-divider"></div>', unsafe_allow_html=True)

    # ── Price Trend for primary item ─────────────────────────────────────────
    pri = primary_item if primary_item in df_filt.columns else df_filt.columns[0]
    st.markdown(f'<div class="sec-header">📈 Price Trend — {pri}</div>', unsafe_allow_html=True)

    s_pri = df_filt[pri].dropna()
    clr_pri = item_color(pri)
    fill_pri = color_fill(pri)

    fig_hh = go.Figure()
    fig_hh.add_trace(go.Scatter(
        x=s_pri.index, y=s_pri.values,
        name=pri,
        line=dict(color=clr_pri, width=3),
        fill="tozeroy", fillcolor=fill_pri,
        hovertemplate="<b>%{x|%b %Y}</b><br>Price: ₹%{y:.1f}<extra></extra>",
    ))
    if len(s_pri) >= 3:
        ma3 = s_pri.rolling(3).mean()
        fig_hh.add_trace(go.Scatter(
            x=ma3.index, y=ma3.values, name="3-Month Average",
            line=dict(color="#94A3B8", width=2, dash="dash"),
            hovertemplate="Average: ₹%{y:.1f}<extra></extra>",
        ))
    fig_hh.update_layout(**CHART_LAYOUT, title=dict(text=f"Price History — {pri}", font=dict(size=14, family="Nunito", weight=700)), height=360, yaxis_title="Price (₹)")
    st.plotly_chart(fig_hh, use_container_width=True)

    if len(s_pri) > 3:
        prev_3m = s_pri.iloc[-4]
        chg_3m = ((s_pri.iloc[-1] / prev_3m) - 1) * 100 if prev_3m > 0 else 0
        tip = f"Prices {'went UP' if chg_3m > 0 else 'went DOWN'} by {abs(chg_3m):.1f}% in the last 3 months."
        if chg_3m > 5:
            tip += " 🔴 Prices are rising fast — consider buying essentials now or wait for prices to settle."
        elif chg_3m < -3:
            tip += " 🟢 Great time to stock up — prices are lower than usual!"
        else:
            tip += " 🟡 Prices are fairly stable right now."
        st.markdown(f'<div class="chart-tip">💡 {tip}</div>', unsafe_allow_html=True)

    # ── Best & Worst month to buy ─────────────────────────────────────────────
    st.markdown('<div class="sec-header">📅 Best Month to Buy</div>', unsafe_allow_html=True)
    monthly_avg = s_pri.groupby(s_pri.index.month).mean()
    month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    monthly_avg.index = [month_names[m-1] for m in monthly_avg.index]
    best_month, worst_month = monthly_avg.idxmin(), monthly_avg.idxmax()

    fig_month = go.Figure(go.Bar(
        x=monthly_avg.index.tolist(), y=monthly_avg.values,
        marker_color=["#22C55E" if m == best_month else ("#EF4444" if m == worst_month else clr_pri) for m in monthly_avg.index],
        hovertemplate="<b>%{x}</b><br>Avg Price: ₹%{y:.1f}<extra></extra>",
        text=[f"₹{v:.0f}" for v in monthly_avg.values], textposition="outside",
        textfont=dict(size=11, family="Nunito", color="#1E293B"),
    ))
    fig_month.update_layout(**CHART_LAYOUT, title=dict(text="Average Price by Month (Green = Cheapest, Red = Most Expensive)", font=dict(size=13, family="Nunito", weight=700)), height=300, yaxis_title="Avg Price (₹)", showlegend=False)
    st.plotly_chart(fig_month, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="insight-big signal-green">✅ <b>Buy in {best_month}</b> — usually the cheapest month for {pri}</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="insight-big signal-red">⚠️ <b>Avoid buying in {worst_month}</b> — usually the most expensive month</div>', unsafe_allow_html=True)

    # ── All items summary ─────────────────────────────────────────────────────
    st.markdown('<div class="bright-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-header">🧾 All Items — Quick Summary</div>', unsafe_allow_html=True)

    rows_html = ""
    for item in [c for c in selected_items if c in df_filt.columns]:
        s = df_filt[item].dropna()
        if len(s) < 2:
            continue
        latest  = s.iloc[-1]
        prev_12 = s.iloc[-13] if len(s) > 13 else s.iloc[0]
        yoy     = ((latest / prev_12) - 1) * 100 if prev_12 > 0 else 0
        signal  = "🔴 Rising" if yoy > 3 else ("🟢 Falling" if yoy < -1 else "🟡 Stable")
        advice  = "Wait" if yoy > 3 else ("Buy Now" if yoy < -1 else "OK to Buy")
        color   = "#991B1B" if yoy > 3 else ("#065F46" if yoy < -1 else "#92400E")
        bg_c    = "#FEF2F2" if yoy > 3 else ("#ECFDF5" if yoy < -1 else "#FFFBEB")
        rows_html += f"""<tr>
            <td>{item}</td>
            <td><b>₹{latest:.1f}</b></td>
            <td style='color:{color};background:{bg_c};border-radius:6px;padding:0.3rem 0.6rem;font-weight:700;'>
                {'↑' if yoy > 0 else '↓'} {abs(yoy):.1f}%
            </td>
            <td>{signal}</td>
            <td style='color:{color};font-weight:800;'>{advice}</td>
        </tr>"""

    st.markdown(f"""
    <table class="sum-table">
        <thead><tr><th>Item</th><th>Today's Price</th><th>Change vs Last Year</th><th>Status</th><th>Advice</th></tr></thead>
        <tbody>{rows_html}</tbody>
    </table>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — SHOPKEEPER DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="sec-header">🏪 Shopkeeper Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#64748B;font-size:1rem;font-weight:600;margin-top:-0.5rem;margin-bottom:1rem;'>"
        "Manage your stock smartly based on price trends</p>", unsafe_allow_html=True
    )

    # ── Stock Signal Cards ────────────────────────────────────────────────────
    st.markdown("### 📦 Stock Decisions — Right Now")
    show_shop = [c for c in selected_items if c in df_filt.columns][:5]
    shop_cols = st.columns(len(show_shop)) if show_shop else st.columns(1)

    for i, item in enumerate(show_shop):
        s = df_filt[item].dropna()
        if len(s) < 4:
            continue
        latest  = s.iloc[-1]
        prev_3  = s.iloc[-4] if len(s) > 3  else s.iloc[0]
        mom_3   = ((latest / prev_3) - 1) * 100 if prev_3 > 0 else 0
        bg, border, text_c = item_bg(item)

        if mom_3 > 3:
            demand_msg = "📈 Demand likely to INCREASE"
            stock_msg  = "📦 Increase your stock!"
            stock_cls  = "signal-green"
            border_col = "#22C55E"
        elif mom_3 < -3:
            demand_msg = "📉 Demand likely to DECREASE"
            stock_msg  = "📦 Reduce your stock"
            stock_cls  = "signal-orange"
            border_col = "#F97316"
        else:
            demand_msg = "➡️ Demand will stay the same"
            stock_msg  = "📦 Keep current stock"
            stock_cls  = "signal-blue"
            border_col = "#3B82F6"

        with shop_cols[i]:
            st.markdown(f"""
            <div class="price-card" style="border-left:5px solid {border_col};background:{bg};">
                <div class="card-name">{item}</div>
                <div class="card-price" style="color:{text_c};font-size:1.6rem;">₹{latest:.1f}</div>
                <div style="font-size:0.8rem;font-weight:700;color:#64748B;">3-month change:
                    <span style="color:{'#991B1B' if mom_3 > 0 else '#065F46'};font-weight:800;">
                        {'↑' if mom_3 > 0 else '↓'} {abs(mom_3):.1f}%
                    </span>
                </div>
                <div class="card-advice {stock_cls}" style="margin-top:0.5rem;font-size:0.78rem;">{demand_msg}</div>
                <div class="card-advice {stock_cls}" style="font-size:0.82rem;margin-top:0.3rem;font-weight:800;">{stock_msg}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="bright-divider"></div>', unsafe_allow_html=True)

    # ── Price Trend for Shopkeepers ───────────────────────────────────────────
    pri_shop = primary_item if primary_item in df_filt.columns else df_filt.columns[0]
    st.markdown(f'<div class="sec-header">📈 Price Trend — {pri_shop}</div>', unsafe_allow_html=True)

    s_shop  = df_filt[pri_shop].dropna()
    clr_shop = item_color(pri_shop)
    fill_shop = color_fill(pri_shop)

    fig_shop = go.Figure()
    fig_shop.add_trace(go.Scatter(
        x=s_shop.index, y=s_shop.values, name="Actual Price",
        line=dict(color=clr_shop, width=3),
        hovertemplate="<b>%{x|%b %Y}</b><br>₹%{y:.1f}<extra></extra>",
    ))
    if len(s_shop) >= 6:
        ma6 = s_shop.rolling(6).mean()
        fig_shop.add_trace(go.Scatter(
            x=ma6.index, y=ma6.values, name="6-Month Average",
            line=dict(color="#94A3B8", width=2, dash="dot"),
            hovertemplate="6M Avg: ₹%{y:.1f}<extra></extra>",
        ))
    fig_shop.update_layout(**CHART_LAYOUT, title=dict(text=f"Price Trend — {pri_shop}", font=dict(size=13, family="Nunito", weight=700)), height=360, yaxis_title="Price (₹)")
    st.plotly_chart(fig_shop, use_container_width=True)

    if len(s_shop) > 6:
        prev_6m = s_shop.iloc[-7]
        chg_6m  = ((s_shop.iloc[-1] / prev_6m) - 1) * 100 if prev_6m > 0 else 0
        tip_shop = f"Prices {'increased' if chg_6m > 0 else 'decreased'} by {abs(chg_6m):.1f}% in the last 6 months."
        tip_shop += " Keep an eye on seasonal changes — prices often rise during Oct–Nov festive season."
        st.markdown(f'<div class="chart-tip">💡 {tip_shop}</div>', unsafe_allow_html=True)

    # ── Price Forecast ────────────────────────────────────────────────────────
    st.markdown('<div class="bright-divider"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sec-header">🔮 Future Price Prediction — next {forecast_horizon} months</div>', unsafe_allow_html=True)

    @st.cache_data
    def run_forecast(series_key, n_forecast):
        from sklearn.ensemble import RandomForestRegressor
        s = master[series_key].dropna()

        def make_features(series):
            d = pd.DataFrame({"price": series})
            for lag in [1, 2, 3, 6]:
                d[f"lag_{lag}"] = d["price"].shift(lag)
            d["month"]     = series.index.month
            d["year"]      = series.index.year
            d["rolling_3"] = d["price"].shift(1).rolling(3).mean()
            d["rolling_6"] = d["price"].shift(1).rolling(6).mean()
            return d.dropna()

        feat = make_features(s)
        fcols = [c for c in feat.columns if c != "price"]
        X, y  = feat[fcols], feat["price"]

        if len(X) < 10:
            return None, s

        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X, y)

        last_vals  = s.values.tolist()
        preds, last_year, last_month = [], s.index[-1].year, s.index[-1].month
        for _ in range(n_forecast):
            last_month += 1
            if last_month > 12: last_month = 1; last_year += 1
            row = {
                "lag_1":     last_vals[-1], "lag_2": last_vals[-2] if len(last_vals)>1 else last_vals[-1],
                "lag_3":     last_vals[-3] if len(last_vals)>2 else last_vals[-1],
                "lag_6":     last_vals[-6] if len(last_vals)>5 else last_vals[-1],
                "month":     last_month, "year": last_year,
                "rolling_3": np.mean(last_vals[-3:]), "rolling_6": np.mean(last_vals[-6:]),
            }
            pred = rf.predict([[row[f] for f in fcols]])[0]
            preds.append(pred)
            last_vals.append(pred)

        future_idx = pd.date_range(s.index[-1] + pd.DateOffset(months=1), periods=n_forecast, freq="MS")
        return pd.Series(preds, index=future_idx), s

    with st.spinner("⏳ Calculating future prices..."):
        fc_series, s_hist_fc = run_forecast(pri_shop, forecast_horizon)

    if fc_series is not None:
        fc_chg = ((fc_series.iloc[-1] / fc_series.iloc[0]) - 1) * 100 if fc_series.iloc[0] > 0 else 0
        hist_recent = s_hist_fc.iloc[-18:]

        fig_fc = go.Figure()
        fig_fc.add_trace(go.Scatter(x=hist_recent.index, y=hist_recent.values, name="Past Prices", line=dict(color="#64748B", width=2.5), hovertemplate="Actual: ₹%{y:.1f}<extra></extra>"))
        fig_fc.add_trace(go.Scatter(x=fc_series.index, y=fc_series.values, name="Predicted Price", line=dict(color=item_color(pri_shop), width=3, dash="dash"), hovertemplate="Predicted: ₹%{y:.1f}<extra></extra>"))
        fig_fc.add_trace(go.Scatter(
            x=list(fc_series.index) + list(fc_series.index[::-1]),
            y=list(fc_series.values * 1.05) + list(fc_series.values[::-1] * 0.95),
            fill="toself", fillcolor=color_fill(pri_shop), line=dict(color="rgba(0,0,0,0)"),
            name="Price Range", showlegend=True, hoverinfo="skip",
        ))
        fig_fc.update_layout(**CHART_LAYOUT, title=dict(text=f"Price Prediction — Next {forecast_horizon} Months for {pri_shop}", font=dict(size=13, family="Nunito", weight=700)), height=380, yaxis_title="Price (₹)")
        st.plotly_chart(fig_fc, use_container_width=True)

        fc_verdict = "📈 Prices may RISE" if fc_chg > 2 else ("📉 Prices may FALL" if fc_chg < -2 else "➡️ Prices should stay STABLE")
        fc_action  = "Increase your stock now before prices go up!" if fc_chg > 2 else ("Reduce stock or wait — prices may go lower." if fc_chg < -2 else "Maintain your current stock levels.")
        fc_cls     = "signal-red" if fc_chg > 2 else ("signal-green" if fc_chg < -2 else "signal-blue")

        st.markdown(f"""
        <div class="insight-big {fc_cls}" style="padding:1.2rem 1.5rem;border-radius:16px;margin:0.5rem 0;">
            <p style="font-size:1.1rem;font-weight:900;margin:0 0 0.4rem 0;">{fc_verdict}</p>
            <p style="font-size:0.95rem;font-weight:700;margin:0;">
                Predicted change: {'↑' if fc_chg > 0 else '↓'} {abs(fc_chg):.1f}% over {forecast_horizon} months<br>
                👉 {fc_action}
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Not enough data to generate a forecast for this item.")

    # ── Stock Decision Table ──────────────────────────────────────────────────
    st.markdown('<div class="bright-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-header">📋 Full Stock Decision Guide</div>', unsafe_allow_html=True)

    shop_rows = ""
    for item in [c for c in selected_items if c in df_filt.columns]:
        s = df_filt[item].dropna()
        if len(s) < 4:
            continue
        latest  = s.iloc[-1]
        prev_3  = s.iloc[-4] if len(s) > 3  else s.iloc[0]
        prev_12 = s.iloc[-13] if len(s) > 13 else s.iloc[0]
        mom     = ((latest / prev_3)  - 1) * 100 if prev_3 > 0 else 0
        yoy     = ((latest / prev_12) - 1) * 100 if prev_12 > 0 else 0
        demand  = "↑ Likely UP"   if mom > 2  else ("↓ Likely DOWN" if mom < -2 else "→ Stable")
        stock   = "📦 Increase"   if mom > 2  else ("📦 Reduce" if mom < -2 else "📦 Maintain")
        color   = "#065F46"       if mom > 2  else ("#991B1B" if mom < -2 else "#92400E")
        bg_c    = "#ECFDF5"       if mom > 2  else ("#FEF2F2" if mom < -2 else "#FFFBEB")
        shop_rows += f"""<tr>
            <td>{item}</td>
            <td><b>₹{latest:.1f}</b></td>
            <td style="color:{'#991B1B' if mom>0 else '#065F46'};font-weight:700;">{'↑' if mom>0 else '↓'} {abs(mom):.1f}%</td>
            <td style="color:{'#991B1B' if yoy>0 else '#065F46'};font-weight:700;">{'↑' if yoy>0 else '↓'} {abs(yoy):.1f}%</td>
            <td style="color:{color};background:{bg_c};font-weight:700;border-radius:6px;padding:0.3rem 0.5rem;">{demand}</td>
            <td style="color:{color};font-weight:800;">{stock}</td>
        </tr>"""

    st.markdown(f"""
    <table class="sum-table">
        <thead><tr><th>Item</th><th>Current Price</th><th>3-Month Change</th><th>Yearly Change</th><th>Customer Demand</th><th>Stock Action</th></tr></thead>
        <tbody>{shop_rows}</tbody>
    </table>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="chart-tip">💡 <b>Tip:</b> Oct–Nov is festive season — stock up in September for vegetables, grocery, and cooking oil. Prices usually go UP during this period.</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — MARKET OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="sec-header">📊 Market Overview</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#64748B;font-size:1rem;font-weight:600;margin-top:-0.5rem;margin-bottom:1rem;'>"
        "See how all items compare — find what's expensive and what's stable</p>", unsafe_allow_html=True
    )

    valid_items = [c for c in selected_items if c in df_filt.columns and len(df_filt[c].dropna()) >= 13]

    # ── Key market metrics ────────────────────────────────────────────────────
    if valid_items:
        yoy_all = {}
        vol_all = {}
        for item in valid_items:
            s = df_filt[item].dropna()
            prev_12 = s.iloc[-13] if len(s) > 13 else s.iloc[0]
            yoy_all[item] = ((s.iloc[-1] / prev_12) - 1) * 100 if prev_12 > 0 else 0
            vol_all[item] = s.pct_change().std() * 100

        most_exp    = max(yoy_all, key=yoy_all.get)
        most_vol    = max(vol_all, key=vol_all.get)
        most_stable = min(vol_all, key=vol_all.get)

        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div class="price-card signal-red" style="text-align:center;border-radius:18px;padding:1.3rem;">
                <div style="font-size:0.8rem;font-weight:700;text-transform:uppercase;color:#64748B;margin:0.3rem 0;">🔴 Most Expensive</div>
                <div style="font-size:1.4rem;font-weight:900;color:#991B1B;">{most_exp}</div>
                <div style="font-size:0.9rem;font-weight:700;color:#991B1B;">↑ {yoy_all[most_exp]:.1f}% vs last year</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="price-card signal-orange" style="text-align:center;border-radius:18px;padding:1.3rem;">
                <div style="font-size:0.8rem;font-weight:700;text-transform:uppercase;color:#64748B;margin:0.3rem 0;">⚡ Most Unpredictable</div>
                <div style="font-size:1.4rem;font-weight:900;color:#92400E;">{most_vol}</div>
                <div style="font-size:0.9rem;font-weight:700;color:#92400E;">Price changes a lot</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="price-card signal-green" style="text-align:center;border-radius:18px;padding:1.3rem;">
                <div style="font-size:0.8rem;font-weight:700;text-transform:uppercase;color:#64748B;margin:0.3rem 0;">✅ Most Stable</div>
                <div style="font-size:1.4rem;font-weight:900;color:#065F46;">{most_stable}</div>
                <div style="font-size:0.9rem;font-weight:700;color:#065F46;">Price stays predictable</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="bright-divider"></div>', unsafe_allow_html=True)

        # ── Inflation Trend ───────────────────────────────────────────────────
        st.markdown('<div class="sec-header">📈 Overall Price Rise (vs Last Year)</div>', unsafe_allow_html=True)

        fig_ov = go.Figure()
        for item in valid_items:
            s_infl = df_inflation[item].dropna()
            clr = item_color(item)
            fig_ov.add_trace(go.Scatter(
                x=s_infl.index, y=s_infl.values, name=item,
                line=dict(color=clr, width=2.5),
                fill="tozeroy", fillcolor=color_fill(item),
                hovertemplate=f"<b>{item}</b><br>%{{x|%b %Y}}<br>Price rise: %{{y:.1f}}%<extra></extra>",
            ))
        fig_ov.add_hline(y=0, line_color="#CBD5E1", line_width=2)
        fig_ov.add_hline(y=6, line_dash="dash", line_color="#EF4444",
                         annotation_text="⚠️ High inflation (6%)",
                         annotation_font=dict(size=11, color="#EF4444", family="Nunito"))
        fig_ov.update_layout(**CHART_LAYOUT, title=dict(text="How much have prices risen vs same month last year? (%)", font=dict(size=13, family="Nunito", weight=700)), height=380, yaxis_title="Price Rise (%)")
        st.plotly_chart(fig_ov, use_container_width=True)

        avg_inflations = {c: df_inflation[c].dropna().iloc[-6:].mean() for c in valid_items}
        if avg_inflations:
            highest = max(avg_inflations, key=avg_inflations.get)
            lowest  = min(avg_inflations, key=avg_inflations.get)
            st.markdown(f'<div class="chart-tip">💡 Recently: <b>{highest}</b> prices rose the most (<b>+{avg_inflations[highest]:.1f}%</b>). <b>{lowest}</b> was the most stable with <b>{avg_inflations[lowest]:.1f}%</b> change.</div>', unsafe_allow_html=True)

        # ── Bar Comparison ────────────────────────────────────────────────────
        st.markdown('<div class="bright-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-header">⚖️ Compare All Items — Price Rise This Year</div>', unsafe_allow_html=True)

        bar_vals   = [yoy_all[c] for c in valid_items]
        bar_labels = valid_items
        bar_colors = [item_color(c) for c in valid_items]

        fig_bar = go.Figure(go.Bar(
            x=bar_labels, y=bar_vals, marker_color=bar_colors,
            text=[f"{'↑' if v > 0 else '↓'} {abs(v):.1f}%" for v in bar_vals],
            textposition="outside", textfont=dict(size=13, family="Nunito", color="#1E293B"),
            hovertemplate="<b>%{x}</b><br>Price rise: %{y:.1f}%<extra></extra>",
        ))
        fig_bar.add_hline(y=0, line_color="#CBD5E1", line_width=2)
        fig_bar.update_layout(**CHART_LAYOUT, title=dict(text="Which item's price rose the most vs last year?", font=dict(size=13, family="Nunito", weight=700)), height=340, yaxis_title="Price Change (%)", showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

        # ── Category Summary ──────────────────────────────────────────────────
        st.markdown('<div class="bright-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-header">🗂️ Category Summary</div>', unsafe_allow_html=True)

        def cat_avg(keys):
            vals = [yoy_all[k] for k in keys if k in yoy_all]
            return np.mean(vals) if vals else 0

        veg_yoy  = cat_avg([k for k in veg_keys  if k in valid_items])
        groc_yoy = cat_avg([k for k in groc_keys if k in valid_items])
        fuel_yoy = cat_avg([k for k in fuel_keys if k in valid_items])

        cat_data = [
            ("🥬 Vegetables", veg_yoy,  "#22C55E", "#F0FDF4", "#14532D"),
            ("🛒 Grocery",    groc_yoy, "#3B82F6", "#EFF6FF", "#1E3A8A"),
            ("⛽ Fuel",       fuel_yoy, "#F97316", "#FFF7ED", "#7C2D12"),
        ]
        cc = st.columns(3)
        for i, (label, yoy, clr, bg, tc) in enumerate(cat_data):
            with cc[i]:
                arrow = "📈 +" if yoy > 0 else "📉 "
                sig   = "signal-red" if yoy > 5 else ("signal-green" if yoy < 0 else "signal-orange")
                st.markdown(f"""
                <div class="price-card" style="background:{bg};border:2px solid {clr}44;text-align:center;">
                    <div style="font-size:1.1rem;font-weight:900;color:{tc};margin-bottom:0.5rem;">{label}</div>
                    <div style="font-size:1.8rem;font-weight:900;color:{clr};">{arrow}{abs(yoy):.1f}%</div>
                    <div class="card-advice {sig}" style="margin-top:0.5rem;">vs last year average</div>
                </div>
                """, unsafe_allow_html=True)

    else:
        st.info("Select more items and a wider date range to see market overview.")

    # ── Download ──────────────────────────────────────────────────────────────
    st.markdown('<div class="bright-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-header">📥 Download Data</div>', unsafe_allow_html=True)

    dcol1, dcol2 = st.columns(2)
    with dcol1:
        st.download_button("📊 Download Price Data (CSV)", df_filt.to_csv(), "commodity_prices.csv", "text/csv", use_container_width=True)
    with dcol2:
        st.download_button("📈 Download Inflation Data (CSV)", df_inflation.dropna().to_csv(), "inflation_rates.csv", "text/csv", use_container_width=True)


# ─── FOOTER ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="bright-divider"></div>
<div style="text-align:center;padding:0.8rem 0 0.5rem 0;">
    <p style="font-size:0.85rem;font-weight:700;color:#94A3B8;margin:0;">
        🛒 Price Watch Dashboard &nbsp;·&nbsp; Real Indian Market Data (2019–2023) &nbsp;·&nbsp; For households & shopkeepers
    </p>
</div>
""", unsafe_allow_html=True)
