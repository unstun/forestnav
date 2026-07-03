---
status: smoke_pass
origin: codex
reviewed: false
created: 2026-07-03
source_head: 190d28b34f8c6b6608b99b1d368bdc7e9d2bba4d
---

# Module2 Timing Smoke Manifest

## Scope

Targeted B01.3 smoke for timing-accounting artifacts only. This run is not a
formal T14 result and must not be used as paper evidence for performance claims.

Scale:

- Methods: `vanilla_ha`, `f_n3p_knn`
- Query set: 9 queries total, 3 per difficulty bucket
- Buckets: Easy, Complex, Extreme
- Seed count: 1
- Queries per map: 3
- Bootstrap resamples: 200
- T06 bucket mode: `validation_t06`

## Failed Preflight Attempt

Directory:

- `0_trials/module2_timing_smoke/run_20260703_b01_3/`

Result:

- Exit code: 1
- Stdout: empty
- Stderr: `T14 profile bucket configuration is inconsistent`
- Cause: default `original_t06` profiles conflicted with the reviewed human decision
  `D-T14-09=revise_to_validation_cutpoints`.

This attempt is preserved as evidence that the smoke did not bypass preflight.

## Passing Smoke

Directory:

- `0_trials/module2_timing_smoke/run_20260703_b01_3_validation_t06/`

Command:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_main_evaluation \
  --output-dir 0_trials/module2_timing_smoke/run_20260703_b01_3_validation_t06 \
  --queries-per-bucket 3 \
  --seed-count 1 \
  --queries-per-map 3 \
  --methods vanilla_ha,f_n3p_knn \
  --density-profile-buckets validation_t06 \
  --allow-unreviewed-cutpoints \
  --allow-unresolved-human-review \
  --no-enforce-t14-scale \
  --bootstrap-resamples 200 \
  --source-head 190d28b34f8c6b6608b99b1d368bdc7e9d2bba4d
```

Captured streams:

- `run_20260703_b01_3_validation_t06/stdout.txt`
- `run_20260703_b01_3_validation_t06/stderr.txt`

Outcome:

- Exit code: 0
- `stdout.txt`: `record_count=18`, `query_count=9`, `status=candidate_or_smoke`
- `stderr.txt`: empty
- `preflight.json`: `ok_to_run=true`, `profile_bucket_satisfied=true`,
  `t14_scale_satisfied=false`
- `verdict.json`: `collision_violation_total=0`, `method_exception_total=0`,
  `formal_acceptance=false`

Timing protocol check:

- `records.csv` includes `metadata.timing_protocol.adapter=planner_run_from_path_stats`
  for `vanilla_ha`.
- `records.csv` includes `metadata.timing_protocol.adapter=planner_run_from_result`
  for `f_n3p_knn`.
- `records.csv` includes `metadata.total_planner_time_s` for both methods.

Method counts from `records.csv`:

| method | count | success | feasible | timing adapter |
|---|---:|---:|---:|---|
| `vanilla_ha` | 9 | 8 | 8 | `planner_run_from_path_stats` |
| `f_n3p_knn` | 9 | 8 | 8 | `planner_run_from_result` |

Artifacts:

- `run_20260703_b01_3_validation_t06/records.csv`
- `run_20260703_b01_3_validation_t06/summary_by_method_bucket.csv`
- `run_20260703_b01_3_validation_t06/summary.json`
- `run_20260703_b01_3_validation_t06/queries.csv`
- `run_20260703_b01_3_validation_t06/preflight.json`
- `run_20260703_b01_3_validation_t06/run_config.json`
- `run_20260703_b01_3_validation_t06/verdict.json`
- `run_20260703_b01_3_validation_t06/report.md`

## Boundary

This smoke only verifies that the timing metadata and evaluation outputs are
generated under a small, reviewed-bucket configuration. It does not satisfy the
formal T14 scale requirement, all official baseline requirement, or Module2 RL
analytic operator requirement.
