"""Deal Team — Market Research Platform."""

from __future__ import annotations

import json
import os
from pathlib import Path

import streamlit as st

from config import COLORS, DEMO_OUTPUT_PATH, FIRM_NAME, APP_TITLE, APP_SUBTITLE, PIPELINE_STEPS
from db import init_db, save_run
from schema import ResearchOutput
from auth import is_authenticated, get_auth_email, render_auth_gate

# ── Page config (must be first Streamlit call) ─────────────────────────
st.set_page_config(
    page_title=f"{FIRM_NAME} | {APP_TITLE}",
    page_icon="🏔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load custom CSS ────────────────────────────────────────────────────
css_path = Path(__file__).parent / "styles" / "custom.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# ── Initialize DB ──────────────────────────────────────────────────────
init_db()

# ── Detect API key ─────────────────────────────────────────────────────
api_key = os.environ.get("ANTHROPIC_API_KEY", "")
if not api_key:
    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
    except FileNotFoundError:
        api_key = ""
demo_mode = not bool(api_key)


def _load_demo_data() -> ResearchOutput | None:
    """Load pre-generated demo output if available."""
    if DEMO_OUTPUT_PATH.exists():
        return ResearchOutput.model_validate_json(DEMO_OUTPUT_PATH.read_text())
    return None


# ── Sidebar ────────────────────────────────────────────────────────────
from components.sidebar import render_sidebar

settings = render_sidebar()

# If a past run was loaded, use it
if settings["loaded_run"] is not None:
    st.session_state["research_output"] = settings["loaded_run"]

# ── Header ─────────────────────────────────────────────────────────────
st.markdown(
    f"""<h1 style="color: {COLORS['navy']}; margin-bottom: 0;">{FIRM_NAME} | {APP_TITLE}</h1>
    <p style="color: {COLORS['muted']}; margin-top: 0;">
    {APP_SUBTITLE}
    </p>""",
    unsafe_allow_html=True,
)

# Demo mode banner
if demo_mode:
    st.markdown(
        '<div class="demo-banner">'
        "🔬 <strong>Demo Mode</strong> — Add your Anthropic API key "
        "(via environment variable or Streamlit secrets) to generate custom research"
        "</div>",
        unsafe_allow_html=True,
    )
    demo_data = _load_demo_data()
    if demo_data:
        st.session_state["research_output"] = demo_data

# ── Input Section ──────────────────────────────────────────────────────
if "research_output" not in st.session_state:
    st.markdown('<div class="section-header">New Research</div>', unsafe_allow_html=True)

    query = st.text_input(
        "Market or sector to research",
        placeholder="e.g., AI-powered accounting automation for SMBs",
    )

    col1, col2 = st.columns(2)
    with col1:
        from config import GEOGRAPHY_OPTIONS
        geography = st.selectbox("Geography Focus", GEOGRAPHY_OPTIONS)
    with col2:
        from config import STAGE_OPTIONS
        stage_focus = st.radio("Stage Focus", STAGE_OPTIONS, horizontal=True)

    include_sources = st.toggle("Include pasted sources / notes", value=True)
    sources = ""
    if include_sources:
        sources = st.text_area(
            "Paste sources, articles, or notes (optional)",
            height=120,
            placeholder="Paste any relevant articles, data points, or notes here...",
        )

    # Generate button — requires authentication (unless demo mode)
    generate_disabled = demo_mode or not query.strip()
    if not demo_mode and not generate_disabled:
        # Auth gate: must be verified before generating
        if not is_authenticated():
            st.markdown("---")
            auth_ok = render_auth_gate()
            if not auth_ok:
                st.stop()

    if st.button("Generate Research", type="primary", disabled=generate_disabled, use_container_width=True):
        from pipeline import run_pipeline

        with st.status("Running research pipeline...", expanded=True) as status:
            step_updates = {}

            def on_step(idx: int, label: str, elapsed: float):
                step_updates[idx] = (label, elapsed)
                st.write(f"✅ {label} ({elapsed:.1f}s)")
                if idx < len(PIPELINE_STEPS) - 1:
                    next_label = PIPELINE_STEPS[idx + 1][1]
                    status.update(label=next_label)

            try:
                output = run_pipeline(
                    api_key=api_key,
                    query=query,
                    geography=geography,
                    stage_focus=stage_focus,
                    sources=sources,
                    detail_level=settings["detail_level"],
                    company_count=settings["company_count"],
                    temperature=settings["temperature"],
                    on_step=on_step,
                )
                st.session_state["research_output"] = output

                # Save to DB
                run_id = save_run(output)
                status.update(label="Research complete!", state="complete")

            except Exception as e:
                status.update(label="Pipeline failed", state="error")
                st.error(f"Error: {e}")
                st.stop()

        st.rerun()

    if demo_mode and not _load_demo_data():
        st.info("No demo data available. Add an API key to generate research, or run the app with demo data in `examples/demo_output.json`.")

# ── Output Section (5 Tabs) ────────────────────────────────────────────
if "research_output" in st.session_state:
    output: ResearchOutput = st.session_state["research_output"]

    # Show what was researched
    st.markdown(
        f"""<div style="background: #F0F4F8; padding: 0.8rem 1.2rem; border-radius: 8px;
        border-left: 4px solid {COLORS['teal']}; margin-bottom: 1rem;">
        <strong style="color: {COLORS['navy']};">Research:</strong> {output.query}
        &nbsp;|&nbsp; <span style="color: {COLORS['muted']};">{output.geography} · {output.stage_focus}</span>
        </div>""",
        unsafe_allow_html=True,
    )

    # New research button
    if st.button("Start New Research"):
        del st.session_state["research_output"]
        st.rerun()

    # Tabs
    tab_overview, tab_landscape, tab_thesis, tab_memo, tab_map = st.tabs([
        "Overview", "Landscape", "Thesis", "Memo", "Market Map",
    ])

    from components.overview_tab import render_overview
    from components.landscape_tab import render_landscape
    from components.thesis_tab import render_thesis
    from components.memo_tab import render_memo
    from components.map_tab import render_map

    with tab_overview:
        render_overview(output.market_spec, output.sizing)

    with tab_landscape:
        render_landscape(output.landscape, output.taxonomy)

    with tab_thesis:
        render_thesis(output.thesis, output.sizing)

    with tab_memo:
        render_memo(output.memo)

    with tab_map:
        render_map(output.landscape, output.taxonomy)
