---
date: 2026-07-03
status: d02_2_device_and_rollout_budget_complete
origin: codex+experiment
reviewed: false
task: Module2 D02.2
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_d02_policy_forward_budget.md
source_head: 4aa9ff48
execution_host: MacBook-Pro.local + gpu3070ti-relay
---

# Module2 D02.2 Device Forward and Rollout Collision Budget

## 直观结论

D02.2 把 D02.1 的本机 CPU forward-only 预算补成了更接近真实 operator 的成本账:

1. 本机 CPU/MPS 跑同一组 forward benchmark。
2. 远端 3070 Ti 跑 CUDA forward benchmark。
3. 基于 C01 dedup RS failure nodes 跑 rollout sampling + collision checking + terminal RS proxy。

结果说明: 神经前向和 rollout collision 本身仍有毫秒预算空间, 但这仍不是 Gate #1 通过。Gate #1 还必须回答更硬的问题: policy rollout 是否能以足够高成功率减少 HA* search expansions / timeout, 否则再便宜的 rollout 也只是额外开销。

## Commands

Local CPU/MPS forward:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_policy_forward_budget \
  --output-dir 0_trials/module2_cost_accounting/d02_policy_forward_device_budget_local \
  --models tiny_mlp,small_cnn,compact_cnn_mlp \
  --batch-sizes 1,8,32 \
  --patch-cells auto,margin_auto \
  --warmup-iterations 100 \
  --timed-iterations 500 \
  --threads 1 \
  --devices cpu,mps \
  --allow-duplicate-openmp \
  --source-head 4aa9ff48
```

Remote CUDA forward on 3070 Ti:

```bash
rsync -az --delete --exclude '__pycache__' \
  2_experiment/forest_n3p/ gpu3070ti-relay:~/ForestNav/2_experiment/forest_n3p/

ssh gpu3070ti-relay 'cd ~/ForestNav && python3 -m venv .venv_d02_cuda && \
  .venv_d02_cuda/bin/python -m pip install --upgrade pip && \
  .venv_d02_cuda/bin/python -m pip install torch pandas pyarrow'

ssh gpu3070ti-relay 'cd ~/ForestNav && PYTHONPATH=2_experiment \
  .venv_d02_cuda/bin/python -m forest_n3p.scripts.run_policy_forward_budget \
  --output-dir 0_trials/module2_cost_accounting/d02_policy_forward_device_budget_cuda \
  --models tiny_mlp,small_cnn,compact_cnn_mlp \
  --batch-sizes 1,8,32 \
  --patch-cells auto,margin_auto \
  --warmup-iterations 100 \
  --timed-iterations 500 \
  --threads 1 \
  --devices cuda \
  --source-head 4aa9ff48'
```

Rollout collision budget:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_rollout_collision_budget \
  --output-dir 0_trials/module2_cost_accounting/d02_rollout_collision_budget \
  --max-records 24 \
  --rollout-step-counts 1,8,16,32 \
  --checker-types grid,edt \
  --timed-iterations 100 \
  --source-head 4aa9ff48
```

## Artifacts

Forward device artifacts:

- `0_trials/module2_cost_accounting/d02_policy_forward_device_budget_local/summary.json`
- `0_trials/module2_cost_accounting/d02_policy_forward_device_budget_local/forward_budget_records.parquet`
- `0_trials/module2_cost_accounting/d02_policy_forward_device_budget_local/forward_budget_samples.parquet`
- `0_trials/module2_cost_accounting/d02_policy_forward_device_budget_cuda/summary.json`
- `0_trials/module2_cost_accounting/d02_policy_forward_device_budget_cuda/forward_budget_records.parquet`
- `0_trials/module2_cost_accounting/d02_policy_forward_device_budget_cuda/forward_budget_samples.parquet`
- `0_trials/module2_cost_accounting/d02_policy_forward_device_budget_cuda/remote_environment.txt`
- `0_trials/module2_cost_accounting/d02_policy_forward_device_budget_cuda/remote_5070_oom.txt`

Rollout collision artifacts:

