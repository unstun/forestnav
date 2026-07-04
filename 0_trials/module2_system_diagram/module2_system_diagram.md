# Module2 System Diagram

- Status: `code_anchored_drawio`
- Source head: `c71851c7dd3520d153ae91e781e36dc758ce6878`
- Figure: Figure: RL-RS analytic expansion system inside Hybrid A*
- Formal claim allowed: `False`
- Local training allowed: `False`
- Remote training resource: `gpu3070ti-relay`

## Figure Caption

Figure: RL-RS analytic expansion system inside Hybrid A*. The learned policy is used only as an analytic-expansion operator. A terminal RS certificate is required before accepting the shortcut; otherwise the planner falls back to primitive expansion.

## Nodes And Anchors

| Node | Role | Code anchors |
| --- | --- | --- |
| `hybrid_astar_loop` | Hybrid A* search loop: Open/closed search; primitive fallback remains authoritative | `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:620` `HybridAStarPlanner.plan`<br>`2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:781` `HybridAStarPlanner.plan` |
| `analytic_trigger` | Analytic expansion trigger: Distance-scaled interval decides when to try a shortcut | `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:287` `HybridAStarPlanner._analytic_interval`<br>`2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:726` `HybridAStarPlanner.plan` |
| `custom_operator_dispatch` | Custom analytic operator dispatch: Call custom operator when provided; otherwise built-in RS | `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:129` `HybridAStarPlanner.__init__`<br>`2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:296` `HybridAStarPlanner._try_analytic_expansion`<br>`2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:301` `HybridAStarPlanner._try_custom_analytic_expansion` |
| `rl_rs_funnel_operator` | RL-RS funnel operator: Checkpoint policy rolls out timed steering from current HA* node | `2_experiment/forest_n3p/rl_rs/operator.py:67` `RlRsFunnelOperator`<br>`2_experiment/forest_n3p/rl_rs/operator.py:81` `RlRsFunnelOperator.try_connect`<br>`2_experiment/forest_n3p/rl_rs/operator.py:99` `RlRsFunnelOperator.try_connect` |
| `rl_rollout_env` | Planner-side RL rollout env: Shared Ackermann rollout, collision, no-progress, reward terms | `2_experiment/forest_n3p/rl_rs/env.py:135` `AnalyticExpansionEnv`<br>`2_experiment/forest_n3p/rl_rs/env.py:156` `AnalyticExpansionEnv.reset`<br>`2_experiment/forest_n3p/rl_rs/env.py:179` `AnalyticExpansionEnv.step`<br>`2_experiment/forest_n3p/rl_rs/env.py:320` `AnalyticExpansionEnv.step` |
| `terminal_rs_certificate` | Terminal RS certificate: Only accept a learned shortcut after RS-connectable check | `2_experiment/forest_n3p/rl_rs/env.py:215` `AnalyticExpansionEnv.step`<br>`2_experiment/forest_n3p/rl_rs/terminal.py:21` `check_terminal_rs_connectable`<br>`2_experiment/forest_n3p/rl_rs/operator.py:126` `RlRsFunnelOperator.try_connect` |
| `accept_shortcut` | Accept shortcut: Return states/actions to HA* trace path when certified | `2_experiment/forest_n3p/rl_rs/operator.py:116` `RlRsFunnelOperator.try_connect`<br>`2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:306` `HybridAStarPlanner._try_custom_analytic_expansion` |
| `fallback_primitives` | Fallback primitive expansion: None means no certified shortcut; HA* continues primitive search | `2_experiment/forest_n3p/rl_rs/operator.py:123` `RlRsFunnelOperator.try_connect`<br>`2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:302` `HybridAStarPlanner._try_custom_analytic_expansion`<br>`2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:781` `HybridAStarPlanner.plan` |
| `gym_training_env` | PPO training environment: Gym adapter: scalar + occupancy/EDT patch, single steering action | `2_experiment/forest_n3p/rl_rs/gym_env.py:26` `GymAnalyticExpansionEnv`<br>`2_experiment/forest_n3p/rl_rs/gym_env.py:40` `GymAnalyticExpansionEnv.__init__`<br>`2_experiment/forest_n3p/rl_rs/obs.py:100` `build_observation`<br>`2_experiment/forest_n3p/rl_rs/reward.py:129` `compute_decomposed_reward` |
| `checkpointed_policy` | Checkpointed policy variants: BC ready; PPO checkpoint missing until remote formal training | `2_experiment/forest_n3p/rl_rs/checkpoint_operator.py:55` `load_rl_rs_funnel_operator_from_checkpoint`<br>`2_experiment/forest_n3p/rl_rs/checkpoint_operator.py:100` `load_bc_funnel_operator_from_checkpoint`<br>`2_experiment/forest_n3p/main_evaluation.py:70` `main_evaluation.RL_RS_OPERATOR_METHODS` |
| `formal_evaluation_boundary` | Formal evaluation boundary: H01/H02 blocked: F02.6 pending + PPO checkpoint missing | `2_experiment/forest_n3p/main_evaluation.py:772` `_run_hybrid_a_operator`<br>`2_experiment/forest_n3p/main_evaluation.py:775` `_run_hybrid_a_operator`<br>`2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py:371` `build_module2_evaluation_manifest` |

## Claim Boundaries

- This system diagram is a code-anchored method artifact, not a formal result.
- F02.6 warm-start decision remains pending; obstacle-summary warm-start is not approved until Dr Sun closes that decision.
- The ppo_analytic_operator and ppo_rs_funnel branches still require a real PPO checkpoint before formal H01/H02 evaluation.
- Local PPO training is disallowed; formal training must run on gpu3070ti-relay or another explicitly approved remote GPU.
- Fallback primitive expansion is part of the safety semantics: a custom operator returning None must not be relabeled as planner failure.

Draw.io file: `0_trials/module2_system_diagram/module2_system_diagram.drawio`.