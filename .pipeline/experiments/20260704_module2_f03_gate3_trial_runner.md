---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_f03_ppo_training_entry.md
  - .pipeline/experiments/20260704_module2_f03_gate3_evaluator.md
---

# Module2 F03.5 Gate #3 Trial Runner 记录

## 直观结论

F03.5 现在有一个可审计的一条命令 trial runner: `run_rl_rs_gate3_trial.py`。它串起三件事: 训练 PPO, 加载训练出的 SB3 model 做 deterministic Gate #3 eval, 最后写顶层 `gate3_trial_manifest.json`。

这不是正式 Gate #3 结果。当前 smoke 是 open-connector 极小训练/评估, 只证明 train -> eval -> manifest 这条链路真实可跑。顶层 manifest 显式写 `formal_gate_claim=false`, 避免把 smoke 中的 `decision=pass` 误当正式 Gate 判定。

## 实现锚点

- runner 入口: `2_experiment/forest_n3p/scripts/run_rl_rs_gate3_trial.py`。
- 主流程: parse args -> smoke override -> train -> eval -> manifest: `2_experiment/forest_n3p/scripts/run_rl_rs_gate3_trial.py:19-46`。
- CLI 覆盖输出目录、seed/device、可选 BC warm-start、train 超参、eval episodes/threshold 和 env/observation config: `2_experiment/forest_n3p/scripts/run_rl_rs_gate3_trial.py:49-93`。
- smoke override 固定为 tiny open-connector train/eval: `2_experiment/forest_n3p/scripts/run_rl_rs_gate3_trial.py:95-114`。
- train argv 编排复用 `train_rl_rs_ppo.py`, 保留 `--bc-checkpoint` 可选路径: `2_experiment/forest_n3p/scripts/run_rl_rs_gate3_trial.py:117-188`。
- eval argv 编排复用 `eval_rl_rs_gate3.py`: `2_experiment/forest_n3p/scripts/run_rl_rs_gate3_trial.py:191-242`。
- 顶层 manifest 汇总 train/eval config、artifact 相对路径、source hash、Gate evaluator decision, 并固定 `formal_gate_claim=false`: `2_experiment/forest_n3p/scripts/run_rl_rs_gate3_trial.py:238-272`。

## 测试锚点

- 测试文件: `2_experiment/forest_n3p/tests/test_run_rl_rs_gate3_trial.py`。
- 测试覆盖真实 runner smoke, 断言 `train/final_model.zip`, `eval/gate3_summary.json`, `gate3_trial_manifest.json`, `formal_gate_claim=false`, `warm_start_status=not_applied_f02_6_pending`: `2_experiment/forest_n3p/tests/test_run_rl_rs_gate3_trial.py:8-41`。

## TDD 记录

RED:

```bash
KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_run_rl_rs_gate3_trial.py -q
```

失败原因:

```text
AssertionError: missing Gate #3 trial runner module: No module named 'forest_n3p.scripts.run_rl_rs_gate3_trial'
```

GREEN:

```bash
KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_run_rl_rs_gate3_trial.py -q
```

stdout:

```text
1 passed in 1.49s
```

局部验证:

```bash
python -m py_compile \
  2_experiment/forest_n3p/scripts/run_rl_rs_gate3_trial.py \
  2_experiment/forest_n3p/tests/test_run_rl_rs_gate3_trial.py

KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_train_rl_rs_ppo.py \
  2_experiment/forest_n3p/tests/test_eval_rl_rs_gate3.py \
  2_experiment/forest_n3p/tests/test_run_rl_rs_gate3_trial.py -q
```

stdout:

```text
5 passed in 2.03s
```

全量小测试:

```bash
KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests -q
```

stdout:

```text
57 passed in 7.41s
```

项目内 warm-start runner smoke:

```bash
KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_rl_rs_gate3_trial \
  --allow-duplicate-openmp \
  --smoke \
  --bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt \
  --output-dir 0_trials/module2_ppo_smoke/f03_gate3_trial_runner_smoke \
  --seed 20260704
```

stdout 关键字段:

```text
"warm_start_status": "applied_obstacle_summary_bc"
"formal_gate_claim": false
"gate3_decision": "pass"
"terminal_rs_success_rate": 1.0
```

产物:

- `0_trials/module2_ppo_smoke/f03_gate3_trial_runner_smoke/train/final_model.zip`
- `0_trials/module2_ppo_smoke/f03_gate3_trial_runner_smoke/train/summary.json`
- `0_trials/module2_ppo_smoke/f03_gate3_trial_runner_smoke/train/training_manifest.json`
- `0_trials/module2_ppo_smoke/f03_gate3_trial_runner_smoke/eval/gate3_eval_episodes.csv`
- `0_trials/module2_ppo_smoke/f03_gate3_trial_runner_smoke/eval/gate3_summary.json`
- `0_trials/module2_ppo_smoke/f03_gate3_trial_runner_smoke/gate3_trial_manifest.json`

## 当前不 claim 的内容

- 不 claim F03.5 Gate #3 正式通过。
- 不 claim PPO 在小规模单一密度 RS-failure 分布上收敛。
- 不 claim F02.6 warm-start 决策已关闭; `--bc-checkpoint` 只是候选路径可审计。
- 不 claim planner integration 已完成。
