---
date: 2026-07-03
status: e03_2_collision_consistency_complete
origin: codex+code
reviewed: false
task: Module2 E03.2
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_e03_single_step_kinematics.md
source_head: b9688e02
execution_host: MacBook-Pro.local
---

# Module2 E03.2 Collision Consistency Test

## 直观结论

E03.2 已增加 rollout collision 与 planner checker 的一致性测试。现在同一条 rollout samples 会被两边用同一个 `GridFootprintChecker` 语义判断, 并覆盖:

- free path: rollout 不碰撞, checker 也不碰撞;
- blocked path: rollout 碰撞, checker 也碰撞。

这一步防止 RL 环境训练时用一套碰撞判断、planner 接入时又用另一套判断。

## Code Changes

Changed files:

- `2_experiment/forest_n3p/tests/test_rl_rs_api.py`

New test:

- `test_rollout_collision_matches_planner_checker_for_free_and_blocked_paths`

The test compares:

- `RolloutStepResult.collided`;
- direct `GridFootprintChecker.collides_path(RolloutStepResult.samples)`。

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
- `pytest`: `22 passed in 0.47s`
- `git diff --check`: pass

## Allowed Conclusions

- RL-RS rollout collision flag is test-locked to shared planner checker semantics for free and blocked local paths.

## Disallowed Conclusions

- Do not claim terminal success-set behavior is fully covered. That is E03.3.
- Do not claim oscillation/no-progress test coverage is complete. That is E03.4.
- Do not claim planner integration exists.

## Next Step

Proceed to E03.3:

- construct terminal RS success and terminal RS blocked cases;
- verify `TerminalRsCheckResult.success`, env termination, and reward success behavior agree.
