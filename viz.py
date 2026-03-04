"""Plotly visualizations — market map, segment distribution, risk heatmap."""

from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go

from config import COLORS, SEGMENT_COLORS
from schema import CompanyLandscape, InvestmentThesis, MarketSizing, Taxonomy


# ── Stage → numeric size for bubble chart ──────────────────────────────
_STAGE_SIZE = {
    "Seed": 15,
    "Series A": 25,
    "Series B": 40,
    "Growth": 60,
    "Late Stage": 60,
    "Growth / Late Stage": 60,
    "Public": 80,
    "Unknown": 20,
}

_STAGE_ORDER = ["Seed", "Series A", "Series B", "Growth", "Public", "Unknown"]


def market_map_bubble(landscape: CompanyLandscape, taxonomy: Taxonomy) -> go.Figure:
    """Interactive bubble chart: x = segment index, y = stage, size = stage maturity, color = segment."""
    rows = []
    segment_names = [s.name for s in taxonomy.segments]

    for bucket in landscape.buckets:
        for co in bucket.companies:
            seg_idx = segment_names.index(co.segment) if co.segment in segment_names else 0
            stage_idx = _STAGE_ORDER.index(co.stage) if co.stage in _STAGE_ORDER else len(_STAGE_ORDER) - 1
            rows.append({
                "Company": co.name,
                "Segment": co.segment,
                "Stage": co.stage,
                "One-Liner": co.one_liner,
                "Differentiation": co.differentiation,
                "Source": co.source_label,
                "x": seg_idx + 1,
                "y": stage_idx + 1,
                "size": _STAGE_SIZE.get(co.stage, 20),
            })

    if not rows:
        fig = go.Figure()
        fig.add_annotation(text="No companies to display", showarrow=False, font=dict(size=16))
        return fig

    fig = px.scatter(
        rows,
        x="x",
        y="y",
        size="size",
        color="Segment",
        hover_name="Company",
        hover_data={
            "One-Liner": True,
            "Stage": True,
            "Differentiation": True,
            "Source": True,
            "x": False,
            "y": False,
            "size": False,
        },
        color_discrete_sequence=SEGMENT_COLORS,
        size_max=30,
    )

    fig.update_layout(
        title=None,
        xaxis=dict(
            title="Segment",
            tickmode="array",
            tickvals=list(range(1, len(segment_names) + 1)),
            ticktext=segment_names,
            gridcolor=COLORS["light_gray"],
        ),
        yaxis=dict(
            title="Funding Stage",
            tickmode="array",
            tickvals=list(range(1, len(_STAGE_ORDER) + 1)),
            ticktext=_STAGE_ORDER,
            gridcolor=COLORS["light_gray"],
        ),
        plot_bgcolor=COLORS["white"],
        paper_bgcolor=COLORS["white"],
        font=dict(family="Inter, sans-serif", color=COLORS["text"]),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(l=60, r=30, t=30, b=80),
        height=500,
    )
    return fig


def segment_distribution_bar(landscape: CompanyLandscape) -> go.Figure:
    """Horizontal bar chart of company count per segment."""
    segments = []
    counts = []
    for bucket in landscape.buckets:
        segments.append(bucket.segment_name)
        counts.append(len(bucket.companies))

    fig = go.Figure(go.Bar(
        x=counts,
        y=segments,
        orientation="h",
        marker_color=COLORS["steel_blue"],
        text=counts,
        textposition="outside",
    ))
    fig.update_layout(
        title=None,
        xaxis_title="Number of Companies",
        yaxis=dict(autorange="reversed"),
        plot_bgcolor=COLORS["white"],
        paper_bgcolor=COLORS["white"],
        font=dict(family="Inter, sans-serif", color=COLORS["text"]),
        margin=dict(l=150, r=30, t=20, b=40),
        height=max(250, len(segments) * 50),
    )
    return fig


def risk_heatmap(thesis: InvestmentThesis) -> go.Figure:
    """Horizontal bar chart of risks colored by severity."""
    risks = sorted(thesis.risks, key=lambda r: r.severity, reverse=True)
    labels = [r.risk[:50] for r in risks]
    severities = [r.severity for r in risks]
    hover_texts = [f"{r.risk}<br>Mitigant: {r.mitigant}" for r in risks]

    # Color map: 1=green, 3=gold, 5=red
    colors = []
    for s in severities:
        if s <= 2:
            colors.append(COLORS["teal"])
        elif s <= 3:
            colors.append(COLORS["gold_accent"])
        else:
            colors.append(COLORS["red_accent"])

    fig = go.Figure(go.Bar(
        x=severities,
        y=labels,
        orientation="h",
        marker_color=colors,
        text=[f"Severity {s}/5" for s in severities],
        textposition="outside",
        hovertext=hover_texts,
        hoverinfo="text",
    ))
    fig.update_layout(
        title=None,
        xaxis=dict(title="Severity", range=[0, 6], dtick=1),
        yaxis=dict(autorange="reversed"),
        plot_bgcolor=COLORS["white"],
        paper_bgcolor=COLORS["white"],
        font=dict(family="Inter, sans-serif", color=COLORS["text"]),
        margin=dict(l=200, r=60, t=20, b=40),
        height=max(250, len(risks) * 55),
    )
    return fig


def tam_sam_bar(sizing: MarketSizing) -> go.Figure:
    """Side-by-side range bars for TAM and SAM."""
    fig = go.Figure()

    categories = ["SAM", "TAM"]
    lows = [sizing.sam_low_b, sizing.tam_low_b]
    highs = [sizing.sam_high_b, sizing.tam_high_b]

    # Low (base) — invisible
    fig.add_trace(go.Bar(
        y=categories,
        x=lows,
        orientation="h",
        marker_color="rgba(0,0,0,0)",
        showlegend=False,
        hoverinfo="skip",
    ))

    # Range portion
    fig.add_trace(go.Bar(
        y=categories,
        x=[h - l for h, l in zip(highs, lows)],
        orientation="h",
        marker_color=[COLORS["teal"], COLORS["steel_blue"]],
        text=[f"${l:.1f}B – ${h:.1f}B" for l, h in zip(lows, highs)],
        textposition="outside",
        hovertemplate="%{y}: $%{text}<extra></extra>",
        showlegend=False,
    ))

    fig.update_layout(
        barmode="stack",
        title=None,
        xaxis_title="Market Size ($B)",
        plot_bgcolor=COLORS["white"],
        paper_bgcolor=COLORS["white"],
        font=dict(family="Inter, sans-serif", color=COLORS["text"]),
        margin=dict(l=60, r=100, t=20, b=40),
        height=200,
    )
    return fig
