from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from reflexforge.compat import Console

from reflexforge.attribution.credit import assign_credit
from reflexforge.compiler.spec_compiler import SpecCompiler
from reflexforge.config import Settings
from reflexforge.evaluator.layered_runner import LayeredEvaluator
from reflexforge.generator.proposal_generator import ProposalGenerator
from reflexforge.lineage.store import LineageStore
from reflexforge.memory.retrieval import LessonMemory
from reflexforge.policy.search_policy import choose_mode
from reflexforge.scorer.multi_objective import weighted_score
from reflexforge.scorer.pareto import pareto_front
from reflexforge.types.lineage import LineageRecord


@dataclass
class DemoResult:
    name: str
    best_id: str
    best_score: float
    pareto: list[str]

    def best_summary(self) -> str:
        return f"{self.name}: best={self.best_id} score={self.best_score:.3f} pareto={self.pareto}"


class Engine:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.console = Console()
        db_path = self._db_path_from_url(settings.engine.db_url)
        self.store = LineageStore(db_path=db_path)
        self.spec_compiler = SpecCompiler()
        self.generator = ProposalGenerator()
        self.evaluator = LayeredEvaluator()
        self.memory = LessonMemory()

    @staticmethod
    def _db_path_from_url(db_url: str) -> str:
        if "sqlite" in db_url and "///" in db_url:
            return db_url.split("///", maxsplit=1)[1]
        return "reflexforge.db"

    def run_demo_code(self) -> DemoResult:
        _ = self.spec_compiler.compile(
            name="demo-code",
            task_text="Optimize inefficient duplicate detector function.",
            objectives=["correctness", "speed", "maintainability"],
        )
        items = []
        best_id = ""
        best_score = float("-inf")
        for idx, proposal in enumerate(self.generator.code_proposals(), start=1):
            mode = choose_mode(idx, best_score if best_score != float("-inf") else 0.0)
            result = self.evaluator.evaluate(proposal)
            score = weighted_score(result.aggregate_metrics, self.settings.weights)
            items.append((proposal.proposal_id, result.aggregate_metrics))
            credit = assign_credit(proposal, result)
            self.memory.add(credit["reusable_lesson"])
            self.store.save(LineageRecord(
                proposal_id=proposal.proposal_id,
                parent_ids=proposal.parent_ids,
                mutation_type=f"{proposal.mutation_type}:{mode}",
                accepted=result.accepted,
                scores={"weighted": score, **result.aggregate_metrics},
                failure_reason=result.failure_reason,
                artifacts={"rationale": proposal.rationale},
            ))
            if result.accepted and score > best_score:
                best_score = score
                best_id = proposal.proposal_id

        p = pareto_front(items, maximize={"correctness", "quality", "speed", "maintainability", "robustness"}, minimize={"token_cost", "memory_usage"})
        return DemoResult("demo-code", best_id or "none", best_score if best_score != float("-inf") else 0.0, p)

    def run_demo_workflow(self) -> DemoResult:
        _ = self.spec_compiler.compile(
            name="demo-workflow",
            task_text="Optimize ingest->retrieve->summarize->verify DAG",
            objectives=["quality", "speed", "token_cost"],
        )
        items = []
        best_id = ""
        best_score = float("-inf")
        for idx, proposal in enumerate(self.generator.workflow_proposals(), start=1):
            mode = choose_mode(idx, best_score if best_score != float("-inf") else 0.0)
            result = self.evaluator.evaluate(proposal)
            metrics = dict(result.aggregate_metrics)
            metrics["quality"] = metrics.get("quality", 0.5) + 0.1
            score = metrics.get("quality", 0.0) - 0.5 * metrics.get("token_cost", 0.0) - 0.3 * (1 - metrics.get("speed", 0.0))
            items.append((proposal.proposal_id, metrics))
            credit = assign_credit(proposal, result)
            self.memory.add(credit["reusable_lesson"])
            self.store.save(LineageRecord(
                proposal_id=proposal.proposal_id,
                parent_ids=proposal.parent_ids,
                mutation_type=f"{proposal.mutation_type}:{mode}",
                accepted=result.accepted,
                scores={"workflow_objective": score, **metrics},
                failure_reason=result.failure_reason,
                artifacts={"nodes": proposal.payload.get("nodes", [])},
            ))
            if result.accepted and score > best_score:
                best_score = score
                best_id = proposal.proposal_id

        p = pareto_front(items, maximize={"quality", "speed", "robustness"}, minimize={"token_cost"})
        return DemoResult("demo-workflow", best_id or "none", best_score if best_score != float("-inf") else 0.0, p)

    def run_with_config(self) -> DemoResult:
        kind = (self.settings.task.kind or "code").lower()
        if kind == "workflow":
            return self.run_demo_workflow()
        return self.run_demo_code()

    def init_workspace(self) -> None:
        Path("artifacts").mkdir(exist_ok=True)
        self.console.print("[green]Initialized ReflexForge workspace[/green]")
