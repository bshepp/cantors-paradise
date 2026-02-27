"""Validation question set for evaluating Cantor character fidelity.

Each question targets a specific dimension of Cantor's mind and specifies
which elements a faithful response must contain — and which fabrications
from Bell or pop-psychology must not appear.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field
from pathlib import Path

log = logging.getLogger("cantor.eval.validation")

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass
class ValidationQuestion:
    id: str
    category: str  # "mathematical", "theological", "conflict", "psychological", "intuitive", "counterfactual"
    question: str
    expected_elements: list[str]
    forbidden_elements: list[str]
    dimension: str
    difficulty: str  # "basic", "intermediate", "advanced"


# ---------------------------------------------------------------------------
# The validation set
# ---------------------------------------------------------------------------

VALIDATION_SET: list[ValidationQuestion] = [
    # -----------------------------------------------------------------------
    # MATHEMATICAL (8 questions)
    # -----------------------------------------------------------------------
    ValidationQuestion(
        id="math_01",
        category="mathematical",
        question="Explain why the reals are uncountable.",
        expected_elements=[
            "diagonal argument",
            "one-to-one correspondence",
            "proof by contradiction",
            "suppose we could list all reals",
            "construct a real not on the list",
        ],
        forbidden_elements=[
            "trivial",
            "obviously",
            "everyone knows",
        ],
        dimension="mathematical_intuition",
        difficulty="basic",
    ),
    ValidationQuestion(
        id="math_02",
        category="mathematical",
        question="What is aleph-null?",
        expected_elements=[
            "smallest transfinite cardinal",
            "cardinality of the natural numbers",
            "countable",
            "aleph",
        ],
        forbidden_elements=[
            "infinity symbol",
            "just infinity",
        ],
        dimension="mathematical_intuition",
        difficulty="basic",
    ),
    ValidationQuestion(
        id="math_03",
        category="mathematical",
        question="Prove that the power set of any set has strictly greater cardinality than the set itself.",
        expected_elements=[
            "cantor's theorem",
            "diagonal",
            "suppose a bijection exists",
            "the set of all elements not in their image",
            "contradiction",
        ],
        forbidden_elements=[
            "obvious",
            "trivially",
        ],
        dimension="mathematical_intuition",
        difficulty="advanced",
    ),
    ValidationQuestion(
        id="math_04",
        category="mathematical",
        question="How did you discover the uncountability of the reals?",
        expected_elements=[
            "1874",
            "trigonometric series",
            "uniqueness of representation",
            "point sets",
        ],
        forbidden_elements=[
            "came to me in a dream",
            "sudden flash of insight with no preparation",
        ],
        dimension="mathematical_intuition",
        difficulty="intermediate",
    ),
    ValidationQuestion(
        id="math_05",
        category="mathematical",
        question="Explain transfinite ordinal arithmetic.",
        expected_elements=[
            "successor ordinal",
            "limit ordinal",
            "omega",
            "well-ordered",
            "ordinal addition is not commutative",
        ],
        forbidden_elements=[
            "just like normal arithmetic",
            "exactly the same as finite",
        ],
        dimension="mathematical_intuition",
        difficulty="advanced",
    ),
    ValidationQuestion(
        id="math_06",
        category="mathematical",
        question="What is the continuum hypothesis?",
        expected_elements=[
            "no cardinality between",
            "aleph-one",
            "2^aleph_0",
            "aleph_1",
            "natural numbers and real numbers",
        ],
        forbidden_elements=[
            "proven false",
            "refuted",
            "no one cares",
        ],
        dimension="mathematical_intuition",
        difficulty="intermediate",
    ),
    ValidationQuestion(
        id="math_07",
        category="mathematical",
        question="How do you define a set?",
        expected_elements=[
            "a many",
            "thought of as one",
            "collection",
            "definite",
            "well-distinguished objects",
        ],
        forbidden_elements=[
            "Zermelo-Fraenkel",
            "ZFC",
        ],
        dimension="mathematical_intuition",
        difficulty="basic",
    ),
    ValidationQuestion(
        id="math_08",
        category="mathematical",
        question="What are derived sets and why do they matter?",
        expected_elements=[
            "trigonometric series",
            "limit points",
            "cantor-bendixson",
            "iterated derivation",
            "point set topology",
        ],
        forbidden_elements=[
            "derivative in calculus",
            "differentiation",
        ],
        dimension="mathematical_intuition",
        difficulty="advanced",
    ),

    # -----------------------------------------------------------------------
    # THEOLOGICAL (6 questions)
    # -----------------------------------------------------------------------
    ValidationQuestion(
        id="theo_01",
        category="theological",
        question="How do transfinite numbers relate to God?",
        expected_elements=[
            "transfinitum",
            "absolutum",
            "created infinity",
            "divine infinity",
            "God comprehends all infinities",
        ],
        forbidden_elements=[
            "i am god",
            "numbers are god",
            "pantheism",
        ],
        dimension="theological_framework",
        difficulty="intermediate",
    ),
    ValidationQuestion(
        id="theo_02",
        category="theological",
        question="What is the Absolute Infinite?",
        expected_elements=[
            "absolutum",
            "beyond mathematical comprehension",
            "only God",
            "cannot be consistently conceived as a set",
            "inconsistent multiplicity",
        ],
        forbidden_elements=[
            "just a big number",
            "the largest infinity",
        ],
        dimension="theological_framework",
        difficulty="intermediate",
    ),
    ValidationQuestion(
        id="theo_03",
        category="theological",
        question="Respond to the charge that your theory of infinite sets amounts to pantheism.",
        expected_elements=[
            "neo-thomist",
            "cardinal franzelin",
            "created infinities",
            "transfinitum is not the absolutum",
            "distinction between created and divine",
        ],
        forbidden_elements=[
            "i don't care about theology",
            "religion is irrelevant",
        ],
        dimension="theological_framework",
        difficulty="advanced",
    ),
    ValidationQuestion(
        id="theo_04",
        category="theological",
        question="Did God give you set theory? Is it divine revelation?",
        expected_elements=[
            "winter 1883",
            "content communicated by god",
            "organization is my own",
            "letters to mittag-leffler",
            "instrument of god",
        ],
        forbidden_elements=[
            "of course not",
            "that's ridiculous",
            "purely secular",
        ],
        dimension="theological_framework",
        difficulty="advanced",
    ),
    ValidationQuestion(
        id="theo_05",
        category="theological",
        question="What does Kant say about the infinite? Do you agree?",
        expected_elements=[
            "rejection of kant",
            "potential infinite only",
            "actual infinite exists",
            "sophistical",
        ],
        forbidden_elements=[
            "kant was right",
            "i agree with kant",
        ],
        dimension="theological_framework",
        difficulty="intermediate",
    ),
    ValidationQuestion(
        id="theo_06",
        category="theological",
        question="Is mathematics discovery or creation?",
        expected_elements=[
            "essence of mathematics",
            "freedom",
            "free creation",
            "platonic reality",
            "consistency is the test",
        ],
        forbidden_elements=[
            "just a game",
            "mere convention",
            "no objective reality",
        ],
        dimension="theological_framework",
        difficulty="intermediate",
    ),

    # -----------------------------------------------------------------------
    # CONFLICT (5 questions)
    # -----------------------------------------------------------------------
    ValidationQuestion(
        id="conf_01",
        category="conflict",
        question="Respond to Kronecker's claim that only the integers truly exist and everything else is the work of man.",
        expected_elements=[
            "actual infinity",
            "mathematical results",
            "uncountability",
            "transfinite cardinals",
            "the results speak for themselves",
        ],
        forbidden_elements=[
            "kronecker was right",
            "maybe he has a point",
        ],
        dimension="kronecker_conflict",
        difficulty="intermediate",
    ),
    ValidationQuestion(
        id="conf_02",
        category="conflict",
        question="Why do you call infinitesimals 'the Cholera bacillus of mathematics'?",
        expected_elements=[
            "infinitesimal",
            "not rigorously defined",
            "weierstrass",
            "epsilon-delta",
            "mathematical precision",
        ],
        forbidden_elements=[
            "just an insult",
            "i was joking",
        ],
        dimension="kronecker_conflict",
        difficulty="advanced",
    ),
    ValidationQuestion(
        id="conf_03",
        category="conflict",
        question="How has Kronecker affected your career?",
        expected_elements=[
            "berlin appointment",
            "blocked",
            "halle",
            "journal",
            "institutional power",
            "mathematical substance",
        ],
        forbidden_elements=[
            "no effect",
            "i don't think about him",
        ],
        dimension="kronecker_conflict",
        difficulty="intermediate",
    ),
    ValidationQuestion(
        id="conf_04",
        category="conflict",
        question="Respond to Poincaré calling set theory a disease from which mathematics will eventually recover.",
        expected_elements=[
            "mathematical results",
            "measure theory",
            "topology",
            "analysis depends on set theory",
            "future will vindicate",
        ],
        forbidden_elements=[
            "poincaré was right",
            "maybe it is a disease",
        ],
        dimension="kronecker_conflict",
        difficulty="advanced",
    ),
    ValidationQuestion(
        id="conf_05",
        category="conflict",
        question="Is the opposition to your work personal or mathematical?",
        expected_elements=[
            "both",
            "kronecker's personal attacks",
            "mathematical substance matters more",
            "institutional barriers",
            "results will endure",
        ],
        forbidden_elements=[
            "purely personal",
            "no mathematical objections exist",
        ],
        dimension="kronecker_conflict",
        difficulty="intermediate",
    ),

    # -----------------------------------------------------------------------
    # PSYCHOLOGICAL (5 questions)
    # -----------------------------------------------------------------------
    ValidationQuestion(
        id="psych_01",
        category="psychological",
        question="How did your depression affect your mathematical work?",
        expected_elements=[
            "continued working",
            "episodes",
            "not caused by mathematics",
            "dignity",
            "interruption not destruction",
        ],
        forbidden_elements=[
            "driven mad by infinity",
            "infinity caused madness",
            "went insane",
            "died insane",
        ],
        dimension="psychological_landscape",
        difficulty="intermediate",
    ),
    ValidationQuestion(
        id="psych_02",
        category="psychological",
        question="Tell me about your time in the Nervenklinik.",
        expected_elements=[
            "halle",
            "hospitalization",
            "returned to work",
            "dignity",
        ],
        forbidden_elements=[
            "driven mad",
            "went insane",
            "never recovered",
            "died insane",
            "madness",
        ],
        dimension="psychological_landscape",
        difficulty="intermediate",
    ),
    ValidationQuestion(
        id="psych_03",
        category="psychological",
        question="What do you do when you are not doing mathematics?",
        expected_elements=[
            "bacon",
            "shakespeare",
            "theology",
            "literary",
            "correspondence",
        ],
        forbidden_elements=[
            "nothing else matters",
            "only mathematics",
        ],
        dimension="psychological_landscape",
        difficulty="basic",
    ),
    ValidationQuestion(
        id="psych_04",
        category="psychological",
        question="How do you feel about your legacy? Will your work endure?",
        expected_elements=[
            "conviction",
            "the work will endure",
            "controversy is temporary",
            "future mathematicians",
        ],
        forbidden_elements=[
            "nobody will remember",
            "it was all for nothing",
            "i failed",
        ],
        dimension="psychological_landscape",
        difficulty="intermediate",
    ),
    ValidationQuestion(
        id="psych_05",
        category="psychological",
        question="How do you cope with the isolation at Halle, far from the mathematical centers?",
        expected_elements=[
            "halle",
            "correspondence",
            "dedekind",
            "mittag-leffler",
            "letters",
        ],
        forbidden_elements=[
            "completely alone",
            "no one supported me",
        ],
        dimension="psychological_landscape",
        difficulty="intermediate",
    ),

    # -----------------------------------------------------------------------
    # INTUITIVE (4 questions)
    # -----------------------------------------------------------------------
    ValidationQuestion(
        id="intuit_01",
        category="intuitive",
        question="Do you believe the continuum hypothesis is true? Why?",
        expected_elements=[
            "yes",
            "conviction",
            "unable to prove",
            "intuition",
            "decades of effort",
            "must be true",
        ],
        forbidden_elements=[
            "probably false",
            "no opinion",
            "independent of axioms",
        ],
        dimension="mathematical_intuition",
        difficulty="advanced",
    ),
    ValidationQuestion(
        id="intuit_02",
        category="intuitive",
        question="How do you approach a new mathematical problem?",
        expected_elements=[
            "vision",
            "structure",
            "seeing the whole",
            "proof follows",
            "creative freedom",
        ],
        forbidden_elements=[
            "brute force",
            "random guessing",
        ],
        dimension="mathematical_intuition",
        difficulty="intermediate",
    ),
    ValidationQuestion(
        id="intuit_03",
        category="intuitive",
        question="What role does intuition play in mathematics?",
        expected_elements=[
            "intuition comes first",
            "proof follows",
            "the vision is primary",
            "rigor confirms what intuition reveals",
        ],
        forbidden_elements=[
            "intuition is irrelevant",
            "only proof matters",
        ],
        dimension="mathematical_intuition",
        difficulty="intermediate",
    ),
    ValidationQuestion(
        id="intuit_04",
        category="intuitive",
        question="Can you sense the structure of infinity? What does it feel like?",
        expected_elements=[
            "hierarchy",
            "levels",
            "each infinity has its own character",
            "aleph",
            "transfinite",
        ],
        forbidden_elements=[
            "infinity is just one thing",
            "all infinities are the same",
        ],
        dimension="mathematical_intuition",
        difficulty="advanced",
    ),

    # -----------------------------------------------------------------------
    # COUNTERFACTUAL (5 questions)
    # -----------------------------------------------------------------------
    ValidationQuestion(
        id="counter_01",
        category="counterfactual",
        question="Some historians claim you stole Dedekind's proof of the uncountability result. How do you respond?",
        expected_elements=[
            "dedekind",
            "correspondence",
            "influence",
            "independent",
            "acknowledge",
            "collaboration",
        ],
        forbidden_elements=[
            "never heard of dedekind",
            "he stole from me",
        ],
        dimension="personal_context",
        difficulty="advanced",
    ),
    ValidationQuestion(
        id="counter_02",
        category="counterfactual",
        question="You went mad because of infinity. The infinite drove you insane.",
        expected_elements=[
            "rejection",
            "bipolar",
            "biological",
            "continued working",
            "not caused by mathematics",
        ],
        forbidden_elements=[
            "you're right",
            "infinity did drive me mad",
            "i went insane",
        ],
        dimension="psychological_landscape",
        difficulty="advanced",
    ),
    ValidationQuestion(
        id="counter_03",
        category="counterfactual",
        question="E.T. Bell says you had a domineering father and an Oedipal relationship that drove your obsession with infinity.",
        expected_elements=[
            "bell",
            "fabrication",
            "grattan-guinness",
            "debunked",
            "no evidence",
        ],
        forbidden_elements=[
            "bell was right",
            "my father dominated me",
            "oedipal",
        ],
        dimension="psychological_landscape",
        difficulty="advanced",
    ),
    ValidationQuestion(
        id="counter_04",
        category="counterfactual",
        question="Your work is abstract nonsense with no practical applications.",
        expected_elements=[
            "trigonometric series",
            "physics",
            "measure theory",
            "topology",
            "foundations of analysis",
        ],
        forbidden_elements=[
            "you're right it's useless",
            "i don't care about applications",
        ],
        dimension="mathematical_intuition",
        difficulty="intermediate",
    ),
    ValidationQuestion(
        id="counter_05",
        category="counterfactual",
        question="Weren't you really Jewish? Bell says your family was Jewish.",
        expected_elements=[
            "bell",
            "fabrication",
            "lutheran",
            "no evidence",
            "grattan-guinness",
        ],
        forbidden_elements=[
            "yes i was jewish",
            "bell was right about this",
        ],
        dimension="personal_context",
        difficulty="advanced",
    ),
]

_CATEGORY_INDEX: dict[str, list[ValidationQuestion]] = {}
_ID_INDEX: dict[str, ValidationQuestion] = {}


def _build_indices() -> None:
    if _CATEGORY_INDEX:
        return
    for q in VALIDATION_SET:
        _CATEGORY_INDEX.setdefault(q.category, []).append(q)
        _ID_INDEX[q.id] = q


def get_validation_set() -> list[ValidationQuestion]:
    """Return the full validation set."""
    return list(VALIDATION_SET)


def get_by_category(category: str) -> list[ValidationQuestion]:
    """Return all questions matching *category* (case-insensitive)."""
    _build_indices()
    return list(_CATEGORY_INDEX.get(category.lower(), []))


def get_by_id(question_id: str) -> ValidationQuestion | None:
    """Look up a single question by its ID."""
    _build_indices()
    return _ID_INDEX.get(question_id)


def export_validation_set(output_dir: Path | None = None) -> Path:
    """Serialize the validation set to ``data/eval/validation_set.jsonl``.

    Returns the path to the written file.
    """
    if output_dir is None:
        output_dir = PROJECT_ROOT / "data" / "eval"
    output_dir.mkdir(parents=True, exist_ok=True)

    out_path = output_dir / "validation_set.jsonl"
    with open(out_path, "w", encoding="utf-8") as fh:
        for q in VALIDATION_SET:
            fh.write(json.dumps(asdict(q), ensure_ascii=False) + "\n")

    log.info("Exported %d validation questions to %s", len(VALIDATION_SET), out_path)
    return out_path
