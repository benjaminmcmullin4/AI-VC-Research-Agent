"""Configuration for Influx."""

APP_NAME = "Influx"
APP_SUBTITLE = "AI-Powered Influencer Acquisition"

# ── LLM ──────────────────────────────────────────────────────────────────
DEFAULT_MODEL = "claude-sonnet-4-20250514"
MAX_RETRIES = 3

# ── Domain ───────────────────────────────────────────────────────────────
PLATFORMS = ["Instagram", "TikTok", "YouTube", "Twitter"]
NICHES = ["Fitness", "Beauty", "Tech", "Food", "Lifestyle", "Fashion", "Gaming", "Travel"]

PIPELINE_STAGES = [
    "Discovered", "Qualified", "Contacted", "Replied",
    "Negotiating", "Signed", "Content Posted", "Converted",
]

STAGE_COLORS = {
    "Discovered":     "#94A3B8",
    "Qualified":      "#6366F1",
    "Contacted":      "#8B5CF6",
    "Replied":        "#10B981",
    "Negotiating":    "#F59E0B",
    "Signed":         "#4F46E5",
    "Content Posted": "#EC4899",
    "Converted":      "#06B6D4",
}

PLATFORM_COLORS = {
    "Instagram": "#E1306C",
    "TikTok":    "#475569",
    "YouTube":   "#EF4444",
    "Twitter":   "#3B82F6",
}

# ── Pages ────────────────────────────────────────────────────────────────
SIDEBAR_PAGES = [
    ("Campaign",       "campaign"),
    ("Influencers",    "influencers"),
    ("Conversations",  "conversations"),
    ("Analytics",      "analytics"),
]

# ── Simulation ───────────────────────────────────────────────────────────
POOL_SIZE = 750
DEFAULT_BUDGET = 50_000

TRANSITION_PROBABILITIES = {
    "Discovered->Qualified": 0.60,
    "Qualified->Contacted": 1.00,
    "Contacted->Replied": 0.50,
    "Replied->Negotiating": 0.80,
    "Replied->Declined": 0.20,
    "Negotiating->Signed": 0.75,
    "Negotiating->Declined": 0.25,
    "Signed->Content Posted": 0.95,
    "Content Posted->Converted": 0.85,
}

TRANSITION_DELAYS = {
    "Discovered": (1, 2),       # days before qualification check
    "Qualified": (0, 1),        # days before auto-outreach
    "Contacted": (2, 7),        # days waiting for reply
    "Replied": (1, 3),          # days before negotiation starts
    "Negotiating": (3, 7),      # days to close or decline
    "Signed": (7, 14),          # days to produce content
    "Content Posted": (7, 21),  # days for revenue to fully attribute
}

DISCOVERY_RATE = (5, 15)  # influencers discovered per day (min, max)

# ── Design tokens ────────────────────────────────────────────────────────
COLORS = {
    "bg":         "#FFFFFF",
    "surface":    "#F8FAFC",
    "border":     "#E2E8F0",
    "text":       "#0F172A",
    "text_sec":   "#475569",
    "text_muted": "#94A3B8",
    "accent":     "#4F46E5",
    "success":    "#10B981",
    "warning":    "#F59E0B",
    "error":      "#EF4444",
    "sidebar_bg": "#0F172A",
}
