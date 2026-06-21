---
origin: ai+local+remote
reviewed: false
created_at_utc: 2026-06-21T01:39:16.801543+00:00
task: T14
---

# T14 k=20 collision-guard fullscale analysis

## 直观结论

- k=20 + RS-verified segments + evaluation-level collision rejection 已通过 T14 的核心数值门：Complex 和 Extreme 均满足时间缩减、成功率下降、路径膨胀、碰撞违例四项检查。
- 本次 fullscale 规模完整：300 queries、1800 records、6 official methods、0 method exceptions、0 collision violations。
- 与 pre-guard k=20 fullscale 相比，新的 safety-gated rerun 把 run-level `collision_violation_total` 从 1 降到 0。需要注意：pre-guard 的同一条 `n3p_k1` 碰撞路径在本次重跑中没有以“被 safety gate 拒绝”的形式复现，而是变成 timeout/failure。
- 因此，本包的准确结论是：安全闸已经由单元测试覆盖并在 fullscale runner 中启用；本次 fullscale 结果本身无碰撞违例。不要把它表述为“安全闸实际拒绝了 1 条路径”。
- 仍不能把 T14 标为完成：run status 仍是 `candidate_or_smoke`，原因是 `.pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md` 仍为 `reviewed:false`，需要 Dr Sun 审阅后才能形成正式接受依据。

## 运行级门槛

| run | k | source_head | records | queries | methods | collisions | exceptions | status | formal | wall_s |
|---|---:|---|---:|---:|---:|---:|---:|---|---|---:|
| k5_rs_verified_fullscale | 5 | `98faaba69dfe` | 1800 | 300 | 6 | 0 | 0 | candidate_or_smoke | False | 1136.58 |
| k20_rs_verified_pre_guard | 20 | `d53fac3b6c79` | 1800 | 300 | 6 | 1 | 0 | candidate_or_smoke | False | 1065.62 |
| k20_rs_verified_collisionguard | 20 | `211e373e9be7` | 1800 | 300 | 6 | 0 | 0 | candidate_or_smoke | False | 1081.62 |

## Contract bucket verdicts

| run | bucket | status | median time reduction | success drop pp | median path inflation | F-N3P feasible | F-N3P median time s | F2 rate | F3 rate |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| k5_rs_verified_fullscale | Complex | pass | 0.908113 | -12.000 | 0.000000 | 0.950 | 0.029095 | 0.440 | 0.060 |
| k5_rs_verified_fullscale | Extreme | fail | 0.422213 | -7.000 | 0.000000 | 0.900 | 0.183417 | 0.600 | 0.130 |
| k20_rs_verified_pre_guard | Complex | pass | 0.919811 | -16.000 | 0.000000 | 0.990 | 0.024418 | 0.190 | 0.020 |
| k20_rs_verified_pre_guard | Extreme | pass | 0.911999 | -16.000 | 0.001344 | 0.980 | 0.028353 | 0.210 | 0.020 |
| k20_rs_verified_collisionguard | Complex | pass | 0.919312 | -16.000 | 0.000000 | 0.990 | 0.024729 | 0.190 | 0.020 |
| k20_rs_verified_collisionguard | Extreme | pass | 0.912134 | -15.000 | 0.001344 | 0.970 | 0.028288 | 0.210 | 0.030 |

## Collision safety gate evidence

- Pre-guard collision records: 1 (`pre_guard_collision_records.csv`).
- Guarded-run rejection records: 0 (`guard_rejections.csv`).
- The same pre-guard colliding query/method is compared in `pre_guard_collision_delta.csv`. In the guarded rerun it ended as failure with `collision_violation_count=0`, not as an accepted colliding path.

| query_id | method | pre success/feasible/coll | guarded success/feasible/coll | guarded reason |
|---|---|---|---|---|
| extreme_s01_q0029 | n3p_k1 | True/False/1 | False/False/0 | `f2_failed:prediction:goal_in_collision;goal:timeout;f3_failed:timeout` |

## Latest k=20 collision-guard headline numbers

- Complex: median time reduction 91.93%, success_drop_pp -16.0, median path inflation 0.0000%.
- Extreme: median time reduction 91.21%, success_drop_pp -15.0, median path inflation 0.1344%.
- Run wall time: 1081.62 s on `gpu3070ti-relay`; source head `211e373e9be7f605a72ecbf5b0cae146d9cf06d4`.

## Files

- `.pipeline/experiments/20260620_t14_k20_collisionguard_analysis/gate_summary.csv`
- `.pipeline/experiments/20260620_t14_k20_collisionguard_analysis/bucket_verdict_comparison.csv`
- `.pipeline/experiments/20260620_t14_k20_collisionguard_analysis/method_bucket_summary_collisionguard.csv`
- `.pipeline/experiments/20260620_t14_k20_collisionguard_analysis/pre_guard_collision_records.csv`
- `.pipeline/experiments/20260620_t14_k20_collisionguard_analysis/pre_guard_collision_delta.csv`
- `.pipeline/experiments/20260620_t14_k20_collisionguard_analysis/guard_rejections.csv`
- source fullscale: `.pipeline/experiments/20260620_t14_candidate_6method_fullscale_rs_k20_collisionguard/`
- source logs: `.pipeline/experiments/logs/20260620_t14_candidate_6method_fullscale_rs_k20_collisionguard.*`

## Do not mark T14 complete yet

This package is ready for Dr Sun review, but it is not a formal T14 completion record until the T06 cutpoint supplement is reviewed and the T14 human-confirmation gate is explicitly cleared.
