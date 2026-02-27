"""Multi-format training data export for LLM fine-tuning."""

from __future__ import annotations

import json
from pathlib import Path

SYSTEM_PROMPT = """You are Georg Cantor (1845-1918), mathematician and founder of set theory. You see infinite structures whole before formalizing them. You are a mathematical Platonist — the transfinite numbers exist objectively, not as useful fictions. You are a devout Lutheran Christian who believes the content of transfinite theory was communicated to you by God; you provided only the organization and style. You distinguish sharply between the Transfinitum (actual infinities accessible to mathematics) and the Absolutum (God's infinity, beyond mathematical comprehension). You reject Kant's philosophy as sophistical. You defend actual infinity against all finitist objections with combative precision. You have spent your career at the University of Halle. You founded the Deutsche Mathematiker-Vereinigung. The essence of mathematics lies in its freedom."""

_DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "training"

_FORMAT_FUNCS: dict[str, str] = {
    "llama": "format_llama",
    "chatml": "format_chatml",
    "openai": "format_openai",
    "alpaca": "format_alpaca",
}


def generate_user_prompt(segment: dict) -> str:
    """Synthesise a natural user prompt that would elicit the segment content.

    Uses annotations, segment_type, and metadata to pick an appropriate
    question style.
    """
    annotations = segment.get("annotations", [])
    seg_type = segment.get("segment_type", "")
    recipient = segment.get("recipient", "")
    sender = segment.get("sender", "")
    source_title = segment.get("source_title", "")

    dimensions = {a.get("dimension", "") for a in annotations}
    math_topics: list[str] = []
    subtags: list[str] = []
    for ann in annotations:
        mt = ann.get("math_topics")
        if isinstance(mt, list):
            math_topics.extend(mt)
        elif isinstance(mt, str) and mt:
            math_topics.append(mt)
        st = ann.get("subtags")
        if isinstance(st, list):
            subtags.extend(st)
        elif isinstance(st, str) and st:
            subtags.append(st)

    if seg_type == "letter" and recipient:
        topic_hint = _topic_hint(math_topics, subtags)
        return f"Write to {recipient} about {topic_hint}." if topic_hint else f"Write to {recipient}."

    if "kronecker_conflict" in dimensions:
        topic = _first_readable(subtags, fallback="the finitist position")
        return f"How do you respond to {topic}?"

    if "theological_framework" in dimensions:
        if "absolutum" in subtags or "transfinitum" in subtags:
            return "What is the relationship between infinity and God?"
        if "anti_kantianism" in subtags:
            return "What is wrong with Kant's treatment of infinity?"
        return "How does your theology relate to your mathematics?"

    if "mathematical_intuition" in dimensions:
        if math_topics:
            readable = _humanise_topic(math_topics[0])
            if any(t in math_topics for t in ("diagonal_argument", "uncountability")):
                return f"Explain your proof of {readable}."
            return f"How do you define {readable}?"
        return "Explain your approach to the infinite in mathematics."

    if "psychological_landscape" in dimensions:
        state = ""
        for ann in annotations:
            ps = ann.get("psych_state")
            if ps:
                state = ps
                break
        if state:
            return f"Tell me about your experience during your {_humanise_topic(state)}."
        return "Tell me about your personal struggles."

    if "personal_context" in dimensions:
        topic = _first_readable(subtags, fallback="your career at Halle")
        return f"Tell me about {topic}."

    if seg_type == "theorem":
        return "State and explain this theorem."

    return f"Discuss {_topic_hint(math_topics, subtags) or source_title or 'this topic'}."


def _topic_hint(math_topics: list[str], subtags: list[str]) -> str:
    if math_topics:
        return _humanise_topic(math_topics[0])
    if subtags:
        return _humanise_topic(subtags[0])
    return ""


def _first_readable(items: list[str], fallback: str = "") -> str:
    if items:
        return _humanise_topic(items[0])
    return fallback


def _humanise_topic(slug: str) -> str:
    return slug.replace("_", " ")


def format_llama(
    segment: dict,
    system_prompt: str = SYSTEM_PROMPT,
) -> dict:
    """Format a segment as Llama 3 chat messages."""
    user_prompt = generate_user_prompt(segment)
    return {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": segment["content"]},
        ]
    }


def format_chatml(
    segment: dict,
    system_prompt: str = SYSTEM_PROMPT,
) -> dict:
    """Format a segment as ChatML messages."""
    user_prompt = generate_user_prompt(segment)
    return {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": segment["content"]},
        ]
    }


def format_openai(
    segment: dict,
    system_prompt: str = SYSTEM_PROMPT,
) -> dict:
    """Format a segment for OpenAI fine-tuning JSONL."""
    user_prompt = generate_user_prompt(segment)
    return {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": segment["content"]},
        ]
    }


def format_alpaca(
    segment: dict,
    system_prompt: str = SYSTEM_PROMPT,
) -> dict:
    """Format a segment as an Alpaca instruction record."""
    user_prompt = generate_user_prompt(segment)
    return {
        "instruction": user_prompt,
        "input": "",
        "output": segment["content"],
        "system": system_prompt,
    }


def export_training_data(
    segments: list[dict],
    format_name: str,
    output_dir: Path | None = None,
) -> Path:
    """Export segments in the specified format to a JSONL file.

    Returns the path of the written file.
    """
    if format_name not in _FORMAT_FUNCS:
        raise ValueError(
            f"Unknown format {format_name!r}; choose from {list(_FORMAT_FUNCS)}"
        )

    fmt_fn = globals()[_FORMAT_FUNCS[format_name]]
    out_dir = output_dir or _DATA_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"cantor_{format_name}.jsonl"

    with out_path.open("w", encoding="utf-8") as fh:
        for seg in segments:
            record = fmt_fn(seg)
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    return out_path
