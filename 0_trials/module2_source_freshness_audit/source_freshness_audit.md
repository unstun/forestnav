# Module2 Source Freshness Audit

This file records gate artifact source-head freshness. It is not a training run, remote preflight, paper table, or result claim.

- status: `source_freshness_clean_current`
- current_head: `818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- runs_training: `False`
- runs_remote_preflight: `False`
- formal_claim_allowed: `False`
- regeneration_required_before_remote_formal_execution: `False`
- blocking_regeneration_required_before_remote_formal_execution: `False`
- blocking_regeneration_target_count: `0`
- self_artifact_only_lag_target_count: `0`
- tracked_artifact_only_lag_target_count: `0`

## Risk Counts

- `current_clean`: `23`

## Commit Lag Diagnostics

- `records_with_commit_lag`: `0`
- `records_with_unknown_commit_lag`: `0`
- `records_with_changed_paths_since_source`: `0`
- `records_with_artifact_path_changed_since_source`: `0`
- `records_with_non_self_changed_paths_since_source`: `0`
- `records_with_blocking_changed_paths_since_source`: `0`
- `records_with_self_artifact_only_lag`: `0`
- `records_with_tracked_artifact_only_lag`: `0`
- `max_commits_since_source`: `0`
- `max_non_self_changed_path_count_since_source`: `0`
- `max_blocking_changed_path_count_since_source`: `0`
- `changed_path_sample_limit`: `12`

## Audit Self-Reference Policy

- `source_head_scope`: `generation_time_repository_head`
- `commit_storing_this_audit_known_at_generation`: `False`
- `expected_post_commit_self_lag`: `True`
- `self_lag_is_formal_gate_blocker`: `False`
- `manifest_path`: `0_trials/module2_source_freshness_audit/source_freshness_audit.json`
- `markdown_path`: `0_trials/module2_source_freshness_audit/source_freshness_audit.md`

## Regeneration Targets

- `formal_gate_handoff_bundle`: `current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`, current_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`, dirty=`False`, commit_exists=`True`, commits_since_source=`0`, changed_paths_since_source=`0`, non_self_changed_paths_since_source=`0`, blocking_changed_paths_since_source=`0`, self_artifact_only_lag=`False`, tracked_artifact_only_lag=`False`, blocking_regeneration=`False`, artifact_path_changed=`False`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json`

## Artifact Records

- `f02_6_warm_start_decision_packet`: status=`pending_human_decision`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- `f02_6_decision_record`: status=`pending_human_decision`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- `f02_6_decision_intake`: status=`f02_6_decision_intake_pending_clean`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- `f02_6_decision_gate_audit`: status=`f02_6_decision_gate_pending_clean`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- `f02_6_transition_gate_audit`: status=`f02_6_transition_gate_audit_passed`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- `remote_formal_execution_packet`: status=`blocked_until_f02_6_decision`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- `h01_evaluation_manifest`: status=`blocked_pending_decisions`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- `h02_formal_acceptance`: status=`blocked_formal_output_acceptance`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- `claim_safety`: status=`blocked_formal_performance_claims`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- `paper_readiness`: status=`partial_methods_ready_results_blocked`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- `formal_gate_gap_audit`: status=`blocked_formal_gate_gaps_open`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- `post_f02_6_regeneration_plan`: status=`blocked_until_f02_6_decision`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- `post_f02_6_plan_audit`: status=`post_f02_6_plan_audit_passed`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- `remote_packet_safety_audit`: status=`remote_packet_safety_audit_passed`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- `formal_gate_closure_checklist`: status=`formal_gate_closure_blocked`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- `gpu3070ti_readiness_refresh`: status=`remote_readiness_refreshed_f02_6_still_blocked`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- `formal_gate_missing_artifacts`: status=`formal_gate_missing_artifacts_open`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- `formal_gate_status_report`: status=`formal_gate_status_blocked`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- `formal_gate_remaining_deliverables`: status=`formal_gate_deliverables_blocked`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- `formal_gate_proof_audit`: status=`formal_gate_proof_audit_blocked`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- `formal_gate_proof_summary_chain_audit`: status=`formal_gate_proof_summary_chain_audit_failed`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- `mainline_formal_gate_state_audit`: status=`mainline_formal_gate_state_audit_failed`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`
- `formal_gate_handoff_bundle`: status=`blocked_until_f02_6_decision`, freshness=`current_clean`, source_head=`818b4b347b211ccef4fbf77fd120ea2c3b48510a`

## Claim Boundaries

- This audit records source-head freshness only; it is not a training run or paper result.
- Historical or dirty source_head values are regeneration risks, not formal experimental failures.
- The audit artifact's own post-commit source_head lag is expected and is not a formal gate blocker by itself.
- F02.6 remains the human approval gate before approved remote preflight or formal PPO training.
- Regenerate stale/dirty gate artifacts after F02.6 closes and before H01/H02 formal evaluation or formal claims.
