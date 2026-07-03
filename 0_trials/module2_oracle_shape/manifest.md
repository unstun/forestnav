---
status: c01_failure_nodes_collected
origin: codex
reviewed: false
created: 2026-07-03
collection_source_head: e39c316d3c7cbed514193126788be244e38517f2
dedup_source_head: a1633c603a69e3f55609aa588f5fab54cf169a65
---

# Module2 Oracle Shape Failure Node Manifest

## Scope

C01 collects failed Hybrid A* analytic expansion states for the later oracle
shape gate. This artifact is an input dataset for C02, not a final conclusion
about whether RL steering is viable.

Collection scale:

- Buckets: Complex, Extreme
- Queries per bucket: 10
- Seed count: 1
- Queries per map: 5
- Analytic operator: `dang_multi_rs`
- Timeout: 2.5 s
- Max nodes: 15000
- T06 bucket mode: `validation_t06`

## C01.1 Raw Failure Nodes

Command:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.collect_rs_failure_nodes \
  --output 0_trials/module2_oracle_shape/rs_failure_nodes.parquet \
  --queries-per-bucket 10 \
  --seed-count 1 \
  --queries-per-map 5 \
  --density-profile-buckets validation_t06 \
  --buckets Complex,Extreme \
  --analytic-operator dang_multi_rs \
  --timeout-s 2.5 \
  --max-nodes 15000 \
  --source-head e39c316d3c7cbed514193126788be244e38517f2
```

Outputs:

- `rs_failure_nodes.parquet`
- `rs_failure_nodes_summary.json`
- `rs_failure_nodes_stdout.txt`
- `rs_failure_nodes_stderr.txt`

Result:

- `query_count=20`
- `row_count=8752`
- `stderr`: empty

Required fields present:

- `query_id`, `difficulty_bucket`, `expansion_idx`
- `state_x`, `state_y`, `state_theta`
- `goal_x`, `goal_y`, `goal_theta`
- `h_holo`, `h_rs`, `nearest_obstacle_m`
- `failed_radii`, `failed_radius_count`

## C01.2 Deduplicated Failure Nodes

Command:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.dedupe_rs_failure_nodes \
  --input 0_trials/module2_oracle_shape/rs_failure_nodes.parquet \
  --output 0_trials/module2_oracle_shape/rs_failure_nodes_dedup.parquet \
  --resolution-m 0.1 \
  --theta-bins 72 \
  --source-head a1633c603a69e3f55609aa588f5fab54cf169a65
```

Outputs:

- `rs_failure_nodes_dedup.parquet`
- `rs_failure_nodes_dedup_summary.json`
- `rs_failure_nodes_dedup_stdout.txt`
- `rs_failure_nodes_dedup_stderr.txt`

Result:

- Input rows: 8752
- Dedup rows: 7860
- Dropped duplicates: 892
- Dedup key: `(query_id, state_gx, state_gy, state_theta_bin)`
- `stderr`: empty

Additional dedup fields:

- `state_gx`, `state_gy`, `state_theta_bin`
- `duplicate_count`
- `dedup_key`
- `dedup_source_head`

## Boundary

This dataset is intentionally pre-oracle. It says where RS analytic expansion
failed, not whether those states are solvable by a local connector. C02 must run
oracle checks before any RL-steering design claim is allowed.
