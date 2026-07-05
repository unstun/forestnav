---
status: complete
origin: ai+local
reviewed: false
created: 2026-07-05
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
not_paper_result_material: true
---

# Module2 Status Report Exposes Decision Intake Counts

## What Changed

`formal_gate_status_report.current_state` now exposes the F02.6 decision-intake contract and route counts directly, instead of requiring downstream auditors to inspect the nested `f02_6_decision_intake_summary`.

New current-state fields:

- `decision_intake_valid_decision_count`
- `decision_intake_required_record_field_count`
- `decision_intake_decision_note_required`
- `decision_intake_record_command_template_count`
- `decision_intake_post_decision_non_authorization_count`
- `decision_intake_post_decision_route_count`

The intent is to make the next blocked lane more machine-auditable: before F02.6 is closed, the top-level status report now states that there are exactly two valid human decisions, three required record fields, two record commands, four explicit non-authorizations, and two post-decision routes.

## Current Evidence

Refreshed `0_trials/module2_formal_gate_status_report/formal_gate_status_report.json` reports:

- `status=formal_gate_status_blocked`
- `decision_intake_valid_decision_count=2`
- `decision_intake_required_record_field_count=3`
- `decision_intake_decision_note_required=true`
- `decision_intake_record_command_template_count=2`
- `decision_intake_post_decision_non_authorization_count=4`
- `decision_intake_post_decision_route_count=2`
- `local_training_allowed_now=false`
- `remote_training_allowed_now=false`
- `formal_claim_allowed_now=false`

Downstream refreshed artifacts preserve the same boundary:

- `module2_claim_safety.status=blocked_formal_performance_claims`
- `module2_claim_safety.input_status.status_report_decision_intake_valid_decision_count=2`
- `module2_claim_safety.input_status.status_report_decision_intake_post_decision_route_count=2`
- `module2_paper_readiness.status=partial_methods_ready_results_blocked`
- `module2_paper_readiness.formal_results_ready=false`
- `module2_paper_readiness.manuscript_ready=false`

## Verification

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py \
  2_experiment/forest_n3p/tests/test_module2_claim_safety.py \
  2_experiment/forest_n3p/tests/test_module2_paper_readiness.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_summary_chain_audit.py
```

Observed: `77 passed in 3.52s`.

## Boundary

This task did not approve or reject F02.6, did not run local training, did not run remote preflight, did not run remote PPO training, did not audit or pull back a remote checkpoint, did not evaluate a formal PPO checkpoint, and did not write paper-result material.
