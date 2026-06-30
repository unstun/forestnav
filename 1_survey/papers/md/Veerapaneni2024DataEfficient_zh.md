---
citation_key: Veerapaneni2024DataEfficient
arxiv_id: "2404.06728"
arxiv_url: "https://arxiv.org/abs/2404.06728"
title: "A Data Efficient Framework for Learning Local Heuristics"
title_zh: "学习局部启发函数的数据高效框架"
authors_short: "Veerapaneni, Park, Saleem, Likhachev"
year: 2024
venue: "SoCS 2024"
direction_tag: E_bounded_suboptimal_search
source: arxiv-html
origin: ai+web
reviewed: false
translation: zh
translated_at: 2026-06-29
---

# 学习局部启发函数的数据高效框架

**A Data Efficient Framework for Learning Local Heuristics**

**作者：** Rishi Veerapaneni¹\*, Jonathan Park¹\*, Muhammad Suhail Saleem¹, Maxim Likhachev¹
（\* 共同第一作者）

¹ Carnegie Mellon University 机器人研究所

**会议：** SoCS 2024（组合搜索国际研讨会）

---

## 摘要

随着机器学习的兴起，近年来已有若干尝试学习有效且可泛化的启发函数（heuristic）。局部启发 A\*（Local Heuristic A\*，LoHA\*）是一种近期方法，它不学习整个启发值估计，而是学习一个"局部"残差启发函数（residual heuristic），用于估计逃离一个区域的代价。

本文提出**数据高效局部启发 A\***（Data Efficient Local Heuristic A\*，**DE-LoHA\***），通过在 A\* 搜索过程中利用回溯逻辑（backtracking logic），将数据收集工作量减少至基线方法的约 **1/10**。该方法支持**在线学习**（online learning），即在求解相关规划任务的同时迭代地进行数据收集和模型改进。测试在一个 4D $(x, y, \theta, v)$ 导航领域上进行。

---

![图 1：LoHA* 方法概览——学习局部残差启发函数，只需对小区域推理即可估计逃离代价](Veerapaneni2024DataEfficient_figs/fig1_method.png)

## 1 引言

机器人学中基于搜索的规划（search-based planning）严重依赖启发函数的质量。虽然手工设计的启发函数（如欧几里得距离、低维投影）计算简单，但它们常常将搜索引导到深度局部极小值（local minima）中。

近期的监督学习方法需要由 oracle 搜索方法生成的训练数据集来学习启发函数。例如，Kim 和 An (2020) 使用 A\* 来生成最优解代价值的训练数据集，而 Takahashi 等人 (2021) 使用反向 Dijkstra。

LoHA\*（Veerapaneni 等人，2023）学习残差"局部"启发函数而非全局估计。"由于局部启发函数只需要对小区域进行推理，它们更容易学习且泛化能力更好。"然而，收集训练数据需要在局部规划问题上进行数千次 oracle A\* 调用，这在计算上变得代价高昂。

![图 2：全局 A* 回溯收集局部启发函数数据的简化示例（K=3）。每个(i)表示第i个展开的状态。展开(2)(3)为 s1,s2 收集不完整数据；展开 s4 并回溯发现 s4∈LRB(s1)，得到完整的 LH(s1)。10 次展开后收集了 4 个完整（绿）和 2 个部分（蓝）局部启发值](Veerapaneni2024DataEfficient_figs/fig2_backtrack.png)

**核心洞察：** "当 A\* 搜索求解一个'全局'起点-终点规划问题时，状态展开所固有的最优优先排序使得**单次 A\* 查询能够自动求解多个局部启发函数问题**。"

主要贡献是 DE-LoHA\* 的高效回溯数据收集技术，展示了：
- **10 倍**的效率提升
- 在测试领域中仅需 **100 次**规划调用即可完成学习

---

## 2 预备知识

### 形式化定义

给定一个规划领域，其中有一个简单的手工设计的"全局"启发函数 $h_g$，LoHA\* 学习一个局部启发函数残差 $h_k$。

