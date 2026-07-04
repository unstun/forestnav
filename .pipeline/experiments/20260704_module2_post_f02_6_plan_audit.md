---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Post-F02.6 Plan Audit

## 直观结论

本轮新增 `build_module2_post_f02_6_plan_audit.py`, 对 post-F02.6 regeneration plan 做独立审计。

上一轮的 plan 负责把 F02.6 之后的阶段排好序。本轮 audit 负责检查这个 plan 有没有漂移成危险状态, 例如:

- 顶层 artifact 是否错误声明会执行命令、训练、预检或允许 claim;
- stage 顺序是否缺失或乱序;
- F02.6 pending 时是否错误放行 training/preflight;
- source freshness 的 target count 是否与 plan 对齐;
- training stage 是否保持 `gpu3070ti-relay` remote-only;
- ready training stage 是否必须通过 `ssh gpu3070ti-relay`。

当前真实 audit 结果:

- `status=post_f02_6_plan_audit_passed`
- `audit_issue_count=0`
- `plan_status=blocked_until_f02_6_decision`
- `training_allowed_now=false`
- `remote_preflight_allowed_now=false`
- `ready_stage_ids=[f02_6_decision_record]`

这个 pass 只说明计划正确保持 blocked, 不是训练许可。

## 产物

- `2_experiment/forest_n3p/scripts/build_module2_post_f02_6_plan_audit.py`
- `2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py`
- `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
- `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.md`

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py` -> `5 passed in 0.29s`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_post_f02_6_plan_audit.py` -> pass
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_plan_audit` -> `status=post_f02_6_plan_audit_passed`

## 边界

- 本轮没有训练。
- 本轮没有运行 remote preflight。
- 本轮没有关闭 F02.6。
- 本轮没有生成 formal PPO checkpoint。
- 本轮没有放行 formal performance claim。
- audit pass 不能被解释成实验结果或论文结果。

