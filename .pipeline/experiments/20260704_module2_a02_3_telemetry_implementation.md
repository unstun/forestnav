---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_a02_3_evaluation_telemetry_gap.md
  - .pipeline/experiments/20260704_module2_h01_metric_protocol.md
---

# A02.3 Telemetry P0 Implementation

## 直观结论

本轮把 A02.3 从“缺口审计”推进到 P0 实现: evaluation records 和 summary 现在能直接暴露 RL/RS attempts、RL successes、NN forward time、analytic-failure-to-primitive fallback count，以及 RL-RS rollout/collision protocol metadata。

这不是训练, 不生成 PPO checkpoint, 不解除 F02.6 warm-start 决策。

## 实现内容

- `RlRsFunnelOperator` 在每次 `action_policy(observation)` 周围记录 wall-clock, 并把 `nn_forward_time_s` 写入 `AnalyticExpansionEnv.step()`。
- `RlRsStepTelemetry` / `RlRsEpisodeTelemetry` 聚合 per-step NN forward time 和 terminal RS check count。
- `RlRsFunnelTelemetry.to_record()` 输出 canonical fields: `rl_attempts`, `rl_successes`, `rs_attempts`, `nn_forward_time_s`, `fallback_to_primitives_count`, `rollout_protocol`, `collision_checker`。
- `EvaluationRecord` / `records.csv` 输出上述 flat columns。
- `summary_by_method_bucket.csv` 输出 `mean_nn_forward_time_s`, `p95_nn_forward_time_s`, `rl_attempts_total`, `rl_successes_total`, `rs_attempts_total`, `fallback_to_primitives_total`。
- `fallback_to_primitives_count` 以 planner-level `analytic_failure_count` 为准, 因为 primitive fallback 是 analytic attempt 失败后的 planner 行为。
- 更新 I01 method/system diagram builder 的 code anchors, 并重新生成 `0_trials/module2_method_algorithms/` 与 `0_trials/module2_system_diagram/`。

## 验证

- RED: 新增 telemetry column/operator timing tests 后, targeted tests 首次失败于缺少 `EvaluationRecord.rl_attempts`、operator record `nn_forward_time_s` 等字段。
- GREEN: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py 2_experiment/forest_n3p/tests/test_rl_rs_funnel_operator.py` -> `14 passed in 1.04s`。
- Artifact anchor regression: 全量测试首次失败于旧 code anchor `step = env.step(self.action_policy(observation))` 不再存在。
- Anchor fix: `KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_method_algorithms.py 2_experiment/forest_n3p/tests/test_module2_system_diagram.py` -> `2 passed in 0.12s`。
- Full regression: `KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests` -> `112 passed in 11.82s`。
- Syntax: `python -m py_compile 2_experiment/forest_n3p/evaluation.py 2_experiment/forest_n3p/rl_rs/telemetry.py 2_experiment/forest_n3p/rl_rs/env.py 2_experiment/forest_n3p/rl_rs/operator.py 2_experiment/forest_n3p/scripts/build_module2_method_algorithms.py 2_experiment/forest_n3p/scripts/build_module2_system_diagram.py` passed.

## 边界

- 未本地训练。
- 未远端训练。
- 未批准 F02.6。
- 未生成 formal PPO checkpoint。
- 不支持 formal performance claim; H01/H02 仍受 F02.6 pending 和缺 PPO checkpoint 阻塞。
