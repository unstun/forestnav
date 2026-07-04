---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_g01_operator_dispatch_stub_integration.md
  - .pipeline/experiments/20260704_module2_g01_rl_rs_funnel_operator_skeleton.md
---

# Module2 G01.4/G02.2/G02.3 Checkpoint Operator CLI + Telemetry 记录

## 直观结论

G01.4/G02.2/G02.3 本轮闭环完成: 现在 `ha_rl_rs_ppo` 是 main evaluation 中显式可选的方法名, 必须提供 RL-RS PPO checkpoint, 缺 checkpoint 会在 preflight/loader 两层硬失败, 不会静默退回 RS。checkpoint 会被加载成 `RlRsFunnelOperator` 的 action policy, 进入 Hybrid A* analytic expansion slot。

同时 evaluation 输出不再只把 analytic/RL-RS 诊断藏在 `metadata` JSON 中。`EvaluationRecord` 和 `records.csv` 现在有 flat columns: `analytic_operator`, `analytic_attempts`, `analytic_successes`, `analytic_failure_count`, `rl_rollout_steps`, `terminal_rs_success_count`, `terminal_rs_used_count`, `rl_rs_checkpoint`, `rl_rs_checkpoint_sha256` 等。

这仍不是性能 claim。tiny PPO smoke 只证明 CLI/config/load/planner/evaluation 这条工程链路可运行、可记录、可审计; 它不是正式 checkpoint、不是 F02.6 warm-start 决策、不是 H01/H02 主实验。

## 实现锚点

- 新增 checkpoint action policy 和 loader: `2_experiment/forest_n3p/rl_rs/checkpoint_operator.py:14-84`。
- `load_rl_rs_funnel_operator_from_checkpoint()` 在加载 SB3 前检查路径存在且为文件; 缺失时抛 `FileNotFoundError("RL-RS checkpoint does not exist: ...")`: `2_experiment/forest_n3p/rl_rs/checkpoint_operator.py:32-49`。
- loader 记录 checkpoint SHA-256, 用 `PPO.load(...)` 加载模型, 并返回 `RlRsFunnelOperator`: `2_experiment/forest_n3p/rl_rs/checkpoint_operator.py:51-72`。
- `RlRsFunnelOperator` 现在保存 `observation_config`, `checkpoint_path`, `checkpoint_sha256`, 并把 observation config 注入 `AnalyticExpansionContext`: `2_experiment/forest_n3p/rl_rs/operator.py:46-58`, `2_experiment/forest_n3p/rl_rs/operator.py:108-123`。
- `main_evaluation.py` 新增 `ha_rl_rs_ppo` 方法组: `2_experiment/forest_n3p/main_evaluation.py:65-77`。
- `MainEvaluationConfig` 新增 checkpoint/device/observation/env 参数: `2_experiment/forest_n3p/main_evaluation.py:134-144`。
- preflight 对 `ha_rl_rs_ppo` 执行两层检查: checkpoint 必须提供, 且路径必须是文件: `2_experiment/forest_n3p/main_evaluation.py:260-320`。
- `_run_hybrid_a_operator()` 在 `method == "ha_rl_rs_ppo"` 时加载 checkpoint-backed operator 并传给 planner: `2_experiment/forest_n3p/main_evaluation.py:730-778`。
- `_make_planner()` 透传 `analytic_expansion_operator` 给 `HybridAStarPlanner`: `2_experiment/forest_n3p/main_evaluation.py:820-835`。
- `run_main_evaluation.py` 新增 CLI 参数 `--module2-rl-rs-checkpoint` 及相关 device/observation/env config: `2_experiment/forest_n3p/scripts/run_main_evaluation.py:43-53`, `2_experiment/forest_n3p/scripts/run_main_evaluation.py:89-99`。
- `EvaluationRecord` 新增 flat analytic/RL-RS telemetry 字段: `2_experiment/forest_n3p/evaluation.py:70-101`。
- `planner_run_from_path_stats()` 现在保留 `analytic_failure_count` 并汇总 `analytic_telemetry_records` 中的 RL rollout / terminal RS 小字段: `2_experiment/forest_n3p/evaluation.py:220-255`。
- `evaluate_run()` 将 metadata 中的 analytic/RL-RS 字段提升到 record columns: `2_experiment/forest_n3p/evaluation.py:330-368`。
- `_update_rl_rs_telemetry_summary()` 汇总 `rl_rollout_steps`, collision checks, terminal RS time/success/used/action count: `2_experiment/forest_n3p/evaluation.py:371-384`。

## 测试锚点

- missing checkpoint hard-fail: `2_experiment/forest_n3p/tests/test_rl_rs_checkpoint_operator.py:16-20`。
- smoke checkpoint load + real observation predict: `2_experiment/forest_n3p/tests/test_rl_rs_checkpoint_operator.py:23-58`。
- preflight 要求 `module2_rl_rs_checkpoint`: `2_experiment/forest_n3p/tests/test_main_evaluation_rl_rs_operator.py:38-44`。
- preflight 拒绝 missing checkpoint path: `2_experiment/forest_n3p/tests/test_main_evaluation_rl_rs_operator.py:47-54`。
- CLI `--module2-rl-rs-checkpoint` preflight-only 跑通 `ha_rl_rs_ppo`: `2_experiment/forest_n3p/tests/test_main_evaluation_rl_rs_operator.py:57-88`。
- `_run_hybrid_a_operator("ha_rl_rs_ppo", ...)` 会调用 checkpoint loader, 注入 operator, 并写 `rl_rs_checkpoint` / `rl_rs_checkpoint_sha256`: `2_experiment/forest_n3p/tests/test_main_evaluation_rl_rs_operator.py:91-122`。
- evaluation 输出 flat telemetry columns: `2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py:107-167`。

