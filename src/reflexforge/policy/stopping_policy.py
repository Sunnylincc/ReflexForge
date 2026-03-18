def should_stop(marginal_gain: float, min_gain: float, iteration: int, max_iterations: int) -> bool:
    return iteration >= max_iterations or marginal_gain < min_gain
