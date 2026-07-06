# Module2 Remote Packet Safety Audit

This file audits the remote formal execution packet. It does not execute any command.

- status: `remote_packet_safety_audit_failed`
- audit_issue_count: `9`
- packet_status: `ready_for_gpu3070ti_remote_training`
- remote_training_allowed_now: `True`
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

## Audit Issues

- `post_plan_handoff_sync_to_remote_allowed_mismatch`: Handoff remote step allowed_now must match the remote packet.
- `post_plan_handoff_sync_to_remote_blockers_mismatch`: Handoff remote step blocked_by must match the remote packet.
- `post_plan_handoff_run_remote_preflight_allowed_mismatch`: Handoff remote step allowed_now must match the remote packet.
- `post_plan_handoff_run_remote_preflight_blockers_mismatch`: Handoff remote step blocked_by must match the remote packet.
- `post_plan_handoff_run_remote_training_allowed_mismatch`: Handoff remote step allowed_now must match the remote packet.
- `post_plan_handoff_run_remote_training_blockers_mismatch`: Handoff remote step blocked_by must match the remote packet.
- `post_plan_handoff_run_remote_audit_blockers_mismatch`: Handoff remote step blocked_by must match the remote packet.
- `post_plan_execution_veto_remote_preflight_packet_mismatch`: Post-plan execution veto consensus must match the remote packet allowed_now state.
- `post_plan_execution_veto_remote_training_packet_mismatch`: Post-plan execution veto consensus must match the remote packet allowed_now state.

## Claim Boundaries

- This audit validates the remote execution packet; it does not execute sync, preflight, training, audit, or pullback commands.
- A passing audit is not permission to train while F02.6 remains pending.
- A passing audit is not a paper result or formal performance claim.
- Remote training must remain gpu3070ti-relay-only and must still be followed by audit, pullback, H01/H02 regeneration, and claim gates.
