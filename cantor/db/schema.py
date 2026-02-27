"""SQLite schema for the Project CANTOR source catalog."""

from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "cantor.db"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS sources (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    title           TEXT NOT NULL,
    author          TEXT,
    date            TEXT,
    tier            INTEGER NOT NULL CHECK (tier BETWEEN 1 AND 8),
    weight          REAL NOT NULL CHECK (weight BETWEEN 0.0 AND 1.0),
    language        TEXT DEFAULT 'de',
    format          TEXT CHECK (format IN ('letter','paper','book','article','collection','biography','web','other')),
    content_tags    TEXT,
    acquisition_status TEXT DEFAULT 'pending'
        CHECK (acquisition_status IN ('pending','available','acquired','processed','excluded')),
    file_path       TEXT,
    url             TEXT,
    notes           TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS segments (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id       INTEGER NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    segment_type    TEXT NOT NULL
        CHECK (segment_type IN ('letter','section','theorem','chapter','dialogue','fragment','full')),
    title           TEXT,
    content         TEXT NOT NULL,
    language        TEXT DEFAULT 'de',
    sender          TEXT,
    recipient       TEXT,
    segment_date    TEXT,
    ordering        INTEGER DEFAULT 0,
    parallel_id     INTEGER REFERENCES segments(id),
    created_at      TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS annotations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    segment_id      INTEGER NOT NULL REFERENCES segments(id) ON DELETE CASCADE,
    dimension       TEXT NOT NULL CHECK (dimension IN (
        'mathematical_intuition','theological_framework',
        'kronecker_conflict','psychological_landscape','personal_context'
    )),
    subtags         TEXT,
    math_topics     TEXT,
    psych_state     TEXT,
    confidence      REAL CHECK (confidence BETWEEN 0.0 AND 1.0),
    contradiction_flag INTEGER DEFAULT 0,
    contradiction_ref  INTEGER REFERENCES segments(id),
    notes           TEXT,
    reviewer        TEXT DEFAULT 'auto',
    created_at      TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS acquisition_log (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id       INTEGER NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    action          TEXT NOT NULL,
    details         TEXT,
    timestamp       TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_sources_tier ON sources(tier);
CREATE INDEX IF NOT EXISTS idx_sources_status ON sources(acquisition_status);
CREATE INDEX IF NOT EXISTS idx_segments_source ON segments(source_id);
CREATE INDEX IF NOT EXISTS idx_annotations_segment ON annotations(segment_id);
CREATE INDEX IF NOT EXISTS idx_annotations_dimension ON annotations(dimension);
"""


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or DB_PATH
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db(db_path: Path | None = None) -> Path:
    """Create the database and all tables. Returns the database path."""
    path = db_path or DB_PATH
    conn = get_connection(path)
    conn.executescript(SCHEMA_SQL)
    conn.close()
    return path
