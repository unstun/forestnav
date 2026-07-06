---
origin: ai+local-source
reviewed: false
date: 2026-07-06
status: recorded
scope: module2 formal gate propagation of next success-attempt invalid substitutes
---

# Module2 Invalid Substitute Inheritance

## Purpose

The previous gate pass propagated next success-attempt artifact IDs, expected paths, and proof requirements through protocol status, handoff, and formal status artifacts. This record closes the adjacent evidence-quality gap: downstream readers now also inherit the exact invalid substitutes for each next success-attempt artifact.

## Change

- `protocol_lane_status_report.current_status` carries `next_success_attempt_artifact_invalid_substitutes_by_id`.
- `formal_gate_handoff_bundle.protocol_lane_status_summary` consumes and audits the invalid-substitute map.
- `formal_gate_status_report.formal_gate_handoff_summary` consumes and audits the invalid-substitute map.
- The map covers all ten next success-attempt artifacts and explicitly rejects local PPO outputs, failed-run checkpoints, smoke CSVs, paper-table previews, missing hash records, and blocked H02 acceptance as substitutes for formal success evidence.

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_handoff_bundle.py` -> `12 passed`
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py` -> `41 passed`
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_protocol_lane_status_report.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_handoff_bundle.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py 2_experiment/forest_n3p/tests/test_module2_mainline_formal_gate_state_audit.py` -> `77 passed`
- JSON spot checks:
  - `protocol_lane_status_report.status=protocol_lane_status_blocked_pending_lane_decision`, `audit_issue_count=0`
  - `formal_gate_handoff_bundle.status=blocked_until_protocol_lane_decision`, `safety_issue_count=0`
  - `formal_gate_status_report.status=formal_gate_status_blocked`, `input_safety_issue_count=0`
  - `mainline_formal_gate_state_audit.status=mainline_formal_gate_state_consistent_blocked`, `audit_issue_count=0`

## Boundary

This is a read-only formal-gate inheritance change. It does not select a protocol lane, draft or approve a contract, run local PPO training, run remote preflight, run remote training, run formal evaluation, accept H02 output, write paper-result material, or claim PPO has replaced RS. The only allowed next action remains `record_protocol_lane_decision`.
