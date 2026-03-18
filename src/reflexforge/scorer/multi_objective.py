from __future__ import annotations


def weighted_score(metrics: dict[str, float], weights: dict[str, float]) -> float:
    return round(sum(metrics.get(k, 0.0) * w for k, w in weights.items()), 10)
