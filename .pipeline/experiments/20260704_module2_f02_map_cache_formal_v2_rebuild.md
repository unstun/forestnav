---
date: 2026-07-04
status: f02_formal_v1_invalidated_formal_v2_clean
origin: codex+code+experiment
reviewed: false
task: Module2 F02 data integrity repair
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_f02_patch_cnn_formal_pilot.md
source_head: 9220bd363d46769edba41a6c086ad70cdb1c3801
execution_host: MacBook-Pro.local
---

# Module2 F02 Map-Cache Audit and Formal V2 Rebuild

## 直观结论

F02 formal-v1 不是干净训练集。根因是 row -> map 重建时缓存只用
`map_seed`, 但 `validation_t06` 中同一个 `map_seed` 会被多个
`profile_name` 复用。直观上就是: 以前有些 `complex_d04` / `extreme_d06`
/ `extreme_d07` 的样本, 实际上用到了同 seed 的第一张 profile 地图。

修复后重新审计 formal-v1, 发现 85514 条 demo row 中有 4764 条在真实
profile 地图下 current 或 next pose 碰撞。因此 formal-v1 上的 scalar /
obstacle-summary / patch-CNN formal 结果都只能作为历史调试记录, 不能再作为
当前 BC 方法排名或 PPO warm-start 依据。

已生成 formal-v2:

- merged rows: 83809
- source rows: 1032
- oracle-A source rows: 1024
- goal_annulus oracle-B source rows: 8
- true-profile collision audit: 0 current collisions, 0 next collisions

## Root Cause

Previous `_grid_for_row()` keyed the map cache as:

```python
map_seed = int(row["map_seed"])
grid_map = cache.get(map_seed)
```

But formal-v1 contains profile reuse:

- `20360620`: `complex_d02`, `complex_d03`, `complex_d04`
- `20460620`: `extreme_d05`, `extreme_d06`, `extreme_d07`

The fix is a profile-aware cache key:

```python
MapCacheKey = tuple[str, int]
cache_key = (str(row["profile_name"]), int(row["map_seed"]))
```

Code commits:

- `f0a9fe67`: `run_oracle_connector_analysis.py` map and EDT cache key
- `d6f2e1dc`: `run_rollout_collision_budget.py` map and checker cache key
- `1079d0d5`: `extract_oracle_demonstrations.py` caller type
- `5e21d568`: `train_bc_policy.py` caller type
- `89e3309c`: `train_bc_patch_policy.py` caller type
- `aa6da209`: `render_oracle_connector_cases.py` caller type
- `9220bd36`: regression test for same seed / different profile

## Formal V1 Invalidating Audit

Full formal-v1 collision audit under profile-aware map reconstruction:

| Metric | Value |
|---|---:|
| rows | 85514 |
| any collision rows | 4764 |
| current collision rows | 4468 |
| next collision rows | 4466 |
| source rows with any collision | 236 |

Collision rows by profile:

| Profile | Rows |
|---|---:|
| `complex_d04` | 2241 |
| `extreme_d06` | 21 |
| `extreme_d07` | 2502 |

Re-evaluating the old patch-CNN formal-v1 pilot after the cache fix produced
13 runtime errors, all with:

```text
runtime_error:ValueError:AnalyticExpansionContext start state is in collision.
```

This is stronger evidence that the old dataset, not only the old evaluator, was
using inconsistent map semantics.

## Formal V2 Generation

Commands:

```bash
PYTHONPATH=2_experiment KMP_DUPLICATE_LIB_OK=TRUE \
python -m forest_n3p.scripts.extract_oracle_demonstrations \
  --buckets Complex \
  --filter-best-oracle oracle_a \
  --oracle-types best \
  --max-records 512 \
  --progress-every 25 \
  --source-head 9220bd363d46769edba41a6c086ad70cdb1c3801 \
  --output 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v2_complex_a512.parquet

PYTHONPATH=2_experiment KMP_DUPLICATE_LIB_OK=TRUE \
python -m forest_n3p.scripts.extract_oracle_demonstrations \
  --buckets Extreme \
  --filter-best-oracle oracle_a \
  --oracle-types best \
  --max-records 512 \
  --progress-every 25 \
  --source-head 9220bd363d46769edba41a6c086ad70cdb1c3801 \
  --output 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v2_extreme_a512.parquet

PYTHONPATH=2_experiment KMP_DUPLICATE_LIB_OK=TRUE \
python -m forest_n3p.scripts.extract_oracle_demonstrations \
  --filter-best-oracle oracle_b \
  --oracle-b-candidate-sources goal_annulus \
  --oracle-types best \
  --progress-every 5 \
  --source-head 9220bd363d46769edba41a6c086ad70cdb1c3801 \
  --output 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v2_b_goal_annulus.parquet

PYTHONPATH=2_experiment KMP_DUPLICATE_LIB_OK=TRUE \
python -m forest_n3p.scripts.merge_demonstration_shards \
  --source-head 9220bd363d46769edba41a6c086ad70cdb1c3801 \
  --output 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v2.parquet \
  --inputs \
    2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v2_complex_a512.parquet \
    2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v2_extreme_a512.parquet \
    2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v2_b_goal_annulus.parquet
```

