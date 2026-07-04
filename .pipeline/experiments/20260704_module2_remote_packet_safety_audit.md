---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Remote Packet Safety Audit

## 直观结论

本轮新增 `build_module2_remote_packet_safety_audit.py`, 独立审计 remote formal execution packet。

它不执行 sync、ssh、preflight、training、audit 或 pullback。它只检查 remote packet 有没有保持安全边界, 防止后续 packet 漂移成危险执行协议。

当前真实结果:

- `status=remote_packet_safety_audit_passed`
- `audit_issue_count=0`
- `packet_status=blocked_until_f02_6_decision`
- `ready_to_run_remote_training=false`
- `gpu_alias=gpu3070ti-relay`
- `training_host_required=gpu3070ti-relay`
- `sync_allowed_now=true`
- `remote_preflight_allowed_now=false`
- `remote_training_allowed_now=false`
- `remote_audit_allowed_now=false`
- `pullback_artifact_count=7`
- `hash_manifest_required=true`

这个 pass 只说明 remote packet 安全地保持 blocked, 不是训练许可。

## 审计内容

- remote packet 顶层不能允许 local training 或 formal claim。
- F02.6 pending 时 `ready_to_run_remote_training` 必须是 false。
- `gpu_alias` 和 `training_host_required` 必须是 `gpu3070ti-relay`。
- sync command 不能包含 `--delete`, 且必须排除 `.git`, `.venv*`, `__pycache__`, `.pytest_cache`, `1_survey`。
- remote training command 必须通过 `ssh gpu3070ti-relay`, 包含 `run_rl_rs_gate3_trial`, `--device cuda`, `--bc-checkpoint`, `--eval-episodes 64`, `--eval-min-episodes 64`, `--eval-success-threshold 0.8`。
- remote audit command 必须通过 `ssh gpu3070ti-relay`, 包含 `audit_rl_rs_gate3_trial` 和 `--warm-start-decision approved_obstacle_summary`。
- pullback 必须包含 7 类 artifact, 必须来自 `gpu3070ti-relay:~/ForestNav/`, 且不能带 `--delete`。
- downstream 必须要求 H01/H02/table 再生成, 且 formal claim 需要 audit pass、checkpoint hash、H01 ready、H02 all-method formal outputs。

## 产物

- `2_experiment/forest_n3p/scripts/build_module2_remote_packet_safety_audit.py`
- `2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py`
- `0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`
- `0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.md`

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py` -> `5 passed in 0.29s`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_remote_packet_safety_audit.py` -> pass
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_remote_packet_safety_audit` -> `status=remote_packet_safety_audit_passed`

## 边界

- 本轮没有训练。
- 本轮没有运行 remote preflight。
- 本轮没有执行 sync 或 pullback。
- 本轮没有关闭 F02.6。
- 本轮没有生成 formal PPO checkpoint。
- 本轮没有放行 formal performance claim。
- audit pass 不能被解释成实验结果或论文结果。
