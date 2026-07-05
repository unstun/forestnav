# Module2 Source Freshness Audit

This file records gate artifact source-head freshness. It is not a training run, remote preflight, paper table, or result claim.

- status: `source_freshness_risks_recorded_gate_still_blocked`
- current_head: `325387fba2c9d145d0e0b742b92f0e334cf8b06d`
- runs_training: `False`
- runs_remote_preflight: `False`
- formal_claim_allowed: `False`
- regeneration_required_before_remote_formal_execution: `True`

## Risk Counts

- `historical_clean`: `11`
- `historical_dirty`: `8`

## Commit Lag Diagnostics

- `records_with_commit_lag`: `19`
- `records_with_unknown_commit_lag`: `0`
- `records_with_changed_paths_since_source`: `19`
- `records_with_artifact_path_changed_since_source`: `19`
- `records_with_non_self_changed_paths_since_source`: `18`
- `records_with_self_artifact_only_lag`: `1`
- `max_commits_since_source`: `678`
- `max_non_self_changed_path_count_since_source`: `206`
- `changed_path_sample_limit`: `12`

## Audit Self-Reference Policy

- `source_head_scope`: `generation_time_repository_head`
- `commit_storing_this_audit_known_at_generation`: `False`
- `expected_post_commit_self_lag`: `True`
- `self_lag_is_formal_gate_blocker`: `False`
- `manifest_path`: `0_trials/module2_source_freshness_audit/source_freshness_audit.json`
- `markdown_path`: `0_trials/module2_source_freshness_audit/source_freshness_audit.md`

## Regeneration Targets

