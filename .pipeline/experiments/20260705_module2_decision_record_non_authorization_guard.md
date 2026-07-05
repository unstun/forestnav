---
status: complete
origin: ai+local
reviewed: false
created: 2026-07-05
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
not_paper_result_material: true
---

# Module2 Decision Record Non-Authorization Guard

## Scope

This record covers a local formal-gate safety guard around the F02.6 decision
record.

It does not approve or reject F02.6, run local training, run remote preflight,
run remote PPO training, run remote audit/pullback, regenerate H01/H02 from a
new checkpoint, or write paper-result material.

## Problem

The downstream F02.6 intake and handoff artifacts already stated that recording
Dr Sun's F02.6 decision is not training authorization. The closer source artifact,
`f02_6_decision_record.json`, did not expose that boundary directly. That made
the most important human-entry artifact less self-explanatory than its
downstream summaries.

## Action

`build_module2_f02_6_decision_record.py` now writes explicit boundary fields:

- `not_paper_result_material=true`
- `runs_training=false`
- `runs_remote_preflight=false`
- `decision_record_is_not_training_authorization=true`
- `decision_record_is_not_paper_result_material=true`
- `current_authorization.current_blocked_action_ids` covering remote preflight,
  remote training, local training, formal claim, and paper-result material
- `post_decision_non_authorization_invariants`, including the gates still
  required after any decision record
- local-only approve/reject `record_command_templates` with
  `allowed_for_agent_now=false`

`build_module2_f02_6_decision_intake.py` now rejects a decision record if those
boundaries are missing or drift to execution/claim permission.

## Current Evidence

`0_trials/module2_f02_6_decision_record/f02_6_decision_record.json` now reports:

- status: `pending_human_decision`
- `decision_record_is_not_training_authorization=true`
- `decision_record_is_not_paper_result_material=true`
- `current_authorization.authorization_status=blocked_until_dr_sun_decision`
- blocked current actions: `remote_preflight`, `remote_training`,
  `local_training`, `formal_claim`, `paper_result_material`
- `remote_preflight_allowed_now=false`
- `remote_training_allowed_now=false`
- `formal_claim_allowed_now=false`
- `paper_result_material_allowed_now=false`

`0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json` now reports:

- status: `f02_6_decision_intake_pending_clean`
- audit issue count: `0`
- record boundary training invariant: `true`
- record boundary paper-material invariant: `true`
- record post-decision non-authorization count: `4`

The refreshed downstream gate chain remains blocked:

- `formal_gate_status_report.status=formal_gate_status_blocked`
- `module2_claim_safety.status=blocked_formal_performance_claims`
- `module2_paper_readiness.status=partial_methods_ready_results_blocked`
- `formal_gate_handoff_bundle.status=blocked_until_f02_6_decision`

## Verification

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_f02_6_decision_record.py \
  2_experiment/forest_n3p/tests/test_module2_f02_6_decision_intake.py
```

Observed: `12 passed in 0.83s`.

The generated artifacts were then refreshed through the local read-only formal
gate chain:

- `f02_6_decision_record`
- `f02_6_decision_gate_audit`
- `f02_6_decision_intake`
- `formal_gate_status_report`
- `claim_safety`
- `paper_readiness`
- `formal_gate_handoff_bundle`
- `formal_gate_proof_summary_chain_audit`
- `mainline_formal_gate_state_audit`
- `source_freshness_audit`

## Remaining Gate

The real formal gate remains blocked:

- F02.6 warm-start decision is pending.
- formal training deliverables are missing: `train_final_model_zip`,
  `train_summary_json`, `train_training_manifest_json`
- formal evaluation deliverables are missing: `eval_gate3_eval_episodes_csv`,
  `eval_gate3_summary_json`
- formal acceptance/pullback deliverables are missing:
  `gate3_trial_manifest_json`, `gate3_formal_audit_json`,
  `pulled_back_checkpoint_hash_record`
- H01/H02 formal acceptance remains blocked:
  `h01_ready_for_formal_run`, `h02_formal_output_acceptance`

This guard only reduces the chance that the future F02.6 decision record is
misread as execution permission.
