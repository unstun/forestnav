# Module2 Mainline Formal Gate State Audit

This file checks that the long-term Module2 mainline task book mirrors the current formal-gate state. It is not a training run, remote preflight, formal evaluation, or paper result.

- status: `mainline_formal_gate_state_audit_failed`
- audit_issue_count: `23`
- expected_next_action_id: `record_protocol_lane_decision`
- expected_next_action_mentioned: `True`
- total_missing_deliverables: `1`
- mainline_missing_deliverable_mention_count: `0`
- f02_6_decision_evidence_matrix_summary: `{'present': True, 'matrix_id': 'module2_f02_6_decision_evidence_matrix', 'status': 'ready_for_dr_sun_decision_not_authorization', 'route_count': 2, 'route_decisions': ['approve_obstacle_summary_warm_start', 'reject_obstacle_summary_warm_start'], 'required_evidence_count': 7, 'satisfied_required_evidence_count': 7, 'missing_required_evidence_count': 0, 'missing_required_evidence_ids': [], 'source_issue_count': 0, 'global_invalid_substitute_count': 4, 'authorization_flags': {'current_authorization_allowed_now': False, 'remote_preflight_allowed_now': False, 'remote_training_allowed_now': False, 'local_training_allowed_now': False, 'formal_claim_allowed_now': False, 'paper_result_material_allowed_now': False}, 'evidence_counts_by_route': {'approve_obstacle_summary_warm_start': 4, 'reject_obstacle_summary_warm_start': 3}, 'invalid_substitute_counts_by_route': {'approve_obstacle_summary_warm_start': 4, 'reject_obstacle_summary_warm_start': 4}}`
- f02_6_decision_evidence_matrix_mentioned: `True`
- f02_6_decision_evidence_matrix_status_mentioned: `True`
- protocol_lane_status_summary: `{'present': True, 'status': 'protocol_lane_status_ready_for_contract_draft', 'audit_issue_count': 0, 'next_blocked_lane': 'new_or_revised_contract', 'decision_packet_status': 'formal_gate_protocol_lane_decision_packet_ready_for_dr_sun', 'decision_record_status': 'protocol_lane_decision_recorded', 'decision_gate_status': 'protocol_lane_decision_gate_recorded_clean', 'contract_authoring_gate_status': 'contract_authoring_gate_ready_for_contract_draft', 'lane_matrix_status': 'formal_gate_protocol_lane_matrix_ready', 'lane_count': 4, 'next_round_requirements_status': 'formal_gate_next_round_requirements_ready', 'selected_lane_id': 'stronger_obstacle_summary_warm_start', 'contract_action': 'draft_new_contract', 'allowed_next_action_ids': ['draft_new_or_revised_contract_after_lane_decision'], 'blocked_action_ids': ['local_training', 'remote_success_training', 'remote_preflight_for_new_success_attempt', 'formal_claim', 'paper_result_material'], 'post_decision_contract_plan_summary_present': True, 'post_decision_contract_plan_status': 'post_decision_contract_plan_ready_for_contract_draft', 'post_decision_contract_plan_audit_issue_count': 0, 'post_decision_contract_plan_required_section_count': 8, 'post_decision_contract_plan_shared_artifact_count': 10, 'post_decision_contract_plan_shared_artifact_category_counts': {'contract': 1, 'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 1}, 'post_decision_contract_plan_old_failed_run_artifacts_invalid_for_next_success_attempt': True, 'post_decision_contract_plan_lane_count': 4, 'post_decision_contract_plan_selected_lane_id': 'stronger_obstacle_summary_warm_start', 'post_decision_contract_plan_writes_contract': False, 'post_decision_contract_plan_approves_contract': False, 'post_decision_contract_plan_runs_training': False, 'post_decision_contract_plan_runs_remote_preflight': False, 'post_decision_contract_plan_remote_training_allowed_now': False, 'post_decision_contract_plan_formal_claim_allowed': False, 'post_decision_contract_plan_paper_result_material_allowed': False, 'post_decision_contract_plan_gate_contract_drafting_allowed_now': True, 'next_success_attempt_artifact_status': 'blocked_until_protocol_lane_decision_and_contract', 'next_success_attempt_artifact_count': 10, 'next_success_attempt_artifact_category_counts': {'contract': 1, 'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 1}, 'next_success_attempt_artifact_ids_by_category': {'contract': ['new_or_revised_research_contract'], 'training': ['train_final_model_zip', 'train_summary_json', 'train_training_manifest_json'], 'evaluation': ['eval_gate3_eval_episodes_csv', 'eval_gate3_summary_json'], 'acceptance': ['gate3_trial_manifest_json', 'gate3_formal_audit_json', 'pulled_back_checkpoint_hash_record'], 'formal_acceptance': ['h02_formal_output_acceptance']}, 'old_failed_run_artifacts_invalid_for_next_success_attempt': True, 'contract_drafting_allowed_now': True, 'contract_approval_allowed_now': False, 'draft_contract_allows_training': False, 'local_training_allowed_now': False, 'remote_training_allowed_now': False, 'formal_claim_allowed_now': False, 'paper_result_material_allowed_now': False, 'new_success_training_allowed_now': False}`
- protocol_lane_status_mentioned: `False`
- protocol_lane_next_blocked_mentioned: `False`
- protocol_lane_next_action_mentioned: `True`
- protocol_lane_readiness_summary: `{'present': True, 'artifact_name': 'module2_formal_gate_protocol_lane_readiness', 'status': 'protocol_lane_readiness_ready_for_dr_sun_decision', 'audit_issue_count': 0, 'lane_count': 4, 'shared_next_success_attempt_artifact_count': 10, 'not_paper_result_material': True, 'executes_commands': False, 'runs_training': False, 'runs_remote_preflight': False, 'remote_training_allowed_now': False, 'formal_claim_allowed': False, 'paper_result_material_allowed': False, 'gate_next_blocked_lane': 'protocol_lane_decision', 'gate_selected_lane_id': None, 'gate_decision_owner_required': 'Dr Sun', 'gate_remote_training_allowed_now': False, 'gate_formal_claim_allowed_now': False, 'gate_paper_result_material_allowed_now': False}`
- protocol_lane_readiness_artifact_mentioned: `True`
- protocol_lane_readiness_status_mentioned: `True`
- post_decision_contract_plan_summary: `{'present': True, 'artifact_name': 'module2_formal_gate_post_decision_contract_plan', 'status': 'post_decision_contract_plan_ready_for_contract_draft', 'audit_issue_count': 0, 'required_contract_section_count': 8, 'shared_next_success_attempt_artifact_count': 10, 'shared_next_success_attempt_artifact_category_counts': {'contract': 1, 'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 1}, 'old_failed_run_artifacts_invalid_for_next_success_attempt': True, 'lane_count': 4, 'not_paper_result_material': True, 'executes_commands': False, 'writes_contract': False, 'approves_contract': False, 'runs_training': False, 'runs_remote_preflight': False, 'remote_training_allowed_now': False, 'formal_claim_allowed': False, 'paper_result_material_allowed': False, 'gate_next_blocked_lane': 'new_or_revised_contract', 'gate_selected_lane_id': 'stronger_obstacle_summary_warm_start', 'gate_contract_drafting_allowed_now': True, 'gate_remote_training_allowed_now': False, 'gate_formal_claim_allowed_now': False}`
- post_decision_contract_plan_artifact_mentioned: `True`
- post_decision_contract_plan_status_mentioned: `False`
- proof_summary_chain_status: `formal_gate_proof_summary_chain_consistent_blocked`
- proof_summary_handoff_single_next_action_consistency: `{'row_count': 3, 'consistent_row_count': 3}`
- executes_commands: `False`
- runs_training: `False`
- runs_remote_preflight: `False`
- formal_claim_allowed: `False`

