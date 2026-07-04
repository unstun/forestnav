---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
scope: formal_gate
not_paper_result_material: true
---

# Module2 Status Report Execution Veto

## 直观结论

这次变更没有跑训练、没有跑远端 preflight、没有写论文结果材料。它把上一轮 `formal_gate_gap_audit.execution_veto_matrix` 接入 `formal_gate_status_report`, 让 status report 也能直接审计"现在是否允许本地训练、远端 preflight、远端训练、远端 audit、formal claim"。

当前真实状态仍为 `formal_gate_status_blocked`。status report 读到的 veto 矩阵为:

- `present=true`
- `all_rows_consistent=true`
- `remote_training=false`
- `formal_claim=false`
- `input_safety_issue_count=0`

这说明当前各 gate 对"不能执行/不能 claim"的判断一致, 但不代表 formal gate 已关闭。

## 新增检查

- status report 读取 `formal_gate_gap_audit.execution_veto_matrix`。
- 如果矩阵缺失, status report 报 `formal_gate_missing_execution_veto_matrix`。
- 如果矩阵有 mismatch, status report 报 `formal_gate_execution_veto_rows_inconsistent` / `formal_gate_execution_veto_mismatch_rows_open`。
- 如果 formal gate 仍 blocked 但矩阵允许 `local_training / remote_preflight / remote_training / remote_audit / formal_claim`, status report 直接报对应 `blocked_formal_gate_execution_veto_allows_*`。

## 产物

- 生成器: `2_experiment/forest_n3p/scripts/build_module2_formal_gate_status_report.py`
- 测试: `2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py`
- JSON: `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
- Markdown: `0_trials/module2_formal_gate_status_report/formal_gate_status_report.md`

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py`
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py 2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py 2_experiment/forest_n3p/tests/test_module2_claim_safety.py 2_experiment/forest_n3p/tests/test_module2_paper_readiness.py`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_status_report`

## 下一步仍缺

- F02.6 PPO warm-start human decision。
- source-fresh gate regeneration。
- approved remote preflight。
- `gpu3070ti-relay` formal PPO checkpoint。
- remote audit/pullback/hash manifest。
- H01/H02 formal acceptance。
- claim safety / paper readiness final gate。
