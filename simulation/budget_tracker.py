"""Budget and revenue tracking for the simulation."""

from __future__ import annotations

import math
import random as _random


def calculate_deal_value(influencer: dict, rng: _random.Random) -> float:
    """Calculate negotiated deal value based on influencer's estimated cost.

    Adds 0.8x-1.2x variance to simulate negotiation outcomes.
    """
    base = influencer["estimated_cost"]
    return round(base * rng.uniform(0.8, 1.2), 2)


def calculate_daily_revenue(deal_cost: float, days_since_posted: int,
                            roi_multiplier: float) -> float:
    """Calculate daily revenue from a posted influencer.

    Revenue follows an exponential decay curve:
    - Most revenue in first 7 days
    - Tapers off over 30 days
    - Total expected revenue = deal_cost * roi_multiplier

    Args:
        deal_cost: The negotiated deal value.
        days_since_posted: Days since content was posted.
        roi_multiplier: Expected total ROI multiplier (3.0-8.0x).

    Returns:
        Revenue generated on this specific day.
    """
    if days_since_posted < 0 or days_since_posted > 45:
        return 0.0

    total_expected = deal_cost * roi_multiplier
    # Exponential decay: daily_share = (1/Z) * exp(-0.12 * day)
    # Normalize so sum over 45 days ≈ 1.0
    decay_rate = 0.12
    normalization = sum(math.exp(-decay_rate * d) for d in range(46))
    daily_share = math.exp(-decay_rate * days_since_posted) / normalization
    return round(total_expected * daily_share, 2)


def assign_roi_multiplier(influencer: dict, rng: _random.Random) -> float:
    """Assign an ROI multiplier to a converted influencer.

    Higher fit scores and engagement rates correlate with higher ROI.
    Range: 2.0x to 10.0x, centered around 4.5x.
    """
    # Base multiplier from fit scores
    avg_fit = (influencer["audience_fit_score"] + influencer["brand_fit_score"]) / 2
    fit_factor = avg_fit / 100  # 0.2 to 0.98

    # Engagement bonus
    eng_factor = min(influencer["engagement_rate"] / 5.0, 1.5)

    base = 2.0 + fit_factor * 4.0 + eng_factor * 2.0
    # Add randomness
    multiplier = base * rng.uniform(0.7, 1.3)
    return round(max(2.0, min(10.0, multiplier)), 2)


def budget_summary(state: dict) -> dict:
    """Compute budget summary from simulation state."""
    return {
        "total": state["budget_total"],
        "spent": state["budget_spent"],
        "committed": state["budget_committed"],
        "remaining": state["budget_total"] - state["budget_spent"] - state["budget_committed"],
    }
