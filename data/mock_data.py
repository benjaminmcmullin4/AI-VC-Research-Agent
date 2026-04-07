"""Central data accessor and derived metrics calculator."""

from __future__ import annotations

import random
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

from data.activity_feed import get_activity_feed
from data.campaigns import get_campaigns
from data.conversations import get_conversations
from data.influencers import get_influencers
from schema import Influencer

# Seeded multipliers for revenue consistency
random.seed(42)
_REVENUE_MULTIPLIERS = {i: random.uniform(3.0, 8.0) for i in range(20)}


@st.cache_data
def load_all_data() -> dict:
    """Load all mock data, cached for the session."""
    return {
        "influencers": get_influencers(),
        "campaigns": get_campaigns(),
        "conversations": get_conversations(),
        "activity_feed": get_activity_feed(),
    }


def compute_dashboard_metrics(data: dict) -> dict:
    """Compute all KPIs from the underlying influencer data."""
    influencers: list[Influencer] = data["influencers"]
    stages = [i.status for i in influencers]

    total = len(influencers)
    qualified = sum(1 for s in stages if s != "Discovered")
    contacted = sum(1 for s in stages if s in ("Contacted", "Replied", "Negotiating", "Signed", "Content Posted", "Converted"))
    replied = sum(1 for s in stages if s in ("Replied", "Negotiating", "Signed", "Content Posted", "Converted"))
    negotiating = sum(1 for s in stages if s in ("Negotiating", "Signed", "Content Posted", "Converted"))
    signed = sum(1 for s in stages if s in ("Signed", "Content Posted", "Converted"))
    content_posted = sum(1 for s in stages if s in ("Content Posted", "Converted"))
    converted = sum(1 for s in stages if s == "Converted")

    total_revenue = sum(i.revenue_generated for i in influencers if i.revenue_generated > 0)
    total_spent = sum(c.spent for c in data["campaigns"])

    reply_rate = (replied / contacted * 100) if contacted else 0
    conversion_rate = (converted / content_posted * 100) if content_posted else 0

    return {
        "total_influencers": total,
        "qualified": qualified,
        "contacted": contacted,
        "replied": replied,
        "negotiating": negotiating,
        "signed": signed,
        "content_posted": content_posted,
        "converted": converted,
        "total_revenue": total_revenue,
        "total_spent": total_spent,
        "reply_rate": reply_rate,
        "conversion_rate": conversion_rate,
        "deals_active": sum(1 for s in stages if s in ("Negotiating", "Signed")),
        "pipeline_counts": {
            "Discovered": sum(1 for s in stages if s == "Discovered"),
            "Qualified": sum(1 for s in stages if s == "Qualified"),
            "Contacted": sum(1 for s in stages if s == "Contacted"),
            "Replied": sum(1 for s in stages if s == "Replied"),
            "Negotiating": sum(1 for s in stages if s == "Negotiating"),
            "Signed": sum(1 for s in stages if s == "Signed"),
            "Content Posted": sum(1 for s in stages if s == "Content Posted"),
            "Converted": sum(1 for s in stages if s == "Converted"),
        },
    }


def compute_revenue_by_influencer(data: dict) -> pd.DataFrame:
    """Revenue breakdown for influencers with revenue > 0."""
    rows = []
    for i in data["influencers"]:
        if i.revenue_generated > 0:
            rows.append({
                "Name": i.name,
                "Handle": i.handle,
                "Platform": i.platform,
                "Revenue": i.revenue_generated,
                "Cost": i.estimated_cost,
                "ROI": round(i.revenue_generated / i.estimated_cost, 1) if i.estimated_cost else 0,
            })
    df = pd.DataFrame(rows)
    return df.sort_values("Revenue", ascending=False).reset_index(drop=True) if len(df) else df


def compute_revenue_by_platform(data: dict) -> pd.DataFrame:
    """Total revenue aggregated by platform."""
    rows = []
    for i in data["influencers"]:
        if i.revenue_generated > 0:
            rows.append({"Platform": i.platform, "Revenue": i.revenue_generated})
    df = pd.DataFrame(rows)
    if len(df):
        return df.groupby("Platform", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)
    return df


def compute_outreach_over_time(data: dict) -> pd.DataFrame:
    """Daily outreach and reply counts from activity feed over last 30 days."""
    today = datetime(2026, 4, 6)
    dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]
    date_set = set(dates)

    outreach_counts = {d: 0 for d in dates}
    reply_counts = {d: 0 for d in dates}

    for event in data["activity_feed"]:
        day = event.timestamp[:10]
        if day in date_set:
            if event.event_type == "outreach":
                outreach_counts[day] += 1
            elif event.event_type == "reply_detected":
                reply_counts[day] += 1

    rows = [{"Date": d, "Outreach": outreach_counts[d], "Replies": reply_counts[d]} for d in sorted(dates)]
    return pd.DataFrame(rows)


def get_top_recommended(data: dict, n: int = 10) -> list[Influencer]:
    """Top N influencers by combined score from Discovered/Qualified status only."""
    candidates = [
        i for i in data["influencers"]
        if i.status in ("Discovered", "Qualified")
    ]
    candidates.sort(
        key=lambda i: 0.6 * i.audience_fit_score + 0.4 * i.brand_fit_score,
        reverse=True,
    )
    return candidates[:n]