- `0_trials/module2_cost_accounting/d02_rollout_collision_budget/summary.json`
- `0_trials/module2_cost_accounting/d02_rollout_collision_budget/rollout_collision_records.parquet`
- `0_trials/module2_cost_accounting/d02_rollout_collision_budget/rollout_collision_samples.parquet`

Artifact counts:

| Artifact | Aggregate rows | Sample rows |
|---|---:|---:|
| Local CPU/MPS forward | 36 | 18000 |
| 3070 Ti CUDA forward | 18 | 9000 |
| Rollout collision | 192 | 19200 |

## Device Evidence

3070 Ti environment:

```text
hostname: ubuntu-OMEN-by-HP-Laptop-17-ck1xxx
user: ubuntu
GPU: NVIDIA GeForce RTX 3070 Ti Laptop GPU, 8192 MiB, driver 595.71.05
python: /home/ubuntu/ForestNav/.venv_d02_cuda/bin/python
torch: 2.12.1+cu130
pandas: 3.0.3
pyarrow: 24.0.0
```

5070 Ti boundary:

- 5070 Ti was reachable, but not usable for this run.
- CUDA forward failed before benchmarking with `RuntimeError: CUDA error: out of memory`.
- `nvidia-smi` showed one Python process using about `15586 MiB`, leaving about `31 MiB` free.
- Evidence: `0_trials/module2_cost_accounting/d02_policy_forward_device_budget_cuda/remote_5070_oom.txt`

## Forward Batch=1 Results

D01.2 reference:

| Metric | Value |
|---|---:|
| Dang multi-RS attempt p50 | `0.814 ms` |
| Dang multi-RS attempt p95 | `2.025 ms` |

Batch=1 forward p50/p95:

| Device | Model | Shape | p50 ms | p95 ms | p50 / D01 p50 |
|---|---|---|---:|---:|---:|
| CPU | `tiny_mlp` | `annulus_auto` | 0.011 | 0.013 | 0.013 |
| CPU | `compact_cnn_mlp` | `annulus_auto` | 0.117 | 0.140 | 0.144 |
| CPU | `small_cnn` | `annulus_auto` | 0.161 | 0.208 | 0.198 |
| CPU | `compact_cnn_mlp` | `footprint_margin_auto` | 0.392 | 0.540 | 0.482 |
| CPU | `small_cnn` | `footprint_margin_auto` | 0.514 | 0.637 | 0.631 |
| MPS | `tiny_mlp` | `annulus_auto` | 0.259 | 1.113 | 0.318 |
| MPS | `compact_cnn_mlp` | `annulus_auto` | 0.398 | 2.065 | 0.488 |
| MPS | `small_cnn` | `annulus_auto` | 0.445 | 2.127 | 0.546 |
| CUDA 3070 Ti | `tiny_mlp` | `annulus_auto` | 0.037 | 0.039 | 0.046 |
| CUDA 3070 Ti | `compact_cnn_mlp` | `annulus_auto` | 0.102 | 0.109 | 0.126 |
| CUDA 3070 Ti | `small_cnn` | `annulus_auto` | 0.127 | 0.145 | 0.156 |
| CUDA 3070 Ti | `compact_cnn_mlp` | `footprint_margin_auto` | 0.119 | 0.124 | 0.146 |
| CUDA 3070 Ti | `small_cnn` | `footprint_margin_auto` | 0.137 | 0.154 | 0.168 |

Interpretation:

- CPU remains a valid low-jitter batch=1 baseline.
- MPS has high small-batch synchronization overhead and p95 jitter; do not use it as the main timing device for paper claims.
- CUDA 3070 Ti makes CNN patch size almost irrelevant at batch=1 for these tiny networks, but deployment value depends on whether planner integration can actually batch or tolerate GPU transfer/sync overhead.

## Rollout Collision Results

Rollout benchmark source:

- Input: `0_trials/module2_oracle_shape/rs_failure_nodes_dedup.parquet`
- Selected: first 24 non-colliding Complex/Extreme RS failure-node states under validation maps
- Rollout action proxy: deterministic forward-only steering sequence
- Action step: `0.3 m`
- Collision sampling step: `0.1 m`
- Checkers: `GridFootprintChecker`, `EDTCollisionChecker`
- Terminal RS proxy: `generate_reeds_shepp_path` + `sample_reeds_shepp_path` + Grid collision check

