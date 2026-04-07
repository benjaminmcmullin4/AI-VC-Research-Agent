"""Agent activity feed — ~60 events over the last 30 days."""

from __future__ import annotations

from schema import AgentEvent


def get_activity_feed() -> list[AgentEvent]:
    """Return agent events sorted newest-first."""
    events = [
        # ── April 2026 (recent) ──────────────────────────────────────────
        AgentEvent(timestamp="2026-04-06 09:12", event_type="insight", description="Weekly report: engagement rate trending up 12% across fitness niche creators", detail="Top performers: @mayafitlife (+18%), @marcusfitpro (+15%)", severity="info"),
        AgentEvent(timestamp="2026-04-06 08:30", event_type="discovery", description="Discovered 8 new creators in beauty niche matching audience profile", detail="Platforms: 4 Instagram, 3 TikTok, 1 YouTube", severity="info"),
        AgentEvent(timestamp="2026-04-05 16:45", event_type="alert", description="Budget utilization for Spring Wellness Push at 72% -- on track for planned spend", detail="$32,400 of $45,000 deployed", severity="info"),
        AgentEvent(timestamp="2026-04-05 14:20", event_type="conversion", description="2 conversions attributed to @ashwilliamsfashion content", detail="Estimated revenue: $1,840 from Instagram Stories campaign", severity="success"),
        AgentEvent(timestamp="2026-04-05 11:00", event_type="outreach", description="Sent personalized outreach to @rajwanders via Instagram DM", detail="Travel campaign partnership inquiry", severity="info"),
        AgentEvent(timestamp="2026-04-04 17:30", event_type="reply_detected", description="Positive reply from @hannahtravels -- interested in Balkans partnership", detail="Sentiment: enthusiastic, mentioned upcoming trip timing alignment", severity="success"),
        AgentEvent(timestamp="2026-04-04 15:00", event_type="negotiation", description="Updated deal terms for @lunaskinlab -- $8,500 for 4 posts + 8 Stories", detail="30-day exclusivity agreed, content approval included", severity="info"),
        AgentEvent(timestamp="2026-04-04 10:15", event_type="outreach", description="Sent follow-up to @meilinbeauty -- second attempt via email", detail="Initial outreach sent 2026-03-20, no response yet", severity="info"),
        AgentEvent(timestamp="2026-04-03 19:00", event_type="content_posted", description="Content posted by @diegoRGG -- 2 TikToks published", detail="Tracking links activated, monitoring engagement", severity="success"),
        AgentEvent(timestamp="2026-04-03 14:30", event_type="qualification", description="Flagged @mayafitlife as high-priority target", detail="Audience fit: 94, engagement: 5.2%, cost efficiency: excellent", severity="info"),
        AgentEvent(timestamp="2026-04-03 09:00", event_type="discovery", description="Discovered 15 new creators in gaming niche on TikTok", detail="Filtered to 4 qualified candidates based on engagement and audience fit", severity="info"),
        AgentEvent(timestamp="2026-04-02 16:00", event_type="conversion", description="5 conversions attributed to @destinyglowup content", detail="Estimated revenue: $4,200 from TikTok tutorial series", severity="success"),
        AgentEvent(timestamp="2026-04-02 11:30", event_type="negotiation", description="Counter-proposal received from @jesstranlife -- $12K for 4 TikToks + 1 YouTube", detail="Reduced TikTok count from 5 to 4 for quality focus", severity="info"),
        AgentEvent(timestamp="2026-04-02 08:45", event_type="outreach", description="Sent 5 personalized outreach messages across Instagram and TikTok", detail="Targets: fitness (2), beauty (1), lifestyle (1), food (1)", severity="info"),
        AgentEvent(timestamp="2026-04-01 20:00", event_type="reply_detected", description="Reply from @ariachengg -- interested but has exclusivity questions", detail="Flagged for manual review: potential Secretlab conflict", severity="warning"),
        AgentEvent(timestamp="2026-04-01 15:30", event_type="insight", description="Campaign ROI analysis: Summer Glow Collection returned 3.2x on spend", detail="Top performer: @destinyglowup (5.1x ROI)", severity="info"),
        AgentEvent(timestamp="2026-04-01 10:00", event_type="outreach", description="Sent personalized outreach to @jaketorresfit via Instagram", detail="Fitness campaign, bodyweight training angle", severity="info"),

        # ── Late March 2026 ──────────────────────────────────────────────
        AgentEvent(timestamp="2026-03-31 17:00", event_type="content_posted", description="Content posted by @amyeatsla -- restaurant review series live", detail="3 Instagram posts + 6 Stories published. Engagement tracking active.", severity="success"),
        AgentEvent(timestamp="2026-03-31 12:00", event_type="outreach", description="Sent outreach to @nathanstreetwear for sneaker collaboration", detail="Premium streetwear brand partnership", severity="info"),
        AgentEvent(timestamp="2026-03-30 18:00", event_type="reply_detected", description="Reply from @yukisatogames -- interested, asked about bilingual content", detail="Positive signal, needs bilingual brief", severity="info"),
        AgentEvent(timestamp="2026-03-30 14:00", event_type="qualification", description="Scored and ranked 12 new tech creators from discovery batch", detail="Top 3: @ninavtech (84), @saramitchtech (80), @ananyatechie (88)", severity="info"),
        AgentEvent(timestamp="2026-03-30 09:30", event_type="discovery", description="Discovered 22 new creators in tech niche across YouTube and Twitter", detail="Focus: AI/ML, developer tools, privacy tech", severity="info"),
        AgentEvent(timestamp="2026-03-29 16:00", event_type="negotiation", description="Contract finalized with @andrejexplores -- $7,200 for 3 YouTube videos", detail="Travel covered separately. Cape Town episode included.", severity="success"),
        AgentEvent(timestamp="2026-03-29 11:00", event_type="outreach", description="Sent outreach to @aabornefit for yoga wellness campaign", detail="VitaGlow Supplements plant-based recovery line", severity="info"),
        AgentEvent(timestamp="2026-03-28 15:30", event_type="conversion", description="3 conversions attributed to @lilygoesglobal content", detail="Estimated revenue: $3,900 from YouTube travel series", severity="success"),
        AgentEvent(timestamp="2026-03-28 10:00", event_type="alert", description="Tech Unboxed Q1 campaign at 80% budget utilization", detail="$48,200 of $60,000 spent. 2 weeks remaining.", severity="warning"),
        AgentEvent(timestamp="2026-03-27 17:00", event_type="outreach", description="Sent follow-up to @rachelglam -- mentioned Charlotte Tilbury partnership", detail="Second attempt, initial sent 2026-03-15", severity="info"),
        AgentEvent(timestamp="2026-03-27 13:00", event_type="insight", description="Beauty niche analysis: TikTok creators driving 2.4x more conversions than Instagram", detail="Recommendation: shift 15% of beauty budget to TikTok creators", severity="info"),
        AgentEvent(timestamp="2026-03-27 09:00", event_type="outreach", description="Sent follow-up to @meilinbeauty via email", detail="First follow-up, original outreach 2026-03-20", severity="info"),
        AgentEvent(timestamp="2026-03-26 16:00", event_type="reply_detected", description="Positive reply from @miathompsonliving -- interested in home collection", detail="Asked about product line details and compensation", severity="success"),

        # ── Mid March 2026 ───────────────────────────────────────────────
        AgentEvent(timestamp="2026-03-25 14:00", event_type="outreach", description="Sent 8 outreach messages across all platforms", detail="Batch outreach: 3 fitness, 2 beauty, 2 lifestyle, 1 travel", severity="info"),
        AgentEvent(timestamp="2026-03-25 09:00", event_type="discovery", description="Discovered 18 new creators in fashion niche", detail="Platforms: 8 Instagram, 6 TikTok, 4 YouTube", severity="info"),
        AgentEvent(timestamp="2026-03-24 17:30", event_type="reply_detected", description="Reply from @isabellamoreno -- interested but requesting sustainability docs", detail="Needs brand certifications before proceeding", severity="info"),
        AgentEvent(timestamp="2026-03-24 11:00", event_type="negotiation", description="Negotiation started with @sarahplaysit for indie game spotlight", detail="Proposed $3,000-$4,000 for 2 videos + livestream", severity="info"),
        AgentEvent(timestamp="2026-03-23 18:45", event_type="reply_detected", description="Positive reply from @tylerbreaks -- interested in NovaTech earbuds", detail="Asked about scope and timeline. High enthusiasm.", severity="success"),
        AgentEvent(timestamp="2026-03-23 10:00", event_type="content_posted", description="Content posted by @ashwilliamsfashion -- NYC fashion week BTS", detail="3 TikToks published, tracking engagement and clicks", severity="success"),
        AgentEvent(timestamp="2026-03-22 15:00", event_type="outreach", description="Sent outreach to @hannahtravels for travel platform partnership", detail="Budget Europe content angle", severity="info"),
        AgentEvent(timestamp="2026-03-22 09:30", event_type="qualification", description="Flagged @deshawntech as high-priority tech creator", detail="Audience fit: 93, brand fit: 87, strong affiliate conversion history", severity="info"),
        AgentEvent(timestamp="2026-03-21 16:00", event_type="insight", description="Outreach response rate this month: 58% -- up from 42% last month", detail="Personalization improvements driving higher engagement", severity="success"),
        AgentEvent(timestamp="2026-03-21 10:00", event_type="outreach", description="Sent 4 outreach messages to gaming creators", detail="Targets: @ariachengg, @sarahplaysit, @yukisatogames, @ryanplayz", severity="info"),
        AgentEvent(timestamp="2026-03-20 14:00", event_type="conversion", description="7 conversions attributed to @lilygoesglobal YouTube series", detail="Estimated revenue: $8,400. Best-performing travel content this quarter.", severity="success"),
        AgentEvent(timestamp="2026-03-20 09:00", event_type="outreach", description="Sent outreach to @meilinbeauty for Radiance Skincare campaign", detail="Vitamin C serum launch partnership", severity="info"),
        AgentEvent(timestamp="2026-03-19 15:00", event_type="negotiation", description="Counter-offer from @sarahplaysit -- wants Twitch for livestream", detail="$3,500 for 2 YouTube videos + 1 Twitch stream", severity="info"),

        # ── Early March 2026 ─────────────────────────────────────────────
        AgentEvent(timestamp="2026-03-18 17:00", event_type="outreach", description="Sent outreach to @ariachengg for gaming peripherals campaign", detail="Cozy gaming aesthetic angle", severity="info"),
        AgentEvent(timestamp="2026-03-18 10:00", event_type="discovery", description="Discovered 30 new creators across fitness and lifestyle niches", detail="Batch scan of Instagram, TikTok, and YouTube", severity="info"),
        AgentEvent(timestamp="2026-03-17 14:30", event_type="content_posted", description="Content posted by @destinyglowup -- beauty tutorial series", detail="4 TikToks published for Radiance Skincare campaign", severity="success"),
        AgentEvent(timestamp="2026-03-17 09:00", event_type="alert", description="Foodie Collab Series campaign launched -- tracking active", detail="6 influencers onboarded, content calendar distributed", severity="info"),
        AgentEvent(timestamp="2026-03-15 16:00", event_type="negotiation", description="Contract signed with @carlosfitmx -- $5,600 for bilingual campaign", detail="4 TikToks over 6 weeks, EN/ES content", severity="success"),
        AgentEvent(timestamp="2026-03-15 10:00", event_type="outreach", description="Sent outreach to @rachelglam for luxury beauty campaign", detail="Charlotte Tilbury collection launch", severity="info"),
        AgentEvent(timestamp="2026-03-14 14:00", event_type="negotiation", description="Contract signed with @marcoeats -- $14,000 for NYC food series", detail="6 TikToks + 2 Reels, 8-week campaign. Creator picks restaurants.", severity="success"),
        AgentEvent(timestamp="2026-03-14 09:00", event_type="discovery", description="Discovered 12 new creators in food niche on Instagram", detail="Filtered to 5 high-fit candidates for FreshBite campaign", severity="info"),
        AgentEvent(timestamp="2026-03-12 15:00", event_type="reply_detected", description="Declined: @jtechio not taking sponsored content currently", detail="Revisit in Q3. Values editorial independence.", severity="warning"),
        AgentEvent(timestamp="2026-03-12 10:00", event_type="qualification", description="Completed quarterly scoring refresh for 55 tracked influencers", detail="8 score increases, 3 decreases. 2 new high-priority flags.", severity="info"),
        AgentEvent(timestamp="2026-03-10 14:00", event_type="negotiation", description="Started negotiation with @lunaskinlab for K-beauty campaign", detail="Proposed $7,000-$9,000 for 4 posts + 8 Stories", severity="info"),
        AgentEvent(timestamp="2026-03-10 09:00", event_type="outreach", description="Sent outreach to @jtechio for developer-focused campaign", detail="NovaTech SaaS tools angle", severity="info"),
        AgentEvent(timestamp="2026-03-08 16:00", event_type="outreach", description="Sent outreach to @jesstranlife for Athletic Greens partnership", detail="Wellness + productivity content angle", severity="info"),
        AgentEvent(timestamp="2026-03-08 10:00", event_type="insight", description="Monthly discovery report: 142 new creators identified across all niches", detail="Conversion to qualified: 34%. Top niche: fitness (38 qualified).", severity="info"),

        # ── Late Feb / Early March ───────────────────────────────────────
        AgentEvent(timestamp="2026-03-05 12:00", event_type="content_posted", description="Content posted by @lilygoesglobal -- SE Asia travel series episode 1", detail="YouTube video published, 45K views in first 24 hours", severity="success"),
        AgentEvent(timestamp="2026-03-03 09:00", event_type="negotiation", description="Onboarding complete for @carlosfitmx -- content calendar sent", detail="First draft due April 10", severity="info"),
        AgentEvent(timestamp="2026-03-02 15:00", event_type="negotiation", description="Contract signed with @andrejexplores -- $7,200 for travel series", detail="3 YouTube videos + 10 Stories, Cape Town included", severity="success"),
    ]
    return sorted(events, key=lambda e: e.timestamp, reverse=True)
