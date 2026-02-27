"""Language detection and parallel-text management."""

from __future__ import annotations

import logging
from pathlib import Path

from langdetect import detect, detect_langs, LangDetectException

from cantor.db.schema import get_connection

log = logging.getLogger("cantor.process.language")

_MIN_CHARS_FOR_DETECTION = 20


def detect_language(text: str) -> str:
    """Detect the primary language of *text*. Returns an ISO 639-1 code."""
    text = text.strip()
    if len(text) < _MIN_CHARS_FOR_DETECTION:
        log.debug("Text too short for reliable detection (%d chars), defaulting to 'de'", len(text))
        return "de"
    try:
        return detect(text)
    except LangDetectException:
        log.warning("Language detection failed, defaulting to 'de'")
        return "de"


def detect_language_robust(text: str) -> tuple[str, float]:
    """Return *(language, confidence)* with graceful handling for short texts."""
    text = text.strip()
    if not text:
        return ("de", 0.0)

    if len(text) < _MIN_CHARS_FOR_DETECTION:
        try:
            lang = detect(text)
            return (lang, 0.3)
        except LangDetectException:
            return ("de", 0.0)

    try:
        results = detect_langs(text)
    except LangDetectException:
        log.warning("Robust detection failed, defaulting to 'de'")
        return ("de", 0.0)

    if not results:
        return ("de", 0.0)

    best = results[0]
    return (best.lang, round(best.prob, 4))


# ---------------------------------------------------------------------------
# Parallel-text linking
# ---------------------------------------------------------------------------

def link_parallel_texts(
    segment_id_original: int,
    segment_id_translation: int,
    db_path: Path | None = None,
) -> None:
    """Link two segments as parallel texts by setting *parallel_id* on each."""
    conn = get_connection(db_path)
    try:
        conn.execute(
            "UPDATE segments SET parallel_id = ? WHERE id = ?",
            (segment_id_translation, segment_id_original),
        )
        conn.execute(
            "UPDATE segments SET parallel_id = ? WHERE id = ?",
            (segment_id_original, segment_id_translation),
        )
        conn.commit()
        log.info(
            "Linked parallel texts: segment %d <-> segment %d",
            segment_id_original,
            segment_id_translation,
        )
    except Exception:
        conn.rollback()
        log.exception("Failed to link parallel texts")
        raise
    finally:
        conn.close()


def find_parallel_candidates(
    db_path: Path | None = None,
) -> list[tuple[int, int, str, str]]:
    """Find segment pairs from the same source in different languages.

    Returns a list of *(seg_id_1, seg_id_2, lang_1, lang_2)* tuples for
    segments that share a ``source_id`` but differ in ``language`` and have
    no ``parallel_id`` set yet.
    """
    conn = get_connection(db_path)
    try:
        rows = conn.execute(
            """
            SELECT a.id, b.id, a.language, b.language
            FROM segments a
            JOIN segments b
                ON a.source_id = b.source_id
                AND a.id < b.id
                AND a.language != b.language
            WHERE a.parallel_id IS NULL
              AND b.parallel_id IS NULL
            ORDER BY a.source_id, a.ordering, b.ordering
            """
        ).fetchall()
        candidates = [(r[0], r[1], r[2], r[3]) for r in rows]
        log.info("Found %d parallel-text candidates", len(candidates))
        return candidates
    finally:
        conn.close()


def flag_translation_discrepancy(
    segment_id_1: int,
    segment_id_2: int,
    note: str,
    db_path: Path | None = None,
) -> None:
    """Create an annotation flagging a translation discrepancy.

    Inserts one annotation per segment, with ``dimension='personal_context'``
    and ``contradiction_flag=1`` pointing at the other segment.
    """
    conn = get_connection(db_path)
    try:
        conn.execute(
            """INSERT INTO annotations
               (segment_id, dimension, contradiction_flag, contradiction_ref, notes, reviewer)
               VALUES (?, 'personal_context', 1, ?, ?, 'auto')""",
            (segment_id_1, segment_id_2, note),
        )
        conn.execute(
            """INSERT INTO annotations
               (segment_id, dimension, contradiction_flag, contradiction_ref, notes, reviewer)
               VALUES (?, 'personal_context', 1, ?, ?, 'auto')""",
            (segment_id_2, segment_id_1, note),
        )
        conn.commit()
        log.info(
            "Flagged translation discrepancy between segments %d and %d",
            segment_id_1,
            segment_id_2,
        )
    except Exception:
        conn.rollback()
        log.exception("Failed to flag translation discrepancy")
        raise
    finally:
        conn.close()
