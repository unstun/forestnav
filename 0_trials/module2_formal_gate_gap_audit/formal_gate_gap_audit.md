# Module2 PPO-RS Formal Gate Gap Audit

This file is a formal-gate gap ledger. It is not a paper result, table, or appendix.

- status: `blocked_formal_gate_gaps_open`
- local_training_allowed: `False`
- remote_training_resource: `gpu3070ti-relay`
- formal_performance_claim_allowed: `False`

## Remote Readiness

- path: `0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.json`
- status: `remote_readiness_refreshed_f02_6_still_blocked`
- runs_training: `False`
- runs_remote_preflight: `False`
- oracle_connector_results_match: `True`
- obstacle_summary_bc_checkpoint_match: `True`

## Decision Gaps

- `f02_6_warm_start_decision_pending`
  - evidence: `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json`
  - why: Dr Sun has not approved or rejected the F02.6 obstacle-summary warm-start protocol.
  - needed: Set effective_warm_start_decision to an approved/rejected state through the decision protocol before remote formal PPO.
- `requires_dr_sun_approval`
  - evidence: `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json`
  - why: Gate artifact still reports decision blocker: requires_dr_sun_approval.
  - needed: Close F02.6 first; do not bypass it by running local training or writing result claims.

## Training Artifact Gaps

- `remote_training_packet_not_ready`
  - evidence: `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json`
  - why: Remote execution packet status is blocked_until_f02_6_decision; training command is not allowed yet.
  - needed: After F02.6 closes, regenerate approved remote preflight and require ready_to_run_remote_training=true.
- `missing_remote_pullback_artifact`
  - evidence: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip`
  - why: Required remote artifact has not been pulled back: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip.
  - needed: Run formal PPO only on gpu3070ti-relay, then pull back the complete trial directory with hashes.
- `missing_remote_pullback_artifact`
  - evidence: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json`
  - why: Required remote artifact has not been pulled back: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json.
  - needed: Run formal PPO only on gpu3070ti-relay, then pull back the complete trial directory with hashes.
- `missing_remote_pullback_artifact`
  - evidence: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json`
  - why: Required remote artifact has not been pulled back: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json.
  - needed: Run formal PPO only on gpu3070ti-relay, then pull back the complete trial directory with hashes.
- `missing_remote_pullback_artifact`
  - evidence: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv`
  - why: Required remote artifact has not been pulled back: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv.
  - needed: Run formal PPO only on gpu3070ti-relay, then pull back the complete trial directory with hashes.
- `missing_remote_pullback_artifact`
  - evidence: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json`
  - why: Required remote artifact has not been pulled back: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json.
  - needed: Run formal PPO only on gpu3070ti-relay, then pull back the complete trial directory with hashes.
- `missing_remote_pullback_artifact`
  - evidence: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json`
  - why: Required remote artifact has not been pulled back: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json.
  - needed: Run formal PPO only on gpu3070ti-relay, then pull back the complete trial directory with hashes.
