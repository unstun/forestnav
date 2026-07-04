---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
topic: module2_rl_rs_formal_gate
not_paper_result_material: true
---

# Module2 status report exposes remote execution blockers

## 直观结论

本轮只加固 formal gate, 不训练、不远端 preflight、不写结果性论文材料。

`formal_gate_status_report` 现在直接暴露 remote packet 中四个执行步骤的当前许可与阻塞原因:

- `sync_to_remote`
- `run_remote_preflight`
- `run_remote_training`
- `run_remote_audit`

当前四个步骤仍全部 `allowed_now=false`。训练和 audit 的 blocker 明确包含:

- `requires_dr_sun_approval`
- `f02_6_warm_start_decision_pending`
- `missing_module2_rl_rs_checkpoint`
- `remote_packet_not_ready`

## 改动范围

- `2_experiment/forest_n3p/scripts/build_module2_formal_gate_status_report.py`
  - 新增 `remote_execution_step_summary`。
  - 在 `current_state` 中新增 remote packet 四个步骤的 `*_allowed_now` 字段。
  - 新增输入安全检查: disabled step 必须有 `blocked_by`; enabled step 不得携带 `blocked_by`; 只有 `run_remote_training` 可标记 `runs_training=true`。
  - Markdown 增加 `Remote Execution Steps` 小节。
- `2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py`
  - 覆盖 pending chain 的 remote step blocker 展示。
  - 覆盖 synthetic complete chain 的 remote step allowed/blocked_by 清空语义。
  - 新增 remote step 缺 blocker 的输入安全测试。
- `2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py`
  - 修正测试语义: `formal_gate_status_report` 必须被 source freshness 审计; 只有 stale/dirty 时才必须出现在 ordered regeneration targets。

## 再生产物

- `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
- `0_trials/module2_formal_gate_status_report/formal_gate_status_report.md`
- `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
- `0_trials/module2_claim_safety/module2_claim_safety.json`
- `0_trials/module2_paper_readiness/module2_paper_readiness.json`
- `0_trials/module2_source_freshness_audit/source_freshness_audit.json`
- `0_trials/module2_source_freshness_audit/source_freshness_audit.md`
- `0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`

## 当前 gate 状态

- `formal_gate_status_report.status=formal_gate_status_blocked`
- `input_safety_issue_count=0`
- `next_blocked_lane.lane_id=decision`
- `permissions_now.local_training_allowed_now=false`
- `permissions_now.remote_preflight_allowed_now=false`
- `permissions_now.remote_training_allowed_now=false`
- `permissions_now.formal_claim_allowed_now=false`
- `remote_packet_safety_audit.status=remote_packet_safety_audit_passed`

## 验证

```bash
PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py
```

结果: `5 passed in 0.35s`

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py \
  2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py \
  2_experiment/forest_n3p/tests/test_module2_claim_safety.py \
  2_experiment/forest_n3p/tests/test_module2_paper_readiness.py \
  2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py \
  2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py
```

结果: `39 passed in 1.79s`

## 边界

- 未执行 `ssh gpu3070ti-relay`。
- 未执行 `rsync`。
- 未执行远端 preflight。
- 未执行本地或远端训练。
- 未新增结果性论文 claim。
- F02.6 warm-start 人类决策仍 pending。
