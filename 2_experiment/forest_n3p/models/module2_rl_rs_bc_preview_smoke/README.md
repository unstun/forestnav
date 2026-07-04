# Module2 F02 BC Preview Smoke

This directory is a preview-smoke artifact for Module2 F02.1.

It proves the BC training, checkpoint, and closed-loop evaluation chain can run on
the F01 preview demonstrations. It does not prove BC is a strong planner
baseline.

## Inputs

- dataset: `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_preview20.parquet`
- dataset manifest: `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest.json`
- source head: `45034d43ce5f23da82a2f7d7eb80da8caeea0f3c`

## Command

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.train_bc_policy \
  --allow-duplicate-openmp \
  --device cpu \
  --epochs 30 \
  --patience 8 \
  --batch-size 128 \
  --hidden-dims 64,64 \
  --source-head 45034d43ce5f23da82a2f7d7eb80da8caeea0f3c \
  --output-dir 2_experiment/forest_n3p/models/module2_rl_rs_bc_preview_smoke
```

`--allow-duplicate-openmp` is a local Mac smoke workaround for the observed
`libomp.dylib already initialized` Torch import failure.

## Outputs

| File | SHA-256 |
|---|---|
| `summary.json` | `48f8f99b4c0d8a083872bbd9dc1bc1c8a25ee70a073d7c84d60719ae831fdb86` |
| `history.json` | `b61bab1743419aef4a53818fd9e3b120084f9ab009b1f12b81515532d714d1ca` |
| `checkpoint.pt` | `36a95f5a40835c4356e65e42258d1367b1555951c9a5be5d91279af63d4585a7` |

## Metrics

| Metric | Value |
|---|---:|
| dataset rows | 1109 |
| train rows | 828 |
| validation rows | 281 |
| best epoch | 29 |
| validation MSE | 0.044572457671165466 |
| validation MAE rad | 0.14736425876617432 |
| closed-loop held-out episodes | 5 |
| terminal RS success | 2 |
| collision | 3 |
| terminal RS success rate | 0.4 |
| collision rate | 0.6 |

## Load Check

```bash
KMP_DUPLICATE_LIB_OK=TRUE python - <<'PY'
import torch
path = "2_experiment/forest_n3p/models/module2_rl_rs_bc_preview_smoke/checkpoint.pt"
ckpt = torch.load(path, map_location="cpu")
print(sorted(ckpt.keys()))
PY
```

Result: checkpoint loads with PyTorch's default `weights_only=True` behavior.

## Boundaries

- This is a preview smoke run, not the formal BC baseline.
- The source dataset is F01 preview data, not the final full BC corpus.
- The closed-loop result is weak: 2 successes and 3 collisions on 5 held-out
  source rows.
- Do not claim PPO training has started.
- Do not claim RL-RS planner integration exists.
