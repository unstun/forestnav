# Module2 Formal Gate Protocol Lane Decision Record

This file records the lane-decision state; it is not paper result material.

## Decision State

- status: `pending_protocol_lane_decision`
- requested_selected_lane: `pending`
- selected_lane_id: `None`
- decider: `None`
- contract_action: `none`
- training_authorization: `not_authorized_by_this_decision_record`
- decision_record_is_not_training_authorization: `True`
- decision_record_is_not_paper_result_material: `True`

## Authorization

- remote_training_allowed_now: `False`
- local_training_allowed_now: `False`
- formal_claim_allowed_now: `False`
- paper_result_material_allowed_now: `False`

## Valid Lanes
- `stronger_obstacle_summary_warm_start`
- `full_patch_cnn_policy`
- `hybrid_ppo_analytic_fallback`
- `stop_or_reframe_module2_claim`

## Record Command Templates
- selected_lane: `stronger_obstacle_summary_warm_start`
  - allowed_for_agent_now: `False`
  - runs_training: `False`
  - runs_remote_preflight: `False`
  - template: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_record --selected-lane stronger_obstacle_summary_warm_start --decider 'Dr Sun' --contract-action <action> --decision-note 'Select stronger_obstacle_summary_warm_start because the failed Gate3 0.53125 result is below the 0.8 threshold; reject <all other lane ids with one rationale each>; use protocol_lane_matrix, gate3_formal_audit, formal_gate_next_round_requirements, and h02_formal_acceptance artifacts as the evidence basis; contract action is <draft_new_contract|draft_revised_contract|stop_success_attempts_and_record_negative_evidence>; this decision does not authorize local training, remote preflight, remote training, formal claim, or paper result material.'`
- selected_lane: `full_patch_cnn_policy`
  - allowed_for_agent_now: `False`
  - runs_training: `False`
  - runs_remote_preflight: `False`
  - template: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_record --selected-lane full_patch_cnn_policy --decider 'Dr Sun' --contract-action <action> --decision-note 'Select full_patch_cnn_policy because the failed Gate3 0.53125 result is below the 0.8 threshold; reject <all other lane ids with one rationale each>; use protocol_lane_matrix, gate3_formal_audit, formal_gate_next_round_requirements, and h02_formal_acceptance artifacts as the evidence basis; contract action is <draft_new_contract|draft_revised_contract|stop_success_attempts_and_record_negative_evidence>; this decision does not authorize local training, remote preflight, remote training, formal claim, or paper result material.'`
- selected_lane: `hybrid_ppo_analytic_fallback`
  - allowed_for_agent_now: `False`
  - runs_training: `False`
  - runs_remote_preflight: `False`
  - template: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_record --selected-lane hybrid_ppo_analytic_fallback --decider 'Dr Sun' --contract-action <action> --decision-note 'Select hybrid_ppo_analytic_fallback because the failed Gate3 0.53125 result is below the 0.8 threshold; reject <all other lane ids with one rationale each>; use protocol_lane_matrix, gate3_formal_audit, formal_gate_next_round_requirements, and h02_formal_acceptance artifacts as the evidence basis; contract action is <draft_new_contract|draft_revised_contract|stop_success_attempts_and_record_negative_evidence>; this decision does not authorize local training, remote preflight, remote training, formal claim, or paper result material.'`
- selected_lane: `stop_or_reframe_module2_claim`
  - allowed_for_agent_now: `False`
  - runs_training: `False`
  - runs_remote_preflight: `False`
  - template: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_record --selected-lane stop_or_reframe_module2_claim --decider 'Dr Sun' --contract-action <action> --decision-note 'Select stop_or_reframe_module2_claim because the failed Gate3 0.53125 result is below the 0.8 threshold; reject <all other lane ids with one rationale each>; use protocol_lane_matrix, gate3_formal_audit, formal_gate_next_round_requirements, and h02_formal_acceptance artifacts as the evidence basis; contract action is <draft_new_contract|draft_revised_contract|stop_success_attempts_and_record_negative_evidence>; this decision does not authorize local training, remote preflight, remote training, formal claim, or paper result material.'`

## Next Success Attempt Requirements

- source_status: `formal_gate_next_round_requirements_ready`
- next_success_attempt_status: `blocked_until_protocol_lane_decision_and_contract`
- next_success_attempt_artifact_count: `10`
- next_success_attempt_artifact_category_counts: `{'contract': 1, 'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 1}`
- old_failed_run_artifacts_invalid_for_next_success_attempt: `True`

## Post-Decision Requirements

- new_or_revised_contract_required: `False`
- contract_status_required_before_training: `approved, frozen`
- draft_contract_allows_training: `False`
- next_success_attempt_artifact_count: `10`
- formal_training_still_requires:
  - approved_or_frozen_contract
  - source_freshness_audit_after_contract
  - remote_execution_packet_for_selected_lane
  - approved_remote_preflight_for_selected_lane
- paper_result_still_requires:
  - new_gate3_formal_audit_pass
  - h02_formal_output_accepted_true
  - paper_result_input_allowed_true

## Audit

- audit_issue_count: `0`
