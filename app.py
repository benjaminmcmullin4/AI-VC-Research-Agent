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

# ── Load CSS ─────────────────────────────────────────────────────────────
with open("styles/custom.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Session state defaults ───────────────────────────────────────────────
if "campaign_configured" not in st.session_state:
    st.session_state["campaign_configured"] = False
    st.session_state["campaign_name"] = ""
    st.session_state["campaign_target"] = 10
    st.session_state["campaign_niches"] = []
    st.session_state["campaign_platforms"] = []

# ── Load data ────────────────────────────────────────────────────────────
data = load_all_data()
metrics = compute_dashboard_metrics(data)
api_key = get_api_key()

# ── Sidebar ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:8px 0 20px">
        <div style="font-size:22px;font-weight:800;color:#F1F5F9;letter-spacing:-0.02em">{APP_NAME}</div>
        <div style="font-size:11px;color:{COLORS["text_muted"]};margin-top:2px;letter-spacing:0.06em;text-transform:uppercase">{APP_SUBTITLE}</div>
    </div>
    """, unsafe_allow_html=True)

    page_labels = [label for label, _ in SIDEBAR_PAGES]
    page_keys = [key for _, key in SIDEBAR_PAGES]

    selected_label = st.radio(
        "Navigation",
        page_labels,
        key="nav",
        label_visibility="collapsed",
    )
    selected_page = page_keys[page_labels.index(selected_label)]

    st.markdown(f"<hr style='border-color:rgba(255,255,255,0.08);margin:24px 0 12px'>", unsafe_allow_html=True)

    if api_key:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;font-size:12px;color:{COLORS["success"]};padding:8px 0">
            <div style="width:6px;height:6px;border-radius:50%;background:{COLORS["success"]}"></div>
            AI enabled
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;font-size:12px;color:{COLORS["text_muted"]};padding:8px 0">
            <div style="width:6px;height:6px;border-radius:50%;background:{COLORS["text_muted"]}"></div>
            Demo mode
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
