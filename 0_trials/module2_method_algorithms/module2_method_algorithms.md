# Module2 Method Algorithms

- Status: `code_anchored`
- Source head: `c4745347b1a379b04072eba9c9a1f4078971017b`
- Formal claim allowed: `False`
- Local training allowed: `False`
- Remote training resource: `gpu3070ti-relay`

## Claim Boundaries

- This artifact is a code-anchored method description, not a formal result.
- F02.6 warm-start decision remains pending; formal PPO runs must not be claimed until that decision is approved and logged.
- Local PPO training is disallowed; formal training must run on gpu3070ti-relay or another explicitly approved remote GPU.
- The ppo_analytic_operator and ppo_rs_funnel paper claims remain blocked until a real RL-RS checkpoint is available.
- Algorithm 1 includes fallback semantics: returning None from the custom operator does not mean planner failure; it hands control back to normal Hybrid A* expansion.

## Algorithm 1: RL-RS funnel analytic expansion inside Hybrid A*

Intent: Replace the hand-crafted analytic RS expansion attempt with a learned steering rollout, then certify the rollout end with terminal RS before accepting the shortcut.

Paper claim: The learned component is an analytic-expansion operator, not a standalone global planner.

| Step | Action | Code anchors |
| --- | --- | --- |
| `A1.1` | Instantiate HybridAStarPlanner with a custom analytic_expansion_operator; the planner records the operator name and routes analytic expansion attempts through the custom hook. | `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:129` `HybridAStarPlanner.__init__`<br>`2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:175` `HybridAStarPlanner.__init__`<br>`2_experiment/forest_n3p/main_evaluation.py:70` `main_evaluation.RL_RS_OPERATOR_METHODS` |
| `A1.2` | During analytic expansion, dispatch to HybridAStarPlanner._try_custom_analytic_expansion when a custom operator exists. | `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:296` `HybridAStarPlanner._try_analytic_expansion`<br>`2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:301` `HybridAStarPlanner._try_custom_analytic_expansion` |
| `A1.3` | Load a checkpoint-backed policy into RlRsFunnelOperator; the checkpoint SHA256 is captured as method provenance. | `2_experiment/forest_n3p/rl_rs/checkpoint_operator.py:55` `load_rl_rs_funnel_operator_from_checkpoint`<br>`2_experiment/forest_n3p/rl_rs/checkpoint_operator.py:77` `load_rl_rs_funnel_operator_from_checkpoint`<br>`2_experiment/forest_n3p/rl_rs/checkpoint_operator.py:85` `load_rl_rs_funnel_operator_from_checkpoint` |
| `A1.4` | Convert the current Hybrid A* node and goal into AnalyticExpansionContext, reset AnalyticExpansionEnv, and start the rollout from the planner state. | `2_experiment/forest_n3p/rl_rs/operator.py:62` `RlRsFunnelOperator.try_connect`<br>`2_experiment/forest_n3p/rl_rs/operator.py:68` `RlRsFunnelOperator.try_connect`<br>`2_experiment/forest_n3p/rl_rs/operator.py:70` `RlRsFunnelOperator.try_connect`<br>`2_experiment/forest_n3p/rl_rs/env.py:156` `AnalyticExpansionEnv.reset` |
| `A1.5` | Iteratively query the RL action policy, apply one constant-steer primitive, update observation, and stop only on terminal/truncated signals. | `2_experiment/forest_n3p/rl_rs/operator.py:77` `RlRsFunnelOperator.try_connect`<br>`2_experiment/forest_n3p/rl_rs/operator.py:78` `RlRsFunnelOperator.try_connect`<br>`2_experiment/forest_n3p/rl_rs/env.py:179` `AnalyticExpansionEnv.step`<br>`2_experiment/forest_n3p/rl_rs/env.py:191` `AnalyticExpansionEnv.step` |
| `A1.6` | Use terminal RS as the acceptance certificate for the learned rollout when append_terminal_rs is enabled. | `2_experiment/forest_n3p/rl_rs/env.py:211` `AnalyticExpansionEnv.step`<br>`2_experiment/forest_n3p/rl_rs/terminal.py:21` `check_terminal_rs_connectable`<br>`2_experiment/forest_n3p/rl_rs/operator.py:102` `RlRsFunnelOperator.try_connect`<br>`2_experiment/forest_n3p/rl_rs/operator.py:129` `RlRsFunnelOperator.try_connect` |
| `A1.7` | Record fallback_to_builtin_search_on_none: if the learned/terminal-RS operator cannot certify a shortcut, it returns None and Hybrid A* continues normal search instead of accepting an unsafe path. | `2_experiment/forest_n3p/rl_rs/operator.py:99` `RlRsFunnelOperator.try_connect`<br>`2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:302` `HybridAStarPlanner._try_custom_analytic_expansion`<br>`2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:304` `HybridAStarPlanner._try_custom_analytic_expansion` |
| `A1.8` | Expose two formal method variants: ppo_rs_funnel keeps terminal RS appended, while ppo_analytic_operator disables terminal RS append and evaluates the learned operator alone. | `2_experiment/forest_n3p/main_evaluation.py:772` `_run_hybrid_a_operator`<br>`2_experiment/forest_n3p/main_evaluation.py:885` `_load_module2_rl_rs_operator`<br>`2_experiment/forest_n3p/main_evaluation.py:775` `_run_hybrid_a_operator`<br>`2_experiment/forest_n3p/main_evaluation.py:902` `_load_module2_ppo_analytic_operator` |

