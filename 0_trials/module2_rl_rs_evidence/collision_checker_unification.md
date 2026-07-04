---
origin: ai+local
reviewed: false
created: 2026-07-04
topic: module2 A02.2 collision checker unification audit
---

# A02.2 Collision Checker 统一备忘

## 直观结论

模块2后续不能让 RL 训练、RL 推理、RS terminal check、HA* primitive expansion 各自判断碰撞。否则会出现最危险的一类假结果:

> policy 在训练环境里学到的 "可走", 到 planner 里被另一套碰撞 checker 判成 "不可走"; 或反过来, 训练时惩罚了安全动作, 推理时却允许。

当前代码已经有一个可统一的入口: 所有关键执行路径最终都能调用 `checker.collides_path(samples)` 或 `checker.collides_pose(...)`。但默认 checker 构造仍分散在多个地方, 因此 A02.2 的结论不是 "已经完全统一", 而是:

- **机制上可统一**: `HybridAStarPlanner`、`AnalyticExpansionEnv`、`RlRsFunnelOperator`、terminal RS check 都能共享同一个 checker 实例。
- **当前默认仍需约束**: planner 默认构造 `GridFootprintChecker`; RL context 如果未注入 checker 也会构造 `GridFootprintChecker`; `EDTCollisionChecker` 存在但不是默认 planner checker。
- **后续最大实现必须做成硬门控**: 任何数据生成、训练、评测、paper table 都要记录 checker class、footprint、theta bins、collision step、padding/margin, 并禁止 train/eval checker 不一致的 formal claim。

## 代码事实

### 1. 地图边界与占据语义

- `GridMap.world_to_grid()` 用 `round((x-origin)/resolution)` 转索引: `2_experiment/forest_n3p/third_party/pathplan/map_utils.py:26-29`。
- `GridMap.is_occupied_index()` 把越界当碰撞: `map_utils.py:40-43`。
- `GridMap.occupancy_patch()` 用 nearest-neighbor patch, 并把 patch 索引 clip 到地图边界: `map_utils.py:49-82`。

影响:

- checker 的边界规则和 observation patch 的边界规则不同: checker 通常越界碰撞, patch extraction clip 到边界。
- 论文或实验记录不能只写 "uses occupancy grid"; 必须写清 collision checker 的越界规则。

### 2. Footprint 语义

- `OrientedBoxFootprint.collides()` 和 `TwoCircleFootprint.collides()` 都只是薄包装, 内部新建 `GridFootprintChecker`: `geometry.py:46-62`, `geometry.py:161-177`。
- `TwoCircleFootprint.from_box()` 用两个圆保守覆盖车体矩形: `geometry.py:97-115`。
- `TwoCircleFootprint.circle_centers()` 给出前后圆心: `geometry.py:149-159`。

影响:

- 训练/推理如果使用 two-circle, 必须固定 length/width/center_shift 派生出的 radius/center_offset。
- 不能把 box checker 和 two-circle checker 的结果混作同一实验口径。

### 3. GridFootprintChecker 是 planner 默认碰撞语义

- planner 构造时如果没有外部 `collision_checker`, 默认创建 `GridFootprintChecker(grid_map, footprint, theta_bins, padding)`: `planner.py:196-201`。
- `GridFootprintChecker` 缓存 occupancy bool grid、map origin/resolution、theta bins 和 pose collision cache: `geometry.py:267-285`。
- 对 oriented box, 它预计算每个 heading bin 的 footprint grid offsets: `geometry.py:303-317`。
- oriented-box `_collides_grid()` 在 footprint offset 越界时直接碰撞, 否则检查 offset cells 是否占据: `geometry.py:322-333`。
- two-circle `_collides_circle_world()` 对 occupied cell square 做 circle-square intersection, 并把圆接触地图外视为碰撞: `geometry.py:335-366`。
- two-circle pose 先算前后圆心, 任一圆碰撞即碰撞: `geometry.py:368-381`。
- `collides_pose()` 对 two-circle 走 exact circle-world path, 对 box 走 quantized heading offset cache: `geometry.py:383-396`。
- `collides_path()` 对 samples 逐点调用 `collides_pose()`: `geometry.py:398-406`。
- `motion_collides()` 包含 start pose 并通过 `interpolate_poses()` 采样中间姿态: `geometry.py:408-416`, `geometry.py:521-537`。

