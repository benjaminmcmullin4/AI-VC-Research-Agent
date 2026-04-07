"""Analytics page — conversion rates, revenue, and trends."""

from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import COLORS
from data.mock_data import (
    compute_outreach_over_time,
    compute_revenue_by_influencer,
    compute_revenue_by_platform,
)


def _metric_card(label: str, value: str) -> str:
    return f"""
    <div class="metric-card">
        <h4>{label}</h4>
        <div class="value">{value}</div>
    </div>
    """


def render_analytics(data: dict, metrics: dict):
    st.markdown('<div class="section-header">Analytics</div>', unsafe_allow_html=True)

    # ── Funnel conversion rate metrics ───────────────────────────────────
    p = metrics["pipeline_counts"]
    total = metrics["total_influencers"]

    # Calculate stage-to-stage rates
    outreach_to_reply = (metrics["replied"] / metrics["contacted"] * 100) if metrics["contacted"] else 0
    reply_to_deal = (metrics["negotiating"] / metrics["replied"] * 100) if metrics["replied"] else 0
    deal_to_post = (metrics["content_posted"] / metrics["signed"] * 100) if metrics["signed"] else 0
    post_to_convert = (metrics["conversion_rate"])

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(_metric_card("Outreach to Reply", f"{outreach_to_reply:.0f}%"), unsafe_allow_html=True)
    c2.markdown(_metric_card("Reply to Deal", f"{reply_to_deal:.0f}%"), unsafe_allow_html=True)
    c3.markdown(_metric_card("Deal to Content", f"{deal_to_post:.0f}%"), unsafe_allow_html=True)
    c4.markdown(_metric_card("Content to Conversion", f"{post_to_convert:.0f}%"), unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ── Charts row 1 ─────────────────────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="section-header">Revenue by Influencer</div>', unsafe_allow_html=True)
        df_rev = compute_revenue_by_influencer(data)
        if len(df_rev):
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=df_rev["Name"], x=df_rev["Revenue"], name="Revenue",
                orientation="h", marker_color=COLORS["teal"],
            ))
            fig.add_trace(go.Bar(
                y=df_rev["Name"], x=df_rev["Cost"], name="Cost",
                orientation="h", marker_color=COLORS["light_gray"],
            ))
            fig.update_layout(
                barmode="group", margin=dict(l=10, r=10, t=10, b=10), height=320,
                font=dict(family="Inter"), plot_bgcolor="white", paper_bgcolor="white",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                yaxis=dict(autorange="reversed"),
                xaxis=dict(showgrid=True, gridcolor="#ECF0F1", tickprefix="$", tickformat=","),
            )
            st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown('<div class="section-header">Revenue by Platform</div>', unsafe_allow_html=True)
        df_plat = compute_revenue_by_platform(data)
        if len(df_plat):
            platform_colors = {"Instagram": "#E1306C", "TikTok": "#333", "YouTube": "#FF0000", "Twitter": "#1DA1F2"}
            fig2 = px.pie(
                df_plat, values="Revenue", names="Platform",
                color="Platform", color_discrete_map=platform_colors,
                hole=0.45,
            )
            fig2.update_layout(
                margin=dict(l=10, r=10, t=10, b=10), height=320,
                font=dict(family="Inter"), paper_bgcolor="white",
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
            )
            fig2.update_traces(textinfo="label+percent", textfont_size=12)
            st.plotly_chart(fig2, use_container_width=True)

    # ── Top performers table ─────────────────────────────────────────────
    st.markdown('<div class="section-header">Top Performers by ROI</div>', unsafe_allow_html=True)
    df_rev = compute_revenue_by_influencer(data)
    if len(df_rev):
        top_roi = df_rev.sort_values("ROI", ascending=False).head(5)
        for _, row in top_roi.iterrows():
            roi_color = "#1ABC9C" if row["ROI"] >= 4 else ("#D4A338" if row["ROI"] >= 2 else "#777")
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #ECF0F1">
                <div>
                    <span style="font-weight:600">{row['Name']}</span>
                    <span style="color:#777;font-size:0.82rem;margin-left:8px">{row['Handle']}</span>
                    <span style="color:#999;font-size:0.78rem;margin-left:8px">{row['Platform']}</span>
                </div>
                <div style="display:flex;gap:20px;align-items:center;font-size:0.85rem">
                    <div><span style="color:#777">Cost:</span> ${row['Cost']:,.0f}</div>
                    <div><span style="color:#777">Revenue:</span> <strong>${row['Revenue']:,.0f}</strong></div>
                    <div style="background:{roi_color}22;color:{roi_color};padding:2px 10px;border-radius:12px;font-weight:600">{row['ROI']}x ROI</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Trends over time ─────────────────────────────────────────────────
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Activity Trends (30 Days)</div>', unsafe_allow_html=True)
    df_trends = compute_outreach_over_time(data)
    # Compute cumulative
    df_trends["Cumulative Outreach"] = df_trends["Outreach"].cumsum()
    df_trends["Cumulative Replies"] = df_trends["Replies"].cumsum()

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=df_trends["Date"], y=df_trends["Cumulative Outreach"],
        mode="lines", name="Cumulative Outreach",
        line=dict(color=COLORS["teal"], width=2.5),
        fill="tozeroy", fillcolor="rgba(26,188,156,0.08)",
    ))
    fig3.add_trace(go.Scatter(
        x=df_trends["Date"], y=df_trends["Cumulative Replies"],
        mode="lines", name="Cumulative Replies",
        line=dict(color=COLORS["gold"], width=2.5),
        fill="tozeroy", fillcolor="rgba(212,163,56,0.08)",
    ))
    fig3.update_layout(
        margin=dict(l=10, r=10, t=10, b=10), height=300,
        font=dict(family="Inter"), plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#ECF0F1"),
    )
    st.plotly_chart(fig3, use_container_width=True)