## Audit Issues

- `mainline_current_section_missing_protocol_lane_status`: Current formal-gate section must mention the protocol-lane status report state.
- `mainline_current_section_missing_protocol_lane_next_blocked`: Current formal-gate section must mention protocol_lane_decision as the current blocked lane.
- `mainline_current_section_missing_protocol_lane_decision_record_status`: Current formal-gate section must mention the pending protocol-lane decision record.
- `mainline_current_section_missing_protocol_status_post_plan_section_count`: Current formal-gate section must mention the protocol status report's inherited post-plan count.
- `mainline_current_section_missing_protocol_status_post_plan_artifact_count`: Current formal-gate section must mention the protocol status report's inherited post-plan count.
- `mainline_current_section_missing_protocol_status_post_plan_lane_count`: Current formal-gate section must mention the protocol status report's inherited post-plan count.
- `mainline_current_section_missing_post_decision_contract_plan_status`: Current formal-gate section must mention the post-decision contract plan status.
- `mainline_current_section_missing_post_decision_contract_section_count`: Current formal-gate section must mention this post-decision contract plan count.
- `mainline_current_section_missing_post_decision_contract_shared_artifact_count`: Current formal-gate section must mention this post-decision contract plan count.
- `mainline_current_section_missing_post_decision_contract_lane_count`: Current formal-gate section must mention this post-decision contract plan count.
- `status_report_next_action_guard_invalid_after_f02_6`: After F02.6 closes, next-action guard should be not-applicable or passed.
- `protocol_lane_status_drift`: Protocol-lane status must remain blocked pending Dr Sun's lane decision.
- `protocol_lane_status_next_blocked_lane_drift`: Current blocked lane must remain protocol_lane_decision.
- `protocol_lane_status_decision_record_not_pending`: Mainline audit currently mirrors the pending protocol-lane decision state.
- `protocol_lane_status_selected_lane_present`: Pending protocol-lane state must not already have a selected lane.
- `protocol_lane_status_allowed_actions_drift`: Pending protocol-lane state may only allow record_protocol_lane_decision.
- `protocol_lane_status_authorization_leak`: Protocol-lane status must not authorize contract approval, training, preflight, claims, or paper-result material.
- `protocol_lane_status_post_plan_status_drift`: Protocol-lane status report must mirror the pending post-decision contract plan status.
- `protocol_lane_status_post_plan_authorization_leak`: Protocol-lane status report's inherited post-plan summary must not authorize contract drafting, training, preflight, claims, or paper-result material while pending.
- `protocol_lane_status_post_plan_selected_lane_present`: Protocol-lane status report must not expose a selected post-plan lane while the decision is pending.
- `post_decision_contract_plan_status_drift`: Post-decision contract plan must remain blocked pending protocol-lane decision.
- `post_decision_contract_plan_authorization_leak`: Post-decision contract plan must not authorize contract writing, training, or claims.
- `post_decision_contract_plan_selected_lane_present`: Post-decision plan mirrored by mainline must not select a lane while protocol decision is pending.

