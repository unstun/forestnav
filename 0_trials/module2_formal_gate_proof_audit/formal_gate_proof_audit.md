# Module2 Formal Gate Proof Audit

- status: `formal_gate_proof_audit_blocked`
- not_paper_result_material: `True`
- executes_commands: `False`
- runs_training: `False`
- runs_remote_preflight: `False`
- total_matrix_rows: `10`
- total_proof_command_count: `20`
- passed_proof_command_count: `2`
- failed_proof_command_count: `2`
- blocked_proof_command_count: `16`

## Blockers

- `missing_formal_training_artifacts`
- `missing_formal_evaluation_artifacts`
- `missing_formal_acceptance_artifacts`
- `failed_formal_h01_h02_acceptance_artifacts`

## Current Gate State

- remaining_deliverables_status: `formal_gate_deliverables_blocked`
- remaining_missing_deliverable_count: `10`
- remaining_open_category_count: `4`
- source_freshness_ready_for_remote_preflight: `True`
- source_freshness_status: `source_freshness_tracked_artifact_lag_only_gate_ready`
- source_freshness_regeneration_required: `True`

## Remaining Deliverables Top-Level Summary

- present: `True`
- missing_counts_by_formal_category: `{'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 2}`
- next_blocked_lane: `decision`
- h01_status: `blocked_pending_decisions`
- h02_status: `blocked_formal_output_acceptance`
- h02_formal_output_accepted: `False`
- h02_paper_result_input_allowed: `False`
- training_missing_matrix_ids: `training:train_final_model_zip, training:train_summary_json, training:train_training_manifest_json`
- evaluation_missing_matrix_ids: `evaluation:eval_gate3_eval_episodes_csv, evaluation:eval_gate3_summary_json`
- acceptance_missing_matrix_ids: `acceptance:gate3_trial_manifest_json, acceptance:gate3_formal_audit_json, acceptance:pulled_back_checkpoint_hash_record`
- formal_acceptance_missing_matrix_ids: `formal_acceptance:h01_ready_for_formal_run, formal_acceptance:h02_formal_output_acceptance`

## Missing Evidence Summary

- `training`: missing=`train_final_model_zip, train_summary_json, train_training_manifest_json`, failed=`none`
- `evaluation`: missing=`eval_gate3_eval_episodes_csv, eval_gate3_summary_json`, failed=`none`
- `acceptance`: missing=`gate3_trial_manifest_json, gate3_formal_audit_json, pulled_back_checkpoint_hash_record`, failed=`none`
- `formal_acceptance`: missing=`none`, failed=`h01_ready_for_formal_run, h02_formal_output_acceptance`

## Proof Command Results

### train_final_model_zip_exists_nonempty
- matrix_id: `training:train_final_model_zip`
- status: `blocked_missing_artifact`
- command_was_executed: `False`
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip`
- diagnostic: `expected artifact is missing: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip`

### train_final_model_zip_valid_zip
- matrix_id: `training:train_final_model_zip`
- status: `blocked_missing_artifact`
- command_was_executed: `False`
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip`
- diagnostic: `expected artifact is missing: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip`

### train_summary_json_exists_nonempty
- matrix_id: `training:train_summary_json`
- status: `blocked_missing_artifact`
- command_was_executed: `False`
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json`
- diagnostic: `expected artifact is missing: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json`

### train_summary_json_formal_warm_start_metadata
- matrix_id: `training:train_summary_json`
- status: `blocked_missing_artifact`
- command_was_executed: `False`
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json`
- diagnostic: `expected artifact is missing: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json`

### train_training_manifest_json_exists_nonempty
- matrix_id: `training:train_training_manifest_json`
- status: `blocked_missing_artifact`
- command_was_executed: `False`
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json`
- diagnostic: `expected artifact is missing: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json`

### train_training_manifest_json_provenance
- matrix_id: `training:train_training_manifest_json`
- status: `blocked_missing_artifact`
- command_was_executed: `False`
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json`
- diagnostic: `expected artifact is missing: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json`

