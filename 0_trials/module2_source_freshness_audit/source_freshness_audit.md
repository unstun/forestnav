# Module2 Source Freshness Audit

This file records gate artifact source-head freshness. It is not a training run, remote preflight, paper table, or result claim.

- status: `source_freshness_risks_recorded_gate_still_blocked`
- current_head: `858ece7f044510d35900ae0fa133b33e375e3dcf`
- runs_training: `False`
- runs_remote_preflight: `False`
- formal_claim_allowed: `False`
- regeneration_required_before_remote_formal_execution: `True`

## Risk Counts

- `current_dirty`: `2`
- `historical_clean`: `3`
- `historical_dirty`: `14`

## Regeneration Targets

- `f02_6_decision_gate_audit`: `historical_dirty`, source_head=`849c39867a5e867d9f78579c176e3b61d04d7556+dirty`, current_head=`858ece7f044510d35900ae0fa133b33e375e3dcf`, dirty=`True`, commit_exists=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.json`
- `f02_6_decision_intake`: `current_dirty`, source_head=`858ece7f044510d35900ae0fa133b33e375e3dcf+dirty`, current_head=`858ece7f044510d35900ae0fa133b33e375e3dcf`, dirty=`True`, commit_exists=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json`
- `f02_6_decision_record`: `historical_dirty`, source_head=`849c39867a5e867d9f78579c176e3b61d04d7556+dirty`, current_head=`858ece7f044510d35900ae0fa133b33e375e3dcf`, dirty=`True`, commit_exists=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json`
- `f02_6_transition_gate_audit`: `historical_dirty`, source_head=`849c39867a5e867d9f78579c176e3b61d04d7556+dirty`, current_head=`858ece7f044510d35900ae0fa133b33e375e3dcf`, dirty=`True`, commit_exists=`True`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json`
- `formal_gate_closure_checklist`: `historical_dirty`, source_head=`4e88777f45f83989bc9fc74090404c86a034ee79+dirty`, current_head=`858ece7f044510d35900ae0fa133b33e375e3dcf`, dirty=`True`, commit_exists=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json`
- `formal_gate_gap_audit`: `historical_dirty`, source_head=`4e88777f45f83989bc9fc74090404c86a034ee79+dirty`, current_head=`858ece7f044510d35900ae0fa133b33e375e3dcf`, dirty=`True`, commit_exists=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json`
- `formal_gate_handoff_bundle`: `historical_clean`, source_head=`e6b5d09156b6299adc8f46658d7b85763148eb6a`, current_head=`858ece7f044510d35900ae0fa133b33e375e3dcf`, dirty=`False`, commit_exists=`True`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json`
- `gpu3070ti_readiness_refresh`: `historical_clean`, source_head=`033356f27e5255c60d64a78753054b86ef2a0428`, current_head=`858ece7f044510d35900ae0fa133b33e375e3dcf`, dirty=`False`, commit_exists=`True`, required before `approved_remote_preflight`, path `0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.json`
- `post_f02_6_plan_audit`: `historical_dirty`, source_head=`4e88777f45f83989bc9fc74090404c86a034ee79+dirty`, current_head=`858ece7f044510d35900ae0fa133b33e375e3dcf`, dirty=`True`, commit_exists=`True`, required before `approved_remote_preflight`, path `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
- `remote_formal_execution_packet`: `historical_dirty`, source_head=`01c57e4da7473cff42e2aafbd62431772eae0bb6+dirty`, current_head=`858ece7f044510d35900ae0fa133b33e375e3dcf`, dirty=`True`, commit_exists=`True`, required before `approved_remote_preflight`, path `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json`
- `remote_packet_safety_audit`: `historical_dirty`, source_head=`cec3317d5977577bfe1014aaecdf4bcd8b501aae+dirty`, current_head=`858ece7f044510d35900ae0fa133b33e375e3dcf`, dirty=`True`, commit_exists=`True`, required before `approved_remote_preflight`, path `0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`
- `h01_evaluation_manifest`: `historical_dirty`, source_head=`4887f66ce6b4d32ce269d9da7d4a691e0ba5e5f6+dirty`, current_head=`858ece7f044510d35900ae0fa133b33e375e3dcf`, dirty=`True`, commit_exists=`True`, required before `formal_h01_h02`, path `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`
- `h02_formal_acceptance`: `historical_dirty`, source_head=`5c4bf4a43c55f74b14f893e8f64dec84eb9d66ad+dirty`, current_head=`858ece7f044510d35900ae0fa133b33e375e3dcf`, dirty=`True`, commit_exists=`True`, required before `formal_h01_h02`, path `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
- `claim_safety`: `historical_clean`, source_head=`f21eb594fdd75e125e74c729ae4a5e751ad08407`, current_head=`858ece7f044510d35900ae0fa133b33e375e3dcf`, dirty=`False`, commit_exists=`True`, required before `formal_claim_gate`, path `0_trials/module2_claim_safety/module2_claim_safety.json`
- `formal_gate_missing_artifacts`: `historical_dirty`, source_head=`4e88777f45f83989bc9fc74090404c86a034ee79+dirty`, current_head=`858ece7f044510d35900ae0fa133b33e375e3dcf`, dirty=`True`, commit_exists=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json`
- `formal_gate_proof_audit`: `historical_dirty`, source_head=`4e88777f45f83989bc9fc74090404c86a034ee79+dirty`, current_head=`858ece7f044510d35900ae0fa133b33e375e3dcf`, dirty=`True`, commit_exists=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json`
- `formal_gate_remaining_deliverables`: `historical_dirty`, source_head=`4e88777f45f83989bc9fc74090404c86a034ee79+dirty`, current_head=`858ece7f044510d35900ae0fa133b33e375e3dcf`, dirty=`True`, commit_exists=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json`
- `formal_gate_status_report`: `current_dirty`, source_head=`858ece7f044510d35900ae0fa133b33e375e3dcf+dirty`, current_head=`858ece7f044510d35900ae0fa133b33e375e3dcf`, dirty=`True`, commit_exists=`True`, required before `formal_claim_gate`, path `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
- `paper_readiness`: `historical_dirty`, source_head=`68a4a448fbeecc0e6ee1d8db5e973b64ce6d8f78+dirty`, current_head=`858ece7f044510d35900ae0fa133b33e375e3dcf`, dirty=`True`, commit_exists=`True`, required before `formal_claim_gate`, path `0_trials/module2_paper_readiness/module2_paper_readiness.json`

## Artifact Records

- `f02_6_decision_record`: status=`pending_human_decision`, freshness=`historical_dirty`, source_head=`849c39867a5e867d9f78579c176e3b61d04d7556+dirty`
- `f02_6_decision_intake`: status=`f02_6_decision_intake_pending_clean`, freshness=`current_dirty`, source_head=`858ece7f044510d35900ae0fa133b33e375e3dcf+dirty`
- `f02_6_decision_gate_audit`: status=`f02_6_decision_gate_pending_clean`, freshness=`historical_dirty`, source_head=`849c39867a5e867d9f78579c176e3b61d04d7556+dirty`
- `f02_6_transition_gate_audit`: status=`f02_6_transition_gate_audit_passed`, freshness=`historical_dirty`, source_head=`849c39867a5e867d9f78579c176e3b61d04d7556+dirty`
- `remote_formal_execution_packet`: status=`blocked_until_f02_6_decision`, freshness=`historical_dirty`, source_head=`01c57e4da7473cff42e2aafbd62431772eae0bb6+dirty`
- `h01_evaluation_manifest`: status=`blocked_pending_decisions`, freshness=`historical_dirty`, source_head=`4887f66ce6b4d32ce269d9da7d4a691e0ba5e5f6+dirty`
- `h02_formal_acceptance`: status=`blocked_formal_output_acceptance`, freshness=`historical_dirty`, source_head=`5c4bf4a43c55f74b14f893e8f64dec84eb9d66ad+dirty`
- `claim_safety`: status=`blocked_formal_performance_claims`, freshness=`historical_clean`, source_head=`f21eb594fdd75e125e74c729ae4a5e751ad08407`
- `paper_readiness`: status=`partial_methods_ready_results_blocked`, freshness=`historical_dirty`, source_head=`68a4a448fbeecc0e6ee1d8db5e973b64ce6d8f78+dirty`
- `formal_gate_gap_audit`: status=`blocked_formal_gate_gaps_open`, freshness=`historical_dirty`, source_head=`4e88777f45f83989bc9fc74090404c86a034ee79+dirty`
- `post_f02_6_plan_audit`: status=`post_f02_6_plan_audit_passed`, freshness=`historical_dirty`, source_head=`4e88777f45f83989bc9fc74090404c86a034ee79+dirty`
- `remote_packet_safety_audit`: status=`remote_packet_safety_audit_passed`, freshness=`historical_dirty`, source_head=`cec3317d5977577bfe1014aaecdf4bcd8b501aae+dirty`
- `formal_gate_closure_checklist`: status=`formal_gate_closure_blocked`, freshness=`historical_dirty`, source_head=`4e88777f45f83989bc9fc74090404c86a034ee79+dirty`
- `gpu3070ti_readiness_refresh`: status=`remote_readiness_refreshed_f02_6_still_blocked`, freshness=`historical_clean`, source_head=`033356f27e5255c60d64a78753054b86ef2a0428`
- `formal_gate_missing_artifacts`: status=`formal_gate_missing_artifacts_open`, freshness=`historical_dirty`, source_head=`4e88777f45f83989bc9fc74090404c86a034ee79+dirty`
- `formal_gate_status_report`: status=`formal_gate_status_blocked`, freshness=`current_dirty`, source_head=`858ece7f044510d35900ae0fa133b33e375e3dcf+dirty`
- `formal_gate_remaining_deliverables`: status=`formal_gate_deliverables_blocked`, freshness=`historical_dirty`, source_head=`4e88777f45f83989bc9fc74090404c86a034ee79+dirty`
- `formal_gate_proof_audit`: status=`formal_gate_proof_audit_blocked`, freshness=`historical_dirty`, source_head=`4e88777f45f83989bc9fc74090404c86a034ee79+dirty`
- `formal_gate_handoff_bundle`: status=`blocked_until_f02_6_decision`, freshness=`historical_clean`, source_head=`e6b5d09156b6299adc8f46658d7b85763148eb6a`

## Claim Boundaries

- This audit records source-head freshness only; it is not a training run or paper result.
- Historical or dirty source_head values are regeneration risks, not formal experimental failures.
- F02.6 remains the human approval gate before approved remote preflight or formal PPO training.
- Regenerate stale/dirty gate artifacts after F02.6 closes and before H01/H02 formal evaluation or formal claims.
