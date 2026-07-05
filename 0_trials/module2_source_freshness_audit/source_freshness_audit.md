# Module2 Source Freshness Audit

This file records gate artifact source-head freshness. It is not a training run, remote preflight, paper table, or result claim.

- status: `source_freshness_risks_recorded_gate_still_blocked`
- current_head: `52e29e32dac4ae0e006408889541cb8d60d81451`
- runs_training: `False`
- runs_remote_preflight: `False`
- formal_claim_allowed: `False`
- regeneration_required_before_remote_formal_execution: `True`
- blocking_regeneration_required_before_remote_formal_execution: `True`
- blocking_regeneration_target_count: `22`
- self_artifact_only_lag_target_count: `0`
- tracked_artifact_only_lag_target_count: `0`

## Risk Counts

- `current_clean`: `1`
- `historical_clean`: `22`

## Commit Lag Diagnostics

- `records_with_commit_lag`: `22`
- `records_with_unknown_commit_lag`: `0`
- `records_with_changed_paths_since_source`: `22`
- `records_with_artifact_path_changed_since_source`: `22`
- `records_with_non_self_changed_paths_since_source`: `22`
- `records_with_blocking_changed_paths_since_source`: `22`
- `records_with_self_artifact_only_lag`: `0`
- `records_with_tracked_artifact_only_lag`: `0`
- `max_commits_since_source`: `139`
- `max_non_self_changed_path_count_since_source`: `100`
- `max_blocking_changed_path_count_since_source`: `43`
- `changed_path_sample_limit`: `12`

## Audit Self-Reference Policy

- `source_head_scope`: `generation_time_repository_head`
- `commit_storing_this_audit_known_at_generation`: `False`
- `expected_post_commit_self_lag`: `True`
- `self_lag_is_formal_gate_blocker`: `False`
- `manifest_path`: `0_trials/module2_source_freshness_audit/source_freshness_audit.json`
- `markdown_path`: `0_trials/module2_source_freshness_audit/source_freshness_audit.md`

## Regeneration Targets

