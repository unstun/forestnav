---
origin: ai_only
reviewed: false
date: 2026-06-26
topic: F-N3P v2 方案——Gate-Constrained Hybrid A* + 学习预测 gate 序列
confidence: low
---

# F-N3P v2：Gate-Constrained Hybrid A*

> 待 Dr Sun 审阅。

---

## 一句话

学习预测"穿哪些门、什么顺序"，HA* 一次全局搜索穿过所有门。

---

## 核心思想

把瓶颈从"分段目标"变成"搜索约束"。HA* 仍然是一次从 start 到 goal 的全局搜索，但状态空间多了一个维度 i，表示"当前要去第几个 gate"。

```
普通 HA*:         state = (x, y, θ)          → 在全图搜索，无拓扑引导
Gate-constrained:  state = (x, y, θ, i)       → 在全图搜索，按顺序穿过 gate
                                    ↑
                              i = 当前目标 gate 编号
```

**不分段、不拼接、不局部。** Gate 只引导搜索方向，不限制搜索范围。

---

## 三方分工

| 模块 | 做什么 | 为什么不可替代 |
|------|--------|-------------|
| 学习模块 | 预测 gate 序列：穿哪些瓶颈、什么顺序 | 拓扑决策是全局性的，需要理解整张地图的连通结构，简单启发式容易选错 |
| Gate 约束 | 引导 HA* 搜索方向 | 防止搜索探索错误拓扑方向，大幅减少无效扩展 |
| HA* | 一次全局搜索，处理运动学 | 保持全局最优性（在 gate 约束下），72 bin 航向精细控制 |

---

## Gate-Constrained HA* 详细设计

### 状态空间

```
标准 HA*:  state = (x, y, θ)           → 6.48M 状态 (300×300×72)
Gate HA*:  state = (x, y, θ, i)        → 6.48M × (k+1) 状态
                                          k = gate 数量，通常 1-3
                                          总状态空间增加不大
```

### Gate 区域定义

每个 gate 是一个小区域（不是一个点）：

```
gate_region[j] = {(x, y) : ||(x,y) - gate_center[j]|| < gate_radius}
```

gate_radius 可以设为瓶颈处的 clearance（约 0.5-1.5m），对应栅格上一个小圆。

### 状态转移规则

```
当 state = (x, y, θ, i) 时：

  if i < k:
    # 还有 gate 没穿过
    正常扩展 successors = {(x', y', θ', i)}      ← i 不变
    
    if (x', y') ∈ gate_region[i+1]:
      额外生成 successor = (x', y', θ', i+1)     ← i+1，表示穿过了这个 gate
  
  if i == k:
    # 所有 gate 都穿过了，向 goal 搜索
    正常扩展，目标是 final goal
```

**关键**：穿过 gate 不是硬性要求。如果 gate 区域不可达，搜索可以绕路，只是启发函数不再给 bonus。这保证了鲁棒性——学习选错 gate 不会导致规划失败。

### 启发函数

Gate-aware 启发函数比标准 2D Dijkstra 更准确：

```
h(x, y, θ, i) = dijkstra_i(x, y) 

其中 dijkstra_i 是从以下目标反向计算的 2D 最短距离：
  - i < k 时：目标 = gate[i+1] 的位置
  - i == k 时：目标 = final goal
```

预计算开销：对每个 gate 位置 + goal 各跑一次 2D Dijkstra。
k=3 个 gate + 1 个 goal = 4 次 Dijkstra，在 300×300 地图上每次约 2-3ms。
总预计算开销 ≈ 8-12ms。

**比标准 HA* 更好的引导**：标准 HA* 的启发函数只知道"离 goal 还有多远"，不知道中间要穿过哪些门。Gate-aware 启发函数知道"先去 gate[i+1]"，搜索方向更精准。

### 为什么能加速

```
标准 HA*:     搜索从 start 向各方向扩散，直到找到 goal
              在 Complex/Extreme 中，搜索经常探索错误的拓扑方向
              → 大量无效节点扩展

Gate HA*:     搜索被分成有方向的"段"
              start → gate₁ → gate₂ → goal
              每段的启发函数指向正确方向
              → 搜索更集中，无效扩展大幅减少
```

但注意：这不是像走廊那样物理剪掉搜索空间。搜索仍然可以探索全图。加速来自**更好的启发函数引导**，类似于给 HA* 装了一个"导航仪"——告诉它先去第一个门，再去第二个门。

### 和原版 N3P 的关系

```
N3P (泊车):     学习预测 1 个准备姿态 → HA* 去那里 → RS 连 goal
Gate HA* (森林): 学习预测 k 个 gate    → HA* 按顺序穿过 → 到达 goal

共同点：学习做拓扑/战略决策，搜索做运动学执行
区别：  N3P 把困难段替换为 RS（零搜索）
        Gate HA* 不替换任何段，只引导搜索方向
```

Gate HA* 没有 N3P 的"RS 替代"加速机制，但也没有 RS 的物理天花板问题。加速纯粹来自更好的搜索引导。

---

## 学习模块设计

### 任务定义

