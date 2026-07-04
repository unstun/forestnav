# Module2 Paper Section Seed

- status: `method_sections_ready_results_blocked`
- local training allowed: `False`
- remote training resource: `gpu3070ti-relay`
- draft audit: `clean`

## Allowed Draft Sections

### methods_rl_rs_operator
- status: `draft_ready`
- evidence: `0_trials/module2_method_algorithms/module2_method_algorithms.json`
- blockers: `none`

Module2 is implemented as a learned analytic-expansion operator inside the existing Hybrid A* search loop. The operator is invoked only at the planner's analytic-expansion hook; it rolls out steering actions from the current search node, then accepts a shortcut only when the terminal Reeds-Shepp check certifies a collision-free connection to the goal. If this certificate is absent, the operator returns no shortcut and Hybrid A* continues primitive expansion. This section should therefore describe a planner-side analytic operator with fallback semantics, not a standalone global planner.

### system_figure_caption
- status: `draft_ready`
- evidence: `0_trials/module2_system_diagram/module2_system_diagram.json`
- blockers: `none`

Figure caption seed: RL-RS analytic expansion is placed inside the Hybrid A* loop. The figure should show the analytic trigger, custom operator dispatch, checkpoint-policy rollout, terminal RS certificate, accepted shortcut path, and fallback primitive expansion. The visual boundary is important: the learned policy proposes a local analytic expansion, while Hybrid A* remains the global search authority.

### no_warm_gate3_failure_note
- status: `draft_ready_with_scope_limit`
- evidence: `0_trials/module2_claim_safety/module2_claim_safety.json, 0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/gate3_formal_audit.json`
- blockers: `none`

No-warm PPO Gate #3 formal trial failed: terminal-RS success rate was 0.453125 over 64 episodes, below threshold 0.8. This does not evaluate obstacle-summary warm-start PPO and does not reject the whole RL-RS direction. This scoped result can be used as a negative training-dynamics observation, not as evidence against the approved-or-pending warm-start branch. Formal performance claims remain blocked.

### formal_results
- status: `blocked`
- evidence: `0_trials/module2_claim_safety/module2_claim_safety.json, 0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json, 0_trials/module2_paper_tables/module2_paper_tables.json`
- blockers: `paper_tables_not_formal, h02_verdict_not_formal, h02_formal_acceptance_not_accepted, h01_manifest_not_ready, f02_6_warm_start_decision_pending, missing_module2_rl_rs_checkpoint, remote_execution_packet_not_ready, requires_dr_sun_approval, missing_gate3_formal_audit, h02_scale_below_h01_manifest, missing_ppo_result_rows, missing_remote_pullback_artifacts, f02_6_formal_chain_pending, claim_safety_blocks_formal_performance, f02_6_pending`

### warm_start_effect
- status: `blocked`
- evidence: `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json, 0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json`
- blockers: `f02_6_not_approved, requires_dr_sun_approval, f02_6_warm_start_decision_pending, missing_module2_rl_rs_checkpoint`

## Writing Boundaries

- These drafts may seed paper Methods and scoped failure text only.
- Formal performance claims remain blocked until H02 formal acceptance and claim safety both pass.
- Warm-start effect text remains blocked until F02.6 closes and a gpu3070ti-relay formal run is audited and pulled back.
- Do not describe Module2 as a standalone RL planner or as a replacement for Hybrid A*.
