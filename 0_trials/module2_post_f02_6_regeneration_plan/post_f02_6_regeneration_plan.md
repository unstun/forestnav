# Module2 Post-F02.6 Regeneration Plan

This file is an ordered plan. It does not execute commands, train, preflight, audit, or write paper results.

- status: `blocked_until_f02_6_decision`
- executes_commands: `False`
- runs_training: `False`
- runs_remote_preflight: `False`
- local_training_allowed: `False`
- formal_claim_allowed: `False`

## Current Gate Summary

- f02_6_decision_status: `pending_human_decision`
- formal_gate_status: `blocked_formal_gate_gaps_open`
- source_freshness_status: `source_freshness_risks_recorded_gate_still_blocked`
- source_freshness_regeneration_required: `True`
- source_freshness_blocking_regeneration_required: `True`
- remote_packet_status: `blocked_until_f02_6_decision`
- ready_to_run_remote_training: `False`

## F02.6 Human Decision Request

- present: `True`
- status: `awaiting_dr_sun_decision`
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

## Ordered Stages

- `f02_6_decision_record` (decision): status=`ready`, allowed_now=`True`, runs_training=`False`, runs_remote_preflight=`False`
  - evidence: `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json`
- `regenerate_preflight_gate_artifacts` (regeneration): status=`blocked`, allowed_now=`False`, runs_training=`False`, runs_remote_preflight=`False`
  - blocked_by: `f02_6_decision_not_approved`
  - evidence: `0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json; 0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json; 0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json; 0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json; 0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json`
- `approved_remote_preflight` (remote_preflight): status=`blocked`, allowed_now=`False`, runs_training=`False`, runs_remote_preflight=`True`, host=`gpu3070ti-relay`
  - blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open`
  - evidence: `0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_approved_remote_v1/gate3_preflight_manifest.json`
- `regenerate_remote_execution_packet` (regeneration): status=`blocked`, allowed_now=`False`, runs_training=`False`, runs_remote_preflight=`False`
  - blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open`
  - evidence: `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json`
- `gate3_remote_training` (training): status=`blocked`, allowed_now=`False`, runs_training=`True`, runs_remote_preflight=`False`, host=`gpu3070ti-relay`
  - blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
  - evidence: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json`
- `gate3_remote_audit_pullback` (acceptance): status=`blocked`, allowed_now=`False`, runs_training=`False`, runs_remote_preflight=`False`, host=`gpu3070ti-relay`
  - blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
  - evidence: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json`
- `regenerate_h01_h02_formal_artifacts` (evaluation): status=`blocked`, allowed_now=`False`, runs_training=`False`, runs_remote_preflight=`False`
  - blocked_by: `missing_remote_audit_pullback`
  - evidence: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
- `regenerate_claim_gate_artifacts` (claim_gate): status=`blocked`, allowed_now=`False`, runs_training=`False`, runs_remote_preflight=`False`
  - blocked_by: `h02_formal_acceptance_not_ready, source_fresh_claim_targets_open`
  - evidence: `0_trials/module2_claim_safety/module2_claim_safety.json; 0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json; 0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json; 0_trials/module2_formal_gate_proof_summary_chain_audit/formal_gate_proof_summary_chain_audit.json; 0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json; 0_trials/module2_formal_gate_status_report/formal_gate_status_report.json; 0_trials/module2_mainline_formal_gate_state_audit/mainline_formal_gate_state_audit.json; 0_trials/module2_paper_readiness/module2_paper_readiness.json`

## Source Regeneration Command Index

- `formal_gate_closure_checklist` -> `regenerate_preflight_gate_artifacts` kind=`known_builder`, required_before=`approved_remote_preflight`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_closure_checklist`
- `formal_gate_gap_audit` -> `regenerate_preflight_gate_artifacts` kind=`known_builder`, required_before=`approved_remote_preflight`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_gap_audit`
- `formal_gate_handoff_bundle` -> `regenerate_preflight_gate_artifacts` kind=`known_builder`, required_before=`approved_remote_preflight`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_handoff_bundle`
- `post_f02_6_plan_audit` -> `regenerate_preflight_gate_artifacts` kind=`known_builder`, required_before=`approved_remote_preflight`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_plan_audit`
- `post_f02_6_regeneration_plan` -> `regenerate_preflight_gate_artifacts` kind=`known_builder`, required_before=`approved_remote_preflight`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_regeneration_plan`
- `claim_safety` -> `regenerate_claim_gate_artifacts` kind=`known_builder`, required_before=`formal_claim_gate`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_claim_safety`
- `formal_gate_missing_artifacts` -> `regenerate_claim_gate_artifacts` kind=`known_builder`, required_before=`formal_claim_gate`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_missing_artifacts_audit`
- `formal_gate_proof_audit` -> `regenerate_claim_gate_artifacts` kind=`known_builder`, required_before=`formal_claim_gate`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_proof_audit`
- `formal_gate_proof_summary_chain_audit` -> `regenerate_claim_gate_artifacts` kind=`known_builder`, required_before=`formal_claim_gate`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_proof_summary_chain_audit`
- `formal_gate_remaining_deliverables` -> `regenerate_claim_gate_artifacts` kind=`known_builder`, required_before=`formal_claim_gate`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_remaining_deliverables`
- `formal_gate_status_report` -> `regenerate_claim_gate_artifacts` kind=`known_builder`, required_before=`formal_claim_gate`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_status_report`
- `mainline_formal_gate_state_audit` -> `regenerate_claim_gate_artifacts` kind=`known_builder`, required_before=`formal_claim_gate`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit`
- `paper_readiness` -> `regenerate_claim_gate_artifacts` kind=`known_builder`, required_before=`formal_claim_gate`
  - command: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_paper_readiness`

## Claim Boundaries

- This artifact is an ordered plan, not an executor, result table, or paper appendix.
- It must not be used to bypass Dr Sun's F02.6 decision record.
- It does not run local training, remote preflight, remote training, or remote audit.
- The only training stage in the plan is remote-only on gpu3070ti-relay after all upstream gates pass.
- Source freshness risks are regeneration requirements, not formal algorithm failures.
