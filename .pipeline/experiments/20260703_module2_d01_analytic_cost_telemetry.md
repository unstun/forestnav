---
date: 2026-07-03
status: d01_1_telemetry_smoke_complete
origin: codex+experiment
reviewed: false
task: Module2 D01.1
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_gate: .pipeline/experiments/20260703_module2_gate2_oracle_shape.md
source_head: 1ff1fa4626d65c8cf67542d7030305f54be1b00d
execution_host: MacBook-Pro.local
---

# Module2 D01.1 Dang Multi-RS Analytic Cost Telemetry

## 直观结论

D01.1 已把 Dang multi-RS analytic expansion 的成本账拆出来了。现在 planner stats 能区分:

1. RS 求解时间: `reeds_shepp_shortest_path`;
2. 轨迹采样时间: `sample_constant_steer_motion`;
3. 碰撞检测时间: `collision_checker.collides_path`;
4. Dang Eq. 3-4 cost 评估时间;
5. 候选半径数量、成功/失败候选数、采样点数和碰撞检查次数。

这一步只是打开成本账接口, 不是成本结论。D01.2 还需要在 C01/C02 同一 query set 上跑分布统计, 才能判断 RS analytic failure 的真实成本是否给 D02 神经前向预算留下空间。

## Code Changes

Planner:

- `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py`
- Adds internal dataclasses:
  - `AnalyticCandidateTelemetry`
  - `AnalyticRadiusResult`
  - `AnalyticExpansionTelemetry`
- `_try_rs_with_radius()` now returns `(AnalyticRadiusResult | None, AnalyticCandidateTelemetry)`, so failed candidates also produce cost telemetry.
- `_try_analytic_expansion()` aggregates per-radius candidate telemetry into per-attempt telemetry.
- `_stats()` exposes summary fields and `analytic_telemetry_records`.
- `_analytic_failure_record()` attaches the same cost summary to failed analytic expansion records.

Evaluation adapter:

- `2_experiment/forest_n3p/evaluation.py`
- `planner_run_from_path_stats()` forwards only summary telemetry keys into regular evaluation metadata.
- It intentionally does not forward `analytic_telemetry_records`, because that per-attempt list can become large.

Tests:

- `2_experiment/forest_n3p/tests/test_hybrid_astar_analytic_operator.py`
- `2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py`

## Telemetry Schema

Summary fields:

| Field | Unit | Meaning |
|---|---|---|
| `analytic_candidate_radius_count` | count | Number of evaluated radius candidates across analytic attempts. |
| `analytic_candidate_success_count` | count | Radius candidates accepted after RS solve, sampling, goal tolerance, and collision checks. |
| `analytic_candidate_failure_count` | count | Radius candidates rejected by the same checks. |
| `analytic_rs_solve_time_s` | seconds | Time in `reeds_shepp_shortest_path`. |
| `analytic_sample_time_s` | seconds | Time in `sample_constant_steer_motion`. |
| `analytic_collision_check_time_s` | seconds | Time in `collision_checker.collides_path`. |
| `analytic_cost_eval_time_s` | seconds | Time in Dang 2022 Eq. 3-4 cost evaluation. |
| `analytic_total_time_s` | seconds | Wall-clock time for analytic expansion attempts. |
| `analytic_sample_count` | count | Sampled poses generated for candidate checks. |
| `analytic_collision_check_count` | count | Path collision-check calls. |

Per-attempt field:

- `analytic_telemetry_records`: list of per analytic-expansion attempts.
- Each attempt includes the summary fields above plus `candidate_records`.
- Each candidate record includes `radius_m`, `success`, `failure_reason`,
  `rs_solve_time_s`, `sample_time_s`, `collision_check_time_s`,
  `sample_count`, and `collision_check_count`.

## Smoke Artifact

Output:

- `0_trials/module2_cost_accounting/d01_analytic_cost_telemetry_smoke/summary.json`

Source head:

- `1ff1fa4626d65c8cf67542d7030305f54be1b00d`

Smoke setup:

- Empty `80 x 80` grid
- Resolution: `0.1 m`
- Start: `(1.0, 1.0, 0.0)`
- Goal: `(1.8, 1.0, 0.0)`
- Operators: `disabled`, `single_rs`, `dang_multi_rs`

Dang multi-RS observed stats:

| Field | Value |
|---|---:|
| `analytic_attempts` | 1 |
| `analytic_successes` | 1 |
| `analytic_candidate_radius_count` | 11 |
| `analytic_candidate_success_count` | 11 |
| `analytic_candidate_failure_count` | 0 |
| `analytic_rs_solve_time_s` | 0.0003742900 |
| `analytic_sample_time_s` | 0.0000428740 |
| `analytic_collision_check_time_s` | 0.0002604170 |
| `analytic_cost_eval_time_s` | 0.0001455000 |
| `analytic_total_time_s` | 0.0009104580 |
| `analytic_sample_count` | 101 |
| `analytic_collision_check_count` | 11 |
| `telemetry_record_count` | 1 |

Interpretation:

- The smoke proves telemetry is populated and internally consistent.
- The numbers are not performance claims. The map is trivial and has no obstacle pressure.
- D01.2 must run on the C01/C02 Complex/Extreme query set to estimate real RS failure costs.

## Verification

Commands:

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

Observed:

- `py_compile`: pass
- `pytest`: `9 passed in 1.00s`

## Boundary

Allowed conclusions:

- The planner can now report candidate-level and attempt-level analytic expansion cost telemetry.
- Evaluation metadata can carry summary telemetry for regular records.
- D01.2 can be implemented without instrumenting planner internals again.

Disallowed conclusions:

- Do not claim Dang multi-RS is cheap or expensive from the smoke alone.
- Do not compare against a neural policy yet; D02 has not run.
- Do not start RL-RS implementation merely because telemetry exists.

## Next Step

D01.2 should run the same C01/C02 Complex/Extreme query configuration and write a distribution over:

- failed and successful analytic attempts,
- radius candidates per attempt,
- RS solve time,
- sampling time,
- collision check time,
- cost evaluation time,
- sample and collision-check counts.

Only after that should D02 choose actual policy input shapes and benchmark NN forward cost.
