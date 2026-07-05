# Module2 Formal Gate Protocol Lane Matrix

This file is a formal-gate lane evidence artifact, not paper result material.

## Gate Summary

- current_formal_decision: `fail`
- current_failure_mode: `threshold_failure`
- terminal_rs_success_rate: `0.53125`
- required_success_threshold: `0.8`
- new_success_training_allowed_now: `False`
- remote_training_allowed_now: `False`
- local_training_allowed_now: `False`
- formal_claim_allowed_now: `False`

## Lane Matrix

| lane | claim_scope | training_allowed_now |
|---|---|---:|
| `stronger_obstacle_summary_warm_start` | direct PPO replacement attempt remains possible only if the new contract preserves the replacement claim boundary | `False` |
| `full_patch_cnn_policy` | direct PPO replacement claim changes substantially and must be re-registered as an observation/architecture delta | `False` |
| `hybrid_ppo_analytic_fallback` | claim likely changes from PPO replacing RS to PPO assisting/selecting/recovering around analytic planning | `False` |
| `stop_or_reframe_module2_claim` | no new success-attempt training; use failure as negative evidence or reframe the module2 contribution | `False` |

## Lane Evidence Details

### `stronger_obstacle_summary_warm_start`

- status: `candidate_requires_dr_sun_decision_and_contract`
- requires_new_or_revised_contract: `True`
- paper_result_material_allowed_now: `False`
- what_changes: keep compact obstacle-summary policy family but strengthen warm-start dataset, curriculum, or PPO stabilization protocol
- must_justify:
  - why the 0.53125 formal success rate is expected to improve
  - which failure modes are addressed without changing the meaning of PPO-vs-RS
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

### `full_patch_cnn_policy`

- status: `candidate_requires_dr_sun_decision_and_contract`
- requires_new_or_revised_contract: `True`
- paper_result_material_allowed_now: `False`
- what_changes: move from compact summary features toward a spatial patch/CNN observation policy
- must_justify:
  - why spatial structure is necessary for the formal gate
  - how observation and architecture changes preserve a fair RS replacement claim
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

### `hybrid_ppo_analytic_fallback`

- status: `candidate_requires_dr_sun_decision_and_contract`
- requires_new_or_revised_contract: `True`
- paper_result_material_allowed_now: `False`
- what_changes: treat PPO as a learned selector or recovery layer instead of direct RS replacement
- must_justify:
  - whether the claim changes from replacement to hybrid assistance
  - how hybrid control is evaluated without hiding RS usage
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

### `stop_or_reframe_module2_claim`

- status: `candidate_requires_dr_sun_decision_and_contract`
- requires_new_or_revised_contract: `True`
- paper_result_material_allowed_now: `False`
- what_changes: record the formal failure and stop pursuing PPO replacement under the current module2 claim
- must_justify:
  - which negative evidence is sufficient to stop
  - what paper claim remains defensible without formal PPO success
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

## Cross-Lane Invariants
- `no_local_training`: Local PPO training output is not formal evidence for any lane.
- `contract_before_new_success_training`: Any new success-attempt remote training requires an approved or frozen new/revised contract first.
- `failed_checkpoint_not_success_evidence`: The failed warm-start checkpoint can be negative evidence only, not a success checkpoint.
- `h02_before_paper_results`: Paper result material requires H02 formal_output_accepted=true and paper_result_input_allowed=true.

## Audit

- status: `formal_gate_protocol_lane_matrix_ready`
- audit_issue_count: `0`
