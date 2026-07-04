---
origin: ai+local
reviewed: false
date: 2026-07-04
topic: module2_manuscript_evidence_map
---

# Module2 Manuscript Evidence Map

## 目的

`module2_manuscript_claim_audit` 已经证明主稿没有越界 claim, 但它还没有回答“正文里每一个可写/不可写的 Module2 表述具体连到哪个证据”。本轮新增 evidence map, 把 `3_paper/main.tex` 展开后的 Module2 claim units 逐条映射到 I01/I03/readiness/Gate3/F02.6/remote execution packet。

本轮不训练、不远端运行、不改 F02.6 决策状态。正式 PPO checkpoint 仍必须等 F02.6 关闭后走 `gpu3070ti-relay`。

## 产物

- `2_experiment/forest_n3p/scripts/build_module2_manuscript_evidence_map.py`
- `2_experiment/forest_n3p/tests/test_module2_manuscript_evidence_map.py`
- `3_paper/module2_evidence_map/module2_manuscript_evidence_map.json`
- `3_paper/module2_evidence_map/module2_manuscript_evidence_map.md`

## 当前状态

- `status=module2_manuscript_evidence_mapped`
- `claim_audit_status=maintex_module2_claim_audit_passed`
- `formal_performance_claim_allowed=False`
- `f02_6_decision_status=pending_human_decision`
- `remote_execution_ready=False`

## Claim Unit 映射

- `method_is_ha_star_analytic_operator`: `evidence_state=mapped`; 证据来自 claim safety、method algorithms、system diagram、paper readiness、section seed；code anchors 当前 14 条。
- `no_warm_gate3_formal_failure`: `evidence_state=mapped`; Gate3 指标为 terminal-RS success `0.453125`, episodes `64`, threshold `0.8`。
- `formal_results_blocked`: `evidence_state=blocked_as_expected`; blockers 包含 `missing_module2_rl_rs_checkpoint`, `h02_formal_acceptance_not_accepted`, `f02_6_pending` 等。
- `warm_start_effect_blocked`: `evidence_state=blocked_as_expected`; blockers 包含 `f02_6_not_approved`, `requires_dr_sun_approval`, `missing_module2_rl_rs_checkpoint`。

## 边界

- evidence map 是主稿 claim-to-evidence 路由表, 不是 formal result。
- method/system/no-warm scoped units 可写, 但只能按 I03 的 qualifier 写。
- formal results/main table/warm-start effect 仍不能写成论文结果或效果 claim。
- 本地禁止训练；正式训练/审计/回传只能在 F02.6 关闭后走 `gpu3070ti-relay`。

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_manuscript_evidence_map.py` -> `2 passed in 0.15s`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_manuscript_evidence_map.py` -> pass
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_manuscript_evidence_map` -> `status=module2_manuscript_evidence_mapped`
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_manuscript_evidence_map.py 2_experiment/forest_n3p/tests/test_module2_manuscript_claim_audit.py 2_experiment/forest_n3p/tests/test_module2_paper_section_seed.py 2_experiment/forest_n3p/tests/test_module2_paper_readiness.py 2_experiment/forest_n3p/tests/test_module2_claim_safety.py` -> `10 passed in 0.46s`
- `KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests` -> `128 passed in 12.25s`
- `cd 3_paper && pdflatex -interaction=nonstopmode -halt-on-error -draftmode -output-directory=/tmp/forestnav_module2_texcheck main.tex` -> pass; 仅有既有 undefined citation/reference warnings; temp directory removed.
