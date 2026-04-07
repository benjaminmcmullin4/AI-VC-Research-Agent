"""Configuration constants for Agentic Marketing and Company Growth."""

APP_NAME = "Agentic Marketing and Company Growth"
APP_SUBTITLE = "Influencer Intelligence Platform"

# ── LLM ──────────────────────────────────────────────────────────────────
DEFAULT_MODEL = "claude-sonnet-4-20250514"
MAX_RETRIES = 3

# ── Domain ───────────────────────────────────────────────────────────────
PLATFORMS = ["Instagram", "TikTok", "YouTube", "Twitter"]

NICHES = [
    "Fitness", "Beauty", "Tech", "Food",
    "Lifestyle", "Fashion", "Gaming", "Travel",
]

PIPELINE_STAGES = [
    "Discovered", "Qualified", "Contacted", "Replied",
    "Negotiating", "Signed", "Content Posted", "Converted",
]

STAGE_COLORS = {
    "Discovered":     "#94A3B8",
    "Qualified":      "#60A5FA",
    "Contacted":      "#A78BFA",
    "Replied":        "#34D399",
    "Negotiating":    "#FBBF24",
    "Signed":         "#F97316",
    "Content Posted": "#F472B6",
    "Converted":      "#1ABC9C",
}

PLATFORM_COLORS = {
    "Instagram": "#E1306C",
    "TikTok":    "#010101",
    "YouTube":   "#FF0000",
    "Twitter":   "#1DA1F2",
}

# ── Sidebar navigation ──────────────────────────────────────────────────
SIDEBAR_PAGES = [
    ("Dashboard",       "dashboard"),
    ("Influencer Discovery", "discovery"),
    ("Recommendations", "recommendations"),
    ("Outreach",        "outreach"),
    ("Campaign Pipeline", "pipeline"),
    ("Analytics",       "analytics"),
    ("Agent Activity",  "activity"),
]

# ── Colors / design tokens ──────────────────────────────────────────────
COLORS = {
    "navy":       "#0A0A0A",
    "steel":      "#333333",
    "teal":       "#1ABC9C",
    "gold":       "#D4A338",
    "red":        "#E74C3C",
    "muted":      "#777777",
    "light_gray": "#ECF0F1",
    "bg":         "#FAFBFC",
    "bg_alt":     "#F0F4F8",
}

FONT = "Inter"
