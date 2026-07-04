---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_f02_formal_v2_mlp_bc_baselines.md
  - .pipeline/experiments/20260704_module2_f03_ppo_training_entry.md
---

# Module2 F03 Obstacle-Summary BC Warm-Start 接线记录

## 直观结论

obstacle-summary BC warm-start 现在已经从“推荐候选”变成“PPO 训练入口可真实加载、可验证行为对齐”的实现路径。`train_rl_rs_ppo.py` 支持 `--bc-checkpoint`, 会把 F02 obstacle-summary MLP 的隐藏层、最终 steering head、feature normalization 转入 SB3 PPO actor, 并在 manifest 中记录 checkpoint path、SHA-256、model_type、hidden_dims 和 `warm_start_status=applied_obstacle_summary_bc`。

这仍然不是 F02.6 决策关闭, 也不是 Gate #3 判定。它只说明: 如果 Dr Sun 选择 obstacle-summary warm-start, 代码路径已经不是口头方案, 而是可复跑、可审计、带行为一致性测试的真实路径。

## 实现锚点

- `TanhLinearActionHead` 保留 F02 BC policy 的 normalized tanh action 输出: `2_experiment/forest_n3p/rl_rs/sb3_policy.py:10-18`。
- SB3 obstacle-summary extractor 输出 scalar + 21 维 region summary, 并支持 feature_mean/std normalization: `2_experiment/forest_n3p/rl_rs/sb3_policy.py:21-77`。
- `--bc-checkpoint` CLI: `2_experiment/forest_n3p/scripts/train_rl_rs_ppo.py:92-129`。
- PPO model 创建后、learn 前执行 warm-start 注入并写入 config: `2_experiment/forest_n3p/scripts/train_rl_rs_ppo.py:33-59`。
- BC checkpoint hidden layers -> PPO policy_net, BC final layer -> `TanhLinearActionHead`, normalization -> extractor buffers: `2_experiment/forest_n3p/scripts/train_rl_rs_ppo.py:206-290`。
- warm-start manifest 记录包含 checkpoint SHA: `2_experiment/forest_n3p/scripts/train_rl_rs_ppo.py:241-250`。

## 测试锚点

- extractor 与 F02 BC obstacle-summary feature 语义一致: `2_experiment/forest_n3p/tests/test_train_rl_rs_ppo.py:30-55`。
- `train_rl_rs_ppo --smoke` 仍写 model/manifest/episode CSV: `2_experiment/forest_n3p/tests/test_train_rl_rs_ppo.py:58-85`。
- warm-start 后 PPO deterministic action 与原 BC normalized action 一致: `2_experiment/forest_n3p/tests/test_train_rl_rs_ppo.py:88-140`。

## 验证记录

RED:

```bash
KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_train_rl_rs_ppo.py -q
```

失败原因:

```text
AttributeError: 'MultiInputActorCriticPolicy' object has no attribute 'lr_schedule'
```

修复: 重建 optimizer 时沿用当前 optimizer param group 的 learning rate, 而不是访问不存在的 `policy.lr_schedule`。

GREEN:

```bash
KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_train_rl_rs_ppo.py -q
```

stdout:

```text
3 passed in 1.78s
```

相关测试:

```bash
python -m py_compile \
  2_experiment/forest_n3p/rl_rs/sb3_policy.py \
  2_experiment/forest_n3p/scripts/train_rl_rs_ppo.py \
  2_experiment/forest_n3p/tests/test_train_rl_rs_ppo.py

KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_rl_rs_api.py \
  2_experiment/forest_n3p/tests/test_rl_rs_gym_env.py \
  2_experiment/forest_n3p/tests/test_rl_rs_curriculum.py \
  2_experiment/forest_n3p/tests/test_rl_rs_training_logging.py \
  2_experiment/forest_n3p/tests/test_train_rl_rs_ppo.py -q
```

stdout:

```text
34 passed in 4.84s
```

全量小测试:

```bash
KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests -q
```

stdout:

```text
55 passed in 6.97s
```

真实 warm-start smoke:

```bash
KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment python -m forest_n3p.scripts.train_rl_rs_ppo \
  --allow-duplicate-openmp \
  --smoke \
  --bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt \
  --output-dir 0_trials/module2_ppo_smoke/f03_warm_start_entry_smoke \
  --seed 20260704
```

stdout 关键字段:

```text
"status": "complete"
"output_dir": "0_trials/module2_ppo_smoke/f03_warm_start_entry_smoke"
"warm_start_status": "applied_obstacle_summary_bc"
"checkpoint_sha256": "3156df44ca7f26da7f2e635707554bb1cd486164638b3a2d11075c3787670683"
"action_head": "TanhLinearActionHead"
```

产物:

- `0_trials/module2_ppo_smoke/f03_warm_start_entry_smoke/final_model.zip`
- `0_trials/module2_ppo_smoke/f03_warm_start_entry_smoke/episodes_env0.csv`
- `0_trials/module2_ppo_smoke/f03_warm_start_entry_smoke/training_manifest.json`
- `0_trials/module2_ppo_smoke/f03_warm_start_entry_smoke/summary.json`

## 当前不 claim 的内容

- 不 claim Dr Sun 已批准 obstacle-summary warm-start。
- 不 claim F02.6 已关闭。
- 不 claim PPO 在 RS-failure / Complex / Extreme 分布上收敛。
- 不 claim F03.5 Gate #3 已通过。
- 不 claim planner integration 完成。
