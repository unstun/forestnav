---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Claim Safety Consumes Status Report

## 直观结论

本轮把 `formal_gate_status_report` 接入 `claim_safety`。

之前 status report 已经被 source freshness 跟踪, 也已被 `formal_gate_gap_audit` 直接消费; 但 `claim_safety` 还没有直接读取它。这样 paper readiness 虽然通过 formal gate 被阻塞, 但 claim safety 自身的 blocker 列表还缺 status report 这一层。

现在 `claim_safety` 会读取:

- `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`

并在 status report 仍 blocked、越权执行命令/训练/preflight、允许本地训练/claim, 或存在 input safety issue 时阻塞 formal performance claim。

当前新增 blocker:

- `formal_gate_status_report_blocked`

它已经进入:

- `claim_safety.formal_performance_blockers`
- `paper_readiness.global_blockers`

## 当前读数

- `claim_safety.status=blocked_formal_performance_claims`
- `claim_safety.formal_performance_claim_allowed=false`
- `claim_safety.input_status.status_report_status=formal_gate_status_blocked`
- `claim_safety.input_status.status_report_formal_claim_allowed_now=false`
- `claim_safety.input_status.status_report_input_safety_issue_count=0`
- `claim_safety.formal_performance_blockers` 包含 `formal_gate_status_report_blocked`
- `paper_readiness.status=partial_methods_ready_results_blocked`
- `paper_readiness.formal_results_ready=false`
- `paper_readiness.global_blockers` 包含 `formal_gate_status_report_blocked`
- `formal_gate_status_report.permissions_now.remote_training_allowed_now=false`
- `formal_gate_status_report.permissions_now.formal_claim_allowed_now=false`
- `formal_gate_status_report.permissions_now.local_training_allowed_now=false`

## 改动

- `build_module2_claim_safety.py`
  - 新增默认输入 `DEFAULT_STATUS_REPORT`。
  - CLI 新增 `--status-report`。
  - `inputs` 和 `input_status` 记录 status report 状态。
  - `formal_performance_blockers` 新增 status report blocked / 越权运行 / 越权 claim / input safety issue 检查。
  - claim boundary 新增 status report 必须 ready 的约束。
- `test_module2_claim_safety.py`
  - 原有 exact blocker 测试显式传入合成 ready status report。
  - 新增 status report blocked 单独阻塞 formal claim 测试。
  - 新增 status report 越权运行/claim 的拒绝测试。
- regenerated:
  - `0_trials/module2_claim_safety/module2_claim_safety.json/.md`
  - `0_trials/module2_paper_readiness/module2_paper_readiness.json/.md`
  - `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json/.md`
  - `0_trials/module2_source_freshness_audit/source_freshness_audit.json/.md`
  - `0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json`
  - `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json`
  - `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json/.md`
  - `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
  - `0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json`

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_claim_safety.py` -> `6 passed in 0.13s`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_claim_safety.py` -> pass
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_claim_safety.py 2_experiment/forest_n3p/tests/test_module2_paper_readiness.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_closure_checklist.py` -> `32 passed in 1.36s`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_claim_safety.py 2_experiment/forest_n3p/scripts/build_module2_paper_readiness.py 2_experiment/forest_n3p/scripts/build_module2_formal_gate_status_report.py 2_experiment/forest_n3p/scripts/build_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/scripts/build_module2_source_freshness_audit.py 2_experiment/forest_n3p/scripts/build_module2_formal_gate_closure_checklist.py` -> pass
- `git diff --check` -> pass

## 边界

- 本轮没有训练。
- 本轮没有运行 remote preflight。
- 本轮没有执行 sync、audit 或 pullback。
- 本轮没有关闭 F02.6。
- 本轮没有生成 formal PPO checkpoint。
- 本轮没有写结果性论文材料。
- 这个变更只把 status report 接入 claim safety / paper readiness 的 formal claim blocker 链。
