from __future__ import annotations

from reflexforge.types.spec import TaskSpec


class SpecCompiler:
    """Compile user-facing task descriptions into executable optimization specs."""

    def compile(self, name: str, task_text: str, objectives: list[str]) -> TaskSpec:
        return TaskSpec(
            name=name,
            task_text=task_text,
            primary_objectives=objectives,
            hard_constraints=["must_pass_static_checks", "must_respect_budget"],
            soft_preferences=["prefer_reversible_mutations", "prefer_maintainable_changes"],
            safety_invariants=["never_disable_safety_checks", "preserve_public_interfaces"],
        )
