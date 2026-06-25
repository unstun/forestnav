---
origin: ai_only
reviewed: false
date: 2026-06-25
topic: DQN10可移植车式基线盘点
confidence: low
codex_gate: PASS
---

# DQN10 可移植车式基线盘点（Q9 主题调研）

> 目的：为 ForestNav（Ackermann 森林路径规划）选 baseline 提供候选清单。
> Dr Sun 2026-06-25 决定暂不锁定，本文件仅作候选库供未来决策时复用。
> 置信度：ai_only，未经 Dr Sun 审阅——仅供检索线索，禁作决策依据。

---

## 1. DQN10 主算法：MD-DQN

| 字段 | 值 |
|------|----|
| 完整名 | CNN-DDQN + Dueling + Munchausen + DQfD（专家预训练 40k 步）+ AM（Action Mask） |
| 动作空间 | Discrete(35) = 7 转向率 × 5 加速度 |
| 车型 | Ackermann；轴距 0.6 m，δmax 27°，vmax 2.0 m/s |
| 观测 | 2-3 通道占据栅格 + 11 标量 |
| 与 ForestNav 匹配 | 同车型 |

---

## 2. 可搬车式基线套件（全 Ackermann）

| 基线 | 来源 | 可搬性 | 备注 |
|------|------|--------|------|
| Improved-HA\* | Dang2022 | 中（依赖 strict_repro 包） | DQN10 专家路径来源之一 |
| LO-HA\* | Chen2025 | 中（依赖 strict_repro 包） | ForestNav third_party 已有未接评测版本 |
| EHA\* + NLP | Lian2023 | 中（依赖 strict_repro 包） | Ackermann 椭圆启发式 + 非线性规划平滑 |
| Spline/SS-RRT\* | Yoon2017 | 中（依赖 strict_repro 包） | 样条平滑 RRT\* |
| iDb-RRT | kinodynamic+TO | 低（依赖外部 Dynoplan） | 运动学 RRT\*；idb_rrt_dynoplan 需连带搬外部库，不建议 |
| Adaptive-APF | Kilic2026 | 中 | 自适应人工势场 |
| SLSQP 滚动时域 MPC 跟踪器 | DQN10 内置 | 高（纯 Python/scipy） | 最易移植 |
| Chaikin 平滑 | DQN10 内置 | 高（纯 Python） | 最易移植 |
| Dual-Baseline-Expert | Dang2022 + iDb-RRT | 中 | DQfD 示教用二选一专家，搬 MPC/cost-to-go 层即可 |

**可搬性最优**：Chaikin、MPC 跟踪器、cost-to-go expert 层；各 paper 规划器主体单向依赖各自
strict_repro 包需连带搬；idb_rrt_dynoplan 依赖外部 Dynoplan 不建议搬。

---

## 3. ForestNav 现状

| 项目 | 状态 |
|------|------|
| third_party LO-Hybrid-A\* | 已引入，未接评测流水线 |
| third_party 运动学 RRT\* | 已引入，未接评测流水线 |
| vanilla_ha | Hybrid A\*（已接入评测） |
| md_dqn 基线 | 实跑 DQN10 最弱的 MLP-DQN，结果坏（SR ≈ 0，297/300 未到终点）|

文件核验：`ForestNav/2_experiment/forest_n3p/baselines/md_dqn_adapter.py`

---

## 4. 可信度警告

- DQN10 论文 SR 86% 与实测 raw_48.csv（DDQN 72%/DQN 88%）存在最高严重度溯源争议，不可直接引用。
- 强 MD-DQN 权重被 .gitignore 且在 realmap 分布上训练；作 ForestNav 基线须在 forest 分布重训。
- md_dqn 基线实跑结果：SR ≈ 0（MLP-DQN，297/300 失败），不可作为 MD-DQN 效果的代理。

---

## 5. Reviewer 判断

- 普通 holonomic A\*/RRT 对 Ackermann 不可行（运动学约束不满足），只作 infeasible 下界参考。
- 有效标准基线 = Hybrid A\* + 改进 HA\* + 运动学 RRT\*（ForestNav third_party 已具备基础）。
- 本文件记录候选，最终 baseline 选取须另立 Research Contract 后确定。

---

*生成时间：2026-06-25；来源：DQN10 项目内部代码盘点 + ForestNav baselines 目录核验。*
*本文件 origin=ai_only，高概率含幻觉，使用前须 Dr Sun 核验。*
