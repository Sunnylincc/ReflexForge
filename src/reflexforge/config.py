from __future__ import annotations

from pathlib import Path
from reflexforge.compat import BaseModel, Field, yaml_safe_load


class EngineSettings(BaseModel):
    max_iterations: int = 5
    min_marginal_gain: float = 0.01
    db_url: str = "sqlite+aiosqlite:///./reflexforge.db"
    storage_backend: str = "sqlite"
    log_level: str = "INFO"


class TaskSettings(BaseModel):
    name: str = "demo"
    kind: str = "code"
    objectives: list[str] = Field(default_factory=list)
    budget: dict[str, int] = Field(default_factory=dict)


class Settings(BaseModel):
    engine: EngineSettings = Field(default_factory=EngineSettings)
    task: TaskSettings = Field(default_factory=TaskSettings)
    weights: dict[str, float] = Field(default_factory=dict)


def load_settings(path: str) -> Settings:
    raw = yaml_safe_load(Path(path).read_text())
    engine_raw = raw.get("engine", {}) if isinstance(raw, dict) else {}
    task_raw = raw.get("task", {}) if isinstance(raw, dict) else {}
    weights_raw = raw.get("weights", {}) if isinstance(raw, dict) else {}

    engine = EngineSettings(**engine_raw) if isinstance(engine_raw, dict) else EngineSettings()
    task = TaskSettings(**task_raw) if isinstance(task_raw, dict) else TaskSettings()
    safe_weights: dict[str, float] = {
        str(k): float(v) for k, v in weights_raw.items()
    } if isinstance(weights_raw, dict) else {}
    return Settings(engine=engine, task=task, weights=safe_weights)
