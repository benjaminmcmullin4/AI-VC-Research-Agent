"""Tab 2: Company landscape tables with expandable details."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from config import COLORS
from schema import CompanyLandscape, Taxonomy
from viz import segment_distribution_bar


def render_landscape(landscape: CompanyLandscape, taxonomy: Taxonomy) -> None:
    """Render the Landscape tab content."""

    # Summary metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Companies Mapped", landscape.total_companies)
    with col2:
        st.metric("Segments", len(landscape.buckets))

    if landscape.coverage_notes:
        st.info(f"**Coverage notes:** {landscape.coverage_notes}")

    # Distribution chart
    st.markdown('<div class="section-header">Segment Distribution</div>', unsafe_allow_html=True)
    fig = segment_distribution_bar(landscape)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Company tables by segment
    st.markdown('<div class="section-header">Companies by Segment</div>', unsafe_allow_html=True)

    for bucket in landscape.buckets:
        with st.expander(f"**{bucket.segment_name}** ({len(bucket.companies)} companies)", expanded=True):
            rows = []
            for co in bucket.companies:
                source_class = "source-from-sources" if co.source_label == "from sources" else "source-model-suggested"
                rows.append({
                    "Company": co.name,
                    "Description": co.one_liner,
                    "Stage": co.stage,
                    "Differentiation": co.differentiation,
                    "Est. ARR": co.estimated_arr_range,
                    "HQ": co.hq_location,
                    "Source": co.source_label,
                })

            df = pd.DataFrame(rows)
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Company": st.column_config.TextColumn(width="medium"),
                    "Description": st.column_config.TextColumn(width="large"),
                    "Differentiation": st.column_config.TextColumn(width="large"),
                },
            )
