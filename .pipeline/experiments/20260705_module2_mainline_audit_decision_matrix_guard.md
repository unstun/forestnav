---
status: complete
origin: ai+local
reviewed: false
created: 2026-07-05
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
not_paper_result_material: true
---

# Module2 Mainline Audit Decision Matrix Guard

## What Changed

`mainline_formal_gate_state_audit` now consumes the F02.6
`decision_evidence_matrix` summary exposed by `formal_gate_status_report`.

The audit now checks that the matrix:

- is present as `module2_f02_6_decision_evidence_matrix`
- remains `ready_for_dr_sun_decision_not_authorization`
- retains both routes: `approve_obstacle_summary_warm_start` and
  `reject_obstacle_summary_warm_start`
- keeps at least 7 required evidence rows with 0 missing required evidence
- keeps invalid substitutes
- keeps current authorization, remote preflight, remote training, local
  training, formal claim, and paper-result material all disabled

The mainline task book also now mentions the matrix id, decision-only status,
both route ids, and invalid-substitute boundary in the current formal-gate
state section.

## Current Evidence

Refreshed artifact:

- `0_trials/module2_mainline_formal_gate_state_audit/mainline_formal_gate_state_audit.json`
- status: `mainline_formal_gate_state_consistent_blocked`
- audit issue count: `0`
- matrix id: `module2_f02_6_decision_evidence_matrix`
- matrix status: `ready_for_dr_sun_decision_not_authorization`
- missing required evidence count: `0`
- authorization flags: all false

This is a blocked-state consistency audit. It does not approve F02.6, does not
start remote preflight, does not start local or remote training, does not
evaluate PPO, and does not create paper-result material.

## Verification

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_mainline_formal_gate_state_audit
```

Observed: `status=mainline_formal_gate_state_consistent_blocked`.

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_mainline_formal_gate_state_audit.py
```

Observed: `9 passed in 0.74s`.

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_mainline_formal_gate_state_audit.py \
  2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py \
  2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py \
  2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py \
  2_experiment/forest_n3p/tests/test_module2_claim_safety.py \
  2_experiment/forest_n3p/tests/test_module2_paper_readiness.py
```

Observed: `128 passed in 10.42s`.

## Remaining Formal Gate Gaps

The formal gate is still blocked. Missing formal deliverables remain:

- training: `train_final_model_zip`, `train_summary_json`,
  `train_training_manifest_json`
- evaluation: `eval_gate3_eval_episodes_csv`, `eval_gate3_summary_json`
- acceptance: `gate3_trial_manifest_json`, `gate3_formal_audit_json`,
  `pulled_back_checkpoint_hash_record`
- formal acceptance: `h01_ready_for_formal_run`,
  `h02_formal_output_acceptance`

The next allowed action is still only `record_f02_6_decision`.
