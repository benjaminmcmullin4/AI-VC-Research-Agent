"""Configuration constants, color palette, and settings."""

from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent
DB_PATH = PROJECT_ROOT / "research.db"
CACHE_DIR = PROJECT_ROOT / ".cache"
DEMO_OUTPUT_PATH = PROJECT_ROOT / "examples" / "demo_output.json"

# ── Branding ──────────────────────────────────────────────────────────
FIRM_NAME = "Deal Team"
APP_TITLE = "Market Research Platform"
APP_SUBTITLE = "AI-powered market maps and thesis memos for internal use"

# ── Design System ──────────────────────────────────────────────────────
COLORS = {
    "navy": "#0A0A0A",
    "steel_blue": "#333333",
    "teal": "#1ABC9C",
    "red_accent": "#E74C3C",
    "gold_accent": "#D4A338",
    "bg": "#FAFBFC",
    "text": "#1A1A1A",
    "muted": "#777777",
    "light_gray": "#ECF0F1",
    "white": "#FFFFFF",
}

FONT = "Inter"

# Plotly color sequence for segments
SEGMENT_COLORS = [
    "#333333",  # dark gray
    "#1ABC9C",  # teal
    "#D4A338",  # gold
    "#E74C3C",  # red
    "#9B59B6",  # purple
    "#2ECC71",  # green
    "#E67E22",  # orange
    "#0A0A0A",  # black
]

# ── LLM Settings ───────────────────────────────────────────────────────
DEFAULT_MODEL = "claude-sonnet-4-20250514"
MAX_RETRIES = 3

DEPTH_PRESETS = {
    "Quick": {
        "label": "Quick (~3 min)",
        "detail_level": "concise",
        "company_count": 10,
        "temperature": 0.4,
    },
    "Standard": {
        "label": "Standard (~5 min)",
        "detail_level": "standard",
        "company_count": 15,
        "temperature": 0.5,
    },
    "Deep": {
        "label": "Deep (~8 min)",
        "detail_level": "detailed",
        "company_count": 20,
        "temperature": 0.6,
    },
}

STAGE_OPTIONS = ["All Stages", "Seed", "Series A", "Series B", "Growth / Late Stage"]

GEOGRAPHY_OPTIONS = [
    "Global",
    "North America",
    "Europe",
    "Asia-Pacific",
    "Latin America",
    "Middle East & Africa",
]

# ── Pipeline Step Names ────────────────────────────────────────────────
PIPELINE_STEPS = [
    ("market_spec", "Analyzing market definition..."),
    ("taxonomy", "Building taxonomy & subsegments..."),
    ("landscape", "Mapping company landscape..."),
    ("sizing", "Estimating TAM/SAM..."),
    ("thesis", "Synthesizing investment thesis..."),
    ("memo", "Assembling full memo..."),
]

# ── Export ──────────────────────────────────────────────────────────────
MEMO_SECTIONS = [
    "Executive Summary",
    "Market Overview",
    "TAM / SAM Sizing",
    "Competitive Landscape",
    "Taxonomy & Segmentation",
    "Company Profiles",
    "Investment Thesis",
    "Value Creation Angles",
    "Risks & Mitigants",
    "Diligence Plan",
    "Sources & Methodology",
]
