---
origin: ai+local-source
reviewed: false
status: formal_fail
created_at: 2026-06-25
updated_at: 2026-06-25
---

# T14 9-method remote status

## Summary

The requested 9-method 50-query/bucket remote run completed on
`gpu3070ti-relay`. Deployment is no longer blocked: `main_idbastar` was built
from the official Dynoplan source using a no-sudo micromamba toolchain, then
used by the ForestNav `idb_rrt` adapter.

The run is complete but did not satisfy the T14 contract thresholds, so the
verdict is `formal_fail`, not `formal_acceptance`.

## Final 9-method run

- Path: `.pipeline/experiments/20260625_t14_9method_50q_remote`
- Log: `2_experiment/runs/20260625_t14_9method_50q_remote_20260625_142901.log`
- Queries: 150
- Records: 1350
- Methods: 9
- `official_methods_satisfied`: true
- `missing_official_methods`: []
- `method_exception_total`: 0
- `collision_violation_total`: 0
- `formal_acceptance`: false
- `status`: `formal_fail`

Official methods in the completed run:

- `f_n3p_knn`
- `vanilla_ha`
- `n3p_k1`
- `voronoi_waypoint`
- `bottleneck_waypoint`
- `improved_ha`
- `lo_ha`
- `ss_rrt`
- `idb_rrt`

`md_dqn` is not part of the current official method set or the completed
records.

## Contract failures

Complex bucket:

- `median_time_reduction`: 0.2154692446390205
- `success_drop_pp`: -17.999999999999993
- `median_path_inflation_ratio`: 0.03447259109623069
- Failed check: `median_time_reduction_ge_50pct`

Extreme bucket:

- `median_time_reduction`: 0.02143796528106101
- `success_drop_pp`: -20.000000000000007
- `median_path_inflation_ratio`: 0.06620978595837068
- Failed checks:
  - `median_time_reduction_ge_50pct`
  - `median_path_inflation_le_5pct`

## iDb-RRT deployment

`idb_rrt` was initially blocked because `gpu3070ti-relay` had no system
toolchain in PATH and sudo required a password. The unblock path used
micromamba under the user account:

- Micromamba root: `$HOME/micromamba-root`
- Environment: `dynoplan-build`
- Build directory:
  `2_experiment/idb_rrt_strict_repro/upstream/dynoplan/build-conda`
- Binary:
  `2_experiment/idb_rrt_strict_repro/upstream/dynoplan/build-conda/main_idbastar`

Dynoplan's `deps/nigh` submodule was empty after source sync. It was restored
from the official locked commit `4e1fad64b2ffecff0449d920dca332bd2eac4aa1`,
then `main_idbastar` built successfully.

## iDb-RRT result summary

- Easy: 50 records, 11 successes, success rate 0.22
- Complex: 50 records, 3 successes, success rate 0.06
- Extreme: 50 records, 2 successes, success rate 0.04

All `idb_rrt` per-query run directories were synchronized back locally under
`2_experiment/idb_rrt_strict_repro/runs/forestnav_adapter/`.
