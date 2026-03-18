from reflexforge.types.proposal import Proposal


def run_cost_checks(proposal: Proposal) -> tuple[bool, dict[str, float], str]:
    token_cost = 0.2 if proposal.risk_level.value == "low" else 0.4
    memory_usage = 0.3 if proposal.risk_level.value == "low" else 0.5
    return True, {"token_cost": token_cost, "memory_usage": memory_usage}, "ok"
