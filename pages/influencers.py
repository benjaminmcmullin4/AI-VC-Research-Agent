"""Influencers — AI-found talent with pipeline/onboarded/queue tabs."""

from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

from components import fmt_followers, page_header, section_label
from config import COLORS, NICHES, PLATFORMS, RADIUS, SHADOWS, STAGE_COLORS
from schema import Influencer, OutreachMessage, OutreachThread


_PIPELINE_STATUSES = {"Contacted", "Replied", "Negotiating"}
_ONBOARDED_STATUSES = {"Signed", "Content Posted", "Converted"}
_QUEUE_STATUSES = {"Discovered", "Qualified"}

# Platform icon mapping
_PLATFORM_ICONS = {
    "Instagram": "bi-instagram",
    "TikTok": "bi-tiktok",
    "YouTube": "bi-youtube",
    "Twitter": "bi-twitter-x",
}


def _influencer_table(influencers: list[Influencer], show_revenue: bool = False):
    """Render a filterable table of influencers."""
    if not influencers:
        st.info("No influencers in this group yet. Advance the simulation to discover more.")
        return None

    rows = []
    for i in influencers:
        row = {
            "Name": i.name,
            "Handle": i.handle,
            "Platform": i.platform,
            "Niche": i.niche,
            "Followers": i.followers,
            "Eng. %": i.engagement_rate,
            "Fit Score": int(0.6 * i.audience_fit_score + 0.4 * i.brand_fit_score),
            "Status": i.status,
        }
        if show_revenue:
            row["Deal Cost"] = i.deal_value if i.deal_value else i.estimated_cost
            row["Revenue"] = i.revenue_generated
            row["ROI"] = round(i.revenue_generated / max(i.deal_value, i.estimated_cost, 1), 1) if i.revenue_generated else 0
        rows.append(row)

    df = pd.DataFrame(rows)
    fmt = {"Followers": "{:,.0f}", "Eng. %": "{:.1f}%"}
    if show_revenue:
        fmt["Deal Cost"] = "${:,.0f}"
        fmt["Revenue"] = "${:,.0f}"
        fmt["ROI"] = "{:.1f}x"

    st.dataframe(
        df.style.format(fmt),
        use_container_width=True,
        height=min(400, 35 * len(df) + 38),
    )
    return influencers


def _influencer_detail(filtered: list[Influencer], tab_key: str, api_key: str | None):
    """Render detail panel for selected influencer."""
    if not filtered:
        return

    st.markdown(section_label("Detail"), unsafe_allow_html=True)
    names = [f"{i.name} ({i.handle})" for i in filtered]
    selected = st.selectbox("Select an influencer", names, key=f"inf_sel_{tab_key}", label_visibility="collapsed")
    if not selected:
        return

    inf = filtered[names.index(selected)]
    score = int(0.6 * inf.audience_fit_score + 0.4 * inf.brand_fit_score)
    platform_icon = _PLATFORM_ICONS.get(inf.platform, "bi-globe")

    col_l, col_r = st.columns([3, 1])
    with col_l:
        st.markdown(f"""
        <div style="font-size:20px;font-weight:700;color:{COLORS["text"]};letter-spacing:-0.015em">{inf.name}
            <span style="font-weight:400;color:{COLORS["text_muted"]};font-size:14px;margin-left:8px">{inf.handle}</span>
        </div>
        <div style="font-size:14px;color:{COLORS["text_sec"]};margin-top:6px;line-height:1.6">{inf.bio}</div>
        """, unsafe_allow_html=True)
        if inf.past_partnerships:
            pills = "".join(
                f'<span style="font-size:12px;font-weight:500;color:{COLORS["text_sec"]};background:{COLORS["surface"]};'
                f'padding:4px 10px;border-radius:20px;border:1px solid {COLORS["border_light"]}">{p}</span>'
                for p in inf.past_partnerships
            )
            st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:10px">{pills}</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown(f"""
        <div style="text-align:right">
            <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;
                color:{COLORS["text_muted"]};margin-bottom:4px">Fit Score</div>
            <div style="font-size:36px;font-weight:800;
                background:linear-gradient(135deg,#6366F1,#4F46E5);-webkit-background-clip:text;
                -webkit-text-fill-color:transparent;letter-spacing:-0.02em">{score}</div>
            <div style="font-size:12px;color:{COLORS["text_muted"]};margin-top:10px;font-weight:500">
                <i class="bi {platform_icon}" style="margin-right:4px"></i>
                {inf.platform} · {inf.niche}
            </div>
            <div style="font-size:12px;color:{COLORS["text_muted"]};font-weight:500">
                {fmt_followers(inf.followers)} followers · {inf.engagement_rate}% eng.
            </div>
        </div>
        """, unsafe_allow_html=True)

    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.metric("Followers", fmt_followers(inf.followers))
    sc2.metric("Engagement", f"{inf.engagement_rate}%")
    sc3.metric("Audience Fit", f"{inf.audience_fit_score}/100")
    sc4.metric("Est. Cost", f"${inf.estimated_cost:,}")

    # Show deal value and revenue for onboarded influencers
    if inf.status in _ONBOARDED_STATUSES and (inf.deal_value or inf.revenue_generated):
        dc1, dc2 = st.columns(2)
        if inf.deal_value:
            dc1.metric("Deal Value", f"${inf.deal_value:,.0f}")
        if inf.revenue_generated:
            dc2.metric("Revenue Generated", f"${inf.revenue_generated:,.0f}")


def render_influencers(data: dict, api_key: str | None):
    all_inf: list[Influencer] = data["influencers"]
    sim = st.session_state.get("sim")
    is_sim = sim and sim.get("active")

    st.markdown(page_header("AI-Found Talent", "Matched by the AI based on your campaign criteria"), unsafe_allow_html=True)

    pipeline = [i for i in all_inf if i.status in _PIPELINE_STATUSES]
    onboarded = [i for i in all_inf if i.status in _ONBOARDED_STATUSES]
    queue = [i for i in all_inf if i.status in _QUEUE_STATUSES]

    tab_pipeline, tab_onboarded, tab_queue = st.tabs([
        f"In Pipeline ({len(pipeline)})",
        f"Onboarded ({len(onboarded)})",
        f"Queue ({len(queue)})",
    ])

    with tab_pipeline:
        st.markdown(f'<div style="font-size:13px;color:{COLORS["text_muted"]};margin:4px 0 12px">{len(pipeline)} influencers in active outreach</div>', unsafe_allow_html=True)
        result = _influencer_table(pipeline)
        if result:
            _influencer_detail(pipeline, "pipeline", api_key)

    with tab_onboarded:
        st.markdown(f'<div style="font-size:13px;color:{COLORS["text_muted"]};margin:4px 0 12px">{len(onboarded)} influencers onboarded</div>', unsafe_allow_html=True)
        result = _influencer_table(onboarded, show_revenue=True)
        if result:
            _influencer_detail(onboarded, "onboarded", api_key)

    with tab_queue:
        st.markdown(f'<div style="font-size:13px;color:{COLORS["text_muted"]};margin:4px 0 12px">{len(queue)} creators queued for next outreach wave</div>', unsafe_allow_html=True)
        result = _influencer_table(queue)
        if result:
            _influencer_detail(queue, "queue", api_key)