影响:

- RL rollout 与 HA* primitive 的一致性重点是 **samples 的生成步长** 和 **同一个 checker 实例/参数**。
- Oriented-box checker 受 theta bins 量化影响; two-circle checker 不走 heading offset cache, 但仍受 circle radius、grid resolution 和 map boundary 影响。

### 4. EDTCollisionChecker 是另一套可选语义

- `EDTCollisionChecker` docstring 写明它是 two-circle footprint 的 EDT-based checker, 目标是与 `UGVBicycleEnv` 碰撞检测一致: `geometry.py:419-425`。
- 初始化时它对 obstacle EDT 再取 boundary distance min, 让边界也成为障碍: `geometry.py:449-458`。
- `_dist_at_m()` 用 bilinear interpolation; 越界返回 0.0: `geometry.py:460-479`。
- `collides_pose()` 对 two-circle 两个圆心查询 EDT, 距离小于等于 `radius + half_cell` 即碰撞: `geometry.py:494-498`。
- `collides_path()` 和 `motion_collides()` 与 GridFootprintChecker 一样逐点判断: `geometry.py:500-518`。

影响:

- EDT checker 和 grid checker 都可实现 `collides_pose/collides_path`, 但不是完全等价。
- 如果后续为了速度或与训练环境一致改用 EDT checker, formal evaluation 必须全链路使用同一种 checker, 不能训练用 EDT、planner 评测用 GridFootprintChecker 后还 claim 同一 protocol。

### 5. HA* primitive 与 RS analytic expansion 都已走 checker

- primitive rollout 用 `sample_constant_steer_motion(... step=self.collision_step)` 生成 arc samples: `planner.py:237-248`。
- primitive collision 用 `self.collision_checker.collides_path(arc_states)`: `planner.py:249-251`。
- RS analytic segment 用相同 `sample_constant_steer_motion(... step=self.collision_step)` 采样: `planner.py:506-515`。
- RS analytic segment collision 也用 `self.collision_checker.collides_path(seg_states)`, 并累计 collision check time/count: `planner.py:519-533`。
- planner self-check 用 `collides_pose()` 检查 start/goal: `planner.py:632-645`。

影响:

- 当前 HA* classical 侧已经有一致的 samples + checker 入口。
- 后续 RL operator 只要从 planner context 接收同一个 checker, 就能和 primitive/RS analytic 共享碰撞语义。

### 6. RL-RS env/operator 已经支持共享 checker

- `AnalyticExpansionContext` 显式包含 `checker`, `collision_sample_step_m`, `theta_bins`, `collision_padding_m`: `rl_rs/env.py:29-55`。
- `AnalyticExpansionContext.collision_checker()` 若有 `checker` 则直接返回, 否则才构造 `GridFootprintChecker`: `rl_rs/env.py:86-92`。
- env reset 立即缓存 context checker, 并用它检查 start collision: `rl_rs/env.py:156-160`。
- rollout step 将同一个 checker 传给 `rollout_constant_steer_step()`: `rl_rs/env.py:191-199`。
- terminal RS check 同样接收 `checker=self._checker`: `rl_rs/env.py:210-222`。
- `rollout_constant_steer_step()` 采样后只调用 `checker.collides_path(samples)`: `rl_rs/rollout.py:42-56`。
- `check_terminal_rs_connectable()` 如果传入 checker, 直接用这个 checker 检查 RS samples; 否则才新建 `GridFootprintChecker`: `rl_rs/terminal.py:44-50`。
- `RlRsFunnelOperator._env_context()` 从 planner context 注入 `context.collision_checker`, 并把 planner 的 `collision_step` 作为默认 `collision_sample_step_m`: `rl_rs/operator.py:133-151`。
- terminal append 阶段调用 planner 的 `_try_rs_with_radius()`, 因此也回到 planner checker: `rl_rs/operator.py:153-162`。

影响:

- planner-integrated RL-RS 推理路径已经具备共享 checker 的结构。
- 风险主要在独立训练/数据生成 context 是否也传入同一 checker 口径, 以及是否在 artifact 中记录。

### 7. 现有测试覆盖但不是完整证明

