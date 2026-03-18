from __future__ import annotations

from reflexforge.evaluator.static_checks import run_static_checks
from reflexforge.evaluator.unit_checks import run_unit_checks
from reflexforge.evaluator.smoke_checks import run_smoke_checks
from reflexforge.evaluator.benchmark_checks import run_benchmark_checks
from reflexforge.evaluator.cost_checks import run_cost_checks
from reflexforge.types.evaluation import EvaluationResult, StageResult
from reflexforge.types.proposal import Proposal


class LayeredEvaluator:
    def evaluate(self, proposal: Proposal) -> EvaluationResult:
        stages = []
        aggregate: dict[str, float] = {}

        for name, fn, stop_on_fail in [
            ("static", run_static_checks, True),
            ("unit", run_unit_checks, True),
            ("smoke", run_smoke_checks, True),
            ("benchmark", run_benchmark_checks, False),
            ("cost", run_cost_checks, False),
        ]:
            passed, metrics, msg = fn(proposal)
            stages.append(StageResult(stage=name, passed=passed, metrics=metrics, message=msg))
            aggregate.update(metrics)
            if stop_on_fail and not passed:
                return EvaluationResult(
                    proposal_id=proposal.proposal_id,
                    accepted=False,
                    stage_results=stages,
                    aggregate_metrics=aggregate,
                    failure_reason=f"failed_{name}",
                )

        return EvaluationResult(
            proposal_id=proposal.proposal_id,
            accepted=True,
            stage_results=stages,
            aggregate_metrics=aggregate,
        )
