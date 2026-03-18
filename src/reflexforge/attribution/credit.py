from __future__ import annotations

from reflexforge.memory.patterns import Lesson
from reflexforge.types.evaluation import EvaluationResult
from reflexforge.types.proposal import Proposal
from reflexforge.attribution.failure_analysis import infer_failure_cause


def assign_credit(proposal: Proposal, result: EvaluationResult) -> dict[str, object]:
    passed = [s for s in result.stage_results if s.passed]
    cause = infer_failure_cause(result.failure_reason)
    confidence = min(1.0, 0.4 + len(passed) * 0.1)
    lesson = Lesson(
        key=proposal.mutation_type,
        summary=("helpful" if result.accepted else f"risky:{cause}"),
        confidence=confidence,
    )
    return {
        "likely_cause": cause,
        "changed_component": proposal.mutation_type,
        "confidence": confidence,
        "reusable_lesson": lesson,
    }
