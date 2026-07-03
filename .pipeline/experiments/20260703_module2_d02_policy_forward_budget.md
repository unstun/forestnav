---
date: 2026-07-03
status: d02_1_policy_forward_budget_complete
origin: codex+experiment
reviewed: false
task: Module2 D02.1
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_d01_cost_distribution.md
source_head: 04cda992
execution_host: MacBook-Pro.local
---

# Module2 D02.1 Neural Policy Forward Budget

## 直观结论

D02.1 已完成本机 CPU 单线程的神经 policy 纯前向预算。结果不是 Gate #1 通过, 也不是 RL-RS funnel 已经值得实现; 它只回答一个窄问题: 如果只看网络 forward, 三类候选 policy 是否已经超过 Dang multi-RS analytic attempt 的毫秒级预算。

结论是:

- batch=1 时, 三类候选网络的 forward p50 都低于 D01.2 的 Dang multi-RS attempt p50 `0.814 ms`。
- 64-cell 核心 patch 下, CNN forward p50 约 `0.120-0.162 ms`; 128-cell footprint-margin patch 下, CNN forward p50 约 `0.405-0.520 ms`。
- tiny MLP forward p50 约 `0.011 ms`, 几乎不是成本瓶颈。
- CPU batch=32 的 CNN 总 forward time 已明显高于单次 Dang attempt, 所以批量数字只能作为 vectorized throughput 线索, 不能直接当顺序 planner 的 per-attempt 成本。
- 真正 Gate #1 仍缺 `rollout collision checking + terminal RS + planner integration overhead`。D01.2 已显示 collision check 是当前 analytic attempt 最大成本项, 因此前向网络便宜不等于 RL-RS operator 便宜。

## Shape Derivation

输入 shape 不是随意猜测, 而是从 C02/D01 约束推导:

| Shape | Resolution | Source radius | Cells | Extent | Meaning |
|---|---:|---:|---:|---:|---|
| `annulus_auto` | `0.1 m` | C02 goal-annulus max `3.0 m` | 64 | `6.4 m` | 覆盖 `2R=6.0 m` 直径后取 power-of-two。 |
| `footprint_margin_auto` | `0.1 m` | `3.0 m` + two-circle footprint radius `~0.592 m` | 128 | `12.8 m` | 覆盖保守 footprint-margin 直径后取 power-of-two。 |

其他固定输入:

- Patch channels: 2 (`occupancy`, `EDT/distance-field` proxy)
- Scalar dim: 8 (`dx`, `dy`, heading/bearing terms, clearance/budget/terminal-distance style terms)
- Action dim: 1 (v1 forward-only steering/curvature command)
- MLP vector bins: match patch cells (`64` or `128`)

Boundary:

- 这些 shape 是 D02.1 forward budget proxy, 不是最终 observation design 冻结。
- E01 环境实现仍必须用 planner state、map、footprint、checker 做真实 patch/EDT 抽取和图像测试。

## Command

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_policy_forward_budget \
  --output-dir 0_trials/module2_cost_accounting/d02_policy_forward_budget \
  --models tiny_mlp,small_cnn,compact_cnn_mlp \
  --batch-sizes 1,8,32 \
  --patch-cells auto,margin_auto \
  --warmup-iterations 150 \
  --timed-iterations 1000 \
  --threads 1 \
  --allow-duplicate-openmp \
  --source-head 04cda992
