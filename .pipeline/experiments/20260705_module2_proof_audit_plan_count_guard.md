---
origin: ai
reviewed: false
created_at: 2026-07-05
topic: module2_proof_audit_plan_count_guard
trust_level: audit_record
---

# Module2 Proof Audit Plan Count Guard

## Scope

This record covers a read-only formal proof-audit input-safety improvement.

It does not approve F02.6, reject F02.6, run local training, run remote preflight, run remote training, run H01/H02 formal evaluation, pull back artifacts, or generate paper-result material.

## Problem

`formal_gate_proof_audit` already evaluated each proof command result without executing command strings, and it rejected unsafe command rows. However, it did not independently fail when the proof plan's declared `total_matrix_rows`, declared `total_proof_command_count`, or declared `rows` length drifted from the actual `deliverable_acceptance_matrix`.

For a formal paper gate, this matters because a malformed upstream ledger could silently under-declare rows or proof commands while the audit continues to summarize the matrix. The proof audit must treat that mismatch as an input-safety issue, not as a harmless metadata discrepancy.

## Change

- `build_module2_formal_gate_proof_audit.py` now checks:
  - `proof_command_plan.total_matrix_rows == len(deliverable_acceptance_matrix)`,
  - `proof_command_plan.total_proof_command_count == actual matrix proof command count`,
  - `len(proof_command_plan.rows) == len(deliverable_acceptance_matrix)` when plan rows are present.
- The proof-audit Markdown now prints an `Input Safety Issues` section so count drift is visible in the human artifact.
- `test_module2_formal_gate_proof_audit.py` now mutates declared plan counts and proves the audit blocks with `proof_audit_input_safety_issues_open`.

## Current Gate State

F02.6 remains pending. The current allowed action remains only `record_f02_6_decision`.

The real formal gate remains blocked:

- local training remains disallowed,
- remote preflight remains disallowed,
- remote training remains disallowed,
- formal claim remains disallowed,
- paper-result material remains disallowed.

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_audit.py`
  - Result: `7 passed`.

## Boundary

This is a proof-plan input-safety guard. It is not evidence that PPO has replaced RS, and it does not reduce the remaining formal training/evaluation/acceptance deliverable count.
