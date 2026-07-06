# Module2 Source Freshness Audit

This file records gate artifact source-head freshness. It is not a training run, remote preflight, paper table, or result claim.

- status: `source_freshness_risks_recorded_gate_still_blocked`
- current_head: `840721f8954515ef1aa443a6cf2d4ceda679b0f3`
- runs_training: `False`
- runs_remote_preflight: `False`
- formal_claim_allowed: `False`
- regeneration_required_before_remote_formal_execution: `True`
- blocking_regeneration_required_before_remote_formal_execution: `True`
- blocking_regeneration_target_count: `23`
- self_artifact_only_lag_target_count: `0`
- tracked_artifact_only_lag_target_count: `0`

## Risk Counts

- `historical_clean`: `10`
- `historical_dirty`: `13`

## Commit Lag Diagnostics

- `records_with_commit_lag`: `23`
- `records_with_unknown_commit_lag`: `0`
- `records_with_changed_paths_since_source`: `23`
- `records_with_artifact_path_changed_since_source`: `23`
- `records_with_non_self_changed_paths_since_source`: `23`
- `records_with_blocking_changed_paths_since_source`: `23`
- `records_with_self_artifact_only_lag`: `0`
- `records_with_tracked_artifact_only_lag`: `0`
- `max_commits_since_source`: `405`
- `max_non_self_changed_path_count_since_source`: `195`
- `max_blocking_changed_path_count_since_source`: `118`
- `changed_path_sample_limit`: `12`

## Audit Self-Reference Policy

- `source_head_scope`: `generation_time_repository_head`
- `commit_storing_this_audit_known_at_generation`: `False`
- `expected_post_commit_self_lag`: `True`
- `self_lag_is_formal_gate_blocker`: `False`
- `manifest_path`: `0_trials/module2_source_freshness_audit/source_freshness_audit.json`
- `markdown_path`: `0_trials/module2_source_freshness_audit/source_freshness_audit.md`

## Regeneration Targets

