# GPT Pro 提示词：森林瓶颈的环境抽象问题

> 本文件是给 GPT Pro 的完整上下文包。包含背景、原版 N3P 论文链接、F-N3P 的关键代码、实验数据、和核心问题。

---

N3P 原文：https://arxiv.org/abs/2605.22722

---

## 一、背景

我们是一个 PhD 项目，做阿克曼小车在密林中的全局路径规划。

车辆参数：最小转弯半径 1.0m，轴距 0.6m，车身宽 0.74m，双圆碰撞模型。
地图：30m×30m，0.1m 分辨率，程序化森林（圆柱树干），障碍率 15-40%。
规划器：Hybrid A*（SE(2) 状态空间，72 个航向 bin，Reeds-Shepp 解析扩展，2D Dijkstra 启发函数）。

我们尝试把 N3P（一篇泊车规划加速论文）适配到森林场景，叫 F-N3P。**适配失败了**，现在在找根本原因和改进方向。

---

## 二、原版 N3P 做法（泊车，成功，加速 80%+）

N3P 的核心不是 ML 模型厉害，而是**环境抽象**做得好。

### 环境抽象

把任意停车场景抽象成 4 个参数：

```
E = {W_lane, W_spot, D_deadend, γ}

W_lane    = 车道宽度
W_spot    = 车位宽度
D_deadend = 死端墙到车位的距离
γ         = 泊车类型（forward / reverse / parallel）
```

两个环境只要这 4 个参数相同，就被认为等价——不管具体障碍物长什么样。

### 数据采集

把 4 参数离散化成网格。对每个组合：
1. 随机撒初始位姿
2. 跑 HA*+RS 到车位
3. 记录 RS 解析扩展成功的起点 x_rs（这就是"准备姿态"）
4. 按环境参数 E 分组存储

### 模型

输入只有 **6 维**：`x = [x₀, y₀, θ₀, W_lane, W_spot, D_deadend]`

γ 不进输入向量，用于选模型变体（每种泊车类型一个独立 KNN/MLP）。

输出 3 维：准备姿态 `g_pred = (x, y, θ)`

KNN (k=1) 返回训练数据中的真实 RS 起点 → **构造性保证** g_pred→goal RS 无碰撞。

### 在线推理

```
Algorithm 1:
1. 从停车场景提取 E = {W_lane, W_spot, D_deadend, γ}
2. 匹配到最近的训练集环境 E_train
3. x = [x₀, y₀, θ₀, W_lane, W_spot, D_deadend]
4. g_pred = f_γ(x; w)              ← KNN 查表，1次，6维输入
5. path = Planner(x₀ → g_pred)     ← HA* 到准备姿态（开阔空间，快）
6. rsPath = RS(g_pred → goal)      ← RS 直连车位（零搜索时间）
7. return path + rsPath
```

加速来源：最困难的入库搜索被 RS 替代，HA* 只在开阔空间搜短距离。

---

## 三、F-N3P 做法（森林适配，失败）

### 特征提取代码（features.py）

F-N3P 的输入是 41 维手工特征，在当前位姿处提取：

```python
def extract_features(map_, current_pose, goal_pose, *, config=None):
    cfg = config or FeatureConfig()
    # 1. 目标相对特征（5维）
    #    log1p(距离), sin(方位角), cos(方位角), sin(航向差), cos(航向差)
    target = relative_goal_features(current_pose, goal_pose)
    
    # 2. 射线距离（32维）
    #    从当前位置向 32 个均匀方向发射射线，记录到障碍物距离
    #    取 log1p 归一化
    ray_distances, rel_angles = ray_cast_profile(
        map_, current_pose, n_ray=32, r_max_m=10.0
    )
    
    # 3. 密度环（3维）
    #    三个同心环（0-2m, 2-5m, 5-10m）内的障碍物占比
    density = density_profile(
        map_, center_xy=(current_pose[0], current_pose[1]),
        rings_m=((0,2), (2,5), (5,10))
    )
    
    # 4. 运动标志（1维）
    motion_flag = 0.0
    
    # 拼接: [目标5 + log射线32 + 密度3 + 标志1] = 41维
    vector = np.concatenate([target, np.log1p(ray_distances), density, [motion_flag]])
    return vector
```

FeatureConfig 默认值：
- n_ray = 32（射线数量）
- r_max_m = 10.0（最大射线距离）
- density_rings_m = ((0,2), (2,5), (5,10))（三个密度环）

### 标签生成代码（labeling.py）

从 teacher HA* 路径中提取子目标序列：

