from __future__ import annotations

import json
from pathlib import Path


def write_artifact(path: str, payload: dict[str, object]) -> None:
    Path(path).write_text(json.dumps(payload, indent=2))
