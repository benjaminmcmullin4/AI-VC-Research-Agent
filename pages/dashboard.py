"""Campaign — setup + AI cycle dashboard."""

from __future__ import annotations

import streamlit as st

from components import activity_item, metric_card, pipeline_bar, progress_bar_html, section_label
from config import COLORS, NICHES, PLATFORMS
from data.mock_data import compute_cycle_metrics


def _render_setup():
    """Campaign setup form shown on first visit."""
    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center;max-width:520px;margin:0 auto 40px">
        <div style="font-size:28px;font-weight:800;color:{COLORS["text"]};margin-bottom:8px">Launch a Campaign</div>
        <div style="font-size:15px;color:{COLORS["text_sec"]};line-height:1.6">
            Tell the AI what you need. It will find the best creators,
            reach out automatically, and fill your roster.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_pad_l, col_form, col_pad_r = st.columns([1, 2, 1])
    with col_form:
        name = st.text_input("Campaign Name", value="Q2 Creator Campaign", key="setup_name")
        target = st.number_input("How many influencers do you want?", min_value=3, max_value=25, value=10, step=1, key="setup_target")
        niches = st.multiselect("Preferred Niches", NICHES, default=[], key="setup_niches",
                                help="Leave empty for all niches")
        platforms = st.multiselect("Preferred Platforms", PLATFORMS, default=[], key="setup_platforms",
                                   help="Leave empty for all platforms")

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        if st.button("Launch Campaign", type="primary", use_container_width=True):
            st.session_state["campaign_configured"] = True
            st.session_state["campaign_name"] = name
            st.session_state["campaign_target"] = int(target)
            st.session_state["campaign_niches"] = niches
            st.session_state["campaign_platforms"] = platforms
            st.rerun()


def _render_cycle(data: dict, metrics: dict, api_key: str | None):
    """Cycle dashboard shown after campaign is configured."""
    name = st.session_state.get("campaign_name", "Campaign")
    target = st.session_state.get("campaign_target", 10)
    niches = st.session_state.get("campaign_niches", [])
    platforms = st.session_state.get("campaign_platforms", [])

    cycle = compute_cycle_metrics(data, target, niches, platforms)

    # Header
    col_title, col_edit = st.columns([4, 1])
    with col_title:
        st.markdown(f'<h1 style="font-size:28px;font-weight:700;margin-bottom:0">{name}</h1>', unsafe_allow_html=True)
        filters_desc = []
        if niches:
            filters_desc.append(", ".join(niches))
        if platforms:
            filters_desc.append(", ".join(platforms))
        sub = " · ".join(filters_desc) if filters_desc else "All niches and platforms"
        st.markdown(f'<div style="font-size:14px;color:{COLORS["text_sec"]};margin-bottom:16px">{sub}</div>', unsafe_allow_html=True)
    with col_edit:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("Edit Campaign", key="edit_campaign"):
            st.session_state["campaign_configured"] = False
            st.rerun()

    # Progress
    st.markdown(progress_bar_html(cycle["onboarded"], cycle["target"]), unsafe_allow_html=True)

    # Metric cards
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(metric_card("AI Discovered", str(cycle["pool_size"])), unsafe_allow_html=True)
    c2.markdown(metric_card("Reached Out", str(cycle["reached_out"])), unsafe_allow_html=True)
    c3.markdown(metric_card("Onboarded", str(cycle["onboarded"])), unsafe_allow_html=True)
    c4.markdown(metric_card("Slots Remaining", str(cycle["slots_remaining"])), unsafe_allow_html=True)

    # Pipeline
    st.markdown(section_label("Pipeline"), unsafe_allow_html=True)
    st.markdown(pipeline_bar(metrics["pipeline_counts"]), unsafe_allow_html=True)

    # Cycle narrative
    st.markdown(section_label("Cycle Status"), unsafe_allow_html=True)
    remaining = cycle["slots_remaining"]
    queue = cycle["discovered"]
    narrative = (
        f"The AI identified <strong>{cycle['pool_size']}</strong> matching creators and has reached out to "
        f"<strong>{cycle['reached_out']}</strong>. "
        f"<strong>{cycle['onboarded']}</strong> have been onboarded so far, with "
        f"<strong>{cycle['in_pipeline']}</strong> in active conversations. "
    )
    if remaining > 0 and queue > 0:
        narrative += f"<strong>{queue}</strong> more creators are queued for the next outreach wave to fill the remaining <strong>{remaining}</strong> slots."
    elif remaining > 0:
        narrative += f"<strong>{remaining}</strong> slots still need to be filled."
    else:
        narrative += "All slots have been filled."

    st.markdown(f"""
    <div style="background:{COLORS["surface"]};border:1px solid {COLORS["border"]};
        border-radius:10px;padding:20px;font-size:14px;color:{COLORS["text_sec"]};line-height:1.65">
        {narrative}
    </div>
    """, unsafe_allow_html=True)

    # Recent activity
    st.markdown(section_label("Recent Activity"), unsafe_allow_html=True)
    for ev in data["activity_feed"][:6]:
        st.markdown(activity_item(ev), unsafe_allow_html=True)


def render_campaign(data: dict, metrics: dict, api_key: str | None):
    if st.session_state.get("campaign_configured"):
        _render_cycle(data, metrics, api_key)
    else:
        _render_setup()
