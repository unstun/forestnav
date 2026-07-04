---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
scope: formal_gate
not_paper_result_material: true
---

# Module2 H02 Formal Acceptance Requirement Matrix

## 直观结论

这次变更不是训练结果, 也不是论文结果材料。它只是把 H02 是否能进入论文表格/claim 的判断拆成机器可读 requirement matrix, 防止把 local smoke、candidate verdict、缺 pullback 的远端 stdout、或 BC/analytic rows 误当成 formal PPO result。

## 改动范围

- `build_module2_h02_formal_acceptance.py` 输出 `formal_acceptance_requirements` 和 `formal_acceptance_requirement_counts`。
- `h02_formal_acceptance.json` / `.md` 重新生成, 当前仍为 `blocked_formal_output_acceptance`。
- `module2_paper_tables.json` 继续保持 `blocked_no_formal_h02_data`。
- `formal_gate_gap_audit`, `formal_gate_missing_artifacts`, `source_freshness_audit`, `post_f02_6_regeneration_plan`, `post_f02_6_plan_audit` 级联刷新, 仍保持 formal gate blocked。
- `test_module2_h02_formal_acceptance.py` 增加当前 blocked 状态、synthetic formal 状态、missing schema 状态三类 requirement matrix 断言。

## 当前 requirement 状态

- `h01_schema_and_h02_output_schema_match`: satisfied, 但当前仍不允许 paper result input。
- `h02_formal_scope_and_scale_match_h01`: blocked, 因 H01/F02.6/PPO checkpoint/remote packet 仍未满足。
- `gate3_audit_and_pullback_acceptance`: blocked, 因缺 formal Gate3 audit 和 remote pullback artifacts。
- `ppo_rows_and_checkpoint_hash_present`: blocked, 因缺 PPO result rows 和正式 checkpoint hash。

当前计数: `satisfied=1`, `blocked_formal_acceptance=3`。

## 明确边界

- 未执行本地训练。
- 未执行远端训练。
- 未执行远端 preflight / sync / audit / pullback。
- 未写结果性论文材料。
- 该 artifact 只能作为 formal gate 状态证据, 不能作为 PPO 替代 RS 的性能证据。

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_h02_formal_acceptance.py`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_h02_formal_acceptance`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_paper_tables`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_missing_artifacts_audit`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_source_freshness_audit`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_regeneration_plan`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_plan_audit`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_gap_audit`

