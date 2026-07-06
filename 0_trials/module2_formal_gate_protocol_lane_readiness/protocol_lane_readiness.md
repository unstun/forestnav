# Module2 Protocol Lane Readiness Packet

This packet is a read-only decision-preparation artifact. It is not paper result material.

## Current Gate

- status: `protocol_lane_readiness_ready_for_dr_sun_decision`
- next_blocked_lane: `protocol_lane_decision`
- decision_owner_required: `Dr Sun`
- selected_lane_id: `None`
- next_action_ids: `record_protocol_lane_decision`
- remote_training_allowed_now: `False`
- formal_claim_allowed_now: `False`
- paper_result_material_allowed_now: `False`

## Failed Gate3 Basis

- formal_decision: `fail`
- failure_mode: `threshold_failure`
- terminal_rs_success_rate: `0.53125`
- required_success_threshold: `0.8`
- threshold_deficit: `0.26875`

## Lane Readiness

| lane_id | claim_scope | next_action_after_selection | remote_training_now |
|---|---|---|---|
| `stronger_obstacle_summary_warm_start` | direct PPO replacement attempt remains possible only if the new contract preserves the replacement claim boundary | `draft_new_or_revised_contract_then_remote_training_packet` | `False` |
| `full_patch_cnn_policy` | direct PPO replacement claim changes substantially and must be re-registered as an observation/architecture delta | `draft_new_or_revised_contract_then_remote_training_packet` | `False` |
| `hybrid_ppo_analytic_fallback` | claim likely changes from PPO replacing RS to PPO assisting/selecting/recovering around analytic planning | `draft_new_or_revised_contract_then_remote_training_packet` | `False` |
| `stop_or_reframe_module2_claim` | no new success-attempt training; use failure as negative evidence or reframe the module2 contribution | `draft_stop_or_reframe_contract` | `False` |

## Lane Evidence Details

### stronger_obstacle_summary_warm_start

- new_success_training_required_if_selected: `True`
- blocked_until: `record_protocol_lane_decision, approved_or_frozen_new_or_revised_contract`
- required_decision_justification:
  - why this lane is justified after observing the failed warm-start Gate3 run
  - which claim wording remains allowed if this lane is selected
  - which prior failed artifacts are only negative evidence and cannot be reused as success evidence
  - why direct PPO replacement is still plausible under compact obstacle-summary features
- required_contract_deltas:
  - warm-start dataset source and acceptance checks
  - PPO stabilization changes
  - curriculum and reward deltas
  - budget and seed policy
- required_training_evidence:
  - new remote checkpoint bundle under a new attempt directory
  - new train/summary.json with protocol label and terminal-RS training signals
  - new training_manifest.json with source head, remote host, command, seed, and warm-start provenance
- required_evaluation_evidence:
  - new formal Gate3 eval CSV with at least 64 episodes
  - new gate3_summary.json with terminal-RS success, collision, truncation, and timing fields
- required_acceptance_evidence:
  - formal_decision=pass in the new gate3_formal_audit.json
  - checkpoint hash tied to the evaluated checkpoint
  - H02 formal_output_accepted=true with PPO rows and checkpoint hash
- invalid_substitutes:
  - the failed warm-start checkpoint
  - more prose explaining the failed result
  - local PPO training output
  - H02 smoke rows without formal PPO rows

### full_patch_cnn_policy

- new_success_training_required_if_selected: `True`
- blocked_until: `record_protocol_lane_decision, approved_or_frozen_new_or_revised_contract`
- required_decision_justification:
  - why this lane is justified after observing the failed warm-start Gate3 run
  - which claim wording remains allowed if this lane is selected
  - which prior failed artifacts are only negative evidence and cannot be reused as success evidence
  - why architecture/observation change is necessary and how it changes fairness against RS
- required_contract_deltas:
  - observation tensor definition
  - CNN architecture and inference budget
  - comparison fairness against RS/analytic baselines
  - new H01/H02 schema fields if telemetry changes
- required_training_evidence:
  - remote training packet with CNN dependencies and deterministic config
  - checkpoint bundle with architecture metadata
  - training manifest recording observation schema version
- required_evaluation_evidence:
  - formal Gate3 eval using the same observation schema as training
  - timing budget evidence for CNN inference
  - per-episode records exposing failure modes beyond success rate
- required_acceptance_evidence:
  - audit proving formal pass under the CNN protocol
  - H02 rows that identify the CNN PPO method and checkpoint hash
  - claim boundary stating this is not the same protocol as the failed compact policy
- invalid_substitutes:
  - using compact-policy failure as CNN success evidence
  - architecture change without revised contract
  - timing-unchecked CNN results
  - paper table without method/schema distinction

