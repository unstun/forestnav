---
origin: ai+web
reviewed: false
date: 2026-07-06
topic: module2 PPO 实现严谨性参考(GitHub 仓库 + 工程细节)
retrieval: 2 个 Opus search agent(Dr Sun 点名,偏离 sonnet 默认规则)+ 主会话抽查 2 条关键引证
---

# Module2 PPO 实现严谨性参考调研

> 背景:Gate3 fail(warm-start PPO 0.5313 / no-warm 0.4531,阈值 0.8,碰撞主导)。
> Dr Sun 假设:实现不严谨,参考成熟开源实现修改本地代码。
> 本文件 reviewed:false,仅作检索线索;写入合同/论文前须 Dr Sun 核验。

## 一、领域对标仓库(已逐一 WebFetch 核实存在)

| 仓库 | 规模/状态 | 与本项目对应点 | 值得读 |
|---|---|---|---|
| [zhm-real/MotionPlanning](https://github.com/zhm-real/MotionPlanning) | 2.7k★, Python | Hybrid A* + RS 解析扩展触发逻辑、碰撞检查 | `HybridAstarPlanner/` |
| [RajPShinde/Hybrid-A-Star](https://github.com/RajPShinde/Hybrid-A-Star) | 139★ | holonomic/non-holonomic 双启发式、RS 可对接域判定 | `scripts/` |
| [Farama-Foundation/HighwayEnv](https://github.com/Farama-Foundation/HighwayEnv) | 3.3k★, 活跃(2026-05 v1.11) | **最直接对标**:goal-conditioned 泊车 env,非全向车,reward=加权 p-norm 距离+碰撞惩罚 | `highway_env/envs/parking_env.py`, `vehicle/kinematics.py` |
| [DLR-RM/rl-baselines3-zoo](https://github.com/DLR-RM/rl-baselines3-zoo) | 2.8k★ | SB3 官方调参基线与训练脚手架 | `hyperparams/*.yml` |
| [DLR-RM/stable-baselines3](https://github.com/DLR-RM/stable-baselines3/blob/master/stable_baselines3/common/torch_layers.py) | 官方 | Dict 观测标准写法:`CombinedExtractor`(patch→NatureCNN 256 维, scalar→MLP, 拼接) | `common/torch_layers.py` |
| [reiniscimurs/DRL-robot-navigation](https://github.com/reiniscimurs/DRL-robot-navigation) | 1.3k★, TD3 | goal-conditioned 导航 reward 塑形(借鉴 reward 逻辑,观测是激光不可照搬) | `TD3/train_velodyne_td3.py` |

- Neural Motion Planning for Autonomous Parking (arXiv 2111.06739):概念最贴合(neural Hybrid A*)但无公开代码,仅思路参考。
- 已筛除:gupann/RL-Autonomous-Parking(1★)、eleurent/rl-agents(无 PPO/parking)。

## 二、PPO 工程严谨性要点(URL 均经 agent WebFetch 核实)

1. **37 Details** (https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/):
   advantage 归一化在 minibatch 级;max_grad_norm=0.5;LR 线性退火到 0;
   正交初始化(策略输出层 0.01/隐层 √2);clipped value loss;连续控制 ent_coef=0。
2. **CleanRL PPO** (https://docs.cleanrl.dev/rl-algorithms/ppo/):
   update_epochs=10, num_minibatches=32, vf_coef=0.5 基准配置。
3. **SB3 RL tips** (https://stable-baselines3.readthedocs.io/en/master/guide/rl_tips.html):
   "always normalize the input"(PPO 须 VecNormalize);默认超参不通用;预算要舍得加。
4. **BC warm-start 的正确接法**:
   - JSRL (https://ar5iv.labs.arxiv.org/html/2204.02372) **[主会话已抽查核实]**:
     Section 3 原文确认"value functions require both good and bad data to initialize
     successfully, and the mere availability of a starting policy does not itself
     readily provide an initial value function";Figure 2 实验确认 actor 预训练 +
     critic 随机初始化时 actor 性能恶化("the untrained critic provides a poor
     learning signal")。
   - Value-Pretraining (https://arxiv.org/html/2503.01491v1):先冻结策略用固定策略
     rollout 把 value 头训到收敛(GAE λ=1.0),再放开 PPO。
   - offline→online 佐证 (arXiv 2210.13846):去掉 BC 约束微调初期性能崩塌。
5. **SB3 具体坑**:自定义 extractor 须正确设置 features_dim;载权重用
   `model.set_parameters()`/`policy.load_state_dict()`;gamma=0.99 对 max_steps=32
   的短 horizon 偏大(parking 通行 0.98,可考虑 0.95–0.98)。
6. **训练预算参照** (https://huggingface.co/sb3/tqc-parking-v0)
   **[主会话已抽查核实]**:TQC+HER parking 100k steps 收敛(gamma 0.98,
   batch 512, net_arch [512,512,512], HerReplayBuffer)。但那是 off-policy+HER;
   同预算给 on-policy 无 HER 的 PPO 明显不足,PPO 预算应到 5e5–1e6,
   或改走 SAC/TQC+HER。

## 三、综合诊断(ai+web 线索级,未经 Dr Sun 审)

0.53 停滞 + 碰撞率 0.34 的可能主因排序:
(a) 观测瓶颈:2×64×64 patch 被手工池化成 21 维摘要([sb3_policy.py:38]
    `RlRsObstacleSummaryExtractor`),策略近乎几何盲——应换 CombinedExtractor 范式;
(b) warm-start 接法缺陷:只载策略权重、critic 冷启动,JSRL Figure 2 的教科书病灶;
(c) 预算不足:100k timesteps 对 on-policy PPO 偏少 5–10 倍;
(d) 次要:VecNormalize 缺失、gamma 与短 horizon 不匹配、ent_coef/LR 退火等细节。

与 07-04 失败诊断(collision 主导、rs_failure_node 0.25)相互印证:观测瓶颈(a)
与碰撞失败模式自洽;(b) 解释 warm-start 只买到 +7.8pt。

## 四、reward 对照审查(origin: ai+local,基于本项目代码 + HighwayEnv 源码,未改语义)

事实(2026-07-06 读代码确认):curriculum.py 从不设置 `reward_config`,
训练环境使用 `RewardConfig()` 全默认值(reward.py:52-66)——
**实际训练 reward 是纯稀疏的**:success +1.0(须 terminal RS 成功且未碰撞)、
collision -1.0、no_progress/oscillation/no_rs_terminal 各 -0.25;
`distance_progress_scale` / `rs_distance_progress_scale` / `clearance_scale` /
`curvature` / `path_length` / `step` 全部默认 0.0,shaping 项存在但从未启用。

与 HighwayEnv parking_env(成熟对标)的差异清单:

| 维度 | 本项目(实际训练用) | HighwayEnv parking |
|---|---|---|
| 密度 | 终局稀疏(中途恒 0) | 每步 dense:-加权 p-norm(位置+朝向+速度,p=0.5) |
| 位置/朝向 shaping | 有钩子但 scale=0 未启用 | 核心信号 |
| 碰撞惩罚量级 | -1(与 success 同量级) | -5(success 量级的 ~5 倍) |
| 成功判据 | terminal RS 可对接检查(领域特有,合理) | reward 阈值 |

含义:稀疏 reward + 32 步短 episode + on-policy PPO 无 HER,
探索信号极弱——与 rs_failure_node 桶 0.25 的成功率自洽,
是 (a)(b)(c) 之外的第四个独立可疑点 (d2)。
**未做任何语义修改**;若 v2 契约决定启用 dense shaping,建议
potential-based 形式(不改变最优策略)且逐项以 ablation 开关记录,
现有 RewardTermSwitches 基建已支持。碰撞惩罚相对量级(-1 vs -5)
也应作为 v2 契约的显式决策项。
