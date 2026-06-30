---
origin: ai_only
reviewed: false
date: 2026-06-26
topic: F-N3P v2 架构设计——瓶颈姿态预测 + 走廊约束 HA*
confidence: low
---

# F-N3P v2：瓶颈姿态预测 + 走廊约束 Hybrid A*

> 待 Dr Sun 审阅。本文件 origin=ai_only，所有判断需核验。

---

## 一、一句话概括

几何找瓶颈在哪，N3P 预测怎么过瓶颈，走廊约束 HA* 连接相邻姿态。

---

## 二、核心设计思想

### 问题

森林路径规划的难点集中在**瓶颈**——树木间距最窄的地方。车辆以什么角度、什么朝向穿过瓶颈，直接决定后续路径是否可行、是否高效。

### 分工

| 任务 | 谁做 | 为什么 |
|------|------|--------|
| 瓶颈**在哪**（位置） | 几何（距离变换 + 中轴线 + clearance profile） | 纯拓扑问题，几何方法可靠且快 |
| 瓶颈**怎么过**（姿态） | N3P 学习模块（预测最优通过姿态） | 运动学优化问题，不同障碍布局需要不同的进入角度、朝向，几何方法给不出最优解 |
| 相邻姿态之间**怎么连**（路径） | 走廊约束 Hybrid A* | 搜索问题，走廊缩小搜索空间实现加速，同时保证运动学可行性 |

### 为什么几何做不了"怎么过"

`bottleneck_waypoint.py` 已有的做法是：在瓶颈处取骨架路径的朝向作为 waypoint 姿态。但骨架朝向是中轴线的切线方向，这个方向是从 Voronoi 图几何得来的，**完全不考虑阿克曼运动学**。实际情况中：

- 车辆可能需要提前偏转 10-20 度才能以正确角度穿过窄缝
- 前一个瓶颈的出口角度会约束后一个瓶颈的进入角度
- 同一个瓶颈，从左边进和从右边进需要的朝向完全不同
- 需不需要在瓶颈前倒车调整也取决于具体布局

这些都是**依赖局部障碍配置的运动学优化**，正是 N3P 式学习擅长的事情。

### 为什么不用 RS 连接

原版 N3P 的速度来自 RS 曲线替代搜索。但在森林中，RS 曲线有物理天花板：

- 阿克曼最小转弯半径 1.0m，RS 曲线在转弯时需要额外侧向空间
- Complex 场景最窄间距 ~0.76m，车身宽 0.74m，RS 转弯 >11 度就碰
- Extreme 场景最窄间距 0.57-0.68m，RS 物理上不可能

改用**走廊约束 HA*** 连接相邻姿态：
- HA* 可以做精细的航向角控制（72 bin × 精确碰撞检测）
- 走廊 mask 把搜索范围从全图 90,000 格子缩小到走廊内几千格子
- 速度来自搜索空间缩小，不依赖 RS 通过率
- RS 仍然保留为 HA* 内部的 analytic expansion 加速手段（不再是主连接方式）

---

## 三、架构总览

```
输入: occupancy_grid, start(x,y,θ), goal(x,y,θ)

Stage 1: 瓶颈检测 [几何, ~5-10ms]
    ├─ EDT 距离变换
    ├─ 中轴线提取 (medial_axis)
    ├─ 骨架图 Dijkstra 最短路 (start → goal)
    ├─ 沿骨架路径计算 clearance profile
    └─ clearance 局部极小值 = 瓶颈位置 (1-3 个)
        输出: bottleneck_locations = [(x₁,y₁), (x₂,y₂), ...]

Stage 2: 瓶颈姿态预测 [N3P 学习, ~2-5ms per bottleneck]
    ├─ 对每个瓶颈位置:
    │   ├─ 裁剪局部占据栅格 (以瓶颈为中心, body-frame 旋转)
    │   ├─ 拼接上下文特征 (前一姿态方向、到 goal 相对位置)
    │   └─ CNN/MLP 预测: (dx, dy, dθ) 相对于瓶颈中心的最优姿态偏移
    └─ 碰撞检查: 预测姿态是否无碰撞，碰撞则用 k 个候选
        输出: bottleneck_poses = [(x₁,y₁,θ₁), (x₂,y₂,θ₂), ...]

Stage 3: 走廊构建 [几何, ~5-10ms]
    ├─ 连接序列: start → bottleneck₁ → bottleneck₂ → ... → goal
    ├─ 每对相邻姿态之间:
    │   ├─ 取骨架路径对应段
    │   ├─ 沿骨架按局部 clearance 膨胀 → 走廊 mask
    │   └─ 急弯处加宽 (转弯气泡)
    └─ 合并为完整走廊 mask (二值数组, 和 grid_map 同尺寸)
        输出: corridor_mask (np.ndarray, bool)

Stage 4: 走廊约束 HA* [搜索, 主要耗时]
    ├─ 修改 HA* 的三个检查点:
    │   ├─ primitive expansion: 运动基元采样点必须在 corridor_mask 内
    │   ├─ RS analytic expansion: RS 采样点必须在 corridor_mask 内
    │   └─ 2D heuristic: 用 "障碍 ∪ 走廊外" 作为 Dijkstra 地图
    ├─ 逐段规划: start→pose₁, pose₁→pose₂, ..., poseN→goal
    │   (每段 HA* 搜索空间仅限走廊内)
    └─ RS 作为 analytic expansion 的加速手段 (不是主连接方式)
        输出: 完整路径 path = [(x,y,θ), ...]

Stage 5: 分层兜底
    ├─ 走廊内 HA* 失败 → 加宽走廊 2× 重试
    ├─ 加宽仍失败 → 全图 HA* (start→goal, 无走廊约束)
    └─ 记录兜底原因用于诊断
```