## TDD 记录

RED 1:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_rl_rs_checkpoint_operator.py -q
```

失败点:

```text
ModuleNotFoundError: No module named 'forest_n3p.rl_rs.checkpoint_operator'
```

GREEN 1:

```text
2 passed in 1.44s
```

RED 2:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_main_evaluation_rl_rs_operator.py -q
```

失败点:

```text
TypeError: MainEvaluationConfig.__init__() got an unexpected keyword argument 'module2_rl_rs_checkpoint'
SystemExit: 2 unrecognized arguments: --module2-rl-rs-checkpoint ...
AttributeError: forest_n3p.main_evaluation has no attribute load_rl_rs_funnel_operator_from_checkpoint
```

GREEN 2:

```text
4 passed in 0.59s
```

RED 3:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py -q
```

失败点:

```text
AttributeError: 'EvaluationRecord' object has no attribute 'analytic_operator'
```

GREEN 3:

```text
3 passed in 0.20s
```

相关回归:

```bash
PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_main_evaluation_rl_rs_operator.py \
  2_experiment/forest_n3p/tests/test_rl_rs_checkpoint_operator.py \
  2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py \
  2_experiment/forest_n3p/tests/test_hybrid_astar_operator_protocol.py \
  2_experiment/forest_n3p/tests/test_rl_rs_funnel_operator.py -q
```

stdout:

```text
17 passed in 1.77s
```

全量回归:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests -q
```

stdout:

```text
77 passed in 11.96s
```

## CLI Smoke

训练 tiny smoke checkpoint:

```bash
KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment python -m forest_n3p.scripts.train_rl_rs_ppo \
  --allow-duplicate-openmp \
  --smoke \
  --output-dir 0_trials/module2_operator_integration_smoke/g02_checkpoint_operator_smoke/train \
  --seed 20260704
```

输出:

- `status=complete`
- `warm_start_status=not_applied_f02_6_pending`
- `final_model=0_trials/module2_operator_integration_smoke/g02_checkpoint_operator_smoke/train/final_model.zip`
- `source_head=c6e8cb242e0cc374642f64a70407bcbcaf1b89fa+dirty`

用 `ha_rl_rs_ppo` 跑极小 main evaluation smoke:

```bash
KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_main_evaluation \
  --output-dir 0_trials/module2_operator_integration_smoke/g02_checkpoint_operator_smoke/eval \
  --methods ha_rl_rs_ppo \
  --module2-rl-rs-checkpoint 0_trials/module2_operator_integration_smoke/g02_checkpoint_operator_smoke/train/final_model.zip \
  --module2-rl-rs-device cpu \
  --module2-rl-rs-obs-patch-size-m 0.4 \
  --module2-rl-rs-obs-patch-cells 5 \
  --module2-rl-rs-max-steps 4 \
  --queries-per-bucket 1 \
  --seed-count 1 \
  --queries-per-map 1 \
  --density-profile-buckets validation_t06 \
  --distance-bins 1:2 \
  --contract-path .pipeline/contracts/module2-ppo-funnel-expansion.md \
  --allow-unresolved-human-review \
  --no-enforce-t14-scale \
  --bootstrap-resamples 100
```

输出:

- `record_count=3`
- `query_count=3`
- `status=candidate_or_smoke`
- `formal_acceptance=false`
- `preflight.ok_to_run=true`
- `preflight.available_methods=["ha_rl_rs_ppo"]`
- `records.csv` flat columns 含 `analytic_operator`, `analytic_attempts`, `analytic_successes`, `analytic_failure_count`, `rl_rollout_steps`, `terminal_rs_success_count`, `terminal_rs_used_count`, `rl_rs_checkpoint`, `rl_rs_checkpoint_sha256`。

抽查 `records.csv`:

- 3/3 rows: `method=ha_rl_rs_ppo`
- 3/3 rows: `analytic_operator=rl_rs_funnel_ppo`
- 3/3 rows: `analytic_attempts=1`, `analytic_successes=1`, `analytic_failure_count=0`
- 3/3 rows: `rl_rollout_steps=1`, `terminal_rs_success_count=1`, `terminal_rs_used_count=1`
- 3/3 rows: `rl_rs_checkpoint=0_trials/module2_operator_integration_smoke/g02_checkpoint_operator_smoke/train/final_model.zip`

## 当前边界

- 可以 claim: `ha_rl_rs_ppo` 已是 main evaluation 的显式方法名。
- 可以 claim: 缺 checkpoint 会 preflight/loader hard-fail, 不会静默 fallback 到 RS。
- 可以 claim: checkpoint-backed `RlRsFunnelOperator` 可进入 Hybrid A* analytic expansion slot。
- 可以 claim: evaluation `records.csv` 已能直接导出 analytic/RL-RS 诊断列。
- 不能 claim: tiny smoke checkpoint 有任何性能意义。
- 不能 claim: F02.6 warm-start 已关闭。
- 不能 claim: no-warm formal Gate #3 failure 被 warm-start 结果覆盖。
- 不能 claim: H01/H02 正式评测协议或正式结果已完成。

下一步应进入 H01.1 evaluation manifest 设计, 但 F02.6 warm-start 决策仍是显式未关闭项; 若要把 obstacle-summary warm-start 作为正式方法, 需要 Dr Sun 对 F02.6 作决策或新 contract 版本。
