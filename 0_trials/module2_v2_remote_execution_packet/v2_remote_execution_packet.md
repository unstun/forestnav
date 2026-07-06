# Module2 V2 Remote Execution Packet

This file packetizes remote commands only. It does not run preflight, train, audit, pull back artifacts, or write paper results.

## Status

- status: `ready_for_v2_remote_preflight`
- ready_to_run_remote_preflight: `True`
- ready_to_run_remote_training: `False`
- remote_training_allowed_now: `False`
- blocker_count: `0`

## Blockers

- none

## Command Plan

### `sync_to_remote`
- allowed_now: `True`
- runs_training: `False`
- blocked_by: ``

```bash
rsync -az --exclude .git /Users/sun/tongbu/study/phdproject/ForestNav/ 'gpu3070ti-relay:~/ForestNav/'
```

### `run_remote_preflight`
- allowed_now: `True`
- runs_training: `False`
- blocked_by: ``

```bash
ssh gpu3070ti-relay 'cd '"'"'~/ForestNav'"'"' && PYTHONPATH=2_experiment .venv/bin/python -m forest_n3p.scripts.preflight_rl_rs_gate3_formal_trial --output-dir 0_trials/module2_gate3_formal/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706 --manifest-out 0_trials/module2_remote_preflight/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706/gate3_preflight_manifest.json --contract-path .pipeline/contracts/module2-stronger_obstacle_summary_warm_start-v2.md --seed 20260706 --device cuda --oracle-path 0_trials/module2_oracle_shape/oracle_connector_results.parquet --heldout-seed 20260706 --train-total-timesteps 500000 --train-n-envs 4 --train-n-steps 256 --train-batch-size 256 --train-n-epochs 8 --train-learning-rate 0.0001 --train-ent-coef 0.01 --train-checkpoint-freq 25000 --eval-episodes 64 --eval-min-episodes 64 --eval-success-threshold 0.8 --bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt --warm-start-decision approved_obstacle_summary --allow-existing-output-dir --allow-duplicate-openmp'
```

### `run_remote_training`
- allowed_now: `False`
- runs_training: `True`
- blocked_by: `v2_remote_preflight_not_ready`

```bash
ssh gpu3070ti-relay 'cd '"'"'~/ForestNav'"'"' && PYTHONPATH=2_experiment .venv/bin/python -m forest_n3p.scripts.run_rl_rs_gate3_trial --output-dir 0_trials/module2_gate3_formal/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706 --contract-path .pipeline/contracts/module2-stronger_obstacle_summary_warm_start-v2.md --seed 20260706 --device cuda --train-curriculum-preset f03 --eval-curriculum-preset f03 --oracle-path 0_trials/module2_oracle_shape/oracle_connector_results.parquet --heldout-seed 20260706 --train-total-timesteps 500000 --train-n-envs 4 --train-n-steps 256 --train-batch-size 256 --train-n-epochs 8 --train-learning-rate 0.0001 --train-ent-coef 0.01 --train-checkpoint-freq 25000 --eval-episodes 64 --eval-min-episodes 64 --eval-success-threshold 0.8 --bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt --allow-duplicate-openmp'
```

### `run_remote_audit`
- allowed_now: `False`
- runs_training: `False`
- blocked_by: `v2_remote_preflight_not_ready, remote_training_not_completed`

```bash
ssh gpu3070ti-relay 'cd '"'"'~/ForestNav'"'"' && PYTHONPATH=2_experiment .venv/bin/python -m forest_n3p.scripts.audit_rl_rs_gate3_trial --trial-dir 0_trials/module2_gate3_formal/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706 --contract-path .pipeline/contracts/module2-stronger_obstacle_summary_warm_start-v2.md --min-formal-episodes 64 --required-success-threshold 0.8 --required-train-curriculum f03 --required-eval-curriculum f03 --warm-start-decision approved_obstacle_summary'
```

### `pullback_after_audit`
- allowed_now: `False`
- runs_training: `False`
- blocked_by: `v2_remote_preflight_not_ready, remote_training_not_completed, remote_audit_not_completed`

```bash
rsync -az 'gpu3070ti-relay:~/ForestNav/0_trials/module2_gate3_formal/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706/' /Users/sun/tongbu/study/phdproject/ForestNav/0_trials/module2_gate3_formal/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706/
```

## Invalid Substitutes

- local PPO training output
- old v1 remote execution packet
- failed gate3_obstacle_summary_warm_approved_v1 checkpoint
- remote preflight smoke
- paper table or appendix prose
