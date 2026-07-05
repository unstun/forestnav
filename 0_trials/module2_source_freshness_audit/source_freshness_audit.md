# Module2 Source Freshness Audit

This file records gate artifact source-head freshness. It is not a training run, remote preflight, paper table, or result claim.

- status: `source_freshness_risks_recorded_gate_still_blocked`
- current_head: `c96e29f0fc8cbf3d2e51713cc18adffe222853ae`
- runs_training: `False`
- runs_remote_preflight: `False`
- formal_claim_allowed: `False`
- regeneration_required_before_remote_formal_execution: `True`

## Risk Counts

- `historical_clean`: `18`
- `historical_dirty`: `1`

## Commit Lag Diagnostics

- `records_with_commit_lag`: `19`
- `records_with_unknown_commit_lag`: `0`
- `records_with_changed_paths_since_source`: `19`
- `records_with_artifact_path_changed_since_source`: `19`
- `records_with_non_self_changed_paths_since_source`: `18`
- `records_with_self_artifact_only_lag`: `1`
- `max_commits_since_source`: `742`
- `max_non_self_changed_path_count_since_source`: `179`
- `changed_path_sample_limit`: `12`

## Audit Self-Reference Policy

- `source_head_scope`: `generation_time_repository_head`
- `commit_storing_this_audit_known_at_generation`: `False`
- `expected_post_commit_self_lag`: `True`
- `self_lag_is_formal_gate_blocker`: `False`
- `manifest_path`: `0_trials/module2_source_freshness_audit/source_freshness_audit.json`
- `markdown_path`: `0_trials/module2_source_freshness_audit/source_freshness_audit.md`

## Regeneration Targets