- E03.2 记录表明已经新增 "rollout collision matches planner checker" 测试, 覆盖 free path / blocked path, 并通过 `22 passed`: `.pipeline/experiments/20260703_module2_e03_collision_consistency.md`。
- `test_rl_rs_gym_env.py` 的 `_empty_context()` 手动构造 `GridFootprintChecker` 并放入 `AnalyticExpansionContext`: `tests/test_rl_rs_gym_env.py:20-37`。
- `test_rollout_collision_budget.py` 只检查 rollout sample count 与 collision step 对齐, 不检查 checker 语义: `tests/test_rollout_collision_budget.py:9-18`。
- `audit_bc_demonstration_collisions.py` 使用 `GridFootprintChecker` 检查 BC demonstrations 当前/下一状态是否碰撞: `scripts/audit_bc_demonstration_collisions.py:34-56`。

影响:

- 已有测试是局部一致性证据, 不能替代完整 A02.2 protocol。
- 后续需要补 formal artifact checker manifest 和 train/eval checker equality guard。

## 统一方案

### 方案 A: 当前主线默认

默认 formal protocol 采用:

- checker class: `GridFootprintChecker`
- footprint: `TwoCircleFootprint.from_box(length=0.924, width=0.740)` 或 evaluation config 的正式 UGV footprint
- theta bins: planner/eval config 中同一 `theta_bins`
- collision step: planner `collision_step` 同时作为 RL rollout `collision_sample_step_m`
- collision padding: `None` or fixed value; formal run 中必须记录
- map boundary: outside map is collision for checker

优点:

- 与当前 HA* primitive/RS analytic 默认一致。
- 代码路径最短, 不需要改 planner 默认。
- 已有 E03.2 测试直接覆盖这一口径。

缺点:

- two-circle exact circle-world checker 与 EDT reward/min-clearance 不是同一个数值函数。
- observation patch 边界 clip 与 collision boundary collision 的语义差异需要在论文方法中说明。

### 方案 B: EDT 统一

把 planner、RL rollout、terminal RS、数据审计都统一注入 `EDTCollisionChecker`。

优点:

- 与 `UGVBicycleEnv`/EDT-style clearance 更近, 有速度潜力。
- min-clearance/reward 与 collision 口径更容易叙事。

缺点:

- 需要构造 map-specific EDT checker 并贯穿 evaluation / dataset / planner。
- 需要补 Grid-vs-EDT 差异审计, 证明不会改变 baseline fairness。
- 当前 planner 默认不是 EDT, 直接切换属于 protocol change, 需单独 contract/version 或至少 decision record。

### 当前建议

在 A02/A03 实现阶段先采用方案 A, 但把 checker manifest 做成硬门控:

```text
collision_protocol:
  checker_class: GridFootprintChecker
  footprint_model: TwoCircleFootprint
  footprint_length_m: ...
  footprint_width_m: ...
  center_shift_m: ...
  theta_bins: ...
  collision_step_m: ...
  collision_padding_m: ...
  map_boundary_policy: out_of_bounds_is_collision
  rollout_checker_source: planner_context.collision_checker
  terminal_rs_checker_source: same_instance
```

## 后续必须补的 gate

1. **A02.3 telemetry**: records.csv 必须有 checker protocol summary 或 manifest link, 否则论文表格不可用。
2. **数据生成 gate**: BC/Oracle demonstrations 必须记录 checker protocol; 旧数据如果缺字段, 只能标为 legacy, 不能直接作为 formal claim。
3. **训练 gate**: `train_rl_rs_ppo` artifact 必须写入 checker protocol, 包括 collision_sample_step_m。
4. **评测 gate**: `ha_rl_rs_ppo` 和 `ha_dang_multi_rs` 必须记录同一个 checker protocol; 不一致则 preflight fail。
5. **回归测试 gate**: 至少补一个 test 证明 `RlRsFunnelOperator._env_context(...).checker is planner.collision_checker`, terminal RS check 也复用同一个 checker。
6. **论文 gate**: 方法章节必须说明 two-circle footprint、out-of-bounds collision、sample-based arc collision, 不能只写 "collision-free"。

## A02.2 判定

A02.2 可以标为完成: 已形成训练/推理共享碰撞语义方案, 并定位当前代码中所有关键碰撞入口。它不等于已实现所有 gate; 它把后续实现不能绕开的 checker protocol 固化下来。
