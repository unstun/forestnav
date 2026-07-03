---
date: 2026-07-03
status: full_run_complete_not_final_gate
origin: codex+experiment
reviewed: false
task: Module2 C02.1
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
source_head: 1f4f96f82bca68f06cc6e9a08adb9ea9aaf993a5
execution_host: MacBook-Pro.local
---

# Module2 C02.1 Oracle Connector Full Run

## 直观结论

全量 C02.1 已覆盖 7860 个去重 RS failure nodes。最重要的结论不是
"RL 已经可以替代 RS", 而是问题形态被缩窄了:

1. 1571 个 unresolved 全部是 `start_in_collision` 或 `goal_in_collision`,
   这类样本不应该被当成 RL connector 失败。
2. 去掉 invalid start/goal 后, 剩下 6289 个 non-invalid failure nodes
   在 default oracle budget 下全部 connectable。
3. 真正体现 "中间 connector 比直接 HA* 更有价值" 的 B-only 样本是 63 个,
   全部来自 Oracle A timeout, 其中 58 个选中 `goal_annulus`, 5 个选中
   `voronoi_skeleton`。

直观上, C02.1 反证了 "多数 RS failure 是 oracle 无解死区"。但它也提醒我们:
不能把 7860 个 RS failure 都包装成 RL 的训练目标。下一步要先做 C02.2
可视化形态标注, 再做 C02.3 Gate #2 判定和 D01/D02 成本账。

## 输入与命令

Input:

- `0_trials/module2_oracle_shape/rs_failure_nodes_dedup.parquet`
- Rows: 7860

Command:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_oracle_connector_chunks \
  --input 0_trials/module2_oracle_shape/rs_failure_nodes_dedup.parquet \
  --output-dir 0_trials/module2_oracle_shape/oracle_connector_full \
  --merged-output 0_trials/module2_oracle_shape/oracle_connector_results.parquet \
  --chunk-size 100 \
  --source-head 1f4f96f82bca68f06cc6e9a08adb9ea9aaf993a5
```

Default budgets:

- Oracle A: `8 s / 50000 nodes`
- Oracle B segment: `4 s / 25000 nodes`
- Oracle B candidate limit: `32`

Execution note:

- The run used resumable chunks. Disjoint far-ahead chunks were precomputed
  while the main runner filled the contiguous gap.
- One auxiliary `chunk_006000_006099` attempt was stopped before parquet/summary
  emission to avoid a race with the main runner. The final accepted
  `chunk_006000_006099` was produced by the main runner.

## Artifacts

- `0_trials/module2_oracle_shape/oracle_connector_full/summary.json`
- `0_trials/module2_oracle_shape/oracle_connector_full/chunks/`
- `0_trials/module2_oracle_shape/oracle_connector_results.parquet`
- `0_trials/module2_oracle_shape/oracle_connector_full_stdout.txt`
- `0_trials/module2_oracle_shape/oracle_connector_full_stderr.txt`
- `0_trials/module2_oracle_shape/oracle_connector_full_analysis.json`
- `0_trials/module2_oracle_shape/oracle_connector_b_only_cases.csv`
- `0_trials/module2_oracle_shape/oracle_connector_a_only_cases.csv`
- `0_trials/module2_oracle_shape/oracle_connector_invalid_query_counts.csv`

## Integrity

Mechanical checks:

- Root summary status: `complete`
- Input rows: 7860
- Selected rows: 7860
- Chunk count: 79
- Chunk four-file sets missing: 0
- Nonzero chunk summaries: 0
- Merged parquet rows: 7860
- Merged parquet columns: 58
- Merged `source_head`: all rows use
  `1f4f96f82bca68f06cc6e9a08adb9ea9aaf993a5`

Verification command used:

```bash
PYTHONPATH=2_experiment python - <<'PY'
from pathlib import Path
import json
import pandas as pd

