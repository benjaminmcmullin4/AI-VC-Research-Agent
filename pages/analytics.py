"""Analytics — revenue, conversion funnel, budget tracking, active roster."""

from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components import budget_bar, metric_card, section_label
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
    sim = st.session_state.get("sim")
    is_sim = sim and sim.get("active")

    st.markdown(f'<h1 style="font-size:28px;font-weight:700;margin-bottom:4px">Analytics</h1>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:14px;color:{COLORS["text_sec"]};margin-bottom:32px">Revenue, conversions, and influencer performance</div>', unsafe_allow_html=True)

    # ── Hero metrics ─────────────────────────────────────────────────────
    onboarded_count = sum(1 for i in data["influencers"] if i.status in ("Signed", "Content Posted", "Converted"))
    total_cost = sum(i.estimated_cost for i in data["influencers"] if i.status in ("Signed", "Content Posted", "Converted"))
    cost_per_onboard = total_cost / onboarded_count if onboarded_count else 0

    total_revenue = sim.get("total_revenue", metrics["total_revenue"]) if is_sim else metrics["total_revenue"]
    budget_spent = sim.get("budget_spent", 0) if is_sim else metrics.get("total_spent", 0)
    roi = total_revenue / budget_spent if budget_spent > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(metric_card("Total Revenue", f"${total_revenue:,.0f}"), unsafe_allow_html=True)
    c2.markdown(metric_card("ROI", f"{roi:.1f}x" if budget_spent > 0 else "—"), unsafe_allow_html=True)
    c3.markdown(metric_card("Avg Cost / Onboard", f"${cost_per_onboard:,.0f}"), unsafe_allow_html=True)
    c4.markdown(metric_card("Active Influencers", str(onboarded_count)), unsafe_allow_html=True)

    # ── Budget tracking (simulation mode) ────────────────────────────────
    if is_sim:
        st.markdown(section_label("Budget Utilization"), unsafe_allow_html=True)
        budget_total = sim.get("budget_total", 0)
        budget_committed = sim.get("budget_committed", 0)
        st.markdown(budget_bar(budget_total, budget_spent, budget_committed), unsafe_allow_html=True)

    # ── Revenue over time (simulation mode) ──────────────────────────────
    if is_sim and sim.get("revenue_by_day"):
        st.markdown(section_label("Revenue Over Time"), unsafe_allow_html=True)
        rev_data = sim["revenue_by_day"]
        current_day = sim.get("day", len(rev_data))

        # Build cumulative revenue series from actual data
        days = [d for d, _ in rev_data]
        daily_rev = [r for _, r in rev_data]
        cumulative = []
        running = 0.0
        for r in daily_rev:
            running += r
            cumulative.append(round(running, 2))

        # Project revenue forward to day 180 using posted influencers' decay curves
        from simulation.budget_tracker import calculate_daily_revenue
        posted_influencers = []
        pipeline = sim.get("pipeline", {})
        for handle, info in pipeline.items():
            if info["stage"] in ("Content Posted", "Converted"):
                # Find content_posted_day from pool
                posted_day = None
                for inf in sim.get("pool", []):
                    if inf["handle"] == handle:
                        posted_day = inf.get("content_posted_day")
                        break
                if posted_day is not None:
                    posted_influencers.append({
                        "deal_value": info["deal_value"],
                        "roi_multiplier": info.get("roi_multiplier", 5.0),
                        "content_posted_day": posted_day,
                    })

        proj_days = []
        proj_cumulative = []
        proj_running = running  # start from last actual value
        for future_day in range(current_day + 1, 181):
            day_rev = 0.0
            for pi in posted_influencers:
                days_since = future_day - pi["content_posted_day"]
                day_rev += calculate_daily_revenue(
                    pi["deal_value"], days_since, pi["roi_multiplier"]
                )
            proj_running += day_rev
            proj_days.append(future_day)
            proj_cumulative.append(round(proj_running, 2))

        fig_rev = go.Figure()
        fig_rev.add_trace(go.Scatter(
            x=days, y=cumulative, mode="lines+markers",
            fill="tozeroy",
            line=dict(color=COLORS["accent"], width=2),
            marker=dict(size=4),
            name="Actual Revenue",
        ))
        if proj_days:
            # Connect projection to actual data
            bridge_days = [days[-1]] + proj_days
            bridge_cumulative = [cumulative[-1]] + proj_cumulative
            fig_rev.add_trace(go.Scatter(
                x=bridge_days, y=bridge_cumulative, mode="lines",
                line=dict(color=COLORS["accent"], width=2, dash="dot"),
                name="Projected Revenue",
            ))
        fig_rev.update_layout(
            xaxis_title="Day", yaxis_title="Revenue ($)",
            yaxis=dict(tickprefix="$", tickformat=","),
        )
        st.plotly_chart(_light_layout(fig_rev, 280), use_container_width=True)

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
    else:
        st.info("No influencers onboarded yet. Advance the simulation to sign deals.")

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
        (c1, "Outreach → Reply", outreach_to_reply),
        (c2, "Reply → Deal", reply_to_deal),
        (c3, "Deal → Content", deal_to_post),
        (c4, "Content → Convert", post_to_convert),
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
            fig = px.bar(df_rev.head(10), x="Revenue", y="Name", orientation="h", color_discrete_sequence=[COLORS["accent"]])
            fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed", showgrid=False), xaxis=dict(tickprefix="$", tickformat=","))
            st.plotly_chart(_light_layout(fig, 280), use_container_width=True)
        else:
            st.info("No revenue data yet.")

    with col_r:
        st.markdown(section_label("Revenue by Platform"), unsafe_allow_html=True)
        df_plat = compute_revenue_by_platform(data)
        if len(df_plat):
            fig2 = px.pie(df_plat, values="Revenue", names="Platform", hole=0.5,
                          color_discrete_sequence=[COLORS["accent"], "#10B981", "#EF4444", "#F59E0B"])
            fig2.update_traces(textinfo="label+percent", textfont_size=12)
            fig2.update_layout(showlegend=False)
            st.plotly_chart(_light_layout(fig2, 280), use_container_width=True)
        else:
            st.info("No revenue data yet.")
