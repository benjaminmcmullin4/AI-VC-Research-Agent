"""Shared HTML component builders for the Influx UI."""

from __future__ import annotations

from config import COLORS, PIPELINE_STAGES, PLATFORM_COLORS, STAGE_COLORS
from schema import AgentEvent, Influencer


def fmt_followers(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}K"
    return str(n)


def metric_card(label: str, value: str, delta: str = "", icon: str = "") -> str:
    icon_html = f'<span style="font-size:1.3rem;margin-right:6px">{icon}</span>' if icon else ""
    delta_html = (
        f'<div style="color:{COLORS["success"]};font-size:0.78rem;margin-top:4px">{delta}</div>'
        if delta else ""
    )
    return f"""
    <div class="metric-card">
        <h4>{icon_html}{label}</h4>
        <div class="value">{value}</div>
        {delta_html}
    </div>
    """


def section_title(text: str, subtitle: str = "") -> str:
    sub = (
        f'<div style="font-size:13px;color:{COLORS["text_secondary"]};margin-top:4px">{subtitle}</div>'
        if subtitle else ""
    )
    return f"""
    <div style="margin-bottom:20px;margin-top:8px">
        <div style="font-size:20px;font-weight:700;color:{COLORS["text"]}">{text}</div>
        {sub}
        <div style="width:40px;height:3px;background:{COLORS["primary"]};border-radius:2px;margin-top:8px"></div>
    </div>
    """


def status_badge(status: str) -> str:
    color = STAGE_COLORS.get(status, COLORS["text_muted"])
    return (
        f'<span style="background:{color}20;color:{color};padding:3px 10px;'
        f'border-radius:6px;font-size:11px;font-weight:600;letter-spacing:0.02em">{status}</span>'
    )


def platform_badge(platform: str) -> str:
    color = PLATFORM_COLORS.get(platform, COLORS["text_muted"])
    bg = f"{color}18" if platform != "TikTok" else f"{COLORS['surface_hover']}"
    return (
        f'<span style="background:{bg};color:{color};padding:3px 10px;'
        f'border-radius:6px;font-size:11px;font-weight:600">{platform}</span>'
    )


def niche_badge(niche: str) -> str:
    return (
        f'<span style="background:{COLORS["surface_hover"]};color:{COLORS["text_secondary"]};'
        f'padding:3px 10px;border-radius:6px;font-size:11px;font-weight:500">{niche}</span>'
    )


def influencer_card(inf: Influencer) -> str:
    score = int(0.6 * inf.audience_fit_score + 0.4 * inf.brand_fit_score)
    initials = "".join(w[0] for w in inf.name.split()[:2]).upper()

    partnerships_html = ""
    if inf.past_partnerships:
        tags = "".join(
            f'<span style="background:{COLORS["surface_hover"]};color:{COLORS["text_secondary"]};'
            f'padding:2px 8px;border-radius:4px;font-size:10px;margin-right:4px">{p}</span>'
            for p in inf.past_partnerships[:4]
        )
        partnerships_html = f'<div style="margin-top:10px;display:flex;flex-wrap:wrap;gap:4px">{tags}</div>'

    return f"""
    <div class="influencer-card">
        <div style="display:flex;gap:14px;align-items:flex-start">
            <div style="width:48px;height:48px;border-radius:12px;background:linear-gradient(135deg,{COLORS["primary"]},{COLORS["secondary"]});
                display:flex;align-items:center;justify-content:center;font-weight:700;font-size:16px;color:white;flex-shrink:0">{initials}</div>
            <div style="flex:1;min-width:0">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <div>
                        <span style="font-weight:700;font-size:16px;color:{COLORS["text"]}">{inf.name}</span>
                        <span style="color:{COLORS["text_muted"]};font-size:13px;margin-left:8px">{inf.handle}</span>
                    </div>
                    <div style="background:{COLORS["primary"]}25;color:{COLORS["primary"]};padding:4px 12px;
                        border-radius:8px;font-size:12px;font-weight:700">Score {score}</div>
                </div>
                <div style="display:flex;gap:6px;margin-top:6px">
                    {platform_badge(inf.platform)}
                    {niche_badge(inf.niche)}
                </div>
                <div style="font-size:13px;color:{COLORS["text_secondary"]};margin-top:8px;line-height:1.5">{inf.bio}</div>
            </div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:8px;margin-top:14px;
            background:{COLORS["bg"]};border-radius:8px;padding:12px">
            <div style="text-align:center">
                <div style="font-size:11px;color:{COLORS["text_muted"]};text-transform:uppercase;letter-spacing:0.05em">Followers</div>
                <div style="font-size:16px;font-weight:700;color:{COLORS["text"]};margin-top:2px">{fmt_followers(inf.followers)}</div>
            </div>
            <div style="text-align:center">
                <div style="font-size:11px;color:{COLORS["text_muted"]};text-transform:uppercase;letter-spacing:0.05em">Engagement</div>
                <div style="font-size:16px;font-weight:700;color:{COLORS["text"]};margin-top:2px">{inf.engagement_rate}%</div>
            </div>
            <div style="text-align:center">
                <div style="font-size:11px;color:{COLORS["text_muted"]};text-transform:uppercase;letter-spacing:0.05em">Aud. Fit</div>
                <div style="font-size:16px;font-weight:700;color:{COLORS["success"]};margin-top:2px">{inf.audience_fit_score}</div>
            </div>
            <div style="text-align:center">
                <div style="font-size:11px;color:{COLORS["text_muted"]};text-transform:uppercase;letter-spacing:0.05em">Est. Cost</div>
                <div style="font-size:16px;font-weight:700;color:{COLORS["text"]};margin-top:2px">${inf.estimated_cost:,}</div>
            </div>
        </div>
        {partnerships_html}
    </div>
    """


