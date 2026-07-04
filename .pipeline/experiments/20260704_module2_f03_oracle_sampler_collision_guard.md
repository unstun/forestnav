---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_f03_curriculum_sampler.md
  - .pipeline/experiments/20260704_module2_f03_gate3_formal_preflight.md
---

# Module2 F03 Oracle Sampler Collision Guard 记录

## 直观结论

no-warm-start formal Gate #3 trial 的首次运行没有跑到 PPO 判定阶段, 而是在训练 reset 中崩溃。根因不是 PPO 收敛, 也不是 runner 参数, 而是 `OracleConnectorContextSampler` 从 `oracle_connector_results.parquet` 抽到了一条在当前 profile-aware 地图重建下 start/goal pose 碰撞的 row。

修复方式是在 oracle sampler 内跳过这类重建后无效的 row, 并记录 skip 计数。这样正式训练不会因为少量坏 row 随机中断, 但 collision 检查本身没有被放宽。

## 失败证据

formal trial 命令来自 preflight manifest:

```bash
PYTHONPATH=2_experiment KMP_DUPLICATE_LIB_OK=TRUE python -m forest_n3p.scripts.run_rl_rs_gate3_trial \
  --output-dir 0_trials/module2_gate3_formal/gate3_no_warm_formal_v1 \
  --seed 20260704 \
  --device auto \
  --train-curriculum-preset f03 \
  --eval-curriculum-preset f03 \
  --oracle-path 0_trials/module2_oracle_shape/oracle_connector_results.parquet \
  --heldout-seed 20260704 \
  --train-total-timesteps 100000 \
  --train-n-envs 1 \
  --train-n-steps 128 \
  --train-batch-size 64 \
  --train-n-epochs 4 \
  --eval-episodes 64 \
  --eval-min-episodes 64 \
  --eval-success-threshold 0.8 \
  --obs-patch-size-m 6.4 \
  --obs-patch-cells 64 \
  --max-steps 32 \
  --allow-duplicate-openmp
```

失败栈:

```text
ValueError: sampled curriculum goal state is in collision
```

失败产物已保留:

- `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/failed_attempt_01/run_formal_trial.log`
- `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/failed_attempt_01/train_partial/episodes_env0.csv`

## 根因量化

用当前 `CurriculumContextConfig`、`_evaluation_config()` 和 profile-aware `_generate_grid_map(profile_name, map_seed)` 重建 `0_trials/module2_oracle_shape/oracle_connector_results.parquet` 中 Complex/Extreme 且 `oracle_connectable=True` 的 rows:

```text
candidate_rows 6289
map_count 11
start_bad 4
goal_bad 54
```

首批坏 row 指向 `extreme_s00_q0006`, `profile_name=extreme_d05`, `map_seed=20460621`, `goal=(9.3, 11.1)`。

## 实现锚点

- `OracleConnectorContextSampler` 初始化新增 `skipped_invalid_rows` 和 `last_invalid_metadata`: `2_experiment/forest_n3p/rl_rs/curriculum.py:140-141`。
- `__call__()` 现在最多尝试 `max(32, 2 * len(rows))` 次, 对 `_build_context()` 抛出的 sampled-curriculum collision `ValueError` 跳过并继续抽样: `2_experiment/forest_n3p/rl_rs/curriculum.py:143-178`。
- 若尝试上限内仍无有效 row, 抛出 `RuntimeError`, 避免静默空转: `2_experiment/forest_n3p/rl_rs/curriculum.py:179`。

## 测试锚点

- 回归测试: `2_experiment/forest_n3p/tests/test_rl_rs_curriculum.py`。
- 测试构造 bad goal row + good row 的 parquet, 用固定 RNG 先抽到 bad row, 期望 sampler 跳过并返回 good row: `2_experiment/forest_n3p/tests/test_rl_rs_curriculum.py:95-143`。

## 验证记录

RED:

```bash
PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_rl_rs_curriculum.py::test_oracle_connector_sampler_skips_rows_that_reconstruct_to_colliding_context -q
```

失败原因:

```text
ValueError: sampled curriculum start state is in collision
```

GREEN:

```bash
PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_rl_rs_curriculum.py::test_oracle_connector_sampler_skips_rows_that_reconstruct_to_colliding_context -q
```

stdout:

```text
1 passed in 2.88s
```

局部验证:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_rl_rs_curriculum.py -q
```

stdout:

```text
6 passed in 6.27s
```

## 当前不 claim 的内容

- 不 claim F03.5 Gate #3 正式通过。
- 不 claim PPO 已在 `f03` / RS-failure 分布上收敛。
- 不改 oracle 结果语义; 只是训练 sampler 跳过当前地图重建下无效的少量 rows。
