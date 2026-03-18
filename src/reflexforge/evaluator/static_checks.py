from reflexforge.types.proposal import Proposal


def run_static_checks(proposal: Proposal) -> tuple[bool, dict[str, float], str]:
    safe = proposal.expected_gain > 0 and proposal.reversibility_score >= 0.5
    return safe, {"static_safety": 1.0 if safe else 0.0}, "ok" if safe else "unsafe metadata"
