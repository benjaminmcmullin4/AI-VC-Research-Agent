"""Configuration for Influx."""

APP_NAME = "Influx"
APP_SUBTITLE = "Influencer Intelligence"

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
    ("Dashboard",      "dashboard"),
    ("Influencers",    "influencers"),
    ("Conversations",  "conversations"),
    ("Analytics",      "analytics"),
]

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
