---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Formal Gate Consumes Closure Checklist

## 直观结论

上一轮已经生成 formal gate closure checklist, 但它还只是独立清单。本轮把它接入 `formal_gate_gap_audit`, 让 checklist open 本身成为 final gate blocker。

现在 final claim gate 不只看 F02.6、source freshness、missing-artifacts inventory、H01/H02 和 claim safety, 还会显式读取:

- `0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json`

如果 checklist 仍是 `formal_gate_closure_blocked`, 或 checklist 自己出现训练/预检/claim 越权, `formal_gate_gap_audit` 会保持 blocked。

## 当前读数

- `formal_gate_gap_audit.status=blocked_formal_gate_gaps_open`
- `formal_gate_gap_audit.closure_checklist.status=formal_gate_closure_blocked`
- `formal_gate_gap_audit.closure_checklist.open_item_count=8`
- `formal_gate_gap_audit.closure_checklist.input_safety_issue_count=0`
- `formal_gate_gap_audit.missing_acceptance_artifacts` 新增/包含 `formal_gate_closure_checklist_open`
- `formal_gate_gap_audit.ordered_next_steps.claim_safety_final_gate.blocked_by` 包含 `formal_gate_closure_checklist_open`
- `formal_gate_closure_checklist.status=formal_gate_closure_blocked`
- `formal_gate_closure_checklist.open_item_count=8`

## 改动

- `build_module2_formal_gate_gap_audit.py`
  - 新增默认输入 `closure_checklist_path`。
  - manifest 新增 `closure_checklist` record。
  - `current_gate_state` 新增 closure checklist status/open 字段。
  - final acceptance gaps 新增 closure checklist read-only / safety / open 检查。
  - Markdown 新增 `Closure Checklist` 区块。
- `test_module2_formal_gate_gap_audit.py`
  - synthetic clean tests 显式传入 complete checklist。
  - 新增 open checklist 阻塞 final gate 测试。
  - 新增 checklist 越权运行/claim 的拒绝测试。

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py` -> `11 passed in 0.44s`
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_missing_artifacts_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py 2_experiment/forest_n3p/tests/test_module2_f02_6_decision_gate_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_closure_checklist.py` -> `45 passed in 2.26s`
- `python -m py_compile ... build_module2_formal_gate_gap_audit.py ...` -> pass
- `git diff --check` -> pass

## 边界

- 本轮没有训练。
- 本轮没有运行 remote preflight。
- 本轮没有执行 sync 或 pullback。
- 本轮没有关闭 F02.6。
- 本轮没有生成 formal PPO checkpoint。
- 本轮没有写结果性论文材料。
- 这个变更只把 closure checklist 纳入 formal gate 总账。
