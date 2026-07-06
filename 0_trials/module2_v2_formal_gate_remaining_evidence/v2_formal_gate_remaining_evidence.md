# Module2 V2 Formal Gate Remaining Evidence

This is a formal-gate evidence ledger. It does not run local training, remote preflight, remote training, audit, pullback, or paper-result writing.

## Status

- status: `blocked_until_source_freshness`
- source_head: `840721f8954515ef1aa443a6cf2d4ceda679b0f3`
- remote_preflight_allowed_now: `False`
- remote_training_allowed_now: `False`
- paper_result_material_allowed_now: `False`

## Failed Gate3 Basis

- decision: `fail`
- terminal_rs_success_rate: `0.53125`
- required_success_threshold: `0.8`
- threshold_deficit: `0.26875`

## Gate Blockers

- `source_freshness_not_ready`: observed=`source_freshness_risks_recorded_gate_still_blocked`, expected=`['source_freshness_clean_current', 'source_freshness_tracked_artifact_lag_only_gate_ready']`
- `v2_remote_execution_packet_not_ready`: observed=`blocked_until_source_freshness`, expected=`ready_for_v2_remote_preflight`
- `v2_remote_preflight_manifest_not_ready`: observed=`missing`, expected=`ready + formal_trial_ready=true`

## Remaining Evidence Summary

- `acceptance`: missing_or_unsatisfied=`3` / total=`3`
- `contract`: missing_or_unsatisfied=`0` / total=`1`
- `evaluation`: missing_or_unsatisfied=`2` / total=`2`
- `formal_acceptance`: missing_or_unsatisfied=`1` / total=`1`
- `gate_precondition`: missing_or_unsatisfied=`2` / total=`2`
- `training`: missing_or_unsatisfied=`3` / total=`3`

## Deliverables

### `contract:v2_contract_promoted`
- expected_path: `.pipeline/contracts/module2-stronger_obstacle_summary_warm_start-v2.md`
- state: `contract_status_approved`
- satisfied_for_v2_success_attempt: `True`
- required_before: `new_success_training`
- proof_requirement: approved_or_frozen_contract_before_any_new_training

### `gate_precondition:source_freshness_ready`
- expected_path: `0_trials/module2_source_freshness_audit/source_freshness_audit.json`
- state: `source_freshness_risks_recorded_gate_still_blocked`
- satisfied_for_v2_success_attempt: `False`
- required_before: `remote_preflight`
- proof_requirement: source freshness gate ready for the v2 contract/source head

### `gate_precondition:v2_remote_preflight_manifest`
- expected_path: `0_trials/module2_remote_preflight/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706/gate3_preflight_manifest.json`
- state: `missing`
- satisfied_for_v2_success_attempt: `False`
- required_before: `remote_training`
- proof_requirement: remote preflight manifest reports ready and formal_trial_ready=true

### `training:train_final_model_zip`
- expected_path: `0_trials/module2_gate3_formal/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706/train/final_model.zip`
- state: `missing`
- satisfied_for_v2_success_attempt: `False`
- required_before: `new_gate3_formal_audit`
- proof_requirement: remote-produced PPO checkpoint pulled back from gpu3070ti-relay

### `training:train_summary_json`
- expected_path: `0_trials/module2_gate3_formal/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706/train/summary.json`
- state: `missing`
- satisfied_for_v2_success_attempt: `False`
- required_before: `new_gate3_formal_audit`
- proof_requirement: training summary records complete v2 remote PPO run

### `training:train_training_manifest_json`
- expected_path: `0_trials/module2_gate3_formal/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706/train/training_manifest.json`
- state: `missing`
- satisfied_for_v2_success_attempt: `False`
- required_before: `new_gate3_formal_audit`
- proof_requirement: training manifest records source, command, host, and checkpoint provenance

### `evaluation:eval_gate3_eval_episodes_csv`
- expected_path: `0_trials/module2_gate3_formal/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706/eval/gate3_eval_episodes.csv`
- state: `missing`
- satisfied_for_v2_success_attempt: `False`
- required_before: `new_gate3_formal_audit`
- proof_requirement: per-episode formal Gate3 CSV from the new v2 attempt

### `evaluation:eval_gate3_summary_json`
- expected_path: `0_trials/module2_gate3_formal/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706/eval/gate3_summary.json`
- state: `missing`
- satisfied_for_v2_success_attempt: `False`
- required_before: `new_gate3_formal_audit`
- proof_requirement: formal Gate3 summary reaches the locked threshold

### `acceptance:gate3_trial_manifest_json`
- expected_path: `0_trials/module2_gate3_formal/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706/gate3_trial_manifest.json`
- state: `missing`
- satisfied_for_v2_success_attempt: `False`
- required_before: `h02_formal_output_acceptance`
- proof_requirement: trial manifest ties train/eval/audit to the v2 contract

### `acceptance:gate3_formal_audit_json`
- expected_path: `0_trials/module2_gate3_formal/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706/gate3_formal_audit.json`
- state: `missing`
- satisfied_for_v2_success_attempt: `False`
- required_before: `h02_formal_output_acceptance`
- proof_requirement: formal audit passes for the new v2 attempt

### `acceptance:pulled_back_checkpoint_hash_record`
- expected_path: `0_trials/module2_gate3_formal/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706/train/final_model.zip.sha256`
- state: `missing`
- satisfied_for_v2_success_attempt: `False`
- required_before: `h02_formal_output_acceptance`
- proof_requirement: pulled-back checkpoint hash matches the evaluated model

### `formal_acceptance:h02_formal_output_acceptance`
- expected_path: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
- state: `blocked_formal_output_acceptance`
- satisfied_for_v2_success_attempt: `False`
- required_before: `paper_result_material`
- proof_requirement: H02 accepts the new v2 PPO rows for paper-result input

## Next Ordered Actions

- Regenerate blocking source-freshness targets
- Rebuild the v2 remote execution packet

## Invalid Substitutes

- local PPO training output
- failed gate3_obstacle_summary_warm_approved_v1 checkpoint or summary
- old v1 remote execution packet
- remote preflight smoke without formal_trial_ready
- H02 smoke rows or blocked H02 acceptance
- paper result table, appendix prose, or narrative reinterpretation
