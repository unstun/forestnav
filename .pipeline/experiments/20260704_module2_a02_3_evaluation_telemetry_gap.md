---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - 0_trials/module2_rl_rs_evidence/local_slot_api.md
  - 0_trials/module2_rl_rs_evidence/collision_checker_unification.md
  - .pipeline/experiments/20260704_module2_h01_metric_protocol.md
---

# A02.3 Evaluation Telemetry Gap Audit

## 直观结论

本轮完成 A02.3: 当前 evaluation 字段缺口审计。

结论很明确: evaluation 已经能输出一部分 RL-RS analytic telemetry, 但还不能支撑完整论文诊断表。特别是 `nn_forward_time_s` 当前在 runtime telemetry 中恒为 0, 而 `rl_attempts` / `rl_successes` / `rs_attempts` / `fallback_to_primitives_count` 没有明确 flat columns。

## 产物

- `0_trials/module2_rl_rs_evidence/evaluation_telemetry_gap.md`
- 更新 `0_trials/module2_rl_rs_evidence/sources.md`
- 更新 `.pipeline/mainline_module2_rl_rs_replacement.md`

## 核验范围

本地代码:

- `2_experiment/forest_n3p/evaluation.py:62-103`
- `2_experiment/forest_n3p/evaluation.py:238-303`
- `2_experiment/forest_n3p/evaluation.py:336-409`
- `2_experiment/forest_n3p/evaluation.py:437-477`
- `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:680-831`
- `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:873-967`
- `2_experiment/forest_n3p/rl_rs/telemetry.py:6-66`
- `2_experiment/forest_n3p/rl_rs/operator.py:31-44`
- `2_experiment/forest_n3p/rl_rs/operator.py:76-80`
- `2_experiment/forest_n3p/main_evaluation.py:92-199`
- `2_experiment/forest_n3p/main_evaluation.py:425-504`
- `2_experiment/forest_n3p/main_evaluation.py:754-808`

项目记录:

- `.pipeline/experiments/20260704_module2_h01_metric_protocol.md`
- `.pipeline/experiments/20260704_module2_h01_evaluation_manifest.md`
- `.pipeline/experiments/20260704_module2_g02_checkpoint_operator_cli_telemetry.md`

## 字段判定

已可用:

- `analytic_attempts`
- `analytic_successes`
- `analytic_failure_count`
- `rl_rollout_steps`
- `rl_rollout_collision_checks`
- `terminal_rs_success_count`
- `terminal_rs_used_count`
- checkpoint path/hash fields

缺失或不够审计:

- `rs_attempts`
- `rl_attempts`
- `rl_successes`
- `nn_forward_time_s`
- `fallback_to_primitives_count`
- checker/rollout protocol manifest fields

## 后续实现要求

P0:

- action policy call 真实计时, 写入 `nn_forward_time_s`。
- `EvaluationRecord` 和 `summary_by_method_bucket.csv` 暴露 NN forward time 聚合。
- 增加 RL/RS attempt/success canonical fields。
- 增加 analytic failed -> primitive fallback count。

P1:

- records 或 companion manifest 记录 collision protocol 与 rollout protocol。
- 保留 compact per-attempt telemetry artifact。

## 验证

- Memory retrieval: confirmed A02.3 had no completed record; H01 metric protocol freezes `nn_forward_time_s` as diagnostic metric。
- ACE: `mcp__auggie__codebase-retrieval` returned `402 Payment Required`; used exact line reads。
- No local training or remote training was run。
- Formal training remains restricted to `gpu3070ti-relay` after Dr Sun approval。

## 边界

- This is a gap audit, not implementation of the missing columns。
- This does not approve F02.6。
- This does not create a PPO checkpoint。
- This does not unlock H02 formal evaluation。
