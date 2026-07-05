---
status: complete
origin: ai+local
reviewed: false
created: 2026-07-05
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
not_paper_result_material: true
---

# Module2 Handoff Decision Matrix Guard

## What Changed

`formal_gate_handoff_bundle` now consumes
`formal_gate_status_report.f02_6_decision_evidence_matrix_summary` and exposes
it as `f02_6_decision_evidence_matrix_handoff_summary`.

The handoff bundle now checks that:

- the matrix id is `module2_f02_6_decision_evidence_matrix`
- the matrix status is `ready_for_dr_sun_decision_not_authorization`
- both route decisions remain present
- the 7 required evidence rows remain satisfied
- missing required evidence count remains 0
- invalid substitutes remain present globally and per route
- current authorization, remote preflight, remote training, local training,
  formal claim, and paper-result material all remain disabled

`formal_gate_proof_summary_chain_audit` was also corrected so an explicitly
reported source-freshness blocker is not treated as a proof-chain failure when
the handoff still routes approval through `source_freshness_audit`.

## Current Evidence

Refreshed artifacts:

- `0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json`
  - status: `blocked_until_f02_6_decision`
  - safety issue count: `0`
  - matrix status: `ready_for_dr_sun_decision_not_authorization`
  - missing required evidence count: `0`
  - authorization flags: all false
- `0_trials/module2_formal_gate_proof_summary_chain_audit/formal_gate_proof_summary_chain_audit.json`
  - status: `formal_gate_proof_summary_chain_consistent_blocked`
- `0_trials/module2_mainline_formal_gate_state_audit/mainline_formal_gate_state_audit.json`
  - status: `mainline_formal_gate_state_consistent_blocked`

The source freshness audit still records formal-gate regeneration risk after
recent code/test changes. That risk is now explicitly visible in the handoff
chain instead of being hidden or misclassified as an execution permission.

## Verification

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_handoff_bundle.py
```

Observed: `10 passed in 0.86s`.

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_summary_chain_audit.py
```

Observed: `10 passed in 0.87s`.

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_handoff_bundle.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_summary_chain_audit.py \
  2_experiment/forest_n3p/tests/test_module2_claim_safety.py \
  2_experiment/forest_n3p/tests/test_module2_paper_readiness.py \
  2_experiment/forest_n3p/tests/test_module2_mainline_formal_gate_state_audit.py \
  2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py
```

Observed: `118 passed in 9.65s`.

## Remaining Formal Gate Gaps

The formal gate remains blocked. Missing formal deliverables are unchanged:

- training: `train_final_model_zip`, `train_summary_json`,
  `train_training_manifest_json`
- evaluation: `eval_gate3_eval_episodes_csv`, `eval_gate3_summary_json`
- acceptance: `gate3_trial_manifest_json`, `gate3_formal_audit_json`,
  `pulled_back_checkpoint_hash_record`
- formal acceptance: `h01_ready_for_formal_run`,
  `h02_formal_output_acceptance`

This task did not approve F02.6, run local training, run remote preflight, run
remote PPO training, evaluate PPO, pull back artifacts, or write paper-result
material.
