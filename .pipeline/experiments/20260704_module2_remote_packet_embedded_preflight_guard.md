---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Remote Packet Embedded Preflight Guard

## 直观结论

本轮继续收紧 PPO 替代 RS 的 formal remote gate。没有执行远端同步、远端 preflight、PPO 训练、remote audit、pullback 或论文结果写作。

`remote_packet_safety_audit` 现在不只检查 packet 顶层状态和 allowed flags, 还会检查 packet 内嵌的 `remote_preflight` record。这样可以防止一个很具体的漂移: F02.6 仍 pending, 但 remote preflight manifest 被错误标成 ready。

## 新增约束

F02.6 pending 时:

- `remote_preflight.formal_trial_ready` 必须是 `false`。
- `remote_preflight.preflight_status` 不能是 `ready`。
- `remote_preflight.warm_start_decision` 必须是 `pending`。
- `remote_preflight.blocker_codes` 必须包含 `warm_start_decision_pending`。

Packet ready for training 时:

- `remote_preflight.formal_trial_ready` 必须是 `true`。
- `remote_preflight.preflight_status` 必须是 `ready`。
- `remote_preflight.warm_start_decision` 必须是 `approved_obstacle_summary`。

## 当前状态

- `remote_packet_safety_audit.status = remote_packet_safety_audit_passed`
- `remote_packet_safety_audit.audit_issue_count = 0`
- `packet_summary.status = blocked_until_f02_6_decision`
- `packet_summary.embedded_preflight_status = blocked`
- `packet_summary.embedded_preflight_ready = false`
- `packet_summary.embedded_preflight_warm_start_decision = pending`
- `packet_summary.remote_training_allowed_now = false`
- `cross_gate_summary.post_plan_status_report_status = formal_gate_status_blocked`

这里的 pass 只证明 packet 和内嵌 preflight 在当前 F02.6 pending 状态下正确 blocked, 不是远端执行许可。

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py`
  - 结果: 9 passed。
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py 2_experiment/forest_n3p/tests/test_module2_remote_formal_execution_packet.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_missing_artifacts_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_closure_checklist.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py 2_experiment/forest_n3p/tests/test_module2_claim_safety.py 2_experiment/forest_n3p/tests/test_module2_paper_readiness.py 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py`
  - 结果: 65 passed。
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_remote_packet_safety_audit.py`
  - 结果: 通过。
- `git diff --check`
  - 结果: 通过。

## 剩余 formal gate 缺口

- F02.6 decision record 仍是 `pending_human_decision`。
- remote preflight manifest 仍是 pending/blocked, 不可作为 approved preflight。
- remote sync / preflight / training / audit / pullback 全部仍不允许执行。
- formal PPO checkpoint、training manifest、eval rows、formal audit、pullback hash 仍缺。
- H01/H02 formal acceptance、claim safety final gate、paper readiness final gate 仍 blocked。
