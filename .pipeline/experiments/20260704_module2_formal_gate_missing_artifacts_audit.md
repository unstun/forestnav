---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Formal Gate Missing Artifacts Audit

## 直观结论

本轮新增 `build_module2_formal_gate_missing_artifacts_audit.py`, 把当前 PPO 替代 RS formal gate 还缺的训练、评测、验收产物固化成机器可读清单。

它不执行训练、不执行 remote preflight、不执行 sync/pullback、不运行 H01/H02 evaluation, 也不生成论文结果材料。它只读取现有 gate artifact, 汇总哪些 evidence 还没有准备好。

当前真实结果:

- `status=formal_gate_missing_artifacts_open`
- `all_required_evidence_present=false`
- `audit_issue_count=0`
- `local_training_allowed=false`
- `formal_claim_allowed=false`
- F02.6 decision record 仍是 `pending_human_decision`
- remote packet 仍是 `blocked_until_f02_6_decision`
- H01 仍是 `blocked_pending_decisions`
- H02 仍是 `blocked_formal_output_acceptance`

## 缺口摘要

- decision: 1
- regeneration: 8
- gate_sequence: 7
- training: 3
- evaluation: 2
- acceptance: 3
- evaluation_acceptance: 2
- claim_gate: 3

关键 file-level 缺口:

- training:
  - `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip`
  - `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json`
  - `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json`
- evaluation:
  - `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv`
  - `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json`
- acceptance:
  - `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json`
  - `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json`
  - pulled-back checkpoint hash record

## 产物

- `2_experiment/forest_n3p/scripts/build_module2_formal_gate_missing_artifacts_audit.py`
- `2_experiment/forest_n3p/tests/test_module2_formal_gate_missing_artifacts_audit.py`
- `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json`
- `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.md`

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_missing_artifacts_audit.py` -> `4 passed in 0.26s`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_formal_gate_missing_artifacts_audit.py` -> pass
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_missing_artifacts_audit` -> `status=formal_gate_missing_artifacts_open`

## 边界

- 本轮没有训练。
- 本轮没有运行 remote preflight。
- 本轮没有执行 sync 或 pullback。
- 本轮没有关闭 F02.6。
- 本轮没有生成 formal PPO checkpoint。
- 本轮没有放行 formal performance claim。
- 这个 audit 是 formal gate inventory, 不是论文结果表或附录材料。
