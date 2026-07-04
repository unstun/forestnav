# Module2 Manuscript Claim Audit

- status: `maintex_module2_claim_audit_passed`
- prohibited claim audit: `clean`
- local training allowed: `False`
- remote training resource: `gpu3070ti-relay`

## Blocking Reasons

- none

## Module2 Input Checks

- `module2_seed_input_present`: `True`
- `module2_label_present`: `True`
- `method_boundary_present`: `True`
- `no_warm_scope_present`: `True`
- `formal_blocked_sentence_present`: `True`
- `formal_results_blocked_comment_present`: `True`
- `warm_start_blocked_comment_present`: `True`

## Readiness Checks

- `paper_readiness_status`: `partial_methods_ready_results_blocked`
- `formal_results_status`: `blocked`
- `formal_results_blockers`: `['paper_tables_not_formal', 'h02_verdict_not_formal', 'h02_formal_acceptance_not_accepted', 'h01_manifest_not_ready', 'f02_6_warm_start_decision_pending', 'missing_module2_rl_rs_checkpoint', 'remote_execution_packet_not_ready', 'requires_dr_sun_approval', 'missing_gate3_formal_audit', 'h02_scale_below_h01_manifest', 'missing_ppo_result_rows', 'missing_remote_pullback_artifacts', 'f02_6_formal_chain_pending', 'claim_safety_blocks_formal_performance', 'f02_6_pending']`
- `warm_start_effect_status`: `blocked`
- `warm_start_effect_blockers`: `['f02_6_not_approved', 'requires_dr_sun_approval', 'f02_6_warm_start_decision_pending', 'missing_module2_rl_rs_checkpoint']`

## Prohibited Claim Violations

- none

## Claim Boundaries

- This audit expands LaTeX inputs before scanning Module2 claims.
- LaTeX comments are ignored for prohibited-claim matching so BLOCKED comments can document missing evidence without becoming claims.
- Formal Module2 results and warm-start effect remain blocked until paper readiness, H02 acceptance, and claim safety are formal-ready.
- No local training is allowed; formal PPO training remains gated on F02.6 and gpu3070ti-relay.
