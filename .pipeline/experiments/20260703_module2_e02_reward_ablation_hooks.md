---
date: 2026-07-03
status: e02_3_reward_ablation_hooks_complete
origin: codex+code
reviewed: false
task: Module2 E02.3
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_e02_reward_shaping_terms.md
source_head: a2cdf379
execution_host: MacBook-Pro.local
---

# Module2 E02.3 Reward Ablation Hooks

## 直观结论

E02.3 已给每个 reward term 增加显式消融开关。现在不能只靠 "把权重设成 0" 来推断某个 reward term 是否参与训练; `RewardConfig.enabled_terms` 会直接记录每一项是否开启, 并通过 `step.info["reward_ablation"]` 暴露给训练日志和后续论文表格。

当前可开关项:

- `success`
- `terminal`
- `collision`
- `progress`
- `rs_progress`
- `clearance`
- `curvature`
- `path_length`
- `step`

这一步只完成 reward ablation hooks, 不代表权重已经调优, 也不代表 PPO/BC 可以开始。

## Code Changes

Changed files:

- `2_experiment/forest_n3p/rl_rs/reward.py`
- `2_experiment/forest_n3p/rl_rs/env.py`
- `2_experiment/forest_n3p/rl_rs/__init__.py`
- `2_experiment/forest_n3p/tests/test_rl_rs_api.py`

New/updated API:

| Symbol | Meaning |
|---|---|
| `RewardTermSwitches` | explicit per-term boolean switches |
| `RewardConfig.enabled_terms` | stores reward ablation configuration |
| `RewardBreakdown.ablation_record()` | returns enabled/disabled map |
| `step.info["reward_ablation"]` | training-log-ready ablation metadata |

## Tests

Tests added/extended:

- `test_env_reset_step_returns_telemetry_and_reward_marker`
- `test_reward_ablation_switches_disable_selected_terms`

The ablation test creates a terminal-RS-success step with positive progress and nonzero shaping weights, then disables selected terms. It verifies:

- terminal RS success remains true;
- telemetry still reports positive progress;
- disabled reward terms are exactly zero;
- enabled `step` term remains active;
- `step.info["reward_ablation"]` records the disabled/enabled state.

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
- `pytest`: `20 passed in 0.45s`
- `git diff --check`: pass

## Allowed Conclusions

- Every current reward term now has an explicit ablation switch.
- The ablation state is visible in `step.info`.
- Reward ablation metadata is ready for future training/evaluation logs.

## Disallowed Conclusions

- Do not claim reward weights are tuned.
- Do not claim any ablation experiment has been run.
- Do not claim PPO/BC training is enabled.
- Do not claim planner integration exists.
- Do not claim RL-RS is faster or better.

## Next Step

Proceed to E03.1:

- add an explicit single-step kinematics test;
- verify RL-RS rollout state matches planner `propagate()` / `sample_constant_steer_motion()` semantics;
- keep this as environment correctness, not training.
