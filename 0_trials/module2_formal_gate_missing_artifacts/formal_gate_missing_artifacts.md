# Module2 Formal Gate Missing Artifacts Audit

This file inventories missing formal-gate evidence. It does not execute commands or write paper results.

- status: `formal_gate_missing_artifacts_open`
- all_required_evidence_present: `False`
- audit_issue_count: `0`
- local_training_allowed: `False`
- formal_claim_allowed: `False`

## Current Gate Summary

- f02_6_decision_record_status: `pending_human_decision`
- f02_6_decision_gate_status: `f02_6_decision_gate_pending_clean`
- f02_6_transition_gate_status: `f02_6_transition_gate_audit_passed`
- f02_6_transition_gate_audit_issue_count: `0`
- post_f02_6_plan_status: `blocked_until_f02_6_decision`
- post_plan_training_allowed_now: `False`
- post_plan_remote_preflight_allowed_now: `False`
- source_freshness_status: `source_freshness_risks_recorded_gate_still_blocked`
- source_freshness_regeneration_required: `True`
- source_freshness_blocking_regeneration_required: `True`
- remote_packet_status: `blocked_until_f02_6_decision`
- ready_to_run_remote_training: `False`
- remote_packet_safety_audit_status: `remote_packet_safety_audit_passed`
- h01_manifest_status: `blocked_pending_decisions`
- h01_blockers: `['f02_6_warm_start_decision_pending', 'missing_module2_bc_checkpoint', 'missing_module2_rl_rs_checkpoint', 'realmap_query_generation_not_frozen']`
- h02_acceptance_status: `blocked_formal_output_acceptance`
- h02_blockers: `['h02_verdict_not_formal', 'h01_manifest_not_ready', 'f02_6_warm_start_decision_pending', 'missing_module2_bc_checkpoint', 'missing_module2_rl_rs_checkpoint', 'realmap_query_generation_not_frozen', 'remote_execution_packet_not_ready', 'requires_dr_sun_approval', 'missing_gate3_formal_audit', 'h02_scale_below_h01_manifest', 'missing_ppo_result_rows', 'missing_remote_pullback_artifacts', 'f02_6_formal_chain_pending']`

## Formal Gate Handoff Index

- status: `blocked_until_f02_6_decision`
- open_requirement_count: `5`
- local_training_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_result_material_allowed_now: `False`
- next_action: `record_f02_6_decision` (requires_dr_sun=`True`, allowed_for_agent_now=`False`)
- next_action_description: Dr Sun must approve obstacle-summary warm-start or reject it before remote formal execution can proceed.
- claim_boundary: This handoff index is a gate-navigation aid; it is not a training command, evaluation command, result table, or paper-result source.

### Authority Artifacts

- decision_record: `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json`
- transition_gate_audit: `0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json`
- post_f02_6_regeneration_plan: `0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json`
- remote_formal_execution_packet: `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json`
- formal_missing_artifacts_inventory: `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json`
- h01_manifest: `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`
- h02_formal_acceptance: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`

### Handoff Requirements

- `f02_6_human_decision` (decision): status=`blocked_missing_decision`, missing_count=`1`, execution_allowed_now=`False`
  - missing_artifact_ids: `f02_6_decision_record`
  - source_artifacts: `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json; 0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json`
  - downstream_consumers: `0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json; 0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json; 0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json; 0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
- `training_remote_ppo_checkpoint` (training): status=`blocked_missing_outputs`, missing_count=`3`, execution_allowed_now=`False`
  - missing_artifact_ids: `train_final_model_zip, train_summary_json, train_training_manifest_json`
  - source_artifacts: `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json; 0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`
  - downstream_consumers: `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json; 0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
  - responsible_stage: `gate3_remote_training` (status=`blocked`, allowed_now=`False`)
- `evaluation_gate3_episode_outputs` (evaluation): status=`blocked_missing_outputs`, missing_count=`2`, execution_allowed_now=`False`
  - missing_artifact_ids: `eval_gate3_eval_episodes_csv, eval_gate3_summary_json`
  - source_artifacts: `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json; 0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
  - downstream_consumers: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
  - responsible_stage: `gate3_remote_audit_pullback` (status=`blocked`, allowed_now=`False`)
