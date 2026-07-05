# Module2 Formal Gate Remaining Deliverables

This ledger is read-only. It lists remaining formal training, evaluation, and acceptance deliverables; it does not execute commands or write paper results.

- status: `formal_gate_deliverables_blocked`
- source_head: `818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- missing_deliverable_count: `10`
- open_category_count: `4`
- missing_counts_by_formal_category: `{'training': 3, 'evaluation': 2, 'acceptance': 3, 'formal_acceptance': 2}`
- next_blocked_lane: `decision`
- h01_status: `blocked_pending_decisions`
- h02_status: `blocked_formal_output_acceptance`
- h02_formal_output_accepted: `False`
- h02_paper_result_input_allowed: `False`
- proof_command_count: `20`
- production_plan_row_count: `10`
- audit_issue_count: `0`
- local_training_allowed_now: `False`
- remote_preflight_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_h01_evaluation_allowed_now: `False`
- formal_h02_acceptance_allowed_now: `False`
- formal_claim_allowed_now: `False`
- paper_result_material_allowed_now: `False`

## Human-Readable Gate Closure Checklist

- next_blocked_lane: `decision`
- total_missing_deliverables: `10`
- open_category_count: `4`
- local_training_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`
- `training`: missing=`3`, stage=`gate3_remote_training`, stage_allowed_now=`False`, missing_artifacts=`training:train_final_model_zip, training:train_summary_json, training:train_training_manifest_json`, proof_commands=`train_final_model_zip_exists_nonempty, train_final_model_zip_valid_zip, train_summary_json_exists_nonempty, train_summary_json_formal_warm_start_metadata, train_training_manifest_json_exists_nonempty, train_training_manifest_json_provenance`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- `evaluation`: missing=`2`, stage=`gate3_remote_audit_pullback`, stage_allowed_now=`False`, missing_artifacts=`evaluation:eval_gate3_eval_episodes_csv, evaluation:eval_gate3_summary_json`, proof_commands=`eval_gate3_eval_episodes_csv_exists_nonempty, eval_gate3_eval_episodes_csv_schema, eval_gate3_summary_json_exists_nonempty, eval_gate3_summary_json_formal_scope`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- `acceptance`: missing=`3`, stage=`gate3_remote_audit_pullback`, stage_allowed_now=`False`, missing_artifacts=`acceptance:gate3_trial_manifest_json, acceptance:gate3_formal_audit_json, acceptance:pulled_back_checkpoint_hash_record`, proof_commands=`gate3_trial_manifest_json_exists_nonempty, gate3_trial_manifest_json_formal_warm_start_scope, gate3_formal_audit_json_exists_nonempty, gate3_formal_audit_json_accepts_formal_scope, pulled_back_checkpoint_hash_record_exists_nonempty, pulled_back_checkpoint_hash_record_matches_model`, blocked_by=`f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- `formal_acceptance`: missing=`2`, stage=`regenerate_h01_h02_formal_artifacts`, stage_allowed_now=`False`, missing_artifacts=`formal_acceptance:h01_ready_for_formal_run, formal_acceptance:h02_formal_output_acceptance`, proof_commands=`h01_ready_for_formal_run_exists_nonempty, h01_ready_for_formal_run_status, h02_formal_output_acceptance_exists_nonempty, h02_formal_output_acceptance_status`, blocked_by=`missing_remote_audit_pullback, source_fresh_h01_h02_targets_open`

## Current Gate Summary

- status_report_status: `formal_gate_status_blocked`
- next_blocked_lane: `decision`
- missing_counts_by_category: `{'decision': 1, 'decision_gate': 0, 'regeneration': 20, 'gate_sequence': 7, 'training': 3, 'evaluation': 2, 'acceptance': 3, 'evaluation_acceptance': 2, 'claim_gate': 6}`
- remote_packet_status: `blocked_until_f02_6_decision`
- ready_to_run_remote_training: `False`
- h01_status: `blocked_pending_decisions`
- h02_status: `blocked_formal_output_acceptance`
- h02_formal_output_accepted: `False`
- h02_paper_result_input_allowed: `False`
- source_freshness_status: `source_freshness_clean_current`
- source_freshness_regeneration_required: `False`
- source_freshness_blocking_regeneration_required: `False`
- source_freshness_non_self_changed_records: `0`
- source_freshness_self_artifact_only_lag_records: `0`

## Formal Gate Gap Summary

- summary_id: `module2_formal_gate_missing_training_eval_acceptance_summary`
- total_missing_deliverables: `10`
- open_category_count: `4`
- execution_boundary: `read_only_no_execution`
### gap:training
- missing_count: `3`
- responsible_stage_id: `gate3_remote_training`
- responsible_stage_allowed_now: `False`
- responsible_stage_blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- missing_artifacts:
  - `training:train_final_model_zip`: state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip`, acceptance_predicate_count=`5`, proof_command_count=`2`
  - `training:train_summary_json`: state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json`, acceptance_predicate_count=`5`, proof_command_count=`2`
  - `training:train_training_manifest_json`: state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json`, acceptance_predicate_count=`5`, proof_command_count=`2`
