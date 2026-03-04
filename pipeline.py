"""LLM orchestration — 6-step research pipeline using instructor + Claude."""

from __future__ import annotations

import json
import time
from datetime import date
from typing import Any, Callable

import anthropic
import instructor

from config import DEFAULT_MODEL, MAX_RETRIES, PIPELINE_STEPS
from prompts import (
    SYSTEM_PROMPT,
    MARKET_SPEC_PROMPT,
    TAXONOMY_PROMPT,
    LANDSCAPE_PROMPT,
    SIZING_PROMPT,
    THESIS_PROMPT,
    MEMO_PROMPT,
    _sources_block,
    format_segments_text,
)
from schema import (
    MarketSpec,
    Taxonomy,
    CompanyLandscape,
    MarketSizing,
    InvestmentThesis,
    MarketMemo,
    ResearchOutput,
)


def _get_client(api_key: str):
    """Create an instructor-patched Anthropic client."""
    return instructor.from_anthropic(
        anthropic.Anthropic(api_key=api_key),
    )


def _call_llm(
    client,
    response_model,
    system: str,
    user: str,
    temperature: float = 0.5,
    max_tokens: int = 4096,
):
    """Make a single structured LLM call with instructor."""
    return client.chat.completions.create(
        model=DEFAULT_MODEL,
        max_tokens=max_tokens,
        temperature=temperature,
        max_retries=MAX_RETRIES,
        messages=[
            {"role": "user", "content": user},
        ],
        system=system,
        response_model=response_model,
    )


# ── Individual pipeline steps ──────────────────────────────────────────

def step_market_spec(
    client, query: str, geography: str, stage_focus: str,
    sources: str, detail_level: str, temperature: float,
) -> MarketSpec:
    system = SYSTEM_PROMPT.format(detail_level=detail_level)
    user = MARKET_SPEC_PROMPT.format(
        query=query,
        geography=geography,
        stage_focus=stage_focus,
        sources_block=_sources_block(sources),
    )
    return _call_llm(client, MarketSpec, system, user, temperature)


def step_taxonomy(
    client, spec: MarketSpec, detail_level: str, temperature: float,
) -> Taxonomy:
    system = SYSTEM_PROMPT.format(detail_level=detail_level)
    user = TAXONOMY_PROMPT.format(
        market_name=spec.market_name,
        definition=spec.definition,
        value_chain=" → ".join(spec.value_chain),
    )
    return _call_llm(client, Taxonomy, system, user, temperature)


def step_landscape(
    client, spec: MarketSpec, taxonomy: Taxonomy,
    company_count: int, sources: str,
    detail_level: str, temperature: float,
) -> CompanyLandscape:
    system = SYSTEM_PROMPT.format(detail_level=detail_level)
    user = LANDSCAPE_PROMPT.format(
        market_name=spec.market_name,
        definition=spec.definition,
        segments_text=format_segments_text(taxonomy.segments),
        company_count=company_count,
        sources_block=_sources_block(sources),
    )
    return _call_llm(client, CompanyLandscape, system, user, temperature, max_tokens=8192)


def step_sizing(
    client, spec: MarketSpec, taxonomy: Taxonomy,
    geography: str, detail_level: str, temperature: float,
) -> MarketSizing:
    system = SYSTEM_PROMPT.format(detail_level=detail_level)
    user = SIZING_PROMPT.format(
        market_name=spec.market_name,
        definition=spec.definition,
        geography=geography,
        segments_text=format_segments_text(taxonomy.segments),
    )
    return _call_llm(client, MarketSizing, system, user, temperature)


def step_thesis(
    client, spec: MarketSpec, taxonomy: Taxonomy,
    landscape: CompanyLandscape, sizing: MarketSizing,
    detail_level: str, temperature: float,
) -> InvestmentThesis:
    # Collect top company names for prompt
    top_companies = []
    for bucket in landscape.buckets:
        for co in bucket.companies[:3]:
            top_companies.append(f"{co.name} ({co.segment})")
    system = SYSTEM_PROMPT.format(detail_level=detail_level)
    user = THESIS_PROMPT.format(
        market_name=spec.market_name,
        definition=spec.definition,
        tam_low_b=sizing.tam_low_b,
        tam_high_b=sizing.tam_high_b,
        sam_low_b=sizing.sam_low_b,
        sam_high_b=sizing.sam_high_b,
        segments_text=format_segments_text(taxonomy.segments),
        top_companies=", ".join(top_companies[:10]),
    )
    return _call_llm(client, InvestmentThesis, system, user, temperature)


def step_memo(
    client, spec: MarketSpec, taxonomy: Taxonomy,
    landscape: CompanyLandscape, sizing: MarketSizing,
    thesis: InvestmentThesis,
    detail_level: str, temperature: float,
) -> MarketMemo:
    system = SYSTEM_PROMPT.format(detail_level=detail_level)
    user = MEMO_PROMPT.format(
        market_name=spec.market_name,
        date=date.today().isoformat(),
        market_spec_json=spec.model_dump_json(),
        taxonomy_json=taxonomy.model_dump_json(),
        landscape_json=landscape.model_dump_json(),
        sizing_json=sizing.model_dump_json(),
        thesis_json=thesis.model_dump_json(),
    )
    return _call_llm(client, MarketMemo, system, user, temperature, max_tokens=8192)


# ── Full pipeline runner ───────────────────────────────────────────────

def run_pipeline(
    api_key: str,
    query: str,
    geography: str = "Global",
    stage_focus: str = "All Stages",
    sources: str = "",
    detail_level: str = "standard",
    company_count: int = 15,
    temperature: float = 0.5,
    on_step: Callable[[int, str, float], None] | None = None,
) -> ResearchOutput:
    """Run the full 6-step research pipeline.

    Args:
        on_step: callback(step_index, step_name, elapsed_seconds) called after each step completes.
    """
    client = _get_client(api_key)
    results: dict[str, Any] = {}

    def _notify(idx: int, elapsed: float):
        step_key, step_label = PIPELINE_STEPS[idx]
        if on_step:
            on_step(idx, step_label, elapsed)

    # Step 1
    t0 = time.time()
    results["market_spec"] = step_market_spec(
        client, query, geography, stage_focus, sources, detail_level, temperature,
    )
    _notify(0, time.time() - t0)

    # Step 2
    t0 = time.time()
    results["taxonomy"] = step_taxonomy(
        client, results["market_spec"], detail_level, temperature,
    )
    _notify(1, time.time() - t0)

    # Step 3
    t0 = time.time()
    results["landscape"] = step_landscape(
        client, results["market_spec"], results["taxonomy"],
        company_count, sources, detail_level, temperature,
    )
    _notify(2, time.time() - t0)

    # Step 4
    t0 = time.time()
    results["sizing"] = step_sizing(
        client, results["market_spec"], results["taxonomy"],
        geography, detail_level, temperature,
    )
    _notify(3, time.time() - t0)

    # Step 5
    t0 = time.time()
    results["thesis"] = step_thesis(
        client, results["market_spec"], results["taxonomy"],
        results["landscape"], results["sizing"],
        detail_level, temperature,
    )
    _notify(4, time.time() - t0)

    # Step 6
    t0 = time.time()
    results["memo"] = step_memo(
        client, results["market_spec"], results["taxonomy"],
        results["landscape"], results["sizing"], results["thesis"],
        detail_level, temperature,
    )
    _notify(5, time.time() - t0)

    return ResearchOutput(
        query=query,
        geography=geography,
        stage_focus=stage_focus,
        **results,
    )
