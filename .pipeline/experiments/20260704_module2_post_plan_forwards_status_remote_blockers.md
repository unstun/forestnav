---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
topic: module2_rl_rs_formal_gate
not_paper_result_material: true
---

# Module2 post-plan forwards status-report remote blockers

## 直观结论

本轮只加固 formal gate 的信息传递链, 不训练、不远端 preflight、不远端同步、不写结果性论文材料。

上一轮 `formal_gate_status_report` 已经能显示 remote packet 四个执行步骤的 `allowed_now/runs_training/blocked_by`。本轮进一步要求:

- `post_f02_6_plan_audit.status_report_summary` 必须转发这份 remote execution step summary。
- `remote_packet_safety_audit.cross_gate_summary` 必须继续暴露 post-plan 转发出的 summary。
- `remote_packet_safety_audit` 必须检查 post-plan 转发摘要与 remote packet 本体一致。

这样 Dr Sun 或后续 agent 不需要跨多个 JSON 猜状态, 就能从 post-plan/remote-safety 链条看到为什么当前不能 sync/preflight/train/audit。

## 改动范围

- `2_experiment/forest_n3p/scripts/build_module2_post_f02_6_plan_audit.py`
  - `status_report_summary` 新增 `remote_execution_step_summary`。
  - 新增检查: status report 必须暴露 remote step summary。
  - 新增检查: formal gate blocked 时, status report 不得把任何 remote step 标为 allowed。
  - Markdown 新增 `Status Report Remote Execution Steps`。
- `2_experiment/forest_n3p/scripts/build_module2_remote_packet_safety_audit.py`
  - `cross_gate_summary` 新增 `post_plan_status_report_remote_execution_step_summary`。
  - 新增检查: post-plan 必须转发 status report remote step summary。
  - 新增检查: post-plan/status-report 的 remote step allowed flags 与 blocked_by 必须和 remote packet 一致。
- 测试覆盖:
  - `test_module2_post_f02_6_plan_audit.py`
  - `test_module2_remote_packet_safety_audit.py`

## 再生产物

- `0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json`
- `0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.md`
- `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
- `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.md`
- `0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`

## 当前 gate 状态

- `post_f02_6_plan_audit.status=post_f02_6_plan_audit_passed`
- `post_f02_6_plan_audit.audit_issue_count=0`
- `remote_packet_safety_audit.status=remote_packet_safety_audit_passed`
- `remote_packet_safety_audit.audit_issue_count=0`
- `training_allowed_now=false`
- `remote_preflight_allowed_now=false`
- `next_blocked_lane_id=decision`

当前转发的 remote step 状态:

- `sync_to_remote.allowed_now=false`, blocked by `requires_dr_sun_approval`
- `run_remote_preflight.allowed_now=false`, blocked by `requires_dr_sun_approval`
- `run_remote_training.allowed_now=false`, blocked by `requires_dr_sun_approval`, `f02_6_warm_start_decision_pending`, `missing_module2_rl_rs_checkpoint`, `remote_packet_not_ready`
- `run_remote_audit.allowed_now=false`, blocked by `requires_dr_sun_approval`, `f02_6_warm_start_decision_pending`, `missing_module2_rl_rs_checkpoint`, `remote_packet_not_ready`

## 验证

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py \
  2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py
```

结果: `26 passed in 1.33s`

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py \
  2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py \
  2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py \
  2_experiment/forest_n3p/tests/test_module2_claim_safety.py \
  2_experiment/forest_n3p/tests/test_module2_paper_readiness.py \
  2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py \
  2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py
```

结果: `47 passed in 2.33s`

## 边界

- 未执行 `ssh gpu3070ti-relay`。
- 未执行 `rsync`。
- 未执行远端 preflight。
- 未执行本地或远端训练。
- 未新增 formal result 或论文性能 claim。
- F02.6 warm-start 人类决策仍 pending。