### gap:evaluation
- missing_count: `2`
- responsible_stage_id: `gate3_remote_audit_pullback`
- responsible_stage_allowed_now: `False`
- responsible_stage_blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- missing_artifacts:
  - `evaluation:eval_gate3_eval_episodes_csv`: state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv`, acceptance_predicate_count=`5`, proof_command_count=`2`
  - `evaluation:eval_gate3_summary_json`: state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json`, acceptance_predicate_count=`5`, proof_command_count=`2`
### gap:acceptance
- missing_count: `3`
- responsible_stage_id: `gate3_remote_audit_pullback`
- responsible_stage_allowed_now: `False`
- responsible_stage_blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- missing_artifacts:
  - `acceptance:gate3_trial_manifest_json`: state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json`, acceptance_predicate_count=`5`, proof_command_count=`2`
  - `acceptance:gate3_formal_audit_json`: state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json`, acceptance_predicate_count=`5`, proof_command_count=`2`
  - `acceptance:pulled_back_checkpoint_hash_record`: state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256 or 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256.json`, acceptance_predicate_count=`5`, proof_command_count=`2`
### gap:formal_acceptance
- missing_count: `2`
- responsible_stage_id: `regenerate_h01_h02_formal_artifacts`
- responsible_stage_allowed_now: `False`
- responsible_stage_blocked_by: `missing_remote_audit_pullback, source_fresh_h01_h02_targets_open`
- missing_artifacts:
  - `formal_acceptance:h01_ready_for_formal_run`: state=`blocked_pending_decisions`, path=`0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`, acceptance_predicate_count=`5`, proof_command_count=`2`
  - `formal_acceptance:h02_formal_output_acceptance`: state=`blocked_formal_output_acceptance`, path=`0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`, acceptance_predicate_count=`5`, proof_command_count=`2`

## Proof Command Plan

- plan_id: `module2_formal_gate_local_read_only_proof_commands`
- execution_boundary: `local_read_only_after_formal_remote_pullback`
- total_matrix_rows: `10`
- total_proof_command_count: `20`
- `training:train_final_model_zip`: proof_command_count=`2`, command_ids=`train_final_model_zip_exists_nonempty, train_final_model_zip_valid_zip`
- `training:train_summary_json`: proof_command_count=`2`, command_ids=`train_summary_json_exists_nonempty, train_summary_json_formal_warm_start_metadata`
- `training:train_training_manifest_json`: proof_command_count=`2`, command_ids=`train_training_manifest_json_exists_nonempty, train_training_manifest_json_provenance`
- `evaluation:eval_gate3_eval_episodes_csv`: proof_command_count=`2`, command_ids=`eval_gate3_eval_episodes_csv_exists_nonempty, eval_gate3_eval_episodes_csv_schema`
- `evaluation:eval_gate3_summary_json`: proof_command_count=`2`, command_ids=`eval_gate3_summary_json_exists_nonempty, eval_gate3_summary_json_formal_scope`
- `acceptance:gate3_trial_manifest_json`: proof_command_count=`2`, command_ids=`gate3_trial_manifest_json_exists_nonempty, gate3_trial_manifest_json_formal_warm_start_scope`
- `acceptance:gate3_formal_audit_json`: proof_command_count=`2`, command_ids=`gate3_formal_audit_json_exists_nonempty, gate3_formal_audit_json_accepts_formal_scope`
- `acceptance:pulled_back_checkpoint_hash_record`: proof_command_count=`2`, command_ids=`pulled_back_checkpoint_hash_record_exists_nonempty, pulled_back_checkpoint_hash_record_matches_model`
- `formal_acceptance:h01_ready_for_formal_run`: proof_command_count=`2`, command_ids=`h01_ready_for_formal_run_exists_nonempty, h01_ready_for_formal_run_status`
- `formal_acceptance:h02_formal_output_acceptance`: proof_command_count=`2`, command_ids=`h02_formal_output_acceptance_exists_nonempty, h02_formal_output_acceptance_status`

## Deliverable Production Plan

- plan_id: `module2_formal_gate_deliverable_production_plan`
- source_plan: `post_f02_6_regeneration_plan`
- post_plan_status: `blocked_until_f02_6_decision`
- execution_boundary: `reference_only_no_execution`
- row_count: `10`
- rows_missing_production_stage: `0`
- rows_missing_materialization_stage: `0`
- rows_allowed_while_missing: `0`
- `training:train_final_model_zip`: generation_stage=`gate3_remote_training`, generation_allowed_now=`False`, materialization_stage=`gate3_remote_audit_pullback`, materialization_allowed_now=`False`, host=`gpu3070ti-relay`, generation_evidence_path_listed=`True`, materialization_evidence_path_listed=`True`
- `training:train_summary_json`: generation_stage=`gate3_remote_training`, generation_allowed_now=`False`, materialization_stage=`gate3_remote_audit_pullback`, materialization_allowed_now=`False`, host=`gpu3070ti-relay`, generation_evidence_path_listed=`True`, materialization_evidence_path_listed=`True`
- `training:train_training_manifest_json`: generation_stage=`gate3_remote_training`, generation_allowed_now=`False`, materialization_stage=`gate3_remote_audit_pullback`, materialization_allowed_now=`False`, host=`gpu3070ti-relay`, generation_evidence_path_listed=`True`, materialization_evidence_path_listed=`True`
- `evaluation:eval_gate3_eval_episodes_csv`: generation_stage=`gate3_remote_training`, generation_allowed_now=`False`, materialization_stage=`gate3_remote_audit_pullback`, materialization_allowed_now=`False`, host=`gpu3070ti-relay`, generation_evidence_path_listed=`True`, materialization_evidence_path_listed=`True`
- `evaluation:eval_gate3_summary_json`: generation_stage=`gate3_remote_training`, generation_allowed_now=`False`, materialization_stage=`gate3_remote_audit_pullback`, materialization_allowed_now=`False`, host=`gpu3070ti-relay`, generation_evidence_path_listed=`True`, materialization_evidence_path_listed=`True`
- `acceptance:gate3_trial_manifest_json`: generation_stage=`gate3_remote_training`, generation_allowed_now=`False`, materialization_stage=`gate3_remote_audit_pullback`, materialization_allowed_now=`False`, host=`gpu3070ti-relay`, generation_evidence_path_listed=`True`, materialization_evidence_path_listed=`True`
- `acceptance:gate3_formal_audit_json`: generation_stage=`gate3_remote_audit_pullback`, generation_allowed_now=`False`, materialization_stage=`gate3_remote_audit_pullback`, materialization_allowed_now=`False`, host=`gpu3070ti-relay`, generation_evidence_path_listed=`True`, materialization_evidence_path_listed=`True`
- `acceptance:pulled_back_checkpoint_hash_record`: generation_stage=`gate3_remote_audit_pullback`, generation_allowed_now=`False`, materialization_stage=`gate3_remote_audit_pullback`, materialization_allowed_now=`False`, host=`gpu3070ti-relay`, generation_evidence_path_listed=`False`, materialization_evidence_path_listed=`False`
- `formal_acceptance:h01_ready_for_formal_run`: generation_stage=`regenerate_h01_h02_formal_artifacts`, generation_allowed_now=`False`, materialization_stage=`regenerate_h01_h02_formal_artifacts`, materialization_allowed_now=`False`, host=`None`, generation_evidence_path_listed=`False`, materialization_evidence_path_listed=`False`
- `formal_acceptance:h02_formal_output_acceptance`: generation_stage=`regenerate_h01_h02_formal_artifacts`, generation_allowed_now=`False`, materialization_stage=`regenerate_h01_h02_formal_artifacts`, materialization_allowed_now=`False`, host=`None`, generation_evidence_path_listed=`True`, materialization_evidence_path_listed=`True`

## Deliverable Unlock Chain

- chain_id: `module2_formal_gate_missing_deliverable_unlock_chain`
- status: `blocked_missing_formal_deliverables`
- row_count: `10`
- blocked_row_count: `10`
- rows_with_missing_required_blockers: `0`
- rows_allowed_while_missing: `0`
- `training:train_final_model_zip`: missing=`True`, stage_allowed_now=`False`, required_current_blockers=`f02_6_decision_not_approved, remote_packet_not_ready`, missing_required_current_blockers=`none`, unlock_sequence=`record_f02_6_decision -> source_freshness_ready_for_remote_preflight -> remote_formal_execution_packet_ready -> approved_remote_preflight -> gate3_remote_training`
- `training:train_summary_json`: missing=`True`, stage_allowed_now=`False`, required_current_blockers=`f02_6_decision_not_approved, remote_packet_not_ready`, missing_required_current_blockers=`none`, unlock_sequence=`record_f02_6_decision -> source_freshness_ready_for_remote_preflight -> remote_formal_execution_packet_ready -> approved_remote_preflight -> gate3_remote_training`
- `training:train_training_manifest_json`: missing=`True`, stage_allowed_now=`False`, required_current_blockers=`f02_6_decision_not_approved, remote_packet_not_ready`, missing_required_current_blockers=`none`, unlock_sequence=`record_f02_6_decision -> source_freshness_ready_for_remote_preflight -> remote_formal_execution_packet_ready -> approved_remote_preflight -> gate3_remote_training`
- `evaluation:eval_gate3_eval_episodes_csv`: missing=`True`, stage_allowed_now=`False`, required_current_blockers=`f02_6_decision_not_approved, remote_packet_not_ready`, missing_required_current_blockers=`none`, unlock_sequence=`record_f02_6_decision -> source_freshness_ready_for_remote_preflight -> remote_formal_execution_packet_ready -> approved_remote_preflight -> gate3_remote_training_complete -> gate3_remote_audit_pullback`
- `evaluation:eval_gate3_summary_json`: missing=`True`, stage_allowed_now=`False`, required_current_blockers=`f02_6_decision_not_approved, remote_packet_not_ready`, missing_required_current_blockers=`none`, unlock_sequence=`record_f02_6_decision -> source_freshness_ready_for_remote_preflight -> remote_formal_execution_packet_ready -> approved_remote_preflight -> gate3_remote_training_complete -> gate3_remote_audit_pullback`
- `acceptance:gate3_trial_manifest_json`: missing=`True`, stage_allowed_now=`False`, required_current_blockers=`f02_6_decision_not_approved, remote_packet_not_ready`, missing_required_current_blockers=`none`, unlock_sequence=`record_f02_6_decision -> source_freshness_ready_for_remote_preflight -> remote_formal_execution_packet_ready -> approved_remote_preflight -> gate3_remote_training_complete -> gate3_remote_audit_pullback`
- `acceptance:gate3_formal_audit_json`: missing=`True`, stage_allowed_now=`False`, required_current_blockers=`f02_6_decision_not_approved, remote_packet_not_ready`, missing_required_current_blockers=`none`, unlock_sequence=`record_f02_6_decision -> source_freshness_ready_for_remote_preflight -> remote_formal_execution_packet_ready -> approved_remote_preflight -> gate3_remote_training_complete -> gate3_remote_audit_pullback`
- `acceptance:pulled_back_checkpoint_hash_record`: missing=`True`, stage_allowed_now=`False`, required_current_blockers=`f02_6_decision_not_approved, remote_packet_not_ready`, missing_required_current_blockers=`none`, unlock_sequence=`record_f02_6_decision -> source_freshness_ready_for_remote_preflight -> remote_formal_execution_packet_ready -> approved_remote_preflight -> gate3_remote_training_complete -> gate3_remote_audit_pullback`
- `formal_acceptance:h01_ready_for_formal_run`: missing=`True`, stage_allowed_now=`False`, required_current_blockers=`missing_remote_audit_pullback`, missing_required_current_blockers=`none`, unlock_sequence=`gate3_remote_audit_pullback_complete -> regenerate_h01_h02_formal_artifacts -> h01_h02_formal_acceptance_audit`
- `formal_acceptance:h02_formal_output_acceptance`: missing=`True`, stage_allowed_now=`False`, required_current_blockers=`missing_remote_audit_pullback`, missing_required_current_blockers=`none`, unlock_sequence=`gate3_remote_audit_pullback_complete -> regenerate_h01_h02_formal_artifacts -> h01_h02_formal_acceptance_audit`

## Deliverable Groups

### training
- status: `blocked`
- missing_count: `3`
- responsible_stage_id: `gate3_remote_training`
- responsible_stage_allowed_now: `False`
- responsible_stage_blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- items:
  - `train_final_model_zip`: missing=`True`, exists=`False`, state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip`
  - `train_summary_json`: missing=`True`, exists=`False`, state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json`
  - `train_training_manifest_json`: missing=`True`, exists=`False`, state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json`
