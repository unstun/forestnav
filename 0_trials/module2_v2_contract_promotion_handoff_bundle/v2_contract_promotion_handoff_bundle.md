# Module2 V2 Contract Promotion Handoff Bundle

This artifact packages the next human decision boundary for the v2 stronger obstacle-summary warm-start contract. It does not approve the contract, write files, run remote preflight, train, or create paper result material.

## Status

- status: `ready_for_dr_sun_v2_contract_promotion_handoff`
- contract_status_now: `draft`
- selected_lane_id: `stronger_obstacle_summary_warm_start`
- contract_action: `draft_new_contract`
- audit_issue_count: `0`
- remote_preflight_allowed_now: `False`
- remote_training_allowed_now: `False`

## Future Apply Command

Only run this after Dr Sun explicitly approves the promotion decision in the current gate.

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.apply_module2_v2_contract_promotion --status approved --decider 'Dr Sun' --remote-alias gpu3070ti-relay --confirm-training-budget --confirm-unsafe-failure-thresholds
```

## Handoff Checks

- contract_remains_draft: passed=`True` observed=`draft` expected=`draft`
- promotion_readiness_ready: passed=`True` observed=`ready_for_dr_sun_v2_contract_promotion_decision` expected=`ready_for_dr_sun_v2_contract_promotion_decision`
- promotion_packet_ready: passed=`True` observed=`v2_contract_promotion_packet_ready_awaiting_dr_sun` expected=`v2_contract_promotion_packet_ready_awaiting_dr_sun`
- promotion_packet_has_four_approval_items: passed=`True` observed=`['contract_status_action', 'remote_alias', 'training_budget', 'unsafe_failure_thresholds']` expected=`['contract_status_action', 'remote_alias', 'training_budget', 'unsafe_failure_thresholds']`
- promotion_dry_run_ready_and_read_only: passed=`True` observed=`{'status': 'promotion_apply_ready', 'dry_run': True, 'writes_contract': False}` expected=`{'status': 'promotion_apply_ready', 'dry_run': True, 'writes_contract': False}`
- chain_waits_at_contract_promotion: passed=`True` observed=`v2_contract_promoted` expected=`v2_contract_promoted`
- post_promotion_plan_waits_for_dr_sun: passed=`True` observed=`await_dr_sun_before_apply_v2_contract_promotion` expected=`await_dr_sun_before_apply_v2_contract_promotion`
- remaining_evidence_still_missing_before_training: passed=`True` observed=`12` expected=`> 0`

## Post-Apply Required Commands

- rerun_v2_contract_readiness_gate: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_v2_contract_readiness_gate`
- rerun_source_freshness_audit: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_source_freshness_audit`
- regenerate_v2_remote_execution_packet: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_v2_remote_execution_packet`
- refresh_v2_remaining_evidence: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_v2_formal_gate_remaining_evidence`
- refresh_v2_formal_gate_chain_audit: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_v2_formal_gate_chain_audit`
- refresh_post_promotion_regeneration_plan: `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_v2_post_promotion_regeneration_plan`

## Remaining Evidence Summary

- total_required_evidence_items: `12`
- total_missing_or_unsatisfied: `12`
- training_missing_or_unsatisfied: `3`
- evaluation_missing_or_unsatisfied: `2`
- acceptance_missing_or_unsatisfied: `3`
- formal_acceptance_missing_or_unsatisfied: `1`

## Invalid Substitutes

- chat-only approval without committed contract frontmatter
- promotion packet alone as approval
- promotion dry-run alone as approval
- old v1 contract or old v1 remote packet
- failed gate3_obstacle_summary_warm_approved_v1 checkpoint
- remote preflight smoke before regenerated source-freshness and v2 packet gates
- local PPO training output
- paper prose, result table, or appendix text before H02 formal acceptance

## Audit Issues

- none
