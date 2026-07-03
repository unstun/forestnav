---
date: 2026-07-03
status: e01_1_rl_rs_api_skeleton_complete
origin: codex+code
reviewed: false
task: Module2 E01.1
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_gate1_cost_accounting.md
source_head: dbedf028
execution_host: MacBook-Pro.local
---

# Module2 E01.1 RL-RS API Skeleton

## 直观结论

E01.1 已新建 `2_experiment/forest_n3p/rl_rs/` 包。这个包不是 PPO 训练实现, 也不是最终 reward 环境; 它只把后续 RL-RS funnel 必须共享的 planner-side API surface 立起来:

- planner context;
- forward-only steering action;
- Ackermann rollout step;
- terminal RS-connectable check;
- observation scalar surface;
- reward breakdown placeholder;
- policy protocol;
- step/episode telemetry。

关键边界: reward 明确标记为 `pending_e02`, 不能把当前 `0.0` reward 当成最终训练配方。

## Files

New package files:

- `2_experiment/forest_n3p/rl_rs/__init__.py`
- `2_experiment/forest_n3p/rl_rs/actions.py`
- `2_experiment/forest_n3p/rl_rs/env.py`
- `2_experiment/forest_n3p/rl_rs/obs.py`
- `2_experiment/forest_n3p/rl_rs/policy.py`
- `2_experiment/forest_n3p/rl_rs/reward.py`
- `2_experiment/forest_n3p/rl_rs/rollout.py`
- `2_experiment/forest_n3p/rl_rs/telemetry.py`
- `2_experiment/forest_n3p/rl_rs/terminal.py`

New test:

- `2_experiment/forest_n3p/tests/test_rl_rs_api.py`

## API Anchors

| Module | Anchor | Meaning |
|---|---|---|
| `actions.py` | `SteeringAction`, `clip_steering_action` | v1 forward-only continuous steering action, clipped by `AckermannParams.max_steer` |
| `rollout.py` | `rollout_constant_steer_step` | Calls planner-source `sample_constant_steer_motion` and supplied checker |
| `terminal.py` | `check_terminal_rs_connectable` | Uses `rs_utils.generate_reeds_shepp_path` + `sample_reeds_shepp_path` + collision checker |
| `env.py` | `AnalyticExpansionContext` | Carries map, footprint, start, goal, params, checker, rollout budget |
| `env.py` | `AnalyticExpansionEnv` | Reset/step API surface for later RL environment work |
| `telemetry.py` | `RlRsStepTelemetry`, `RlRsEpisodeTelemetry` | Required future timing and failure fields |
| `policy.py` | `SteeringPolicy` | Protocol for future BC/PPO policy adapters |

## Verification

Commands:

```bash
PYTHONPATH=2_experiment python -m py_compile \
  2_experiment/forest_n3p/rl_rs/*.py

PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_rl_rs_api.py \
  -q
```

Results:

- `py_compile`: pass
- `pytest`: `2 passed in 0.22s`

## Allowed Conclusions

- The RL-RS package now exists with a typed planner-compatible API skeleton.
- One rollout step uses the same Ackermann sampling function as Hybrid A* primitive evaluation.
- The environment step returns telemetry fields needed by D02/D03 cost accounting.

## Disallowed Conclusions

- Do not claim E01.2/E01.3 are complete.
- Do not claim reward is implemented.
- Do not claim PPO/BC policy exists.
- Do not claim planner integration exists.

## Next Step

Proceed to E01.2:

- harden `AnalyticExpansionEnv.reset/step` around real planner-state context;
- add tests for collision, truncation, terminal RS success/failure, and missing reset;
- keep reward work in E02.