- acceptable_evidence:
  - remote-produced train/final_model.zip pulled back to the local formal Gate3 trial directory
  - train/summary.json with PPO run metadata and terminal-RS training signals
  - train/training_manifest.json with protocol label, source head, host, seed, and command provenance
- invalid_substitutes:
  - local training output
  - available-subset smoke model
  - no-warm Gate3 failed checkpoint
  - stdout without pulled-back checkpoint and manifest
### evaluation
- status: `blocked`
- missing_count: `2`
- responsible_stage_id: `gate3_remote_audit_pullback`
- responsible_stage_allowed_now: `False`
- responsible_stage_blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- items:
  - `eval_gate3_eval_episodes_csv`: missing=`True`, exists=`False`, state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv`
  - `eval_gate3_summary_json`: missing=`True`, exists=`False`, state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json`
- acceptable_evidence:
  - eval/gate3_eval_episodes.csv from the approved formal remote run
  - eval/gate3_summary.json with formal terminal-RS success, collision, truncation, and timing fields
- invalid_substitutes:
  - H02 available-subset smoke CSV
  - paper table preview
  - no-warm formal failure eval reused as warm-start evidence
### acceptance
- status: `blocked`
- missing_count: `3`
- responsible_stage_id: `gate3_remote_audit_pullback`
- responsible_stage_allowed_now: `False`
- responsible_stage_blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- items:
  - `gate3_trial_manifest_json`: missing=`True`, exists=`False`, state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json`
  - `gate3_formal_audit_json`: missing=`True`, exists=`False`, state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json`
  - `pulled_back_checkpoint_hash_record`: missing=`True`, exists=`False`, state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256 or 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256.json`
- acceptable_evidence:
  - gate3_trial_manifest.json copied back from the formal remote run
  - gate3_formal_audit.json marking the run formal, scoped, and non-smoke
  - checkpoint SHA-256 record for the pulled-back final_model.zip
- invalid_substitutes:
  - remote command success without local pullback
  - checkpoint file without hash record
  - audit marked candidate, smoke, preview, or not_formal
### formal_acceptance
- status: `blocked`
- missing_count: `2`
- responsible_stage_id: `regenerate_h01_h02_formal_artifacts`
- responsible_stage_allowed_now: `False`
- responsible_stage_blocked_by: `missing_remote_audit_pullback, source_fresh_h01_h02_targets_open`
- items:
  - `h01_ready_for_formal_run`: missing=`True`, exists=`True`, state=`blocked_pending_decisions`, path=`0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`
  - `h02_formal_output_acceptance`: missing=`True`, exists=`True`, state=`blocked_formal_output_acceptance`, path=`0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