---

## 四、和现有方法的对比

### 和 F-N3P v1 的区别

| | F-N3P v1 (当前) | F-N3P v2 (本方案) |
|---|---|---|
| 子目标位置 | 沿教师路径等间隔，由 RS 可达性决定 | 在拓扑瓶颈处，由 clearance profile 决定 |
| 子目标数量 | 5-10+ 个 | 1-3 个 |
| 子目标姿态 | 预测 body-frame 偏移 (dx,dy,dθ) | 同，但基于瓶颈位置而非当前位置 |
| 连接方式 | RS 直连 (失败→HA*→全图HA*) | 走廊约束 HA* (失败→加宽→全图HA*) |
| 特征 | 41D 射线 | 局部占据栅格 (32×32 或 64×64) |
| 预测器 | KNN (10万样本) | CNN/MLP (<100K 参数) |
| 保证结构 | current→subgoal RS 可达 | 无 RS 保证；HA* 在走廊内保证分辨率完备 |

### 和 bottleneck_waypoint 的区别

| | bottleneck_waypoint (已有) | F-N3P v2 |
|---|---|---|
| 瓶颈检测 | clearance profile 极小值 ✓ (相同) | clearance profile 极小值 ✓ (相同) |
| 瓶颈姿态 | 骨架路径切线方向 (几何) | **学习预测最优通过姿态** (N3P) |
| 段间搜索 | **全图 HA*** (无走廊约束) | **走廊约束 HA*** |
| 速度 | 比 vanilla HA* 更慢 (0.5-0.6s) | 目标比 vanilla HA* 更快 |

这两个区别缺一不可：
- 只换姿态不加走廊 → 和 bottleneck_waypoint 一样慢（全图搜索）
- 只加走廊不换姿态 → 几何姿态可能导致 HA* 在走廊内也找不到路（方向不对）

### 和纯走廊方案 (Route B / C') 的区别

| | 纯走廊 | F-N3P v2 |
|---|---|---|
| 学习角色 | 走廊排序 (trivial, 可用启发式替代) | **瓶颈姿态预测** (non-trivial, 几何做不了) |
| N3P 贡献 | 无 | 核心贡献——预测运动学最优通过姿态 |
| 论文新颖性 | 低 (G²VD Planner 等已有) | 高 (学习 + 几何 + 搜索的明确分工) |

---

## 五、训练数据生成

### 数据来源

用 teacher HA* (vanilla_ha) 在大量 (map, start, goal) 上规划成功路径。

### 标注流程

对每条成功的 teacher 路径：

1. **几何检测瓶颈位置**：沿 teacher 路径计算 clearance profile → 找局部极小值
   （复用 `bottleneck_waypoint.py` 的 `place_bottleneck_waypoints` 逻辑）

2. **提取 teacher 在瓶颈处的实际姿态**：teacher 路径经过瓶颈附近时的 (x, y, θ)
   → 这就是标签——"专家示范的最优通过姿态"

