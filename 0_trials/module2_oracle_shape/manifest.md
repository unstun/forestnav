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

## C02.1 Default-Budget Pilot

Status: `pilot_pass_not_gate`

Purpose:

- Estimate default oracle-budget runtime before starting all 7860 rows.
- Unlike earlier smoke commands, this pilot uses the analysis script defaults:
  Oracle A `8 s / 50000 nodes`, Oracle B `4 s / 25000 nodes`, and
  `32` candidates.

Command:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_oracle_connector_chunks \
  --input 0_trials/module2_oracle_shape/rs_failure_nodes_dedup.parquet \
  --output-dir 0_trials/module2_oracle_shape/oracle_connector_default_budget_pilot20 \
  --merged-output 0_trials/module2_oracle_shape/oracle_connector_results_default_budget_pilot20.parquet \
  --max-records 20 \
  --chunk-size 10 \
  --source-head 19962660f81a5cab27921ec9f5dd32b8cafe798e
```

Outputs:

- `oracle_connector_default_budget_pilot20/summary.json`
- `oracle_connector_default_budget_pilot20/chunks/`
- `oracle_connector_results_default_budget_pilot20.parquet`
- `oracle_connector_default_budget_pilot20_stdout.txt`
- `oracle_connector_default_budget_pilot20_stderr.txt`

Result:

- Selected rows: 20 / 7860
- Chunk count: 2
- Oracle A success: 20 / 20
- Oracle B success: 20 / 20
- Oracle connectable: 20 / 20
- Root stderr: 0 bytes
- Chunk stderr: 0 bytes each
- Wall-clock observed by main session: about 40 seconds for 20 rows, roughly
  2 seconds per row on this machine.
- Rough full-run estimate: 4-5 hours for 7860 rows, before any harder-node
  timeout skew.

Boundary:

- This is still the first 20 Complex rows only, so it is a runtime pilot and
  toolchain sanity check, not Gate #2 evidence.

## C02.1 Full Default-Budget Run

Status: `full_run_complete_not_final_gate`

Source head:

- `1f4f96f82bca68f06cc6e9a08adb9ea9aaf993a5`

Command:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_oracle_connector_chunks \
  --input 0_trials/module2_oracle_shape/rs_failure_nodes_dedup.parquet \
  --output-dir 0_trials/module2_oracle_shape/oracle_connector_full \
  --merged-output 0_trials/module2_oracle_shape/oracle_connector_results.parquet \
  --chunk-size 100 \
  --source-head 1f4f96f82bca68f06cc6e9a08adb9ea9aaf993a5
```

Execution note:

- The run used the chunk runner's resume/skip contract. Disjoint far-ahead
  chunks were precomputed while the main runner handled the contiguous gap.
- One auxiliary `chunk_006000_006099` attempt was stopped before parquet/summary
  emission to avoid a race with the main runner. The accepted final
  `chunk_006000_006099` artifact was produced by the main runner.
- Final root summary is `status=complete`; chunk summaries report no nonzero
  return codes.

Outputs:

- `oracle_connector_full/summary.json`
- `oracle_connector_full/chunks/`
- `oracle_connector_results.parquet`
- `oracle_connector_full_stdout.txt`
- `oracle_connector_full_stderr.txt`
- `oracle_connector_full_analysis.json`
- `oracle_connector_b_only_cases.csv`
- `oracle_connector_a_only_cases.csv`
- `oracle_connector_invalid_query_counts.csv`

Integrity checks:

- Input rows: 7860
- Selected rows: 7860
- Chunk count: 79
- Chunk four-file sets missing: 0
- Nonzero chunk summaries: 0
- Merged rows: 7860
- Merged columns: 58
- `source_head` values in merged parquet: one value, all
  `1f4f96f82bca68f06cc6e9a08adb9ea9aaf993a5`

Full-run result:

| Metric | Count |
|---|---:|
| Rows | 7860 |
| Oracle A success | 6226 |
| Oracle B success | 6287 |
| Oracle connectable | 6289 |
| Both A and B success | 6224 |
| B-only | 63 |
| A-only | 2 |
| Unresolved | 1571 |

By bucket:

| Bucket | Rows | Oracle A | Oracle B | Connectable |
|---|---:|---:|---:|---:|
| Complex | 3368 | 2596 | 2596 | 2597 |
| Extreme | 4492 | 3630 | 3691 | 3692 |

Failure triage:

- Oracle A failure reasons: `goal_in_collision=1182`,
  `start_in_collision=389`, `timeout=63`.
- The 1571 unresolved rows are exactly the
  `goal_in_collision/start_in_collision` rows.
- After excluding those invalid start/goal rows, remaining rows are 6289/7860
  and oracle connectable is 6289/6289.