- `acceptance_remote_pullback_and_audit` (acceptance): status=`blocked_missing_outputs`, missing_count=`3`, execution_allowed_now=`False`
  - missing_artifact_ids: `gate3_trial_manifest_json, gate3_formal_audit_json, pulled_back_checkpoint_hash_record`
  - source_artifacts: `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json; 0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json; 0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
  - downstream_consumers: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
  - responsible_stage: `gate3_remote_audit_pullback` (status=`blocked`, allowed_now=`False`)
- `h01_h02_formal_evaluation_acceptance` (evaluation_acceptance): status=`blocked_missing_outputs`, missing_count=`2`, execution_allowed_now=`False`
  - missing_artifact_ids: `h01_ready_for_formal_run, h02_formal_output_acceptance`
  - source_artifacts: `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json; 0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
  - downstream_consumers: `0_trials/module2_claim_safety/module2_claim_safety.json; 0_trials/module2_paper_readiness/module2_paper_readiness.json`
  - responsible_stage: `regenerate_h01_h02_formal_artifacts` (status=`blocked`, allowed_now=`False`)

## Missing Counts

- acceptance: `3`
- claim_gate: `8`
- decision: `1`
- decision_gate: `0`
- evaluation: `2`
- evaluation_acceptance: `2`
- gate_sequence: `7`
- regeneration: `11`
- training: `3`

## Formal Gate Requirements

- `training_remote_ppo_checkpoint` (training): status=`blocked_missing_outputs`, execution_allowed_now=`False`
  - missing_artifact_ids: `train_final_model_zip, train_summary_json, train_training_manifest_json`
  - blocked_by: `train_final_model_zip, train_summary_json, train_training_manifest_json`
  - responsible_stage: `gate3_remote_training` (status=`blocked`, allowed_now=`False`)
  - responsible_stage_blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
  - acceptable_evidence: `remote-produced train/final_model.zip pulled back to the local formal Gate3 trial directory; train/summary.json with PPO run metadata and terminal-RS training signals; train/training_manifest.json with protocol label, source head, host, seed, and command provenance`
  - invalid_substitutes: `local training output; available-subset smoke model; no-warm Gate3 failed checkpoint; stdout without pulled-back checkpoint and manifest`
- `evaluation_gate3_episode_outputs` (evaluation): status=`blocked_missing_outputs`, execution_allowed_now=`False`
  - missing_artifact_ids: `eval_gate3_eval_episodes_csv, eval_gate3_summary_json`
  - blocked_by: `eval_gate3_eval_episodes_csv, eval_gate3_summary_json`
  - responsible_stage: `gate3_remote_audit_pullback` (status=`blocked`, allowed_now=`False`)
  - responsible_stage_blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
  - acceptable_evidence: `eval/gate3_eval_episodes.csv from the approved formal remote run; eval/gate3_summary.json with formal terminal-RS success, collision, truncation, and timing fields`
  - invalid_substitutes: `H02 available-subset smoke CSV; paper table preview; no-warm formal failure eval reused as warm-start evidence`
- `acceptance_remote_pullback_and_audit` (acceptance): status=`blocked_missing_outputs`, execution_allowed_now=`False`
  - missing_artifact_ids: `gate3_trial_manifest_json, gate3_formal_audit_json, pulled_back_checkpoint_hash_record`
  - blocked_by: `gate3_trial_manifest_json, gate3_formal_audit_json, pulled_back_checkpoint_hash_record`
  - responsible_stage: `gate3_remote_audit_pullback` (status=`blocked`, allowed_now=`False`)
  - responsible_stage_blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
  - acceptable_evidence: `gate3_trial_manifest.json copied back from the formal remote run; gate3_formal_audit.json marking the run formal, scoped, and non-smoke; checkpoint SHA-256 record for the pulled-back final_model.zip`
  - invalid_substitutes: `remote command success without local pullback; checkpoint file without hash record; audit marked candidate, smoke, preview, or not_formal`
- `h01_h02_formal_evaluation_acceptance` (evaluation_acceptance): status=`blocked_missing_outputs`, execution_allowed_now=`False`
  - missing_artifact_ids: `h01_ready_for_formal_run, h02_formal_output_acceptance`
  - blocked_by: `h01_ready_for_formal_run, h02_formal_output_acceptance`
  - responsible_stage: `regenerate_h01_h02_formal_artifacts` (status=`blocked`, allowed_now=`False`)
  - responsible_stage_blocked_by: `missing_remote_audit_pullback, source_fresh_h01_h02_targets_open`
  - acceptable_evidence: `H01 manifest status ready_for_formal_run or ready_for_formal_evaluation after F02.6 is closed; H02 acceptance with formal_output_accepted=true and paper_result_input_allowed=true; formal PPO rows present and accepted against the H01 required output schema`
  - invalid_substitutes: `blocked H01 manifest; blocked H02 acceptance audit; formal-looking tables generated from smoke or missing PPO rows`

