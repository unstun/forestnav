---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
scope: formal_gate
not_paper_result_material: true
---

# Module2 Status Report Requirement Stage Summary

## 直观结论

本轮没有记录 F02.6 决策, 没有执行 ssh/rsync/remote preflight/remote training/audit/pullback, 也没有写论文结果材料。

本轮让顶层 `formal_gate_status_report` 直接消费 `formal_gate_handoff_bundle.formal_gate_requirements` 中的 responsible stage 映射。这样 status report 不只知道 handoff bundle 当前 blocked, 也能直接列出四类 formal 缺口分别卡在哪个 post-F02.6 stage。

## 新增字段

`formal_gate_status_report.json` 新增:

- `formal_gate_requirement_stage_summary`
- `current_state.handoff_requirement_stage_mapped_count`
- `current_state.handoff_requirement_stage_unmapped_count`

status report 现在会检查:

- handoff bundle 必须暴露 `formal_gate_requirements`
- 四条 required requirement 必须都存在
- 四条 requirement 必须有 `responsible_stage_id`
- `responsible_stage_id` 必须匹配预期 stage
- 被禁用的 responsible stage 必须解释 `blocked_by`
- blocked requirement 的 responsible stage 不得提前 ready

## 当前读数

- `formal_gate_status_report.status=formal_gate_status_blocked`
- `formal_gate_requirement_stage_summary.mapped_requirement_count=4`
- `formal_gate_requirement_stage_summary.unmapped_requirement_count=0`
- `formal_gate_requirement_stage_summary.mismatched_requirement_count=0`
- `formal_gate_requirement_stage_summary.blocked_stage_count=4`
- `permissions_now.remote_training_allowed_now=false`
- `permissions_now.formal_claim_allowed_now=false`

当前四条映射:

- `training_remote_ppo_checkpoint` -> `gate3_remote_training`
- `evaluation_gate3_episode_outputs` -> `gate3_remote_audit_pullback`
- `acceptance_remote_pullback_and_audit` -> `gate3_remote_audit_pullback`
- `h01_h02_formal_evaluation_acceptance` -> `regenerate_h01_h02_formal_artifacts`

## 产物

- `2_experiment/forest_n3p/scripts/build_module2_formal_gate_status_report.py`
- `2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py`
- `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
- `0_trials/module2_formal_gate_status_report/formal_gate_status_report.md`
- `0_trials/module2_claim_safety/module2_claim_safety.json`
- `0_trials/module2_paper_readiness/module2_paper_readiness.json`
- `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
- `0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`

## 验证

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py \
  2_experiment/forest_n3p/tests/test_module2_claim_safety.py \
  2_experiment/forest_n3p/tests/test_module2_paper_readiness.py \
  2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py \
  2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py
```

结果: `63 passed in 2.91s`

```bash
python -m py_compile \
  2_experiment/forest_n3p/scripts/build_module2_formal_gate_status_report.py \
  2_experiment/forest_n3p/scripts/build_module2_claim_safety.py \
  2_experiment/forest_n3p/scripts/build_module2_paper_readiness.py \
  2_experiment/forest_n3p/scripts/build_module2_post_f02_6_plan_audit.py \
  2_experiment/forest_n3p/scripts/build_module2_remote_packet_safety_audit.py
```

结果: pass

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_status_report
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_claim_safety
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_paper_readiness
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_plan_audit
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_remote_packet_safety_audit
```

结果:

- `formal_gate_status_report.status=formal_gate_status_blocked`
- `module2_claim_safety.status=blocked_formal_performance_claims`
- `module2_paper_readiness.status=partial_methods_ready_results_blocked`
- `post_f02_6_plan_audit.status=post_f02_6_plan_audit_passed`
- `remote_packet_safety_audit.status=remote_packet_safety_audit_passed`

## 边界

- 不代表 F02.6 已批准。
- 不代表可以本地训练。
- 不代表可以远端训练。
- 不代表 H01/H02 formal evaluation 已解锁。
- 不代表可以写 formal performance claim 或论文结果表。
