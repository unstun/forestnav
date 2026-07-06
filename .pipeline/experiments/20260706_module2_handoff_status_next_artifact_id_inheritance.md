---
origin: ai+local-source
reviewed: false
date: 2026-07-06
status: recorded
scope: module2 formal gate handoff and status-report propagation of next success-attempt artifact ids
---

# Module2 Handoff / Status Next Artifact ID Inheritance

## Purpose

The previous gate pass made handoff and status-report layers preserve the next success-attempt artifact category counts and the old failed-run invalid-substitute boundary. This record hardens the same path one level deeper: downstream readers must see the concrete artifact IDs, not only the category totals.

## Change

- `formal_gate_handoff_bundle.protocol_lane_status_summary` now carries `next_success_attempt_artifact_ids_by_category`.
- `formal_gate_status_report.formal_gate_handoff_summary` now consumes the same artifact-ID map from the handoff bundle.
- Both layers now reject drift in the expected next success-attempt artifact IDs:
  - `contract:new_or_revised_research_contract`
  - `training:train_final_model_zip`
  - `training:train_summary_json`
  - `training:train_training_manifest_json`
  - `evaluation:eval_gate3_eval_episodes_csv`
  - `evaluation:eval_gate3_summary_json`
  - `acceptance:gate3_trial_manifest_json`
  - `acceptance:gate3_formal_audit_json`
  - `acceptance:pulled_back_checkpoint_hash_record`
  - `formal_acceptance:h02_formal_output_acceptance`

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_handoff_bundle.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py` -> `53 passed`
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_mainline_formal_gate_state_audit.py` -> `18 passed`
- Regenerated:
  - `0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json`
  - `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
  - `0_trials/module2_mainline_formal_gate_state_audit/mainline_formal_gate_state_audit.json`

## Boundary

This is a read-only formal-gate inheritance change. It does not select a protocol lane, approve or draft a contract, run local training, run remote preflight, run remote training, perform formal evaluation, accept H02 output, or produce paper-result material. The top gate remains `protocol_lane_decision`.
