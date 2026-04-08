"""Core simulation engine — discrete day-step state machine."""

from __future__ import annotations

import random as _random
from datetime import datetime, timedelta

from config import (
    DISCOVERY_RATE,
    POOL_SIZE,
    TRANSITION_DELAYS,
    TRANSITION_PROBABILITIES,
)
from schema import AgentEvent, Influencer, OutreachMessage, OutreachThread
from simulation.budget_tracker import (
    assign_roi_multiplier,
    budget_summary,
    calculate_daily_revenue,
    calculate_deal_value,
)
from simulation.conversation_generator import (
    generate_decline_message,
    generate_negotiation_exchange,
    generate_outreach,
    generate_reply,
    generate_signed_message,
)
from simulation.influencer_generator import generate_pool


# ── Initialization ───────────────────────────────────────────────────────

def initialize_simulation(
    campaign_name: str,
    target_count: int,
    niches: list[str],
    platforms: list[str],
    budget: int,
    seed: int = 42,
) -> dict:
    """Create initial simulation state."""
    pool = generate_pool(n=POOL_SIZE, seed=seed)

    return {
        "active": True,
        "day": 0,
        "start_date": datetime.now().strftime("%Y-%m-%d"),
        "campaign_name": campaign_name,
        "target_count": target_count,
        "niches": niches,
        "platforms": platforms,
        "budget_total": budget,
        "budget_spent": 0.0,
        "budget_committed": 0.0,
        "seed": seed,
        "pool": pool,
        "pipeline": {},
        "conversations": {},
        "activity_feed": [],
        "revenue_by_influencer": {},
        "revenue_by_day": [],
        "total_revenue": 0.0,
        "declined_handles": set(),
        "ghost_handles": set(),
    }


# ── Day advance ──────────────────────────────────────────────────────────

