# Module2 V2 Post-Promotion Regeneration Plan

This artifact plans the local gate regeneration sequence after v2 contract promotion. It does not execute the commands, train, run remote preflight, or write paper results.

## Status

- status: `ready_for_run_remote_preflight_only`
- contract_status: `approved`
- next_action: `run_remote_preflight_only`
- remote_preflight_allowed_now: `False`
- remote_training_allowed_now: `False`

## Ordered Targets

### `apply_v2_contract_promotion`
- category: `contract`
- satisfied_now: `True`
- allowed_now: `False`
- blocked_by: ``
- runs_remote_preflight: `False`
- runs_training: `False`

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.apply_module2_v2_contract_promotion --status approved --decider 'Dr Sun' --remote-alias gpu3070ti-relay --confirm-training-budget --confirm-unsafe-failure-thresholds
```

### `rerun_v2_contract_readiness_gate`
- category: `local_gate`
- satisfied_now: `True`
- allowed_now: `True`
- blocked_by: ``
- runs_remote_preflight: `False`
- runs_training: `False`

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_v2_contract_readiness_gate
```

### `rerun_source_freshness_audit`
- category: `local_gate`
- satisfied_now: `True`
- allowed_now: `True`
- blocked_by: ``
- runs_remote_preflight: `False`
- runs_training: `False`

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_source_freshness_audit
```

### `regenerate_v2_remote_execution_packet`
- category: `local_gate`
- satisfied_now: `True`
- allowed_now: `True`
- blocked_by: ``
- runs_remote_preflight: `False`
- runs_training: `False`

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_v2_remote_execution_packet
```

### `rerun_v2_formal_gate_chain_audit`
- category: `local_gate`
- satisfied_now: `True`
- allowed_now: `True`
- blocked_by: ``
- runs_remote_preflight: `False`
- runs_training: `False`

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_v2_formal_gate_chain_audit
```

### `run_remote_preflight_only`
- category: `remote_preflight`
- satisfied_now: `False`
- allowed_now: `True`
- blocked_by: ``
- runs_remote_preflight: `True`
- runs_training: `False`

```bash
ssh gpu3070ti-relay 'cd '"'"'~/ForestNav'"'"' && PYTHONPATH=2_experiment .venv/bin/python -m forest_n3p.scripts.preflight_rl_rs_gate3_formal_trial --output-dir 0_trials/module2_gate3_formal/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706 --manifest-out 0_trials/module2_remote_preflight/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706/gate3_preflight_manifest.json --contract-path .pipeline/contracts/module2-stronger_obstacle_summary_warm_start-v2.md --seed 20260706 --device cuda --oracle-path 0_trials/module2_oracle_shape/oracle_connector_results.parquet --heldout-seed 20260706 --train-total-timesteps 500000 --train-n-envs 4 --train-n-steps 256 --train-batch-size 256 --train-n-epochs 8 --train-learning-rate 0.0001 --train-ent-coef 0.01 --train-checkpoint-freq 25000 --eval-episodes 64 --eval-min-episodes 64 --eval-success-threshold 0.8 --bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt --warm-start-decision approved_obstacle_summary --allow-existing-output-dir --allow-duplicate-openmp'
```

### `run_remote_training_after_preflight`
- category: `remote_training`
- satisfied_now: `False`
- allowed_now: `False`
- blocked_by: `v2_remote_preflight_not_ready`
- runs_remote_preflight: `False`
- runs_training: `True`

```bash
ssh gpu3070ti-relay 'cd '"'"'~/ForestNav'"'"' && PYTHONPATH=2_experiment .venv/bin/python -m forest_n3p.scripts.run_rl_rs_gate3_trial --output-dir 0_trials/module2_gate3_formal/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706 --contract-path .pipeline/contracts/module2-stronger_obstacle_summary_warm_start-v2.md --seed 20260706 --device cuda --train-curriculum-preset f03 --eval-curriculum-preset f03 --oracle-path 0_trials/module2_oracle_shape/oracle_connector_results.parquet --heldout-seed 20260706 --train-total-timesteps 500000 --train-n-envs 4 --train-n-steps 256 --train-batch-size 256 --train-n-epochs 8 --train-learning-rate 0.0001 --train-ent-coef 0.01 --train-checkpoint-freq 25000 --eval-episodes 64 --eval-min-episodes 64 --eval-success-threshold 0.8 --bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt --allow-duplicate-openmp'
```

### `pullback_eval_audit_hash_artifacts`
- category: `acceptance`
- satisfied_now: `False`
- allowed_now: `False`
- blocked_by: `remote_training_not_completed`
- runs_remote_preflight: `False`
- runs_training: `False`

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_v2_formal_gate_remaining_evidence
```

## Invalid Substitutes

- promotion dry-run treated as approval
- running source freshness before contract is approved or frozen
- old v1 remote execution packet
- remote preflight smoke
- remote training before ready preflight manifest
- paper result prose before H02 formal acceptance
