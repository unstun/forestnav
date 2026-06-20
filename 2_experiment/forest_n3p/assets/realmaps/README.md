# F-N3P RealMap Assets

These maps are the T07 validated ROS PGM/YAML assets for ForestNav.
They are intended as real-map evaluation inputs, not as procedural forest scenes.

| id | source | size | resolution | preview |
|---|---|---:|---:|---|
| dqn_realmap_a | DQN9 original PGM/YAML + DQN10 realmap_a lineage | 410x129 | 0.1 m/cell | 2_experiment/forest_n3p/assets/realmaps/dqn_realmap_a/preview.png |
| willow_garage_0p10 | TurtleBot navigation Willow Garage map | 566x608 | 0.1 m/cell | 2_experiment/forest_n3p/assets/realmaps/willow_garage_0p10/preview.png |

Notes:
- `dqn_realmap_a` is the local DQN RealMap source; DQN10 keeps this map as
  NPZ fallback snapshots, while DQN9 preserves the original PGM/YAML pair.
- `willow_garage_0p10` is copied from the BSD-licensed TurtleBot navigation
  map package to satisfy the T07 two-map loading/display gate without
  counting repeated DQN10 snapshots as independent maps.
