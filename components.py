"""Shared UI components for Influx."""

from __future__ import annotations

from datetime import datetime, timedelta

from config import COLORS, PIPELINE_STAGES, PLATFORM_COLORS, STAGE_COLORS
from schema import AgentEvent, Influencer


def fmt_followers(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}K"
    return str(n)


def metric_card(label: str, value: str, sub: str = "") -> str:
    sub_html = f'<div style="color:{COLORS["text_muted"]};font-size:13px;margin-top:4px">{sub}</div>' if sub else ""
    return f"""
    <div style="background:{COLORS["surface"]};border:1px solid {COLORS["border"]};
        border-radius:10px;padding:24px;margin-bottom:8px">
        <div style="font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;
            color:{COLORS["text_muted"]};margin-bottom:8px">{label}</div>
        <div style="font-size:32px;font-weight:800;color:{COLORS["text"]};letter-spacing:-0.02em">{value}</div>
        {sub_html}
    </div>
    """


def section_label(text: str) -> str:
    return f"""
    <div style="font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;
        color:{COLORS["text_muted"]};margin:32px 0 12px">{text}</div>
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
        segments += f'<div style="flex:{pct};background:{color};height:6px" title="{stage}: {count}"></div>'
        labels += (
            f'<div style="flex:{pct};text-align:center;min-width:0">'
            f'<div style="font-size:11px;color:{COLORS["text_muted"]};margin-top:6px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{stage}</div>'
            f'<div style="font-size:14px;font-weight:700;color:{COLORS["text"]}">{count}</div>'
            f'</div>'
        )
    return f"""
    <div style="margin:8px 0 24px">
        <div style="display:flex;gap:2px;border-radius:3px;overflow:hidden">{segments}</div>
        <div style="display:flex;gap:2px">{labels}</div>
    </div>
    """


def activity_item(ev: AgentEvent, sim_start_date: str | None = None) -> str:
    color = (
        COLORS["success"] if ev.severity == "success"
        else (COLORS["warning"] if ev.severity == "warning" else COLORS["text_muted"])
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
    <div style="display:flex;gap:12px;padding:12px 0;border-bottom:1px solid {COLORS["border"]}">
        <div style="width:6px;height:6px;border-radius:50%;background:{color};margin-top:7px;flex-shrink:0"></div>
        <div style="flex:1;min-width:0">
            <div style="font-size:14px;color:{COLORS["text"]};line-height:1.45">{ev.description}</div>
        </div>
        <div style="font-size:13px;color:{COLORS["text_muted"]};white-space:nowrap">{rel}</div>
    </div>
    """


def budget_bar(total: float, spent: float, committed: float) -> str:
    """Horizontal stacked bar showing budget allocation."""
    remaining = max(0, total - spent - committed)
    pct_spent = spent / total * 100 if total else 0
    pct_committed = committed / total * 100 if total else 0
    pct_remaining = remaining / total * 100 if total else 0
    return f"""
    <div style="margin:8px 0 16px">
        <div style="display:flex;gap:2px;border-radius:4px;overflow:hidden;height:10px">
            <div style="flex:{pct_spent};background:{COLORS["accent"]};height:100%" title="Spent: ${spent:,.0f}"></div>
            <div style="flex:{pct_committed};background:{COLORS["warning"]};height:100%" title="Committed: ${committed:,.0f}"></div>
            <div style="flex:{pct_remaining};background:{COLORS["border"]};height:100%" title="Remaining: ${remaining:,.0f}"></div>
        </div>
        <div style="display:flex;justify-content:space-between;margin-top:6px;font-size:12px;color:{COLORS["text_muted"]}">
            <span><span style="display:inline-block;width:8px;height:8px;border-radius:2px;background:{COLORS["accent"]};margin-right:4px"></span>Spent ${spent:,.0f}</span>
            <span><span style="display:inline-block;width:8px;height:8px;border-radius:2px;background:{COLORS["warning"]};margin-right:4px"></span>Committed ${committed:,.0f}</span>
            <span><span style="display:inline-block;width:8px;height:8px;border-radius:2px;background:{COLORS["border"]};margin-right:4px"></span>Remaining ${remaining:,.0f}</span>
        </div>
    </div>
    """


def day_counter_html(day: int, start_date: str) -> str:
    """Styled day counter with calendar date."""
    base = datetime.strptime(start_date, "%Y-%m-%d")
    calendar_date = (base + timedelta(days=day)).strftime("%b %d, %Y")
    return f"""
    <div style="background:{COLORS["surface"]};border:1px solid {COLORS["border"]};
        border-radius:10px;padding:16px;margin-bottom:16px;display:flex;align-items:center;gap:16px">
        <div>
            <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;
                color:{COLORS["text_muted"]}">Simulation Day</div>
            <div style="font-size:28px;font-weight:800;color:{COLORS["accent"]};letter-spacing:-0.02em">{day}</div>
        </div>
        <div style="width:1px;height:36px;background:{COLORS["border"]}"></div>
        <div>
            <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;
                color:{COLORS["text_muted"]}">Calendar Date</div>
            <div style="font-size:16px;font-weight:600;color:{COLORS["text"]}">{calendar_date}</div>
        </div>
    </div>
    """


def progress_bar_html(current: int, target: int) -> str:
    pct = min(100, current / target * 100) if target else 0
    return f"""
    <div style="margin:8px 0 24px">
        <div style="display:flex;justify-content:space-between;margin-bottom:6px">
            <span style="font-size:14px;font-weight:600;color:{COLORS["text"]}">{current} of {target} onboarded</span>
            <span style="font-size:14px;font-weight:700;color:{COLORS["accent"]}">{pct:.0f}%</span>
        </div>
        <div style="background:{COLORS["border"]};border-radius:4px;height:8px;overflow:hidden">
            <div style="width:{pct}%;height:100%;background:{COLORS["accent"]};border-radius:4px;transition:width 0.3s"></div>
        </div>
    </div>
    """


def chat_bubble(content: str, sender: str, name: str, timestamp: str) -> str:
    is_agent = sender == "agent"
    if is_agent:
        bg, text_c, align, radius = COLORS["accent"], "#FFFFFF", "flex-end", "14px 14px 4px 14px"
        label_c = "rgba(255,255,255,0.65)"
    else:
        bg, text_c, align, radius = COLORS["surface"], COLORS["text"], "flex-start", "14px 14px 14px 4px"
        label_c = COLORS["text_muted"]
    label = "Agent" if is_agent else name
    return f"""
    <div style="display:flex;justify-content:{align};margin-bottom:10px">
        <div style="max-width:75%;background:{bg};color:{text_c};padding:12px 16px;border-radius:{radius};
            border:{'none' if is_agent else f'1px solid {COLORS["border"]}'}">
            <div style="font-size:12px;color:{label_c};margin-bottom:3px">{label} · {timestamp[5:16]}</div>
            <div style="font-size:14px;line-height:1.55">{content}</div>
        </div>
    </div>
    """
