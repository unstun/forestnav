# Module2 Remote Packet Safety Audit

This file audits the remote formal execution packet. It does not execute any command.

- status: `remote_packet_safety_audit_failed`
- audit_issue_count: `3`
- packet_status: `blocked_until_protocol_lane_decision`
- remote_training_allowed_now: `False`
- pullback_artifact_count: `7`
- post_plan_status_report_status: `formal_gate_status_blocked`
- post_plan_status_report_next_blocked_lane_id: `source_fresh_preflight`
- post_plan_handoff_status: `blocked_until_protocol_lane_decision`
- post_plan_handoff_remote_training_allowed_now: `False`
- post_plan_execution_veto_present: `True`
- post_plan_execution_veto_all_rows_consistent: `True`
- post_plan_execution_veto_remote_training_allowed_now: `False`
- post_plan_command_index_present: `True`
- post_plan_command_index_row_count: `23`
- post_plan_command_index_source_target_count: `23`
- post_plan_command_index_missing_target_ids: `[]`
- post_plan_command_index_unknown_manual_count: `0`
- post_plan_command_index_forbidden_command_count: `0`
- post_plan_remaining_deliverables_gap_total_missing: `1`
- post_plan_status_report_gap_total_missing: `1`
- post_plan_proof_deliverables_present: `True`
- post_plan_proof_deliverables_missing_counts: `{'training': 0, 'evaluation': 0, 'acceptance': 0, 'formal_acceptance': 1}`
- post_plan_proof_deliverables_h02_paper_result_input_allowed: `False`
- post_plan_protocol_lane_status_present: `True`
- post_plan_protocol_lane_status: `protocol_lane_status_blocked_pending_lane_decision`
- post_plan_protocol_lane_next_blocked: `protocol_lane_decision`
- post_plan_protocol_lane_allowed_next_actions: `['record_protocol_lane_decision']`
- post_plan_protocol_lane_new_success_training_allowed_now: `False`
- post_plan_protocol_lane_next_attempt_artifact_counts: `{'contract': 1, 'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 1}`
- post_plan_protocol_lane_old_failed_run_artifacts_invalid: `None`

## Audit Issues

- `protocol_lane_shared_artifact_category_counts_drift`: Protocol contract plan must keep the contract/training/evaluation/acceptance/formal_acceptance split.
- `protocol_lane_post_plan_old_failed_invalid_flag_drift`: Protocol contract plan must preserve that old failed-run artifacts are invalid substitutes.
- `protocol_lane_old_failed_invalid_flag_drift`: Protocol lane status must preserve that old failed-run artifacts are invalid substitutes.

## Claim Boundaries

- This audit validates the remote execution packet; it does not execute sync, preflight, training, audit, or pullback commands.
- A passing audit is not permission to train while protocol_lane_decision remains pending.
- A passing audit is not a paper result or formal performance claim.
- Remote training must remain gpu3070ti-relay-only and must still be preceded by protocol-lane decision, approved/frozen contract, audit, pullback, H01/H02 regeneration, and claim gates.
