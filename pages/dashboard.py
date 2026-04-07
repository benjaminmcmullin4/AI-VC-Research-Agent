"""Executive Dashboard page."""

from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import COLORS, PIPELINE_STAGES, STAGE_COLORS


def _metric_card(label: str, value: str, delta: str = "") -> str:
    delta_html = f'<div style="color:#1ABC9C;font-size:0.78rem;margin-top:2px">{delta}</div>' if delta else ""
    return f"""
    <div class="metric-card">
        <h4>{label}</h4>
        <div class="value">{value}</div>
        {delta_html}
    </div>
    """


def render_dashboard(data: dict, metrics: dict, api_key: str | None):
    st.markdown('<div class="section-header">Executive Dashboard</div>', unsafe_allow_html=True)

    # ── AI insight box ───────────────────────────────────────────────────
    if api_key and st.button("Generate AI Insight", key="dash_ai"):
        from ai_engine import generate_dashboard_insight
        insight = generate_dashboard_insight(api_key, metrics)
        if insight:
            st.session_state["dash_insight"] = insight

    if "dash_insight" in st.session_state:
        ins = st.session_state["dash_insight"]
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0A0A0A,#1a3a2a);color:white;padding:1rem 1.4rem;border-radius:8px;margin-bottom:1.5rem;border-left:4px solid #1ABC9C">
            <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.08em;color:#1ABC9C;margin-bottom:6px">AI Campaign Insight</div>
            <div style="font-size:0.92rem;line-height:1.5">{ins.summary}</div>
            <div style="font-size:0.82rem;color:#aaa;margin-top:8px">{ins.top_recommendation}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#0A0A0A,#1a3a2a);color:white;padding:1rem 1.4rem;border-radius:8px;margin-bottom:1.5rem;border-left:4px solid #1ABC9C">
            <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.08em;color:#1ABC9C;margin-bottom:6px">Campaign Insight</div>
            <div style="font-size:0.92rem;line-height:1.5">Pipeline is healthy with a 58% reply rate on outreach, up from 42% last month. Beauty niche TikTok creators are driving 2.4x more conversions than Instagram counterparts -- consider shifting budget allocation.</div>
            <div style="font-size:0.82rem;color:#aaa;margin-top:8px">Recommendation: Increase TikTok creator budget by 15% for Q2 beauty campaigns.</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Metric cards — row 1 ─────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(_metric_card("Total Influencers", str(metrics["total_influencers"]), "+8 this week"), unsafe_allow_html=True)
    c2.markdown(_metric_card("Qualified", str(metrics["qualified"])), unsafe_allow_html=True)
    c3.markdown(_metric_card("Outreach Sent", str(metrics["contacted"])), unsafe_allow_html=True)
    c4.markdown(_metric_card("Reply Rate", f"{metrics['reply_rate']:.0f}%", "+16pp vs last month"), unsafe_allow_html=True)

    # ── Metric cards — row 2 ─────────────────────────────────────────────
    c5, c6, c7, c8 = st.columns(4)
    c5.markdown(_metric_card("Active Deals", str(metrics["deals_active"])), unsafe_allow_html=True)
    c6.markdown(_metric_card("Content Posted", str(metrics["content_posted"])), unsafe_allow_html=True)
    c7.markdown(_metric_card("Total Revenue", f"${metrics['total_revenue']:,.0f}"), unsafe_allow_html=True)
    c8.markdown(_metric_card("Conversion Rate", f"{metrics['conversion_rate']:.0f}%"), unsafe_allow_html=True)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    # ── Charts row 1 ─────────────────────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="section-header">Influencer Funnel</div>', unsafe_allow_html=True)
        pipeline = metrics["pipeline_counts"]
        # Build cumulative funnel values
        funnel_stages = PIPELINE_STAGES
        funnel_values = []
        running = metrics["total_influencers"]
        for stage in funnel_stages:
            funnel_values.append(running)
            running -= pipeline.get(stage, 0)

        fig = go.Figure(go.Funnel(
            y=funnel_stages,
            x=funnel_values,
            marker=dict(color=[STAGE_COLORS[s] for s in funnel_stages]),
            textinfo="value+percent initial",
            textfont=dict(family="Inter", size=12),
        ))
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10), height=340,
            font=dict(family="Inter"), plot_bgcolor="white", paper_bgcolor="white",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown('<div class="section-header">Outreach Over Time</div>', unsafe_allow_html=True)
        from data.mock_data import compute_outreach_over_time
        df_outreach = compute_outreach_over_time(data)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=df_outreach["Date"], y=df_outreach["Outreach"],
            mode="lines+markers", name="Outreach", line=dict(color=COLORS["teal"], width=2),
            marker=dict(size=4),
        ))
        fig2.add_trace(go.Scatter(
            x=df_outreach["Date"], y=df_outreach["Replies"],
            mode="lines+markers", name="Replies", line=dict(color=COLORS["gold"], width=2),
            marker=dict(size=4),
        ))
        fig2.update_layout(
            margin=dict(l=10, r=10, t=10, b=10), height=340,
            font=dict(family="Inter"), plot_bgcolor="white", paper_bgcolor="white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#ECF0F1"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Charts row 2 ─────────────────────────────────────────────────────
    col_left2, col_right2 = st.columns(2)

    with col_left2:
        st.markdown('<div class="section-header">Deal Pipeline</div>', unsafe_allow_html=True)
        pipeline_df_data = [{"Stage": s, "Count": pipeline[s]} for s in PIPELINE_STAGES]
        import pandas as pd
        pipeline_df = pd.DataFrame(pipeline_df_data)
        fig3 = px.bar(
            pipeline_df, x="Count", y="Stage", orientation="h",
            color="Stage", color_discrete_map=STAGE_COLORS,
        )
        fig3.update_layout(
            margin=dict(l=10, r=10, t=10, b=10), height=340, showlegend=False,
            font=dict(family="Inter"), plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(categoryorder="array", categoryarray=list(reversed(PIPELINE_STAGES))),
            xaxis=dict(showgrid=True, gridcolor="#ECF0F1"),
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col_right2:
        st.markdown('<div class="section-header">Revenue by Influencer</div>', unsafe_allow_html=True)
        from data.mock_data import compute_revenue_by_influencer
        df_rev = compute_revenue_by_influencer(data)
        if len(df_rev):
            fig4 = px.bar(
                df_rev.head(8), x="Revenue", y="Name", orientation="h",
                color_discrete_sequence=[COLORS["teal"]],
            )
            fig4.update_layout(
                margin=dict(l=10, r=10, t=10, b=10), height=340, showlegend=False,
                font=dict(family="Inter"), plot_bgcolor="white", paper_bgcolor="white",
                yaxis=dict(autorange="reversed"),
                xaxis=dict(showgrid=True, gridcolor="#ECF0F1", tickprefix="$", tickformat=","),
            )
            st.plotly_chart(fig4, use_container_width=True)

    # ── Recent agent activity ────────────────────────────────────────────
    st.markdown('<div class="section-header">Recent Agent Activity</div>', unsafe_allow_html=True)
    _event_icons = {
        "discovery": "🔍", "qualification": "⭐", "outreach": "📤",
        "reply_detected": "💬", "negotiation": "🤝", "content_posted": "📸",
        "conversion": "💰", "insight": "📊", "alert": "⚠️",
    }
    events = data["activity_feed"][:10]
    for ev in events:
        icon = _event_icons.get(ev.event_type, "📌")
        sev_color = "#1ABC9C" if ev.severity == "success" else ("#D4A338" if ev.severity == "warning" else "#777")
        st.markdown(f"""
        <div style="display:flex;align-items:flex-start;gap:10px;padding:8px 0;border-bottom:1px solid #ECF0F1">
            <span style="font-size:1.1rem">{icon}</span>
            <div style="flex:1">
                <div style="font-size:0.88rem;color:#1A1A1A">{ev.description}</div>
                <div style="font-size:0.75rem;color:{sev_color}">{ev.detail}</div>
            </div>
            <div style="font-size:0.72rem;color:#999;white-space:nowrap">{ev.timestamp[5:]}</div>
        </div>
        """, unsafe_allow_html=True)
