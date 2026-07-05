# Module2 Source Freshness Audit

This file records gate artifact source-head freshness. It is not a training run, remote preflight, paper table, or result claim.

- status: `source_freshness_risks_recorded_gate_still_blocked`
- current_head: `8587f2fdfa74efc3a3773235734832ec618b5334`
- runs_training: `False`
- runs_remote_preflight: `False`
- formal_claim_allowed: `False`
- regeneration_required_before_remote_formal_execution: `True`

## Risk Counts

- `historical_clean`: `19`

## Commit Lag Diagnostics

- `records_with_commit_lag`: `19`
- `records_with_unknown_commit_lag`: `0`
- `records_with_changed_paths_since_source`: `19`
- `records_with_artifact_path_changed_since_source`: `19`
- `records_with_non_self_changed_paths_since_source`: `18`
- `records_with_self_artifact_only_lag`: `1`
- `max_commits_since_source`: `651`
- `max_non_self_changed_path_count_since_source`: `169`
- `changed_path_sample_limit`: `12`

## Audit Self-Reference Policy

- `source_head_scope`: `generation_time_repository_head`
- `commit_storing_this_audit_known_at_generation`: `False`
- `expected_post_commit_self_lag`: `True`
- `self_lag_is_formal_gate_blocker`: `False`
- `manifest_path`: `0_trials/module2_source_freshness_audit/source_freshness_audit.json`
- `markdown_path`: `0_trials/module2_source_freshness_audit/source_freshness_audit.md`

## Regeneration Targets

