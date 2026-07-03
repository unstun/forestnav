---
date: 2026-07-03
status: e01_3_observation_patch_complete
origin: codex+code
reviewed: false
task: Module2 E01.3
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_e01_env_state_machine.md
source_head: 1f0e9df6
execution_host: MacBook-Pro.local
---

# Module2 E01.3 Egocentric Observation Patch

## 直观结论

E01.3 已实现 RL-RS 环境的观测 patch:

- 主通道: egocentric occupancy patch;
- 辅通道: normalized EDT/distance-field patch;
- scalar: 保留 E01.1/E01.2 的 relative goal / heading / budget 8 维向量;
- env reset/step 返回的 `RlRsObservation.patch` 现在默认是 `(2, 64, 64)`。

关键语义:

- patch 坐标系是机器人坐标系, forward 为 +x。
- 同一个“机器人前方障碍”在不同世界朝向下会落到同一个 patch cell。
- 越界区域按 occupied 处理, 避免边界外被误当成 free space。
- EDT 通道按米计算后用 `edt_clip_m` 裁剪归一化, 避免网络输入尺度无界。

## Code Changes

Changed files:

- `2_experiment/forest_n3p/rl_rs/obs.py`
- `2_experiment/forest_n3p/rl_rs/env.py`
- `2_experiment/forest_n3p/rl_rs/__init__.py`
- `2_experiment/forest_n3p/tests/test_rl_rs_api.py`

New/updated API:

| Symbol | Meaning |
|---|---|
| `ObservationConfig.patch_size_m` | local egocentric support, default `6.4m` from D02.1 annulus budget |
| `ObservationConfig.patch_cells` | raster cells, default `64` |
| `ObservationConfig.include_edt` | include distance-field channel |
| `ObservationConfig.edt_clip_m` | EDT normalization clip distance |
| `build_egocentric_occupancy_patch` | occupancy raster in robot frame |
| `build_egocentric_edt_patch` | normalized EDT raster in robot frame |
| `build_patch_observation` | stacked `(C,H,W)` float32 patch |
| `RlRsObservation.patch` | optional patch attached to scalar observation |

## Tests

Tests added/extended in `2_experiment/forest_n3p/tests/test_rl_rs_api.py`:

| Behavior | Test |
|---|---|
| Env reset returns `(2,5,5)` patch under small test config | `test_env_reset_step_returns_telemetry_and_pending_reward_marker` |
| Forward obstacle aligns under east/north robot headings | `test_egocentric_occupancy_patch_aligns_obstacle_in_robot_frame` |
| Out-of-bounds cells are occupied | `test_egocentric_patch_marks_out_of_bounds_as_occupied` |
| Occupancy and normalized EDT channels stack correctly | `test_patch_observation_stacks_occupancy_and_normalized_edt_channels` |

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
- `pytest`: `14 passed in 0.43s`
- `git diff --check`: pass

## Allowed Conclusions

- RL-RS observation now includes real occupancy and EDT patch channels.
- Patch orientation and boundary semantics are tested.
- E01.3 is complete enough to support action/terminal/reward work.

## Disallowed Conclusions

- Do not claim the observation is final for the paper.
- Do not claim reward or policy training is implemented.
- Do not claim planner integration exists.
- Do not claim EDT checker consistency is fully settled for training/inference; E03 collision tests still need to lock that down.

## Next Step

Proceed to E01.4:

- keep v1 action as forward-only steering;
- define action metadata needed by future planner operator;
- keep reverse/direction gate disabled unless C02 later proves reverse is necessary.
