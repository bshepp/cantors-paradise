"""Scraper for archive.org — public-domain Cantor texts."""

from __future__ import annotations

import asyncio
import logging

from cantor.acquire.base import BaseScraper

log = logging.getLogger("cantor.acquire.archive_org")

TEXTS: dict[str, dict[str, str]] = {
    "contributions_jourdain_1915": {
        "identifier": "contributionstot00markup",
        "title": "Contributions to the Founding of the Theory of Transfinite Numbers",
        "author": "Georg Cantor (trans. P. Jourdain)",
        "date": "1915",
    },
}

FULL_TEXT_URL = "https://archive.org/download/{identifier}/{identifier}_djvu.txt"
METADATA_URL = "https://archive.org/metadata/{identifier}"


class ArchiveOrgScraper(BaseScraper):
    """Fetch public-domain texts from archive.org."""

    async def fetch_metadata(self, identifier: str) -> str:
        """Download the JSON metadata for an archive.org item."""
        url = METADATA_URL.format(identifier=identifier)
        return await self.fetch_page(url)

    async def scrape_text(self, identifier: str) -> str:
        """Download the full plain-text (DjVu-derived) for *identifier*."""
        url = FULL_TEXT_URL.format(identifier=identifier)
        log.info("Downloading full text for %s", identifier)
        text = await self.fetch_page(url)
        filename = f"archive_org/{identifier}.txt"
        self.save_raw(text, filename)
        return text

    async def scrape_all(self) -> dict[str, str]:
        results: dict[str, str] = {}
        for key, info in TEXTS.items():
            ident = info["identifier"]
            log.info("Scraping archive.org item: %s (%s)", key, ident)
            text = await self.scrape_text(ident)
            results[key] = text
        return results

    async def run(self) -> None:
        await self.scrape_all()


def scrape_all_sync() -> dict[str, str]:
    """Synchronous entry point."""
    scraper = ArchiveOrgScraper()
    return asyncio.run(scraper.scrape_all())


if __name__ == "__main__":
    scrape_all_sync()
