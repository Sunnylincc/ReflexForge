# ReflexForge

ReflexForge is a **lineage-aware self-improving engine** that co-evolves code patches, workflow graphs, evaluator settings, runtime/resource policies, and memory strategies under real-world constraints.

## Vision
ReflexForge compiles a task into an optimization spec, generates structured proposals, evaluates them in layered sandboxes, assigns credit, records lineage, and improves future iterations.

## Why ReflexForge is different
- Optimizes **more than code**: workflows, evaluators, policies, and memory strategy are first-class.
- Uses **layered evaluation** to reject weak candidates early and preserve budget.
- Provides explicit **lineage and replay** for reproducibility and governance.
- Supports **weighted + Pareto multi-objective** ranking.

> Inspiration and differentiation: ReflexForge is an original production-oriented self-improving architecture and not a clone of any existing system.

## Architecture overview
Core loop:
1. Spec Compiler → executable optimization spec
2. Proposal Generator → typed proposals
3. Layered Evaluator → static/unit/smoke/benchmark/cost checks
4. Scorer → weighted + Pareto ranking
5. Attribution → likely gain/loss cause + lesson extraction
6. Lineage Store + Memory → history + reusable patterns
7. Search Policy → explore/exploit/escalate/stop decisions

See `docs/architecture.md` for module map.

## Proposal types
- `CodePatchProposal`
- `WorkflowProposal`
- `EvaluatorProposal`
- `ResourcePolicyProposal`
- `MemoryPolicyProposal`

Each includes rationale, expected gain, risk, reversibility, and ancestry.

## Layered evaluation
1. Static validation
2. Unit/syntax checks
3. Smoke checks
4. Benchmark checks
5. Cost/runtime checks

The engine short-circuits on failing stages when appropriate.

## Lineage memory
Every proposal (accepted or rejected) is stored with parents, mutation type, scores, failure reason, artifacts, and timestamp. Replay utilities help inspect branch decisions.

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
reflexforge init
reflexforge run --config configs/default.yaml
reflexforge run --config configs/demo_agent.yaml
```

## Demo commands
```bash
reflexforge demo code
reflexforge demo workflow
reflexforge lineage --config configs/default.yaml show
reflexforge lineage --config configs/default.yaml replay code-p1
```

## Roadmap
- checkpoint/resume policies
- richer HTML lineage visualization
- pluggable remote executors
- adaptive evaluator scheduling

## Limitations
- MVP uses deterministic local generators (no external LLM calls).
- Sandboxing is simulated and should be hardened for production.
- Scoring defaults are generic and may require task-specific tuning.

## Safety note
ReflexForge is intended for controlled experimentation with strict constraints, budget ceilings, and invariant checks. Use strong sandboxing and review gates before deploying autonomous modifications.


## Runtime dependency behavior
ReflexForge prefers real `pydantic`, `PyYAML`, and `rich` packages when installed. In constrained offline environments, it falls back to small internal compatibility shims to keep demos and tests runnable.
