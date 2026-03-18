from __future__ import annotations

import argparse
from reflexforge.compat import Console

from reflexforge.config import load_settings
from reflexforge.core.engine import Engine
from reflexforge.lineage.replay import replay
from reflexforge.lineage.store import LineageStore

console = Console()


def app() -> None:
    parser = argparse.ArgumentParser(prog="reflexforge")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init")

    run_p = sub.add_parser("run")
    run_p.add_argument("--config", required=True)

    demo_p = sub.add_parser("demo")
    demo_p.add_argument("target", choices=["code", "workflow"])

    lineage_p = sub.add_parser("lineage")
    lineage_p.add_argument("--config", default="configs/default.yaml")
    lineage_sub = lineage_p.add_subparsers(dest="lineage_cmd", required=True)
    lineage_sub.add_parser("show")
    replay_p = lineage_sub.add_parser("replay")
    replay_p.add_argument("proposal_id")

    args = parser.parse_args()

    if args.cmd == "init":
        engine = Engine(load_settings("configs/default.yaml"))
        engine.init_workspace()
    elif args.cmd == "run":
        settings = load_settings(args.config)
        result = Engine(settings).run_with_config()
        console.print(result.best_summary())
    elif args.cmd == "demo":
        engine = Engine(load_settings("configs/default.yaml"))
        result = engine.run_demo_code() if args.target == "code" else engine.run_demo_workflow()
        console.print(result.best_summary())
    elif args.cmd == "lineage":
        settings = load_settings(args.config)
        store = LineageStore(Engine._db_path_from_url(settings.engine.db_url))
        if args.lineage_cmd == "show":
            for rec in store.list_all():
                console.print(rec)
        elif args.lineage_cmd == "replay":
            for rec in replay(store, args.proposal_id):
                console.print(rec)


if __name__ == "__main__":
    app()
