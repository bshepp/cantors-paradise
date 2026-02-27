"""Scraper for MacTutor History of Mathematics — Cantor biography."""

from __future__ import annotations

import asyncio
import logging

from bs4 import BeautifulSoup

from cantor.acquire.base import BaseScraper

log = logging.getLogger("cantor.acquire.mactutors")

CANTOR_BIO_URL = "https://mathshistory.st-andrews.ac.uk/Biographies/Cantor/"


def _extract_biography(html: str) -> str:
    """Pull the main biography text, stripping chrome."""
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup.find_all(["nav", "header", "footer", "script", "style"]):
        tag.decompose()

    main = (
        soup.find("main")
        or soup.find("article")
        or soup.find("div", class_="biography")
        or soup.find("div", id="content")
    )

    if main is None:
        main = soup.body or soup

    return main.get_text(separator="\n", strip=True)


class MacTutorScraper(BaseScraper):
    """Fetch the Cantor biography from MacTutor."""

    async def scrape_biography(self, url: str | None = None) -> str:
        """Download and extract the biography text."""
        target = url or CANTOR_BIO_URL
        log.info("Scraping MacTutor biography from %s", target)
        html = await self.fetch_page(target)
        text = _extract_biography(html)
        self.save_raw(text, "mactutors/cantor_biography.txt")
        return text

    async def run(self) -> None:
        await self.scrape_biography()


def scrape_sync() -> str:
    """Synchronous entry point."""
    scraper = MacTutorScraper()
    return asyncio.run(scraper.scrape_biography())


if __name__ == "__main__":
    scrape_sync()
