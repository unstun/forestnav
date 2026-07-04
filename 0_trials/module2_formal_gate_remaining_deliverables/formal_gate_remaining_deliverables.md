# Module2 Formal Gate Remaining Deliverables

This ledger is read-only. It lists remaining formal training, evaluation, and acceptance deliverables; it does not execute commands or write paper results.

- status: `formal_gate_deliverables_blocked`
- source_head: `ec0a4ba6ad60a56723cebe3a742bbd6e3609a176+dirty`
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

## Audit Issues

- none

## Claim Boundaries

- This ledger lists remaining formal training, evaluation, and acceptance deliverables only.
- It does not approve F02.6, run ssh/rsync, run remote preflight, train, evaluate, audit, or pull back artifacts.
- Local training remains prohibited; formal PPO training remains gpu3070ti-relay-only after the formal gate opens.
- Smoke, preview, no-warm failure, stdout-only logs, and partial pullbacks are invalid substitutes for the listed deliverables.
- This ledger is not paper result material and must not be cited as a performance result.
