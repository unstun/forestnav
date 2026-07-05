---
origin: ai
reviewed: false
created_at: 2026-07-05
topic: module2_proof_audit_acceptance_matrix_integrity_input_guard
trust_level: audit_record
---

# Module2 Proof Audit Acceptance Matrix Integrity Input Guard

## Scope

This record covers a read-only proof-audit input-safety improvement.

It does not approve F02.6, reject F02.6, run local training, run remote preflight, run remote training, run H01/H02 formal evaluation, pull back artifacts, or generate paper-result material.

## Problem

`formal_gate_remaining_deliverables` now self-checks acceptance-matrix identity. However, `formal_gate_proof_audit` consumes the serialized remaining-deliverables artifact as an upstream input. A downstream proof audit should not blindly trust that upstream matrix if the JSON was manually edited, stale, partially regenerated, or corrupted after generation.

Without an independent consumer-side guard, a malformed `deliverable_acceptance_matrix` could still drive proof-command evaluation while carrying an incorrect `matrix_id`, duplicate matrix row, mismatched `(category, artifact_id)`, missing invalid-substitute warning, or missing-matrix summary drift.

For a paper-level formal gate, this is an input-safety issue. The proof audit must reject identity drift before treating proof-command results as meaningful.

## Change

`build_module2_formal_gate_proof_audit.py` now validates the consumed upstream acceptance matrix:

- each matrix row is an object,
- `matrix_id` is present and unique,
- `category` and `artifact_id` are present,
- `matrix_id == category:artifact_id`,
- `(category, artifact_id)` pairs are unique,
- row category belongs to `missing_counts_by_formal_category` when that summary is present,
- missing rows list invalid substitutes,
- row `execution_boundary` is `read_only_no_execution`,
- top-level `missing_counts_by_formal_category` agrees with `missing_matrix_ids_by_formal_category`,
- missing rows in the matrix agree with top-level `missing_matrix_ids_by_formal_category`.

`test_module2_formal_gate_proof_audit.py` now directly corrupts the upstream remaining-deliverables matrix and proves the proof audit blocks with `proof_audit_input_safety_issues_open` while still not executing command strings.

## Current Gate State

F02.6 remains pending. The only currently allowed formal-gate action remains `record_f02_6_decision`.

The real formal gate remains blocked:

- local training remains disallowed,
- remote preflight remains disallowed,
- remote training remains disallowed,
- H01/H02 formal evaluation remains disallowed,
- formal claim remains disallowed,
- paper-result material remains disallowed.

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_audit.py`
  - Result: `8 passed`.
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests`
  - Result: `357 passed`.

## Boundary

This is a downstream proof-audit input-safety guard. It is not evidence that PPO has replaced RS, and it does not reduce the remaining formal training/evaluation/acceptance deliverable count.
