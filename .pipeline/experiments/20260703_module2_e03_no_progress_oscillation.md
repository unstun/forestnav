---
date: 2026-07-03
status: e03_4_no_progress_oscillation_complete
origin: codex+code
reviewed: false
task: Module2 E03.4
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_e03_terminal_rs_success_set.md
source_head: a7c29888
execution_host: MacBook-Pro.local
---

# Module2 E03.4 No-Progress and Oscillation Tests

## 直观结论

E03.4 已把 no-progress 和 oscillation 都变成可测试的环境终止语义。

已有 no-progress guard 继续覆盖: 连续没有达到 `min_progress_m` 时提前 `truncated`, failure reason 为 `no_progress`。

新增 oscillation guard 覆盖: 短窗口内 steering 符号反复翻转, 且累计 progress 不足阈值时提前 `truncated`, failure reason 为 `oscillation`。

这一步解决了 E01.5 当时留下的边界: `oscillation` 不再只是一个未实现标签。

## Code Changes

Changed files:

- `2_experiment/forest_n3p/rl_rs/env.py`
- `2_experiment/forest_n3p/rl_rs/reward.py`
- `2_experiment/forest_n3p/rl_rs/telemetry.py`
- `2_experiment/forest_n3p/tests/test_rl_rs_api.py`

New/updated behavior:

| Field | Meaning |
|---|---|
| `AnalyticExpansionContext.oscillation_window` | recent action/progress window |
| `AnalyticExpansionContext.oscillation_min_sign_flips` | minimum steering sign flips |
| `AnalyticExpansionContext.oscillation_progress_tolerance_m` | max net progress in window |
| `AnalyticExpansionContext.oscillation_steering_eps` | near-zero steering ignored |
| `RlRsStepTelemetry.oscillation_detected` | terminal signal exposed in telemetry |
| `RewardConfig.oscillation_penalty` | terminal penalty for oscillation truncation |

## Tests

Tests added/extended:

- `test_env_step_truncates_on_no_progress_before_budget_exhausted`
- `test_env_step_truncates_on_oscillation_before_no_progress_patience`
- `test_env_reset_step_returns_telemetry_and_reward_marker`

The oscillation test uses small forward steps and alternating steering signs `(+, -, +, -)`, with no-progress patience set high enough that oscillation triggers first. It asserts:

- first three steps are not truncated;
- fourth step is truncated;
- `failure_reason == "oscillation"`;
- telemetry/info expose `oscillation_detected`;
- terminal reward penalty is applied.

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
- `pytest`: `24 passed in 0.46s`
- `git diff --check`: pass

## Allowed Conclusions

- no-progress and oscillation terminal guards are both implemented and tested.
- oscillation is now a measurable signal, not an unimplemented failure label.

## Disallowed Conclusions

- Do not claim PPO/BC training is enabled.
- Do not claim oscillation thresholds are final tuned values.
- Do not claim planner integration exists.

## Next Step

Proceed to F01.1:

- extract state-action demonstrations from C02 oracle paths;
- keep dataset manifest source-bound;
- filter invalid endpoint / collision / already-terminal samples.
