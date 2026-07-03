---
date: 2026-07-03
status: smoke_pass_not_gate
origin: codex+experiment
reviewed: false
task: Module2 C02.1
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
source_head: f7bdb0e8a2a26d5b052b710fe299b799d1e85ee6
execution_host: MacBook-Pro.local
---

# Module2 C02.1 Oracle Connector Smoke

## 直观结论

本次只证明 C02 oracle connector 工具链能真实跑通, 还不能下 Gate #2 结论。

有一个关键正信号: Extreme smoke 中 `extreme_s00_q0001:150:45:26`
出现 Oracle A 失败但 Oracle B 成功。直观上, 这说明至少有失败节点不是
"直接禁用 RS 以后 HA* 就能接上" 的平凡情况, 中间候选 + 末端 RS 的
oracle 形态确实能提供额外解释力。

## 方法

- 输入: `0_trials/module2_oracle_shape/rs_failure_nodes_dedup.parquet`
- 输入总行数: 7860
- Oracle A: failed node -> final goal, Hybrid A* analytic operator disabled
- Oracle B:
  - 从 `goal_annulus`, `corridor_offset`, `edt_high_clearance`,
    `voronoi_skeleton` 生成中间姿态。
  - 先过滤出 candidate -> final goal 的 collision-free RS 候选。
  - 再用 analytic-disabled HA* 从 failed node 接 candidate。
  - 最后从实际 segment endpoint 重新做 RS -> final goal, 避免 goal
    tolerance 造成假阳性。

## Complex Smoke

Command:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_oracle_connector_analysis \
  --input 0_trials/module2_oracle_shape/rs_failure_nodes_dedup.parquet \
  --output 0_trials/module2_oracle_shape/oracle_connector_results_smoke5.parquet \
  --max-records 5 \
  --oracle-a-timeout-s 4 \
  --oracle-a-max-nodes 30000 \
  --oracle-b-segment-timeout-s 2 \
  --oracle-b-segment-max-nodes 15000 \
  --oracle-b-candidate-limit 16 \
  --source-head f7bdb0e8a2a26d5b052b710fe299b799d1e85ee6
```

Result:

- Selected rows: 5 / 7860
- Bucket: Complex
- Oracle A success: 5 / 5
- Oracle B success: 5 / 5
- Oracle connectable: 5 / 5
- RS-reachable candidate count: 191-196 per row
- Accepted path collision violations: 0
- `stderr`: empty

Artifacts:

- `0_trials/module2_oracle_shape/oracle_connector_results_smoke5.parquet`
- `0_trials/module2_oracle_shape/oracle_connector_results_smoke5_summary.json`
- `0_trials/module2_oracle_shape/oracle_connector_results_smoke5_stdout.txt`
- `0_trials/module2_oracle_shape/oracle_connector_results_smoke5_stderr.txt`

## Extreme Smoke

Command:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_oracle_connector_analysis \
  --input 0_trials/module2_oracle_shape/rs_failure_nodes_dedup.parquet \
  --output 0_trials/module2_oracle_shape/oracle_connector_results_smoke_extreme3.parquet \
  --row-offset 3368 \
  --max-records 3 \
  --oracle-a-timeout-s 4 \
  --oracle-a-max-nodes 30000 \
  --oracle-b-segment-timeout-s 2 \
  --oracle-b-segment-max-nodes 15000 \
  --oracle-b-candidate-limit 16 \
  --source-head f7bdb0e8a2a26d5b052b710fe299b799d1e85ee6
```

Result:

- Selected rows: 3 / 7860
- Bucket: Extreme
- Oracle A success: 2 / 3
- Oracle B success: 3 / 3
- Oracle connectable: 3 / 3
- RS-reachable candidate count: 34-233 per row
- Accepted path collision violations: 0
- Non-trivial case: `extreme_s00_q0001:150:45:26` has Oracle A failure but
  Oracle B success.
- `stderr`: empty

Artifacts:

- `0_trials/module2_oracle_shape/oracle_connector_results_smoke_extreme3.parquet`
- `0_trials/module2_oracle_shape/oracle_connector_results_smoke_extreme3_summary.json`
- `0_trials/module2_oracle_shape/oracle_connector_results_smoke_extreme3_stdout.txt`
- `0_trials/module2_oracle_shape/oracle_connector_results_smoke_extreme3_stderr.txt`

## Verification

```bash
PYTHONPATH=2_experiment python -m py_compile \
  2_experiment/forest_n3p/scripts/run_oracle_connector_analysis.py

PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_hybrid_astar_analytic_operator.py \
  2_experiment/forest_n3p/tests/test_inference_timing.py \
  2_experiment/forest_n3p/tests/test_evaluation_timing_protocol.py \
  -q
```

Result:

- `py_compile`: pass
- `pytest`: `8 passed in 0.99s`

## 边界

本报告不是 Gate #2 结论。全量 C02.1 仍需覆盖 7860 个去重失败节点,
或者先预注册一个分层抽样方案, 再用同一脚本执行。
