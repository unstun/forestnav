---
origin: ai
reviewed: false
created_at: 2026-07-05
topic: module2_f02_6_decision_note_audit_guidance
trust_level: audit_record
---

# Module2 F02.6 Decision Note Audit Guidance

## Scope

This record covers a read-only F02.6 decision-record and decision-intake audit improvement.

It does not approve F02.6, reject F02.6, run local training, run remote preflight, run remote training, run H01/H02 formal evaluation, pull back artifacts, or generate paper-result material.

## Problem

Before this change, a non-pending F02.6 decision required a non-empty `decision_note`, but the record did not expose machine-readable information about whether the note mentioned the selected route, evidence/risk basis, or next gated action.

That was enough to prevent an empty note, but weak for a long-running research gate: a future reviewer could see that a note exists, but not whether it carries the minimum rationale needed to understand why obstacle-summary warm-start was approved or rejected.

## Change

- `build_module2_f02_6_decision_record.py` now emits `decision_note_audit` with:
  - whether the note is required and present,
  - character and word counts,
  - guidance items,
  - whether the note mentions the selected route,
  - whether it mentions evidence or risk basis,
  - whether it mentions the next gated action,
  - a non-blocking `quality_warning` when guidance items appear absent.
- `build_module2_f02_6_decision_intake.py` now exposes the same `decision_note_guidance` in `decision_intake_contract` and Markdown.
- Tests now cover pending, approved, and rejected record note audit behavior, plus intake guidance visibility.

## Current Gate State

F02.6 remains pending. The only current allowed action remains `record_f02_6_decision`.

The real formal gate remains blocked:

- source freshness is clean,
- decision lane is still blocked,
- training/evaluation/acceptance/formal-acceptance deliverables remain missing,
- local training, remote preflight, remote training, formal claim, and paper-result material remain disallowed.

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_f02_6_decision_record.py 2_experiment/forest_n3p/tests/test_module2_f02_6_decision_intake.py 2_experiment/forest_n3p/tests/test_module2_f02_6_decision_gate_audit.py 2_experiment/forest_n3p/tests/test_module2_f02_6_warm_start_decision_packet.py 2_experiment/forest_n3p/tests/test_module2_f02_6_transition_gate_audit.py`
  - Result: `22 passed`.

## Boundary

This is a decision-rationale audit improvement. It is not evidence that PPO has replaced RS, and it does not reduce the remaining formal training/evaluation/acceptance deliverable count.
