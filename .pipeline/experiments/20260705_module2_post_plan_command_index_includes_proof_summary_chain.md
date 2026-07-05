---
status: complete
origin: ai+local
reviewed: false
created: 2026-07-05
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
not_paper_result_material: true
---

# Module2 Post-Plan Command Index Includes Proof Summary Chain Audit

## What Changed

The post-F02.6 source-regeneration command index now includes the new `formal_gate_proof_summary_chain_audit` artifact as a known builder target.

The target is assigned to:

- `required_before=formal_claim_gate`
- `stage_id=regenerate_claim_gate_artifacts`
- `command_kind=known_builder`
- `command_template=PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_proof_summary_chain_audit`

This closes the gap where source freshness knew about the new proof-summary-chain artifact, but the post-F02.6 regeneration plan still had only the older command-index target set.

## Current State

Refreshed artifacts now carry a 20-row command index through the gate chain:

- `post_f02_6_regeneration_plan`
- `post_f02_6_plan_audit`
- `remote_packet_safety_audit`
- `formal_gate_gap_audit`
- `formal_gate_status_report`
- `claim_safety`
- `paper_readiness`

Observed propagation:

- `index_row_count=20`
- `source_target_count=20`
- `formal_gate_proof_summary_chain_audit` present in post-plan rows
- `formal_gate_proof_summary_chain_audit` present in downstream `claim_gate_rows`
- `unknown_manual_count=0`
- `forbidden_command_count=0`

The gate remains blocked by F02.6 and the missing formal PPO checkpoint. This change only hardens regeneration provenance; it does not create training or evaluation results.

## Verification

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py \
  2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py \
  2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py \
  2_experiment/forest_n3p/tests/test_module2_claim_safety.py \
  2_experiment/forest_n3p/tests/test_module2_paper_readiness.py
```

Observed: `138 passed`.

Also checked the refreshed JSON chain with `jq`; all seven layers report 20 rows and expose `formal_gate_proof_summary_chain_audit`.

## Boundary

This task did not approve F02.6, did not train locally, did not run remote preflight, did not run remote PPO training, did not evaluate a PPO checkpoint, did not pull back formal artifacts, and did not write paper-result material.
