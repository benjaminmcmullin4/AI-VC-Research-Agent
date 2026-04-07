"""Influencers — AI-found talent with pipeline/onboarded/queue tabs."""

from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

from components import fmt_followers, section_label
from config import COLORS, NICHES, PLATFORMS, STAGE_COLORS
from schema import Influencer, OutreachMessage, OutreachThread


_PIPELINE_STATUSES = {"Contacted", "Replied", "Negotiating"}
_ONBOARDED_STATUSES = {"Signed", "Content Posted", "Converted"}
_QUEUE_STATUSES = {"Discovered", "Qualified"}


def _influencer_table(influencers: list[Influencer], show_revenue: bool = False):
    """Render a filterable table of influencers."""
    if not influencers:
        st.info("No influencers in this group.")
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
            row["Revenue"] = i.revenue_generated
            row["Est. Cost"] = i.estimated_cost
        rows.append(row)

    df = pd.DataFrame(rows)
    fmt = {"Followers": "{:,.0f}", "Eng. %": "{:.1f}%"}
    if show_revenue:
        fmt["Revenue"] = "${:,.0f}"
        fmt["Est. Cost"] = "${:,.0f}"

    st.dataframe(
        df.style.format(fmt),
        use_container_width=True,
        height=min(400, 35 * len(df) + 38),
    )
    return influencers


def _influencer_detail(filtered: list[Influencer], tab_key: str, api_key: str | None, show_outreach: bool = False):
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

    col_l, col_r = st.columns([3, 1])
    with col_l:
        st.markdown(f"""
        <div style="font-size:18px;font-weight:700;color:{COLORS["text"]}">{inf.name}
            <span style="font-weight:400;color:{COLORS["text_muted"]};font-size:14px;margin-left:8px">{inf.handle}</span>
        </div>
        <div style="font-size:14px;color:{COLORS["text_sec"]};margin-top:6px;line-height:1.5">{inf.bio}</div>
        """, unsafe_allow_html=True)
        if inf.past_partnerships:
            partners = ", ".join(inf.past_partnerships)
            st.markdown(f'<div style="font-size:13px;color:{COLORS["text_muted"]};margin-top:8px">Past partnerships: {partners}</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown(f"""
        <div style="text-align:right">
            <div style="font-size:13px;color:{COLORS["text_muted"]}">Fit Score</div>
            <div style="font-size:28px;font-weight:800;color:{COLORS["accent"]}">{score}</div>
            <div style="font-size:13px;color:{COLORS["text_muted"]};margin-top:8px">{inf.platform} · {inf.niche}</div>
            <div style="font-size:13px;color:{COLORS["text_muted"]}">{fmt_followers(inf.followers)} followers · {inf.engagement_rate}% eng.</div>
        </div>
        """, unsafe_allow_html=True)

    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.metric("Followers", fmt_followers(inf.followers))
    sc2.metric("Engagement", f"{inf.engagement_rate}%")
    sc3.metric("Audience Fit", f"{inf.audience_fit_score}/100")
    sc4.metric("Est. Cost", f"${inf.estimated_cost:,}")

    # Outreach for queue influencers
    if show_outreach and inf.status in ("Discovered", "Qualified"):
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        with st.expander("Send outreach message"):
            default_msg = (
                f"Hi {inf.name.split()[0]}! We've been following your {inf.niche.lower()} content on "
                f"{inf.platform} and love what you're building. We're working on a campaign that "
                f"could be a great fit for your audience. Would you be open to a quick chat?"
            )

            if api_key:
                if st.button("Generate with AI", key=f"inf_ai_draft_{tab_key}"):
                    from ai_engine import generate_outreach_draft
                    draft = generate_outreach_draft(api_key, inf.model_dump())
                    if draft:
                        st.session_state["inf_draft"] = draft.body

            msg = st.text_area("Message", value=st.session_state.get("inf_draft", default_msg), height=120, key=f"inf_msg_{tab_key}")

            if st.button("Send", key=f"inf_send_{tab_key}"):
                now = datetime.now().strftime("%Y-%m-%d %H:%M")
                thread = OutreachThread(
                    influencer_handle=inf.handle, influencer_name=inf.name,
                    platform=inf.platform, status="Awaiting Reply",
                    messages=[OutreachMessage(sender="agent", content=msg, timestamp=now, message_type="initial")],
                    current_stage="Contacted", assigned_to="AI Agent", next_action="Wait for reply",
                )
                st.session_state.setdefault("new_threads", []).append(thread)
                st.session_state.pop("inf_draft", None)
                st.success(f"Message sent to {inf.handle}. View it in Conversations.")


def render_influencers(data: dict, api_key: str | None):
    all_inf: list[Influencer] = data["influencers"]

    st.markdown(f'<h1 style="font-size:28px;font-weight:700;margin-bottom:4px">AI-Found Talent</h1>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:14px;color:{COLORS["text_sec"]};margin-bottom:24px">Matched by the AI based on your campaign criteria</div>', unsafe_allow_html=True)

    tab_pipeline, tab_onboarded, tab_queue = st.tabs(["In Pipeline", "Onboarded", "Queue"])

    with tab_pipeline:
        pipeline = [i for i in all_inf if i.status in _PIPELINE_STATUSES]
        st.markdown(f'<div style="font-size:13px;color:{COLORS["text_muted"]};margin:4px 0 12px">{len(pipeline)} influencers in active outreach</div>', unsafe_allow_html=True)
        result = _influencer_table(pipeline)
        if result:
            _influencer_detail(pipeline, "pipeline", api_key)

    with tab_onboarded:
        onboarded = [i for i in all_inf if i.status in _ONBOARDED_STATUSES]
        st.markdown(f'<div style="font-size:13px;color:{COLORS["text_muted"]};margin:4px 0 12px">{len(onboarded)} influencers onboarded</div>', unsafe_allow_html=True)
        result = _influencer_table(onboarded, show_revenue=True)
        if result:
            _influencer_detail(onboarded, "onboarded", api_key)

    with tab_queue:
        queue = [i for i in all_inf if i.status in _QUEUE_STATUSES]
        st.markdown(f'<div style="font-size:13px;color:{COLORS["text_muted"]};margin:4px 0 12px">{len(queue)} creators queued for next outreach wave</div>', unsafe_allow_html=True)
        result = _influencer_table(queue)
        if result:
            _influencer_detail(queue, "queue", api_key, show_outreach=True)
