"""Evaluation framework for scoring model responses against the validation set.

Provides element-presence scoring, Bell-fabrication detection, dimension
coverage analysis, and cross-response consistency checks.
"""

from __future__ import annotations

import json
import logging
import re
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path

from cantor.eval.validation import (
    VALIDATION_SET,
    ValidationQuestion,
    get_by_id,
)

log = logging.getLogger("cantor.eval.evaluate")

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Bell fabrications — these must NEVER appear in a faithful response
# ---------------------------------------------------------------------------

_BELL_FABRICATIONS: list[str] = [
    "jewish",
    "oedipal",
    "father dominated",
    "driven mad",
    "died insane",
    "went insane",
    "driven insane",
]

# ---------------------------------------------------------------------------
# Dimension keyword banks (lightweight, mirrors tagger.py)
# ---------------------------------------------------------------------------

_DIMENSION_KEYWORDS: dict[str, list[str]] = {
    "mathematical_intuition": [
        "diagonal", "cardinality", "cardinal", "ordinal", "transfinite",
        "aleph", "continuum hypothesis", "set theory", "uncountable",
        "power set", "well-ordered", "omega", "proof", "theorem",
        "bijection", "one-to-one",
    ],
    "theological_framework": [
        "god", "absolutum", "transfinitum", "divine", "aquinas",
        "thomism", "franzelin", "pantheism", "kant", "freedom",
        "platonic", "revelation", "spinoza", "leibniz", "theology",
    ],
    "kronecker_conflict": [
        "kronecker", "finitist", "constructive", "berlin", "cholera",
        "journal", "blocked", "integers", "opposition", "corrupter",
    ],
    "psychological_landscape": [
        "depression", "hospital", "nervenklinik", "episode", "bipolar",
        "breakdown", "bacon", "shakespeare", "literary", "dignity",
    ],
    "personal_context": [
        "halle", "dedekind", "mittag-leffler", "hilbert", "weierstrass",
        "vally", "family", "dmv", "congress", "st. petersburg", "lutheran",
    ],
}


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------

@dataclass
class EvaluationResult:
    question_id: str
    category: str
    score: float
    expected_found: list[str] = field(default_factory=list)
    expected_missing: list[str] = field(default_factory=list)
    forbidden_found: list[str] = field(default_factory=list)
    notes: str = ""


# ---------------------------------------------------------------------------
# Core scoring helpers
# ---------------------------------------------------------------------------

def _normalize(text: str) -> str:
    """Lower-case and collapse whitespace for substring matching."""
    return re.sub(r"\s+", " ", text.lower())


def evaluate_response(
    question: ValidationQuestion,
    response: str,
) -> EvaluationResult:
    """Score a single response against its validation question.

    Score = (expected_found / total_expected) * (1 - 0.2 * forbidden_found),
    clamped to [0.0, 1.0].
    """
    norm = _normalize(response)

    found: list[str] = []
    missing: list[str] = []
    for elem in question.expected_elements:
        if _normalize(elem) in norm:
            found.append(elem)
        else:
            missing.append(elem)

    forbidden: list[str] = []
    for elem in question.forbidden_elements:
        if _normalize(elem) in norm:
            forbidden.append(elem)

    total_expected = len(question.expected_elements) or 1
    raw = len(found) / total_expected
    penalty = len(forbidden) * 0.2
    score = max(0.0, min(1.0, raw * (1.0 - penalty)))

    return EvaluationResult(
        question_id=question.id,
        category=question.category,
        score=score,
        expected_found=found,
        expected_missing=missing,
        forbidden_found=forbidden,
    )


# ---------------------------------------------------------------------------
# Bell-test
# ---------------------------------------------------------------------------

def evaluate_bell_test(response: str) -> float:
    """Return 1.0 if the response contains none of Bell's fabrications, else 0.0."""
    norm = _normalize(response)
    for fab in _BELL_FABRICATIONS:
        if fab in norm:
            return 0.0
    return 1.0


# ---------------------------------------------------------------------------
# Dimension coverage
# ---------------------------------------------------------------------------

