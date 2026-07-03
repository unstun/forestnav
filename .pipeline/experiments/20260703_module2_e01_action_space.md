---
date: 2026-07-03
status: e01_4_action_space_complete
origin: codex+code
reviewed: false
task: Module2 E01.4
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_e01_observation_patch.md
source_head: b3c6d395
execution_host: MacBook-Pro.local
---

# Module2 E01.4 Forward-Only Action Space

## 直观结论

E01.4 已把 RL-RS v1 动作空间明确锁成 forward-only continuous steering:

- action 可以是实际 steering radian, 也可以是 normalized `[-1, 1]` 风格输出;
- normalized action 会按 `AckermannParams.max_steer` 解码;
- steering 会 clip 到车辆物理极限;
- 输出可以转换为 planner `MotionPrimitive`;
- direction 固定为 `+1`;
- reverse/direction gate 明确禁止, 不能在没有 C02 倒车必要性证据前偷偷启用。

这一步仍不实现 reward、policy training 或 planner integration。

## Code Changes

Changed files:

- `2_experiment/forest_n3p/rl_rs/actions.py`
- `2_experiment/forest_n3p/rl_rs/rollout.py`
- `2_experiment/forest_n3p/rl_rs/env.py`
- `2_experiment/forest_n3p/rl_rs/telemetry.py`
- `2_experiment/forest_n3p/rl_rs/__init__.py`
- `2_experiment/forest_n3p/tests/test_rl_rs_api.py`

New/updated API:

| Symbol | Meaning |
|---|---|
| `ActionConfig` | v1 action-space contract; `allow_reverse=True` raises |
| `SteeringAction.normalized` | marks policy output as normalized steering fraction |
| `decode_steering_action` | converts normalized action to physical steering radian |
| `clip_steering_action` | clips steering to `AckermannParams.max_steer` |
| `steering_action_to_primitive` | emits forward `MotionPrimitive(direction=1)` |
| `RolloutStepResult.primitive` | records planner primitive used by rollout |
| `RlRsStepTelemetry.primitive_direction` | telemetry records action direction |

## Tests

Tests added/extended:

- `test_action_config_is_forward_only_and_rejects_reverse_gate`
- `test_normalized_steering_action_decodes_and_converts_to_primitive`
- `test_rollout_step_uses_ackermann_sampling_and_checker`
- `test_env_reset_step_returns_telemetry_and_pending_reward_marker`

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
- `pytest`: `16 passed in 0.48s`
- `git diff --check`: pass

## Allowed Conclusions

- RL-RS v1 action schema is now explicit and test-covered.
- Forward-only MotionPrimitive conversion is available for later planner integration.
- Reverse action is explicitly disabled until evidence justifies a v2 contract/decision.

## Disallowed Conclusions

- Do not claim reverse maneuvers are supported.
- Do not claim policy training or action distribution is implemented.
- Do not claim planner integration exists.

## Next Step

Proceed to E01.5:

- formalize terminal conditions and failure metadata;
- keep success defined as terminal RS-connectable;
- add no-progress/oscillation metadata only after defining a testable signal.