- `f02_6_decision_gate_audit`: `historical_dirty`, source_head=`849c39867a5e867d9f78579c176e3b61d04d7556+dirty`, current_head=`325387fba2c9d145d0e0b742b92f0e334cf8b06d`, dirty=`True`, commit_exists=`True`, commits_since_source=`242`, changed_paths_since_source=`86`, non_self_changed_paths_since_source=`85`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.json`
- `f02_6_decision_intake`: `historical_dirty`, source_head=`858ece7f044510d35900ae0fa133b33e375e3dcf+dirty`, current_head=`325387fba2c9d145d0e0b742b92f0e334cf8b06d`, dirty=`True`, commit_exists=`True`, commits_since_source=`50`, changed_paths_since_source=`40`, non_self_changed_paths_since_source=`38`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json`
- `f02_6_decision_record`: `historical_dirty`, source_head=`849c39867a5e867d9f78579c176e3b61d04d7556+dirty`, current_head=`325387fba2c9d145d0e0b742b92f0e334cf8b06d`, dirty=`True`, commit_exists=`True`, commits_since_source=`242`, changed_paths_since_source=`86`, non_self_changed_paths_since_source=`84`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json`
- `f02_6_transition_gate_audit`: `historical_dirty`, source_head=`849c39867a5e867d9f78579c176e3b61d04d7556+dirty`, current_head=`325387fba2c9d145d0e0b742b92f0e334cf8b06d`, dirty=`True`, commit_exists=`True`, commits_since_source=`242`, changed_paths_since_source=`86`, non_self_changed_paths_since_source=`85`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json`
- `formal_gate_closure_checklist`: `historical_dirty`, source_head=`72da37c56a2009311b02bff57685ef1efcdd6dc3+dirty`, current_head=`325387fba2c9d145d0e0b742b92f0e334cf8b06d`, dirty=`True`, commit_exists=`True`, commits_since_source=`39`, changed_paths_since_source=`24`, non_self_changed_paths_since_source=`23`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json`
- `formal_gate_gap_audit`: `historical_clean`, source_head=`9949fa4b4797c875818487289ddf378efc141402`, current_head=`325387fba2c9d145d0e0b742b92f0e334cf8b06d`, dirty=`False`, commit_exists=`True`, commits_since_source=`38`, changed_paths_since_source=`22`, non_self_changed_paths_since_source=`20`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json`
- `formal_gate_handoff_bundle`: `historical_clean`, source_head=`a11e340c7b8f8ce37bb97c0699af2c4561d7674d`, current_head=`325387fba2c9d145d0e0b742b92f0e334cf8b06d`, dirty=`False`, commit_exists=`True`, commits_since_source=`12`, changed_paths_since_source=`10`, non_self_changed_paths_since_source=`8`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json`
- `gpu3070ti_readiness_refresh`: `historical_clean`, source_head=`033356f27e5255c60d64a78753054b86ef2a0428`, current_head=`325387fba2c9d145d0e0b742b92f0e334cf8b06d`, dirty=`False`, commit_exists=`True`, commits_since_source=`623`, changed_paths_since_source=`170`, non_self_changed_paths_since_source=`168`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.json`
- `post_f02_6_plan_audit`: `historical_clean`, source_head=`1b3a75f45e2992ccca370c24d1db4532ecff5887`, current_head=`325387fba2c9d145d0e0b742b92f0e334cf8b06d`, dirty=`False`, commit_exists=`True`, commits_since_source=`41`, changed_paths_since_source=`27`, non_self_changed_paths_since_source=`26`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
- `remote_formal_execution_packet`: `historical_dirty`, source_head=`01c57e4da7473cff42e2aafbd62431772eae0bb6+dirty`, current_head=`325387fba2c9d145d0e0b742b92f0e334cf8b06d`, dirty=`True`, commit_exists=`True`, commits_since_source=`466`, changed_paths_since_source=`131`, non_self_changed_paths_since_source=`129`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json`
- `remote_packet_safety_audit`: `historical_clean`, source_head=`4ca06623749ce1942ec92a671b5c71693cee6fdc`, current_head=`325387fba2c9d145d0e0b742b92f0e334cf8b06d`, dirty=`False`, commit_exists=`True`, commits_since_source=`40`, changed_paths_since_source=`26`, non_self_changed_paths_since_source=`24`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`
- `h01_evaluation_manifest`: `historical_dirty`, source_head=`4887f66ce6b4d32ce269d9da7d4a691e0ba5e5f6+dirty`, current_head=`325387fba2c9d145d0e0b742b92f0e334cf8b06d`, dirty=`True`, commit_exists=`True`, commits_since_source=`678`, changed_paths_since_source=`208`, non_self_changed_paths_since_source=`206`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `formal_h01_h02`, path `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`
- `h02_formal_acceptance`: `historical_dirty`, source_head=`5c4bf4a43c55f74b14f893e8f64dec84eb9d66ad+dirty`, current_head=`325387fba2c9d145d0e0b742b92f0e334cf8b06d`, dirty=`True`, commit_exists=`True`, commits_since_source=`461`, changed_paths_since_source=`125`, non_self_changed_paths_since_source=`124`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `formal_h01_h02`, path `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
- `claim_safety`: `historical_clean`, source_head=`d1e136a7e77379b15d9206f9d98c414e793c1533`, current_head=`325387fba2c9d145d0e0b742b92f0e334cf8b06d`, dirty=`False`, commit_exists=`True`, commits_since_source=`46`, changed_paths_since_source=`32`, non_self_changed_paths_since_source=`30`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_claim_safety/module2_claim_safety.json`
- `formal_gate_missing_artifacts`: `historical_clean`, source_head=`72da37c56a2009311b02bff57685ef1efcdd6dc3`, current_head=`325387fba2c9d145d0e0b742b92f0e334cf8b06d`, dirty=`False`, commit_exists=`True`, commits_since_source=`39`, changed_paths_since_source=`24`, non_self_changed_paths_since_source=`23`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json`
- `formal_gate_proof_audit`: `historical_clean`, source_head=`4ca2b01fed14bee09bf14b7d00eac36cecccad55`, current_head=`325387fba2c9d145d0e0b742b92f0e334cf8b06d`, dirty=`False`, commit_exists=`True`, commits_since_source=`6`, changed_paths_since_source=`6`, non_self_changed_paths_since_source=`4`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json`
- `formal_gate_remaining_deliverables`: `historical_clean`, source_head=`dfc1a89ee1fb0bf9752ef97a91c6839734dd7216`, current_head=`325387fba2c9d145d0e0b742b92f0e334cf8b06d`, dirty=`False`, commit_exists=`True`, commits_since_source=`26`, changed_paths_since_source=`16`, non_self_changed_paths_since_source=`14`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json`
- `formal_gate_status_report`: `historical_clean`, source_head=`ad69fc1bc1f7265d14b1b8c223de2274d7808c8d`, current_head=`325387fba2c9d145d0e0b742b92f0e334cf8b06d`, dirty=`False`, commit_exists=`True`, commits_since_source=`1`, changed_paths_since_source=`2`, non_self_changed_paths_since_source=`0`, self_artifact_only_lag=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
- `paper_readiness`: `historical_clean`, source_head=`21905c71383680b02db6c383db664025a0794300`, current_head=`325387fba2c9d145d0e0b742b92f0e334cf8b06d`, dirty=`False`, commit_exists=`True`, commits_since_source=`45`, changed_paths_since_source=`30`, non_self_changed_paths_since_source=`28`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_paper_readiness/module2_paper_readiness.json`

