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
    # Backgrounds
    "bg":           "#FFFFFF",
    "surface":      "#F8FAFC",
    "surface_alt":  "#F1F5F9",
    "overlay":      "#FFFFFF",
    # Borders
    "border":       "#E2E8F0",
    "border_light": "#F1F5F9",
    # Text
    "text":         "#0F172A",
    "text_sec":     "#475569",
    "text_muted":   "#94A3B8",
    "text_inverse": "#FFFFFF",
    # Brand
    "accent":       "#4F46E5",
    "accent_hover": "#4338CA",
    "accent_light": "#EEF2FF",
    "accent_muted": "rgba(79,70,229,0.08)",
    # Semantic
    "success":      "#10B981",
    "success_light":"#ECFDF5",
    "warning":      "#F59E0B",
    "warning_light":"#FFFBEB",
    "error":        "#EF4444",
    "error_light":  "#FEF2F2",
    # Sidebar
    "sidebar_bg":   "#0F172A",
    "sidebar_hover":"rgba(255,255,255,0.06)",
    "sidebar_active":"rgba(79,70,229,0.15)",
}

# ── Elevation (box-shadow scale) ─────────────────────────────────────────
SHADOWS = {
    "xs":  "0 1px 2px rgba(0,0,0,0.04)",
    "sm":  "0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04)",
    "md":  "0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -2px rgba(0,0,0,0.05)",
    "lg":  "0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.04)",
    "xl":  "0 20px 25px -5px rgba(0,0,0,0.08), 0 8px 10px -6px rgba(0,0,0,0.04)",
}

# ── Radius scale ─────────────────────────────────────────────────────────
RADIUS = {
    "sm": "6px", "md": "10px", "lg": "14px", "xl": "20px", "full": "9999px",
}
