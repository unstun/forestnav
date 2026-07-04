---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - 0_trials/module2_rl_rs_evidence/local_slot_api.md
  - .pipeline/experiments/20260703_module2_e03_collision_consistency.md
---

# A02.2 Collision Checker Unification

## 直观结论

本轮完成 A02.2 collision checker 统一备忘。

关键结论:

- 当前代码已经有统一入口: planner primitive、RS analytic expansion、RL rollout、terminal RS check 都能落到 `checker.collides_path(samples)` / `checker.collides_pose(...)`。
- 但默认 checker 构造仍分散: planner 和 RL context 默认都会构造 `GridFootprintChecker`; `EDTCollisionChecker` 存在但不是默认 planner checker。
- 因此后续不能只说 "collision checked"。formal artifact 必须记录 checker class、footprint、theta bins、collision step、padding/margin, 并禁止 train/eval checker protocol 不一致时写 performance claim。

## 产物

- `0_trials/module2_rl_rs_evidence/collision_checker_unification.md`
- 更新 `0_trials/module2_rl_rs_evidence/sources.md`
- 更新 `.pipeline/mainline_module2_rl_rs_replacement.md`

## 核验范围

本地代码:

- `2_experiment/forest_n3p/third_party/pathplan/geometry.py:262-416`
- `2_experiment/forest_n3p/third_party/pathplan/geometry.py:419-518`
- `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:196-201`
- `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:237-251`
- `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:506-533`
- `2_experiment/forest_n3p/rl_rs/env.py:86-92`
- `2_experiment/forest_n3p/rl_rs/env.py:191-222`
- `2_experiment/forest_n3p/rl_rs/rollout.py:42-56`
- `2_experiment/forest_n3p/rl_rs/terminal.py:44-50`
- `2_experiment/forest_n3p/rl_rs/operator.py:133-162`
- `2_experiment/forest_n3p/scripts/audit_bc_demonstration_collisions.py:34-56`

项目记录:

- `.pipeline/experiments/20260703_module2_e03_collision_consistency.md`
- `.pipeline/contracts/module2-ppo-funnel-expansion.md`
- `.pipeline/experiments/20260704_module2_g02_checkpoint_operator_cli_telemetry.md`

## 当前建议

Formal v1 collision protocol 应先采用:

- checker class: `GridFootprintChecker`
- footprint model: `TwoCircleFootprint`
- collision step: planner `collision_step`, 同步给 RL `collision_sample_step_m`
- terminal RS checker: same planner checker instance
- map boundary: out of bounds is collision

`EDTCollisionChecker` 暂不作为默认 formal protocol。若后续切 EDT, 需要单独 decision/version, 因为它改变 baseline 和训练/评测碰撞口径。

## 后续 gate

- A02.3 telemetry 要纳入 checker protocol manifest/link。
- BC/Oracle dataset 要记录 checker protocol; 缺字段旧数据标 legacy。
- `train_rl_rs_ppo` artifact 要记录 checker protocol。
- `run_main_evaluation` preflight 要能拒绝 train/eval checker 不一致的 formal claim。
- 增加回归测试: `RlRsFunnelOperator` 的 env context checker 必须复用 planner checker, terminal RS 也必须复用同一 checker。

## 验证

- Memory retrieval: confirmed A02.2 was still open; E03.2 was only local collision consistency, not this protocol memo。
- ACE: `mcp__auggie__codebase-retrieval` returned `402 Payment Required`; used exact line reads。
- No local training or remote training was run。
- Future formal training remains restricted to `gpu3070ti-relay` after Dr Sun approval。

## 边界

- This is a local code audit and protocol memo, not a code implementation gate completion。
- This does not approve F02.6。
- This does not create a PPO checkpoint。
- This does not unlock H02 formal evaluation。