Mean across 24 source rows:

| Checker | Rollout steps | Rollout p50 ms | Rollout p95 ms | Candidate total p50 ms | Candidate total p95 ms | Rollout collision rate | Terminal RS success rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| EDT | 1 | 0.008 | 0.011 | 0.080 | 0.099 | 0.208 | 0.000 |
| EDT | 8 | 0.033 | 0.040 | 0.123 | 0.146 | 0.583 | 0.000 |
| EDT | 16 | 0.058 | 0.068 | 0.137 | 0.162 | 0.625 | 0.208 |
| EDT | 32 | 0.096 | 0.111 | 0.207 | 0.242 | 0.875 | 0.667 |
| Grid | 1 | 0.014 | 0.018 | 0.087 | 0.104 | 0.208 | 0.000 |
| Grid | 8 | 0.050 | 0.061 | 0.141 | 0.169 | 0.583 | 0.000 |
| Grid | 16 | 0.082 | 0.099 | 0.161 | 0.196 | 0.625 | 0.208 |
| Grid | 32 | 0.129 | 0.152 | 0.239 | 0.281 | 0.875 | 0.667 |

Interpretation:

- Rollout sampling + collision checking is not the dominant cost at this scale.
- Terminal RS proxy dominates the candidate total in this deterministic microbenchmark.
- EDT checker is faster than Grid checker, but using EDT in the final operator requires explicit train/inference checker consistency.
- The collision/success rates here are not policy quality metrics. They reflect a fixed steering proxy from failure nodes.

## Conservative Combined Cost Envelope

Forward + Grid rollout candidate total, batch=1:

| Device/model/shape | Forward p50 ms | Grid 32-step candidate p50 ms | Combined p50 ms | D01 attempt p50 ms |
|---|---:|---:|---:|---:|
| CPU `compact_cnn_mlp` 128-cell | 0.392 | 0.239 | 0.631 | 0.814 |
| CPU `small_cnn` 128-cell | 0.514 | 0.239 | 0.753 | 0.814 |
| CUDA `compact_cnn_mlp` 128-cell | 0.119 | 0.239 | 0.358 | 0.814 |
| CUDA `small_cnn` 128-cell | 0.137 | 0.239 | 0.376 | 0.814 |

This is a cost-plausibility envelope, not a performance claim. It shows D02 should not be killed on pure compute grounds yet. It does not show that an RL-RS rollout will reduce total HA* search time.

## Verification

Commands:

```bash
PYTHONPATH=2_experiment python -m py_compile \
  2_experiment/forest_n3p/scripts/run_policy_forward_budget.py \
  2_experiment/forest_n3p/scripts/run_rollout_collision_budget.py

PYTHONPATH=2_experiment pytest \
  2_experiment/forest_n3p/tests/test_policy_forward_budget.py \
  2_experiment/forest_n3p/tests/test_rollout_collision_budget.py \
  -q
```

Results:

- `py_compile`: pass
- `pytest`: `4 passed in 0.45s`
- artifact checks: local forward `36/18000`, CUDA forward `18/9000`, rollout collision `192/19200`

## Allowed Conclusions

- D02.2 closes the missing forward-device comparison and adds a first real rollout collision cost account.
- Compute cost alone does not currently disqualify compact CNN or small CNN operator candidates.
- CPU batch=1 is still a credible local baseline; CUDA is faster for CNN but requires integration proof.
- MPS is not attractive for small-batch planner timing on this Mac.

## Disallowed Conclusions

- Do not claim Gate #1 is passed.
- Do not claim RL-RS is faster than Dang multi-RS.
- Do not claim deterministic steering proxy success/collision rates represent a trained policy.
- Do not claim 5070 Ti CUDA results exist; that host was occupied and OOM for this run.

## Next Step

Proceed to D02.3 Gate #1:

1. combine D01/D02.1/D02.2 into a formal compute gate table;
2. decide whether compute budget permits E01 environment implementation;
3. if not failed, explicitly state the remaining risk is policy effectiveness/search reduction, not raw forward/collision cost.
