# Module2 F02 Formal V1 Obstacle-Summary BC

This directory contains the formal-v1 obstacle-summary BC baseline.

The feature vector is:

- 8 scalar observation values;
- 21 obstacle-summary values derived from the same egocentric occupancy/EDT
  patch used by `AnalyticExpansionEnv`.

This is stronger than scalar-only BC but still weaker than a full patch+scalar
CNN.

## Input

- dataset: `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v1.parquet`
- manifest: `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest_formal_v1.json`
- source head: `4faf0f399495ae5844c1f34d12aab95027d64fbe`

## Training Command

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

## Metrics

| Metric | Scalar 0.1m | Obstacle-summary 0.1m |
|---|---:|---:|
| validation MAE rad | 0.09640851616859436 | 0.0998290479183197 |
| held-out episodes | 259 | 259 |
| terminal RS success | 45 | 84 |
| collision | 199 | 164 |
| truncated | 15 | 11 |
| success rate | 0.17374517374517376 | 0.32432432432432434 |
| collision rate | 0.7683397683397684 | 0.6332046332046332 |

The action MAE is slightly worse than scalar-only, while closed-loop success is
much better. This reinforces that action loss alone is not the decision metric.

## Artifacts

| File | SHA-256 |
|---|---|
| `checkpoint.pt` | `2391a88a6a9eb3b88cc3d6eaaca7385a33dbde52d679e7ce0be99dd481800692` |
| `history.json` | `37139edd501ac0212377a0d7663dc6c26271cb09426e127e4d71d9ad48f0ed72` |
| `summary.json` | `20c30f843369c853ca25f3cf0b686053b8290fc85ded838d5bce2cca2ed2cd3d` |

## Boundary

- Obstacle information helps: success improves from 45/259 to 84/259.
- The baseline is still not strong enough for planner insertion.
- This does not start PPO.
- This does not implement the final RL-RS analytic operator.
- Next maximum-implementation step is patch+scalar CNN BC warm-start.
