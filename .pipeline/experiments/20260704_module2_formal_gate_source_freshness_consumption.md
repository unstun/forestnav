---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
---

# Module2 Formal Gate Consumes Source Freshness

## 直观结论

本轮把 `0_trials/module2_source_freshness_audit/source_freshness_audit.json` 接入 formal gate gap audit。

之前 source freshness audit 是旁路记录: 它能告诉我们哪些 gate artifact 的 `source_head` 已经是 historical/dirty, 但 formal gate 本身还不会消费这个风险。

现在 `build_module2_formal_gate_gap_audit.py` 会默认读取 source freshness audit, 并把以下情况变成 formal gate blocker:

- source freshness audit 缺失;
- source freshness audit 自己声称跑过 training 或 remote preflight;
- source freshness audit 允许 local training 或 formal claim;
- source freshness audit 报告 `regeneration_required_before_remote_formal_execution=true`。

当前真实状态仍是 `blocked_formal_gate_gaps_open`。新增 blocker 是 `source_freshness_regeneration_required`; 它会阻塞 `remote_preflight`, `gate3_remote_training`, `gate3_remote_audit_pullback`, `h01_h02_regeneration`, `claim_safety_final_gate`。

## 关键边界

`source_freshness_regeneration_required` 不是算法失败、不是 PPO 训练失败、不是 formal result。它只表示 F02.6 关闭后、approved remote preflight / H01-H02 / formal claim gate 前, 必须按 source freshness audit 的 target list 重生成旧 gate artifact。

本轮没有训练、没有运行 approved remote preflight、没有关闭 F02.6、没有放行 formal performance claim、没有写结果性论文材料。

## 产物

- `2_experiment/forest_n3p/scripts/build_module2_formal_gate_gap_audit.py`
- `2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py`
- `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json`
- `0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.md`

## 当前 formal gate 读数

- `source_freshness.status=source_freshness_risks_recorded_gate_still_blocked`
- `source_freshness.regeneration_required_before_remote_formal_execution=true`
- `source_freshness.risk_counts={historical_dirty: 6, historical_clean: 2}`
- `source_freshness.ordered_regeneration_target_count=8`
- `remote_preflight.status=blocked`
- `gate3_remote_training.status=blocked`
- `formal_performance_claim_allowed=false`

## 验证

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py` -> `10 passed in 0.56s`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/scripts/build_module2_source_freshness_audit.py` -> pass
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_gap_audit` -> `status=blocked_formal_gate_gaps_open`

