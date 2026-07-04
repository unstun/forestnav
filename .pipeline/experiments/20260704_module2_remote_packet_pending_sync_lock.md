---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Remote Packet Pending Sync Lock

## 直观结论

本轮继续收紧 PPO 替代 RS formal execution gate。没有执行远端同步、远端 preflight、PPO 训练、remote audit、pullback 或论文结果写作。

之前 `remote_formal_execution_packet` 在 F02.6 pending 时仍把 `sync_to_remote.allowed_now` 标为 `true`。虽然 sync 不是训练, 但它是远端副作用动作, 不应该在 decision lane 和 status report 仍 blocked 时被机器标成当前可执行。

现在:

- F02.6 pending 时, `sync_to_remote.allowed_now=false`。
- F02.6 approved 后, packet 才能把 sync 标为 allowed。
- `remote_packet_safety_audit` 会在 pending decision 或 blocked status report 下发现 sync allowed 时失败。

## 当前状态

- `remote_formal_execution_packet.status = blocked_until_f02_6_decision`
- `remote_formal_execution_packet.ready_to_run_remote_training = false`
- `execution_steps.sync_to_remote.allowed_now = false`
- `execution_steps.run_remote_preflight.allowed_now = false`
- `execution_steps.run_remote_training.allowed_now = false`
- `execution_steps.run_remote_audit.allowed_now = false`
- `remote_packet_safety_audit.status = remote_packet_safety_audit_passed`
- `remote_packet_safety_audit.audit_issue_count = 0`
- `formal_gate_status_report.status = formal_gate_status_blocked`
- `formal_gate_status_report.next_blocked_lane = decision`

这个 pass 只证明 packet 在当前 F02.6 pending 状态下安全 blocked, 不是远端执行许可。

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_remote_formal_execution_packet.py 2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py`
  - 结果: 10 passed。
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_remote_formal_execution_packet.py 2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_missing_artifacts_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_closure_checklist.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py 2_experiment/forest_n3p/tests/test_module2_claim_safety.py 2_experiment/forest_n3p/tests/test_module2_paper_readiness.py 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py`
  - 结果: 63 passed。
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_remote_formal_execution_packet.py 2_experiment/forest_n3p/scripts/build_module2_remote_packet_safety_audit.py`
  - 结果: 通过。
- `git diff --check`
  - 结果: 通过。

## 剩余 formal gate 缺口

- F02.6 decision record 仍是 `pending_human_decision`。
- remote sync / preflight / training / audit / pullback 全部仍不允许执行。
- formal PPO checkpoint、training manifest、eval rows、formal audit、pullback hash 仍缺。
- H01/H02 formal acceptance、claim safety final gate、paper readiness final gate 仍 blocked。
