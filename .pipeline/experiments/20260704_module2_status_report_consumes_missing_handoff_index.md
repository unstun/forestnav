---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
scope: formal_gate
not_paper_result_material: true
---

# Module2 Status Report Consumes Missing-Artifacts Handoff Index

## 直观结论

本轮没有记录 F02.6 决策, 没有执行 ssh/rsync/remote preflight/remote training/audit/pullback, 也没有写论文结果材料。

本轮只让顶层 `formal_gate_status_report` 消费 `formal_gate_missing_artifacts.formal_gate_handoff_index`, 使 status report 不仅知道 missing-artifacts inventory 仍 open, 也直接暴露缺口索引的下一步和权限状态。

当前刷新后的 status report 仍是:

- `status=formal_gate_status_blocked`
- `current_state.missing_artifacts_handoff_index_status=blocked_until_f02_6_decision`
- `current_state.missing_artifacts_handoff_next_action=record_f02_6_decision`
- `current_state.missing_artifacts_handoff_remote_training_allowed_now=false`
- `current_state.missing_artifacts_handoff_formal_result_material_allowed_now=false`
- `permissions_now.remote_training_allowed_now=false`
- `permissions_now.formal_claim_allowed_now=false`

## Safety coverage

新增/确认的 status-report 审计语义:

- missing-artifacts inventory 必须暴露 `formal_gate_handoff_index`。
- 若 inventory 仍 open, handoff index 不能放行 remote training。
- handoff index 永远不能放行 local training。
- handoff index 不能放行 formal result material。
- open inventory 必须暴露 next blocked action。

## 产物

- `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
- `0_trials/module2_formal_gate_status_report/formal_gate_status_report.md`
- `2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py`

## 验证

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py \
  2_experiment/forest_n3p/tests/test_module2_claim_safety.py \
  2_experiment/forest_n3p/tests/test_module2_paper_readiness.py
```

结果: `24 passed in 0.96s`

```bash
python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_formal_gate_status_report.py
```

结果: pass

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_status_report
```

结果: `status=formal_gate_status_blocked`

## 边界

- 不代表 F02.6 已批准。
- 不代表可以本地训练。
- 不代表可以远端训练。
- 不代表 H01/H02 formal evaluation 已解锁。
- 不代表可以写 formal performance claim 或论文结果表。
