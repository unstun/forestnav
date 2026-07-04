---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Source Freshness Tracks Status Report

## 直观结论

本轮把 `formal_gate_status_report` 纳入 source freshness 默认跟踪目标, 防止它成为一个孤立的旁路报告。

现在 source freshness 会检查:

- `artifact_id=formal_gate_status_report`
- `path=0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
- `required_before=formal_claim_gate`

当前它被判定为:

- `freshness_state=current_dirty`
- `regenerate_before_formal_execution=true`

也就是说, status report 虽然提供了当前 formal gate 的单一入口, 但它本身也必须在 formal claim gate 前被 source-fresh regeneration 覆盖, 不能拿旧状态报告当最终 claim 依据。

## 当前 gate 读数

- `source_freshness.artifact_count=14`
- `source_freshness.ordered_regeneration_targets | length = 13`
- `source_freshness.status_report.required_before=formal_claim_gate`
- `missing_artifacts.source_fresh_regeneration_targets` 包含 `formal_gate_status_report`
- `closure_checklist.preflight_source_fresh_regeneration.required_items` 包含 `formal_gate_status_report`
- `formal_gate_status_report.source_fresh_preflight.missing_items` 包含 `formal_gate_status_report`
- `formal_gate_status_report.permissions_now.remote_preflight_allowed_now=false`
- `formal_gate_status_report.permissions_now.remote_training_allowed_now=false`
- `formal_gate_status_report.permissions_now.formal_claim_allowed_now=false`
- `formal_gate_status_report.next_blocked_lane.lane_id=decision`

## 改动

- `build_module2_source_freshness_audit.py`
  - `DEFAULT_ARTIFACTS` 新增 `formal_gate_status_report`, category=`formal_gate`, required_before=`formal_claim_gate`。
- `test_module2_source_freshness_audit.py`
  - CLI 测试断言默认 artifact records 包含 `formal_gate_status_report`。
  - 断言其 regeneration target 的 `required_before=formal_claim_gate`。
- regenerated:
  - `0_trials/module2_source_freshness_audit/source_freshness_audit.json/.md`
  - `0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json/.md`
  - `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json/.md`
  - `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json/.md`
  - `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json/.md`
  - `0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json/.md`
  - `0_trials/module2_claim_safety/module2_claim_safety.json/.md`
  - `0_trials/module2_paper_readiness/module2_paper_readiness.json/.md`
  - `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json/.md`

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py` -> `3 passed in 0.39s`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_source_freshness_audit.py` -> pass
- Gate regeneration chain completed with final statuses:
  - `source_freshness_risks_recorded_gate_still_blocked`
  - `blocked_until_f02_6_decision`
  - `formal_gate_missing_artifacts_open`
  - `blocked_formal_gate_gaps_open`
  - `post_f02_6_plan_audit_passed`
  - `formal_gate_closure_blocked`
  - `blocked_formal_performance_claims`
  - `partial_methods_ready_results_blocked`
  - `formal_gate_status_blocked`
- `jq '.ordered_regeneration_targets | length, (.[] | select(.artifact_id=="formal_gate_status_report"))' 0_trials/module2_source_freshness_audit/source_freshness_audit.json` confirmed status report target exists.
- `jq '.missing_evidence_groups[] | select(.group_id=="source_fresh_regeneration_targets") | ...' 0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json` confirmed missing-artifacts consumes the target.
- `jq '.closure_checklist[] | select(.checklist_id=="preflight_source_fresh_regeneration") | ...' 0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json` confirmed closure checklist consumes the target.
- `jq '.formal_gate_lanes[] | select(.lane_id=="source_fresh_preflight") | ...' 0_trials/module2_formal_gate_status_report/formal_gate_status_report.json` confirmed status report exposes the target as blocked source-fresh work.

## 边界

- 本轮没有训练。
- 本轮没有运行 remote preflight。
- 本轮没有执行 sync、audit 或 pullback。
- 本轮没有关闭 F02.6。
- 本轮没有生成 formal PPO checkpoint。
- 本轮没有写结果性论文材料。
- 这个变更只把 status report 纳入 source freshness 和 formal gate 再生成链。
