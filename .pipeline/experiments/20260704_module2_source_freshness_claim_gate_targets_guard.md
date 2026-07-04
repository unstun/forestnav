---
status: completed
origin: ai+local
reviewed: false
created: 2026-07-04
scope: formal_gate
not_paper_result_material: true
---

# Module2 source freshness guards claim-gate targets

## What changed

`test_module2_source_freshness_audit.py` now locks `claim_safety` and
`paper_readiness` as source-freshness targets required before
`formal_claim_gate`.

This matters because the final claim gate now depends on the inherited formal
gate gap summaries. If either `claim_safety` or `paper_readiness` is stale or
dirty after F02.6 closes, it must be regenerated before any formal performance
claim can be treated as ready.

## Current generated state

`0_trials/module2_source_freshness_audit/source_freshness_audit.json` now
records the current head and marks both claim-gate targets as regeneration
requirements:

- `claim_safety.required_before=formal_claim_gate`
- `claim_safety.freshness_state=historical_clean`
- `claim_safety.regenerate_before_formal_execution=true`
- `paper_readiness.required_before=formal_claim_gate`
- `paper_readiness.freshness_state=historical_dirty`
- `paper_readiness.regenerate_before_formal_execution=true`

`0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json`
keeps the formal gate blocked until F02.6, but its command index now explicitly
includes:

- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_claim_safety`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_paper_readiness`

Both commands are assigned to `regenerate_claim_gate_artifacts`.

## Verification

Commands run:

```bash
PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py
PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_source_freshness_audit
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_regeneration_plan
PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py 2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py
```

Observed results:

- Source-freshness tests: 3 passed.
- Post-F02.6 regeneration-plan tests: 4 passed.
- Combined tests: 7 passed.
- The refreshed source-freshness artifact keeps
  `regeneration_required_before_remote_formal_execution=true`.
- The refreshed post-F02.6 plan remains `blocked_until_f02_6_decision`.

## Boundary

This change did not:

- approve or reject F02.6,
- run local training,
- run remote sync, preflight, training, audit, or pullback,
- run H01/H02 formal evaluation,
- write result-like paper material.