## Algorithm 2: PPO training environment for analytic expansion

Intent: Train a continuous steering policy on the same planner-side analytic expansion surface used at evaluation time.

Paper claim: The environment optimizes a local analytic-expansion policy with terminal-RS-aware reward shaping; it is not a separate end-to-end navigation policy.

| Step | Action | Code anchors |
| --- | --- | --- |
| `A2.1` | Create a GymAnalyticExpansionEnv around a context sampler; reset samples an AnalyticExpansionContext and forwards it to the planner-side environment. | `2_experiment/forest_n3p/rl_rs/gym_env.py:26` `GymAnalyticExpansionEnv`<br>`2_experiment/forest_n3p/rl_rs/gym_env.py:70` `GymAnalyticExpansionEnv.reset`<br>`2_experiment/forest_n3p/rl_rs/gym_env.py:73` `GymAnalyticExpansionEnv.reset` |
| `A2.2` | Represent observations as scalar geometry plus an egocentric occupancy/EDT patch. | `2_experiment/forest_n3p/rl_rs/obs.py:14` `ObservationConfig`<br>`2_experiment/forest_n3p/rl_rs/obs.py:37` `build_scalar_observation`<br>`2_experiment/forest_n3p/rl_rs/obs.py:85` `build_patch_observation`<br>`2_experiment/forest_n3p/rl_rs/obs.py:100` `build_observation` |
| `A2.3` | Define a single continuous normalized steering action and apply it through the same AnalyticExpansionEnv.step used by Algorithm 1. | `2_experiment/forest_n3p/rl_rs/gym_env.py:40` `GymAnalyticExpansionEnv.__init__`<br>`2_experiment/forest_n3p/rl_rs/gym_env.py:81` `GymAnalyticExpansionEnv.step`<br>`2_experiment/forest_n3p/rl_rs/gym_env.py:82` `GymAnalyticExpansionEnv.step`<br>`2_experiment/forest_n3p/rl_rs/env.py:179` `AnalyticExpansionEnv.step` |
| `A2.4` | Evaluate each rollout primitive with collision checks, no-progress/oscillation truncation, and terminal RS reachability. | `2_experiment/forest_n3p/rl_rs/env.py:191` `AnalyticExpansionEnv.step`<br>`2_experiment/forest_n3p/rl_rs/env.py:242` `AnalyticExpansionEnv.step`<br>`2_experiment/forest_n3p/rl_rs/env.py:251` `AnalyticExpansionEnv.step`<br>`2_experiment/forest_n3p/rl_rs/terminal.py:21` `check_terminal_rs_connectable` |
| `A2.5` | Compute decomposed reward terms for success, terminal failure, collision, goal progress, RS-distance progress, clearance, curvature change, path length, and step cost. | `2_experiment/forest_n3p/rl_rs/env.py:314` `AnalyticExpansionEnv.step`<br>`2_experiment/forest_n3p/rl_rs/reward.py:129` `compute_decomposed_reward`<br>`2_experiment/forest_n3p/rl_rs/reward.py:152` `compute_decomposed_reward` |
| `A2.6` | Return Gymnasium observation, scalar reward, terminated/truncated flags, and telemetry info for PPO training logs. | `2_experiment/forest_n3p/rl_rs/gym_env.py:84` `GymAnalyticExpansionEnv.step`<br>`2_experiment/forest_n3p/rl_rs/gym_env.py:85` `GymAnalyticExpansionEnv.step`<br>`2_experiment/forest_n3p/rl_rs/gym_env.py:88` `GymAnalyticExpansionEnv.step` |
| `A2.7` | Enforce local_training_disallowed for this artifact: it documents the code contract only; PPO execution belongs on gpu3070ti-relay after F02.6 approval. | `2_experiment/forest_n3p/rl_rs/gym_env.py:26` `GymAnalyticExpansionEnv`<br>`2_experiment/forest_n3p/rl_rs/reward.py:129` `compute_decomposed_reward` |
