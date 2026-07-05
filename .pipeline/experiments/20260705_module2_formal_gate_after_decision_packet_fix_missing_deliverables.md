---
origin: ai+local
reviewed: false
created_at: 2026-07-05
topic: module2_formal_gate_after_decision_packet_fix_missing_deliverables
trust_level: internal_status_record
---

# Module2 Formal Gate State After F02.6 Decision-Packet Fix

## Scope

This checkpoint records the current PPO-replaces-RS formal-gate state after
commit `35a388d8` (`F02.6 decision packet keeps pending gate semantics`).

This file is not paper result material. It does not run local training, remote
preflight, remote training, remote audit, H01/H02 evaluation, claim generation,
or paper-readiness generation.

The purpose is narrow:

- keep the current dirty-diff fix tied to the formal gate;
- restate what training, evaluation, and acceptance evidence is still missing;
- prevent the existing failed run from being reused as a success result;
- preserve the next allowed action boundary before any new PPO success attempt.

## Current Gate Truth

Authoritative artifact:
`0_trials/module2_formal_gate_protocol_lane_status_report/protocol_lane_status_report.json`.

Current status:

- `status`: `protocol_lane_status_blocked_pending_lane_decision`
- `current_status.next_blocked_lane`: `protocol_lane_decision`
- `current_status.decision_record_status`: `pending_protocol_lane_decision`
- `current_status.allowed_next_action_ids`: `record_protocol_lane_decision`
- `current_status.selected_lane_id`: `null`
- `current_status.contract_action`: `none`
- `current_status.local_training_allowed_now`: `false`
- `current_status.remote_training_allowed_now`: `false`
- `current_status.new_success_training_allowed_now`: `false`
- `current_status.formal_claim_allowed_now`: `false`
- `current_status.paper_result_material_allowed_now`: `false`

Blocked actions at the current gate:

- `local_training`
- `remote_success_training`
- `remote_preflight_for_new_success_attempt`
- `formal_claim`
- `paper_result_material`

The next allowed action is therefore not training. It is a Dr Sun protocol-lane
decision record.

## Existing Failed Run Boundary

Authoritative artifact:
`0_trials/module2_formal_gate_next_round_requirements/formal_gate_next_round_requirements.json`.

Current failed run:

- `current_failed_run.formal_decision`: `fail`
- `current_failed_run.evaluator_decision`: `fail`
- `current_failed_run.failure_mode`: `threshold_failure`
- `current_failed_run.episodes`: `64`
- `current_failed_run.terminal_rs_success_rate`: `0.53125`
- `current_failed_run.required_success_threshold`: `0.8`
- `current_failed_run.threshold_deficit`: `0.26875`
- `current_failed_run.negative_formal_evidence_recorded`: `true`
- `current_failed_run.paper_success_claim_allowed`: `false`

Interpretation:

- The failed warm-start run may be retained as negative formal evidence.
- It is not a successful PPO replacement for RS.
- It cannot be used for paper result tables, success claims, or appendix result
  material.

## Current Failed-Run Artifact Coverage

Authoritative artifact:
`0_trials/module2_formal_gate_next_round_requirements/formal_gate_next_round_requirements.json`.

The current failed-run artifacts are sufficient to record the failure, not to
support a success claim.

- Training evidence for the failed run: `3` present, `0` missing.
- Evaluation evidence for the failed run: `2` present, `0` missing.
- Acceptance evidence for the failed run: `3` present, `0` missing.
- Formal-acceptance evidence for the failed run: `1` present, `1` missing.

The still-open failed-run formal-acceptance item is:

- `formal_acceptance:h02_formal_output_acceptance`

## H02 Acceptance Blocker

Authoritative artifact:
`0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`.

Current H02 state:

- `status`: `blocked_formal_output_acceptance`
- `formal_output_accepted`: `false`
- `paper_result_input_allowed`: `false`
- `formal_checks.gate3_formal_decision`: `fail`
- `formal_checks.gate3_formal_audit_passed`: `false`
- `formal_checks.scale_satisfies_h01`: `false`
- `method_checks.has_ppo_result_rows`: `false`
- `method_checks.ppo_rows_have_checkpoint_hash`: `false`

Current H02 blockers:

- `h02_verdict_not_formal`
- `gate3_formal_audit_not_passed`
- `h02_scale_below_h01_manifest`
- `missing_ppo_result_rows`

Interpretation:

- H02 cannot feed paper results.
- CSV schema validity is not enough.
- Smoke-scale or available-subset rows are invalid substitutes.
- PPO rows must exist and must carry the accepted checkpoint hash before H02 can
  become paper-result input.

## Next-Round Missing Deliverables

Authoritative artifact:
`0_trials/module2_formal_gate_next_round_requirements/formal_gate_next_round_requirements.json`.

### 1. Contract Deliverable

Requirement id: `new_or_revised_research_contract`.

Current status: `missing_required_before_new_training`.

Missing evidence:

