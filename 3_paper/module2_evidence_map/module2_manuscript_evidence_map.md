# Module2 Manuscript Evidence Map

- status: `module2_manuscript_evidence_mapped`
- local training allowed: `False`
- remote training resource: `gpu3070ti-relay`
- claim audit status: `maintex_module2_claim_audit_passed`
- formal performance claim allowed: `False`

## Blocking Reasons

- none

## Claim Units

### method_is_ha_star_analytic_operator
- claim status: `allowed_method_structure`
- evidence state: `mapped`
- mapping blockers: none
- evidence:
  - `0_trials/module2_claim_safety/module2_claim_safety.json` status=`blocked_formal_performance_claims`
  - `0_trials/module2_method_algorithms/module2_method_algorithms.json` status=`code_anchored`
  - `0_trials/module2_system_diagram/module2_system_diagram.json` status=`code_anchored_drawio`
  - `0_trials/module2_paper_readiness/module2_paper_readiness.json` status=`ready_to_write`
  - `3_paper/module2_section_seed/module2_paper_section_seed.json` status=`draft_ready`

### no_warm_gate3_formal_failure
- claim status: `allowed_with_no_warm_scope_limit`
- evidence state: `mapped`
- mapping blockers: none
- evidence:
  - `0_trials/module2_claim_safety/module2_claim_safety.json` status=`blocked_formal_performance_claims`
  - `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/gate3_formal_audit.json` status=`fail`
  - `0_trials/module2_paper_readiness/module2_paper_readiness.json` status=`ready_with_scope_limit`
  - `3_paper/module2_section_seed/module2_paper_section_seed.json` status=`draft_ready_with_scope_limit`
- metric values: `terminal_rs_success_rate=0.453125, episodes=64, success_threshold=0.8`

### formal_results_blocked
- claim status: `blocked_placeholder_not_a_result_claim`
- evidence state: `blocked_as_expected`
- mapping blockers: none
- evidence:
  - `3_paper/module2_claim_audit/module2_manuscript_claim_audit.json` status=`maintex_module2_claim_audit_passed`
  - `0_trials/module2_claim_safety/module2_claim_safety.json` status=`blocked_formal_performance_claims`
  - `0_trials/module2_paper_readiness/module2_paper_readiness.json` status=`blocked`
  - `3_paper/module2_section_seed/module2_paper_section_seed.json` status=`blocked`
- paper blockers: `paper_tables_not_formal`, `h02_verdict_not_formal`, `h02_formal_acceptance_not_accepted`, `h01_manifest_not_ready`, `f02_6_warm_start_decision_pending`, `missing_module2_rl_rs_checkpoint`, `remote_execution_packet_not_ready`, `requires_dr_sun_approval`, `missing_gate3_formal_audit`, `h02_scale_below_h01_manifest`, `missing_ppo_result_rows`, `missing_remote_pullback_artifacts`, `f02_6_formal_chain_pending`, `claim_safety_blocks_formal_performance`, `f02_6_pending`

### warm_start_effect_blocked
- claim status: `blocked_placeholder_pending_f02_6`
- evidence state: `blocked_as_expected`
- mapping blockers: none
- evidence:
  - `0_trials/module2_paper_readiness/module2_paper_readiness.json` status=`blocked`
  - `3_paper/module2_section_seed/module2_paper_section_seed.json` status=`blocked`
  - `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json` status=`pending_human_decision`
  - `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json` status=`blocked_until_f02_6_decision`
- paper blockers: `f02_6_not_approved`, `requires_dr_sun_approval`, `f02_6_warm_start_decision_pending`, `missing_module2_rl_rs_checkpoint`

## Writing Boundaries

- Use this artifact as a claim-to-evidence map, not as a formal result.
- The method/system/no-warm units are mapped because their manuscript cues and upstream evidence are present.
- Formal result and warm-start units are mapped only as blocked placeholders; they are not paper claims yet.
- No local training is allowed; formal PPO checkpoint production remains gated on F02.6 and gpu3070ti-relay.
