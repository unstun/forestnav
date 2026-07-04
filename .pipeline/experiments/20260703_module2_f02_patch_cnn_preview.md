---
date: 2026-07-03
status: f02_3_patch_cnn_preview_smoke_complete_formal_pending
origin: codex+code+experiment
reviewed: false
task: Module2 F02.3
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_f02_obstacle_summary_bc.md
source_head: ab8645e94717b34bd85a8e41109a17330c58ed7c
execution_host: MacBook-Pro.local
---

# Module2 F02.3 Patch-Scalar CNN Preview

## 直观结论

F02.3 已经有 patch+scalar CNN 训练脚本和 preview smoke, 但还没有形成 formal
CNN baseline。

脚本层面已经跑通:

- 从 parquet row 重建 `(2,64,64)` occupancy/EDT patch;
- 与 8 维 scalar observation 一起输入 CNN+MLP;
- checkpoint 可以默认加载;
- closed-loop eval 仍使用 `AnalyticExpansionEnv` 和 0.1m action step。

结果层面不理想:

- 小 smoke: 0/5 success, 5/5 collision
- stronger preview: 1/5 success, 4/5 collision

对比 F02.2 obstacle-summary preview 的 4/5 success, 当前 CNN preview 不能证明
patch CNN 更强。不能因为模型更复杂就把它当最大实现已经完成。下一步需要
formal bounded pilot 或训练协议修正。

## Code Change

New script:

- `2_experiment/forest_n3p/scripts/train_bc_patch_policy.py`

New test:

- `2_experiment/forest_n3p/tests/test_train_bc_patch_policy.py`

Implemented behavior:

| Item | Detail |
|---|---|
| input | BC parquet rows |
| patch | reconstructed via `build_patch_observation` |
| scalar | normalized 8-dim `obs_scalar` |
| network | Conv2d stack + scalar MLP + tanh steering head |
| split | source-row group split, same as scalar/summary BC |
| eval | closed-loop terminal-RS-success through `AnalyticExpansionEnv` |
| bounded mode | `--max-train-rows`, `--max-val-rows` for formal pilot |

## Smoke Run

Command:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.train_bc_patch_policy \
  --allow-duplicate-openmp \
  --device cpu \
  --dataset 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_preview20.parquet \
  --manifest 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest.json \
  --output-dir 2_experiment/forest_n3p/models/module2_rl_rs_bc_patch_preview_smoke \
  --epochs 12 \
  --patience 4 \
  --batch-size 128 \
  --cnn-channels 8,16,32 \
  --hidden-dims 64,32 \
  --rollout-action-step-m 0.1 \
  --collision-sample-step-m 0.05 \
  --rollout-max-steps 96 \
  --source-head ab8645e94717b34bd85a8e41109a17330c58ed7c
```

Result:

- validation MAE: 0.1668064296245575 rad
- closed-loop success: 0/5
- collision: 5/5

Artifacts:

| File | SHA-256 |
|---|---|
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_patch_preview_smoke/checkpoint.pt` | `edd4091260947455f6d42413af4d8342ca0e6ac731f28e71ce7dc80b4c8ef08a` |
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_patch_preview_smoke/history.json` | `7d64c84339504cf6fcbaba21251044bb439a27c1a62312b556ee36ffec4dfd3e` |
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_patch_preview_smoke/summary.json` | `27558ccb56063aa00e4802b3d708490ac9d2f09f300ba87166d2c7e3bbbae1ad` |

## Stronger Preview Run

Command:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.train_bc_patch_policy \
  --allow-duplicate-openmp \
  --device cpu \
  --dataset 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_preview20.parquet \
  --manifest 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest.json \
  --output-dir 2_experiment/forest_n3p/models/module2_rl_rs_bc_patch_preview_stronger \
  --epochs 60 \
  --patience 12 \
  --batch-size 128 \
  --cnn-channels 16,32,64 \
  --hidden-dims 128,64 \
  --rollout-action-step-m 0.1 \
  --collision-sample-step-m 0.05 \
  --rollout-max-steps 96 \
  --source-head ab8645e94717b34bd85a8e41109a17330c58ed7c
```

Result:

- best epoch: 45
- epochs ran: 58
- validation MAE: 0.13033735752105713 rad
- closed-loop success: 1/5
- collision: 4/5

Artifacts:

| File | SHA-256 |
|---|---|
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_patch_preview_stronger/checkpoint.pt` | `008c1e7ca964419296e593bf291f4e03305009a9db58de2e36dc057943de0d56` |
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_patch_preview_stronger/history.json` | `aba9402a230657bdbfbca1f5d9a352b6899ead99fe4dcab6aee8c7999d104177` |
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_patch_preview_stronger/summary.json` | `7536536e967436108ace0228e5af273d5343dedad52810e89958763acd24548d` |

## Verification

Commands:

```bash
PYTHONPATH=2_experiment python -m py_compile \
  2_experiment/forest_n3p/scripts/train_bc_patch_policy.py

KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_train_bc_patch_policy.py \
  2_experiment/forest_n3p/tests/test_train_bc_policy_features.py \
  2_experiment/forest_n3p/tests/test_extract_oracle_demonstrations.py \
  -q

KMP_DUPLICATE_LIB_OK=TRUE python - <<'PY'
import torch
ckpt = torch.load(
    "2_experiment/forest_n3p/models/module2_rl_rs_bc_patch_preview_stronger/checkpoint.pt",
    map_location="cpu",
)
print(ckpt["model_type"], ckpt["patch_channels"], ckpt["cnn_channels"])
PY

git diff --check
```

Results before record commit:

- `py_compile`: pass
- pytest: `6 passed`
- checkpoint load: pass
- `git diff --check`: pass

## Allowed Conclusions

- Patch+scalar CNN training and evaluation are now implemented and smoke-tested.
- The current preview runs are weaker than obstacle-summary preview.
- Action MAE again fails to predict closed-loop behavior.

## Disallowed Conclusions

- Do not claim patch+scalar CNN formal baseline is complete.
- Do not claim patch CNN is better than obstacle-summary.
- Do not start PPO from this checkpoint.
- Do not claim RL-RS planner integration exists.

## Next Step

Run a formal bounded pilot, for example:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.train_bc_patch_policy \
  --allow-duplicate-openmp \
  --device cpu \
  --dataset 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v1.parquet \
  --manifest 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest_formal_v1.json \
  --output-dir 2_experiment/forest_n3p/models/module2_rl_rs_bc_patch_formal_v1_pilot \
  --max-train-rows 4096 \
  --max-val-rows 1024 \
  --epochs 24 \
  --patience 8 \
  --batch-size 128 \
  --cnn-channels 16,32,64 \
  --hidden-dims 128,64 \
  --rollout-action-step-m 0.1 \
  --collision-sample-step-m 0.05 \
  --rollout-max-steps 96
```
