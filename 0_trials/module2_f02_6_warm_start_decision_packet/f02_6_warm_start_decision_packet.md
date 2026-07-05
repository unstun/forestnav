# Module2 F02.6 Warm-Start Decision Packet

- status: `pending_human_decision`
- recommendation: `approve_obstacle_summary_warm_start`
- decision owner: `Dr Sun`
- remote preflight allowed now: `False`
- remote training allowed now: `False`

## Current Authorization

- authorization_status: `blocked_until_dr_sun_decision`
- allowed_now: `record_f02_6_decision`
- blocked_now: `remote_preflight, remote_training, local_training, formal_claim, paper_result_material`
- post_decision_routes_are_current_authorization: `False`

## Key Evidence

- No-warm formal Gate #3: `fail`, 29/64 terminal-RS success, rate `0.453125`.
- Obstacle-summary BC formal-v2 closed loop: 67/258 terminal-RS success.
- Same bounded rows: obstacle-summary 101/242 vs patch-CNN 63/242.

## Remote Readiness

- no-warm formal preflight ready: `True`
- warm-start formal preflight ready: `False`
- warm-start blockers: `warm_start_decision_pending`
- CUDA smoke formal decision: `not_formal`

## Decision Evidence Matrix

- matrix_status: `ready_for_dr_sun_decision_not_authorization`
- current_authorization_allowed_now: `False`
- missing_required_evidence_count: `0`

### approve_obstacle_summary_warm_start

- route_status: `decision_supported_not_authorized`
- next_lane_after_record: `source_fresh_regeneration`
- current_authorization_allowed_now: `False`
- allows_remote_training_now: `False`
- allows_formal_claim_now: `False`
- invalid_substitutes: `decision packet recommendation without Dr Sun decision record; remote CUDA smoke as formal evidence; local training output; no-warm formal failure as obstacle-summary warm-start evidence`
- evidence_id: `no_warm_formal_gate3_failure`
  - satisfied: `True`
  - artifacts: `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/gate3_formal_audit.json; 0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/eval/gate3_summary.json`
  - invalid_substitutes: `remote CUDA smoke audit; available-subset smoke evaluation; paper table preview`
- evidence_id: `obstacle_summary_bc_candidate_readiness`
  - satisfied: `True`
  - artifacts: `2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/summary.json; 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/eval_patch_bounded_rows.json; 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt`
  - invalid_substitutes: `checkpoint path without sha256; BC training summary without closed-loop rows; manual note that the model exists`
- evidence_id: `bounded_candidate_comparison_against_patch_cnn`
  - satisfied: `True`
  - artifacts: `2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/eval_patch_bounded_rows.json; 2_experiment/forest_n3p/models/module2_rl_rs_bc_patch_formal_v2_pilot/summary.json`
  - invalid_substitutes: `cross-protocol comparison; single scalar validation loss; README-level model description`
- evidence_id: `remote_route_guarded_until_decision`
  - satisfied: `True`
  - artifacts: `0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_pending_remote_v1/gate3_preflight_manifest.json; 0_trials/module2_remote_smoke/gate3_warm_start_cuda_smoke/gate3_formal_audit.json; 0_trials/module2_f02_6_decision_record/f02_6_decision_record.json; 0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json`
  - invalid_substitutes: `pending remote preflight manifest; CUDA smoke treated as formal Gate #3 evidence; post-decision command copied into a shell`

### reject_obstacle_summary_warm_start

- route_status: `redesign_route_defined_not_authorized`
- next_lane_after_record: `protocol_redesign`
- current_authorization_allowed_now: `False`
- allows_remote_training_now: `False`
- allows_formal_claim_now: `False`
- invalid_substitutes: `implicit rejection by inaction; continuing obstacle-summary formal training after rejection; protocol redesign without revised contract; paper result claim before new formal acceptance`
- evidence_id: `reject_route_defined_in_decision_intake`
  - satisfied: `True`
  - artifacts: `0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json`
  - invalid_substitutes: `using the rejected obstacle-summary checkpoint anyway; editing downstream permission JSON by hand; paper discussion paragraph without a revised protocol`
- evidence_id: `reject_route_does_not_relabel_no_warm_failure`
  - satisfied: `True`
  - artifacts: `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/gate3_formal_audit.json; 0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/eval/gate3_summary.json`
  - invalid_substitutes: `no-warm failure relabeled as warm-start failure; no-warm failure relabeled as patch-CNN evidence; claim that all PPO warm-starts have failed`
- evidence_id: `reject_route_requires_stronger_protocol_before_training`
  - satisfied: `True`
  - artifacts: `0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json; 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/summary.json; 2_experiment/forest_n3p/models/module2_rl_rs_bc_patch_formal_v2_pilot/summary.json`
  - invalid_substitutes: `stronger protocol name without a contract; remote training command from the approve route; warm-start paper result before new acceptance`

## Source Integrity

- source_count: `12`
- missing_source_count: `0`
- all_sources_present: `True`
- all_existing_sources_hashed: `True`

## Post-Approval Remote-Only Command Candidate

- command_kind: `post_approval_remote_training_candidate`
- current_authorization_allowed_now: `False`
- execution_host_required: `gpu3070ti-relay`
- local_execution_allowed: `False`
- remote_preflight_allowed_now: `False`
- remote_training_allowed_now: `False`
- requires_dr_sun_decision_record: `True`
- requires_source_fresh_regeneration: `True`
- requires_post_f02_6_plan_audit: `True`
- requires_approved_remote_preflight: `True`

```bash
ssh gpu3070ti-relay 'cd ~/ForestNav && python -m forest_n3p.scripts.run_rl_rs_gate3_trial --output-dir 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1 --seed 20260704 --device cuda --train-curriculum-preset f03 --eval-curriculum-preset f03 --oracle-path 0_trials/module2_oracle_shape/oracle_connector_results.parquet --heldout-seed 20260704 --train-total-timesteps 100000 --train-n-envs 1 --train-n-steps 128 --train-batch-size 64 --train-n-epochs 4 --eval-episodes 64 --eval-min-episodes 64 --eval-success-threshold 0.8 --obs-patch-size-m 6.4 --obs-patch-cells 64 --max-steps 32 --allow-duplicate-openmp --bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt'
```

## Claim Boundaries
- This packet is decision support, not a formal experiment result.
- It does not close F02.6; Dr Sun must explicitly approve or reject the recommendation.
- Remote smoke artifacts prove executable CUDA plumbing only; they are not Gate #3 evidence.
- The listed remote command is a post-approval route, not current authorization to preflight or train.
- The listed command must not be run on the local Mac; approved execution is remote-only on gpu3070ti-relay after the formal gates reopen it.
- No-warm formal failure cannot be relabeled as obstacle-summary warm-start failure.
- The obstacle-summary checkpoint is a warm-start initializer candidate, not a finished planner checkpoint.
