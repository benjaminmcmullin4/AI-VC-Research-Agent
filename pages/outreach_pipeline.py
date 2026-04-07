"""Outreach & Pipeline page — inbox + kanban board."""

from __future__ import annotations

import streamlit as st

from components import (
    chat_bubble,
    pipeline_bar,
    platform_badge,
    section_title,
    status_badge,
)
from config import COLORS, PIPELINE_STAGES, STAGE_COLORS
from schema import Influencer, OutreachThread


def _status_color(status: str) -> str:
    mapping = {
        "Awaiting Reply": "#8B8D9E", "Follow-up Sent": "#A78BFA",
        "Interested": "#00D68F", "Questions": "#FFB800",
        "Negotiating": "#F97316", "Signed": "#6C5CE7", "Declined": "#FF4757",
    }
    return mapping.get(status, COLORS["text_muted"])


def render_outreach_pipeline(data: dict, metrics: dict, api_key: str | None):
    st.markdown(section_title("Outreach & Pipeline"), unsafe_allow_html=True)

    # Pipeline bar
    st.markdown(pipeline_bar(metrics["pipeline_counts"]), unsafe_allow_html=True)

    # Tabs
    tab_inbox, tab_pipeline = st.tabs(["Inbox", "Pipeline Board"])

    # ── Tab 1: Inbox ─────────────────────────────────────────────────────
    with tab_inbox:
        # Combine stored + new threads
        all_threads: list[OutreachThread] = list(data["conversations"]) + st.session_state.get("new_threads", [])

        # Check onboarded overrides
        onboarded = st.session_state.get("onboarded", set())

        if not all_threads:
            st.info("No outreach conversations yet. Go to **Find & Reach Out** to start.")
            return

        # Thread list + detail
        col_list, col_detail = st.columns([1, 2])

        with col_list:
            thread_labels = [
                f"{t.influencer_name} · {t.status}" for t in all_threads
            ]
            selected_idx = st.radio(
                "Conversations", range(len(thread_labels)),
                format_func=lambda i: thread_labels[i],
                key="inbox_sel", label_visibility="collapsed",
            )

        with col_detail:
            thread = all_threads[selected_idx]
            color = _status_color(thread.status)

            # Check if onboarded
            display_status = "Signed" if thread.influencer_handle in onboarded else thread.status

            # Header
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;
                padding-bottom:12px;border-bottom:1px solid {COLORS["border"]}">
                <div>
                    <span style="font-size:18px;font-weight:700;color:{COLORS["text"]}">{thread.influencer_name}</span>
                    <span style="color:{COLORS["text_muted"]};margin-left:8px;font-size:13px">{thread.influencer_handle}</span>
                </div>
                <div style="display:flex;gap:8px;align-items:center">
                    {status_badge(display_status)}
                    {platform_badge(thread.platform)}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Messages
            for msg in thread.messages:
                name = thread.influencer_name.split()[0]
                st.markdown(chat_bubble(msg.content, msg.sender, name, msg.timestamp), unsafe_allow_html=True)

            # Metadata
            deal_str = f"${thread.deal_value:,.0f}" if thread.deal_value else "TBD"
            st.markdown(f"""
            <div style="background:{COLORS["surface"]};border:1px solid {COLORS["border"]};
                border-radius:8px;padding:14px;margin-top:16px">
                <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;font-size:13px">
                    <div><span style="color:{COLORS["text_muted"]}">Stage:</span> <span style="color:{COLORS["text"]}">{thread.current_stage}</span></div>
                    <div><span style="color:{COLORS["text_muted"]}">Assigned:</span> <span style="color:{COLORS["text"]}">{thread.assigned_to}</span></div>
                    <div><span style="color:{COLORS["text_muted"]}">Deal Value:</span> <span style="color:{COLORS["text"]}">{deal_str}</span></div>
                </div>
                <div style="font-size:13px;margin-top:8px">
                    <span style="color:{COLORS["text_muted"]}">Next Action:</span>
                    <strong style="color:{COLORS["text"]}">{thread.next_action}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Action buttons
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            btn_cols = st.columns(3)

            # Onboard button for interested threads
            if thread.status in ("Interested", "Signed") and thread.influencer_handle not in onboarded:
                with btn_cols[0]:
                    if st.button("✅  Onboard Influencer", key=f"onboard_{selected_idx}"):
                        ob = st.session_state.setdefault("onboarded", set())
                        ob.add(thread.influencer_handle)
                        st.success(f"{thread.influencer_name} has been onboarded!")
                        st.rerun()

            if thread.influencer_handle in onboarded:
                st.markdown(f"""
                <div style="background:{COLORS["success"]}15;border:1px solid {COLORS["success"]}40;
                    border-radius:8px;padding:12px;text-align:center;margin-top:8px">
                    <span style="color:{COLORS["success"]};font-weight:600;font-size:14px">✅ Onboarded</span>
                </div>
                """, unsafe_allow_html=True)

            # AI reply
            if api_key:
                with btn_cols[1]:
                    if st.button("🤖  Draft AI Reply", key=f"ai_reply_{selected_idx}"):
                        from ai_engine import generate_outreach_draft
                        inf_data = {"name": thread.influencer_name, "handle": thread.influencer_handle, "platform": thread.platform}
                        draft = generate_outreach_draft(api_key, inf_data)
                        if draft:
                            st.session_state["inbox_draft"] = draft

            if "inbox_draft" in st.session_state:
                d = st.session_state["inbox_draft"]
                st.markdown(f"""
                <div style="background:{COLORS["primary"]}10;border:1px solid {COLORS["primary"]}40;
                    border-radius:8px;padding:14px;margin-top:12px;border-left:3px solid {COLORS["primary"]}">
                    <div style="font-size:11px;text-transform:uppercase;letter-spacing:0.06em;
                        color:{COLORS["primary"]};margin-bottom:6px;font-weight:600">AI-Generated Draft</div>
                    <div style="font-size:14px;color:{COLORS["text"]};line-height:1.55">{d.body}</div>
                </div>
                """, unsafe_allow_html=True)

    # ── Tab 2: Pipeline Board ────────────────────────────────────────────
    with tab_pipeline:
        influencers: list[Influencer] = data["influencers"]
        by_stage: dict[str, list[Influencer]] = {s: [] for s in PIPELINE_STAGES}
        for inf in influencers:
            if inf.status in by_stage:
                by_stage[inf.status].append(inf)

        # 2 rows of 4
        for row_start in (0, 4):
            row_stages = PIPELINE_STAGES[row_start:row_start + 4]
            cols = st.columns(4)
            for col, stage in zip(cols, row_stages):
                color = STAGE_COLORS[stage]
                items = by_stage[stage]
                with col:
                    st.markdown(f"""
                    <div style="background:{COLORS["surface"]};border:1px solid {COLORS["border"]};
                        border-top:3px solid {color};border-radius:10px;padding:12px;min-height:180px;margin-bottom:10px">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
                            <span style="font-weight:700;font-size:13px;color:{color}">{stage}</span>
                            <span style="background:{color}25;color:{color};padding:2px 8px;
                                border-radius:6px;font-size:11px;font-weight:700">{len(items)}</span>
                        </div>
                    """, unsafe_allow_html=True)

                    for inf in items:
                        st.markdown(f"""
                        <div style="background:{COLORS["bg"]};border:1px solid {COLORS["border"]};
                            border-radius:6px;padding:8px 10px;margin-bottom:4px;font-size:12px">
                            <div style="font-weight:600;color:{COLORS["text"]}">{inf.name}</div>
                            <div style="color:{COLORS["text_muted"]};font-size:11px">{inf.handle} · {inf.platform}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)
