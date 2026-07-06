---
topic: module2-v2-contract-promotion-readiness-audit
status: ready_for_dr_sun_v2_contract_promotion_decision
date: 2026-07-06
origin: ai+local-source
reviewed: false
executes_training: false
executes_remote_preflight: false
paper_result_material: false
---

# Module2 V2 Contract Promotion Readiness Audit

## Scope

This audit checks whether the v2 `stronger_obstacle_summary_warm_start`
contract promotion packet is ready for Dr Sun's explicit decision.

It does not approve the contract, write contract frontmatter, run local
training, run remote preflight, run remote training, audit, pull back artifacts,
or write paper-result material.

## Generated Artifacts

- `0_trials/module2_v2_contract_promotion_readiness_audit/v2_contract_promotion_readiness_audit.json`
- `0_trials/module2_v2_contract_promotion_readiness_audit/v2_contract_promotion_readiness_audit.md`

## Current Result

- status: `ready_for_dr_sun_v2_contract_promotion_decision`
- contract status: `draft`
- decision required from Dr Sun: `true`
- audit issue count: `0`
- remote preflight allowed now: `false`
- remote training allowed now: `false`
- paper result material allowed now: `false`

## Decision Payload Ready For Review

The audit confirms that the promotion packet, promotion dry-run, chain audit,
and post-promotion regeneration plan are mutually consistent.

Recommended decision payload:

- target status: `approved`
- remote alias: `gpu3070ti-relay`
- training budget:
  - seed: `20260706`
  - total timesteps: `500000`
  - n envs: `4`
  - n steps: `256`
  - batch size: `256`
  - n epochs: `8`
  - learning rate: `0.0001`
  - entropy coefficient: `0.01`
  - checkpoint frequency: `25000`
- unsafe failure thresholds:
  - collision rate `>= 0.30`
  - truncation rate `>= 0.20`

## Boundary

Invalid substitutes remain invalid:

- promotion packet alone as approval;
- promotion dry-run alone as approval;
- chat-only approval without committed contract frontmatter;
- remote preflight before source freshness and v2 packet regeneration;
- remote training before ready preflight manifest;
- paper result material before H02 formal acceptance.

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_v2_contract_promotion_readiness_audit.py 2_experiment/forest_n3p/tests/test_module2_v2_contract_promotion_packet.py 2_experiment/forest_n3p/tests/test_apply_module2_v2_contract_promotion.py 2_experiment/forest_n3p/tests/test_module2_v2_post_promotion_regeneration_plan.py 2_experiment/forest_n3p/tests/test_module2_v2_formal_gate_chain_audit.py`
  -> `19 passed`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_v2_contract_promotion_readiness_audit.py 2_experiment/forest_n3p/scripts/build_module2_v2_contract_promotion_packet.py 2_experiment/forest_n3p/scripts/apply_module2_v2_contract_promotion.py 2_experiment/forest_n3p/scripts/build_module2_v2_post_promotion_regeneration_plan.py 2_experiment/forest_n3p/scripts/build_module2_v2_formal_gate_chain_audit.py 2_experiment/forest_n3p/scripts/_module2_source_head.py`
  -> passed