## Artifact Records

- `f02_6_decision_record`: status=`pending_human_decision`, freshness=`historical_dirty`, source_head=`849c39867a5e867d9f78579c176e3b61d04d7556+dirty`
- `f02_6_decision_intake`: status=`f02_6_decision_intake_pending_clean`, freshness=`historical_dirty`, source_head=`858ece7f044510d35900ae0fa133b33e375e3dcf+dirty`
- `f02_6_decision_gate_audit`: status=`f02_6_decision_gate_pending_clean`, freshness=`historical_dirty`, source_head=`849c39867a5e867d9f78579c176e3b61d04d7556+dirty`
- `f02_6_transition_gate_audit`: status=`f02_6_transition_gate_audit_passed`, freshness=`historical_dirty`, source_head=`849c39867a5e867d9f78579c176e3b61d04d7556+dirty`
- `remote_formal_execution_packet`: status=`blocked_until_f02_6_decision`, freshness=`historical_dirty`, source_head=`01c57e4da7473cff42e2aafbd62431772eae0bb6+dirty`
- `h01_evaluation_manifest`: status=`blocked_pending_decisions`, freshness=`historical_dirty`, source_head=`4887f66ce6b4d32ce269d9da7d4a691e0ba5e5f6+dirty`
- `h02_formal_acceptance`: status=`blocked_formal_output_acceptance`, freshness=`historical_dirty`, source_head=`5c4bf4a43c55f74b14f893e8f64dec84eb9d66ad+dirty`
- `claim_safety`: status=`blocked_formal_performance_claims`, freshness=`historical_clean`, source_head=`d1e136a7e77379b15d9206f9d98c414e793c1533`
- `paper_readiness`: status=`partial_methods_ready_results_blocked`, freshness=`historical_clean`, source_head=`21905c71383680b02db6c383db664025a0794300`
- `formal_gate_gap_audit`: status=`blocked_formal_gate_gaps_open`, freshness=`historical_clean`, source_head=`9949fa4b4797c875818487289ddf378efc141402`
- `post_f02_6_plan_audit`: status=`post_f02_6_plan_audit_passed`, freshness=`historical_clean`, source_head=`1b3a75f45e2992ccca370c24d1db4532ecff5887`
- `remote_packet_safety_audit`: status=`remote_packet_safety_audit_passed`, freshness=`historical_clean`, source_head=`4ca06623749ce1942ec92a671b5c71693cee6fdc`
- `formal_gate_closure_checklist`: status=`formal_gate_closure_blocked`, freshness=`historical_dirty`, source_head=`72da37c56a2009311b02bff57685ef1efcdd6dc3+dirty`
- `gpu3070ti_readiness_refresh`: status=`remote_readiness_refreshed_f02_6_still_blocked`, freshness=`historical_clean`, source_head=`033356f27e5255c60d64a78753054b86ef2a0428`
- `formal_gate_missing_artifacts`: status=`formal_gate_missing_artifacts_open`, freshness=`historical_clean`, source_head=`72da37c56a2009311b02bff57685ef1efcdd6dc3`
- `formal_gate_status_report`: status=`formal_gate_status_blocked`, freshness=`historical_clean`, source_head=`ad69fc1bc1f7265d14b1b8c223de2274d7808c8d`
- `formal_gate_remaining_deliverables`: status=`formal_gate_deliverables_blocked`, freshness=`historical_clean`, source_head=`dfc1a89ee1fb0bf9752ef97a91c6839734dd7216`
- `formal_gate_proof_audit`: status=`formal_gate_proof_audit_blocked`, freshness=`historical_clean`, source_head=`4ca2b01fed14bee09bf14b7d00eac36cecccad55`
- `formal_gate_handoff_bundle`: status=`blocked_until_f02_6_decision`, freshness=`historical_clean`, source_head=`a11e340c7b8f8ce37bb97c0699af2c4561d7674d`

## Claim Boundaries

- This audit records source-head freshness only; it is not a training run or paper result.
- Historical or dirty source_head values are regeneration risks, not formal experimental failures.
- The audit artifact's own post-commit source_head lag is expected and is not a formal gate blocker by itself.
- F02.6 remains the human approval gate before approved remote preflight or formal PPO training.
- Regenerate stale/dirty gate artifacts after F02.6 closes and before H01/H02 formal evaluation or formal claims.
