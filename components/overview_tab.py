"""Tab 1: Market definition, ICP, value chain, key metrics."""

from __future__ import annotations

import streamlit as st

from config import COLORS
from schema import MarketSpec, MarketSizing


def _metric_card(label: str, value: str) -> str:
    return f"""<div class="metric-card">
        <h4>{label}</h4>
        <div class="value">{value}</div>
    </div>"""


def render_overview(spec: MarketSpec, sizing: MarketSizing) -> None:
    """Render the Overview tab content."""

    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            _metric_card("TAM Range", f"${sizing.tam_low_b:.1f}B – ${sizing.tam_high_b:.1f}B"),
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            _metric_card("SAM Range", f"${sizing.sam_low_b:.1f}B – ${sizing.sam_high_b:.1f}B"),
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            _metric_card("Growth (CAGR)", f"{sizing.growth_rate_pct:.1f}%"),
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            _metric_card("Confidence", sizing.confidence),
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Market definition
    st.markdown('<div class="section-header">Market Definition</div>', unsafe_allow_html=True)
    st.markdown(spec.definition)

    # ICP
    st.markdown('<div class="section-header">Ideal Customer Profile</div>', unsafe_allow_html=True)
    st.markdown(spec.ideal_customer_profile)

    # Value chain
    st.markdown('<div class="section-header">Value Chain</div>', unsafe_allow_html=True)
    chain_display = " → ".join(spec.value_chain)
    st.markdown(f"**{chain_display}**")

    # Two columns: workflows + pricing
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Key Workflows</div>', unsafe_allow_html=True)
        for wf in spec.key_workflows:
            st.markdown(f"- {wf}")
    with col2:
        st.markdown('<div class="section-header">Pricing Models</div>', unsafe_allow_html=True)
        for pm in spec.pricing_models:
            st.markdown(f"- {pm}")

    # Regulatory + assumptions in expander
    with st.expander("Regulatory Context & Assumptions"):
        st.markdown("**Regulatory Context**")
        st.markdown(spec.regulatory_context)
        st.markdown("**Assumptions**")
        for a in spec.assumptions:
            st.markdown(f"- {a}")
