---
origin: ai_only
reviewed: false
status: migration_complete_rerun_pending
created_at: 2026-06-26
updated_at: 2026-06-26
---

# T14 DQN10 Full Migration Status

## Summary

DQN10 Ackermann baseline migration is complete in local source and committed as
`f85a146a` (`Migrate DQN10 Ackermann baselines`). The official main evaluation
method set now contains 11 methods and excludes `md_dqn`.

This file is a status page, not a new formal experiment result. The new
11-method 50q remote rerun has not started yet.

## Official method set after migration

- `f_n3p_knn`
- `vanilla_ha`
- `n3p_k1`
- `voronoi_waypoint`
- `bottleneck_waypoint`
- `dang2022_ugv_adapted`
- `lo_ha`
- `yoon2017_ugv_adapted`
- `lian2023_ugv_adapted`
- `idb_rrt_ugv_adapted`
- `apf_local`

`md_dqn` is removed from the current official method set. If a full MD-DQN
forest-distribution baseline is trained later, it should be introduced by a new
contract decision rather than silently reusing the old placeholder.

## Verification performed

- DQN10 import smoke: 20 baseline entries passed.
- Light runtime smoke: Dang/LO/Yoon/iDb/APF and aliases passed on tiny maps;
  Lian lowered-budget smoke reached optimization infeasibility rather than an
  import/runtime integration error.
- `tests/test_main_evaluation.py`: 12 passed.
- `pytest tests -q --ignore=tests/test_inference.py`: 57 passed.
- Full `pytest tests -q`: blocked during collection because local environment
  lacks `sklearn`; this is not specific to the migration diff.

## Existing 2026-06-25 9-method run

Existing path:
`.pipeline/experiments/20260625_t14_9method_50q_remote`

That run remains:

- methods: 9
- queries: 150
- records: 1350
- status: `formal_fail`
- `method_exception_total`: 0
- `collision_violation_total`: 0

New comparison artifacts generated from the existing run:

- `.pipeline/experiments/20260625_t14_9method_50q_remote/figures/all_algorithms_one_figure.png`
- `.pipeline/experiments/20260625_t14_9method_50q_remote/method_comparison_overall.csv`
- `.pipeline/experiments/20260625_t14_9method_50q_remote/method_comparison_overall.md`
- `.pipeline/experiments/20260625_t14_9method_50q_remote/method_comparison_detailed.csv`
- `.pipeline/experiments/20260625_t14_9method_50q_remote/method_comparison_detailed.md`

## Timing note

Yesterday's 9-method 50q log only contains the final JSON summary and does not
record start/end/duration. The best available estimate is about 23m52s, inferred
from log filename `20260625_t14_9method_50q_remote_20260625_142901.log` and
remote artifact mtime `2026-06-25 14:52:53 -0400`.

This is an inferred duration, not a hard timing record.

## Rerun status

The intended next run is a full 11-method 50q remote rerun with explicit
`--source-head f85a146a` and a separate `run_timing.json`.

It has not started. A remote sync attempt was interrupted and the lingering
local `rsync`/`ssh` process was stopped. Before launching the next formal run,
verify remote source state and avoid treating the interrupted sync as complete.