```python
def extract_subgoal_labels(grid_map, footprint, teacher_path, *, config=None):
    cfg = config or LabelingConfig()  
    # LabelingConfig: l_max_m=8.0, l_min_m=1.5, turning_radius_m=1.0
    
    poses, s_values = resample_teacher_path(teacher_path, step_m=0.1)
    goal_pose = poses[-1]
    
    current_idx = 0
    subgoals = []
    
    for iteration in range(len(poses)):
        current_pose = poses[current_idx]
        
        # 先检查能否 RS 直连终点
        direct = check_rs_connection(current_pose, goal_pose)
        if direct and direct.collision_free and direct.length_m <= 8.0:
            return success(subgoals)  # 完成
        
        # 从路径末端向前扫描，找当前位置能 RS 直连的最远点
        best_idx = None
        for idx in range(len(poses)-1, current_idx, -1):
            connection = check_rs_connection(current_pose, poses[idx])
            if connection and connection.collision_free and connection.length_m <= 8.0:
                best_idx = idx
                break  # 找到最远的可达点
        
        if best_idx is None:
            return failure("no_reachable_candidate")
        
        # 检查进展是否足够（至少 1.5m）
        progress = s_values[best_idx] - s_values[current_idx]
        if progress < 1.5:
            return failure("short_progress")
        
        # 记录子目标
        subgoal_pose = poses[best_idx]
        feature = extract_features(grid_map, current_pose, goal_pose)
        delta_body = body_relative_pose(current_pose, subgoal_pose)  # (dx,dy,dθ) 车体系
        subgoals.append(LabelSample(
            current_pose=current_pose,
            subgoal_pose=subgoal_pose,
            delta_body=delta_body,        # 标签：车体系下的相对偏移
            feature_vector=feature.vector,  # 输入：41维特征
        ))
        current_idx = best_idx  # 移到子目标位置，继续循环
```

关键特点：
- 保证方向：**current→subgoal RS 可达**（和原版 N3P 反了，原版是 subgoal→goal RS 可达）
- 每条路径产生多个子目标（不是 1 个）
- 段长上限 l_max_m = 8.0m，下限 l_min_m = 1.5m

### 推理代码（inference.py）

```python
def run_forest_n3p(grid_map, footprint, start, goal, predictor, *, config=None):
    cfg = config or InferenceConfig()
    # InferenceConfig: k_neighbors=5, segment_timeout_s=1.0, segment_max_nodes=2000,
    #   commit_verified_rs_segments=False  ← 关键bug
    
    current = start
    path_out = [current]
    
    for step_index in range(max_steps):
        # 1. 检查能否 RS 直连终点
        direct = try_rs(current, goal)
        if direct:
            path_out.extend(direct)
            return success(path_out)
        
        # 2. 提取 41 维特征
        feature = extract_features(grid_map, current, goal).vector
        
        # 3. KNN 查询 k=5 个近邻
        neighbors = predictor.query(feature, current_pose=current, k=5)
        
        # 4. 逐个尝试候选子目标
        chosen = None
        for candidate in neighbors:
            if collides(candidate.subgoal_pose):
                continue
            candidate_rs = try_rs(current, candidate.subgoal_pose)
            if candidate_rs is None:
                continue
            chosen = candidate
            break
        
        if chosen is None:
            # 所有候选都不行 → Fallback
            # F2: 有预算 HA* (max_nodes=2000, timeout=1.0s)
            # F3: 全图 HA* (max_nodes=15000, timeout=2.5s)
            ...
        else:
            # 找到了可用候选
            if cfg.commit_verified_rs_segments and chosen_rs is not None:
                # RS 验证通过 → 直接走 RS 路径（零搜索时间）
                path_out.extend(rs_path)
                current = subgoal
            else:
                # BUG: commit_verified_rs_segments 默认 False
                # 即使 RS 已验证通过，仍然跑段内 HA*！白白浪费时间
                segment = plan_segment(current, chosen.subgoal_pose, 
                                       timeout_s=1.0, max_nodes=2000)
                path_out.extend(segment.path)
                current = path_out[-1]
```

KNN 预测器：
- 10 万样本，41 维特征
- KDTree 查询，z-score 归一化
- 所有样本混在一个库里，**没有按环境类型分组**

### Fallback 层级

```
Primary:  KNN 预测子目标 → RS 验证 → 段内 HA*（或直接 RS）
   ↓ 失败
F1:       尝试 k=5 个近邻中的其他候选
   ↓ 失败
F2:       有预算 HA*（max_nodes=2000, timeout=1.0s）目标=子目标或终点
   ↓ 失败
F3:       全图 HA*（max_nodes=15000, timeout=2.5s）从起点直接搜到终点
```