## Evidence Groups

- `f02_6_decision_record` (decision): complete=`False`, blocked_by=`f02_6_decision_not_approved`
  - missing `f02_6_decision_record`: `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json` (requires Dr Sun approval record before warm-start formal chain)
- `f02_6_transition_gate_audit` (decision_gate): complete=`True`, blocked_by=``
- `source_fresh_regeneration_targets` (regeneration): complete=`False`, blocked_by=`source_freshness_regeneration_required`
  - missing `formal_gate_closure_checklist`: `0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json` (source freshness audit requires regeneration before the corresponding formal gate)
  - missing `formal_gate_gap_audit`: `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json` (source freshness audit requires regeneration before the corresponding formal gate)
  - missing `formal_gate_handoff_bundle`: `0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json` (source freshness audit requires regeneration before the corresponding formal gate)
  - missing `post_f02_6_regeneration_plan`: `0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json` (source freshness audit requires regeneration before the corresponding formal gate)
  - missing `claim_safety`: `0_trials/module2_claim_safety/module2_claim_safety.json` (source freshness audit requires regeneration before the corresponding formal gate)
  - missing `formal_gate_missing_artifacts`: `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json` (source freshness audit requires regeneration before the corresponding formal gate)
  - missing `formal_gate_proof_audit`: `0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json` (source freshness audit requires regeneration before the corresponding formal gate)
  - missing `formal_gate_proof_summary_chain_audit`: `0_trials/module2_formal_gate_proof_summary_chain_audit/formal_gate_proof_summary_chain_audit.json` (source freshness audit requires regeneration before the corresponding formal gate)
  - missing `formal_gate_remaining_deliverables`: `0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json` (source freshness audit requires regeneration before the corresponding formal gate)
  - missing `mainline_formal_gate_state_audit`: `0_trials/module2_mainline_formal_gate_state_audit/mainline_formal_gate_state_audit.json` (source freshness audit requires regeneration before the corresponding formal gate)
  - missing `paper_readiness`: `0_trials/module2_paper_readiness/module2_paper_readiness.json` (source freshness audit requires regeneration before the corresponding formal gate)
- `post_f02_6_ordered_stages` (gate_sequence): complete=`False`, blocked_by=`regenerate_preflight_gate_artifacts, approved_remote_preflight, regenerate_remote_execution_packet, gate3_remote_training, gate3_remote_audit_pullback, regenerate_h01_h02_formal_artifacts, regenerate_claim_gate_artifacts`
  - missing `regenerate_preflight_gate_artifacts`: `0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.json; 0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json; 0_trials/module2_f02_6_decision_record/f02_6_decision_record.json; 0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json; 0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json; 0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json; 0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json; 0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json; 0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.json; 0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json; 0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json; 0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json; 0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json` (f02_6_decision_not_approved)
  - missing `approved_remote_preflight`: `0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_approved_remote_v1/gate3_preflight_manifest.json` (f02_6_decision_not_approved, source_fresh_preflight_targets_open)
  - missing `regenerate_remote_execution_packet`: `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json` (f02_6_decision_not_approved, source_fresh_preflight_targets_open)
  - missing `gate3_remote_training`: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json` (f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready)
  - missing `gate3_remote_audit_pullback`: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json` (f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready)
  - missing `regenerate_h01_h02_formal_artifacts`: `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json; 0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json; 0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json` (missing_remote_audit_pullback, source_fresh_h01_h02_targets_open)
  - missing `regenerate_claim_gate_artifacts`: `0_trials/module2_claim_safety/module2_claim_safety.json; 0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json; 0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json; 0_trials/module2_formal_gate_proof_summary_chain_audit/formal_gate_proof_summary_chain_audit.json; 0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json; 0_trials/module2_formal_gate_status_report/formal_gate_status_report.json; 0_trials/module2_mainline_formal_gate_state_audit/mainline_formal_gate_state_audit.json; 0_trials/module2_paper_readiness/module2_paper_readiness.json` (h02_formal_acceptance_not_ready, source_fresh_claim_targets_open)
