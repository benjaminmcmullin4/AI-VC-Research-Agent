"""Tab 3: Investment thesis — why now, entry points, risks."""

from __future__ import annotations

import streamlit as st

from config import COLORS
from schema import InvestmentThesis, MarketSizing
from viz import risk_heatmap, tam_sam_bar


def render_thesis(thesis: InvestmentThesis, sizing: MarketSizing) -> None:
    """Render the Thesis tab content."""

    # Thesis statement — prominent
    st.markdown(
        f"""<div style="background: linear-gradient(135deg, #0A0A0A, #333333);
        color: white; padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem;">
        <h3 style="margin: 0 0 0.5rem 0; color: #1ABC9C;">Investment Thesis</h3>
        <p style="font-size: 1.1rem; margin: 0; line-height: 1.5;">{thesis.thesis_statement}</p>
        </div>""",
        unsafe_allow_html=True,
    )

    # TAM/SAM visual
    st.markdown('<div class="section-header">Market Sizing</div>', unsafe_allow_html=True)
    fig = tam_sam_bar(sizing)
    st.plotly_chart(fig, use_container_width=True)

    # Why now
    st.markdown('<div class="section-header">Why Now?</div>', unsafe_allow_html=True)
    for item in thesis.why_now:
        st.markdown(f"- {item}")

    # Two columns: entry points + winner characteristics
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Entry Points</div>', unsafe_allow_html=True)
        for ep in thesis.entry_points:
            st.markdown(f"- {ep}")
    with col2:
        st.markdown('<div class="section-header">Winner Characteristics</div>', unsafe_allow_html=True)
        for wc in thesis.winner_characteristics:
            st.markdown(f"- {wc}")

    # Risks
    st.markdown('<div class="section-header">Risk Assessment</div>', unsafe_allow_html=True)
    fig = risk_heatmap(thesis)
    st.plotly_chart(fig, use_container_width=True)

    # Risk details table
    with st.expander("Risk Details & Mitigants"):
        for risk in sorted(thesis.risks, key=lambda r: r.severity, reverse=True):
            severity_class = f"severity-{risk.severity}"
            st.markdown(
                f'<span class="severity-badge {severity_class}">{risk.severity}/5</span> '
                f"**{risk.risk}**",
                unsafe_allow_html=True,
            )
            st.markdown(f"_{risk.description}_")
            st.markdown(f"**Mitigant:** {risk.mitigant}")
            st.markdown("---")

    # Value creation angles
    if thesis.value_creation_angles:
        st.markdown('<div class="section-header">Value Creation Angles</div>', unsafe_allow_html=True)
        for vc in thesis.value_creation_angles:
            st.markdown(f"- {vc}")

    # Key unknowns + diligence in expander
    with st.expander("Key Unknowns & Diligence Plan"):
        st.markdown("**Key Unknowns**")
        for ku in thesis.key_unknowns:
            st.markdown(f"- {ku}")
        st.markdown("**Recommended Diligence Steps**")
        for dp in thesis.diligence_plan:
            st.markdown(f"1. {dp}")
        st.markdown("**Sourcing Angles**")
        for sa in thesis.sourcing_angles:
            st.markdown(f"- {sa}")
