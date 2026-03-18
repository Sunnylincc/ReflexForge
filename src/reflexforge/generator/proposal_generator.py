from __future__ import annotations

from reflexforge.types.proposal import CodePatchProposal, WorkflowProposal, RiskLevel


class ProposalGenerator:
    """Deterministic local proposal generation for MVP demos."""

    def code_proposals(self) -> list[CodePatchProposal]:
        return [
            CodePatchProposal(
                proposal_id="code-p1",
                parent_ids=["root"],
                rationale="Replace O(n^2) duplicate scan with set-based pass.",
                expected_gain=0.55,
                risk_level=RiskLevel.low,
                reversibility_score=0.95,
                patch="use set membership for duplicate checks",
                mutation_type="algorithmic_local",
            ),
            CodePatchProposal(
                proposal_id="code-p2",
                parent_ids=["root"],
                rationale="Inline caching for repeated normalization.",
                expected_gain=0.30,
                risk_level=RiskLevel.medium,
                reversibility_score=0.8,
                patch="memoize normalization",
                mutation_type="micro_optimization",
            ),
        ]

    def workflow_proposals(self) -> list[WorkflowProposal]:
        return [
            WorkflowProposal(
                proposal_id="wf-p1",
                parent_ids=["root-wf"],
                rationale="Insert lightweight validation before summarize.",
                expected_gain=0.35,
                risk_level=RiskLevel.low,
                reversibility_score=0.9,
                mutation_type="graph_insert",
                payload={"nodes": ["ingest", "retrieve", "verify_input", "summarize", "verify"]},
            ),
            WorkflowProposal(
                proposal_id="wf-p2",
                parent_ids=["root-wf"],
                rationale="Parallelize retrieve and heuristic context pruning.",
                expected_gain=0.45,
                risk_level=RiskLevel.medium,
                reversibility_score=0.7,
                mutation_type="graph_parallelize",
                payload={"nodes": ["ingest", "retrieve_parallel", "summarize", "verify"]},
            ),
        ]
