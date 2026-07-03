---
status: smoke_pass_v2
origin: codex
reviewed: false
created: 2026-07-03
source_head: ec96ffa217ab0af2665ff8018794400be5ecb6f3
---

# Module2 Analytic Operator Baseline Smoke Manifest

## Scope

Targeted B02.3 smoke for attributing the contribution of the Hybrid A* analytic
expansion slot before replacing it with an RL operator. This is not a formal
T14 result and must not be used as paper performance evidence.

Scale:

- Methods: `ha_no_analytic`, `ha_single_rs`, `ha_dang_multi_rs`
- Query set: 9 queries total, 3 per difficulty bucket
- Buckets: Easy, Complex, Extreme
- Seed count: 1
- Queries per map: 3
- Bootstrap resamples: 200
- T06 bucket mode: `validation_t06`

## Run History

### v1: Missing Analytic Telemetry

Directory:

- `0_trials/module2_operator_baseline_smoke/run_20260703_b02_3/`

Result:

- Exit code: 0
- `record_count=27`, `query_count=9`
- Problem: `records.csv` preserved `analytic_operator`, but did not preserve
  `analytic_attempts` or `analytic_successes` from planner stats.
- Follow-up: `planner_run_from_path_stats()` was updated so these planner stats
  are copied into `EvaluationRun.metadata`.

### v2: Valid B02.3 Smoke

Directory:

- `0_trials/module2_operator_baseline_smoke/run_20260703_b02_3_v2/`

Command:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_main_evaluation \
  --output-dir 0_trials/module2_operator_baseline_smoke/run_20260703_b02_3_v2 \
  --queries-per-bucket 3 \
  --seed-count 1 \
  --queries-per-map 3 \
  --methods ha_no_analytic,ha_single_rs,ha_dang_multi_rs \
  --density-profile-buckets validation_t06 \
  --allow-unreviewed-cutpoints \
  --allow-unresolved-human-review \
  --no-enforce-t14-scale \
  --bootstrap-resamples 200 \
  --source-head ec96ffa217ab0af2665ff8018794400be5ecb6f3
```

Captured streams:

- `run_20260703_b02_3_v2/stdout.txt`
- `run_20260703_b02_3_v2/stderr.txt`

Outcome:

- Exit code: 0
- `stdout.txt`: `record_count=27`, `query_count=9`, `status=candidate_or_smoke`
- `stderr.txt`: empty
- `verdict.json`: `collision_violation_total=0`, `method_exception_total=0`,
  `formal_acceptance=false`

Telemetry check from `records.csv`:

| method | operator | records | feasible | analytic attempts | analytic successes |
|---|---|---:|---:|---:|---:|
| `ha_no_analytic` | `disabled` | 9 | 8 | 0 | 0 |
| `ha_single_rs` | `single_rs` | 9 | 8 | 2733 | 8 |
| `ha_dang_multi_rs` | `dang_multi_rs` | 9 | 8 | 1504 | 8 |

Per-bucket summary:

| method | bucket | success_rate | median_time_s | median_expansions |
|---|---|---:|---:|---:|
| `ha_no_analytic` | Easy | 1.000 | 0.3929 | 658 |
| `ha_single_rs` | Easy | 1.000 | 0.1642 | 61 |
| `ha_dang_multi_rs` | Easy | 1.000 | 0.1588 | 31 |
| `ha_no_analytic` | Complex | 1.000 | 0.5344 | 1110 |
| `ha_single_rs` | Complex | 1.000 | 0.3894 | 729 |
| `ha_dang_multi_rs` | Complex | 0.667 | 0.5111 | 729 |
| `ha_no_analytic` | Extreme | 0.667 | 2.1416 | 7132 |
| `ha_single_rs` | Extreme | 0.667 | 1.1521 | 4477 |
| `ha_dang_multi_rs` | Extreme | 1.000 | 0.5304 | 1537 |

Artifacts:

- `run_20260703_b02_3_v2/records.csv`
- `run_20260703_b02_3_v2/summary_by_method_bucket.csv`
- `run_20260703_b02_3_v2/summary.json`
- `run_20260703_b02_3_v2/queries.csv`
- `run_20260703_b02_3_v2/preflight.json`
- `run_20260703_b02_3_v2/run_config.json`
- `run_20260703_b02_3_v2/verdict.json`
- `run_20260703_b02_3_v2/report.md`

## Boundary

This smoke only shows that the analytic expansion slot has measurable effect
and that the no-analytic/single-RS/Dang-multi-RS methods are now reproducible
through the common evaluation entrypoint. It is too small for a paper claim.