Logs:

- `2_experiment/forest_n3p/logs/module2_f02_formal_v2/complex_a512.log`
- `2_experiment/forest_n3p/logs/module2_f02_formal_v2/extreme_a512.log`
- `2_experiment/forest_n3p/logs/module2_f02_formal_v2/b_goal_annulus.log`
- `2_experiment/forest_n3p/logs/module2_f02_formal_v2/merge.log`
- `2_experiment/forest_n3p/logs/module2_f02_formal_v2/formal_v1_collision_audit.json`
- `2_experiment/forest_n3p/logs/module2_f02_formal_v2/formal_v2_collision_audit.json`

## Formal V2 Composition

| Shard | Source rows | Demo rows | Replay failed |
|---|---:|---:|---:|
| Complex oracle-A | 512 | 40619 | 0 |
| Extreme oracle-A | 512 | 42428 | 0 |
| goal_annulus oracle-B | 8 | 762 | 50 |
| merged | 1032 | 83809 | n/a |

Merged artifact:

- `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v2.parquet`
- SHA-256: `2ae60a1f7f16b6028c1b1b491f6ab053b09241c4edc85a2b8d9d5e9eefab128d`
- manifest: `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest_formal_v2.json`

## Verification

Commands:

```bash
PYTHONPATH=2_experiment KMP_DUPLICATE_LIB_OK=TRUE python -m pytest \
  2_experiment/forest_n3p/tests/test_train_bc_patch_policy.py \
  2_experiment/forest_n3p/tests/test_train_bc_policy_features.py \
  2_experiment/forest_n3p/tests/test_extract_oracle_demonstrations.py \
  2_experiment/forest_n3p/tests/test_rollout_collision_budget.py \
  -q

python -m py_compile \
  2_experiment/forest_n3p/scripts/run_oracle_connector_analysis.py \
  2_experiment/forest_n3p/scripts/extract_oracle_demonstrations.py \
  2_experiment/forest_n3p/scripts/train_bc_policy.py \
  2_experiment/forest_n3p/scripts/train_bc_patch_policy.py \
  2_experiment/forest_n3p/scripts/render_oracle_connector_cases.py \
  2_experiment/forest_n3p/scripts/audit_bc_demonstration_collisions.py \
  2_experiment/forest_n3p/scripts/run_rollout_collision_budget.py

PYTHONPATH=2_experiment KMP_DUPLICATE_LIB_OK=TRUE \
python -m forest_n3p.scripts.audit_bc_demonstration_collisions \
  --dataset 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v1.parquet \
  --output 2_experiment/forest_n3p/logs/module2_f02_formal_v2/formal_v1_collision_audit.json \
  --source-head 9220bd363d46769edba41a6c086ad70cdb1c3801+working_tree_audit_script

PYTHONPATH=2_experiment KMP_DUPLICATE_LIB_OK=TRUE \
python -m forest_n3p.scripts.audit_bc_demonstration_collisions \
  --dataset 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v2.parquet \
  --output 2_experiment/forest_n3p/logs/module2_f02_formal_v2/formal_v2_collision_audit.json \
  --source-head 9220bd363d46769edba41a6c086ad70cdb1c3801+working_tree_audit_script

git diff --check
```

Results before data rebuild:

- pytest: `10 passed in 2.88s`
- py_compile: pass, including `audit_bc_demonstration_collisions.py`
- git diff --check: pass

Full formal-v2 collision audit:

| Metric | Value |
|---|---:|
| rows | 83809 |
| current collision rows | 0 |
| next collision rows | 0 |
| any collision rows | 0 |
| source rows with any collision | 0 |

## Allowed Conclusions

- Formal-v2 is the current trainable BC corpus for Module2 F02.
- Formal-v2 uses profile-aware map reconstruction and passes current/next pose
  collision audit.
- Historical formal-v1 BC metrics are stale after this audit.

## Disallowed Conclusions

- Do not use formal-v1 scalar, obstacle-summary, or patch-CNN results to rank
  BC methods under the fixed map semantics.
- Do not claim all 58 historical goal_annulus B-only rows are reproducible.
- Do not claim PPO training or planner integration exists.

## Next Step

Rerun scalar, obstacle-summary, and patch+scalar CNN BC on formal-v2 before
making any PPO warm-start decision.
