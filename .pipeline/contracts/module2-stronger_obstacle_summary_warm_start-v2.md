---
topic: module2-stronger_obstacle_summary_warm_start
status: approved
version: v2-draft
date: 2026-07-06
origin: ai+local-source
reviewed: false
parent_contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
selected_protocol_lane: stronger_obstacle_summary_warm_start
contract_action: draft_new_contract
training_allowed: false
remote_training_allowed_now: false
local_training_allowed_now: false
formal_claim_allowed_now: false
paper_result_material_allowed_now: false
allowed_status_before_training:
  - approved
  - frozen
promotion_decider: Dr Sun
approved_remote_alias: gpu3070ti-relay
promotion_packet: 0_trials/module2_v2_contract_promotion_packet/v2_contract_promotion_packet.json
contract_approved_for_source_freshness: true
---

# Research Contract Draft: Module2 Stronger Obstacle-Summary Warm Start

This file is a draft Research Contract. It is not training authorization, not a
remote preflight packet, not a formal evaluation, and not paper result material.
It may be edited until Dr Sun explicitly promotes it to `approved` or `frozen`.
Until then, no local training, remote preflight, remote PPO training, formal
claim, or result-table writing is authorized.

## 0. Evidence Basis

| Evidence | What it contributes |
|---|---|
| `.pipeline/contracts/module2-ppo-funnel-expansion.md:21-39` | v1 hypothesis and Gate #3 failure criterion: terminal-RS connectability must exceed 80 percent within the prescribed budget. |
| `0_trials/module2_formal_gate_protocol_lane_decision_record/protocol_lane_decision_record.md:7-21` | Dr Sun selected `stronger_obstacle_summary_warm_start`; this selection does not authorize training or paper-result material. |
| `0_trials/module2_formal_gate_protocol_lane_decision_record/protocol_lane_decision_record.md:61-73` | A new or revised contract is required before training; paper result still requires Gate3 pass and H02 acceptance. |
| `0_trials/module2_formal_gate_post_decision_contract_plan/post_decision_contract_plan.md:29-45` | Selected lane expects a new v2 contract, fresh training/evaluation/acceptance artifacts, and invalidates the failed warm-start checkpoint as a substitute. |
| `0_trials/module2_formal_gate_post_decision_contract_plan/post_decision_contract_plan.md:102-113` | Next success attempt still needs 10 fresh artifacts across contract, training, evaluation, acceptance, and formal-acceptance categories. |
| `0_trials/module2_formal_gate_contract_intake/formal_gate_contract_intake.json:52-160` | Required contract fields: protocol lane, hypothesis, success signal, failure signal, training budget/seed policy, protocol delta, and H01/H02 acceptance plan. |
| `0_trials/module2_formal_gate_contract_intake/formal_gate_contract_intake.json:202-233` | Contract output must live under `.pipeline/contracts/module2-*.md`; draft cannot authorize training; invalid shortcuts include local PPO output and paper tables before H02 acceptance. |
| `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json:5-19` | Failed warm-start formal result: decision `fail`, 64 episodes, 34 terminal-RS successes, success rate 0.53125, threshold 0.8, collision rate 0.34375, truncation rate 0.125, model hash recorded. |
| `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json:7-24` | Failed formal audit command and result: formal decision `fail`, required threshold 0.8, train/eval preset `f03`, warm-start status `applied_obstacle_summary_bc`. |
| `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json:10-24` | Failed run used obstacle-summary BC warm-start, `f03`, seed `20260704`, 100000 PPO timesteps, 1 env, 128 steps, batch 64. |
| `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest_formal_v2.json:68-87` | Formal-v2 BC corpus: 83809 rows, 1032 source rows, Complex/Extreme split, oracle-A/B counts, SHA-256 recorded. |
| `2_experiment/forest_n3p/datasets/module2_rl_rs_bc/manifest_formal_v2.json:127-174` | Formal-v2 collision audit has zero current/next/any collision rows, while v1 is invalidated and not paper-final. |
| `2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/README.md:35-85` | Obstacle-summary BC checkpoint SHA-256 and closed-loop evidence; it is the current practical warm-start candidate but not sufficient without PPO improvement. |
| `2_experiment/forest_n3p/scripts/train_rl_rs_ppo.py:78-89` and `:96-134` | Existing PPO train entry records the contract path and exposes seed, device, curriculum, total timesteps, PPO hyperparameters, observation config, env config, and BC checkpoint path. |
| `2_experiment/forest_n3p/scripts/train_rl_rs_ppo.py:217-265` | Existing warm-start loader validates obstacle-summary BC checkpoint fields and records checkpoint SHA-256. |
| `2_experiment/forest_n3p/scripts/eval_rl_rs_gate3.py:61-84` and `:145-188` | Gate3 evaluator accepts `--contract-path` and writes it into the summary and config. |
| `2_experiment/forest_n3p/scripts/run_rl_rs_gate3_trial.py:52-97`, `:120-205`, and `:246-310` | Gate3 trial runner accepts `--contract-path`, passes it into train/eval, and writes it into complete or incomplete trial manifests. |
| `2_experiment/forest_n3p/scripts/audit_rl_rs_gate3_trial.py:39-54` and `:177-201` | Gate3 audit accepts `--contract-path` and blocks non-default v2 audits when the trial/train/eval contract fields do not match. |
| `2_experiment/forest_n3p/scripts/preflight_rl_rs_gate3_formal_trial.py:34-73`, `:106-143`, and `:227-285` | Gate3 preflight packetizes contract path plus stronger PPO budget/stabilization parameters into the future runner command. |
| `2_experiment/forest_n3p/tests/test_preflight_rl_rs_gate3_formal_trial.py:84-145` | Targeted preflight test proves the v2 draft contract path and stronger PPO parameters propagate while draft status still blocks execution. |
| `0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.md:17-25` | Current remote resource evidence names `gpu3070ti-relay`, RTX 3070 Ti Laptop GPU, matching oracle parquet and BC checkpoint hashes; this evidence is readiness only, not training authorization. |

