---
date: 2026-07-03
status: e02_1_success_reward_complete
origin: codex+code
reviewed: false
task: Module2 E02.1
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_e01_terminal_conditions.md
source_head: 65e33505
execution_host: MacBook-Pro.local
---

# Module2 E02.1 Terminal-RS Success Reward

## 直观结论

E02.1 已把 RL-RS 环境的 success reward 绑定到部署时真正需要的事件:

- policy rollout 后的当前 state 能通过 terminal RS 无碰撞接到 final goal;
- reward 不使用 "离目标距离小于阈值" 作为成功替代;
- terminal RS success 即使还有非零欧氏距离, 也给 success reward;
- 未执行 terminal RS check、terminal RS 失败、rollout collision 都不给 success reward。

这一步只完成 success reward。collision penalty、progress shaping、clearance、curvature-rate、step penalty 和 reward ablation hook 仍属于 E02.2/E02.3。

## Code Changes

Changed files:

- `2_experiment/forest_n3p/rl_rs/reward.py`
- `2_experiment/forest_n3p/rl_rs/env.py`
- `2_experiment/forest_n3p/rl_rs/__init__.py`
- `2_experiment/forest_n3p/tests/test_rl_rs_api.py`

New/updated API:

| Symbol | Meaning |
|---|---|
| `RewardConfig.terminal_rs_success` | configurable terminal-RS success reward weight |
| `compute_terminal_success_reward` | computes success term from `TerminalRsCheckResult.success` |
| `RewardBreakdown.status` | exposes current reward protocol in `step.info["reward_status"]` |
| `AnalyticExpansionContext.reward_config` | planner/env context carries reward protocol settings |

## Tests

Tests added/extended:

- `test_env_reset_step_returns_telemetry_and_reward_marker`
- `test_env_step_terminates_on_terminal_rs_success`
- `test_reward_config_controls_terminal_rs_success_reward`

The terminal success test asserts `goal_distance_m > 0.0` while `reward.success == 1.0`, which locks the key E02.1 distinction: success reward follows terminal RS-connectability, not exact goal distance.

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
- `pytest`: `18 passed in 0.49s`
- `git diff --check`: pass

## Allowed Conclusions

- E02 reward no longer uses the E01 placeholder in active env steps.
- The success reward is deployment-aligned with terminal RS-connectability.
- Reward weight is configurable through `AnalyticExpansionContext.reward_config`.

## Disallowed Conclusions

- Do not claim reward shaping is complete.
- Do not claim collision/no-progress penalties are implemented.
- Do not claim reward ablation hooks are implemented.
- Do not claim PPO/BC training is enabled.
- Do not claim planner integration exists.

## Next Step

Proceed to E02.2:

- add decomposed shaping terms to `RewardBreakdown`;
- write every active term into `info`;
- keep each term individually testable so E02.3 can expose ablation switches.
