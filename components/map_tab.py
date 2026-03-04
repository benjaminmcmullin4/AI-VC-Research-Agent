"""Tab 5: Interactive Plotly market map."""

from __future__ import annotations

import streamlit as st

from schema import CompanyLandscape, Taxonomy
from viz import market_map_bubble


def render_map(landscape: CompanyLandscape, taxonomy: Taxonomy) -> None:
    """Render the Market Map tab with interactive bubble chart."""

    st.markdown(
        """<div style="color: #777777; font-size: 0.85rem; margin-bottom: 1rem;">
        Bubble size represents funding stage maturity. Hover over a bubble for company details.
        </div>""",
        unsafe_allow_html=True,
    )

    # Segment filter
    all_segments = [b.segment_name for b in landscape.buckets]
    selected_segments = st.multiselect(
        "Filter segments",
        options=all_segments,
        default=all_segments,
    )

    # Filter landscape
    if selected_segments and set(selected_segments) != set(all_segments):
        from schema import CompanyBucket, CompanyLandscape as CL

        filtered_buckets = [b for b in landscape.buckets if b.segment_name in selected_segments]
        filtered_count = sum(len(b.companies) for b in filtered_buckets)
        filtered_landscape = CL(
            buckets=filtered_buckets,
            total_companies=filtered_count,
            coverage_notes=landscape.coverage_notes,
        )
    else:
        filtered_landscape = landscape

    # Render chart
    fig = market_map_bubble(filtered_landscape, taxonomy)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<p class="citation">Source: AI-generated market map based on provided inputs and model knowledge. '
        "Company positions are approximate.</p>",
        unsafe_allow_html=True,
    )