---

## 四、实验数据（50 次实验）

### Fallback 率

| 难度 | Primary | F1 | F2 | F3 | 总成功率 |
|------|---------|----|----|----| --------|
| Easy | 52.9% | 29.4% | 17.6% | 0% | 100% |
| Complex | 0% | 29.4% | 58.8% | 11.8% | 94.1% |
| Extreme | 12.5% | 12.5% | 62.5% | 12.5% | 93.8% |

### 完整指标对比

| 难度 | 方法 | 成功率 | 中位时间(s) | P95时间(s) | 路径长度(m) | 路径膨胀(%) | 曲率(rad/m) |
|------|------|--------|-----------|-----------|-----------|-----------|-----------|
| Easy | F-N3P | 100% | 0.113 | 0.544 | 16.62 | 2.98 | 0.0705 |
| Easy | HA* | 100% | 0.112 | 0.610 | 16.12 | 0.00 | 0.0886 |
| Complex | F-N3P | 94.1% | 0.548 | 1.752 | 16.52 | 5.35 | 0.2386 |
| Complex | HA* | 76.5% | 0.534 | 2.501 | 15.20 | 0.00 | 0.1847 |
| Extreme | F-N3P | 93.8% | 0.744 | 2.345 | 19.02 | 3.39 | 0.2406 |
| Extreme | HA* | 75.0% | 0.625 | 2.501 | 17.20 | 0.00 | 0.2521 |

结论：F-N3P 成功率高于 HA*（因为有 fallback），但**速度没有提升**（Complex/Extreme 反而更慢），路径质量也更差。

---

## 五、和原版 N3P 的关键差异

| | 原版 N3P（泊车） | F-N3P（森林） |
|---|---|---|
| 环境表示 | 4 参数抽象 (W_lane, W_spot, D_deadend, γ) | **无抽象**，41 维局部射线 |
| 输入维度 | 6 维 (位姿 3 + 环境 3) | 41 维 (射线 32 + 密度 3 + 目标 5 + 标志 1) |
| 训练数据组织 | 按环境类型分组，每组独立 | 所有样本混在一个 KNN |
| 保证方向 | subgoal→goal RS 可达（向前保证） | current→subgoal RS 可达（向后保证） |
| KNN 保证 | 返回真实 RS 起点，构造性保证 | 无保证 |
| 预测次数 | 1 次 | 多次循环 |
| HA* 的角色 | 只走开阔空间（起点→准备姿态） | 走窄通道（段间连接） |

---

## 六、我们的核心发现

F-N3P 失败的根本原因是**缺少环境抽象**。

N3P 能用是因为泊车环境可以被 4 个参数完整描述。同参数 = 同最优准备姿态 = KNN 在 6 维空间查表就够了。

F-N3P 用 41 维射线做输入，本质上是 raw 局部感知。两个拓扑结构完全不同的位置（左边有通道 vs 右边有通道）可能射线特征很像 → KNN 返回错误的子目标 → fallback → 速度反而更慢。

---

## 七、核心问题

我们现在要找的是：**森林瓶颈的等价环境抽象。**

就像 N3P 用 {W_lane, W_spot, D_deadend, γ} 4 个参数完整描述一个泊车场景一样，我们需要用少量参数完整描述一个森林瓶颈——使得同参数 = 同最优通过姿态。

森林的"瓶颈"是路径上最窄的地方——两棵树（或树和边界）之间车辆必须穿过的间隙。

### 我的初步想法（不确定对不对）

| N3P 泊车参数 | 森林瓶颈可能的对应 |
|---|---|
| W_spot（车位宽） | w：间隙宽度 |
| W_lane（车道宽） | d_before / d_after：瓶颈前后的机动空间 |
| D_deadend（死端距离） | gap_depth：窄段持续多长 |
| γ（泊车类型） | α：间隙方向和行进方向的夹角 |

但我不确定这是否足够，因为泊车场景是标准化结构（矩形车位+车道），而森林瓶颈形状多变。

### 请你思考

1. 森林瓶颈能不能像泊车那样做低维环境抽象？如果能，需要哪些参数？
2. 如果不能做到同等程度的抽象（因为森林比泊车更多变），有没有折中方案？
3. N3P 的哪些设计元素可以迁移到森林（不只是 KNN 查表，还有数据组织、保证结构等），哪些必须放弃？
4. 你有没有完全不同的切入角度？

不需要给我一个完整方案，给我思考方向和关键洞察就好。

---

## 附录 A：森林地图生成参数（forest.py）

程序化森林的具体生成方式：

