---
date: 2026-07-03
status: e03_1_single_step_kinematics_complete
origin: codex+code
reviewed: false
task: Module2 E03.1
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_e02_reward_ablation_hooks.md
source_head: 654647d4
execution_host: MacBook-Pro.local
---

# Module2 E03.1 Single-Step Kinematics Test

## 直观结论

E03.1 已增加非零转向的单步运动学一致性测试。现在 RL-RS rollout 的 `next_state` 和最后一个 sampled pose 必须与 planner 的 `propagate()` 输出严格一致。

这一步很关键: RL 环境不能偷偷用另一套运动学近似。如果训练时 rollout 曲线和 planner 里的 Ackermann primitive 不一致, 后续 policy 即使训练成功, 接入 Hybrid A* 时也会出现 deployment mismatch。

## Code Changes

Changed files:

- `2_experiment/forest_n3p/tests/test_rl_rs_api.py`

New test:

- `test_rollout_step_matches_planner_propagate_for_curved_action`

The test uses `SteeringAction(0.2)` and compares:

- `RolloutStepResult.next_state.x/y/theta`;
- `RolloutStepResult.samples[-1].x/y/theta`;
- planner-source `propagate(...).x/y/theta`。

Tolerance is `1e-12`, so this is formula-level alignment, not a loose smoke test.

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
- `pytest`: `21 passed in 0.45s`
- `git diff --check`: pass

## Allowed Conclusions

- RL-RS rollout single-step kinematics are test-locked against planner `propagate()`.
- Nonzero steering curved motion is covered, not only straight-line movement.

## Disallowed Conclusions

- Do not claim all collision semantics are covered. That is E03.2.
- Do not claim success-set tests are complete. That is E03.3.
- Do not claim planner integration exists.

## Next Step

Proceed to E03.2:

- verify env rollout collision and planner checker collision agree on the same pose/path;
- include at least one free path and one colliding path;
- keep checker semantics tied to the shared `GridFootprintChecker`.
