"""Influencers — browse, filter, and reach out."""

from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

from components import fmt_followers, section_label
from config import COLORS, NICHES, PLATFORMS, STAGE_COLORS
from schema import Influencer, OutreachMessage, OutreachThread


def render_influencers(data: dict, api_key: str | None):
    total = len(data["influencers"])
    platforms_used = len(set(i.platform for i in data["influencers"]))

    st.markdown(f'<h1 style="font-size:28px;font-weight:700;margin-bottom:4px">Influencers</h1>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:14px;color:{COLORS["text_sec"]};margin-bottom:32px">{total} creators tracked across {platforms_used} platforms</div>', unsafe_allow_html=True)

    # ── Filters ──────────────────────────────────────────────────────────
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        sel_platform = st.multiselect("Platform", PLATFORMS, default=[], key="inf_plat")
    with fc2:
        sel_niche = st.multiselect("Niche", NICHES, default=[], key="inf_niche")
    with fc3:
        min_engagement = st.slider("Min Engagement %", 0.0, 8.0, 0.0, step=0.5, key="inf_eng")

    filtered: list[Influencer] = data["influencers"]
    if sel_platform:
        filtered = [i for i in filtered if i.platform in sel_platform]
    if sel_niche:
        filtered = [i for i in filtered if i.niche in sel_niche]
    if min_engagement > 0:
        filtered = [i for i in filtered if i.engagement_rate >= min_engagement]

    st.markdown(f'<div style="font-size:13px;color:{COLORS["text_muted"]};margin:8px 0 16px">Showing {len(filtered)} of {total}</div>', unsafe_allow_html=True)

    if not filtered:
        st.info("No influencers match the current filters.")
        return

    # ── Table ────────────────────────────────────────────────────────────
    df = pd.DataFrame([{
        "Name": i.name,
        "Handle": i.handle,
        "Platform": i.platform,
        "Niche": i.niche,
        "Followers": i.followers,
        "Eng. %": i.engagement_rate,
        "Fit Score": int(0.6 * i.audience_fit_score + 0.4 * i.brand_fit_score),
        "Status": i.status,
    } for i in filtered])

    st.dataframe(
        df.style.format({"Followers": "{:,.0f}", "Eng. %": "{:.1f}%"}),
        use_container_width=True,
        height=min(450, 35 * len(df) + 38),
    )

    # ── Detail / outreach ────────────────────────────────────────────────
    st.markdown(section_label("Influencer Detail"), unsafe_allow_html=True)

    names = [f"{i.name} ({i.handle})" for i in filtered]
    selected = st.selectbox("Select an influencer", names, key="inf_sel", label_visibility="collapsed")
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

    # ── Quick stats ──────────────────────────────────────────────────────
    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.metric("Followers", fmt_followers(inf.followers))
    sc2.metric("Engagement", f"{inf.engagement_rate}%")
    sc3.metric("Audience Fit", f"{inf.audience_fit_score}/100")
    sc4.metric("Est. Cost", f"${inf.estimated_cost:,}")

    # ── Send outreach ────────────────────────────────────────────────────
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    if inf.status in ("Discovered", "Qualified"):
        with st.expander("Send outreach message"):
            default_msg = (
                f"Hi {inf.name.split()[0]}! We've been following your {inf.niche.lower()} content on "
                f"{inf.platform} and love what you're building. We're working on a campaign that "
                f"could be a great fit for your audience. Would you be open to a quick chat?"
            )

            if api_key:
                if st.button("Generate with AI", key="inf_ai_draft"):
                    from ai_engine import generate_outreach_draft
                    draft = generate_outreach_draft(api_key, inf.model_dump())
                    if draft:
                        st.session_state["inf_draft"] = draft.body

            msg = st.text_area("Message", value=st.session_state.get("inf_draft", default_msg), height=120, key="inf_msg")

            if st.button("Send", key="inf_send"):
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
