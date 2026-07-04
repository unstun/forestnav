---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
scope: formal_gate
not_paper_result_material: true
---

# Module2 Handoff Source Freshness Coverage

## 直观结论

这次变更把 `formal_gate_handoff_bundle` 纳入 source freshness 审计, 防止 handoff bundle 成为未纳管的远端执行旁路。

当前结果仍然是 formal gate blocked: F02.6 未关闭, 不允许本地训练、远端 preflight、远端训练、audit、pullback 或 formal performance claim。

## 改动范围

- `build_module2_source_freshness_audit.py` 新增 artifact target: `formal_gate_handoff_bundle`。
- `build_module2_post_f02_6_regeneration_plan.py` 新增 handoff bundle regeneration command mapping。
- `test_module2_source_freshness_audit.py` 和 `test_module2_post_f02_6_regeneration_plan.py` 覆盖该 target。
- 刷新:
  - `0_trials/module2_source_freshness_audit/source_freshness_audit.json`
  - `0_trials/module2_source_freshness_audit/source_freshness_audit.md`
  - `0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json`
  - `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
  - `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json`

## 当前状态

- source freshness artifact count: `15`
- `formal_gate_handoff_bundle.required_before=approved_remote_preflight`
- `formal_gate_handoff_bundle.freshness_state=historical_clean`
- post-F02.6 regeneration plan 包含 `build_module2_formal_gate_handoff_bundle`
- post-plan audit 仍为 `post_f02_6_plan_audit_passed`
- formal gate gap 仍为 `blocked_formal_gate_gaps_open`

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_source_freshness_audit`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_regeneration_plan`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_plan_audit`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_gap_audit`

