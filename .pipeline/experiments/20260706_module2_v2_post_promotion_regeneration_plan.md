---
topic: module2-v2-post-promotion-regeneration-plan
status: blocked_until_v2_contract_promotion
date: 2026-07-06
origin: ai+local-source
reviewed: false
executes_training: false
executes_remote_preflight: false
paper_result_material: false
---

# Module2 V2 Post-Promotion Regeneration Plan

## Scope

This artifact records what must be regenerated after Dr Sun explicitly promotes
the v2 `stronger_obstacle_summary_warm_start` contract to `approved` or
`frozen`.

It does not promote the contract, execute commands, run local training, run
remote preflight, run remote training, audit, pull back artifacts, or write
paper-result material.

## Generated Artifacts

- `0_trials/module2_v2_post_promotion_regeneration_plan/v2_post_promotion_regeneration_plan.json`
- `0_trials/module2_v2_post_promotion_regeneration_plan/v2_post_promotion_regeneration_plan.md`

## Current Result

- status: `blocked_until_v2_contract_promotion`
- contract status: `draft`
- next action: `await_dr_sun_before_apply_v2_contract_promotion`
- remote preflight allowed now: `false`
- remote training allowed now: `false`
- paper result material allowed now: `false`

## Ordered Targets

The plan currently lists eight ordered targets:

1. `apply_v2_contract_promotion`
2. `rerun_v2_contract_readiness_gate`
3. `rerun_source_freshness_audit`
4. `regenerate_v2_remote_execution_packet`
5. `rerun_v2_formal_gate_chain_audit`
6. `run_remote_preflight_only`
7. `run_remote_training_after_preflight`
8. `pullback_eval_audit_hash_artifacts`

Only `rerun_v2_formal_gate_chain_audit` is currently locally allowed, because it
is a read-only audit refresh. The contract promotion target requires Dr Sun.
Training remains blocked until contract promotion, readiness, source freshness,
remote packet, and remote preflight manifest are all ready.

## Boundary

Invalid substitutes remain invalid:

- promotion dry-run treated as approval;
- source freshness before an approved/frozen v2 contract;
- old v1 remote packet;
- remote preflight smoke;
- remote training before a ready preflight manifest;
- paper result prose before H02 formal acceptance.

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_v2_post_promotion_regeneration_plan.py 2_experiment/forest_n3p/tests/test_module2_v2_formal_gate_chain_audit.py 2_experiment/forest_n3p/tests/test_module2_v2_formal_gate_remaining_evidence.py 2_experiment/forest_n3p/tests/test_module2_v2_remote_execution_packet.py 2_experiment/forest_n3p/tests/test_module2_v2_contract_readiness_gate.py`
  -> `19 passed`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_v2_post_promotion_regeneration_plan.py 2_experiment/forest_n3p/scripts/build_module2_v2_formal_gate_chain_audit.py 2_experiment/forest_n3p/scripts/_module2_source_head.py`
  -> passed
