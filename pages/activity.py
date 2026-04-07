"""Agent Activity Feed page."""

from __future__ import annotations

from collections import Counter

import streamlit as st

from schema import AgentEvent

_EVENT_ICONS = {
    "discovery": "🔍", "qualification": "⭐", "outreach": "📤",
    "reply_detected": "💬", "negotiation": "🤝", "content_posted": "📸",
    "conversion": "💰", "insight": "📊", "alert": "⚠️",
}

_EVENT_COLORS = {
    "discovery": "#60A5FA", "qualification": "#A78BFA", "outreach": "#1ABC9C",
    "reply_detected": "#34D399", "negotiation": "#F97316", "content_posted": "#F472B6",
    "conversion": "#1ABC9C", "insight": "#94A3B8", "alert": "#FBBF24",
}

_EVENT_LABELS = {
    "discovery": "Discovery", "qualification": "Qualification", "outreach": "Outreach",
    "reply_detected": "Reply Detected", "negotiation": "Negotiation",
    "content_posted": "Content Posted", "conversion": "Conversion",
    "insight": "Insight", "alert": "Alert",
}


def render_activity(data: dict):
    st.markdown('<div class="section-header">Agent Activity</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#777;font-size:0.88rem;margin-bottom:1.2rem">Real-time feed of autonomous agent actions and observations.</div>', unsafe_allow_html=True)

    events: list[AgentEvent] = data["activity_feed"]

    # ── Summary stats ────────────────────────────────────────────────────
    today_events = [e for e in events if e.timestamp.startswith("2026-04-06")]
    week_events = [e for e in events if e.timestamp >= "2026-03-30"]
    type_counts = Counter(e.event_type for e in events)
    most_common_type = type_counts.most_common(1)[0] if type_counts else ("", 0)

    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.markdown(f"""<div class="metric-card"><h4>Events Today</h4><div class="value">{len(today_events)}</div></div>""", unsafe_allow_html=True)
    sc2.markdown(f"""<div class="metric-card"><h4>Events This Week</h4><div class="value">{len(week_events)}</div></div>""", unsafe_allow_html=True)
    sc3.markdown(f"""<div class="metric-card"><h4>Total Events</h4><div class="value">{len(events)}</div></div>""", unsafe_allow_html=True)
    sc4.markdown(f"""<div class="metric-card"><h4>Most Active Type</h4><div class="value" style="font-size:1.1rem">{_EVENT_LABELS.get(most_common_type[0], most_common_type[0])}</div></div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    # ── Filters ──────────────────────────────────────────────────────────
    fc1, fc2 = st.columns(2)
    with fc1:
        all_types = sorted(set(e.event_type for e in events))
        sel_types = st.multiselect(
            "Event Type", all_types,
            format_func=lambda t: f"{_EVENT_ICONS.get(t, '')} {_EVENT_LABELS.get(t, t)}",
            default=[], key="act_types",
        )
    with fc2:
        date_range = st.selectbox("Date Range", ["Last 7 days", "Last 14 days", "Last 30 days"], index=2, key="act_range")

    cutoff = {"Last 7 days": "2026-03-30", "Last 14 days": "2026-03-23", "Last 30 days": "2026-03-07"}
    min_date = cutoff.get(date_range, "2026-03-07")

    filtered = events
    if sel_types:
        filtered = [e for e in filtered if e.event_type in sel_types]
    filtered = [e for e in filtered if e.timestamp >= min_date]

    st.markdown(f"<div style='color:#777;font-size:0.82rem;margin-bottom:12px'>Showing {len(filtered)} events</div>", unsafe_allow_html=True)

    # ── Feed ─────────────────────────────────────────────────────────────
    for ev in filtered:
        icon = _EVENT_ICONS.get(ev.event_type, "📌")
        color = _EVENT_COLORS.get(ev.event_type, "#777")
        sev_bg = "#ECFDF5" if ev.severity == "success" else ("#FFFBEB" if ev.severity == "warning" else "white")

        # Relative timestamp
        ts_day = ev.timestamp[:10]
        ts_time = ev.timestamp[11:16]
        if ts_day == "2026-04-06":
            rel_ts = f"Today {ts_time}"
        elif ts_day == "2026-04-05":
            rel_ts = f"Yesterday {ts_time}"
        else:
            rel_ts = f"{ts_day[5:]} {ts_time}"

        st.markdown(f"""
        <div style="display:flex;gap:12px;padding:12px;background:{sev_bg};border-left:3px solid {color};border-radius:0 8px 8px 0;margin-bottom:6px">
            <div style="font-size:1.2rem;min-width:28px;text-align:center">{icon}</div>
            <div style="flex:1">
                <div style="font-size:0.88rem;color:#1A1A1A;line-height:1.4">{ev.description}</div>
                {"<div style='font-size:0.78rem;color:#777;margin-top:3px'>" + ev.detail + "</div>" if ev.detail else ""}
            </div>
            <div style="font-size:0.72rem;color:#999;white-space:nowrap;min-width:90px;text-align:right">{rel_ts}</div>
        </div>
        """, unsafe_allow_html=True)
