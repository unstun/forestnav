---
topic: module2-v2-formal-gate-remaining-evidence
status: blocked_until_v2_contract_promotion
date: 2026-07-06
origin: ai+local-source
reviewed: false
executes_training: false
executes_remote_preflight: false
paper_result_material: false
---

# Module2 V2 Formal Gate Remaining Evidence

## Scope

This is a formal-gate evidence ledger for the selected
`stronger_obstacle_summary_warm_start` lane. It does not run local training,
remote preflight, remote training, audit, pullback, H02 acceptance, or paper
result writing.

## Generated Artifacts

- `0_trials/module2_v2_formal_gate_remaining_evidence/v2_formal_gate_remaining_evidence.json`
- `0_trials/module2_v2_formal_gate_remaining_evidence/v2_formal_gate_remaining_evidence.md`

## Current Gate State

- status: `blocked_until_v2_contract_promotion`
- selected lane: `stronger_obstacle_summary_warm_start`
- contract action: `draft_new_contract`
- v2 contract status: `draft`
- local training allowed now: `false`
- remote preflight allowed now: `false`
- remote training allowed now: `false`
- paper result material allowed now: `false`

## Failed Gate3 Basis

The ledger carries the failed formal Gate3 basis forward as negative evidence:

- decision: `fail`
- episodes: `64`
- terminal-RS successes: `34`
- terminal-RS success rate: `0.53125`
- required threshold: `0.8`
- threshold deficit: `0.26875`

This failed run is not usable as success evidence for PPO replacing RS.

## Missing V2 Evidence

For the next v2 success attempt, all fresh evidence remains unsatisfied:

- contract: `1/1` missing or unsatisfied
- gate precondition: `2/2` missing or unsatisfied
- training: `3/3` missing or unsatisfied
- evaluation: `2/2` missing or unsatisfied
- acceptance: `3/3` missing or unsatisfied
- formal acceptance: `1/1` missing or unsatisfied

Training evidence expected later:

- `train/final_model.zip`
- `train/summary.json`
- `train/training_manifest.json`

Evaluation evidence expected later:

- `eval/gate3_eval_episodes.csv`
- `eval/gate3_summary.json`

Acceptance evidence expected later:

- `gate3_trial_manifest.json`
- `gate3_formal_audit.json`
- `train/final_model.zip.sha256`

Formal acceptance evidence expected later:

- `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
  with `formal_output_accepted=true` and `paper_result_input_allowed=true`.

## Next Allowed Chain

The immediate next gate is still contract promotion:

1. Dr Sun explicitly promotes the v2 contract to `approved` or `frozen`.
2. Apply the promotion and commit the contract status change.
3. Re-run the v2 contract readiness gate.
4. Re-run source freshness and regenerate the v2 remote execution packet.
5. Only after a ready packet, run remote preflight.
6. Only after a ready remote preflight manifest, remote training can be considered.

## Verification

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_v2_formal_gate_remaining_evidence.py 2_experiment/forest_n3p/tests/test_module2_v2_remote_execution_packet.py 2_experiment/forest_n3p/tests/test_module2_v2_contract_readiness_gate.py`
  -> `11 passed`
- `python -m py_compile 2_experiment/forest_n3p/scripts/build_module2_v2_formal_gate_remaining_evidence.py`
  -> passed
