# Module2 Source Freshness Audit

This file records gate artifact source-head freshness. It is not a training run, remote preflight, paper table, or result claim.

- status: `source_freshness_risks_recorded_gate_still_blocked`
- current_head: `d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`
- runs_training: `False`
- runs_remote_preflight: `False`
- formal_claim_allowed: `False`
- regeneration_required_before_remote_formal_execution: `True`
- blocking_regeneration_required_before_remote_formal_execution: `True`
- blocking_regeneration_target_count: `15`
- self_artifact_only_lag_target_count: `1`
- tracked_artifact_only_lag_target_count: `8`

## Risk Counts

- `historical_clean`: `17`
- `historical_dirty`: `6`

## Commit Lag Diagnostics

- `records_with_commit_lag`: `23`
- `records_with_unknown_commit_lag`: `0`
- `records_with_changed_paths_since_source`: `23`
- `records_with_artifact_path_changed_since_source`: `23`
- `records_with_non_self_changed_paths_since_source`: `22`
- `records_with_blocking_changed_paths_since_source`: `15`
- `records_with_self_artifact_only_lag`: `1`
- `records_with_tracked_artifact_only_lag`: `8`
- `max_commits_since_source`: `870`
- `max_non_self_changed_path_count_since_source`: `222`
- `max_blocking_changed_path_count_since_source`: `177`
- `changed_path_sample_limit`: `12`

## Audit Self-Reference Policy

- `source_head_scope`: `generation_time_repository_head`
- `commit_storing_this_audit_known_at_generation`: `False`
- `expected_post_commit_self_lag`: `True`
- `self_lag_is_formal_gate_blocker`: `False`
- `manifest_path`: `0_trials/module2_source_freshness_audit/source_freshness_audit.json`
- `markdown_path`: `0_trials/module2_source_freshness_audit/source_freshness_audit.md`

## Regeneration Targets

