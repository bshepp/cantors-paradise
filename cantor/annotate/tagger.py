"""Annotation tagger: rule-based and LLM-assisted segment classification."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from cantor.annotate.schema import (
    MATH_TOPICS,
    SUBTAGS,
    Dimension,
    SegmentAnnotation,
    confidence_from_tier,
    validate_annotation,
)
from cantor.db.schema import DB_PATH, get_connection

log = logging.getLogger("cantor.annotate.tagger")

# ---------------------------------------------------------------------------
# Keyword dictionaries for rule-based tagging
# ---------------------------------------------------------------------------

_DIMENSION_KEYWORDS: dict[Dimension, dict[str, list[str]]] = {
    Dimension.MATHEMATICAL_INTUITION: {
        "diagonal_argument": [
            "diagonal", "Diagonalverfahren", "diagonalization",
        ],
        "cardinality": [
            "cardinal", "Mächtigkeit", "cardinality", "equipollent",
            "gleichmächtig",
        ],
        "ordinals": [
            "ordinal", "Ordnungszahl", "ordinal number", "well-ordered",
            "wohlgeordnet",
        ],
        "continuum_hypothesis": [
            "continuum hypothesis", "Kontinuumhypothese", "Kontinuum",
            "continuum problem",
        ],
        "well_ordering": [
            "well-ordering", "Wohlordnung", "well ordering",
            "well ordered", "wohlgeordnet",
        ],
        "transfinite_arithmetic": [
            "transfinite", "transfinit", "aleph", "ℵ", "omega", "ω",
        ],
        "trigonometric_series": [
            "trigonometric", "trigonometrisch", "Fourier",
            "representation theorem",
        ],
        "set_theory": [
            "Mengenlehre", "set theory", "Mannigfaltigkeit", "manifold",
            "Inbegriff",
        ],
        "uncountability": [
            "uncountable", "überabzählbar", "uncountability",
            "non-denumerable",
        ],
        "power_set": [
            "power set", "Potenzmenge", "subset", "Teilmenge",
        ],
    },
    Dimension.THEOLOGICAL_FRAMEWORK: {
        "absolutum": [
            "Absolutum", "absolute infinite", "das Absolute",
        ],
        "transfinitum": [
            "Transfinitum", "transfinite", "transfinit",
        ],
        "neo_thomism": [
            "Aquinas", "Thomas", "Thomism", "Thomistic", "Franzelin",
            "neo-scholastic",
        ],
        "anti_kantianism": [
            "Kant", "Kantian", "anti-Kantian", "Critique",
            "pure reason",
        ],
        "platonic_realism": [
            "Plato", "Platonic", "realism", "Ideenlehre",
        ],
        "divine_revelation": [
            "God", "Gott", "divine", "göttlich", "revelation",
            "Offenbarung", "Creator", "Schöpfer",
        ],
        "spinoza": [
            "Spinoza", "pantheism", "Pantheismus",
        ],
        "leibniz": [
            "Leibniz", "monad", "Monade",
        ],
        "mathematical_freedom": [
            "free mathematics", "Freiheit", "freedom of mathematics",
            "essence of mathematics is freedom",
        ],
    },
    Dimension.KRONECKER_CONFLICT: {
        "finitism": [
            "finitist", "finitism", "finite", "Endlichkeit",
        ],
        "institutional_power": [
            "journal", "Zeitschrift", "publish", "appointment",
            "Berufung", "referee",
        ],
        "combative_rhetoric": [
            "charlatan", "Scharlatan", "corrupter of youth",
            "Jugendverderber", "cholera bacillus",
        ],
        "mathematical_substance": [
            "integers", "ganzen Zahlen", "constructive",
            "constructivism", "arithmetic",
        ],
        "berlin_appointment": [
            "Berlin", "Berliner", "chair", "Lehrstuhl",
        ],
        "constructivism": [
            "constructive", "constructivism", "konstruktiv",
        ],
    },
    Dimension.PSYCHOLOGICAL_LANDSCAPE: {
        "depressive_episode": [
            "depression", "depressive", "melancholy", "Melancholie",
            "breakdown", "Zusammenbruch", "nervous", "nervös",
        ],
        "productive_period": [
            "productive", "fruitful", "burst of work",
        ],
        "hospitalization": [
            "hospitalization", "Nervenklinik", "sanatorium",
            "clinic", "Klinik", "committed", "Halle Nervenklinik",
        ],
        "non_math_interests": [
            "Shakespeare", "Bacon", "Baconian", "Francis Bacon",
            "literary", "literature",
        ],
        "baconian_theory": [
            "Bacon", "Baconian", "Shakespeare authorship",
        ],
        "family": [
            "Rudolph", "children", "Kinder", "son", "daughter",
            "Sohn", "Tochter",
        ],
    },
    Dimension.PERSONAL_CONTEXT: {
        "halle_career": [
            "Halle", "Universität Halle", "ordinarius",
            "extraordinary professor",
        ],
        "family_life": [
            "Vally", "Guttmann", "wife", "Frau", "marriage",
            "wedding", "Hochzeit",
        ],
        "dmv_founding": [
            "DMV", "Mathematiker-Vereinigung",
            "Deutsche Mathematiker",
        ],
        "supporters": [
            "Dedekind", "Mittag-Leffler", "Hilbert", "Weierstrass",
            "supporter", "defended",
        ],
        "st_petersburg": [
            "St. Petersburg", "Sankt Petersburg", "Petersburg",
            "Russia", "Russland",
        ],
        "lutheran_faith": [
            "Lutheran", "lutherisch", "Protestant", "evangelisch",
            "faith", "Glaube",
        ],
        "icm": [
            "ICM", "congress", "Kongress",
            "International Congress",
        ],
    },
}

# Map keywords to math topics
_MATH_TOPIC_KEYWORDS: dict[str, list[str]] = {
    "set_theory": ["Mengenlehre", "set theory", "Mannigfaltigkeit"],
    "cardinality": ["cardinality", "Mächtigkeit", "equipollent"],
    "ordinal_numbers": ["ordinal number", "Ordnungszahl"],
    "cardinal_numbers": ["cardinal number", "Kardinalzahl"],
    "transfinite_induction": ["transfinite induction", "transfinite Induktion"],
    "well_ordering_theorem": ["well-ordering theorem", "Wohlordnungssatz"],
    "continuum_hypothesis": [
        "continuum hypothesis", "Kontinuumhypothese", "continuum problem",
    ],
    "diagonal_argument": ["diagonal", "Diagonalverfahren", "diagonalization"],
    "uncountability": ["uncountable", "überabzählbar", "non-denumerable"],
    "countability": ["countable", "abzählbar", "denumerable"],
    "trigonometric_series": ["trigonometric series", "trigonometrische Reihe"],
    "point_sets": ["point set", "Punktmenge"],
    "real_analysis": ["real analysis", "reelle Analysis", "real number"],
    "topology": ["topology", "Topologie", "connected", "zusammenhängend"],
    "power_set": ["power set", "Potenzmenge"],
    "aleph_numbers": ["aleph", "ℵ"],
    "beth_numbers": ["beth", "ℶ"],
    "ordinal_arithmetic": ["ordinal arithmetic", "ordinal addition"],
    "cardinal_arithmetic": ["cardinal arithmetic", "cardinal addition"],
    "axiom_of_choice": ["axiom of choice", "Auswahlaxiom"],
    "zermelo_axioms": ["Zermelo", "axiom system", "Axiomensystem"],
    "burali_forti_paradox": ["Burali-Forti", "greatest ordinal"],
    "russell_paradox": ["Russell", "Russell's paradox", "set of all sets"],
    "absolute_infinite": [
        "absolute infinite", "Absolutum", "Absolute Unendlichkeit",
    ],
}

# Kronecker-specific keywords kept separate for precise matching
_KRONECKER_KEYWORDS: list[str] = [
    "Kronecker", "finitist", "constructive", "integers",
    "ganzen Zahlen", "Berlin", "cholera bacillus",
]


# ---------------------------------------------------------------------------
# Rule-based tagger
# ---------------------------------------------------------------------------

class RuleBasedTagger:
    """Keyword-matching tagger that classifies segments along five dimensions."""

    def tag(self, segment_content: str, source_tier: int) -> SegmentAnnotation:
        text = segment_content
        text_lower = text.lower()

        detected_dims: list[Dimension] = []
        detected_subtags: dict[Dimension, list[str]] = {}

        for dim, subtag_keywords in _DIMENSION_KEYWORDS.items():
            dim_subtags: list[str] = []
            for subtag, keywords in subtag_keywords.items():
                for kw in keywords:
                    if kw.lower() in text_lower:
                        if subtag not in dim_subtags:
                            dim_subtags.append(subtag)
                        break
            if dim_subtags:
                detected_dims.append(dim)
                detected_subtags[dim] = dim_subtags

        detected_topics: list[str] = []
        for topic, keywords in _MATH_TOPIC_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in text_lower:
                    detected_topics.append(topic)
                    break

        psych_state = ""
        if Dimension.PSYCHOLOGICAL_LANDSCAPE in detected_dims:
            psych_subtags = detected_subtags.get(
                Dimension.PSYCHOLOGICAL_LANDSCAPE, []
            )
            if "depressive_episode" in psych_subtags:
                psych_state = "depressive episode indicated"
            elif "hospitalization" in psych_subtags:
                psych_state = "hospitalization period"
            elif "productive_period" in psych_subtags:
                psych_state = "productive period"
            else:
                psych_state = "psychological content present"

        return SegmentAnnotation(
            segment_id=0,
            dimensions=detected_dims,
            subtags=detected_subtags,
            math_topics=detected_topics,
            psych_state=psych_state,
            confidence=confidence_from_tier(source_tier),
            contradiction_flag=False,
            contradiction_ref=None,
            notes="rule-based tagging",
            reviewer="auto",
        )


# ---------------------------------------------------------------------------
# LLM-assisted tagger
# ---------------------------------------------------------------------------

_LLM_SYSTEM_PROMPT = """\
You are an expert annotator for historical texts about Georg Cantor and his mathematics.
Classify the following text segment along these five dimensions. For each dimension
that applies, list the relevant subtags.

