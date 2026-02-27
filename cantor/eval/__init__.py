"""Evaluation module: validation questions and scoring for Cantor fidelity."""

from cantor.eval.evaluate import (
    EvaluationResult,
    evaluate_bell_test,
    evaluate_consistency,
    evaluate_dimension_coverage,
    evaluate_response,
    export_results,
    run_evaluation,
)
from cantor.eval.validation import (
    VALIDATION_SET,
    ValidationQuestion,
    export_validation_set,
    get_by_category,
    get_by_id,
    get_validation_set,
)

__all__ = [
    "EvaluationResult",
    "VALIDATION_SET",
    "ValidationQuestion",
    "evaluate_bell_test",
    "evaluate_consistency",
    "evaluate_dimension_coverage",
    "evaluate_response",
    "export_results",
    "export_validation_set",
    "get_by_category",
    "get_by_id",
    "get_validation_set",
    "run_evaluation",
]
