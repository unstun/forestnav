---
date: 2026-07-03
status: gate1_not_failed_preimplementation_compute_gate
origin: codex+experiment
reviewed: false
task: Module2 D02.3
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_records:
  - .pipeline/experiments/20260703_module2_d01_cost_distribution.md
  - .pipeline/experiments/20260703_module2_d02_policy_forward_budget.md
  - .pipeline/experiments/20260703_module2_d02_device_and_rollout_budget.md
source_head: 66d82b63
execution_host: MacBook-Pro.local
---

# Module2 D02.3 Gate #1 Cost Accounting Decision

## 直观结论

D02.3 的判定是:

> `gate1_not_failed_preimplementation_compute_gate`

意思不是“Gate #1 通过”, 更不是“RL-RS 一定更快”。准确含义是:

- 以 D01/D02 当前证据看, 神经前向 + rollout collision + terminal RS proxy 没有大到足以直接杀死方向。
- 可以进入 E01 环境 API/观测/动作/终止条件实现, 因为 compute 预算不是当前第一阻塞。
- 但 Contract 中真正的 Gate #1 仍要等 trained/integrated operator 跑端到端评测: 如果节点数没有显著减少, 这些额外开销仍会让总时间不降反升。

## Contract Anchor

Approved Contract: `.pipeline/contracts/module2-ppo-funnel-expansion.md`

Relevant lines in the contract:

- 成功需要总扩展节点数中位数缩减 >= 50%。
- 成功需要端到端规划时间中位数缩减 >= 30%。
- Gate #1 failure: PPO 单步/多步推理耗时过大, 完全吃掉减少节点带来的时间收益, 端到端时间未下降。

Current D02.3 can only judge pre-implementation compute plausibility. It cannot judge trained policy effectiveness or end-to-end time reduction yet.

## Evidence Inputs

### D01.2 Dang Multi-RS Cost Baseline

Source: `0_trials/module2_cost_accounting/d01_analytic_cost_distribution/summary.json`

| Metric | Value |
|---|---:|
| Dang multi-RS attempt p50 | `0.814 ms` |
| Dang multi-RS attempt p95 | `2.025 ms` |
| Dang multi-RS attempt p99 | `2.829 ms` |
| Collision-check component p50 | `0.360 ms` |
| Collision-check component p95 | `1.444 ms` |
| Analytic / total plan time ratio | `33.2%` |

Interpretation:

- D01 gives the per-attempt budget reference.
- It does not by itself prove any RL operator saves time.

### D02.2 Forward + Rollout Proxy

Source:

- `0_trials/module2_cost_accounting/d02_policy_forward_device_budget_local/`
- `0_trials/module2_cost_accounting/d02_policy_forward_device_budget_cuda/`
- `0_trials/module2_cost_accounting/d02_rollout_collision_budget/`

Conservative Grid checker, 32-step rollout candidate total:

| Component | p50 ms | p95 ms |
|---|---:|---:|
| Grid 32-step rollout + terminal RS proxy | 0.239 | 0.281 |

Combined p50/p95 envelopes:

| Candidate | Forward p50 | Forward p95 | + Grid 32-step p50 | + Grid 32-step p95 | D01 attempt p50/p95 |
|---|---:|---:|---:|---:|---:|
| CPU `compact_cnn_mlp`, 128-cell | 0.392 | 0.540 | 0.631 | 0.821 | 0.814 / 2.025 |
| CPU `small_cnn`, 128-cell | 0.514 | 0.637 | 0.753 | 0.918 | 0.814 / 2.025 |
| CUDA `compact_cnn_mlp`, 128-cell | 0.119 | 0.124 | 0.358 | 0.404 | 0.814 / 2.025 |
| CUDA `small_cnn`, 128-cell | 0.137 | 0.154 | 0.376 | 0.435 | 0.814 / 2.025 |

Interpretation:

- Even with 128-cell patch and Grid checker, the compute proxy remains below D01 p50/p95 for batch=1.
- CUDA has more headroom, but relying on CUDA inside a sequential planner still needs integration proof.
- MPS is not recommended for this path because small-batch p95 jitter is high.

## Decision

Gate #1 pre-implementation compute failure is **not triggered**.

Allowed next action:

- Proceed to E01 environment API implementation.

Required guardrails for E01:

1. Use the same Ackermann propagation / `sample_constant_steer_motion` semantics as the planner.
2. Use the same collision checker family as planner/evaluation, or explicitly record checker differences.
3. Define success as terminal RS-connectable, not simply “near goal”.
4. Log `nn_forward_time_s`, `rollout_collision_time_s`, `terminal_rs_time_s`, `rollout_steps`, `rollout_collision_checks`, `terminal_rs_success`, and fallback reason.
5. Do not claim speedup until planner-integrated paired evaluation proves end-to-end time drops.

## Why This Is Not A Full Pass

The Contract's real Gate #1 includes end-to-end time. D02.3 lacks:

- trained PPO or BC policy;
- actual `RlRsFunnelOperator`;
- integration with `_try_analytic_expansion()`;
- measured reduction in HA* expansions;
- paired wall-clock evaluation against Dang multi-RS.

Therefore the correct statement is:

- Compute budget is plausible enough to continue.
- Final Gate #1 remains open until integrated evaluation.

## Disallowed Conclusions

- Do not claim RL-RS is faster than Dang multi-RS.
- Do not claim PPO is necessary.
- Do not claim the final architecture is selected.
- Do not use deterministic rollout collision/success rates as policy quality evidence.
- Do not move to PPO training before E01/E02/E03 environment semantics and tests exist.

## Next Step

Proceed to E01.1:

- create `2_experiment/forest_n3p/rl_rs/` package;
- define environment API skeleton with planner-compatible context/result types;
- add tests for reset/step surface before reward or PPO code.
