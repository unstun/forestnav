---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_h01_evaluation_manifest.md
  - .pipeline/experiments/20260704_module2_h01_bc_operator_main_eval.md
  - .pipeline/experiments/20260704_module2_h01_realmap_query_protocol.md
---

# Module2 H01.1 PPO Analytic Operator Manifest Refresh

## 直观结论

本轮解除 H01.1 的 `missing_required_method_implementation` blocker。`ppo_analytic_operator` 现在是 `main_evaluation` 的显式方法名, 但不是 PPO+RS funnel 的改名版。

关键边界:

- `ha_rl_rs_ppo`: PPO rollout 后追加 terminal RS, operator 名为 `rl_rs_funnel_ppo`。
- `ppo_analytic_operator`: PPO rollout 不追加 terminal RS, operator 名为 `rl_rs_ppo_no_terminal_rs`。
- 为避免假成功, no-terminal-RS 模式只有在 rollout 自己进入 planner 的 `goal_xy_tol/goal_theta_tol` 时才返回 `AnalyticExpansionResult`。
- 如果 rollout 只是进入 terminal-RS-connectable 区域, 但还没到 goal tolerance, 返回 `None`, 让 Hybrid A* 回到普通 primitive expansion。

因此当前不是 formal-ready。H01 manifest 已重新生成, global blockers 只剩:

```text
f02_6_warm_start_decision_pending
missing_module2_rl_rs_checkpoint
```

PPO checkpoint 缺口必须在 `gpu3070ti-relay` 等远端 GPU 上补齐, 本轮没有也不应在本地训练。

## 实现锚点

- `AnalyticExpansionContext` 增加 `terminal_success_mode`, `goal_xy_tolerance_m`, `goal_theta_tolerance_rad`: `2_experiment/forest_n3p/rl_rs/env.py:52-54`。
- env 在 `goal_tolerance` 模式下用 goal tolerance 而不是 terminal RS success 作为成功终止: `2_experiment/forest_n3p/rl_rs/env.py:226-241`。
- goal tolerance 未达到但预算耗尽时写 `goal_tolerance_not_reached`: `2_experiment/forest_n3p/rl_rs/env.py:258-267`。
- `RlRsFunnelOperator.append_terminal_rs=False` 时不调用 `_terminal_rs_segments()`, 只在 `goal_tolerance_reached` 时返回 result: `2_experiment/forest_n3p/rl_rs/operator.py:83-99`。
- operator 把 planner tolerance 传入 env, 避免使用另一套成功半径: `2_experiment/forest_n3p/rl_rs/operator.py:148-150`。
- `main_evaluation` 把 `ppo_analytic_operator` 加入 RL-RS checkpoint gate: `2_experiment/forest_n3p/main_evaluation.py:67`, `2_experiment/forest_n3p/main_evaluation.py:324-328`。
- runtime dispatch 显式区分 `ha_rl_rs_ppo` 和 `ppo_analytic_operator`: `2_experiment/forest_n3p/main_evaluation.py:755-763`。
- PPO+RS funnel loader 传 `append_terminal_rs=True`; PPO-only analytic loader 传 `append_terminal_rs=False`: `2_experiment/forest_n3p/main_evaluation.py:859-889`。
- H01 manifest builder 将 `ppo_analytic_operator` 映射到同名 main evaluation method, 并用 PPO checkpoint/F02.6 blocker gate: `2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py:133-162`。
- H01 manifest global blockers 新增 `missing_module2_rl_rs_checkpoint`, formal command 同时要求 PPO-only 和 PPO+RS funnel ready: `2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py:216-257`。

## TDD 记录

RED:

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_rl_rs_funnel_operator.py \
  2_experiment/forest_n3p/tests/test_main_evaluation_rl_rs_operator.py \
  2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py
```

失败点覆盖:

- `RlRsFunnelOperator.__init__()` 没有 `append_terminal_rs`。
- preflight/CLI 不认识 `ppo_analytic_operator`。
- `_run_hybrid_a_operator("ppo_analytic_operator", ...)` 触发 `KeyError`。
- manifest 仍把 `ppo_analytic_operator` 标成 `missing_main_evaluation_method`。

GREEN:

```text
19 passed in 0.58s
```

相邻回归:

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_hybrid_astar_operator_protocol.py \
  2_experiment/forest_n3p/tests/test_hybrid_astar_analytic_operator.py \
  2_experiment/forest_n3p/tests/test_rl_rs_api.py \
  2_experiment/forest_n3p/tests/test_rl_rs_gym_env.py \
  2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py
```

结果:

```text
35 passed in 0.98s
```

## Manifest 产物

重新生成命令:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_evaluation_manifest \
  --output-dir 0_trials/module2_v1_evaluation_manifest \
  --manifest-out 0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json \
  --markdown-out 0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.md \
  --contract-path .pipeline/contracts/module2-ppo-funnel-expansion.md \
  --cutpoint-supplement-path .pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md \
  --warm-start-decision pending \
  --realmap-query-protocol-path 0_trials/module2_realmap_query_protocol/module2_realmap_query_protocol.json \
  --bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt \
  --queries-per-bucket 100 \
  --seed-count 5 \
  --queries-per-map 5
```

抽查:

```text
status=blocked_pending_decisions
blockers=["f02_6_warm_start_decision_pending", "missing_module2_rl_rs_checkpoint"]
bc_analytic_operator.status=ready
ppo_analytic_operator.main_evaluation_method=ppo_analytic_operator
ppo_analytic_operator.blockers=["missing_module2_rl_rs_checkpoint", "f02_6_warm_start_decision_pending"]
ppo_rs_funnel.blockers=["missing_module2_rl_rs_checkpoint", "f02_6_warm_start_decision_pending"]
formal_main_evaluation=None
```

## 当前边界

- 可以 claim: `ppo_analytic_operator` without terminal RS 已接入 main evaluation 和 H01 manifest。
- 可以 claim: no-terminal-RS 模式不会把 terminal-RS-connectable 的非 goal rollout 当作成功路径。
- 可以 claim: H01 的 `missing_required_method_implementation` blocker 已解除。
- 不能 claim: H01 formal-ready。
- 不能 claim: PPO policy 已训练或 checkpoint 已存在。
- 不能 claim: F02.6 warm-start 决策已关闭。
- 不能本地训练 PPO; 下一步训练/导出 checkpoint 必须走远端 GPU。
