from reflexforge.core.engine import Engine
from reflexforge.config import load_settings


def main() -> None:
    settings = load_settings("configs/default.yaml")
    engine = Engine(settings)
    result = engine.run_demo_code()
    print(result.best_summary())


if __name__ == "__main__":
    main()