- All 63 timeout rows are connectable by Oracle B.
- B-only selected source distribution: `goal_annulus=58`,
  `voronoi_skeleton=5`.

Boundary:

- This full run proves that the C02.1 oracle machinery covers all 7860
  deduplicated RS failure nodes under the default budget.
- It does not by itself finish Gate #2. C02.2 still needs visual/shape labels,
  because "connectable" does not say whether the shape is a narrow bottleneck,
  short obstacle-avoidance detour, reverse maneuver, or dirty invalid endpoint.
- The strongest mechanical implication is that the current dataset has no
  non-invalid oracle-no-solution rows under this oracle. The RL target is
  therefore narrower than "all RS failures": it should focus on timeout and
  operator-cost cases, not invalid endpoints.

## C02.2 Shape Label Visual Seed

Status: `visual_seed_complete_not_gate`

Source head:

- `833eb1a4`

Script:

- `2_experiment/forest_n3p/scripts/render_oracle_connector_cases.py`

Command:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.render_oracle_connector_cases \
  --results 0_trials/module2_oracle_shape/oracle_connector_results.parquet \
  --output-dir 0_trials/module2_oracle_shape/c02_shape_labels \
  --source-head 833eb1a4
```

Outputs:

- `c02_shape_labels/summary.json`
- `c02_shape_labels/index.md`
- `c02_shape_labels/invalid_goal_complex.png`
- `c02_shape_labels/invalid_goal_extreme.png`
- `c02_shape_labels/invalid_start_extreme.png`
- `c02_shape_labels/b_only_complex_timeout.png`
- `c02_shape_labels/b_only_extreme_goal_annulus.png`
- `c02_shape_labels/a_only_complex_conservative_b.png`
- `c02_shape_labels/a_only_extreme_conservative_b.png`

Visual categories:

| Shape label | Count in seed | Meaning |
|---|---:|---|
| `invalid_goal_in_collision` | 2 | The final goal is inside an occupied footprint region. |
| `invalid_start_in_collision_goal_also_blocked` | 1 | The failed node is already colliding; in this representative case the goal is also blocked. |
| `timeout_saved_by_goal_annulus` | 2 | Oracle A times out, while Oracle B reaches a goal-annulus candidate and terminal RS connects to the goal. |
| `oracle_b_conservative_combined_collision_rejection` | 2 | Oracle A succeeds; current Oracle B rejects candidates at the combined-path acceptance stage. |

Verification:

- `summary.json` status is `complete`, `case_count=7`.
- All PNGs are `1393 x 1292`.
- Image QA checked dimensions, color diversity, and that B-success rows replay
  as `rendered_b_success=true`.

Boundary:

- This is a first visual seed set for C02.2, not the final Gate #2 decision.
- The visual positives currently use reproducible `goal_annulus` B-only rows.
- The 5 full-run `voronoi_skeleton` B-only rows currently fail replay:
  each had 38 RS-reachable candidates in the full result, but current
  candidate regeneration returns 0 candidates. They must be audited before
  being used as paper evidence.

Experiment record:

- `.pipeline/experiments/20260703_module2_c02_shape_labels.md`

## C02.3 Gate #2 Oracle Shape Decision

Status: `gate2_not_failed_scope_narrowed`

Source head:

- `be2c7f14`

Input artifacts:

- `oracle_connector_results.parquet`
- `oracle_connector_full/summary.json`
- `c02_shape_labels/summary.json`
- `c02_shape_labels/index.md`

Independent verification result:

| Item | Value |
|---|---:|
| Full status | `complete` |
| Chunk count | 79 |
| Rows | 7860 |
| Invalid start/goal | 1571 |
| Non-invalid rows | 6289 |
| Non-invalid connectable | 6289 |
| Non-invalid unresolved | 0 |
| B-only | 63 |
| A-only | 2 |
| Both success | 6224 |
| Total unresolved | 1571 |
| Shape-label cases | 7 |
| Replayed/rendered B-success visual cases | 2 |

B-only selected source distribution:

| Source | Count | Evidence status |
|---|---:|---|
| `goal_annulus` | 58 | Reproducible visual positives exist. |
| `voronoi_skeleton` | 5 | Replay mismatch; do not use as paper evidence until audited. |

Decision:

- Gate #2 no-solution failure is not triggered, because all 6289 non-invalid
  rows are oracle-connectable under the C02.1 budget.
- The broad claim "most RS failures need RL" is rejected. Invalid endpoints
  dominate unresolved rows, and B-only timeout rows are narrow.
- D01/D02 cost accounting is the next allowed step before any RL-RS funnel
  implementation or PPO training.

Experiment record:

- `.pipeline/experiments/20260703_module2_gate2_oracle_shape.md`
