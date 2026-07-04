---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
scope: formal_gate
not_paper_result_material: true
---

# Module2 post-F02.6 regeneration command index

## Summary

`module2_post_f02_6_regeneration_plan` now carries a machine-readable `source_regeneration_command_index`.

The goal is to make the source-fresh / clean-head regeneration gate auditable before any approved remote preflight or formal PPO training can happen. Each source-freshness target now maps to:

- `artifact_id`
- `required_before`
- `freshness_state`
- expected artifact `path`
- regeneration `stage_id`
- `command_kind`
- `command_template`

## Current Coverage

Current refreshed plan:

- `status`: `blocked_until_f02_6_decision`
- command index rows: `17`
- unknown/manual fallback rows: `0`
- `regenerate_preflight_gate_artifacts`: `11` rows
- `regenerate_h01_h02_formal_artifacts`: `2` rows
- `regenerate_claim_gate_artifacts`: `4` rows

Key targets now have explicit commands:

- `f02_6_decision_intake` -> `build_module2_f02_6_decision_intake`
- `f02_6_decision_gate_audit` -> `build_module2_f02_6_decision_gate_audit`
- `f02_6_transition_gate_audit` -> `build_module2_f02_6_transition_gate_audit`
- `formal_gate_status_report` -> `build_module2_formal_gate_status_report`
- `formal_gate_remaining_deliverables` -> `build_module2_formal_gate_remaining_deliverables`
- `h01_evaluation_manifest` -> `build_module2_evaluation_manifest --module2-rl-rs-checkpoint <pulled-back-final_model.zip>`
- `h02_formal_acceptance` -> `build_module2_h02_formal_acceptance`
- `claim_safety` -> `build_module2_claim_safety`
- `paper_readiness` -> `build_module2_paper_readiness`

## Current Gate State

- `training_allowed_now`: `false`
- `remote_preflight_allowed_now`: `false`
- `gate3_remote_training.allowed_now`: `false`
- `gate3_remote_training.blocked_by`: `f02_6_decision_not_approved`, `source_fresh_preflight_targets_open`, `remote_packet_not_ready`
- `approved_remote_preflight.allowed_now`: `false`
- `approved_remote_preflight.blocked_by`: `f02_6_decision_not_approved`, `source_fresh_preflight_targets_open`

## Verification

- `PYTHONPATH=2_experiment python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_post_f02_6_regeneration_plan.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py`
  - Result: passed
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py`
  - Result: `4 passed`
- Artifact refresh:
  - `post_f02_6_regeneration_plan`: `blocked_until_f02_6_decision`
  - `post_f02_6_plan_audit`: `post_f02_6_plan_audit_passed`
  - `remote_packet_safety_audit`: `remote_packet_safety_audit_passed`
  - `formal_gate_status_report`: `formal_gate_status_blocked`
  - `claim_safety`: `blocked_formal_performance_claims`
  - `paper_readiness`: `partial_methods_ready_results_blocked`
  - `source_freshness_audit`: `source_freshness_risks_recorded_gate_still_blocked`

## Boundary

This is a plan and audit artifact. It does not execute any command, approve F02.6, run remote preflight, run remote training, run remote audit, pull back artifacts, regenerate H01/H02 as accepted, or authorize formal paper results.
