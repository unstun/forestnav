---
citation_key: Yang2025PACHS
arxiv_id: "2509.25402"
arxiv_url: "https://arxiv.org/abs/2509.25402"
title: "Parallel Heuristic Search as Inference for Actor-Critic Reinforcement Learning Models"
title_zh: "PACHS：用 Actor-Critic RL 模型做并行启发式搜索"
authors_short: "Yang, Mishani, Pivetti, Kingston, Likhachev"
year: 2025
venue: "arXiv"
direction_tag: E_bounded_suboptimal_search
source: arxiv-html
origin: ai+web
reviewed: false
translation: zh
translated_at: 2026-06-29
---

# PACHS：用 Actor-Critic RL 模型做并行启发式搜索

**作者：** Hanlan Yang (CMU/Rice), Itamar Mishani (CMU), Luca Pivetti (CMU/PoliMi), Zachary Kingston (Rice), Maxim Likhachev (CMU)

---

## 一句话总结

把 Soft Actor-Critic (SAC) 的 actor 当动作生成器、critic 当启发函数，塞进并行 A* 搜索框架里。效果：RL 策略从"单步预测器"升级为"多步搜索+回溯"，泛化能力大幅提升。

![图 1：Pachs 架构总览——actor 生成候选动作，critic 评估优先级，多线程并行展开](Yang2025PACHS_figs/fig1.png)

---

## 1 问题：RL 策略在部署时太脆弱

RL 训练出的策略通常这样用：观测 → 网络前向传播 → 输出一个动作 → 执行。这是**单步贪心**，没有前瞻、没有回溯。一旦遇到训练分布外的情况（新障碍物、新目标位置），策略就失效。

Pachs 的思路：既然 actor-critic 已经学到了"哪些动作好"（actor）和"当前状态值多少"（critic），为什么不用搜索把它们组合起来，做多步规划？

---

## 2 核心思路：RL 组件 → 搜索组件的映射

| RL 概念 | 搜索概念 | Pachs 中的用法 |
|---------|---------|---------------|
| Actor $\pi_\theta(a|s)$ | 后继生成器（动作空间采样） | 给状态 $s$ 生成一批候选动作 |
| Critic $Q_\phi(s,a)$ | 启发函数 $h(s)$ | 评估每条边的优先级 |
| 策略 rollout | 贪心搜索（无回溯） | Pachs 用 best-first search 替代 |

