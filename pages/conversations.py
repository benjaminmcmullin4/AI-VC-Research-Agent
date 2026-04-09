"""Conversations — outreach inbox."""

from __future__ import annotations

import streamlit as st

from components import chat_bubble, page_header, section_label
from config import COLORS, SHADOWS, RADIUS, STAGE_COLORS
from schema import OutreachThread


def _status_badge(status: str) -> str:
    color_map = {
        "Awaiting Reply": ("#94A3B8", "#F1F5F9"),
        "Follow-up Sent": ("#8B5CF6", "#F5F3FF"),
        "Interested":     ("#10B981", "#ECFDF5"),
        "Questions":      ("#F59E0B", "#FFFBEB"),
        "Negotiating":    ("#F97316", "#FFF7ED"),
        "Signed":         ("#4F46E5", "#EEF2FF"),
        "Declined":       ("#EF4444", "#FEF2F2"),
    }
    fg, bg = color_map.get(status, ("#94A3B8", "#F1F5F9"))
    return (
        f'<span style="display:inline-flex;align-items:center;gap:5px;font-size:12px;font-weight:600;'
        f'color:{fg};background:{bg};padding:3px 10px;border-radius:20px">'
        f'<span style="width:6px;height:6px;border-radius:50%;background:{fg}"></span>{status}</span>'
    )


def render_conversations(data: dict, api_key: str | None):
    st.markdown(page_header("Conversations"), unsafe_allow_html=True)

    all_threads: list[OutreachThread] = list(data["conversations"])

    if not all_threads:
        st.info("No conversations yet. Advance the simulation from the sidebar to generate outreach.")
        return

    # Status filter
    statuses = sorted(set(t.status for t in all_threads))
    sel_status = st.multiselect("Filter by status", statuses, default=[], key="conv_status_filter")
    if sel_status:
        all_threads = [t for t in all_threads if t.status in sel_status]

    st.markdown(f'<div style="font-size:14px;color:{COLORS["text_sec"]};margin-bottom:24px">{len(all_threads)} AI-powered outreach threads</div>', unsafe_allow_html=True)

    if not all_threads:
        st.info("No conversations match the selected filters.")
        return

    col_list, col_detail = st.columns([1, 2])

    with col_list:
        labels = [f"{t.influencer_name}" for t in all_threads]
        selected_idx = st.radio("Threads", range(len(labels)), format_func=lambda i: labels[i], key="conv_sel", label_visibility="collapsed")

    with col_detail:
        thread = all_threads[selected_idx]

        # Header
        st.markdown(f"""
        <div style="margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid {COLORS["border_light"]}">
            <div style="font-size:20px;font-weight:700;color:{COLORS["text"]};letter-spacing:-0.015em">{thread.influencer_name}
                <span style="font-weight:400;color:{COLORS["text_muted"]};font-size:14px;margin-left:8px">{thread.influencer_handle}</span>
            </div>
            <div style="font-size:13px;color:{COLORS["text_sec"]};margin-top:8px;display:flex;align-items:center;gap:8px">
                <span>{thread.platform}</span>
                {_status_badge(thread.status)}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Messages
        for msg in thread.messages:
            name = thread.influencer_name.split()[0]
            st.markdown(chat_bubble(msg.content, msg.sender, name, msg.timestamp), unsafe_allow_html=True)

        # Metadata
        deal_str = f"${thread.deal_value:,.0f}" if thread.deal_value else "TBD"
        next_action = thread.next_action or _infer_next_action(thread.status)
        st.markdown(f"""
        <div class="influx-card" style="background:{COLORS["surface"]};
            border-radius:{RADIUS["md"]};padding:18px 20px;margin-top:20px;
            font-size:13px;color:{COLORS["text_sec"]};box-shadow:{SHADOWS["xs"]}">
            <div style="display:flex;gap:28px;flex-wrap:wrap">
                <span style="display:flex;align-items:center;gap:6px">
                    <i class="bi bi-diagram-3" style="color:{COLORS["text_muted"]}"></i>
                    Stage: <strong style="color:{COLORS["text"]}">{thread.current_stage}</strong>
                </span>
                <span style="display:flex;align-items:center;gap:6px">
                    <i class="bi bi-currency-dollar" style="color:{COLORS["text_muted"]}"></i>
                    Deal: <strong style="color:{COLORS["text"]}">{deal_str}</strong>
                </span>
                <span style="display:flex;align-items:center;gap:6px">
                    <i class="bi bi-arrow-right-circle" style="color:{COLORS["text_muted"]}"></i>
                    Next: <strong style="color:{COLORS["text"]}">{next_action}</strong>
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # AI draft button
        if api_key:
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            if st.button("Draft AI Reply", key=f"ai_{selected_idx}"):
                from ai_engine import generate_outreach_draft
                draft = generate_outreach_draft(api_key, {"name": thread.influencer_name, "handle": thread.influencer_handle, "platform": thread.platform})
                if draft:
                    st.session_state["conv_draft"] = draft

        if "conv_draft" in st.session_state:
            d = st.session_state["conv_draft"]
            st.markdown(f"""
            <div class="influx-card" style="background:{COLORS["accent_light"]};
                border-left:3px solid {COLORS["accent"]};border-radius:{RADIUS["md"]};
                padding:16px 20px;margin-top:12px;box-shadow:{SHADOWS["xs"]}">
                <div style="font-size:12px;font-weight:600;color:{COLORS["accent"]};text-transform:uppercase;
                    letter-spacing:0.04em;margin-bottom:8px">AI Draft</div>
                <div style="font-size:14px;color:{COLORS["text"]};line-height:1.6">{d.body}</div>
            </div>
            """, unsafe_allow_html=True)


def _infer_next_action(status: str) -> str:
    """Infer next action from conversation status."""
    actions = {
        "Awaiting Reply": "Waiting for influencer response",
        "Follow-up Sent": "Waiting for response to follow-up",
        "Interested": "Move to negotiation",
        "Questions": "Address influencer questions",
        "Negotiating": "Finalize deal terms",
        "Signed": "Content production in progress",
        "Declined": "Closed — no further action",
    }
    return actions.get(status, "Review")
