# Module2 Formal Gate Proof Summary Chain Audit

This file checks that formal-gate proof-deliverables summaries remain consistent across downstream gate artifacts. It is not a training run, evaluation, remote preflight, paper table, or paper result.

- status: `formal_gate_proof_summary_chain_audit_failed`
- audit_issue_count: `12`
- proof_open: `True`
- row_count: `14`
- consistent_row_count: `2`
- missing_row_count: `0`
- mismatch_row_count: `12`
- next_action_guard_row_count: `3`
- next_action_guard_consistent_row_count: `3`
- next_required_deliverables_row_count: `3`
- next_required_deliverables_consistent_row_count: `3`
- handoff_single_next_action_row_count: `3`
- handoff_single_next_action_consistent_row_count: `3`
- executes_commands: `False`
- runs_training: `False`
- runs_remote_preflight: `False`
- formal_claim_allowed: `False`

## Baseline Summary

- missing_counts_by_formal_category: `{'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 2}`
- next_blocked_lane: `decision`
- h01_status: `blocked_pending_decisions`
- h02_status: `blocked_formal_output_acceptance`
- h02_formal_output_accepted: `False`
- h02_paper_result_input_allowed: `False`

## Audit Issues

- `formal_gate_status_report_proof_summary_summary_mismatch`: Downstream proof-deliverables summary does not match the remaining-deliverables baseline.
- `status_report_remote_safety_proof_summary_summary_mismatch`: Downstream proof-deliverables summary does not match the remaining-deliverables baseline.
- `status_report_remote_safety_status_report_proof_summary_summary_mismatch`: Downstream proof-deliverables summary does not match the remaining-deliverables baseline.
- `post_plan_status_report_proof_summary_summary_mismatch`: Downstream proof-deliverables summary does not match the remaining-deliverables baseline.
- `remote_safety_post_plan_proof_summary_summary_mismatch`: Downstream proof-deliverables summary does not match the remaining-deliverables baseline.
- `remote_safety_post_plan_status_report_proof_summary_summary_mismatch`: Downstream proof-deliverables summary does not match the remaining-deliverables baseline.
- `gap_audit_remote_safety_proof_summary_summary_mismatch`: Downstream proof-deliverables summary does not match the remaining-deliverables baseline.
- `gap_audit_remote_safety_status_report_proof_summary_summary_mismatch`: Downstream proof-deliverables summary does not match the remaining-deliverables baseline.
- `claim_safety_remote_safety_proof_summary_summary_mismatch`: Downstream proof-deliverables summary does not match the remaining-deliverables baseline.
- `claim_safety_remote_safety_status_report_proof_summary_summary_mismatch`: Downstream proof-deliverables summary does not match the remaining-deliverables baseline.
- `paper_readiness_remote_safety_proof_summary_summary_mismatch`: Downstream proof-deliverables summary does not match the remaining-deliverables baseline.
- `paper_readiness_remote_safety_status_report_proof_summary_summary_mismatch`: Downstream proof-deliverables summary does not match the remaining-deliverables baseline.

## Chain Rows

- `remaining_deliverables_top_level`: present=`True`, matches=`True`, h02_paper_result_input_allowed=`False`, path=`0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json`, key=`top_level`
- `formal_gate_proof_audit_remaining_summary`: present=`True`, matches=`True`, h02_paper_result_input_allowed=`False`, path=`0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json`, key=`remaining_deliverables_top_level_summary`
- `formal_gate_status_report_proof_summary`: present=`True`, matches=`False`, h02_paper_result_input_allowed=`False`, path=`0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`, key=`formal_gate_proof_audit_remaining_deliverables_top_level_summary`
- `status_report_remote_safety_proof_summary`: present=`True`, matches=`False`, h02_paper_result_input_allowed=`False`, path=`0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`, key=`remote_packet_safety_proof_deliverables_summary`
- `status_report_remote_safety_status_report_proof_summary`: present=`True`, matches=`False`, h02_paper_result_input_allowed=`False`, path=`0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`, key=`remote_packet_safety_status_report_proof_deliverables_summary`
- `post_plan_status_report_proof_summary`: present=`True`, matches=`False`, h02_paper_result_input_allowed=`False`, path=`0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`, key=`status_report_proof_audit_deliverables_summary`
- `remote_safety_post_plan_proof_summary`: present=`True`, matches=`False`, h02_paper_result_input_allowed=`False`, path=`0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`, key=`cross_gate_summary.post_plan_proof_audit_deliverables_summary`
- `remote_safety_post_plan_status_report_proof_summary`: present=`True`, matches=`False`, h02_paper_result_input_allowed=`False`, path=`0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`, key=`cross_gate_summary.post_plan_status_report_proof_audit_deliverables_summary`
- `gap_audit_remote_safety_proof_summary`: present=`True`, matches=`False`, h02_paper_result_input_allowed=`False`, path=`0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json`, key=`remote_packet_safety.proof_deliverables_summary`
- `gap_audit_remote_safety_status_report_proof_summary`: present=`True`, matches=`False`, h02_paper_result_input_allowed=`False`, path=`0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json`, key=`remote_packet_safety.status_report_proof_deliverables_summary`
- `claim_safety_remote_safety_proof_summary`: present=`True`, matches=`False`, h02_paper_result_input_allowed=`False`, path=`0_trials/module2_claim_safety/module2_claim_safety.json`, key=`status_report_remote_packet_safety_proof_deliverables_summary`
- `claim_safety_remote_safety_status_report_proof_summary`: present=`True`, matches=`False`, h02_paper_result_input_allowed=`False`, path=`0_trials/module2_claim_safety/module2_claim_safety.json`, key=`status_report_remote_packet_safety_status_report_proof_deliverables_summary`
- `paper_readiness_remote_safety_proof_summary`: present=`True`, matches=`False`, h02_paper_result_input_allowed=`False`, path=`0_trials/module2_paper_readiness/module2_paper_readiness.json`, key=`claim_safety_remote_packet_safety_proof_deliverables_summary`
- `paper_readiness_remote_safety_status_report_proof_summary`: present=`True`, matches=`False`, h02_paper_result_input_allowed=`False`, path=`0_trials/module2_paper_readiness/module2_paper_readiness.json`, key=`claim_safety_remote_packet_safety_status_report_proof_deliverables_summary`

