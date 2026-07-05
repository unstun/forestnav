---
origin: ai
reviewed: false
created_at: 2026-07-05
topic: module2_source_freshness_blocking_self_lag_policy
trust_level: audit_record
---

# Module2 Source Freshness Blocking Self-Lag Policy

## Scope

This record covers a read-only formal-gate source-freshness policy refinement.

It does not approve F02.6, run local training, run remote preflight, run remote training, run H01/H02 formal evaluation, pull back artifacts, or generate paper-result material.

## Problem

`source_freshness_audit` already documented that an artifact's own post-commit source-head lag is expected and is not a formal gate blocker by itself.

The previous machine-readable gate, however, only exposed `regeneration_required_before_remote_formal_execution`, which was true for any non-current source head. That conflated two cases:

- blocking freshness risks: dirty source heads, unknown commits, or historical clean artifacts with non-self source changes;
- non-blocking bookkeeping lag: a historical clean artifact whose only changed paths since generation are its own JSON/Markdown files.

Without a separate blocking flag, downstream preflight gates could treat pure self-artifact lag as a remote-execution blocker even when no code/config/input source changed.

## Change

- `build_module2_source_freshness_audit.py` now emits:
  - `blocking_regeneration_required_before_remote_formal_execution`,
  - `blocking_regeneration_target_count`,
  - `blocking_ordered_regeneration_targets`,
  - per-record `blocking_regeneration_required_before_remote_formal_execution`.
- Pure tracked-artifact lag is now classified as `source_freshness_tracked_artifact_lag_only_gate_ready`.
- Downstream formal-gate readers prefer the new blocking flag and fall back to the legacy regeneration flag for older JSON.
- Blocking risks still include dirty source heads, unknown commits, missing source heads, and any historical clean artifact with non-self source changes.

## Current Gate State

This change does not unblock the real PPO-vs-RS formal gate.

F02.6 remains pending. Formal PPO checkpoint, training summary, evaluation rows, formal audit, checkpoint hash, H01 ready manifest, and H02 formal acceptance remain missing or blocked.

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py`
  - Result: `39 passed`.
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_remaining_deliverables.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_summary_chain_audit.py 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py 2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py 2_experiment/forest_n3p/tests/test_module2_claim_safety.py 2_experiment/forest_n3p/tests/test_module2_paper_readiness.py 2_experiment/forest_n3p/tests/test_module2_mainline_formal_gate_state_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_missing_artifacts_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_handoff_bundle.py`
  - Result: `187 passed`.

## Boundary

This policy only prevents a false source-freshness blocker after gate artifacts commit themselves. It does not declare the current source-freshness audit clean, does not approve remote execution, and does not create formal PPO result evidence.