- `f02_6_decision_gate_audit`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`False`, commit_exists=`True`, commits_since_source=`405`, changed_paths_since_source=`196`, non_self_changed_paths_since_source=`195`, blocking_changed_paths_since_source=`118`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.json`
- `f02_6_decision_intake`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`False`, commit_exists=`True`, commits_since_source=`405`, changed_paths_since_source=`196`, non_self_changed_paths_since_source=`194`, blocking_changed_paths_since_source=`118`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json`
- `f02_6_decision_record`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`False`, commit_exists=`True`, commits_since_source=`405`, changed_paths_since_source=`196`, non_self_changed_paths_since_source=`195`, blocking_changed_paths_since_source=`118`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json`
- `f02_6_transition_gate_audit`: `historical_clean`, source_head=`b1c238c311ee96e614e4cc48094b712f1c352d7e`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`False`, commit_exists=`True`, commits_since_source=`304`, changed_paths_since_source=`165`, non_self_changed_paths_since_source=`163`, blocking_changed_paths_since_source=`102`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json`
- `f02_6_warm_start_decision_packet`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`False`, commit_exists=`True`, commits_since_source=`405`, changed_paths_since_source=`196`, non_self_changed_paths_since_source=`195`, blocking_changed_paths_since_source=`118`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json`
- `formal_gate_closure_checklist`: `historical_clean`, source_head=`849bc20581dab04dbc5954387ffa7a9996dc0d9a`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`False`, commit_exists=`True`, commits_since_source=`230`, changed_paths_since_source=`149`, non_self_changed_paths_since_source=`148`, blocking_changed_paths_since_source=`94`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json`
- `formal_gate_gap_audit`: `historical_dirty`, source_head=`74a171c7017ee34962c9e3a3a6044312d29e4b07+dirty`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`True`, commit_exists=`True`, commits_since_source=`219`, changed_paths_since_source=`145`, non_self_changed_paths_since_source=`143`, blocking_changed_paths_since_source=`93`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json`
- `formal_gate_handoff_bundle`: `historical_dirty`, source_head=`39a019e870c68345506067cdf398f961f416c597+dirty`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`True`, commit_exists=`True`, commits_since_source=`51`, changed_paths_since_source=`69`, non_self_changed_paths_since_source=`68`, blocking_changed_paths_since_source=`45`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json`
- `gpu3070ti_readiness_refresh`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`False`, commit_exists=`True`, commits_since_source=`405`, changed_paths_since_source=`196`, non_self_changed_paths_since_source=`194`, blocking_changed_paths_since_source=`118`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.json`
- `post_f02_6_plan_audit`: `historical_dirty`, source_head=`f7e5516acee90c0b3487f058fd48d7b8ddaca009+dirty`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`True`, commit_exists=`True`, commits_since_source=`108`, changed_paths_since_source=`92`, non_self_changed_paths_since_source=`91`, blocking_changed_paths_since_source=`59`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
- `post_f02_6_regeneration_plan`: `historical_dirty`, source_head=`74a171c7017ee34962c9e3a3a6044312d29e4b07+dirty`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`True`, commit_exists=`True`, commits_since_source=`219`, changed_paths_since_source=`145`, non_self_changed_paths_since_source=`143`, blocking_changed_paths_since_source=`93`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json`
- `remote_formal_execution_packet`: `historical_dirty`, source_head=`74a171c7017ee34962c9e3a3a6044312d29e4b07+dirty`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`True`, commit_exists=`True`, commits_since_source=`219`, changed_paths_since_source=`145`, non_self_changed_paths_since_source=`143`, blocking_changed_paths_since_source=`93`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json`
- `remote_packet_safety_audit`: `historical_dirty`, source_head=`f7e5516acee90c0b3487f058fd48d7b8ddaca009+dirty`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`True`, commit_exists=`True`, commits_since_source=`108`, changed_paths_since_source=`92`, non_self_changed_paths_since_source=`91`, blocking_changed_paths_since_source=`59`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`
- `h01_evaluation_manifest`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`False`, commit_exists=`True`, commits_since_source=`405`, changed_paths_since_source=`196`, non_self_changed_paths_since_source=`195`, blocking_changed_paths_since_source=`118`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_h01_h02`, path `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`
- `h02_formal_acceptance`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`False`, commit_exists=`True`, commits_since_source=`405`, changed_paths_since_source=`196`, non_self_changed_paths_since_source=`195`, blocking_changed_paths_since_source=`118`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_h01_h02`, path `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
- `claim_safety`: `historical_dirty`, source_head=`8d94b15602ece2611f05b72c62685425d2948c5d+dirty`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`True`, commit_exists=`True`, commits_since_source=`218`, changed_paths_since_source=`137`, non_self_changed_paths_since_source=`135`, blocking_changed_paths_since_source=`92`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_claim_safety/module2_claim_safety.json`
- `formal_gate_missing_artifacts`: `historical_clean`, source_head=`445a706946f58790a92e2bf959032688b529b140`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`False`, commit_exists=`True`, commits_since_source=`263`, changed_paths_since_source=`159`, non_self_changed_paths_since_source=`157`, blocking_changed_paths_since_source=`98`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json`
- `formal_gate_proof_audit`: `historical_dirty`, source_head=`74a171c7017ee34962c9e3a3a6044312d29e4b07+dirty`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`True`, commit_exists=`True`, commits_since_source=`219`, changed_paths_since_source=`145`, non_self_changed_paths_since_source=`144`, blocking_changed_paths_since_source=`93`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json`
- `formal_gate_proof_summary_chain_audit`: `historical_dirty`, source_head=`8d94b15602ece2611f05b72c62685425d2948c5d+dirty`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`True`, commit_exists=`True`, commits_since_source=`218`, changed_paths_since_source=`137`, non_self_changed_paths_since_source=`135`, blocking_changed_paths_since_source=`92`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_proof_summary_chain_audit/formal_gate_proof_summary_chain_audit.json`
- `formal_gate_remaining_deliverables`: `historical_dirty`, source_head=`001268dfbeada5388d905fc6704bd6f09ab609bc+dirty`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`True`, commit_exists=`True`, commits_since_source=`149`, changed_paths_since_source=`113`, non_self_changed_paths_since_source=`111`, blocking_changed_paths_since_source=`75`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json`
- `formal_gate_status_report`: `historical_dirty`, source_head=`39a019e870c68345506067cdf398f961f416c597+dirty`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`True`, commit_exists=`True`, commits_since_source=`51`, changed_paths_since_source=`69`, non_self_changed_paths_since_source=`67`, blocking_changed_paths_since_source=`45`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
- `mainline_formal_gate_state_audit`: `historical_dirty`, source_head=`39a019e870c68345506067cdf398f961f416c597+dirty`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`True`, commit_exists=`True`, commits_since_source=`51`, changed_paths_since_source=`69`, non_self_changed_paths_since_source=`68`, blocking_changed_paths_since_source=`45`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_mainline_formal_gate_state_audit/mainline_formal_gate_state_audit.json`
- `paper_readiness`: `historical_dirty`, source_head=`8d94b15602ece2611f05b72c62685425d2948c5d+dirty`, current_head=`840721f8954515ef1aa443a6cf2d4ceda679b0f3`, dirty=`True`, commit_exists=`True`, commits_since_source=`218`, changed_paths_since_source=`137`, non_self_changed_paths_since_source=`135`, blocking_changed_paths_since_source=`92`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_paper_readiness/module2_paper_readiness.json`

