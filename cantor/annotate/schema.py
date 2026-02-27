"""Annotation schema: dimensions, subtags, and validation for segment annotations."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Dimension(str, Enum):
    MATHEMATICAL_INTUITION = "mathematical_intuition"
    THEOLOGICAL_FRAMEWORK = "theological_framework"
    KRONECKER_CONFLICT = "kronecker_conflict"
    PSYCHOLOGICAL_LANDSCAPE = "psychological_landscape"
    PERSONAL_CONTEXT = "personal_context"


SUBTAGS: dict[Dimension, list[str]] = {
    Dimension.MATHEMATICAL_INTUITION: [
        "diagonal_argument",
        "cardinality",
        "ordinals",
        "continuum_hypothesis",
        "well_ordering",
        "transfinite_arithmetic",
        "trigonometric_series",
        "set_theory",
        "uncountability",
        "power_set",
    ],
    Dimension.THEOLOGICAL_FRAMEWORK: [
        "absolutum",
        "transfinitum",
        "neo_thomism",
        "anti_kantianism",
        "platonic_realism",
        "divine_revelation",
        "spinoza",
        "leibniz",
        "mathematical_freedom",
    ],
    Dimension.KRONECKER_CONFLICT: [
        "finitism",
        "institutional_power",
        "combative_rhetoric",
        "mathematical_substance",
        "berlin_appointment",
        "constructivism",
    ],
    Dimension.PSYCHOLOGICAL_LANDSCAPE: [
        "depressive_episode",
        "productive_period",
        "hospitalization",
        "non_math_interests",
        "baconian_theory",
        "family",
    ],
    Dimension.PERSONAL_CONTEXT: [
        "halle_career",
        "family_life",
        "dmv_founding",
        "supporters",
        "st_petersburg",
        "lutheran_faith",
        "icm",
    ],
}

MATH_TOPICS: list[str] = [
    "set_theory",
    "cardinality",
    "ordinal_numbers",
    "cardinal_numbers",
    "transfinite_induction",
    "well_ordering_theorem",
    "continuum_hypothesis",
    "diagonal_argument",
    "uncountability",
    "countability",
    "trigonometric_series",
    "point_sets",
    "real_analysis",
    "topology",
    "power_set",
    "aleph_numbers",
    "beth_numbers",
    "ordinal_arithmetic",
    "cardinal_arithmetic",
    "axiom_of_choice",
    "zermelo_axioms",
    "burali_forti_paradox",
    "russell_paradox",
    "absolute_infinite",
]

HOSPITALIZATION_DATES: list[str] = [
    "1884-05",
    "1899",
    "1903",
    "1904",
    "1905",
    "1907",
    "1911",
    "1912",
    "1917-06",
]


@dataclass
class SegmentAnnotation:
    segment_id: int
    dimensions: list[Dimension] = field(default_factory=list)
    subtags: dict[Dimension, list[str]] = field(default_factory=dict)
    math_topics: list[str] = field(default_factory=list)
    psych_state: str = ""
    confidence: float = 0.0
    contradiction_flag: bool = False
    contradiction_ref: int | None = None
    notes: str = ""
    reviewer: str = "auto"


_TIER_CONFIDENCE: dict[int, float] = {
    1: 0.95,
    2: 0.85,
    3: 0.70,
    4: 0.65,
    5: 0.55,
    6: 0.35,
    7: 0.15,
    8: 0.00,
}


def confidence_from_tier(tier: int) -> float:
    """Map a source tier (1-8) to a confidence score."""
    return _TIER_CONFIDENCE.get(tier, 0.0)


def validate_annotation(ann: SegmentAnnotation) -> list[str]:
    """Return a list of validation errors (empty if valid)."""
    errors: list[str] = []

    if not ann.dimensions:
        errors.append("At least one dimension is required")

    for dim in ann.dimensions:
        if not isinstance(dim, Dimension):
            errors.append(f"Invalid dimension: {dim!r}")

    for dim, tags in ann.subtags.items():
        if dim not in Dimension:
            errors.append(f"Subtag key is not a valid dimension: {dim!r}")
            continue
        valid = SUBTAGS.get(dim, [])
        for tag in tags:
            if tag not in valid:
                errors.append(
                    f"Invalid subtag '{tag}' for dimension {dim.value}; "
                    f"valid: {valid}"
                )

    for topic in ann.math_topics:
        if topic not in MATH_TOPICS:
            errors.append(f"Invalid math_topic: '{topic}'")

    if not (0.0 <= ann.confidence <= 1.0):
        errors.append(
            f"Confidence must be between 0.0 and 1.0, got {ann.confidence}"
        )

    if ann.contradiction_flag and ann.contradiction_ref is None:
        errors.append(
            "contradiction_flag is set but contradiction_ref is None"
        )

    if ann.contradiction_ref is not None and not ann.contradiction_flag:
        errors.append(
            "contradiction_ref is set but contradiction_flag is False"
        )

    return errors
