---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
topic: module2_rl_rs_formal_gate
not_paper_result_material: true
---

# Module2 status report exposes closure remote stages

## 直观结论

本轮只加固 formal gate status report, 不训练、不远端 preflight、不远端同步、不写结果性论文材料。

上一轮 `formal_gate_closure_checklist` 已经能显示 post-plan 的三个远端阶段。本轮把这份摘要转发到 central `formal_gate_status_report`, 让总状态报告同时包含:

- remote packet 的低层执行步骤: sync / preflight / training / audit
- closure checklist 的高层远端阶段: approved preflight / Gate3 remote training / audit pullback

这样读取一个 status report 就能看到“为什么不能进入远端执行链”, 而不需要在多个 JSON 之间人工拼接。

## 改动范围

- `2_experiment/forest_n3p/scripts/build_module2_formal_gate_status_report.py`
  - 新增 `closure_remote_stage_summary`。
  - `current_state` 新增:
    - `closure_remote_preflight_allowed_now`
    - `closure_remote_training_allowed_now`
    - `closure_remote_audit_pullback_allowed_now`
  - 新增 input safety:
    - closure checklist 必须暴露 `post_plan_remote_stage_summary`。
    - disabled closure remote stage 必须有 `blocked_by`。
    - enabled closure remote stage 不得携带 `blocked_by`。
    - `gate3_remote_training` 必须标记 `runs_training=true`。
    - approved remote preflight 必须标记 `runs_remote_preflight=true`。
    - remote preflight/training stage 必须绑定 `gpu3070ti-relay`。
  - Markdown 新增 `Closure Remote Stages`。
- `2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py`
  - 覆盖 pending chain 的 closure remote stage 摘要。
  - 覆盖 synthetic complete chain 的 allowed/blocked_by 清空语义。
  - 新增 closure remote stage summary 缺失和 disabled stage 缺 blocker 的反例。

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

closure remote stages:

- `approved_remote_preflight.allowed_now=false`
- `gate3_remote_training.allowed_now=false`
- `gate3_remote_audit_pullback.allowed_now=false`
- `gate3_remote_training.host=gpu3070ti-relay`

remote packet execution steps:

- `sync_to_remote.allowed_now=false`
- `run_remote_preflight.allowed_now=false`
- `run_remote_training.allowed_now=false`
- `run_remote_audit.allowed_now=false`

## 验证

```bash
PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py
```

结果: `7 passed in 0.42s`

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_closure_checklist.py \
  2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py \
  2_experiment/forest_n3p/tests/test_module2_claim_safety.py \
  2_experiment/forest_n3p/tests/test_module2_paper_readiness.py \
  2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py \
  2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py
```

结果: `50 passed in 2.68s`

## 边界

- 未执行 `ssh gpu3070ti-relay`。
- 未执行 `rsync`。
- 未执行远端 preflight。
- 未执行本地或远端训练。
- 未新增 formal result 或论文性能 claim。
- F02.6 warm-start 人类决策仍 pending。
