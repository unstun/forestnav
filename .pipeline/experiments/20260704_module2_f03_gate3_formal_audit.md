---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_f03_gate3_trial_runner.md
---

# Module2 F03.5 Gate #3 Formal Audit 记录

## 直观结论

F03.5 现在不只会跑 train/eval, 还会审计“这个结果能不能被当作正式 Gate #3 证据”。新增 `audit_rl_rs_gate3_trial.py` 读取 runner 的 `gate3_trial_manifest.json`, 检查 artifact 完整性、是否 smoke、episode 数是否达到正式下限、train/eval curriculum 是否为 `f03`, 以及 F02.6 warm-start 决策是否仍 pending。

当前 warm-start runner smoke 的 evaluator summary 里虽然有 `decision=pass` 和 `terminal_rs_success_rate=1.0`, 但 formal audit 明确输出 `formal_decision=not_formal`。这一步的意义是把“smoke pass 不能写成正式 Gate pass”从口头纪律变成机器可读 artifact。

## 实现锚点

- audit 入口: `2_experiment/forest_n3p/scripts/audit_rl_rs_gate3_trial.py`。
- CLI 覆盖 trial dir、输出路径、正式 episode 下限、success threshold、train/eval curriculum 要求和 F02.6 warm-start 决策状态: `2_experiment/forest_n3p/scripts/audit_rl_rs_gate3_trial.py:38-52`。
- 主审计逻辑读取 trial manifest、train summary、eval summary, 并聚合 blockers/warnings: `2_experiment/forest_n3p/scripts/audit_rl_rs_gate3_trial.py:55-174`。
- artifact 完整性检查覆盖 model、train summary、training manifest、eval summary、eval CSV: `2_experiment/forest_n3p/scripts/audit_rl_rs_gate3_trial.py:177-194`。
- formal 判定规则: 只在无 blockers 时允许 formal `pass` 或 `fail`; 否则固定 `not_formal`: `2_experiment/forest_n3p/scripts/audit_rl_rs_gate3_trial.py:146-160`。

## 测试锚点

- 测试文件: `2_experiment/forest_n3p/tests/test_audit_rl_rs_gate3_trial.py`。
- 真实 smoke artifact 审计必须输出 `not_formal`, 并包含 smoke、episode 不足、非 f03 curriculum、warm-start pending 等 blockers: `2_experiment/forest_n3p/tests/test_audit_rl_rs_gate3_trial.py:9-34`。
- 合成 non-smoke/f03/64-episode manifest 必须能被审计为 formal pass, 防止审计器只会否定: `2_experiment/forest_n3p/tests/test_audit_rl_rs_gate3_trial.py:40-60`。

## TDD 记录

RED:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_audit_rl_rs_gate3_trial.py -q
```

失败原因:

```text
AssertionError: missing Gate #3 formal audit module: No module named 'forest_n3p.scripts.audit_rl_rs_gate3_trial'
```

GREEN:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_audit_rl_rs_gate3_trial.py -q
```

stdout:

```text
2 passed in 0.17s
```

项目内 smoke audit:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.audit_rl_rs_gate3_trial \
  --trial-dir 0_trials/module2_ppo_smoke/f03_gate3_trial_runner_smoke \
  --output 0_trials/module2_ppo_smoke/f03_gate3_trial_runner_smoke/gate3_formal_audit.json
```

stdout 关键字段:

```text
"formal_decision": "not_formal"
"formal_claim_allowed": false
"evaluator_decision": "pass"
"terminal_rs_success_rate": 1.0
```

formal blockers:

```text
smoke_trial
train_curriculum_not_f03
eval_curriculum_not_f03
insufficient_eval_episodes
warm_start_decision_pending
```

产物:

- `0_trials/module2_ppo_smoke/f03_gate3_trial_runner_smoke/gate3_formal_audit.json`

## 当前不 claim 的内容

- 不 claim F03.5 Gate #3 正式通过。
- 不 claim PPO 在小规模单一密度 RS-failure 分布上收敛。
- 不 claim F02.6 obstacle-summary warm-start 已被 Dr Sun 批准。
- 不 claim planner integration 已完成。
