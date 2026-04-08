"""Template-based conversation generation for outreach simulation."""

from __future__ import annotations

import random as _random
from datetime import datetime, timedelta


# ── Outreach templates ───────────────────────────────────────────────────

OUTREACH_TEMPLATES = [
    "Hi {first_name}! I came across your {content_ref} and was really impressed. We're running a {campaign_name} campaign and think your audience would be a perfect fit. Would you be open to a quick chat about a potential partnership?",
    "Hey {first_name}, love what you've been doing with {content_ref}. I'm reaching out from {campaign_name} — we're looking for creators like you to collaborate with. Interested in learning more?",
    "Hi {first_name}! Your {content_ref} caught our attention. We're putting together a creator campaign ({campaign_name}) and think you'd be amazing. Can I send over some details?",
    "{first_name} — huge fan of your {content_ref}. We're launching {campaign_name} and are looking for authentic voices in the {niche} space. Would love to explore a collab. Thoughts?",
    "Hey {first_name}! We've been following your work, especially your {content_ref}. For our {campaign_name} initiative, we're partnering with select {niche} creators. You'd be a great fit — interested?",
    "Hi {first_name}, I hope this message finds you well! Your {content_ref} really resonates with our brand. We'd love to discuss a paid partnership as part of our {campaign_name} campaign. Open to chatting?",
    "Hey there {first_name}! Quick intro — we're running {campaign_name} and curating a group of {niche} creators to partner with. Your {content_ref} stood out to us. Want to hear more?",
    "Hi {first_name}! We noticed your amazing {content_ref} and think there's a great alignment with {campaign_name}. We're offering paid partnerships for select creators. Can I share the details?",
    "{first_name}, your {content_ref} is exactly the kind of content we love. We're looking for {niche} creators for {campaign_name}. Would you be interested in a sponsored collaboration?",
    "Hey {first_name}! Your audience engagement on {content_ref} is incredible. We think our {campaign_name} campaign could be a great match. Mind if I share more info?",
    "Hi {first_name} — reaching out because your {content_ref} aligns perfectly with what we're building for {campaign_name}. We'd love to bring you on as a creator partner. Interested?",
    "Hey {first_name}! I'm with the {campaign_name} team. Your {content_ref} caught our eye and we think you'd be an incredible fit for our upcoming campaign. Can we connect?",
    "Hi {first_name}, love your approach to {content_ref}! We're launching {campaign_name} and looking for {niche} creators who bring authenticity. Would you be open to collaborating?",
    "Hey {first_name}! Just discovered your {content_ref} and had to reach out. We're running {campaign_name} and would love to partner with you. Let me know if you'd like to hear more!",
    "{first_name} — your {content_ref} is fire. We're putting together something special with {campaign_name} and think you'd crush it. Want to learn more about the opportunity?",
]

# ── Niche-specific content references ────────────────────────────────────

NICHE_CONTENT_REFS = {
    "Fitness": [
        "HIIT series", "workout breakdowns", "transformation content",
        "training vlogs", "meal prep posts", "fitness challenges",
        "gym tutorials", "recovery routines", "strength series",
    ],
    "Beauty": [
        "skincare routines", "makeup tutorials", "product reviews",
        "get-ready-with-me content", "beauty hauls", "glow-up series",
        "foundation comparisons", "beauty tips content", "morning routine",
    ],
    "Tech": [
        "tech reviews", "unboxing content", "gear comparisons",
        "setup tours", "product deep dives", "how-to guides",
        "first look videos", "tech tip series", "gadget roundups",
    ],
    "Food": [
        "recipe content", "restaurant reviews", "cooking tutorials",
        "meal prep series", "food challenges", "kitchen hack posts",
        "taste test content", "brunch series", "comfort food recipes",
    ],
    "Lifestyle": [
        "daily vlogs", "productivity content", "self-care routines",
        "home organization posts", "journaling content", "morning routine series",
        "wellness tips", "day-in-my-life content", "mindfulness posts",
    ],
    "Fashion": [
        "outfit-of-the-day posts", "styling content", "try-on hauls",
        "thrift flip series", "capsule wardrobe content", "trend analysis",
        "fashion lookbooks", "seasonal styling guides", "wardrobe tours",
    ],
    "Gaming": [
        "gameplay streams", "game reviews", "tier list content",
        "speedrun attempts", "build guides", "gaming setup tours",
        "first impressions videos", "challenge runs", "community events",
    ],
    "Travel": [
        "travel vlogs", "destination guides", "hidden gem series",
        "budget travel tips", "hotel reviews", "adventure content",
        "cultural exploration posts", "travel photography", "itinerary breakdowns",
    ],
}

