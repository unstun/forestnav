# Module2 F02.6 Decision Record

- status: `approved`
- requested decision: `approve_obstacle_summary_warm_start`
- effective warm-start decision: `approved_obstacle_summary`
- decider: `Dr Sun`
- decision note audit: `{'required_for_non_pending_decision': True, 'present': True, 'character_count': 378, 'word_count': 46, 'guidance_items': ['selected decision', 'human rationale', 'evidence basis', 'risk accepted or avoided', 'next gated action'], 'mentions_selected_route': True, 'mentions_evidence_or_risk_basis': True, 'mentions_next_gated_action': True, 'quality_warning': None}`
- remote training allowed: `True`
- remote preflight allowed now: `False`
- remote training allowed now: `False`
- local training allowed: `False`
- formal claim allowed: `False`
- paper result material allowed now: `False`
- decision_record_is_not_training_authorization: `True`
- decision_record_is_not_paper_result_material: `True`
- next remote preflight status: `ready_to_regenerate_approved_warm_start_preflight`

## Blockers
- none

## Packet
- path: `0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json`
- status: `pending_human_decision`
- recommendation: `approve_obstacle_summary_warm_start`

## Current Authorization Boundary
- authorization_status: `decision_recorded_not_execution_authorization`
- current_allowed_action_ids: `regenerate_post_f02_6_gate_artifacts`
- current_blocked_action_ids: `remote_preflight, remote_training, local_training, formal_claim, paper_result_material`
- post_decision_routes_are_current_authorization: `False`
- remote_preflight_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`

## Post-Decision Non-Authorization Invariants
- formal_training_still_requires: `source_freshness_audit, post_f02_6_regeneration_plan, post_f02_6_plan_audit, remote_formal_execution_packet_ready, approved_remote_preflight`
- blocked_after_decision_record_count: `4`

## Remote Preflight Intent
- host: `gpu3070ti-relay`
- observed pending preflight: `ready`

```bash
python -m forest_n3p.scripts.preflight_rl_rs_gate3_formal_trial --output-dir 0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_approved_remote_v1 --manifest-out 0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_approved_remote_v1/gate3_preflight_manifest.json --warm-start-decision approved_obstacle_summary --bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt --device cuda --allow-duplicate-openmp --allow-existing-output-dir
```

## Claim Boundaries
- This record only stores Dr Sun's F02.6 decision state; it is not a training result.
- Approval unlocks source-fresh regeneration and approved preflight regeneration, but does not itself allow remote execution now.
- Formal PPO warm-start training must run on gpu3070ti-relay, not on the local Mac.
- A rejected obstacle-summary warm-start requires a stronger/full patch-CNN protocol before a warm-start formal run.
