---
date: 2026-07-03
status: f01_2_dataset_manifest_complete
origin: codex+code+experiment
reviewed: false
task: Module2 F01.2
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_f01_oracle_demonstration_extraction.md
source_head: ab41e299
execution_host: MacBook-Pro.local
---

# Module2 F01.2 Dataset Manifest

## 直观结论

F01.2 已为 Module2 RL-RS BC preview dataset 写入正式 manifest。

Manifest 文件:

- `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest.json`
- `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/README.md`

manifest 明确记录:

- source input: `0_trials/module2_oracle_shape/oracle_connector_results.parquet`
- source extractor: `2_experiment/forest_n3p/scripts/extract_oracle_demonstrations.py`
- source head: `96be287b3ab67f4899d4f2ab765c21f75c5661e8`
- preview parquet SHA-256
- schema
- extraction config
- filters
- known boundaries

关键边界: 当前 dataset status 是 `preview`, 不是最终完整 BC corpus。

## Dataset Files

| File | Rows | SHA-256 |
|---|---:|---|
| `demonstrations_preview20.parquet` | 1109 | `a9fda719c255197190cbc3a379d39ee9a991702e4c5f2625e9d7cfea051aadc3` |
| `demonstrations_preview20_summary.json` | n/a | `846fa284d08016d478130e0d17926ae1b9062ae2d3144d19b2326aa48f79d16c` |

Smoke artifacts:

| File | Rows | Purpose |
|---|---:|---|
| `0_trials/module2_rl_rs_bc_demo_smoke/demonstrations_smoke3.parquet` | 202 | oracle A replay smoke |
| `0_trials/module2_rl_rs_bc_demo_smoke/demonstrations_bonly_smoke1.parquet` | 136 | B-only goal-annulus replay smoke |

## Schema

The manifest records every column. Core fields:

- source: `source_row_index`, `query_id`, `map_seed`, `query_seed`, `dedup_key`, `expansion_idx`, `source_head`
- state: `current_x`, `current_y`, `current_theta`
- target: `goal_x`, `goal_y`, `goal_theta`
- next pose: `next_x`, `next_y`, `next_theta`
- action: `expert_steering_rad`, `expert_curvature`, `expert_direction`, `step_length_m`
- observation: `obs_scalar`
- terminal set: `terminal_rs_checked`, `terminal_rs_success`, `terminal_rs_path_length_m`

## Filters

Manifest filters:

- require `oracle_connectable`;
- skip colliding current/next pose;
- skip reverse direction because E01 action space is forward-only;
- skip too-short segment;
- stop/skip when current state is already terminal-RS-connectable;
- exclude invalid endpoint rows through oracle-connectable filter.

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
- `pytest`: `24 passed in 0.50s`
- `git diff --check`: pass

## Allowed Conclusions

- The preview dataset has a manifest with source hash, schema, extraction config, filters, and known boundaries.
- The dataset can be audited back to C02 oracle rows and extraction script version.

## Disallowed Conclusions

- Do not claim full BC corpus is materialized.
- Do not claim BC training has started.
- Do not claim PPO training has started.
- Do not claim RL-RS planner integration exists.

## Next Step

Proceed to F02.1:

- train a BC policy only after deciding whether to use preview data or run a larger chunked extraction;
- evaluate rollout success to RS-connectable terminal set, not only action MSE.
