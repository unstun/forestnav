# Module2 Source Freshness Audit

This file records gate artifact source-head freshness. It is not a training run, remote preflight, paper table, or result claim.

- status: `source_freshness_risks_recorded_gate_still_blocked`
- current_head: `38eb2dfc8c590156ef32714f59e0a737b1785be3`
- runs_training: `False`
- runs_remote_preflight: `False`
- formal_claim_allowed: `False`
- regeneration_required_before_remote_formal_execution: `True`
- blocking_regeneration_required_before_remote_formal_execution: `True`
- blocking_regeneration_target_count: `18`
- self_artifact_only_lag_target_count: `0`
- tracked_artifact_only_lag_target_count: `5`

## Risk Counts

- `historical_clean`: `21`
- `historical_dirty`: `2`

## Commit Lag Diagnostics

- `records_with_commit_lag`: `23`
- `records_with_unknown_commit_lag`: `0`
- `records_with_changed_paths_since_source`: `23`
- `records_with_artifact_path_changed_since_source`: `23`
- `records_with_non_self_changed_paths_since_source`: `23`
- `records_with_blocking_changed_paths_since_source`: `18`
- `records_with_self_artifact_only_lag`: `0`
- `records_with_tracked_artifact_only_lag`: `5`
- `max_commits_since_source`: `901`
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