对于状态 $s = (x, y, \Omega)$，其中 $x, y$ 是位置，$\Omega$ 是其他状态参数（航向角、速度）：

**局部区域（Local Region）：**

$$LR(s) = \{s' \mid K \geq |s.x - s'.x|, K \geq |s.y - s'.y|\}$$

**局部区域边界（Local Region Border）：**

$$LRB(s) = \{s' \mid K = |s.x - s'.x| \lor K = |s.y - s'.y|\}$$

**局部启发值计算：**

$$h_{gk}(s) = \min_{s'} \begin{cases} c(s, s') + h_g(s'), & s' \in LRB(s) \\ c(s, s') + 0, & s' = s_g \in LR(s) \\ \infty, & \text{otherwise} \end{cases}$$

**局部启发函数残差：**

$$h_k(s) = h_{gk}(s) - h_g(s)$$

该残差捕捉了 $h_g$ 的估计与到达局部区域边界的实际代价之间的偏差。

计算 $h_k(s)$ 需要从 $s$ 出发运行一次局部多目标 A\* 搜索（local multi-goal A\* search），将所有边界状态作为目标，使用 $h_g$ 作为启发函数。搜索通常在展开第一个边界状态时终止。

LoHA\* 使用一个**神经网络**来近似 $h_k(s)$，该网络在真值残差上训练，输入为局部障碍物地图和 $h_g$ 值。

---

## 3 数据高效局部启发函数

### 3.1 通过"回望"收集数据

**核心观察：** 在全局 A\* 搜索中，$LR(s)$ 内从 $s$ 出发的节点展开的相对顺序，与从 $s$ 出发的局部多目标 A\* 搜索中的顺序**完全一致**。

#### 定理 1（全局-局部排序一致性）

"使用优先级 $b(s, s')$ 的局部 A\*，和使用优先级 $b(s_{\text{start}}, s')$ 的全局 A\*，会对从 $s$ 出发在 $LR(s)$ 内的状态进行**相同的排序**。"

**证明：** 一旦 $s$ 在全局 A\* 中被展开，所有后继状态 $s'$ 的优先级为：

$$b(s_{\text{start}}, s') = c(s_{\text{start}}, s) + c(s, s') + h_g(s') = c(s_{\text{start}}, s) + b(s, s')$$

由于 $c(s_{\text{start}}, s)$ 是常数，按 $b(s, s')$ 排序的结果与局部 A\* 的排序完全相同。$\square$

**实现方式：** 在全局 A\* 展开状态 $s'$ 时，沿父指针回溯到每个祖先 $s$，检查：
1. $s'$ 是否属于 $LRB(s)$（即 $s'$ 是否在 $s$ 的局部区域边界上）
2. $LRB(s)$ 中是否已有节点被之前展开过

如果两个条件都满足，$s'$ 就是 $s$ 的最佳边界状态，计算 $h_k(s)$ 并加入数据集。

**关键优势：** 这种验证的计算开销**可以忽略**，不需要碰撞检测或优先队列操作。

### 3.2 收集部分数据

许多节点 $s$ 永远不会有 $LRB(s)$ 中的任何 $s'$ 被展开——但 $LR(s)$ 内部可能已有部分进展。与其丢弃这些数据：

**部分数据收集：** 对于每个被展开的 $s' \in LR(s) \setminus LRB(s)$，更新：

$$h_{gk}(s) \leftarrow c(s, s') + h_g(s')$$

这是一个下界（lower bound）更新，适用于 $LRB(s)$ 尚未被到达的每个 $s$ 的祖先。

**数据质量管理：** 使用进度度量（progress metric）对不完整数据的贡献进行降权：

$$\alpha(s, s') = \frac{d(s, s')}{K} < 1$$

其中 $d(s, s') = \max(|s.x - s'.x|, |s.y - s'.y|)$。

训练损失按 $\alpha(s, s')$ 加权，将不完整数据点的权重按到边界距离的比例降低。

**关于 Closed List 的考虑：** 虽然 closed list 在局部搜索中充当障碍物，但实证测试表明将这一细节纳入考虑**不产生有意义的性能差异**。

---

## 4 实验结果

### 领域和设置

**环境：** 10 张 1024×1024 的地图，30% 随机障碍物，最小化起点-终点之间的行驶时间。

**状态空间：** 小车模型，状态为 $(x, y, \theta, v)$
- 位置 $x, y$ 以 0.5 为步长离散化
- 航向角 $\theta$ 以 30 度为步长离散化
- 速度 $v \in \{-1, 0, 1, 2, 3\}$

**动作：** 单位代价动作，遵循**阿克曼（Ackermann）约束**
- $\Delta v \in \{-1, 0, 1\}$
- 转向角 $\in \{-60°, -30°, 0°, 30°, 60°\}$

**全局启发函数：** $h_g = L_2(s, s_{\text{goal}}) / 3$（缩放后的欧几里得距离）

**默认局部区域大小：** $K = 4$

### 4.1 数据效率分析

**表 3(a) — 每个数据样本所需的节点展开次数：**

| $K$ | 局部 A\*（oracle） | 完整数据（回溯） | 不完整数据（回溯） |
|-----|-------------------|-----------------|-------------------|
| 2   | 11                | 16.5            | 5.0               |
| 4   | 74.4              | 27.1            | 5.0               |
| 8   | 247               | 34.9            | 5.0               |
| 12  | 458               | 37.6            | 5.0               |
| 16  | 616               | 38.9            | 5.0               |

**分析：**
- 局部 A\* 的代价随区域大小 $K$ **急剧增长**（$K=16$ 时需 616 次展开/样本）
- 通过回溯收集完整数据的代价初始增加后**趋于饱和**（全局 A\* 很少完全探索解路径之外的区域）
- 不完整数据收集的代价**无论 $K$ 多大都保持恒定**（5.0 次展开/样本）

![图 3b：加速比 vs 数据收集工作量。绿线（不完整数据）以远低于 oracle 的工作量实现性能提升；蓝线（局部 A*）需要一个数量级以上的工作量](Veerapaneni2024DataEfficient_figs/fig3_results.png)

### 4.2 性能 vs. 数据收集工作量

**图 3(b)** 绘制了加速比（LoHA\* 与加权 A\* 的节点展开次数之比）与每个数据集所需工作量的关系。

结果：
- **不完整数据**（绿线）：以**远低于** oracle 方法的工作量实现了性能提升
- **局部 A\***（蓝线）：需要**一个数量级以上**的工作量才能达到类似性能
- **仅完整数据**（橙线）：介于两者之间
- **消融实验**：去掉 $\alpha(s, s')$ 降权后，性能从 **3.9x 下降到 2.4x** 加速比

**关于推理开销的说明：** LoHA\* 展开的节点更少，但模型推理增加了计算开销（约 2.3 秒/问题 vs. 基线 0.1 秒/问题）。

![图 3c：DE-LoHA* 在线学习性能。每 5 个问题重新训练一次，20 个问题后即出现显著性能提升](Veerapaneni2024DataEfficient_figs/fig3c_online.png)

### 4.3 在线学习性能

**实验协议：**
1. **初始数据集：** 使用带回溯的全局 A\* 求解 5 个起点-终点问题
2. 在这个小数据集上训练初始模型
3. 使用训练好的模型求解另外 5 个问题，搜索过程中同时收集数据
4. 每 5 个问题重新训练一次模型
5. 在 50 个测试问题上评估（仅 5 个问题太嘈杂）

**结果（图 3c）：**
- 在遇到 **20 个问题**（3 次重新训练迭代）内，就出现了非平凡的性能提升
- $w=16$：随着经验积累，改进持续增长
- $w=4, 8$：初始增益后性能**趋于饱和**
- 证明了**无需独立数据收集阶段**即可有效学习

---

## 算法 1：带回溯数据收集的 A\*

```
输入：状态集 S，边集 E，起始状态 s_start，目标状态 s_goal，局部窗口大小 K
输出：路径 [s_start, s_i, ..., s_goal]，局部启发函数数据点 D_i

过程 Plan(S, E, s_start, s_goal, K):
  CompletedData, IncompleteData = {}, {}
  OPEN = {s_start}
  
  while OPEN 非空:
    s_min = OPEN.min()        // 取优先级最低的节点
    if s_min == s_goal:
      return 反转[s_min, s_min.parent, ..., s_start],
             IncompleteData, CompletedData
    
    Successors = Expand(s_min)  // 展开 s_min
    
    for all s' in Successors:
      s'.parent = s_min         // 记录父节点，用于回溯
    
    BacktrackDataCollection(s_min)  // 回溯收集数据
    
    for all s' in Successors:
      OPEN.insert(s')
  
  return 失败

过程 BacktrackDataCollection(s):
  s_cur = s.parent              // 从父节点开始回溯
  
  while s_cur != null 且 s_cur 不在 CompletedData 中:
    if dist(s_cur, s) > K:
      // s 已经在 s_cur 的局部区域边界之外——完整数据
      CompletedData[s_cur] = b(s_cur, s)
      从 IncompleteData 中移除 s_cur
    else:
      // s 仍在 s_cur 的局部区域内——部分数据（下界）
      IncompleteData[s_cur] = b(s_cur, s)
    
    s_cur = s_cur.parent        // 继续向上回溯

过程 b(s, s'):
  c(s, s') = s'.cost - s.cost  // 路径代价差
  h_k = c(s, s') + h_g(s') - h_g(s)  // 局部启发函数残差
  return h_k
```

**算法要点解读：**
- 每次展开一个新节点 $s_{\min}$ 时，沿父指针链向上回溯
- 对每个祖先 $s_{\text{cur}}$，检查 $s_{\min}$ 是否已经逃出了 $s_{\text{cur}}$ 的局部区域
- 如果逃出了（$\text{dist} > K$），就得到了该祖先的完整局部启发值
- 如果还没逃出，就记录一个下界估计（部分数据）
- 整个过程**不需要额外的搜索或碰撞检测**，仅利用全局 A\* 已有的信息

---

## 5 结论

本文展示了通过推理 oracle 搜索中间步骤来高效收集数据的方法，并将其应用于 LoHA\*。核心贡献："我们展示了如何通过推理应用于 LoHA\* 时 oracle 的中间步骤来更高效地收集数据。"

该方法支持仅从起点-终点任务求解中进行**在线学习**，无需显式的数据收集阶段。

### 扩展到其他方法

该技术可以稍加修改就应用于其他需要 oracle 搜索的学习方法：

**Cost-to-go 学习：** 不仅使用解路径上的状态，oracle 搜索树中的任何祖先-后代状态对 $(s_i', s_i)$ 都通过回溯提供有效的最优 $c(s_i', s_i)$ 数据。

**展开延迟学习（Expansion Delay Learning）：** 祖先-后代状态对之间的延迟同样可以类似地提取。

"我们希望未来的工作能在我们的数据高效框架基础上进一步降低计算负担并实现在线学习。"

---

## 参考文献

- Aine 等人 (2014). Multi-Heuristic A\*
- Andrychowicz 等人 (2017). Hindsight Experience Replay
- Bhardwaj, Choudhury, & Scherer (2017). Learning Heuristic Search via Imitation
- Felner, Shperberg, & Buzhish (2021). The Closed List is an Obstacle Too
- Jabbari Arfaee, Zilles, & Holte (2011). Learning heuristic functions for large state spaces
- Kaur, Chatterjee, & Likhachev (2021). Speeding Up Search-Based Motion Planning using Expansion Delay Heuristics
- Kim & An (2020). Learning Heuristic A\*: Efficient Graph Search using Neural Network
- Korf (1990). Real-time heuristic search
- Pearl & Kim (1982). Studies in Semi-Admissible Heuristics
- Takahashi 等人 (2021). Learning Heuristic Functions for Mobile Robot Path Planning Using Deep Neural Networks
- Veerapaneni, Saleem, & Likhachev (2023). Learning Local Heuristics for Search-Based Navigation Planning
