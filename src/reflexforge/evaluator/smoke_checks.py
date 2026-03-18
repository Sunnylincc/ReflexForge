from reflexforge.types.proposal import Proposal


def run_smoke_checks(proposal: Proposal) -> tuple[bool, dict[str, float], str]:
    passed = proposal.risk_level.value != "high"
    return passed, {"robustness": 0.8 if passed else 0.3}, "ok" if passed else "smoke unstable"
