---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
scope: formal_gate
not_paper_result_material: true
---

# Module2 Post-Plan Audits Handoff Coverage

## 直观结论

这次变更让 `post_f02_6_plan_audit` 显式审计 handoff bundle 是否被纳入 formal gate 执行链, 而不是只依赖 source freshness 或 status report 各自的单元测试。

它仍然是只读审计: 不执行计划, 不远端 preflight, 不训练, 不 audit/pullback, 不写论文结果材料。

## 新增审计

`build_module2_post_f02_6_plan_audit.py` 现在检查:

- `formal_gate_handoff_bundle` 是否出现在 source freshness target 中。
- handoff target 是否 required_before=`approved_remote_preflight`。
- post-F02.6 plan 的 `approved_remote_preflight` source-regeneration target 是否包含 handoff。
- `regenerate_preflight_gate_artifacts` stage 是否包含 `build_module2_formal_gate_handoff_bundle` 命令。
- status report 是否暴露 `formal_gate_handoff_summary`。
- status report blocked 时 handoff summary 不得允许 remote training。

## 当前状态

- `post_f02_6_plan_audit.status=post_f02_6_plan_audit_passed`
- `post_f02_6_plan_audit.audit_issue_count=0`
- `formal_gate_handoff_summary.status=blocked_until_f02_6_decision`
- `formal_gate_handoff_summary.remote_training_allowed_now=false`
- `formal_gate_status_report.status=formal_gate_status_blocked`
- `claim_safety.status=blocked_formal_performance_claims`
- `paper_readiness.status=partial_methods_ready_results_blocked`

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py`
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py 2_experiment/forest_n3p/tests/test_module2_claim_safety.py 2_experiment/forest_n3p/tests/test_module2_paper_readiness.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_handoff_bundle.py`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_plan_audit`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_gap_audit`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_status_report`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_claim_safety`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_paper_readiness`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_source_freshness_audit`

