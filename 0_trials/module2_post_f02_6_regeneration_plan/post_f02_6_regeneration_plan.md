# Module2 Post-F02.6 Regeneration Plan

This file is an ordered plan. It does not execute commands, train, preflight, audit, or write paper results.

- status: `ready_to_execute_post_f02_6_regeneration_plan`
- executes_commands: `False`
- runs_training: `False`
- runs_remote_preflight: `False`
- local_training_allowed: `False`
- formal_claim_allowed: `False`

## Current Gate Summary

- f02_6_decision_status: `approved`
- formal_gate_status: `blocked_formal_gate_gaps_open`
- source_freshness_status: `source_freshness_risks_recorded_gate_still_blocked`
- source_freshness_regeneration_required: `True`
- source_freshness_blocking_regeneration_required: `True`
- remote_packet_status: `blocked_remote_preflight_not_ready`
- ready_to_run_remote_training: `False`

## F02.6 Human Decision Request

- present: `True`
- status: `decision_recorded`
- decision_owner_required: `Dr Sun`
- current_allowed_action_ids: `record_f02_6_decision`
- current_blocked_action_ids: `remote_preflight, remote_training, local_training, formal_claim, paper_result_material`
- post_decision_routes_are_current_authorization: `False`
- all_execution_disabled_now: `True`

## Remaining Deliverables Gap Summary

- present: `True`
- total_missing_deliverables: `10`
- open_category_count: `4`
- `training`: missing=`3`, responsible_stage=`gate3_remote_training`, allowed_now=`False`
- `evaluation`: missing=`2`, responsible_stage=`gate3_remote_audit_pullback`, allowed_now=`False`
- `acceptance`: missing=`3`, responsible_stage=`gate3_remote_audit_pullback`, allowed_now=`False`
- `formal_acceptance`: missing=`2`, responsible_stage=`regenerate_h01_h02_formal_artifacts`, allowed_now=`False`

## Remaining Deliverables Unlock Chain

- present: `True`
- chain_id: `module2_formal_gate_missing_deliverable_unlock_chain`
- status: `blocked_missing_formal_deliverables`
- execution_boundary: `read_only_no_execution`
- row_count: `10`
- blocked_row_count: `10`
- rows_with_missing_required_blockers: `8`
- rows_allowed_while_missing: `0`
- `training`: blocked_row_count=`3`, required_current_blockers=`f02_6_decision_not_approved, remote_packet_not_ready`, unlock_sequence=`record_f02_6_decision -> source_freshness_ready_for_remote_preflight -> remote_formal_execution_packet_ready -> approved_remote_preflight -> gate3_remote_training`
- `evaluation`: blocked_row_count=`2`, required_current_blockers=`f02_6_decision_not_approved, remote_packet_not_ready`, unlock_sequence=`record_f02_6_decision -> source_freshness_ready_for_remote_preflight -> remote_formal_execution_packet_ready -> approved_remote_preflight -> gate3_remote_training_complete -> gate3_remote_audit_pullback`
- `acceptance`: blocked_row_count=`3`, required_current_blockers=`f02_6_decision_not_approved, remote_packet_not_ready`, unlock_sequence=`record_f02_6_decision -> source_freshness_ready_for_remote_preflight -> remote_formal_execution_packet_ready -> approved_remote_preflight -> gate3_remote_training_complete -> gate3_remote_audit_pullback`
- `formal_acceptance`: blocked_row_count=`2`, required_current_blockers=`missing_remote_audit_pullback`, unlock_sequence=`gate3_remote_audit_pullback_complete -> regenerate_h01_h02_formal_artifacts -> h01_h02_formal_acceptance_audit`

## Ordered Stages

- `f02_6_decision_record` (decision): status=`blocked`, allowed_now=`False`, runs_training=`False`, runs_remote_preflight=`False`
  - blocked_by: `current_decision_status_approved`
  - evidence: `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json`
- `regenerate_preflight_gate_artifacts` (regeneration): status=`ready`, allowed_now=`True`, runs_training=`False`, runs_remote_preflight=`False`
  - evidence: `0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.json; 0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json; 0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json; 0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json; 0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json; 0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json; 0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json; 0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json; 0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json; 0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json; 0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`
- `approved_remote_preflight` (remote_preflight): status=`blocked`, allowed_now=`False`, runs_training=`False`, runs_remote_preflight=`True`, host=`gpu3070ti-relay`
  - blocked_by: `source_fresh_preflight_targets_open`
  - evidence: `0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_approved_remote_v1/gate3_preflight_manifest.json`
- `regenerate_remote_execution_packet` (regeneration): status=`blocked`, allowed_now=`False`, runs_training=`False`, runs_remote_preflight=`False`
  - blocked_by: `source_fresh_preflight_targets_open`
  - evidence: `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json`
- `gate3_remote_training` (training): status=`blocked`, allowed_now=`False`, runs_training=`True`, runs_remote_preflight=`False`, host=`gpu3070ti-relay`
  - blocked_by: `source_fresh_preflight_targets_open, remote_packet_not_ready`
  - evidence: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json`
- `gate3_remote_audit_pullback` (acceptance): status=`blocked`, allowed_now=`False`, runs_training=`False`, runs_remote_preflight=`False`, host=`gpu3070ti-relay`
  - blocked_by: `source_fresh_preflight_targets_open, remote_packet_not_ready`
  - evidence: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json`