```

Local environment note:

- Plain `import torch` on this Mac hit OpenMP duplicate runtime abort.
- This D02.1 run used `--allow-duplicate-openmp`, which sets `KMP_DUPLICATE_LIB_OK=TRUE`.
- Treat these numbers as local budget evidence, not final cross-machine timing.

## Artifacts

Output directory:

- `0_trials/module2_cost_accounting/d02_policy_forward_budget/`

Files:

- `summary.json`
- `forward_budget_records.parquet`
- `forward_budget_samples.parquet`

Run metadata:

| Field | Value |
|---|---:|
| Aggregate records | 18 |
| Sample records | 18000 |
| Torch version | `2.11.0` |
| Torch threads | 1 |
| Devices benchmarked | `cpu` |
| CUDA available | false |
| MPS available | true, not benchmarked in D02.1 |

## Batch=1 Results

D01.2 reference:

| Metric | Value |
|---|---:|
| Dang multi-RS attempt p50 | `0.814 ms` |
| Dang multi-RS attempt p95 | `2.025 ms` |
| Dang multi-RS attempt p99 | `2.829 ms` |

Policy forward, batch=1:

| Model | Shape | Params | p50 ms | p95 ms | p50 / D01 p50 |
|---|---|---:|---:|---:|---:|
| `tiny_mlp` | `annulus_auto` | 8897 | 0.011 | 0.013 | 0.014 |
| `compact_cnn_mlp` | `annulus_auto` | 15049 | 0.120 | 0.151 | 0.148 |
| `small_cnn` | `annulus_auto` | 164497 | 0.162 | 0.189 | 0.199 |
| `tiny_mlp` | `footprint_margin_auto` | 12993 | 0.011 | 0.015 | 0.014 |
| `compact_cnn_mlp` | `footprint_margin_auto` | 15049 | 0.405 | 0.537 | 0.497 |
| `small_cnn` | `footprint_margin_auto` | 164497 | 0.520 | 0.642 | 0.638 |

Interpretation:

- Forward-only latency is plausible under the D01 per-attempt budget.
- The 128-cell CNN budget is still below D01 p50 for batch=1, but leaves less room for rollout collision checks.
- `compact_cnn_mlp` is the more conservative CNN candidate for D02.2/E01 unless later quality evidence requires `small_cnn`.

## Batch Throughput Results

| Model | Shape | Batch | p50 ms | p95 ms | Per-item p50 ms |
|---|---|---:|---:|---:|---:|
| `tiny_mlp` | `annulus_auto` | 8 | 0.013 | 0.018 | 0.002 |
| `tiny_mlp` | `annulus_auto` | 32 | 0.016 | 0.020 | 0.000 |
| `compact_cnn_mlp` | `annulus_auto` | 8 | 0.725 | 0.851 | 0.091 |
| `compact_cnn_mlp` | `annulus_auto` | 32 | 4.243 | 4.428 | 0.133 |
| `small_cnn` | `annulus_auto` | 8 | 1.048 | 1.220 | 0.131 |
| `small_cnn` | `annulus_auto` | 32 | 7.466 | 7.695 | 0.233 |
| `compact_cnn_mlp` | `footprint_margin_auto` | 8 | 3.133 | 3.379 | 0.392 |
| `compact_cnn_mlp` | `footprint_margin_auto` | 32 | 16.533 | 17.115 | 0.517 |
| `small_cnn` | `footprint_margin_auto` | 8 | 4.715 | 5.060 | 0.589 |
| `small_cnn` | `footprint_margin_auto` | 32 | 28.901 | 29.352 | 0.903 |

Boundary:

- Batch throughput may matter for offline evaluation or vectorized rollout.
- Sequential Hybrid A* analytic expansion should use batch=1 wall-clock, not per-item batch amortization, unless planner integration actually batches multiple attempts.

## Verification

Commands:

```bash
PYTHONPATH=2_experiment python -m py_compile \
  2_experiment/forest_n3p/scripts/run_policy_forward_budget.py

PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_policy_forward_budget.py \
  -q

PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_policy_forward_budget \
  --output-dir 0_trials/module2_cost_accounting/d02_policy_forward_budget \
  --models tiny_mlp,small_cnn,compact_cnn_mlp \
  --batch-sizes 1,8,32 \
  --patch-cells auto,margin_auto \
  --warmup-iterations 150 \
  --timed-iterations 1000 \
  --threads 1 \
  --allow-duplicate-openmp \
  --source-head 04cda992
```

Results:

- `py_compile`: pass
- `pytest`: `2 passed in 0.30s`
- benchmark: `status=complete`, aggregate rows `18`, sample rows `18000`

## Allowed Conclusions

- On this Mac CPU single-thread run, pure policy forward is not the first obvious blocker for D02.
- CNN observation budgets derived from C02 geometry remain plausible at batch=1.
- D02.2 can focus on full CPU/GPU device comparison and rollout collision accounting instead of rejecting the idea at network-forward stage.

## Disallowed Conclusions

- Do not claim Gate #1 is passed.
- Do not claim RL-RS is faster than Dang multi-RS; rollout collision and terminal RS are not measured here.
- Do not claim the final policy architecture is selected.
- Do not use the OpenMP-workaround Mac timing as final paper timing without clean CPU/GPU reruns.

## Next Step

Proceed to D02.2:

1. repeat forward benchmark on clean CPU and CUDA/MPS if used;
2. add rollout collision-check microbenchmark using the same `GridFootprintChecker` / EDT semantics as planner;
3. estimate `NN forward + rollout collision + terminal RS` before D02.3 Gate #1.
