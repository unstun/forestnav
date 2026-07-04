---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Post-F02.6 Regeneration Plan

## 直观结论

本轮新增 `build_module2_post_f02_6_regeneration_plan.py`, 把 F02.6 关闭后的 formal gate 执行顺序写成机器可读计划。

这个计划不是执行器。它不运行命令、不训练、不跑 remote preflight、不 audit、不写论文结果。它只把已有 gate artifact 中的约束串成有序阶段, 防止后续 F02.6 一旦关闭后靠口头记忆执行。

当前真实状态:

- `status=blocked_until_f02_6_decision`
- `executes_commands=false`
- `runs_training=false`
- `runs_remote_preflight=false`
- `training_allowed_now=false`
- `remote_preflight_allowed_now=false`
- 只有 `f02_6_decision_record` 阶段是 ready, 且该阶段需要 Dr Sun 人类决策输入。

## 阶段顺序

1. `f02_6_decision_record`: 记录 Dr Sun 对 obstacle-summary warm-start 的 approve/reject。
2. `regenerate_preflight_gate_artifacts`: F02.6 关闭后重生成 source-freshness 指出的 preflight 前置 artifact。
3. `approved_remote_preflight`: 在 `gpu3070ti-relay` 生成 approved warm-start preflight。
4. `regenerate_remote_execution_packet`: 用 approved preflight 刷新 remote formal execution packet。
5. `gate3_remote_training`: 仅当 remote packet ready 时在 `gpu3070ti-relay` 跑 formal PPO。
6. `gate3_remote_audit_pullback`: audit 远端 trial 并回传 checkpoint/eval/audit artifacts 和 hash。
7. `regenerate_h01_h02_formal_artifacts`: 用回传 checkpoint 重新生成 H01/H02 formal evaluation/acceptance。
8. `regenerate_claim_gate_artifacts`: H02 formal accepted 后才重算 claim safety 和 paper readiness。

当前 `gate3_remote_training` 仍被三类上游条件阻塞:

- `f02_6_decision_not_approved`
- `source_fresh_preflight_targets_open`
- `remote_packet_not_ready`

## 产物

- `2_experiment/forest_n3p/scripts/build_module2_post_f02_6_regeneration_plan.py`
- `2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py`
- `0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json`
- `0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.md`

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py` -> `4 passed in 0.29s`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_post_f02_6_regeneration_plan.py` -> pass
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_regeneration_plan` -> `status=blocked_until_f02_6_decision`

## 边界

- 本轮没有训练。
- 本轮没有运行 remote preflight。
- 本轮没有关闭 F02.6。
- 本轮没有生成 formal PPO checkpoint。
- 本轮没有放行 formal performance claim。
- Source freshness 风险仍是重生成要求, 不是算法失败或 formal result。

