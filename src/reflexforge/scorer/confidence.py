def estimate_confidence(num_stages_passed: int, risk_level: str) -> float:
    base = min(1.0, num_stages_passed / 5)
    penalty = 0.0 if risk_level == "low" else 0.1 if risk_level == "medium" else 0.2
    return max(0.0, base - penalty)
