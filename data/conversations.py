"""Outreach conversation mock data — 22 threads at various stages."""

from __future__ import annotations

from schema import OutreachMessage, OutreachThread


def _msg(sender, content, ts, mtype="initial"):
    return OutreachMessage(sender=sender, content=content, timestamp=ts, message_type=mtype)


def get_conversations() -> list[OutreachThread]:
    return [
        # ── Initial outreach sent, no reply yet (4) ──────────────────────
        OutreachThread(
            influencer_handle="@aabornefit", influencer_name="Aisha Rahman",
            platform="TikTok", status="Awaiting Reply", current_stage="Contacted",
            next_action="Send follow-up in 3 days",
            messages=[
                _msg("agent", "Hi Aisha! We've been following your yoga and mobility content -- your flows are incredible. We're working with VitaGlow Supplements on their Spring Wellness campaign and think your audience would love their plant-based recovery line. Would you be open to a quick chat about a potential collaboration?", "2026-03-28 10:15", "initial"),
            ],
        ),
        OutreachThread(
            influencer_handle="@jaketorresfit", influencer_name="Jake Torres",
            platform="Instagram", status="Awaiting Reply", current_stage="Contacted",
            next_action="Send follow-up in 2 days",
            messages=[
                _msg("agent", "Hey Jake! Your calisthenics content is next level -- especially the park workout series. We're putting together a fitness creator campaign and your bodyweight training expertise would be a perfect fit. Interested in learning more?", "2026-03-30 14:22", "initial"),
            ],
        ),
        OutreachThread(
            influencer_handle="@nathanstreetwear", influencer_name="Nathan Brooks",
            platform="Instagram", status="Awaiting Reply", current_stage="Contacted",
            next_action="Send follow-up in 4 days",
            messages=[
                _msg("agent", "Nathan, love your fit checks and drop coverage. We're working with a premium streetwear brand launching a new sneaker collab and think your audience is the exact right crowd. Want to hear the details?", "2026-03-31 09:45", "initial"),
            ],
        ),
        OutreachThread(
            influencer_handle="@rajwanders", influencer_name="Raj Krishnan",
            platform="Instagram", status="Awaiting Reply", current_stage="Contacted",
            next_action="Follow up next week",
            messages=[
                _msg("agent", "Hi Raj, your heritage site photography is stunning -- the Hampi series was incredible. We're partnering with a premium travel brand and your storytelling style is exactly what we're looking for. Would love to explore a collaboration.", "2026-04-01 11:30", "initial"),
            ],
        ),

        # ── Follow-up sent (3) ───────────────────────────────────────────
        OutreachThread(
            influencer_handle="@meilinbeauty", influencer_name="Mei Lin Wu",
            platform="YouTube", status="Follow-up Sent", current_stage="Contacted",
            next_action="Wait 5 days, then try DM",
            messages=[
                _msg("agent", "Hi Mei Lin! Your skincare science breakdowns are exactly what we look for in a partner. Radiance Skincare is launching a new vitamin C serum and we'd love to have you involved. Interested?", "2026-03-20 09:00", "initial"),
                _msg("agent", "Just following up on my note from last week! Totally understand if you're busy. The campaign would involve 2 YouTube videos over 6 weeks. Happy to share full details whenever works for you.", "2026-03-27 10:30", "follow_up"),
            ],
        ),
        OutreachThread(
            influencer_handle="@rachelglam", influencer_name="Rachel Green",
            platform="YouTube", status="Follow-up Sent", current_stage="Contacted",
            next_action="Try alternate contact channel",
            messages=[
                _msg("agent", "Rachel, huge fan of your red carpet recreation series! We have a luxury beauty campaign that would be a natural fit for your channel. Can we set up a quick call?", "2026-03-15 14:00", "initial"),
                _msg("agent", "Hey Rachel! Circling back on this -- the campaign is with Charlotte Tilbury for their new collection launch. We think your 1.2M audience is the perfect match. Let me know if you'd like to hear more!", "2026-03-25 11:00", "follow_up"),
            ],
        ),
        OutreachThread(
            influencer_handle="@danielkimlife", influencer_name="Daniel Kim",
            platform="YouTube", status="Follow-up Sent", current_stage="Contacted",
            next_action="Await reply, consider alternate approach",
            messages=[
                _msg("agent", "Daniel, your gear reviews and lifestyle vlogs are exactly the vibe we're going for. Working on a campaign for a premium wellness brand -- would love to chat about a partnership.", "2026-03-18 16:00", "initial"),
                _msg("agent", "Following up! We're specifically interested in a 2-video series featuring your daily routine with the product. Budget is competitive for your tier. Would love 15 min to discuss.", "2026-03-28 09:15", "follow_up"),
            ],
        ),

        # ── Replied positively (4) ───────────────────────────────────────
        OutreachThread(
            influencer_handle="@tylerbreaks", influencer_name="Tyler Brooks",
            platform="TikTok", status="Interested", current_stage="Replied",
            next_action="Schedule call this week",
            messages=[
                _msg("agent", "Tyler! Your 60-second gadget unboxings are addictive. NovaTech is launching a new wireless earbuds line and we think your audience would go crazy for them. Want to collab?", "2026-03-22 10:00", "initial"),
                _msg("influencer", "hey! yeah these look cool, I'm definitely interested. what's the scope and timeline looking like?", "2026-03-23 18:45", "reply"),
                _msg("agent", "Awesome! Thinking 3 TikToks over 4 weeks -- an unboxing, a vs. comparison, and a daily carry video. We'll send product + comp. Free to jump on a 15-min call Thursday?", "2026-03-24 09:30", "follow_up"),
            ],
        ),
        OutreachThread(
            influencer_handle="@emmabakes", influencer_name="Emma Johansson",
            platform="YouTube", status="Interested", current_stage="Replied",
            next_action="Send campaign brief",
            messages=[
                _msg("agent", "Emma, your sourdough content is incredible! FreshBite Delivery is building a campaign around artisan cooking and your Nordic baking style would be a beautiful fit. Interested in a sponsored series?", "2026-03-19 08:00", "initial"),
                _msg("influencer", "Oh this sounds lovely! I've been wanting to do more brand work. What does the collaboration look like exactly? I'm curious about the creative freedom aspect.", "2026-03-21 14:20", "reply"),
            ],
        ),
        OutreachThread(
            influencer_handle="@miathompsonliving", influencer_name="Mia Thompson",
            platform="Instagram", status="Interested", current_stage="Replied",
            next_action="Send detailed proposal",
            messages=[
                _msg("agent", "Mia! Your Southern living content with modern interior design touches is exactly our brand's aesthetic. We're launching a home collection and would love to feature your styling. Interested?", "2026-03-25 11:00", "initial"),
                _msg("influencer", "I love this! The aesthetic match is definitely there. Can you tell me more about the product line and what the content expectations would be? Also curious about timeline and compensation.", "2026-03-26 20:15", "reply"),
            ],
        ),
        OutreachThread(
            influencer_handle="@hannahtravels", influencer_name="Hannah Muller",
            platform="TikTok", status="Interested", current_stage="Replied",
            next_action="Send travel partnership details",
            messages=[
                _msg("agent", "Hannah, your budget Europe content is so useful -- the hidden gems series is pure gold. We're working with a travel platform and think a partnership could be amazing. Thoughts?", "2026-03-20 12:00", "initial"),
                _msg("influencer", "ooh yes!! I'm actually planning a Balkans trip in May that could work perfectly. what platform are you guys working with?", "2026-03-22 09:30", "reply"),
                _msg("agent", "Perfect timing! It's with Skyscanner for their summer campaign. The Balkans angle would be ideal. Let me send over the full brief.", "2026-03-22 14:00", "follow_up"),
            ],
        ),

        # ── Replied with questions / hesitant (3) ────────────────────────
        OutreachThread(
            influencer_handle="@ariachengg", influencer_name="Aria Chen",
            platform="TikTok", status="Questions", current_stage="Replied",
            next_action="Address concerns and send revised proposal",
            messages=[
                _msg("agent", "Aria! Your cozy gaming setups are goals. We're working with a premium peripherals brand on a content series and your aesthetic is exactly right. Want to hear more?", "2026-03-18 10:00", "initial"),
                _msg("influencer", "thanks for reaching out! I'm interested but I need to know more about exclusivity terms. I have an existing relationship with Secretlab and want to make sure there's no conflict.", "2026-03-20 16:30", "reply"),
                _msg("agent", "Totally understand and respect that! The campaign is specifically for audio peripherals, so no overlap with your Secretlab partnership. We can include a non-compete carve-out in the agreement. Want me to send the specifics?", "2026-03-21 09:00", "follow_up"),
                _msg("influencer", "ok that helps! send over the details and I'll review with my manager", "2026-03-21 22:15", "reply"),
            ],
        ),
        OutreachThread(
            influencer_handle="@isabellamoreno", influencer_name="Isabella Moreno",
            platform="YouTube", status="Questions", current_stage="Replied",
            next_action="Provide sustainability documentation",
            messages=[
                _msg("agent", "Isabella, your commitment to sustainable fashion is inspiring. We're working with an ethical fashion brand and think your audience would genuinely benefit from this partnership. Interested?", "2026-03-22 09:00", "initial"),
                _msg("influencer", "Thank you! I'm selective about partnerships -- can you share the brand's sustainability certifications and supply chain transparency reports? My audience trusts my vetting process.", "2026-03-24 11:45", "reply"),
            ],
        ),
        OutreachThread(
            influencer_handle="@yukisatogames", influencer_name="Yuki Sato",
            platform="TikTok", status="Questions", current_stage="Contacted",
            next_action="Send Japanese-language brief",
            messages=[
                _msg("agent", "Yuki-san, your retro gaming collection tours are fantastic! We're building a campaign around classic gaming culture and your perspective would be perfect. Would you be interested?", "2026-03-29 08:00", "initial"),
                _msg("influencer", "Hi! This sounds interesting but I mostly create content in Japanese. Would bilingual content work for your campaign, or do you need English-only?", "2026-03-30 21:00", "reply"),
                _msg("agent", "Bilingual is actually preferred! We're targeting both NA and JP markets. Would love to discuss further -- can I send a bilingual brief?", "2026-03-31 10:00", "follow_up"),
            ],
        ),

        # ── Active negotiation (3) ───────────────────────────────────────
        OutreachThread(
            influencer_handle="@lunaskinlab", influencer_name="Luna Kim",
            platform="Instagram", status="Negotiating", current_stage="Negotiating",
            next_action="Finalize rate and send contract", deal_value=8500,
            messages=[
                _msg("agent", "Luna, your K-beauty formulation expertise is exactly what Radiance Skincare needs for their new serum launch. Interested in a content partnership?", "2026-03-10 09:00", "initial"),
                _msg("influencer", "Very interested! I've actually used some Radiance products before. What are you thinking in terms of deliverables?", "2026-03-11 15:00", "reply"),
                _msg("agent", "Great to hear! We're thinking 4 Instagram posts + 8 Stories over 8 weeks, featuring the full skincare routine. Budget range is $7,000-$9,000. Does that work?", "2026-03-12 10:00", "negotiation"),
                _msg("influencer", "The scope works for me. For 4 posts + 8 stories with usage rights, I'd need $8,500. I also want approval on final edits and a 30-day exclusivity window (not 90).", "2026-03-14 11:30", "negotiation"),
                _msg("agent", "$8,500 works. We can do 30-day exclusivity and you'll have final approval on all content. I'll send the contract for review.", "2026-03-15 09:00", "negotiation"),
            ],
        ),
        OutreachThread(
            influencer_handle="@jesstranlife", influencer_name="Jessica Tran",
            platform="TikTok", status="Negotiating", current_stage="Negotiating",
            next_action="Await counter-proposal on deliverables", deal_value=12000,
            messages=[
                _msg("agent", "Jessica! Your day-in-my-life content is incredible. We're working with Athletic Greens on a wellness series and your productivity-meets-health angle is perfect.", "2026-03-08 10:00", "initial"),
                _msg("influencer", "Oh I love AG! I've actually been a customer for a year. This could be super authentic. What's the campaign look like?", "2026-03-09 19:00", "reply"),
                _msg("agent", "That's amazing -- authentic partnerships perform so much better. Thinking 5 TikToks + 1 YouTube integration over 6 weeks. Budget is $10K-$14K depending on scope.", "2026-03-10 09:30", "negotiation"),
                _msg("influencer", "For the full package with both platforms, I'd be at $12K. But I'd want to reduce to 4 TikToks since I want each one to feel really intentional, not rushed.", "2026-03-12 14:00", "negotiation"),
            ],
        ),
        OutreachThread(
            influencer_handle="@sarahplaysit", influencer_name="Sarah McDonald",
            platform="YouTube", status="Negotiating", current_stage="Negotiating",
            next_action="Send revised scope with indie game focus", deal_value=3500,
            messages=[
                _msg("agent", "Sarah, your indie game spotlights are a treasure for the gaming community. We have a unique opportunity with a new indie studio launching their first title. Interested in an early-access partnership?", "2026-03-15 08:00", "initial"),
                _msg("influencer", "This is right up my alley! What's the game and what kind of content are we talking?", "2026-03-16 17:30", "reply"),
                _msg("agent", "It's a narrative-driven puzzle game with gorgeous art. Thinking 2 dedicated videos: a first-look and a deeper review. Plus a livestream of your first playthrough. Budget is $3,000-$4,000.", "2026-03-17 10:00", "negotiation"),
                _msg("influencer", "I'd love to do the 2 videos. For the livestream, can we do it on my Twitch instead of YouTube? My community is more engaged there for live content. $3,500 for the full package.", "2026-03-19 12:00", "negotiation"),
            ],
        ),

        # ── Deal signed (3) ──────────────────────────────────────────────
        OutreachThread(
            influencer_handle="@carlosfitmx", influencer_name="Carlos Mendez",
            platform="TikTok", status="Signed", current_stage="Signed",
            next_action="Review first content draft (due Apr 10)", deal_value=5600,
            messages=[
                _msg("agent", "Carlos! Your functional fitness content is incredible. VitaGlow wants to partner for their bilingual Spring campaign. Interested?", "2026-02-25 10:00", "initial"),
                _msg("influencer", "Sounds great! I've been looking for supplement partnerships. What's the deal?", "2026-02-26 20:00", "reply"),
                _msg("agent", "4 TikToks over 6 weeks, bilingual EN/ES. $5,600 all-in plus product. Contract attached.", "2026-02-28 09:00", "negotiation"),
                _msg("influencer", "Deal! Signed and sent back. When do we start?", "2026-03-02 10:00", "negotiation"),
                _msg("agent", "Welcome aboard! Content calendar sent. First draft due April 10. Let's make this amazing.", "2026-03-03 09:00", "follow_up"),
            ],
        ),
        OutreachThread(
            influencer_handle="@marcoeats", influencer_name="Marco DiNapoli",
            platform="TikTok", status="Signed", current_stage="Signed",
            next_action="Confirm restaurant list for shoot days", deal_value=14000,
            messages=[
                _msg("agent", "Marco! FreshBite wants to feature your NYC street food expertise in their spring campaign. Your first-bite reactions are gold. Interested?", "2026-02-20 11:00", "initial"),
                _msg("influencer", "YES. This is literally what I do. What's the scope?", "2026-02-21 09:00", "reply"),
                _msg("agent", "6 TikToks + 2 Instagram Reels featuring FreshBite partner restaurants. $14K including production costs. 8-week campaign.", "2026-02-22 10:00", "negotiation"),
                _msg("influencer", "I'm in. Only ask -- I pick the restaurants from their partner list. Creative control is non-negotiable for me.", "2026-02-23 15:00", "negotiation"),
                _msg("agent", "Absolutely, you choose. Contract signed and countersigned. Let's build the restaurant shortlist.", "2026-02-25 09:00", "follow_up"),
            ],
        ),
        OutreachThread(
            influencer_handle="@andrejexplores", influencer_name="Andre Jackson",
            platform="YouTube", status="Signed", current_stage="Signed",
            next_action="Ship equipment for safari shoot", deal_value=7200,
            messages=[
                _msg("agent", "Andre, your African tourism content is world-class. We're partnering with a premium travel brand for a series on authentic cultural experiences. This has your name on it.", "2026-02-18 08:00", "initial"),
                _msg("influencer", "I've been waiting for a partnership like this. What's the vision?", "2026-02-19 16:00", "reply"),
                _msg("agent", "3 long-form YouTube videos covering different regions, plus 10 Instagram Stories. $7,200 plus all travel covered. 12-week production window.", "2026-02-20 10:00", "negotiation"),
                _msg("influencer", "Perfect budget and timeline. I want to include a Cape Town episode since that's home base. Signed.", "2026-02-22 11:00", "negotiation"),
            ],
        ),

        # ── Declined (2) ─────────────────────────────────────────────────
        OutreachThread(
            influencer_handle="@jtechio", influencer_name="James O'Brien",
            platform="Twitter", status="Declined", current_stage="Contacted",
            next_action="Revisit in Q3 with adjusted offer",
            messages=[
                _msg("agent", "James, your SaaS commentary is sharp. NovaTech is building a developer-focused campaign and your credibility in the space is exactly what they need.", "2026-03-10 09:00", "initial"),
                _msg("influencer", "Appreciate the outreach. I'm currently not taking sponsored content -- my audience trusts me because I keep it independent. Happy to revisit in a few months if anything changes.", "2026-03-12 10:00", "reply"),
            ],
        ),
        OutreachThread(
            influencer_handle="@davidgrills", influencer_name="David Park",
            platform="Instagram", status="Declined", current_stage="Contacted",
            next_action="Archive -- timing conflict",
            messages=[
                _msg("agent", "David! Your brisket content is incredible. FreshBite Delivery is launching a BBQ series and you'd be perfect. Want to hear more?", "2026-03-14 10:00", "initial"),
                _msg("influencer", "Hey, thanks! Unfortunately I just signed an exclusive with Traeger through June so I can't do food brand partnerships right now. Circle back after that?", "2026-03-15 22:00", "reply"),
                _msg("agent", "Totally understand -- congrats on the Traeger deal! We'll definitely circle back in July. Best of luck with the partnership!", "2026-03-16 09:00", "follow_up"),
            ],
        ),
    ]
