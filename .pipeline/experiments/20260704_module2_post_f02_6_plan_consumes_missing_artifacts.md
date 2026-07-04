---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Post-F02.6 Plan Consumes Missing Artifacts

## 直观结论

本轮把 `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json` 接入 `build_module2_post_f02_6_plan_audit.py`。

之前 post-F02.6 plan audit 会检查 plan 的非执行边界、stage 顺序、F02.6 pending 阻塞、source freshness 对齐和 gpu3070ti-only training host, 但不会读取 formal gate missing-artifacts inventory。

现在 post-plan audit 默认读取 inventory, 并检查:

- inventory 是否存在;
- inventory 是否错误声称会执行命令、训练或 remote preflight;
- inventory 是否错误允许 local training 或 formal claim;
- inventory 是否有 audit issues;
- inventory 仍 open 时, `regenerate_claim_gate_artifacts` 不能处于 ready。

当前真实结果仍是:

- `status=post_f02_6_plan_audit_passed`
- `audit_issue_count=0`
- `training_allowed_now=false`
- `remote_preflight_allowed_now=false`
- `missing_artifacts_summary.status=formal_gate_missing_artifacts_open`
- `missing_artifacts_summary.all_required_evidence_present=false`

这个 pass 只说明 ordered plan 正确保持 blocked, 不是训练许可, 也不是 formal claim。

## 产物

- `2_experiment/forest_n3p/scripts/build_module2_post_f02_6_plan_audit.py`
- `2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py`
- `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
- `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.md`

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py` -> `8 passed in 0.42s`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_post_f02_6_plan_audit.py` -> pass
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_plan_audit` -> `status=post_f02_6_plan_audit_passed`

## 边界

- 本轮没有训练。
- 本轮没有运行 remote preflight。
- 本轮没有执行 sync 或 pullback。
- 本轮没有关闭 F02.6。
- 本轮没有生成 formal PPO checkpoint。
- 本轮没有放行 formal performance claim。
- 这个变更只让 post-F02.6 plan audit 消费缺失产物清单, 不是论文结果材料。
