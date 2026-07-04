# Module2 Paper Tables Protocol

- Status: `blocked_no_formal_h02_data`
- Formal claim allowed: `False`
- Local training allowed: `False`
- Remote training resource: `gpu3070ti-relay`

This artifact is not formal unless `formal_claim_allowed=true`.

## Blockers

- h02_verdict_not_formal
- h01_manifest_not_ready
- f02_6_warm_start_decision_pending
- f02_6_decision_packet_pending
- missing_module2_rl_rs_checkpoint
- missing_ppo_result_rows

## I02.1 Main Table Preview

- status: `preview_not_formal`

| method | success | timeout | time p50/p95 | expansions p50/p95 | path inflation p50 | clearance p50 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| bc_analytic_operator | 1 | 0 | 0.18/1.905 | 13/571.9 | NA | 0.1909 |
| ha_dang_multi_rs | 1 | 0 | 0.1678/0.5217 | 31/659.2 | NA | 0.1909 |
| ha_no_analytic | 1 | 0 | 0.4084/0.5821 | 658/1065 | NA | 0.07062 |
| ha_single_rs | 1 | 0 | 0.1715/0.5745 | 61/662.2 | NA | 0.1736 |
| mlp | 1 | 0 | 0.2034/0.5233 | 31/659.2 | NA | 0.1909 |

## I02.2 Ablation Table

- status: `blocked_missing_formal_data`
- planned: `occupancy_only_vs_occupancy_plus_edt`
- planned: `bc_vs_ppo`
- planned: `terminal_rs_on_vs_off`
- planned: `action_mask_on_vs_off`
- planned: `forward_only_vs_forward_reverse_if_enabled`

## I02.3 Failure Analysis Preview

- status: `preview_not_formal`

| method | failures | timeout | collision | terminal RS | oscillation | oracle no-solution | other |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| bc_analytic_operator | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ha_dang_multi_rs | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ha_no_analytic | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ha_single_rs | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| mlp | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Claim Boundaries

- Do not use preview_not_formal rows as paper results.
- Main paper claims require H02 formal_acceptance=true, H01 formal-ready status, frozen metric protocol, and no missing PPO checkpoint blocker.
- Use records.csv.total_time_s for timing claims; planner_time_s is diagnostic only.
- Use paired Wilcoxon for total_time_s and total_expansions and bootstrap CI for success/failure/timeout-rate differences.
- PPO formal training and checkpoint production must run on gpu3070ti-relay or another explicitly approved remote GPU, not locally.