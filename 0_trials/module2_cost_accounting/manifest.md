---
status: d01_analytic_cost_telemetry_smoke_complete
origin: codex
reviewed: false
created: 2026-07-03
source_head: 1ff1fa4626d65c8cf67542d7030305f54be1b00d
---

# Module2 Cost Accounting Manifest

## Scope

This directory stores Module2 Phase D cost-accounting artifacts. Phase D is a
budget gate before any RL-RS funnel implementation. It should answer whether a
neural rollout plus terminal RS could plausibly beat the current Dang multi-RS
analytic expansion cost.

## D01.1 Analytic Cost Telemetry Smoke

Status: `telemetry_smoke_complete`

Code scope:

- `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py`
- `2_experiment/forest_n3p/evaluation.py`
- `2_experiment/forest_n3p/tests/test_hybrid_astar_analytic_operator.py`
- `2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py`

Telemetry fields:

| Field | Meaning |
|---|---|
| `analytic_candidate_radius_count` | Number of radii evaluated across analytic attempts. |
| `analytic_candidate_success_count` | Radius candidates whose RS path sampled and collision-checked successfully. |
| `analytic_candidate_failure_count` | Radius candidates rejected by RS solve, sampling, goal tolerance, or collision. |
| `analytic_rs_solve_time_s` | Time spent in `reeds_shepp_shortest_path`. |
| `analytic_sample_time_s` | Time spent sampling constant-steer segments. |
| `analytic_collision_check_time_s` | Time spent in path collision checks. |
| `analytic_cost_eval_time_s` | Time spent evaluating Dang Eq. 3-4 cost. |
| `analytic_total_time_s` | Wall-clock time for analytic expansion attempts. |
| `analytic_sample_count` | Number of sampled poses produced for candidate checking. |
| `analytic_collision_check_count` | Number of candidate segment collision-check calls. |

Smoke artifact:

- `d01_analytic_cost_telemetry_smoke/summary.json`

Smoke result:

| Operator | Attempts | Successes | Radius candidates | Candidate successes | RS solve s | Sample s | Collision-check s | Cost-eval s | Total analytic s | Samples | Collision checks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `dang_multi_rs` | 1 | 1 | 11 | 11 | 0.0003742900 | 0.0000428740 | 0.0002604170 | 0.0001455000 | 0.0009104580 | 101 | 11 |

Verification:

```bash
PYTHONPATH=2_experiment python -m py_compile \
  2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py \
  2_experiment/forest_n3p/evaluation.py

PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_hybrid_astar_analytic_operator.py \
  2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py \
  2_experiment/forest_n3p/tests/test_inference_timing.py \
  -q
```

Result:

- `py_compile`: pass
- `pytest`: `9 passed in 1.00s`

Boundary:

- This smoke only proves the telemetry mechanism works and is visible from
  planner stats / evaluation metadata.
- It is not yet the D01.2 cost distribution over the C01/C02 query set.
- It does not compare against NN forward or rollout cost; that remains D02.

Experiment record:

- `.pipeline/experiments/20260703_module2_d01_analytic_cost_telemetry.md`

## D01.2 Analytic Cost Distribution

Status: `cost_distribution_complete`

Source head:

- `c152ed20cdced9034bca6932d65d0e4d1299f73e`

Command:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_analytic_cost_distribution \
  --output-dir 0_trials/module2_cost_accounting/d01_analytic_cost_distribution \
  --queries-per-bucket 10 \
  --seed-count 1 \
  --queries-per-map 5 \
  --density-profile-buckets validation_t06 \
  --buckets Complex,Extreme \
  --analytic-operator dang_multi_rs \
  --timeout-s 2.5 \
  --max-nodes 15000 \
  --source-head c152ed20cdced9034bca6932d65d0e4d1299f73e
```

Outputs:

- `d01_analytic_cost_distribution/summary.json`
- `d01_analytic_cost_distribution/query_costs.parquet`
- `d01_analytic_cost_distribution/attempt_costs.parquet`
- `d01_analytic_cost_distribution/candidate_costs.parquet`
- `d01_analytic_cost_distribution_stdout.txt`
- `d01_analytic_cost_distribution_stderr.txt`

Result:

| Metric | Value |
|---|---:|
| Queries | 20 |
| Analytic attempts | 8622 |
| Radius candidates | 94842 |
| Attempt total time p50 s | 0.000814 |
| Attempt total time p95 s | 0.002025 |
| Attempt total time p99 s | 0.002829 |
| Total plan time s | 24.751256 |
| Total analytic expansion time s | 8.215955 |
| Analytic / plan time ratio | 0.331941 |

Boundary:

- This is a local budget audit over the C01/C02 query configuration.
- It does not pass or fail Gate #1 by itself; D02 NN forward and rollout
  collision costs are still missing.
- Attempt counts are timeout-sensitive and should be treated as this run's
  source-bound artifact, not a cross-run invariant.

Experiment record:

- `.pipeline/experiments/20260703_module2_d01_cost_distribution.md`
