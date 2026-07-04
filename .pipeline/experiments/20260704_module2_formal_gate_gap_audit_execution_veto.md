---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
scope: formal_gate
not_paper_result_material: true
---

# Module2 Formal Gate Gap Audit Execution Veto

## 直观结论

这次变更没有推进训练, 也没有写论文结果材料。它把 `formal_gate_gap_audit` 从单纯的缺口总账, 加固成会直接消费 handoff bundle 和 remote packet safety audit 的执行 veto 总账。

当前真实状态仍然是 `blocked_formal_gate_gaps_open`: F02.6 决策未关闭, source freshness 需要重生成, formal PPO checkpoint 缺失, H01/H02/formal claim 仍阻塞。

## 新增检查

- `formal_gate_handoff`: 直接读取 `0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json`, 检查它是否只读、是否禁止本地训练、是否禁止 formal claim、是否有 safety issue, 以及 `sync/preflight/training/audit` 四个 remote step 是否和 remote packet 一致。
- `remote_packet_safety`: 直接读取 `0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`, 检查 safety audit 是否通过、是否只读、是否与当前 remote packet 的 step allowed/blocker 状态一致。
- `execution_veto_matrix`: 汇总 `status_report`、`handoff_bundle`、`remote_packet`、`remote_packet_safety` 和 `decision_record` 对 `local_training / remote_preflight / remote_training / remote_audit / formal_claim` 的许可判断。

## 当前真实矩阵

- `all_rows_consistent=true`
- `mismatch_rows=[]`
- `local_training=false`
- `remote_preflight=false`
- `remote_training=false`
- `remote_audit=false`
- `formal_claim=false`

这说明当前所有 gate 产物对"不能执行、不能 claim"是一致的。它不是训练许可; 它只是证明现在没有某个子产物偷偷把远端执行打开。

## 产物

- 生成器: `2_experiment/forest_n3p/scripts/build_module2_formal_gate_gap_audit.py`
- 测试: `2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py`
- JSON: `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json`
- Markdown: `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.md`

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_gap_audit`

## 下一步仍缺

- Dr Sun 关闭 F02.6: 批准 obstacle-summary BC warm-start, 或驳回并转 stronger/full patch-CNN protocol。
- F02.6 后重生成 source-fresh gate artifacts。
- approved remote preflight。
- 只在 `gpu3070ti-relay` 远端训练 formal PPO checkpoint。
- pullback checkpoint/eval/audit/hash manifest。
- 重生成 H01/H02 formal acceptance。
- 重生成 claim safety / paper readiness final gate。
