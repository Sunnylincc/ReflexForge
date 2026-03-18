from __future__ import annotations


def infer_failure_cause(stage: str | None) -> str:
    if stage is None:
        return "no_failure"
    if "static" in stage:
        return "safety_or_metadata_issue"
    if "unit" in stage:
        return "correctness_regression"
    if "smoke" in stage:
        return "runtime_stability_issue"
    return "unknown"
