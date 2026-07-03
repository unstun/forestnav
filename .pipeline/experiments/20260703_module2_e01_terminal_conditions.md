---
date: 2026-07-03
status: e01_5_terminal_conditions_complete
origin: codex+code
reviewed: false
task: Module2 E01.5
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_e01_action_space.md
source_head: 742f2b55
execution_host: MacBook-Pro.local
---

# Module2 E01.5 Terminal Conditions

## 直观结论

E01.5 已把 RL-RS 环境的 episode 结束语义从 "跑到 budget 结束" 加固成可审计的 planner-side terminal contract:

- success 仍严格定义为当前 rollout state 能通过 terminal RS 无碰撞接到 final goal;
- rollout segment 碰撞直接 `terminated`;
- budget exhausted 且 terminal RS 仍失败时 `truncated`, failure reason 写成 `no_rs_terminal:<detail>`;
- 连续没有朝目标取得最小进展时提前 `truncated`, failure reason 写成 `no_progress`;
- telemetry/info 显式带出 `goal_distance_m`, `progress_to_goal_m`, `no_progress_count`。

这一步没有把 `oscillation` 写成已完成。原因是 oscillation 需要 E03.4 单独定义可测试信号, 例如 steering sign flip、pose displacement、heading change 与 budget window 的组合。现在硬写一个字符串会制造不可审计的假终止条件。

## Code Changes

Changed files:

- `2_experiment/forest_n3p/rl_rs/env.py`
- `2_experiment/forest_n3p/rl_rs/telemetry.py`
- `2_experiment/forest_n3p/tests/test_rl_rs_api.py`

New/updated behavior:

| Behavior | Implementation surface |
|---|---|
| Track current distance to final goal | `AnalyticExpansionEnv._last_goal_distance_m` |
| Measure per-step progress | `progress_to_goal_m = previous_goal_distance - current_goal_distance` |
| Count no-progress streak | `AnalyticExpansionEnv._no_progress_count` |
| Configure no-progress gate | `AnalyticExpansionContext.min_progress_m`, `no_progress_patience` |
| Expose terminal metadata | `AnalyticExpansionStep.info`, `RlRsStepTelemetry` |

## Tests

Tests added/extended:

- `test_env_reset_step_returns_telemetry_and_pending_reward_marker`
- `test_env_step_truncates_on_no_progress_before_budget_exhausted`

Existing E01 terminal tests still cover:

- `test_env_step_terminates_on_rollout_collision_and_blocks_followup_step`
- `test_env_step_terminates_on_terminal_rs_success`
- `test_env_step_truncates_with_no_terminal_rs_when_budget_exhausted`

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
- `pytest`: `17 passed in 0.47s`
- `git diff --check`: pass

## Allowed Conclusions

- RL-RS environment terminal semantics now distinguish success, collision, no-terminal-RS truncation, and no-progress truncation.
- Goal-distance progress is now recorded in telemetry and available to later reward/diagnostic code.
- No-progress is configurable and test-covered.

## Disallowed Conclusions

- Do not claim oscillation detection is implemented.
- Do not claim E02 reward is implemented.
- Do not claim PPO/BC training exists.
- Do not claim planner integration exists.
- Do not claim no-progress is a complete anti-loop policy; it is a minimal terminal guard pending E03.4.

## Next Step

Proceed to E02.1:

- define success reward from terminal RS-connectability, not arbitrary Euclidean distance;
- keep reward terms decomposed for ablation and paper tables;
- preserve E01 terminal metadata as reward/debug input rather than hiding it in scalar reward.
