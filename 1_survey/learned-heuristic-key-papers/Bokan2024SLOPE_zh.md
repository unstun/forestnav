---
citation_key: Bokan2024SLOPE
arxiv_id: "2406.04935"
arxiv_url: "https://arxiv.org/abs/2406.04935"
title: "SLOPE: Search with Learned Optimal Pruning-based Expansion"
title_zh: "SLOPE：基于学习最优剪枝扩展的搜索"
authors_short: "Bokan, Ajanovic, Lacevic"
year: 2024
venue: "ICAPS 2024 Workshop (Bridging Planning and RL)"
direction_tag: E_bounded_suboptimal_search
source: arxiv-html
origin: ai+web
reviewed: false
translation: zh
translated_at: 2026-06-29
---

# SLOPE：基于学习最优剪枝扩展的搜索

**SLOPE: Search with Learned Optimal Pruning-based Expansion**

**作者：** Davor Bokan, Zlatan Ajanovic, Bakir Lacevic

---

## 摘要

启发式搜索（heuristic search）常用于运动规划和路径寻找问题，在保证完备性和最优效率的同时寻找图中的最短路径。其缺点是**空间复杂度**——具体来说是在内存中存储所有展开的子节点和对大量活跃节点列表排序，这在计算资源有限的实时场景中可能成为问题。

为此，我们提出 **SLOPE**（Search with Learned Optimal Pruning-based Expansion），它学习一个节点**到可能最优路径的距离**，而非像其他方法那样学习 cost-to-go 值。然后根据该距离**剪枝**（prune）不被看好的节点，从而减小 open list 的大小。这确保搜索只探索最优路径附近的区域，同时降低内存和计算成本。

"与传统学习方法不同，我们的方法与 cost-to-go 启发函数的估计是**正交的**（orthogonal），提供了一种互补的策略来提高搜索效率。"

---

## 核心创新

### 学什么

传统方法学的是 $h(s) \approx h^*(s)$（cost-to-go），SLOPE 学的是完全不同的东西：

$$d(n) \in [0, 1] \quad \text{（节点 } n \text{ 到最优路径的归一化距离）}$$

- $d(n) = 1.0$：节点在最优路径上
- $d(n) = 0.0$：节点远离最优路径

### 怎么用

根据学到的距离 $d(n)$ 设定阈值，**剪掉**远离最优路径的节点，减小 open list 大小：

**两种算法变体：**

1. **SLOPE**：使用固定阈值 + 备份 open list。当需要时将阈值减半以保证完备性
2. **SLOPEr**：递归调整阈值，从高值（0.9）开始递减 0.1，实现更好的逐实例定制

### 训练数据生成

1. 从目标反向 Dijkstra 计算最优 cost-to-go
2. 从起点正向 Dijkstra 识别最优路径上的节点
3. 扩展到 $m$ 个邻近区域，代表逐渐远离的距离
4. 归一化距离得到"最优性评分"

---

## 实验结果

在 **8 个网格世界领域**上测试：

| 指标 | SLOPE | 基线 |
|------|-------|------|
| 相对误差（交替间隙地图）| **0.458** | 3.284 |
| Open list 大小（归一化）| **0.086** | 0.122 |

**与学习启发函数组合时**结果不一：某些地图类型（间隙+森林、迷宫）有改进，但有时因两个学习模型之间的方向偏差冲突而**性能下降**。

---

## 与 LoHA\* 的关系

| 维度 | LoHA\* | SLOPE |
|------|--------|-------|
| 学什么 | 局部逃离代价 $h_k$ | 到最优路径的距离 $d(n)$ |
| 怎么减少搜索 | 改进启发函数引导 | 剪枝远离最优路径的节点 |
| 关系 | — | **正交互补**：LoHA\* 改 h，SLOPE 减 open list |
| 运动学约束 | 阿克曼 4D | 无（2D 网格） |

---

## 局限性与未来工作

- 在最优路径附近的**瓶颈区域**敏感度较高
- 模型架构简单（基础 CNN）
- 未来考虑使用 GNN、Transformer
- 在全分辨率地图上测试

代码开源：https://github.com/dbokan1/SLOPE
