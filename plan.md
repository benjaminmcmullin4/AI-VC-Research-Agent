You are helping me repurpose an existing Streamlit app into a new MVP for an **agentic influencer marketing platform**.

## High-level objective

Take my current Streamlit website and transform it into a polished MVP / demo product for an **Influencer Management Dashboard**.

This is not meant to be a full production app yet. It should be a believable, clean, interactive **first version** that helps a potential cofounder, investor, or client visualize what this company could become.

## Important instruction about the existing codebase

I already have a Streamlit website built.

Your job is to:

1. Inspect the current codebase
2. Delete or remove everything that is unrelated to this new influencer management product
3. **Preserve any useful existing setup for Streamlit and especially anything related to how my Claude API is currently configured and called**
4. Rebuild the app around this new use case

If there are existing helper functions, environment variable patterns, API wrappers, session state patterns, or UI patterns that are useful, keep and reuse them.

Do **not** preserve old business logic, old pages, or old UI just because it exists. This should feel like a clean pivot into a new app.

## Product concept

This app is the first module in a much bigger future platform: an **agentic marketing operating system**.

For now, the MVP is focused on **influencer discovery, qualification, outreach visibility, and performance tracking**.

The vision is that a client logs in and sees:

* overall campaign dashboard
* influencers found by the system
* top influencers recommended to reach out to next
* explanations for why those influencers are recommended
* outreach / conversation history
* campaign pipeline and statuses
* conversion metrics
* revenue attributed to influencers
* a sense that “agents are doing the work”

So the product should feel like:

* part dashboard
* part ops console
* part campaign intelligence layer

## Design goal

Make it feel like a modern SaaS product, not a hackathon toy.

Priorities:

* clean
* simple
* visually polished
* easy to navigate
* realistic enough to demo
* high signal, not cluttered

Use Streamlit in a polished way:

* clear page structure
* good use of columns, containers, metrics, tables, expanders, charts, tabs
* consistent naming and spacing
* thoughtful fake data
* strong information hierarchy

## Core UX

The MVP should have a main app shell with a sidebar and several pages or sections.

I want the app to include these primary areas:

### 1. Executive Dashboard

This is the first page the client sees.

Show:

* total influencers identified
* qualified influencers
* outreach sent
* reply rate
* active deals
* content posted
* total attributed revenue
* conversion rate
* cost per acquisition if relevant
* pipeline overview

Include charts and summaries like:

* influencer funnel
* outreach over time
* replies over time
* deal pipeline by stage
* revenue by influencer
* recent agent activity

This page should help the client quickly understand what is happening.

### 2. Influencer Discovery

A page showing discovered influencers.

Each influencer should have realistic fields like:

* name / handle
* platform
* niche
* follower count
* engagement rate
* audience fit score
* brand fit score
* estimated cost
* location
* status
* recommended / not recommended
* notes

Allow filtering and sorting by:

* platform
* niche
* fit score
* engagement
* status
* follower range

This page should include:

* a table of influencers
* ability to click/select one and view more detail
* a “recommended next” section for top targets

### 3. Recommendations / Why These Influencers

I want a section that clearly shows:

* top influencers the system thinks we should contact next
* a written explanation for each recommendation

Example reasoning:

* strong audience overlap with target customer
* high engagement relative to follower count
* historically similar creators performed well
* estimated CAC is attractive
* brand style match

If useful, use Claude to generate short recommendation blurbs from influencer profile data.

This is important because it helps make the app feel “agentic” rather than just a database.

### 4. Outreach / Conversations

A page where the user can view outreach activity and influencer conversations.

Show:

* outreach status
* first message
* follow-ups
* replies
* negotiation stage
* current owner / handled by system
* next action
* sentiment or status tag

The UI can be a simplified inbox / CRM style.

It does not need real messaging integrations yet. Use sample data and simulated threads if necessary.

But make it feel real.

### 5. Campaign Pipeline

A view of the influencer pipeline from:

* discovered
* qualified
* contacted
* replied
* negotiating
* signed
* content posted
* converted / revenue generated

This can be a kanban-style layout or a staged summary view using Streamlit-friendly components.

### 6. Analytics

A dedicated analytics page showing:

