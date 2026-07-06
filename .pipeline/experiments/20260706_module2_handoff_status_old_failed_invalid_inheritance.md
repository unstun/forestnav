---
origin: ai+local-source
reviewed: false
date: 2026-07-06
status: recorded
scope: module2 formal gate handoff and status-report inheritance of next-success artifact split and old failed-run invalid-substitute boundary
---

# Module2 Handoff / Status Old-Failed Invalid Inheritance

## Purpose

The previous gate pass pushed `old_failed_run_artifacts_invalid_for_next_success_attempt=true` through protocol status, post-F02.6 plan audit, remote safety, and mainline audit. This record extends the same boundary into the formal handoff and status report layers, so downstream readers do not see only the ten-artifact count while losing the rule that failed-run artifacts cannot be reused as a success-attempt substitute.

## Change

- `formal_gate_handoff_bundle.protocol_lane_status_summary` now carries:
  - `next_success_attempt_artifact_category_counts`
  - `post_decision_contract_plan_shared_artifact_category_counts`
  - `old_failed_run_artifacts_invalid_for_next_success_attempt`
  - `post_decision_contract_plan_old_failed_run_artifacts_invalid_for_next_success_attempt`
- `formal_gate_status_report.formal_gate_handoff_summary` now consumes the same fields from the handoff bundle and reports input-safety issues if they drift.
- Regenerated the affected read-only artifacts in dependency order: handoff bundle, status report, post-F02.6 plan audit, remote packet safety audit, and mainline formal gate state audit.

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_handoff_bundle.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py` -> `53 passed`
- Regenerated:
  - `0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json`
  - `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
  - `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
  - `0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`
  - `0_trials/module2_mainline_formal_gate_state_audit/mainline_formal_gate_state_audit.json`

## Boundary

This is not training, remote preflight, formal evaluation, formal claim, or paper-result material. The top-level gate remains `protocol_lane_decision`; the only allowed action remains `record_protocol_lane_decision`.
