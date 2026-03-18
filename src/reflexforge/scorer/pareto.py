from __future__ import annotations


def dominates(a: dict[str, float], b: dict[str, float], maximize: set[str], minimize: set[str]) -> bool:
    better_or_equal = True
    strictly_better = False
    for key in maximize:
        av, bv = a.get(key, 0.0), b.get(key, 0.0)
        if av < bv:
            better_or_equal = False
        if av > bv:
            strictly_better = True
    for key in minimize:
        av, bv = a.get(key, 0.0), b.get(key, 0.0)
        if av > bv:
            better_or_equal = False
        if av < bv:
            strictly_better = True
    return better_or_equal and strictly_better


def pareto_front(items: list[tuple[str, dict[str, float]]], maximize: set[str], minimize: set[str]) -> list[str]:
    front: list[str] = []
    for i, (pid, metrics) in enumerate(items):
        dominated = False
        for j, (_, other) in enumerate(items):
            if i == j:
                continue
            if dominates(other, metrics, maximize, minimize):
                dominated = True
                break
        if not dominated:
            front.append(pid)
    return front