3. **提取特征**：在瓶颈位置裁剪局部占据栅格
   - 以瓶颈位置为中心
   - 旋转到某个标准方向（骨架切线方向或到 goal 的方向）
   - 尺寸: 32×32 (覆盖 3.2m×3.2m @ 0.1m) 或 64×64 (覆盖 6.4m×6.4m)
   - 额外特征: 上一个姿态的相对位置/方向, goal 的相对位置/方向

4. **标签格式**：(dx, dy, dθ) = teacher 姿态相对于瓶颈中心的偏移（body frame）

### 数据规模估算

- 2000 张地图 × 40 个 query = 80,000 条路径
- 每条路径 1-3 个瓶颈 → 约 80,000-240,000 个训练样本
- 对 <100K 参数的 CNN/MLP 来说足够
- 数据生成时间：取决于 teacher HA* 速度，估计数小时（可并行）

### 预测器架构

```
输入:
  - 局部占据栅格: [1, 32, 32] 或 [1, 64, 64]
  - 上下文向量: [prev_dx, prev_dy, prev_dθ, goal_dx, goal_dy, goal_dθ, clearance]
    (约 7-10 维)

网络:
  CNN 分支:
    Conv2d(1, 16, 3, padding=1) → ReLU → MaxPool
    Conv2d(16, 32, 3, padding=1) → ReLU → MaxPool
    Conv2d(32, 64, 3, padding=1) → ReLU → AdaptiveAvgPool → Flatten
    → 64 维特征

  拼接 CNN 特征 (64) + 上下文向量 (7-10) = 71-74 维

  MLP:
    Linear(74, 64) → ReLU
    Linear(64, 32) → ReLU
    Linear(32, 3)  → 输出 (dx, dy, dθ)

参数量: ~50K-80K
推理时间: CPU < 3ms, GPU < 1ms
```

### 损失函数

```
L = L_position + λ_θ × L_heading

L_position = MSE(predicted_dx - true_dx, predicted_dy - true_dy)
L_heading  = 1 - cos(predicted_dθ - true_dθ)    # 角度周期性
```

---

## 六、走廊构建细节

### 基本走廊

沿骨架路径上相邻姿态之间的段，以每个骨架像素的 clearance 值为半宽膨胀：

```python
corridor_half_width[i] = max(
    edt[skeleton_pixel[i]] * width_ratio,   # 默认 0.8 × clearance
    vehicle_half_width + safety_margin       # 下界: 车身半宽 + 0.1m
)
```

### 急弯加宽（转弯气泡）

在骨架路径转角 > 30 度的位置，额外膨胀：

```python
if turn_angle[i] > 30_deg:
    bubble_radius = R_min * sin(turn_angle[i] / 2) + vehicle_half_width
    corridor_half_width[i] = max(corridor_half_width[i], bubble_radius)
```

这保证阿克曼小车有足够空间完成转弯。

### 走廊 mask 生成

```python
corridor_mask = np.zeros_like(grid_map.data, dtype=bool)
for pixel in skeleton_path_pixels:
    half_w = corridor_half_width[pixel_index]
    half_w_cells = int(half_w / resolution)
    # 以 pixel 为中心, half_w_cells 为半径的圆形区域置 True
    # (实际可用 distance_transform 高效实现)
corridor_mask &= ~grid_map.data  # 走廊内障碍物仍然不可通行
```

### 走廊面积预算

目标: 走廊面积 < 全图自由空间的 15-20%

30m×30m 地图, 15% 障碍 → 自由面积 ~765 m²
走廊目标面积: < 115-153 m²
典型走廊: 长 20-30m, 平均宽 2-4m → 面积 40-120 m² ✓

---

## 七、走廊约束 HA* 的具体改动

需要修改 `HybridAStarPlanner` 的三个位置：

### 7.1 运动基元扩展

在 `_evaluate_primitive()` 中，检查基元弧线的所有采样点是否在走廊内：

```python
for sample_x, sample_y in arc_samples:
    grid_x, grid_y = world_to_grid(sample_x, sample_y)
    if not corridor_mask[grid_y, grid_x]:
        return None  # 超出走廊, 剪枝
```

### 7.2 RS 解析扩展

在 `_try_rs_with_radius()` 中，RS 采样点也必须在走廊内：

```python
for sample in rs_dense_samples:
    grid_x, grid_y = world_to_grid(sample.x, sample.y)
    if not corridor_mask[grid_y, grid_x]:
        return None  # RS 路径超出走廊
```

### 7.3 2D 启发函数

预计算 Dijkstra heuristic 时，把走廊外区域视为障碍：

