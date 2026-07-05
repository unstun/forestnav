---
origin: ai
reviewed: false
created_at: 2026-07-05
topic: module2_hash_record_proof_command_candidates
trust_level: audit_record
---

# Module2 Hash Record Proof Command Candidates

## Scope

This record covers a read-only formal-gate proof-command fix for `pulled_back_checkpoint_hash_record`.

It does not approve F02.6, run local training, run remote preflight, run remote training, run H01/H02 formal evaluation, pull back artifacts, or generate paper-result material.

## Problem

`formal_gate_remaining_deliverables` allowed the checkpoint hash record to be either `train/final_model.zip.sha256` or `train/final_model.zip.sha256.json`, but its generated proof command treated the human-readable `A or B` path as a single filesystem path. That made the future local proof command impossible to satisfy even if one valid hash record existed.

## Change

- `build_module2_formal_gate_remaining_deliverables.py` now normalizes `"A or B"` path strings into concrete candidate paths for `pulled_back_checkpoint_hash_record`.
- The `pulled_back_checkpoint_hash_record_exists_nonempty` proof command now checks for the first existing non-empty candidate.
- The `pulled_back_checkpoint_hash_record_matches_model` proof command now hashes the pulled-back `train/final_model.zip` and accepts either `.sha256` or `.sha256.json` when the digest is recorded there.
- Tests now assert the candidate-path command shape.

## Current Gate State

F02.6 remains pending. The only current allowed action remains `record_f02_6_decision`.

This fix improves future post-pullback acceptance checking only. It does not create a checkpoint, does not satisfy the hash-record deliverable, and does not authorize formal performance claims.

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_remaining_deliverables.py`
  - Result: `4 passed`.
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_remaining_deliverables.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_summary_chain_audit.py 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py 2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py 2_experiment/forest_n3p/tests/test_module2_claim_safety.py 2_experiment/forest_n3p/tests/test_module2_paper_readiness.py 2_experiment/forest_n3p/tests/test_module2_mainline_formal_gate_state_audit.py`
  - Result: `170 passed`.
- Direct JSON check confirms `pulled_back_checkpoint_hash_record` now emits two concrete candidate paths and the formal gate remains blocked.

## Boundary

This is a proof-command correctness fix. It is not evidence that PPO has replaced RS in formal evaluation. The checkpoint, training summary, evaluation outputs, formal audit, hash record, and H01/H02 acceptance artifacts are still missing or blocked.
