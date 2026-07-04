# Module2 F02 Formal V1 Scalar BC

This directory contains the scalar-observation BC lower-bound run on the F02
formal-v1 corpus.

It is a real training run, but it is not a strong BC baseline.

## Inputs

- dataset: `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v1.parquet`
- manifest: `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest_formal_v1.json`
- source head: `2139ce17aece9fe4c44054295a9bc0e711020c3f`

## Training Command

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.train_bc_policy \
  --allow-duplicate-openmp \
  --device cpu \
  --dataset 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v1.parquet \
  --manifest 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest_formal_v1.json \
  --output-dir 2_experiment/forest_n3p/models/module2_rl_rs_bc_formal_v1 \
  --epochs 120 \
  --patience 16 \
  --batch-size 512 \
  --hidden-dims 128,128,64 \
  --source-head 2139ce17aece9fe4c44054295a9bc0e711020c3f
```

## Outputs

| File | SHA-256 |
|---|---|
| `checkpoint.pt` | `4bc0fe2850691a872aba56e3c21f4f7b14a0fc3fc4cfdc42c167202f24919e29` |
| `history.json` | `43baaea714f1ce6f77ce0e85fe257483cb8d7d3c3b5d0eabe47669a1c0f90813` |
| `summary.json` | `6fbd5fbb51c0743c14d206525cc0078ce7481ccf23e5dee3d2dffb819a7bcfd5` |
| `eval_rollout_step01.json` | `3e4de476e466d09430b452bda929012e5d317e35a3fc8b2a8994d65186329438` |

## Training Metrics

| Metric | Value |
|---|---:|
| dataset rows | 85514 |
| train rows | 64071 |
| validation rows | 21443 |
| train source rows | 776 |
| validation source rows | 259 |
| best epoch | 116 |
| validation MSE | 0.024822887033224106 |
| validation MAE rad | 0.09640851616859436 |

Closed loop with the original 0.3m rollout step:

| Metric | Value |
|---|---:|
| episodes | 259 |
| terminal RS success | 11 |
| collision | 236 |
| truncated | 12 |
| success rate | 0.04247104247104247 |
| collision rate | 0.9111969111969112 |

Posthoc closed loop with 0.1m rollout step, matching the demonstration
`step_length_m` distribution:

| Metric | Value |
|---|---:|
| episodes | 259 |
| terminal RS success | 45 |
| collision | 199 |
| truncated | 15 |
| success rate | 0.17374517374517376 |
| collision rate | 0.7683397683397684 |

## Interpretation Boundary

- Action regression improved over preview smoke, but closed-loop performance is
  still poor.
- The default 0.3m rollout evaluation is mismatched with the formal-v1
  demonstration step length, which is approximately 0.1m.
- Even after step-length-aligned 0.1m evaluation, scalar-only BC collides too
  often to serve as the final BC baseline.
- Next BC baseline must use obstacle-aware observation, for example patch+scalar
  or a derived clearance feature set.