## Next-Action Guard Chain Rows

- `status_report_next_action_guard`: present=`True`, matches=`True`, expected_next_action_id=`None`, execution_leak_count=`2`, path=`0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`, key=`next_action_guard_summary`
- `claim_safety_status_report_next_action_guard`: present=`True`, matches=`True`, expected_next_action_id=`None`, execution_leak_count=`2`, path=`0_trials/module2_claim_safety/module2_claim_safety.json`, key=`status_report_next_action_guard_summary`
- `paper_readiness_claim_safety_next_action_guard`: present=`True`, matches=`True`, expected_next_action_id=`None`, execution_leak_count=`2`, path=`0_trials/module2_paper_readiness/module2_paper_readiness.json`, key=`claim_safety_next_action_guard_summary`

## Next Required Formal Deliverables Chain Rows

- `status_report_next_required_formal_deliverables`: present=`True`, matches=`True`, total_missing_deliverables=`10`, row_count=`10`, runs_training=`False`, path=`0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`, key=`next_required_formal_deliverables`
- `claim_safety_status_report_next_required_formal_deliverables`: present=`True`, matches=`True`, total_missing_deliverables=`10`, row_count=`10`, runs_training=`False`, path=`0_trials/module2_claim_safety/module2_claim_safety.json`, key=`status_report_next_required_formal_deliverables`
- `paper_readiness_claim_safety_next_required_formal_deliverables`: present=`True`, matches=`True`, total_missing_deliverables=`10`, row_count=`10`, runs_training=`False`, path=`0_trials/module2_paper_readiness/module2_paper_readiness.json`, key=`claim_safety_next_required_formal_deliverables`

## Handoff Single Next-Action Chain Rows

- `handoff_bundle_single_next_action_index`: present=`True`, matches=`True`, next_action_id=`manual_handoff_stage_review`, decision_owner_required=`Dr Sun`, all_execution_disabled_now=`False`, remote_training_allowed_now=`False`, path=`0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json`, key=`single_next_action_index`
- `claim_safety_handoff_single_next_action_index`: present=`True`, matches=`True`, next_action_id=`manual_handoff_stage_review`, decision_owner_required=`Dr Sun`, all_execution_disabled_now=`False`, remote_training_allowed_now=`False`, path=`0_trials/module2_claim_safety/module2_claim_safety.json`, key=`handoff_single_next_action_index_summary`
- `paper_readiness_claim_safety_handoff_single_next_action_index`: present=`True`, matches=`True`, next_action_id=`manual_handoff_stage_review`, decision_owner_required=`Dr Sun`, all_execution_disabled_now=`False`, remote_training_allowed_now=`False`, path=`0_trials/module2_paper_readiness/module2_paper_readiness.json`, key=`claim_safety_handoff_single_next_action_index_summary`

## Claim Boundaries

- This audit is a local read-only consistency check over existing formal-gate summary fields.
- It does not execute proof commands, run training, run remote preflight, evaluate PPO, pull back artifacts, or write paper results.
- A consistent blocked chain only proves the downstream artifacts agree that the formal gate is still blocked.
- Next-action and next-required-deliverable consistency does not authorize the next action; it only checks that the artifacts agree on the current blocked lane.
- Single-next-action consistency only proves the handoff pointer is mirrored; it is still not Dr Sun's F02.6 decision record.
- Formal PPO-vs-RS performance claims still require the missing training, evaluation, acceptance, and H01/H02 artifacts to be produced and audited.
