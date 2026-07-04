---
status: completed
origin: ai+web+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 F03.1 RL 库选择记录

## 直观结论

F03 训练主线选择 **Stable-Baselines3 2.9.0 + Gymnasium wrapper**。

CleanRL 只作为 PPO 实现细节的参考读物, 不作为本项目生产训练库。local minimal PPO 不进入主线, 除非后续单独做完整 PPO 审计和测试, 否则会违反主线里 "不允许手写不可审计临时 PPO" 的约束。

原因很直接:

1. 本项目现在已有 planner-side `AnalyticExpansionEnv`, 但它不是 Gymnasium env; F03.2 应该写一个薄 Gymnasium adapter, 不重写环境逻辑。
2. 本项目 action 是单维连续 steering; SB3 README 的算法表显示 PPO 支持 `Box` action 和 multiprocessing。
3. 本项目 observation 同时有 scalar 和 `(C,H,W)` patch; SB3 支持 custom env、custom policy、`Dict` observation、TensorBoard、callback。
4. CleanRL 是高质量单文件 PPO 参考, 但其 README 明确说它不是 modular library, 不适合作为可导入训练框架。
5. 本机运行时已安装并 import smoke 通过 SB3 2.9.0; CleanRL README 的 Python 版本要求仍是 `>=3.7.1,<3.11`, 与本机 Python 3.13.12 冲突。

## 决策矩阵

| 候选 | 结论 | 关键证据 | 本项目影响 |
|---|---|---|---|
| Stable-Baselines3 | 选中 | SB3 README: reliable PyTorch RL implementations, custom env/policy/Dict obs/TensorBoard/callback, Python 3.10+, PyTorch >=2.8, PPO supports Box action and multiprocessing, MIT license. | 写 Gymnasium adapter + custom policy, 用 PPO 主线训练。 |
| CleanRL | reference only | CleanRL README: single-file implementations, TensorBoard/seeding/W&B; also states not modular/not meant to be imported; Python prerequisite `<3.11`; continuous PPO docs support Box obs/action but Gymnasium support is experimental. | 读 `ppo_continuous_action.py` 的实现细节和 logging checklist, 不直接接入训练主线。 |
| local minimal PPO | 拒绝 | 主线 F03.1 明确禁止 "手写不可审计的临时 PPO"。 | 除非另开完整算法审计任务, 否则不写自制 PPO。 |

## 本地代码适配事实

### 当前环境不是 Gymnasium env

- `AnalyticExpansionEnv` 是 planner-side surface, 没有继承 `gymnasium.Env`: `2_experiment/forest_n3p/rl_rs/env.py:109-153`。
- reset 需要传入 `AnalyticExpansionContext`, 并拒绝 colliding start: `2_experiment/forest_n3p/rl_rs/env.py:130-151`。
- step 直接接受 `SteeringAction | float`, 返回项目自定义 `AnalyticExpansionStep`: `2_experiment/forest_n3p/rl_rs/env.py:153-260`。

结论: F03.2 要做的是 adapter, 不是替换现有 env。adapter 负责抽样 context、暴露 Gymnasium spaces、把 SB3 action 映射回 `AnalyticExpansionEnv.step()`。

### 动作空间匹配 SB3 PPO

- v1 action 是 forward-only steering command: `2_experiment/forest_n3p/rl_rs/actions.py:10-17`。
- `decode_steering_action()` 支持 normalized steering, 并最终按 `AckermannParams.max_steer` 映射到物理 steering: `2_experiment/forest_n3p/rl_rs/actions.py:45-58`。
- reverse 明确禁止, 需要 C02 evidence 或 v2 contract: `2_experiment/forest_n3p/rl_rs/actions.py:19-35`。

结论: Gymnasium `action_space` 应该先用 `spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)`, adapter 内部传 `SteeringAction(value, normalized=True)`。

### 观测空间需要 Dict / MultiInputPolicy

- scalar obs 当前是 8 维 tuple: `2_experiment/forest_n3p/rl_rs/obs.py:37-53`。
- patch obs 是 channel-first `(C,H,W)` float32, 默认 occupancy + normalized EDT 两通道: `2_experiment/forest_n3p/rl_rs/obs.py:85-113`。

结论: Gymnasium `observation_space` 应为 `spaces.Dict({"scalar": Box(... shape=(8,)), "patch": Box(0, 1, shape=(2,64,64), dtype=np.float32)})`。SB3 custom-env docs 对 normalized image-like observation 的要求是使用 `normalize_images=False` 并保持 channel-first。

## 外部依据

### Stable-Baselines3