```python
@dataclass(frozen=True)
class ForestParams:
    width_cells: int = 128       # 地图宽 = 128 × 0.1m = 12.8m（实际评测用 300×300 = 30m）
    height_cells: int = 128
    cell_size_m: float = 0.1     # 分辨率 0.1m

    trunk_count: int = 90        # 树干数量
    trunk_radius_m_min: float = 0.15   # 树干半径 0.15-0.35m
    trunk_radius_m_max: float = 0.35
    
    trunk_gap_m: float = 1.0     # 树干表面间目标间隙（米）← 控制难度的关键参数
    trunk_gap_jitter: float = 0.25  # 间隙随机抖动 ±25%
```

树干放置算法（`_place_trunks`）：
1. 随机撒树干位置
2. 每棵新树必须和所有已有树保持 `min_gap` 距离（树干表面间距）
3. `min_gap = min(新树gap, 已有树gap)`
4. 间隙采样有混合系数：`mix ∈ {0.85, 1.0, 1.15}`（概率 15%/70%/15%），实现"部分宽部分窄"
5. 起点/终点周围有禁入区

实际最窄间距计算：
```
实际间距 = trunk_gap_m × mix × scale_jit
         = trunk_gap_m × {0.85,1.0,1.15} × uniform(0.75, 1.25)

最窄可能 = trunk_gap_m × 0.85 × 0.75 = trunk_gap_m × 0.6375
```

各难度下的实际间距：

| 难度 | trunk_gap_m | 标称间距 | 最窄间距 | 车身宽 0.74m 余量 |
|------|------------|---------|---------|-----------------|
| Easy (d00) | ~1.35m | 1.35m | ~0.86m | +0.12m |
| Easy (d01) | ~1.25m | 1.25m | ~0.80m | +0.06m |
| Complex (d02) | ~1.15m | 1.15m | ~0.73m | -0.01m |
| Extreme (d03) | ~1.05m | 1.05m | ~0.67m | -0.07m |
| Extreme (d04) | ~0.95m | 0.95m | ~0.61m | -0.13m |

## 附录 B：车辆与规划器参数

### 车辆（阿克曼模型）

```
轴距:       0.6m
最小转弯半径: 1.0m
最大转向角:   27°
车身宽:      0.74m（双圆碰撞模型）
双圆参数:    前圆 x1=+0.4m, 后圆 x2=-0.1m, 半径 r=0.37m
```

### Hybrid A* 规划器

```
分辨率:       0.1m（和地图一致）
航向 bin:     72（每 5°一个）
目标位置容差:  0.30m
目标航向容差:  15°
启发函数:     2D Dijkstra (全图反向) + Reeds-Shepp heuristic
解析扩展:     定期尝试 RS 直连目标
```

### F-N3P 推理参数

```
k_neighbors:              5      （KNN 近邻数）
l_min_m:                  1.0    （最小推进距离）
segment_timeout_s:        1.0    （段内 HA* 超时）
segment_max_nodes:        2,000  （段内 HA* 节点上限）
full_fallback_timeout_s:  2.5    （全图 HA* 超时）
full_fallback_max_nodes:  15,000 （全图 HA* 节点上限）
commit_verified_rs_segments: False  ← BUG
```

### F-N3P 标签参数

```
l_max_m:          8.0   （RS 弧长上限）
l_min_m:          1.5   （单步推进下限）
turning_radius_m: 1.0
rs_sample_step_m: 0.1
theta_bins:       72
```

## 附录 C：已有 Baseline 代码——瓶颈路标方法（bottleneck_waypoint.py）

这是代码库里已有的、纯几何的瓶颈引导方法：

```python
def plan_bottleneck_waypoint(grid_map, footprint, start, goal, *, config=None):
    # 1. 构建骨架图（GVD 中轴线 + Dijkstra）
    graph = build_skeleton_graph(grid_map, start, goal, footprint=footprint)
    
    # 2. 沿骨架路径检测瓶颈（clearance profile 局部极小值）
    bottlenecks = place_bottleneck_waypoints(grid_map, graph.polyline, checker)
    
    # 3. 逐段 HA*：start → bottleneck₁ → bottleneck₂ → ... → goal
    #    每段 HA* 在完整地图上搜索（无走廊约束）
    targets = [bottleneck.pose for bottleneck in bottlenecks] + [goal]
    for target in targets:
        segment = plan_segment(planner, current, target)  # 全图 HA*
        path.extend(segment)
        current = path[-1]
```

