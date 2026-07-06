---
origin: ai+local-source
reviewed: false
date: 2026-07-06
status: recorded
scope: module2 formal gate protocol status, post-plan audit, remote safety, and mainline inheritance of old failed-run invalid-substitute boundary
---

# Module2 Protocol Status / Remote / Mainline Old-Failed Invalid Inheritance

## Purpose

This record closes a gate-propagation gap in the PPO/RL-RS formal gate chain. Upstream `formal_gate_next_round_requirements`, `protocol_lane_decision_record`, and `post_decision_contract_plan` already distinguish the current failed run from a future success attempt, but the status/remote/mainline layers still mostly displayed the ten-artifact count and category split. This could let a downstream overview lose the explicit boundary that old failed-run artifacts are invalid substitutes for the next success attempt.

## Change

- `protocol_lane_status_report` now exposes and audits:
  - `post_decision_contract_plan_shared_artifact_category_counts`
  - `post_decision_contract_plan_old_failed_run_artifacts_invalid_for_next_success_attempt`
  - `old_failed_run_artifacts_invalid_for_next_success_attempt`
- `post_f02_6_plan_audit` now preserves those fields in `protocol_lane_status_summary` and fails if they drift.
- `remote_packet_safety_audit` now requires the same protocol summary fields before it can pass.
- `mainline_formal_gate_state_audit` now normalizes and audits those fields, and the mainline fixture requires the old failed-run invalid boundary in the current formal-gate section.

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_protocol_lane_status_report.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py 2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py 2_experiment/forest_n3p/tests/test_module2_mainline_formal_gate_state_audit.py` -> `80 passed`
- `git diff --check` -> clean
- Regenerated artifacts:
  - `0_trials/module2_formal_gate_protocol_lane_status_report/protocol_lane_status_report.json`
  - `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
  - `0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`
  - `0_trials/module2_mainline_formal_gate_state_audit/mainline_formal_gate_state_audit.json`

## Current Boundary

The current top-level gate remains `protocol_lane_decision`. The only allowed action remains `record_protocol_lane_decision`. This record does not authorize local training, remote preflight, remote training, formal evaluation, formal claims, or paper-result material.

Next success attempt still requires fresh `contract/training/evaluation/acceptance/formal_acceptance = 1/3/2/3/1` artifacts. The old failed-run artifacts remain invalid substitutes.
