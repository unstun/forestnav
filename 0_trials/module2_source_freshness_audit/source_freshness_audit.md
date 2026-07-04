# Module2 Source Freshness Audit

This file records gate artifact source-head freshness. It is not a training run, remote preflight, paper table, or result claim.

- status: `source_freshness_risks_recorded_gate_still_blocked`
- current_head: `8a9877145f992f38d8721630a9e2f2a9866833aa`
- runs_training: `False`
- runs_remote_preflight: `False`
- formal_claim_allowed: `False`
- regeneration_required_before_remote_formal_execution: `True`

## Risk Counts

- `historical_clean`: `3`
- `historical_dirty`: `14`

## Regeneration Targets

- `f02_6_decision_gate_audit`: `historical_dirty`, source_head=`e0e5c100c6a5fe777648a91e2039f1f40ed88262+dirty`, current_head=`8a9877145f992f38d8721630a9e2f2a9866833aa`, dirty=`True`, commit_exists=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.json`
- `f02_6_decision_intake`: `historical_dirty`, source_head=`8b76a651a8a34e20390979a8e22a6ce05a3e06fd+dirty`, current_head=`8a9877145f992f38d8721630a9e2f2a9866833aa`, dirty=`True`, commit_exists=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json`
- `f02_6_decision_record`: `historical_dirty`, source_head=`b9c4085a20ce37a5dbcc9dffb0a707403eb8e6fb+dirty`, current_head=`8a9877145f992f38d8721630a9e2f2a9866833aa`, dirty=`True`, commit_exists=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json`
- `f02_6_transition_gate_audit`: `historical_dirty`, source_head=`4e882c09d8ede868504f3dbf63a31a1125841170+dirty`, current_head=`8a9877145f992f38d8721630a9e2f2a9866833aa`, dirty=`True`, commit_exists=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json`
- `formal_gate_closure_checklist`: `historical_dirty`, source_head=`59caee5cc01ed95e6e8d5d82384dafdb09292d45+dirty`, current_head=`8a9877145f992f38d8721630a9e2f2a9866833aa`, dirty=`True`, commit_exists=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json`
- `formal_gate_gap_audit`: `historical_dirty`, source_head=`59caee5cc01ed95e6e8d5d82384dafdb09292d45+dirty`, current_head=`8a9877145f992f38d8721630a9e2f2a9866833aa`, dirty=`True`, commit_exists=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json`
- `formal_gate_handoff_bundle`: `historical_clean`, source_head=`03373965cd5c3696ba1ac0fe12e6e5547b421513`, current_head=`8a9877145f992f38d8721630a9e2f2a9866833aa`, dirty=`False`, commit_exists=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json`
- `gpu3070ti_readiness_refresh`: `historical_clean`, source_head=`033356f27e5255c60d64a78753054b86ef2a0428`, current_head=`8a9877145f992f38d8721630a9e2f2a9866833aa`, dirty=`False`, commit_exists=`True`, required before `approved_remote_preflight`, path `0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.json`
- `post_f02_6_plan_audit`: `historical_dirty`, source_head=`4368599f29da0e63bc272d3ef2facfcc942c5d47+dirty`, current_head=`8a9877145f992f38d8721630a9e2f2a9866833aa`, dirty=`True`, commit_exists=`True`, required before `approved_remote_preflight`, path `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
- `remote_formal_execution_packet`: `historical_dirty`, source_head=`01c57e4da7473cff42e2aafbd62431772eae0bb6+dirty`, current_head=`8a9877145f992f38d8721630a9e2f2a9866833aa`, dirty=`True`, commit_exists=`True`, required before `approved_remote_preflight`, path `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json`
- `remote_packet_safety_audit`: `historical_dirty`, source_head=`4368599f29da0e63bc272d3ef2facfcc942c5d47+dirty`, current_head=`8a9877145f992f38d8721630a9e2f2a9866833aa`, dirty=`True`, commit_exists=`True`, required before `approved_remote_preflight`, path `0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`
- `h01_evaluation_manifest`: `historical_dirty`, source_head=`4887f66ce6b4d32ce269d9da7d4a691e0ba5e5f6+dirty`, current_head=`8a9877145f992f38d8721630a9e2f2a9866833aa`, dirty=`True`, commit_exists=`True`, required before `formal_h01_h02`, path `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`
- `h02_formal_acceptance`: `historical_dirty`, source_head=`5c4bf4a43c55f74b14f893e8f64dec84eb9d66ad+dirty`, current_head=`8a9877145f992f38d8721630a9e2f2a9866833aa`, dirty=`True`, commit_exists=`True`, required before `formal_h01_h02`, path `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
- `claim_safety`: `historical_clean`, source_head=`5c57bd520100776c878f3235dd6d203b236770b7`, current_head=`8a9877145f992f38d8721630a9e2f2a9866833aa`, dirty=`False`, commit_exists=`True`, required before `formal_claim_gate`, path `0_trials/module2_claim_safety/module2_claim_safety.json`
- `formal_gate_missing_artifacts`: `historical_dirty`, source_head=`03373965cd5c3696ba1ac0fe12e6e5547b421513+dirty`, current_head=`8a9877145f992f38d8721630a9e2f2a9866833aa`, dirty=`True`, commit_exists=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json`
- `formal_gate_status_report`: `historical_dirty`, source_head=`5c57bd520100776c878f3235dd6d203b236770b7+dirty`, current_head=`8a9877145f992f38d8721630a9e2f2a9866833aa`, dirty=`True`, commit_exists=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
- `paper_readiness`: `historical_dirty`, source_head=`c09b48b139461911443bc843fc144507dcd85dc4+dirty`, current_head=`8a9877145f992f38d8721630a9e2f2a9866833aa`, dirty=`True`, commit_exists=`True`, required before `formal_claim_gate`, path `0_trials/module2_paper_readiness/module2_paper_readiness.json`

