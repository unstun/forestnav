---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Formal Gate Consumes gpu3070ti Readiness

## 直观结论

本轮把 `gpu3070ti-relay` 只读 readiness refresh 接入 formal gate gap audit。

之前 readiness refresh 是独立记录；现在 `build_module2_formal_gate_gap_audit.py` 会默认读取 `0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.json`，并检查它是否满足以下边界:

- `runs_training=false`
- `runs_remote_preflight=false`
- `local_training_allowed=false`
- `formal_claim_allowed=false`
- `remote_training_resource=gpu3070ti-relay`
- oracle parquet 本地/远端 match
- obstacle-summary BC checkpoint 本地/远端 match

当前 readiness refresh 通过这些检查，因此不会新增 remote-readiness blocker。Formal gate 仍保持 `blocked_formal_gate_gaps_open`，原因仍是 F02.6 pending、remote packet not ready、缺 formal PPO checkpoint / H02 formal outputs / pullback artifacts。

## 产物

- `2_experiment/forest_n3p/scripts/build_module2_formal_gate_gap_audit.py`
- `2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py`
- `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json`
- `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.md`

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py` -> `5 passed in 0.26s`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_formal_gate_gap_audit.py` -> pass
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_gap_audit` -> `status=blocked_formal_gate_gaps_open`

## 边界

- 本轮没有训练。
- 本轮没有运行 remote preflight。
- 本轮没有关闭 F02.6。
- 本轮没有放行 formal performance claim。
- 本轮只是让 formal gate 机器台账消费 readiness refresh，防止后续批准后忽略远端资源漂移。
