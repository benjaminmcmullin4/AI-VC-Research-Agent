"""Campaign — setup + AI cycle dashboard with simulation."""

from __future__ import annotations

import streamlit as st

from components import (
    activity_item,
    budget_bar,
    day_counter_html,
    metric_card,
    page_header,
    pipeline_bar,
    progress_bar_html,
    section_label,
)
from config import COLORS, DEFAULT_BUDGET, NICHES, PLATFORMS, SHADOWS, RADIUS
from data.mock_data import compute_cycle_metrics


def _render_setup():
    """Campaign setup form shown on first visit."""
    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center;max-width:520px;margin:0 auto 48px">
        <div style="width:56px;height:56px;border-radius:16px;margin:0 auto 20px;
            background:linear-gradient(135deg,#6366F1,#4F46E5);display:flex;align-items:center;
            justify-content:center;box-shadow:0 4px 14px rgba(79,70,229,0.25)">
            <i class="bi bi-rocket-takeoff" style="font-size:24px;color:white"></i>
        </div>
        <div style="font-size:28px;font-weight:800;color:{COLORS["text"]};letter-spacing:-0.02em;
            margin-bottom:8px">Launch a Campaign</div>
        <div style="font-size:15px;color:{COLORS["text_sec"]};line-height:1.65;max-width:400px;margin:0 auto">
            Tell the AI what you need. It will find the best creators,
            reach out automatically, and fill your roster.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_pad_l, col_form, col_pad_r = st.columns([1, 2, 1])
    with col_form:
        name = st.text_input("Campaign Name", value="Q2 Creator Campaign", key="setup_name")
        target = st.number_input("How many influencers do you want?", min_value=3, max_value=50, value=10, step=1, key="setup_target")
        budget = st.number_input(
            "Campaign Budget ($)",
            min_value=5_000,
            max_value=500_000,
            value=DEFAULT_BUDGET,
            step=5_000,
            key="setup_budget",
            help="Total budget for influencer partnerships",
        )
        niches = st.multiselect("Preferred Niches", NICHES, default=[], key="setup_niches",
                                help="Leave empty for all niches")
        platforms = st.multiselect("Preferred Platforms", PLATFORMS, default=[], key="setup_platforms",
                                   help="Leave empty for all platforms")

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        if st.button("Launch Campaign", type="primary", use_container_width=True):
            from simulation.engine import initialize_simulation
            sim = initialize_simulation(
                campaign_name=name,
                target_count=int(target),
                niches=niches,
                platforms=platforms,
                budget=int(budget),
            )
            st.session_state["sim"] = sim
            st.session_state["campaign_configured"] = True
            st.session_state["campaign_name"] = name
            st.session_state["campaign_target"] = int(target)
            st.session_state["campaign_niches"] = niches
            st.session_state["campaign_platforms"] = platforms
            st.session_state["campaign_budget"] = int(budget)
            st.rerun()


def _render_cycle(data: dict, metrics: dict, api_key: str | None):
    """Cycle dashboard shown after campaign is configured."""
    sim = st.session_state.get("sim", {})
    name = st.session_state.get("campaign_name", "Campaign")
    target = st.session_state.get("campaign_target", 10)
    niches = st.session_state.get("campaign_niches", [])
    platforms = st.session_state.get("campaign_platforms", [])
    budget_total = sim.get("budget_total", 0)
    budget_spent = sim.get("budget_spent", 0)
    budget_committed = sim.get("budget_committed", 0)
    total_revenue = sim.get("total_revenue", 0)

    cycle = compute_cycle_metrics(data, target, niches, platforms)

    # Header row
    col_title, col_edit = st.columns([4, 1])
    with col_title:
        filters_desc = []
        if niches:
            filters_desc.append(", ".join(niches))
        if platforms:
            filters_desc.append(", ".join(platforms))
        sub = " · ".join(filters_desc) if filters_desc else "All niches and platforms"
        st.markdown(page_header(name, sub), unsafe_allow_html=True)
    with col_edit:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("Edit Campaign", key="edit_campaign"):
            st.session_state["campaign_configured"] = False
            st.session_state["sim"] = None
            st.rerun()

    # Day counter (only if sim is active)
    if sim.get("active"):
        day = sim.get("day", 0)
        start_date = sim.get("start_date", "2026-04-08")
        if day == 0:
            st.info("Campaign initialized. Use the sidebar controls to advance the simulation day by day or in bulk.")
        else:
            st.markdown(day_counter_html(day, start_date), unsafe_allow_html=True)

    # Progress bar
    st.markdown(progress_bar_html(cycle["onboarded"], cycle["target"]), unsafe_allow_html=True)

    # Metric cards row 1: Pipeline
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(metric_card("AI Discovered", str(cycle["pool_size"])), unsafe_allow_html=True)
    c2.markdown(metric_card("Reached Out", str(cycle["reached_out"])), unsafe_allow_html=True)
    c3.markdown(metric_card("Onboarded", str(cycle["onboarded"]), accent=True), unsafe_allow_html=True)
    c4.markdown(metric_card("Slots Remaining", str(cycle["slots_remaining"])), unsafe_allow_html=True)

    # Metric cards row 2: Budget & Revenue
    if sim.get("active"):
        remaining = max(0, budget_total - budget_spent - budget_committed)
        roi = total_revenue / budget_spent if budget_spent > 0 else 0
        b1, b2, b3, b4 = st.columns(4)
        b1.markdown(metric_card("Budget", f"${budget_total:,.0f}"), unsafe_allow_html=True)
        b2.markdown(metric_card("Spent", f"${budget_spent:,.0f}"), unsafe_allow_html=True)
        b3.markdown(metric_card("Revenue", f"${total_revenue:,.0f}", accent=True), unsafe_allow_html=True)
        b4.markdown(metric_card("ROI", f"{roi:.1f}x" if budget_spent > 0 else "—"), unsafe_allow_html=True)

        # Budget bar
        st.markdown(section_label("Budget Allocation"), unsafe_allow_html=True)
        st.markdown(budget_bar(budget_total, budget_spent, budget_committed), unsafe_allow_html=True)

    # Pipeline
    st.markdown(section_label("Pipeline"), unsafe_allow_html=True)
    st.markdown(pipeline_bar(metrics["pipeline_counts"]), unsafe_allow_html=True)

    # Cycle narrative
    st.markdown(section_label("Cycle Status"), unsafe_allow_html=True)
    remaining_slots = cycle["slots_remaining"]
    queue = cycle["discovered"]
    narrative = (
        f"The AI identified <strong>{cycle['pool_size']}</strong> matching creators and has reached out to "
        f"<strong>{cycle['reached_out']}</strong>. "
        f"<strong>{cycle['onboarded']}</strong> have been onboarded so far, with "
        f"<strong>{cycle['in_pipeline']}</strong> in active conversations. "
    )
    if sim.get("active") and budget_spent > 0:
        narrative += f"<strong>${total_revenue:,.0f}</strong> in revenue generated so far. "
    if remaining_slots > 0 and queue > 0:
        narrative += f"<strong>{queue}</strong> more creators are queued for the next outreach wave to fill the remaining <strong>{remaining_slots}</strong> slots."
    elif remaining_slots > 0:
        narrative += f"<strong>{remaining_slots}</strong> slots still need to be filled."
    else:
        narrative += "All slots have been filled."

    st.markdown(f"""
    <div class="influx-card" style="background:{COLORS["bg"]};
        border-radius:{RADIUS["lg"]};padding:24px;
        box-shadow:{SHADOWS["sm"]};font-size:14px;color:{COLORS["text_sec"]};line-height:1.7">
        {narrative}
    </div>
    """, unsafe_allow_html=True)

    # Recent activity
    st.markdown(section_label("Recent Activity"), unsafe_allow_html=True)
    feed = data["activity_feed"][:8]
    if feed:
        for ev in feed:
            st.markdown(activity_item(ev), unsafe_allow_html=True)
    else:
        st.info("No activity yet. Advance the simulation to see agent activity.")


def render_campaign(data: dict, metrics: dict, api_key: str | None):
    if st.session_state.get("campaign_configured"):
        _render_cycle(data, metrics, api_key)
    else:
        _render_setup()
