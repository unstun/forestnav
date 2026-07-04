# Module2 F02.6 Decision Record

- status: `pending_human_decision`
- requested decision: `pending`
- effective warm-start decision: `pending`
- decider: `None`
- remote training allowed: `False`
- remote preflight allowed now: `False`
- remote training allowed now: `False`
- local training allowed: `False`
- formal claim allowed: `False`
- next remote preflight status: `blocked_until_decision`

## Blockers
- `requires_dr_sun_approval`

## Packet
- path: `0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json`
- status: `pending_human_decision`
- recommendation: `approve_obstacle_summary_warm_start`

## Remote Preflight Intent
- host: `gpu3070ti-relay`
- observed pending preflight: `blocked`

```bash
python -m forest_n3p.scripts.preflight_rl_rs_gate3_formal_trial --output-dir 0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_approved_remote_v1 --manifest-out 0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_approved_remote_v1/gate3_preflight_manifest.json --warm-start-decision approved_obstacle_summary --bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt --device cuda --allow-duplicate-openmp --allow-existing-output-dir
```

## Claim Boundaries
- This record only stores Dr Sun's F02.6 decision state; it is not a training result.
- Approval unlocks source-fresh regeneration and approved preflight regeneration, but does not itself allow remote execution now.
- Formal PPO warm-start training must run on gpu3070ti-relay, not on the local Mac.
- A rejected obstacle-summary warm-start requires a stronger/full patch-CNN protocol before a warm-start formal run.
