from reflexforge.types.proposal import Proposal


def run_unit_checks(proposal: Proposal) -> tuple[bool, dict[str, float], str]:
    passed = "disable" not in proposal.rationale.lower()
    return passed, {"correctness": 0.9 if passed else 0.2}, "ok" if passed else "unit check failed"
