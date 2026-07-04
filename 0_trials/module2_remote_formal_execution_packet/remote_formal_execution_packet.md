# Module2 Remote Formal Execution Packet

- status: `blocked_until_f02_6_decision`
- ready to run remote training: `False`
- local training allowed: `False`
- GPU alias: `gpu3070ti-relay`

## Blockers
- `requires_dr_sun_approval`
- `f02_6_warm_start_decision_pending`
- `missing_module2_rl_rs_checkpoint`

## Commands

### Sync To Remote

```bash
rsync -az --exclude .git --exclude '.venv*' --exclude __pycache__ --exclude .pytest_cache --exclude 1_survey /Users/sun/tongbu/study/phdproject/ForestNav/ 'gpu3070ti-relay:~/ForestNav/'
```

### Remote Training

```bash
ssh gpu3070ti-relay 'cd ~/ForestNav && PYTHONPATH=2_experiment .venv/bin/python -m forest_n3p.scripts.run_rl_rs_gate3_trial --output-dir 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1 --seed 20260704 --device cuda --train-curriculum-preset f03 --eval-curriculum-preset f03 --oracle-path 0_trials/module2_oracle_shape/oracle_connector_results.parquet --heldout-seed 20260704 --train-total-timesteps 100000 --train-n-envs 1 --train-n-steps 128 --train-batch-size 64 --train-n-epochs 4 --eval-episodes 64 --eval-min-episodes 64 --eval-success-threshold 0.8 --obs-patch-size-m 6.4 --obs-patch-cells 64 --max-steps 32 --allow-duplicate-openmp --bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt'
```

### Remote Audit

```bash
ssh gpu3070ti-relay 'cd ~/ForestNav && PYTHONPATH=2_experiment .venv/bin/python -m forest_n3p.scripts.audit_rl_rs_gate3_trial --trial-dir 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1 --min-formal-episodes 64 --required-success-threshold 0.8 --required-train-curriculum f03 --required-eval-curriculum f03 --warm-start-decision approved_obstacle_summary'
```

### Pull Back

```bash
rsync -az 'gpu3070ti-relay:~/ForestNav/0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/' /Users/sun/tongbu/study/phdproject/ForestNav/0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/
```