- acceptable_evidence:
  - H01 manifest status ready_for_formal_run or ready_for_formal_evaluation after F02.6 is closed
  - H02 acceptance with formal_output_accepted=true and paper_result_input_allowed=true
  - formal PPO rows present and accepted against the H01 required output schema
- invalid_substitutes:
  - blocked H01 manifest
  - blocked H02 acceptance audit
  - formal-looking tables generated from smoke or missing PPO rows

## Deliverable Acceptance Matrix

### training:train_final_model_zip
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip`
- missing: `True`
- current_state: `missing`
- responsible_stage_id: `gate3_remote_training`
- responsible_stage_allowed_now: `False`
- responsible_stage_blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- acceptance_predicates:
  - expected_path exists in the local pulled-back formal Gate3 artifact tree
  - artifact state is not missing, blocked, smoke, preview, or candidate
  - artifact provenance traces to the approved gpu3070ti-relay formal run after F02.6 closure
  - final_model.zip is non-empty and paired with summary.json plus training_manifest.json from the same run
  - checkpoint is later referenced by the pulled-back SHA-256 record
- proof_commands:
  - `train_final_model_zip_exists_nonempty`: python -c "from pathlib import Path; p=Path('0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip'); assert p.is_file() and p.stat().st_size > 0, p"
    - expected_evidence: `exit_code=0`
  - `train_final_model_zip_valid_zip`: python -c "from pathlib import Path; import zipfile; p=Path('0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip'); assert p.is_file() and zipfile.is_zipfile(p), p"
    - expected_evidence: `zipfile.is_zipfile(path) is true`
- invalid_substitutes:
  - local training output
  - available-subset smoke model
  - no-warm Gate3 failed checkpoint
  - stdout without pulled-back checkpoint and manifest
### training:train_summary_json
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json`
- missing: `True`
- current_state: `missing`
- responsible_stage_id: `gate3_remote_training`
- responsible_stage_allowed_now: `False`
- responsible_stage_blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- acceptance_predicates:
  - expected_path exists in the local pulled-back formal Gate3 artifact tree
  - artifact state is not missing, blocked, smoke, preview, or candidate
  - artifact provenance traces to the approved gpu3070ti-relay formal run after F02.6 closure
  - summary.json parses as JSON and records formal PPO run metadata plus terminal-RS training signals
  - summary protocol label matches the approved obstacle-summary warm-start formal Gate3 run
