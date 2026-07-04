---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on: .pipeline/experiments/20260704_module2_f03_rl_library_selection.md
---

# Module2 F03.2 Gymnasium Adapter 记录

## 直观结论

F03.2 已完成最小但真实的 SB3 接入面: 新增 `GymAnalyticExpansionEnv`, 让现有 planner-side `AnalyticExpansionEnv` 能通过 Gymnasium `reset/step/action_space/observation_space` 被 Stable-Baselines3 调用。

这个实现不是另写一个训练环境。它只做接口转换:

1. Gymnasium action `Box(-1, 1, shape=(1,))` 转为项目内 `SteeringAction(normalized=True)`。
2. 项目内 `RlRsObservation` 转为 SB3 可消费的 `Dict({"scalar", "patch"})`。
3. reward、terminal/truncated、collision、terminal RS、telemetry 仍全部来自原 `AnalyticExpansionEnv`。

## 实现锚点

- 新 adapter: `2_experiment/forest_n3p/rl_rs/gym_env.py:26-84`。
- context sampler 类型与静态 sampler: `2_experiment/forest_n3p/rl_rs/gym_env.py:15-23`。
- action space: `2_experiment/forest_n3p/rl_rs/gym_env.py:40`。
- observation space: `2_experiment/forest_n3p/rl_rs/gym_env.py:41-51`。
- reset 逻辑: 抽样/覆盖固定 observation config, 调原 `AnalyticExpansionEnv.reset()`: `2_experiment/forest_n3p/rl_rs/gym_env.py:63-74`。
- step 逻辑: 单维 normalized steering -> planner step -> Gymnasium 五元组: `2_experiment/forest_n3p/rl_rs/gym_env.py:76-84`。
- 导出: `2_experiment/forest_n3p/rl_rs/__init__.py:10`, `2_experiment/forest_n3p/rl_rs/__init__.py:40-51`。

## 测试锚点

- 测试文件: `2_experiment/forest_n3p/tests/test_rl_rs_gym_env.py`。
- `test_gym_env_exposes_spaces_and_maps_normalized_action_to_planner_step`: 验证 reset/step observation 被 observation_space 接受, action_space 接受 normalized action, 并证明 `0.5` normalized steering 映射到 `0.5 * max_steer`: `2_experiment/forest_n3p/tests/test_rl_rs_gym_env.py:40-60`。
- `test_gym_env_passes_sb3_checker_and_dummy_vec_env_smoke`: 验证 `stable_baselines3.common.env_checker.check_env()` 和双环境 `DummyVecEnv` smoke: `2_experiment/forest_n3p/tests/test_rl_rs_gym_env.py:63-81`。

## 验证命令

先按 TDD 观察 RED:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_rl_rs_gym_env.py -q
```

RED 失败原因为缺少目标模块:

```text
ModuleNotFoundError: No module named 'forest_n3p.rl_rs.gym_env'
```

实现后 targeted GREEN:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_rl_rs_gym_env.py -q
```

stdout:

```text
2 passed in 0.73s
```

相关测试:

```bash
python -m py_compile 2_experiment/forest_n3p/rl_rs/gym_env.py 2_experiment/forest_n3p/rl_rs/__init__.py
PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_rl_rs_api.py \
  2_experiment/forest_n3p/tests/test_rl_rs_gym_env.py \
  2_experiment/forest_n3p/tests/test_policy_forward_budget.py \
  2_experiment/forest_n3p/tests/test_rollout_collision_budget.py -q
```

stdout:

```text
26 passed in 0.99s
```

全量小测试:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests -q
```

stdout:

```text
43 passed in 3.75s
```

## 当前不 claim 的内容

- 不 claim PPO 训练已开始。
- 不 claim vectorized context sampler 已覆盖真实多地图分布; 当前 `DummyVecEnv` smoke 只证明 SB3 向量接口可运行。
- 不 claim curriculum 已实现; F03.3 仍需单独定义 stage sampler。
- 不 claim custom CNN/MultiInput policy 已接入; 当前只完成 env adapter。
