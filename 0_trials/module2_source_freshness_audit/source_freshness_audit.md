# Module2 Source Freshness Audit

This file records gate artifact source-head freshness. It is not a training run, remote preflight, paper table, or result claim.

- status: `source_freshness_risks_recorded_gate_still_blocked`
- current_head: `2a19340105406bae8ad54ba1eac679b95a41580f`
- runs_training: `False`
- runs_remote_preflight: `False`
- formal_claim_allowed: `False`
- regeneration_required_before_remote_formal_execution: `True`
- blocking_regeneration_required_before_remote_formal_execution: `True`
- blocking_regeneration_target_count: `23`
- self_artifact_only_lag_target_count: `0`
- tracked_artifact_only_lag_target_count: `0`

## Risk Counts

- `historical_clean`: `12`
- `historical_dirty`: `11`

## Commit Lag Diagnostics

- `records_with_commit_lag`: `23`
- `records_with_unknown_commit_lag`: `0`
- `records_with_changed_paths_since_source`: `23`
- `records_with_artifact_path_changed_since_source`: `19`
- `records_with_non_self_changed_paths_since_source`: `23`
- `records_with_blocking_changed_paths_since_source`: `23`
- `records_with_self_artifact_only_lag`: `0`
- `records_with_tracked_artifact_only_lag`: `0`
- `max_commits_since_source`: `55`
- `max_non_self_changed_path_count_since_source`: `63`
- `max_blocking_changed_path_count_since_source`: `24`
- `changed_path_sample_limit`: `12`

## Audit Self-Reference Policy

- `source_head_scope`: `generation_time_repository_head`
- `commit_storing_this_audit_known_at_generation`: `False`
- `expected_post_commit_self_lag`: `True`
- `self_lag_is_formal_gate_blocker`: `False`
- `manifest_path`: `0_trials/module2_source_freshness_audit/source_freshness_audit.json`
- `markdown_path`: `0_trials/module2_source_freshness_audit/source_freshness_audit.md`

## Regeneration Targets