- `f02_6_decision_gate_audit`: `historical_clean`, source_head=`0349d3fd560940fff35b959d7ba89314e9e493a1`, current_head=`8587f2fdfa74efc3a3773235734832ec618b5334`, dirty=`False`, commit_exists=`True`, commits_since_source=`11`, changed_paths_since_source=`9`, non_self_changed_paths_since_source=`8`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.json`
- `f02_6_decision_intake`: `historical_clean`, source_head=`d85b7bcfe03b2794f5babc3e0f0bcd07b7a80309`, current_head=`8587f2fdfa74efc3a3773235734832ec618b5334`, dirty=`False`, commit_exists=`True`, commits_since_source=`10`, changed_paths_since_source=`8`, non_self_changed_paths_since_source=`7`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json`
- `f02_6_decision_record`: `historical_clean`, source_head=`457a683d21472b90b590418577db5ae2d069d5b9`, current_head=`8587f2fdfa74efc3a3773235734832ec618b5334`, dirty=`False`, commit_exists=`True`, commits_since_source=`13`, changed_paths_since_source=`11`, non_self_changed_paths_since_source=`10`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json`
- `f02_6_transition_gate_audit`: `historical_clean`, source_head=`67ac01b069f5bfc4cca16ee7c9e3332065beca93`, current_head=`8587f2fdfa74efc3a3773235734832ec618b5334`, dirty=`False`, commit_exists=`True`, commits_since_source=`5`, changed_paths_since_source=`6`, non_self_changed_paths_since_source=`4`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json`
- `formal_gate_closure_checklist`: `historical_clean`, source_head=`97621b3bee5e38fc7f5b7a24367bd6dd6ce39ed8`, current_head=`8587f2fdfa74efc3a3773235734832ec618b5334`, dirty=`False`, commit_exists=`True`, commits_since_source=`3`, changed_paths_since_source=`4`, non_self_changed_paths_since_source=`3`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json`
- `formal_gate_gap_audit`: `historical_clean`, source_head=`9949fa4b4797c875818487289ddf378efc141402`, current_head=`8587f2fdfa74efc3a3773235734832ec618b5334`, dirty=`False`, commit_exists=`True`, commits_since_source=`66`, changed_paths_since_source=`34`, non_self_changed_paths_since_source=`32`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json`
- `formal_gate_handoff_bundle`: `historical_clean`, source_head=`5772fdef83a70192cd33c7171c4057c78c476daf`, current_head=`8587f2fdfa74efc3a3773235734832ec618b5334`, dirty=`False`, commit_exists=`True`, commits_since_source=`18`, changed_paths_since_source=`15`, non_self_changed_paths_since_source=`14`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json`
- `gpu3070ti_readiness_refresh`: `historical_clean`, source_head=`033356f27e5255c60d64a78753054b86ef2a0428`, current_head=`8587f2fdfa74efc3a3773235734832ec618b5334`, dirty=`False`, commit_exists=`True`, commits_since_source=`651`, changed_paths_since_source=`171`, non_self_changed_paths_since_source=`169`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.json`
- `post_f02_6_plan_audit`: `historical_clean`, source_head=`1b3a75f45e2992ccca370c24d1db4532ecff5887`, current_head=`8587f2fdfa74efc3a3773235734832ec618b5334`, dirty=`False`, commit_exists=`True`, commits_since_source=`69`, changed_paths_since_source=`37`, non_self_changed_paths_since_source=`36`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
- `remote_formal_execution_packet`: `historical_clean`, source_head=`9ec25e9564e46fbfb7f2363429a5ac187ac61517`, current_head=`8587f2fdfa74efc3a3773235734832ec618b5334`, dirty=`False`, commit_exists=`True`, commits_since_source=`22`, changed_paths_since_source=`20`, non_self_changed_paths_since_source=`19`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json`
- `remote_packet_safety_audit`: `historical_clean`, source_head=`e0c7995c243b79b0b7a977f9698e3f5daa12c13a`, current_head=`8587f2fdfa74efc3a3773235734832ec618b5334`, dirty=`False`, commit_exists=`True`, commits_since_source=`15`, changed_paths_since_source=`12`, non_self_changed_paths_since_source=`11`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `approved_remote_preflight`, path `0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`
- `h01_evaluation_manifest`: `historical_clean`, source_head=`92bf7f431a61fbe7e7818b8a58092ab30c64850d`, current_head=`8587f2fdfa74efc3a3773235734832ec618b5334`, dirty=`False`, commit_exists=`True`, commits_since_source=`1`, changed_paths_since_source=`1`, non_self_changed_paths_since_source=`0`, self_artifact_only_lag=`True`, artifact_path_changed=`True`, required before `formal_h01_h02`, path `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`
- `h02_formal_acceptance`: `historical_clean`, source_head=`127cd7d019313dfe5e03d44db6c391cc895d5ec6`, current_head=`8587f2fdfa74efc3a3773235734832ec618b5334`, dirty=`False`, commit_exists=`True`, commits_since_source=`21`, changed_paths_since_source=`19`, non_self_changed_paths_since_source=`18`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `formal_h01_h02`, path `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
- `claim_safety`: `historical_clean`, source_head=`d1e136a7e77379b15d9206f9d98c414e793c1533`, current_head=`8587f2fdfa74efc3a3773235734832ec618b5334`, dirty=`False`, commit_exists=`True`, commits_since_source=`74`, changed_paths_since_source=`41`, non_self_changed_paths_since_source=`39`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_claim_safety/module2_claim_safety.json`
- `formal_gate_missing_artifacts`: `historical_clean`, source_head=`72da37c56a2009311b02bff57685ef1efcdd6dc3`, current_head=`8587f2fdfa74efc3a3773235734832ec618b5334`, dirty=`False`, commit_exists=`True`, commits_since_source=`67`, changed_paths_since_source=`35`, non_self_changed_paths_since_source=`34`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json`
- `formal_gate_proof_audit`: `historical_clean`, source_head=`5c9935b0f841f4869a47a91e29d14ba6ee8012fa`, current_head=`8587f2fdfa74efc3a3773235734832ec618b5334`, dirty=`False`, commit_exists=`True`, commits_since_source=`19`, changed_paths_since_source=`16`, non_self_changed_paths_since_source=`15`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json`
- `formal_gate_remaining_deliverables`: `historical_clean`, source_head=`4e65e8347a28f828a86df1e563ffea48432051e8`, current_head=`8587f2fdfa74efc3a3773235734832ec618b5334`, dirty=`False`, commit_exists=`True`, commits_since_source=`20`, changed_paths_since_source=`18`, non_self_changed_paths_since_source=`16`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json`
- `formal_gate_status_report`: `historical_clean`, source_head=`8a1eaf5e8c13ea97f04d98588089ca11187ae5ec`, current_head=`8587f2fdfa74efc3a3773235734832ec618b5334`, dirty=`False`, commit_exists=`True`, commits_since_source=`17`, changed_paths_since_source=`14`, non_self_changed_paths_since_source=`12`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
- `paper_readiness`: `historical_clean`, source_head=`21905c71383680b02db6c383db664025a0794300`, current_head=`8587f2fdfa74efc3a3773235734832ec618b5334`, dirty=`False`, commit_exists=`True`, commits_since_source=`73`, changed_paths_since_source=`39`, non_self_changed_paths_since_source=`37`, self_artifact_only_lag=`False`, artifact_path_changed=`True`, required before `formal_claim_gate`, path `0_trials/module2_paper_readiness/module2_paper_readiness.json`

