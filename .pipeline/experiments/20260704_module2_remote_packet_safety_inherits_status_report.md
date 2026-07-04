---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Remote Packet Safety Inherits Status Report Gate

## 直观结论

本轮继续加固 PPO 替代 RS formal gate, 只修改本地审计逻辑与再生成 artifact。没有执行 `ssh`、`rsync`、远端 preflight、PPO 训练、remote audit、pullback 或论文结果写作。

`remote_packet_safety_audit` 现在不再只相信 remote packet、F02.6 decision gate 和 post-F02.6 plan 的训练开关; 它还会检查 post-plan audit 是否已经消费 `formal_gate_status_report`, 并读取 `post_f02_6_plan_audit.status_report_summary`。

## 新增约束

- 如果 `post_f02_6_plan_audit.inputs.formal_gate_status_report` 缺失, remote packet safety audit 失败。
- 如果 `post_f02_6_plan_audit.status_report_summary` 缺失, remote packet safety audit 失败。
- 如果 status report 的 `local_training_allowed_now` 不是 `false`, remote packet safety audit 失败。
- 如果 status report 仍不是 `formal_gate_status_ready_for_claim_audit`, 但 remote packet 标记为 ready 或放行 remote preflight/training/audit, remote packet safety audit 失败。

## 当前状态

- `remote_packet_safety_audit.status = remote_packet_safety_audit_passed`
- `remote_packet_safety_audit.audit_issue_count = 0`
- `packet_summary.status = blocked_until_f02_6_decision`
- `packet_summary.remote_preflight_allowed_now = false`
- `packet_summary.remote_training_allowed_now = false`
- `packet_summary.remote_audit_allowed_now = false`
- `cross_gate_summary.post_plan_status_report_status = formal_gate_status_blocked`
- `cross_gate_summary.post_plan_status_report_next_blocked_lane_id = decision`

这里的 `passed` 只证明 packet 安全地保持 blocked, 不是 remote execution 许可。

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py`
  - 结果: 7 passed。
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_missing_artifacts_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_closure_checklist.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py 2_experiment/forest_n3p/tests/test_module2_claim_safety.py 2_experiment/forest_n3p/tests/test_module2_paper_readiness.py 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py`
  - 结果: 56 passed。
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_remote_packet_safety_audit.py`
  - 结果: 通过。
- `git diff --check`
  - 结果: 通过。

## 剩余 formal gate 缺口

- F02.6 decision record 仍是 `pending_human_decision`。
- Status report 仍是 `formal_gate_status_blocked`, next blocked lane 是 `decision`。
- Remote preflight、remote PPO training、remote audit、pullback 都仍未放行。
- Gate3 formal training/eval/audit artifacts 仍缺。
- H01/H02 formal acceptance、claim safety final regeneration、paper readiness final regeneration 仍 blocked。
