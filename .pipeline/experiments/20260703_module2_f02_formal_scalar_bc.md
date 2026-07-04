---
date: 2026-07-03
status: f02_2_scalar_lower_bound_complete_strong_bc_pending
origin: codex+code+experiment
reviewed: false
task: Module2 F02.2
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_f02_bc_policy_smoke.md
source_head: 2139ce17aece9fe4c44054295a9bc0e711020c3f
execution_host: MacBook-Pro.local
---

# Module2 F02.2 Formal V1 Scalar BC

## 直观结论

F02.2 已经完成一个真实的 formal-v1 scalar BC lower-bound, 但还不能把它当作
最终强 BC baseline。

这次不是 preview 玩具数据:

- formal-v1 corpus: 85514 demo rows
- source rows: 1035
- oracle-A source rows: 1024
- current-code-replayable oracle-B source rows: 11
- Complex/Extreme demo rows: 42429 / 43085

训练后 action regression 看起来变好, validation MAE 从 preview smoke 的
0.147 rad 降到 0.096 rad。但闭环指标很差:

- 0.3m rollout step: 259 episodes 中成功 11, 碰撞 236
- 0.1m rollout step: 259 episodes 中成功 45, 碰撞 199

所以这里的研究结论不是 "BC 足够好", 而是:

1. action MSE 仍然会严重误导;
2. demonstration step length 和 rollout action step 必须对齐;
3. scalar-only observation 缺少障碍信息, 不能作为论文级强 BC baseline。

## Dataset Corpus

Dataset manifest:

- `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest_formal_v1.json`

Merged dataset:

- `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v1.parquet`
- rows: 85514
- SHA-256: `e39a11828f9eb45d3397d0264e366364664ecaadc9cdca64e49a95c527e62de1`

Composition:

| Shard | Source rows | Demo rows |
|---|---:|---:|
| Complex oracle-A | 512 | 42293 |
| Extreme oracle-A | 512 | 42209 |
| goal_annulus oracle-B | 11 | 1012 |

B-only boundary:

- historical C02 has 58 `goal_annulus` B-only rows;
- current-code replay succeeds for 11/58;
- the other rows are invalid under current collision/start-goal semantics;
- wider 12s / 100k-node segment budget did not recover them.

## Training Run

Command:

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

Outputs:

| File | SHA-256 |
|---|---|
| `checkpoint.pt` | `4bc0fe2850691a872aba56e3c21f4f7b14a0fc3fc4cfdc42c167202f24919e29` |
| `history.json` | `43baaea714f1ce6f77ce0e85fe257483cb8d7d3c3b5d0eabe47669a1c0f90813` |
| `summary.json` | `6fbd5fbb51c0743c14d206525cc0078ce7481ccf23e5dee3d2dffb819a7bcfd5` |
| `eval_rollout_step01.json` | `3e4de476e466d09430b452bda929012e5d317e35a3fc8b2a8994d65186329438` |

Action metrics:

- best epoch: 116
- epochs ran: 120
- validation MSE: 0.024822887033224106
- validation MAE rad: 0.09640851616859436
- validation max absolute error rad: 1.0433231592178345

Closed-loop metrics with 0.3m rollout step:

| Metric | Value |
|---|---:|
| episodes | 259 |
| terminal RS success | 11 |
| collision | 236 |
| truncated | 12 |
| runtime error | 0 |
| terminal RS success rate | 0.04247104247104247 |
| collision rate | 0.9111969111969112 |

Closed-loop metrics with 0.1m rollout step:

| Metric | Value |
|---|---:|
| episodes | 259 |
| terminal RS success | 45 |
| collision | 199 |
| truncated | 15 |
| runtime error | 0 |
| terminal RS success rate | 0.17374517374517376 |
| collision rate | 0.7683397683397684 |

## Verification

Commands:

```bash
PYTHONPATH=2_experiment python -m py_compile \
  2_experiment/forest_n3p/scripts/extract_oracle_demonstrations.py \
  2_experiment/forest_n3p/scripts/merge_demonstration_shards.py \
  2_experiment/forest_n3p/scripts/train_bc_policy.py

PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_extract_oracle_demonstrations.py \
  -q

git diff --check
```

Results before record commit:

- formal manifest check: pass
- checkpoint hash recorded
- `py_compile`: pass
- `pytest`: `3 passed`
- `git diff --check`: pass

## Allowed Conclusions

- Formal-v1 scalar BC training is real and reproducible.
- Scalar-only BC is a weak lower-bound under current observation design.
- Closed-loop terminal-RS-success is the correct decision metric; action MSE is insufficient.
- Step-length alignment matters: 0.1m evaluation improves success but remains weak.

## Disallowed Conclusions

- Do not claim F02.2 strong BC baseline is complete.
- Do not claim BC is good enough for planner insertion.
- Do not claim PPO training has started.
- Do not claim RL-RS planner integration exists.
- Do not use the historical 58 B-only rows as if all were current-code reproducible.

## Next Step

Continue F02.2 with an obstacle-aware BC baseline:

- either patch+scalar CNN using reconstructed egocentric occupancy/EDT patches;
- or a lighter clearance-feature baseline explicitly labeled as obstacle-summary BC;
- and align demonstration action step with rollout action step before judging BC.
