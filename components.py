"""Shared UI components for Influx."""

from __future__ import annotations

from datetime import datetime, timedelta

from config import COLORS, PIPELINE_STAGES, PLATFORM_COLORS, RADIUS, SHADOWS, STAGE_COLORS
from schema import AgentEvent, Influencer


def fmt_followers(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}K"
    return str(n)


def page_header(title: str, subtitle: str = "") -> str:
    sub_html = f'<div style="font-size:14px;color:{COLORS["text_sec"]};margin-top:4px;font-weight:400">{subtitle}</div>' if subtitle else ""
    return f"""
    <div style="margin-bottom:32px">
        <div style="font-size:28px;font-weight:700;color:{COLORS["text"]};letter-spacing:-0.02em">{title}</div>
        {sub_html}
    </div>
    """


def metric_card(label: str, value: str, sub: str = "", accent: bool = False) -> str:
    bg = COLORS["accent_light"] if accent else COLORS["bg"]
    border = f'border:1px solid {COLORS["accent"]}20;' if accent else "border:none;"
    shadow = SHADOWS["md"] if accent else SHADOWS["sm"]
    sub_html = f'<div style="color:{COLORS["text_muted"]};font-size:13px;margin-top:6px;font-weight:500">{sub}</div>' if sub else ""
    return f"""
    <div class="influx-card" style="background:{bg};{border}
        border-radius:{RADIUS["lg"]};padding:24px 20px;
        box-shadow:{shadow}">
        <div style="font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;
            color:{COLORS["text_muted"]};margin-bottom:10px">{label}</div>
        <div style="font-size:28px;font-weight:800;color:{COLORS["text"]};letter-spacing:-0.025em;
            line-height:1.1">{value}</div>
        {sub_html}
    </div>
    """


def section_label(text: str) -> str:
    return f"""
    <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;
        color:{COLORS["text_muted"]};margin:36px 0 14px;padding-bottom:8px;
        border-bottom:2px solid {COLORS["border_light"]};display:inline-block">{text}</div>
    """


def pipeline_bar(counts: dict) -> str:
    total = sum(counts.values())
    if total == 0:
        return ""
    segments = ""
    labels = ""
    for stage in PIPELINE_STAGES:
        count = counts.get(stage, 0)
        if count == 0:
            continue
        pct = count / total * 100
        color = STAGE_COLORS.get(stage, COLORS["text_muted"])
        segments += f'<div style="flex:{pct};background:{color};height:100%;transition:flex 0.5s ease" title="{stage}: {count}"></div>'
        labels += (
            f'<div style="flex:{pct};text-align:center;min-width:0;padding-top:10px">'
            f'<div style="font-size:11px;color:{COLORS["text_muted"]};overflow:hidden;text-overflow:ellipsis;'
            f'white-space:nowrap;font-weight:500">{stage}</div>'
            f'<div style="font-size:16px;font-weight:700;color:{COLORS["text"]};margin-top:2px">{count}</div>'
            f'</div>'
        )
    return f"""
    <div class="influx-card" style="background:{COLORS["bg"]};border-radius:{RADIUS["lg"]};
        padding:20px 24px;box-shadow:{SHADOWS["sm"]};margin:8px 0 24px">
        <div style="display:flex;gap:2px;border-radius:{RADIUS["full"]};overflow:hidden;height:8px;
            background:{COLORS["surface_alt"]}">{segments}</div>
        <div style="display:flex;gap:2px">{labels}</div>
    </div>
    """


def activity_item(ev: AgentEvent, sim_start_date: str | None = None) -> str:
    icon_map = {
        "discovery": ("bi-search", COLORS["accent"]),
        "qualification": ("bi-check-circle", COLORS["accent"]),
        "outreach": ("bi-send", "#8B5CF6"),
        "reply_detected": ("bi-reply", COLORS["success"]),
        "negotiation": ("bi-currency-dollar", COLORS["warning"]),
        "content_posted": ("bi-camera-video", "#EC4899"),
        "conversion": ("bi-graph-up-arrow", COLORS["success"]),
        "insight": ("bi-lightbulb", COLORS["warning"]),
        "alert": ("bi-exclamation-triangle", COLORS["error"]),
    }
    # Fall back based on severity
    severity_map = {
        "success": ("bi-check-circle", COLORS["success"]),
        "warning": ("bi-exclamation-circle", COLORS["warning"]),
        "info": ("bi-info-circle", COLORS["text_muted"]),
    }
    icon_cls, icon_color = icon_map.get(
        ev.event_type,
        severity_map.get(ev.severity, ("bi-circle", COLORS["text_muted"])),
    )

    ts = ev.timestamp[:10]
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    if ts == today:
        rel = "Today"
    elif ts == yesterday:
        rel = "Yesterday"
    else:
        rel = ts[5:]

    return f"""
    <div style="display:flex;gap:14px;padding:14px 0;border-bottom:1px solid {COLORS["border_light"]};
        align-items:flex-start">
        <div style="width:32px;height:32px;border-radius:8px;background:{icon_color}12;
            display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px">
            <i class="bi {icon_cls}" style="font-size:14px;color:{icon_color}"></i>
        </div>
        <div style="flex:1;min-width:0">
            <div style="font-size:14px;color:{COLORS["text"]};line-height:1.5;font-weight:500">{ev.description}</div>
        </div>
        <div style="font-size:12px;color:{COLORS["text_muted"]};white-space:nowrap;font-weight:500;
            margin-top:2px">{rel}</div>
    </div>
    """