# ── Reply templates by outcome ───────────────────────────────────────────

POSITIVE_REPLIES = [
    "Hey! Thanks so much for reaching out — this sounds really cool! I'd love to hear more about the campaign and what the partnership would look like.",
    "Hi there! I'm definitely interested. I've been looking for brand collabs that align with my content. Can you send over more details?",
    "Oh wow, thanks for thinking of me! This sounds like a great fit. What are the next steps?",
    "Hey! Love this. I'm always open to partnerships that feel authentic to my audience. Let's chat more!",
    "Thanks for reaching out! I checked out your campaign and I think this could work really well. What did you have in mind?",
    "Hi! Appreciate you reaching out. I'm interested — what's the timeline and scope looking like?",
    "This sounds amazing! I've been wanting to work on something like this. Can we hop on a quick call?",
    "Hey, thanks! I'm really interested. My schedule is flexible this month — what are you thinking for deliverables?",
    "I love this idea! My audience would be really into it. Send over the details and let's make it happen.",
    "Hi! Yes, I'm open to this. I've done similar collabs before and they performed really well. Let's discuss!",
    "Oh this is right up my alley! Would love to learn more about the creative direction and compensation.",
    "Hey! I'm in. Just send me the brief and let's get started!",
]

QUESTION_REPLIES = [
    "Hey, thanks for reaching out! Before I commit, can I ask — what's the exclusivity window? I have some other brand conversations going on.",
    "Interesting! Can you tell me more about the brand and campaign goals? I want to make sure it's the right fit for my audience.",
    "Hi! I'm potentially interested. What kind of deliverables are you thinking, and what's the timeline?",
    "Thanks for reaching out. What's the compensation structure looking like? I want to be upfront about my rates.",
    "Hey! This sounds cool but I'd want to know more about creative freedom. Do I get to put my own spin on it?",
    "I appreciate the message! Quick question — is this a one-time thing or an ongoing partnership? That affects my decision.",
    "Hi! Before I say yes, what platforms are you thinking for the content? I'm strongest on {platform}.",
    "Interesting opportunity! What's the campaign budget per creator? Want to make sure we're aligned on expectations.",
    "Thanks for the outreach! Do you have examples of other creators you've worked with? I like to vet partnerships carefully.",
    "Hey! Sounds promising. What's the usage rights situation? I need to know how the content will be repurposed.",
]

NEGOTIATION_MESSAGES_INFLUENCER = [
    "I appreciate the offer! My rate for this type of content is usually ${rate}. Is there flexibility on the budget?",
    "Thanks for the details! I'd be happy to do this for ${rate}. That includes one main post and story coverage.",
    "Love the brief! For the scope you described, I'd normally charge ${rate}. Can we meet in the middle?",
    "The creative direction looks great. My standard rate is ${rate} for this kind of partnership. Does that work?",
    "I'm excited about this! For the full package (post + stories + usage rights), I'd say ${rate} is fair.",
    "Thanks for putting this together. Given my engagement rates and audience size, ${rate} would be my rate for this.",
    "Happy to move forward! My rate for a campaign like this is ${rate}. Open to discussing the scope if needed.",
    "This looks awesome. I'd want ${rate} for the deliverables listed. I can also add extra stories for a small bump.",
]

NEGOTIATION_MESSAGES_AGENT = [
    "Thanks for sharing your rate! We can work with ${deal}. That would include the main content piece plus one round of stories. Does that work?",
    "Appreciate the transparency! Our budget for this slot is ${deal}. We think it's a fair match given the campaign exposure and ongoing partnership potential.",
    "We can do ${deal} for the full package. This also includes being featured in our campaign wrap-up and potential for renewal next quarter.",
    "Our offer is ${deal}. We've structured this to be competitive — plus you'd get affiliate commission on any sales your content drives.",
    "How about ${deal}? That covers the main deliverable plus usage rights for 90 days. We're flexible on the creative approach.",
]

DECLINE_REPLIES = [
    "Hey, thanks so much for thinking of me! Unfortunately, I'm not taking on sponsored content right now. Best of luck with the campaign!",
    "I appreciate the outreach but this doesn't quite align with my current brand direction. Wishing you all the best!",
    "Thanks for reaching out! I'm currently exclusive with a competing brand so I can't take this on. Maybe next time!",
    "Hey! I love the concept but my schedule is completely packed for the next few months. Hope to work together in the future.",
    "Thanks but I'll have to pass on this one. The brand fit isn't quite right for my audience. No hard feelings!",
    "Appreciate the opportunity! I've decided to focus on fewer partnerships this quarter to keep things authentic. Best of luck!",
    "Hi! I'm going to pass for now — I'm being selective about collabs and this one isn't quite the right fit. Thanks though!",
    "Thanks for the offer! I'm currently committed to other campaigns and can't take on anything new right now.",
]