- `f02_6_decision_gate_audit`: `historical_dirty`, source_head=`4e88654613293ffea82c63203b47007c49cb45e9+dirty`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`True`, commit_exists=`True`, commits_since_source=`40`, changed_paths_since_source=`34`, non_self_changed_paths_since_source=`33`, blocking_changed_paths_since_source=`17`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.json`
- `f02_6_decision_intake`: `historical_dirty`, source_head=`1d03fd8b1a091b6e2e4017757ef8d9220fc6e3b9+dirty`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`True`, commit_exists=`True`, commits_since_source=`12`, changed_paths_since_source=`21`, non_self_changed_paths_since_source=`19`, blocking_changed_paths_since_source=`8`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json`
- `f02_6_decision_record`: `historical_clean`, source_head=`181860fa90c7f5f35dfb9bc224ca84c849a60d8a`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`False`, commit_exists=`True`, commits_since_source=`55`, changed_paths_since_source=`64`, non_self_changed_paths_since_source=`63`, blocking_changed_paths_since_source=`24`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json`
- `f02_6_transition_gate_audit`: `historical_dirty`, source_head=`1d03fd8b1a091b6e2e4017757ef8d9220fc6e3b9+dirty`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`True`, commit_exists=`True`, commits_since_source=`12`, changed_paths_since_source=`21`, non_self_changed_paths_since_source=`20`, blocking_changed_paths_since_source=`8`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json`
- `f02_6_warm_start_decision_packet`: `historical_dirty`, source_head=`4e88654613293ffea82c63203b47007c49cb45e9+dirty`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`True`, commit_exists=`True`, commits_since_source=`40`, changed_paths_since_source=`34`, non_self_changed_paths_since_source=`32`, blocking_changed_paths_since_source=`17`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json`
- `formal_gate_closure_checklist`: `historical_clean`, source_head=`0f5d0e63cebbb4df6544aa04918b02a95f4a4cb9`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`False`, commit_exists=`True`, commits_since_source=`45`, changed_paths_since_source=`44`, non_self_changed_paths_since_source=`42`, blocking_changed_paths_since_source=`19`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json`
- `formal_gate_gap_audit`: `historical_clean`, source_head=`0f5d0e63cebbb4df6544aa04918b02a95f4a4cb9`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`False`, commit_exists=`True`, commits_since_source=`45`, changed_paths_since_source=`44`, non_self_changed_paths_since_source=`42`, blocking_changed_paths_since_source=`19`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json`
- `formal_gate_handoff_bundle`: `historical_dirty`, source_head=`fe22dc299174dc75fe47b69a25866a9a7a271a45+dirty`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`True`, commit_exists=`True`, commits_since_source=`1`, changed_paths_since_source=`1`, non_self_changed_paths_since_source=`1`, blocking_changed_paths_since_source=`1`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`False`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json`
- `gpu3070ti_readiness_refresh`: `historical_clean`, source_head=`181860fa90c7f5f35dfb9bc224ca84c849a60d8a`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`False`, commit_exists=`True`, commits_since_source=`55`, changed_paths_since_source=`64`, non_self_changed_paths_since_source=`62`, blocking_changed_paths_since_source=`24`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.json`
- `post_f02_6_plan_audit`: `historical_clean`, source_head=`35ccf9ed2e1fe52cde81c260b031113f15319efa`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`False`, commit_exists=`True`, commits_since_source=`49`, changed_paths_since_source=`50`, non_self_changed_paths_since_source=`48`, blocking_changed_paths_since_source=`20`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
- `post_f02_6_regeneration_plan`: `historical_dirty`, source_head=`1d03fd8b1a091b6e2e4017757ef8d9220fc6e3b9+dirty`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`True`, commit_exists=`True`, commits_since_source=`12`, changed_paths_since_source=`21`, non_self_changed_paths_since_source=`20`, blocking_changed_paths_since_source=`8`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json`
- `remote_formal_execution_packet`: `historical_clean`, source_head=`181860fa90c7f5f35dfb9bc224ca84c849a60d8a`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`False`, commit_exists=`True`, commits_since_source=`55`, changed_paths_since_source=`64`, non_self_changed_paths_since_source=`63`, blocking_changed_paths_since_source=`24`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json`
- `remote_packet_safety_audit`: `historical_clean`, source_head=`35ccf9ed2e1fe52cde81c260b031113f15319efa`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`False`, commit_exists=`True`, commits_since_source=`49`, changed_paths_since_source=`50`, non_self_changed_paths_since_source=`48`, blocking_changed_paths_since_source=`20`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`
- `h01_evaluation_manifest`: `historical_clean`, source_head=`181860fa90c7f5f35dfb9bc224ca84c849a60d8a`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`False`, commit_exists=`True`, commits_since_source=`55`, changed_paths_since_source=`64`, non_self_changed_paths_since_source=`63`, blocking_changed_paths_since_source=`24`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_h01_h02`, path `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`
- `h02_formal_acceptance`: `historical_clean`, source_head=`181860fa90c7f5f35dfb9bc224ca84c849a60d8a`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`False`, commit_exists=`True`, commits_since_source=`55`, changed_paths_since_source=`64`, non_self_changed_paths_since_source=`63`, blocking_changed_paths_since_source=`24`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_h01_h02`, path `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
- `claim_safety`: `historical_dirty`, source_head=`fe22dc299174dc75fe47b69a25866a9a7a271a45+dirty`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`True`, commit_exists=`True`, commits_since_source=`1`, changed_paths_since_source=`1`, non_self_changed_paths_since_source=`1`, blocking_changed_paths_since_source=`1`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`False`, required before `formal_claim_gate`, path `0_trials/module2_claim_safety/module2_claim_safety.json`
- `formal_gate_missing_artifacts`: `historical_clean`, source_head=`0f5d0e63cebbb4df6544aa04918b02a95f4a4cb9`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`False`, commit_exists=`True`, commits_since_source=`45`, changed_paths_since_source=`44`, non_self_changed_paths_since_source=`42`, blocking_changed_paths_since_source=`19`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json`
- `formal_gate_proof_audit`: `historical_clean`, source_head=`181860fa90c7f5f35dfb9bc224ca84c849a60d8a`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`False`, commit_exists=`True`, commits_since_source=`55`, changed_paths_since_source=`64`, non_self_changed_paths_since_source=`63`, blocking_changed_paths_since_source=`24`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json`
- `formal_gate_proof_summary_chain_audit`: `historical_dirty`, source_head=`fe22dc299174dc75fe47b69a25866a9a7a271a45+dirty`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`True`, commit_exists=`True`, commits_since_source=`1`, changed_paths_since_source=`1`, non_self_changed_paths_since_source=`1`, blocking_changed_paths_since_source=`1`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`False`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_proof_summary_chain_audit/formal_gate_proof_summary_chain_audit.json`
- `formal_gate_remaining_deliverables`: `historical_clean`, source_head=`181860fa90c7f5f35dfb9bc224ca84c849a60d8a`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`False`, commit_exists=`True`, commits_since_source=`55`, changed_paths_since_source=`64`, non_self_changed_paths_since_source=`62`, blocking_changed_paths_since_source=`24`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json`
- `formal_gate_status_report`: `historical_dirty`, source_head=`1d03fd8b1a091b6e2e4017757ef8d9220fc6e3b9+dirty`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`True`, commit_exists=`True`, commits_since_source=`12`, changed_paths_since_source=`21`, non_self_changed_paths_since_source=`19`, blocking_changed_paths_since_source=`8`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
- `mainline_formal_gate_state_audit`: `historical_dirty`, source_head=`2feccc86d769b82d2f8f8a01d76131a8cbd8a722+dirty`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`True`, commit_exists=`True`, commits_since_source=`5`, changed_paths_since_source=`5`, non_self_changed_paths_since_source=`4`, blocking_changed_paths_since_source=`4`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_mainline_formal_gate_state_audit/mainline_formal_gate_state_audit.json`
- `paper_readiness`: `historical_dirty`, source_head=`fe22dc299174dc75fe47b69a25866a9a7a271a45+dirty`, current_head=`2a19340105406bae8ad54ba1eac679b95a41580f`, dirty=`True`, commit_exists=`True`, commits_since_source=`1`, changed_paths_since_source=`1`, non_self_changed_paths_since_source=`1`, blocking_changed_paths_since_source=`1`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`False`, required before `formal_claim_gate`, path `0_trials/module2_paper_readiness/module2_paper_readiness.json`