### hybrid_ppo_analytic_fallback

- new_success_training_required_if_selected: `True`
- blocked_until: `record_protocol_lane_decision, approved_or_frozen_new_or_revised_contract`
- required_decision_justification:
  - why this lane is justified after observing the failed warm-start Gate3 run
  - which claim wording remains allowed if this lane is selected
  - which prior failed artifacts are only negative evidence and cannot be reused as success evidence
  - whether the target claim changes from replacement to analytic-assisted hybrid control
- required_contract_deltas:
  - hybrid control handoff rule
  - fallback usage metric
  - success signal that separates PPO-only from analytic-assisted success
  - paper claim boundary for hybrid assistance
- required_training_evidence:
  - remote checkpoint for the learned selector/recovery policy
  - training manifest recording analytic fallback interface
  - logs that expose fallback-trigger distribution
- required_evaluation_evidence:
  - formal eval with fallback usage columns
  - paired PPO-only / hybrid / RS baseline comparison if claiming assistance
  - collision and recovery metrics tied to fallback events
- required_acceptance_evidence:
  - formal audit using hybrid-specific success and failure signals
  - H02 rows that expose fallback usage and checkpoint hash
  - claim safety artifact that prevents wording as pure RS replacement unless proven
- invalid_substitutes:
  - calling hybrid success direct PPO replacement
  - hiding RS/analytic fallback calls inside aggregate success
  - using direct-replacement threshold without a hybrid contract
  - paper prose that omits fallback usage

### stop_or_reframe_module2_claim

- new_success_training_required_if_selected: `False`
- blocked_until: `record_protocol_lane_decision, approved_or_frozen_negative_or_reframe_contract`
- required_decision_justification:
  - why this lane is justified after observing the failed warm-start Gate3 run
  - which claim wording remains allowed if this lane is selected
  - which prior failed artifacts are only negative evidence and cannot be reused as success evidence
  - why no new success-attempt training is warranted and what negative-result claim remains
- required_contract_deltas:
  - stop criterion
  - negative-result scope
  - allowed paper claim after failure
  - archival requirements for failed checkpoint and audit
- required_training_evidence:
  - no new training evidence required if the contract explicitly stops success attempts
- required_evaluation_evidence:
  - existing failed formal Gate3 audit retained as negative evidence
  - failure-mode analysis from existing eval CSV/logs only
- required_acceptance_evidence:
  - claim safety audit blocks success wording
  - H02 remains blocked for success results
  - paper-readiness artifact, if later used, is scoped to negative evidence only
- invalid_substitutes:
  - quietly dropping failed PPO without recording the stop decision
  - writing a positive replacement claim from failed evidence
  - running new training while pretending the lane was stop/reframe

## Shared Next Success Attempt Artifact Index

- `new_or_revised_research_contract` (contract): status=`missing_required_before_new_success_training`, blocked_until=`record_protocol_lane_decision`
- `train_final_model_zip` (training): status=`not_created_for_next_success_attempt`, blocked_until=`approved_or_frozen_new_or_revised_contract`
- `train_summary_json` (training): status=`not_created_for_next_success_attempt`, blocked_until=`approved_or_frozen_new_or_revised_contract`
- `train_training_manifest_json` (training): status=`not_created_for_next_success_attempt`, blocked_until=`approved_or_frozen_new_or_revised_contract`
- `eval_gate3_eval_episodes_csv` (evaluation): status=`blocked_until_new_checkpoint`, blocked_until=`new_remote_ppo_checkpoint_bundle`
- `eval_gate3_summary_json` (evaluation): status=`blocked_until_new_checkpoint`, blocked_until=`new_remote_ppo_checkpoint_bundle`
- `gate3_trial_manifest_json` (acceptance): status=`blocked_until_new_eval`, blocked_until=`new_formal_gate3_eval_bundle`
- `gate3_formal_audit_json` (acceptance): status=`blocked_until_new_eval`, blocked_until=`new_formal_gate3_eval_bundle`
- `pulled_back_checkpoint_hash_record` (acceptance): status=`blocked_until_new_eval`, blocked_until=`new_formal_gate3_eval_bundle`
- `h02_formal_output_acceptance` (formal_acceptance): status=`blocked_until_new_gate3_pass`, blocked_until=`new_gate3_audit_and_hash_acceptance`

## Claim Boundaries
- This readiness packet is not a protocol-lane decision record.
- It does not authorize local training, remote preflight, remote training, formal claims, or paper result material.
- Every non-stop success lane still requires a new or revised approved/frozen Research Contract before remote training.
- The failed Gate3 run is negative evidence only: terminal-RS success 0.53125 remains below the 0.8 threshold.

## Audit

- audit_issue_count: `0`
- no audit issues
