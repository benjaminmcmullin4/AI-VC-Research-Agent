"""Influencer Discovery page."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from config import NICHES, PIPELINE_STAGES, PLATFORMS, STAGE_COLORS
from schema import Influencer


def _fmt_followers(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}K"
    return str(n)


def _status_badge(status: str) -> str:
    color = STAGE_COLORS.get(status, "#777")
    return f'<span style="background:{color}22;color:{color};border:1px solid {color};padding:1px 8px;border-radius:10px;font-size:0.72rem;font-weight:500">{status}</span>'


def _platform_badge(platform: str) -> str:
    colors = {"Instagram": "#E1306C", "TikTok": "#010101", "YouTube": "#FF0000", "Twitter": "#1DA1F2"}
    c = colors.get(platform, "#777")
    return f'<span style="background:{c}18;color:{c};border:1px solid {c};padding:1px 8px;border-radius:10px;font-size:0.72rem;font-weight:500">{platform}</span>'


def render_discovery(data: dict, api_key: str | None):
    st.markdown('<div class="section-header">Influencer Discovery</div>', unsafe_allow_html=True)

    influencers: list[Influencer] = data["influencers"]

    # ── Filters ──────────────────────────────────────────────────────────
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        sel_platforms = st.multiselect("Platform", PLATFORMS, default=[], key="disc_plat")
    with fc2:
        sel_niches = st.multiselect("Niche", NICHES, default=[], key="disc_niche")
    with fc3:
        sel_statuses = st.multiselect("Status", PIPELINE_STAGES, default=[], key="disc_stat")
    with fc4:
        min_aud_fit = st.slider("Min Audience Fit", 0, 100, 0, key="disc_fit")

    fc5, fc6 = st.columns(2)
    with fc5:
        follower_range = st.slider("Follower Range", 0, 5_000_000, (0, 5_000_000), step=10_000, format="%d", key="disc_fol")
    with fc6:
        min_engagement = st.slider("Min Engagement %", 0.0, 10.0, 0.0, step=0.1, key="disc_eng")

    # ── Apply filters ────────────────────────────────────────────────────
    filtered = influencers
    if sel_platforms:
        filtered = [i for i in filtered if i.platform in sel_platforms]
    if sel_niches:
        filtered = [i for i in filtered if i.niche in sel_niches]
    if sel_statuses:
        filtered = [i for i in filtered if i.status in sel_statuses]
    if min_aud_fit > 0:
        filtered = [i for i in filtered if i.audience_fit_score >= min_aud_fit]
    filtered = [i for i in filtered if follower_range[0] <= i.followers <= follower_range[1]]
    if min_engagement > 0:
        filtered = [i for i in filtered if i.engagement_rate >= min_engagement]

    st.markdown(f"<div style='color:#777;font-size:0.85rem;margin-bottom:0.8rem'>Showing **{len(filtered)}** of {len(influencers)} influencers</div>", unsafe_allow_html=True)

    # ── Table ────────────────────────────────────────────────────────────
    if not filtered:
        st.info("No influencers match the current filters.")
        return

    df = pd.DataFrame([{
        "Name": i.name,
        "Handle": i.handle,
        "Platform": i.platform,
        "Niche": i.niche,
        "Followers": i.followers,
        "Engagement %": i.engagement_rate,
        "Audience Fit": i.audience_fit_score,
        "Brand Fit": i.brand_fit_score,
        "Est. Cost": i.estimated_cost,
        "Location": i.location,
        "Status": i.status,
    } for i in filtered])

    st.dataframe(
        df.style.format({
            "Followers": "{:,.0f}",
            "Engagement %": "{:.1f}%",
            "Est. Cost": "${:,.0f}",
        }),
        use_container_width=True,
        height=min(400, 36 * len(df) + 38),
    )

    # ── Detail panel ─────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Influencer Detail</div>', unsafe_allow_html=True)

    names = [f"{i.name} ({i.handle})" for i in filtered]
    selected = st.selectbox("Select an influencer to view details", names, key="disc_detail_sel")
    if selected:
        idx = names.index(selected)
        inf = filtered[idx]

        col_l, col_r = st.columns([2, 1])

        with col_l:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">
                <div>
                    <span style="font-size:1.2rem;font-weight:700">{inf.name}</span>
                    <span style="color:#777;margin-left:8px">{inf.handle}</span>
                </div>
                {_platform_badge(inf.platform)}
                {_status_badge(inf.status)}
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"<div style='color:#555;font-size:0.9rem;margin-bottom:12px'>{inf.bio}</div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:16px">
                <div class="metric-card"><h4>Followers</h4><div class="value">{_fmt_followers(inf.followers)}</div></div>
                <div class="metric-card"><h4>Engagement</h4><div class="value">{inf.engagement_rate}%</div></div>
                <div class="metric-card"><h4>Est. Cost</h4><div class="value">${inf.estimated_cost:,}</div></div>
            </div>
            """, unsafe_allow_html=True)

            if inf.past_partnerships:
                partnerships = " &middot; ".join(inf.past_partnerships)
                st.markdown(f"<div style='font-size:0.82rem;color:#555'><strong>Past Partnerships:</strong> {partnerships}</div>", unsafe_allow_html=True)

            st.markdown(f"<div style='font-size:0.82rem;color:#555;margin-top:4px'><strong>Location:</strong> {inf.location} &middot; <strong>Niche:</strong> {inf.niche}</div>", unsafe_allow_html=True)

        with col_r:
            st.markdown("<div style='margin-top:8px'>", unsafe_allow_html=True)
            # Score bars
            st.markdown(f"""
            <div style="margin-bottom:12px">
                <div style="font-size:0.75rem;color:#777;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:4px">Audience Fit</div>
                <div style="background:#ECF0F1;border-radius:4px;height:20px;overflow:hidden">
                    <div style="background:#1ABC9C;height:100%;width:{inf.audience_fit_score}%;display:flex;align-items:center;padding-left:8px;font-size:0.75rem;color:white;font-weight:600">{inf.audience_fit_score}</div>
                </div>
            </div>
            <div style="margin-bottom:12px">
                <div style="font-size:0.75rem;color:#777;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:4px">Brand Fit</div>
                <div style="background:#ECF0F1;border-radius:4px;height:20px;overflow:hidden">
                    <div style="background:#60A5FA;height:100%;width:{inf.brand_fit_score}%;display:flex;align-items:center;padding-left:8px;font-size:0.75rem;color:white;font-weight:600">{inf.brand_fit_score}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Outreach draft button
            if api_key:
                if st.button("Generate Outreach Draft", key="disc_outreach_btn"):
                    from ai_engine import generate_outreach_draft
                    draft = generate_outreach_draft(api_key, inf.model_dump())
                    if draft:
                        st.session_state["disc_draft"] = draft

            if "disc_draft" in st.session_state:
                d = st.session_state["disc_draft"]
                st.markdown(f"""
                <div style="background:#F0F4F8;padding:12px;border-radius:8px;margin-top:12px">
                    <div style="font-weight:600;font-size:0.85rem;margin-bottom:6px">{d.subject}</div>
                    <div style="font-size:0.82rem;color:#333;line-height:1.5">{d.body}</div>
                    <div style="font-size:0.72rem;color:#777;margin-top:8px">Tone: {d.tone}</div>
                </div>
                """, unsafe_allow_html=True)
