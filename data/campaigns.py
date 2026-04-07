"""Campaign mock data — 4 active/completed campaigns."""

from __future__ import annotations

from schema import Campaign


def get_campaigns() -> list[Campaign]:
    return [
        Campaign(
            name="Spring Wellness Push",
            brand="VitaGlow Supplements",
            start_date="2026-02-01",
            end_date="2026-04-30",
            budget=45000,
            spent=32400,
            influencer_count=12,
            status="Active",
            target_niche="Fitness",
            target_platforms=["Instagram", "TikTok"],
        ),
        Campaign(
            name="Tech Unboxed Q1",
            brand="NovaTech Devices",
            start_date="2026-01-15",
            end_date="2026-03-31",
            budget=60000,
            spent=48200,
            influencer_count=10,
            status="Active",
            target_niche="Tech",
            target_platforms=["YouTube", "Twitter"],
        ),
        Campaign(
            name="Summer Glow Collection",
            brand="Radiance Skincare",
            start_date="2025-11-01",
            end_date="2026-02-28",
            budget=35000,
            spent=35000,
            influencer_count=8,
            status="Completed",
            target_niche="Beauty",
            target_platforms=["Instagram", "TikTok"],
        ),
        Campaign(
            name="Foodie Collab Series",
            brand="FreshBite Delivery",
            start_date="2026-02-15",
            end_date="2026-05-15",
            budget=25000,
            spent=18600,
            influencer_count=6,
            status="Active",
            target_niche="Food",
            target_platforms=["Instagram", "YouTube"],
        ),
    ]
