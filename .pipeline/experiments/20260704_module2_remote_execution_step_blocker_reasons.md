---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Remote Execution Step Blocker Reasons

## 直观结论

本轮继续收紧 PPO 替代 RS 的 formal remote gate。没有执行远端同步、远端 preflight、PPO 训练、remote audit、pullback 或论文结果写作。

之前 remote packet 的远端动作只有 `allowed_now=false`, 但机器不能直接知道每个 false 是因为什么。现在每个 disabled execution step 都必须带 `blocked_by`。这让 formal gate 更像真正的执行闸门, 而不是只靠一个布尔值。

## 新增约束

`remote_formal_execution_packet.execution_steps` 现在包含:

- `sync_to_remote.blocked_by`
- `run_remote_preflight.blocked_by`
- `run_remote_training.blocked_by`
- `run_remote_audit.blocked_by`

`remote_packet_safety_audit` 新增检查:

- `allowed_now=false` 的 step 必须有非空 `blocked_by`。
- `allowed_now=true` 的 step 不得携带 `blocked_by`。
- F02.6 pending 时, sync/preflight 必须包含 `requires_dr_sun_approval`。
- packet blocked 时, training/audit 必须包含 `remote_packet_not_ready`。

## 当前状态

- `remote_formal_execution_packet.status = blocked_until_f02_6_decision`
- `sync_to_remote.allowed_now = false`
- `sync_to_remote.blocked_by = [requires_dr_sun_approval]`
- `run_remote_preflight.allowed_now = false`
- `run_remote_preflight.blocked_by = [requires_dr_sun_approval]`
- `run_remote_training.allowed_now = false`
- `run_remote_training.blocked_by = [requires_dr_sun_approval, f02_6_warm_start_decision_pending, missing_module2_rl_rs_checkpoint, remote_packet_not_ready]`
- `run_remote_audit.allowed_now = false`
- `run_remote_audit.blocked_by = [requires_dr_sun_approval, f02_6_warm_start_decision_pending, missing_module2_rl_rs_checkpoint, remote_packet_not_ready]`
- `remote_packet_safety_audit.status = remote_packet_safety_audit_passed`
- `remote_packet_safety_audit.audit_issue_count = 0`

这里的 pass 只证明 remote packet 的 disabled 状态可解释、可审计, 不是远端执行许可。

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_remote_formal_execution_packet.py 2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py`
  - 结果: 13 passed。
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_remote_formal_execution_packet.py 2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_missing_artifacts_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_closure_checklist.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py 2_experiment/forest_n3p/tests/test_module2_claim_safety.py 2_experiment/forest_n3p/tests/test_module2_paper_readiness.py 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py`
  - 结果: 66 passed。
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_remote_formal_execution_packet.py 2_experiment/forest_n3p/scripts/build_module2_remote_packet_safety_audit.py`
  - 结果: 通过。
- `git diff --check`
  - 结果: 通过。

## 剩余 formal gate 缺口

- F02.6 decision record 仍是 `pending_human_decision`。
- remote sync / preflight / training / audit / pullback 全部仍不允许执行。
- formal PPO checkpoint、training manifest、eval rows、formal audit、pullback hash 仍缺。
- H01/H02 formal acceptance、claim safety final gate、paper readiness final gate 仍 blocked。
