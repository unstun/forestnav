---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
scope: formal_gate
not_paper_result_material: true
---

# Module2 Source Freshness Regeneration Target Provenance

## 直观结论

本轮没有记录 F02.6 决策, 没有执行 ssh/rsync/remote preflight/remote training/audit/pullback, 也没有写论文结果材料。

本轮只增强 `source_freshness_audit` 的交接可读性: `ordered_regeneration_targets` 现在不只列 artifact/path/state, 还直接携带每个待再生成目标的 source provenance:

- `source_head`
- `source_commit`
- `current_head`
- `source_head_dirty`
- `source_commit_exists`
- `matches_current_head`

这样 F02.6 关闭后, 人和脚本都能从 regeneration target 行直接判断为什么某个 gate artifact 必须重生成, 不需要再跳到 `artifact_records` 里手工对照。

## 当前读数

刷新后的 `source_freshness_audit` 仍保持 blocked:

- `status=source_freshness_risks_recorded_gate_still_blocked`
- `regeneration_required_before_remote_formal_execution=true`
- `risk_counts.historical_dirty=13`
- `risk_counts.historical_clean=3`

这只说明 formal gate 产物存在 source-head freshness 风险; 它不是训练结果, 也不是实验失败结论。

## 产物

- `2_experiment/forest_n3p/scripts/build_module2_source_freshness_audit.py`
- `2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py`
- `0_trials/module2_source_freshness_audit/source_freshness_audit.json`
- `0_trials/module2_source_freshness_audit/source_freshness_audit.md`

## 验证

```bash
PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py
```

结果: `3 passed in 0.48s`

```bash
python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_source_freshness_audit.py
```

结果: pass

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_source_freshness_audit
```

结果: `status=source_freshness_risks_recorded_gate_still_blocked`

## 边界

- 不代表 F02.6 已批准。
- 不代表可以本地训练。
- 不代表可以远端训练。
- 不代表 H01/H02 formal evaluation 已解锁。
- 不代表可以写 formal performance claim 或论文结果表。