- `f02_6_decision_gate_audit`: `historical_clean`, source_head=`d660065ee07319f803425e6948d91d9bd7901a27`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`False`, commit_exists=`True`, commits_since_source=`69`, changed_paths_since_source=`85`, non_self_changed_paths_since_source=`84`, blocking_changed_paths_since_source=`58`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.json`
- `f02_6_decision_intake`: `historical_dirty`, source_head=`c8c9a0649b7c8487821b0756cbfdc15d736fa937+dirty`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`True`, commit_exists=`True`, commits_since_source=`47`, changed_paths_since_source=`81`, non_self_changed_paths_since_source=`79`, blocking_changed_paths_since_source=`56`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json`
- `f02_6_decision_record`: `historical_clean`, source_head=`457a683d21472b90b590418577db5ae2d069d5b9`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`False`, commit_exists=`True`, commits_since_source=`232`, changed_paths_since_source=`118`, non_self_changed_paths_since_source=`117`, blocking_changed_paths_since_source=`80`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json`
- `f02_6_transition_gate_audit`: `historical_clean`, source_head=`67ac01b069f5bfc4cca16ee7c9e3332065beca93`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`False`, commit_exists=`True`, commits_since_source=`224`, changed_paths_since_source=`117`, non_self_changed_paths_since_source=`115`, blocking_changed_paths_since_source=`79`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json`
- `f02_6_warm_start_decision_packet`: `historical_dirty`, source_head=`d660065ee07319f803425e6948d91d9bd7901a27+dirty`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`True`, commit_exists=`True`, commits_since_source=`69`, changed_paths_since_source=`85`, non_self_changed_paths_since_source=`84`, blocking_changed_paths_since_source=`58`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json`
- `formal_gate_closure_checklist`: `historical_clean`, source_head=`3a901a307d73c8119e1d29dc863b834d47376c68`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`False`, commit_exists=`True`, commits_since_source=`203`, changed_paths_since_source=`113`, non_self_changed_paths_since_source=`112`, blocking_changed_paths_since_source=`79`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json`
- `formal_gate_gap_audit`: `historical_clean`, source_head=`35efd5009d4e8545048cf836c8ecd72d12d04672`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`False`, commit_exists=`True`, commits_since_source=`4`, changed_paths_since_source=`6`, non_self_changed_paths_since_source=`4`, blocking_changed_paths_since_source=`0`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`True`, blocking_regeneration=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json`
- `formal_gate_handoff_bundle`: `historical_clean`, source_head=`2c81a650271875c04a628ef21a367cc878787bb0`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`False`, commit_exists=`True`, commits_since_source=`178`, changed_paths_since_source=`107`, non_self_changed_paths_since_source=`105`, blocking_changed_paths_since_source=`75`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json`
- `gpu3070ti_readiness_refresh`: `historical_clean`, source_head=`033356f27e5255c60d64a78753054b86ef2a0428`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`False`, commit_exists=`True`, commits_since_source=`870`, changed_paths_since_source=`224`, non_self_changed_paths_since_source=`222`, blocking_changed_paths_since_source=`177`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.json`
- `post_f02_6_plan_audit`: `historical_clean`, source_head=`a563869d41c4ead800270de5eaa5bed4ecf87432`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`False`, commit_exists=`True`, commits_since_source=`6`, changed_paths_since_source=`8`, non_self_changed_paths_since_source=`7`, blocking_changed_paths_since_source=`0`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`True`, blocking_regeneration=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
- `post_f02_6_regeneration_plan`: `historical_clean`, source_head=`cd50821ab8cf8ffdd5a7d88a22a315bef10ccfc1`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`False`, commit_exists=`True`, commits_since_source=`7`, changed_paths_since_source=`10`, non_self_changed_paths_since_source=`8`, blocking_changed_paths_since_source=`0`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`True`, blocking_regeneration=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json`
- `remote_formal_execution_packet`: `historical_clean`, source_head=`9ec25e9564e46fbfb7f2363429a5ac187ac61517`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`False`, commit_exists=`True`, commits_since_source=`241`, changed_paths_since_source=`119`, non_self_changed_paths_since_source=`118`, blocking_changed_paths_since_source=`80`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json`
- `remote_packet_safety_audit`: `historical_clean`, source_head=`02694701e4117e8a5880c50decfcd7060fe13a07`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`False`, commit_exists=`True`, commits_since_source=`5`, changed_paths_since_source=`7`, non_self_changed_paths_since_source=`6`, blocking_changed_paths_since_source=`0`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`True`, blocking_regeneration=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`
- `h01_evaluation_manifest`: `historical_clean`, source_head=`92bf7f431a61fbe7e7818b8a58092ab30c64850d`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`False`, commit_exists=`True`, commits_since_source=`220`, changed_paths_since_source=`115`, non_self_changed_paths_since_source=`114`, blocking_changed_paths_since_source=`79`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_h01_h02`, path `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`
- `h02_formal_acceptance`: `historical_clean`, source_head=`136e70a25f8843ace4b0b707881248d4f107682c`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`False`, commit_exists=`True`, commits_since_source=`218`, changed_paths_since_source=`114`, non_self_changed_paths_since_source=`113`, blocking_changed_paths_since_source=`79`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_h01_h02`, path `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
- `claim_safety`: `historical_clean`, source_head=`c3704f32027de19718c688215c32cff374c4aa90`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`False`, commit_exists=`True`, commits_since_source=`2`, changed_paths_since_source=`2`, non_self_changed_paths_since_source=`1`, blocking_changed_paths_since_source=`0`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`True`, blocking_regeneration=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_claim_safety/module2_claim_safety.json`
- `formal_gate_missing_artifacts`: `historical_dirty`, source_head=`37fca35f7d525e6bacfc3c49a7f45aedcd87a89d+dirty`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`True`, commit_exists=`True`, commits_since_source=`101`, changed_paths_since_source=`96`, non_self_changed_paths_since_source=`94`, blocking_changed_paths_since_source=`66`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json`
- `formal_gate_proof_audit`: `historical_dirty`, source_head=`429271d516bc45bb9d823b7092e70c80fd7ab584+dirty`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`True`, commit_exists=`True`, commits_since_source=`13`, changed_paths_since_source=`51`, non_self_changed_paths_since_source=`50`, blocking_changed_paths_since_source=`34`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json`
- `formal_gate_proof_summary_chain_audit`: `historical_dirty`, source_head=`429271d516bc45bb9d823b7092e70c80fd7ab584+dirty`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`True`, commit_exists=`True`, commits_since_source=`13`, changed_paths_since_source=`51`, non_self_changed_paths_since_source=`50`, blocking_changed_paths_since_source=`34`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_proof_summary_chain_audit/formal_gate_proof_summary_chain_audit.json`
- `formal_gate_remaining_deliverables`: `historical_clean`, source_head=`0876902d5fa346cfb1ac1216badd1d41caf4bc54`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`False`, commit_exists=`True`, commits_since_source=`9`, changed_paths_since_source=`14`, non_self_changed_paths_since_source=`12`, blocking_changed_paths_since_source=`0`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`True`, blocking_regeneration=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json`
- `formal_gate_status_report`: `historical_clean`, source_head=`230d20df4d86b4eebcd32db7df5f604688aaa10b`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`False`, commit_exists=`True`, commits_since_source=`3`, changed_paths_since_source=`4`, non_self_changed_paths_since_source=`2`, blocking_changed_paths_since_source=`0`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`True`, blocking_regeneration=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
- `mainline_formal_gate_state_audit`: `historical_dirty`, source_head=`429271d516bc45bb9d823b7092e70c80fd7ab584+dirty`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`True`, commit_exists=`True`, commits_since_source=`13`, changed_paths_since_source=`51`, non_self_changed_paths_since_source=`50`, blocking_changed_paths_since_source=`34`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_mainline_formal_gate_state_audit/mainline_formal_gate_state_audit.json`
- `paper_readiness`: `historical_clean`, source_head=`84657f47735f4457c0c88486b7aebf41926712c4`, current_head=`d0a8c851d3b89dc01c9ace65dde6c3728d1e211f`, dirty=`False`, commit_exists=`True`, commits_since_source=`1`, changed_paths_since_source=`1`, non_self_changed_paths_since_source=`0`, blocking_changed_paths_since_source=`0`, self_artifact_only_lag=`True`, tracked_artifact_only_lag=`True`, blocking_regeneration=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_paper_readiness/module2_paper_readiness.json`

