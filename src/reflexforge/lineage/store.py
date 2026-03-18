from __future__ import annotations

import json
import sqlite3
from reflexforge.types.lineage import LineageRecord


class LineageStore:
    def __init__(self, db_path: str = "reflexforge.db") -> None:
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        con = sqlite3.connect(self.db_path)
        con.execute(
            """CREATE TABLE IF NOT EXISTS lineage (
            proposal_id TEXT PRIMARY KEY,
            parent_ids TEXT,
            mutation_type TEXT,
            accepted INTEGER,
            scores TEXT,
            failure_reason TEXT,
            artifacts TEXT,
            timestamp TEXT
            )"""
        )
        con.commit()
        con.close()

    def save(self, record: LineageRecord) -> None:
        con = sqlite3.connect(self.db_path)
        con.execute(
            "INSERT OR REPLACE INTO lineage VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                record.proposal_id,
                ",".join(record.parent_ids),
                record.mutation_type,
                int(record.accepted),
                json.dumps(record.scores, sort_keys=True),
                record.failure_reason,
                json.dumps(record.artifacts, sort_keys=True),
                record.timestamp,
            ),
        )
        con.commit()
        con.close()

    def list_all(self) -> list[dict[str, object]]:
        con = sqlite3.connect(self.db_path)
        rows = con.execute(
            "SELECT proposal_id,parent_ids,mutation_type,accepted,scores,failure_reason,artifacts,timestamp "
            "FROM lineage ORDER BY timestamp"
        ).fetchall()
        con.close()
        return [
            {
                "proposal_id": r[0],
                "parent_ids": r[1],
                "mutation_type": r[2],
                "accepted": bool(r[3]),
                "scores": json.loads(r[4]) if r[4] else {},
                "failure_reason": r[5] or "",
                "artifacts": json.loads(r[6]) if r[6] else {},
                "timestamp": r[7],
            }
            for r in rows
        ]

    def get(self, proposal_id: str) -> dict[str, object] | None:
        con = sqlite3.connect(self.db_path)
        row = con.execute(
            "SELECT proposal_id,parent_ids,mutation_type,accepted,scores,failure_reason,artifacts,timestamp "
            "FROM lineage WHERE proposal_id = ?",
            (proposal_id,),
        ).fetchone()
        con.close()
        if row is None:
            return None
        return {
            "proposal_id": row[0],
            "parent_ids": row[1],
            "mutation_type": row[2],
            "accepted": bool(row[3]),
            "scores": json.loads(row[4]) if row[4] else {},
            "failure_reason": row[5] or "",
            "artifacts": json.loads(row[6]) if row[6] else {},
            "timestamp": row[7],
        }
