# Module2 Claim Safety

- Status: `blocked_formal_performance_claims`
- Formal performance claim allowed: `False`

## Formal Performance Blockers

- paper_tables_not_formal
- h02_verdict_not_formal
- h02_formal_acceptance_not_accepted
- h01_manifest_not_ready
- f02_6_warm_start_decision_pending
- missing_module2_rl_rs_checkpoint
- remote_execution_packet_not_ready
- requires_dr_sun_approval
- missing_gate3_formal_audit
- h02_scale_below_h01_manifest
- missing_ppo_result_rows
- missing_remote_pullback_artifacts
- f02_6_formal_chain_pending
- f02_6_pending
- formal_gate_closure_checklist_open

## Allowed Claims

- `method_is_ha_star_analytic_operator` (method_structure): Module2 implements a learned analytic-expansion operator inside Hybrid A*, with terminal RS certification and primitive fallback.
  - qualifier: Do not describe it as an end-to-end RL global planner.
- `no_warm_gate3_formal_failure` (no_warm_only): No-warm PPO Gate #3 formal trial failed: terminal-RS success rate was 0.453125 over 64 episodes, below threshold 0.8.
  - qualifier: This does not evaluate obstacle-summary warm-start PPO and does not reject the whole RL-RS direction.

## Conditional Claims

- `formal_performance_improvement`: blocked_until_formal_h02
- `warm_start_effect`: blocked_until_f02_6_and_remote_formal

## Prohibited Claims

- `global_optimality`: not allowed; patterns=全局最优, globally optimal, global optimality
- `completeness_enhancement`: not allowed; patterns=完备性增强, 提高完备性, completeness enhancement, improves completeness
- `rl_replaces_hybrid_astar`: not allowed; patterns=RL 替代 Hybrid A*, RL replaces Hybrid A*, replace Hybrid A*, 替代 Hybrid A*
- `universal_generalization`: not allowed; patterns=泛化到所有森林, all forest environments, universal generalization, generalizes to all
- `warm_start_approved`: not allowed; patterns=warm-start approved, 热启动已批准, obstacle-summary warm-start is approved

## Draft Audit

- status: `not_requested`

## Claim Boundaries

- Do not claim formal performance improvement until formal_performance_claim_allowed=true.
- No-warm Gate #3 failure is scoped to no-warm PPO only; it does not reject obstacle-summary warm-start.
- Method claims must say the learned policy is an analytic-expansion operator inside Hybrid A*, not a standalone global planner.
- Completeness/global-optimality/generalization claims are prohibited unless a future contract explicitly proves them.
- Formal PPO training/checkpoint production must run on gpu3070ti-relay or another explicitly approved remote GPU.
- Formal gate closure checklist must be closed before any formal performance claim is allowed.