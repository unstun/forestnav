---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on: .pipeline/experiments/20260704_module2_f03_gymnasium_adapter.md
---

# Module2 F03.3 Curriculum / Context Sampler 记录

## 直观结论

F03.3 已完成 PPO 训练前必须要有的 staged context sampler。它不是随便随机 reset, 而是把 PPO episode 绑定到四类来源:

1. `open_connector`: 空场简单连接, 用于最早期动作/终止语义 sanity。
2. `obstacle_bypass`: 单侧障碍局部绕行, 用于引入近障碍但仍可绕开的局部避障。
3. `rs_failure_node`: 从 C02 oracle connector 结果里的 RS failure nodes 采样, 这是主训练分布。
4. `heldout_procedural`: 使用 held-out seed 重新生成程序化地图/query, 用于避免只在 C02/F02 数据上循环。

这个实现仍然不 claim PPO 训练已经开始, 也不绕过 F02.6 warm-start 未关闭决策。

## 实现锚点

- 新模块: `2_experiment/forest_n3p/rl_rs/curriculum.py`。
- 统一 context 配置与 metadata: `2_experiment/forest_n3p/rl_rs/curriculum.py:24-67`。
- `OpenConnectorContextSampler`: `2_experiment/forest_n3p/rl_rs/curriculum.py:77-87`。
- `ObstacleBypassContextSampler`: `2_experiment/forest_n3p/rl_rs/curriculum.py:90-115`。
- `OracleConnectorContextSampler`: `2_experiment/forest_n3p/rl_rs/curriculum.py:118-167`。
- `HeldoutQueryContextSampler`: `2_experiment/forest_n3p/rl_rs/curriculum.py:170-223`。
- `WeightedCurriculumContextSampler`: `2_experiment/forest_n3p/rl_rs/curriculum.py:226-248`。
- 默认 F03 sampler factory: `2_experiment/forest_n3p/rl_rs/curriculum.py:251-266`。
- Gym reset metadata 接入: `2_experiment/forest_n3p/rl_rs/gym_env.py:63-88`, `2_experiment/forest_n3p/rl_rs/gym_env.py:102-109`。

## 本地数据依据

- C02 dedup RS failure nodes: `0_trials/module2_oracle_shape/rs_failure_nodes_dedup.parquet`, 7860 rows。
- C02 oracle connector results: `0_trials/module2_oracle_shape/oracle_connector_results.parquet`, 7860 rows; `oracle_connectable_count=6289`, `oracle_connectable_rate=0.8001272264631043`。
- formal-v2 BC corpus 仍是 warm-start 依据: `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v2.parquet`, 83809 rows / 1032 source rows。

F03.3 的 `OracleConnectorContextSampler` 默认使用 `oracle_connector_results.parquet`, 并筛 `oracle_connectable=True`, 避免把 oracle 判定无解的节点混入 PPO 主训练分布。

## 测试锚点

- 测试文件: `2_experiment/forest_n3p/tests/test_rl_rs_curriculum.py`。
- open connector non-collision + metadata: `2_experiment/forest_n3p/tests/test_rl_rs_curriculum.py:29-40`。
- obstacle bypass near-obstacle + start/goal non-collision: `2_experiment/forest_n3p/tests/test_rl_rs_curriculum.py:43-55`。
- profile-aware oracle row reconstruction: `2_experiment/forest_n3p/tests/test_rl_rs_curriculum.py:58-92`。
- held-out procedural seed/query metadata: `2_experiment/forest_n3p/tests/test_rl_rs_curriculum.py:95-111`。
- Gym reset exposes curriculum metadata: `2_experiment/forest_n3p/tests/test_rl_rs_curriculum.py:114-124`。

## TDD 记录

RED:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_rl_rs_curriculum.py -q
```

失败原因:

```text
ModuleNotFoundError: No module named 'forest_n3p.rl_rs.curriculum'
```

GREEN:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_rl_rs_curriculum.py -q
```

stdout:

```text
5 passed in 3.42s
```

相关测试:

```bash
python -m py_compile \
  2_experiment/forest_n3p/rl_rs/curriculum.py \
  2_experiment/forest_n3p/rl_rs/gym_env.py \
  2_experiment/forest_n3p/rl_rs/__init__.py

PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_rl_rs_api.py \
  2_experiment/forest_n3p/tests/test_rl_rs_gym_env.py \
  2_experiment/forest_n3p/tests/test_rl_rs_curriculum.py -q
```

stdout:

```text
27 passed in 3.97s
```

全量小测试:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests -q
```

stdout:

```text
48 passed in 6.59s
```

真实数据 smoke:

```bash
PYTHONPATH=2_experiment python - <<'PY'
from forest_n3p.rl_rs import ObservationConfig
from forest_n3p.rl_rs.curriculum import (
    CurriculumContextConfig,
    HeldoutQueryContextSampler,
    ObstacleBypassContextSampler,
    OpenConnectorContextSampler,
    OracleConnectorContextSampler,
)
from forest_n3p.rl_rs.gym_env import GymAnalyticExpansionEnv

cfg = CurriculumContextConfig(
    max_steps=2,
    action_step_m=0.3,
    collision_sample_step_m=0.1,
    terminal_check_every=1,
    theta_bins=32,
    observation_config=ObservationConfig(patch_size_m=0.4, patch_cells=5, include_edt=True, edt_clip_m=1.0),
)
samplers = [
    OpenConnectorContextSampler(config=cfg),
    ObstacleBypassContextSampler(config=cfg),
    OracleConnectorContextSampler('0_trials/module2_oracle_shape/oracle_connector_results.parquet', config=cfg, max_rows=50),
    HeldoutQueryContextSampler(seed=20260704, buckets=('Complex',), queries_per_bucket=1, seed_count=1, queries_per_map=1, config=cfg),
]
for idx, sampler in enumerate(samplers):
    env = GymAnalyticExpansionEnv(sampler, observation_config=cfg.observation_config)
    obs, info = env.reset(seed=100 + idx)
    action = env.action_space.sample() * 0.0
    _obs2, reward, terminated, truncated, step_info = env.step(action)
    record = info['curriculum']
    print(record['stage'], record['source'], obs['scalar'].shape, obs['patch'].shape, reward, terminated, truncated, step_info.get('failure_reason'))
PY
```

stdout:

```text
open_connector procedural_empty_grid (8,) (2, 5, 5) 1.0 True False None
obstacle_bypass procedural_single_side_obstacle (8,) (2, 5, 5) -1.0 True False collision
rs_failure_node 0_trials/module2_oracle_shape/oracle_connector_results.parquet (8,) (2, 5, 5) -1.0 True False collision
heldout_procedural main_evaluation_build_query_set (8,) (2, 5, 5) 0.0 False False None
```

解释: obstacle 和 RS-failure stage 用 zero-steering 一步撞车是预期风险信号, 说明这些样本确实不是空场假任务。训练时 action 需要学到绕障碍/进入 terminal-RS domain。

## 当前不 claim 的内容

- 不 claim PPO 已训练。
- 不 claim warm-start checkpoint 已选定; F02.6 仍需 Dr Sun 对 obstacle-summary vs stronger/full patch-CNN 作路线决策。
- 不 claim Gate #3 已通过。
- 不 claim held-out stage 已替代正式 evaluation; 它只是训练 curriculum 的 held-out procedural source。
