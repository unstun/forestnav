---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
scope: formal_gate
not_paper_result_material: true
---

# Module2 F02.6 decision intake

## What changed

新增只读 builder:

- `2_experiment/forest_n3p/scripts/build_module2_f02_6_decision_intake.py`

新增产物:

- `0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json`
- `0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.md`

这个 artifact 的目的不是记录真实 F02.6 决策, 而是把 Dr Sun 关闭 F02.6 时需要填写和满足的条件集中成一个可审计入口。

## Current state

当前状态:

- `f02_6_decision_intake.status=f02_6_decision_intake_pending_clean`
- `audit_issue_count=0`
- `record_status=pending_human_decision`
- `next_blocked_lane=decision`
- `missing_deliverable_count=10`
- `remote_preflight_allowed_now=false`
- `remote_training_allowed_now=false`
- `formal_claim_allowed_now=false`

## Decision intake contract

非 pending 决策必须包含:

- `decision`: `approve_obstacle_summary_warm_start` 或 `reject_obstacle_summary_warm_start`
- `decider`: 必须等于 `Dr Sun`
- `decision_note`: Dr Sun 的人类可读批准/驳回理由

artifact 同时写出两条 command template:

- approve obstacle-summary warm-start
- reject obstacle-summary warm-start

## Invalid inputs

当前 intake 显式拒绝或标记以下无效输入:

- decider 不是 Dr Sun
- 批准/驳回缺少 decision note
- 手动改 downstream JSON permission flag
- local training output
- paper result table 或 claim preview

## Verification

Commands run:

```bash
PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_f02_6_decision_intake.py
PYTHONPATH=2_experiment python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_f02_6_decision_intake.py 2_experiment/forest_n3p/tests/test_module2_f02_6_decision_intake.py
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_decision_intake
jq '{status, audit_issue_count, current_state:{record_status:.current_state.record_status,next_blocked_lane:.current_state.next_blocked_lane,missing:.current_state.missing_deliverable_count,remote_preflight:.current_state.status_report_remote_preflight_allowed_now,remote_training:.current_state.status_report_remote_training_allowed_now,formal_claim:.current_state.status_report_formal_claim_allowed_now}, contract:.decision_intake_contract.required_record_fields_for_non_pending_decision}' 0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json
```

Observed:

- Targeted tests: 4 passed.
- `py_compile` completed successfully.
- Real artifact status: `f02_6_decision_intake_pending_clean`.
- Real artifact audit issues: 0.

## Boundary

This task did not:

- approve or reject F02.6,
- edit the decision record to a non-pending state,
- run ssh/rsync,
- run remote preflight,
- run local or remote training,
- run remote audit/pullback,
- run H01/H02 formal evaluation,
- write result-like paper material.
