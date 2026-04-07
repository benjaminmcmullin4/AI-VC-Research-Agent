"""Find & Reach Out page — search, discover top 3, send outreach."""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from components import influencer_card, section_title
from config import COLORS, NICHES, PLATFORMS
from data.mock_data import get_top_recommended
from schema import Influencer, OutreachMessage, OutreachThread


def render_find(data: dict, api_key: str | None):
    st.markdown(section_title("Find Your Next Creator", "Search or filter to discover your top matches"), unsafe_allow_html=True)

    # ── Filters ──────────────────────────────────────────────────────────
    search_query = st.text_input("Describe your ideal influencer...", key="find_search", placeholder="e.g. fitness creator on Instagram with high engagement")

    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        sel_platforms = st.multiselect("Platform", PLATFORMS, default=[], key="find_plat")
    with fc2:
        sel_niches = st.multiselect("Niche", NICHES, default=[], key="find_niche")
    with fc3:
        min_followers = st.slider("Min Followers", 0, 3_000_000, 0, step=10_000, format="%d", key="find_fol")
    with fc4:
        min_engagement = st.slider("Min Engagement %", 0.0, 8.0, 0.0, step=0.5, key="find_eng")

    # ── Find button ──────────────────────────────────────────────────────
    if st.button("⚡  Find Top 3", key="find_btn", use_container_width=True):
        candidates = [
            i for i in data["influencers"]
            if i.status in ("Discovered", "Qualified")
        ]

        # Apply filters
        if sel_platforms:
            candidates = [i for i in candidates if i.platform in sel_platforms]
        if sel_niches:
            candidates = [i for i in candidates if i.niche in sel_niches]
        if min_followers > 0:
            candidates = [i for i in candidates if i.followers >= min_followers]
        if min_engagement > 0:
            candidates = [i for i in candidates if i.engagement_rate >= min_engagement]

        # Search query matching
        if search_query:
            q = search_query.lower()
            candidates = [
                i for i in candidates
                if q in i.bio.lower() or q in i.niche.lower() or q in i.platform.lower()
                or q in i.name.lower() or q in i.handle.lower()
                or any(q in p.lower() for p in i.past_partnerships)
            ]

        # Score and take top 3
        candidates.sort(
            key=lambda i: 0.6 * i.audience_fit_score + 0.4 * i.brand_fit_score,
            reverse=True,
        )
        st.session_state["find_results"] = candidates[:3]
        # Clear previous outreach state
        st.session_state.pop("reaching_out_to", None)
        st.session_state.pop("outreach_draft_text", None)

    # ── Results ──────────────────────────────────────────────────────────
    results: list[Influencer] = st.session_state.get("find_results", [])

    if not results:
        # Show default top 3 on first load
        if "find_results" not in st.session_state:
            top = get_top_recommended(data, n=3)
            st.markdown(f"""
            <div style="font-size:13px;color:{COLORS["text_muted"]};margin:16px 0 8px">
                Showing top 3 recommended influencers. Use filters and click <strong>Find Top 3</strong> to search.
            </div>
            """, unsafe_allow_html=True)
            results = top
        else:
            st.markdown(f"""
            <div style="background:{COLORS["surface"]};border:1px solid {COLORS["border"]};border-radius:12px;
                padding:40px;text-align:center;margin-top:20px">
                <div style="font-size:28px;margin-bottom:8px">🔍</div>
                <div style="font-size:16px;font-weight:600;color:{COLORS["text"]}">No matches found</div>
                <div style="font-size:13px;color:{COLORS["text_muted"]};margin-top:4px">Try adjusting your filters or search query</div>
            </div>
            """, unsafe_allow_html=True)
            return

    st.markdown(f"""
    <div style="font-size:12px;text-transform:uppercase;letter-spacing:0.08em;
        color:{COLORS["primary"]};font-weight:600;margin:20px 0 12px">Top {len(results)} Match{'es' if len(results) != 1 else ''}</div>
    """, unsafe_allow_html=True)

    # Render cards + reach out buttons
    cols = st.columns(len(results))
    for idx, (col, inf) in enumerate(zip(cols, results)):
        with col:
            st.markdown(influencer_card(inf), unsafe_allow_html=True)

            # Blurb
            if inf.recommendation_blurb:
                st.markdown(f"""
                <div style="background:{COLORS["bg"]};border:1px solid {COLORS["border"]};
                    border-radius:8px;padding:12px;margin:-4px 0 8px;font-size:13px;
                    color:{COLORS["text_secondary"]};line-height:1.5">
                    {inf.recommendation_blurb}
                </div>
                """, unsafe_allow_html=True)

            if st.button(f"📨  Reach Out to {inf.name.split()[0]}", key=f"reach_{idx}", use_container_width=True):
                st.session_state["reaching_out_to"] = inf.handle
                st.session_state["reaching_out_inf"] = inf
                # Generate draft
                if api_key:
                    from ai_engine import generate_outreach_draft
                    draft = generate_outreach_draft(api_key, inf.model_dump())
                    if draft:
                        st.session_state["outreach_draft_text"] = draft.body
                if "outreach_draft_text" not in st.session_state:
                    st.session_state["outreach_draft_text"] = (
                        f"Hi {inf.name.split()[0]}! We've been following your {inf.niche.lower()} content on "
                        f"{inf.platform} and love what you're building with {inf.handle}. "
                        f"We're working on a campaign that we think would be a perfect fit for your audience. "
                        f"Would you be open to a quick chat about a potential collaboration?"
                    )

    # ── Outreach composer ────────────────────────────────────────────────
    if "reaching_out_to" in st.session_state:
        inf = st.session_state.get("reaching_out_inf")
        if inf:
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background:{COLORS["surface"]};border:1px solid {COLORS["primary"]}40;
                border-radius:12px;padding:20px;border-left:4px solid {COLORS["primary"]}">
                <div style="font-size:12px;text-transform:uppercase;letter-spacing:0.08em;
                    color:{COLORS["primary"]};font-weight:600;margin-bottom:10px">
                    Composing message to {inf.name} ({inf.handle})
                </div>
            </div>
            """, unsafe_allow_html=True)

            msg_text = st.text_area(
                "Your message",
                value=st.session_state.get("outreach_draft_text", ""),
                height=140,
                key="outreach_msg_input",
                label_visibility="collapsed",
            )

            sc1, sc2 = st.columns([1, 4])
            with sc1:
                if st.button("📤  Send Message", key="send_msg"):
                    now = datetime.now().strftime("%Y-%m-%d %H:%M")
                    new_msg = OutreachMessage(
                        sender="agent", content=msg_text, timestamp=now, message_type="initial",
                    )
                    new_thread = OutreachThread(
                        influencer_handle=inf.handle,
                        influencer_name=inf.name,
                        platform=inf.platform,
                        status="Awaiting Reply",
                        messages=[new_msg],
                        current_stage="Contacted",
                        assigned_to="AI Agent",
                        next_action="Wait for reply",
                    )
                    threads = st.session_state.setdefault("new_threads", [])
                    threads.append(new_thread)

                    st.session_state.pop("reaching_out_to", None)
                    st.session_state.pop("reaching_out_inf", None)
                    st.session_state.pop("outreach_draft_text", None)
                    st.success(f"Message sent to {inf.handle}! Track it in **Outreach & Pipeline**.")
            with sc2:
                if st.button("Cancel", key="cancel_msg"):
                    st.session_state.pop("reaching_out_to", None)
                    st.session_state.pop("reaching_out_inf", None)
                    st.session_state.pop("outreach_draft_text", None)
                    st.rerun()
