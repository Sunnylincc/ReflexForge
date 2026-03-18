from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Lesson:
    key: str
    summary: str
    confidence: float