```python
heuristic_map = grid_map.data | ~corridor_mask  # 障碍 ∪ 走廊外 = 不可通行
dijkstra_cost = compute_2d_dijkstra(heuristic_map, goal)
```

这保证启发函数只考虑走廊内的路径，和实际搜索空间一致。

---

## 八、推理流程（完整）

```python
def plan_fn3p_v2(grid_map, footprint, start, goal, pose_predictor, config):
    # Stage 1: 瓶颈检测 [~5-10ms]
    skeleton_graph = build_skeleton_graph(grid_map, start, goal)
    bottleneck_locations = detect_bottlenecks(skeleton_graph, grid_map)
    
    # Stage 2: 姿态预测 [~2-5ms per bottleneck]
    bottleneck_poses = []
    for loc in bottleneck_locations:
        local_crop = extract_local_grid(grid_map, loc, crop_size=32)
        context = compute_context_features(loc, start, goal, bottleneck_poses)
        delta = pose_predictor.predict(local_crop, context)  # CNN forward
        predicted_pose = apply_delta(loc, delta)
        
        # 碰撞检查 + 候选
        if not collides(predicted_pose):
            bottleneck_poses.append(predicted_pose)
        else:
            # 尝试 k 个扰动候选
            found = try_k_candidates(pose_predictor, loc, local_crop, context, k=5)
            if found:
                bottleneck_poses.append(found)
            else:
                pass  # 跳过此瓶颈，直接连下一个
    
    # Stage 3: 走廊构建 [~5-10ms]
    waypoint_sequence = [start] + bottleneck_poses + [goal]
    corridor_mask = build_corridor(grid_map, skeleton_graph, waypoint_sequence)
    
    # Stage 4: 走廊约束 HA* [主要耗时]
    corridor_planner = make_corridor_ha_star(grid_map, footprint, corridor_mask)
    full_path = []
    for i in range(len(waypoint_sequence) - 1):
        segment = corridor_planner.plan(waypoint_sequence[i], waypoint_sequence[i+1])
        if segment.success:
            full_path.extend(segment.path)
        else:
            # 兜底: 加宽走廊
            wide_corridor = widen_corridor(corridor_mask, factor=2.0)
            wide_planner = make_corridor_ha_star(grid_map, footprint, wide_corridor)
            segment = wide_planner.plan(waypoint_sequence[i], waypoint_sequence[i+1])
            if segment.success:
                full_path.extend(segment.path)
            else:
                # 最终兜底: 全图 HA*
                return fallback_full_ha_star(grid_map, footprint, start, goal)
    
    return success(full_path)
```

---

## 九、为什么 N3P 在这里不可替代

如果去掉 N3P（回到 bottleneck_waypoint 的几何姿态），会发生什么：

1. 瓶颈处的 waypoint 朝向 = 骨架切线方向。但骨架切线是中轴线的几何属性，不考虑：
   - 车从哪个方向来（前一段路的出口角）
   - 车要往哪个方向去（后一段路的入口角）
   - 瓶颈两侧障碍物的非对称性（左窄右宽 vs 左宽右窄）

2. 结果：HA* 到达瓶颈附近后，需要大量节点扩展来调整朝向，甚至可能在走廊内找不到解（走廊不够宽来做大角度转弯）

3. 现有数据佐证：bottleneck_waypoint 的速度 0.5-0.6s，比 vanilla HA* 的 0.3s 还慢。
   原因之一就是几何姿态不够好，导致段间 HA* 搜索量大。

N3P 预测的姿态考虑了"教师是怎么过的"——教师路径已经做了运动学优化，学习的正是这个优化后的结果。

---

## 十、预期效果与风险

### 加速来源分析

| 来源 | 预期贡献 | 依赖条件 |
|------|---------|---------|
| 走廊缩小搜索空间 | 扩展节点减少 50-70% | 走廊面积 < 15-20% 全图 |
| 更好的瓶颈姿态 | 段间 HA* 搜索更快收敛 | 预测姿态接近教师 |
| 段间距离缩短 | 每段 HA* 更快完成 | 瓶颈数 1-3 个 |
| RS analytic expansion | 走廊内局部 RS 加速 | 走廊局部净空足够 |

### 风险点

