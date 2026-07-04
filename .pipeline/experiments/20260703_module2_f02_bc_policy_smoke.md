---
date: 2026-07-03
status: f02_1_bc_preview_smoke_complete
origin: codex+code+experiment
reviewed: false
task: Module2 F02.1
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_f01_dataset_manifest.md
source_head: 45034d43ce5f23da82a2f7d7eb80da8caeea0f3c
execution_host: MacBook-Pro.local
---

# Module2 F02.1 BC Policy Preview Smoke

## 直观结论

F02.1 已经把 F01 preview demonstrations 接到一个可复跑的 BC 训练脚本上,
并实际跑出了 checkpoint、训练曲线、动作误差和闭环 rollout 指标。

这一步的结论很克制: 训练链路是真的, 但效果还不能当正式 baseline。动作回归
MAE 为 0.147 rad, 可是闭环只在 5 个 held-out source rows 中成功 2 个,
碰撞 3 个。也就是说, 单看 action MSE 会过度乐观; 必须继续保留 closed-loop
terminal-RS-success 作为 F02/F03 的主指标之一。

## Code Changes

Changed files:

- `2_experiment/forest_n3p/scripts/train_bc_policy.py`

Implemented behavior:

| Behavior | Implementation |
|---|---|
| Input | F01 preview parquet + manifest |
| Split | group split by `source_row_index` to avoid adjacent-step leakage |
| Model | scalar-observation MLP, output clipped by `max_steer * tanh(...)` |
| Loss | steering regression MSE |
| Checkpoint | state dict + scalar config + feature mean/std as safe Python lists |
| Evaluation | validation action metrics + closed-loop rollout over held-out source rows |
| Rollout terminal | success only when terminal RS succeeds from the policy rollout state |
| Collision accounting | shared local collision check during rollout |

## Training Run

Command:

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

Local note:

- `--allow-duplicate-openmp` was required for this Mac smoke because bare Torch
  import hit `OMP: Error #15 ... libomp.dylib already initialized`.
- This is a local smoke workaround, not a paper timing condition.

## Outputs

| File | SHA-256 |
|---|---|
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_preview_smoke/summary.json` | `48f8f99b4c0d8a083872bbd9dc1bc1c8a25ee70a073d7c84d60719ae831fdb86` |
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_preview_smoke/history.json` | `b61bab1743419aef4a53818fd9e3b120084f9ab009b1f12b81515532d714d1ca` |
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_preview_smoke/checkpoint.pt` | `36a95f5a40835c4356e65e42258d1367b1555951c9a5be5d91279af63d4585a7` |

## Metrics

Dataset:

- total rows: 1109
- train rows: 828
- validation rows: 281
- train source rows: 15
- validation source rows: 5

Action metrics:

- best epoch: 29
- epochs ran: 30
- validation MSE: 0.044572457671165466
- validation MAE rad: 0.14736425876617432
- validation max absolute error rad: 0.7077865600585938

Closed-loop metrics:

| Metric | Value |
|---|---:|
| held-out episodes | 5 |
| terminal RS success | 2 |
| collision | 3 |
| truncated | 0 |
| runtime error | 0 |
| terminal RS success rate | 0.4 |
| collision rate | 0.6 |

Per-episode result:

| source row | query id | result | steps | failure reason |
|---:|---|---|---:|---|
| 2 | `complex_s00_q0000` | success | 22 | n/a |
| 4 | `complex_s00_q0000` | collision | 5 | collision |
| 11 | `complex_s00_q0000` | success | 14 | n/a |
| 12 | `complex_s00_q0000` | collision | 1 | collision |
| 17 | `complex_s00_q0000` | collision | 2 | collision |

## Verification

Commands:

```bash
KMP_DUPLICATE_LIB_OK=TRUE python - <<'PY'
import torch
path = "2_experiment/forest_n3p/models/module2_rl_rs_bc_preview_smoke/checkpoint.pt"
ckpt = torch.load(path, map_location="cpu")
print("checkpoint_load_ok")
print(sorted(ckpt.keys()))
PY

PYTHONPATH=2_experiment python -m py_compile \
  2_experiment/forest_n3p/scripts/extract_oracle_demonstrations.py \
  2_experiment/forest_n3p/scripts/train_bc_policy.py \
  2_experiment/forest_n3p/rl_rs/*.py \
  2_experiment/forest_n3p/scripts/run_policy_forward_budget.py \
  2_experiment/forest_n3p/scripts/run_rollout_collision_budget.py

PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_policy_forward_budget.py \
  2_experiment/forest_n3p/tests/test_rollout_collision_budget.py \
  2_experiment/forest_n3p/tests/test_rl_rs_api.py \
  -q

git diff --check
```

Results before record commit:

- checkpoint load: pass
- `py_compile`: pass
- `pytest`: `24 passed`
- `git diff --check`: pass

## Allowed Conclusions

- F02.1 has a real BC training script and a reproducible preview smoke artifact.
- The script reports closed-loop terminal-RS-success, not only action loss.
- The checkpoint can be loaded with default PyTorch safe loading behavior.

## Disallowed Conclusions

- Do not claim this is the formal BC baseline.
- Do not claim BC is good enough for planner insertion.
- Do not claim PPO training has started.
- Do not claim RL-RS planner integration exists.
- Do not use this smoke timing as paper timing evidence.

## Next Step

Proceed to F02.2 only after deciding whether the formal BC baseline should use:

- a larger extracted oracle corpus;
- balanced oracle A/B rows;
- stronger observation features than scalar-only;
- or an explicit statement that scalar-only BC is a weak lower-bound baseline.
