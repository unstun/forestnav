---
status: completed
origin: ai+local
reviewed: false
not_paper_result_material: true
created: 2026-07-04
scope: formal_gate
---

# Module2 Formal Gate Requirement Matrix

## 直观结论

本轮只推进 PPO 替代 RS 的 formal gate, 不训练、不远端执行、不写结果性论文材料。

`formal_gate_missing_artifacts` 现在不只列出缺文件, 还新增 `formal_gate_requirements` 矩阵, 把正式链条里还缺的训练、评测、验收产物拆成四条机器可读 requirement:

- `training_remote_ppo_checkpoint`
- `evaluation_gate3_episode_outputs`
- `acceptance_remote_pullback_and_audit`
- `h01_h02_formal_evaluation_acceptance`

每条 requirement 都写清:

- `phase`
- `status`
- `execution_allowed_now`
- `missing_artifact_ids`
- `missing_paths`
- `blocked_by`
- `acceptable_evidence`
- `invalid_substitutes`

## 当前 gate 状态

- `formal_gate_missing_artifacts.status=formal_gate_missing_artifacts_open`
- `formal_gate_requirement_counts={blocked_missing_outputs: 4}`
- `post_f02_6_plan_audit.status=post_f02_6_plan_audit_passed`
- `formal_gate_status_report.status=formal_gate_status_blocked`
- `claim_safety.status=blocked_formal_performance_claims`
- `paper_readiness.status=partial_methods_ready_results_blocked`

## 仍缺的 formal 产物

训练产物:

- `train/final_model.zip`
- `train/summary.json`
- `train/training_manifest.json`

评测产物:

- `eval/gate3_eval_episodes.csv`
- `eval/gate3_summary.json`

验收/回传产物:

- `gate3_trial_manifest.json`
- `gate3_formal_audit.json`
- pulled-back checkpoint SHA-256 record
- H01 ready formal manifest
- H02 formal output acceptance

## 不能替代的东西

- 本地训练输出不能替代远端 formal PPO checkpoint。
- available-subset smoke 不能替代 Gate3 formal evaluation。
- no-warm Gate3 failed checkpoint/eval 不能替代 obstacle-summary warm-start formal evidence。
- 远端 stdout 或单个 checkpoint 文件不能替代 pullback manifest、formal audit 和 SHA-256 记录。
- paper table preview 不能替代 H02 formal acceptance。

## 验证

```bash
PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_missing_artifacts_audit.py
```

结果: `4 passed in 0.31s`

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_missing_artifacts_audit
```

结果: `status=formal_gate_missing_artifacts_open`

刷新相邻 gate 后:

- `source_freshness_audit.status=source_freshness_risks_recorded_gate_still_blocked`
- `post_f02_6_regeneration_plan.status=blocked_until_f02_6_decision`
- `post_f02_6_plan_audit.status=post_f02_6_plan_audit_passed`
- `remote_packet_safety_audit.status=remote_packet_safety_audit_passed`
- `formal_gate_closure_checklist.status=formal_gate_closure_blocked`
- `formal_gate_status_report.status=formal_gate_status_blocked`
- `claim_safety.status=blocked_formal_performance_claims`
- `paper_readiness.status=partial_methods_ready_results_blocked`

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_missing_artifacts_audit.py \
  2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py \
  2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py \
  2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py \
  2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_closure_checklist.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py \
  2_experiment/forest_n3p/tests/test_module2_claim_safety.py \
  2_experiment/forest_n3p/tests/test_module2_paper_readiness.py
```

结果: `60 passed in 3.17s`

## 注意

刷新 `source_freshness_audit` 后, `post_f02_6_plan_audit` 曾短暂失败, 原因是 source freshness 的 approved remote preflight target 计数更新为 8, 而 regeneration plan 仍是旧计数 7。重生成 `post_f02_6_regeneration_plan` 后 audit 恢复 passed。这个过程没有执行训练、远端 preflight、远端同步或远端 audit。
