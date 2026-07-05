# Module2 Remote Formal Execution Packet

- status: `blocked_preconditions`
- ready to run remote training: `False`
- local training allowed: `False`
- GPU alias: `gpu3070ti-relay`

## Blockers
- `missing_module2_rl_rs_checkpoint`
- `realmap_query_generation_not_frozen`

## Remote Preflight Requirements

- `f02_6_decision_closed_for_preflight` (decision): status=`satisfied`, execution_allowed_now=`True`
  - invalid_substitutes: `decision packet recommendation without Dr Sun decision record; remote smoke output; manual command execution without approved record`
- `approved_remote_preflight_manifest` (remote_preflight): status=`satisfied`, execution_allowed_now=`True`
  - invalid_substitutes: `pending remote preflight manifest; CUDA import smoke not tied to the approved Gate3 command; local preflight output`
- `remote_preflight_protocol_contract` (remote_preflight): status=`satisfied`, execution_allowed_now=`True`
  - invalid_substitutes: `protocol missing eval_min_episodes or success threshold; CPU protocol; smoke protocol`
- `remote_preflight_command_packetized` (remote_preflight): status=`satisfied`, execution_allowed_now=`True`
  - invalid_substitutes: `bare local python preflight command; ssh command targeting another host; preflight command without approved warm-start decision`

## Post-Run Acceptance Requirements

- `pullback_expected_artifacts_complete` (pullback): status=`blocked_until_remote_audit`, remote_training_ready_now=`False`
  - invalid_substitutes: `remote stdout saying files exist; partial pullback with only checkpoint or summary; local files copied from a non-gpu3070ti host`
- `checkpoint_hash_manifest_recorded` (pullback): status=`blocked_until_remote_audit`, remote_training_ready_now=`False`
  - invalid_substitutes: `checkpoint file without hash; hash written before remote pullback; hash of a smoke or no-warm checkpoint`
- `gate3_formal_audit_accepts_remote_run` (acceptance): status=`blocked_until_remote_audit`, remote_training_ready_now=`False`
  - missing_artifact_ids: `gate3_formal_audit_formal_decision_pass`
  - invalid_substitutes: `audit marked not_formal, candidate, smoke, or preview; no-warm Gate3 audit reused as warm-start audit; training completion without audit`
- `h01_h02_regenerated_from_audited_checkpoint` (evaluation_acceptance): status=`blocked_until_remote_audit`, remote_training_ready_now=`False`
  - invalid_substitutes: `paper table preview generated before H02 acceptance; H01/H02 generated from a smoke checkpoint; claim safety run without regenerated formal evaluation rows`

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
