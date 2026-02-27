"""Base scraper class for Project CANTOR web acquisition."""

from __future__ import annotations

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from pathlib import Path

import httpx
from rich.console import Console
from rich.logging import RichHandler

from cantor.db.catalog import update_source_file
from cantor.db.schema import DB_PATH

console = Console()

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console, rich_tracebacks=True)],
)
log = logging.getLogger("cantor.acquire")


class BaseScraper(ABC):
    """Abstract base for all CANTOR web scrapers.

    Provides an async httpx client with rate limiting, user-agent header,
    and helpers for saving raw content and updating the catalog database.
    """

    USER_AGENT = (
        "ProjectCANTOR/0.1 "
        "(academic research; reconstructing Cantor's intellectual world)"
    )
    DEFAULT_RATE_LIMIT: float = 1.0  # seconds between requests

    def __init__(self, rate_limit: float | None = None) -> None:
        self.rate_limit = rate_limit or self.DEFAULT_RATE_LIMIT
        self._last_request: float = 0.0

    async def _get_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            headers={"User-Agent": self.USER_AGENT},
            timeout=30.0,
            follow_redirects=True,
        )

    async def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_request
        if elapsed < self.rate_limit:
            await asyncio.sleep(self.rate_limit - elapsed)
        self._last_request = time.monotonic()

    async def fetch_page(self, url: str) -> str:
        """Fetch a single URL and return its text content."""
        await self._throttle()
        async with await self._get_client() as client:
            log.info("Fetching %s", url)
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.text

    def save_raw(self, content: str, filename: str, source_id: int | None = None) -> Path:
        """Persist raw content to ``data/raw/<subdir>/filename``.

        *source_id* is forwarded to :func:`update_catalog` when provided.
        Returns the path the file was written to.
        """
        out_path = DATA_DIR / filename
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content, encoding="utf-8")
        log.info("Saved %s (%d bytes)", out_path, len(content))

        if source_id is not None:
            self.update_catalog(source_id, out_path)
        return out_path

    def update_catalog(
        self,
        source_id: int,
        file_path: Path,
        db_path: Path | None = None,
    ) -> None:
        """Mark a source as *acquired* in the catalog database."""
        update_source_file(source_id, str(file_path), db_path=db_path or DB_PATH)
        log.info("Catalog updated: source %d -> %s", source_id, file_path)

    @abstractmethod
    async def run(self) -> None:
        """Execute the full scrape workflow."""
