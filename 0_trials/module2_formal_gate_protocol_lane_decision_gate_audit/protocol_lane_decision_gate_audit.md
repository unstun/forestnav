# Module2 Formal Gate Protocol Lane Decision Gate Audit

This file audits the protocol-lane decision gate; it is not paper result material.

## Decision State

- packet_status: `formal_gate_protocol_lane_decision_packet_ready_for_dr_sun`
- record_status: `pending_protocol_lane_decision`
- selected_lane_id: `None`
- training_authorization: `not_authorized_by_this_decision_record`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`
- next_success_attempt_artifact_count: `10`
- old_failed_run_artifacts_invalid_for_next_success_attempt: `True`

## Decision Note Audit

- gate_review_status: `not_required_while_pending`
- gate_requires_note_quality: `False`
- decision_note_present: `False`
- mentions_selected_lane: `True`
- mentions_failed_gate3: `True`
- mentions_contract_action: `True`
- mentions_rejected_lanes: `True`
- mentions_evidence_artifacts: `True`
- quality_warning: `None`

## Allowed Next Human Actions
- `record_protocol_lane_decision`
  - requires_dr_sun: `True`
  - runs_training: `False`
  - runs_remote_preflight: `False`
  - valid_lane_ids:
    - `stronger_obstacle_summary_warm_start`
    - `full_patch_cnn_policy`
    - `hybrid_ppo_analytic_fallback`
    - `stop_or_reframe_module2_claim`

## Post-Decision Gate Requirements

- new_or_revised_contract_required: `False`
- contract_status_required_before_training: `approved, frozen`
- draft_contract_allows_training: `False`
- next_success_attempt_artifact_count: `10`
- next_success_attempt_artifact_category_counts: `{'contract': 1, 'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 1}`
- old_failed_run_artifacts_invalid_for_next_success_attempt: `True`
- formal_training_still_requires:
  - approved_or_frozen_contract
  - source_freshness_audit_after_contract
  - remote_execution_packet_for_selected_lane
  - approved_remote_preflight_for_selected_lane
- paper_result_still_requires:
  - new_gate3_formal_audit_pass
  - h02_formal_output_accepted_true
  - paper_result_input_allowed_true

## Claim Boundaries
- This audit validates the protocol-lane decision gate; it does not select a lane.
- A clean pending audit is not training authorization.
- A recorded lane decision can only unlock new/revised contract drafting, not remote execution.
- Formal claims and paper result material remain blocked until new formal acceptance passes.

## Audit

- status: `protocol_lane_decision_gate_pending_clean`
- audit_issue_count: `0`
