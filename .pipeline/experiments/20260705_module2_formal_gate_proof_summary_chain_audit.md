---
status: complete
origin: ai+local
reviewed: false
created: 2026-07-05
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
not_paper_result_material: true
---

# Module2 Formal Gate Proof Summary Chain Audit

## What Changed

Added a local read-only audit for the downstream proof-deliverables summary chain.

The new builder is:

- `2_experiment/forest_n3p/scripts/build_module2_formal_gate_proof_summary_chain_audit.py`

It reads the formal-gate remaining-deliverables baseline and checks that the same proof summary is preserved across:

- `formal_gate_proof_audit`
- `formal_gate_status_report`
- `post_f02_6_plan_audit`
- `remote_packet_safety_audit`
- `formal_gate_gap_audit`
- `claim_safety`
- `paper_readiness`

The audited summary is the current formal gap:

- training: `3`
- evaluation: `2`
- acceptance: `3`
- formal_acceptance: `2`
- next blocked lane: `decision`
- H01 status: `blocked_pending_decisions`
- H02 status: `blocked_formal_output_acceptance`
- H02 paper-result input allowed: `false`

## Current State

The generated artifact is:

- `0_trials/module2_formal_gate_proof_summary_chain_audit/formal_gate_proof_summary_chain_audit.json`
- `0_trials/module2_formal_gate_proof_summary_chain_audit/formal_gate_proof_summary_chain_audit.md`

Current status:

- `formal_gate_proof_summary_chain_consistent_blocked`
- `audit_issue_count=0`
- `row_count=14`
- `consistent_row_count=14`
- `missing_row_count=0`
- `mismatch_row_count=0`
- `proof_open=true`
- `h02_paper_result_input_allowed=false`

This means the downstream artifacts agree that the formal gate is still blocked. It does not mean the PPO-vs-RS formal result exists.

## Verification

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_summary_chain_audit.py

PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py

PYTHONPATH=2_experiment python -m \
  forest_n3p.scripts.build_module2_formal_gate_proof_summary_chain_audit
```

Observed:

- Proof summary chain audit tests: `5 passed`.
- Source freshness tests after adding the new target: `6 passed`.
- Generated chain audit status: `formal_gate_proof_summary_chain_consistent_blocked`.

## Boundary

This task did not approve F02.6, did not train locally, did not run remote preflight, did not run remote PPO training, did not evaluate a PPO checkpoint, did not pull back formal artifacts, and did not write paper-result material.

The remaining formal gate gap is still the same `3/2/3/2` training/evaluation/acceptance/formal-acceptance package.
