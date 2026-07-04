---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Claim Safety Consumes Closure Checklist

## 直观结论

本轮把 formal gate closure checklist 接入 `claim_safety`。现在 formal performance claim 不只受 H02 acceptance、paper tables、H01、F02.6 和 Gate3 audit 约束, 还必须等 closure checklist 关闭。

当前 checklist 仍是:

- `status=formal_gate_closure_blocked`
- `open_item_count=8`
- `input_safety_issue_count=0`

因此 `claim_safety` 现在新增 blocker:

- `formal_gate_closure_checklist_open`

这个 blocker 会继续被 `paper_readiness` 通过 `claim_safety.formal_performance_blockers` 继承, 所以 paper readiness 也不会在 checklist open 时误放行 formal results。

## 当前读数

- `claim_safety.status=blocked_formal_performance_claims`
- `claim_safety.formal_performance_claim_allowed=false`
- `claim_safety.input_status.closure_checklist_status=formal_gate_closure_blocked`
- `claim_safety.input_status.closure_checklist_open_item_count=8`
- `claim_safety.formal_performance_blockers` 包含 `formal_gate_closure_checklist_open`
- `paper_readiness.status=partial_methods_ready_results_blocked`
- `paper_readiness.formal_results_ready=false`
- `paper_readiness.global_blockers` 包含 `formal_gate_closure_checklist_open`

## 改动

- `build_module2_claim_safety.py`
  - 新增默认输入 `closure_checklist_path`。
  - CLI 新增 `--closure-checklist`。
  - `inputs` 和 `input_status` 记录 closure checklist 状态。
  - `formal_performance_blockers` 新增 closure checklist open / 越权运行 / 越权 claim / input safety issue 检查。
  - claim boundary 新增 closure checklist 必须关闭的约束。
- `test_module2_claim_safety.py`
  - 原有用例显式传入 closure checklist。
  - 新增 checklist open 单独阻塞 formal claim 测试。
  - 新增 checklist 越权运行/claim 的拒绝测试。
- regenerated:
  - `0_trials/module2_claim_safety/module2_claim_safety.json`
  - `0_trials/module2_claim_safety/module2_claim_safety.md`
  - `0_trials/module2_paper_readiness/module2_paper_readiness.json`
  - `0_trials/module2_paper_readiness/module2_paper_readiness.md`

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_claim_safety.py` -> `4 passed in 0.11s`
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_claim_safety.py 2_experiment/forest_n3p/tests/test_module2_paper_readiness.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_closure_checklist.py` -> `31 passed in 1.21s`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_claim_safety.py 2_experiment/forest_n3p/scripts/build_module2_paper_readiness.py 2_experiment/forest_n3p/scripts/build_module2_formal_gate_closure_checklist.py 2_experiment/forest_n3p/scripts/build_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/scripts/build_module2_post_f02_6_plan_audit.py` -> pass
- `git diff --check` -> pass

## 边界

- 本轮没有训练。
- 本轮没有运行 remote preflight。
- 本轮没有执行 sync 或 pullback。
- 本轮没有关闭 F02.6。
- 本轮没有生成 formal PPO checkpoint。
- 本轮没有写结果性论文材料。
- 这个变更只把 closure checklist 纳入 claim safety / paper readiness 的 formal claim blocker 链。
