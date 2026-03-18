from reflexforge.compiler.spec_compiler import SpecCompiler


def test_compile_spec_includes_core_fields() -> None:
    spec = SpecCompiler().compile("x", "optimize", ["speed"])
    assert spec.primary_objectives == ["speed"]
    assert spec.hard_constraints
    assert spec.safety_invariants