## 1. Protocol Lane

Selected lane: `stronger_obstacle_summary_warm_start`.

This lane keeps the compact obstacle-summary policy family and the module2
PPO-vs-RS replacement boundary. It does not switch to a patch-CNN policy, does
not introduce analytic fallback as hidden assistance, and does not stop/reframe
the module2 claim. The terminal RS check remains the Gate3 target: the learned
middle rollout must enter a terminal pose where RS can connect.

Rejected lanes for this immediate next attempt:

- `full_patch_cnn_policy`: rejected for now because it changes the observation
  tensor and architecture, which would require a different fairness argument
  and new H01/H02 schema fields before it can support the same replacement
  claim.
- `hybrid_ppo_analytic_fallback`: rejected for now because it changes the claim
  from direct PPO replacement of the analytic expansion slot to PPO-assisted
  hybrid control; that may be useful later, but it is a different contract.
- `stop_or_reframe_module2_claim`: rejected for now because Dr Sun selected a
  new success-attempt lane rather than closing the module2 replacement attempt
  as negative evidence only.

## 2. Hypothesis

Falsifiable hypothesis:

Keeping the obstacle-summary policy family but strengthening the formal
warm-start protocol and PPO stabilization can raise Gate3 terminal-RS success
from the failed 0.53125 run to at least 0.8 on the same `f03` formal Gate3
evaluation, without using local training output, failed PPO checkpoints, hidden
analytic fallback, or post-hoc threshold changes.

Mechanism being tested:

The formal-v2 obstacle-summary BC checkpoint gives PPO a collision-audited
steering prior, but the previous 100000-timestep, 1-env, entropy-free PPO run
was not strong enough. This contract tests whether a fresh PPO run from the same
audited BC source, with locked stronger budget/stabilization and strict
provenance, can improve terminal-RS connectability while preserving the
meaning of module2 as an RL-RS operator.

This hypothesis is not a claim of success. The old failed run remains negative
formal evidence.

## 3. Success Signal

The next attempt is successful only if all conditions below hold.

1. A new attempt directory is used:
   `0_trials/module2_gate3_formal/gate3_stronger_obstacle_summary_warm_start_v2_seed<seed>/`.
2. Training is remote-only on the approved 3070 Ti route after this contract is
   promoted and after source freshness / remote preflight are regenerated.
3. `train/final_model.zip` exists under the new attempt directory and its
   SHA-256 is recorded in `train/training_manifest.json`, `eval/gate3_summary.json`,
   and the pulled-back hash record.
4. `train/summary.json` reports `status=complete`, `smoke=false`,
   `warm_start_status=applied_obstacle_summary_bc`, `curriculum_preset=f03`,
   the approved v2 contract path, the remote host, the seed, the source head,
   and the full PPO hyperparameter block.
5. `eval/gate3_summary.json` reports at least 64 evaluation episodes,
   `success_threshold=0.8`, and `terminal_rs_success_rate >= 0.8`.
6. `gate3_formal_audit.json` reports `formal_decision=pass` and is tied to this
   v2 contract path, the evaluated checkpoint hash, and the same new attempt
   directory.
