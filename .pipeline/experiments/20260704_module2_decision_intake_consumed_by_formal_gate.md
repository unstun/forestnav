---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
scope: formal_gate
not_paper_result_material: true
---

# Module2 decision intake consumed by formal gate

## What changed

将 `f02_6_decision_intake` 接入 formal gate 消费链:

- `build_module2_formal_gate_status_report.py` 默认读取 `0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json`。
- status report 新增 `f02_6_decision_intake_summary`。
- status report input safety 会在 intake 缺失、失败、pending 时误放行 preflight/training/claim, 或 closed intake 非 Dr Sun 决策时阻塞。
- `build_module2_claim_safety.py` 继承 status report 的 decision-intake summary, 并在 summary 缺失/失败/误放行时加入 formal performance blockers。
- `build_module2_source_freshness_audit.py` 将 `f02_6_decision_intake` 纳入 `approved_remote_preflight` 前必须跟踪的 artifact target。

## Current state

刷新后的真实 artifact 状态:

- `formal_gate_status_report.status=formal_gate_status_blocked`
- `formal_gate_status_report.f02_6_decision_intake_summary.status=f02_6_decision_intake_pending_clean`
- `formal_gate_status_report.f02_6_decision_intake_summary.audit_issue_count=0`
- `formal_gate_status_report.permissions_now.remote_preflight_allowed_now=false`
- `formal_gate_status_report.permissions_now.remote_training_allowed_now=false`
- `formal_gate_status_report.permissions_now.formal_claim_allowed_now=false`
- `module2_claim_safety.status=blocked_formal_performance_claims`
- `module2_claim_safety.status_report_decision_intake_summary.status=f02_6_decision_intake_pending_clean`
- `module2_paper_readiness.status=partial_methods_ready_results_blocked`
- `source_freshness_audit.artifact_count=17`
- `source_freshness_audit` now tracks `f02_6_decision_intake`, required before `approved_remote_preflight`

## Verification

Commands run:

```bash
PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py 2_experiment/forest_n3p/tests/test_module2_claim_safety.py 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py
PYTHONPATH=2_experiment python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_formal_gate_status_report.py 2_experiment/forest_n3p/scripts/build_module2_claim_safety.py 2_experiment/forest_n3p/scripts/build_module2_source_freshness_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py 2_experiment/forest_n3p/tests/test_module2_claim_safety.py 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_status_report
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_claim_safety
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_paper_readiness
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_source_freshness_audit
```

Observed:

- Targeted tests: 33 passed.
- `py_compile` completed successfully.
- Real status report still blocks F02.6, remote preflight, remote training, and formal claim.
- Source freshness now tracks 17 artifacts including `f02_6_decision_intake`.

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
