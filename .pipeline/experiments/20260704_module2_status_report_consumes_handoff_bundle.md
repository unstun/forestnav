---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
scope: formal_gate
not_paper_result_material: true
---

# Module2 Status Report Consumes Handoff Bundle

## 直观结论

这次变更让 `formal_gate_status_report` 直接消费 `formal_gate_handoff_bundle`, 防止 handoff bundle 状态漂移时 status report 仍然显示安全。

它仍是只读 gate artifact: 不执行命令, 不运行远端 preflight, 不训练, 不 audit/pullback, 不写结果性论文材料。

## 改动范围

- `build_module2_formal_gate_status_report.py` 新增 `--handoff-bundle` 输入。
- status report 输出 `formal_gate_handoff_summary` 和 `current_state.handoff_bundle_*`。
- status report input safety 会捕捉:
  - handoff bundle 自身 `safety_issue_count > 0`
  - F02.6 pending 时 handoff 误放行 remote steps
  - handoff training step 未标记为 training
  - 非 training remote step 误标 training
- `test_module2_formal_gate_status_report.py` 增加 handoff bundle 消费和漂移测试。
- 刷新 status report、claim safety、paper readiness、source freshness、post-F02.6 plan/audit、formal gate gap artifact。

## 当前状态

- `formal_gate_status_report.status=formal_gate_status_blocked`
- `formal_gate_status_report.input_safety_issue_count=0`
- `handoff_bundle_status=blocked_until_f02_6_decision`
- `handoff_bundle_next_action=record_f02_6_decision`
- `handoff_bundle_remote_training_allowed_now=false`
- `claim_safety.status=blocked_formal_performance_claims`
- `paper_readiness.status=partial_methods_ready_results_blocked`

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py`
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py 2_experiment/forest_n3p/tests/test_module2_claim_safety.py 2_experiment/forest_n3p/tests/test_module2_paper_readiness.py 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_handoff_bundle.py`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_status_report`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_claim_safety`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_paper_readiness`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_source_freshness_audit`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_regeneration_plan`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_plan_audit`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_gap_audit`

