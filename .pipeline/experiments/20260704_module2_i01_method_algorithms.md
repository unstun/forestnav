---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_g01_operator_dispatch_stub_integration.md
  - .pipeline/experiments/20260704_module2_g02_checkpoint_operator_cli_telemetry.md
  - .pipeline/experiments/20260704_module2_h01_ppo_analytic_operator_manifest.md
  - .pipeline/experiments/20260704_module2_h02_statistical_ci_infra.md
---

# I01 Method Algorithms

## 直观结论

本轮完成的是论文 Method 部分的代码锚定版 Algorithm 1/2, 不是实验结果。

Algorithm 1 把当前实现说清楚: Hybrid A* 在 analytic expansion 槽位调用 custom RL-RS operator; operator 用 checkpoint-backed policy 逐步输出 steering, 用真实 planner-side `AnalyticExpansionEnv` rollout, terminal RS 通过后才接受 shortcut; 失败时返回 `None`, planner 回到普通 primitive expansion。

Algorithm 2 把训练环境说清楚: PPO 训练用的不是另一个世界模型, 而是同一个 planner-side env 的 Gymnasium adapter; reset 采样 `AnalyticExpansionContext`, observation 是 scalar + egocentric occupancy/EDT patch, action 是单连续 steering, reward 是 terminal-RS-aware decomposed reward。

## 产物

- `2_experiment/forest_n3p/scripts/build_module2_method_algorithms.py`
- `2_experiment/forest_n3p/tests/test_module2_method_algorithms.py`
- `0_trials/module2_method_algorithms/module2_method_algorithms.json`
- `0_trials/module2_method_algorithms/module2_method_algorithms.md`

## 关键代码锚点

- Planner custom dispatch: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:294`, `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:301`
- RL-RS funnel operator: `2_experiment/forest_n3p/rl_rs/operator.py:62`, `2_experiment/forest_n3p/rl_rs/operator.py:77`, `2_experiment/forest_n3p/rl_rs/operator.py:102`, `2_experiment/forest_n3p/rl_rs/operator.py:129`
- Planner-side env: `2_experiment/forest_n3p/rl_rs/env.py:156`, `2_experiment/forest_n3p/rl_rs/env.py:179`, `2_experiment/forest_n3p/rl_rs/env.py:211`, `2_experiment/forest_n3p/rl_rs/env.py:314`
- Terminal RS check: `2_experiment/forest_n3p/rl_rs/terminal.py:21`
- Gym training adapter: `2_experiment/forest_n3p/rl_rs/gym_env.py:26`, `2_experiment/forest_n3p/rl_rs/gym_env.py:63`, `2_experiment/forest_n3p/rl_rs/gym_env.py:80`
- Observation and reward: `2_experiment/forest_n3p/rl_rs/obs.py:14`, `2_experiment/forest_n3p/rl_rs/obs.py:100`, `2_experiment/forest_n3p/rl_rs/reward.py:129`
- Formal method variants: `2_experiment/forest_n3p/main_evaluation.py:70`, `2_experiment/forest_n3p/main_evaluation.py:772`, `2_experiment/forest_n3p/main_evaluation.py:775`, `2_experiment/forest_n3p/main_evaluation.py:885`, `2_experiment/forest_n3p/main_evaluation.py:902`

## 验证

- RED: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_method_algorithms.py` 先失败于缺少 `forest_n3p.scripts.build_module2_method_algorithms`。
- GREEN targeted: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_method_algorithms.py` -> `1 passed in 0.12s`。
- Syntax: `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_method_algorithms.py`。
- Anchor audit: 读取 `0_trials/module2_method_algorithms/module2_method_algorithms.json`, 对每个 `code_anchors[]` 检查文件存在、行号有效、该行包含记录的 `pattern` -> `method_algorithm_artifact=ok`。
- Adjacent: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_method_algorithms.py 2_experiment/forest_n3p/tests/test_rl_rs_funnel_operator.py 2_experiment/forest_n3p/tests/test_rl_rs_gym_env.py 2_experiment/forest_n3p/tests/test_main_evaluation_rl_rs_operator.py` -> `19 passed in 1.54s`。

## 边界

- 本记录不声称任何方法优于 Dang multi-RS 或其他 baseline。
- 本记录不关闭 H02.2/H02.3 formal evaluation。
- F02.6 warm-start decision 仍是 `pending_human_decision`。
- `ppo_analytic_operator` 和 `ppo_rs_funnel` 仍缺 formal PPO checkpoint。
- PPO formal training 必须在 `gpu3070ti-relay` 等远端 GPU 执行, 禁止本地训练补洞。