- proof_commands:
  - `train_summary_json_exists_nonempty`: python -c "from pathlib import Path; p=Path('0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json'); assert p.is_file() and p.stat().st_size > 0, p"
    - expected_evidence: `exit_code=0`
  - `train_summary_json_formal_warm_start_metadata`: python -c "import json; from pathlib import Path; p=Path('0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json'); data=json.loads(p.read_text(encoding='utf-8')); assert isinstance(data, dict); assert data.get('status') == 'complete'; assert data.get('warm_start_status') == 'applied_obstacle_summary_bc'; assert data.get('config', {}).get('curriculum_preset') == 'f03'; assert data.get('config', {}).get('smoke') is False"
    - expected_evidence: `status=complete, warm_start_status=applied_obstacle_summary_bc, curriculum=f03, smoke=false`
- invalid_substitutes:
  - local training output
  - available-subset smoke model
  - no-warm Gate3 failed checkpoint
  - stdout without pulled-back checkpoint and manifest
### training:train_training_manifest_json
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json`
- missing: `True`
- current_state: `missing`
- responsible_stage_id: `gate3_remote_training`
- responsible_stage_allowed_now: `False`
- responsible_stage_blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- acceptance_predicates:
  - expected_path exists in the local pulled-back formal Gate3 artifact tree
  - artifact state is not missing, blocked, smoke, preview, or candidate
  - artifact provenance traces to the approved gpu3070ti-relay formal run after F02.6 closure
  - training_manifest.json parses as JSON and records command provenance, source head, seed, and run host
  - training host is gpu3070ti-relay and local_training_allowed remains false
- proof_commands:
  - `train_training_manifest_json_exists_nonempty`: python -c "from pathlib import Path; p=Path('0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json'); assert p.is_file() and p.stat().st_size > 0, p"
    - expected_evidence: `exit_code=0`
  - `train_training_manifest_json_provenance`: python -c "import json; from pathlib import Path; p=Path('0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json'); data=json.loads(p.read_text(encoding='utf-8')); assert isinstance(data, dict); assert isinstance(data.get('command'), (str, list)); assert data.get('command'); assert isinstance(data.get('source_hashes'), dict) and data['source_hashes']; assert data.get('config', {}).get('curriculum_preset') == 'f03'"
    - expected_evidence: `command provenance, source_hashes, and f03 curriculum are present`
- invalid_substitutes:
  - local training output
  - available-subset smoke model
  - no-warm Gate3 failed checkpoint
  - stdout without pulled-back checkpoint and manifest
### evaluation:eval_gate3_eval_episodes_csv
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv`
- missing: `True`
- current_state: `missing`
- responsible_stage_id: `gate3_remote_audit_pullback`
- responsible_stage_allowed_now: `False`
- responsible_stage_blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- acceptance_predicates:
  - expected_path exists in the local pulled-back formal Gate3 artifact tree
  - artifact state is not missing, blocked, smoke, preview, or candidate
  - artifact provenance traces to the approved gpu3070ti-relay formal run after F02.6 closure
  - gate3_eval_episodes.csv contains formal episode rows for the approved PPO/RL-RS method
  - episode rows satisfy the H01 output schema including success, collision, truncation, and timing fields
