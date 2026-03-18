# ReflexForge Rapid Stabilization Review

Date: 2026-03-18
Scope: README/docs/configs/CLI-first review, architecture mapping, tests + demos, focused correctness pass.

## Architecture map (intended vs current)

Intended loop from docs:
1. compile task spec
2. generate typed proposals
3. layered evaluation
4. multi-objective ranking
5. attribution + lessons
6. lineage persistence + replay
7. policy-guided iteration

Current implementation status:
- **Implemented in MVP**: steps 1-6 and basic policy mode tagging.
- **Partially implemented**: true iterative policy-driven search control (engine mostly runs fixed demo batches).
- **Partially implemented**: co-evolution breadth (code + workflow run paths exist; evaluator/resource/memory proposal families are typed but not yet actively generated in demos).

## Top 15 issues

| # | Issue | Severity | Confidence | Notes |
|---|---|---|---|---|
| 1 | Local stub packages (`src/pydantic`, `src/rich`, `src/yaml.py`) shadow real dependencies and can break production packaging behavior. | High | High | **Fixed** |
| 2 | `run --config` ignored task intent and always executed code demo path. | High | High | **Fixed** |
| 3 | CLI lineage commands were hardwired to default config DB path (could inspect wrong lineage DB). | High | High | **Fixed** |
| 4 | Lineage `scores` and `artifacts` persisted as `str(dict)` instead of JSON, preventing safe roundtrip/parsing. | High | High | **Fixed** |
| 5 | Workflow artifacts stored node lists as stringified lists, not structured data. | Medium | High | **Fixed** |
| 6 | Config model lacked typed `task` section, reducing control-path reliability for config-driven runs. | Medium | High | **Fixed** |
| 7 | Weight values were not normalized/coerced to float in config load path. | Medium | High | **Fixed** |
| 8 | README lineage command examples did not match updated/safer `--config` flow. | Medium | High | **Fixed** |
| 9 | README run examples did not demonstrate workflow config execution path. | Low | High | **Fixed** |
|10 | Replay only follows first parent and does not expose branch-aware traversal. | Medium | Medium | Not fixed (non-trivial behavior change) |
|11 | Engine does not yet generate evaluator/resource/memory proposals in demos (co-evolution breadth gap). | Medium | High | Not fixed (scope expansion) |
|12 | Lessons are recorded but not yet consumed by proposal generation policy. | Medium | High | Not fixed (requires broader generator-policy integration) |
|13 | Search policy is invoked per candidate mode tag, but stopping/escalation control is not loop-governing. | Medium | High | Not fixed (requires larger loop redesign) |
|14 | Postgres support is declared as optional dependency but lineage store runtime is SQLite-only. | Low | High | Not fixed (feature expansion) |
|15 | No test coverage for lineage JSON roundtrip and config-driven workflow run path. | Medium | High | **Fixed** |

## Stabilization strategy used

Applied only small, local, low-risk fixes that improve correctness/readiness without broad refactors:
- dependency compatibility handling
- config/CLI correctness
- lineage persistence correctness
- targeted tests and docs alignment

Deferred broader architectural expansions to avoid destabilizing MVP.
