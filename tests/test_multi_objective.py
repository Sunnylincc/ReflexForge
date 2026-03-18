from reflexforge.scorer.multi_objective import weighted_score
from reflexforge.scorer.pareto import pareto_front


def test_weighted_score() -> None:
    score = weighted_score({"speed": 0.8, "token_cost": 0.2}, {"speed": 1.0, "token_cost": -1.0})
    assert score == 0.6


def test_pareto_front_non_empty() -> None:
    ids = pareto_front([
        ("a", {"quality": 0.8, "token_cost": 0.5}),
        ("b", {"quality": 0.7, "token_cost": 0.4}),
    ], maximize={"quality"}, minimize={"token_cost"})
    assert ids
