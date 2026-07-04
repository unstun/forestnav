---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_f02_6_warm_start_decision_packet.md
  - .pipeline/experiments/20260704_module2_h01_evaluation_manifest.md
---

# H01 F02.6 Decision Packet Guard

## 直观结论

H01 评测协议现在不会只相信一个命令行字符串。

之前 `build_module2_evaluation_manifest.py` 只有 `--warm-start-decision approved_obstacle_summary` 这种手动字符串。如果未来有人误传这个参数, manifest 可能看起来像 F02.6 已经批准, 但实际没有审批证据。本次改动让 H01 manifest 可读取 F02.6 decision packet, 并以 packet 的实际 status 计算 effective decision。

当前 packet 仍是 `pending_human_decision`, 所以 H01 仍 blocked。

## 改动

- `Module2EvaluationManifestConfig` 新增 `warm_start_decision_packet_path`。
- CLI 新增 `--warm-start-decision-packet`。
- manifest 新增 `f02_6_decision_packet` 字段, 记录 packet path/status/requested decision/effective decision/recommendation/blockers。
- 当 packet status 为 `pending_human_decision` 时, effective decision 强制为 `pending`。
- PPO 相关方法 blocker 新增 `f02_6_decision_packet_pending`。
- 全局 blocker 新增 `f02_6_decision_packet_pending`。

## 当前 H01 产物

- Manifest: `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`
- Markdown: `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.md`
- Status: `blocked_pending_decisions`
- Packet status: `pending_human_decision`
- Effective warm-start decision: `pending`
- Blockers: `f02_6_warm_start_decision_pending`, `f02_6_decision_packet_pending`, `missing_module2_rl_rs_checkpoint`

## 验证

- RED: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py::test_module2_manifest_cannot_bypass_pending_f02_6_packet_with_cli_decision` 先失败于缺少 `warm_start_decision_packet_path`。
- GREEN: 同一测试转为 `1 passed`。
- Manifest tests: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py` -> `4 passed`。
- Adjacent: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_evaluation_manifest.py 2_experiment/forest_n3p/tests/test_module2_f02_6_warm_start_decision_packet.py` -> `5 passed`。
- Syntax: `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py`。

## 边界

- 本改动不批准 F02.6。
- 本改动不训练 PPO。
- 本改动不产生可用于 H01 formal evaluation 的 PPO checkpoint。
- 若 Dr Sun 后续批准 obstacle-summary warm-start, 仍需要更新/生成 approved decision packet 后再解除该 blocker。
