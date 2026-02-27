"""CLI entry point for Cantor's Paradise."""

from __future__ import annotations

import json
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

console = Console()

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@click.group()
def cli() -> None:
    """Cantor's Paradise: Reconstructing a Mathematical Mind."""


# ---------------------------------------------------------------------------
# db commands
# ---------------------------------------------------------------------------
@cli.group()
def db() -> None:
    """Database operations."""


@db.command()
def init() -> None:
    """Initialize the database and seed the source catalog."""
    from cantor.db.seed_data import seed_database

    count = seed_database()
    console.print(f"[green]Database initialized with {count} sources.[/green]")


@db.command()
def status() -> None:
    """Show catalog statistics."""
    from cantor.db.catalog import get_catalog_stats

    stats = get_catalog_stats()
    table = Table(title="Source Catalog")
    table.add_column("Metric", style="bold")
    table.add_column("Value", justify="right")
    table.add_row("Total sources", str(stats["total"]))
    table.add_section()

    tier_labels = {
        1: "Cantor's own words",
        2: "Direct correspondents",
        3: "Mathematical opponents",
        4: "Catholic theologians",
        5: "Serious scholarship",
        6: "Secondary exposition",
        7: "Popular accounts",
        8: "Bell (EXCLUDED)",
    }
    for tier, count in sorted(stats["by_tier"].items()):
        label = tier_labels.get(tier, f"Tier {tier}")
        table.add_row(f"  Tier {tier}: {label}", str(count))
    table.add_section()
    for st, count in sorted(stats["by_status"].items()):
        table.add_row(f"  Status: {st}", str(count))
    console.print(table)


@db.command("list")
@click.option("--tier", type=int, help="Filter by tier number")
@click.option("--status", "acq_status", type=str, help="Filter by acquisition status")
def list_sources(tier: int | None, acq_status: str | None) -> None:
    """List sources in the catalog."""
    from cantor.db.catalog import get_all_sources, get_sources_by_tier, get_sources_by_status

    if tier is not None:
        sources = get_sources_by_tier(tier)
    elif acq_status is not None:
        sources = get_sources_by_status(acq_status)
    else:
        sources = get_all_sources()

    table = Table(title=f"Sources ({len(sources)})")
    table.add_column("ID", justify="right", width=4)
    table.add_column("Tier", justify="center", width=4)
    table.add_column("Title", max_width=60)
    table.add_column("Author", max_width=25)
    table.add_column("Status", width=10)
    for s in sources:
        style = "dim" if s.acquisition_status == "excluded" else ""
        table.add_row(str(s.id or ""), str(s.tier), s.title, s.author, s.acquisition_status, style=style)
    console.print(table)


# ---------------------------------------------------------------------------
# acquire commands
# ---------------------------------------------------------------------------
@cli.group()
def acquire() -> None:
    """Acquire source materials."""


@acquire.command()
def jamesrmeyer() -> None:
    """Scrape Cantor's papers from jamesrmeyer.com."""
    import asyncio
    from cantor.acquire.jamesrmeyer import JamesRMeyerScraper

    scraper = JamesRMeyerScraper()
    asyncio.run(scraper.run())
    console.print("[green]jamesrmeyer.com scraping complete.[/green]")


@acquire.command("archive-org")
def archive_org() -> None:
    """Download public domain texts from archive.org."""
    import asyncio
    from cantor.acquire.archive_org import ArchiveOrgScraper

    scraper = ArchiveOrgScraper()
    asyncio.run(scraper.run())
    console.print("[green]archive.org download complete.[/green]")


@acquire.command()
def arxiv() -> None:
    """Download papers from arXiv."""
    import asyncio
    from cantor.acquire.arxiv import ArxivScraper

    scraper = ArxivScraper()
    asyncio.run(scraper.run())
    console.print("[green]arXiv download complete.[/green]")


@acquire.command()
def mactutors() -> None:
    """Scrape MacTutor biography."""
    import asyncio
    from cantor.acquire.mactutors import MacTutorScraper

    scraper = MacTutorScraper()
    asyncio.run(scraper.run())
    console.print("[green]MacTutor scraping complete.[/green]")


@acquire.command("status")
def acquire_status() -> None:
    """Show acquisition status for all sources."""
    from cantor.acquire.tracker import show_status

    show_status()


