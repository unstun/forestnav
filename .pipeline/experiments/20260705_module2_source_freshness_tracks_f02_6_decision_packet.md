---
status: complete
origin: ai+local
reviewed: false
created: 2026-07-05
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
not_paper_result_material: true
---

# Module2 Source Freshness Tracks F02.6 Decision Packet

## What Changed

`f02_6_warm_start_decision_packet` is now a source-freshness target.

This closes a pre-decision audit gap: the F02.6 decision packet is the human-facing evidence packet for approving or rejecting obstacle-summary warm-start, but it was not previously included in the formal source-freshness target set.

The target is registered as:

- `artifact_id=f02_6_warm_start_decision_packet`
- `category=decision`
- `path=0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json`
- `required_before=approved_remote_preflight`

`post_f02_6_regeneration_plan` also knows how to regenerate it:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_warm_start_decision_packet
```

## Current Evidence

Current refreshed artifacts report:

- `source_freshness_audit.artifact_records` has `22` records.
- `source_freshness_audit` includes `f02_6_warm_start_decision_packet`.
- The current decision packet freshness state is `current_clean`.
- Because the packet is current-clean, `post_f02_6_plan_audit.source_regeneration_command_index_summary.index_row_count=21`, not `22`.
- Synthetic stale-source tests cover the opposite case: when the decision packet is stale, it is mapped to `regenerate_preflight_gate_artifacts` with a known-builder command.
- `formal_gate_status_report.status=formal_gate_status_blocked`.
- `local_training_allowed_now=false`.
- `remote_training_allowed_now=false`.
- `formal_claim_allowed_now=false`.

## Verification

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py \
  2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py \
  2_experiment/forest_n3p/tests/test_module2_post_f02_6_plan_audit.py \
  2_experiment/forest_n3p/tests/test_module2_remote_packet_safety_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_gap_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py \
  2_experiment/forest_n3p/tests/test_module2_claim_safety.py \
  2_experiment/forest_n3p/tests/test_module2_paper_readiness.py
```

Observed: `144 passed in 7.04s`.

## Boundary

This task did not approve or reject F02.6, did not run local training, did not run remote preflight, did not run remote PPO training, did not audit or pull back a remote checkpoint, did not evaluate a formal PPO checkpoint, and did not write paper-result material.