7. `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json` reports
   `formal_output_accepted=true` and `paper_result_input_allowed=true` for rows
   that explicitly name the PPO result and checkpoint hash.

## 4. Failure Signal

Failure is not defined only as the negation of success. Any of the following is
an independent failure signal.

1. Gate3 threshold failure: formal evaluation has at least 64 episodes but
   `terminal_rs_success_rate < 0.8`.
2. Unsafe-rollout failure: collision rate is at least 0.30 or truncation rate is
   at least 0.20 on the formal 64-episode Gate3 evaluation.
3. Provenance failure: `source_head` is `unknown`, the evaluated checkpoint hash
   is missing or inconsistent, the attempt directory is reused from the failed
   warm-start run, or the audit points to the old v1 contract path.
4. Protocol failure: training uses a local output, smoke run, hidden analytic
   fallback, patch-CNN architecture, unapproved reward/curriculum change, or any
   budget/seed change not present in the approved/frozen contract.
5. H02 failure: Gate3 passes but H02 remains blocked by missing PPO rows,
   missing checkpoint hash, scale/schema mismatch, or `formal_output_accepted`
   is not `true`.

If the attempt fails, the failed checkpoint and artifacts may be archived as
negative evidence only. They cannot be reused as a success attempt substitute.

## 5. Protocol Delta From Failed Run

Locked deltas relative to the failed `gate3_obstacle_summary_warm_approved_v1`
run:

| Item | Failed run | v2 draft requirement |
|---|---|---|
| Attempt directory | `gate3_obstacle_summary_warm_approved_v1` | Fresh `gate3_stronger_obstacle_summary_warm_start_v2_seed<seed>` directory. |
| PPO checkpoint reuse | Failed `final_model.zip` exists and failed at 0.53125 | Do not reuse failed PPO checkpoint. Start from approved obstacle-summary BC checkpoint only. |
| Warm-start source | `module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt` | Same BC checkpoint is allowed only after SHA-256 and formal-v2 manifest checks pass; it remains initialization, not success evidence. |
| PPO budget | 100000 timesteps, 1 env | Draft stronger budget: 500000 timesteps, 4 envs, 256 rollout steps, batch 256, 8 epochs, checkpoint every 25000 environment steps. |
| PPO stabilization | learning rate 0.0003, entropy coefficient 0.0 | Draft stabilization: learning rate 0.0001, entropy coefficient 0.01, clip range 0.2, GAE lambda 0.95, gamma 0.99, max grad norm 0.5. |
| Curriculum | train/eval `f03` | Train/eval remain `f03` to preserve Gate3 comparability. No post-hoc easier curriculum may be substituted. |
| Observation and architecture | obstacle-summary extractor, 128/128/64 MLP | Preserve obstacle-summary extractor and 128/128/64 actor/value MLP. Patch-CNN requires a separate contract. |
| Reward formula | Current `RewardConfig` defaults and enabled reward terms | No reward formula change is authorized by this draft. If reward weights are changed, create a revised contract before training. |
| Contract path propagation | Earlier gate code was v1-path oriented | Current train/eval/trial/preflight/audit code accepts `--contract-path`; after approval, source-fresh and remote packet artifacts must be regenerated with this v2 path. |
| Provenance | failed run source head was `unknown` in formal artifacts | v2 requires non-unknown source head, committed source, remote host, command, seed, source hashes, and checkpoint hashes. |

These draft hyperparameters are not approved training parameters until Dr Sun
promotes this contract. They are written now to prevent after-result budget
extension or seed cherry-picking.

## 6. Training Budget And Seed Policy

Remote resource:

- Candidate remote route: `gpu3070ti-relay`.
- The alias must be revalidated after contract approval and before any preflight.
- If Dr Sun intends a different alias such as `gpu3070ti-reply`, this draft must
  be corrected before approval.
- Local PPO training is not valid evidence under this contract.

Primary seed policy:

- Primary formal seed: `20260706`.
- Training seed and heldout/evaluation seed must be recorded separately if they
  differ. If they are the same, the manifest must state that explicitly.
- The seed cannot be changed after seeing training or evaluation output.
- A failed primary seed cannot be retried under a new seed without a new or
  revised contract.

Draft PPO command block to be packetized after approval:

