---
date: 2026-07-03
status: f02_2_obstacle_summary_bc_complete_patch_cnn_pending
origin: codex+code+experiment
reviewed: false
task: Module2 F02.2
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_f02_formal_scalar_bc.md
source_head: 4faf0f399495ae5844c1f34d12aab95027d64fbe
execution_host: MacBook-Pro.local
---

# Module2 F02.2 Obstacle-Summary BC Baseline

## 直观结论

F02.2 的正式 BC baseline 已从 scalar-only 下界推进到 obstacle-summary BC。

这一步没有只调 MLP 层数。新实现把 `AnalyticExpansionEnv` 已有的
egocentric occupancy/EDT patch 接入训练, 从 patch 派生 21 个障碍摘要特征,
再与 8 维 scalar observation 拼接成 29 维特征。训练和闭环评估使用同一套
feature mode, 避免训练/评估口径分裂。

结果:

- scalar-only 0.1m closed loop: 45/259 success, 199/259 collision
- obstacle-summary 0.1m closed loop: 84/259 success, 164/259 collision

障碍信息明显有效, 但还不够。32.4% success rate 不能支撑 planner insertion,
也达不到 PPO Gate #3 试点期望的 >80% 量级。因此 F02 的最大实现下一步应
继续做 patch+scalar CNN BC warm-start, 再进入 PPO fine-tuning。

## Code Change

Changed file:

- `2_experiment/forest_n3p/scripts/train_bc_policy.py`

New behavior:

| Item | Detail |
|---|---|
| feature mode | `--feature-mode scalar` or `--feature-mode obstacle_summary` |
| obstacle source | `build_patch_observation(...)` from existing RL-RS observation code |
| patch semantics | occupancy + normalized EDT, robot-frame 6.4m / 64 cells by default |
| summary features | 7 regions x occupancy mean / EDT min / EDT mean = 21 values |
| policy input | 8 scalar values + 21 obstacle values = 29 values |
| closed-loop eval | derives the same feature mode from `AnalyticExpansionEnv` observations |

Tests:

- `2_experiment/forest_n3p/tests/test_train_bc_policy_features.py`

## Preview Smoke

Command:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.train_bc_policy \
  --allow-duplicate-openmp \
  --device cpu \
  --feature-mode obstacle_summary \
  --dataset 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_preview20.parquet \
  --manifest 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest.json \
  --output-dir 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_preview_smoke \
  --epochs 20 \
  --patience 6 \
  --batch-size 128 \
  --hidden-dims 96,64 \
  --rollout-action-step-m 0.1 \
  --collision-sample-step-m 0.05 \
  --rollout-max-steps 96 \
  --source-head 4faf0f399495ae5844c1f34d12aab95027d64fbe
```

Result:

- validation MAE: 0.14981937408447266 rad
- closed-loop success: 4/5
- collision: 1/5

This is only an end-to-end smoke.

## Formal V1 Run

Command:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.train_bc_policy \
  --allow-duplicate-openmp \
  --device cpu \
  --feature-mode obstacle_summary \
  --dataset 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v1.parquet \
  --manifest 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest_formal_v1.json \
  --output-dir 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v1 \
  --epochs 120 \
  --patience 16 \
  --batch-size 512 \
  --hidden-dims 128,128,64 \
  --rollout-action-step-m 0.1 \
  --collision-sample-step-m 0.05 \
  --rollout-max-steps 96 \
  --source-head 4faf0f399495ae5844c1f34d12aab95027d64fbe
```

Artifacts:

| File | SHA-256 |
|---|---|
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v1/checkpoint.pt` | `2391a88a6a9eb3b88cc3d6eaaca7385a33dbde52d679e7ce0be99dd481800692` |
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v1/history.json` | `37139edd501ac0212377a0d7663dc6c26271cb09426e127e4d71d9ad48f0ed72` |
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v1/summary.json` | `20c30f843369c853ca25f3cf0b686053b8290fc85ded838d5bce2cca2ed2cd3d` |

Action metrics:

- best epoch: 64
- epochs ran: 81
- validation MSE: 0.0278336089104414
- validation MAE rad: 0.0998290479183197
- validation max absolute error rad: 1.079706072807312

Closed-loop metrics:

| Metric | Value |
|---|---:|
| episodes | 259 |
| terminal RS success | 84 |
| collision | 164 |
| truncated | 11 |
| runtime error | 0 |
| terminal RS success rate | 0.32432432432432434 |
| collision rate | 0.6332046332046332 |
| truncation rate | 0.04247104247104247 |

## Scalar vs Obstacle-Summary

| Metric | Scalar 0.1m | Obstacle-summary 0.1m |
|---|---:|---:|
| validation MAE rad | 0.09640851616859436 | 0.0998290479183197 |
| terminal RS success | 45/259 | 84/259 |
| collision | 199/259 | 164/259 |
| truncated | 15/259 | 11/259 |
| success rate | 0.17374517374517376 | 0.32432432432432434 |
| collision rate | 0.7683397683397684 | 0.6332046332046332 |

Interpretation:

- obstacle features improve closed-loop behavior despite slightly worse action MAE;
- action loss remains an insufficient proxy;
- current obstacle-summary BC is useful evidence, but not a final neural analytic operator.

## Verification

Commands:

```bash
PYTHONPATH=2_experiment python -m py_compile \
  2_experiment/forest_n3p/scripts/train_bc_policy.py

PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_train_bc_policy_features.py \
  2_experiment/forest_n3p/tests/test_extract_oracle_demonstrations.py \
  -q

KMP_DUPLICATE_LIB_OK=TRUE python - <<'PY'
import torch
ckpt = torch.load(
    "2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v1/checkpoint.pt",
    map_location="cpu",
)
print(ckpt["model_type"], ckpt["input_dim"], ckpt["feature_mode"])
PY

git diff --check
```

Results before record commit:

- `py_compile`: pass
- pytest: `5 passed`
- checkpoint load: pass, `obstacle_summary_steering_mlp 29 obstacle_summary`
- `git diff --check`: pass

## Allowed Conclusions

- Obstacle-summary BC is a real, source-bound formal-v1 baseline.
- Obstacle features materially improve closed-loop success over scalar-only BC.
- BC is not yet strong enough for planner insertion.

## Disallowed Conclusions

- Do not claim RL-RS planner integration exists.
- Do not claim PPO training has started.
- Do not claim obstacle-summary BC reaches Gate #3.
- Do not claim action MAE alone shows quality.
- Do not claim this replaces patch+scalar CNN if maximum implementation is required.

## Next Step

Add F02.3 patch+scalar CNN BC warm-start:

- train directly on reconstructed `(2,64,64)` occupancy/EDT patches plus scalar features;
- evaluate with 0.1m action step and terminal-RS-success;
- use the resulting checkpoint as PPO initialization only if closed-loop behavior improves.
