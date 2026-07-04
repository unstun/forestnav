---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Formal Gate Consumes Missing Artifacts

## 直观结论

本轮把 `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json` 接入 `build_module2_formal_gate_gap_audit.py`。

之前 missing-artifacts audit 是旁路 inventory: 它能列出 formal gate 还缺哪些训练、评测、验收和 claim-gate evidence, 但 formal gate gap audit 本身还不会消费这个 inventory。

现在 formal gate gap audit 默认读取 missing-artifacts inventory, 并把以下情况变成 formal gate acceptance blocker:

- inventory artifact 缺失;
- inventory 声称会执行命令、训练或 remote preflight;
- inventory 允许 local training 或 formal claim;
- inventory 自己有 audit issues;
- inventory 报告 `all_required_evidence_present=false`。

当前真实状态仍是 `blocked_formal_gate_gaps_open`。新增 blocker 是 `formal_gate_missing_artifacts_open`; 它出现在 acceptance gaps 和 `claim_safety_final_gate.blocked_by` 中。它不会把训练输出缺失误当成 `gate3_remote_training` 的前置条件。

## 当前读数

- `missing_artifacts_inventory.status=formal_gate_missing_artifacts_open`
- `missing_artifacts_inventory.all_required_evidence_present=false`
- `missing_artifacts_inventory.audit_issue_count=0`
- `missing_artifacts_inventory.runs_training=false`
- `missing_artifacts_inventory.runs_remote_preflight=false`
- `missing_artifacts_inventory.local_training_allowed=false`
- `missing_artifacts_inventory.formal_claim_allowed=false`
- `missing_artifacts_inventory.missing_counts_by_category={decision:1, regeneration:8, gate_sequence:7, training:3, evaluation:2, acceptance:3, evaluation_acceptance:2, claim_gate:3}`
- `claim_safety_final_gate.blocked_by` now includes `formal_gate_missing_artifacts_open`

## 产物

- `2_experiment/forest_n3p/scripts/build_module2_formal_gate_gap_audit.py`
- `2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py`
- `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json`
- `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.md`

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_missing_artifacts_audit.py 2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py 2_experiment/forest_n3p/tests/test_module2_h02_formal_acceptance.py` -> `21 passed in 1.02s`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_formal_gate_gap_audit.py` -> pass
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_gap_audit` -> `status=blocked_formal_gate_gaps_open`

## 边界

- 本轮没有训练。
- 本轮没有运行 remote preflight。
- 本轮没有执行 sync 或 pullback。
- 本轮没有关闭 F02.6。
- 本轮没有生成 formal PPO checkpoint。
- 本轮没有放行 formal performance claim。
- 这个变更只让 formal gate 消费缺失产物清单, 不是论文结果材料。
