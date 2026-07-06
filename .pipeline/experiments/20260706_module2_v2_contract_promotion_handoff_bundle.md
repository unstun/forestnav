---
topic: module2-v2-contract-promotion-handoff-bundle
status: ready_for_dr_sun_v2_contract_promotion_handoff
date: 2026-07-06
origin: ai+local-source
reviewed: false
executes_training: false
executes_remote_preflight: false
paper_result_material: false
---

# Module2 V2 Contract Promotion Handoff Bundle

## Scope

This handoff bundle packages the exact next human decision boundary for the v2
`stronger_obstacle_summary_warm_start` contract.

It does not approve the contract, write contract frontmatter, run local
training, run remote preflight, run remote training, run audit, pull back
artifacts, or write paper-result material.

## Generated Artifacts

- `0_trials/module2_v2_contract_promotion_handoff_bundle/v2_contract_promotion_handoff_bundle.json`
- `0_trials/module2_v2_contract_promotion_handoff_bundle/v2_contract_promotion_handoff_bundle.md`

## Current Result

- status: `ready_for_dr_sun_v2_contract_promotion_handoff`
- selected lane: `stronger_obstacle_summary_warm_start`
- contract action: `draft_new_contract`
- contract status: `draft`
- audit issue count: `0`
- remote preflight allowed now: `false`
- remote training allowed now: `false`
- paper result material allowed now: `false`

## Handoff Boundary

The bundle records the future apply command only as a guarded handoff:

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.apply_module2_v2_contract_promotion --status approved --decider 'Dr Sun' --remote-alias gpu3070ti-relay --confirm-training-budget --confirm-unsafe-failure-thresholds
```

The command must not be run from this bundle alone. It still requires Dr Sun's
explicit approval of the v2 promotion decision in the current gate.

After promotion is explicitly applied and committed, the required non-training
regeneration chain is:

- rerun v2 contract readiness gate;
- rerun source freshness audit;
- regenerate v2 remote execution packet;
- refresh v2 remaining-evidence ledger;
- refresh v2 formal-gate chain audit;
- refresh post-promotion regeneration plan.

Only later gates can decide whether remote preflight is allowed. Remote training
still requires a ready preflight manifest and downstream acceptance gates.

## Remaining Formal Evidence

The current v2 success attempt still has all 12 formal evidence items missing or
unsatisfied:

- contract: `1`
- gate preconditions: `2`
- training: `3`
- evaluation: `2`
- acceptance: `3`
- formal acceptance: `1`

Training artifacts still missing include `train/final_model.zip`,
`train/summary.json`, and `train/training_manifest.json`. Evaluation and
acceptance still require the new Gate3 CSV/summary, trial manifest, formal audit,
checkpoint hash, and H02 formal output acceptance.

## Invalid Substitutes

- chat-only approval without committed contract frontmatter;
- promotion packet alone as approval;
- promotion dry-run alone as approval;
- old v1 contract or old v1 remote packet;
- failed `gate3_obstacle_summary_warm_approved_v1` checkpoint;
- remote preflight smoke before regenerated source-freshness and v2 packet gates;
- local PPO training output;
- paper prose, result table, or appendix text before H02 formal acceptance.

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_v2_contract_promotion_handoff_bundle.py 2_experiment/forest_n3p/tests/test_module2_v2_contract_promotion_readiness_audit.py 2_experiment/forest_n3p/tests/test_module2_v2_contract_promotion_packet.py 2_experiment/forest_n3p/tests/test_apply_module2_v2_contract_promotion.py 2_experiment/forest_n3p/tests/test_module2_v2_post_promotion_regeneration_plan.py`
  -> `19 passed`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_v2_contract_promotion_handoff_bundle.py 2_experiment/forest_n3p/scripts/_module2_source_head.py`
  -> passed