## Artifact Records

- `f02_6_warm_start_decision_packet`: status=`pending_human_decision`, freshness=`historical_dirty`, source_head=`d660065ee07319f803425e6948d91d9bd7901a27+dirty`
- `f02_6_decision_record`: status=`pending_human_decision`, freshness=`historical_clean`, source_head=`457a683d21472b90b590418577db5ae2d069d5b9`
- `f02_6_decision_intake`: status=`f02_6_decision_intake_pending_clean`, freshness=`historical_dirty`, source_head=`c8c9a0649b7c8487821b0756cbfdc15d736fa937+dirty`
- `f02_6_decision_gate_audit`: status=`f02_6_decision_gate_pending_clean`, freshness=`historical_clean`, source_head=`d660065ee07319f803425e6948d91d9bd7901a27`
- `f02_6_transition_gate_audit`: status=`f02_6_transition_gate_audit_passed`, freshness=`historical_clean`, source_head=`67ac01b069f5bfc4cca16ee7c9e3332065beca93`
- `remote_formal_execution_packet`: status=`blocked_until_f02_6_decision`, freshness=`historical_clean`, source_head=`9ec25e9564e46fbfb7f2363429a5ac187ac61517`
- `h01_evaluation_manifest`: status=`blocked_pending_decisions`, freshness=`historical_clean`, source_head=`92bf7f431a61fbe7e7818b8a58092ab30c64850d`
- `h02_formal_acceptance`: status=`blocked_formal_output_acceptance`, freshness=`historical_clean`, source_head=`136e70a25f8843ace4b0b707881248d4f107682c`
- `claim_safety`: status=`blocked_formal_performance_claims`, freshness=`historical_clean`, source_head=`c3704f32027de19718c688215c32cff374c4aa90`
- `paper_readiness`: status=`partial_methods_ready_results_blocked`, freshness=`historical_clean`, source_head=`84657f47735f4457c0c88486b7aebf41926712c4`
- `formal_gate_gap_audit`: status=`blocked_formal_gate_gaps_open`, freshness=`historical_clean`, source_head=`35efd5009d4e8545048cf836c8ecd72d12d04672`
- `post_f02_6_regeneration_plan`: status=`blocked_until_f02_6_decision`, freshness=`historical_clean`, source_head=`cd50821ab8cf8ffdd5a7d88a22a315bef10ccfc1`
- `post_f02_6_plan_audit`: status=`post_f02_6_plan_audit_passed`, freshness=`historical_clean`, source_head=`a563869d41c4ead800270de5eaa5bed4ecf87432`
- `remote_packet_safety_audit`: status=`remote_packet_safety_audit_passed`, freshness=`historical_clean`, source_head=`02694701e4117e8a5880c50decfcd7060fe13a07`
- `formal_gate_closure_checklist`: status=`formal_gate_closure_blocked`, freshness=`historical_clean`, source_head=`3a901a307d73c8119e1d29dc863b834d47376c68`
- `gpu3070ti_readiness_refresh`: status=`remote_readiness_refreshed_f02_6_still_blocked`, freshness=`historical_clean`, source_head=`033356f27e5255c60d64a78753054b86ef2a0428`
- `formal_gate_missing_artifacts`: status=`formal_gate_missing_artifacts_open`, freshness=`historical_dirty`, source_head=`37fca35f7d525e6bacfc3c49a7f45aedcd87a89d+dirty`
- `formal_gate_status_report`: status=`formal_gate_status_blocked`, freshness=`historical_clean`, source_head=`230d20df4d86b4eebcd32db7df5f604688aaa10b`
- `formal_gate_remaining_deliverables`: status=`formal_gate_deliverables_blocked`, freshness=`historical_clean`, source_head=`0876902d5fa346cfb1ac1216badd1d41caf4bc54`
- `formal_gate_proof_audit`: status=`formal_gate_proof_audit_blocked`, freshness=`historical_dirty`, source_head=`429271d516bc45bb9d823b7092e70c80fd7ab584+dirty`
- `formal_gate_proof_summary_chain_audit`: status=`formal_gate_proof_summary_chain_consistent_blocked`, freshness=`historical_dirty`, source_head=`429271d516bc45bb9d823b7092e70c80fd7ab584+dirty`
- `mainline_formal_gate_state_audit`: status=`mainline_formal_gate_state_consistent_blocked`, freshness=`historical_dirty`, source_head=`429271d516bc45bb9d823b7092e70c80fd7ab584+dirty`
- `formal_gate_handoff_bundle`: status=`blocked_until_f02_6_decision`, freshness=`historical_clean`, source_head=`2c81a650271875c04a628ef21a367cc878787bb0`

## Claim Boundaries

- This audit records source-head freshness only; it is not a training run or paper result.
- Historical or dirty source_head values are regeneration risks, not formal experimental failures.
- The audit artifact's own post-commit source_head lag is expected and is not a formal gate blocker by itself.
- F02.6 remains the human approval gate before approved remote preflight or formal PPO training.
- Regenerate stale/dirty gate artifacts after F02.6 closes and before H01/H02 formal evaluation or formal claims.
