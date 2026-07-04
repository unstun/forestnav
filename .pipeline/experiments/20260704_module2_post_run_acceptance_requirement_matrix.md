---
status: completed
origin: ai+local
reviewed: false
not_paper_result_material: true
created: 2026-07-04
scope: formal_gate
---

# Module2 Post-Run Acceptance Requirement Matrix

## 直观结论

本轮只推进 remote training 之后的本地验收门, 不训练、不远端执行、不写结果性论文材料。

`remote_formal_execution_packet` 现在新增 `post_run_acceptance_requirements`, 防止把“远端训练命令结束”误当成“本地可写结果 / 可 claim”。当前状态仍是:

- `remote_formal_execution_packet.status=blocked_until_f02_6_decision`
- `ready_to_run_remote_training=false`
- `post_run_acceptance_requirement_counts={blocked_until_remote_audit: 4}`

## 新增 post-run requirements

- `pullback_expected_artifacts_complete`
- `checkpoint_hash_manifest_recorded`
- `gate3_formal_audit_accepts_remote_run`
- `h01_h02_regenerated_from_audited_checkpoint`

这些 requirement 都是远端训练/审计之后的本地验收门。当前全部:

- `status=blocked_until_remote_audit`
- `execution_allowed_now=false`
- `remote_training_ready_now=false`

## 不能替代的东西

- remote stdout 不能替代本地 pullback 文件。
- 只有 checkpoint 或 summary 的 partial pullback 不能替代完整七类产物。
- checkpoint 文件没有 SHA-256 记录不能进入 H01/H02。
- `not_formal` / `candidate` / `smoke` / `preview` audit 不能替代 formal audit。
- no-warm Gate3 audit 不能复用成 obstacle-summary warm-start formal audit。
- paper table preview 不能替代 H02 formal acceptance。

## Safety audit

`remote_packet_safety_audit` 现在检查:

- packet 必须包含 `post_run_acceptance_requirements`。
- 四个 post-run requirement 不能缺项。
- requirement 必须列出 acceptable evidence 和 invalid substitutes。
- post-run requirement 不得 `execution_allowed_now=true`。
- pre-run packet 不得把 post-run requirement 误标为 `satisfied` 或 `complete=true`。

## 验证

```bash
PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_remote_formal_execution_packet.py
```

结果: `3 passed in 0.21s`

```bash
PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py
```

结果: `16 passed in 0.82s`

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

结果: `80 passed in 3.52s`
