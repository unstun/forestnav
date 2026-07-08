# Module2 Planner-Integration Diagnostic Probe Summary

Diagnostic probe with a Gate3-failed checkpoint. Not formal evidence. No paper claims. Informs the next contract decision only.

## Scope

- Status: diagnostic, non-formal, no paper claims.
- Checkpoint: `0_trials/module2_gate3_formal_v3/seed20260709/train/final_model.zip`.
- Query manifest: `0_trials/module2_planner_probe/query_manifest.csv`, reused verbatim, 40 Complex + 40 Extreme, seed 20260710.
- Execution host: gpu3070ti-relay; M3 run source HEAD `0de18b9b3c73a9407fab57876056b49b35b4f79a`; D6 summary regenerated after M3 artifact commit `2972e153695ad5f65ae7d3a7b430116079e07b66`.
- M1/M2 baselines are reused unchanged from the prior probe; only M3 was rerun.
- M3 crash rule: M3 query crashes count as M3 failures. After the environment fix, no `m3_exception:*` rows remain.

## Per-Bucket Table

| Bucket | Method | Success rate | Timeout rate | Median exp | P95 exp | Median time s | P95 time s | Median path inflation | Collision violations | RL attempts | RL success rate | Mean NN forward s | Fallbacks |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Complex | M1 vanilla HA* / single_rs | 0.675 | 0.325 | 737.5 | 6537.9 | 0.5062 | 2.5005 | NA | 0 | 0 | NA | NA | 15868 |
| Complex | M2 Dang multi-curvature RS / dang_multi_rs | 0.750 | 0.250 | 355.5 | 3977.4 | 0.3686 | 2.5014 | 0.0009 | 0 | 0 | NA | NA | 8572 |
| Complex | M3 HA* + RL-RS PPO funnel / ha_rl_rs_ppo | 0.900 | 0.100 | 1.0 | 218.2 | 0.2374 | 2.5192 | 0.0310 | 0 | 233 | 0.1545 | 0.0811 | 197 |
| Extreme | M1 vanilla HA* / single_rs | 0.725 | 0.275 | 870.0 | 6195.6 | 0.5843 | 2.5005 | NA | 0 | 0 | NA | NA | 15011 |
| Extreme | M2 Dang multi-curvature RS / dang_multi_rs | 0.675 | 0.325 | 562.5 | 4613.2 | 0.4915 | 2.5012 | 0.0021 | 0 | 0 | NA | NA | 10284 |
| Extreme | M3 HA* + RL-RS PPO funnel / ha_rl_rs_ppo | 0.775 | 0.225 | 37.0 | 307.8 | 0.4632 | 2.5709 | 0.0169 | 0 | 555 | 0.0559 | 0.1324 | 524 |

## M3 vs M1 Paired Comparisons

| Bucket | Paired queries | Median expansions ratio M3/M1 | Median time ratio M3/M1 |
|---|---:|---:|---:|
| Complex | 40 | 0.0136 | 0.8528 |
| Extreme | 40 | 0.0370 | 1.0054 |

## Extreme-Bucket Band

- M3 vs M1 success delta: 5.0 percentage points.
- M3/M1 median time ratio: 0.7928.
- M3/M1 median expansions ratio: 0.0425.
- Reported band verdict: `no_signal`.
- Mechanical threshold basis: strong requires Extreme success delta >= +10pp and median time <= 110% of M1; weak requires median expansions <= 70% of M1 and time > 110%; otherwise no_signal.

## M3 Failure Condition

- M3 failure reasons: `{"": 67, "timeout": 13}`.
- No M3 query crashed after the environment fix; the >50% same-exception infrastructure stop condition did not trigger.
- Timeouts remain ordinary per-query planning failures under the frozen protocol; no timeout or parameter tuning was applied.

## Operator Telemetry For M3

| Bucket | RL attempts | RL successes | RL attempt success rate | RS attempts | Mean NN forward s | P95 NN forward s | Fallbacks |
|---|---:|---:|---:|---:|---:|---:|---:|
| Complex | 233 | 36 | 0.1545 | 5174 | 0.0811 | 0.4274 | 197 |
| Extreme | 555 | 31 | 0.0559 | 8688 | 0.1324 | 0.4054 | 524 |

## Artifact Index

- M1 records: `0_trials/module2_planner_probe/M1/records.csv`.
- M1 summary: `0_trials/module2_planner_probe/M1/summary_by_method_bucket.csv`.
- M2 records: `0_trials/module2_planner_probe/M2/records.csv`.
- M2 summary: `0_trials/module2_planner_probe/M2/summary_by_method_bucket.csv`.
- M3 records: `0_trials/module2_planner_probe/M3/records.csv`.
- M3 summary: `0_trials/module2_planner_probe/M3/summary_by_method_bucket.csv`.
- Combined summary CSV: `0_trials/module2_planner_probe/probe_summary.csv`.
- Paired comparison CSV: `0_trials/module2_planner_probe/paired_m3_vs_m1.csv`.
- Band verdict JSON: `0_trials/module2_planner_probe/probe_band_verdict.json`.
