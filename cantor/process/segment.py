"""Text segmentation into training units: letters, paper sections, chapters."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

from cantor.db.schema import get_connection

log = logging.getLogger("cantor.process.segment")

# ---------------------------------------------------------------------------
# Date patterns for German correspondence
# ---------------------------------------------------------------------------

_DE_MONTHS = (
    r"Januar|Februar|März|April|Mai|Juni|Juli|August|"
    r"September|Oktober|November|Dezember"
)
_DATE_PATTERN = re.compile(
    rf"(?:den\s+)?\d{{1,2}}\.\s*(?:{_DE_MONTHS})\s+\d{{4}}", re.IGNORECASE
)

# Salutation patterns (German and English)
_SALUTATION_PATTERN = re.compile(
    r"^\s*(?:Lieber|Liebster|Hochgeehrter\s+Herr|Sehr\s+geehrter|"
    r"Verehrter|Dear\s+(?:Sir|Mr|Professor|Dr|Friend))",
    re.MULTILINE | re.IGNORECASE,
)

# Closing patterns
_CLOSING_PATTERN = re.compile(
    r"(?:Ihr\s+ergebener|Ihr\s+ergebenster|Hochachtungsvoll|"
    r"Mit\s+(?:herzlichem|freundlichem)\s+Gru[ßss]|"
    r"Yours\s+(?:truly|sincerely|faithfully))",
    re.IGNORECASE,
)

# Section markers for mathematical papers
_SECTION_PATTERN = re.compile(
    r"^\s*(?:§\s*\d+|Abschnitt\s+\w+|Section\s+\d+|\d+\.\s+[A-Z])",
    re.MULTILINE,
)

# Theorem-like environments
_THEOREM_PATTERN = re.compile(
    r"^\s*(?:Satz|Theorem|Lemma|Korollar|Corollary|Definition|"
    r"Beweis|Proof|Proposition)\b[.\s:]",
    re.MULTILINE | re.IGNORECASE,
)

# Chapter markers for books
_CHAPTER_PATTERN = re.compile(
    r"^\s*(?:Chapter|Kapitel|CHAPTER|KAPITEL)\s+"
    r"(?:\d+|[IVXLCDM]+|[ivxlcdm]+)",
    re.MULTILINE | re.IGNORECASE,
)


@dataclass
class Segment:
    source_id: int
    segment_type: str
    title: str = ""
    content: str = ""
    language: str = "de"
    sender: str = ""
    recipient: str = ""
    segment_date: str = ""
    ordering: int = 0


# ---------------------------------------------------------------------------
# Letter segmentation
# ---------------------------------------------------------------------------

def _extract_letter_metadata(text: str) -> dict:
    """Pull date, sender hints, and recipient hints from a single letter."""
    meta: dict = {}
    date_match = _DATE_PATTERN.search(text[:500])
    if date_match:
        meta["segment_date"] = date_match.group(0).strip()

    sal_match = _SALUTATION_PATTERN.search(text[:300])
    if sal_match:
        after = text[sal_match.end(): sal_match.end() + 80]
        name_match = re.match(r"\s*([A-ZÄÖÜa-zäöüß\-]+(?:\s+[A-ZÄÖÜa-zäöüß\-]+)?)", after)
        if name_match:
            meta["recipient"] = name_match.group(1).strip(" ,!\n")

    return meta


def segment_letter(text: str, source_id: int) -> list[Segment]:
    """Split a letter collection by letter boundaries."""
    boundaries: list[int] = []

    for m in _SALUTATION_PATTERN.finditer(text):
        preceding = text[max(0, m.start() - 200): m.start()]
        if _DATE_PATTERN.search(preceding) or _CLOSING_PATTERN.search(preceding) or m.start() == 0:
            boundaries.append(m.start())

    if not boundaries:
        seg = Segment(
            source_id=source_id,
            segment_type="letter",
            title="Complete letter",
            content=text.strip(),
            ordering=0,
        )
        meta = _extract_letter_metadata(text)
        seg.segment_date = meta.get("segment_date", "")
        seg.recipient = meta.get("recipient", "")
        return [seg]

    if boundaries[0] > 0:
        boundaries.insert(0, 0)

    segments: list[Segment] = []
    for idx, start in enumerate(boundaries):
        end = boundaries[idx + 1] if idx + 1 < len(boundaries) else len(text)
        chunk = text[start:end].strip()
        if not chunk:
            continue

        meta = _extract_letter_metadata(chunk)
        title = meta.get("segment_date", f"Letter {idx + 1}")
        seg = Segment(
            source_id=source_id,
            segment_type="letter",
            title=title,
            content=chunk,
            sender=meta.get("sender", ""),
            recipient=meta.get("recipient", ""),
            segment_date=meta.get("segment_date", ""),
            ordering=idx,
        )
        segments.append(seg)

    log.info("Segmented %d letters from source %d", len(segments), source_id)
    return segments


# ---------------------------------------------------------------------------
# Paper segmentation
# ---------------------------------------------------------------------------

def segment_paper(text: str, source_id: int) -> list[Segment]:
    """Split a mathematical paper by section and theorem boundaries."""
    section_hits = list(_SECTION_PATTERN.finditer(text))

    if not section_hits:
        return [
            Segment(
                source_id=source_id,
                segment_type="section",
                title="Full paper",
                content=text.strip(),
                ordering=0,
            )
        ]

    segments: list[Segment] = []

    if section_hits[0].start() > 0:
        preamble = text[: section_hits[0].start()].strip()
        if preamble:
            segments.append(
                Segment(
                    source_id=source_id,
                    segment_type="section",
                    title="Preamble",
                    content=preamble,
                    ordering=0,
                )
            )

    for idx, hit in enumerate(section_hits):
        end = section_hits[idx + 1].start() if idx + 1 < len(section_hits) else len(text)
        content = text[hit.start(): end].strip()
        if not content:
            continue

        title_line = content.split("\n", 1)[0].strip()

        theorem_spans = list(_THEOREM_PATTERN.finditer(content))
        if len(theorem_spans) > 1:
            for tidx, thm in enumerate(theorem_spans):
                thm_end = (
                    theorem_spans[tidx + 1].start()
                    if tidx + 1 < len(theorem_spans)
                    else len(content)
                )
                thm_text = content[thm.start(): thm_end].strip()
                thm_title = thm_text.split("\n", 1)[0].strip()
                segments.append(
                    Segment(
                        source_id=source_id,
                        segment_type="theorem",
                        title=f"{title_line} > {thm_title}",
                        content=thm_text,
                        ordering=len(segments),
                    )
                )
        else:
            segments.append(
                Segment(
                    source_id=source_id,
                    segment_type="section",
                    title=title_line,
                    content=content,
                    ordering=len(segments),
                )
            )

    log.info("Segmented %d sections/theorems from source %d", len(segments), source_id)
    return segments


# ---------------------------------------------------------------------------
# Book segmentation
# ---------------------------------------------------------------------------

def segment_book(text: str, source_id: int) -> list[Segment]:
    """Split a book by chapter markers."""
    chapter_hits = list(_CHAPTER_PATTERN.finditer(text))

    if not chapter_hits:
        return [
            Segment(
                source_id=source_id,
                segment_type="chapter",
                title="Full text",
                content=text.strip(),
                ordering=0,
            )
        ]

    segments: list[Segment] = []

    if chapter_hits[0].start() > 0:
        front_matter = text[: chapter_hits[0].start()].strip()
        if front_matter:
            segments.append(
                Segment(
                    source_id=source_id,
                    segment_type="chapter",
                    title="Front matter",
                    content=front_matter,
                    ordering=0,
                )
            )

    for idx, hit in enumerate(chapter_hits):
        end = chapter_hits[idx + 1].start() if idx + 1 < len(chapter_hits) else len(text)
        content = text[hit.start(): end].strip()
        if not content:
            continue
        title_line = content.split("\n", 1)[0].strip()
        segments.append(
            Segment(
                source_id=source_id,
                segment_type="chapter",
                title=title_line,
                content=content,
                ordering=len(segments),
            )
        )

    log.info("Segmented %d chapters from source %d", len(segments), source_id)
    return segments


# ---------------------------------------------------------------------------
# Dialogue segmentation
# ---------------------------------------------------------------------------

def segment_dialogue(
    texts: list[tuple[str, str, str]], source_id: int
) -> list[Segment]:
    """Create dialogue segments from (sender, recipient, content) tuples."""
    segments: list[Segment] = []
    for idx, (sender, recipient, content) in enumerate(texts):
        segments.append(
            Segment(
                source_id=source_id,
                segment_type="dialogue",
                title=f"{sender} -> {recipient}",
                content=content.strip(),
                sender=sender,
                recipient=recipient,
                ordering=idx,
            )
        )

    log.info("Created %d dialogue segments from source %d", len(segments), source_id)
    return segments


# ---------------------------------------------------------------------------
# Auto-dispatch
# ---------------------------------------------------------------------------

def auto_segment(text: str, source_id: int, format_hint: str = "paper") -> list[Segment]:
    """Auto-detect and segment based on *format_hint*."""
    dispatch = {
        "letter": segment_letter,
        "collection": segment_letter,
        "paper": segment_paper,
        "article": segment_paper,
        "book": segment_book,
        "biography": segment_book,
    }
    func = dispatch.get(format_hint, segment_paper)
    return func(text, source_id)


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def save_segments(segments: list[Segment], db_path: Path | None = None) -> None:
    """Insert segments into the database segments table."""
    if not segments:
        return

    conn = get_connection(db_path)
    try:
        conn.executemany(
            """INSERT INTO segments
               (source_id, segment_type, title, content, language,
                sender, recipient, segment_date, ordering)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                (
                    s.source_id,
                    s.segment_type,
                    s.title,
                    s.content,
                    s.language,
                    s.sender,
                    s.recipient,
                    s.segment_date,
                    s.ordering,
                )
                for s in segments
            ],
        )
        conn.commit()
        log.info("Saved %d segments to database", len(segments))
    except Exception:
        conn.rollback()
        log.exception("Failed to save segments")
        raise
    finally:
        conn.close()
