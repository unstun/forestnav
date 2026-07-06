---
topic: module2-v2-formal-gate-gap-ledger
status: blocked_until_approved_or_frozen_contract
date: 2026-07-06
origin: ai+local-source
reviewed: false
selected_protocol_lane: stronger_obstacle_summary_warm_start
contract_path: .pipeline/contracts/module2-stronger_obstacle_summary_warm_start-v2.md
contract_status: draft
executes_training: false
executes_remote_preflight: false
paper_result_material: false
---

# Module2 V2 Formal Gate Gap Ledger

This file is a gate-facing status ledger, not paper result material. It records
what is still missing before the `stronger_obstacle_summary_warm_start` PPO
attempt can become formal evidence for replacing RS in Module2.

## Current Gate State

- Selected lane: `stronger_obstacle_summary_warm_start`.
- Contract action: `draft_new_contract`.
- Current contract: `.pipeline/contracts/module2-stronger_obstacle_summary_warm_start-v2.md`.
- Current contract status: `draft`; allowed training statuses are only
  `approved` or `frozen`.
- Existing negative evidence: the prior warm-start Gate3 run failed with
  `terminal_rs_success_rate=0.53125` against the locked `0.8` threshold.
- Current code status: train/eval/trial/preflight/audit can now carry
  `--contract-path`; preflight can also packetize the v2 stronger PPO budget and
  stabilization parameters.
- Current execution permission: no local training, no remote preflight, no
  remote PPO training, no H01/H02 formal evaluation, no formal claim, and no
  paper-result material.

## Evidence Checked

| Evidence | Current meaning |
|---|---|
| `0_trials/module2_formal_gate_protocol_lane_decision_record/protocol_lane_decision_record.md` | Dr Sun selected `stronger_obstacle_summary_warm_start`; the decision record explicitly does not authorize training or paper-result material. |
| `.pipeline/contracts/module2-stronger_obstacle_summary_warm_start-v2.md` | v2 exists but is still `draft`, so it blocks execution. |
| `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json` | Prior formal warm-start result is a threshold failure: `0.53125 < 0.8`. |
| `2_experiment/forest_n3p/scripts/train_rl_rs_ppo.py` | Training summary/config records `contract` and PPO hyperparameters. |
| `2_experiment/forest_n3p/scripts/eval_rl_rs_gate3.py` | Gate3 evaluation accepts and records `--contract-path`. |
| `2_experiment/forest_n3p/scripts/run_rl_rs_gate3_trial.py` | Trial runner passes `--contract-path` into train/eval and writes it into the trial manifest. |
| `2_experiment/forest_n3p/scripts/audit_rl_rs_gate3_trial.py` | Formal audit checks expected v2 contract path and emits `contract_path_mismatch` on drift. |
| `2_experiment/forest_n3p/scripts/preflight_rl_rs_gate3_formal_trial.py` | Preflight writes `contract`, `contract_status`, stronger PPO parameter protocol fields, and runner/audit commands without running training. |
| `2_experiment/forest_n3p/tests/test_preflight_rl_rs_gate3_formal_trial.py` | Targeted test covers v2 draft path propagation, stronger PPO parameter propagation, and draft-status blocking. |

## Missing Contract And Pre-Execution Artifacts

| Artifact | Missing state | Required proof |
|---|---|---|
| Approved/frozen v2 contract | Current v2 contract is `draft`. | Dr Sun explicitly promotes the contract to `approved` or `frozen` after resolving remote alias, budget, and failure-threshold questions. |
| Source-freshness regeneration after contract promotion | Not regenerated for the v2 approved/frozen contract. | Source-freshness artifacts point to the post-promotion commit and include the v2 contract path. |
| Remote alias confirmation | Contract still records `gpu3070ti-relay` and asks whether `gpu3070ti-reply` was intended. | SSH/readiness evidence confirms the actual 3070 Ti route before remote packet generation. |
| Remote execution packet for v2 | No fresh v2 packet exists. | Packet command includes the v2 contract path, 500000 timesteps, 4 envs, 256 steps, batch 256, 8 epochs, learning rate 0.0001, entropy coefficient 0.01, checkpoint frequency 25000, and the approved BC checkpoint. |
| Remote preflight manifest for v2 | No approved/frozen-contract preflight exists. | Preflight manifest reports `formal_trial_ready=true`, `contract_status=approved` or `frozen`, and no formal blockers. |

