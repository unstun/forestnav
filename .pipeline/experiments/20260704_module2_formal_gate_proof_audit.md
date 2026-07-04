---
status: complete
origin: ai+local
reviewed: false
created: 2026-07-04
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
not_paper_result_material: true
---

# Module2 Formal Gate Proof Audit

## What Changed

Added a local read-only proof audit for Module2 formal gate deliverables.

- New builder: `2_experiment/forest_n3p/scripts/build_module2_formal_gate_proof_audit.py`.
- New tests: `2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_audit.py`.
- New artifact: `0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json/md`.
- The audit reads `formal_gate_remaining_deliverables.proof_command_plan` and `deliverable_acceptance_matrix`.
- It evaluates each proof command's acceptance semantics directly with local read-only Python checks.
- It does not execute proof command strings; every result records `command_was_executed=false`.
- It never trains, runs remote preflight, syncs, audits remote outputs, or writes paper-result material.

## Current Evidence

`0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json` currently reports:

- `status=formal_gate_proof_audit_blocked`
- `total_matrix_rows=10`
- `total_proof_command_count=20`
- `passed_proof_command_count=2`
- `failed_proof_command_count=2`
- `blocked_proof_command_count=16`
- `executes_commands=false`
- `runs_training=false`
- `runs_remote_preflight=false`
- `local_training_allowed=false`
- `formal_claim_allowed=false`

Current blocker classes:

- `missing_formal_training_artifacts`
- `missing_formal_evaluation_artifacts`
- `missing_formal_acceptance_artifacts`
- `failed_formal_h01_h02_acceptance_artifacts`

Interpretation:

- Training/evaluation/acceptance proof commands remain blocked because the formal remote pullback tree is still missing.
- H01/H02 source files exist locally, so existence checks pass.
- H01/H02 formal-status checks still fail because formal-ready / formal-output-accepted states are not present.
- This is a formal gate proof ledger, not a result claim.

## Verification

```bash
python -m py_compile \
  2_experiment/forest_n3p/scripts/build_module2_formal_gate_proof_audit.py

PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_audit.py
```

Observed: `4 passed in 0.25s`.

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_proof_audit
```

Observed:

- `status=formal_gate_proof_audit_blocked`
- `passed=2`
- `failed=2`
- `blocked=16`

## Boundary

No local training, remote sync, remote preflight, remote PPO training, remote audit, pullback, H01/H02 formal run, or paper result writing was performed. This artifact only evaluates local read-only proof-command evidence against the current filesystem state.
