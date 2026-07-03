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

## C02.1 Oracle Connector Smoke

Status: `smoke_pass_not_gate`

Script:

- `2_experiment/forest_n3p/scripts/run_oracle_connector_analysis.py`
- Source head: `f7bdb0e8a2a26d5b052b710fe299b799d1e85ee6`

Oracle definitions:

- Oracle A: Hybrid A* from failed analytic-expansion node to final goal with
  analytic operator disabled.
- Oracle B: generate intermediate poses from `goal_annulus`,
  `corridor_offset`, `edt_high_clearance`, and `voronoi_skeleton`; keep only
  candidates with collision-free RS to the final goal; plan from the failed node
  to the candidate with analytic disabled; then re-run RS from the actual segment
  endpoint to the final goal before accepting the combined path.

Complex smoke command:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_oracle_connector_analysis \
  --input 0_trials/module2_oracle_shape/rs_failure_nodes_dedup.parquet \
  --output 0_trials/module2_oracle_shape/oracle_connector_results_smoke5.parquet \
  --max-records 5 \
  --oracle-a-timeout-s 4 \
  --oracle-a-max-nodes 30000 \
  --oracle-b-segment-timeout-s 2 \
  --oracle-b-segment-max-nodes 15000 \
  --oracle-b-candidate-limit 16 \
  --source-head f7bdb0e8a2a26d5b052b710fe299b799d1e85ee6
```

Complex smoke outputs:

- `oracle_connector_results_smoke5.parquet`
- `oracle_connector_results_smoke5_summary.json`
- `oracle_connector_results_smoke5_stdout.txt`
- `oracle_connector_results_smoke5_stderr.txt`

Complex smoke result:

- Selected rows: 5 / 7860
- Bucket: Complex
- Oracle A success: 5 / 5
- Oracle B success: 5 / 5
- Oracle connectable: 5 / 5
- Candidate counts: 191-196 RS-reachable candidates per row
- Collision violations: 0 on accepted A/B paths
- `stderr`: empty

Extreme smoke command:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_oracle_connector_analysis \
  --input 0_trials/module2_oracle_shape/rs_failure_nodes_dedup.parquet \
  --output 0_trials/module2_oracle_shape/oracle_connector_results_smoke_extreme3.parquet \
  --row-offset 3368 \
  --max-records 3 \
  --oracle-a-timeout-s 4 \
  --oracle-a-max-nodes 30000 \
  --oracle-b-segment-timeout-s 2 \
  --oracle-b-segment-max-nodes 15000 \
  --oracle-b-candidate-limit 16 \
  --source-head f7bdb0e8a2a26d5b052b710fe299b799d1e85ee6
```

Extreme smoke outputs:

- `oracle_connector_results_smoke_extreme3.parquet`
- `oracle_connector_results_smoke_extreme3_summary.json`
- `oracle_connector_results_smoke_extreme3_stdout.txt`
- `oracle_connector_results_smoke_extreme3_stderr.txt`

Extreme smoke result:

- Selected rows: 3 / 7860
- Bucket: Extreme
- Oracle A success: 2 / 3
- Oracle B success: 3 / 3
- Oracle connectable: 3 / 3
- Candidate counts: 34-233 RS-reachable candidates per row
- Collision violations: 0 on accepted A/B paths
- Non-trivial case: `extreme_s00_q0001:150:45:26` has Oracle A failure but
  Oracle B success, so the B pipeline is not merely duplicating direct HA*.
- `stderr`: empty

Verification:

```bash
PYTHONPATH=2_experiment python -m py_compile \
  2_experiment/forest_n3p/scripts/run_oracle_connector_analysis.py

PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_hybrid_astar_analytic_operator.py \
  2_experiment/forest_n3p/tests/test_inference_timing.py \
  2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py \
  -q
```

Result:

- `py_compile`: pass
- `pytest`: `8 passed in 0.99s`

Boundary:

- This is a bounded C02.1 smoke, not the full Gate #2 result.
- Full C02.1 still needs all 7860 deduplicated RS failure nodes, or a
  preregistered stratified subset if the full run is too expensive.

## C02.1 Chunk Runner Smoke

Status: `runner_smoke_pass`

Script:

- `2_experiment/forest_n3p/scripts/run_oracle_connector_chunks.py`
- Source head: `e0dbe829f74e363ee73e6e8fb70e911b944480d7`

Purpose:

- Full C02.1 can take hours. The runner makes the long run resumable by writing
  independent chunk parquet/stdout/stderr/summary artifacts, then merging the
  chunk parquet files into one result table.

Command:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_oracle_connector_chunks \
  --input 0_trials/module2_oracle_shape/rs_failure_nodes_dedup.parquet \
  --output-dir 0_trials/module2_oracle_shape/oracle_connector_runner_smoke \
  --merged-output 0_trials/module2_oracle_shape/oracle_connector_results_runner_smoke.parquet \
  --max-records 3 \
  --chunk-size 2 \
  --source-head e0dbe829f74e363ee73e6e8fb70e911b944480d7 \
  --oracle-a-timeout-s 4 \
  --oracle-a-max-nodes 30000 \
  --oracle-b-segment-timeout-s 2 \
  --oracle-b-segment-max-nodes 15000 \
  --oracle-b-candidate-limit 16
```

Outputs:

- `oracle_connector_runner_smoke/summary.json`
- `oracle_connector_runner_smoke/chunks/chunk_000000_000001.parquet`
- `oracle_connector_runner_smoke/chunks/chunk_000002_000002.parquet`
- corresponding chunk stdout/stderr/summary files
- `oracle_connector_results_runner_smoke.parquet`
- `oracle_connector_runner_smoke_stdout.txt`
- `oracle_connector_runner_smoke_stderr.txt`

Result:

- Selected rows: 3 / 7860
- Chunk count: 2
- Merged rows: 3
- Oracle A success: 3 / 3
- Oracle B success: 3 / 3
- Oracle connectable: 3 / 3
- Root stderr: 0 bytes
- Chunk stderr: 0 bytes each

Boundary:

- This validates long-run execution mechanics only. It does not add new Gate #2
  evidence beyond the bounded oracle smoke above.