@acquire.command("all")
def acquire_all() -> None:
    """Run all web scrapers."""
    import asyncio
    from cantor.acquire.jamesrmeyer import JamesRMeyerScraper
    from cantor.acquire.archive_org import ArchiveOrgScraper
    from cantor.acquire.arxiv import ArxivScraper
    from cantor.acquire.mactutors import MacTutorScraper

    scrapers = [
        ("jamesrmeyer.com", JamesRMeyerScraper()),
        ("archive.org", ArchiveOrgScraper()),
        ("arXiv", ArxivScraper()),
        ("MacTutor", MacTutorScraper()),
    ]
    for name, scraper in scrapers:
        console.print(f"[cyan]Scraping {name}...[/cyan]")
        try:
            asyncio.run(scraper.run())
            console.print(f"  [green]{name} complete.[/green]")
        except Exception as e:
            console.print(f"  [red]{name} failed: {e}[/red]")
    console.print("[green]All acquisition complete.[/green]")


# ---------------------------------------------------------------------------
# process commands
# ---------------------------------------------------------------------------
@cli.group()
def process() -> None:
    """Process acquired source texts."""


@process.command()
def extract() -> None:
    """Extract text from all acquired sources."""
    from cantor.process.extract import process_all_raw

    results = process_all_raw()
    table = Table(title=f"Extracted {len(results)} files")
    table.add_column("Source", max_width=50)
    table.add_column("Format", width=6)
    table.add_column("Characters", justify="right")
    for r in results:
        table.add_row(str(r["source_file"]), r["format"], f'{r["char_count"]:,}')
    console.print(table)


@process.command()
@click.option("--format-hint", default="paper", help="Segmentation format hint")
def segment(format_hint: str) -> None:
    """Segment extracted texts into training units."""
    from cantor.process.segment import auto_segment, save_segments, Segment
    from cantor.db.catalog import get_all_sources
    from cantor.db.schema import get_connection, DB_PATH

    processed_dir = DATA_DIR / "processed"
    if not processed_dir.exists():
        console.print("[yellow]No processed files found. Run 'cantor process extract' first.[/yellow]")
        return

    total = 0
    for txt_file in processed_dir.rglob("*.txt"):
        content = txt_file.read_text(encoding="utf-8", errors="replace")
        if not content.strip():
            continue
        segments = auto_segment(content, source_id=0, format_hint=format_hint)
        if segments:
            save_segments(segments)
            total += len(segments)
            console.print(f"  {txt_file.name}: {len(segments)} segments")

    console.print(f"[green]Created {total} segments total.[/green]")


# ---------------------------------------------------------------------------
# annotate commands
# ---------------------------------------------------------------------------
@cli.group()
def annotate() -> None:
    """Annotate segments."""


@annotate.command()
@click.option("--tagger", default="rule", type=click.Choice(["rule", "llm"]), help="Tagger type")
def tag(tagger: str) -> None:
    """Run annotation tagger on all unannotated segments."""
    from cantor.annotate.tagger import tag_all_segments

    count = tag_all_segments(tagger_type=tagger)
    console.print(f"[green]Tagged {count} segments.[/green]")


@annotate.command()
def review() -> None:
    """Review annotations (interactive)."""
    from cantor.db.schema import get_connection, DB_PATH

    conn = get_connection()
    rows = conn.execute(
        """SELECT a.id, s.title, a.dimension, a.subtags, a.confidence, a.reviewer
           FROM annotations a JOIN segments s ON a.segment_id = s.id
           WHERE a.reviewer = 'auto'
           ORDER BY a.confidence ASC LIMIT 20"""
    ).fetchall()
    conn.close()

    if not rows:
        console.print("[green]No annotations pending review.[/green]")
        return

    table = Table(title="Annotations pending review (lowest confidence first)")
    table.add_column("ID", justify="right", width=5)
    table.add_column("Segment", max_width=40)
    table.add_column("Dimension", width=25)
    table.add_column("Subtags", max_width=30)
    table.add_column("Confidence", justify="right", width=10)
    for r in rows:
        table.add_row(str(r["id"]), r["title"] or "(untitled)", r["dimension"], r["subtags"] or "", f'{r["confidence"]:.2f}')
    console.print(table)


# ---------------------------------------------------------------------------
# training commands
# ---------------------------------------------------------------------------
@cli.group()
def training() -> None:
    """Build training data."""


@training.command()
@click.option("--format", "fmt", default="llama", type=click.Choice(["llama", "chatml", "openai", "alpaca"]))
@click.option("--oversample", default=3.0, type=float, help="Tier 1 oversample multiplier")
def build(fmt: str, oversample: float) -> None:
    """Build weighted training set from annotated segments."""
    from cantor.training.sampler import WeightedSampler
    from cantor.training.formatter import export_training_data

    sampler = WeightedSampler(oversample_tier1=oversample)
    pool = sampler.build_training_pool()
    if not pool:
        console.print("[yellow]No segments in database. Run acquisition and processing first.[/yellow]")
        return

    train_set, val_set = sampler.split_train_val()
    train_path = export_training_data(train_set, fmt)
    console.print(f"[green]Training set: {len(train_set)} examples -> {train_path}[/green]")
    if val_set:
        val_path = export_training_data(val_set, f"{fmt}_val")
        console.print(f"[green]Validation set: {len(val_set)} examples -> {val_path}[/green]")


