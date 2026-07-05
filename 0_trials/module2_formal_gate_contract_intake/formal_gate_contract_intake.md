# Module2 Formal Gate Contract Intake

This file is a formal-gate decision intake artifact, not paper result material.

## Current Failed Run

- formal_decision: `fail`
- failure_mode: `threshold_failure`
- terminal_rs_success_rate: `0.53125`
- required_success_threshold: `0.8`
- threshold_deficit: `0.26875`

## Gate Boundaries

- new_success_training_allowed_now: `False`
- local_training_allowed_now: `False`
- formal_claim_allowed_now: `False`
- h02_status: `blocked_formal_output_acceptance`
- h02_blockers: `h02_verdict_not_formal, gate3_formal_audit_not_passed, h02_scale_below_h01_manifest, missing_ppo_result_rows`

## Required Contract Decisions

| field | status | prompt |
|---|---|---|
| `protocol_lane` | `awaiting_dr_sun_decision` | Choose the next protocol lane: stronger warm-start, full patch-CNN policy, hybrid PPO+analytic fallback, or abandon PPO replacement. |
| `hypothesis` | `awaiting_dr_sun_decision` | Lock the next-round hypothesis before training. |
| `success_signal` | `awaiting_dr_sun_decision` | Lock the success signal before training. |
| `failure_signal` | `awaiting_dr_sun_decision` | Lock a failure signal that is not merely the negation of success. |
| `training_budget_and_seed_policy` | `awaiting_dr_sun_decision` | Lock budget and seed policy before training. |
| `protocol_delta` | `awaiting_dr_sun_decision` | Lock every protocol delta from the failed warm-start run. |
| `h01_h02_acceptance_plan` | `awaiting_dr_sun_decision` | Lock how the next run will become paper-eligible if it passes. |

## Candidate Protocol Lanes

| lane | status | change |
|---|---|---|
| `stronger_obstacle_summary_warm_start` | `candidate_requires_contract` | keep compact obstacle-summary policy family but strengthen warm-start dataset, curriculum, or PPO stabilization protocol |
| `full_patch_cnn_policy` | `candidate_requires_contract` | move from compact summary features toward a spatial patch/CNN observation policy |
| `hybrid_ppo_analytic_fallback` | `candidate_requires_contract` | treat PPO as a learned selector or recovery layer instead of direct RS replacement |
| `stop_or_reframe_module2_claim` | `candidate_requires_contract` | record the formal failure and stop pursuing PPO replacement under the current module2 claim |

## Invalid Shortcuts
- start another PPO success attempt from the failed checkpoint without a new or revised contract
- change reward, curriculum, architecture, observations, budget, seed policy, or threshold in code without pre-registration
- treat blocked H02 smoke rows as formal PPO result rows
- use local PPO training output as formal gate evidence
- write a paper success table before H02 formal_output_accepted=true

## Audit

- status: `formal_gate_contract_intake_ready_for_dr_sun`
- audit_issue_count: `0`
