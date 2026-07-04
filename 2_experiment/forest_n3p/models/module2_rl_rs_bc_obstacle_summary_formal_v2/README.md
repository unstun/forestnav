# Module2 F02 Formal V2 Obstacle-Summary BC

This directory contains the obstacle-summary BC rerun on the profile-aware
formal-v2 corpus. The feature vector is scalar observation plus summary
statistics derived from the same egocentric occupancy/EDT patch used by the
RL-RS environment.

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
  --feature-mode obstacle_summary \
  --dataset 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v2.parquet \
  --manifest 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest_formal_v2.json \
  --output-dir 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2 \
  --epochs 120 \
  --patience 16 \
  --batch-size 512 \
  --hidden-dims 128,128,64 \
  --rollout-action-step-m 0.1 \
  --collision-sample-step-m 0.05 \
  --rollout-max-steps 96 \
  --source-head 801455da1acd77af8cea9b42f674d3039c52e394
```

## Outputs

| File | SHA-256 |
|---|---|
| `checkpoint.pt` | `3156df44ca7f26da7f2e635707554bb1cd486164638b3a2d11075c3787670683` |
| `history.json` | `3bc13c766f566ba2e0985bbb8d9a3f54a301cca1f450d3b6f7421b83f5df3491` |
| `summary.json` | `73baacd42654fa63b94b2323d5612098e55a870a0e81064d53880f80d342a2d7` |

## Metrics

Training split:

| Metric | Value |
|---|---:|
| dataset rows | 83809 |
| train rows | 62269 |
| validation rows | 21540 |
| train source rows | 774 |
| validation source rows | 258 |
| best epoch | 67 |
| epochs ran | 84 |
| validation MAE rad | 0.0966578796505928 |

Closed loop with 0.1m rollout step:

| Metric | Value |
|---|---:|
| episodes | 258 |
| terminal RS success | 67 |
| collision | 178 |
| truncated | 13 |
| runtime error | 0 |

## Boundary

Obstacle-summary BC remains stronger than scalar-only BC on formal-v2, but
67/258 success is not enough for planner insertion. Patch-CNN formal-v2 must be
rerun before selecting a PPO warm start.