@training.command("synthetic")
def build_synthetic() -> None:
    """Generate synthetic training dialogues."""
    from cantor.training.synthetic import generate_all, export_synthetic

    examples = generate_all()
    path = export_synthetic(examples)
    table = Table(title=f"Synthetic examples: {len(examples)}")
    table.add_column("Category")
    table.add_column("Count", justify="right")
    counts: dict[str, int] = {}
    for ex in examples:
        counts[ex.category] = counts.get(ex.category, 0) + 1
    for cat, cnt in sorted(counts.items()):
        table.add_row(cat, str(cnt))
    console.print(table)
    console.print(f"[green]Exported to {path}[/green]")


@training.command("negative")
def build_negative() -> None:
    """Generate negative/contrastive training examples."""
    from cantor.training.negative import generate_all_negative, export_negative

    examples = generate_all_negative()
    path = export_negative(examples)
    table = Table(title=f"Contrastive examples: {len(examples)}")
    table.add_column("Category")
    table.add_column("Count", justify="right")
    counts: dict[str, int] = {}
    for ex in examples:
        counts[ex.category] = counts.get(ex.category, 0) + 1
    for cat, cnt in sorted(counts.items()):
        table.add_row(cat, str(cnt))
    console.print(table)
    console.print(f"[green]Exported to {path}[/green]")


# ---------------------------------------------------------------------------
# finetune commands
# ---------------------------------------------------------------------------
@cli.group()
def finetune() -> None:
    """Fine-tune a language model."""


@finetune.command("presets")
def show_presets() -> None:
    """Show available model presets."""
    from cantor.finetune.config import PRESETS

    table = Table(title="Model Presets")
    table.add_column("Preset", style="bold")
    table.add_column("Base Model")
    table.add_column("LoRA Rank", justify="right")
    table.add_column("4-bit", justify="center")
    table.add_column("Batch Size", justify="right")
    for name, cfg in PRESETS.items():
        table.add_row(name, cfg.base_model, str(cfg.lora_rank), "yes" if cfg.use_4bit else "no", str(cfg.per_device_batch_size))
    console.print(table)


@finetune.command("train")
@click.option("--preset", default="8b-qlora", help="Model preset name")
@click.option("--base-model", default=None, help="Override base model path/name")
@click.option("--train-data", required=True, type=click.Path(exists=True), help="Training data JSONL path")
@click.option("--val-data", default=None, type=click.Path(exists=True), help="Validation data JSONL path")
@click.option("--epochs", default=None, type=int, help="Override number of epochs")
def train_model(preset: str, base_model: str | None, train_data: str, val_data: str | None, epochs: int | None) -> None:
    """Fine-tune with LoRA/QLoRA."""
    from cantor.finetune.config import PRESETS, ModelConfig
    from cantor.finetune.train import train

    cfg = PRESETS.get(preset, ModelConfig())
    if base_model:
        cfg.base_model = base_model
    if epochs:
        cfg.num_epochs = epochs

    console.print(f"[cyan]Starting fine-tune: {cfg.base_model}[/cyan]")
    console.print(f"  LoRA rank={cfg.lora_rank}, 4-bit={'yes' if cfg.use_4bit else 'no'}")
    output = train(cfg, Path(train_data), Path(val_data) if val_data else None)
    console.print(f"[green]Training complete. Adapter saved to {output}[/green]")


@finetune.command("merge")
@click.option("--preset", default="8b-qlora", help="Model preset used for training")
@click.option("--adapter-path", required=True, type=click.Path(exists=True), help="Path to LoRA adapter")
@click.option("--output-path", required=True, type=click.Path(), help="Output path for merged model")
def merge_model(preset: str, adapter_path: str, output_path: str) -> None:
    """Merge LoRA adapter into base model."""
    from cantor.finetune.config import PRESETS, ModelConfig
    from cantor.finetune.train import merge_and_save

    cfg = PRESETS.get(preset, ModelConfig())
    merge_and_save(cfg, Path(adapter_path), Path(output_path))
    console.print(f"[green]Merged model saved to {output_path}[/green]")


# ---------------------------------------------------------------------------
# eval commands
# ---------------------------------------------------------------------------
@cli.group("eval")
def eval_cmd() -> None:
    """Evaluate model outputs."""


