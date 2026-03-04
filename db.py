"""SQLite persistence layer for research runs."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

from config import DB_PATH
from schema import ResearchOutput

_DDL = """
CREATE TABLE IF NOT EXISTS research_runs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    query       TEXT NOT NULL,
    geography   TEXT NOT NULL DEFAULT 'Global',
    stage_focus TEXT NOT NULL DEFAULT 'All Stages',
    output_json TEXT NOT NULL,
    created_at  TEXT NOT NULL
);
"""


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    """Create tables if they don't exist."""
    with _connect() as conn:
        conn.executescript(_DDL)


def save_run(output: ResearchOutput) -> int:
    """Persist a completed research run. Returns the row id."""
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO research_runs (query, geography, stage_focus, output_json, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                output.query,
                output.geography,
                output.stage_focus,
                output.model_dump_json(),
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        return cur.lastrowid  # type: ignore[return-value]


def list_runs() -> list[dict]:
    """Return summary rows (id, query, created_at) newest first."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, query, geography, stage_focus, created_at "
            "FROM research_runs ORDER BY id DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def load_run(run_id: int) -> ResearchOutput | None:
    """Load a full research output by id."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT output_json FROM research_runs WHERE id = ?", (run_id,)
        ).fetchone()
    if row is None:
        return None
    return ResearchOutput.model_validate_json(row["output_json"])


def delete_run(run_id: int) -> None:
    """Delete a research run by id."""
    with _connect() as conn:
        conn.execute("DELETE FROM research_runs WHERE id = ?", (run_id,))
