# Project: AI VC Research Agent (Weekend Version)
You are a VC research lead + AI engineer. Build a local Streamlit market research agent that generates credible, investor-ready market maps and thesis memos.

## Outcome
User inputs a market (e.g., “AI accounting automation for SMBs”). Tool outputs:
- market definition + ICP + value chain
- TAM/SAM heuristics (assumptions shown)
- category taxonomy (subsegments)
- company landscape (10–25 companies) with buckets
- emerging trends and “why now”
- investment thesis + entry points
- open questions + diligence plan
- export as Markdown “market memo”
Also generate a “market map” visualization (simple, clean).

## Constraints
- Local Streamlit app
- SQLite persistence of research runs
- Minimal dependencies
- Must work without web browsing (default), but include an OPTIONAL browsing mode:
  - If enabled: do lightweight web search via a configurable provider OR just accept pasted links/text.
  - Since API access may be limited, default to “Paste sources” mode.
- Demo mode without API key: output a template with placeholders.

## UI Inputs
- Market query (text)
- Geography (optional)
- Stage focus (seed / Series A / growth)
- Toggle: "Use pasted sources" (default ON)
- Text area: "Sources / Notes" (user can paste snippets, links, bullet notes)
- Button: Generate
Sidebar:
- Depth: quick / standard / deep
- Output style: concise / detailed
- Temperature slider
- Company count slider (10–25)

## Data Model (SQLite)
- research_runs
  - id, created_at, market_query, geography, stage, sources_text
  - structured_json, memo_markdown

## LLM Pipeline (make it impressive)
### Step 1: Build “Market Spec”
LLM returns JSON:
- market_definition
- icp
- buyer, user, champion
- value_chain (upstream/downstream)
- key_workflows_affected
- pricing_models_seen (guesses)
- regulatory_context (if applicable)
- assumptions (list)

### Step 2: Taxonomy + Subsegments
Return JSON:
- taxonomy: [{segment, description, examples}]
- wedge_strategies: [bullets]
- “adjacent categories” (list)

### Step 3: Company Landscape (structured + bucketed)
Return JSON:
- buckets: [
  {
    bucket_name,
    description,
    companies: [{name, one_liner, stage_guess, why_in_bucket, differentiation}]
  }
]
Total companies 10–25 depending slider.
If sources_text includes companies, prioritize them and label “from sources”.
Otherwise label “model suggested”.

### Step 4: TAM/SAM Heuristics
Return JSON:
- tam_range
- sam_range
- method (top-down / bottoms-up hybrid)
- assumptions
- sensitivity (what changes the estimate)

Never output a single precise number. Always ranges + confidence.

### Step 5: Thesis + Risks + Open Questions
Return JSON:
- why_now (5 bullets)
- thesis (short paragraph)
- best_entry_points (bullets)
- winners_characteristics (bullets)
- risks (table-like list with severity 1–5)
- key_unknowns (bullets)
- diligence_plan (10 steps)
- sourcing_angles (where to find deals)

### Step 6: Produce the Market Memo Markdown
Generate a polished memo in Markdown using the structured JSON.
Must include:
- an “Evidence & Sources” section:
  - if sources_text provided, cite as “From provided sources”
  - if not, label as “General reasoning (no sources provided)”
Be explicit about uncertainty.

## Market Map Visualization (simple but impressive)
Create a 2D plot:
- x-axis: “Buyer size” (SMB -> Enterprise)
- y-axis: “Workflow depth” (light automation -> full-stack platform)
Place companies roughly based on their described positioning.
If uncertain, place as “unknown” bucket.

Use matplotlib (no seaborn), one chart.

## UI Outputs
Tabs:
1) Overview (definition + taxonomy)
2) Landscape (bucketed tables)
3) Thesis (why now, entry points, risks)
4) Memo (markdown + download)
5) Visual map (chart)

## Deliverables
app.py, db.py, llm.py, prompts.py, schema.py, render.py, viz.py, utils.py
requirements.txt, README.md, examples/sample_sources.txt

## Important
- Provide clean, commented code
- Add caching so reruns are fast
- Validate JSON with pydantic; show errors; auto-retry once with “fix JSON” prompt if invalid
- If the model cannot identify companies confidently, it must say so and output fewer rather than hallucinating.

Now generate the full project with all files and instructions.