- proof_commands:
  - `eval_gate3_eval_episodes_csv_exists_nonempty`: python -c "from pathlib import Path; p=Path('0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv'); assert p.is_file() and p.stat().st_size > 0, p"
    - expected_evidence: `exit_code=0`
  - `eval_gate3_eval_episodes_csv_schema`: python -c "import csv; from pathlib import Path; p=Path('0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv'); rows=list(csv.DictReader(p.open(newline='', encoding='utf-8'))); required={'terminal_rs_success','collision','truncated','nn_forward_time_s'}; assert len(rows) >= 64; assert required.issubset(rows[0])"
    - expected_evidence: `rows>=64 and terminal_rs_success/collision/truncated/nn_forward_time_s columns are present`
- invalid_substitutes:
  - H02 available-subset smoke CSV
  - paper table preview
  - no-warm formal failure eval reused as warm-start evidence
### evaluation:eval_gate3_summary_json
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json`
- missing: `True`
- current_state: `missing`
- responsible_stage_id: `gate3_remote_audit_pullback`
- responsible_stage_allowed_now: `False`
- responsible_stage_blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- acceptance_predicates:
  - expected_path exists in the local pulled-back formal Gate3 artifact tree
  - artifact state is not missing, blocked, smoke, preview, or candidate
  - artifact provenance traces to the approved gpu3070ti-relay formal run after F02.6 closure
  - gate3_summary.json parses as JSON and summarizes the pulled-back formal evaluation CSV
  - summary scope and row counts match the H01 formal evaluation manifest
- proof_commands:
  - `eval_gate3_summary_json_exists_nonempty`: python -c "from pathlib import Path; p=Path('0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json'); assert p.is_file() and p.stat().st_size > 0, p"
    - expected_evidence: `exit_code=0`
  - `eval_gate3_summary_json_formal_scope`: python -c "import json; from pathlib import Path; p=Path('0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json'); data=json.loads(p.read_text(encoding='utf-8')); assert isinstance(data, dict); assert data.get('gate_name') == 'module2_f03_gate3'; assert data.get('contract') == '.pipeline/contracts/module2-ppo-funnel-expansion.md'; assert int(data.get('episodes', 0)) >= int(data.get('min_episodes', 64)) >= 64; assert data.get('config', {}).get('curriculum_preset') == 'f03'"
    - expected_evidence: `gate_name, contract, f03 curriculum, and >=64 formal episodes are present`
- invalid_substitutes:
  - H02 available-subset smoke CSV
  - paper table preview
  - no-warm formal failure eval reused as warm-start evidence
### acceptance:gate3_trial_manifest_json
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json`
- missing: `True`
- current_state: `missing`
- responsible_stage_id: `gate3_remote_audit_pullback`
- responsible_stage_allowed_now: `False`
- responsible_stage_blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- acceptance_predicates:
  - expected_path exists in the local pulled-back formal Gate3 artifact tree
  - artifact state is not missing, blocked, smoke, preview, or candidate
  - artifact provenance traces to the approved gpu3070ti-relay formal run after F02.6 closure
  - gate3_trial_manifest.json records a formal non-smoke, non-preview, non-candidate trial
  - manifest records source head, protocol label, host, seed, command provenance, and pullback paths
