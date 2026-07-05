# Module2 Formal Gate Protocol Lane Matrix

This file is a formal-gate lane evidence artifact, not paper result material.

## Gate Summary

- current_formal_decision: `fail`
- current_failure_mode: `threshold_failure`
- terminal_rs_success_rate: `0.53125`
- required_success_threshold: `0.8`
- new_success_training_allowed_now: `False`
- remote_training_allowed_now: `False`
- local_training_allowed_now: `False`
- formal_claim_allowed_now: `False`

## Lane Matrix

| lane | claim_scope | training_allowed_now |
|---|---|---:|
| `stronger_obstacle_summary_warm_start` | direct PPO replacement attempt remains possible only if the new contract preserves the replacement claim boundary | `False` |
| `full_patch_cnn_policy` | direct PPO replacement claim changes substantially and must be re-registered as an observation/architecture delta | `False` |
| `hybrid_ppo_analytic_fallback` | claim likely changes from PPO replacing RS to PPO assisting/selecting/recovering around analytic planning | `False` |
| `stop_or_reframe_module2_claim` | no new success-attempt training; use failure as negative evidence or reframe the module2 contribution | `False` |

## Cross-Lane Invariants
- `no_local_training`: Local PPO training output is not formal evidence for any lane.
- `contract_before_new_success_training`: Any new success-attempt remote training requires an approved or frozen new/revised contract first.
- `failed_checkpoint_not_success_evidence`: The failed warm-start checkpoint can be negative evidence only, not a success checkpoint.
- `h02_before_paper_results`: Paper result material requires H02 formal_output_accepted=true and paper_result_input_allowed=true.

## Audit

- status: `formal_gate_protocol_lane_matrix_ready`
- audit_issue_count: `0`