| 风险 | 严重度 | 缓解措施 |
|------|--------|---------|
| 走廊内 HA* 仍然慢 | 高 | 走廊面积预算 < 15-20%；走廊内 Dijkstra 替代全图 Dijkstra |
| 预测姿态不好，HA* 在走廊内找不到路 | 中 | k 候选 + 加宽走廊 + 全图兜底 |
| 瓶颈检测不稳定（密林噪声） | 中 | 骨架压缩 + prominence 阈值过滤 |
| 分段 HA* 的函数调用开销 | 中 | 瓶颈数仅 1-3 个，比 voronoi_waypoint 的 5-10 段少 |
| CNN 推理时间 | 低 | <100K 参数，CPU < 3ms |

### 和 Research Contract v9 的对照

| 指标 | 目标 | 评估 |
|------|------|------|
| 成功率 ≥ vanilla HA* | 全图兜底保证 | 可达 |
| 路径膨胀 ≤ 5% | 走廊引导可能偏中轴线 | 需实验验证 |
| 时间 ≥ 50% 缩减 | 走廊面积 < 15% + 好姿态 | Easy/Complex 较乐观，Extreme 存疑 |

---

## 十一、实现计划——已有 vs 需新建

### 已有组件（可直接复用）

| 组件 | 文件 | 功能 |
|------|------|------|
| 距离变换 | `voronoi_waypoint.py` | `distance_transform_edt` |
| 中轴线提取 | `voronoi_waypoint.py` | `medial_axis` |
| 骨架图构建 | `voronoi_waypoint.py` | `build_skeleton_graph()` |
| 瓶颈检测 | `bottleneck_waypoint.py` | `place_bottleneck_waypoints()` |
| HA* 规划器 | `third_party/pathplan/` | `HybridAStarPlanner` |
| 碰撞检测 | `third_party/pathplan/geometry.py` | `GridFootprintChecker` |
| RS 工具 | `rs_utils.py` | `generate_reeds_shepp_path` |
| 特征提取 | `features.py` | 可参考，但需重写为局部栅格 |

### 需要新建

| 组件 | 工作量 | 说明 |
|------|--------|------|
| 局部栅格裁剪 | 小 | 以瓶颈为中心裁剪 + body-frame 旋转 |
| CNN/MLP 预测器 | 中 | ~50-80K 参数，PyTorch |
| 训练数据生成脚本 | 中 | 调用 teacher HA* + 瓶颈检测 + 标签提取 |
| 走廊 mask 构建 | 中 | 沿骨架路径按 clearance 膨胀 + 转弯气泡 |
| 走廊约束 HA* | 中-大 | 修改 `HybridAStarPlanner` 的三个检查点 |
| v2 推理主循环 | 中 | 串接以上组件 |
| 消融实验脚本 | 小 | 复用现有 50-trial 评测框架 |

### 消融实验设计

按顺序叠加，每步独立验证：

```
Ablation 0: vanilla HA* (baseline)
Ablation 1: bottleneck_waypoint (几何瓶颈 + 几何姿态 + 全图 HA*)  [已有]
Ablation 2: bottleneck + 走廊 HA* (几何瓶颈 + 几何姿态 + 走廊约束 HA*)  [走廊的单独贡献]
Ablation 3: bottleneck + 走廊 + N3P 姿态 (几何瓶颈 + 学习姿态 + 走廊约束 HA*)  [N3P 的单独贡献]
```

Ablation 2 vs 1 → 走廊约束值多少
Ablation 3 vs 2 → 学习姿态值多少
Ablation 3 vs 0 → 完整方案 vs baseline

---

## 十二、论文贡献叙事

> 子目标姿态预测（N3P）在泊车规划中取得了显著加速，其核心机制是用 Reeds-Shepp 解析曲线替代搜索。
> 然而，我们发现这一机制在多瓶颈密林环境中遭遇了根本性的适配失败：
> RS 曲线的物理限制（最小转弯半径 vs 窄通道）导致替代率过低，多步预测的误差累积进一步恶化性能。
>
> 我们提出 F-N3P v2，重新定义学习模块的角色：
> 不再预测 RS 可达的子目标序列，而是预测拓扑瓶颈处的运动学最优通过姿态。
> 走廊约束 Hybrid A* 负责相邻姿态之间的物理可行连接，RS 降级为局部加速手段。
>
> 这一设计实现了三方分工：几何找瓶颈、学习选姿态、搜索连路径。
> 每个模块只做自己擅长的事，没有一个可以被另外两个替代。
>
> 实验表明，F-N3P v2 在 30m×30m 程序化森林（15-40% 障碍率）中，
> 对阿克曼小车实现了 [待填] 的规划加速，同时保持 [待填] 的成功率和 [待填] 的路径质量。
