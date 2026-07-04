---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
depends_on:
  - .pipeline/experiments/20260704_module2_f02_6_decision_record_protocol.md
  - .pipeline/experiments/20260704_module2_f03_gpu3070ti_remote_readiness.md
  - .pipeline/experiments/20260704_module2_h01_output_schema_guard.md
---

# Module2 Remote Formal Execution Packet

## 直观结论

本轮补齐了 F02.6 批准后的远端 formal 执行包, 但没有启动训练。

当前生成的 packet 明确写死:

- 训练 host 必须是 `gpu3070ti-relay`。
- 本地训练仍为 `local_training_allowed=false`。
- F02.6 pending 时 `ready_to_run_remote_training=false`。
- 同步命令不使用 `--delete`, 避免清掉远端 `.venv` 或既有 artifact。
- 跑完必须回传 7 类 artifact, 包括 `train/final_model.zip`、`train/training_manifest.json`、`eval/gate3_summary.json` 和 `gate3_formal_audit.json`。
- 只有 formal audit 通过并回传后, 才能用该 checkpoint 重新生成 H01/H02/I02。

## 实现内容

- 新增 `build_module2_remote_formal_execution_packet.py`。
- 新增 `test_module2_remote_formal_execution_packet.py`。
- 生成真实 artifact:
  - `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json`
  - `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.md`

## 当前真实状态

真实 packet 状态:

```text
status=blocked_until_f02_6_decision
ready_to_run_remote_training=false
local_training_allowed=false
blockers=[
  requires_dr_sun_approval,
  f02_6_warm_start_decision_pending,
  missing_module2_rl_rs_checkpoint
]
gpu_alias=gpu3070ti-relay
sync_has_delete=false
run_remote_training.allowed_now=false
expected_artifact_count=7
H01 required_output_schema=frozen_for_module2_v1
```

## 验证

- RED: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_remote_formal_execution_packet.py` -> missing builder, 3 failed。
- GREEN: same test -> `3 passed in 0.22s`。
- Artifact audit: pending packet correctly blocks remote training, all remote execution commands start with `ssh gpu3070ti-relay`, sync command has no `--delete`, H01 schema guard is present。
- Targeted regression: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_remote_formal_execution_packet.py 2_experiment/forest_n3p/tests/test_module2_f02_6_decision_record.py 2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py 2_experiment/forest_n3p/tests/test_module2_h02_smoke_preflight.py` -> `13 passed in 0.72s`。
- Full regression: `KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests` -> `115 passed in 12.38s`。
- Syntax: `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_remote_formal_execution_packet.py` passed。

## 边界

- 未本地训练。
- 未远端训练。
- 未批准 F02.6。
- 未生成正式 PPO checkpoint。
- 未解除 H01/H02 formal blockers。
- 此 packet 是执行协议, 不是训练结果, 也不是论文性能 claim。
