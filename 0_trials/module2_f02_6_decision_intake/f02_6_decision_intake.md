# Module2 F02.6 Decision Intake

This read-only artifact explains how F02.6 can be closed. It does not record a decision, run preflight, train, or write paper results.

- status: `f02_6_decision_intake_failed`
- decision_owner_required: `Dr Sun`
- record_status: `approved`
- effective_warm_start_decision: `approved_obstacle_summary`
- packet_recommendation: `approve_obstacle_summary_warm_start`
- packet_authorization_status: `blocked_until_dr_sun_decision`
- packet_allowed_now: `record_f02_6_decision`
- packet_blocked_now: `remote_preflight, remote_training, local_training, formal_claim, paper_result_material`
- next_blocked_lane: `decision`
- missing_deliverable_count: `10`
- local_training_allowed_now: `False`
- remote_preflight_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`

## Next Human Decision Request

- status: `decision_recorded`
- decision_owner_required: `Dr Sun`
- valid_decisions: `approve_obstacle_summary_warm_start, reject_obstacle_summary_warm_start`
- required_record_fields: `decision, decider, decision_note`
- current_allowed_action_ids: `record_f02_6_decision`
- current_blocked_action_ids: `remote_preflight, remote_training, local_training, formal_claim, paper_result_material`
- post_decision_routes_are_current_authorization: `False`
- all_execution_disabled_now: `True`

## Decision Evidence Matrix

- present: `True`
- matrix_id: `module2_f02_6_decision_evidence_matrix`
- status: `ready_for_dr_sun_decision_not_authorization`
- route_count: `2`
- route_decisions: `approve_obstacle_summary_warm_start, reject_obstacle_summary_warm_start`
- required_evidence_count: `7`
- missing_required_evidence_count: `0`
- global_invalid_substitute_count: `4`
- current_authorization_allowed_now: `False`
- remote_preflight_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`
- paper_result_material_allowed_now: `False`
- `approve_obstacle_summary_warm_start`: next_lane_after_record=`source_fresh_regeneration`, remote_preflight_now=`False`, remote_training_now=`False`, formal_claim_now=`False`
- `reject_obstacle_summary_warm_start`: next_lane_after_record=`protocol_redesign`, remote_preflight_now=`False`, remote_training_now=`False`, formal_claim_now=`False`

## Formal Gate Decision Impact

- current_blocker: `decision`
- current_record_status: `approved`
- missing_deliverable_count: `10`
- missing_by_category: `{'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 2}`
- current_allowed_action_ids: `record_f02_6_decision`
- current_blocked_action_ids: `remote_preflight, remote_training, local_training, formal_claim, paper_result_material`
- `approve_obstacle_summary_warm_start`: next_lane_after_record=`source_fresh_regeneration`, requires_new_protocol_contract=`False`, remote_training_now=`False`, formal_claim_now=`False`
- `reject_obstacle_summary_warm_start`: next_lane_after_record=`protocol_redesign`, requires_new_protocol_contract=`True`, remote_training_now=`False`, formal_claim_now=`False`
- decision_record_is_not_training_authorization: `True`
- decision_record_is_not_paper_result_material: `True`
- local_training_allowed_now_after_record: `False`
- remote_preflight_allowed_now_after_record: `False`
- remote_training_allowed_now_after_record: `False`
- formal_claim_allowed_now_after_record: `False`
- paper_result_material_allowed_now_after_record: `False`
- formal_training_still_requires: `source_freshness_audit, post_f02_6_regeneration_plan, post_f02_6_plan_audit, remote_formal_execution_packet_ready, approved_remote_preflight`

## Required Fields

- `decision`: must be one of approve_obstacle_summary_warm_start or reject_obstacle_summary_warm_start
- `decider`: must equal Dr Sun
- `decision_note`: must be a human-readable Dr Sun note explaining the approval or rejection rationale
- decision_note_guidance: `selected decision, human rationale, evidence basis, risk accepted or avoided, next gated action`

## Command Templates

### approve_obstacle_summary_warm_start
```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_decision_record --decision approve_obstacle_summary_warm_start --decider 'Dr Sun' --decision-note '<Dr Sun approval note>'
```

### reject_obstacle_summary_warm_start
```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_decision_record --decision reject_obstacle_summary_warm_start --decider 'Dr Sun' --decision-note '<Dr Sun rejection note>'
```

## Post-Decision Route Matrix

### approve_obstacle_summary_warm_start
- next_lane_after_record: `source_fresh_regeneration`
- next_protocol: `obstacle-summary BC warm-start PPO formal gate`
- requires_new_protocol_contract: `False`
- allows_local_training_now: `False`
- allows_remote_preflight_now: `False`
- allows_remote_training_now: `False`
- allows_formal_claim_now: `False`
- required_next_artifacts: `source_freshness_audit, post_f02_6_regeneration_plan, post_f02_6_plan_audit`
- claim_boundary: Approval records Dr Sun's decision; it does not directly run preflight, train, or allow paper claims.

### reject_obstacle_summary_warm_start
- next_lane_after_record: `protocol_redesign`
- next_protocol: `stronger/full patch-CNN warm-start protocol`
- requires_new_protocol_contract: `True`
- allows_local_training_now: `False`
- allows_remote_preflight_now: `False`
- allows_remote_training_now: `False`
- allows_formal_claim_now: `False`
- required_next_artifacts: `new_or_revised_research_contract, stronger_patch_cnn_protocol_spec, fresh_formal_gate_artifact_plan`
- claim_boundary: Rejection blocks obstacle-summary warm-start PPO until a stronger protocol is approved.

## Invalid Inputs

- `decider other than Dr Sun`: Only Dr Sun can close F02.6.
- `approval or rejection without a decision note`: A formal research decision must preserve rationale for audit and future paper rebuttal.
- `manual permission flips in downstream JSON`: Downstream permissions must be regenerated from the decision record and gate artifacts.
- `local training output`: The formal PPO checkpoint must be produced on gpu3070ti-relay after the gate opens.
- `paper result table or claim preview`: F02.6 intake is not formal evaluation evidence.

## Audit Issues

- `decision_gate_has_issues`: F02.6 decision gate audit must be clean before using this intake.
- `decision_gate_failed`: F02.6 decision gate audit currently failed.

## Claim Boundaries

- This intake explains how to close F02.6; it does not close F02.6.
- It must not be cited as a PPO performance result or warm-start effect result.
- The only valid decider for a non-pending F02.6 record is Dr Sun.
- Approval records the human decision and leads to source-fresh gate regeneration; it is not a command to train.
- Rejected obstacle-summary warm-start keeps formal warm-start PPO blocked and routes to a stronger/full patch-CNN protocol.
- Local PPO training remains disallowed.
