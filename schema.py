"""Pydantic models for all 6 pipeline steps."""

from __future__ import annotations

from pydantic import BaseModel, Field


# ── Step 1: Market Spec ────────────────────────────────────────────────

class MarketSpec(BaseModel):
    """Core market definition produced by Step 1."""

    market_name: str = Field(description="Short canonical name for this market")
    definition: str = Field(description="2–3 sentence market definition")
    ideal_customer_profile: str = Field(description="Who buys this and why")
    value_chain: list[str] = Field(
        description="Ordered list of value-chain stages (e.g. Data Ingestion → Processing → Output)"
    )
    key_workflows: list[str] = Field(
        description="Core workflows this market automates or enables"
    )
    pricing_models: list[str] = Field(
        description="Common pricing approaches (SaaS, usage-based, per-seat, etc.)"
    )
    regulatory_context: str = Field(
        description="Relevant regulatory or compliance considerations"
    )
    assumptions: list[str] = Field(
        description="Explicit assumptions made in this analysis"
    )


# ── Step 2: Taxonomy ──────────────────────────────────────────────────

class Segment(BaseModel):
    """One segment within the taxonomy."""

    name: str
    description: str
    example_companies: list[str] = Field(default_factory=list)
    wedge_strategy: str = Field(
        default="",
        description="How a startup might enter via this segment",
    )


class Taxonomy(BaseModel):
    """Market taxonomy with segments and adjacencies."""

    segments: list[Segment] = Field(min_length=2)
    adjacent_categories: list[str] = Field(
        description="Related markets or categories worth monitoring"
    )


# ── Step 3: Company Landscape ─────────────────────────────────────────

class Company(BaseModel):
    """A single company in the landscape."""

    name: str
    one_liner: str = Field(description="What they do in ≤15 words")
    segment: str = Field(description="Which taxonomy segment they belong to")
    stage: str = Field(description="Funding stage: Seed, Series A, Series B, Growth, Public")
    differentiation: str = Field(description="Key differentiator vs. peers")
    source_label: str = Field(
        description="'from sources' if mentioned in user-provided sources, else 'model suggested'"
    )
    estimated_arr_range: str = Field(
        default="Unknown",
        description="Estimated ARR range if available (e.g. '$5M–$15M')",
    )
    hq_location: str = Field(default="Unknown", description="Headquarters location")


class CompanyBucket(BaseModel):
    """A group of companies in one segment."""

    segment_name: str
    companies: list[Company]


class CompanyLandscape(BaseModel):
    """Full company landscape across all segments."""

    buckets: list[CompanyBucket]
    total_companies: int = Field(description="Total number of companies mapped")
    coverage_notes: str = Field(
        default="",
        description="Notes on coverage gaps or uncertainty",
    )


# ── Step 4: TAM / SAM Sizing ─────────────────────────────────────────

class MarketSizing(BaseModel):
    """TAM/SAM heuristics with ranges and assumptions."""

    tam_low_b: float = Field(description="TAM low estimate in $B")
    tam_high_b: float = Field(description="TAM high estimate in $B")
    sam_low_b: float = Field(description="SAM low estimate in $B")
    sam_high_b: float = Field(description="SAM high estimate in $B")
    methodology: str = Field(description="Top-down, bottom-up, or triangulated")
    assumptions: list[str] = Field(description="Key sizing assumptions")
    growth_rate_pct: float = Field(description="Expected CAGR %")
    confidence: str = Field(
        description="Low / Medium / High — how confident is this sizing"
    )
    sensitivity_factors: list[str] = Field(
        description="Factors that could materially change the sizing"
    )


# ── Step 5: Investment Thesis ─────────────────────────────────────────

class Risk(BaseModel):
    """A single risk item with severity rating."""

    risk: str
    description: str
    severity: int = Field(ge=1, le=5, description="1 = low, 5 = critical")
    mitigant: str = Field(description="How an investor/company might mitigate this")


class InvestmentThesis(BaseModel):
    """Full investment thesis and risk assessment."""

    why_now: list[str] = Field(description="Why is this market timely?")
    thesis_statement: str = Field(
        description="1–2 sentence investment thesis"
    )
    entry_points: list[str] = Field(
        description="Attractive entry strategies for a PE/growth investor"
    )
    winner_characteristics: list[str] = Field(
        description="What the eventual category winner looks like"
    )
    risks: list[Risk] = Field(min_length=1)
    key_unknowns: list[str] = Field(
        description="Important questions that need further diligence"
    )
    diligence_plan: list[str] = Field(
        description="Recommended diligence steps"
    )
    sourcing_angles: list[str] = Field(
        description="How a deal team might source opportunities in this space"
    )
    value_creation_angles: list[str] = Field(
        default_factory=list,
        description="Post-acquisition value creation levers",
    )


# ── Step 6: Market Memo ───────────────────────────────────────────────

class MarketMemo(BaseModel):
    """Assembled PE-style market memo in markdown sections."""

    title: str
    date: str
    executive_summary: str
    market_overview: str
    tam_sam_sizing: str
    competitive_landscape: str
    taxonomy_segmentation: str
    company_profiles: str
    investment_thesis: str
    value_creation_angles: str
    risks_and_mitigants: str
    diligence_plan: str
    sources_and_methodology: str


# ── Full Research Output (wraps all steps) ─────────────────────────────

class ResearchOutput(BaseModel):
    """Complete output of a research run — all 6 steps."""

    query: str
    geography: str
    stage_focus: str
    market_spec: MarketSpec
    taxonomy: Taxonomy
    landscape: CompanyLandscape
    sizing: MarketSizing
    thesis: InvestmentThesis
    memo: MarketMemo
