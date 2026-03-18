from __future__ import annotations
from reflexforge.compat import BaseModel, Field


class StageResult(BaseModel):
    stage: str
    passed: bool
    metrics: dict[str, float] = Field(default_factory=dict)
    message: str = ""


class EvaluationResult(BaseModel):
    proposal_id: str
    accepted: bool
    stage_results: list[StageResult]
    aggregate_metrics: dict[str, float] = Field(default_factory=dict)
    failure_reason: str | None = None
