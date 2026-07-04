---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_i01_method_algorithms.md
  - .pipeline/experiments/20260704_module2_h01_evaluation_manifest.md
  - .pipeline/experiments/20260704_module2_f02_6_warm_start_decision_packet.md
  - .pipeline/experiments/20260704_module2_f03_gpu3070ti_remote_readiness.md
---

# I01 System Diagram

## 直观结论

本轮完成 I01.1 系统图。图的核心信息是: Module2 不是外接一个 RL planner, 而是在 Hybrid A* 的 analytic expansion 槽内接入一个 RL-RS operator。该 operator 先做 learned steering rollout, 再用 terminal RS 作为 acceptance certificate; 若无法认证, 返回 `None`, Hybrid A* 继续 primitive expansion。

图中同时显式标注当前研究边界: F02.6 warm-start 决策仍 pending, PPO formal checkpoint 仍缺, 正式 PPO 训练只能走 `gpu3070ti-relay`, 本地产物只允许做代码、文档和测试。

## 产物

- `2_experiment/forest_n3p/scripts/build_module2_system_diagram.py`
- `2_experiment/forest_n3p/tests/test_module2_system_diagram.py`
- `0_trials/module2_system_diagram/module2_system_diagram.drawio`
- `0_trials/module2_system_diagram/module2_system_diagram.json`
- `0_trials/module2_system_diagram/module2_system_diagram.md`

## 图节点覆盖

- `hybrid_astar_loop`
- `analytic_trigger`
- `custom_operator_dispatch`
- `rl_rs_funnel_operator`
- `rl_rollout_env`
- `terminal_rs_certificate`
- `accept_shortcut`
- `fallback_primitives`
- `gym_training_env`
- `checkpointed_policy`
- `formal_evaluation_boundary`

## 关键代码锚点

- HA* main loop and primitive fallback: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:620`, `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:781`
- Analytic trigger: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:287`, `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:726`
- Custom operator dispatch: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:129`, `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:296`, `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:301`
- RL-RS funnel: `2_experiment/forest_n3p/rl_rs/operator.py:48`, `2_experiment/forest_n3p/rl_rs/operator.py:62`, `2_experiment/forest_n3p/rl_rs/operator.py:77`
- Rollout env and reward: `2_experiment/forest_n3p/rl_rs/env.py:135`, `2_experiment/forest_n3p/rl_rs/env.py:156`, `2_experiment/forest_n3p/rl_rs/env.py:179`, `2_experiment/forest_n3p/rl_rs/env.py:314`
- Terminal RS certificate: `2_experiment/forest_n3p/rl_rs/env.py:211`, `2_experiment/forest_n3p/rl_rs/terminal.py:21`, `2_experiment/forest_n3p/rl_rs/operator.py:102`
- Training adapter: `2_experiment/forest_n3p/rl_rs/gym_env.py:26`, `2_experiment/forest_n3p/rl_rs/gym_env.py:40`, `2_experiment/forest_n3p/rl_rs/obs.py:100`, `2_experiment/forest_n3p/rl_rs/reward.py:129`
- Checkpoint/evaluation boundary: `2_experiment/forest_n3p/rl_rs/checkpoint_operator.py:55`, `2_experiment/forest_n3p/rl_rs/checkpoint_operator.py:100`, `2_experiment/forest_n3p/main_evaluation.py:70`, `2_experiment/forest_n3p/main_evaluation.py:772`, `2_experiment/forest_n3p/main_evaluation.py:775`, `2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py:322`

## 验证

- Memory retrieval: memory-retriever 确认热区过期, 当前应以 `.pipeline/mainline` 为准; I01.1 仍未完成, 且系统图应标注 F02.6 pending / PPO checkpoint missing / `gpu3070ti-relay`。
- ACE: `mcp__auggie__codebase-retrieval` 返回 `402 Payment Required`, 因此回退到精确文件读取。
- RED: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_system_diagram.py` 先失败于缺少 `forest_n3p.scripts.build_module2_system_diagram`。
- GREEN targeted: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_system_diagram.py` -> `1 passed in 0.08s`。
- Adjacent I01: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_system_diagram.py 2_experiment/forest_n3p/tests/test_module2_method_algorithms.py` -> `2 passed in 0.09s`。
- Syntax: `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_system_diagram.py`。
- Artifact audit: XML parse + every `code_anchors[]` file/line/pattern check -> `module2_system_diagram_artifact=ok`。

## 边界

- 本记录不声称任何方法优于 Dang multi-RS 或其他 baseline。
- 本记录不关闭 H01/H02 formal evaluation。
- F02.6 warm-start decision 仍是 `pending_human_decision`。
- `ppo_analytic_operator` 和 `ppo_rs_funnel` 仍缺 formal PPO checkpoint。
- PPO formal training 必须在 `gpu3070ti-relay` 等远端 GPU 执行, 禁止本地训练补洞。
