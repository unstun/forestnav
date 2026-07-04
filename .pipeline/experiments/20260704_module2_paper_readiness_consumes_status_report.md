---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Paper Readiness Consumes Status Report

## 直观结论

本轮把 `formal_gate_status_report` 直接接入 `paper_readiness`。

之前 paper readiness 已经能通过 `claim_safety.formal_performance_blockers` 间接继承 `formal_gate_status_report_blocked`; 但它自己的 inputs / evidence list 还没有 status report。现在 readiness ledger 会直接读取:

- `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`

并把 status report 的状态写入:

- `paper_readiness.inputs.formal_gate_status_report`
- `paper_readiness.input_status.status_report_status`
- `paper_readiness.input_status.status_report_formal_claim_allowed_now`
- `paper_readiness.section_readiness[formal_results].evidence`
- `paper_readiness.global_blockers`

当前新增/确认的 blocker:

- `formal_gate_status_report_blocked`

## 当前读数

- `paper_readiness.status=partial_methods_ready_results_blocked`
- `paper_readiness.formal_results_ready=false`
- `paper_readiness.input_status.status_report_status=formal_gate_status_blocked`
- `paper_readiness.input_status.status_report_formal_claim_allowed_now=false`
- `paper_readiness.input_status.status_report_input_safety_issue_count=0`
- `paper_readiness.global_blockers` 包含 `formal_gate_status_report_blocked`
- `paper_readiness.section_readiness[formal_results].evidence` 包含 `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
- `paper_readiness.section_readiness[formal_results].blockers` 包含 `formal_gate_status_report_blocked`
- `formal_gate_status_report.permissions_now.remote_training_allowed_now=false`
- `formal_gate_status_report.permissions_now.formal_claim_allowed_now=false`
- `formal_gate_status_report.permissions_now.local_training_allowed_now=false`

## 改动

- `build_module2_paper_readiness.py`
  - 新增默认输入 `DEFAULT_STATUS_REPORT`。
  - CLI 新增 `--status-report`。
  - `inputs` 和 `input_status` 记录 status report 状态。
  - `_global_blockers()` 直接检查 status report。
  - `formal_results` section evidence 新增 status report。
  - claim boundary 新增 status report 必须 ready 的约束。
- `test_module2_paper_readiness.py`
  - CLI 测试传入合成 blocked status report, 并断言 readiness ledger 直接暴露 blocker。
  - synthetic complete evidence 测试传入 ready status report。
  - 新增测试: 即使 claim safety 已 ready, blocked status report 也会直接阻塞 paper readiness。
- regenerated:
  - `0_trials/module2_paper_readiness/module2_paper_readiness.json/.md`
  - `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json/.md`
  - `0_trials/module2_source_freshness_audit/source_freshness_audit.json/.md`
  - `0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json/.md`
  - `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json/.md`
  - `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json/.md`
  - `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
  - `0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json/.md`
  - `0_trials/module2_claim_safety/module2_claim_safety.json`

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_paper_readiness.py` -> `3 passed in 0.20s`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_paper_readiness.py` -> pass
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_paper_readiness.py 2_experiment/forest_n3p/tests/test_module2_claim_safety.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py` -> `29 passed in 1.18s`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_paper_readiness.py 2_experiment/forest_n3p/scripts/build_module2_claim_safety.py 2_experiment/forest_n3p/scripts/build_module2_formal_gate_status_report.py 2_experiment/forest_n3p/scripts/build_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/scripts/build_module2_source_freshness_audit.py` -> pass
- `git diff --check` -> pass

## 边界

- 本轮没有训练。
- 本轮没有运行 remote preflight。
- 本轮没有执行 sync、audit 或 pullback。
- 本轮没有关闭 F02.6。
- 本轮没有生成 formal PPO checkpoint。
- 本轮没有写结果性论文材料。
- 这个变更只把 status report 接入 paper readiness 的 formal results readiness gate。