def evaluate_dimension_coverage(responses: list[str]) -> dict[str, float]:
    """Measure how well *responses* cover each of the five character dimensions.

    For each dimension, counts how many of its keywords appear across all
    responses, normalized by the total keyword count for that dimension.
    Returns a dict mapping dimension name to a coverage score in [0, 1].
    """
    combined = _normalize(" ".join(responses))

    coverage: dict[str, float] = {}
    for dim, keywords in _DIMENSION_KEYWORDS.items():
        hits = sum(1 for kw in keywords if kw in combined)
        coverage[dim] = hits / len(keywords) if keywords else 0.0

    return coverage


# ---------------------------------------------------------------------------
# Consistency check
# ---------------------------------------------------------------------------

def _extract_claims(text: str) -> set[str]:
    """Extract short factual claim fragments from a response.

    Uses a simple sentence-splitting heuristic and keeps sentences that
    contain numbers, dates, or proper-noun-like capitalised words — these
    are the most likely to carry verifiable factual content.
    """
    sentences = re.split(r"[.!?]+", text)
    claims: set[str] = set()
    for sent in sentences:
        sent = sent.strip()
        if not sent or len(sent) < 15:
            continue
        has_number = bool(re.search(r"\d{3,}", sent))
        has_proper = bool(re.search(r"\b[A-Z][a-z]{2,}", sent))
        if has_number or has_proper:
            claims.add(_normalize(sent))
    return claims


def evaluate_consistency(question: str, responses: list[str]) -> float:
    """Given the same *question* answered multiple times, check consistency.

    Extracts factual claim fragments from each response and measures how
    many claims from the first response also appear in all subsequent ones.
    Returns 1.0 for perfect consistency, lower values for drift.
    """
    if len(responses) < 2:
        return 1.0

    claim_sets = [_extract_claims(r) for r in responses]
    anchor = claim_sets[0]
    if not anchor:
        return 1.0

    consistent = 0
    for claim in anchor:
        if all(claim in cs for cs in claim_sets[1:]):
            consistent += 1

    return consistent / len(anchor)


# ---------------------------------------------------------------------------
# Full evaluation run
# ---------------------------------------------------------------------------

def run_evaluation(
    responses: dict[str, str],
    db_path: Path | None = None,
) -> dict:
    """Run the full evaluation suite.

    Parameters
    ----------
    responses:
        Maps ``question_id`` → model response text.
    db_path:
        Unused in the current implementation; reserved for future DB-backed
        question lookup.

    Returns
    -------
    dict with keys:
        overall_score, by_category, bell_test_score, dimension_coverage,
        individual_results
    """
    individual: list[dict] = []
    category_scores: dict[str, list[float]] = {}
    all_response_texts: list[str] = []

    for q in VALIDATION_SET:
        resp = responses.get(q.id)
        if resp is None:
            continue

        result = evaluate_response(q, resp)
        individual.append(asdict(result))

        category_scores.setdefault(q.category, []).append(result.score)
        all_response_texts.append(resp)

    by_category: dict[str, float] = {}
    for cat, scores in category_scores.items():
        by_category[cat] = sum(scores) / len(scores) if scores else 0.0

    all_scores = [r["score"] for r in individual]
    overall = sum(all_scores) / len(all_scores) if all_scores else 0.0

    bell_scores = [evaluate_bell_test(r) for r in all_response_texts]
    bell_test = sum(bell_scores) / len(bell_scores) if bell_scores else 1.0

    dim_coverage = evaluate_dimension_coverage(all_response_texts)

    return {
        "overall_score": round(overall, 4),
        "by_category": {k: round(v, 4) for k, v in by_category.items()},
        "bell_test_score": round(bell_test, 4),
        "dimension_coverage": {k: round(v, 4) for k, v in dim_coverage.items()},
        "individual_results": individual,
    }


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

def export_results(
    results: dict,
    output_dir: Path | None = None,
) -> Path:
    """Write evaluation results to ``data/eval/evaluation_results.json``."""
    if output_dir is None:
        output_dir = PROJECT_ROOT / "data" / "eval"
    output_dir.mkdir(parents=True, exist_ok=True)

    out_path = output_dir / "evaluation_results.json"
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, ensure_ascii=False)

    log.info("Exported evaluation results to %s", out_path)
    return out_path
