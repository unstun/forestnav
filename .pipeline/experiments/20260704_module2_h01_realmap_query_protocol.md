---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_h01_evaluation_manifest.md
  - .pipeline/experiments/20260620_t07_realmap_inventory.md
---

# Module2 H01.1 RealMap Query Protocol 记录

## 直观结论

本轮解除 H01.1 的 `realmap_query_generation_not_frozen` blocker。现在真实 SLAM map 不再只是 inventory, 而是有独立、可 hash、可复现的 query protocol artifact。

产物冻结了两张真实地图各 5 个 query, 总计 10 个 query。每张地图第 0 个 query 是 `manifest.json` 中的 canonical start/goal, 其余 query 按固定 seed 和距离桶采样。endpoint audit 显示 start/goal collision 均为 0。

这不是 realmap 评测结果, 也不是方法性能 claim。它只是后续 realmap 方法评测必须引用的 query source-of-truth。

## 实现锚点

- 新增脚本: `2_experiment/forest_n3p/scripts/build_module2_realmap_query_protocol.py`。
- `Module2RealmapQueryProtocolConfig` 固定 output paths、realmap manifest、seed、queries_per_map、distance bins、theta_bins: `2_experiment/forest_n3p/scripts/build_module2_realmap_query_protocol.py:20-32`。
- 复用 `generalization.py` 中 `_append_realmap_queries()` 的真实地图采样语义, 避免另写一套不一致 protocol: `2_experiment/forest_n3p/scripts/build_module2_realmap_query_protocol.py:71-90`。
- 每行 query 记录 query_id/map_id/seed/start/goal/distance_bin/map hash, 并用 `GridFootprintChecker` 审计 start/goal collision: `2_experiment/forest_n3p/scripts/build_module2_realmap_query_protocol.py:152-184`。
- manifest 写出 `realmap_manifest_sha256`, `query_rows_sha256`, `queries_csv_sha256`, endpoint audit 和 claim boundaries: `2_experiment/forest_n3p/scripts/build_module2_realmap_query_protocol.py:92-119`, `2_experiment/forest_n3p/scripts/build_module2_realmap_query_protocol.py:237-244`。
- H01 manifest 新增 `--realmap-query-protocol-path`, 并只有在 protocol `status=frozen` 且 endpoint audit pass 时移除 realmap blocker: `2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py:19-23`, `2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py:65-72`, `2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py:209-223`, `2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py:285-306`。

## TDD 记录

RED 1:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_module2_realmap_query_protocol.py -q
```

失败点:

```text
ModuleNotFoundError: No module named 'forest_n3p.scripts.build_module2_realmap_query_protocol'
```

GREEN 1:

```text
2 passed in 0.42s
```

RED 2:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py -q
```

失败点:

```text
Module2EvaluationManifestConfig.__init__() got an unexpected keyword argument 'realmap_query_protocol_path'
unrecognized arguments: --realmap-query-protocol-path ...
```

GREEN 2:

```text
3 passed in 0.24s
```

## 产物

生成命令:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_realmap_query_protocol \
  --output-dir 0_trials/module2_realmap_query_protocol \
  --manifest-out 0_trials/module2_realmap_query_protocol/module2_realmap_query_protocol.json \
  --queries-out 0_trials/module2_realmap_query_protocol/module2_realmap_queries.csv \
  --markdown-out 0_trials/module2_realmap_query_protocol/module2_realmap_query_protocol.md \
  --queries-per-map 5 \
  --distance-bins 4:8,8:12,12:16,16:20,20: \
  --seed 20260623
```

输出:

```text
status=frozen
query_count=10
query_count_by_map={"dqn_realmap_a": 5, "willow_garage_0p10": 5}
endpoint_audit={"start_collision_count": 0, "goal_collision_count": 0, "pass": true}
queries_csv_sha256=36f80e9e69cd41d3658d4d9858b04aee874c93933c85188254c7731565764b59
query_rows_sha256=47a85142114fb03d4ac29ca479f44821e1896f0e23c03705a992387a1b9aaa41
```

H01 manifest 已重新生成并引用该 protocol:

```text
status=blocked_pending_decisions
realmap_query_protocol.frozen=true
realmap_query_protocol.query_count=10
blockers=["f02_6_warm_start_decision_pending", "missing_required_method_implementation"]
```

## 当前边界

- 可以 claim: realmap query generation protocol 已冻结。
- 可以 claim: H01 manifest 已不再因为 realmap query protocol 阻塞。
- 可以 claim: 后续 realmap 评测必须引用 `module2_realmap_queries.csv` 及其 SHA-256 才可比较。
- 不能 claim: realmap 上任何方法已经跑过正式评测。
- 不能 claim: H01.1 formal-ready, 因为 F02.6 和 pure PPO analytic operator 仍未关闭。