```
输入：occupancy_grid (300×300), start (x,y,θ), goal (x,y,θ)
输出：有序 gate 序列 [(x₁,y₁), (x₂,y₂), ..., (xₖ,yₖ)]，k ∈ {0,1,2,3}
```

k=0 表示"不需要 gate，直接搜到 goal"（Easy 场景很多是这种情况）。

### 方案一：几何候选 + 学习选序（推荐先做）

```
Step 1: 几何检测候选 gate（已有代码）
   - EDT + medial_axis + skeleton graph + clearance profile
   - find_peaks 找 clearance 局部极小值
   - 输出：所有候选瓶颈位置 + 各自参数（clearance, prominence, 位置）
   
Step 2: 学习模块选择和排序
   - 输入：候选列表 + 地图特征 + start/goal
   - 输出：选中哪些候选、按什么顺序
   - 架构：MLP/小型 CNN，在候选特征上做分类/排序
```

这个方案最稳——几何保证候选质量，学习只做选择。

### 方案二：端到端 gate 预测

```
输入：occupancy_grid + start/goal channels → CNN/U-Net
输出：gate 位置热力图 + 顺序预测

网络架构：
  Encoder: 3-4 层 Conv2d (occupancy + start_channel + goal_channel)
  Decoder: gate position heatmap (2D)
  Head: 从 heatmap peaks 提取 gate 位置 + 排序
```

更端到端但需要更多训练数据、更难调试。

### 推荐：先方案一，后方案二

方案一可以快速验证"gate 约束是否能加速 HA*"；如果有效，方案二可以作为论文中的"进阶版本"。

### 训练数据

对每条成功的 teacher HA* 路径：

```
1. 提取骨架路径
2. 检测所有瓶颈（clearance 极小值）
3. 找 teacher 路径实际穿过了哪些瓶颈（距离 < threshold）
4. 记录穿过顺序
5. 标签：(map_id, start, goal) → [(gate₁_xy), (gate₂_xy), ...]
```

已有 80,000 条 teacher 路径，估计可产生 80,000 个 (map, start, goal, gate_sequence) 训练样本。

---

## 实现细节

### 需要修改的代码

**HybridAStarPlanner 改动（核心）：**

```python
class GateConstrainedHybridAStarPlanner:
    def __init__(self, grid_map, footprint, gates, ...):
        self.gates = gates  # [(x₁,y₁,r₁), (x₂,y₂,r₂), ...]
        self.n_gates = len(gates)
        
        # 预计算每个 gate + goal 的 2D Dijkstra
        self.heuristics = []
        for gate in gates:
            h = compute_2d_dijkstra(grid_map, gate.position)
            self.heuristics.append(h)
        self.heuristics.append(compute_2d_dijkstra(grid_map, goal))
    
    def plan(self, start, goal):
        # 初始状态：i=0（还没穿过任何 gate）
        initial = (start.x, start.y, start.theta, 0)
        
        # A* 搜索
        open_set.push(initial, priority=self.h(initial))
        
        while open_set:
            state = open_set.pop()
            x, y, theta, i = state
            
            # 终止条件：穿过了所有 gate 且到达 goal
            if i == self.n_gates and near(x, y, goal):
                return reconstruct_path(state)
            
            # 扩展 successors
            for primitive in motion_primitives:
                nx, ny, ntheta = apply_primitive(x, y, theta, primitive)
                if collision(nx, ny, ntheta):
                    continue
                
                ni = i
                # 检查是否穿过了当前目标 gate
                if i < self.n_gates:
                    gate = self.gates[i]
                    if dist(nx, ny, gate.x, gate.y) < gate.radius:
                        ni = i + 1  # 穿过 gate，i+1
                
                successor = (nx, ny, ntheta, ni)
                open_set.push(successor, priority=g + self.h(successor))
    
    def h(self, state):
        x, y, theta, i = state
        if i < self.n_gates:
            # 还有 gate 没穿过，启发函数指向下一个 gate
            return self.heuristics[i][y_cell, x_cell]  
            # 可选：加上 gate 到 goal 的预估距离
        else:
            # 所有 gate 穿过了，指向 goal
            return self.heuristics[-1][y_cell, x_cell]
```

### 启发函数的可采纳性

对于 state (x, y, θ, i)：

```
h(x,y,θ,i) = dijkstra_dist(x,y → gate[i+1]) 
            + dijkstra_dist(gate[i+1] → gate[i+2])
            + ...
            + dijkstra_dist(gate[k] → goal)
```

这是可采纳的（不高估真实代价），因为：
- 2D Dijkstra 距离 ≤ 阿克曼运动学实际距离（忽略转弯半径）
- 各段距离之和 ≤ 必须按顺序穿过 gate 的实际总距离

所以 gate-constrained HA* 在其约束下保持最优性。

### 已有组件复用