SIGNED_CONFIRMATIONS = [
    "Let's do it! I'll sign the agreement today and start planning the content. So excited!",
    "Deal! Sending the signed contract back now. Looking forward to this partnership!",
    "We're a go! I've reviewed everything and I'm happy with the terms. Let's make something great.",
    "Signed, sealed, delivered! Can't wait to get started on the creative.",
    "All signed! I already have some content ideas in mind. When do you want the first draft?",
]


# ── Generator functions ──────────────────────────────────────────────────

def _format_date(start_date: str, day: int) -> str:
    """Convert simulation day number to a formatted timestamp."""
    base = datetime.strptime(start_date, "%Y-%m-%d")
    dt = base + timedelta(days=day)
    hour = 9 + (hash(str(day)) % 9)  # 9 AM to 5 PM-ish
    minute = (hash(str(day) + "m") % 60)
    return dt.replace(hour=hour, minute=minute).strftime("%Y-%m-%d %H:%M")


def generate_outreach(influencer: dict, campaign_name: str, day: int,
                      start_date: str, rng: _random.Random) -> dict:
    """Generate an outreach message for an influencer."""
    niche = influencer["niche"]
    first_name = influencer["name"].split()[0]
    content_refs = NICHE_CONTENT_REFS.get(niche, ["content"])
    content_ref = rng.choice(content_refs)

    template = rng.choice(OUTREACH_TEMPLATES)
    body = template.format(
        first_name=first_name,
        content_ref=content_ref,
        campaign_name=campaign_name,
        niche=niche.lower(),
        platform=influencer["platform"],
    )

    return {
        "sender": "agent",
        "content": body,
        "timestamp": _format_date(start_date, day),
        "message_type": "initial",
    }


def generate_reply(influencer: dict, outcome: str, day: int,
                   start_date: str, rng: _random.Random) -> dict | None:
    """Generate an influencer reply based on outcome.

    outcome: 'interested', 'questions', 'declined'
    """
    if outcome == "interested":
        content = rng.choice(POSITIVE_REPLIES)
    elif outcome == "questions":
        template = rng.choice(QUESTION_REPLIES)
        content = template.replace("{platform}", influencer["platform"])
    elif outcome == "declined":
        content = rng.choice(DECLINE_REPLIES)
    else:
        return None

    return {
        "sender": "influencer",
        "content": content,
        "timestamp": _format_date(start_date, day),
        "message_type": "reply",
    }


def generate_negotiation_exchange(influencer: dict, deal_value: float, day: int,
                                  start_date: str, rng: _random.Random) -> list[dict]:
    """Generate a negotiation exchange (influencer rate + agent offer)."""
    # Influencer asks for a rate (slightly above the deal value)
    influencer_rate = int(deal_value * rng.uniform(1.0, 1.4))
    inf_template = rng.choice(NEGOTIATION_MESSAGES_INFLUENCER)
    inf_msg = {
        "sender": "influencer",
        "content": inf_template.replace("${rate}", f"${influencer_rate:,}"),
        "timestamp": _format_date(start_date, day),
        "message_type": "negotiation",
    }

    # Agent responds with the deal value
    agent_template = rng.choice(NEGOTIATION_MESSAGES_AGENT)
    agent_msg = {
        "sender": "agent",
        "content": agent_template.replace("${deal}", f"${int(deal_value):,}"),
        "timestamp": _format_date(start_date, day + 1),
        "message_type": "negotiation",
    }

    return [inf_msg, agent_msg]


def generate_signed_message(day: int, start_date: str, rng: _random.Random) -> dict:
    """Generate a confirmation message from the influencer after signing."""
    return {
        "sender": "influencer",
        "content": rng.choice(SIGNED_CONFIRMATIONS),
        "timestamp": _format_date(start_date, day),
        "message_type": "reply",
    }


def generate_decline_message(influencer: dict, day: int,
                             start_date: str, rng: _random.Random) -> dict:
    """Generate a decline message during negotiation."""
    declines = [
        "I appreciate the offer but after thinking about it, the budget doesn't quite work for me. Thanks anyway!",
        "Hey, I've decided to go in a different direction. The terms aren't quite what I was hoping for. No hard feelings!",
        "Thanks for working with me on this, but I'm going to pass. The scope vs compensation isn't aligned for me right now.",
        "I've thought it over and I'll have to decline. I hope we can work together on something else in the future!",
    ]
    return {
        "sender": "influencer",
        "content": rng.choice(declines),
        "timestamp": _format_date(start_date, day),
        "message_type": "reply",
    }
