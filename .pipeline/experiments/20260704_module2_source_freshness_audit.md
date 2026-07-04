---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Source Freshness Audit

## 直观结论

本轮新增 source-head/freshness audit，用来检查 formal gate 关键 artifact 是不是由当前 clean HEAD 生成。

当前结果是 `source_freshness_risks_recorded_gate_still_blocked`：8 个核心 artifact 中 6 个是 `historical_dirty`，2 个是 `historical_clean`。这不是实验失败，也不改变 F02.6 pending；它只是说明 F02.6 关闭后、approved remote preflight / H01-H02 formal evaluation / claim safety 放行前，必须重生成这些 gate artifact，避免用旧 dirty 快照支撑 formal 链。

## 风险分布

- `historical_dirty`: 6
- `historical_clean`: 2

## 需要在 formal 执行前重生成的 artifact

- approved remote preflight 前: F02.6 decision record、formal gate gap audit、gpu3070ti readiness refresh、remote formal execution packet。
- H01/H02 formal evaluation 前: H01 evaluation manifest、H02 formal acceptance。
- formal claim gate 前: claim safety、paper readiness。

## 产物

- `2_experiment/forest_n3p/scripts/build_module2_source_freshness_audit.py`
- `2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py`
- `0_trials/module2_source_freshness_audit/source_freshness_audit.json`
- `0_trials/module2_source_freshness_audit/source_freshness_audit.md`

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py` -> `3 passed in 0.35s`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_source_freshness_audit.py` -> pass
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_source_freshness_audit` -> `status=source_freshness_risks_recorded_gate_still_blocked`

## 边界

- 本轮没有训练。
- 本轮没有运行 remote preflight。
- 本轮没有关闭 F02.6。
- 本轮没有放行 formal performance claim。
- Historical/dirty source-head 是 regeneration risk，不是 formal experimental failure。
