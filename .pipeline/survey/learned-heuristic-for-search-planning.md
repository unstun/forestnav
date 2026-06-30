---
origin: ai+web
reviewed: false
date: 2026-06-30
topic: learned heuristic for search-based planning
confidence: medium
---

# 学习型启发函数综述：面向搜索式规划

> 状态：AI 整理，未经 Dr Sun 审阅（reviewed: false）。
> 引用前须回到原文核验。

---

## 一、谱系梳理

| 论文 | 方法 | 核心创新 | 场景 |
|------|------|---------|------|
| Veerapaneni2023Learning (LoHA*) | 局部残差启发函数 + focal search | 学 9x9 局部 patch 的残差 h_k，加到全局 h_g，节点减少 2–20x | 2D 网格导航 |
| Veerapaneni2024DataEfficient (DE-LoHA*) | 数据高效收集框架 | backward A* 回溯免费标注训练数据，10x 数据效率，支持在线学习 | 2D 网格导航 |
| Hadar2026Beyond (LHBL) | 多步搜索标签训练 | 用多步 lookahead 搜索标签替代单步 ground-truth，更好捕捉搜索动态 | 离散组合规划 |
| Yang2025PACHS | RL + 并行搜索推断 | actor-critic RL 训练学习启发函数，搜索即推断，支持并行探索 | 导航基准 |
| Bokan2024SLOPE | 最优路径距离剪枝 | 学节点到最优路径的距离（非 cost-to-go）剪 open list，降内存和扩展量 | 通用运动规划 |
| Menon2026TSEASL | 时序自适应 lattice | 时序采样动态调整 lattice 分辨率，面向非完整约束实时重规划 | 地面车辆 |

---

## 二、LoHA* 系列深度分析

### 2.1 LoHA*（Veerapaneni2023Learning，ICAPS 2023）

**核心设计**：
- 启发函数 h(s) = h_g(s) + h_k(s)
  - h_g(s)：全局 Dijkstra cost-to-go（保可采纳性基础）
  - h_k(s)：局部 9×9 patch 上训练的残差神经网络预测值
- 在 weighted A*（focal search）框架下使用，允许 h_k 非严格可采纳
- 节点扩展量减少 2–20x（依环境复杂度）

**关键问题**：节点减少但 wall-clock 时间因 NN 推理反而增加。
原因：单次 NN 推理延迟 >> 单次节点扩展的 CPU 开销；没有批量推理优化。

**训练方式**：监督学习，标签来自离线最优路径。

### 2.2 DE-LoHA*（Veerapaneni2024DataEfficient，SoCS 2024）

**在 LoHA* 基础上的改进**：
- 数据收集：backward A* 回溯时自动标注所有中间节点的 h* 值，无需额外求解
- 效率：10x 数据效率提升（同等数据量下性能更好，或同等性能用 1/10 数据）
- 支持在线学习：规划过程中持续更新启发函数

**局限**：仍是 2D 网格，仍有 NN 推理 wall-clock 瓶颈。

---

## 三、其他方法要点

### LHBL（Hadar2026Beyond，AAAI 2026）

- 训练标签改为多步 lookahead 的搜索结果，而非单步最优值
- 更准确反映搜索过程中的节点"重要性"
- 仅在离散组合规划（如 SAS+ planning）上验证，无连续状态/非完整约束实验

### PACHS（Yang2025PACHS，arXiv 2025）

- 将启发式搜索重新表述为概率推断问题
- actor（策略网络）+ critic（价值/启发网络）联合训练
- 支持并行搜索，exploration 有原则性保证
- 无 Ackermann 运动学实验

### SLOPE（Bokan2024SLOPE，ICAPS Workshop 2024）

- 学习的目标不是 cost-to-go，而是"节点到最优路径的距离"
- 用此距离剪 open list（而非改 h 值），降低内存和扩展量
- 通用运动规划框架，无显式非完整约束
- 中文翻译：`1_survey/papers/md/Bokan2024SLOPE_zh.md`

### TSEASL（Menon2026TSEASL，arXiv 2026）

- State Lattice 自适应分辨率：低障碍区域稀疏 lattice，高障碍区域密集 lattice
- 时序采样（temporal sampling）使分辨率调整可在线进行
- 目标：非完整约束地面车辆的实时重规划
- 与 Hybrid A* 互补（lattice planner vs. continuous-state search）

---

## 四、对 ForestNav 的启示

### 研究空白（已确认）

当前文献中**没有**将以下要素同时结合的工作：

1. **学习型局部启发函数**（如 LoHA* 的 9×9 残差设计）
2. **Hybrid A*** 框架（非完整 Ackermann 运动学，连续状态空间）
3. **森林/密集障碍**场景（窄通道、多瓶颈）

LoHA*/DE-LoHA*：全是 2D 网格，无运动学约束。
LHBL/SLOPE：离散/通用规划，无非完整约束。
PACHS：连续状态但无 Ackermann。
TSEASL：非完整约束，但不是学习型启发函数。

### LoHA* 移植到 Hybrid A* 的主要挑战

| 挑战 | 说明 |
|------|------|
| 状态空间扩展 | HA* 状态 = (x, y, θ)，patch 需要包含航向信息（从 2D 变 3D） |
| NN 推理速度 | HA* 节点数更多（72 bin × 空间），推理开销更显著 |
| 可采纳性 | LoHA* 依赖 h_g 保底；HA* 已有 2D Dijkstra h_g，可复用此框架 |
| 训练数据 | 已有 80,000 条 teacher HA* 路径可作为标签来源 |

### DE-LoHA* 的数据收集策略可直接复用

teacher HA* 规划时，backward replay 可免费标注所有节点的近似 h* 值，无需额外求解。
这与 Gate-Constrained HA* 的训练数据收集思路兼容。

---

## 五、相关文献链接

- `Veerapaneni2023Learning` → `1_survey/papers/md/Veerapaneni2023Learning.md`（已有中文翻译）
- `Veerapaneni2024DataEfficient` → `1_survey/papers/md/Veerapaneni2024DataEfficient.md`（已有中文翻译）
- `Hadar2026Beyond` → `1_survey/papers/md/Hadar2026Beyond.md`（已有中文翻译）
- `Yang2025PACHS` → `1_survey/papers/md/Yang2025PACHS.md`（已有中文翻译）
- `Bokan2024SLOPE` → `1_survey/papers/md/Bokan2024SLOPE.md`（已有中文翻译）
- `Menon2026TSEASL` → `1_survey/papers/md/Menon2026TSEASL.md`（已有中文翻译）

---

## 六、未解决问题

1. LHBL 的多步标签策略是否可迁移到连续状态空间的 HA*？
2. LoHA* 的 wall-clock 瓶颈能否通过批量推理（batching）+ GPU 解决？
3. SLOPE 的"到最优路径距离"目标是否比残差 h_k 更适合 HA* 场景？
