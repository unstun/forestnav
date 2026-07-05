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
  - template: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_record --selected-lane stronger_obstacle_summary_warm_start --decider 'Dr Sun' --contract-action <action> --decision-note '<Dr Sun rationale>'`
- selected_lane: `full_patch_cnn_policy`
  - allowed_for_agent_now: `False`
  - runs_training: `False`
  - runs_remote_preflight: `False`
  - template: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_record --selected-lane full_patch_cnn_policy --decider 'Dr Sun' --contract-action <action> --decision-note '<Dr Sun rationale>'`
- selected_lane: `hybrid_ppo_analytic_fallback`
  - allowed_for_agent_now: `False`
  - runs_training: `False`
  - runs_remote_preflight: `False`
  - template: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_record --selected-lane hybrid_ppo_analytic_fallback --decider 'Dr Sun' --contract-action <action> --decision-note '<Dr Sun rationale>'`
- selected_lane: `stop_or_reframe_module2_claim`
  - allowed_for_agent_now: `False`
  - runs_training: `False`
  - runs_remote_preflight: `False`
  - template: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_record --selected-lane stop_or_reframe_module2_claim --decider 'Dr Sun' --contract-action <action> --decision-note '<Dr Sun rationale>'`

## Post-Decision Requirements

- new_or_revised_contract_required: `False`
- contract_status_required_before_training: `approved, frozen`
- draft_contract_allows_training: `False`
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
