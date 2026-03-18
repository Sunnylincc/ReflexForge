from __future__ import annotations


def to_adjacency(records: list[dict[str, str]]) -> dict[str, list[str]]:
    graph: dict[str, list[str]] = {}
    for rec in records:
        parents = [p for p in rec.get("parent_ids", "").split(",") if p]
        graph[rec["proposal_id"]] = parents
    return graph
