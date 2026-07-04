---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Post-F02.6 Plan Consumes Status Report

## 直观结论

本轮只加固 PPO 替代 RS formal gate 的计划审计链, 不执行训练、不执行远端 preflight、不同步远端、不写结果性论文材料。

`post_f02_6_plan_audit` 现在直接读取 `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`。这样 ordered plan audit 不能只看 missing-artifacts 和 closure checklist, 还必须看到最终 status report 的当前阻塞状态。

## 改动

- `build_module2_post_f02_6_plan_audit.py` 新增默认输入 `formal_gate_status_report`。
- `post_f02_6_plan_audit.json` 新增 `inputs.formal_gate_status_report` 和 `status_report_summary`。
- audit 新增 status report safety checks:
  - status report 不得执行命令。
  - status report 不得运行训练。
  - status report 不得运行远端 preflight。
  - status report 不得允许本地训练。
  - status report 不得绕过 formal claim gate。
  - status report 有 input safety issue 时 audit 失败。
  - claim-gate stage ready 但 status report 仍 blocked 时 audit 失败。

## 当前状态

- `post_f02_6_plan_audit.status = post_f02_6_plan_audit_passed`
- `post_f02_6_plan_audit.audit_issue_count = 0`
- `status_report_summary.status = formal_gate_status_blocked`
- `status_report_summary.formal_claim_allowed_now = false`
- `status_report_summary.local_training_allowed_now = false`
- `status_report_summary.next_blocked_lane_id = decision`
- `current_blocking_summary.training_allowed_now = false`
- `current_blocking_summary.remote_preflight_allowed_now = false`

这个 pass 的含义只是: 当前 ordered plan 正确保持 blocked。它不是训练许可, 不是远端 preflight 许可, 也不是论文 formal result claim。

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py`
  - 结果: 12 passed。
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_post_f02_6_plan_audit.py`
  - 结果: 通过。
- 重新生成:
  - `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_regeneration_plan`
  - `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_plan_audit`
  - `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_source_freshness_audit`

## 剩余 formal gate 缺口

下一步仍不是写结果性论文材料, 而是回到 formal gate:

- F02.6 decision record 仍需 Dr Sun 关闭。
- F02.6 关闭后才允许 source-fresh preflight target regeneration。
- approved remote preflight 仍缺。
- `gpu3070ti-relay` 上的 formal PPO training 仍缺。
- formal checkpoint、training manifest、train summary 仍缺。
- Gate3 eval rows、summary、formal audit、pullback hash 仍缺。
- H01/H02 formal acceptance 仍缺。
- claim safety / paper readiness final regeneration 仍 blocked。
