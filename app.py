"""Influx — Influencer Intelligence Platform."""

from __future__ import annotations

import streamlit as st

from ai_engine import get_api_key
from config import APP_NAME, APP_SUBTITLE, COLORS, SIDEBAR_PAGES
from data.mock_data import compute_dashboard_metrics, load_all_data

# ── Page config ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_NAME,
    page_icon="⚡",
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
    # Brand
    st.markdown(f"""
    <div style="padding:8px 0 20px">
        <div style="font-size:24px;font-weight:800;letter-spacing:-0.02em">
            <span style="background:linear-gradient(135deg,{COLORS["primary"]},{COLORS["secondary"]});
                -webkit-background-clip:text;-webkit-text-fill-color:transparent">⚡ {APP_NAME}</span>
        </div>
        <div style="font-size:12px;color:{COLORS["text_muted"]};margin-top:2px;letter-spacing:0.04em;text-transform:uppercase">{APP_SUBTITLE}</div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation
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
    st.markdown(f"<hr style='border-color:{COLORS['border']}'>", unsafe_allow_html=True)

    # API status
    if api_key:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;font-size:12px;color:{COLORS["success"]};padding:8px 0">
            <div style="width:8px;height:8px;border-radius:50%;background:{COLORS["success"]}"></div>
            Live — AI features enabled
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;font-size:12px;color:{COLORS["text_muted"]};padding:8px 0">
            <div style="width:8px;height:8px;border-radius:50%;background:{COLORS["text_muted"]}"></div>
            Demo Mode
        </div>
        <div style="font-size:11px;color:{COLORS["text_muted"]};opacity:0.6">Add ANTHROPIC_API_KEY for AI</div>
        """, unsafe_allow_html=True)

# ── Demo banner ──────────────────────────────────────────────────────────
if not api_key:
    st.markdown(
        '<div class="demo-banner">Running in demo mode with sample data. Add your API key for AI-powered insights.</div>',
        unsafe_allow_html=True,
    )

# ── Page routing ─────────────────────────────────────────────────────────
if selected_page == "dashboard":
    from pages.dashboard import render_dashboard
    render_dashboard(data, metrics, api_key)

elif selected_page == "find":
    from pages.find import render_find
    render_find(data, api_key)

elif selected_page == "outreach_pipeline":
    from pages.outreach_pipeline import render_outreach_pipeline
    render_outreach_pipeline(data, metrics, api_key)
