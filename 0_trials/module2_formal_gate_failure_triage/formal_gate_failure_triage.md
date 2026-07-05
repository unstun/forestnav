# Module2 Formal Gate Failure Triage

This file is a gate-control artifact, not paper result material.

## Gate3 Outcome

- formal_decision: `fail`
- evaluator_decision: `fail`
- episodes: `64`
- terminal_rs_success_rate: `0.53125`
- required_success_threshold: `0.8`
- threshold_deficit: `0.26875`
- failure_mode: `threshold_failure`

## Deliverable Status

| category | status | present | missing |
|---|---:|---:|---:|
| `training` | `complete` | `3` | `0` |
| `evaluation` | `complete` | `2` | `0` |
| `acceptance` | `complete` | `3` | `0` |
| `formal_acceptance` | `blocked` | `1` | `1` |

## Missing Formal Acceptance
- `formal_acceptance:h02_formal_output_acceptance`: h02_verdict_not_formal, gate3_formal_audit_not_passed, h02_scale_below_h01_manifest, missing_ppo_result_rows

## Next Gate

- status: `requires_protocol_decision_before_new_success_attempt`
- new_or_revised_contract_required_before_new_training: `True`
- same_contract_success_rerun_allowed: `False`

## Boundaries
- This triage is a formal-gate operations artifact, not a paper result table, appendix, or success claim.
- The current warm-start PPO Gate3 run is a threshold failure and must not be reframed as PPO replacing RS successfully.
- New training intended to overturn this failure requires a new or revised Research Contract before execution.
- Local PPO training remains disallowed; remote-only evidence must keep checkpoint, eval, audit, and hash provenance.

## Audit

- status: `formal_gate_failure_triage_ready`
- audit_issue_count: `0`
