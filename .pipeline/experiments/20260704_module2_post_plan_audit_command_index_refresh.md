---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
scope: formal_gate
not_paper_result_material: true
---

# Module2 post-plan audit command-index refresh

## Summary

`module2_post_f02_6_plan_audit` has been regenerated after the command-index audit code and tests landed.

The refreshed artifact now exposes `source_regeneration_command_index_summary` directly in:

- `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
- `0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.md`

## Current Result

- `status`: `post_f02_6_plan_audit_passed`
- `audit_issue_count`: `0`
- command-index rows: `17`
- source-freshness target count: `17`
- unknown/manual fallback rows: `0`
- stage mismatch rows: `0`
- commands absent from their ordered stage: `0`
- forbidden remote/preflight/training/audit commands: `0`
- rows missing required fields: `0`

Stage coverage:

- `regenerate_preflight_gate_artifacts`: `11`
- `regenerate_h01_h02_formal_artifacts`: `2`
- `regenerate_claim_gate_artifacts`: `4`

## Boundary

This refresh only updates read-only audit artifacts. It does not approve F02.6, run local training, run remote preflight, run remote training, run remote audit, pull back artifacts, regenerate H01/H02 accepted results, or authorize formal paper claims.

The formal gate remains blocked:

- `training_allowed_now`: `false`
- `remote_preflight_allowed_now`: `false`
- next formal blocker: F02.6 human decision

## Verification

- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_plan_audit`
  - Result: `post_f02_6_plan_audit_passed`
- `jq -c '{status,audit_issue_count,idx:.source_regeneration_command_index_summary|{present,index_row_count,source_target_count,unknown_manual_count,stage_mismatch_count,command_not_in_stage_count,forbidden_command_count,missing_required_field_count,stage_counts},training:.current_blocking_summary.training_allowed_now,preflight:.current_blocking_summary.remote_preflight_allowed_now}' 0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json`
  - Result: command index present, `17/17`, zero unknown/manual, zero mismatch, zero forbidden commands, training/preflight both `false`.
