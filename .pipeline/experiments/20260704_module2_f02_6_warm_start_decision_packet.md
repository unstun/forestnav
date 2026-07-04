---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_f02_formal_v2_mlp_bc_baselines.md
  - .pipeline/experiments/20260704_module2_f03_gate3_no_warm_formal_trial.md
  - .pipeline/experiments/20260704_module2_f03_gpu3070ti_remote_readiness.md
---

# F02.6 Warm-Start Decision Packet

## 直观结论

F02.6 现在不是证据不足, 而是需要 Dr Sun 明确拍板。

本次新增的决策包把 no-warm 失败、BC 候选排名、远端 3070Ti 可执行状态和 warm-start 阻塞原因放进同一个机器可读 JSON 与人读 Markdown。推荐是 `approve_obstacle_summary_warm_start`, 但 status 仍是 `pending_human_decision`; 这不能被当作批准、训练结果或论文 claim。

## 产物

- JSON: `0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json`
- Markdown: `0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.md`
- 生成器: `2_experiment/forest_n3p/scripts/build_module2_f02_6_warm_start_decision_packet.py`
- 回归测试: `2_experiment/forest_n3p/tests/test_module2_f02_6_warm_start_decision_packet.py`

## 证据锚点

- No-warm formal Gate #3: `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/gate3_formal_audit.json`, `formal_decision=fail`, `formal_claim_allowed=true`, `formal_blockers=[]`。
- No-warm eval summary: `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/eval/gate3_summary.json`, terminal-RS-success `29/64=0.453125`, collision rate `0.359375`, truncation rate `0.1875`。
- Obstacle-summary BC formal-v2: `2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/summary.json`, terminal-RS-success `67/258`。
- Obstacle-summary same bounded rows: `2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/eval_patch_bounded_rows.json`, terminal-RS-success `101/242`。
- Patch+scalar CNN bounded pilot: `2_experiment/forest_n3p/models/module2_rl_rs_bc_patch_formal_v2_pilot/summary.json`, terminal-RS-success `63/242`。
- Remote no-warm preflight: `0_trials/module2_remote_preflight/gate3_no_warm_remote_v1/gate3_preflight_manifest.json`, `formal_trial_ready=true`。
- Remote obstacle-summary warm-start preflight: `0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_pending_remote_v1/gate3_preflight_manifest.json`, `formal_trial_ready=false`, blocker `warm_start_decision_pending`。
- Remote warm-start CUDA smoke: `0_trials/module2_remote_smoke/gate3_warm_start_cuda_smoke/gate3_formal_audit.json`, `formal_decision=not_formal`, blockers include `smoke_trial` and `warm_start_decision_pending`。

## 推荐与边界

推荐: 若进入下一次 formal PPO, 使用 obstacle-summary BC checkpoint 作为 warm-start initializer。

理由:

- No-warm PPO 已经在正式 64 episode Gate #3 下失败, 不是 smoke 失败。
- 当前 formal-v2 证据里 obstacle-summary 是最强 practical candidate。
- Patch+scalar CNN bounded pilot 在同一 bounded validation rows 上没有超过 obstacle-summary。
- `gpu3070ti-relay` 已完成远端执行链路预检, 但 warm-start formal preflight 正确阻塞在 F02.6 人类决策。

边界:

- 本记录不关闭 F02.6。
- 本记录不批准 warm-start。
- 本记录不启动本地训练。
- 本记录不把远端 CUDA smoke 当正式 Gate #3 证据。
- 本记录不生成可填补 H01 `missing_module2_rl_rs_checkpoint` 的正式 PPO checkpoint。

## 验证

- RED: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_f02_6_warm_start_decision_packet.py` 先因缺少生成器失败。
- GREEN: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_f02_6_warm_start_decision_packet.py` -> `1 passed`。
- Adjacent: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_f02_6_warm_start_decision_packet.py 2_experiment/forest_n3p/tests/test_preflight_rl_rs_gate3_formal_trial.py 2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py` -> `6 passed`。
- Syntax: `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_f02_6_warm_start_decision_packet.py`。

## 下一步

如果 Dr Sun 批准 `approve_obstacle_summary_warm_start`, 下一步 formal run 必须在 `gpu3070ti-relay` 上执行决策包中的 CUDA runner command, 不在本地训练。