- `f02_6_decision_gate_audit`: `historical_clean`, source_head=`0349d3fd560940fff35b959d7ba89314e9e493a1`, current_head=`c96e29f0fc8cbf3d2e51713cc18adffe222853ae`, dirty=`False`, commit_exists=`True`, commits_since_source=`102`, changed_paths_since_source=`58`, non_self_changed_paths_since_source=`57`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.json`
- `f02_6_decision_intake`: `historical_clean`, source_head=`d85b7bcfe03b2794f5babc3e0f0bcd07b7a80309`, current_head=`c96e29f0fc8cbf3d2e51713cc18adffe222853ae`, dirty=`False`, commit_exists=`True`, commits_since_source=`101`, changed_paths_since_source=`57`, non_self_changed_paths_since_source=`56`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json`
- `f02_6_decision_record`: `historical_clean`, source_head=`457a683d21472b90b590418577db5ae2d069d5b9`, current_head=`c96e29f0fc8cbf3d2e51713cc18adffe222853ae`, dirty=`False`, commit_exists=`True`, commits_since_source=`104`, changed_paths_since_source=`60`, non_self_changed_paths_since_source=`59`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json`
- `f02_6_transition_gate_audit`: `historical_clean`, source_head=`67ac01b069f5bfc4cca16ee7c9e3332065beca93`, current_head=`c96e29f0fc8cbf3d2e51713cc18adffe222853ae`, dirty=`False`, commit_exists=`True`, commits_since_source=`96`, changed_paths_since_source=`55`, non_self_changed_paths_since_source=`53`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json`
- `formal_gate_closure_checklist`: `historical_clean`, source_head=`3a901a307d73c8119e1d29dc863b834d47376c68`, current_head=`c96e29f0fc8cbf3d2e51713cc18adffe222853ae`, dirty=`False`, commit_exists=`True`, commits_since_source=`75`, changed_paths_since_source=`50`, non_self_changed_paths_since_source=`49`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json`
- `formal_gate_gap_audit`: `historical_clean`, source_head=`555e1ad3e6c3e2fa9c8c0ba3b505e32b2847a103`, current_head=`c96e29f0fc8cbf3d2e51713cc18adffe222853ae`, dirty=`False`, commit_exists=`True`, commits_since_source=`35`, changed_paths_since_source=`21`, non_self_changed_paths_since_source=`19`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json`
- `formal_gate_handoff_bundle`: `historical_clean`, source_head=`2c81a650271875c04a628ef21a367cc878787bb0`, current_head=`c96e29f0fc8cbf3d2e51713cc18adffe222853ae`, dirty=`False`, commit_exists=`True`, commits_since_source=`50`, changed_paths_since_source=`36`, non_self_changed_paths_since_source=`34`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json`
- `gpu3070ti_readiness_refresh`: `historical_clean`, source_head=`033356f27e5255c60d64a78753054b86ef2a0428`, current_head=`c96e29f0fc8cbf3d2e51713cc18adffe222853ae`, dirty=`False`, commit_exists=`True`, commits_since_source=`742`, changed_paths_since_source=`181`, non_self_changed_paths_since_source=`179`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.json`
- `post_f02_6_plan_audit`: `historical_clean`, source_head=`ea458d44d9cf4a77d88e1765673f3a2acc20056c`, current_head=`c96e29f0fc8cbf3d2e51713cc18adffe222853ae`, dirty=`False`, commit_exists=`True`, commits_since_source=`45`, changed_paths_since_source=`31`, non_self_changed_paths_since_source=`29`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
- `remote_formal_execution_packet`: `historical_clean`, source_head=`9ec25e9564e46fbfb7f2363429a5ac187ac61517`, current_head=`c96e29f0fc8cbf3d2e51713cc18adffe222853ae`, dirty=`False`, commit_exists=`True`, commits_since_source=`113`, changed_paths_since_source=`61`, non_self_changed_paths_since_source=`60`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json`
- `remote_packet_safety_audit`: `historical_clean`, source_head=`53e3bbf6b8afef8ee779d568bac05b9ad1308ab5`, current_head=`c96e29f0fc8cbf3d2e51713cc18adffe222853ae`, dirty=`False`, commit_exists=`True`, commits_since_source=`40`, changed_paths_since_source=`26`, non_self_changed_paths_since_source=`24`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`
- `h01_evaluation_manifest`: `historical_clean`, source_head=`92bf7f431a61fbe7e7818b8a58092ab30c64850d`, current_head=`c96e29f0fc8cbf3d2e51713cc18adffe222853ae`, dirty=`False`, commit_exists=`True`, commits_since_source=`92`, changed_paths_since_source=`53`, non_self_changed_paths_since_source=`52`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `formal_h01_h02`, path `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`
- `h02_formal_acceptance`: `historical_clean`, source_head=`136e70a25f8843ace4b0b707881248d4f107682c`, current_head=`c96e29f0fc8cbf3d2e51713cc18adffe222853ae`, dirty=`False`, commit_exists=`True`, commits_since_source=`90`, changed_paths_since_source=`52`, non_self_changed_paths_since_source=`51`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `formal_h01_h02`, path `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
- `claim_safety`: `historical_clean`, source_head=`4082e6fae4cdebee0795e91653d73d2cca7dff75`, current_head=`c96e29f0fc8cbf3d2e51713cc18adffe222853ae`, dirty=`False`, commit_exists=`True`, commits_since_source=`14`, changed_paths_since_source=`12`, non_self_changed_paths_since_source=`10`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_claim_safety/module2_claim_safety.json`
- `formal_gate_missing_artifacts`: `historical_clean`, source_head=`becec5f7e49d9fff9f7d32275bc3f4dd6c6a0ccf`, current_head=`c96e29f0fc8cbf3d2e51713cc18adffe222853ae`, dirty=`False`, commit_exists=`True`, commits_since_source=`78`, changed_paths_since_source=`51`, non_self_changed_paths_since_source=`50`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json`
- `formal_gate_proof_audit`: `historical_clean`, source_head=`8ce84db65f9defd70df9295b3ef45f96d60f8fa9`, current_head=`c96e29f0fc8cbf3d2e51713cc18adffe222853ae`, dirty=`False`, commit_exists=`True`, commits_since_source=`60`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`39`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json`
- `formal_gate_remaining_deliverables`: `historical_clean`, source_head=`df1e95b557eb90564f1229187ae8b48f20199d95`, current_head=`c96e29f0fc8cbf3d2e51713cc18adffe222853ae`, dirty=`False`, commit_exists=`True`, commits_since_source=`65`, changed_paths_since_source=`46`, non_self_changed_paths_since_source=`44`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json`
- `formal_gate_status_report`: `historical_dirty`, source_head=`6ed0ca78b99e41d8ce86946d2672cfbd0325ddf0+dirty`, current_head=`c96e29f0fc8cbf3d2e51713cc18adffe222853ae`, dirty=`True`, commit_exists=`True`, commits_since_source=`24`, changed_paths_since_source=`17`, non_self_changed_paths_since_source=`15`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
- `paper_readiness`: `historical_clean`, source_head=`a8fb987d0d9b130af03bf5a5a7e647af69151de6`, current_head=`c96e29f0fc8cbf3d2e51713cc18adffe222853ae`, dirty=`False`, commit_exists=`True`, commits_since_source=`1`, changed_paths_since_source=`1`, non_self_changed_paths_since_source=`0`, self_artifact_only_lag=`True`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_paper_readiness/module2_paper_readiness.json`

