from __future__ import annotations
from reflexforge.compat import BaseModel, Field


class EngineRunState(BaseModel):
    iteration: int = 0
    best_score: float = float("-inf")
    history: list[str] = Field(default_factory=list)
