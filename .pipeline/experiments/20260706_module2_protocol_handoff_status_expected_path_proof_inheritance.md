---
origin: ai+local-source
reviewed: false
date: 2026-07-06
status: recorded
scope: module2 formal gate propagation of next success-attempt expected paths and proof requirements
---

# Module2 Expected Path / Proof Inheritance

## Purpose

The previous gate pass propagated the next success-attempt artifact IDs through handoff and status report. This record extends the same read-only chain to expected paths and proof requirements, so the gate does not only name missing artifacts but also preserves where each fresh artifact must appear and what evidence would prove it.

## Change

- `protocol_lane_status_report.current_status` now carries:
  - `next_success_attempt_artifact_expected_paths_by_id`
  - `next_success_attempt_artifact_proof_requirements_by_id`
- `formal_gate_handoff_bundle.protocol_lane_status_summary` consumes and audits both maps.
- `formal_gate_status_report.formal_gate_handoff_summary` consumes and audits both maps.
- The expected path map covers all ten next success-attempt artifacts: one contract, three training artifacts, two evaluation artifacts, three acceptance artifacts, and one formal acceptance artifact.

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_protocol_lane_status_report.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_handoff_bundle.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py 2_experiment/forest_n3p/tests/test_module2_mainline_formal_gate_state_audit.py` -> `77 passed`
- `git diff --check` -> clean
- JSON spot checks:
  - `protocol_lane_status_report.status=protocol_lane_status_blocked_pending_lane_decision`, `audit_issue_count=0`, `proof_count=10`
  - `formal_gate_handoff_bundle.status=blocked_until_protocol_lane_decision`, `safety_issue_count=0`, `proof_count=10`
  - `formal_gate_status_report.status=formal_gate_status_blocked`, `input_safety_issue_count=0`, `proof_count=10`
  - `mainline_formal_gate_state_audit.status=mainline_formal_gate_state_consistent_blocked`, `audit_issue_count=0`

## Boundary

This is a read-only formal-gate inheritance change. It does not select a protocol lane, draft or approve a contract, run local PPO training, run remote preflight, run remote training, run formal evaluation, accept H02 output, or produce paper-result material. The only allowed next action remains `record_protocol_lane_decision`.