## Artifact Records

- `f02_6_decision_record`: status=`pending_human_decision`, freshness=`historical_clean`, source_head=`457a683d21472b90b590418577db5ae2d069d5b9`
- `f02_6_decision_intake`: status=`f02_6_decision_intake_pending_clean`, freshness=`historical_clean`, source_head=`d85b7bcfe03b2794f5babc3e0f0bcd07b7a80309`
- `f02_6_decision_gate_audit`: status=`f02_6_decision_gate_pending_clean`, freshness=`historical_clean`, source_head=`0349d3fd560940fff35b959d7ba89314e9e493a1`
- `f02_6_transition_gate_audit`: status=`f02_6_transition_gate_audit_passed`, freshness=`historical_clean`, source_head=`67ac01b069f5bfc4cca16ee7c9e3332065beca93`
- `remote_formal_execution_packet`: status=`blocked_until_f02_6_decision`, freshness=`historical_clean`, source_head=`9ec25e9564e46fbfb7f2363429a5ac187ac61517`
- `h01_evaluation_manifest`: status=`blocked_pending_decisions`, freshness=`historical_clean`, source_head=`92bf7f431a61fbe7e7818b8a58092ab30c64850d`
- `h02_formal_acceptance`: status=`blocked_formal_output_acceptance`, freshness=`historical_clean`, source_head=`136e70a25f8843ace4b0b707881248d4f107682c`
- `claim_safety`: status=`blocked_formal_performance_claims`, freshness=`historical_clean`, source_head=`4082e6fae4cdebee0795e91653d73d2cca7dff75`
- `paper_readiness`: status=`partial_methods_ready_results_blocked`, freshness=`historical_clean`, source_head=`a8fb987d0d9b130af03bf5a5a7e647af69151de6`
- `formal_gate_gap_audit`: status=`blocked_formal_gate_gaps_open`, freshness=`historical_clean`, source_head=`555e1ad3e6c3e2fa9c8c0ba3b505e32b2847a103`
- `post_f02_6_plan_audit`: status=`post_f02_6_plan_audit_passed`, freshness=`historical_clean`, source_head=`ea458d44d9cf4a77d88e1765673f3a2acc20056c`
- `remote_packet_safety_audit`: status=`remote_packet_safety_audit_passed`, freshness=`historical_clean`, source_head=`53e3bbf6b8afef8ee779d568bac05b9ad1308ab5`
- `formal_gate_closure_checklist`: status=`formal_gate_closure_blocked`, freshness=`historical_clean`, source_head=`3a901a307d73c8119e1d29dc863b834d47376c68`
- `gpu3070ti_readiness_refresh`: status=`remote_readiness_refreshed_f02_6_still_blocked`, freshness=`historical_clean`, source_head=`033356f27e5255c60d64a78753054b86ef2a0428`
- `formal_gate_missing_artifacts`: status=`formal_gate_missing_artifacts_open`, freshness=`historical_clean`, source_head=`becec5f7e49d9fff9f7d32275bc3f4dd6c6a0ccf`
- `formal_gate_status_report`: status=`formal_gate_status_blocked`, freshness=`historical_dirty`, source_head=`6ed0ca78b99e41d8ce86946d2672cfbd0325ddf0+dirty`
- `formal_gate_remaining_deliverables`: status=`formal_gate_deliverables_blocked`, freshness=`historical_clean`, source_head=`df1e95b557eb90564f1229187ae8b48f20199d95`
- `formal_gate_proof_audit`: status=`formal_gate_proof_audit_blocked`, freshness=`historical_clean`, source_head=`8ce84db65f9defd70df9295b3ef45f96d60f8fa9`
- `formal_gate_handoff_bundle`: status=`blocked_until_f02_6_decision`, freshness=`historical_clean`, source_head=`2c81a650271875c04a628ef21a367cc878787bb0`

## Claim Boundaries

- This audit records source-head freshness only; it is not a training run or paper result.
- Historical or dirty source_head values are regeneration risks, not formal experimental failures.
- The audit artifact's own post-commit source_head lag is expected and is not a formal gate blocker by itself.
- F02.6 remains the human approval gate before approved remote preflight or formal PPO training.
- Regenerate stale/dirty gate artifacts after F02.6 closes and before H01/H02 formal evaluation or formal claims.
