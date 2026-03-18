from reflexforge.types.proposal import Proposal


def run_benchmark_checks(proposal: Proposal) -> tuple[bool, dict[str, float], str]:
    speed = min(1.0, 0.4 + proposal.expected_gain)
    quality = min(1.0, 0.5 + proposal.expected_gain / 2)
    return True, {"speed": speed, "quality": quality}, "ok"
