"""Acquisition status tracker — rich table display and status helpers."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from rich.console import Console
from rich.table import Table

from cantor.db.catalog import (
    Source,
    get_all_sources,
    update_source_file,
    update_source_status,
)
from cantor.db.schema import DB_PATH

console = Console()

TIER_LABELS: dict[int, str] = {
    1: "Cantor's Own Words",
    2: "Direct Correspondents",
    3: "Mathematical Opponents",
    4: "Catholic Theologians",
    5: "Historical Scholarship",
    6: "Secondary Exposition",
    7: "Popular Accounts",
    8: "Excluded (Bell)",
}

STATUS_STYLES: dict[str, str] = {
    "acquired": "bold green",
    "processed": "bold cyan",
    "available": "yellow",
    "pending": "dim",
    "excluded": "bold red",
}


def show_status(db_path: Path | None = None) -> None:
    """Print a rich table showing acquisition status grouped by tier."""
    sources = get_all_sources(db_path=db_path or DB_PATH)

    by_tier: dict[int, list[Source]] = defaultdict(list)
    for src in sources:
        by_tier[src.tier].append(src)

    table = Table(
        title="Project CANTOR — Acquisition Status",
        show_lines=True,
        expand=True,
    )
    table.add_column("Tier", justify="center", width=6)
    table.add_column("Label", width=24)
    table.add_column("ID", justify="right", width=5)
    table.add_column("Title", ratio=2)
    table.add_column("Status", justify="center", width=12)
    table.add_column("File", ratio=1)

    for tier in sorted(by_tier):
        label = TIER_LABELS.get(tier, f"Tier {tier}")
        for src in by_tier[tier]:
            status = src.acquisition_status
            style = STATUS_STYLES.get(status, "")
            table.add_row(
                str(tier),
                label,
                str(src.id) if src.id is not None else "–",
                src.title,
                f"[{style}]{status}[/{style}]" if style else status,
                src.file_path or "",
            )
        label = ""  # only show the tier label on the first row of each group

    console.print(table)


def mark_acquired(source_id: int, file_path: str, db_path: Path | None = None) -> None:
    """Mark a source as acquired and record its file path."""
    update_source_file(source_id, file_path, db_path=db_path or DB_PATH)
    console.print(
        f"[green]✓[/green] Source {source_id} marked acquired → {file_path}"
    )


def mark_available(source_id: int, db_path: Path | None = None) -> None:
    """Mark a source as web-available (ready to scrape)."""
    update_source_status(source_id, "available", db_path=db_path or DB_PATH)
    console.print(f"[yellow]●[/yellow] Source {source_id} marked available")


if __name__ == "__main__":
    show_status()
