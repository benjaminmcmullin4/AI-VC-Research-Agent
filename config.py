"""Configuration constants for Influx — Influencer Intelligence."""

APP_NAME = "Influx"
APP_SUBTITLE = "Influencer Intelligence"

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
    "Discovered":     "#8B8D9E",
    "Qualified":      "#60A5FA",
    "Contacted":      "#A78BFA",
    "Replied":        "#00D68F",
    "Negotiating":    "#FFB800",
    "Signed":         "#6C5CE7",
    "Content Posted": "#F472B6",
    "Converted":      "#00CFD5",
}

PLATFORM_COLORS = {
    "Instagram": "#E1306C",
    "TikTok":    "#E8E8ED",
    "YouTube":   "#FF4757",
    "Twitter":   "#1DA1F2",
}

# ── Sidebar navigation ──────────────────────────────────────────────────
SIDEBAR_PAGES = [
    ("Dashboard",          "dashboard"),
    ("Find & Reach Out",   "find"),
    ("Outreach & Pipeline", "outreach_pipeline"),
]

# ── Colors / design tokens ──────────────────────────────────────────────
COLORS = {
    "bg":             "#0F1117",
    "surface":        "#1A1D2E",
    "surface_hover":  "#252836",
    "border":         "#2A2D3E",
    "primary":        "#6C5CE7",
    "secondary":      "#00CFD5",
    "text":           "#E8E8ED",
    "text_secondary": "#8B8D9E",
    "text_muted":     "#5B5D6E",
    "success":        "#00D68F",
    "warning":        "#FFB800",
    "error":          "#FF4757",
}

FONT = "Inter"
