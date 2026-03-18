from __future__ import annotations
from enum import Enum


class ObjectiveName(str, Enum):
    correctness = "correctness"
    quality = "quality"
    speed = "speed"
    token_cost = "token_cost"
    memory_usage = "memory_usage"
    maintainability = "maintainability"
    robustness = "robustness"
