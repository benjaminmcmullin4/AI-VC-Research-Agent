"""Recommendations page — top influencers with AI-generated blurbs."""

from __future__ import annotations

import streamlit as st

from config import STAGE_COLORS
from data.mock_data import get_top_recommended
from schema import Influencer


def _fmt_followers(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}K"
    return str(n)


def _rec_card(inf: Influencer, blurb: str) -> str:
    platform_colors = {"Instagram": "#E1306C", "TikTok": "#010101", "YouTube": "#FF0000", "Twitter": "#1DA1F2"}
    pc = platform_colors.get(inf.platform, "#777")
    score = int(0.6 * inf.audience_fit_score + 0.4 * inf.brand_fit_score)
    return f"""
    <div style="background:white;border:1px solid #ECF0F1;border-radius:10px;padding:1.2rem;box-shadow:0 2px 6px rgba(0,0,0,0.04);transition:box-shadow 0.2s;margin-bottom:0.5rem">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px">
            <div>
                <div style="font-weight:700;font-size:1rem">{inf.name}</div>
                <div style="color:#777;font-size:0.82rem">{inf.handle}</div>
            </div>
            <div style="background:#1ABC9C22;color:#1ABC9C;padding:3px 10px;border-radius:12px;font-size:0.78rem;font-weight:600">Score: {score}</div>
        </div>
        <div style="display:flex;gap:6px;margin-bottom:10px;flex-wrap:wrap">
            <span style="background:{pc}18;color:{pc};border:1px solid {pc};padding:1px 8px;border-radius:10px;font-size:0.7rem;font-weight:500">{inf.platform}</span>
            <span style="background:#F0F4F8;color:#555;padding:1px 8px;border-radius:10px;font-size:0.7rem">{inf.niche}</span>
            <span style="background:{STAGE_COLORS.get(inf.status, '#777')}22;color:{STAGE_COLORS.get(inf.status, '#777')};padding:1px 8px;border-radius:10px;font-size:0.7rem">{inf.status}</span>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:4px;margin-bottom:12px;font-size:0.78rem">
            <div><span style="color:#777">Followers</span><br><strong>{_fmt_followers(inf.followers)}</strong></div>
            <div><span style="color:#777">Engagement</span><br><strong>{inf.engagement_rate}%</strong></div>
            <div><span style="color:#777">Aud. Fit</span><br><strong>{inf.audience_fit_score}</strong></div>
            <div><span style="color:#777">Est. Cost</span><br><strong>${inf.estimated_cost:,}</strong></div>
        </div>
        <div style="font-size:0.84rem;color:#444;line-height:1.55;border-top:1px solid #ECF0F1;padding-top:10px">{blurb}</div>
    </div>
    """


def render_recommendations(data: dict, api_key: str | None):
    st.markdown('<div class="section-header">Top Recommendations</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#777;font-size:0.88rem;margin-bottom:1.2rem">Influencers our agents recommend contacting next, ranked by audience and brand fit.</div>', unsafe_allow_html=True)

    top = get_top_recommended(data, n=10)

    # AI refresh button
    if api_key:
        if st.button("Refresh with AI", key="rec_ai_refresh"):
            from ai_engine import generate_recommendation
            ai_blurbs = {}
            for inf in top:
                result = generate_recommendation(api_key, inf.model_dump())
                if result:
                    ai_blurbs[inf.handle] = result.reasoning
            if ai_blurbs:
                st.session_state["ai_rec_blurbs"] = ai_blurbs

    ai_blurbs = st.session_state.get("ai_rec_blurbs", {})

    # Render 2-column grid
    for i in range(0, len(top), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(top):
                inf = top[i + j]
                # Prefer AI blurb > pre-written blurb > generic
                blurb = (
                    ai_blurbs.get(inf.handle)
                    or inf.recommendation_blurb
                    or f"{inf.name} shows strong audience alignment with a {inf.audience_fit_score}/100 audience fit score and {inf.engagement_rate}% engagement rate. Their {inf.niche.lower()} content on {inf.platform} reaches {_fmt_followers(inf.followers)} followers with proven brand partnership experience."
                )
                with col:
                    st.markdown(_rec_card(inf, blurb), unsafe_allow_html=True)