瓶颈检测逻辑（`place_bottleneck_waypoints`）：
```python
def place_bottleneck_waypoints(grid_map, polyline, checker, *, config=None):
    # 1. 沿骨架路径计算 clearance profile（每个点到最近障碍物距离）
    clearance = clearance_profile_m(grid_map, poses)
    
    # 2. 平滑 clearance 曲线
    smooth = smooth_profile(clearance, window)
    
    # 3. 找 clearance 局部极小值 = 瓶颈
    #    用 scipy.signal.find_peaks(-smooth, distance=..., prominence=0.10)
    peaks, props = find_peaks(-smooth, distance=distance_samples, prominence=0.10)
    
    # 4. 按 clearance 从小到大排序（最窄的优先）
    candidates.sort(key=lambda item: smooth[item[0]])
    
    # 5. 如果相邻 waypoint 间距过长（>10m），在中间补充瓶颈
    add_long_gap_minima(...)
    
    # 6. 返回瓶颈列表，每个包含 (pose, clearance, prominence, type)
```

BottleneckWaypoint 数据结构：
```python
@dataclass(frozen=True)
class BottleneckWaypoint:
    pose: Pose              # (x, y, θ) — θ 是骨架路径在该点的切线方向
    clearance_m: float      # 到最近障碍物的距离
    smooth_clearance_m: float
    prominence_m: float     # 瓶颈的"显著度"（clearance 下降幅度）
    kind: str               # "local_minimum" 或 "long_gap_minimum"
```

注意：**瓶颈处的姿态 θ 是骨架切线方向**，不考虑阿克曼运动学（不知道车从哪来、要往哪去）。

### bottleneck_waypoint 的实验数据

这个方法成功率高但速度反而更慢：

| 难度 | 成功率 | 中位时间 | vs vanilla HA* |
|------|--------|---------|---------------|
| Easy | ~99% | ~0.50s | 比 HA*(0.11s) **慢 4.5 倍** |
| Complex | ~95% | ~0.55s | 比 HA*(0.53s) 略慢 |
| Extreme | ~90% | ~0.60s | 比 HA*(0.63s) 略快 |

慢的原因：多段全图 HA* 的函数调用开销、每段的 heuristic 预计算、碰撞检查冗余。

## 附录 D：骨架图构建代码（voronoi_waypoint.py）

```python
def build_skeleton_graph(grid_map, start, goal, *, footprint=None, config=None):
    # 1. 提取自由空间的中轴线
    free = ~grid_map.data  # 自由空间 mask
    skeleton = medial_axis(free)  # skimage
    
    # 2. 每个骨架像素作为图节点，8-邻居连边
    coords_yx = np.argwhere(skeleton)
    for each skeleton pixel:
        add 8-neighbor edges with weight = euclidean distance
    
    # 3. 把 start 和 goal 连到最近的骨架节点
    tree = cKDTree(skeleton_world_coords)
    for special in [start, goal]:
        k_nearest = tree.query(special_xy, k=24)
        add edges from special to k nearest skeleton nodes
    
    # 4. Dijkstra 最短路 start → goal
    dist_matrix, predecessors = dijkstra(graph, indices=start_node)
    
    # 5. 回溯得到骨架路径（像素级多段线）
    polyline = backtrack(predecessors, goal_node)
    
    return SkeletonGraph(skeleton, polyline, node_count, edge_count)
```

## 附录 E：训练数据集统计

```
地图数:        2,000 张程序化森林
每张地图查询:   40 个随机 (start, goal) 对
总查询:        80,000
成功路径:       ~74,500 (标签失败率 6.8%)
总样本数:       100,531 个 (feature, delta_body) 对
每条路径平均子目标数: ~1.35 个

特征维度: 41
标签维度: 3 (dx, dy, dθ in body frame)

难度分布: Easy / Complex / Extreme 按 trunk_gap_m 分档
```

## 附录 F：设计文档中的问题形式化（design.md）

```
任务：阿克曼小车在密林先验占据图上做离线全局规划
      整图 + 起终点输入 → 输出整条无碰撞路径

方法：学习模块逐步预测"下一个中间位姿"，
      Hybrid A* 只做相邻位姿间的短段搜索并拼接
      学习承担长程分解决策，搜索保证段内运动学可行

学习目标：一步预测器 π: R^41 → R^3
          输入特征 f(x; x_g, M)
          输出车体系相对位姿 Δ = (Δx, Δy, Δθ)
          世界系子目标 g = x ⊕ Δ (SE(2) 复合)
          序列由逐步展开生成：g_{i+1} = g_i ⊕ π(f(g_i))

监督来源：教师路径（vanilla HA*+RS 成功解）经前向贪心 RS 分段
          → (特征, Δ位姿) 样本对
          标签由规划器自产、零人工标注
```