def advance_day(state: dict) -> dict:
    """Process one simulated day. Phases run upstream-first so new entries
    can flow through the pipeline within the same day where appropriate.
    """
    state["day"] += 1
    day = state["day"]
    rng = _random.Random(state["seed"] * 10000 + day)
    start_date = state["start_date"]
    campaign = state["campaign_name"]
    today_events: list[dict] = []
    daily_revenue = 0.0

    # ── Phase 1: Discovery (Pool -> Discovered) ─────────────────────
    budget_info = budget_summary(state)
    signed_count = sum(
        1 for info in state["pipeline"].values()
        if info["stage"] in ("Signed", "Content Posted", "Converted")
    )
    target = state["target_count"]
    total_pipeline = len(state["pipeline"])

    should_discover = (
        signed_count < target
        and total_pipeline < target * 6
        and budget_info["remaining"] > 0
        and day <= 60
    )

    if should_discover:
        base_min, base_max = DISCOVERY_RATE
        scale = max(0.3, min(1.0, target / 15))
        n_discover = rng.randint(max(2, int(base_min * scale)), max(3, int(base_max * scale)))
        candidates = []
        niches = state["niches"]
        platforms = state["platforms"]
        for inf in state["pool"]:
            h = inf["handle"]
            if inf["status"] != "Pool":
                continue
            if h in state["pipeline"]:
                continue
            if niches and inf["niche"] not in niches:
                continue
            if platforms and inf["platform"] not in platforms:
                continue
            candidates.append(inf)

        candidates.sort(
            key=lambda i: (
                0.6 * i["audience_fit_score"] + 0.4 * i["brand_fit_score"]
                + rng.uniform(-10, 10)
            ),
            reverse=True,
        )

        discovered_today = candidates[:n_discover]
        if discovered_today:
            for inf in discovered_today:
                handle = inf["handle"]
                inf["status"] = "Discovered"
                inf["discovered_day"] = day
                inf["stage_entered_day"] = day
                state["pipeline"][handle] = {
                    "stage": "Discovered",
                    "entered_day": day,
                    "deal_value": 0.0,
                    "roi_multiplier": 0.0,
                }
            today_events.append(_event(
                day, start_date, "discovery",
                f"Discovered {len(discovered_today)} new creators matching campaign criteria",
                f"Niches: {', '.join(niches) if niches else 'All'} | "
                f"Platforms: {', '.join(platforms) if platforms else 'All'}",
                "info",
            ))

    # ── Phase 2: Qualification (Discovered -> Qualified/Rejected) ───
    for handle, info in list(state["pipeline"].items()):
        if info["stage"] == "Discovered":
            delay = _deterministic_delay(handle, "Discovered", *TRANSITION_DELAYS["Discovered"])
            if day - info["entered_day"] == delay:
                if rng.random() < TRANSITION_PROBABILITIES["Discovered->Qualified"]:
                    info["stage"] = "Qualified"
                    info["entered_day"] = day
                    inf = _get_influencer(state, handle)
                    if inf:
                        inf["status"] = "Qualified"
                    today_events.append(_event(
                        day, start_date, "qualification",
                        f"Qualified {handle} — strong audience fit",
                        f"Fit score: {(inf or {}).get('audience_fit_score', 0)}",
                        "info",
                    ))
                else:
                    info["stage"] = "Rejected"
                    inf = _get_influencer(state, handle)
                    if inf:
                        inf["status"] = "Rejected"

    # ── Phase 3: Outreach (Qualified -> Contacted) ──────────────────
    # Use >= for this automatic (100% probability) transition so same-day
    # qualifications can immediately proceed to outreach.
    active_deal_count = sum(
        1 for info in state["pipeline"].values()
        if info["stage"] in ("Negotiating", "Signed", "Content Posted", "Converted")
    )
    for handle, info in list(state["pipeline"].items()):
        if info["stage"] == "Qualified":
            if active_deal_count >= state["target_count"] * 1.5:
                continue
            delay = _deterministic_delay(handle, "Qualified", *TRANSITION_DELAYS["Qualified"])
            if day - info["entered_day"] >= delay:
                budget_info = budget_summary(state)
                if budget_info["remaining"] <= 0:
                    continue
                info["stage"] = "Contacted"
                info["entered_day"] = day
                inf = _get_influencer(state, handle)
                if inf:
                    inf["status"] = "Contacted"
                outreach_msg = generate_outreach(
                    inf or {}, campaign, day, start_date, rng
                )
                state["conversations"][handle] = {
                    "influencer_handle": handle,
                    "influencer_name": (inf or {}).get("name", handle),
                    "platform": (inf or {}).get("platform", "Instagram"),
                    "status": "Awaiting Reply",
                    "messages": [outreach_msg],
                    "current_stage": "Contacted",
                    "assigned_to": "AI Agent",
                    "next_action": "Waiting for reply",
                    "deal_value": None,
                }
                active_deal_count_contacted = sum(
                    1 for i2 in state["pipeline"].values()
                    if i2["stage"] in ("Contacted", "Replied", "Negotiating", "Signed", "Content Posted", "Converted")
                )
                today_events.append(_event(
                    day, start_date, "outreach",
                    f"Outreach sent to {handle}",
                    f"Platform: {(inf or {}).get('platform', 'Unknown')}",
                    "info",
                ))

    # ── Phase 4: Response (Contacted -> Replied / Ghost) ────────────
    for handle, info in list(state["pipeline"].items()):
        if info["stage"] == "Contacted":
            delay_min, delay_max = TRANSITION_DELAYS["Contacted"]
            days_waiting = day - info["entered_day"]
            delay = _deterministic_delay(handle, "Contacted", delay_min, delay_max)
            if days_waiting == delay:
                if rng.random() < TRANSITION_PROBABILITIES["Contacted->Replied"]:
                    reply_type = rng.choices(
                        ["interested", "questions"], weights=[60, 40],
                    )[0]
                    info["stage"] = "Replied"
                    info["entered_day"] = day
                    inf = _get_influencer(state, handle)
                    if inf:
                        inf["status"] = "Replied"
                    msg = generate_reply(inf or {}, reply_type, day, start_date, rng)
                    conv = state["conversations"].get(handle)
                    if conv and msg:
                        conv["messages"].append(msg)
                        conv["status"] = "Interested" if reply_type == "interested" else "Questions"
                        conv["current_stage"] = "Replied"
                    today_events.append(_event(
                        day, start_date, "reply_detected",
                        f"Positive reply from {handle}",
                        f"Reply type: {reply_type}",
                        "success",
                    ))
                else:
                    # No reply on their check day — ghost
                    info["stage"] = "Ghost"
                    state["ghost_handles"].add(handle)
                    inf = _get_influencer(state, handle)
                    if inf:
                        inf["status"] = "Ghost"

    # ── Phase 5: Reply -> Negotiating / Declined ────────────────────
    for handle, info in list(state["pipeline"].items()):
        if info["stage"] == "Replied":
            delay = _deterministic_delay(handle, "Replied", *TRANSITION_DELAYS["Replied"])
            if day - info["entered_day"] == delay:
                budget_remaining = state["budget_total"] - state["budget_spent"] - state["budget_committed"]
                inf = _get_influencer(state, handle)
                est_deal = (inf or {}).get("estimated_cost", 2000)
                if budget_remaining > est_deal and rng.random() < TRANSITION_PROBABILITIES["Replied->Negotiating"]:
                    info["stage"] = "Negotiating"
                    info["entered_day"] = day
                    if inf:
                        inf["status"] = "Negotiating"
                    deal = calculate_deal_value(inf or {}, rng)
                    info["deal_value"] = deal
                    info["roi_multiplier"] = assign_roi_multiplier(inf or {}, rng)
                    state["budget_committed"] += deal
                    if inf:
                        inf["deal_value"] = deal
                    conv = state["conversations"].get(handle)
                    if conv:
                        msgs = generate_negotiation_exchange(
                            inf or {}, deal, day, start_date, rng
                        )
                        conv["messages"].extend(msgs)
                        conv["status"] = "Negotiating"
                        conv["current_stage"] = "Negotiating"
                        conv["deal_value"] = deal
                    today_events.append(_event(
                        day, start_date, "negotiation",
                        f"Negotiation started with {handle}",
                        f"Proposed deal: ${deal:,.0f}",
                        "info",
                    ))
                else:
                    info["stage"] = "Declined"
                    state["declined_handles"].add(handle)
                    if inf:
                        inf["status"] = "Declined"
                    conv = state["conversations"].get(handle)
                    if conv:
                        msg = generate_decline_message(
                            inf or {}, day, start_date, rng
                        )
                        conv["messages"].append(msg)
                        conv["status"] = "Declined"
                        conv["current_stage"] = "Declined"

    # ── Phase 6: Negotiation -> Signed / Declined ───────────────────
    for handle, info in list(state["pipeline"].items()):
        if info["stage"] == "Negotiating":
            delay = _deterministic_delay(handle, "Negotiating", *TRANSITION_DELAYS["Negotiating"])
            if day - info["entered_day"] == delay:
                deal = info["deal_value"]
                budget_remaining = state["budget_total"] - state["budget_spent"]
                can_afford = budget_remaining >= deal
                if can_afford and rng.random() < TRANSITION_PROBABILITIES["Negotiating->Signed"]:
                    info["stage"] = "Signed"
                    info["entered_day"] = day
                    state["budget_spent"] += deal
                    state["budget_committed"] = max(0, state["budget_committed"] - deal)
                    inf = _get_influencer(state, handle)
                    if inf:
                        inf["status"] = "Signed"
                    conv = state["conversations"].get(handle)
                    if conv:
                        msg = generate_signed_message(day, start_date, rng)
                        conv["messages"].append(msg)
                        conv["status"] = "Signed"
                        conv["current_stage"] = "Signed"
                    today_events.append(_event(
                        day, start_date, "negotiation",
                        f"Deal signed with {handle} for ${deal:,.0f}",
                        "Contract finalized. Content production begins.",
                        "success",
                    ))
                else:
                    info["stage"] = "Declined"
                    state["budget_committed"] = max(0, state["budget_committed"] - info["deal_value"])
                    state["declined_handles"].add(handle)
                    inf = _get_influencer(state, handle)
                    if inf:
                        inf["status"] = "Declined"
                    conv = state["conversations"].get(handle)
                    if conv:
                        msg = generate_decline_message(
                            inf or {}, day, start_date, rng
                        )
                        conv["messages"].append(msg)
                        conv["status"] = "Declined"
                        conv["current_stage"] = "Declined"
                    today_events.append(_event(
                        day, start_date, "negotiation",
                        f"{handle} declined the partnership",
                        "Moving on to other candidates.",
                        "warning",
                    ))

    # ── Phase 7: Signed -> Content Posted ───────────────────────────
    for handle, info in list(state["pipeline"].items()):
        if info["stage"] == "Signed":
            delay = _deterministic_delay(handle, "Signed", *TRANSITION_DELAYS["Signed"])
            if day - info["entered_day"] == delay:
                if rng.random() < TRANSITION_PROBABILITIES["Signed->Content Posted"]:
                    info["stage"] = "Content Posted"
                    info["entered_day"] = day
                    inf = _get_influencer(state, handle)
                    if inf:
                        inf["status"] = "Content Posted"
                        inf["content_posted_day"] = day
                    today_events.append(_event(
                        day, start_date, "content_posted",
                        f"{handle} posted sponsored content",
                        "Content is now live and being tracked for conversions.",
                        "success",
                    ))

    # ── Phase 8: Revenue + Content Posted -> Converted ──────────────
    for handle, info in list(state["pipeline"].items()):
        if info["stage"] in ("Content Posted", "Converted"):
            inf = _get_influencer(state, handle)
            if inf and inf.get("content_posted_day") is not None:
                days_since = day - inf["content_posted_day"]
                roi_mult = info.get("roi_multiplier", 5.0)
                rev = calculate_daily_revenue(info["deal_value"], days_since, roi_mult)
                if rev > 0:
                    state["revenue_by_influencer"].setdefault(handle, 0.0)
                    state["revenue_by_influencer"][handle] += rev
                    daily_revenue += rev
                    inf["revenue_generated"] = state["revenue_by_influencer"][handle]

                if info["stage"] == "Content Posted":
                    conv_delay = _deterministic_delay(handle, "ContentPosted", 7, 21)
                    if days_since == conv_delay:
                        if rng.random() < TRANSITION_PROBABILITIES["Content Posted->Converted"]:
                            info["stage"] = "Converted"
                            inf["status"] = "Converted"
                            today_events.append(_event(
                                day, start_date, "conversion",
                                f"Conversion attributed to {handle}",
                                f"Revenue: ${state['revenue_by_influencer'].get(handle, 0):,.0f}",
                                "success",
                            ))

    state["total_revenue"] += daily_revenue
    state["revenue_by_day"].append((day, round(daily_revenue, 2)))

    # ── Daily summary insight (every 3 days) ────────────────────────
    if day % 3 == 0 and today_events:
        total_signed = sum(
            1 for info in state["pipeline"].values()
            if info["stage"] in ("Signed", "Content Posted", "Converted")
        )
        budget_info = budget_summary(state)
        today_events.append(_event(
            day, start_date, "insight",
            f"Day {day} summary: {total_signed} influencers signed, "
            f"${state['total_revenue']:,.0f} total revenue, "
            f"${budget_info['remaining']:,.0f} budget remaining",
            "",
            "info",
        ))

    state["activity_feed"] = today_events + state["activity_feed"]
    return state


