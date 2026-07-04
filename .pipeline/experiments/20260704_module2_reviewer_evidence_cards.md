---
origin: ai+local
reviewed: false
date: 2026-07-04
topic: module2_reviewer_evidence_cards
---

# Module2 Reviewer Evidence Cards

## 目的

`module2_manuscript_evidence_map` 已经把主稿 Module2 claim units 映射到证据, 但审稿/写作时还需要更直接的“证据卡片”：每张卡给出正文 `.tex` 行号、primary evidence、代码锚点或指标、blocked 原因和写作指令。本轮把 evidence map 转成 reviewer-facing cards, 方便后续 supplement、内部审稿清单或主稿 claim audit 使用。

本轮不训练、不远端运行、不改变 F02.6 pending。正式 PPO checkpoint 仍必须等 F02.6 关闭后走 `gpu3070ti-relay`。

## 产物

- `2_experiment/forest_n3p/scripts/build_module2_reviewer_evidence_cards.py`
- `2_experiment/forest_n3p/tests/test_module2_reviewer_evidence_cards.py`
- `3_paper/module2_reviewer_evidence_cards/module2_reviewer_evidence_cards.json`
- `3_paper/module2_reviewer_evidence_cards/module2_reviewer_evidence_cards.md`
- `3_paper/module2_reviewer_evidence_cards/module2_reviewer_evidence_cards.tex`

## 当前状态

- `status=reviewer_evidence_cards_ready`
- `supplement_latex_audit.status=clean`
- `formal_performance_claim_allowed=False`
- `f02_6_decision_status=pending_human_decision`
- `remote_execution_ready=False`

## Cards

- `method_is_ha_star_analytic_operator`: reviewer verdict `claim_traceable_with_scope_limit`; manuscript anchors include `3_paper/module2_section_seed/module2_paper_section_seed.tex:8` and `:11`; code anchors count 14.
- `no_warm_gate3_formal_failure`: reviewer verdict `claim_traceable_with_scope_limit`; manuscript anchor `3_paper/module2_section_seed/module2_paper_section_seed.tex:14`; metric values `terminal_rs_success_rate=0.453125`, `episodes=64`, `success_threshold=0.8`.
- `formal_results_blocked`: reviewer verdict `blocked_placeholder_traceable`; manuscript anchors `3_paper/module2_section_seed/module2_paper_section_seed.tex:14` and `:16`; writing instruction says not to write as a result claim.
- `warm_start_effect_blocked`: reviewer verdict `blocked_placeholder_traceable`; manuscript anchors `3_paper/module2_section_seed/module2_paper_section_seed.tex:17` and `:14`; writing instruction says not to write as a result claim.

## 边界

- reviewer cards 是 traceability/supplement-ready artifact, 不是 formal result。
- LaTeX appendix fragment 是 supplement/input-ready 产物, 不是默认接入主稿正文的正式结果段。
- method/no-warm cards 可用于写作, 但只能按卡片 scope/qualifier 写。
- formal results/main table/warm-start effect 仍不能写成论文结果或效果 claim。
- 本地禁止训练；正式训练/审计/回传只能在 F02.6 关闭后走 `gpu3070ti-relay`。

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_manuscript_evidence_map.py 2_experiment/forest_n3p/tests/test_module2_reviewer_evidence_cards.py` -> `4 passed in 0.25s`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_manuscript_evidence_map.py 2_experiment/forest_n3p/scripts/build_module2_reviewer_evidence_cards.py` -> pass
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_manuscript_evidence_map` -> `status=module2_manuscript_evidence_mapped`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_reviewer_evidence_cards` -> `status=reviewer_evidence_cards_ready`, outputs JSON/Markdown/LaTeX
- wrapper compile for `3_paper/module2_reviewer_evidence_cards/module2_reviewer_evidence_cards.tex` -> pdflatex draftmode pass; long path overfull warnings remain.
- `KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests` -> `130 passed in 11.95s`
- `cd 3_paper && pdflatex -interaction=nonstopmode -halt-on-error -draftmode -output-directory=/tmp/forestnav_module2_texcheck main.tex` -> pass; 仅有既有 undefined citation/reference warnings; temp directory removed.
