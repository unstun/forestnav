---
status: complete
origin: ai+local
reviewed: false
created: 2026-07-05
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
not_paper_result_material: true
---

# Module2 F02.6 Decision Evidence Matrix

## What Changed

The F02.6 warm-start decision packet now exposes a machine-readable
`decision_evidence_matrix`.

The matrix is decision support only. It does not approve F02.6, run local
training, run remote preflight, run remote PPO training, enable formal claims,
or provide paper-result material.

The matrix records two routes:

- `approve_obstacle_summary_warm_start`
- `reject_obstacle_summary_warm_start`

Each route now includes:

- required evidence rows with `evidence_id`
- local artifact anchors in `required_artifact_paths`
- observed facts copied from audited JSON inputs
- `satisfied` flags
- route-level and evidence-level `invalid_substitutes`
- current authorization fields that remain false

## Current Evidence

Refreshed `0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json`
reports:

- `status=pending_human_decision`
- `decision_evidence_matrix.status=ready_for_dr_sun_decision_not_authorization`
- `decision_evidence_matrix.route_count=2`
- `decision_evidence_matrix.required_evidence_count=7`
- `decision_evidence_matrix.satisfied_required_evidence_count=7`
- `decision_evidence_matrix.missing_required_evidence_count=0`
- `decision_evidence_matrix.current_authorization_allowed_now=false`
- `decision_evidence_matrix.remote_preflight_allowed_now=false`
- `decision_evidence_matrix.remote_training_allowed_now=false`
- `decision_evidence_matrix.local_training_allowed_now=false`
- `decision_evidence_matrix.formal_claim_allowed_now=false`
- `decision_evidence_matrix.paper_result_material_allowed_now=false`

The approve route evidence rows are:

- `no_warm_formal_gate3_failure`
- `obstacle_summary_bc_candidate_readiness`
- `bounded_candidate_comparison_against_patch_cnn`
- `remote_route_guarded_until_decision`

The reject route evidence rows are:

- `reject_route_defined_in_decision_intake`
- `reject_route_does_not_relabel_no_warm_failure`
- `reject_route_requires_stronger_protocol_before_training`

## Formal Gate Boundary

Downstream refreshed artifacts still report the correct blocked state:

- `f02_6_decision_gate_audit.status=f02_6_decision_gate_pending_clean`
- `f02_6_decision_intake.status=f02_6_decision_intake_pending_clean`
- `f02_6_transition_gate_audit.status=f02_6_transition_gate_audit_passed`
- `formal_gate_status_report.status=formal_gate_status_blocked`
- `module2_claim_safety.status=blocked_formal_performance_claims`
- `module2_paper_readiness.status=partial_methods_ready_results_blocked`

`formal_gate_status_report.next_required_formal_deliverables` still lists 10
missing formal deliverables:

- training: `train_final_model_zip`, `train_summary_json`,
  `train_training_manifest_json`
- evaluation: `eval_gate3_eval_episodes_csv`, `eval_gate3_summary_json`
- acceptance: `gate3_trial_manifest_json`, `gate3_formal_audit_json`,
  `pulled_back_checkpoint_hash_record`
- formal acceptance: `h01_ready_for_formal_run`,
  `h02_formal_output_acceptance`

## Verification

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_f02_6_warm_start_decision_packet.py \
  2_experiment/forest_n3p/tests/test_module2_f02_6_decision_intake.py \
  2_experiment/forest_n3p/tests/test_module2_f02_6_decision_gate_audit.py \
  2_experiment/forest_n3p/tests/test_module2_f02_6_transition_gate_audit.py \
  2_experiment/forest_n3p/tests/test_module2_source_freshness_audit.py \
  2_experiment/forest_n3p/tests/test_module2_post_f02_6_regeneration_plan.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_status_report.py \
  2_experiment/forest_n3p/tests/test_module2_claim_safety.py \
  2_experiment/forest_n3p/tests/test_module2_paper_readiness.py
```

Observed: `111 passed in 13.60s`.

```bash
PYTHONPATH=2_experiment pytest -q \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_missing_artifacts_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_remaining_deliverables.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_proof_audit.py \
  2_experiment/forest_n3p/tests/test_module2_formal_gate_handoff_bundle.py
```

Observed: `27 passed in 2.02s`.

## Boundary

This task did not approve or reject F02.6, did not run local training, did not
run remote preflight, did not run remote PPO training, did not pull back a
checkpoint, did not run H01/H02 formal evaluation, and did not write paper
result material.