def advance_days(state: dict, n: int) -> dict:
    """Advance the simulation by n days."""
    for _ in range(n):
        state = advance_day(state)
    return state


# ── Data export ──────────────────────────────────────────────────────────

def get_simulation_data(state: dict) -> dict:
    """Convert simulation state into the standard data dict format."""
    influencers = []
    for inf in state["pool"]:
        if inf["status"] not in ("Pool", "Rejected", "Ghost"):
            influencers.append(Influencer(**{
                k: v for k, v in inf.items() if k != "_pool_index"
            }))

    conversations = []
    for handle, conv in state["conversations"].items():
        messages = [OutreachMessage(**m) for m in conv["messages"]]
        conversations.append(OutreachThread(
            influencer_handle=conv["influencer_handle"],
            influencer_name=conv["influencer_name"],
            platform=conv["platform"],
            status=conv["status"],
            messages=messages,
            current_stage=conv["current_stage"],
            assigned_to=conv.get("assigned_to", "AI Agent"),
            next_action=conv.get("next_action", ""),
            deal_value=conv.get("deal_value"),
        ))

    activity_feed = [AgentEvent(**e) for e in state["activity_feed"][:100]]

    from schema import Campaign
    start = state["start_date"]
    end_date = (
        datetime.strptime(start, "%Y-%m-%d") + timedelta(days=max(state["day"], 1))
    ).strftime("%Y-%m-%d")
    campaigns = [Campaign(
        name=state["campaign_name"],
        brand="Your Brand",
        start_date=start,
        end_date=end_date,
        budget=state["budget_total"],
        spent=int(state["budget_spent"]),
        influencer_count=sum(
            1 for info in state["pipeline"].values()
            if info["stage"] in ("Signed", "Content Posted", "Converted")
        ),
        status="Active",
        target_niche=", ".join(state["niches"]) if state["niches"] else "All",
        target_platforms=state["platforms"] if state["platforms"] else [],
    )]

    return {
        "influencers": influencers,
        "campaigns": campaigns,
        "conversations": conversations,
        "activity_feed": activity_feed,
    }


# ── Helpers ──────────────────────────────────────────────────────────────

def _deterministic_delay(handle: str, stage: str, delay_min: int, delay_max: int) -> int:
    """Compute a deterministic delay for this influencer at this stage."""
    h = hash(handle + stage + "delay") & 0x7FFFFFFF
    return delay_min + (h % (delay_max - delay_min + 1))


def _get_influencer(state: dict, handle: str) -> dict | None:
    """Look up an influencer dict in the pool by handle."""
    for inf in state["pool"]:
        if inf["handle"] == handle:
            return inf
    return None


def _event(day: int, start_date: str, event_type: str,
           description: str, detail: str, severity: str) -> dict:
    """Create an AgentEvent dict."""
    base = datetime.strptime(start_date, "%Y-%m-%d")
    dt = base + timedelta(days=day)
    hour = 9 + (hash(str(day) + event_type) % 9)
    minute = hash(str(day) + description) % 60
    ts = dt.replace(hour=hour, minute=minute).strftime("%Y-%m-%d %H:%M")
    return {
        "timestamp": ts,
        "event_type": event_type,
        "description": description,
        "detail": detail,
        "severity": severity,
    }
