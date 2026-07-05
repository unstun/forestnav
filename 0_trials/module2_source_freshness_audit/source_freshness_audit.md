# Module2 Source Freshness Audit

This file records gate artifact source-head freshness. It is not a training run, remote preflight, paper table, or result claim.

- status: `source_freshness_risks_recorded_gate_still_blocked`
- current_head: `e5ba1501cecf92a9901fe718128019b0836f7302`
- runs_training: `False`
- runs_remote_preflight: `False`
- formal_claim_allowed: `False`
- regeneration_required_before_remote_formal_execution: `True`
- blocking_regeneration_required_before_remote_formal_execution: `True`
- blocking_regeneration_target_count: `21`
- self_artifact_only_lag_target_count: `0`
- tracked_artifact_only_lag_target_count: `0`

## Risk Counts

- `current_clean`: `2`
- `historical_clean`: `21`

## Commit Lag Diagnostics

- `records_with_commit_lag`: `21`
- `records_with_unknown_commit_lag`: `0`
- `records_with_changed_paths_since_source`: `21`
- `records_with_artifact_path_changed_since_source`: `21`
- `records_with_non_self_changed_paths_since_source`: `21`
- `records_with_blocking_changed_paths_since_source`: `21`
- `records_with_self_artifact_only_lag`: `0`
- `records_with_tracked_artifact_only_lag`: `0`
- `max_commits_since_source`: `7`
- `max_non_self_changed_path_count_since_source`: `40`
- `max_blocking_changed_path_count_since_source`: `5`
- `changed_path_sample_limit`: `12`

## Audit Self-Reference Policy

- `source_head_scope`: `generation_time_repository_head`
- `commit_storing_this_audit_known_at_generation`: `False`
- `expected_post_commit_self_lag`: `True`
- `self_lag_is_formal_gate_blocker`: `False`
- `manifest_path`: `0_trials/module2_source_freshness_audit/source_freshness_audit.json`
- `markdown_path`: `0_trials/module2_source_freshness_audit/source_freshness_audit.md`

## Regeneration Targets

- `f02_6_decision_gate_audit`: `historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`, current_head=`e5ba1501cecf92a9901fe718128019b0836f7302`, dirty=`False`, commit_exists=`True`, commits_since_source=`7`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`40`, blocking_changed_paths_since_source=`5`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.json`
- `f02_6_decision_intake`: `historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`, current_head=`e5ba1501cecf92a9901fe718128019b0836f7302`, dirty=`False`, commit_exists=`True`, commits_since_source=`7`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`39`, blocking_changed_paths_since_source=`5`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json`
- `f02_6_transition_gate_audit`: `historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`, current_head=`e5ba1501cecf92a9901fe718128019b0836f7302`, dirty=`False`, commit_exists=`True`, commits_since_source=`7`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`40`, blocking_changed_paths_since_source=`5`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json`
- `f02_6_warm_start_decision_packet`: `historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`, current_head=`e5ba1501cecf92a9901fe718128019b0836f7302`, dirty=`False`, commit_exists=`True`, commits_since_source=`7`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`40`, blocking_changed_paths_since_source=`5`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json`
- `formal_gate_closure_checklist`: `historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`, current_head=`e5ba1501cecf92a9901fe718128019b0836f7302`, dirty=`False`, commit_exists=`True`, commits_since_source=`7`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`39`, blocking_changed_paths_since_source=`5`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json`
- `formal_gate_gap_audit`: `historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`, current_head=`e5ba1501cecf92a9901fe718128019b0836f7302`, dirty=`False`, commit_exists=`True`, commits_since_source=`7`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`39`, blocking_changed_paths_since_source=`5`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json`
- `formal_gate_handoff_bundle`: `historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`, current_head=`e5ba1501cecf92a9901fe718128019b0836f7302`, dirty=`False`, commit_exists=`True`, commits_since_source=`7`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`39`, blocking_changed_paths_since_source=`5`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json`
- `post_f02_6_plan_audit`: `historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`, current_head=`e5ba1501cecf92a9901fe718128019b0836f7302`, dirty=`False`, commit_exists=`True`, commits_since_source=`7`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`39`, blocking_changed_paths_since_source=`5`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
- `post_f02_6_regeneration_plan`: `historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`, current_head=`e5ba1501cecf92a9901fe718128019b0836f7302`, dirty=`False`, commit_exists=`True`, commits_since_source=`7`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`40`, blocking_changed_paths_since_source=`5`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json`
- `remote_formal_execution_packet`: `historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`, current_head=`e5ba1501cecf92a9901fe718128019b0836f7302`, dirty=`False`, commit_exists=`True`, commits_since_source=`7`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`40`, blocking_changed_paths_since_source=`5`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json`
- `remote_packet_safety_audit`: `historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`, current_head=`e5ba1501cecf92a9901fe718128019b0836f7302`, dirty=`False`, commit_exists=`True`, commits_since_source=`7`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`39`, blocking_changed_paths_since_source=`5`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`
- `h01_evaluation_manifest`: `historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`, current_head=`e5ba1501cecf92a9901fe718128019b0836f7302`, dirty=`False`, commit_exists=`True`, commits_since_source=`7`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`40`, blocking_changed_paths_since_source=`5`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_h01_h02`, path `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`
- `h02_formal_acceptance`: `historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`, current_head=`e5ba1501cecf92a9901fe718128019b0836f7302`, dirty=`False`, commit_exists=`True`, commits_since_source=`7`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`39`, blocking_changed_paths_since_source=`5`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_h01_h02`, path `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
- `claim_safety`: `historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`, current_head=`e5ba1501cecf92a9901fe718128019b0836f7302`, dirty=`False`, commit_exists=`True`, commits_since_source=`7`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`39`, blocking_changed_paths_since_source=`5`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_claim_safety/module2_claim_safety.json`
- `formal_gate_missing_artifacts`: `historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`, current_head=`e5ba1501cecf92a9901fe718128019b0836f7302`, dirty=`False`, commit_exists=`True`, commits_since_source=`7`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`39`, blocking_changed_paths_since_source=`5`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json`
- `formal_gate_proof_audit`: `historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`, current_head=`e5ba1501cecf92a9901fe718128019b0836f7302`, dirty=`False`, commit_exists=`True`, commits_since_source=`7`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`40`, blocking_changed_paths_since_source=`5`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json`
- `formal_gate_proof_summary_chain_audit`: `historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`, current_head=`e5ba1501cecf92a9901fe718128019b0836f7302`, dirty=`False`, commit_exists=`True`, commits_since_source=`7`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`39`, blocking_changed_paths_since_source=`5`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_proof_summary_chain_audit/formal_gate_proof_summary_chain_audit.json`
- `formal_gate_remaining_deliverables`: `historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`, current_head=`e5ba1501cecf92a9901fe718128019b0836f7302`, dirty=`False`, commit_exists=`True`, commits_since_source=`7`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`39`, blocking_changed_paths_since_source=`5`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json`
- `formal_gate_status_report`: `historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`, current_head=`e5ba1501cecf92a9901fe718128019b0836f7302`, dirty=`False`, commit_exists=`True`, commits_since_source=`7`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`39`, blocking_changed_paths_since_source=`5`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
- `mainline_formal_gate_state_audit`: `historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`, current_head=`e5ba1501cecf92a9901fe718128019b0836f7302`, dirty=`False`, commit_exists=`True`, commits_since_source=`7`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`40`, blocking_changed_paths_since_source=`5`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_mainline_formal_gate_state_audit/mainline_formal_gate_state_audit.json`
- `paper_readiness`: `historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`, current_head=`e5ba1501cecf92a9901fe718128019b0836f7302`, dirty=`False`, commit_exists=`True`, commits_since_source=`7`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`39`, blocking_changed_paths_since_source=`5`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_paper_readiness/module2_paper_readiness.json`

