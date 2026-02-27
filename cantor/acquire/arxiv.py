"""Scraper for arXiv — academic papers on Cantor's work."""

from __future__ import annotations

import asyncio
import logging
from xml.etree import ElementTree

from cantor.acquire.base import BaseScraper

log = logging.getLogger("cantor.acquire.arxiv")

PAPERS: dict[str, dict[str, str]] = {
    "2407.18972": {
        "title": "Theological Reasoning of Cantor's Set Theory",
        "note": "Recent interdisciplinary analysis of theology and set theory",
    },
}

ARXIV_API_URL = "http://export.arxiv.org/api/query?id_list={arxiv_id}"
ARXIV_PDF_URL = "https://arxiv.org/pdf/{arxiv_id}.pdf"
ARXIV_HTML_URL = "https://arxiv.org/html/{arxiv_id}"

ATOM_NS = "{http://www.w3.org/2005/Atom}"


class ArxivScraper(BaseScraper):
    """Fetch papers from arXiv by ID."""

    async def fetch_metadata(self, arxiv_id: str) -> dict[str, str]:
        """Query the arXiv Atom API and return basic metadata."""
        url = ARXIV_API_URL.format(arxiv_id=arxiv_id)
        xml_text = await self.fetch_page(url)
        root = ElementTree.fromstring(xml_text)

        entry = root.find(f"{ATOM_NS}entry")
        if entry is None:
            log.warning("No entry found for %s", arxiv_id)
            return {"id": arxiv_id, "title": "", "summary": ""}

        title = (entry.findtext(f"{ATOM_NS}title") or "").strip()
        summary = (entry.findtext(f"{ATOM_NS}summary") or "").strip()
        published = (entry.findtext(f"{ATOM_NS}published") or "").strip()

        authors: list[str] = []
        for author_el in entry.findall(f"{ATOM_NS}author"):
            name = author_el.findtext(f"{ATOM_NS}name")
            if name:
                authors.append(name.strip())

        return {
            "id": arxiv_id,
            "title": title,
            "summary": summary,
            "published": published,
            "authors": ", ".join(authors),
            "pdf_url": ARXIV_PDF_URL.format(arxiv_id=arxiv_id),
            "html_url": ARXIV_HTML_URL.format(arxiv_id=arxiv_id),
        }

    async def fetch_paper(self, arxiv_id: str) -> str:
        """Download paper content (HTML version preferred, falls back to metadata+abstract)."""
        meta = await self.fetch_metadata(arxiv_id)

        try:
            html = await self.fetch_page(meta["html_url"])
            self.save_raw(html, f"arxiv/{arxiv_id}.html")
            log.info("Saved HTML for %s", arxiv_id)
            return html
        except Exception:
            log.info("HTML unavailable for %s, saving metadata only", arxiv_id)

        content_lines = [
            f"Title: {meta['title']}",
            f"Authors: {meta['authors']}",
            f"Published: {meta['published']}",
            f"PDF: {meta['pdf_url']}",
            "",
            "Abstract:",
            meta["summary"],
        ]
        content = "\n".join(content_lines)
        self.save_raw(content, f"arxiv/{arxiv_id}.txt")
        return content

    async def scrape_all(self) -> dict[str, str]:
        results: dict[str, str] = {}
        for arxiv_id in PAPERS:
            log.info("Fetching arXiv paper %s", arxiv_id)
            text = await self.fetch_paper(arxiv_id)
            results[arxiv_id] = text
        return results

    async def run(self) -> None:
        await self.scrape_all()


def scrape_all_sync() -> dict[str, str]:
    """Synchronous entry point."""
    scraper = ArxivScraper()
    return asyncio.run(scraper.scrape_all())


if __name__ == "__main__":
    scrape_all_sync()
