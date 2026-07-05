# Module2 Formal Gate Next-Round Requirements

This file is a formal-gate planning artifact, not paper result material.

## Current Failed Run

- formal_decision: `fail`
- failure_mode: `threshold_failure`
- episodes: `64`
- terminal_rs_success_rate: `0.53125`
- required_success_threshold: `0.8`
- threshold_deficit: `0.26875`

## Current Run Artifact Closure

- training_missing: `0`
- evaluation_missing: `0`
- acceptance_missing: `0`
- formal_acceptance_missing: `1`

## Blocked Formal Acceptance

- h02_status: `blocked_formal_output_acceptance`
- formal_output_accepted: `False`
- paper_result_input_allowed: `False`
- blockers: `h02_verdict_not_formal, gate3_formal_audit_not_passed, h02_scale_below_h01_manifest, missing_ppo_result_rows`

## Next-Round Requirements

| category | requirement | status | required_before |
|---|---|---|---|
| `contract` | `new_or_revised_research_contract` | `missing_required_before_new_training` | `new_success_training` |
| `training` | `new_remote_ppo_checkpoint_bundle` | `blocked_until_contract` | `new_gate3_formal_audit` |
| `evaluation` | `new_formal_gate3_eval_bundle` | `blocked_until_new_checkpoint` | `new_gate3_formal_audit` |
| `acceptance` | `new_gate3_audit_and_hash_acceptance` | `blocked_until_new_eval` | `h02_formal_output_acceptance` |
| `formal_acceptance` | `h02_formal_output_acceptance` | `blocked_until_new_gate3_pass` | `paper_result_material` |

## Boundaries
- This artifact is a formal-gate planning artifact, not a paper result table or appendix.
- The failed warm-start PPO Gate3 checkpoint is negative formal evidence, not a successful PPO replacement for RS.
- The failed checkpoint, failed audit, and smoke H02 rows are invalid substitutes for the next success-attempt evidence.
- Any new remote training intended to overturn this failure requires a new or revised Research Contract first.
- Local PPO training remains disallowed.

## Audit

- status: `formal_gate_next_round_requirements_ready`
- audit_issue_count: `0`
