from __future__ import annotations

from reflexforge.lineage.store import LineageStore


def replay(store: LineageStore, proposal_id: str) -> list[dict[str, object]]:
    chain: list[dict[str, object]] = []
    current = store.get(proposal_id)
    while current:
        chain.append(current)
        raw = current.get("parent_ids", "")
        parent_ids = [p for p in str(raw).split(",") if p]
        if not parent_ids:
            break
        current = store.get(parent_ids[0])
    return chain
