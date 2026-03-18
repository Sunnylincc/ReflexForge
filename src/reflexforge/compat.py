"""Compatibility shims for optional third-party dependencies.

Prefers real dependencies when installed. Falls back to tiny local
implementations that are sufficient for ReflexForge MVP tests/demos.
"""
from __future__ import annotations

from dataclasses import MISSING, asdict, dataclass, field, fields
from typing import Any, Callable

# pydantic compatibility
try:  # pragma: no cover - exercised when dependency exists
    from pydantic import BaseModel as BaseModel  # type: ignore
    from pydantic import Field as Field  # type: ignore
except Exception:  # pragma: no cover - offline fallback path
    def Field(default: Any = MISSING, default_factory: Callable[[], Any] | None = None) -> Any:
        if default_factory is not None:
            return field(default_factory=default_factory)
        if default is MISSING:
            return field(default=None)
        return field(default=default)

    class BaseModel:
        def __init_subclass__(cls) -> None:
            try:
                dataclass(cls, kw_only=True)
            except TypeError:
                pass

        @classmethod
        def model_validate(cls, data: dict[str, Any]) -> "BaseModel":
            kwargs: dict[str, Any] = {}
            for f in fields(cls):
                if f.name in data:
                    kwargs[f.name] = data[f.name]
            return cls(**kwargs)  # type: ignore[arg-type]

        def model_dump(self) -> dict[str, Any]:
            return asdict(self)


# YAML compatibility
try:  # pragma: no cover
    import yaml as _yaml  # type: ignore
except Exception:  # pragma: no cover
    _yaml = None


def _parse_scalar(value: str) -> Any:
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value.startswith("[") and value.endswith("]"):
        items = [x.strip() for x in value[1:-1].split(",") if x.strip()]
        return [i.strip('"\'') for i in items]
    num = value.lstrip("+-")
    if num.replace(".", "", 1).isdigit():
        return float(value) if "." in num else int(value)
    return value.strip('"\'')


def yaml_safe_load(text: str) -> dict[str, Any]:
    if _yaml is not None:
        loaded = _yaml.safe_load(text)
        return loaded if isinstance(loaded, dict) else {}

    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]
    for raw in text.splitlines():
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        key, _, tail = line.partition(":")
        key = key.strip()
        val = tail.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()
        current = stack[-1][1]

        if val == "":
            new: dict[str, Any] = {}
            current[key] = new
            stack.append((indent, new))
        else:
            current[key] = _parse_scalar(val)
    return root


# Rich compatibility
try:  # pragma: no cover
    from rich.console import Console as Console  # type: ignore
except Exception:  # pragma: no cover
    class Console:  # type: ignore[override]
        def print(self, *args: object, **kwargs: object) -> None:
            print(*args)