- proof_commands:
  - `gate3_trial_manifest_json_exists_nonempty`: python -c "from pathlib import Path; p=Path('0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json'); assert p.is_file() and p.stat().st_size > 0, p"
    - expected_evidence: `exit_code=0`
  - `gate3_trial_manifest_json_formal_warm_start_scope`: python -c "import json; from pathlib import Path; p=Path('0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json'); data=json.loads(p.read_text(encoding='utf-8')); assert isinstance(data, dict); assert data.get('trial_name') == 'module2_f03_gate3_train_eval'; assert data.get('status') == 'complete'; assert data.get('smoke') is False; assert data.get('formal_gate_claim') is False; assert data.get('warm_start_status') == 'applied_obstacle_summary_bc'"
    - expected_evidence: `complete non-smoke trial with applied_obstacle_summary_bc warm start`
- invalid_substitutes:
  - remote command success without local pullback
  - checkpoint file without hash record
  - audit marked candidate, smoke, preview, or not_formal
### acceptance:gate3_formal_audit_json
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json`
- missing: `True`
- current_state: `missing`
- responsible_stage_id: `gate3_remote_audit_pullback`
- responsible_stage_allowed_now: `False`
- responsible_stage_blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- acceptance_predicates:
  - expected_path exists in the local pulled-back formal Gate3 artifact tree
  - artifact state is not missing, blocked, smoke, preview, or candidate
  - artifact provenance traces to the approved gpu3070ti-relay formal run after F02.6 closure
  - gate3_formal_audit.json accepts the pulled-back run as formal and scoped to the approved protocol
  - audit is generated after checkpoint, eval CSV, summary, manifest, and hash records are present
- proof_commands:
  - `gate3_formal_audit_json_exists_nonempty`: python -c "from pathlib import Path; p=Path('0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json'); assert p.is_file() and p.stat().st_size > 0, p"
    - expected_evidence: `exit_code=0`
  - `gate3_formal_audit_json_accepts_formal_scope`: python -c "import json; from pathlib import Path; p=Path('0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json'); data=json.loads(p.read_text(encoding='utf-8')); assert isinstance(data, dict); assert data.get('audit_name') == 'module2_f03_gate3_formal_audit'; assert data.get('formal_decision') in {'pass', 'fail'}; assert data.get('formal_claim_allowed') is True; assert not data.get('formal_blockers')"
    - expected_evidence: `formal_decision is pass/fail and formal_blockers is empty`
- invalid_substitutes:
  - remote command success without local pullback
  - checkpoint file without hash record
  - audit marked candidate, smoke, preview, or not_formal
### acceptance:pulled_back_checkpoint_hash_record
- expected_path: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256 or 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256.json`
- missing: `True`
- current_state: `missing`
- responsible_stage_id: `gate3_remote_audit_pullback`
- responsible_stage_allowed_now: `False`
- responsible_stage_blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- acceptance_predicates:
  - expected_path exists in the local pulled-back formal Gate3 artifact tree
  - artifact state is not missing, blocked, smoke, preview, or candidate
  - artifact provenance traces to the approved gpu3070ti-relay formal run after F02.6 closure
  - SHA-256 file or JSON exists for train/final_model.zip
  - recorded digest matches the locally pulled-back final_model.zip