```bash
PYTHONPATH=2_experiment .venv/bin/python -m forest_n3p.scripts.run_rl_rs_gate3_trial \
  --output-dir 0_trials/module2_gate3_formal/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706 \
  --contract-path .pipeline/contracts/module2-stronger_obstacle_summary_warm_start-v2.md \
  --seed 20260706 \
  --device cuda \
  --train-curriculum-preset f03 \
  --eval-curriculum-preset f03 \
  --oracle-path 0_trials/module2_oracle_shape/oracle_connector_results.parquet \
  --heldout-seed 20260706 \
  --train-total-timesteps 500000 \
  --train-n-envs 4 \
  --train-n-steps 256 \
  --train-batch-size 256 \
  --train-n-epochs 8 \
  --train-learning-rate 0.0001 \
  --train-gamma 0.99 \
  --train-gae-lambda 0.95 \
  --train-clip-range 0.2 \
  --train-ent-coef 0.01 \
  --train-vf-coef 0.5 \
  --train-max-grad-norm 0.5 \
  --train-policy-net-arch 128,128,64 \
  --train-value-net-arch 128,128,64 \
  --train-checkpoint-freq 25000 \
  --eval-episodes 64 \
  --eval-min-episodes 64 \
  --eval-success-threshold 0.8 \
  --obs-patch-size-m 6.4 \
  --obs-patch-cells 64 \
  --max-steps 32 \
  --allow-duplicate-openmp \
  --bc-checkpoint 2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt
```

Before this command can be run, the approved/frozen contract must be consumed by
fresh source-freshness, remote packet, remote preflight, and downstream gate
artifacts. The current preflight path can packetize these parameters, but this
draft status still blocks execution.

## 7. Evaluation And Acceptance Plan

Expected fresh artifacts for the next success attempt:

| Category | Artifact | Required path or predicate |
|---|---|---|
| contract | new/revised Research Contract | This file, after explicit Dr Sun promotion to `approved` or `frozen`. |
| training | PPO checkpoint bundle | `0_trials/module2_gate3_formal/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706/train/final_model.zip` plus checkpoint cadence files. |
| training | train summary | `train/summary.json` with complete config, remote host, source head, seed, warm-start status, and no smoke flag. |
| training | training manifest | `train/training_manifest.json` with source hashes, command, checkpoint hashes, BC checkpoint hash, and v2 contract path. |
| evaluation | Gate3 episode CSV | `eval/gate3_eval_episodes.csv`, at least 64 rows. |
| evaluation | Gate3 summary | `eval/gate3_summary.json`, threshold 0.8, terminal-RS success/collision/truncation/timing/model hash fields. |
| acceptance | trial manifest | `gate3_trial_manifest.json`, complete pointers to train/eval/audit artifacts and v2 contract path. |
| acceptance | formal audit | `gate3_formal_audit.json`, `formal_decision=pass`, `required_success_threshold=0.8`, v2 contract path. |
| acceptance | pulled-back hash record | `train/final_model.zip.sha256` or equivalent JSON tied to the evaluated model hash. |
| formal acceptance | H02 formal output acceptance | `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`, `formal_output_accepted=true`, `paper_result_input_allowed=true`. |

Invalid substitutes:

- the failed `gate3_obstacle_summary_warm_approved_v1` PPO checkpoint;
- any local PPO training output;
- H02 smoke rows without formal PPO rows;
- a paper table, appendix paragraph, or prose explanation;
- a Gate3 audit tied to the old v1 contract path;
- a checkpoint without a source-bound SHA-256 record.

## 8. Paper Claim Boundary

No result claim is allowed from this draft.

If this contract is later approved/frozen and the next attempt passes, the
claim boundary is still narrow:

- Allowed after H02 acceptance: "under the approved v2 protocol, the
  obstacle-summary warm-start PPO operator passed Gate3 terminal-RS
  connectability on the recorded formal evaluation."
- Not allowed without additional evidence: "PPO fully replaces RS in all Hybrid
  A* planning contexts", "module2 is complete", "patch-CNN is unnecessary", or
  "hybrid fallback is equivalent to direct PPO replacement."
- Any table or manuscript result text must consume H02 accepted rows and the
  evaluated checkpoint hash. This contract draft itself cannot be cited as a
  result source.

## 9. Promotion Checklist

Before Dr Sun can promote this draft:

- confirm whether the remote alias is `gpu3070ti-relay` or `gpu3070ti-reply`;
- approve or edit the 500000-step / 4-env / seed `20260706` budget;
- decide whether the unsafe-rollout failure thresholds
  (`collision_rate >= 0.30`, `truncation_rate >= 0.20`) should remain;
- re-run the targeted preflight/audit contract-path tests after any contract
  status promotion and verify generated packet commands still carry this v2
  contract path and stronger PPO parameters;
- regenerate source freshness, remote execution packet, remote preflight, and
  downstream gate artifacts after the approved/frozen contract commit.

Until these items are closed, this file remains a draft and blocks training.
