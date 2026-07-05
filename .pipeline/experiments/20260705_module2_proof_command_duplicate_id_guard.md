---
origin: ai
reviewed: false
created_at: 2026-07-05
topic: module2_proof_command_duplicate_id_guard
trust_level: audit_record
---

# Module2 Proof Command Duplicate ID Guard

## Scope

This record covers a read-only formal-gate safety guard for proof command IDs.

It does not approve F02.6, run local training, run remote preflight, run remote training, run H01/H02 formal evaluation, pull back artifacts, or generate paper-result material.

## Problem

`formal_gate_proof_audit` exposes `proof_command_results_by_id`. If two proof commands in the same acceptance-matrix row share the same `command_id`, a downstream consumer keyed by ID can silently collapse distinct proof results.

That would make the formal proof interface weaker than the acceptance matrix claims: the matrix could say that two independent checks exist, while a keyed summary only preserves one result.

## Change

- `build_module2_formal_gate_remaining_deliverables.py` now rejects duplicate `proof_commands[*].command_id` values within each deliverable acceptance-matrix row.
- `build_module2_formal_gate_proof_audit.py` now rejects duplicate upstream proof command IDs before evaluating local read-only proof results.
- Tests cover both generation-time and proof-audit-input duplicate IDs.

## Current Gate State

F02.6 remains pending. The only current allowed action remains `record_f02_6_decision`.

The real formal gate remains blocked:

- `formal_gate_remaining_deliverables.status=formal_gate_deliverables_blocked`
- `formal_gate_remaining_deliverables.audit_issue_count=0`
- `formal_gate_proof_audit.status=formal_gate_proof_audit_blocked`
- `formal_gate_proof_audit.input_safety_issue_count=0`
- `formal_gate_proof_audit.total_proof_command_count=20`
- `formal_gate_proof_audit.blocked_proof_command_count=16`
- `mainline_formal_gate_state_audit.status=mainline_formal_gate_state_consistent_blocked`
- `mainline_formal_gate_state_audit.audit_issue_count=0`

Local training, remote preflight, remote training, and formal claim remain disallowed.

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_remaining_deliverables.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_audit.py`
  - Result: `11 passed`.
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_formal_gate_remaining_deliverables.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_summary_chain_audit.py 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py 2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py 2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py 2_experiment/forest_n3p/tests/test_module2_claim_safety.py 2_experiment/forest_n3p/tests/test_module2_paper_readiness.py 2_experiment/forest_n3p/tests/test_module2_mainline_formal_gate_state_audit.py`
  - Result: `173 passed`.
- Direct JSON check confirms no input-safety issues in the real proof plan and confirms the gate remains blocked because formal artifacts are missing, not because proof command IDs drifted.

## Boundary

This is a proof-interface integrity guard. It is not evidence that PPO has replaced RS in formal evaluation. The formal checkpoint, training summary, evaluation outputs, formal audit, hash record, and H01/H02 acceptance artifacts remain missing or blocked.
