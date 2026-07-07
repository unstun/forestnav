# Module2 Planner-Integration Diagnostic Probe Summary

Diagnostic probe with a Gate3-failed checkpoint. Not formal evidence. No paper claims. Informs the next contract decision only.

## Scope

- Status: diagnostic, non-formal, no paper claims.
- Checkpoint: `0_trials/module2_gate3_formal_v3/seed20260709/train/final_model.zip`.
- Query manifest: `0_trials/module2_planner_probe/query_manifest.csv`, 40 Complex + 40 Extreme, seed 20260710.
- Execution host: gpu3070ti-relay, source HEAD `f2043f60b0c46bea3d90ac27b0afc59e7af80ffa`.
- M3 crash rule: M3 query crashes count as M3 failures; no dependency install or rerun fix was applied.

## Per-Bucket Table

| Bucket | Method | Success rate | Timeout rate | Median exp | P95 exp | Median time s | P95 time s | Median path inflation | Collision violations | RL attempts | RL success rate | Mean NN forward s | Fallbacks |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Complex | M1 vanilla HA* / single_rs | 0.675 | 0.325 | 737.5 | 6537.9 | 0.5062 | 2.5005 | 0.0000 | 0 | 0 | NA | NA | 15868 |
| Complex | M2 Dang multi-curvature RS / dang_multi_rs | 0.750 | 0.250 | 355.5 | 3977.4 | 0.3686 | 2.5014 | 0.0009 | 0 | 0 | NA | NA | 8572 |
| Complex | M3 HA* + RL-RS PPO funnel / ha_rl_rs_ppo | 0.000 | 0.000 | 0.0 | 0.0 | 7.1856 | 10.7308 | NA | 0 | 0 | NA | NA | 0 |
| Extreme | M1 vanilla HA* / single_rs | 0.725 | 0.275 | 870.0 | 6195.6 | 0.5843 | 2.5005 | 0.0000 | 0 | 0 | NA | NA | 15011 |
| Extreme | M2 Dang multi-curvature RS / dang_multi_rs | 0.675 | 0.325 | 562.5 | 4613.2 | 0.4915 | 2.5012 | 0.0021 | 0 | 0 | NA | NA | 10284 |
| Extreme | M3 HA* + RL-RS PPO funnel / ha_rl_rs_ppo | 0.000 | 0.000 | 0.0 | 0.0 | 20.3417 | 27.3731 | NA | 0 | 0 | NA | NA | 0 |

## M3 vs M1 Paired Comparisons

| Bucket | Paired queries | Median expansions ratio M3/M1 | Median time ratio M3/M1 |
|---|---:|---:|---:|
| Complex | 40 | 0.0000 | 7.2141 |
| Extreme | 40 | 0.0000 | 38.4544 |

## Extreme-Bucket Band

- M3 vs M1 success delta: -72.5 percentage points.
- M3/M1 median time ratio: 34.8117.
- M3/M1 median expansions ratio: 0.0000.
- Raw numeric D2 threshold band: `weak_signal`.
- Reported band verdict: `no_signal`.
- Note: M3 has 80/80 m3_exception:ModuleNotFoundError rows, so crash-as-failure rule makes this no usable planner signal. Raw numeric D2 thresholds alone would label weak_signal because exception rows have 0 expansions.

## M3 Failure Condition

- M3 failure reasons: `{"m3_exception:ModuleNotFoundError": 80}`.
- Operator telemetry for M3 is zero/NA because the checkpoint-backed operator never entered usable planner inference.

## Artifact Index

- M1 records: `0_trials/module2_planner_probe/M1/records.csv`.
- M1 summary: `0_trials/module2_planner_probe/M1/summary_by_method_bucket.csv`.
- M2 records: `0_trials/module2_planner_probe/M2/records.csv`.
- M2 summary: `0_trials/module2_planner_probe/M2/summary_by_method_bucket.csv`.
- M3 records: `0_trials/module2_planner_probe/M3/records.csv`.
- M3 summary: `0_trials/module2_planner_probe/M3/summary_by_method_bucket.csv`.
- Combined summary CSV: `0_trials/module2_planner_probe/probe_summary.csv`.
- Paired comparison CSV: `0_trials/module2_planner_probe/paired_m3_vs_m1.csv`.