Dimensions and valid subtags:
{dimensions_schema}

Valid math_topics:
{math_topics}

Respond with a JSON object:
{{
  "dimensions": ["dimension_value", ...],
  "subtags": {{"dimension_value": ["subtag", ...], ...}},
  "math_topics": ["topic", ...],
  "psych_state": "free text describing psychological state or empty string",
  "contradiction_flag": false,
  "notes": ""
}}
Only use values from the lists above. If a dimension does not apply, omit it.\
"""


def _build_llm_prompt() -> str:
    """Build the system prompt with full schema definitions."""
    dim_lines: list[str] = []
    for dim in Dimension:
        tags = SUBTAGS[dim]
        dim_lines.append(f"  {dim.value}: {tags}")
    dimensions_schema = "\n".join(dim_lines)
    return _LLM_SYSTEM_PROMPT.format(
        dimensions_schema=dimensions_schema,
        math_topics=MATH_TOPICS,
    )


class LLMTagger:
    """LLM-assisted tagger that uses an OpenAI-compatible API for classification."""

    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        api_key: str | None = None,
    ) -> None:
        self.model_name = model_name
        self.api_key = api_key
        self._fallback = RuleBasedTagger()
        self._system_prompt = _build_llm_prompt()

    def _call_llm(self, user_prompt: str) -> str:
        """Call the OpenAI-compatible API. Raises if not configured."""
        try:
            import openai  # noqa: F811
        except ImportError:
            raise RuntimeError(
                "The 'openai' package is required for LLM tagging. "
                "Install it with: pip install openai"
            )

        if not self.api_key:
            import os
            self.api_key = os.environ.get("OPENAI_API_KEY")

        if not self.api_key:
            raise RuntimeError(
                "No OpenAI API key provided. Pass api_key= or set "
                "the OPENAI_API_KEY environment variable."
            )

        client = openai.OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content or "{}"

    def _parse_response(
        self, raw_json: str, source_tier: int
    ) -> SegmentAnnotation:
        """Parse LLM JSON response into a SegmentAnnotation."""
        data = json.loads(raw_json)

        dimensions = [
            Dimension(d) for d in data.get("dimensions", [])
            if d in Dimension._value2member_map_
        ]

        subtags: dict[Dimension, list[str]] = {}
        for dim_str, tags in data.get("subtags", {}).items():
            if dim_str not in Dimension._value2member_map_:
                continue
            dim = Dimension(dim_str)
            valid = SUBTAGS.get(dim, [])
            subtags[dim] = [t for t in tags if t in valid]

        valid_topics = set(MATH_TOPICS)
        math_topics = [
            t for t in data.get("math_topics", []) if t in valid_topics
        ]

        return SegmentAnnotation(
            segment_id=0,
            dimensions=dimensions,
            subtags=subtags,
            math_topics=math_topics,
            psych_state=data.get("psych_state", ""),
            confidence=confidence_from_tier(source_tier),
            contradiction_flag=bool(data.get("contradiction_flag", False)),
            contradiction_ref=data.get("contradiction_ref"),
            notes=data.get("notes", ""),
            reviewer="auto",
        )

    def tag(self, segment_content: str, source_tier: int) -> SegmentAnnotation:
        try:
            raw = self._call_llm(segment_content)
            return self._parse_response(raw, source_tier)
        except Exception:
            log.warning(
                "LLM tagging failed, falling back to rule-based tagger",
                exc_info=True,
            )
            return self._fallback.tag(segment_content, source_tier)


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def save_annotation(
    ann: SegmentAnnotation, db_path: Path | None = None
) -> None:
    """Insert annotation rows into the database.

    One row per dimension, since the DB schema stores one dimension per row.
    """
    conn = get_connection(db_path or DB_PATH)
    try:
        math_topics_json = json.dumps(ann.math_topics)

        if not ann.dimensions:
            return

        for dim in ann.dimensions:
            subtags_json = json.dumps(ann.subtags.get(dim, []))
            conn.execute(
                """INSERT INTO annotations
                   (segment_id, dimension, subtags, math_topics,
                    psych_state, confidence, contradiction_flag,
                    contradiction_ref, notes, reviewer)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    ann.segment_id,
                    dim.value,
                    subtags_json,
                    math_topics_json,
                    ann.psych_state,
                    ann.confidence,
                    1 if ann.contradiction_flag else 0,
                    ann.contradiction_ref,
                    ann.notes,
                    ann.reviewer,
                ),
            )
        conn.commit()
    except Exception:
        conn.rollback()
        log.exception(
            "Failed to save annotation for segment %d", ann.segment_id
        )
        raise
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Batch tagging
# ---------------------------------------------------------------------------

def tag_all_segments(
    tagger_type: str = "rule", db_path: Path | None = None
) -> int:
    """Tag all unannotated segments in the database.

    Returns the number of segments tagged.
    """
    path = db_path or DB_PATH
    conn = get_connection(path)

    try:
        rows = conn.execute(
            """SELECT s.id, s.content, src.tier
               FROM segments s
               JOIN sources src ON s.source_id = src.id
               WHERE s.id NOT IN (
                   SELECT DISTINCT segment_id FROM annotations
               )"""
        ).fetchall()
    finally:
        conn.close()

    if not rows:
        log.info("No unannotated segments found")
        return 0

    if tagger_type == "llm":
        tagger: RuleBasedTagger | LLMTagger = LLMTagger()
    else:
        tagger = RuleBasedTagger()

    count = 0
    for row in rows:
        segment_id = row["id"]
        content = row["content"]
        tier = row["tier"]

        ann = tagger.tag(content, tier)
        ann.segment_id = segment_id

        errors = validate_annotation(ann)
        if errors:
            log.warning(
                "Validation errors for segment %d: %s", segment_id, errors
            )
            continue

        save_annotation(ann, path)
        count += 1

    log.info("Tagged %d segments using %s tagger", count, tagger_type)
    return count
