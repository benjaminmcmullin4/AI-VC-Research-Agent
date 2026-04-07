"""Dashboard page — executive overview."""

from __future__ import annotations

import streamlit as st

from components import activity_item, metric_card, pipeline_bar, section_title
from config import COLORS


def render_dashboard(data: dict, metrics: dict, api_key: str | None):

    # ── AI insight box ───────────────────────────────────────────────────
    if api_key and st.button("Generate AI Insight", key="dash_ai"):
        from ai_engine import generate_dashboard_insight
        insight = generate_dashboard_insight(api_key, metrics)
        if insight:
            st.session_state["dash_insight"] = insight

    if "dash_insight" in st.session_state:
        ins = st.session_state["dash_insight"]
        summary, rec = ins.summary, ins.top_recommendation
    else:
        summary = "Pipeline is healthy with a 63% reply rate on outreach. Beauty niche TikTok creators are driving 2.4x more conversions than Instagram counterparts."
        rec = "Increase TikTok creator budget by 15% for Q2 beauty campaigns."

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{COLORS["surface"]},{COLORS["bg"]});
        padding:20px 24px;border-radius:12px;margin-bottom:20px;
        border:1px solid {COLORS["border"]};border-left:4px solid {COLORS["primary"]}">
        <div style="font-size:11px;text-transform:uppercase;letter-spacing:0.08em;
            color:{COLORS["primary"]};margin-bottom:8px;font-weight:600">Campaign Insight</div>
        <div style="font-size:14px;color:{COLORS["text"]};line-height:1.6">{summary}</div>
        <div style="font-size:13px;color:{COLORS["text_secondary"]};margin-top:8px">→ {rec}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI cards ────────────────────────────────────────────────────────
    active_campaigns = sum(1 for c in data["campaigns"] if c.status == "Active")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(metric_card("Total Influencers", str(metrics["total_influencers"]), "+8 this week", "👥"), unsafe_allow_html=True)
    c2.markdown(metric_card("Active Campaigns", str(active_campaigns), "", "📣"), unsafe_allow_html=True)
    c3.markdown(metric_card("Reply Rate", f"{metrics['reply_rate']:.0f}%", "+21pp vs last month", "💬"), unsafe_allow_html=True)
    c4.markdown(metric_card("Total Revenue", f"${metrics['total_revenue']:,.0f}", "", "💰"), unsafe_allow_html=True)

    # ── Pipeline + Activity ──────────────────────────────────────────────
    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.markdown(section_title("Pipeline Overview"), unsafe_allow_html=True)
        st.markdown(pipeline_bar(metrics["pipeline_counts"]), unsafe_allow_html=True)

        # Campaign cards
        for camp in data["campaigns"]:
            pct = (camp.spent / camp.budget * 100) if camp.budget else 0
            status_color = COLORS["success"] if camp.status == "Active" else COLORS["text_muted"]
            st.markdown(f"""
            <div style="background:{COLORS["surface"]};border:1px solid {COLORS["border"]};border-radius:10px;
                padding:14px 16px;margin-bottom:8px">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <div>
                        <span style="font-weight:600;font-size:14px;color:{COLORS["text"]}">{camp.name}</span>
                        <span style="color:{COLORS["text_muted"]};font-size:12px;margin-left:8px">{camp.brand}</span>
                    </div>
                    <span style="background:{status_color}20;color:{status_color};padding:2px 10px;
                        border-radius:6px;font-size:11px;font-weight:600">{camp.status}</span>
                </div>
                <div style="display:flex;gap:20px;margin-top:8px;font-size:12px;color:{COLORS["text_secondary"]}">
                    <span>Budget: <strong style="color:{COLORS["text"]}">${camp.budget:,}</strong></span>
                    <span>Spent: <strong style="color:{COLORS["text"]}">${camp.spent:,}</strong></span>
                    <span>Utilization: <strong style="color:{COLORS["text"]}">{pct:.0f}%</strong></span>
                </div>
                <div style="background:{COLORS["bg"]};border-radius:4px;height:4px;margin-top:10px;overflow:hidden">
                    <div style="background:{status_color};height:100%;width:{min(pct, 100)}%;border-radius:4px"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_r:
        st.markdown(section_title("Recent Activity"), unsafe_allow_html=True)
        for ev in data["activity_feed"][:6]:
            st.markdown(activity_item(ev), unsafe_allow_html=True)

    # ── CTA ──────────────────────────────────────────────────────────────
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    if st.button("🔍  Find New Influencers", key="dash_cta", use_container_width=True):
        st.session_state["nav"] = "Find & Reach Out"
        st.rerun()
