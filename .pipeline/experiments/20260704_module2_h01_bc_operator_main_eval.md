---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_h01_evaluation_manifest.md
  - .pipeline/experiments/20260704_module2_f02_formal_v2_mlp_bc_baselines.md
---

# Module2 H01.1 BC Analytic Operator Main Evaluation 记录

## 直观结论

本轮解除 H01.1 的一个真实 blocker: `bc_analytic_operator` 现在是 `main_evaluation` 的显式方法名, 必须提供 BC checkpoint, 缺 checkpoint 会在 preflight/loader 两层硬失败, 不会静默退回 RS 或空策略。

实现语义是: formal-v2 obstacle-summary BC checkpoint 输出 steering action, 复用 `RlRsFunnelOperator` 做真实闭环 rollout, 再用 terminal RS 连接目标。也就是说, 这不是离线 BC 误差评估, 而是 Hybrid A* analytic expansion slot 中的 checkpoint-backed BC operator。

这仍不是 formal 性能结果。本轮 smoke 只有 3 queries, `formal_acceptance=false`, 只证明 loader/config/planner/evaluation/CSV 证据链可运行。

## 实现锚点

- BC checkpoint action policy: `2_experiment/forest_n3p/rl_rs/checkpoint_operator.py:32-52`。
- BC checkpoint loader hard-fail + PyTorch checkpoint load + SHA-256 记录: `2_experiment/forest_n3p/rl_rs/checkpoint_operator.py:98-156`。
- `main_evaluation` 注册 `BC_OPERATOR_METHODS=("bc_analytic_operator",)` 并加入 `IMPLEMENTED_METHODS`: `2_experiment/forest_n3p/main_evaluation.py:65-79`。
- `MainEvaluationConfig` 新增 `module2_bc_checkpoint` / `module2_bc_device`: `2_experiment/forest_n3p/main_evaluation.py:136-139`。
- preflight 要求 BC checkpoint 存在: `2_experiment/forest_n3p/main_evaluation.py:318-322`。
- `_run_hybrid_a_operator()` 在 `bc_analytic_operator` 时加载 `rl_rs_funnel_bc`: `2_experiment/forest_n3p/main_evaluation.py:740-790`。
- BC loader wrapper 和 shared rollout/env 参数: `2_experiment/forest_n3p/main_evaluation.py:872-897`。
- `EvaluationRecord` / `records.csv` 新增 `bc_checkpoint`, `bc_checkpoint_sha256` flat columns: `2_experiment/forest_n3p/evaluation.py:86-101`, `2_experiment/forest_n3p/evaluation.py:354-369`。
- H01 manifest 新增 `--bc-checkpoint`; checkpoint 存在时 `bc_analytic_operator` 为 ready 且映射到 main evaluation 同名方法: `2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py:20-22`, `2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py:121-141`。

## TDD 记录

RED 1:

```bash
PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_rl_rs_checkpoint_operator.py \
  2_experiment/forest_n3p/tests/test_main_evaluation_rl_rs_operator.py \
  -k bc -q
```

失败点:

```text
ImportError: cannot import name 'load_bc_funnel_operator_from_checkpoint'
```

GREEN 1:

```text
6 passed, 6 deselected in 1.07s
```

RED 2:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py -q
```

失败点:

```text
Module2EvaluationManifestConfig.__init__() got an unexpected keyword argument 'bc_checkpoint'
unrecognized arguments: --bc-checkpoint ...
```

GREEN 2:

```text
2 passed in 0.16s
```

RED 3:

```bash
PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py \
  -k bc_operator_checkpoint -q
```

失败点:

```text
AttributeError: 'EvaluationRecord' object has no attribute 'bc_checkpoint'
```

GREEN 3:

```text
4 passed in 0.19s
```

相关 targeted 回归:

```bash
PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_rl_rs_checkpoint_operator.py \
  2_experiment/forest_n3p/tests/test_main_evaluation_rl_rs_operator.py \
  2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py \
  -k "bc or module2_manifest" -q
