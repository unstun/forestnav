---
origin: ai_only
reviewed: false
task: T07
created: 2026-06-20
---

# T07 RealMap 资产清点

## 结论

- DQN10 历史结果目录中找到了 `realmap_a` NPZ fallback，但 20 个快照只有 1 个唯一数组哈希，不能算作 2 张独立地图。
- DQN9 保留了同一张 RealMap 的原始 `map_a.pgm` / `map_a.yaml`，已复制为 `dqn_realmap_a`。
- 为满足 T07 至少 2 张地图加载/显示验收，补入 BSD 许可的 TurtleBot Willow Garage ROS 地图 `willow_garage_0p10`，并在 manifest 中标记为外部开源来源。

## 可用地图

| id | source | size | resolution(m/cell) | start_xy | goal_xy | load |
|---|---|---:|---:|---:|---:|---|
| dqn_realmap_a | DQN9 original PGM/YAML + DQN10 realmap_a lineage | 410x129 | 0.1 | [34, 29] | [371, 109] | ok |
| willow_garage_0p10 | TurtleBot navigation Willow Garage map | 566x608 | 0.1 | [381, 222] | [253, 36] | ok |

## DQN10 重复快照核查

- NPZ 快照数量: 20
- 唯一数组哈希数量: 1
- hash_counts: `{'b7aa11d982ac18bf172f5769bc40c03a6fc5a8057fa80b6b09e0bd27ffe86597': 20}`

## 产物

- Manifest: `2_experiment/forest_n3p/assets/realmaps/manifest.json`
- Overview preview: `2_experiment/forest_n3p/assets/realmaps/preview_overview.png`