- `f02_6_decision_gate_audit`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`52e29e32dac4ae0e006408889541cb8d60d81451`, dirty=`False`, commit_exists=`True`, commits_since_source=`139`, changed_paths_since_source=`101`, non_self_changed_paths_since_source=`100`, blocking_changed_paths_since_source=`43`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.json`
- `f02_6_decision_intake`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`52e29e32dac4ae0e006408889541cb8d60d81451`, dirty=`False`, commit_exists=`True`, commits_since_source=`139`, changed_paths_since_source=`101`, non_self_changed_paths_since_source=`99`, blocking_changed_paths_since_source=`43`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json`
- `f02_6_decision_record`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`52e29e32dac4ae0e006408889541cb8d60d81451`, dirty=`False`, commit_exists=`True`, commits_since_source=`139`, changed_paths_since_source=`101`, non_self_changed_paths_since_source=`100`, blocking_changed_paths_since_source=`43`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json`
- `f02_6_transition_gate_audit`: `historical_clean`, source_head=`b1c238c311ee96e614e4cc48094b712f1c352d7e`, current_head=`52e29e32dac4ae0e006408889541cb8d60d81451`, dirty=`False`, commit_exists=`True`, commits_since_source=`38`, changed_paths_since_source=`24`, non_self_changed_paths_since_source=`22`, blocking_changed_paths_since_source=`10`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json`
- `f02_6_warm_start_decision_packet`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`52e29e32dac4ae0e006408889541cb8d60d81451`, dirty=`False`, commit_exists=`True`, commits_since_source=`139`, changed_paths_since_source=`101`, non_self_changed_paths_since_source=`100`, blocking_changed_paths_since_source=`43`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json`
- `formal_gate_closure_checklist`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`52e29e32dac4ae0e006408889541cb8d60d81451`, dirty=`False`, commit_exists=`True`, commits_since_source=`139`, changed_paths_since_source=`101`, non_self_changed_paths_since_source=`99`, blocking_changed_paths_since_source=`43`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json`
- `formal_gate_gap_audit`: `historical_clean`, source_head=`e1a6329a97e0baa55aad8212196a537acc4dc302`, current_head=`52e29e32dac4ae0e006408889541cb8d60d81451`, dirty=`False`, commit_exists=`True`, commits_since_source=`3`, changed_paths_since_source=`14`, non_self_changed_paths_since_source=`12`, blocking_changed_paths_since_source=`2`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json`
- `formal_gate_handoff_bundle`: `historical_clean`, source_head=`e1a6329a97e0baa55aad8212196a537acc4dc302`, current_head=`52e29e32dac4ae0e006408889541cb8d60d81451`, dirty=`False`, commit_exists=`True`, commits_since_source=`3`, changed_paths_since_source=`14`, non_self_changed_paths_since_source=`12`, blocking_changed_paths_since_source=`2`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json`
- `gpu3070ti_readiness_refresh`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`52e29e32dac4ae0e006408889541cb8d60d81451`, dirty=`False`, commit_exists=`True`, commits_since_source=`139`, changed_paths_since_source=`101`, non_self_changed_paths_since_source=`99`, blocking_changed_paths_since_source=`43`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.json`
- `post_f02_6_plan_audit`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`52e29e32dac4ae0e006408889541cb8d60d81451`, dirty=`False`, commit_exists=`True`, commits_since_source=`139`, changed_paths_since_source=`101`, non_self_changed_paths_since_source=`99`, blocking_changed_paths_since_source=`43`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
- `post_f02_6_regeneration_plan`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`52e29e32dac4ae0e006408889541cb8d60d81451`, dirty=`False`, commit_exists=`True`, commits_since_source=`139`, changed_paths_since_source=`101`, non_self_changed_paths_since_source=`99`, blocking_changed_paths_since_source=`43`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json`
- `remote_formal_execution_packet`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`52e29e32dac4ae0e006408889541cb8d60d81451`, dirty=`False`, commit_exists=`True`, commits_since_source=`139`, changed_paths_since_source=`101`, non_self_changed_paths_since_source=`100`, blocking_changed_paths_since_source=`43`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json`
- `remote_packet_safety_audit`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`52e29e32dac4ae0e006408889541cb8d60d81451`, dirty=`False`, commit_exists=`True`, commits_since_source=`139`, changed_paths_since_source=`101`, non_self_changed_paths_since_source=`100`, blocking_changed_paths_since_source=`43`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`
- `h01_evaluation_manifest`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`52e29e32dac4ae0e006408889541cb8d60d81451`, dirty=`False`, commit_exists=`True`, commits_since_source=`139`, changed_paths_since_source=`101`, non_self_changed_paths_since_source=`100`, blocking_changed_paths_since_source=`43`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_h01_h02`, path `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`
- `h02_formal_acceptance`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`52e29e32dac4ae0e006408889541cb8d60d81451`, dirty=`False`, commit_exists=`True`, commits_since_source=`139`, changed_paths_since_source=`101`, non_self_changed_paths_since_source=`100`, blocking_changed_paths_since_source=`43`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_h01_h02`, path `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
- `claim_safety`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`52e29e32dac4ae0e006408889541cb8d60d81451`, dirty=`False`, commit_exists=`True`, commits_since_source=`139`, changed_paths_since_source=`101`, non_self_changed_paths_since_source=`99`, blocking_changed_paths_since_source=`43`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_claim_safety/module2_claim_safety.json`
- `formal_gate_proof_audit`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`52e29e32dac4ae0e006408889541cb8d60d81451`, dirty=`False`, commit_exists=`True`, commits_since_source=`139`, changed_paths_since_source=`101`, non_self_changed_paths_since_source=`100`, blocking_changed_paths_since_source=`43`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json`
- `formal_gate_proof_summary_chain_audit`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`52e29e32dac4ae0e006408889541cb8d60d81451`, dirty=`False`, commit_exists=`True`, commits_since_source=`139`, changed_paths_since_source=`101`, non_self_changed_paths_since_source=`99`, blocking_changed_paths_since_source=`43`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_proof_summary_chain_audit/formal_gate_proof_summary_chain_audit.json`
- `formal_gate_remaining_deliverables`: `historical_clean`, source_head=`e1a6329a97e0baa55aad8212196a537acc4dc302`, current_head=`52e29e32dac4ae0e006408889541cb8d60d81451`, dirty=`False`, commit_exists=`True`, commits_since_source=`3`, changed_paths_since_source=`14`, non_self_changed_paths_since_source=`12`, blocking_changed_paths_since_source=`2`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json`
- `formal_gate_status_report`: `historical_clean`, source_head=`e1a6329a97e0baa55aad8212196a537acc4dc302`, current_head=`52e29e32dac4ae0e006408889541cb8d60d81451`, dirty=`False`, commit_exists=`True`, commits_since_source=`3`, changed_paths_since_source=`14`, non_self_changed_paths_since_source=`12`, blocking_changed_paths_since_source=`2`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
- `mainline_formal_gate_state_audit`: `historical_clean`, source_head=`2cd4e13da6aff82d096cbf7cd11595f859ec4d05`, current_head=`52e29e32dac4ae0e006408889541cb8d60d81451`, dirty=`False`, commit_exists=`True`, commits_since_source=`40`, changed_paths_since_source=`27`, non_self_changed_paths_since_source=`25`, blocking_changed_paths_since_source=`11`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_mainline_formal_gate_state_audit/mainline_formal_gate_state_audit.json`
- `paper_readiness`: `historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`, current_head=`52e29e32dac4ae0e006408889541cb8d60d81451`, dirty=`False`, commit_exists=`True`, commits_since_source=`139`, changed_paths_since_source=`101`, non_self_changed_paths_since_source=`99`, blocking_changed_paths_since_source=`43`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_paper_readiness/module2_paper_readiness.json`

## Artifact Records

- `f02_6_warm_start_decision_packet`: status=`pending_human_decision`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `f02_6_decision_record`: status=`approved`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `f02_6_decision_intake`: status=`f02_6_decision_intake_closed_clean`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `f02_6_decision_gate_audit`: status=`f02_6_decision_gate_audit_passed`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `f02_6_transition_gate_audit`: status=`f02_6_transition_gate_audit_passed`, freshness=`historical_clean`, source_head=`b1c238c311ee96e614e4cc48094b712f1c352d7e`
- `remote_formal_execution_packet`: status=`ready_for_gpu3070ti_remote_training`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `h01_evaluation_manifest`: status=`ready_for_formal_run`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `h02_formal_acceptance`: status=`blocked_formal_output_acceptance`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `claim_safety`: status=`blocked_formal_performance_claims`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `paper_readiness`: status=`partial_methods_ready_results_blocked`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `formal_gate_gap_audit`: status=`blocked_formal_gate_gaps_open`, freshness=`historical_clean`, source_head=`e1a6329a97e0baa55aad8212196a537acc4dc302`
- `post_f02_6_regeneration_plan`: status=`ready_for_remote_training_packet_execution`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `post_f02_6_plan_audit`: status=`post_f02_6_plan_audit_passed`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `remote_packet_safety_audit`: status=`remote_packet_safety_audit_passed`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `formal_gate_closure_checklist`: status=`formal_gate_closure_blocked`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `gpu3070ti_readiness_refresh`: status=`remote_readiness_refreshed_f02_6_still_blocked`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `formal_gate_missing_artifacts`: status=`formal_gate_missing_artifacts_open`, freshness=`current_clean`, source_head=`52e29e32dac4ae0e006408889541cb8d60d81451`
- `formal_gate_status_report`: status=`formal_gate_status_blocked`, freshness=`historical_clean`, source_head=`e1a6329a97e0baa55aad8212196a537acc4dc302`
- `formal_gate_remaining_deliverables`: status=`formal_gate_deliverables_blocked`, freshness=`historical_clean`, source_head=`e1a6329a97e0baa55aad8212196a537acc4dc302`
- `formal_gate_proof_audit`: status=`formal_gate_proof_audit_blocked`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `formal_gate_proof_summary_chain_audit`: status=`formal_gate_proof_summary_chain_consistent_blocked`, freshness=`historical_clean`, source_head=`82cec025c50398dc56df7de4a1ea15b3c5e67287`
- `mainline_formal_gate_state_audit`: status=`mainline_formal_gate_state_consistent_blocked`, freshness=`historical_clean`, source_head=`2cd4e13da6aff82d096cbf7cd11595f859ec4d05`
- `formal_gate_handoff_bundle`: status=`blocked_until_protocol_lane_decision`, freshness=`historical_clean`, source_head=`e1a6329a97e0baa55aad8212196a537acc4dc302`

## Claim Boundaries

- This audit records source-head freshness only; it is not a training run or paper result.
- Historical or dirty source_head values are regeneration risks, not formal experimental failures.
- The audit artifact's own post-commit source_head lag is expected and is not a formal gate blocker by itself.
- F02.6 remains the human approval gate before approved remote preflight or formal PPO training.
- Regenerate stale/dirty gate artifacts after F02.6 closes and before H01/H02 formal evaluation or formal claims.