- `f02_6_decision_gate_audit`: `historical_clean`, source_head=`d660065ee07319f803425e6948d91d9bd7901a27`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`False`, commit_exists=`True`, commits_since_source=`100`, changed_paths_since_source=`88`, non_self_changed_paths_since_source=`87`, blocking_changed_paths_since_source=`59`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.json`
- `f02_6_decision_intake`: `historical_clean`, source_head=`0935d403a6d0f37c91925cc3222d113202c2ca6c`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`False`, commit_exists=`True`, commits_since_source=`25`, changed_paths_since_source=`24`, non_self_changed_paths_since_source=`23`, blocking_changed_paths_since_source=`8`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json`
- `f02_6_decision_record`: `historical_clean`, source_head=`457a683d21472b90b590418577db5ae2d069d5b9`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`False`, commit_exists=`True`, commits_since_source=`263`, changed_paths_since_source=`118`, non_self_changed_paths_since_source=`117`, blocking_changed_paths_since_source=`80`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json`
- `f02_6_transition_gate_audit`: `historical_clean`, source_head=`67ac01b069f5bfc4cca16ee7c9e3332065beca93`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`False`, commit_exists=`True`, commits_since_source=`255`, changed_paths_since_source=`117`, non_self_changed_paths_since_source=`115`, blocking_changed_paths_since_source=`79`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json`
- `f02_6_warm_start_decision_packet`: `historical_dirty`, source_head=`d660065ee07319f803425e6948d91d9bd7901a27+dirty`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`True`, commit_exists=`True`, commits_since_source=`100`, changed_paths_since_source=`88`, non_self_changed_paths_since_source=`87`, blocking_changed_paths_since_source=`59`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json`
- `formal_gate_closure_checklist`: `historical_clean`, source_head=`3a901a307d73c8119e1d29dc863b834d47376c68`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`False`, commit_exists=`True`, commits_since_source=`234`, changed_paths_since_source=`113`, non_self_changed_paths_since_source=`112`, blocking_changed_paths_since_source=`79`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json`
- `formal_gate_gap_audit`: `historical_clean`, source_head=`9928985465ec8f3a4e8601185988fc7aae2d8c32`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`False`, commit_exists=`True`, commits_since_source=`2`, changed_paths_since_source=`5`, non_self_changed_paths_since_source=`3`, blocking_changed_paths_since_source=`0`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`True`, blocking_regeneration=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json`
- `formal_gate_handoff_bundle`: `historical_clean`, source_head=`e6a35d1b1d62e0089c447b53fccc558bbe846216`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`False`, commit_exists=`True`, commits_since_source=`3`, changed_paths_since_source=`7`, non_self_changed_paths_since_source=`5`, blocking_changed_paths_since_source=`0`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`True`, blocking_regeneration=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json`
- `gpu3070ti_readiness_refresh`: `historical_clean`, source_head=`033356f27e5255c60d64a78753054b86ef2a0428`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`False`, commit_exists=`True`, commits_since_source=`901`, changed_paths_since_source=`224`, non_self_changed_paths_since_source=`222`, blocking_changed_paths_since_source=`177`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.json`
- `post_f02_6_plan_audit`: `historical_clean`, source_head=`52259b91424d11c535d7cdf8fe3053359a675baf`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`False`, commit_exists=`True`, commits_since_source=`30`, changed_paths_since_source=`30`, non_self_changed_paths_since_source=`29`, blocking_changed_paths_since_source=`10`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
- `post_f02_6_regeneration_plan`: `historical_clean`, source_head=`52259b91424d11c535d7cdf8fe3053359a675baf`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`False`, commit_exists=`True`, commits_since_source=`30`, changed_paths_since_source=`30`, non_self_changed_paths_since_source=`29`, blocking_changed_paths_since_source=`10`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json`
- `remote_formal_execution_packet`: `historical_clean`, source_head=`9ec25e9564e46fbfb7f2363429a5ac187ac61517`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`False`, commit_exists=`True`, commits_since_source=`272`, changed_paths_since_source=`119`, non_self_changed_paths_since_source=`118`, blocking_changed_paths_since_source=`80`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json`
- `remote_packet_safety_audit`: `historical_clean`, source_head=`674ba1cdf00819826003f2340beb81e74a91863e`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`False`, commit_exists=`True`, commits_since_source=`29`, changed_paths_since_source=`28`, non_self_changed_paths_since_source=`27`, blocking_changed_paths_since_source=`10`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`
- `h01_evaluation_manifest`: `historical_clean`, source_head=`92bf7f431a61fbe7e7818b8a58092ab30c64850d`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`False`, commit_exists=`True`, commits_since_source=`251`, changed_paths_since_source=`115`, non_self_changed_paths_since_source=`114`, blocking_changed_paths_since_source=`79`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_h01_h02`, path `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`
- `h02_formal_acceptance`: `historical_clean`, source_head=`136e70a25f8843ace4b0b707881248d4f107682c`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`False`, commit_exists=`True`, commits_since_source=`249`, changed_paths_since_source=`114`, non_self_changed_paths_since_source=`113`, blocking_changed_paths_since_source=`79`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_h01_h02`, path `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
- `claim_safety`: `historical_clean`, source_head=`db3c7aa23b7bc4a27836397902543bc1cca8312d`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`False`, commit_exists=`True`, commits_since_source=`6`, changed_paths_since_source=`13`, non_self_changed_paths_since_source=`12`, blocking_changed_paths_since_source=`2`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_claim_safety/module2_claim_safety.json`
- `formal_gate_missing_artifacts`: `historical_dirty`, source_head=`37fca35f7d525e6bacfc3c49a7f45aedcd87a89d+dirty`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`True`, commit_exists=`True`, commits_since_source=`132`, changed_paths_since_source=`99`, non_self_changed_paths_since_source=`97`, blocking_changed_paths_since_source=`67`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json`
- `formal_gate_proof_audit`: `historical_clean`, source_head=`7c389151ad8fbb7d6dd0212f33fb9910c1629ca3`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`False`, commit_exists=`True`, commits_since_source=`1`, changed_paths_since_source=`3`, non_self_changed_paths_since_source=`2`, blocking_changed_paths_since_source=`0`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`True`, blocking_regeneration=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json`
- `formal_gate_proof_summary_chain_audit`: `historical_clean`, source_head=`7c389151ad8fbb7d6dd0212f33fb9910c1629ca3`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`False`, commit_exists=`True`, commits_since_source=`1`, changed_paths_since_source=`3`, non_self_changed_paths_since_source=`2`, blocking_changed_paths_since_source=`0`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`True`, blocking_regeneration=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_proof_summary_chain_audit/formal_gate_proof_summary_chain_audit.json`
- `formal_gate_remaining_deliverables`: `historical_clean`, source_head=`0876902d5fa346cfb1ac1216badd1d41caf4bc54`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`False`, commit_exists=`True`, commits_since_source=`40`, changed_paths_since_source=`33`, non_self_changed_paths_since_source=`31`, blocking_changed_paths_since_source=`10`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json`
- `formal_gate_status_report`: `historical_clean`, source_head=`db3c7aa23b7bc4a27836397902543bc1cca8312d`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`False`, commit_exists=`True`, commits_since_source=`6`, changed_paths_since_source=`13`, non_self_changed_paths_since_source=`11`, blocking_changed_paths_since_source=`2`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
- `mainline_formal_gate_state_audit`: `historical_clean`, source_head=`7c389151ad8fbb7d6dd0212f33fb9910c1629ca3`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`False`, commit_exists=`True`, commits_since_source=`1`, changed_paths_since_source=`3`, non_self_changed_paths_since_source=`2`, blocking_changed_paths_since_source=`0`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`True`, blocking_regeneration=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_mainline_formal_gate_state_audit/mainline_formal_gate_state_audit.json`
- `paper_readiness`: `historical_clean`, source_head=`db3c7aa23b7bc4a27836397902543bc1cca8312d`, current_head=`38eb2dfc8c590156ef32714f59e0a737b1785be3`, dirty=`False`, commit_exists=`True`, commits_since_source=`6`, changed_paths_since_source=`13`, non_self_changed_paths_since_source=`12`, blocking_changed_paths_since_source=`2`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_paper_readiness/module2_paper_readiness.json`

## Artifact Records

