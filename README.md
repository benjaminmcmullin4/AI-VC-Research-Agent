# AI VC Research Agent

An AI-powered market research tool that generates investor-ready market maps and thesis memos, designed for growth equity and PE workflows.

Built with **Claude** (Anthropic) for structured analysis, **Streamlit** for interactive UI, and **Plotly** for visualization.

## Features

- **6-Step Research Pipeline** — Market definition → taxonomy → company landscape → TAM/SAM sizing → investment thesis → full memo
- **Structured Outputs** — Every pipeline step produces validated Pydantic models via `instructor`
- **Interactive Market Map** — Plotly bubble chart with segment filtering and hover details
- **PE Memo Format** — 11-section memo matching TA Associates / General Atlantic format
- **PDF & DOCX Export** — Download professional memos for your investment committee
- **Demo Mode** — Works without an API key using pre-generated research data
- **Persistent History** — SQLite-backed research run history

## Quick Start

```bash
# Clone and install
pip install -r requirements.txt

# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# Run
streamlit run app.py
```

## Demo Mode

Visit the app without an API key to explore a pre-generated analysis of "AI Accounting Automation for SMBs" with all tabs fully functional.

## Architecture

```
UI Layer (Streamlit)        → app.py, components/
Orchestration Layer         → pipeline.py, prompts.py
Data/Service Layer          → db.py, schema.py, export.py
```

The LLM pipeline is fully testable without Streamlit — the UI is a thin wrapper.

## Tech Stack

| Purpose | Library |
|---|---|
| LLM structured output | `instructor` + `anthropic` |
| Data validation | `pydantic` v2 |
| Visualization | `plotly` |
| PDF export | `fpdf2` |
| DOCX export | `python-docx` |
| Persistence | `sqlite3` |
| UI | `streamlit` |

## Deploy to Streamlit Cloud

1. Push to GitHub
2. Connect repo on [share.streamlit.io](https://share.streamlit.io)
3. Add `ANTHROPIC_API_KEY` in Streamlit Cloud secrets
4. App works in demo mode for visitors without keys
