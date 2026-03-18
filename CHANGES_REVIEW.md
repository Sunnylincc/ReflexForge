# Applied Fixes (Rapid Stabilization Pass)

Date: 2026-03-18

## Fix 1: Replace shadowing stub packages with compatibility module
- **Bug**: Top-level fallback modules (`src/pydantic`, `src/rich`, `src/yaml.py`) could shadow real third-party packages, causing unpredictable runtime behavior.
- **Patch**: Added `reflexforge.compat` to prefer real dependencies and use internal fallback only if missing; updated imports across project to use compat symbols.
- **Residual risk**: Fallbacks are intentionally minimal and not full-featured replacements; advanced pydantic/yaml/rich behavior is still out of scope.

## Fix 2: Make `run --config` honor config task kind
- **Bug**: Engine ignored config task intent and always ran code demo.
- **Patch**: Added typed `TaskSettings` to config and updated `Engine.run_with_config()` to dispatch by `task.kind` (`code` / `workflow`).
- **Residual risk**: Unknown task kinds still default to code path; multi-task orchestration is not implemented yet.

## Fix 3: Add config-aware lineage CLI flows
- **Bug**: `lineage` subcommands always used default DB config, even if runs used another config.
- **Patch**: Added `--config` option to `reflexforge lineage`, loading DB path from selected config.
- **Residual risk**: Users can still point at a DB with mixed run contexts; no run-id filtering exists yet.

## Fix 4: Serialize lineage scores/artifacts as JSON
- **Bug**: Store used `str(dict)` for scores/artifacts, making parsing brittle and type-unsafe.
- **Patch**: Switched lineage persistence to `json.dumps/json.loads`; list/get now return structured typed payloads.
- **Residual risk**: No schema migration mechanism for old rows stored in legacy string format.

## Fix 5: Preserve workflow artifact structure
- **Bug**: Workflow node artifacts were stringified list literals.
- **Patch**: Saved node lists as structured JSON-compatible arrays and widened lineage artifact model to `dict[str, object]`.
- **Residual risk**: Artifact schema is still permissive (not strongly validated per proposal type).

## Fix 6: Harden config parsing/coercion
- **Bug**: Config lacked typed task section and did not coerce weight values to numeric floats reliably.
- **Patch**: Extended `Settings` with `TaskSettings`; loader now parses engine/task/weights and coerces weights to float.
- **Residual risk**: YAML fallback parser supports only a practical subset of YAML syntax.

## Fix 7: Increase regression coverage for stabilized paths
- **Bug**: Tests did not protect config-driven workflow dispatch or structured lineage JSON roundtrip.
- **Patch**: Added tests in `test_engine_smoke.py` and `test_lineage_store.py` for these paths.
- **Residual risk**: Replay branching semantics and broader multi-type co-evolution remain untested.

## Fix 8: Align README commands with executable CLI behavior
- **Bug**: README examples under-specified lineage config usage and workflow run path.
- **Patch**: Updated command examples to include workflow config run and config-aware lineage commands; documented dependency compatibility behavior.
- **Residual risk**: README still documents MVP scope, not production hardening details.
