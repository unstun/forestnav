# Module2 Mainline Formal Gate State Audit

This file checks that the long-term Module2 mainline task book mirrors the current formal-gate state. It is not a training run, remote preflight, formal evaluation, or paper result.

- status: `mainline_formal_gate_state_consistent_blocked`
- audit_issue_count: `0`
- expected_next_action_id: `None`
- expected_next_action_mentioned: `False`
- total_missing_deliverables: `1`
- mainline_missing_deliverable_mention_count: `0`
- f02_6_decision_evidence_matrix_summary: `{'present': True, 'matrix_id': 'module2_f02_6_decision_evidence_matrix', 'status': 'ready_for_dr_sun_decision_not_authorization', 'route_count': 2, 'route_decisions': ['approve_obstacle_summary_warm_start', 'reject_obstacle_summary_warm_start'], 'required_evidence_count': 7, 'satisfied_required_evidence_count': 7, 'missing_required_evidence_count': 0, 'missing_required_evidence_ids': [], 'source_issue_count': 0, 'global_invalid_substitute_count': 4, 'authorization_flags': {'current_authorization_allowed_now': False, 'remote_preflight_allowed_now': False, 'remote_training_allowed_now': False, 'local_training_allowed_now': False, 'formal_claim_allowed_now': False, 'paper_result_material_allowed_now': False}, 'evidence_counts_by_route': {'approve_obstacle_summary_warm_start': 4, 'reject_obstacle_summary_warm_start': 3}, 'invalid_substitute_counts_by_route': {'approve_obstacle_summary_warm_start': 4, 'reject_obstacle_summary_warm_start': 4}}`
- f02_6_decision_evidence_matrix_mentioned: `True`
- f02_6_decision_evidence_matrix_status_mentioned: `True`
- proof_summary_chain_status: `formal_gate_proof_summary_chain_consistent_blocked`
- proof_summary_handoff_single_next_action_consistency: `{'row_count': 3, 'consistent_row_count': 3}`
- executes_commands: `False`
- runs_training: `False`
- runs_remote_preflight: `False`
- formal_claim_allowed: `False`

## Audit Issues

- none

## Missing Formal Deliverables

- `formal_acceptance:h02_formal_output_acceptance`: artifact_id=`h02_formal_output_acceptance`, mentioned=`True`, mentioned_in_current_section=`True`

## F02.6 Decision Evidence Matrix

- matrix_id: `module2_f02_6_decision_evidence_matrix`
- status: `ready_for_dr_sun_decision_not_authorization`
- route_count: `2`
- required_evidence_count: `7`
- missing_required_evidence_count: `0`
- authorization_flags: `{'current_authorization_allowed_now': False, 'remote_preflight_allowed_now': False, 'remote_training_allowed_now': False, 'local_training_allowed_now': False, 'formal_claim_allowed_now': False, 'paper_result_material_allowed_now': False}`

## Current Boundary Tokens

- `local training`: mentioned=`True`
- `remote preflight`: mentioned=`True`
- `remote training`: mentioned=`True`
- `formal claim`: mentioned=`True`
- `paper-result material`: mentioned=`True`
- `gpu3070ti-relay`: mentioned=`True`

## Claim Boundaries

- This audit only checks that the long-term mainline task book mirrors the current formal-gate state.
- It does not execute commands, run local training, run remote preflight, run remote PPO training, evaluate PPO, pull back artifacts, or write paper results.
- A consistent blocked audit does not prove PPO has replaced RS in formal evaluation.
- Formal PPO-vs-RS performance claims still require the missing training, evaluation, acceptance, and H01/H02 artifacts to be produced and audited.
