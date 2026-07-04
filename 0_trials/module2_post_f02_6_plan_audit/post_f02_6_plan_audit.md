# Module2 Post-F02.6 Plan Audit

This file audits the ordered post-F02.6 plan. It does not execute the plan.

- status: `post_f02_6_plan_audit_passed`
- audit_issue_count: `0`
- executes_commands: `False`
- runs_training: `False`
- runs_remote_preflight: `False`

## Current Blocking Summary

- plan_status: `blocked_until_f02_6_decision`
- training_allowed_now: `False`
- remote_preflight_allowed_now: `False`
- ready_stage_ids: `['f02_6_decision_record']`
- blocked_stage_ids: `['regenerate_preflight_gate_artifacts', 'approved_remote_preflight', 'regenerate_remote_execution_packet', 'gate3_remote_training', 'gate3_remote_audit_pullback', 'regenerate_h01_h02_formal_artifacts', 'regenerate_claim_gate_artifacts']`

## Source Regeneration Command Index

- present: `True`
- index_row_count: `19`
- source_target_count: `19`
- unknown_manual_count: `0`
- stage_mismatch_count: `0`
- command_not_in_stage_count: `0`
- forbidden_command_count: `0`

## Missing Artifacts Inventory

- path: `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json`
- status: `formal_gate_missing_artifacts_open`
- runs_training: `False`
- runs_remote_preflight: `False`
- all_required_evidence_present: `False`
- audit_issue_count: `0`
- missing_counts_by_category: `{'decision': 1, 'decision_gate': 0, 'regeneration': 19, 'gate_sequence': 7, 'training': 3, 'evaluation': 2, 'acceptance': 3, 'evaluation_acceptance': 2, 'claim_gate': 7}`

## Closure Checklist

- path: `0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json`
- status: `formal_gate_closure_blocked`
- runs_training: `False`
- runs_remote_preflight: `False`
- open_item_count: `8`
- input_safety_issue_count: `0`

## Formal Gate Status Report

- path: `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json`
- status: `formal_gate_status_blocked`
- runs_training: `False`
- runs_remote_preflight: `False`
- formal_claim_allowed_now: `False`
- local_training_allowed_now: `False`
- input_safety_issue_count: `0`
- next_blocked_lane_id: `decision`

### Remaining Deliverables Gap Summary

- ledger_path: `0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json`
- ledger_exists: `True`
- ledger_total_missing_deliverables: `10`
- ledger_open_category_count: `4`
- status_report_total_missing_deliverables: `10`
- status_report_open_category_count: `4`

### Status Report Handoff Summary

- status: `blocked_until_f02_6_decision`
- remote_training_allowed_now: `False`
- safety_issue_count: `0`

### Status Report Execution Veto Matrix

- present: `True`
- all_rows_consistent: `True`
- mismatch_rows: `[]`

### Status Report Remote Execution Steps

- `local_training`: consensus_allowed_now=`False`
- `remote_preflight`: consensus_allowed_now=`False`
- `remote_training`: consensus_allowed_now=`False`
- `remote_audit`: consensus_allowed_now=`False`
- `formal_claim`: consensus_allowed_now=`False`

- `sync_to_remote`: allowed_now=`False`, runs_training=`False`, blocked_by=`requires_dr_sun_approval`
- `run_remote_preflight`: allowed_now=`False`, runs_training=`False`, blocked_by=`requires_dr_sun_approval`
- `run_remote_training`: allowed_now=`False`, runs_training=`True`, blocked_by=`requires_dr_sun_approval, f02_6_warm_start_decision_pending, missing_module2_rl_rs_checkpoint, remote_packet_not_ready`
- `run_remote_audit`: allowed_now=`False`, runs_training=`False`, blocked_by=`requires_dr_sun_approval, f02_6_warm_start_decision_pending, missing_module2_rl_rs_checkpoint, remote_packet_not_ready`

## Audit Issues

- none

## Claim Boundaries

- This audit validates a plan artifact; it does not execute the plan.
- A passing audit is not permission to train while F02.6 remains pending.
- A passing audit is not a paper result or formal performance claim.
- Training stages must remain remote-only on gpu3070ti-relay and blocked until upstream gates pass.
