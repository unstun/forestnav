---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_f03_gate3_formal_audit.md
---

# Module2 F03.5 Gate #3 Formal Preflight 记录

## 直观结论

F03.5 现在有正式 trial 的运行前预检脚本: `preflight_rl_rs_gate3_formal_trial.py`。它不启动 PPO 训练, 只生成正式 runner 命令、formal audit 命令、参数快照、expected artifacts 和 blockers。这样可以先把“什么才算正式 Gate #3 trial”冻结成机器可读协议, 再把高噪声训练交给后续 experiment-driver 或远端执行。

本次生成了两份项目内 preflight artifact:

- no-warm-start formal trial: `preflight_status=ready`。
- obstacle-summary warm-start formal trial: `preflight_status=blocked`, blocker 是 `warm_start_decision_pending`。

这不关闭 F02.6, 也不 claim Gate #3 通过。

## 实现锚点

- preflight 入口: `2_experiment/forest_n3p/scripts/preflight_rl_rs_gate3_formal_trial.py`。
- CLI 覆盖 output dir、manifest path、seed/device、可选 BC checkpoint、F02.6 warm-start decision、oracle path、正式 train/eval budget: `2_experiment/forest_n3p/scripts/preflight_rl_rs_gate3_formal_trial.py:33-60`。
- manifest 生成主逻辑写入 contract status、protocol、runner/audit 命令、expected artifacts 和 blockers: `2_experiment/forest_n3p/scripts/preflight_rl_rs_gate3_formal_trial.py:64-90`。
- protocol 固定 `smoke=false`, train/eval curriculum 均为 `f03`, eval episodes/min episodes 均为 64, threshold 为 0.8: `2_experiment/forest_n3p/scripts/preflight_rl_rs_gate3_formal_trial.py:94-121`。
- blockers 覆盖 contract 未 approved、oracle 缺失、checkpoint 缺失、warm-start pending、episode 不足、threshold 不足、已有 trial 输出等: `2_experiment/forest_n3p/scripts/preflight_rl_rs_gate3_formal_trial.py:124-180`。
- runner 命令固定调用 `run_rl_rs_gate3_trial.py`, 且不包含 `--smoke`: `2_experiment/forest_n3p/scripts/preflight_rl_rs_gate3_formal_trial.py:197-243`。
- audit 命令固定调用 `audit_rl_rs_gate3_trial.py`, 并传入当前 warm-start decision: `2_experiment/forest_n3p/scripts/preflight_rl_rs_gate3_formal_trial.py:246-263`。

## 测试锚点

- 测试文件: `2_experiment/forest_n3p/tests/test_preflight_rl_rs_gate3_formal_trial.py`。
- no-warm-start preflight 必须 ready, 且 runner command 不含 `--smoke`, train/eval curriculum 为 `f03`, eval episodes/min episodes 为 64: `2_experiment/forest_n3p/tests/test_preflight_rl_rs_gate3_formal_trial.py:9-45`。
- 传入 obstacle-summary BC checkpoint 且 warm-start decision 为 pending 时必须 blocked, blocker 包含 `warm_start_decision_pending`: `2_experiment/forest_n3p/tests/test_preflight_rl_rs_gate3_formal_trial.py:48-76`。

## TDD 记录

RED:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_preflight_rl_rs_gate3_formal_trial.py -q
```

失败原因:

```text
AssertionError: missing Gate #3 formal preflight module: No module named 'forest_n3p.scripts.preflight_rl_rs_gate3_formal_trial'
```

GREEN:

```bash
PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_preflight_rl_rs_gate3_formal_trial.py -q
```

stdout:

```text
2 passed in 0.19s
```

项目内 no-warm-start preflight:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.preflight_rl_rs_gate3_formal_trial \
  --output-dir 0_trials/module2_gate3_formal/gate3_no_warm_formal_v1 \
  --manifest-out 0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/gate3_preflight_manifest.json \
  --seed 20260704 \
  --allow-duplicate-openmp
```

stdout 关键字段:

```text
"contract_status": "approved"
"preflight_status": "ready"
"formal_trial_ready": true
"train_curriculum_preset": "f03"
"eval_curriculum_preset": "f03"
"eval_episodes": 64
```

项目内 obstacle-summary warm-start preflight:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.preflight_rl_rs_gate3_formal_trial \
  --output-dir 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_pending_v1 \
  --manifest-out 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_pending_v1/gate3_preflight_manifest.json \
  --seed 20260704 \
  --allow-duplicate-openmp \
  --bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt \
  --warm-start-decision pending
```

stdout 关键字段:

```text
"preflight_status": "blocked"
"formal_trial_ready": false
"code": "warm_start_decision_pending"
```

产物:

- `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/gate3_preflight_manifest.json`
- `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_pending_v1/gate3_preflight_manifest.json`

## 当前不 claim 的内容

- 不 claim F03.5 Gate #3 正式通过。
- 不 claim PPO 已在 `f03` / RS-failure 分布上收敛。
- 不 claim F02.6 obstacle-summary warm-start 已被 Dr Sun 批准。
- 不启动训练; 训练运行必须走后续 experiment-driver / 远端执行并同步完整产物。
