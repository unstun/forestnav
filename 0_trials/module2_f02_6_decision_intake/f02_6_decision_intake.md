# Module2 F02.6 Decision Intake

This read-only artifact explains how F02.6 can be closed. It does not record a decision, run preflight, train, or write paper results.

- status: `f02_6_decision_intake_pending_clean`
- decision_owner_required: `Dr Sun`
- record_status: `pending_human_decision`
- effective_warm_start_decision: `pending`
- packet_recommendation: `approve_obstacle_summary_warm_start`
- next_blocked_lane: `decision`
- missing_deliverable_count: `10`
- local_training_allowed_now: `False`
- remote_preflight_allowed_now: `False`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`

## Required Fields

- `decision`: must be one of approve_obstacle_summary_warm_start or reject_obstacle_summary_warm_start
- `decider`: must equal Dr Sun
- `decision_note`: must be a human-readable Dr Sun note explaining the approval or rejection rationale

## Command Templates

### approve_obstacle_summary_warm_start
```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_decision_record --decision approve_obstacle_summary_warm_start --decider 'Dr Sun' --decision-note '<Dr Sun approval note>'
```

### reject_obstacle_summary_warm_start
```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_decision_record --decision reject_obstacle_summary_warm_start --decider 'Dr Sun' --decision-note '<Dr Sun rejection note>'
```

## Invalid Inputs

- `decider other than Dr Sun`: Only Dr Sun can close F02.6.
- `approval or rejection without a decision note`: A formal research decision must preserve rationale for audit and future paper rebuttal.
- `manual permission flips in downstream JSON`: Downstream permissions must be regenerated from the decision record and gate artifacts.
- `local training output`: The formal PPO checkpoint must be produced on gpu3070ti-relay after the gate opens.
- `paper result table or claim preview`: F02.6 intake is not formal evaluation evidence.

## Audit Issues

- none

## Claim Boundaries

- This intake explains how to close F02.6; it does not close F02.6.
- It must not be cited as a PPO performance result or warm-start effect result.
- The only valid decider for a non-pending F02.6 record is Dr Sun.
- Approval records the human decision and leads to source-fresh gate regeneration; it is not a command to train.
- Rejected obstacle-summary warm-start keeps formal warm-start PPO blocked and routes to a stronger/full patch-CNN protocol.
- Local PPO training remains disallowed.
