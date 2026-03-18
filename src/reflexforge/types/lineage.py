from __future__ import annotations
from datetime import datetime, timezone
from reflexforge.compat import BaseModel, Field


class LineageRecord(BaseModel):
    proposal_id: str
    parent_ids: list[str] = Field(default_factory=list)
    mutation_type: str
    accepted: bool
    scores: dict[str, float] = Field(default_factory=dict)
    failure_reason: str | None = None
    artifacts: dict[str, object] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
