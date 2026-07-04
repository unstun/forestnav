---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Post-F02.6 Plan Consumes Closure Checklist

## 直观结论

上一轮 `formal_gate_gap_audit` 已经消费 closure checklist。本轮把同一个 checklist 接入 `post_f02_6_plan_audit`, 让 post-F02.6 ordered plan 的审计也能看到 closure checklist 的 open 状态和 safety 状态。

当前语义:

- closure checklist open 是当前真实状态, 不会单独让 pending plan audit 失败。
- 如果 claim gate stage 被错误标为 ready, 而 closure checklist 仍 open, plan audit 会失败。
- 如果 closure checklist 自己执行命令、训练、remote preflight、允许本地训练、允许 claim, 或报告 input safety issue, plan audit 会失败。

也就是说, `post_f02_6_plan_audit_passed` 现在只表示 ordered plan 正确保持 blocked, 不是训练许可。

## 当前读数

- `post_f02_6_plan_audit.status=post_f02_6_plan_audit_passed`
- `post_f02_6_plan_audit.audit_issue_count=0`
- `closure_checklist_summary.status=formal_gate_closure_blocked`
- `closure_checklist_summary.open_item_count=8`
- `closure_checklist_summary.input_safety_issue_count=0`
- `closure_checklist_summary.runs_training=false`
- `closure_checklist_summary.runs_remote_preflight=false`
- `closure_checklist_summary.formal_claim_allowed=false`

## 改动

- `build_module2_post_f02_6_plan_audit.py`
  - 新增默认输入 `closure_checklist_path`。
  - manifest 新增 `closure_checklist_summary`。
  - CLI 新增 `--closure-checklist`。
  - 新增 closure checklist safety checks。
  - 新增 `claim_gate_ready_with_open_closure_checklist` 检查。
  - Markdown 新增 `Closure Checklist` 区块。
- `test_module2_post_f02_6_plan_audit.py`
  - 所有 synthetic plan audit 测试显式传入 closure checklist。
  - 新增 claim gate ready + open closure checklist 的失败测试。
  - 新增 closure checklist 越权运行/claim 的失败测试。
- regenerated:
  - `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
  - `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.md`

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py` -> `10 passed in 0.51s`
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_missing_artifacts_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py 2_experiment/forest_n3p/tests/test_module2_f02_6_decision_gate_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_closure_checklist.py` -> `47 passed in 2.28s`
- `python -m py_compile ... build_module2_post_f02_6_plan_audit.py ...` -> pass
- `git diff --check` -> pass

## 边界

- 本轮没有训练。
- 本轮没有运行 remote preflight。
- 本轮没有执行 sync 或 pullback。
- 本轮没有关闭 F02.6。
- 本轮没有生成 formal PPO checkpoint。
- 本轮没有写结果性论文材料。
- 这个变更只把 closure checklist 纳入 post-F02.6 ordered plan audit。
