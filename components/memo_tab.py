"""Tab 4: Full rendered memo with PDF/DOCX download."""

from __future__ import annotations

import streamlit as st

from config import MEMO_SECTIONS
from export import generate_docx, generate_pdf
from schema import MarketMemo


def render_memo(memo: MarketMemo) -> None:
    """Render the Memo tab with full text and download buttons."""

    # Download buttons at top
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        pdf_bytes = generate_pdf(memo)
        st.download_button(
            "Download PDF",
            data=pdf_bytes,
            file_name=f"{memo.title.replace(' ', '_')}_Memo.pdf",
            mime="application/pdf",
        )
    with col2:
        docx_bytes = generate_docx(memo)
        st.download_button(
            "Download DOCX",
            data=docx_bytes,
            file_name=f"{memo.title.replace(' ', '_')}_Memo.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    st.markdown("---")

    # Title
    st.markdown(f"# {memo.title}")
    st.markdown(f"*Market Research Memo  |  {memo.date}*")
    st.markdown("---")

    # Render each section
    sections = [
        ("Executive Summary", memo.executive_summary),
        ("Market Overview", memo.market_overview),
        ("TAM / SAM Sizing", memo.tam_sam_sizing),
        ("Competitive Landscape", memo.competitive_landscape),
        ("Taxonomy & Segmentation", memo.taxonomy_segmentation),
        ("Company Profiles", memo.company_profiles),
        ("Investment Thesis", memo.investment_thesis),
        ("Value Creation Angles", memo.value_creation_angles),
        ("Risks & Mitigants", memo.risks_and_mitigants),
        ("Diligence Plan", memo.diligence_plan),
        ("Sources & Methodology", memo.sources_and_methodology),
    ]

    for heading, content in sections:
        st.markdown(f"## {heading}")
        st.markdown(content)
        st.markdown("---")

    st.markdown(
        '<p class="citation">Mercato Partners — Internal Use Only</p>',
        unsafe_allow_html=True,
    )
