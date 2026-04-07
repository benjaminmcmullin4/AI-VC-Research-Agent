"""Dashboard — KPIs, pipeline, recent activity."""

from __future__ import annotations

import streamlit as st

from components import activity_item, metric_card, pipeline_bar, section_label
from config import COLORS


def render_dashboard(data: dict, metrics: dict):
    st.markdown(f'<h1 style="font-size:28px;font-weight:700;margin-bottom:4px">Dashboard</h1>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:14px;color:{COLORS["text_sec"]};margin-bottom:32px">Overview of your influencer pipeline</div>', unsafe_allow_html=True)

    # ── KPIs ──────────────────────────────────────────────────────────────
    active_campaigns = sum(1 for c in data["campaigns"] if c.status == "Active")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(metric_card("Influencers Tracked", str(metrics["total_influencers"])), unsafe_allow_html=True)
    c2.markdown(metric_card("Active Campaigns", str(active_campaigns)), unsafe_allow_html=True)
    c3.markdown(metric_card("Reply Rate", f"{metrics['reply_rate']:.0f}%"), unsafe_allow_html=True)
    c4.markdown(metric_card("Revenue", f"${metrics['total_revenue']:,.0f}"), unsafe_allow_html=True)

    # ── Pipeline ──────────────────────────────────────────────────────────
    st.markdown(section_label("Pipeline"), unsafe_allow_html=True)
    st.markdown(pipeline_bar(metrics["pipeline_counts"]), unsafe_allow_html=True)

    # ── Recent activity ───────────────────────────────────────────────────
    st.markdown(section_label("Recent Activity"), unsafe_allow_html=True)
    for ev in data["activity_feed"][:5]:
        st.markdown(activity_item(ev), unsafe_allow_html=True)
