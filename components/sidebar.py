"""Sidebar controls for research configuration."""

from __future__ import annotations

import streamlit as st

from config import DEPTH_PRESETS, FIRM_NAME, GEOGRAPHY_OPTIONS, STAGE_OPTIONS
from db import list_runs, load_run


def render_sidebar() -> dict:
    """Render sidebar controls and return the current settings dict."""
    st.sidebar.markdown(
        f'<div style="text-align: center; padding: 0.5rem 0 1rem 0;">'
        f'<span style="color: #FFFFFF; font-size: 1.2rem; font-weight: 700; '
        f'letter-spacing: 0.05em;">{FIRM_NAME}</span><br>'
        f'<span style="color: #999; font-size: 0.75rem;">Market Research Platform</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")

    # Show auth status
    from auth import get_auth_email
    auth_email = get_auth_email()
    if auth_email:
        st.sidebar.markdown(
            f'<div style="background: rgba(26,188,156,0.15); padding: 0.4rem 0.8rem; '
            f'border-radius: 6px; font-size: 0.8rem; color: #1ABC9C; margin-bottom: 0.5rem;">'
            f'Authenticated as <strong>{auth_email}</strong></div>',
            unsafe_allow_html=True,
        )

    st.sidebar.markdown("## Research Settings")

    # Depth preset
    depth = st.sidebar.selectbox(
        "Analysis Depth",
        options=list(DEPTH_PRESETS.keys()),
        format_func=lambda k: DEPTH_PRESETS[k]["label"],
        index=1,
    )
    preset = DEPTH_PRESETS[depth]

    st.sidebar.markdown("---")

    # Advanced settings in expander
    with st.sidebar.expander("Advanced Settings", expanded=False):
        company_count = st.slider(
            "Company count",
            min_value=10,
            max_value=25,
            value=preset["company_count"],
        )
        temperature = st.slider(
            "Temperature",
            min_value=0.3,
            max_value=0.9,
            value=preset["temperature"],
            step=0.1,
        )
        output_style = st.radio(
            "Output style",
            options=["Concise", "Detailed"],
            index=0 if preset["detail_level"] == "concise" else 1,
        )

    st.sidebar.markdown("---")

    # Past runs
    st.sidebar.markdown("## Past Research")
    runs = list_runs()
    loaded_run = None
    if runs:
        run_labels = {r["id"]: f"{r['query'][:40]}  ({r['created_at'][:10]})" for r in runs}
        selected_id = st.sidebar.selectbox(
            "Load previous run",
            options=[None] + list(run_labels.keys()),
            format_func=lambda x: "— New Research —" if x is None else run_labels[x],
        )
        if selected_id is not None:
            loaded_run = load_run(selected_id)
    else:
        st.sidebar.caption("No past research runs yet.")

    return {
        "depth": depth,
        "detail_level": output_style.lower(),
        "company_count": company_count,
        "temperature": temperature,
        "loaded_run": loaded_run,
    }