- GitHub README lines 283-288: SB3 是 PyTorch 中可靠的 RL algorithm implementations, 目标包括帮助复现、改进和建立 baseline: https://github.com/DLR-RM/stable-baselines3
- GitHub README lines 295-307: features 包含 custom environments、custom policies、common interface、`Dict` observation、TensorBoard、custom callback、type hints: https://github.com/DLR-RM/stable-baselines3
- GitHub README lines 358-362: SB3 supports PyTorch >= 2.8, requires Python 3.10+: https://github.com/DLR-RM/stable-baselines3
- GitHub README lines 421-430: PPO 支持 `Box` action, `Discrete`, `MultiDiscrete`, `MultiBinary`, multiprocessing: https://github.com/DLR-RM/stable-baselines3
- GitHub README lines 517-553: license 为 MIT, latest release 为 v2.9.0 on Jun 15, 2026: https://github.com/DLR-RM/stable-baselines3
- Custom env docs lines 61-65: custom env 需要 follow Gymnasium interface; normalized channel-first image-like observation 应传 `normalize_images=False`: https://stable-baselines3.readthedocs.io/en/master/guide/custom_env.html
- VecEnv docs lines 120-165: vectorized environments 支持多个独立 env 叠加; Dict/Tuple sub-observations; DummyVecEnv/SubprocVecEnv 支持 Dict/Tuple; terminal observation 需要从 info 取: https://stable-baselines3.readthedocs.io/en/master/guide/vec_envs.html
- SB3 raw LICENSE lines 0-1: MIT License: https://raw.githubusercontent.com/DLR-RM/stable-baselines3/master/LICENSE

### Gymnasium

- Spaces docs lines 137-150: env 必须有 `action_space` 和 `observation_space`; spaces 定义交互格式并支持 structured data/Dict flattening: https://gymnasium.farama.org/api/spaces/
- Spaces docs lines 227-243: fundamental spaces 包括 Box, composite spaces 包括 Dict/Tuple: https://gymnasium.farama.org/api/spaces/

### CleanRL

- GitHub README lines 298-307: CleanRL 是 high-quality single-file implementation, 支持 TensorBoard、seeding、W&B 等研究功能: https://github.com/vwxyzjn/cleanrl
- GitHub README lines 315-322: CleanRL 不是 modular library、不 meant to be imported; prerequisite 是 Python >=3.7.1,<3.11: https://github.com/vwxyzjn/cleanrl
- CleanRL PPO docs lines 386-393: `ppo_continuous_action.py` 面向 continuous action, Box observation/action, Gymnasium support 仍是 experimental: https://docs.cleanrl.dev/rl-algorithms/ppo/
- CleanRL raw LICENSE lines 0-5: license 主体是 MIT, 但包含 adapted-code notices: https://raw.githubusercontent.com/vwxyzjn/cleanrl/master/LICENSE

## 本机环境验证

安装命令:

```bash
python -m pip install stable-baselines3
```

关键 stdout:

```text
Successfully installed stable-baselines3-2.9.0
```

Import smoke:

```bash
python - <<'PY'
import sys
import gymnasium as gym
import stable_baselines3 as sb3
import torch
from stable_baselines3 import PPO

print('python', sys.version.split()[0])
print('gymnasium', gym.__version__)
print('stable_baselines3', sb3.__version__)
print('torch', torch.__version__)
print('ppo_class', PPO.__name__)
PY
```

stdout:

```text
python 3.13.12
gymnasium 1.2.3
stable_baselines3 2.9.0
torch 2.11.0
ppo_class PPO
```

## F03.2 具体落地边界

下一项不是直接开 PPO 训练, 而是先写可测的 Gymnasium adapter:

1. 新增 `forest_n3p.rl_rs.gym_env` 或同等模块, 保留现有 `AnalyticExpansionEnv` 为真环境逻辑。
2. adapter 接收一个 `ContextSampler`, 每次 reset 抽一个 `AnalyticExpansionContext`。
3. `action_space = Box(-1, 1, shape=(1,), dtype=np.float32)`。
4. `observation_space = Dict({"scalar": Box(...), "patch": Box(...)})`。
5. `step()` 返回 Gymnasium 五元组 `(obs, reward, terminated, truncated, info)`。
6. info 必须保留 `terminal_rs`, `reward_terms`, `failure_reason`, `telemetry`, 并为 SB3 VecEnv auto-reset 保留 final observation 可追踪字段。
7. 先用 `stable_baselines3.common.env_checker.check_env()` 做 adapter smoke, 再接 `DummyVecEnv`。
8. PPO policy 默认走 `MultiInputPolicy`; normalized patch 使用 `policy_kwargs=dict(normalize_images=False)`。

## 当前不 claim 的内容

- 不 claim PPO 已开始训练。
- 不 claim SB3 custom policy 已写好。
- 不 claim CleanRL 不好; 它是很好的 PPO 细节参考, 只是本项目生产接入不合适。
- 不 claim local Python 3.13 下 CleanRL 完全不可用; 这里只记录 README 前提与本项目接入风险。