def chat_bubble(content: str, sender: str, name: str, timestamp: str) -> str:
    is_agent = sender == "agent"
    align = "flex-end" if is_agent else "flex-start"
    bg = COLORS["primary"] if is_agent else COLORS["surface_hover"]
    text_color = "white" if is_agent else COLORS["text"]
    label = "Agent" if is_agent else name
    radius = "14px 14px 4px 14px" if is_agent else "14px 14px 14px 4px"
    label_color = "rgba(255,255,255,0.6)" if is_agent else COLORS["text_muted"]

    return f"""
    <div style="display:flex;justify-content:{align};margin-bottom:10px">
        <div style="max-width:78%;background:{bg};color:{text_color};padding:12px 16px;border-radius:{radius}">
            <div style="font-size:11px;color:{label_color};margin-bottom:4px;font-weight:500">{label} · {timestamp[5:16]}</div>
            <div style="font-size:14px;line-height:1.55">{content}</div>
        </div>
    </div>
    """


def pipeline_bar(counts: dict) -> str:
    total = sum(counts.values())
    if total == 0:
        return ""
    segments = ""
    labels = ""
    for stage in PIPELINE_STAGES:
        count = counts.get(stage, 0)
        pct = max(count / total * 100, 0)
        color = STAGE_COLORS.get(stage, COLORS["text_muted"])
        segments += (
            f'<div style="flex:{pct};background:{color};height:8px;min-width:{2 if count else 0}px" '
            f'title="{stage}: {count}"></div>'
        )
        if count > 0:
            labels += (
                f'<div style="text-align:center;flex:{pct};min-width:0">'
                f'<div style="font-size:10px;color:{color};margin-top:6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{stage}</div>'
                f'<div style="font-size:13px;font-weight:700;color:{COLORS["text"]}">{count}</div>'
                f'</div>'
            )

    return f"""
    <div style="margin:16px 0">
        <div style="display:flex;gap:2px;border-radius:4px;overflow:hidden">{segments}</div>
        <div style="display:flex;gap:2px;margin-top:2px">{labels}</div>
    </div>
    """


def activity_item(ev: AgentEvent) -> str:
    icons = {
        "discovery": "🔍", "qualification": "⭐", "outreach": "📤",
        "reply_detected": "💬", "negotiation": "🤝", "content_posted": "📸",
        "conversion": "💰", "insight": "📊", "alert": "⚠️",
    }
    icon = icons.get(ev.event_type, "📌")
    accent = (
        COLORS["success"] if ev.severity == "success"
        else (COLORS["warning"] if ev.severity == "warning" else COLORS["text_muted"])
    )

    ts_day = ev.timestamp[:10]
    ts_time = ev.timestamp[11:16]
    if ts_day == "2026-04-06":
        rel_ts = f"Today {ts_time}"
    elif ts_day == "2026-04-05":
        rel_ts = f"Yesterday {ts_time}"
    else:
        rel_ts = f"{ts_day[5:]} {ts_time}"

    detail_html = (
        f'<div style="font-size:12px;color:{COLORS["text_muted"]};margin-top:2px">{ev.detail}</div>'
        if ev.detail else ""
    )

    return f"""
    <div style="display:flex;gap:12px;padding:10px 14px;background:{COLORS["surface"]};
        border-radius:8px;margin-bottom:6px;border-left:3px solid {accent}">
        <span style="font-size:1.1rem;flex-shrink:0">{icon}</span>
        <div style="flex:1;min-width:0">
            <div style="font-size:13px;color:{COLORS["text"]};line-height:1.4">{ev.description}</div>
            {detail_html}
        </div>
        <div style="font-size:11px;color:{COLORS["text_muted"]};white-space:nowrap">{rel_ts}</div>
    </div>
    """
