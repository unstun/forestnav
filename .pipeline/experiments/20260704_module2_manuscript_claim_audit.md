---
origin: ai+local
reviewed: false
date: 2026-07-04
topic: module2_manuscript_claim_audit
---

# Module2 Manuscript Claim Audit

## 目的

`module2_paper_section_seed.tex` 已经 input 到 `3_paper/main.tex`。下一步需要把“主稿里有没有越界 claim”变成机器可复查的安全闸，而不是靠人工记忆。这个 audit 展开 `main.tex` 的 `\input{...}` 后扫描 Module2 prohibited claims，同时确认 formal results 和 warm-start effect 仍保持 blocked。

本轮不训练，不远端运行，不写 formal result。

## 产物

- `2_experiment/forest_n3p/scripts/build_module2_manuscript_claim_audit.py`
- `2_experiment/forest_n3p/tests/test_module2_manuscript_claim_audit.py`
- `3_paper/module2_claim_audit/module2_manuscript_claim_audit.json`
- `3_paper/module2_claim_audit/module2_manuscript_claim_audit.md`

## 当前状态

- `status=maintex_module2_claim_audit_passed`
- `prohibited_claim_audit.status=clean`
- `module2_seed_input_present=True`
- `module2_label_present=True`
- `formal_results_status=blocked`
- `warm_start_effect_status=blocked`
- `formal_results_blocked_comment_present=True`
- `warm_start_blocked_comment_present=True`

## 边界

- LaTeX comments are ignored for prohibited-claim matching, so blocked comments can document missing evidence without becoming claims.
- `main.tex` 仍不能写 Module2 formal performance improvement、warm-start effect、RL replaces Hybrid A*、global optimality、completeness/generalization overclaims。
- 正式 PPO checkpoint 仍必须等 F02.6 关闭后在 `gpu3070ti-relay` 训练/审计/回传。

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_manuscript_claim_audit.py` -> `2 passed in 0.17s`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_manuscript_claim_audit --output-dir 3_paper/module2_claim_audit --manifest-out 3_paper/module2_claim_audit/module2_manuscript_claim_audit.json --markdown-out 3_paper/module2_claim_audit/module2_manuscript_claim_audit.md` -> `status=maintex_module2_claim_audit_passed`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_manuscript_claim_audit.py` -> pass
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_manuscript_claim_audit.py 2_experiment/forest_n3p/tests/test_module2_paper_section_seed.py 2_experiment/forest_n3p/tests/test_module2_claim_safety.py` -> `6 passed in 0.35s`
- `cd 3_paper && pdflatex -interaction=nonstopmode -halt-on-error -draftmode -output-directory=/tmp/forestnav_module2_texcheck main.tex` -> pass; temp directory removed.
- `KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests` -> `126 passed in 11.54s`
