# Module2 Source Freshness Audit

This file records gate artifact source-head freshness. It is not a training run, remote preflight, paper table, or result claim.

- status: `source_freshness_risks_recorded_gate_still_blocked`
- current_head: `75430fd83c32e0e1f667407f54cf8b987b1cd849`
- runs_training: `False`
- runs_remote_preflight: `False`
- formal_claim_allowed: `False`
- regeneration_required_before_remote_formal_execution: `True`

## Risk Counts

- `historical_clean`: `2`
- `historical_dirty`: `6`

## Regeneration Targets

- `f02_6_decision_record`: `historical_dirty`, required before `approved_remote_preflight`, path `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json`
- `formal_gate_gap_audit`: `historical_dirty`, required before `approved_remote_preflight`, path `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json`
- `gpu3070ti_readiness_refresh`: `historical_clean`, required before `approved_remote_preflight`, path `0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.json`
- `remote_formal_execution_packet`: `historical_dirty`, required before `approved_remote_preflight`, path `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json`
- `h01_evaluation_manifest`: `historical_dirty`, required before `formal_h01_h02`, path `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`
- `h02_formal_acceptance`: `historical_dirty`, required before `formal_h01_h02`, path `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
- `claim_safety`: `historical_clean`, required before `formal_claim_gate`, path `0_trials/module2_claim_safety/module2_claim_safety.json`
- `paper_readiness`: `historical_dirty`, required before `formal_claim_gate`, path `0_trials/module2_paper_readiness/module2_paper_readiness.json`

## Artifact Records

- `f02_6_decision_record`: status=`pending_human_decision`, freshness=`historical_dirty`, source_head=`b9c4085a20ce37a5dbcc9dffb0a707403eb8e6fb+dirty`
- `remote_formal_execution_packet`: status=`blocked_until_f02_6_decision`, freshness=`historical_dirty`, source_head=`bca5a976bff4950e62e419ebd0b87ba2acfb0bae+dirty`
- `h01_evaluation_manifest`: status=`blocked_pending_decisions`, freshness=`historical_dirty`, source_head=`4887f66ce6b4d32ce269d9da7d4a691e0ba5e5f6+dirty`
- `h02_formal_acceptance`: status=`blocked_formal_output_acceptance`, freshness=`historical_dirty`, source_head=`09926d3d8e833d6b5b1d52faea5127a7d644d147+dirty`
- `claim_safety`: status=`blocked_formal_performance_claims`, freshness=`historical_clean`, source_head=`f4459945dbde1ba2ca66c178efcb53db03bd4c6f`
- `paper_readiness`: status=`partial_methods_ready_results_blocked`, freshness=`historical_dirty`, source_head=`6689b3ab720df72d364492094379eb76a8b09ef2+dirty`
- `formal_gate_gap_audit`: status=`blocked_formal_gate_gaps_open`, freshness=`historical_dirty`, source_head=`be670b451f57f661180f7a5e82de3be19965bb35+dirty`
- `gpu3070ti_readiness_refresh`: status=`remote_readiness_refreshed_f02_6_still_blocked`, freshness=`historical_clean`, source_head=`033356f27e5255c60d64a78753054b86ef2a0428`

## Claim Boundaries

- This audit records source-head freshness only; it is not a training run or paper result.
- Historical or dirty source_head values are regeneration risks, not formal experimental failures.
- F02.6 remains the human approval gate before approved remote preflight or formal PPO training.
- Regenerate stale/dirty gate artifacts after F02.6 closes and before H01/H02 formal evaluation or formal claims.
