"""Scraper for jamesrmeyer.com — English translations of Cantor's papers."""

from __future__ import annotations

import asyncio
import logging

from bs4 import BeautifulSoup

from cantor.acquire.base import BaseScraper

log = logging.getLogger("cantor.acquire.jamesrmeyer")

PAGES: dict[str, str] = {
    "cantors-first-paper-1874": (
        "https://www.jamesrmeyer.com/infinite/cantors-first-paper.html"
    ),
    "punktmannichfaltigkeiten-part1": (
        "https://www.jamesrmeyer.com/infinite/cantor-punkt1.html"
    ),
    "punktmannichfaltigkeiten-part2": (
        "https://www.jamesrmeyer.com/infinite/cantor-punkt2.html"
    ),
    "punktmannichfaltigkeiten-part3": (
        "https://www.jamesrmeyer.com/infinite/cantor-punkt3.html"
    ),
    "punktmannichfaltigkeiten-part4": (
        "https://www.jamesrmeyer.com/infinite/cantor-punkt4.html"
    ),
    "grundlagen-part5": (
        "https://www.jamesrmeyer.com/infinite/cantor-grundlagen.html"
    ),
    "punktmannichfaltigkeiten-part6": (
        "https://www.jamesrmeyer.com/infinite/cantor-punkt6.html"
    ),
    "diagonal-argument-1891": (
        "https://www.jamesrmeyer.com/infinite/cantors-1891-proof.html"
    ),
    "beitrage-part-i": (
        "https://www.jamesrmeyer.com/infinite/cantors-beitrage.html"
    ),
    "beitrage-part-ii": (
        "https://www.jamesrmeyer.com/infinite/cantors-beitrage2.html"
    ),
}


def _extract_main_content(html: str) -> str:
    """Strip navigation, header, footer; return the main text content."""
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup.find_all(["nav", "header", "footer", "script", "style"]):
        tag.decompose()

    main = (
        soup.find("main")
        or soup.find("article")
        or soup.find("div", class_="content")
        or soup.find("div", id="content")
    )

    if main is None:
        main = soup.body or soup

    return main.get_text(separator="\n", strip=True)


class JamesRMeyerScraper(BaseScraper):
    """Fetch translated Cantor papers from jamesrmeyer.com."""

    async def scrape_page(self, url: str, filename: str) -> str:
        """Fetch a single page, extract text, and save to disk."""
        html = await self.fetch_page(url)
        text = _extract_main_content(html)
        self.save_raw(text, f"jamesrmeyer/{filename}")
        return text

    async def scrape_all(self) -> dict[str, str]:
        """Fetch every page in :data:`PAGES` and return ``{key: text}``."""
        results: dict[str, str] = {}
        for key, url in PAGES.items():
            filename = f"{key}.txt"
            log.info("Scraping %s -> %s", key, filename)
            text = await self.scrape_page(url, filename)
            results[key] = text
        return results

    async def run(self) -> None:
        await self.scrape_all()


def scrape_all_sync() -> dict[str, str]:
    """Synchronous entry point."""
    scraper = JamesRMeyerScraper()
    return asyncio.run(scraper.scrape_all())


if __name__ == "__main__":
    scrape_all_sync()
