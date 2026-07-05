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