## Missing Formal Deliverables

- `formal_acceptance:h02_formal_output_acceptance`: artifact_id=`h02_formal_output_acceptance`, mentioned=`True`, mentioned_in_current_section=`True`

## F02.6 Decision Evidence Matrix

- matrix_id: `module2_f02_6_decision_evidence_matrix`
- status: `ready_for_dr_sun_decision_not_authorization`
- route_count: `2`
- required_evidence_count: `7`
- missing_required_evidence_count: `0`
- authorization_flags: `{'current_authorization_allowed_now': False, 'remote_preflight_allowed_now': False, 'remote_training_allowed_now': False, 'local_training_allowed_now': False, 'formal_claim_allowed_now': False, 'paper_result_material_allowed_now': False}`

## Protocol Lane Status

- status: `protocol_lane_status_ready_for_contract_draft`
- next_blocked_lane: `new_or_revised_contract`
- decision_record_status: `protocol_lane_decision_recorded`
- selected_lane_id: `stronger_obstacle_summary_warm_start`
- lane_count: `4`
- allowed_next_action_ids: `['draft_new_or_revised_contract_after_lane_decision']`
- blocked_action_ids: `['local_training', 'remote_success_training', 'remote_preflight_for_new_success_attempt', 'formal_claim', 'paper_result_material']`
- lane `stronger_obstacle_summary_warm_start`: mentioned=`True`
- lane `full_patch_cnn_policy`: mentioned=`True`
- lane `hybrid_ppo_analytic_fallback`: mentioned=`True`
- lane `stop_or_reframe_module2_claim`: mentioned=`True`
- blocked action `local_training`: mentioned=`True`
- blocked action `remote_success_training`: mentioned=`True`
- blocked action `remote_preflight_for_new_success_attempt`: mentioned=`True`
- blocked action `formal_claim`: mentioned=`True`
- blocked action `paper_result_material`: mentioned=`True`

## Protocol Lane Readiness

- artifact_name: `module2_formal_gate_protocol_lane_readiness`
- status: `protocol_lane_readiness_ready_for_dr_sun_decision`
- audit_issue_count: `0`
- lane_count: `4`
- shared_next_success_attempt_artifact_count: `10`
- gate_next_blocked_lane: `protocol_lane_decision`
- gate_selected_lane_id: `None`
- gate_remote_training_allowed_now: `False`

## Post-Decision Contract Plan

- artifact_name: `module2_formal_gate_post_decision_contract_plan`
- status: `post_decision_contract_plan_ready_for_contract_draft`
- audit_issue_count: `0`
- required_contract_section_count: `8`
- shared_next_success_attempt_artifact_count: `10`
- lane_count: `4`
- gate_selected_lane_id: `stronger_obstacle_summary_warm_start`
- gate_contract_drafting_allowed_now: `True`
- gate_remote_training_allowed_now: `False`

## Current Boundary Tokens

- `local training`: mentioned=`True`
- `remote preflight`: mentioned=`True`
- `remote training`: mentioned=`True`
- `formal claim`: mentioned=`True`
- `paper-result material`: mentioned=`True`
- `gpu3070ti-relay`: mentioned=`True`

## Claim Boundaries

- This audit only checks that the long-term mainline task book mirrors the current formal-gate state.
- It does not execute commands, run local training, run remote preflight, run remote PPO training, evaluate PPO, pull back artifacts, or write paper results.
- A consistent blocked audit does not prove PPO has replaced RS in formal evaluation.
- Formal PPO-vs-RS performance claims still require the missing training, evaluation, acceptance, and H01/H02 artifacts to be produced and audited.
- Protocol-lane status must remain blocked on record_protocol_lane_decision before any new or revised contract can authorize future remote success attempts.
