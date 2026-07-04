# Module2 F02 Formal V2 Scalar BC

This directory contains the scalar-observation BC lower-bound rerun on the
profile-aware formal-v2 corpus.

## Inputs

- dataset: `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v2.parquet`
- manifest: `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest_formal_v2.json`
- source head: `801455da1acd77af8cea9b42f674d3039c52e394`

## Training Command

```bash
PYTHONPATH=2_experiment KMP_DUPLICATE_LIB_OK=TRUE \
python -m forest_n3p.scripts.train_bc_policy \
  --allow-duplicate-openmp \
  --device cpu \
  --dataset 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v2.parquet \
  --manifest 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest_formal_v2.json \
  --output-dir 2_experiment/forest_n3p/models/module2_rl_rs_bc_formal_v2_scalar \
  --epochs 120 \
  --patience 16 \
  --batch-size 512 \
  --hidden-dims 128,128,64 \
  --source-head 801455da1acd77af8cea9b42f674d3039c52e394
```

## Outputs

| File | SHA-256 |
|---|---|
| `checkpoint.pt` | `84223cf1f7978d9646068d54507a3220da91dfc58ba7fb26e77f479d83e5e33f` |
| `history.json` | `f57440f6d094391dc5ebc9ff516dddfff7bf475e4ee89cf292231b96b489c1d3` |
| `summary.json` | `cc8e7fd50180d437d62e2b5e4d4db745e038f34c53bb406fe41b12dd61e52a5f` |
| `eval_rollout_step01.json` | `62037ed1999cb6cd5e02452c8fb686a6785226ff06ca229895223bd79d853d63` |
| `eval_patch_bounded_rows.json` | `06f784583cdf119ea1c337ae824c690c504451b9cbca09f17bf155c33282e9d8` |

## Metrics

Training split:

| Metric | Value |
|---|---:|
| dataset rows | 83809 |
| train rows | 62269 |
| validation rows | 21540 |
| train source rows | 774 |
| validation source rows | 258 |
| best epoch | 74 |
| epochs ran | 91 |
| validation MAE rad | 0.10266680270433426 |

Closed loop with original 0.3m rollout step:

| Metric | Value |
|---|---:|
| episodes | 258 |
| terminal RS success | 6 |
| collision | 252 |
| truncated | 0 |
| runtime error | 0 |

Posthoc closed loop with 0.1m rollout step:

| Metric | Value |
|---|---:|
| episodes | 258 |
| terminal RS success | 38 |
| collision | 200 |
| truncated | 20 |
| runtime error | 0 |

Posthoc closed loop on the same 1024 bounded validation rows used by the
patch-CNN pilot:

| Metric | Value |
|---|---:|
| episodes | 242 |
| terminal RS success | 65 |
| collision | 162 |
| truncated | 15 |
| runtime error | 0 |

## Boundary

Scalar-only BC is a weak lower bound. It is not suitable for planner insertion
or PPO warm-start selection.
