# Module2 Formal Gate Remaining Deliverables

This ledger is read-only. It lists remaining formal training, evaluation, and acceptance deliverables; it does not execute commands or write paper results.

- status: `formal_gate_deliverables_blocked`
- source_head: `b04b22573dd0d37aeff35f9e75961418051c6264+dirty`
- missing_deliverable_count: `10`
- open_category_count: `4`
- audit_issue_count: `0`
- local_training_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`

## Current Gate Summary

- status_report_status: `formal_gate_status_blocked`
- next_blocked_lane: `decision`
- missing_counts_by_category: `{'decision': 1, 'decision_gate': 0, 'regeneration': 16, 'gate_sequence': 7, 'training': 3, 'evaluation': 2, 'acceptance': 3, 'evaluation_acceptance': 2, 'claim_gate': 5}`
- remote_packet_status: `blocked_until_f02_6_decision`
- ready_to_run_remote_training: `False`
- h01_status: `blocked_pending_decisions`
- h02_status: `blocked_formal_output_acceptance`
- h02_formal_output_accepted: `False`
- h02_paper_result_input_allowed: `False`

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
  - `training:train_final_model_zip`: state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip`, acceptance_predicate_count=`5`
  - `training:train_summary_json`: state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json`, acceptance_predicate_count=`5`
  - `training:train_training_manifest_json`: state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json`, acceptance_predicate_count=`5`
### gap:evaluation
- missing_count: `2`
- responsible_stage_id: `gate3_remote_audit_pullback`
- responsible_stage_allowed_now: `False`
- responsible_stage_blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- missing_artifacts:
  - `evaluation:eval_gate3_eval_episodes_csv`: state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv`, acceptance_predicate_count=`5`
  - `evaluation:eval_gate3_summary_json`: state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json`, acceptance_predicate_count=`5`
### gap:acceptance
- missing_count: `3`
- responsible_stage_id: `gate3_remote_audit_pullback`
- responsible_stage_allowed_now: `False`
- responsible_stage_blocked_by: `f02_6_decision_not_approved, source_fresh_preflight_targets_open, remote_packet_not_ready`
- missing_artifacts:
  - `acceptance:gate3_trial_manifest_json`: state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json`, acceptance_predicate_count=`5`
  - `acceptance:gate3_formal_audit_json`: state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json`, acceptance_predicate_count=`5`
  - `acceptance:pulled_back_checkpoint_hash_record`: state=`missing`, path=`0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256 or 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.sha256.json`, acceptance_predicate_count=`5`
### gap:formal_acceptance
- missing_count: `2`
- responsible_stage_id: `regenerate_h01_h02_formal_artifacts`
- responsible_stage_allowed_now: `False`
- responsible_stage_blocked_by: `missing_remote_audit_pullback, source_fresh_h01_h02_targets_open`
- missing_artifacts:
  - `formal_acceptance:h01_ready_for_formal_run`: state=`blocked_pending_decisions`, path=`0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`, acceptance_predicate_count=`5`
  - `formal_acceptance:h02_formal_output_acceptance`: state=`blocked_formal_output_acceptance`, path=`0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`, acceptance_predicate_count=`5`

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
