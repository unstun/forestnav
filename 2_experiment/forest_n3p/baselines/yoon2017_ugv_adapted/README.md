# Yoon2017-UGV Adapted Baseline

This adapter uses the independent `2_experiment/yoon2017_strict_repro` package for the Yoon2017 SS-RRT* algorithm and only changes vehicle/map integration for the local UGV benchmark.

Paper-reported algorithm defaults kept here:

- `steer_step_m = 5.0`
- strict package default `goal_sample_rate = 0.05`

Implementation defaults made explicit because the paper does not fully specify them:

- `neighbor_radius_m = 5.0`
- Fig. 7 `gamma` is computed per edge from `x_near-x_int-x_new`, following the paper geometry.
- `samples_per_segment = 24`

This baseline should be described as `Yoon2017-UGV adapted`, not as the original Yoon2017 implementation.
