---
origin: ai
reviewed: false
created_at: 2026-07-05
topic: module2_source_head_generated_artifact_dirty_filter
trust_level: audit_record
---

# Module2 Source Head Generated Artifact Dirty Filter

## Scope

This record covers a read-only formal-gate provenance helper for Module2 gate artifacts.

It does not approve F02.6, run local training, run remote preflight, run remote training, run H01/H02 formal evaluation, pull back artifacts, or generate paper-result material.

## Problem

Several formal-gate builders record `source_head` when writing their JSON/Markdown artifacts. During a sequential local refresh, an earlier generated gate artifact can make the worktree dirty before a later builder records its own `source_head`.

If the later builder writes `HEAD+dirty` only because another tracked gate artifact was just generated, `source_freshness_audit` can later treat a pure generated-artifact refresh as a blocking source risk. That is too coarse: generated gate outputs should not mask real source changes, but they also should not create a false blocker by dirtying each other.

## Change

- Added `forest_n3p.scripts._module2_source_head`.
- The helper records `HEAD+dirty` only when dirty paths include non-ignored paths.
- Known tracked Module2 gate JSON artifacts and their Markdown siblings are ignored for this helper's dirty decision.
- Builder-specific output paths can be added as ignored paths when needed.
- Non-artifact dirty paths still produce `HEAD+dirty`.
- Migrated the tracked Module2 formal-gate builders to call the shared helper instead of each script carrying a local dirty-check variant.

## Current Gate State

This change only makes gate artifact provenance more precise during local artifact refreshes.

F02.6 remains pending. The only currently allowed action remains `record_f02_6_decision`.

The real formal gate remains blocked because formal training, evaluation, acceptance, and H01/H02 artifacts are still missing. Local training, remote preflight, remote training, formal claim, and paper-result material remain disallowed.

## Verification

- `python -m py_compile ...`
  - Result: passed for `_module2_source_head.py` and the migrated Module2 formal-gate builders.
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_source_head.py`
  - Result: `3 passed`.
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_source_head.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_remaining_deliverables.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_summary_chain_audit.py 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py 2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py 2_experiment/forest_n3p/tests/test_module2_claim_safety.py 2_experiment/forest_n3p/tests/test_module2_paper_readiness.py 2_experiment/forest_n3p/tests/test_module2_mainline_formal_gate_state_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_missing_artifacts_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_handoff_bundle.py`
  - Result: `190 passed`.

## Boundary

This is a provenance hygiene change for read-only gate artifacts. It is not evidence that PPO has replaced RS in formal evaluation. It does not satisfy the missing checkpoint, training summary, evaluation CSV/JSON, formal audit, checkpoint hash, H01 ready manifest, or H02 formal acceptance artifacts.