## Artifact Records

- `f02_6_warm_start_decision_packet`: status=`pending_human_decision`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `f02_6_decision_record`: status=`approved`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `f02_6_decision_intake`: status=`f02_6_decision_intake_closed_clean`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `f02_6_decision_gate_audit`: status=`f02_6_decision_gate_audit_passed`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `f02_6_transition_gate_audit`: status=`f02_6_transition_gate_audit_passed`, freshness=`historical_clean`, source_head=`b1c238c311ee96e614e4cc48094b712f1c352d7e`
- `remote_formal_execution_packet`: status=`blocked_until_protocol_lane_decision`, freshness=`historical_dirty`, source_head=`74a171c7017ee34962c9e3a3a6044312d29e4b07+dirty`
- `h01_evaluation_manifest`: status=`ready_for_formal_run`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `h02_formal_acceptance`: status=`blocked_formal_output_acceptance`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `claim_safety`: status=`blocked_formal_performance_claims`, freshness=`historical_dirty`, source_head=`8d94b15602ece2611f05b72c62685425d2948c5d+dirty`
- `paper_readiness`: status=`partial_methods_ready_results_blocked`, freshness=`historical_dirty`, source_head=`8d94b15602ece2611f05b72c62685425d2948c5d+dirty`
- `formal_gate_gap_audit`: status=`blocked_formal_gate_gaps_open`, freshness=`historical_dirty`, source_head=`74a171c7017ee34962c9e3a3a6044312d29e4b07+dirty`
- `post_f02_6_regeneration_plan`: status=`ready_to_execute_post_f02_6_regeneration_plan`, freshness=`historical_dirty`, source_head=`74a171c7017ee34962c9e3a3a6044312d29e4b07+dirty`
- `post_f02_6_plan_audit`: status=`post_f02_6_plan_audit_passed`, freshness=`historical_dirty`, source_head=`f7e5516acee90c0b3487f058fd48d7b8ddaca009+dirty`
- `remote_packet_safety_audit`: status=`remote_packet_safety_audit_passed`, freshness=`historical_dirty`, source_head=`f7e5516acee90c0b3487f058fd48d7b8ddaca009+dirty`
- `formal_gate_closure_checklist`: status=`formal_gate_closure_blocked`, freshness=`historical_clean`, source_head=`849bc20581dab04dbc5954387ffa7a9996dc0d9a`
- `gpu3070ti_readiness_refresh`: status=`remote_readiness_refreshed_f02_6_still_blocked`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `formal_gate_missing_artifacts`: status=`formal_gate_missing_artifacts_open`, freshness=`historical_clean`, source_head=`445a706946f58790a92e2bf959032688b529b140`
- `formal_gate_status_report`: status=`formal_gate_status_blocked`, freshness=`historical_dirty`, source_head=`39a019e870c68345506067cdf398f961f416c597+dirty`
- `formal_gate_remaining_deliverables`: status=`formal_gate_deliverables_blocked`, freshness=`historical_dirty`, source_head=`001268dfbeada5388d905fc6704bd6f09ab609bc+dirty`
- `formal_gate_proof_audit`: status=`formal_gate_proof_audit_blocked`, freshness=`historical_dirty`, source_head=`74a171c7017ee34962c9e3a3a6044312d29e4b07+dirty`
- `formal_gate_proof_summary_chain_audit`: status=`formal_gate_proof_summary_chain_consistent_blocked`, freshness=`historical_dirty`, source_head=`8d94b15602ece2611f05b72c62685425d2948c5d+dirty`
- `mainline_formal_gate_state_audit`: status=`mainline_formal_gate_state_consistent_blocked`, freshness=`historical_dirty`, source_head=`39a019e870c68345506067cdf398f961f416c597+dirty`
- `formal_gate_handoff_bundle`: status=`blocked_formal_gate_handoff`, freshness=`historical_dirty`, source_head=`39a019e870c68345506067cdf398f961f416c597+dirty`

## Claim Boundaries

- This audit records source-head freshness only; it is not a training run or paper result.
- Historical or dirty source_head values are regeneration risks, not formal experimental failures.
- The audit artifact's own post-commit source_head lag is expected and is not a formal gate blocker by itself.
- F02.6 remains the human approval gate before approved remote preflight or formal PPO training.
- Regenerate stale/dirty gate artifacts after F02.6 closes and before H01/H02 formal evaluation or formal claims.