关键等价关系：当奖励定义为负代价时，critic 的 $Q(s,a)$ 就近似于 $c(s,a) + h(s')$，即"走这一步的代价 + 后续到目标的估计代价"。

![图 2：ePA*SE（传统并行搜索）与 Pachs 的对比——Pachs 用 actor 替代固定动作集，用 critic 替代手工启发函数](Yang2025PACHS_figs/fig2.png)

---

## 3 算法细节

### 3.1 边优先级

Pachs 对**边**（而非节点）排优先级：

$$f(e) = g(s) + w \cdot Q_\phi(s, a)$$

其中 $g(s)$ 是从起点到 $s$ 的已知代价，$Q_\phi(s,a)$ 是 critic 对"从 $s$ 执行 $a$ 后到目标的总代价"的估计，$w$ 是权重因子。

### 3.2 两种边

![图 3：Pachs 展开过程——虚拟边触发 actor+critic 推理，实际边触发物理仿真](Yang2025PACHS_figs/fig3.png)

搜索维护一个按 $f$ 排序的 OPEN 边列表，每次取最优边处理：

**虚拟边（状态展开）**——第一次访问一个状态时插入：
1. Actor 生成一批候选动作：$\vec{a} = \pi_\theta(s)$
2. Critic 批量评估 Q 值：$\vec{q} = Q_\phi(s, \vec{a})$
3. 为每个动作创建一条实际边，优先级 $f = g(s) + w \cdot q_i$
4. 所有实际边插入 OPEN

**实际边（边评估）**——执行具体动作：
1. 用物理仿真器计算后继状态 $s'$ 和真实代价 $c(s,a)$
2. 如果 $g(s) + c(s,a) < g(s')$，更新 $s'$ 的 g 值
3. 为 $s'$ 插入一条虚拟边（等待后续展开）

### 3.3 两级并行化

这是 Pachs 解决 NN 推理瓶颈的方式（对比 LoHA* 的瓶颈）：

**GPU 批量级**：多个状态的 actor 推理和 critic 评估合并为一次 GPU batch forward pass，摊薄单次推理开销。

**CPU 多线程级**：多个工作线程同时处理不同的边评估（物理仿真/碰撞检测），主线程继续管理 OPEN 列表。

### 3.4 实时模式

给定时间预算（如 3 秒）：
1. 观察当前环境
2. 在预算内尽可能搜索
3. 如果找到完整路径 → 执行前几步
4. 如果超时 → 选 OPEN 中 $f$ 最小的边，重建部分路径，执行
5. 回到步骤 1

---

## 4 实验

硬件：Intel i7-11800H + NVIDIA RTX 3070。模型用 PyTorch，搜索引擎用 C++。

### 4.1 Panda 货架：无碰撞运动规划

7-DoF Franka Panda 机械臂在货架间规划无碰撞路径。

![图 4：Panda Shelf 实验结果——Pachs 和 ePA*SE 均 100% 成功，但 Pachs 评估的边数远少](Yang2025PACHS_figs/fig4.png)

| 方法 | 成功率 | 评估边数 |
|------|--------|---------|
| ePA*SE（传统搜索） | 100% | 多 |
| Pachs | 100% | **远少于 ePA*SE** |
| 并行 rollout | 低 | — |
| Beam search | 低 | — |

Pachs 和传统搜索都能解决问题，但 Pachs 靠 critic 引导，探索的边更少。

### 4.2 Push T：接触丰富的操控任务

用机械臂推动 T 形物体到目标位姿。三个变体：固定目标、随机目标、有障碍物。

![图 5：Push T 解寻找评估——Pachs 在所有变体上 100% 成功](Yang2025PACHS_figs/fig5.png)

| 方法 | Fixed | Rand | Obs（训练时未见） |
|------|-------|------|-----------------|
| 策略 rollout | 93% | 20% | — |
| Pachs | **100%** | **100%** | **100%** |

关键：PushT-Obs 中的障碍物在训练时完全没见过，策略 rollout 直接失败，但 Pachs 靠搜索+回溯能绕过去。这就是"搜索带来的泛化"。

### 4.3 闭环执行

3 秒时间预算，最多 30 次重规划。

![图 6：Push T 闭环执行——Pachs 在所有任务上始终优越](Yang2025PACHS_figs/fig6.png)

Pachs 在闭环中保持一致性能，而并行 rollout 性能显著下降。原因：rollout 对仿真误差累积很敏感（单步误差会雪崩），搜索天然有纠错能力。

![图 7：不同评估预算下的性能曲线——更多预算带来更高成功率](Yang2025PACHS_figs/fig7.png)

---

## 5 与 LoHA* 的关系

| 维度 | LoHA* | Pachs |
|------|-------|-------|
| 学什么 | 局部逃逸代价 $h_k$ | Actor（动作）+ Critic（Q 值） |
| 怎么用 | 加到 $h_g$ 上引导 focal search | Critic 当 $h$，actor 当后继生成器 |
| 动作空间 | 固定离散动作集 | **NN 生成连续动作** |
| 并行化 | 无（逐节点 NN 推理） | **GPU batch + CPU 多线程** |
| 应用领域 | 2D 导航 + Ackermann | 7-DoF 机械臂操控 |
| NN 推理瓶颈 | 未解决（4500 vs 140000 节点/秒） | **通过并行化缓解** |

Pachs 和 LoHA* 解决不同问题：LoHA* 改进启发函数质量，Pachs 改进 RL 模型的部署方式。但 Pachs 的**并行化策略**（batch NN inference + 多线程展开）对解决 LoHA* 的推理瓶颈有直接参考价值。

---

## 6 局限性

- 只在仿真中测试，没有真实机器人实验
- 没有搜索的理论保证（bounded suboptimality）——critic 可能不准，$w$ 的选择缺乏理论指导
- 依赖高质量的 SAC 训练——如果 actor/critic 本身训练不好，搜索也帮不了

![图 8：Push T 环境可视化](Yang2025PACHS_figs/fig8.png)

![图 9：附加实验结果](Yang2025PACHS_figs/fig9.png)
