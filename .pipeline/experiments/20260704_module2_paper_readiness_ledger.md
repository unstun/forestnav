---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
depends_on:
  - .pipeline/experiments/20260704_module2_i01_method_algorithms.md
  - .pipeline/experiments/20260704_module2_i01_system_diagram.md
  - .pipeline/experiments/20260704_module2_i02_i03_h02_acceptance_integration.md
  - .pipeline/experiments/20260704_module2_h02_formal_acceptance_audit.md
---

# Module2 Paper Readiness Ledger

## 直观结论

本轮新增论文证据矩阵, 把“哪些内容现在能写”和“哪些必须等 formal data”分开。

当前真实状态:

- 方法算法段: ready to write。
- 系统图/架构段: ready to write。
- no-warm Gate #3 failure claim: ready with scope limit。
- 主结果表、formal performance claim、warm-start effect: blocked。

这让论文写作不会因为已有 preview 表格和 no-warm failure 数字而误写 formal performance claim。

## 实现内容

- 新增 `build_module2_paper_readiness.py`。
- 新增 `test_module2_paper_readiness.py`。
- 生成真实 artifact:
  - `0_trials/module2_paper_readiness/module2_paper_readiness.json`
  - `0_trials/module2_paper_readiness/module2_paper_readiness.md`

## 当前真实状态

```text
status=partial_methods_ready_results_blocked
manuscript_ready=false
formal_results_ready=false
allowed_claim_ids=[
  method_is_ha_star_analytic_operator,
  no_warm_gate3_formal_failure
]
```

Section readiness:

```text
method_algorithm=ready_to_write
system_figure=ready_to_write
no_warm_failure_claim=ready_with_scope_limit
main_results_table=blocked
formal_results=blocked
warm_start_effect=blocked
```

主要 blockers:

```text
paper_tables_not_formal
h02_verdict_not_formal
h02_formal_acceptance_not_accepted
h01_manifest_not_ready
f02_6_warm_start_decision_pending
missing_module2_rl_rs_checkpoint
remote_execution_packet_not_ready
requires_dr_sun_approval
missing_gate3_formal_audit
h02_scale_below_h01_manifest
missing_ppo_result_rows
missing_remote_pullback_artifacts
f02_6_formal_chain_pending
claim_safety_blocks_formal_performance
f02_6_pending
```

## 验证

- RED: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_paper_readiness.py` -> missing builder, 2 failed。
- GREEN: same test -> `2 passed in 0.16s`。
- Artifact audit: current readiness ledger separates method/system/no-warm scoped writing from blocked formal result writing。
- Targeted regression: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_paper_readiness.py 2_experiment/forest_n3p/tests/test_module2_paper_tables.py 2_experiment/forest_n3p/tests/test_module2_claim_safety.py 2_experiment/forest_n3p/tests/test_module2_h02_formal_acceptance.py` -> `9 passed in 0.43s`。
- Full regression: `KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests` -> `122 passed in 12.20s`。
- Syntax: `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_paper_readiness.py` passed。

## 边界

- 未本地训练。
- 未远端训练。
- 未批准 F02.6。
- 未生成正式 PPO checkpoint。
- 未把 H02 smoke 升格成 formal。
- 该 ledger 是论文证据路由表, 不是论文结果或正文。
