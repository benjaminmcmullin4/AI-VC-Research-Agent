"""Agentic Marketing and Company Growth — Main App Entry Point."""

from __future__ import annotations

import streamlit as st

from ai_engine import get_api_key
from config import APP_NAME, APP_SUBTITLE, SIDEBAR_PAGES
from data.mock_data import compute_dashboard_metrics, load_all_data

# ── Page config ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_NAME,
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load CSS ─────────────────────────────────────────────────────────────
with open("styles/custom.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Load data ────────────────────────────────────────────────────────────
data = load_all_data()
metrics = compute_dashboard_metrics(data)
api_key = get_api_key()

# ── Sidebar ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### {APP_NAME}")
    st.markdown(f'<div style="color:#888;font-size:0.82rem;margin-top:-10px;margin-bottom:20px">{APP_SUBTITLE}</div>', unsafe_allow_html=True)

    page_labels = [label for label, _ in SIDEBAR_PAGES]
    page_keys = [key for _, key in SIDEBAR_PAGES]

    selected_label = st.radio(
        "Navigation",
        page_labels,
        key="nav",
        label_visibility="collapsed",
    )
    selected_page = page_keys[page_labels.index(selected_label)]

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    st.markdown("---")

    # API status
    if api_key:
        st.markdown('<div style="display:flex;align-items:center;gap:6px;font-size:0.78rem;color:#1ABC9C"><div style="width:8px;height:8px;border-radius:50%;background:#1ABC9C"></div> Live — AI features active</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="display:flex;align-items:center;gap:6px;font-size:0.78rem;color:#777"><div style="width:8px;height:8px;border-radius:50%;background:#777"></div> Demo Mode</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.72rem;color:#555;margin-top:4px">Add ANTHROPIC_API_KEY for AI features</div>', unsafe_allow_html=True)

# ── Demo mode banner ─────────────────────────────────────────────────────
if not api_key:
    st.markdown('<div class="demo-banner">Running in demo mode with sample data. Add your Anthropic API key to enable AI-powered insights and recommendations.</div>', unsafe_allow_html=True)

# ── Page routing ─────────────────────────────────────────────────────────
if selected_page == "dashboard":
    from pages.dashboard import render_dashboard
    render_dashboard(data, metrics, api_key)

elif selected_page == "discovery":
    from pages.discovery import render_discovery
    render_discovery(data, api_key)

elif selected_page == "recommendations":
    from pages.recommendations import render_recommendations
    render_recommendations(data, api_key)

elif selected_page == "outreach":
    from pages.outreach import render_outreach
    render_outreach(data, api_key)

elif selected_page == "pipeline":
    from pages.pipeline import render_pipeline
    render_pipeline(data)

elif selected_page == "analytics":
    from pages.analytics import render_analytics
    render_analytics(data, metrics)

elif selected_page == "activity":
    from pages.activity import render_activity
    render_activity(data)