## Missing Training Artifacts

Expected attempt directory:
`0_trials/module2_gate3_formal/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706/`.

| Artifact | Required path or predicate | Invalid substitutes |
|---|---|---|
| PPO checkpoint bundle | `train/final_model.zip` plus periodic checkpoint files from the approved remote run. | Local PPO output, the failed `gate3_obstacle_summary_warm_approved_v1` checkpoint, or a checkpoint from a different contract path. |
| Train summary | `train/summary.json` reports `status=complete`, `smoke=false`, `contract=<v2 path>`, remote host, source head, seed, `warm_start_status=applied_obstacle_summary_bc`, and the full PPO hyperparameter block. | Stdout-only notes, summary from the failed run, summary without v2 contract path, or summary without stronger PPO parameters. |
| Training manifest | `train/training_manifest.json` records command provenance, source hashes, BC checkpoint hash, checkpoint hashes, and v2 contract path. | Manifest with `source_head=unknown`, missing hashes, missing BC hash, or old v1 contract path. |
| Pulled-back checkpoint hash | `train/final_model.zip.sha256` or equivalent JSON matches the evaluated checkpoint. | Remote stdout hash, hash for a different checkpoint, or no local pulled-back checkpoint. |

## Missing Evaluation Artifacts

| Artifact | Required path or predicate | Invalid substitutes |
|---|---|---|
| Gate3 episode CSV | `eval/gate3_eval_episodes.csv` from the new v2 attempt with at least 64 rows. | H02 smoke CSV, no-warm failure rows, or an aggregate summary without per-episode rows. |
| Gate3 summary | `eval/gate3_summary.json` records `contract=<v2 path>`, `episodes>=64`, `success_threshold=0.8`, terminal-RS success rate, collision rate, truncation rate, timing, seed, source head, and model hash. | Failed-run summary, summary without v2 contract path, summary without model hash, or paper-table preview. |

## Missing Acceptance Artifacts

| Artifact | Required path or predicate | Invalid substitutes |
|---|---|---|
| Trial manifest | `gate3_trial_manifest.json` ties train/eval outputs, source hashes, v2 contract path, and evaluated checkpoint identity. | Manifest from the failed run, manifest without contract path, or manifest without evaluated checkpoint identity. |
| Formal Gate3 audit | `gate3_formal_audit.json` reports `formal_decision=pass`, `required_success_threshold=0.8`, and v2 contract path. | `formal_decision=fail` reinterpreted as success, audit tied to old v1 contract path, or audit over smoke/candidate outputs. |
| H02 formal output acceptance | `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json` reports `formal_output_accepted=true`, `paper_result_input_allowed=true`, PPO rows, and accepted checkpoint hash. | Blocked H02 acceptance, H02 smoke rows, PPO rows without checkpoint hash, or paper prose. |

## Next Allowed Non-Training Work

1. Resolve v2 contract promotion questions: remote alias, stronger PPO budget,
   and unsafe-rollout failure thresholds.
2. Only after explicit promotion to `approved` or `frozen`, regenerate
   source-freshness and remote packet artifacts for the v2 contract.
3. Run remote preflight only after the regenerated packet says it is allowed.
4. Run remote PPO training only after preflight is ready and tied to the
   approved/frozen v2 contract.
5. Pull back train/eval/audit/hash artifacts, then run H02 acceptance.

Until those steps are complete, the current state remains formal-gate blocked.