```

stdout:

```text
8 passed, 6 deselected in 1.16s
```

## 不训练的 Main Evaluation Smoke

Dr Sun 已明确要求不要本地训练。本轮没有本地训练; 只加载已有 formal-v2 BC checkpoint 并跑 3-query main evaluation smoke。

preflight:

```bash
KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_main_evaluation \
  --output-dir 0_trials/module2_operator_integration_smoke/bc_operator_preflight \
  --preflight-only \
  --methods bc_analytic_operator \
  --module2-bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt \
  --queries-per-bucket 1 \
  --seed-count 1 \
  --density-profile-buckets validation_t06 \
  --contract-path .pipeline/contracts/module2-ppo-funnel-expansion.md \
  --cutpoint-supplement-path .pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md \
  --allow-unresolved-human-review \
  --no-enforce-t14-scale
```

结果:

```text
ok_to_run=true
available_methods=["bc_analytic_operator"]
blocking_issues=[]
t14_scale_satisfied=false
```

smoke:

```bash
KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_main_evaluation \
  --output-dir 0_trials/module2_operator_integration_smoke/bc_operator_smoke \
  --methods bc_analytic_operator \
  --module2-bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt \
  --queries-per-bucket 1 \
  --seed-count 1 \
  --density-profile-buckets validation_t06 \
  --contract-path .pipeline/contracts/module2-ppo-funnel-expansion.md \
  --cutpoint-supplement-path .pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md \
  --allow-unresolved-human-review \
  --no-enforce-t14-scale \
  --bootstrap-resamples 100
```

输出:

```text
record_count=3
query_count=3
status=candidate_or_smoke
formal_acceptance=false
```

`records.csv` 抽查:

- 3/3 rows: `method=bc_analytic_operator`
- 3/3 rows: `success=True`
- 3/3 rows: `analytic_operator=rl_rs_funnel_bc`
- `analytic_attempts` values: `1`, `3`, `122`
- `analytic_successes` value: `1`
- `terminal_rs_success_count=1`, `terminal_rs_used_count=1`
- `bc_checkpoint=2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt`
- `bc_checkpoint_sha256=3156df44ca7f26da7f2e635707554bb1cd486164638b3a2d11075c3787670683`

## H01 Manifest 更新

重新生成:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_evaluation_manifest \
  --output-dir 0_trials/module2_v1_evaluation_manifest \
  --manifest-out 0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json \
  --markdown-out 0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.md \
  --contract-path .pipeline/contracts/module2-ppo-funnel-expansion.md \
  --cutpoint-supplement-path .pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md \
  --warm-start-decision pending \
  --bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt \
  --queries-per-bucket 100 \
  --seed-count 5 \
  --queries-per-map 5
```

当前 manifest 状态:

```text
status=blocked_pending_decisions
bc_analytic_operator=ready
ppo_analytic_operator=blocked missing_main_evaluation_method
ppo_rs_funnel=blocked missing_module2_rl_rs_checkpoint + f02_6_warm_start_decision_pending
global blockers=f02_6_warm_start_decision_pending, missing_required_method_implementation, realmap_query_generation_not_frozen
```

## 当前边界

- 可以 claim: `bc_analytic_operator` 已接入 main evaluation。
- 可以 claim: 缺 BC checkpoint 会 hard-fail, 不会静默 fallback。
- 可以 claim: BC checkpoint path/hash 已进入 `records.csv` flat columns。
- 可以 claim: H01 manifest 已不再把 BC 记为 `missing_main_evaluation_method`。
- 不能 claim: BC operator 已有 formal 性能结论。
- 不能 claim: H01.1 formal-ready, 因为 F02.6、pure PPO analytic operator、realmap query protocol 仍未关闭。
- 不能 claim: 本轮做过任何本地训练。
