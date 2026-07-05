---
status: complete
origin: ai+local
reviewed: false
created: 2026-07-05
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
not_paper_result_material: true
---

# Module2 Proof/Mainline Current Gate Refresh

## Scope

This record covers a local read-only refresh of the proof and mainline mirror
layer after the downstream formal-gate status chain was refreshed.

It does not approve or reject F02.6, run local training, run SSH, run remote
preflight, run remote PPO training, run remote audit/pullback, or write
paper-result material.

## Action

Refreshed:

- `formal_gate_proof_audit`
- `formal_gate_proof_summary_chain_audit`
- `mainline_formal_gate_state_audit`

## Current Evidence

The refreshed proof audit records:

- status: `formal_gate_proof_audit_blocked`
- `input_safety_issue_count=0`
- `total_proof_command_count=20`
- `passed_proof_command_count=2`
- `failed_proof_command_count=2`
- `blocked_proof_command_count=16`
- `runs_training=false`
- `runs_remote_preflight=false`
- `formal_claim_allowed=false`

The refreshed proof summary chain records:

- status: `formal_gate_proof_summary_chain_consistent_blocked`
- `audit_issue_count=0`
- `proof_open=true`

The refreshed mainline audit records:

- status: `mainline_formal_gate_state_consistent_blocked`
- `audit_issue_count=0`

## Verification

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_summary_chain_audit.py \
  2_experiment/forest_n3p/tests/test_module2_mainline_formal_gate_state_audit.py
```

Observed: `27 passed in 2.26s`.

## Boundary

The proof layer is still blocked because formal training, evaluation,
acceptance, and H01/H02 acceptance artifacts are missing. This refresh is not
PPO-vs-RS performance evidence and does not unlock remote execution or formal
claims.