- `remote_training_outputs` (training): complete=`False`, blocked_by=`train_final_model_zip, train_summary_json, train_training_manifest_json`
  - missing `train_final_model_zip`: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip` (required formal Gate3 training artifact)
  - missing `train_summary_json`: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json` (required formal Gate3 training artifact)
  - missing `train_training_manifest_json`: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json` (required formal Gate3 training artifact)
- `gate3_evaluation_outputs` (evaluation): complete=`False`, blocked_by=`eval_gate3_eval_episodes_csv, eval_gate3_summary_json`
  - missing `eval_gate3_eval_episodes_csv`: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv` (required formal Gate3 evaluation artifact)
  - missing `eval_gate3_summary_json`: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json` (required formal Gate3 evaluation artifact)
- `gate3_acceptance_pullback` (acceptance): complete=`False`, blocked_by=`gate3_trial_manifest_json, gate3_formal_audit_json, pulled_back_checkpoint_hash_record`
  - missing `gate3_trial_manifest_json`: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json` (required formal Gate3 acceptance artifact)
  - missing `gate3_formal_audit_json`: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json` (required formal Gate3 acceptance artifact)
  - missing `pulled_back_checkpoint_hash_record`: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256 or 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256.json` (remote packet requires checkpoint hash before any local formal claim)
- `h01_h02_formal_evaluation_acceptance` (evaluation_acceptance): complete=`False`, blocked_by=`h01_ready_for_formal_run, h02_formal_output_acceptance`
  - missing `h01_ready_for_formal_run`: `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json` (f02_6_warm_start_decision_pending, missing_module2_bc_checkpoint, missing_module2_rl_rs_checkpoint, realmap_query_generation_not_frozen)
  - missing `h02_formal_output_acceptance`: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json` (h02_verdict_not_formal, h01_manifest_not_ready, f02_6_warm_start_decision_pending, missing_module2_bc_checkpoint, missing_module2_rl_rs_checkpoint, realmap_query_generation_not_frozen, remote_execution_packet_not_ready, requires_dr_sun_approval, missing_gate3_formal_audit, h02_scale_below_h01_manifest, missing_ppo_result_rows, missing_remote_pullback_artifacts, f02_6_formal_chain_pending)
- `claim_gate_regeneration` (claim_gate): complete=`False`, blocked_by=`claim_safety, formal_gate_missing_artifacts, formal_gate_proof_audit, formal_gate_proof_summary_chain_audit, formal_gate_remaining_deliverables, mainline_formal_gate_state_audit, paper_readiness, h02_formal_acceptance_before_claim_gate`
  - missing `claim_safety`: `0_trials/module2_claim_safety/module2_claim_safety.json` (claim gate artifact must be regenerated after H02 formal acceptance)
  - missing `formal_gate_missing_artifacts`: `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json` (claim gate artifact must be regenerated after H02 formal acceptance)
  - missing `formal_gate_proof_audit`: `0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json` (claim gate artifact must be regenerated after H02 formal acceptance)
  - missing `formal_gate_proof_summary_chain_audit`: `0_trials/module2_formal_gate_proof_summary_chain_audit/formal_gate_proof_summary_chain_audit.json` (claim gate artifact must be regenerated after H02 formal acceptance)
  - missing `formal_gate_remaining_deliverables`: `0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json` (claim gate artifact must be regenerated after H02 formal acceptance)
  - missing `mainline_formal_gate_state_audit`: `0_trials/module2_mainline_formal_gate_state_audit/mainline_formal_gate_state_audit.json` (claim gate artifact must be regenerated after H02 formal acceptance)
  - missing `paper_readiness`: `0_trials/module2_paper_readiness/module2_paper_readiness.json` (claim gate artifact must be regenerated after H02 formal acceptance)
  - missing `h02_formal_acceptance_before_claim_gate`: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json` (claim gate cannot be regenerated from blocked H02 outputs)

## Audit Issues

- none

## Claim Boundaries

- This audit lists missing formal-gate evidence; it does not run training, preflight, sync, audit, pullback, or evaluation.
- A complete file list is still not a paper claim unless Gate3 audit passes, hashes are recorded, H01 is ready, and H02 accepts formal outputs.
- F02.6 approval by Dr Sun is required before obstacle-summary warm-start formal training.
- PPO formal training remains gpu3070ti-relay-only; local training remains prohibited.
- This artifact is a gate inventory, not result-table or appendix material.