- `f02_6_warm_start_decision_packet`: status=`pending_human_decision`, freshness=`historical_dirty`, source_head=`d660065ee07319f803425e6948d91d9bd7901a27+dirty`
- `f02_6_decision_record`: status=`pending_human_decision`, freshness=`historical_clean`, source_head=`457a683d21472b90b590418577db5ae2d069d5b9`
- `f02_6_decision_intake`: status=`f02_6_decision_intake_pending_clean`, freshness=`historical_clean`, source_head=`0935d403a6d0f37c91925cc3222d113202c2ca6c`
- `f02_6_decision_gate_audit`: status=`f02_6_decision_gate_pending_clean`, freshness=`historical_clean`, source_head=`d660065ee07319f803425e6948d91d9bd7901a27`
- `f02_6_transition_gate_audit`: status=`f02_6_transition_gate_audit_passed`, freshness=`historical_clean`, source_head=`67ac01b069f5bfc4cca16ee7c9e3332065beca93`
- `remote_formal_execution_packet`: status=`blocked_until_f02_6_decision`, freshness=`historical_clean`, source_head=`9ec25e9564e46fbfb7f2363429a5ac187ac61517`
- `h01_evaluation_manifest`: status=`blocked_pending_decisions`, freshness=`historical_clean`, source_head=`92bf7f431a61fbe7e7818b8a58092ab30c64850d`
- `h02_formal_acceptance`: status=`blocked_formal_output_acceptance`, freshness=`historical_clean`, source_head=`136e70a25f8843ace4b0b707881248d4f107682c`
- `claim_safety`: status=`blocked_formal_performance_claims`, freshness=`historical_clean`, source_head=`db3c7aa23b7bc4a27836397902543bc1cca8312d`
- `paper_readiness`: status=`partial_methods_ready_results_blocked`, freshness=`historical_clean`, source_head=`db3c7aa23b7bc4a27836397902543bc1cca8312d`
- `formal_gate_gap_audit`: status=`blocked_formal_gate_gaps_open`, freshness=`historical_clean`, source_head=`9928985465ec8f3a4e8601185988fc7aae2d8c32`
- `post_f02_6_regeneration_plan`: status=`blocked_until_f02_6_decision`, freshness=`historical_clean`, source_head=`52259b91424d11c535d7cdf8fe3053359a675baf`
- `post_f02_6_plan_audit`: status=`post_f02_6_plan_audit_passed`, freshness=`historical_clean`, source_head=`52259b91424d11c535d7cdf8fe3053359a675baf`
- `remote_packet_safety_audit`: status=`remote_packet_safety_audit_passed`, freshness=`historical_clean`, source_head=`674ba1cdf00819826003f2340beb81e74a91863e`
- `formal_gate_closure_checklist`: status=`formal_gate_closure_blocked`, freshness=`historical_clean`, source_head=`3a901a307d73c8119e1d29dc863b834d47376c68`
- `gpu3070ti_readiness_refresh`: status=`remote_readiness_refreshed_f02_6_still_blocked`, freshness=`historical_clean`, source_head=`033356f27e5255c60d64a78753054b86ef2a0428`
- `formal_gate_missing_artifacts`: status=`formal_gate_missing_artifacts_open`, freshness=`historical_dirty`, source_head=`37fca35f7d525e6bacfc3c49a7f45aedcd87a89d+dirty`
- `formal_gate_status_report`: status=`formal_gate_status_blocked`, freshness=`historical_clean`, source_head=`db3c7aa23b7bc4a27836397902543bc1cca8312d`
- `formal_gate_remaining_deliverables`: status=`formal_gate_deliverables_blocked`, freshness=`historical_clean`, source_head=`0876902d5fa346cfb1ac1216badd1d41caf4bc54`
- `formal_gate_proof_audit`: status=`formal_gate_proof_audit_blocked`, freshness=`historical_clean`, source_head=`7c389151ad8fbb7d6dd0212f33fb9910c1629ca3`
- `formal_gate_proof_summary_chain_audit`: status=`formal_gate_proof_summary_chain_consistent_blocked`, freshness=`historical_clean`, source_head=`7c389151ad8fbb7d6dd0212f33fb9910c1629ca3`
- `mainline_formal_gate_state_audit`: status=`mainline_formal_gate_state_consistent_blocked`, freshness=`historical_clean`, source_head=`7c389151ad8fbb7d6dd0212f33fb9910c1629ca3`
- `formal_gate_handoff_bundle`: status=`blocked_until_f02_6_decision`, freshness=`historical_clean`, source_head=`e6a35d1b1d62e0089c447b53fccc558bbe846216`

## Claim Boundaries

- This audit records source-head freshness only; it is not a training run or paper result.
- Historical or dirty source_head values are regeneration risks, not formal experimental failures.
- The audit artifact's own post-commit source_head lag is expected and is not a formal gate blocker by itself.
- F02.6 remains the human approval gate before approved remote preflight or formal PPO training.
- Regenerate stale/dirty gate artifacts after F02.6 closes and before H01/H02 formal evaluation or formal claims.
