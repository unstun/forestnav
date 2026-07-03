---
date: 2026-07-03
status: e02_2_reward_shaping_terms_complete
origin: codex+code
reviewed: false
task: Module2 E02.2
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_e02_success_reward.md
source_head: 2bb12651
execution_host: MacBook-Pro.local
---

# Module2 E02.2 Decomposed Reward Shaping Terms

## 直观结论

E02.2 已把 reward 从单一 success bonus 扩展成可审计的分项结构。现在每个 env step 都能在 `step.info` 里看到:

- terminal RS success bonus;
- terminal failure penalty (`no_rs_terminal`, `no_progress`);
- rollout collision penalty;
- Euclidean goal-distance progress;
- Reeds-Shepp path-length progress;
- minimum rollout clearance reward;
- curvature-rate penalty;
- rollout path-length penalty;
- per-step penalty。

这一步的重点是让 reward 分项可读、可测、可记录, 而不是宣称权重已经调优。默认配置只主动使用 terminal success、collision、terminal failure/no-progress penalty; progress/clearance/curvature/path-length/step shaping 都有实现和测试, 但需要显式配置非零权重。这样 E02.2 不会把未调参的 shaping 伪装成最终训练配方。

## Code Changes

Changed files:

- `2_experiment/forest_n3p/rl_rs/reward.py`
- `2_experiment/forest_n3p/rl_rs/env.py`
- `2_experiment/forest_n3p/rl_rs/__init__.py`
- `2_experiment/forest_n3p/tests/test_rl_rs_api.py`

New/updated API:

| Symbol | Meaning |
|---|---|
| `RewardConfig.collision_penalty` | collision terminal penalty |
| `RewardConfig.terminal_rs_failure_penalty` | budget/no-terminal-RS penalty |
| `RewardConfig.no_progress_penalty` | no-progress truncation penalty |
| `RewardConfig.distance_progress_scale` | Euclidean distance-progress weight |
| `RewardConfig.rs_distance_progress_scale` | Reeds-Shepp path-length progress weight |
| `RewardConfig.clearance_scale` / `clearance_target_m` | normalized minimum-clearance reward |
| `RewardConfig.curvature_rate_penalty_scale` | penalty on curvature change |
| `RewardConfig.path_length_penalty_scale` | rollout segment length penalty |
| `RewardConfig.step_penalty` | per-step penalty |
| `compute_decomposed_reward` | combines all active reward terms |
| `build_clearance_distance_field` | grid-map EDT + boundary-distance field |
| `min_rollout_clearance_m` | two-circle footprint minimum clearance over rollout samples |
| `RewardBreakdown.to_record()` | structured `info["reward_terms"]` payload |

## Implementation Notes

- Clearance uses the same `GridMap` occupancy and `TwoCircleFootprint.circle_centers()` geometry as planner-side collision checking.
- RS-distance progress is computed from Reeds-Shepp path length when available. If terminal RS is not checked or path generation fails, the term is `0.0` and previous RS-distance state is not updated.
- Curvature-rate penalty uses bicycle curvature `tan(steering) / wheelbase`, not raw steering angle alone.
- `step.info` now exposes both `reward_total` and `reward_terms`, so training logs do not have to reverse-engineer the scalar reward.

## Tests

Tests added/extended:

- `test_env_reset_step_returns_telemetry_and_reward_marker`
- `test_env_step_terminates_on_rollout_collision_and_blocks_followup_step`
- `test_reward_breakdown_records_configured_shaping_terms`
- `test_env_step_truncates_with_no_terminal_rs_when_budget_exhausted`
- `test_env_step_truncates_on_no_progress_before_budget_exhausted`

The shaping test enables all shaping weights and asserts nonzero/structured terms for distance progress, RS-distance progress, clearance, curvature-rate, path length, and step penalty.

## Verification

Commands:

```bash
PYTHONPATH=2_experiment python -m py_compile \
  2_experiment/forest_n3p/rl_rs/*.py \
  2_experiment/forest_n3p/scripts/run_policy_forward_budget.py \
  2_experiment/forest_n3p/scripts/run_rollout_collision_budget.py

PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_policy_forward_budget.py \
  2_experiment/forest_n3p/tests/test_rollout_collision_budget.py \
  2_experiment/forest_n3p/tests/test_rl_rs_api.py \
  -q

git diff --check
```

Results:

- `py_compile`: pass
- `pytest`: `19 passed in 0.48s`
- `git diff --check`: pass

## Allowed Conclusions

- E02 reward shaping terms are now implemented as independent, inspectable components.
- Reward terms are available through `step.info["reward_terms"]`.
- Collision, no-terminal-RS, and no-progress penalties are active by default.
- Progress, RS-progress, clearance, curvature-rate, path-length, and step terms are implemented and configurable.

## Disallowed Conclusions

- Do not claim reward weights are tuned.
- Do not claim E02.3 ablation hooks are complete.
- Do not claim PPO/BC training is enabled.
- Do not claim planner integration exists.
- Do not claim oscillation detection is implemented.

## Next Step

Proceed to E02.3:

- expose explicit reward-term ablation switches;
- record ablation configuration in env metadata/info;
- keep each term independently disable-able for later paper tables.