- `regenerate_h01_h02_formal_artifacts` (evaluation): status=`blocked`, allowed_now=`False`, runs_training=`False`, runs_remote_preflight=`False`
  - blocked_by: `missing_remote_audit_pullback, source_fresh_h01_h02_targets_open`
  - evidence: `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json; 0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json; 0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
- `regenerate_claim_gate_artifacts` (claim_gate): status=`blocked`, allowed_now=`False`, runs_training=`False`, runs_remote_preflight=`False`
  - blocked_by: `h02_formal_acceptance_not_ready, source_fresh_claim_targets_open`
  - evidence: `0_trials/module2_claim_safety/module2_claim_safety.json; 0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json; 0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json; 0_trials/module2_formal_gate_proof_summary_chain_audit/formal_gate_proof_summary_chain_audit.json; 0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json; 0_trials/module2_formal_gate_status_report/formal_gate_status_report.json; 0_trials/module2_mainline_formal_gate_state_audit/mainline_formal_gate_state_audit.json; 0_trials/module2_paper_readiness/module2_paper_readiness.json`

## Source Regeneration Command Index

- `f02_6_warm_start_decision_packet` -> `regenerate_preflight_gate_artifacts` kind=`known_builder`, required_before=`approved_remote_preflight`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_warm_start_decision_packet`
- `f02_6_decision_record` -> `regenerate_preflight_gate_artifacts` kind=`human_decision_record`, required_before=`approved_remote_preflight`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_decision_record --decision approve_obstacle_summary_warm_start --decider 'Dr Sun' --decision-note '<Dr Sun approval note>'`
- `f02_6_decision_intake` -> `regenerate_preflight_gate_artifacts` kind=`known_builder`, required_before=`approved_remote_preflight`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_decision_intake`
- `f02_6_decision_gate_audit` -> `regenerate_preflight_gate_artifacts` kind=`known_builder`, required_before=`approved_remote_preflight`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_decision_gate_audit`
- `f02_6_transition_gate_audit` -> `regenerate_preflight_gate_artifacts` kind=`known_builder`, required_before=`approved_remote_preflight`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_transition_gate_audit`
- `remote_formal_execution_packet` -> `regenerate_preflight_gate_artifacts` kind=`known_builder`, required_before=`approved_remote_preflight`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_remote_formal_execution_packet`
- `h01_evaluation_manifest` -> `regenerate_h01_h02_formal_artifacts` kind=`known_builder`, required_before=`formal_h01_h02`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_evaluation_manifest --module2-rl-rs-checkpoint <pulled-back-final_model.zip>`
- `h02_formal_acceptance` -> `regenerate_h01_h02_formal_artifacts` kind=`known_builder`, required_before=`formal_h01_h02`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_h02_formal_acceptance`
- `claim_safety` -> `regenerate_claim_gate_artifacts` kind=`known_builder`, required_before=`formal_claim_gate`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_claim_safety`
- `paper_readiness` -> `regenerate_claim_gate_artifacts` kind=`known_builder`, required_before=`formal_claim_gate`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_paper_readiness`
- `formal_gate_gap_audit` -> `regenerate_preflight_gate_artifacts` kind=`known_builder`, required_before=`approved_remote_preflight`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_gap_audit`
- `post_f02_6_regeneration_plan` -> `regenerate_preflight_gate_artifacts` kind=`known_builder`, required_before=`approved_remote_preflight`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_regeneration_plan`
- `post_f02_6_plan_audit` -> `regenerate_preflight_gate_artifacts` kind=`known_builder`, required_before=`approved_remote_preflight`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_plan_audit`
- `remote_packet_safety_audit` -> `regenerate_preflight_gate_artifacts` kind=`known_builder`, required_before=`approved_remote_preflight`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_remote_packet_safety_audit`
- `formal_gate_closure_checklist` -> `regenerate_preflight_gate_artifacts` kind=`known_builder`, required_before=`approved_remote_preflight`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_closure_checklist`
- `gpu3070ti_readiness_refresh` -> `regenerate_preflight_gate_artifacts` kind=`read_only_remote_resource_check`, required_before=`approved_remote_preflight`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_gpu3070ti_readiness_refresh`
- `formal_gate_missing_artifacts` -> `regenerate_claim_gate_artifacts` kind=`known_builder`, required_before=`formal_claim_gate`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_missing_artifacts_audit`
- `formal_gate_status_report` -> `regenerate_claim_gate_artifacts` kind=`known_builder`, required_before=`formal_claim_gate`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_status_report`
- `formal_gate_remaining_deliverables` -> `regenerate_claim_gate_artifacts` kind=`known_builder`, required_before=`formal_claim_gate`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_remaining_deliverables`
- `formal_gate_proof_audit` -> `regenerate_claim_gate_artifacts` kind=`known_builder`, required_before=`formal_claim_gate`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_proof_audit`
- `formal_gate_proof_summary_chain_audit` -> `regenerate_claim_gate_artifacts` kind=`known_builder`, required_before=`formal_claim_gate`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_proof_summary_chain_audit`
- `mainline_formal_gate_state_audit` -> `regenerate_claim_gate_artifacts` kind=`known_builder`, required_before=`formal_claim_gate`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit`
- `formal_gate_handoff_bundle` -> `regenerate_preflight_gate_artifacts` kind=`known_builder`, required_before=`approved_remote_preflight`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_handoff_bundle`

## Claim Boundaries

- This artifact is an ordered plan, not an executor, result table, or paper appendix.
- It must not be used to bypass Dr Sun's F02.6 decision record.
- It does not run local training, remote preflight, remote training, or remote audit.
- The only training stage in the plan is remote-only on gpu3070ti-relay after all upstream gates pass.
- Source freshness risks are regeneration requirements, not formal algorithm failures.
