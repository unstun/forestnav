---
origin: ai
reviewed: false
created_at: 2026-07-05
topic: module2_proof_summary_chain_consumes_proof_audit_input_safety
trust_level: audit_record
---

# Module2 Proof Summary Chain Consumes Proof-Audit Input Safety

## Scope

This record covers a read-only formal-gate summary-chain safety improvement.

It does not approve F02.6, reject F02.6, run local training, run remote preflight, run remote training, run H01/H02 formal evaluation, pull back artifacts, or generate paper-result material.

## Problem

`formal_gate_proof_audit` now rejects unsafe upstream proof inputs, including acceptance-matrix identity drift. However, `formal_gate_proof_summary_chain_audit` primarily checked whether proof-deliverables summaries stayed numerically consistent across downstream artifacts.

That left a downstream ambiguity: a proof audit could report `proof_audit_input_safety_issues_open` while still exposing a top-level remaining-deliverables summary that matched the baseline. A chain audit that only checked summary equality could be misread as saying the proof chain was trustworthy, even though the upstream proof audit had already declared its input unsafe.

For a paper-level formal gate, input safety must propagate across the chain. A consistent summary is not enough if the upstream proof audit says its input was malformed.

## Change

`build_module2_formal_gate_proof_summary_chain_audit.py` now reads the proof-audit manifest and fails when:

- `formal_gate_proof_audit.input_safety_issue_count > 0`,
- `formal_gate_proof_audit.input_safety_issues` is non-empty,
- `formal_gate_proof_audit.blockers` includes `proof_audit_input_safety_issues_open`,
- proof audit unexpectedly allows command execution, training, remote preflight, local training, or formal claims,
- proof audit is marked as paper-result material.

The chain artifact now exposes:

- `proof_audit_input_safety_issue_count`,
- `proof_audit_input_safety_issues`,
- `proof_audit_blockers`.

`test_module2_formal_gate_proof_summary_chain_audit.py` now constructs a summary-consistent proof audit with an input-safety blocker and proves the chain audit fails instead of reporting a clean consistent chain.

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

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_summary_chain_audit.py`
  - Result: `9 passed`.
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests`
  - Result: `358 passed`.

## Boundary

This is a summary-chain input-safety propagation guard. It is not evidence that PPO has replaced RS, and it does not reduce the remaining formal training/evaluation/acceptance deliverable count.