- proof_commands:
  - `pulled_back_checkpoint_hash_record_exists_nonempty`: python -c "from pathlib import Path; records=[Path(item) for item in ['0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256', '0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256.json']]; record=next((item for item in records if item.is_file()), None); assert record is not None and record.stat().st_size > 0, records"
    - expected_evidence: `exit_code=0`
  - `pulled_back_checkpoint_hash_record_matches_model`: python -c "from pathlib import Path; import hashlib; records=[Path(item) for item in ['0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256', '0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256.json']]; model=Path('0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip'); record=next((item for item in records if item.is_file()), None); assert record is not None and record.stat().st_size > 0, records; digest=hashlib.sha256(model.read_bytes()).hexdigest(); assert digest in record.read_text(encoding='utf-8')"
    - expected_evidence: `recorded digest contains sha256(train/final_model.zip)`
- invalid_substitutes:
  - remote command success without local pullback
  - checkpoint file without hash record
  - audit marked candidate, smoke, preview, or not_formal
### formal_acceptance:h01_ready_for_formal_run
- expected_path: `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`
- missing: `True`
- current_state: `blocked_pending_decisions`
- responsible_stage_id: `regenerate_h01_h02_formal_artifacts`
- responsible_stage_allowed_now: `False`
- responsible_stage_blocked_by: `missing_remote_audit_pullback, source_fresh_h01_h02_targets_open`
- acceptance_predicates:
  - expected_path exists in the local pulled-back formal Gate3 artifact tree
  - artifact state is not missing, blocked, smoke, preview, or candidate
  - artifact provenance traces to the approved gpu3070ti-relay formal run after F02.6 closure
  - module2_v1_evaluation_manifest status is ready_for_formal_run or ready_for_formal_evaluation
  - manifest references the audited PPO checkpoint and requires formal PPO result rows
- proof_commands:
  - `h01_ready_for_formal_run_exists_nonempty`: python -c "from pathlib import Path; p=Path('0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json'); assert p.is_file() and p.stat().st_size > 0, p"
    - expected_evidence: `exit_code=0`
  - `h01_ready_for_formal_run_status`: python -c "import json; from pathlib import Path; p=Path('0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json'); data=json.loads(p.read_text(encoding='utf-8')); assert isinstance(data, dict); assert data.get('status') in {'ready_for_formal_run', 'ready_for_formal_evaluation'}"
    - expected_evidence: `H01 status is ready_for_formal_run or ready_for_formal_evaluation`
- invalid_substitutes:
  - blocked H01 manifest
  - blocked H02 acceptance audit
  - formal-looking tables generated from smoke or missing PPO rows
### formal_acceptance:h02_formal_output_acceptance
- expected_path: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
- missing: `True`
- current_state: `blocked_formal_output_acceptance`
- responsible_stage_id: `regenerate_h01_h02_formal_artifacts`
- responsible_stage_allowed_now: `False`
- responsible_stage_blocked_by: `missing_remote_audit_pullback, source_fresh_h01_h02_targets_open`
- acceptance_predicates:
  - expected_path exists in the local pulled-back formal Gate3 artifact tree
  - artifact state is not missing, blocked, smoke, preview, or candidate
  - artifact provenance traces to the approved gpu3070ti-relay formal run after F02.6 closure
  - h02_formal_acceptance has formal_output_accepted=true and paper_result_input_allowed=true
  - acceptance is regenerated from audited remote artifacts and rejects smoke or preview substitutes
- proof_commands:
  - `h02_formal_output_acceptance_exists_nonempty`: python -c "from pathlib import Path; p=Path('0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json'); assert p.is_file() and p.stat().st_size > 0, p"
    - expected_evidence: `exit_code=0`
  - `h02_formal_output_acceptance_status`: python -c "import json; from pathlib import Path; p=Path('0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json'); data=json.loads(p.read_text(encoding='utf-8')); assert isinstance(data, dict); assert data.get('status') == 'formal_output_accepted'; assert data.get('formal_output_accepted') is True; assert data.get('paper_result_input_allowed') is True"
    - expected_evidence: `formal_output_accepted=true and paper_result_input_allowed=true`
- invalid_substitutes:
  - blocked H01 manifest
  - blocked H02 acceptance audit
  - formal-looking tables generated from smoke or missing PPO rows

## Audit Issues

- none

## Claim Boundaries

- This ledger lists remaining formal training, evaluation, and acceptance deliverables only.
- It does not approve F02.6, run ssh/rsync, run remote preflight, train, evaluate, audit, or pull back artifacts.
- Local training remains prohibited; formal PPO training remains gpu3070ti-relay-only after the formal gate opens.
- Smoke, preview, no-warm failure, stdout-only logs, and partial pullbacks are invalid substitutes for the listed deliverables.
- This ledger is not paper result material and must not be cited as a performance result.