* conversion rate by influencer
* revenue by influencer
* revenue by platform
* top performing creators
* outreach-to-reply rate
* reply-to-deal rate
* deal-to-post rate
* post-to-conversion rate
* trend charts over time

Use charts that are easy to read and demo well.

### 7. Agent Activity Feed

This is important for the vision.

Add a page or section that simulates “agent activity,” such as:

* discovered 48 new creators in fitness niche
* flagged 7 high-priority creators
* sent 22 outreach messages
* detected positive reply from @creatorname
* suggested deal range for creator X
* updated expected ROI for campaign Y

This should make it feel like background systems are actively working.

## Suggested architecture inside the app

Structure the code cleanly.

Possible modules:

* app entrypoint
* pages or sections
* sample data generator or data files
* utility functions
* Claude helper functions
* styling helpers

Use maintainable code organization.

If multipage Streamlit is appropriate, use it.

## Data strategy for MVP

Use realistic seeded mock data unless there is already a useful data layer in the current project.

Create believable sample data for:

* influencer profiles
* campaign metrics
* conversations
* deal stages
* attributed revenue
* activity feed

The sample data should feel coherent and internally consistent.

For example:

* the revenue totals should roughly match the underlying influencer conversions
* the top recommended influencers should actually look strong based on their scores
* pipeline numbers should align across pages

## Claude API usage

Preserve and reuse my existing Claude API setup from the current codebase.

I specifically want you to:

* inspect how Claude API calls are currently handled
* keep the useful configuration and auth pattern
* reuse that setup for this app

Then use Claude only where it adds visible value in the MVP.

Good uses:

* recommendation blurbs for why an influencer is a fit
* summary insights on dashboard
* generated outreach drafts
* concise campaign observations

Do not over-engineer this. If live Claude calls would make the MVP fragile, allow a fallback to mocked output.

## Important implementation guidance

Please optimize for:

* working demo experience
* clean UX
* believable product vision
* reuse of useful existing infrastructure
* speed and simplicity over enterprise complexity

Do not:

* build unnecessary backend complexity
* add heavy auth unless it already exists and is easy to keep
* build real scraping
* build real messaging integrations
* build real databases unless already present and easy to reuse
* get stuck preserving legacy pages that do not fit this new concept

## What I want you to do step-by-step

1. Inspect the current Streamlit app structure
2. Identify what should be preserved:

   * Claude API setup
   * env var patterns
   * shared utilities worth keeping
   * styling/setup worth keeping
3. Identify what should be removed
4. Refactor the app into the new Influencer Management MVP
5. Create or seed realistic sample data
6. Build the pages and navigation
7. Make the UI polished and demo-worthy
8. Test the app enough that it runs cleanly
9. Briefly summarize:

   * what you kept
   * what you removed
   * what you built
   * how to run it

## Extra product framing

This should feel like the first version of a future “agentic marketing operating system.”

So while the MVP is focused on influencer management, the structure should imply that later we could add:

* lead gen
* paid ads
* email marketing
* SEO/content
* customer journey tracking

You do not need to build those now, but the app architecture and naming should make expansion feel natural.

## UI tone

Modern, sharp, operational, intelligent.

Not gimmicky.
Not overly futuristic.
Not generic startup template.

## Final deliverable

Please modify the existing codebase directly and convert it into this new product.

When done, give me:

* a summary of the new app structure
* any new files created
* any files deleted
* environment variables needed
* how to run it locally
* any assumptions you made

Before making changes, first inspect the project and tell me your plan briefly. Then proceed with implementation.

One more thing: if any part of the current UX or information architecture is weak, do not preserve it. Prefer a smaller number of really polished pages over a larger number of mediocre ones.

Please make the sample data rich enough that when I click through the app, it feels like a live client account with real campaign history, not placeholder rows.


so in the end I want you to completely redo this project with this new one so that the website infra via streamlit still works with the new one and the claude ai api with this one works just like the old one im scrapping

make sure the fake data is so good that this actaully seems like a real product. I don't want this to be to flashy, call it Agentic Marketing and Company Growth, and make it look like a very good professional website to impress my startup partner. 

fianl goal is a great website that "works" with rich data as if it was scrapped from social media.