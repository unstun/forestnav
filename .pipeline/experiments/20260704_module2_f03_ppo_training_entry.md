---
status: completed
origin: ai+local+web
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on: .pipeline/experiments/20260704_module2_f03_training_logging.md
---

# Module2 F03 PPO Training Entry / Smoke 记录

## 直观结论

F03.5 正式 Gate #3 还没有判定，但 PPO 训练入口已经补上并通过真实 SB3 smoke。现在项目内有可复跑的 `train_rl_rs_ppo.py`，它会创建 Gymnasium/SB3 向量环境、使用 F03 curriculum、写 episode CSV、保存 SB3 model zip，并生成包含 config/source-hash/checkpoint 的 `training_manifest.json`。

关键边界: 本次 smoke 是 open-connector 极小训练，只验证训练链路真实可运行；不 claim PPO 收敛，不 claim Gate #3 通过，不绕过 F02.6 warm-start 决策。manifest 和 summary 都显式记录 `warm_start_status=not_applied_f02_6_pending`。

## 外部依据

- SB3 2.9.0 官方文档说明 Dict observation 可走 `MultiInputPolicy`: https://stable-baselines3.readthedocs.io/en/master/guide/custom_policy.html
- SB3 2.9.0 官方 callback 文档说明自定义 callback 继承 `BaseCallback`, checkpoint callback 保存 model zip: https://stable-baselines3.readthedocs.io/en/master/guide/callbacks.html
- 本地签名核验: `stable_baselines3.__version__ == 2.9.0`; `PPO.__init__` 支持 `policy_kwargs`, `tensorboard_log`, `seed`, `device`; `CheckpointCallback.__init__` 支持 `save_freq`, `save_path`, `name_prefix`。

## 实现锚点

- SB3 feature extractor: `2_experiment/forest_n3p/rl_rs/sb3_policy.py`。
- `RlRsObstacleSummaryExtractor` 使用 Dict observation 中的 scalar + patch, 输出 29 维 obstacle-summary 特征: `2_experiment/forest_n3p/rl_rs/sb3_policy.py:10-66`。
- region mask 与归一化坐标语义: `2_experiment/forest_n3p/rl_rs/sb3_policy.py:69-89`。
- PPO training entry: `2_experiment/forest_n3p/scripts/train_rl_rs_ppo.py`。
- SB3 lazy import、env 构建、PPO learn、final model、manifest/summary: `2_experiment/forest_n3p/scripts/train_rl_rs_ppo.py:25-86`。
- CLI 与 smoke override: `2_experiment/forest_n3p/scripts/train_rl_rs_ppo.py:89-141`。
- curriculum/env factory: `2_experiment/forest_n3p/scripts/train_rl_rs_ppo.py:152-185`。
- policy kwargs: `2_experiment/forest_n3p/scripts/train_rl_rs_ppo.py:188-197`。
- checkpoint/source hash/config provenance: `2_experiment/forest_n3p/scripts/train_rl_rs_ppo.py:200-283`。

## 测试锚点

- 测试文件: `2_experiment/forest_n3p/tests/test_train_rl_rs_ppo.py`。
- SB3 extractor 与 F02 BC obstacle-summary 特征一致: `2_experiment/forest_n3p/tests/test_train_rl_rs_ppo.py:17-41`。
- `train_rl_rs_ppo --smoke` 写 model/manifest/summary/episode CSV: `2_experiment/forest_n3p/tests/test_train_rl_rs_ppo.py:44-71`。

## TDD 记录

RED:

```bash
KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_train_rl_rs_ppo.py -q
```

失败原因:

```text
ModuleNotFoundError: No module named 'forest_n3p.rl_rs.sb3_policy'
```

GREEN:

```bash
KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests/test_train_rl_rs_ppo.py -q
```

stdout:

```text
2 passed in 1.64s
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
33 passed in 4.70s
```

全量小测试:

```bash
KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest 2_experiment/forest_n3p/tests -q
```

stdout:

```text
54 passed in 7.17s
```

项目内真实 smoke:

```bash
KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment python -m forest_n3p.scripts.train_rl_rs_ppo \
  --allow-duplicate-openmp \
  --smoke \
  --output-dir 0_trials/module2_ppo_smoke/f03_train_entry_smoke \
  --seed 20260704
```

stdout 关键字段:

```text
"status": "complete"
"output_dir": "0_trials/module2_ppo_smoke/f03_train_entry_smoke"
"final_model": "final_model.zip"
"checkpoint_count": 1
"warm_start_status": "not_applied_f02_6_pending"
"total_timesteps": 16
```

产物:

- `0_trials/module2_ppo_smoke/f03_train_entry_smoke/final_model.zip`
- `0_trials/module2_ppo_smoke/f03_train_entry_smoke/episodes_env0.csv`
- `0_trials/module2_ppo_smoke/f03_train_entry_smoke/training_manifest.json`
- `0_trials/module2_ppo_smoke/f03_train_entry_smoke/summary.json`

## 当前不 claim 的内容

- 不 claim Gate #3 通过。
- 不 claim PPO 已在 Complex/Extreme 或 RS-failure 分布上收敛。
- 不 claim obstacle-summary BC checkpoint 已被用于 warm-start；F02.6 仍需 Dr Sun 明确确认。
- 不 claim planner integration 完成；G01/G02 仍未开始。