## Artifact Records

- `f02_6_decision_record`: status=`pending_human_decision`, freshness=`historical_dirty`, source_head=`b9c4085a20ce37a5dbcc9dffb0a707403eb8e6fb+dirty`
- `f02_6_decision_intake`: status=`f02_6_decision_intake_pending_clean`, freshness=`historical_dirty`, source_head=`8b76a651a8a34e20390979a8e22a6ce05a3e06fd+dirty`
- `f02_6_decision_gate_audit`: status=`f02_6_decision_gate_pending_clean`, freshness=`historical_dirty`, source_head=`e0e5c100c6a5fe777648a91e2039f1f40ed88262+dirty`
- `f02_6_transition_gate_audit`: status=`f02_6_transition_gate_audit_passed`, freshness=`historical_dirty`, source_head=`4e882c09d8ede868504f3dbf63a31a1125841170+dirty`
- `remote_formal_execution_packet`: status=`blocked_until_f02_6_decision`, freshness=`historical_dirty`, source_head=`01c57e4da7473cff42e2aafbd62431772eae0bb6+dirty`
- `h01_evaluation_manifest`: status=`blocked_pending_decisions`, freshness=`historical_dirty`, source_head=`4887f66ce6b4d32ce269d9da7d4a691e0ba5e5f6+dirty`
- `h02_formal_acceptance`: status=`blocked_formal_output_acceptance`, freshness=`historical_dirty`, source_head=`5c4bf4a43c55f74b14f893e8f64dec84eb9d66ad+dirty`
- `claim_safety`: status=`blocked_formal_performance_claims`, freshness=`historical_clean`, source_head=`5c57bd520100776c878f3235dd6d203b236770b7`
- `paper_readiness`: status=`partial_methods_ready_results_blocked`, freshness=`historical_dirty`, source_head=`c09b48b139461911443bc843fc144507dcd85dc4+dirty`
- `formal_gate_gap_audit`: status=`blocked_formal_gate_gaps_open`, freshness=`historical_dirty`, source_head=`59caee5cc01ed95e6e8d5d82384dafdb09292d45+dirty`
- `post_f02_6_plan_audit`: status=`post_f02_6_plan_audit_passed`, freshness=`historical_dirty`, source_head=`4368599f29da0e63bc272d3ef2facfcc942c5d47+dirty`
- `remote_packet_safety_audit`: status=`remote_packet_safety_audit_passed`, freshness=`historical_dirty`, source_head=`4368599f29da0e63bc272d3ef2facfcc942c5d47+dirty`
- `formal_gate_closure_checklist`: status=`formal_gate_closure_blocked`, freshness=`historical_dirty`, source_head=`59caee5cc01ed95e6e8d5d82384dafdb09292d45+dirty`
- `gpu3070ti_readiness_refresh`: status=`remote_readiness_refreshed_f02_6_still_blocked`, freshness=`historical_clean`, source_head=`033356f27e5255c60d64a78753054b86ef2a0428`
- `formal_gate_missing_artifacts`: status=`formal_gate_missing_artifacts_open`, freshness=`historical_dirty`, source_head=`03373965cd5c3696ba1ac0fe12e6e5547b421513+dirty`
- `formal_gate_status_report`: status=`formal_gate_status_blocked`, freshness=`historical_dirty`, source_head=`5c57bd520100776c878f3235dd6d203b236770b7+dirty`
- `formal_gate_handoff_bundle`: status=`blocked_until_f02_6_decision`, freshness=`historical_clean`, source_head=`03373965cd5c3696ba1ac0fe12e6e5547b421513`

## Claim Boundaries

- This audit records source-head freshness only; it is not a training run or paper result.
- Historical or dirty source_head values are regeneration risks, not formal experimental failures.
- F02.6 remains the human approval gate before approved remote preflight or formal PPO training.
- Regenerate stale/dirty gate artifacts after F02.6 closes and before H01/H02 formal evaluation or formal claims.
