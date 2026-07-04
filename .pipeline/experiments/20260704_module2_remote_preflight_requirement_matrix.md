---
status: completed
origin: ai+local
reviewed: false
not_paper_result_material: true
created: 2026-07-04
scope: formal_gate
---

# Module2 Remote Preflight Requirement Matrix

## 直观结论

本轮只推进 remote formal gate, 不训练、不远端执行、不写结果性论文材料。

`remote_formal_execution_packet` 现在新增 `remote_preflight_requirements`, 用来防止 F02.6 一旦批准后直接跳过 remote preflight 进入 PPO training。当前状态仍是:

- `remote_formal_execution_packet.status=blocked_until_f02_6_decision`
- `ready_to_run_remote_training=false`
- `remote_preflight_requirement_counts={blocked_missing_preflight: 2, satisfied: 2}`

## 新增 preflight requirements

- `f02_6_decision_closed_for_preflight`
- `approved_remote_preflight_manifest`
- `remote_preflight_protocol_contract`
- `remote_preflight_command_packetized`

pending 状态下:

- F02.6 decision closed requirement blocked。
- approved remote preflight manifest requirement blocked。
- CUDA/formal protocol contract 已可被 packet 检查, 但 `execution_allowed_now=false`。
- preflight command 已 packetize 成 `ssh gpu3070ti-relay ... preflight_rl_rs_gate3_formal_trial`, 但 `execution_allowed_now=false`。

## Safety audit

`remote_packet_safety_audit` 现在检查:

- packet 必须包含 `remote_preflight_requirements`。
- 四个 requirement 不能缺项。
- 每个 requirement 必须列出 acceptable evidence 和 invalid substitutes。
- packet blocked 时, requirement 不得 `execution_allowed_now=true`。
- F02.6 pending 时, decision/preflight manifest requirement 不得误标 satisfied。
- packet ready 时, 四个 requirement 必须全部 satisfied。

## 当前边界

本轮没有执行:

- `ssh gpu3070ti-relay`
- `rsync`
- remote preflight
- PPO training
- remote audit
- pullback

本轮只是让 packet 和 safety audit 更严格地描述 remote preflight 的验收条件。

## 验证

```bash
PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_remote_formal_execution_packet.py
```

结果: `3 passed in 0.23s`

```bash
PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py
```

结果: `14 passed in 0.72s`

刷新本地 gate 后:

- `remote_packet_safety_audit.status=remote_packet_safety_audit_passed`
- `source_freshness_audit.status=source_freshness_risks_recorded_gate_still_blocked`
- `post_f02_6_regeneration_plan.status=blocked_until_f02_6_decision`
- `post_f02_6_plan_audit.status=post_f02_6_plan_audit_passed`
- `formal_gate_missing_artifacts.status=formal_gate_missing_artifacts_open`
- `formal_gate_status_report.status=formal_gate_status_blocked`
- `claim_safety.status=blocked_formal_performance_claims`
- `paper_readiness.status=partial_methods_ready_results_blocked`

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_remote_formal_execution_packet.py \
  2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py \
  2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py \
  2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py \
  2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_missing_artifacts_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_closure_checklist.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py \
  2_experiment/forest_n3p/tests/test_module2_claim_safety.py \
  2_experiment/forest_n3p/tests/test_module2_paper_readiness.py
```

结果: `78 passed in 3.46s`