## Artifact Records

- `f02_6_warm_start_decision_packet`: status=`pending_human_decision`, freshness=`historical_dirty`, source_head=`4e88654613293ffea82c63203b47007c49cb45e9+dirty`
- `f02_6_decision_record`: status=`pending_human_decision`, freshness=`historical_clean`, source_head=`181860fa90c7f5f35dfb9bc224ca84c849a60d8a`
- `f02_6_decision_intake`: status=`f02_6_decision_intake_pending_clean`, freshness=`historical_dirty`, source_head=`1d03fd8b1a091b6e2e4017757ef8d9220fc6e3b9+dirty`
- `f02_6_decision_gate_audit`: status=`f02_6_decision_gate_pending_clean`, freshness=`historical_dirty`, source_head=`4e88654613293ffea82c63203b47007c49cb45e9+dirty`
- `f02_6_transition_gate_audit`: status=`f02_6_transition_gate_audit_passed`, freshness=`historical_dirty`, source_head=`1d03fd8b1a091b6e2e4017757ef8d9220fc6e3b9+dirty`
- `remote_formal_execution_packet`: status=`blocked_until_f02_6_decision`, freshness=`historical_clean`, source_head=`181860fa90c7f5f35dfb9bc224ca84c849a60d8a`
- `h01_evaluation_manifest`: status=`blocked_pending_decisions`, freshness=`historical_clean`, source_head=`181860fa90c7f5f35dfb9bc224ca84c849a60d8a`
- `h02_formal_acceptance`: status=`blocked_formal_output_acceptance`, freshness=`historical_clean`, source_head=`181860fa90c7f5f35dfb9bc224ca84c849a60d8a`
- `claim_safety`: status=`blocked_formal_performance_claims`, freshness=`historical_dirty`, source_head=`fe22dc299174dc75fe47b69a25866a9a7a271a45+dirty`
- `paper_readiness`: status=`partial_methods_ready_results_blocked`, freshness=`historical_dirty`, source_head=`fe22dc299174dc75fe47b69a25866a9a7a271a45+dirty`
- `formal_gate_gap_audit`: status=`blocked_formal_gate_gaps_open`, freshness=`historical_clean`, source_head=`0f5d0e63cebbb4df6544aa04918b02a95f4a4cb9`
- `post_f02_6_regeneration_plan`: status=`blocked_until_f02_6_decision`, freshness=`historical_dirty`, source_head=`1d03fd8b1a091b6e2e4017757ef8d9220fc6e3b9+dirty`
- `post_f02_6_plan_audit`: status=`post_f02_6_plan_audit_passed`, freshness=`historical_clean`, source_head=`35ccf9ed2e1fe52cde81c260b031113f15319efa`
- `remote_packet_safety_audit`: status=`remote_packet_safety_audit_passed`, freshness=`historical_clean`, source_head=`35ccf9ed2e1fe52cde81c260b031113f15319efa`
- `formal_gate_closure_checklist`: status=`formal_gate_closure_blocked`, freshness=`historical_clean`, source_head=`0f5d0e63cebbb4df6544aa04918b02a95f4a4cb9`
- `gpu3070ti_readiness_refresh`: status=`remote_readiness_refreshed_f02_6_still_blocked`, freshness=`historical_clean`, source_head=`181860fa90c7f5f35dfb9bc224ca84c849a60d8a`
- `formal_gate_missing_artifacts`: status=`formal_gate_missing_artifacts_open`, freshness=`historical_clean`, source_head=`0f5d0e63cebbb4df6544aa04918b02a95f4a4cb9`
- `formal_gate_status_report`: status=`formal_gate_status_blocked`, freshness=`historical_dirty`, source_head=`1d03fd8b1a091b6e2e4017757ef8d9220fc6e3b9+dirty`
- `formal_gate_remaining_deliverables`: status=`formal_gate_deliverables_blocked`, freshness=`historical_clean`, source_head=`181860fa90c7f5f35dfb9bc224ca84c849a60d8a`
- `formal_gate_proof_audit`: status=`formal_gate_proof_audit_blocked`, freshness=`historical_clean`, source_head=`181860fa90c7f5f35dfb9bc224ca84c849a60d8a`
- `formal_gate_proof_summary_chain_audit`: status=`formal_gate_proof_summary_chain_audit_failed`, freshness=`historical_dirty`, source_head=`fe22dc299174dc75fe47b69a25866a9a7a271a45+dirty`
- `mainline_formal_gate_state_audit`: status=`mainline_formal_gate_state_consistent_blocked`, freshness=`historical_dirty`, source_head=`2feccc86d769b82d2f8f8a01d76131a8cbd8a722+dirty`
- `formal_gate_handoff_bundle`: status=`blocked_until_f02_6_decision`, freshness=`historical_dirty`, source_head=`fe22dc299174dc75fe47b69a25866a9a7a271a45+dirty`

## Claim Boundaries

- This audit records source-head freshness only; it is not a training run or paper result.
- Historical or dirty source_head values are regeneration risks, not formal experimental failures.
- The audit artifact's own post-commit source_head lag is expected and is not a formal gate blocker by itself.
- F02.6 remains the human approval gate before approved remote preflight or formal PPO training.
- Regenerate stale/dirty gate artifacts after F02.6 closes and before H01/H02 formal evaluation or formal claims.