@eval_cmd.command("questions")
@click.option("--category", default=None, help="Filter by category")
def show_questions(category: str | None) -> None:
    """Show validation questions."""
    from cantor.eval.validation import get_validation_set, get_by_category

    questions = get_by_category(category) if category else get_validation_set()
    table = Table(title=f"Validation Questions ({len(questions)})")
    table.add_column("ID", width=12)
    table.add_column("Category", width=15)
    table.add_column("Difficulty", width=12)
    table.add_column("Question", max_width=60)
    for q in questions:
        table.add_row(q.id, q.category, q.difficulty, q.question)
    console.print(table)


@eval_cmd.command("export-questions")
def export_questions() -> None:
    """Export validation question set to JSONL."""
    from cantor.eval.validation import export_validation_set

    path = export_validation_set()
    console.print(f"[green]Validation set exported to {path}[/green]")


@eval_cmd.command("run")
@click.option("--responses-file", required=True, type=click.Path(exists=True), help="JSONL file with model responses (question_id, response)")
def run_eval(responses_file: str) -> None:
    """Evaluate model responses against validation set."""
    from cantor.eval.evaluate import run_evaluation, export_results

    responses: dict[str, str] = {}
    with open(responses_file, encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line.strip())
            responses[obj["question_id"]] = obj["response"]

    results = run_evaluation(responses)
    path = export_results(results)

    console.print(f"\n[bold]Evaluation Results[/bold]")
    console.print(f"  Overall score: [cyan]{results['overall_score']:.2%}[/cyan]")
    console.print(f"  Bell test: [{'green' if results['bell_test_score'] == 1.0 else 'red'}]{results['bell_test_score']:.2%}[/]")
    console.print(f"\n  By category:")
    for cat, score in results.get("by_category", {}).items():
        console.print(f"    {cat}: {score:.2%}")
    console.print(f"\n  Dimension coverage:")
    for dim, score in results.get("dimension_coverage", {}).items():
        console.print(f"    {dim}: {score:.2%}")
    console.print(f"\n[green]Full results saved to {path}[/green]")


# ---------------------------------------------------------------------------
# pipeline command — run the full pipeline
# ---------------------------------------------------------------------------
@cli.command()
@click.option("--format", "fmt", default="llama", type=click.Choice(["llama", "chatml", "openai", "alpaca"]))
def pipeline(fmt: str) -> None:
    """Run the full data pipeline: init -> acquire -> extract -> segment -> annotate -> build."""
    from cantor.db.seed_data import seed_database
    from cantor.process.extract import process_all_raw
    from cantor.process.segment import auto_segment, save_segments
    from cantor.annotate.tagger import tag_all_segments
    from cantor.training.sampler import WeightedSampler
    from cantor.training.formatter import export_training_data
    from cantor.training.synthetic import generate_all, export_synthetic
    from cantor.training.negative import generate_all_negative, export_negative

    console.print("[bold cyan]Step 1/7: Initialize database[/bold cyan]")
    count = seed_database()
    console.print(f"  {count} sources loaded")

    console.print("\n[bold cyan]Step 2/7: Acquire web sources[/bold cyan]")
    console.print("  [dim]Run 'cantor acquire all' separately for web scraping[/dim]")

    console.print("\n[bold cyan]Step 3/7: Extract text[/bold cyan]")
    results = process_all_raw()
    console.print(f"  {len(results)} files extracted")

    console.print("\n[bold cyan]Step 4/7: Segment texts[/bold cyan]")
    processed_dir = DATA_DIR / "processed"
    seg_total = 0
    if processed_dir.exists():
        for txt_file in processed_dir.rglob("*.txt"):
            content = txt_file.read_text(encoding="utf-8", errors="replace")
            if content.strip():
                segs = auto_segment(content, source_id=0)
                if segs:
                    save_segments(segs)
                    seg_total += len(segs)
    console.print(f"  {seg_total} segments created")

    console.print("\n[bold cyan]Step 5/7: Annotate segments[/bold cyan]")
    tagged = tag_all_segments(tagger_type="rule")
    console.print(f"  {tagged} segments annotated")

    console.print("\n[bold cyan]Step 6/7: Generate synthetic data[/bold cyan]")
    synth = generate_all()
    synth_path = export_synthetic(synth)
    console.print(f"  {len(synth)} synthetic examples -> {synth_path}")
    neg = generate_all_negative()
    neg_path = export_negative(neg)
    console.print(f"  {len(neg)} contrastive examples -> {neg_path}")

    console.print("\n[bold cyan]Step 7/7: Build training set[/bold cyan]")
    sampler = WeightedSampler()
    pool = sampler.build_training_pool()
    if pool:
        train_set, val_set = sampler.split_train_val()
        train_path = export_training_data(train_set, fmt)
        console.print(f"  {len(train_set)} training examples -> {train_path}")
    else:
        console.print("  [yellow]No segments available for training set (acquire sources first)[/yellow]")

    console.print("\n[bold green]Pipeline complete.[/bold green]")


if __name__ == "__main__":
    cli()
