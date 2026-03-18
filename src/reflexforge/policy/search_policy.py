from __future__ import annotations


def choose_mode(iteration: int, last_gain: float) -> str:
    if iteration < 2:
        return "explore"
    if last_gain > 0.05:
        return "exploit"
    if iteration % 3 == 0:
        return "escalate_redesign"
    return "explore_risky"
