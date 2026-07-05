---
origin: ai
reviewed: false
created_at: 2026-07-05
topic: module2_proof_audit_hash_candidate_resolution
trust_level: audit_record
---

# Module2 Proof Audit Hash Candidate Resolution

## Scope

This record covers a read-only formal proof-audit fix for `pulled_back_checkpoint_hash_record`.

It does not approve F02.6, run local training, run remote preflight, run remote training, run H01/H02 formal evaluation, pull back artifacts, or generate paper-result material.

## Problem

`formal_gate_remaining_deliverables` now emits a correct proof command for either `train/final_model.zip.sha256` or `train/final_model.zip.sha256.json`, but `formal_gate_proof_audit` still resolved `expected_path` as one filesystem path before evaluating each proof command.

That meant a future formal pullback containing only the JSON hash record could still be marked missing by the audit layer, despite the ledger and proof command allowing it.

## Change

- `build_module2_formal_gate_proof_audit.py` now resolves `"A or B"` expected paths into candidate paths.
- `_evaluate_command` selects the first existing candidate and only reports `blocked_missing_artifact` when all candidates are absent.
- A new test proves a synthetic complete pullback passes when `checkpoint.sha256` is absent but `checkpoint.sha256.json` contains the matching digest.

## Current Gate State

F02.6 remains pending. The only current allowed action remains `record_f02_6_decision`.

The real proof audit remains `formal_gate_proof_audit_blocked` because the formal checkpoint and hash-record artifacts are still absent.

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_audit.py`
  - Result: `5 passed`.
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_remaining_deliverables.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_summary_chain_audit.py 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py 2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py 2_experiment/forest_n3p/tests/test_module2_claim_safety.py 2_experiment/forest_n3p/tests/test_module2_paper_readiness.py 2_experiment/forest_n3p/tests/test_module2_mainline_formal_gate_state_audit.py`
  - Result: `171 passed`.
- Direct JSON check confirms the real proof audit still blocks the hash-record proof commands because both candidate files are absent, not because candidate resolution failed.

## Boundary

This is a proof-audit acceptance correctness fix. It is not evidence that PPO has replaced RS in formal evaluation. The formal checkpoint, training summary, evaluation outputs, formal audit, hash record, and H01/H02 acceptance artifacts remain missing or blocked.
