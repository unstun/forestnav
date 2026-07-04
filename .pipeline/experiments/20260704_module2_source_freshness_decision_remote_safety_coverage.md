---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Source Freshness Decision And Remote Safety Coverage

## 直观结论

本轮把两个已经存在、但尚未进入 source freshness 默认覆盖面的 formal gate artifact 纳入再生成闸门:

- `0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.json`
- `0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`

这样做的原因很直接: F02.6 decision gate audit 负责证明人类决策没有被绕过; remote packet safety audit 负责证明远端训练包没有在 pending 状态下误放行。如果 source freshness 不跟踪它们, F02.6 关闭后可能重生成了 remote packet、formal gap、H01/H02 和 claim gate, 却漏掉这两个安全审计层。

现在 `source_freshness_audit` 默认 target 数从 10 扩到 12。

## 当前读数

- `source_freshness_audit.status=source_freshness_risks_recorded_gate_still_blocked`
- `artifact_count=12`
- `risk_counts={historical_dirty: 10, historical_clean: 2}`
- `regeneration_required_before_remote_formal_execution=true`
- `post_f02_6_regeneration_plan.status=blocked_until_f02_6_decision`
- `approved_remote_preflight` 前需要 source-fresh 的 target 数从 5 变为 7
- `formal_gate_missing_artifacts.status=formal_gate_missing_artifacts_open`
- `formal_gate_missing_artifacts.missing_counts_by_category.regeneration=12`
- `formal_gate_gap_audit.source_freshness.ordered_regeneration_target_count=12`
- `post_f02_6_plan_audit.status=post_f02_6_plan_audit_passed`
- `training_allowed_now=false`
- `remote_preflight_allowed_now=false`

新增 `approved_remote_preflight` 前 regeneration targets:

- `f02_6_decision_gate_audit`
- `remote_packet_safety_audit`

## 改动

- `build_module2_source_freshness_audit.py`
  - 默认 target 新增 `f02_6_decision_gate_audit`。
  - 默认 target 新增 `remote_packet_safety_audit`。
- `build_module2_post_f02_6_regeneration_plan.py`
  - 为 `f02_6_decision_gate_audit` 增加再生成命令。
  - 为 `remote_packet_safety_audit` 增加再生成命令。
- tests
  - `test_module2_source_freshness_audit.py` 断言两个新 target 默认存在且 required before `approved_remote_preflight`。
  - `test_module2_post_f02_6_regeneration_plan.py` 断言两个新 target 的再生成命令进入 plan。
- generated gate artifacts
  - 重新生成 source freshness、post-F02.6 regeneration plan、formal gate missing-artifacts inventory、formal gate gap audit、post-F02.6 plan audit。

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py` -> `7 passed in 0.55s`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_source_freshness_audit.py 2_experiment/forest_n3p/scripts/build_module2_post_f02_6_regeneration_plan.py` -> pass

## 边界

- 本轮没有训练。
- 本轮没有运行 remote preflight。
- 本轮没有执行 sync 或 pullback。
- 本轮没有关闭 F02.6。
- 本轮没有生成 formal PPO checkpoint。
- 本轮没有写结果性论文材料。
- 这个变更只补 source freshness / regeneration coverage, 不改变 PPO 替代 RS 的 formal evidence 状态。
