from __future__ import annotations

from reflexforge.compat import BaseModel, Field


class BudgetLimits(BaseModel):
    max_candidates: int = 10
    max_runtime_seconds: int = 60


class TaskSpec(BaseModel):
    name: str
    task_text: str
    primary_objectives: list[str]
    hard_constraints: list[str] = Field(default_factory=list)
    soft_preferences: list[str] = Field(default_factory=list)
    allowed_mutation_scopes: list[str] = Field(default_factory=lambda: ["code", "workflow", "evaluator", "resource", "memory"])
    budget_limits: BudgetLimits = Field(default_factory=BudgetLimits)
    safety_invariants: list[str] = Field(default_factory=list)
