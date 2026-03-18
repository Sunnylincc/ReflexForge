from __future__ import annotations

from enum import Enum
from reflexforge.compat import BaseModel, Field


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class ProposalBase(BaseModel):
    proposal_id: str
    parent_ids: list[str] = Field(default_factory=list)
    rationale: str
    expected_gain: float
    risk_level: RiskLevel
    reversibility_score: float
    mutation_type: str = "mutate"


class CodePatchProposal(ProposalBase):
    patch: str


class WorkflowProposal(ProposalBase):
    payload: dict[str, object]


class EvaluatorProposal(ProposalBase):
    payload: dict[str, object]


class ResourcePolicyProposal(ProposalBase):
    payload: dict[str, object]


class MemoryPolicyProposal(ProposalBase):
    payload: dict[str, object]


Proposal = CodePatchProposal | WorkflowProposal | EvaluatorProposal | ResourcePolicyProposal | MemoryPolicyProposal