### eval_gate3_eval_episodes_csv_exists_nonempty
- matrix_id: `evaluation:eval_gate3_eval_episodes_csv`
- status: `blocked_missing_artifact`
- command_was_executed: `False`
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv`
- diagnostic: `expected artifact is missing: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv`

### eval_gate3_eval_episodes_csv_schema
- matrix_id: `evaluation:eval_gate3_eval_episodes_csv`
- status: `blocked_missing_artifact`
- command_was_executed: `False`
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv`
- diagnostic: `expected artifact is missing: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv`

### eval_gate3_summary_json_exists_nonempty
- matrix_id: `evaluation:eval_gate3_summary_json`
- status: `blocked_missing_artifact`
- command_was_executed: `False`
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json`
- diagnostic: `expected artifact is missing: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json`

### eval_gate3_summary_json_formal_scope
- matrix_id: `evaluation:eval_gate3_summary_json`
- status: `blocked_missing_artifact`
- command_was_executed: `False`
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json`
- diagnostic: `expected artifact is missing: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json`

### gate3_trial_manifest_json_exists_nonempty
- matrix_id: `acceptance:gate3_trial_manifest_json`
- status: `blocked_missing_artifact`
- command_was_executed: `False`
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json`
- diagnostic: `expected artifact is missing: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json`

### gate3_trial_manifest_json_formal_warm_start_scope
- matrix_id: `acceptance:gate3_trial_manifest_json`
- status: `blocked_missing_artifact`
- command_was_executed: `False`
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json`
- diagnostic: `expected artifact is missing: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json`

### gate3_formal_audit_json_exists_nonempty
- matrix_id: `acceptance:gate3_formal_audit_json`
- status: `blocked_missing_artifact`
- command_was_executed: `False`
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json`
- diagnostic: `expected artifact is missing: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json`

### gate3_formal_audit_json_accepts_formal_scope
- matrix_id: `acceptance:gate3_formal_audit_json`
- status: `blocked_missing_artifact`
- command_was_executed: `False`
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json`
- diagnostic: `expected artifact is missing: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json`

### pulled_back_checkpoint_hash_record_exists_nonempty
- matrix_id: `acceptance:pulled_back_checkpoint_hash_record`
- status: `blocked_missing_artifact`
- command_was_executed: `False`
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256 or 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256.json`
- diagnostic: `expected artifact is missing: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256 or 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256.json`

### pulled_back_checkpoint_hash_record_matches_model
- matrix_id: `acceptance:pulled_back_checkpoint_hash_record`
- status: `blocked_missing_artifact`
- command_was_executed: `False`
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256 or 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256.json`
- diagnostic: `expected artifact is missing: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256 or 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256.json`

### h01_ready_for_formal_run_exists_nonempty
- matrix_id: `formal_acceptance:h01_ready_for_formal_run`
- status: `passed`
- command_was_executed: `False`
- expected_path: `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`
- diagnostic: `h01_ready_for_formal_run_exists_nonempty passed`

### h01_ready_for_formal_run_status
- matrix_id: `formal_acceptance:h01_ready_for_formal_run`
- status: `failed`
- command_was_executed: `False`
- expected_path: `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`
- diagnostic: `h01_ready_for_formal_run_status failed: ; expected H01 status is ready_for_formal_run or ready_for_formal_evaluation`

### h02_formal_output_acceptance_exists_nonempty
- matrix_id: `formal_acceptance:h02_formal_output_acceptance`
- status: `passed`
- command_was_executed: `False`
- expected_path: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
- diagnostic: `h02_formal_output_acceptance_exists_nonempty passed`

### h02_formal_output_acceptance_status
- matrix_id: `formal_acceptance:h02_formal_output_acceptance`
- status: `failed`
- command_was_executed: `False`
- expected_path: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
- diagnostic: `h02_formal_output_acceptance_status failed: ; expected formal_output_accepted=true and paper_result_input_allowed=true`

## Claim Boundaries

- This proof audit performs local read-only filesystem and metadata checks only.
- It does not execute proof command strings, run training, run remote preflight, ssh, rsync, evaluate, audit, or pull back artifacts.
- Missing proof-command evidence keeps the formal gate blocked and is not paper result material.
- Passing this audit alone would still not authorize a formal paper claim without the upstream contract, F02.6, H01/H02, and claim-safety gates.
