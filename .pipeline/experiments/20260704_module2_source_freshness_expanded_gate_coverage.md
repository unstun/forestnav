---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Source Freshness Expanded Gate Coverage

## 直观结论

本轮把新加入的 gate artifact 纳入 `build_module2_source_freshness_audit.py` 的默认检查范围。

之前 source freshness audit 跟踪 8 个核心 gate artifact。后续我们新增了:

- `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
- `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json`

如果 source freshness 不覆盖它们, 后续 F02.6 关闭后可能只重生成旧 8 个 artifact, 漏掉 post-plan audit 和 missing-artifacts inventory 这两个新 gate 层。现在默认 artifact count 已扩为 10。

## 当前读数

- `status=source_freshness_risks_recorded_gate_still_blocked`
- `artifact_count=10`
- `risk_counts={historical_dirty: 8, historical_clean: 2}`
- `regeneration_required_before_remote_formal_execution=true`
- `runs_training=false`
- `runs_remote_preflight=false`
- `local_training_allowed=false`
- `formal_claim_allowed=false`

新增 regeneration targets:

- `post_f02_6_plan_audit`: required before `approved_remote_preflight`
- `formal_gate_missing_artifacts`: required before `formal_claim_gate`

下游已刷新:

- `post_f02_6_regeneration_plan` 的 `source_regeneration_targets_by_gate` 现在包含 5 个 `approved_remote_preflight` target 和 3 个 `formal_claim_gate` target。
- `formal_gate_missing_artifacts` 的 regeneration count 从 8 变为 10, claim_gate count 从 3 变为 4。
- `formal_gate_gap_audit` 的 `source_freshness.ordered_regeneration_target_count=10`。
- `post_f02_6_plan_audit` 仍为 `post_f02_6_plan_audit_passed`, 且 `training_allowed_now=false`, `remote_preflight_allowed_now=false`。

## 产物

- `2_experiment/forest_n3p/scripts/build_module2_source_freshness_audit.py`
- `2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py`
- `2_experiment/forest_n3p/scripts/build_module2_post_f02_6_regeneration_plan.py`
- `0_trials/module2_source_freshness_audit/source_freshness_audit.json`
- `0_trials/module2_source_freshness_audit/source_freshness_audit.md`
- `0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json`
- `0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.md`
- `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json`
- `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.md`
- `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json`
- `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.md`
- `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
- `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.md`

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_missing_artifacts_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py` -> `28 passed in 1.39s`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_source_freshness_audit.py 2_experiment/forest_n3p/scripts/build_module2_post_f02_6_regeneration_plan.py 2_experiment/forest_n3p/scripts/build_module2_post_f02_6_plan_audit.py 2_experiment/forest_n3p/scripts/build_module2_formal_gate_missing_artifacts_audit.py 2_experiment/forest_n3p/scripts/build_module2_formal_gate_gap_audit.py` -> pass
- `git diff --check` -> pass

## 边界

- 本轮没有训练。
- 本轮没有运行 remote preflight。
- 本轮没有执行 sync 或 pullback。
- 本轮没有关闭 F02.6。
- 本轮没有生成 formal PPO checkpoint。
- 本轮没有放行 formal performance claim。
- 这个变更只扩展 source freshness coverage, 不是论文结果材料。
