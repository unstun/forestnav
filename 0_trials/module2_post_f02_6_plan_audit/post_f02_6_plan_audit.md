# Module2 Post-F02.6 Plan Audit

This file audits the ordered post-F02.6 plan. It does not execute the plan.

- status: `post_f02_6_plan_audit_passed`
- audit_issue_count: `0`
- executes_commands: `False`
- runs_training: `False`
- runs_remote_preflight: `False`

## Current Blocking Summary

- plan_status: `ready_to_execute_post_f02_6_regeneration_plan`
- training_allowed_now: `False`
- remote_preflight_allowed_now: `False`
- ready_stage_ids: `['regenerate_preflight_gate_artifacts']`
- blocked_stage_ids: `['f02_6_decision_record', 'approved_remote_preflight', 'regenerate_remote_execution_packet', 'gate3_remote_training', 'gate3_remote_audit_pullback', 'regenerate_h01_h02_formal_artifacts', 'regenerate_claim_gate_artifacts']`

## F02.6 Human Decision Request

- present: `True`
- status: `decision_recorded`
- decision_owner_required: `Dr Sun`
- current_allowed_action_ids: `['record_f02_6_decision']`
- current_blocked_action_ids: `['remote_preflight', 'remote_training', 'local_training', 'formal_claim', 'paper_result_material']`
- post_decision_routes_are_current_authorization: `False`
- all_execution_disabled_now: `False`
- remote_preflight_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`
- local_training_allowed_now: `False`

## Source Regeneration Command Index

- present: `True`
- index_row_count: `23`
- source_target_count: `23`
- unknown_manual_count: `0`
- stage_mismatch_count: `0`
- command_not_in_stage_count: `0`
- forbidden_command_count: `0`

## Missing Artifacts Inventory

- path: `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json`
- status: `formal_gate_missing_artifacts_open`
- runs_training: `False`
- runs_remote_preflight: `False`
- all_required_evidence_present: `False`
- audit_issue_count: `0`
- missing_counts_by_category: `{'decision': 0, 'decision_gate': 0, 'regeneration': 22, 'gate_sequence': 4, 'training': 0, 'evaluation': 0, 'acceptance': 0, 'evaluation_acceptance': 1, 'claim_gate': 8}`

## Closure Checklist

- path: `0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json`
- status: `formal_gate_closure_blocked`
- runs_training: `False`
- runs_remote_preflight: `False`
- open_item_count: `8`
- input_safety_issue_count: `0`

## Formal Gate Status Report

- path: `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
- status: `formal_gate_status_blocked`
- runs_training: `False`
- runs_remote_preflight: `False`
- formal_claim_allowed_now: `False`
- local_training_allowed_now: `False`
- input_safety_issue_count: `0`
- next_blocked_lane_id: `source_fresh_preflight`

## Protocol Lane Status Report

- path: `0_trials/module2_formal_gate_protocol_lane_status_report/protocol_lane_status_report.json`
- status: `protocol_lane_status_blocked_pending_lane_decision`
- audit_issue_count: `0`
- next_blocked_lane: `protocol_lane_decision`
- selected_lane_id: `None`
- allowed_next_action_ids: `['record_protocol_lane_decision']`
- blocked_action_ids: `['local_training', 'remote_success_training', 'remote_preflight_for_new_success_attempt', 'formal_claim', 'paper_result_material']`
- post_decision_contract_plan_status: `post_decision_contract_plan_ready_blocked_pending_lane_decision`
- post_decision_contract_plan_required_section_count: `8`
- post_decision_contract_plan_shared_artifact_count: `10`
- post_decision_contract_plan_lane_count: `4`
- next_success_attempt_artifact_count: `10`
- next_success_attempt_artifact_category_counts: `{'contract': 1, 'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 1}`
- next_success_attempt_artifact_ids_by_category: `{'contract': ['new_or_revised_research_contract'], 'training': ['train_final_model_zip', 'train_summary_json', 'train_training_manifest_json'], 'evaluation': ['eval_gate3_eval_episodes_csv', 'eval_gate3_summary_json'], 'acceptance': ['gate3_trial_manifest_json', 'gate3_formal_audit_json', 'pulled_back_checkpoint_hash_record'], 'formal_acceptance': ['h02_formal_output_acceptance']}`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`
- paper_result_material_allowed_now: `False`

### Remaining Deliverables Gap Summary

- ledger_path: `0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json`
- ledger_exists: `True`
- ledger_total_missing_deliverables: `1`
- ledger_open_category_count: `1`
- status_report_total_missing_deliverables: `1`
- status_report_open_category_count: `1`

### Remaining Deliverables Unlock Chain

- ledger_path: `0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json`
- ledger_exists: `True`
- status: `blocked_missing_formal_deliverables`
- row_count: `10`
- blocked_row_count: `1`
- rows_with_missing_required_blockers: `0`
- rows_allowed_while_missing: `0`

### Status Report Proof-Audit Deliverables Summary

- present: `True`
- missing_counts_by_formal_category: `{'training': 0, 'evaluation': 0, 'acceptance': 0, 'formal_acceptance': 1}`
- next_blocked_lane: `protocol_lane_decision`
- h01_status: `ready_for_formal_run`
- h02_status: `blocked_formal_output_acceptance`
- h02_paper_result_input_allowed: `False`

### Status Report Handoff Summary

- status: `blocked_until_protocol_lane_decision`
- remote_training_allowed_now: `False`
- safety_issue_count: `0`

### Status Report Execution Veto Matrix

- present: `True`
- all_rows_consistent: `True`
- mismatch_rows: `[]`

### Status Report Remote Execution Steps

- `local_training`: consensus_allowed_now=`False`
- `remote_preflight`: consensus_allowed_now=`False`
- `remote_training`: consensus_allowed_now=`False`
- `remote_audit`: consensus_allowed_now=`False`
- `formal_claim`: consensus_allowed_now=`False`

- `sync_to_remote`: allowed_now=`False`, runs_training=`False`, blocked_by=`protocol_lane_decision_pending`
- `run_remote_preflight`: allowed_now=`False`, runs_training=`False`, blocked_by=`protocol_lane_decision_pending`
- `run_remote_training`: allowed_now=`False`, runs_training=`True`, blocked_by=`protocol_lane_decision_pending, remote_formal_preflight_not_ready, warm_start_decision_pending, remote_packet_not_ready`
- `run_remote_audit`: allowed_now=`False`, runs_training=`False`, blocked_by=`protocol_lane_decision_pending, remote_formal_preflight_not_ready, warm_start_decision_pending, remote_packet_not_ready`

## Audit Issues

- none

## Claim Boundaries

- This audit validates a plan artifact; it does not execute the plan.
- A passing audit is not permission to train while F02.6 remains pending.
- A passing audit is not a paper result or formal performance claim.
- Training stages must remain remote-only on gpu3070ti-relay and blocked until upstream gates pass.
