"""CRUD operations for the source catalog."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from cantor.db.schema import get_connection, DB_PATH


@dataclass
class Source:
    title: str
    tier: int
    weight: float
    author: str = ""
    date: str = ""
    language: str = "de"
    format: str = "paper"
    content_tags: list[str] = field(default_factory=list)
    acquisition_status: str = "pending"
    file_path: str = ""
    url: str = ""
    notes: str = ""
    id: int | None = None


def _tags_to_str(tags: list[str]) -> str:
    return json.dumps(tags) if tags else "[]"


def _tags_from_str(raw: str | None) -> list[str]:
    if not raw:
        return []
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return []


def _row_to_source(row: sqlite3.Row) -> Source:
    d = dict(row)
    d["content_tags"] = _tags_from_str(d.get("content_tags"))
    d.pop("created_at", None)
    d.pop("updated_at", None)
    return Source(**d)


def add_source(src: Source, db_path: Path | None = None) -> int:
    conn = get_connection(db_path or DB_PATH)
    cur = conn.execute(
        """INSERT INTO sources
           (title, author, date, tier, weight, language, format,
            content_tags, acquisition_status, file_path, url, notes)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            src.title, src.author, src.date, src.tier, src.weight,
            src.language, src.format, _tags_to_str(src.content_tags),
            src.acquisition_status, src.file_path, src.url, src.notes,
        ),
    )
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id


def add_sources_bulk(sources: list[Source], db_path: Path | None = None) -> int:
    conn = get_connection(db_path or DB_PATH)
    rows = [
        (
            s.title, s.author, s.date, s.tier, s.weight,
            s.language, s.format, _tags_to_str(s.content_tags),
            s.acquisition_status, s.file_path, s.url, s.notes,
        )
        for s in sources
    ]
    conn.executemany(
        """INSERT INTO sources
           (title, author, date, tier, weight, language, format,
            content_tags, acquisition_status, file_path, url, notes)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        rows,
    )
    conn.commit()
    count = len(rows)
    conn.close()
    return count


def get_source(source_id: int, db_path: Path | None = None) -> Source | None:
    conn = get_connection(db_path or DB_PATH)
    row = conn.execute("SELECT * FROM sources WHERE id = ?", (source_id,)).fetchone()
    conn.close()
    return _row_to_source(row) if row else None


def get_all_sources(db_path: Path | None = None) -> list[Source]:
    conn = get_connection(db_path or DB_PATH)
    rows = conn.execute("SELECT * FROM sources ORDER BY tier, title").fetchall()
    conn.close()
    return [_row_to_source(r) for r in rows]


def get_sources_by_tier(tier: int, db_path: Path | None = None) -> list[Source]:
    conn = get_connection(db_path or DB_PATH)
    rows = conn.execute(
        "SELECT * FROM sources WHERE tier = ? ORDER BY title", (tier,)
    ).fetchall()
    conn.close()
    return [_row_to_source(r) for r in rows]


def get_sources_by_status(status: str, db_path: Path | None = None) -> list[Source]:
    conn = get_connection(db_path or DB_PATH)
    rows = conn.execute(
        "SELECT * FROM sources WHERE acquisition_status = ? ORDER BY tier, title",
        (status,),
    ).fetchall()
    conn.close()
    return [_row_to_source(r) for r in rows]


def update_source_status(
    source_id: int, status: str, db_path: Path | None = None
) -> None:
    conn = get_connection(db_path or DB_PATH)
    conn.execute(
        "UPDATE sources SET acquisition_status = ?, updated_at = datetime('now') WHERE id = ?",
        (status, source_id),
    )
    conn.commit()
    conn.close()


def update_source_file(
    source_id: int, file_path: str, db_path: Path | None = None
) -> None:
    conn = get_connection(db_path or DB_PATH)
    conn.execute(
        """UPDATE sources
           SET file_path = ?, acquisition_status = 'acquired',
               updated_at = datetime('now')
           WHERE id = ?""",
        (file_path, source_id),
    )
    conn.commit()
    conn.close()


def get_catalog_stats(db_path: Path | None = None) -> dict[str, Any]:
    conn = get_connection(db_path or DB_PATH)
    total = conn.execute("SELECT COUNT(*) FROM sources").fetchone()[0]
    by_tier = {}
    for row in conn.execute(
        "SELECT tier, COUNT(*) as cnt FROM sources GROUP BY tier ORDER BY tier"
    ):
        by_tier[row["tier"]] = row["cnt"]
    by_status = {}
    for row in conn.execute(
        "SELECT acquisition_status, COUNT(*) as cnt FROM sources GROUP BY acquisition_status"
    ):
        by_status[row["acquisition_status"]] = row["cnt"]
    conn.close()
    return {"total": total, "by_tier": by_tier, "by_status": by_status}
