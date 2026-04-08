"""Pydantic v2 models for the influencer marketing platform."""

from __future__ import annotations

from pydantic import BaseModel, Field


# ── Domain models (mock data structures) ─────────────────────────────────

class Influencer(BaseModel):
    name: str
    handle: str
    platform: str
    niche: str
    followers: int
    engagement_rate: float
    audience_fit_score: int = Field(ge=0, le=100)
    brand_fit_score: int = Field(ge=0, le=100)
    estimated_cost: int
    location: str
    status: str
    bio: str = ""
    past_partnerships: list[str] = Field(default_factory=list)
    avg_likes: int = 0
    avg_comments: int = 0
    recommendation_blurb: str = ""
    revenue_generated: float = 0.0
    # Simulation fields
    stage_entered_day: int = 0
    deal_value: float = 0.0
    content_posted_day: int | None = None
    discovered_day: int | None = None


class OutreachMessage(BaseModel):
    sender: str  # "agent" or "influencer"
    content: str
    timestamp: str
    message_type: str = "initial"  # initial, follow_up, reply, negotiation


class OutreachThread(BaseModel):
    influencer_handle: str
    influencer_name: str
    platform: str
    status: str
    messages: list[OutreachMessage] = Field(default_factory=list)
    current_stage: str = "Contacted"
    assigned_to: str = "AI Agent"
    next_action: str = ""
    deal_value: float | None = None


class Campaign(BaseModel):
    name: str
    brand: str
    start_date: str
    end_date: str
    budget: int
    spent: int
    influencer_count: int
    status: str  # "Active", "Completed", "Paused"
    target_niche: str
    target_platforms: list[str] = Field(default_factory=list)


class AgentEvent(BaseModel):
    timestamp: str
    event_type: str  # discovery, qualification, outreach, reply_detected, negotiation, content_posted, conversion, insight, alert
    description: str
    detail: str = ""
    severity: str = "info"  # info, success, warning


# ── Claude response models (instructor structured outputs) ───────────────

class RecommendationBlurb(BaseModel):
    """AI-generated recommendation for an influencer."""
    influencer_handle: str = Field(description="The influencer's social handle")
    reasoning: str = Field(description="2-3 sentence explanation of why this influencer is recommended")
    confidence_score: float = Field(description="Confidence from 0.0 to 1.0")
    key_factors: list[str] = Field(description="Top 3-4 factors driving the recommendation")


class DashboardInsight(BaseModel):
    """AI-generated executive summary insight."""
    summary: str = Field(description="2-3 sentence executive summary of campaign performance")
    key_metrics_commentary: str = Field(description="Brief commentary on standout metrics")
    top_recommendation: str = Field(description="One actionable next step")


class OutreachDraft(BaseModel):
    """AI-generated outreach message draft."""
    subject: str = Field(description="Short subject line for the outreach")
    body: str = Field(description="Personalized outreach message body, 3-5 sentences")
    tone: str = Field(description="Tone descriptor, e.g. 'professional-friendly'")
    personalization_notes: str = Field(description="What was personalized and why")
