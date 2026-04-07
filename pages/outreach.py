"""Outreach / Conversations page — CRM-style inbox."""

from __future__ import annotations

import streamlit as st

from config import STAGE_COLORS
from schema import OutreachThread


def _status_color(status: str) -> str:
    mapping = {
        "Awaiting Reply": "#94A3B8", "Follow-up Sent": "#A78BFA",
        "Interested": "#34D399", "Questions": "#FBBF24",
        "Negotiating": "#F97316", "Signed": "#1ABC9C",
        "Declined": "#E74C3C",
    }
    return mapping.get(status, "#777")


def _thread_preview(thread: OutreachThread, is_selected: bool) -> str:
    color = _status_color(thread.status)
    bg = "#F0F4F8" if is_selected else "white"
    last_msg = thread.messages[-1].content[:80] + "..." if thread.messages else ""
    last_ts = thread.messages[-1].timestamp[5:16] if thread.messages else ""
    return f"""
    <div style="background:{bg};padding:10px 12px;border-left:3px solid {color};margin-bottom:4px;border-radius:0 6px 6px 0;cursor:pointer">
        <div style="display:flex;justify-content:space-between;align-items:center">
            <div style="font-weight:600;font-size:0.88rem">{thread.influencer_name}</div>
            <span style="background:{color}22;color:{color};padding:1px 6px;border-radius:8px;font-size:0.65rem;font-weight:500">{thread.status}</span>
        </div>
        <div style="font-size:0.75rem;color:#777;margin-top:2px">{thread.platform} &middot; {last_ts}</div>
        <div style="font-size:0.78rem;color:#999;margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{last_msg}</div>
    </div>
    """


def render_outreach(data: dict, api_key: str | None):
    st.markdown('<div class="section-header">Outreach &amp; Conversations</div>', unsafe_allow_html=True)

    conversations: list[OutreachThread] = data["conversations"]

    # ── Filters ──────────────────────────────────────────────────────────
    fc1, fc2 = st.columns([1, 2])
    with fc1:
        statuses = sorted(set(t.status for t in conversations))
        sel_status = st.multiselect("Filter by Status", statuses, default=[], key="out_status")
    with fc2:
        search = st.text_input("Search by name", key="out_search")

    filtered = conversations
    if sel_status:
        filtered = [t for t in filtered if t.status in sel_status]
    if search:
        filtered = [t for t in filtered if search.lower() in t.influencer_name.lower()]

    if not filtered:
        st.info("No conversations match the current filters.")
        return

    # ── Layout: thread list + detail ─────────────────────────────────────
    col_list, col_detail = st.columns([1, 2])

    with col_list:
        thread_names = [f"{t.influencer_name} ({t.influencer_handle})" for t in filtered]
        selected_idx = st.radio(
            "Conversations", range(len(thread_names)),
            format_func=lambda i: thread_names[i],
            key="out_thread_sel", label_visibility="collapsed",
        )

    with col_detail:
        thread = filtered[selected_idx]
        color = _status_color(thread.status)

        # Header
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;padding-bottom:10px;border-bottom:2px solid #ECF0F1">
            <div>
                <span style="font-size:1.1rem;font-weight:700">{thread.influencer_name}</span>
                <span style="color:#777;margin-left:8px">{thread.influencer_handle}</span>
            </div>
            <div style="display:flex;gap:8px;align-items:center">
                <span style="background:{color}22;color:{color};border:1px solid {color};padding:2px 10px;border-radius:12px;font-size:0.75rem;font-weight:500">{thread.status}</span>
                <span style="font-size:0.75rem;color:#777">{thread.platform}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Messages
        for msg in thread.messages:
            is_agent = msg.sender == "agent"
            align = "flex-end" if is_agent else "flex-start"
            bg = "#0A0A0A" if is_agent else "#F0F4F8"
            text_color = "white" if is_agent else "#1A1A1A"
            label = "Agent" if is_agent else thread.influencer_name.split()[0]
            radius = "16px 16px 4px 16px" if is_agent else "16px 16px 16px 4px"

            st.markdown(f"""
            <div style="display:flex;justify-content:{align};margin-bottom:12px">
                <div style="max-width:80%;background:{bg};color:{text_color};padding:12px 16px;border-radius:{radius}">
                    <div style="font-size:0.7rem;color:{'#888' if is_agent else '#999'};margin-bottom:4px">{label} &middot; {msg.timestamp[5:16]}</div>
                    <div style="font-size:0.86rem;line-height:1.55">{msg.content}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Thread metadata
        st.markdown(f"""
        <div style="background:#F8FAFC;border:1px solid #ECF0F1;border-radius:8px;padding:12px;margin-top:16px">
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;font-size:0.82rem">
                <div><span style="color:#777">Stage:</span> {thread.current_stage}</div>
                <div><span style="color:#777">Assigned:</span> {thread.assigned_to}</div>
                <div><span style="color:#777">Deal Value:</span> {"${:,.0f}".format(thread.deal_value) if thread.deal_value else "TBD"}</div>
            </div>
            <div style="font-size:0.82rem;margin-top:8px"><span style="color:#777">Next Action:</span> <strong>{thread.next_action}</strong></div>
        </div>
        """, unsafe_allow_html=True)

        # Draft reply button
        if api_key:
            if st.button("Draft AI Reply", key="out_draft_btn"):
                from ai_engine import generate_outreach_draft
                inf_data = {"name": thread.influencer_name, "handle": thread.influencer_handle, "platform": thread.platform}
                draft = generate_outreach_draft(api_key, inf_data)
                if draft:
                    st.session_state["out_draft"] = draft

        if "out_draft" in st.session_state:
            d = st.session_state["out_draft"]
            st.markdown(f"""
            <div style="background:#1ABC9C11;border:1px solid #1ABC9C;border-radius:8px;padding:12px;margin-top:12px">
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.05em;color:#1ABC9C;margin-bottom:6px">AI-Generated Draft</div>
                <div style="font-size:0.86rem;color:#333;line-height:1.55">{d.body}</div>
            </div>
            """, unsafe_allow_html=True)
