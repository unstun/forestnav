---
date: 2026-07-04
status: f02_5_formal_v2_scalar_and_obstacle_summary_complete_patch_cnn_pending
origin: codex+code+experiment
reviewed: false
task: Module2 F02.5
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260704_module2_f02_map_cache_formal_v2_rebuild.md
source_head: 801455da1acd77af8cea9b42f674d3039c52e394
execution_host: MacBook-Pro.local
---

# Module2 F02.5 Formal V2 MLP BC Baselines

## 直观结论

在 profile-aware formal-v2 corpus 上, obstacle-summary BC 仍明显强于
scalar-only BC, 但还远不足以进入 planner insertion 或直接当 PPO warm start。

关键数字:

| Model | Eval step | Success | Collision | Truncated | Runtime error |
|---|---:|---:|---:|---:|---:|
| scalar | 0.3m | 6/258 | 252/258 | 0/258 | 0 |
| scalar | 0.1m | 38/258 | 200/258 | 20/258 | 0 |
| obstacle-summary | 0.1m | 67/258 | 178/258 | 13/258 | 0 |

这说明:

1. action MAE 仍不能替代闭环指标;
2. step-aligned 0.1m eval 对 scalar 有帮助, 但仍弱;
3. obstacle features 仍有真实闭环收益;
4. 当前 practical warm-start 只能暂记为 obstacle-summary, 但必须等
   patch+scalar CNN formal-v2 rerun 后再决策。

## Dataset

- dataset: `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v2.parquet`
- manifest: `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest_formal_v2.json`
- rows: 83809
- source rows: 1032
- collision audit: 0 current collision, 0 next collision

## Scalar BC

Training command:

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

Posthoc 0.1m eval command:

```bash
PYTHONPATH=2_experiment KMP_DUPLICATE_LIB_OK=TRUE \
python -m forest_n3p.scripts.eval_bc_policy \
  --device cpu \
  --checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_formal_v2_scalar/checkpoint.pt \
  --dataset 2_experiment/forest_n3p/datasets/module2_rl_rs_bc/demonstrations_formal_v2.parquet \
  --output 2_experiment/forest_n3p/models/module2_rl_rs_bc_formal_v2_scalar/eval_rollout_step01.json \
  --rollout-action-step-m 0.1 \
  --collision-sample-step-m 0.05 \
  --rollout-max-steps 96 \
  --source-head 801455da1acd77af8cea9b42f674d3039c52e394+working_tree_eval_script
```

Metrics:

| Metric | Value |
|---|---:|
| train rows | 62269 |
| val rows | 21540 |
| train source rows | 774 |
| val source rows | 258 |
| best epoch | 74 |
| epochs ran | 91 |
| validation MAE rad | 0.10266680270433426 |

Artifacts:

| File | SHA-256 |
|---|---|
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_formal_v2_scalar/checkpoint.pt` | `84223cf1f7978d9646068d54507a3220da91dfc58ba7fb26e77f479d83e5e33f` |
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_formal_v2_scalar/history.json` | `f57440f6d094391dc5ebc9ff516dddfff7bf475e4ee89cf292231b96b489c1d3` |
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_formal_v2_scalar/summary.json` | `cc8e7fd50180d437d62e2b5e4d4db745e038f34c53bb406fe41b12dd61e52a5f` |
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_formal_v2_scalar/eval_rollout_step01.json` | `62037ed1999cb6cd5e02452c8fb686a6785226ff06ca229895223bd79d853d63` |

## Obstacle-Summary BC

Training command:

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

Metrics:

| Metric | Value |
|---|---:|
| train rows | 62269 |
| val rows | 21540 |
| train source rows | 774 |
| val source rows | 258 |
| best epoch | 67 |
| epochs ran | 84 |
| validation MAE rad | 0.0966578796505928 |
| terminal RS success | 67/258 |
| collision | 178/258 |
| truncated | 13/258 |
| runtime error | 0/258 |

Artifacts:

| File | SHA-256 |
|---|---|
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt` | `3156df44ca7f26da7f2e635707554bb1cd486164638b3a2d11075c3787670683` |
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/history.json` | `3bc13c766f566ba2e0985bbb8d9a3f54a301cca1f450d3b6f7421b83f5df3491` |
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/summary.json` | `73baacd42654fa63b94b2323d5612098e55a870a0e81064d53880f80d342a2d7` |

## Verification

Commands:

```bash
python -m py_compile \
  2_experiment/forest_n3p/scripts/eval_bc_policy.py \
  2_experiment/forest_n3p/scripts/train_bc_policy.py

PYTHONPATH=2_experiment KMP_DUPLICATE_LIB_OK=TRUE python -m pytest \
  2_experiment/forest_n3p/tests/test_train_bc_policy_features.py \
  2_experiment/forest_n3p/tests/test_extract_oracle_demonstrations.py \
  -q

jq empty \
  2_experiment/forest_n3p/models/module2_rl_rs_bc_formal_v2_scalar/summary.json \
  2_experiment/forest_n3p/models/module2_rl_rs_bc_formal_v2_scalar/eval_rollout_step01.json \
  2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/summary.json
```

## Allowed Conclusions

- Formal-v2 scalar and obstacle-summary MLP baselines are current and source-bound.
- Obstacle-summary is the stronger MLP BC baseline under formal-v2.
- Neither MLP baseline is strong enough for planner insertion.

## Disallowed Conclusions

- Do not select PPO warm-start before patch+scalar CNN formal-v2 rerun.
- Do not compare these formal-v2 metrics numerically against formal-v1 as if the
  datasets shared the same map semantics.
- Do not claim PPO training or planner integration exists.

## Next Step

Run patch+scalar CNN bounded pilot on formal-v2 using the fixed profile-aware
map cache, then decide whether obstacle-summary or patch-CNN should seed PPO.
