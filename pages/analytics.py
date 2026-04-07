"""Analytics — revenue, conversion funnel, active roster."""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from components import metric_card, section_label
from config import COLORS
from data.mock_data import compute_revenue_by_influencer, compute_revenue_by_platform, get_active_roster


def _light_layout(fig, height=320):
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0), height=height,
        font=dict(family="Inter", color=COLORS["text_sec"]),
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
    )
    return fig


def render_analytics(data: dict, metrics: dict):
    st.markdown(f'<h1 style="font-size:28px;font-weight:700;margin-bottom:4px">Analytics</h1>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:14px;color:{COLORS["text_sec"]};margin-bottom:32px">Revenue, conversions, and influencer performance</div>', unsafe_allow_html=True)

    # ── Hero metrics ─────────────────────────────────────────────────────
    onboarded_count = metrics["signed"] + metrics["content_posted"] + metrics["converted"] - metrics["negotiating"]
    # Simpler: count from data directly
    onboarded_count = sum(1 for i in data["influencers"] if i.status in ("Signed", "Content Posted", "Converted"))
    total_cost = sum(i.estimated_cost for i in data["influencers"] if i.status in ("Signed", "Content Posted", "Converted"))
    cost_per_onboard = total_cost / onboarded_count if onboarded_count else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(metric_card("Total Revenue", f"${metrics['total_revenue']:,.0f}"), unsafe_allow_html=True)
    c2.markdown(metric_card("Outreach → Onboard", f"{(onboarded_count / metrics['contacted'] * 100):.0f}%" if metrics["contacted"] else "0%"), unsafe_allow_html=True)
    c3.markdown(metric_card("Avg Cost / Onboard", f"${cost_per_onboard:,.0f}"), unsafe_allow_html=True)
    c4.markdown(metric_card("Active Influencers", str(onboarded_count)), unsafe_allow_html=True)

    # ── Active Roster ────────────────────────────────────────────────────
    st.markdown(section_label("Active Influencer Roster"), unsafe_allow_html=True)
    df_roster = get_active_roster(data)
    if len(df_roster):
        st.dataframe(
            df_roster.style.format({
                "Est. Cost": "${:,.0f}",
                "Revenue": "${:,.0f}",
                "ROI": "{:.1f}x",
            }),
            use_container_width=True,
            height=min(350, 35 * len(df_roster) + 38),
        )

    # ── Conversion metrics ───────────────────────────────────────────────
    st.markdown(section_label("Conversion Rates"), unsafe_allow_html=True)

    contacted = metrics["contacted"]
    replied = metrics["replied"]
    negotiating = metrics["negotiating"]
    signed = metrics["signed"]
    posted = metrics["content_posted"]
    converted = metrics["converted"]

    outreach_to_reply = (replied / contacted * 100) if contacted else 0
    reply_to_deal = (negotiating / replied * 100) if replied else 0
    deal_to_post = (posted / signed * 100) if signed else 0
    post_to_convert = (converted / posted * 100) if posted else 0

    c1, c2, c3, c4 = st.columns(4)
    for col, label, val in [
        (c1, "Outreach  -  Reply", outreach_to_reply),
        (c2, "Reply  -  Deal", reply_to_deal),
        (c3, "Deal  -  Content", deal_to_post),
        (c4, "Content  -  Convert", post_to_convert),
    ]:
        col.markdown(f"""
        <div style="background:{COLORS["surface"]};border:1px solid {COLORS["border"]};
            border-radius:10px;padding:24px;text-align:center">
            <div style="font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;
                color:{COLORS["text_muted"]};margin-bottom:8px">{label}</div>
            <div style="font-size:32px;font-weight:800;color:{COLORS["text"]}">{val:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Revenue charts ───────────────────────────────────────────────────
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown(section_label("Revenue by Influencer"), unsafe_allow_html=True)
        df_rev = compute_revenue_by_influencer(data)
        if len(df_rev):
            fig = px.bar(df_rev, x="Revenue", y="Name", orientation="h", color_discrete_sequence=[COLORS["accent"]])
            fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed", showgrid=False), xaxis=dict(tickprefix="$", tickformat=","))
            st.plotly_chart(_light_layout(fig, 280), use_container_width=True)

    with col_r:
        st.markdown(section_label("Revenue by Platform"), unsafe_allow_html=True)
        df_plat = compute_revenue_by_platform(data)
        if len(df_plat):
            fig2 = px.pie(df_plat, values="Revenue", names="Platform", hole=0.5,
                          color_discrete_sequence=[COLORS["accent"], "#10B981", "#EF4444", "#F59E0B"])
            fig2.update_traces(textinfo="label+percent", textfont_size=12)
            fig2.update_layout(showlegend=False)
            st.plotly_chart(_light_layout(fig2, 280), use_container_width=True)