- a new or revised `.pipeline/contracts/module2-*` Research Contract;
- status `approved` or `frozen` before any new success attempt;
- locked hypothesis;
- locked success signal;
- locked failure signal;
- locked training budget;
- locked protocol deltas.

Invalid substitutes:

- editing old results after seeing the failure;
- changing threshold, reward, curriculum, architecture, or observation without a
  new contract;
- chat-only approval without a committed contract artifact.

### 2. Training Deliverable

Requirement id: `new_remote_ppo_checkpoint_bundle`.

Current status: `blocked_until_contract`.

Missing evidence:

- remote-produced `train/final_model.zip` under a new attempt directory;
- `train/summary.json` with protocol label, training budget, seed, and
  terminal-RS training signals;
- `train/training_manifest.json` with source head, remote host, command
  provenance, and warm-start/protocol provenance;
- checkpoint hash or hash manifest tied to the same checkpoint that will be
  evaluated.

Invalid substitutes:

- local PPO training output;
- the failed warm-start Gate3 checkpoint;
- a checkpoint file without summary, manifest, or hash provenance.

### 3. Evaluation Deliverable

Requirement id: `new_formal_gate3_eval_bundle`.

Current status: `blocked_until_new_checkpoint`.

Missing evidence:

- `eval/gate3_eval_episodes.csv` from the new approved formal run;
- `eval/gate3_summary.json` with at least 64 formal episodes;
- terminal-RS success rate;
- collision rate;
- truncation rate;
- timing;
- seed and protocol provenance.

Invalid substitutes:

- H02 available-subset smoke CSV;
- no-warm failure rows reused for a warm-start or new-lane success claim;
- summary JSON without per-episode CSV.

### 4. Acceptance Deliverable

Requirement id: `new_gate3_audit_and_hash_acceptance`.

Current status: `blocked_until_new_eval`.

Missing evidence:

- new `gate3_formal_audit.json` with `formal_decision=pass`;
- `gate3_trial_manifest.json` tying train, eval, audit, source head, and
  approved/frozen contract together;
- `train/final_model.zip.sha256` or equivalent hash manifest matching the
  pulled-back checkpoint;
- local pullback of the remote train/eval/audit bundle.

Invalid substitutes:

- reinterpreting `formal_decision=fail` as success;
- remote stdout without local pullback;
- checkpoint hash not tied to the evaluated checkpoint.

### 5. Formal-Acceptance Deliverable

Requirement id: `h02_formal_output_acceptance`.

Current status: `blocked_until_new_gate3_pass`.

Missing evidence:

- `h02_formal_acceptance.json` with `formal_output_accepted=true`;
- `paper_result_input_allowed=true`;
- formal PPO rows present;
- accepted checkpoint hash present in PPO rows;
- H02 scale satisfying the frozen H01 manifest.

Invalid substitutes:

- blocked H02 acceptance;
- formal-looking tables generated from smoke scale;
- PPO rows without checkpoint hash.

## Protocol Lane Choices Still Open

Authoritative artifact:
`0_trials/module2_formal_gate_protocol_lane_matrix/formal_gate_protocol_lane_matrix.json`.

Valid lane ids:

- `stronger_obstacle_summary_warm_start`
- `full_patch_cnn_policy`
- `hybrid_ppo_analytic_fallback`
- `stop_or_reframe_module2_claim`

All lanes currently have:

- `training_allowed_now`: `false`
- `paper_result_material_allowed_now`: `false`
- `requires_new_or_revised_contract`: `true`

Cross-lane invariants:

- Local PPO training output is not formal evidence for any lane.
- Any new success-attempt remote training requires an approved or frozen
  new/revised contract first.
- The failed warm-start checkpoint can be negative evidence only.
- Paper result material requires H02 `formal_output_accepted=true` and
  `paper_result_input_allowed=true`.

## Next Allowed Action

The next allowed action is:

1. Record Dr Sun's protocol-lane decision.

The next disallowed actions remain:

1. local PPO training;
2. remote success training before lane decision and contract approval/freeze;
3. remote preflight for a new success attempt before lane decision and contract
   gate;
4. formal success claim;
5. paper result or appendix result material.

## Verification Performed

- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_f02_6_warm_start_decision_packet.py`
  -> `1 passed`
- `git diff --check` -> no output
- `git commit -m '修复：F02.6 decision packet保持pending守门语义'`
  -> `35a388d8`
- `jq '.' 0_trials/module2_formal_gate_protocol_lane_status_report/protocol_lane_status_report.json`
- `jq '.' 0_trials/module2_formal_gate_next_round_requirements/formal_gate_next_round_requirements.json`
- `jq '.' 0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
- `jq '.' 0_trials/module2_formal_gate_protocol_lane_matrix/formal_gate_protocol_lane_matrix.json`
- `jq '.' 0_trials/module2_formal_gate_protocol_lane_decision_record/protocol_lane_decision_record.json`

No local training, remote preflight, remote training, remote audit, H01/H02
regeneration, claim generation, paper table generation, or appendix-result
material generation was run.
