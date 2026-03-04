"""All prompt templates for the 6-step pipeline."""

SYSTEM_PROMPT = """You are a senior associate at a top-tier growth equity firm (similar to TA Associates or General Atlantic). You produce rigorous, data-informed market research for investment committees. Your analysis should be:

- Specific and quantitative where possible (use ranges, not single numbers)
- Honest about uncertainty — flag assumptions and gaps explicitly
- Structured for quick consumption by busy partners
- Grounded in the user-provided sources when available
- Written in professional PE memo style (no marketing fluff)

Detail level for this analysis: {detail_level}"""

# ── Step 1: Market Spec ────────────────────────────────────────────────

MARKET_SPEC_PROMPT = """Analyze the following market research query and produce a structured market specification.

**Query:** {query}
**Geography focus:** {geography}
**Stage focus:** {stage_focus}

{sources_block}

Provide:
1. A canonical market name
2. A precise 2-3 sentence market definition
3. Ideal customer profile (who buys and why)
4. Value chain stages in order
5. Key workflows this market automates/enables
6. Common pricing models
7. Regulatory considerations
8. Explicit assumptions you're making

Be specific to the query. If the query is broad, narrow to the most investable subsection."""

# ── Step 2: Taxonomy ──────────────────────────────────────────────────

TAXONOMY_PROMPT = """Given this market specification, build a taxonomy of market segments.

**Market:** {market_name}
**Definition:** {definition}
**Value chain:** {value_chain}

Create 3-7 distinct segments that:
- Are mutually exclusive and collectively exhaustive for the core market
- Each have a clear wedge strategy for startups
- Include 2-3 example companies per segment (real companies if you know them)

Also identify 2-4 adjacent categories worth monitoring."""

# ── Step 3: Company Landscape ─────────────────────────────────────────

LANDSCAPE_PROMPT = """Map the competitive landscape for this market.

**Market:** {market_name}
**Definition:** {definition}
**Segments:** {segments_text}
**Target company count:** {company_count}

{sources_block}

For each company provide:
- Name, one-liner (≤15 words), segment, funding stage
- Key differentiator vs. peers
- Source label: "from sources" if mentioned in the user's pasted sources above, otherwise "model suggested"
- Estimated ARR range if you have a reasonable basis (otherwise "Unknown")
- HQ location

Group companies by segment. If you're uncertain about a company's details, include fewer companies rather than guessing. Note any coverage gaps."""

# ── Step 4: TAM/SAM Sizing ────────────────────────────────────────────

SIZING_PROMPT = """Estimate the Total Addressable Market (TAM) and Serviceable Addressable Market (SAM) for this market.

**Market:** {market_name}
**Definition:** {definition}
**Geography:** {geography}
**Segments:** {segments_text}

Requirements:
- Provide ranges (low–high), never a single number
- State your methodology (top-down, bottom-up, or triangulated)
- List every major assumption
- Estimate a CAGR growth rate
- Rate your confidence (Low / Medium / High)
- Identify 3-5 sensitivity factors that could materially change the sizing

Use $B (billions) for TAM/SAM figures."""

# ── Step 5: Investment Thesis ─────────────────────────────────────────

THESIS_PROMPT = """Synthesize an investment thesis for this market.

**Market:** {market_name}
**Definition:** {definition}
**TAM:** ${tam_low_b}B – ${tam_high_b}B | **SAM:** ${sam_low_b}B – ${sam_high_b}B
**Segments:** {segments_text}
**Key companies:** {top_companies}

Provide:
1. **Why now** — 3-5 specific catalysts making this market timely
2. **Thesis statement** — 1-2 sentences a partner would remember
3. **Entry points** — How would a growth equity firm invest in this space?
4. **Winner characteristics** — What does the category leader look like?
5. **Risks** — At least 4 risks, each rated 1-5 severity with a mitigant
6. **Key unknowns** — What needs further diligence?
7. **Diligence plan** — Concrete next steps for the deal team
8. **Sourcing angles** — How to find and approach targets
9. **Value creation angles** — Post-investment levers (ops improvement, M&A, pricing, etc.)"""

# ── Step 6: Memo Assembly ─────────────────────────────────────────────

MEMO_PROMPT = """Assemble a polished PE-style market research memo using all the structured data below.

**Market:** {market_name}
**Date:** {date}

## Structured Inputs
- **Market Spec:** {market_spec_json}
- **Taxonomy:** {taxonomy_json}
- **Landscape:** {landscape_json}
- **Sizing:** {sizing_json}
- **Thesis:** {thesis_json}

Write each of the 11 sections as polished markdown. Each section should be:
- Professional and concise (PE memo style, not academic)
- Data-forward: lead with numbers and specifics
- Actionable: what does this mean for the investment committee?

Sections:
1. Executive Summary (≤200 words — the "so what")
2. Market Overview
3. TAM / SAM Sizing
4. Competitive Landscape
5. Taxonomy & Segmentation
6. Company Profiles (brief table-friendly summaries)
7. Investment Thesis
8. Value Creation Angles
9. Risks & Mitigants
10. Diligence Plan
11. Sources & Methodology

Use markdown formatting. For the title, use the market name."""


def _sources_block(sources: str) -> str:
    """Format user-provided sources into a prompt block."""
    if not sources or not sources.strip():
        return "No additional sources provided."
    return f"**User-provided sources and notes:**\n```\n{sources.strip()}\n```"


def format_segments_text(segments: list) -> str:
    """Format segment list into readable text for prompts."""
    lines = []
    for seg in segments:
        name = seg.name if hasattr(seg, "name") else seg.get("name", "")
        desc = seg.description if hasattr(seg, "description") else seg.get("description", "")
        lines.append(f"- **{name}**: {desc}")
    return "\n".join(lines)
