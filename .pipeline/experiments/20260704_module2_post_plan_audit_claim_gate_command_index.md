---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
scope: formal_gate
not_paper_result_material: true
---

# Module2 post-F02.6 plan audit guards claim-gate command index

## What changed

`test_module2_post_f02_6_plan_audit.py` now requires `paper_readiness` to be
present beside `claim_safety` in the source-regeneration command index fixture.

The test fixture now checks that the post-F02.6 plan audit covers both
claim-gate artifacts:

- `claim_safety`
- `paper_readiness`

Both must be listed as `formal_claim_gate` regeneration targets, both must map
to `regenerate_claim_gate_artifacts`, and both commands must be present in the
corresponding stage command list.

## Current generated state

`0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json` remains a
read-only audit pass while the plan itself remains blocked by F02.6:

- `status=post_f02_6_plan_audit_passed`
- `audit_issue_count=0`
- `source_regeneration_command_index_summary.index_row_count=18`
- `source_regeneration_command_index_summary.source_target_count=18`
- `source_regeneration_command_index_summary.missing_target_ids=[]`
- `source_regeneration_command_index_summary.unknown_manual_count=0`
- `source_regeneration_command_index_summary.forbidden_command_count=0`

The refreshed audit summary includes these claim-gate rows:

- `claim_safety`: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_claim_safety`
- `paper_readiness`: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_paper_readiness`

Both rows are assigned to `regenerate_claim_gate_artifacts`.

## Verification

Commands run:

```bash
PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_plan_audit
jq '{status,audit_issue_count,command_index:{present:.source_regeneration_command_index_summary.present,index_row_count:.source_regeneration_command_index_summary.index_row_count,source_target_count:.source_regeneration_command_index_summary.source_target_count,stage_counts:.source_regeneration_command_index_summary.stage_counts,missing:.source_regeneration_command_index_summary.missing_target_ids,unknown:.source_regeneration_command_index_summary.unknown_manual_count,forbidden:.source_regeneration_command_index_summary.forbidden_command_count},claim_rows:[.source_regeneration_command_index_summary.rows | to_entries[] | select(.key=="claim_safety" or .key=="paper_readiness") | {artifact_id:.key,stage_id:.value.stage_id,command_template:.value.command_template}]}' 0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json
PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py
git diff --check
```

Observed results:

- Post-F02.6 plan-audit tests: 19 passed.
- Source-freshness + post-F02.6 regeneration-plan + post-plan-audit tests:
  26 passed.
- The refreshed audit artifact reports no missing source target, no unknown
  manual row, and no forbidden command.

## Boundary

This change did not:

- approve or reject F02.6,
- run local training,
- run remote sync, preflight, training, audit, or pullback,
- run H01/H02 formal evaluation,
- write result-like paper material.
