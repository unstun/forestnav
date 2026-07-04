---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Formal Gate Consumes Status Report

## 直观结论

本轮把 `formal_gate_status_report` 接入 `formal_gate_gap_audit` 的 final acceptance gap。

上一轮 status report 已经被 source freshness 跟踪, 但 final gate ledger 本身还没有直接消费它。本轮修复后, final gate audit 会读取:

- `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`

并在 status report 仍 blocked、越权执行命令/训练/preflight、允许本地训练/claim, 或存在 input safety issue 时阻塞最终 claim gate。

当前新增 blocker:

- `formal_gate_status_report_blocked`

它已经进入:

- `formal_gate_gap_audit.missing_acceptance_artifacts`
- `formal_gate_gap_audit.ordered_next_steps[claim_safety_final_gate].blocked_by`

## 当前读数

- `formal_gate_gap_audit.status=blocked_formal_gate_gaps_open`
- `formal_gate_gap_audit.formal_gate_status_report.status=formal_gate_status_blocked`
- `formal_gate_gap_audit.formal_gate_status_report.formal_claim_allowed_now=false`
- `formal_gate_gap_audit.formal_gate_status_report.local_training_allowed_now=false`
- `formal_gate_gap_audit.current_gate_state.formal_gate_status_report_status=formal_gate_status_blocked`
- `formal_gate_gap_audit.current_gate_state.formal_gate_status_report_formal_claim_allowed_now=false`
- `formal_gate_gap_audit.missing_acceptance_artifacts` 包含 `formal_gate_status_report_blocked`
- `formal_gate_gap_audit.ordered_next_steps[claim_safety_final_gate].blocked_by` 包含 `formal_gate_status_report_blocked`
- `formal_gate_status_report.permissions_now.remote_preflight_allowed_now=false`
- `formal_gate_status_report.permissions_now.remote_training_allowed_now=false`
- `formal_gate_status_report.permissions_now.formal_claim_allowed_now=false`
- `formal_gate_status_report.permissions_now.local_training_allowed_now=false`

## 改动

- `build_module2_formal_gate_gap_audit.py`
  - 新增默认输入 `DEFAULT_STATUS_REPORT`。
  - CLI 新增 `--status-report`。
  - manifest 新增 `formal_gate_status_report` 摘要。
  - `current_gate_state` 新增 status report 状态和 `formal_claim_allowed_now`。
  - final acceptance gaps 新增 `_status_report_gaps()`。
  - Markdown 新增 Formal Gate Status Report 小节。
- `test_module2_formal_gate_gap_audit.py`
  - 现有测试显式传入合成 ready status report, 避免真实工作区状态污染 tmp 测试。
  - 新增 status report blocked 消费测试。
  - 新增 status report 越权运行/claim 拒绝测试。
- regenerated:
  - `0_trials/module2_source_freshness_audit/source_freshness_audit.json/.md`
  - `0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json`
  - `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json`
  - `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json/.md`
  - `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
  - `0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json/.md`
  - `0_trials/module2_claim_safety/module2_claim_safety.json`
  - `0_trials/module2_paper_readiness/module2_paper_readiness.json`
  - `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json/.md`

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py` -> `13 passed in 0.51s`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_formal_gate_gap_audit.py` -> pass
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
- `jq '{status, formal_gate_status_report, current_gate_state, status_report_gap: (.missing_acceptance_artifacts[] | select(.gap_id=="formal_gate_status_report_blocked")), claim_step: (.ordered_next_steps[] | select(.step_id=="claim_safety_final_gate"))}' 0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json` confirmed status report gap is present.

## 边界

- 本轮没有训练。
- 本轮没有运行 remote preflight。
- 本轮没有执行 sync、audit 或 pullback。
- 本轮没有关闭 F02.6。
- 本轮没有生成 formal PPO checkpoint。
- 本轮没有写结果性论文材料。
- 这个变更只把 status report 接入 final formal gate gap ledger。