## Artifact Records

- `f02_6_decision_record`: status=`pending_human_decision`, freshness=`historical_clean`, source_head=`457a683d21472b90b590418577db5ae2d069d5b9`
- `f02_6_decision_intake`: status=`f02_6_decision_intake_pending_clean`, freshness=`historical_clean`, source_head=`d85b7bcfe03b2794f5babc3e0f0bcd07b7a80309`
- `f02_6_decision_gate_audit`: status=`f02_6_decision_gate_pending_clean`, freshness=`historical_clean`, source_head=`0349d3fd560940fff35b959d7ba89314e9e493a1`
- `f02_6_transition_gate_audit`: status=`f02_6_transition_gate_audit_passed`, freshness=`historical_clean`, source_head=`67ac01b069f5bfc4cca16ee7c9e3332065beca93`
- `remote_formal_execution_packet`: status=`blocked_until_f02_6_decision`, freshness=`historical_clean`, source_head=`9ec25e9564e46fbfb7f2363429a5ac187ac61517`
- `h01_evaluation_manifest`: status=`blocked_pending_decisions`, freshness=`historical_clean`, source_head=`92bf7f431a61fbe7e7818b8a58092ab30c64850d`
- `h02_formal_acceptance`: status=`blocked_formal_output_acceptance`, freshness=`historical_clean`, source_head=`127cd7d019313dfe5e03d44db6c391cc895d5ec6`
- `claim_safety`: status=`blocked_formal_performance_claims`, freshness=`historical_clean`, source_head=`d1e136a7e77379b15d9206f9d98c414e793c1533`
- `paper_readiness`: status=`partial_methods_ready_results_blocked`, freshness=`historical_clean`, source_head=`21905c71383680b02db6c383db664025a0794300`
- `formal_gate_gap_audit`: status=`blocked_formal_gate_gaps_open`, freshness=`historical_clean`, source_head=`9949fa4b4797c875818487289ddf378efc141402`
- `post_f02_6_plan_audit`: status=`post_f02_6_plan_audit_passed`, freshness=`historical_clean`, source_head=`1b3a75f45e2992ccca370c24d1db4532ecff5887`
- `remote_packet_safety_audit`: status=`remote_packet_safety_audit_passed`, freshness=`historical_clean`, source_head=`e0c7995c243b79b0b7a977f9698e3f5daa12c13a`
- `formal_gate_closure_checklist`: status=`formal_gate_closure_blocked`, freshness=`historical_clean`, source_head=`97621b3bee5e38fc7f5b7a24367bd6dd6ce39ed8`
- `gpu3070ti_readiness_refresh`: status=`remote_readiness_refreshed_f02_6_still_blocked`, freshness=`historical_clean`, source_head=`033356f27e5255c60d64a78753054b86ef2a0428`
- `formal_gate_missing_artifacts`: status=`formal_gate_missing_artifacts_open`, freshness=`historical_clean`, source_head=`72da37c56a2009311b02bff57685ef1efcdd6dc3`
- `formal_gate_status_report`: status=`formal_gate_status_blocked`, freshness=`historical_clean`, source_head=`8a1eaf5e8c13ea97f04d98588089ca11187ae5ec`
- `formal_gate_remaining_deliverables`: status=`formal_gate_deliverables_blocked`, freshness=`historical_clean`, source_head=`4e65e8347a28f828a86df1e563ffea48432051e8`
- `formal_gate_proof_audit`: status=`formal_gate_proof_audit_blocked`, freshness=`historical_clean`, source_head=`5c9935b0f841f4869a47a91e29d14ba6ee8012fa`
- `formal_gate_handoff_bundle`: status=`blocked_until_f02_6_decision`, freshness=`historical_clean`, source_head=`5772fdef83a70192cd33c7171c4057c78c476daf`

## Claim Boundaries

- This audit records source-head freshness only; it is not a training run or paper result.
- Historical or dirty source_head values are regeneration risks, not formal experimental failures.
- The audit artifact's own post-commit source_head lag is expected and is not a formal gate blocker by itself.
- F02.6 remains the human approval gate before approved remote preflight or formal PPO training.
- Regenerate stale/dirty gate artifacts after F02.6 closes and before H01/H02 formal evaluation or formal claims.
