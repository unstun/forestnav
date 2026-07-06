# Module2 V2 Formal Gate Chain Audit

This artifact audits the ordered formal-gate chain only. It does not run local training, remote preflight, remote training, audit, pullback, H02 acceptance, or paper-result writing.

## Status

- status: `blocked_until_source_freshness`
- current_blocking_stage_id: `source_freshness_ready`
- next_allowed_action: `rerun_source_freshness_for_v2_contract`
- remote_preflight_allowed_now: `False`
- remote_training_allowed_now: `False`
- audit_issue_count: `0`

## Stages

- `protocol_lane_decision_recorded`: satisfied=`True`, observed=`{'status': 'protocol_lane_decision_recorded', 'selected_lane_id': 'stronger_obstacle_summary_warm_start', 'contract_action': 'draft_new_contract'}`, expected=`{'selected_lane_id': 'stronger_obstacle_summary_warm_start', 'contract_action': 'draft_new_contract'}`
- `promotion_packet_ready`: satisfied=`True`, observed=`v2_contract_promotion_packet_ready_awaiting_dr_sun`, expected=`v2_contract_promotion_packet_ready_awaiting_dr_sun`
- `promotion_dry_run_ready`: satisfied=`True`, observed=`promotion_apply_ready`, expected=`promotion_apply_ready`
- `v2_contract_promoted`: satisfied=`True`, observed=`approved`, expected=`['approved', 'frozen']`
- `v2_contract_readiness_ready`: satisfied=`True`, observed=`v2_contract_ready_for_source_freshness`, expected=`v2_contract_ready_for_source_freshness`
- `source_freshness_ready`: satisfied=`False`, observed=`source_freshness_risks_recorded_gate_still_blocked`, expected=`['source_freshness_clean_current', 'source_freshness_tracked_artifact_lag_only_gate_ready']`
- `v2_remote_packet_ready`: satisfied=`False`, observed=`{'status': 'blocked_until_source_freshness', 'remote_preflight_allowed_now': False}`, expected=`{'status': 'ready_for_v2_remote_preflight', 'remote_preflight_allowed_now': True}`
- `v2_remote_preflight_ready`: satisfied=`False`, observed=`{'preflight_status': 'missing', 'formal_trial_ready': None}`, expected=`{'preflight_status': 'ready', 'formal_trial_ready': True}`
- `v2_training_artifacts_ready`: satisfied=`False`, observed=`3`, expected=`0`
- `v2_evaluation_artifacts_ready`: satisfied=`False`, observed=`2`, expected=`0`
- `v2_acceptance_artifacts_ready`: satisfied=`False`, observed=`3`, expected=`0`
- `h02_formal_acceptance_ready`: satisfied=`False`, observed=`{'status': 'blocked_formal_output_acceptance', 'formal_output_accepted': False, 'paper_result_input_allowed': False}`, expected=`{'formal_output_accepted': True, 'paper_result_input_allowed': True}`

## Audit Issues

- none

## Invalid Substitutes

- draft contract
- promotion dry-run treated as approval
- old v1 remote packet
- remote smoke without formal preflight ready
- failed warm-start PPO checkpoint
- local PPO output
- paper prose or table before H02 acceptance
