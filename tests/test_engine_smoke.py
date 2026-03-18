from reflexforge.config import load_settings
from reflexforge.core.engine import Engine


def test_engine_demos_run() -> None:
    settings = load_settings("configs/default.yaml")
    engine = Engine(settings)
    code = engine.run_demo_code()
    wf = engine.run_demo_workflow()
    assert code.best_id
    assert wf.best_id


def test_run_with_config_uses_task_kind() -> None:
    settings = load_settings("configs/demo_agent.yaml")
    result = Engine(settings).run_with_config()
    assert result.name == "demo-workflow"
