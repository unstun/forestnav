---
date: 2026-07-03
status: d01_2_cost_distribution_complete
origin: codex+experiment
reviewed: false
task: Module2 D01.2
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_d01_analytic_cost_telemetry.md
source_head: c152ed20cdced9034bca6932d65d0e4d1299f73e
execution_host: MacBook-Pro.local
---

# Module2 D01.2 Analytic Attempt Cost Distribution

## 直观结论

D01.2 已在 C01/C02 同一 Complex/Extreme query 配置上统计 Dang multi-RS analytic expansion 成本分布。结果不是“RL 已经值得做”，而是给 D02 神经前向预算划出了一个硬上限:

- 20 个 queries 共产生 8622 次 analytic attempts 和 94842 个 radius candidates。
- 每次 analytic attempt 固定扫描 11 个半径。
- attempt total time: p50 `0.814 ms`, p95 `2.025 ms`, p99 `2.829 ms`, max `14.479 ms`。
- 当前 run 的 analytic expansion 总时间是 `8.216 s`, 总 plan time 是 `24.751 s`, 占比约 `33.2%`。
- 成本主要来自 collision check, 其次是 RS solve; sampling 通常更小, cost eval 只在有成功候选时出现。

这说明 D02 的 NN forward + rollout collision budget 不能拍脑袋。若 RL-RS funnel 不能显著减少后续 search expansions 或 timeout, 单次 policy rollout 很容易吃掉 Dang multi-RS 的毫秒级 attempt budget。

## Scope

This run uses the same query configuration as C01/C02:

- Buckets: `Complex,Extreme`
- Queries per bucket: 10
- Seed count: 1
- Queries per map: 5
- Density profiles: `validation_t06`
- Analytic operator: `dang_multi_rs`
- Timeout: `2.5 s`
- Max nodes: `15000`

Important boundary:

- This is the same query configuration, not a bit-identical replay of old C01 raw rows.
- Attempt counts are wall-clock-timeout sensitive. The authoritative count for this D01.2 run is the artifact generated at `source_head=c152ed20cdced9034bca6932d65d0e4d1299f73e`.

## Command

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

Stdout/stderr:

- `0_trials/module2_cost_accounting/d01_analytic_cost_distribution_stdout.txt`
- `0_trials/module2_cost_accounting/d01_analytic_cost_distribution_stderr.txt`

`stderr` is empty.

## Artifacts

Output directory:

- `0_trials/module2_cost_accounting/d01_analytic_cost_distribution/`

Files:

- `summary.json`
- `query_costs.parquet`
- `attempt_costs.parquet`
- `candidate_costs.parquet`

Table rows:

| Table | Rows | Meaning |
|---|---:|---|
| `query_costs.parquet` | 20 | One row per C01/C02 query. |
| `attempt_costs.parquet` | 8622 | One row per analytic expansion attempt. |
| `candidate_costs.parquet` | 94842 | One row per radius candidate inside an attempt. |

## Counts

| Metric | Count |
|---|---:|
| Queries | 20 |
| Plan successes | 15 |
| Plan failures | 5 |
| Analytic attempts | 8622 |
| Attempts with at least one successful radius candidate | 15 |
| Attempts with all radius candidates failed | 8607 |
| Radius candidates | 94842 |
| Successful radius candidates | 60 |
| Failed radius candidates | 94782 |

Failure reasons:

| Level | Reason | Count |
|---|---|---:|
| Query | `None` | 15 |
| Query | `timeout` | 5 |
| Candidate | `collision` | 94782 |
| Candidate | `None` | 60 |

By bucket:

| Bucket | Queries | Successes | Attempts | Analytic successes | Plan time sum s | Analytic time sum s |
|---|---:|---:|---:|---:|---:|---:|
| Complex | 10 | 7 | 3516 | 7 | 11.535665 | 3.824022 |
| Extreme | 10 | 8 | 5106 | 8 | 13.215591 | 4.391933 |

## Attempt-Level Timing

Overall:

| Field | Mean s | P50 s | P90 s | P95 s | P99 s | Max s |
|---|---:|---:|---:|---:|---:|---:|
| `analytic_total_time_s` | 0.000953 | 0.000814 | 0.001615 | 0.002025 | 0.002829 | 0.014479 |
| `analytic_rs_solve_time_s` | 0.000255 | 0.000249 | 0.000303 | 0.000318 | 0.000383 | 0.001261 |
| `analytic_sample_time_s` | 0.000150 | 0.000111 | 0.000318 | 0.000355 | 0.000441 | 0.013450 |
| `analytic_collision_check_time_s` | 0.000500 | 0.000360 | 0.001049 | 0.001444 | 0.002198 | 0.005361 |
| `analytic_cost_eval_time_s` | 0.000000390 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.002268 |

Candidate counts:

| Field | Mean | P50 | P95 | Max |
|---|---:|---:|---:|---:|
| `analytic_candidate_radius_count` | 11.0 | 11.0 | 11.0 | 11.0 |
| `analytic_sample_count` | 659.287 | 450.0 | 1726.95 | 3168.0 |
| `analytic_collision_check_count` | 18.440 | 22.0 | 22.0 | 33.0 |

By bucket total time:

| Bucket | Attempts | Mean s | P50 s | P90 s | P95 s | P99 s | Max s |
|---|---:|---:|---:|---:|---:|---:|---:|
| Complex | 3516 | 0.001088 | 0.000931 | 0.001891 | 0.002185 | 0.002828 | 0.006923 |
| Extreme | 5106 | 0.000860 | 0.000756 | 0.001291 | 0.001655 | 0.002832 | 0.014479 |

## Time Budget Totals

| Field | Value |
|---|---:|
| Total plan time s | 24.751256 |
| Total analytic expansion time s | 8.215955 |
| Analytic / plan time ratio | 0.331941 |

Interpretation:

- Dang multi-RS analytic expansion is not the whole planner cost, but it is a large enough slice to matter.
- Any RL-RS operator must be judged against both per-attempt latency and downstream search reduction.
- D02 should benchmark policy forward plus rollout collision at batch=1 and at batched analytic-attempt scales.

## Verification

Commands:

```bash
PYTHONPATH=2_experiment python -m py_compile \
  2_experiment/forest_n3p/scripts/run_analytic_cost_distribution.py \
  2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py

PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_hybrid_astar_analytic_operator.py \
  2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py \
  -q
```

Result:

- `py_compile`: pass
- `pytest`: `6 passed in 0.30s`

Artifact verification:

```text
status complete
source_head c152ed20cdced9034bca6932d65d0e4d1299f73e
rows query/attempt/candidate = 20 / 8622 / 94842
stderr_size 0
```

## Boundary

Allowed conclusions:

- D01.2 now gives a real C01/C02 query-set analytic expansion cost distribution.
- The current D02 NN budget should target sub-millisecond to low-millisecond latency per analytic call unless it demonstrably reduces search expansion cost.
- Collision checking is the largest measured analytic-attempt component in this run.

Disallowed conclusions:

- Do not claim Gate #1 is passed or failed yet; D02 NN forward/rollout cost is missing.
- Do not claim PPO or RL is necessary.
- Do not infer a stable universal attempt count from this timeout-sensitive local run.
- Do not use these numbers as final paper performance results; they are a local budget audit.

## Next Step

Proceed to D02.1:

1. derive candidate observation/input shapes from C02/D01 evidence, not arbitrary network guesses;
2. benchmark tiny MLP, small CNN, and compact CNN+MLP forward time;
3. include rollout collision-check cost estimates, because collision checking dominates analytic-attempt cost here.