root = Path("0_trials/module2_oracle_shape/oracle_connector_full")
summary = json.loads((root / "summary.json").read_text())
df = pd.read_parquet("0_trials/module2_oracle_shape/oracle_connector_results.parquet")
print(summary["status"], summary["chunk_count"], len(df))
print(df["source_head"].value_counts(dropna=False).to_dict())
PY
```

## Full Counts

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

Relation by bucket:

| Bucket | A-only | B-only | Both success | Unresolved |
|---|---:|---:|---:|---:|
| Complex | 1 | 1 | 2595 | 771 |
| Extreme | 1 | 62 | 3629 | 800 |

## Failure Triage

Oracle A failure reasons:

| Reason | Count |
|---|---:|
| `goal_in_collision` | 1182 |
| `start_in_collision` | 389 |
| `timeout` | 63 |

Oracle B failure prefixes:

| Prefix | Count |
|---|---:|
| `no_rs_reachable_candidates` | 1409 |
| `no_candidate_connected` | 164 |

Invalid start/goal:

- Invalid by Oracle A reason: 1571
- `goal_in_collision`: 1182
- `start_in_collision`: 389
- Non-invalid rows: 6289
- Non-invalid connectable: 6289
- Non-invalid unresolved: 0

Top invalid query groups:

| Bucket | Query | Reason | Count |
|---|---|---|---:|
| Complex | `complex_s00_q0007` | `goal_in_collision` | 706 |
| Extreme | `extreme_s00_q0006` | `goal_in_collision` | 434 |
| Extreme | `extreme_s00_q0006` | `start_in_collision` | 222 |
| Extreme | `extreme_s00_q0002` | `start_in_collision` | 93 |
| Complex | `complex_s00_q0002` | `start_in_collision` | 62 |

## B-only Cases

B-only means Oracle A failed, but Oracle B connected through an intermediate
candidate and terminal RS.

- Count: 63
- Oracle A reason: all `timeout`
- Bucket split: Complex 1, Extreme 62
- Selected source: `goal_annulus=58`, `voronoi_skeleton=5`

Top B-only query groups:

| Bucket | Query | Count |
|---|---|---:|
| Extreme | `extreme_s00_q0006` | 52 |
| Extreme | `extreme_s00_q0004` | 6 |
| Extreme | `extreme_s00_q0003` | 3 |
| Complex | `complex_s00_q0003` | 1 |
| Extreme | `extreme_s00_q0008` | 1 |

Representative B-only row:

| Bucket | Query | Expansion | A reason | B source | B path length | B min clearance |
|---|---|---:|---|---|---:|---:|
| Complex | `complex_s00_q0003` | 4640 | `timeout` | `goal_annulus` | 16.641391 | 0.088110 |
| Extreme | `extreme_s00_q0006` | 0 | `timeout` | `goal_annulus` | 17.914892 | 0.082413 |

## A-only Cases

A-only means direct analytic-disabled HA* succeeded, but the current Oracle B
acceptance rule rejected all intermediate candidates.

- Count: 2
- Both are still oracle connectable through Oracle A.
- B failure details are mostly `combined_collision:1`, meaning the B pipeline is
  conservative at the combined path acceptance stage.

## Timing And Candidate Diagnostics

Candidate counts:

| Field | Median | P75 | Max | Mean |
|---|---:|---:|---:|---:|
| `candidate_raw_count` | 393.0 | 395.0 | 399.0 | 381.424 |
| `candidate_rs_reachable_count` | 123.5 | 193.0 | 359.0 | 126.777 |
| `oracle_b_attempted_candidate_count` | 1.0 | 1.0 | 32.0 | 1.542 |

Runtime:

| Field | Mean | P50 | P90 | P99 | Max |
|---|---:|---:|---:|---:|---:|
| `oracle_a_time_s` | 0.885 | 0.307 | 2.468 | 6.758 | 8.016 |
| `oracle_b_segment_time_s` | 0.740 | 0.434 | 1.822 | 3.468 | 3.988 |

## Interpretation Boundary

This full run is C02.1 evidence, not a final Gate #2 decision.

Allowed conclusions:

- The full C02.1 oracle pipeline is now run-complete on all 7860 deduplicated
  RS failure nodes.
- Invalid start/goal states dominate unresolved rows and must be cleaned or
  separated before RL training claims.
- There is a real but narrow B-only signal: 63 timeout rows become connectable
  through intermediate candidates.
- The dataset does not currently support a broad claim that most RS failures
  require a learned connector.

Disallowed conclusions:

- Do not claim RL is implemented.
- Do not claim PPO is necessary before D01/D02 cost accounting and later RL
  experiments.
- Do not use invalid start/goal rows as negative RL samples.
- Do not call Gate #2 complete until C02.2 visual/shape labels are written.

## Follow-up

C02.2 visual seed is now recorded separately:

- `.pipeline/experiments/20260703_module2_c02_shape_labels.md`
- `0_trials/module2_oracle_shape/c02_shape_labels/`

C02.2 rendered:

- invalid start/goal representatives,
- reproducible `goal_annulus` B-only timeout representatives,
- A-only conservative Oracle B rejection representatives.

It also found a provenance issue: the 5 full-run `voronoi_skeleton` B-only
rows currently do not replay under the render script's candidate regeneration,
so they remain excluded from visual/paper evidence until audited.

Next step is C02.3:

1. Write Gate #2 with a narrower claim: whether the remaining
   timeout/B-only shape justifies RL-RS funnel work, and what part of the
   problem must be solved instead by data cleaning or cost accounting.
2. Do not use the `voronoi_skeleton` B-only rows as positive examples until
   the replay mismatch is resolved.
