# F-N3P Experiment Package

This package is the implementation home for the v9 ForestNav method:
oracle-supervised SE(2) subgoal decomposition plus segment-wise Hybrid A*.

## Current Scope

T01 establishes the runnable skeleton only:

- `maps/forest.py`: procedural forest occupancy grid map generation copied from DQN10.
- `maps/pgm.py`: ROS PGM occupancy grid map loader copied from DQN10 and retargeted to `forest_n3p`.
- `third_party/pathplan`: vendored Hybrid A* / Reeds-Shepp planning code copied from DQN10.
- `forest_policy.py`: DQN10 forest action gating reference, retained for the MD-DQN baseline lineage.
- `configs/default.json`: pilot defaults from the v9 design and Contract.

The default configuration is not frozen experimental evidence. The approved
Contract still requires pilot calibration for difficulty cut points and for
`L_max`, `L_min`, `N_seg`, `R_max`, and `n_ray`.

## Import Contract

Run from the repository root with `PYTHONPATH=2_experiment`:

```bash
python -c "import pathplan; from forest_n3p import configs; print('OK')"
```

`pathplan` is exposed through `2_experiment/pathplan` as a compatibility alias
to `forest_n3p.third_party.pathplan`, so future scripts can use the short import
name while keeping the vendored source inside the F-N3P package.