- `missing_remote_pullback_artifact`
  - evidence: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json`
  - why: Required remote artifact has not been pulled back: 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json.
  - needed: Run formal PPO only on gpu3070ti-relay, then pull back the complete trial directory with hashes.
- `missing_ppo_result_rows`
  - evidence: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
  - why: H02 acceptance sees no PPO/RL-RS formal result rows.
  - needed: Generate formal evaluation outputs that include ppo_analytic_operator or ha_rl_rs_ppo rows from the audited checkpoint.
- `missing_ppo_checkpoint_hash`
  - evidence: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
  - why: PPO rows do not contain a non-empty rl_rs_checkpoint_sha256.
  - needed: Record checkpoint path and SHA-256 in every PPO/RL-RS result row.

## Evaluation Artifact Gaps

- `h01_manifest_not_ready`
  - evidence: `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`
  - why: H01 manifest status is blocked_pending_decisions.
  - needed: Regenerate H01 after F02.6 and checkpoint availability so the formal run command is unblocked.
- `formal_main_evaluation_command_missing`
  - evidence: `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`
  - why: H01 does not expose a runnable formal_main_evaluation command.
  - needed: Regenerate H01 with the audited checkpoint and formal scale so the main evaluation command is explicit.
- `h02_scale_below_h01_queries_per_bucket`
  - evidence: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
  - why: H02 queries_per_bucket observed=1.0 required=100.0.
  - needed: Run formal evaluation at the H01 scale instead of the local smoke scale.
- `h02_scale_below_h01_seed_count`
  - evidence: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
  - why: H02 seed_count observed=1.0 required=5.0.
  - needed: Run formal evaluation at the H01 scale instead of the local smoke scale.
- `h02_scale_below_h01_queries_per_map`
  - evidence: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
  - why: H02 queries_per_map observed=1.0 required=5.0.
  - needed: Run formal evaluation at the H01 scale instead of the local smoke scale.
- `h02_verdict_not_formal`
  - evidence: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
  - why: H02 verdict status is candidate_or_smoke.
  - needed: Produce formal evaluation outputs whose verdict marks formal_acceptance=true.

## Acceptance Artifact Gaps

- `missing_or_failed_gate3_formal_audit`
  - evidence: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json`
  - why: Gate3 formal audit for the approved warm-start trial is missing or not pass.
  - needed: Run remote audit after training and require formal_decision=pass before H02 acceptance.
- `h02_formal_output_not_accepted`
  - evidence: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
  - why: H02 status is blocked_formal_output_acceptance; paper_result_input_allowed=False.
  - needed: Regenerate H02 acceptance after formal evaluation, checkpoint hash, and pullback artifacts are present.
- `claim_safety_blocks_formal_performance`
  - evidence: `0_trials/module2_claim_safety/module2_claim_safety.json`
  - why: Claim safety status is blocked_formal_performance_claims.
  - needed: Regenerate claim safety only after H02 formal acceptance is true; do not manually override.
- `readiness_blocks_formal_results`
  - evidence: `0_trials/module2_paper_readiness/module2_paper_readiness.json`
  - why: Readiness status is partial_methods_ready_results_blocked; formal_results_ready=False.
  - needed: Use readiness only as a gate; do not write result material until it reports formal_results_ready=true.

## Ordered Next Steps

- `F02.6` (decision): status=`blocked`, runs_training=`False`. Close Dr Sun's obstacle-summary warm-start decision record.
- `remote_preflight` (training): status=`blocked`, runs_training=`False`, host=`gpu3070ti-relay`. Regenerate approved gpu3070ti preflight and require formal_trial_ready=true.
- `gate3_remote_training` (training): status=`blocked`, runs_training=`True`, host=`gpu3070ti-relay`. Run formal PPO Gate3 trial remotely; never on local Mac.
- `gate3_remote_audit_pullback` (acceptance): status=`blocked`, runs_training=`False`, host=`gpu3070ti-relay`. Audit remote trial, pull back checkpoint/eval/audit artifacts, and record hashes.
- `h01_h02_regeneration` (evaluation): status=`blocked`, runs_training=`False`. Regenerate H01 with checkpoint and run H02 formal evaluation at H01 scale.
- `claim_safety_final_gate` (acceptance): status=`blocked`, runs_training=`False`. Regenerate claim safety/readiness; allow formal claims only if all gates pass.

## Claim Boundaries

- This audit is a formal-gate gap ledger, not a paper result, table, or appendix.
- Do not write performance-improvement or warm-start-effect claims from this artifact.
- No PPO/RL-RS formal training is allowed on the local Mac.
- Formal PPO checkpoint production must run on gpu3070ti-relay after F02.6 closes.
- Remote completion is insufficient until audit artifacts, checkpoint hashes, H01/H02 regeneration, and claim safety all pass.
