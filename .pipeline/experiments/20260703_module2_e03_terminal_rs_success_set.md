---
date: 2026-07-03
status: e03_3_terminal_rs_success_set_complete
origin: codex+code
reviewed: false
task: Module2 E03.3
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_e03_collision_consistency.md
source_head: 8a91eb64
execution_host: MacBook-Pro.local
---

# Module2 E03.3 Terminal-RS Success Set Test

## 直观结论

E03.3 已直接测试 terminal RS success set。现在同一套 terminal RS checker 在人工构造样例中必须表现为:

- 空图直连: `success=True`;
- 同一路径附近放障碍: `success=False`, `failure_reason="terminal_rs_collision"`。

这一步把 E02 success reward 的基础事件单独钉住, 防止后续把 "离目标近" 误当作 "terminal RS 可接"。

## Code Changes

Changed files:

- `2_experiment/forest_n3p/tests/test_rl_rs_api.py`

New test:

- `test_terminal_rs_success_set_distinguishes_free_and_blocked_connections`

The test directly calls `check_terminal_rs_connectable()` and checks:

- `TerminalRsCheckResult.success`;
- `failure_reason`;
- `path_length_m`;
- `sample_count`。

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
- `pytest`: `23 passed in 0.48s`
- `git diff --check`: pass

## Allowed Conclusions

- Terminal RS success/failure set now has direct free/blocked tests.
- E02 success reward has a tested terminal-RS event underneath it.

## Disallowed Conclusions

- Do not claim no-progress/oscillation testing is complete. That is E03.4.
- Do not claim planner integration exists.
- Do not claim trained policy behavior.

## Next Step

Proceed to E03.4:

- define and test no-progress behavior;
- decide whether an explicit oscillation signal is ready, or keep it as a documented unsupported label until a measurable signal exists.