def budget_bar(total: float, spent: float, committed: float) -> str:
    """Horizontal stacked bar showing budget allocation."""
    remaining = max(0, total - spent - committed)
    pct_spent = spent / total * 100 if total else 0
    pct_committed = committed / total * 100 if total else 0
    pct_remaining = remaining / total * 100 if total else 0
    return f"""
    <div class="influx-card" style="background:{COLORS["bg"]};border-radius:{RADIUS["lg"]};
        padding:20px 24px;box-shadow:{SHADOWS["sm"]}">
        <div style="display:flex;gap:2px;border-radius:{RADIUS["full"]};overflow:hidden;height:10px;
            background:{COLORS["surface_alt"]}">
            <div style="flex:{pct_spent};background:linear-gradient(90deg,#4F46E5,#6366F1);height:100%;
                transition:flex 0.5s ease" title="Spent: ${spent:,.0f}"></div>
            <div style="flex:{pct_committed};background:{COLORS["warning"]};height:100%;
                transition:flex 0.5s ease" title="Committed: ${committed:,.0f}"></div>
            <div style="flex:{pct_remaining};height:100%" title="Remaining: ${remaining:,.0f}"></div>
        </div>
        <div style="display:flex;justify-content:space-between;margin-top:12px;font-size:12px;font-weight:500;
            color:{COLORS["text_sec"]}">
            <span style="display:flex;align-items:center;gap:6px">
                <span style="width:8px;height:8px;border-radius:3px;background:linear-gradient(135deg,#4F46E5,#6366F1)"></span>
                Spent ${spent:,.0f}
            </span>
            <span style="display:flex;align-items:center;gap:6px">
                <span style="width:8px;height:8px;border-radius:3px;background:{COLORS["warning"]}"></span>
                Committed ${committed:,.0f}
            </span>
            <span style="display:flex;align-items:center;gap:6px">
                <span style="width:8px;height:8px;border-radius:3px;background:{COLORS["surface_alt"]}"></span>
                Available ${remaining:,.0f}
            </span>
        </div>
    </div>
    """


def day_counter_html(day: int, start_date: str) -> str:
    """Styled day counter with calendar date."""
    base = datetime.strptime(start_date, "%Y-%m-%d")
    calendar_date = (base + timedelta(days=day)).strftime("%b %d, %Y")
    return f"""
    <div class="influx-card" style="background:{COLORS["bg"]};
        border-radius:{RADIUS["lg"]};padding:20px 24px;margin-bottom:20px;
        display:flex;align-items:center;gap:20px;box-shadow:{SHADOWS["sm"]}">
        <div>
            <div style="font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;
                color:{COLORS["text_muted"]};margin-bottom:4px">Simulation Day</div>
            <div style="font-size:32px;font-weight:800;
                background:linear-gradient(135deg,#6366F1,#4F46E5);-webkit-background-clip:text;
                -webkit-text-fill-color:transparent;letter-spacing:-0.02em">{day}</div>
        </div>
        <div style="width:1px;height:40px;background:{COLORS["border_light"]}"></div>
        <div>
            <div style="font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;
                color:{COLORS["text_muted"]};margin-bottom:4px">Calendar Date</div>
            <div style="font-size:16px;font-weight:600;color:{COLORS["text"]}">{calendar_date}</div>
        </div>
    </div>
    """


def progress_bar_html(current: int, target: int) -> str:
    pct = min(100, current / target * 100) if target else 0
    return f"""
    <div style="margin:8px 0 28px">
        <div style="display:flex;justify-content:space-between;margin-bottom:8px;align-items:baseline">
            <span style="font-size:14px;font-weight:600;color:{COLORS["text"]}">{current} of {target} onboarded</span>
            <span style="font-size:20px;font-weight:800;color:{COLORS["accent"]};letter-spacing:-0.02em">{pct:.0f}%</span>
        </div>
        <div style="background:{COLORS["surface_alt"]};border-radius:{RADIUS["full"]};height:10px;overflow:hidden">
            <div style="width:{pct}%;height:100%;background:linear-gradient(90deg,#6366F1,#4F46E5);
                border-radius:{RADIUS["full"]};transition:width 0.5s ease;
                box-shadow:0 0 8px rgba(79,70,229,0.3)"></div>
        </div>
    </div>
    """


def chat_bubble(content: str, sender: str, name: str, timestamp: str) -> str:
    is_agent = sender == "agent"
    if is_agent:
        bg = "linear-gradient(135deg,#4F46E5,#6366F1)"
        text_c = "#FFFFFF"
        align = "flex-end"
        radius = "18px 18px 4px 18px"
        label_c = "rgba(255,255,255,0.6)"
        shadow = "0 2px 8px rgba(79,70,229,0.2)"
        border = "none"
    else:
        bg = COLORS["bg"]
        text_c = COLORS["text"]
        align = "flex-start"
        radius = "18px 18px 18px 4px"
        label_c = COLORS["text_muted"]
        shadow = SHADOWS["sm"]
        border = f"1px solid {COLORS['border_light']}"
    label = "AI Agent" if is_agent else name
    return f"""
    <div style="display:flex;justify-content:{align};margin-bottom:12px">
        <div style="max-width:72%;background:{bg};color:{text_c};padding:14px 18px;border-radius:{radius};
            border:{border};box-shadow:{shadow}">
            <div style="font-size:11px;font-weight:600;color:{label_c};margin-bottom:4px;
                letter-spacing:0.02em">{label} · {timestamp[5:16]}</div>
            <div style="font-size:14px;line-height:1.6">{content}</div>
        </div>
    </div>
    """
