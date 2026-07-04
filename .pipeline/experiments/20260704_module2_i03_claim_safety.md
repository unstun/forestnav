---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - .pipeline/experiments/20260704_module2_i01_method_algorithms.md
  - .pipeline/experiments/20260704_module2_i01_system_diagram.md
  - .pipeline/experiments/20260704_module2_i02_paper_table_protocol.md
  - .pipeline/experiments/20260704_module2_h02_formal_acceptance_audit.md
  - .pipeline/experiments/20260704_module2_f03_gate3_no_warm_formal_trial.md
  - .pipeline/experiments/20260704_module2_f02_6_warm_start_decision_packet.md
---

# I03 Claim Safety

## 直观结论

本轮完成 I03 claim safety guard。它的作用不是生成漂亮文字, 而是在写论文前先把哪些 claim 可以写、哪些 claim 只能条件性写、哪些 claim 必须禁止固定下来。

当前 formal performance claim 仍被阻塞, 因为 H02 不是 formal, H02 formal acceptance 未通过, H01 不是 ready, F02.6 仍 pending, PPO checkpoint/rows 仍缺。允许写的只有两类:

- 方法结构 claim: Module2 是 Hybrid A* 内部 learned analytic-expansion operator, 有 terminal RS certificate 和 primitive fallback, 不是 standalone RL global planner。
- no-warm failure claim: no-warm PPO Gate #3 formal branch 失败, terminal-RS success 29/64=0.453125, 低于 0.8 阈值。这个 claim 只限 no-warm branch, 不评价 obstacle-summary warm-start。

## 产物

- `2_experiment/forest_n3p/scripts/build_module2_claim_safety.py`
- `2_experiment/forest_n3p/tests/test_module2_claim_safety.py`
- `0_trials/module2_claim_safety/module2_claim_safety.json`
- `0_trials/module2_claim_safety/module2_claim_safety.md`

## 当前状态

- status: `blocked_formal_performance_claims`
- formal_performance_claim_allowed: `false`
- blockers:
  - `paper_tables_not_formal`
  - `h02_verdict_not_formal`
  - `h02_formal_acceptance_not_accepted`
  - `h01_manifest_not_ready`
  - `f02_6_warm_start_decision_pending`
  - `f02_6_decision_packet_pending`
  - `missing_module2_rl_rs_checkpoint`
  - `missing_ppo_result_rows`
  - `f02_6_pending`
  - `requires_dr_sun_approval`

## Allowed Claims

- `method_is_ha_star_analytic_operator`
  - claim: Module2 implements a learned analytic-expansion operator inside Hybrid A*, with terminal RS certification and primitive fallback.
  - qualifier: Do not describe it as an end-to-end RL global planner.
- `no_warm_gate3_formal_failure`
  - claim: No-warm PPO Gate #3 formal trial failed: terminal-RS success rate was 0.453125 over 64 episodes, below threshold 0.8.
  - qualifier: This does not evaluate obstacle-summary warm-start PPO and does not reject the whole RL-RS direction.

## Conditional Claims

- `formal_performance_improvement`: blocked until formal H02.
- `warm_start_effect`: blocked until F02.6 is approved and remote warm-start formal run/audit exists.

## Prohibited Claims

- `global_optimality`
- `completeness_enhancement`
- `rl_replaces_hybrid_astar`
- `universal_generalization`
- `warm_start_approved`

The builder also supports `--draft-text` audit and reports matched prohibited patterns.

## 验证

- Memory retrieval: confirmed I03 claim safety is appropriate after I02, but cannot replace F02.6/H02.
- ACE: `mcp__auggie__codebase-retrieval` returned `402 Payment Required`; used exact file reads.
- RED: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_claim_safety.py` first failed on missing builder.
- GREEN targeted: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_claim_safety.py` -> `1 passed in 0.07s`.
- Adjacent: `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_claim_safety.py 2_experiment/forest_n3p/tests/test_module2_paper_tables.py 2_experiment/forest_n3p/tests/test_module2_method_algorithms.py 2_experiment/forest_n3p/tests/test_module2_system_diagram.py` -> `4 passed in 0.13s`.
- Syntax: `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_claim_safety.py`.
- Artifact audit: `module2_claim_safety_artifact=ok`.
- 2026-07-04 H02 acceptance integration: `--h02-formal-acceptance` 已接入; 即使 paper tables/H01/F02.6 都看似 formal, 只要 H02 acceptance blocked, I03 仍输出 `blocked_formal_performance_claims`; I02/I03 targeted `4 passed in 0.12s`。

## 边界

- This does not approve F02.6.
- This does not create a PPO checkpoint.
- This does not make H01/H02 formal-ready.
- This does not allow formal performance improvement claims.
- Formal PPO training/checkpoint production must run on `gpu3070ti-relay`, not locally.
