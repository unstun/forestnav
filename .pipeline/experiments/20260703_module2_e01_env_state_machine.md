---
date: 2026-07-03
status: e01_2_env_state_machine_complete
origin: codex+code
reviewed: false
task: Module2 E01.2
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_e01_rl_rs_api_skeleton.md
source_head: af00cecd
execution_host: MacBook-Pro.local
---

# Module2 E01.2 RL-RS Environment State Machine

## 直观结论

E01.2 已把 E01.1 的 API skeleton 加固成可测试的 planner-state 环境状态机。现在 `AnalyticExpansionEnv.reset/step` 不再只是能调用, 而是明确处理:

- reset 前 step 报错;
- reset 拒绝起点已经碰撞的 planner context;
- rollout collision 直接 terminated;
- terminal RS success 直接 terminated;
- budget exhausted 且 terminal RS 不可接时 truncated;
- episode done 后再次 step 报错;
- `info` 显式带出 `terminated`、`truncated`、`failure_reason`、`terminal_rs` 和 telemetry。

这一步仍不实现 reward、观测 patch、PPO/BC 或 planner integration。reward 继续标记为 `pending_e02`。

## Code Changes

Changed files:

- `2_experiment/forest_n3p/rl_rs/env.py`
- `2_experiment/forest_n3p/tests/test_rl_rs_api.py`

Behavior locked by tests:

| Behavior | Test |
|---|---|
| Ackermann rollout uses planner-source sampling/checker | `test_rollout_step_uses_ackermann_sampling_and_checker` |
| step before reset raises | `test_env_step_before_reset_raises` |
| colliding start context rejected | `test_env_reset_rejects_colliding_start_state` |
| rollout collision terminates and blocks follow-up step | `test_env_step_terminates_on_rollout_collision_and_blocks_followup_step` |
| terminal RS success terminates | `test_env_step_terminates_on_terminal_rs_success` |
| budget exhausted without terminal RS success truncates | `test_env_step_truncates_with_no_terminal_rs_when_budget_exhausted` |
| info exposes status/failure fields | `test_env_reset_step_returns_telemetry_and_pending_reward_marker` |

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
- `pytest`: `11 passed in 0.44s`
- `git diff --check`: pass

## Allowed Conclusions

- `AnalyticExpansionEnv` now has tested reset/step state-machine semantics.
- The environment rejects invalid colliding start states instead of silently training on invalid C02 rows.
- Collision, terminal success, and truncation outcomes are explicitly visible in telemetry/info.

## Disallowed Conclusions

- Do not claim E01.3 observation patch is implemented.
- Do not claim E02 reward is implemented.
- Do not claim policy training or planner integration exists.
- Do not claim terminal RS success rate for a trained policy.

## Next Step

Proceed to E01.3:

- implement egocentric occupancy patch and EDT/distance-field patch extraction;
- keep scalar observation anchored to planner state and remaining budget;
- add image/array tests for translation/rotation behavior and obstacle alignment.
