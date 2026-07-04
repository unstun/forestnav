# Module2 F02 Formal V2 Patch-Scalar CNN Pilot

This directory contains a bounded patch+scalar CNN BC pilot on the profile-aware
formal-v2 corpus.

## Inputs

- dataset: `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v2.parquet`
- manifest: `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest_formal_v2.json`
- source head: `dc94ac9f234ff9a1606895bc79b8809326981002`

## Training Command

```bash
PYTHONPATH=2_experiment KMP_DUPLICATE_LIB_OK=TRUE \
python -m forest_n3p.scripts.train_bc_patch_policy \
  --allow-duplicate-openmp \
  --device cpu \
  --dataset 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v2.parquet \
  --manifest 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest_formal_v2.json \
  --output-dir 2_experiment/forest_n3p/models/module2_rl_rs_bc_patch_formal_v2_pilot \
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
  --source-head dc94ac9f234ff9a1606895bc79b8809326981002
```

## Outputs

| File | SHA-256 |
|---|---|
| `checkpoint.pt` | `2e1d069178e5b76ac2ac78a94cff690edac702749ddf7e7ed8bfe04f00daf0ed` |
| `history.json` | `86388ab8337fd0175c72a696f61f8f93e66e429793e24728e91d694950f68b80` |
| `summary.json` | `0454193ac49c55194cca168d196c1a7ea82f27d14c9cc989f215cc82e704d669` |

## Metrics

| Metric | Value |
|---|---:|
| dataset rows | 83809 |
| train rows | 4096 |
| validation rows | 1024 |
| train source rows | 747 |
| validation source rows | 242 |
| best epoch | 22 |
| epochs ran | 24 |
| validation MAE rad | 0.14376741647720337 |
| terminal RS success | 63/242 |
| collision | 171/242 |
| truncated | 8/242 |
| runtime error | 0/242 |

## Boundary

This bounded pilot does not establish patch-CNN superiority over
obstacle-summary BC. The validation source set differs from the obstacle-summary
run, the success rate is similar, and action MAE is worse. Do not use this
checkpoint as the PPO warm-start without an explicit follow-up decision.
