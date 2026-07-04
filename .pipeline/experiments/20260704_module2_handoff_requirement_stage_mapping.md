---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
scope: formal_gate
not_paper_result_material: true
---

# Module2 Formal Gate Requirement Stage Mapping

## 直观结论

本轮没有记录 F02.6 决策, 没有执行 ssh/rsync/remote preflight/remote training/audit/pullback, 也没有写论文结果材料。

本轮只增强 PPO 替代 RS formal gate 的交接可审计性: `formal_gate_requirements` 现在不只列出还缺哪些训练、评测、验收产物, 还直接指向负责产出或验收这些产物的 `post_f02_6_regeneration_plan.ordered_stages` stage。

## 新增映射

- `training_remote_ppo_checkpoint` -> `gate3_remote_training`
- `evaluation_gate3_episode_outputs` -> `gate3_remote_audit_pullback`
- `acceptance_remote_pullback_and_audit` -> `gate3_remote_audit_pullback`
- `h01_h02_formal_evaluation_acceptance` -> `regenerate_h01_h02_formal_artifacts`

每条 requirement 现在携带:

- `responsible_stage_id`
- `responsible_stage_status`
- `responsible_stage_allowed_now`
- `responsible_stage_blocked_by`
- `responsible_stage_evidence_paths`

`formal_gate_handoff_bundle` 也会保留这些字段, markdown 摘要直接显示 responsible stage。

## 当前读数

- `formal_gate_missing_artifacts.status=formal_gate_missing_artifacts_open`
- `formal_gate_handoff_bundle.status=blocked_until_f02_6_decision`
- 4/4 formal gate requirements 仍为 `blocked_missing_outputs`
- 所有 responsible stages 仍 `allowed_now=false`
- training/evaluation/acceptance/H01-H02 仍被 F02.6 pending、source freshness、remote packet 或 pullback/audit 缺口阻塞

## 产物

- `2_experiment/forest_n3p/scripts/build_module2_formal_gate_handoff_bundle.py`
- `2_experiment/forest_n3p/tests/test_module2_formal_gate_handoff_bundle.py`
- `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json`
- `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.md`
- `0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json`
- `0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.md`

## 验证

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_missing_artifacts_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_handoff_bundle.py
```

结果: `9 passed in 0.40s`

```bash
python -m py_compile \
  2_experiment/forest_n3p/scripts/build_module2_formal_gate_missing_artifacts_audit.py \
  2_experiment/forest_n3p/scripts/build_module2_formal_gate_handoff_bundle.py
```

结果: pass

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_missing_artifacts_audit
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_handoff_bundle
```

结果:

- `formal_gate_missing_artifacts.status=formal_gate_missing_artifacts_open`
- `formal_gate_handoff_bundle.status=blocked_until_f02_6_decision`

## 边界

- 不代表 F02.6 已批准。
- 不代表可以本地训练。
- 不代表可以远端训练。
- 不代表 H01/H02 formal evaluation 已解锁。
- 不代表可以写 formal performance claim 或论文结果表。
