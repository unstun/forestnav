---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_f03_obstacle_summary_warm_start.md
---

# Module2 F03.5 Gate #3 Evaluator 记录

## 直观结论

F03.5 现在有独立 deterministic evaluation / gate 判定脚本: `eval_rl_rs_gate3.py`。它不是读训练过程中的 reward 曲线, 而是加载 SB3 model zip, 重新跑指定 curriculum 的 deterministic episodes, 写 `gate3_eval_episodes.csv`, 再按预注册规则输出 `gate3_summary.json`。

这一步仍不 claim Gate #3 已通过。当前项目内 smoke 使用 open-connector 4 episodes, 只验证 evaluator 和 warm-start checkpoint 可加载、可运行、可出判定文件；正式 Gate #3 仍需按小规模单一密度试点预算运行。

## 实现锚点

- evaluator 入口: `2_experiment/forest_n3p/scripts/eval_rl_rs_gate3.py`。
- 加载 SB3 model, 逐 episode deterministic rollout, 写 episode CSV: `2_experiment/forest_n3p/scripts/eval_rl_rs_gate3.py:26-52`。
- CLI 覆盖 model/output/curriculum/episodes/threshold/env config: `2_experiment/forest_n3p/scripts/eval_rl_rs_gate3.py:55-77`。
- eval env 构造复用 RL-RS Gym env + episode logging: `2_experiment/forest_n3p/scripts/eval_rl_rs_gate3.py:86-115`。
- gate summary 按 `episodes >= min_episodes` 且 `terminal_rs_success_rate >= success_threshold` 判定 pass/fail: `2_experiment/forest_n3p/scripts/eval_rl_rs_gate3.py:125-177`。
- warm-start model 可序列化 policy: `2_experiment/forest_n3p/rl_rs/sb3_policy.py:11-35`。
- `train_rl_rs_ppo.py` 在 `--bc-checkpoint` 时使用 `RlRsMultiInputPolicy`, 持久化 feature normalization 到 SB3 policy kwargs: `2_experiment/forest_n3p/scripts/train_rl_rs_ppo.py:156-214`, `2_experiment/forest_n3p/scripts/train_rl_rs_ppo.py:217-305`。

## 测试锚点

- Gate #3 evaluator smoke 测试: `2_experiment/forest_n3p/tests/test_eval_rl_rs_gate3.py`。
- 训练 smoke model 后加载评估, 写 `gate3_summary.json` 和 eval CSV: `2_experiment/forest_n3p/tests/test_eval_rl_rs_gate3.py:11-63`。
- warm-start save/load roundtrip 行为一致性: `2_experiment/forest_n3p/tests/test_train_rl_rs_ppo.py` 中 warm-start roundtrip 测试。

## 发现并修复的问题

真实项目内 warm-start model 第一次被 evaluator 加载时失败:

```text
RuntimeError: Error(s) in loading state_dict for MultiInputActorCriticPolicy:
  Missing key(s) in state_dict: "action_net.weight", "action_net.bias".
  Unexpected key(s) in state_dict: "action_net.linear.weight", "action_net.linear.bias".
```

原因: 之前是在 PPO model 创建后手动替换 `action_net` 为 `TanhLinearActionHead`; SB3 保存时记录的是替换后的 state dict, 但加载时仍按默认 `MultiInputActorCriticPolicy` 重建 `nn.Linear action_net`。

修复:

1. 增加 `RlRsMultiInputPolicy`, 在 policy `_build()` 阶段创建可序列化的 `TanhLinearActionHead`。
2. warm-start 训练入口在 `--bc-checkpoint` 时使用该 policy。
3. 将 BC `feature_mean/std` 写入 `policy_kwargs.features_extractor_kwargs`, 避免 reload 后 normalization 丢失。
4. 测试增加 save/load roundtrip: reload 后 deterministic action 仍等于原 BC normalized action。

## 验证记录

RED:

```bash
KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_eval_rl_rs_gate3.py -q
```

失败原因:

```text
ModuleNotFoundError: No module named 'forest_n3p.scripts.eval_rl_rs_gate3'
```

GREEN:

```bash
KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_eval_rl_rs_gate3.py -q
```

stdout:

```text
1 passed in 1.44s
```

综合验证:

```bash
KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_eval_rl_rs_gate3.py \
  2_experiment/forest_n3p/tests/test_train_rl_rs_ppo.py -q

KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests -q
```

stdout:

```text
4 passed in 1.88s
56 passed in 7.28s
```

真实 eval smoke:

```bash
KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment python -m forest_n3p.scripts.eval_rl_rs_gate3 \
  --allow-duplicate-openmp \
  --model 0_trials/module2_ppo_smoke/f03_warm_start_entry_smoke/final_model.zip \
  --output-dir 0_trials/module2_ppo_smoke/f03_gate3_eval_entry_smoke \
  --curriculum-preset open \
  --episodes 4 \
  --min-episodes 4 \
  --success-threshold 0.8 \
  --seed 20260704 \
  --obs-patch-size-m 0.4 \
  --obs-patch-cells 5 \
  --max-steps 4
```

stdout 关键字段:

```text
"decision": "pass"
"episodes": 4
"terminal_rs_success": 4
"terminal_rs_success_rate": 1.0
"model": "0_trials/module2_ppo_smoke/f03_warm_start_entry_smoke/final_model.zip"
```

产物:

- `0_trials/module2_ppo_smoke/f03_gate3_eval_entry_smoke/gate3_eval_episodes.csv`
- `0_trials/module2_ppo_smoke/f03_gate3_eval_entry_smoke/gate3_summary.json`

## 当前不 claim 的内容

- 不 claim F03.5 Gate #3 正式通过。
- 不 claim PPO 在小规模单一密度 RS-failure 分布上收敛。
- 不 claim F02.6 warm-start 决策已关闭。
- 不 claim planner integration 已完成。
