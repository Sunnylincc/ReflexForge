# Architecture

ReflexForge is split into composable packages:

- `compiler`: compiles task specs into optimization specs
- `generator`: deterministic proposal generation, mutation, crossover, repair
- `evaluator`: layered evaluators with early rejection
- `scorer`: weighted and Pareto multi-objective analysis
- `attribution`: credit assignment and failure analysis
- `lineage`: storage, graph queries, replay
- `memory`: lessons and reusable pattern retrieval
- `policy`: search, promotion, and stopping decisions
- `runtime`: budget controls, sandbox metadata, artifacts
- `core`: orchestration engine and scheduler
- `integrations`: local executor and future LLM adapters