| 组件 | 来源 | 用途 |
|------|------|------|
| 骨架图 + Dijkstra | `voronoi_waypoint.py` | 候选 gate 检测 |
| 瓶颈检测 | `bottleneck_waypoint.py` | 候选 gate 位置 |
| HA* 主循环 | `third_party/pathplan/` | 改造为 gate-constrained |
| 2D Dijkstra | `HybridAStarPlanner.plan()` | gate-aware heuristic |
| 碰撞检测 | `GridFootprintChecker` | 不变 |
| RS 解析扩展 | `rs_utils.py` | 不变（在 HA* 内部使用） |

### 需要新建

| 组件 | 工作量 | 说明 |
|------|--------|------|
| GateConstrainedHybridAStarPlanner | 中 | 在现有 HA* 上加 i 维度 + gate-aware heuristic |
| Gate 候选生成 | 小 | 复用 bottleneck 检测 + 包装 |
| Gate 选择学习模块 | 中 | MLP/CNN 做候选排序 |
| 训练数据生成 | 中 | teacher path → gate 标签提取 |
| 评测脚本 | 小 | 复用 50-trial 框架 |

---

## 和 N3P 环境抽象的关系

### N3P 泊车

```
4 参数抽象整个场景 → 1 个准备姿态 → RS 直连 goal
全局决策在抽象层完成，执行层几乎无搜索
```

### Gate-Constrained HA* 森林

```
学习预测 gate 序列 → gate 引导 HA* 搜索方向 → HA* 全局搜索到 goal
全局拓扑决策由学习完成，执行层是引导下的全局搜索
```

N3P 的环境抽象迁移到森林的形式是：
- 不再抽象整张地图（森林太复杂）
- 而是抽象"拓扑路线"——穿过哪些 gate
- Gate 序列就是森林版的"环境类型参数"

GPT Pro 提出的局部瓶颈参数 E_b 可以作为学习模块的**输入特征**：

```
每个候选 gate 的特征 = [clearance, prominence, throat_depth, 
                       approach_angle, exit_angle, 
                       left_asymmetry, right_asymmetry,
                       distance_to_next_gate, ...]
```

学习模块用这些特征判断：这个 gate 该不该选、排在第几个。

---

## 消融实验设计

```
Ablation 0: vanilla HA* (baseline)
Ablation 1: Gate HA* + 几何 gate（所有瓶颈都当 gate，按骨架顺序）
Ablation 2: Gate HA* + 学习选 gate（从候选中选最优子集和顺序）
Ablation 3: Gate HA* + 学习 gate + N3P 姿态 hint（gate 处附加推荐姿态偏置）
```

A1 vs A0 → gate 约束本身值多少（无学习）
A2 vs A1 → 学习选 gate 比全选好多少
A3 vs A2 → N3P 姿态 hint 额外值多少

---

## 预期效果

### 加速来源

| 来源 | 机制 | 依赖条件 |
|------|------|---------|
| 更好的启发函数 | 分段 Dijkstra 比全局 Dijkstra 更精准 | gate 位置正确 |
| 更少的无效扩展 | 搜索朝正确拓扑方向走 | gate 序列正确 |
| RS 解析扩展仍有效 | 穿过 gate 后在开阔处 RS 可能直连 goal | gate 后有足够空间 |

### 风险

| 风险 | 严重度 | 缓解 |
|------|--------|------|
| Gate 选错，搜索走弯路 | 中 | 兜底到 vanilla HA*；soft constraint 版本 |
| 多个 Dijkstra 预计算开销 | 低 | k=3 个 gate → 4 次 Dijkstra ≈ 8-12ms |
| 状态空间膨胀 (×k+1) | 低 | k 通常 1-3，增加有限 |
| 加速幅度不如走廊 | 中 | 不硬剪搜索空间，纯靠引导 |

### 对比 Research Contract v9

| 指标 | 目标 | 评估 |
|------|------|------|
| 成功率 ≥ vanilla HA* | Gate 错了可以绕路或兜底 | 高概率达标 |
| 路径膨胀 ≤ 5% | 启发函数可采纳，gate 约束下仍最优 | 较乐观 |
| 时间 ≥ 50% 缩减 | 纯引导加速，不硬剪空间，50% 是挑战 | 需实验验证 |

**最大不确定性**：纯引导（不剪搜索空间）能否达到 50% 加速。这需要实验来回答。

---

## 论文贡献叙事

> N3P 通过环境抽象和准备姿态预测实现了泊车规划 80%+ 的加速。
> 我们发现 N3P 的环境抽象无法直接迁移到森林——森林缺少泊车的标准化模板结构。
> 
> 我们提出 Gate-Constrained Hybrid A*：
> 将 N3P 的"环境抽象 → 引导规划"思想迁移到森林，
> 用学习模块预测拓扑 gate 序列（森林版的"环境类型参数"），
> 用 gate-aware 启发函数引导 HA* 的单次全局搜索。
> 
> 和 N3P 的关键对应：
> - N3P 的环境抽象 4 参数 → 我们的 gate 序列
> - N3P 的准备姿态 → 我们的 gate 位置
> - N3P 的 RS 替代搜索 → 我们的 gate-aware 启发函数引导搜索
> 
> 不同于分段规划（bottleneck waypoint、corridor HA*），
> Gate-Constrained HA* 保持了全局搜索的完整性——
> gate 只引导方向，不限制范围。
