---
origin: ai+local
reviewed: false
created_at: 2026-07-05
topic: module2_protocol_status_consumes_contract_post_plan
trust_level: audit_record
parent: .pipeline/mainline_module2_rl_rs_replacement.md
---

# Module2 Protocol Status Consumes Contract Post-Plan

## Scope

This record covers a formal-gate status update. It makes the top-level protocol-lane status report consume the contract-authoring gate's post-decision contract plan summary and expose the missing next-attempt artifact list.

It does not select a protocol lane, write or approve a contract, run local training, run remote preflight, run remote training, run H01/H02 formal evaluation, or write paper-result material.

## Change

- `protocol_lane_status_report.current_status` now exposes the consumed post-decision contract plan status, audit count, required contract section count, shared next-attempt artifact count, lane count, selected-lane state, and no-authorization flags.
- `protocol_lane_status_report.current_status` now exposes the next-attempt artifact index by category:
  - contract: `new_or_revised_research_contract`
  - training: `train_final_model_zip`, `train_summary_json`, `train_training_manifest_json`
  - evaluation: `eval_gate3_eval_episodes_csv`, `eval_gate3_summary_json`
  - acceptance: `gate3_trial_manifest_json`, `gate3_formal_audit_json`, `pulled_back_checkpoint_hash_record`
  - formal_acceptance: `h02_formal_output_acceptance`
- The status-report audit now fails if the post-plan summary is missing, has the wrong status/counts, leaks contract writing/approval, training, remote preflight, formal claim, paper-result authorization, or exposes a selected lane while the protocol-lane decision is pending.
- The status-report audit now fails if the next-attempt artifact index drifts away from the 10 expected formal-gate artifacts or from category counts `1/3/2/3/1`.

## Current State

- `protocol_lane_status_report.status`: `protocol_lane_status_blocked_pending_lane_decision`
- `protocol_lane_status_report.audit_issue_count`: `0`
- `post_decision_contract_plan.status`: `post_decision_contract_plan_ready_blocked_pending_lane_decision`
- `post_decision_contract_plan.required_contract_section_count`: `8`
- `post_decision_contract_plan.shared_next_success_attempt_artifact_count`: `10`
- `post_decision_contract_plan.lane_count`: `4`
- `selected_lane_id`: `None`
- `allowed_next_action_ids`: `record_protocol_lane_decision`
- blocked actions remain `local_training`, `remote_success_training`, `remote_preflight_for_new_success_attempt`, `formal_claim`, `paper_result_material`.

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_protocol_lane_status_report.py` -> `6 passed`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_protocol_lane_status_report` -> `protocol_lane_status_blocked_pending_lane_decision`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit` -> `mainline_formal_gate_state_consistent_blocked`

## Boundary

The next formal-gate action remains `record_protocol_lane_decision`, owned by Dr Sun. A recorded lane can only open contract drafting. It still cannot approve a contract, start local or remote training, run a new remote preflight, unlock formal claims, or unlock paper-result material.
