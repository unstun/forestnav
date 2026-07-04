---
date: 2026-07-03
status: f01_1_oracle_demonstration_extraction_complete
origin: codex+code+experiment
reviewed: false
task: Module2 F01.1
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_e03_no_progress_oscillation.md
source_head: 96be287b3ab67f4899d4f2ab765c21f75c5661e8
execution_host: MacBook-Pro.local
---

# Module2 F01.1 Oracle Demonstration Extraction

## 直观结论

F01.1 已建立从 C02 oracle connector 结果重放并提取 state-action demonstrations 的可复跑链路。

这一步没有把 C02 摘要行当作轨迹使用。`oracle_connector_results.parquet` 只保存 oracle 摘要和 selected candidate, 不保存完整 path poses。新脚本会按 C02 row 的 `map_seed/profile/state/goal` 重建地图并重放 oracle A/B path, 再从相邻 pose 提取 expert steering。

当前产出是:

- 可复跑脚本: `2_experiment/forest_n3p/scripts/extract_oracle_demonstrations.py`
- 20-row preview dataset: `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_preview20.parquet`
- preview summary: `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_preview20_summary.json`
- oracle A smoke: `0_trials/module2_rl_rs_bc_demo_smoke/demonstrations_smoke3.parquet`
- B-only smoke: `0_trials/module2_rl_rs_bc_demo_smoke/demonstrations_bonly_smoke1.parquet`

这是 F01.1 extraction pipeline + source-bound preview, 不是最终完整 BC training corpus。全量数据清单和正式 manifest 属于 F01.2。

## Code Changes

Changed files:

- `2_experiment/forest_n3p/scripts/extract_oracle_demonstrations.py`

Implemented behavior:

| Behavior | Implementation |
|---|---|
| Input source | C02 `oracle_connector_results.parquet` |
| Map replay | `_grid_for_row(...)` with validation T06 profiles |
| Oracle A replay | disabled-analytic HA* from failure node to final goal |
| Oracle B replay | disabled-analytic HA* to selected candidate + terminal RS to goal |
| Expert action | local curvature from adjacent poses, converted to steering radian |
| Forward-only filter | reverse segments skipped |
| Terminal filter | samples already terminal-RS-connectable skipped/stopped |
| Collision filter | colliding current/next poses skipped |
| Too-short filter | segments shorter than `min_step_length_m` skipped |
| Observation | scalar observation stored; patch reconstructable from map seed/pose/goal/config |
| Provenance | source row index, query id, map seed, oracle type, source head |

## Smoke Runs

### Oracle A smoke

Command:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.extract_oracle_demonstrations \
  --max-records 3 \
  --source-head 96be287b3ab67f4899d4f2ab765c21f75c5661e8 \
  --output 0_trials/module2_rl_rs_bc_demo_smoke/demonstrations_smoke3.parquet
```

Result:

- selected rows: 3
- replay success rows: 3
- demo rows: 202
- skipped terminal-ready: 47
- skipped collision/reverse/short: 0/0/0
- all output rows: `oracle_type=oracle_a`, `expert_direction=1`, `terminal_rs_success=false`

### Oracle B-only smoke

Source row:

- selected offset: 1474
- source row index: 1539
- query id: `complex_s00_q0003`
- dedup key: `complex_s00_q0003:133:67:26`
- selected candidate source: `goal_annulus`

Command:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.extract_oracle_demonstrations \
  --row-offset 1474 \
  --max-records 1 \
  --source-head 96be287b3ab67f4899d4f2ab765c21f75c5661e8 \
  --output 0_trials/module2_rl_rs_bc_demo_smoke/demonstrations_bonly_smoke1.parquet
```

Result:

- selected rows: 1
- replay success rows: 1
- demo rows: 136
- skipped terminal-ready: 57
- skipped collision/reverse/short: 0/0/0
- all output rows: `oracle_type=oracle_b`, `expert_direction=1`, `terminal_rs_success=false`

### Dataset preview

Command:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.extract_oracle_demonstrations \
  --max-records 20 \
  --source-head 96be287b3ab67f4899d4f2ab765c21f75c5661e8 \
  --output 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_preview20.parquet
```

Result:

- selected rows: 20
- replay success rows: 20
- demo rows: 1109
- skipped terminal-ready: 313
- skipped reverse: 9
- skipped collision/short: 0/0
- all output rows: `oracle_type=oracle_a`, `expert_direction=1`, `terminal_rs_success=false`

## Verification

Commands:

```bash
PYTHONPATH=2_experiment python -m py_compile \
  2_experiment/forest_n3p/scripts/extract_oracle_demonstrations.py \
  2_experiment/forest_n3p/rl_rs/*.py \
  2_experiment/forest_n3p/scripts/run_policy_forward_budget.py \
  2_experiment/forest_n3p/scripts/run_rollout_collision_budget.py

PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_policy_forward_budget.py \
  2_experiment/forest_n3p/tests/test_rollout_collision_budget.py \
  2_experiment/forest_n3p/tests/test_rl_rs_api.py \
  -q

git diff --check
```

Results:

- `py_compile`: pass
- `pytest`: `24 passed in 0.47s`
- `git diff --check`: pass

## Allowed Conclusions

- C02 oracle results can now be replayed into source-bound state-action demonstrations.
- Oracle A and at least one B-only goal-annulus row have been smoke-validated.
- The extractor records enough provenance to audit each sample back to C02 row/query/map/source head.

## Disallowed Conclusions

- Do not claim the full BC dataset is materialized.
- Do not claim `voronoi_skeleton` B-only rows are valid training evidence.
- Do not claim BC training is started.
- Do not claim PPO training or planner integration exists.

## Next Step

Proceed to F01.2:

- write formal dataset manifest;
- decide whether the official corpus is preview-only, chunked full extraction, or a staged A/B split;
- include invalid endpoint policy, B-only/voronoi policy, source hash, schema, and reconstruction config.
