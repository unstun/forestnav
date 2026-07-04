# Module2 F02 Obstacle-Summary BC Preview Smoke

This directory is a smoke run for `--feature-mode obstacle_summary`.

It validates that the training script can reconstruct egocentric occupancy/EDT
patches, derive obstacle-summary features, train a policy, save a checkpoint,
and evaluate the same feature mode in closed loop.

## Input

- dataset: `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_preview20.parquet`
- source head: `4faf0f399495ae5844c1f34d12aab95027d64fbe`

## Metrics

| Metric | Value |
|---|---:|
| dataset rows | 1109 |
| validation MAE rad | 0.14981937408447266 |
| held-out episodes | 5 |
| terminal RS success | 4 |
| collision | 1 |
| terminal RS success rate | 0.8 |

## Artifacts

| File | SHA-256 |
|---|---|
| `checkpoint.pt` | `d4aacebcd0f8a422dfb293a689da78dfd00aa9b1986273ba674d5b4382b0ac2c` |
| `history.json` | `670dcd1509adc0a4492af2bc157f4488d5f19cc0d0e0641f6632c9ad3448adf0` |
| `summary.json` | `95627a1aea1add4d3f31e32fe8fdf9d9d7d478291901d3917200d58c7bda8384` |

## Boundary

This is not the formal baseline. It is a preview smoke over 5 held-out source
rows.
