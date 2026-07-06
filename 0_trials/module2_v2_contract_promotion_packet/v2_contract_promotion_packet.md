# Module2 V2 Contract Promotion Packet

This file is an approval packet for Dr Sun. It does not approve the contract, run preflight, run training, or write paper results.

## Status

- status: `v2_contract_promotion_packet_ready_awaiting_dr_sun`
- contract_promotion_allowed_by_packet: `False`
- remote_training_allowed_now: `False`
- audit_issue_count: `0`

## Current Gate

- status: `v2_contract_readiness_blocked`
- source_head: `21a4f99885461c99d3b97ba3c9ad39551ac3803d`
- next_action: `promote_or_edit_v2_contract_before_source_freshness`
- blocker_count: `1`
- blockers: `contract_status_not_approved_or_frozen`
- runner_command_contains_v2_params: `True`
- remote_training_allowed_now: `False`

## Remote Alias Evidence

- recommended_alias: `gpu3070ti-relay`
- gpu3070ti-relay: `alias=gpu3070ti-relay, user=ubuntu, hostname=127.0.0.1, port=23070, proxyjump=ubuntu-obgx`
- gpu3070ti-reply: `alias=gpu3070ti-reply, user=sun, hostname=gpu3070ti-reply, port=22`

## Approval Items

- `remote_alias`: awaiting_dr_sun_confirmation -> `gpu3070ti-relay`
- `training_budget`: awaiting_dr_sun_approval -> `seed=20260706, train_total_timesteps=500000, train_n_envs=4, train_n_steps=256, train_batch_size=256, train_n_epochs=8, train_learning_rate=0.0001, train_ent_coef=0.01, train_checkpoint_freq=25000`
- `unsafe_failure_thresholds`: awaiting_dr_sun_approval -> `collision_rate_gte=0.3, truncation_rate_gte=0.2`
- `contract_status_action`: awaiting_dr_sun_approval -> `approved`

## Audit Issues

- none

## Post-Approval Next Steps

- commit the contract status promotion to approved or frozen
- re-run v2 contract readiness gate and require v2_contract_ready_for_source_freshness
- regenerate source-freshness artifacts from the post-promotion commit
- generate the v2 remote execution packet
- run remote preflight only after the regenerated packet allows it
