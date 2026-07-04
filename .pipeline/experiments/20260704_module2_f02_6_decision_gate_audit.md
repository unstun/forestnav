---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 F02.6 Decision Gate Audit

## 直观结论

本轮新增 `build_module2_f02_6_decision_gate_audit.py`, 独立审计 F02.6 人类决策门。

它不替 Dr Sun 批准或驳回。它只检查当前 decision packet、decision record 和 post-F02.6 plan 是否一致, 是否仍然正确卡住训练/预检/claim。

当前真实结果:

- `status=f02_6_decision_gate_pending_clean`
- `audit_issue_count=0`
- `packet_recommendation=approve_obstacle_summary_warm_start`
- `record_status=pending_human_decision`
- `record_decider=null`
- `effective_warm_start_decision=pending`
- `remote_training_allowed=false`
- `local_training_allowed=false`
- `formal_claim_allowed=false`
- `training_allowed_now=false`
- `remote_preflight_allowed_now=false`

这说明 F02.6 当前是“干净地 pending”: 证据包有推荐, 但机器记录没有人类批准, 后续 plan 没有放行训练或 preflight。

## 审计内容

- decision packet 必须保持 `pending_human_decision`, 且 `decision_owner=Dr Sun`。
- packet 推荐分支不能允许 formal claim。
- approved 分支必须指向 `gpu3070ti-relay`, runner 必须包含 obstacle-summary BC checkpoint 和 `--device cuda`。
- rejected 分支必须转向 stronger/full patch-CNN protocol, 不能继续偷跑 obstacle-summary warm-start。
- pending decision record 不得有 decider, 不得允许 remote/local training, 必须保留 `requires_dr_sun_approval`。
- approved decision record 必须由 `Dr Sun` 记录, 且只解锁远端后续路径, 不解锁 paper claim。
- rejected decision record 必须继续阻塞 obstacle-summary warm-start formal training。
- post-F02.6 plan 的 decision status 必须与 record 一致; pending 时 training/preflight 都必须是 false。

## 产物

- `2_experiment/forest_n3p/scripts/build_module2_f02_6_decision_gate_audit.py`
- `2_experiment/forest_n3p/tests/test_module2_f02_6_decision_gate_audit.py`
- `0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.json`
- `0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.md`

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_f02_6_decision_gate_audit.py` -> `6 passed in 0.43s`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_f02_6_decision_gate_audit.py` -> pass
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_decision_gate_audit` -> `status=f02_6_decision_gate_pending_clean`

## 边界

- 本轮没有批准或驳回 F02.6。
- 本轮没有训练。
- 本轮没有运行 remote preflight。
- 本轮没有生成 formal PPO checkpoint。
- 本轮没有放行 formal performance claim。
- audit pass 只表示当前 decision gate 没有错误放行。

