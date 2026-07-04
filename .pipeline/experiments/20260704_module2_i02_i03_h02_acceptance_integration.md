---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
depends_on:
  - .pipeline/experiments/20260704_module2_h02_formal_acceptance_audit.md
  - .pipeline/experiments/20260704_module2_i02_paper_table_protocol.md
  - .pipeline/experiments/20260704_module2_i03_claim_safety.md
---

# I02/I03 H02 Acceptance Integration

## 直观结论

本轮把新加的 H02 formal acceptance audit 接入 I02 paper table builder 和 I03 claim safety guard。

现在不是只有 H02 verdict 或 paper table 自己说 formal 才算数。论文结果链必须同时满足:

- H02 formal acceptance artifact: `formal_output_accepted=true`
- H02 formal acceptance artifact: `paper_result_input_allowed=true`
- I02 paper tables: `formal_claim_allowed=true`
- I03 claim safety: `formal_performance_claim_allowed=true`

当前真实状态仍为 blocked。

## 实现内容

- `build_module2_paper_tables.py` 新增 `--h02-formal-acceptance`, 并把 `h02_formal_acceptance_not_accepted` 及其 blockers 纳入 I02 blocker list。
- `build_module2_claim_safety.py` 新增 `--h02-formal-acceptance`, 并把 H02 acceptance 纳入 formal performance claim gate。
- `test_module2_paper_tables.py` 增加 paper tables 自称 formal 但 H02 acceptance blocked 时仍必须 blocked 的回归测试。
- `test_module2_claim_safety.py` 增加 paper tables/H01/F02.6 都看似 formal 但 H02 acceptance blocked 时仍必须 blocked 的回归测试。
- 重建:
  - `0_trials/module2_paper_tables/module2_paper_tables.json`
  - `0_trials/module2_paper_tables/module2_paper_tables.md`
  - `0_trials/module2_claim_safety/module2_claim_safety.json`
  - `0_trials/module2_claim_safety/module2_claim_safety.md`

## 当前真实状态

I02:

```text
status=blocked_no_formal_h02_data
formal_claim_allowed=false
h02_formal_acceptance_status=blocked_formal_output_acceptance
h02_formal_output_accepted=false
h02_paper_result_input_allowed=false
blockers include h02_formal_acceptance_not_accepted
```

I03:

```text
status=blocked_formal_performance_claims
formal_performance_claim_allowed=false
h02_formal_acceptance_status=blocked_formal_output_acceptance
h02_formal_output_accepted=false
h02_paper_result_input_allowed=false
blockers include h02_formal_acceptance_not_accepted
```

## 验证

- RED I03: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_claim_safety.py` failed because CLI/build_manifest did not accept `h02_formal_acceptance`。
- GREEN I03: same test -> `2 passed in 0.09s`。
- RED I02: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_paper_tables.py` failed because CLI/build_manifest did not accept `h02_formal_acceptance`。
- GREEN I02+I03: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_paper_tables.py 2_experiment/forest_n3p/tests/test_module2_claim_safety.py` -> `4 passed in 0.12s`。
- Artifact audit: I02/I03 both read `h02_formal_acceptance_status=blocked_formal_output_acceptance` and both remain blocked。
- Targeted regression: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_paper_tables.py 2_experiment/forest_n3p/tests/test_module2_claim_safety.py 2_experiment/forest_n3p/tests/test_module2_h02_formal_acceptance.py 2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py` -> `12 passed in 0.57s`。
- Full regression: `KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests` -> `120 passed in 12.01s`。
- Syntax: `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_paper_tables.py 2_experiment/forest_n3p/scripts/build_module2_claim_safety.py` passed。

## 边界

- 未本地训练。
- 未远端训练。
- 未批准 F02.6。
- 未生成正式 PPO checkpoint。
- 未把 H02 smoke 升格成 formal。
- 这一步只补 claim/table 链路的验收依赖, 不是论文结果。
