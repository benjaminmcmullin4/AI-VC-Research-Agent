"""Claude API wrapper — preserves the instructor + anthropic pattern from the original codebase."""

from __future__ import annotations

import json
import os
from typing import Any

import anthropic
import instructor
import streamlit as st

from config import DEFAULT_MODEL, MAX_RETRIES
from prompts import (
    DASHBOARD_INSIGHT_SYSTEM,
    DASHBOARD_INSIGHT_USER,
    OUTREACH_DRAFT_SYSTEM,
    OUTREACH_DRAFT_USER,
    RECOMMENDATION_SYSTEM,
    RECOMMENDATION_USER,
)
from schema import DashboardInsight, OutreachDraft, RecommendationBlurb


# ── Client setup (same pattern as original pipeline.py) ──────────────────

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


def get_api_key() -> str | None:
    """Resolve API key from environment or Streamlit secrets."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except (KeyError, FileNotFoundError):
        return None


# ── High-level generation helpers ────────────────────────────────────────

def generate_recommendation(api_key: str, influencer_data: dict) -> RecommendationBlurb | None:
    """Generate an AI recommendation blurb for an influencer."""
    try:
        client = _get_client(api_key)
        user_prompt = RECOMMENDATION_USER.format(
            influencer_json=json.dumps(influencer_data, indent=2),
        )
        return _call_llm(client, RecommendationBlurb, RECOMMENDATION_SYSTEM, user_prompt, temperature=0.6)
    except Exception:
        return None


def generate_dashboard_insight(api_key: str, metrics: dict) -> DashboardInsight | None:
    """Generate an AI executive insight for the dashboard."""
    try:
        client = _get_client(api_key)
        user_prompt = DASHBOARD_INSIGHT_USER.format(
            metrics_json=json.dumps(metrics, indent=2),
        )
        return _call_llm(client, DashboardInsight, DASHBOARD_INSIGHT_SYSTEM, user_prompt, temperature=0.4)
    except Exception:
        return None


def generate_outreach_draft(api_key: str, influencer_data: dict, brand_context: str = "") -> OutreachDraft | None:
    """Generate an AI-drafted outreach message."""
    try:
        client = _get_client(api_key)
        user_prompt = OUTREACH_DRAFT_USER.format(
            influencer_json=json.dumps(influencer_data, indent=2),
            brand_context=brand_context or "Premium DTC brand seeking authentic creator partnerships for product awareness and conversion.",
        )
        return _call_llm(client, OutreachDraft, OUTREACH_DRAFT_SYSTEM, user_prompt, temperature=0.7)
    except Exception:
        return None
