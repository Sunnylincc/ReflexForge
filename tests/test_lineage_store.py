from reflexforge.lineage.store import LineageStore
from reflexforge.types.lineage import LineageRecord


def test_lineage_store_roundtrip(tmp_path) -> None:
    db = tmp_path / "test.db"
    store = LineageStore(str(db))
    store.save(
        LineageRecord(
            proposal_id="p1",
            mutation_type="mut",
            accepted=True,
            scores={"weighted": 0.9},
            artifacts={"nodes": ["a", "b"]},
        )
    )
    rec = store.get("p1")
    assert rec is not None
    assert rec["proposal_id"] == "p1"
    assert rec["scores"] == {"weighted": 0.9}
    assert rec["artifacts"] == {"nodes": ["a", "b"]}
