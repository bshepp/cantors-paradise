"""Text extraction from PDF, HTML, and plain-text sources."""

from __future__ import annotations

import logging
from pathlib import Path

import fitz  # PyMuPDF
from bs4 import BeautifulSoup

log = logging.getLogger("cantor.process.extract")

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

_SUPPORTED_EXTENSIONS = {".pdf", ".html", ".htm", ".txt"}


def extract_pdf(file_path: Path) -> str:
    """Extract text from a PDF using PyMuPDF, preserving structural markers."""
    blocks: list[str] = []
    try:
        doc = fitz.open(str(file_path))
    except Exception:
        log.exception("Failed to open PDF: %s", file_path)
        raise

    for page_num, page in enumerate(doc, start=1):
        page_blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
        for block in page_blocks:
            if block["type"] != 0:  # skip images
                continue
            for line in block["lines"]:
                spans = line["spans"]
                if not spans:
                    continue
                text = "".join(s["text"] for s in spans).strip()
                if not text:
                    continue

                max_size = max(s["size"] for s in spans)
                is_bold = any(s["flags"] & 2 ** 4 for s in spans)

                if max_size >= 14 or (is_bold and max_size >= 12):
                    text = f"\n## {text}\n"
                elif max_size >= 11 and is_bold:
                    text = f"\n### {text}\n"

                blocks.append(text)
        blocks.append(f"\n--- page {page_num} ---\n")

    doc.close()
    return "\n".join(blocks)


def extract_html(file_path: Path) -> str:
    """Extract clean text from an HTML file, preserving header structure."""
    raw = file_path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(raw, "lxml")

    for tag in soup.find_all(["script", "style", "nav", "footer"]):
        tag.decompose()

    parts: list[str] = []
    for element in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "blockquote", "li"]):
        tag_name = element.name
        text = element.get_text(separator=" ", strip=True)
        if not text:
            continue

        if tag_name == "h1":
            parts.append(f"\n# {text}\n")
        elif tag_name == "h2":
            parts.append(f"\n## {text}\n")
        elif tag_name in ("h3", "h4", "h5", "h6"):
            parts.append(f"\n### {text}\n")
        elif tag_name == "blockquote":
            parts.append(f"> {text}")
        elif tag_name == "li":
            parts.append(f"- {text}")
        else:
            parts.append(text)

    return "\n\n".join(parts)


def extract_text(file_path: Path) -> str:
    """Auto-detect format by extension and call the appropriate extractor."""
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        return extract_pdf(file_path)
    if suffix in (".html", ".htm"):
        return extract_html(file_path)
    if suffix == ".txt":
        return file_path.read_text(encoding="utf-8", errors="replace")
    raise ValueError(f"Unsupported file format: {suffix!r} ({file_path})")


def process_all_raw(raw_dir: Path | None = None) -> list[dict]:
    """Walk the raw directory, extract every supported file, save to processed/.

    Returns a manifest: list of {source_file, output_file, format, char_count}.
    """
    source_dir = raw_dir or RAW_DIR
    if not source_dir.exists():
        log.warning("Raw data directory does not exist: %s", source_dir)
        return []

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []

    for file_path in sorted(source_dir.rglob("*")):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in _SUPPORTED_EXTENSIONS:
            log.debug("Skipping unsupported file: %s", file_path)
            continue

        log.info("Extracting: %s", file_path)
        try:
            text = extract_text(file_path)
        except Exception:
            log.exception("Extraction failed for %s", file_path)
            continue

        relative = file_path.relative_to(source_dir)
        out_path = PROCESSED_DIR / relative.with_suffix(".txt")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")

        entry = {
            "source_file": str(file_path),
            "output_file": str(out_path),
            "format": file_path.suffix.lower().lstrip("."),
            "char_count": len(text),
        }
        manifest.append(entry)
        log.info(
            "  -> %s (%d chars)",
            out_path.relative_to(DATA_DIR),
            entry["char_count"],
        )

    log.info("Extraction complete: %d files processed", len(manifest))
    return manifest