## Artifact Records

- `f02_6_warm_start_decision_packet`: status=`pending_human_decision`, freshness=`historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`
- `f02_6_decision_record`: status=`approved`, freshness=`current_clean`, source_head=`e5ba1501cecf92a9901fe718128019b0836f7302`
- `f02_6_decision_intake`: status=`f02_6_decision_intake_closed_clean`, freshness=`historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`
- `f02_6_decision_gate_audit`: status=`f02_6_decision_gate_audit_passed`, freshness=`historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`
- `f02_6_transition_gate_audit`: status=`f02_6_transition_gate_audit_failed`, freshness=`historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`
- `remote_formal_execution_packet`: status=`blocked_remote_preflight_not_ready`, freshness=`historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`
- `h01_evaluation_manifest`: status=`blocked_protocol_gap`, freshness=`historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`
- `h02_formal_acceptance`: status=`blocked_formal_output_acceptance`, freshness=`historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`
- `claim_safety`: status=`blocked_formal_performance_claims`, freshness=`historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`
- `paper_readiness`: status=`partial_methods_ready_results_blocked`, freshness=`historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`
- `formal_gate_gap_audit`: status=`blocked_formal_gate_gaps_open`, freshness=`historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`
- `post_f02_6_regeneration_plan`: status=`blocked_formal_gate_preconditions`, freshness=`historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`
- `post_f02_6_plan_audit`: status=`post_f02_6_plan_audit_failed`, freshness=`historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`
- `remote_packet_safety_audit`: status=`remote_packet_safety_audit_failed`, freshness=`historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`
- `formal_gate_closure_checklist`: status=`formal_gate_closure_blocked`, freshness=`historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`
- `gpu3070ti_readiness_refresh`: status=`remote_readiness_refreshed_f02_6_still_blocked`, freshness=`current_clean`, source_head=`e5ba1501cecf92a9901fe718128019b0836f7302`
- `formal_gate_missing_artifacts`: status=`formal_gate_missing_artifacts_open`, freshness=`historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`
- `formal_gate_status_report`: status=`formal_gate_status_blocked`, freshness=`historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`
- `formal_gate_remaining_deliverables`: status=`formal_gate_deliverables_blocked`, freshness=`historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`
- `formal_gate_proof_audit`: status=`formal_gate_proof_audit_blocked`, freshness=`historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`
- `formal_gate_proof_summary_chain_audit`: status=`formal_gate_proof_summary_chain_audit_failed`, freshness=`historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`
- `mainline_formal_gate_state_audit`: status=`mainline_formal_gate_state_audit_failed`, freshness=`historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`
- `formal_gate_handoff_bundle`: status=`blocked_handoff_input_safety_issues`, freshness=`historical_clean`, source_head=`8ef61f3b4657309273fabf649e950ab7752d9e51`

## Claim Boundaries

- This audit records source-head freshness only; it is not a training run or paper result.
- Historical or dirty source_head values are regeneration risks, not formal experimental failures.
- The audit artifact's own post-commit source_head lag is expected and is not a formal gate blocker by itself.
- F02.6 remains the human approval gate before approved remote preflight or formal PPO training.
- Regenerate stale/dirty gate artifacts after F02.6 closes and before H01/H02 formal evaluation or formal claims.
