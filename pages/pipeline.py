"""Campaign Pipeline page — staged view of influencers."""

from __future__ import annotations

import streamlit as st

from config import PIPELINE_STAGES, STAGE_COLORS
from schema import Influencer


def _mini_card(inf: Influencer) -> str:
    return f"""
    <div style="background:white;border:1px solid #ECF0F1;border-radius:6px;padding:8px 10px;margin-bottom:4px;font-size:0.78rem;box-shadow:0 1px 2px rgba(0,0,0,0.03)">
        <div style="font-weight:600">{inf.name}</div>
        <div style="color:#777;font-size:0.7rem">{inf.handle} &middot; {inf.platform}</div>
        <div style="color:#999;font-size:0.68rem">{inf.niche} &middot; ${inf.estimated_cost:,}</div>
    </div>
    """


def render_pipeline(data: dict):
    st.markdown('<div class="section-header">Campaign Pipeline</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#777;font-size:0.88rem;margin-bottom:1.2rem">Influencer progression through the partnership pipeline.</div>', unsafe_allow_html=True)

    influencers: list[Influencer] = data["influencers"]

    # Group by stage
    by_stage: dict[str, list[Influencer]] = {s: [] for s in PIPELINE_STAGES}
    for inf in influencers:
        if inf.status in by_stage:
            by_stage[inf.status].append(inf)

    # ── Kanban — 2 rows of 4 ────────────────────────────────────────────
    for row_start in (0, 4):
        row_stages = PIPELINE_STAGES[row_start:row_start + 4]
        cols = st.columns(4)
        for col, stage in zip(cols, row_stages):
            color = STAGE_COLORS[stage]
            items = by_stage[stage]
            with col:
                st.markdown(f"""
                <div style="background:{color}15;border-top:3px solid {color};border-radius:8px;padding:10px;min-height:220px;margin-bottom:12px">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
                        <span style="font-weight:700;font-size:0.85rem;color:{color}">{stage}</span>
                        <span style="background:{color}33;color:{color};padding:1px 8px;border-radius:10px;font-size:0.72rem;font-weight:600">{len(items)}</span>
                    </div>
                    {''.join(_mini_card(i) for i in items)}
                </div>
                """, unsafe_allow_html=True)

    # ── Campaign summary ─────────────────────────────────────────────────
    st.markdown('<div class="section-header">Active Campaigns</div>', unsafe_allow_html=True)

    campaigns = data["campaigns"]
    for camp in campaigns:
        pct = (camp.spent / camp.budget * 100) if camp.budget else 0
        status_color = "#1ABC9C" if camp.status == "Active" else ("#94A3B8" if camp.status == "Completed" else "#FBBF24")

        st.markdown(f"""
        <div style="background:white;border:1px solid #ECF0F1;border-radius:8px;padding:16px;margin-bottom:10px;box-shadow:0 1px 3px rgba(0,0,0,0.04)">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
                <div>
                    <span style="font-weight:700;font-size:1rem">{camp.name}</span>
                    <span style="color:#777;font-size:0.82rem;margin-left:10px">{camp.brand}</span>
                </div>
                <span style="background:{status_color}22;color:{status_color};border:1px solid {status_color};padding:2px 10px;border-radius:12px;font-size:0.72rem;font-weight:500">{camp.status}</span>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr 1fr;gap:12px;font-size:0.82rem">
                <div><span style="color:#777">Budget</span><br><strong>${camp.budget:,}</strong></div>
                <div><span style="color:#777">Spent</span><br><strong>${camp.spent:,}</strong></div>
                <div><span style="color:#777">Utilization</span><br><strong>{pct:.0f}%</strong></div>
                <div><span style="color:#777">Influencers</span><br><strong>{camp.influencer_count}</strong></div>
                <div><span style="color:#777">Dates</span><br><strong>{camp.start_date[5:]} - {camp.end_date[5:]}</strong></div>
            </div>
            <div style="background:#ECF0F1;border-radius:4px;height:6px;margin-top:12px;overflow:hidden">
                <div style="background:{status_color};height:100%;width:{min(pct, 100)}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
