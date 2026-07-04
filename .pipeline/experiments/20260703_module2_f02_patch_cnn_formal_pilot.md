---
date: 2026-07-03
status: f02_3_patch_cnn_formal_pilot_failed_to_beat_obstacle_summary
origin: codex+code+experiment
reviewed: false
task: Module2 F02.3
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_f02_patch_cnn_preview.md
source_head: 866b6a825613311c8aea7c21e83eb73ef532a59d
execution_host: MacBook-Pro.local
---

# Module2 F02.3 Patch-Scalar CNN Formal Pilot

## 直观结论

F02.3 已跑一个 formal-v1 bounded pilot, 但 patch+scalar CNN 仍没有超过
obstacle-summary BC。

这一步很重要, 因为它避免了一个常见假结论: "CNN 用了 patch, 所以一定更真实,
可以直接作为 PPO warm start"。当前证据不支持这个结论。

Pilot 结果:

- train rows: 4096
- validation rows: 1024
- validation source rows: 241
- closed-loop success: 44/241
- collision: 185/241
- runtime error: 8/241

对照:

- obstacle-summary formal-v1: 84/259 success, 164/259 collision, 0 runtime error

因此当前 patch CNN checkpoint 不应进入 PPO warm start。

## Command

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
  --rollout-max-steps 96 \
  --source-head 866b6a825613311c8aea7c21e83eb73ef532a59d
```

## Artifacts

| File | SHA-256 |
|---|---|
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_patch_formal_v1_pilot/checkpoint.pt` | `a49d1869928569ca79e82ebd5265102aadd6685c44581583797ea03833d48ab1` |
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_patch_formal_v1_pilot/history.json` | `4e81d585fe970344bc55c05c40d8a42b300a54b7a209b731a4fd18d6993b6e5e` |
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_patch_formal_v1_pilot/summary.json` | `a95b50355b628557017a7a4fe07eb2e49b8d882c85c1fb0c8335e7da0d6c33c3` |

## Metrics

Action metrics:

- best epoch: 10
- epochs ran: 19
- validation MSE: 0.04630407318472862
- validation MAE rad: 0.1442122608423233
- validation max absolute error rad: 0.928107738494873

Closed-loop metrics:

| Metric | Value |
|---|---:|
| episodes | 241 |
| terminal RS success | 44 |
| collision | 185 |
| truncated | 4 |
| runtime error | 8 |
| terminal RS success rate | 0.1825726141078838 |
| collision rate | 0.7676348547717843 |
| truncation rate | 0.016597510373443983 |

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
    "2_experiment/forest_n3p/models/module2_rl_rs_bc_patch_formal_v1_pilot/checkpoint.pt",
    map_location="cpu",
)
print(ckpt["model_type"], ckpt["patch_channels"], ckpt["cnn_channels"])
PY

git diff --check
```

Results before record commit:

- `py_compile`: pass
- pytest: `7 passed`
- checkpoint load: pass
- `git diff --check`: pass

## Allowed Conclusions

- The patch+scalar CNN formal pilot is real and source-bound.
- Current patch CNN does not beat obstacle-summary BC.
- Runtime error recording needed improvement; the script was patched after this run.

## Disallowed Conclusions

- Do not claim patch CNN formal baseline is complete.
- Do not use this checkpoint for PPO warm start.
- Do not claim CNN is better than obstacle-summary.
- Do not claim planner integration exists.

## Next Step

Before another CNN run:

1. rerun a small eval with the improved runtime-error message path to identify
   the 8 `ValueError` causes;
2. consider patch cache or remote training before full formal-v1 CNN;
3. consider using obstacle-summary checkpoint as the practical BC warm-start
   candidate while CNN protocol is debugged.
