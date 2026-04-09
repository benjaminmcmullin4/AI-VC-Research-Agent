"""Influx — AI-Powered Influencer Acquisition."""

from __future__ import annotations

import streamlit as st

from ai_engine import get_api_key
from config import APP_NAME, APP_SUBTITLE, COLORS, SIDEBAR_PAGES
from data.mock_data import compute_dashboard_metrics, load_all_data

# ── Page config ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_NAME,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load CSS + Icons ─────────────────────────────────────────────────────
with open("styles/custom.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">',
    unsafe_allow_html=True,
)

# ── Session state defaults ───────────────────────────────────────────────
if "campaign_configured" not in st.session_state:
    st.session_state["campaign_configured"] = False
    st.session_state["campaign_name"] = ""
    st.session_state["campaign_target"] = 10
    st.session_state["campaign_niches"] = []
    st.session_state["campaign_platforms"] = []
    st.session_state["campaign_budget"] = 50_000

# ── Load data (simulation or static) ────────────────────────────────────
sim = st.session_state.get("sim")
if sim and sim.get("active"):
    from simulation.engine import get_simulation_data
    data = get_simulation_data(sim)
else:
    data = load_all_data()
metrics = compute_dashboard_metrics(data)
api_key = get_api_key()

# ── Sidebar ──────────────────────────────────────────────────────────────
with st.sidebar:
    # Brand header
    st.markdown(f"""
    <div style="padding:20px 16px 24px;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:8px">
        <div style="display:flex;align-items:center;gap:10px">
            <div style="width:32px;height:32px;border-radius:8px;background:linear-gradient(135deg,#6366F1,#4F46E5);
                display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:800;color:white;
                box-shadow:0 2px 8px rgba(79,70,229,0.3)">I</div>
            <div>
                <div style="font-size:18px;font-weight:700;color:#F1F5F9;letter-spacing:-0.02em">{APP_NAME}</div>
                <div style="font-size:10px;color:#64748B;letter-spacing:0.08em;text-transform:uppercase;margin-top:1px">{APP_SUBTITLE}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation
    _NAV_ICONS = {"Campaign": "\u00a0\u00a0\U0001F680", "Influencers": "\u00a0\u00a0\U0001F465", "Conversations": "\u00a0\u00a0\U0001F4AC", "Analytics": "\u00a0\u00a0\U0001F4C8"}
    page_labels = [label for label, _ in SIDEBAR_PAGES]
    page_keys = [key for _, key in SIDEBAR_PAGES]
    display_labels = [f"{icon}{label}" for label, icon in [(l, _NAV_ICONS.get(l, "")) for l in page_labels]]

    selected_display = st.radio(
        "Navigation",
        display_labels,
        key="nav",
        label_visibility="collapsed",
    )
    selected_page = page_keys[display_labels.index(selected_display)]

    st.markdown("<hr style='border-color:rgba(255,255,255,0.06);margin:16px 0 12px'>", unsafe_allow_html=True)

    # ── Simulation controls in sidebar ───────────────────────────────
    if sim and sim.get("active"):
        from simulation.engine import advance_day, advance_days
        from simulation.budget_tracker import budget_summary

        day = sim["day"]
        budget_info = budget_summary(sim)
        day_pct = min(100, day / 180 * 100)

        st.markdown(f"""
        <div style="padding:16px;margin:0 8px;background:rgba(255,255,255,0.03);border-radius:10px;
            border:1px solid rgba(255,255,255,0.06)">
            <div style="font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;
                color:#64748B;margin-bottom:12px">Simulation</div>
            <div style="display:flex;align-items:baseline;gap:8px;margin-bottom:4px">
                <div style="font-size:28px;font-weight:800;color:#F1F5F9;letter-spacing:-0.02em">Day {day}</div>
                <div style="font-size:13px;color:#64748B">of 180</div>
            </div>
            <div style="font-size:12px;color:#64748B;margin-bottom:4px">
                ${budget_info['remaining']:,.0f} remaining
            </div>
            <div style="height:3px;background:rgba(255,255,255,0.06);border-radius:2px;margin-top:8px;overflow:hidden">
                <div style="height:100%;width:{day_pct:.0f}%;background:linear-gradient(90deg,#6366F1,#4F46E5);
                    border-radius:2px"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Next Day", key="sim_next_1", use_container_width=True):
                advance_day(sim)
                st.rerun()
        with col_b:
            if st.button("+7 Days", key="sim_next_7", use_container_width=True):
                advance_days(sim, 7)
                st.rerun()
        if st.button("+30 Days", key="sim_next_30", use_container_width=True):
            advance_days(sim, 30)
            st.rerun()

        st.markdown("<hr style='border-color:rgba(255,255,255,0.06);margin:16px 0 12px'>", unsafe_allow_html=True)

    # ── API status ───────────────────────────────────────────────────
    if api_key:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;font-size:12px;
            padding:12px 16px;margin:0 8px">
            <div style="width:7px;height:7px;border-radius:50%;background:#10B981;
                box-shadow:0 0 6px rgba(16,185,129,0.4)"></div>
            <span style="color:#CBD5E1">AI engine connected</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;font-size:12px;color:#64748B;
            padding:12px 16px;margin:0 8px">
            <div style="width:7px;height:7px;border-radius:50%;background:#475569"></div>
            <span>Demo mode</span>
        </div>
        """, unsafe_allow_html=True)

# ── Page routing ─────────────────────────────────────────────────────────
if selected_page == "campaign":
    from pages.dashboard import render_campaign
    render_campaign(data, metrics, api_key)

elif selected_page == "influencers":
    from pages.influencers import render_influencers
    render_influencers(data, api_key)

elif selected_page == "conversations":
    from pages.conversations import render_conversations
    render_conversations(data, api_key)

elif selected_page == "analytics":
    from pages.analytics import render_analytics
    render_analytics(data, metrics)
