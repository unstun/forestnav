---
topic: module2-encoder-pilot
status: approved_by_dr_sun
version: v3-pilot
approved_by: Dr Sun
approved_date: 2026-07-06
origin: human-approved-goal
reviewed: false
training_allowed: true
remote_training_allowed_now: true
local_training_allowed_now: false
formal_claim_allowed_now: false
paper_result_material_allowed_now: false
---

# Research Contract: Module2 Encoder Pilot V3

This contract authorizes only the module2 encoder pilot described below. The
pilot results are not formal results, do not unlock paper claims, and do not
authorize drafting or approving a later formal v3 contract.

## R1-R6 Matrix And Common Protocol

Common: total_timesteps=500000 (or 300000 after a D6 downgrade), n_envs=8,
n_steps=256, batch_size=256, n_epochs=10, gamma=0.98, gae_lambda=0.95,
clip_range=0.2, ent_coef=0.01, max_grad_norm=0.5, lr-schedule=linear,
train+eval curriculum=f03, seed=20260707 (the formal seed 20260706 must NEVER
be used), checkpoint_freq=50000, eval = eval_rl_rs_gate3.py, 64 deterministic
episodes.
Dense reward = distance_progress_scale=0.2, clearance_scale=0.1,
step_penalty=-0.01; all terminal/collision terms stay at defaults.
R1: summary extractor + BC warm-start (obstacle_summary_formal_v2) + value-pretrain 50k + sparse reward + lr 1e-4
R2: same as R1 but dense reward
R3: patch_cnn extractor + no warm-start + sparse reward + lr 3e-4
R4: same as R3 but dense reward
R5: transformer extractor + no warm-start + dense reward + lr 3e-4
R6 (optional): transformer + sparse reward + lr 3e-4

## Seed Policy

Pilot seed: `20260707`.

Formal seed: `20260706`. The formal seed must never be used by this pilot.

The pilot seed is fixed before seeing pilot results. Changing it after any
training or evaluation output exists is prohibited.

## Pre-Registered Decision Rule

- Any run >= 0.80 -> freeze that config into a v3 contract; formal attempt with
  seed 20260706, fresh directory, full provenance.
- Best run in [0.65, 0.80) and clearly above R1 -> one refinement round on the
  winning branch only (reward magnitudes / budget to 1M / warm-start for patch
  encoders), pre-registered before running.
- All runs < 0.65 -> stop-and-reframe discussion (hybrid-fallback lane C or
  negative-result framing); do not keep grinding blind.
- Pilot numbers are never paper results; they select the formal protocol only.

## Authorized Outputs

Only these output classes are authorized:

- Code and tests needed for the pilot.
- Training and evaluation artifacts for R1-R6 and local micro-smokes.
- This contract file, including this progress section.
- `0_trials/module2_encoder_pilot/pilot_summary.md` and `.csv`.

## Progress

- 2026-07-06 D1 complete: committed existing remote-workdir fix and test as `93df7eea`; targeted test `PYTHONPATH=2_experiment KMP_DUPLICATE_LIB_OK=TRUE pytest 2_experiment/forest_n3p/tests/test_module2_v2_remote_execution_packet.py -q` passed with `3 passed in 0.33s`; working tree was clean afterward.
- 2026-07-06 D2 complete: created this approved pilot contract with the R1-R6 matrix, common protocol, seed policy, and pre-registered decision rule.
- 2026-07-06 D3 complete: wired `train_rl_rs_ppo.py --reward-config` through curriculum/env RewardConfig injection, recorded effective reward parameters in training manifests, added dense reward config and pytest coverage; `PYTHONPATH=2_experiment KMP_DUPLICATE_LIB_OK=TRUE pytest 2_experiment/forest_n3p/tests/test_train_rl_rs_ppo.py -q` passed with `11 passed in 3.11s`; full suite `PYTHONPATH=2_experiment KMP_DUPLICATE_LIB_OK=TRUE pytest 2_experiment/forest_n3p/tests -q` passed with `508 passed, 2 xfailed in 68.70s`.
- 2026-07-06 D4 complete: implemented `RlRsPatchTransformerExtractor`, connected `train_rl_rs_ppo.py --features-extractor transformer`, and added pytest coverage for forward shape, tiny 5x5 patch interpolation, BC-checkpoint exclusivity, and parameter count <2M; `PYTHONPATH=2_experiment KMP_DUPLICATE_LIB_OK=TRUE pytest 2_experiment/forest_n3p/tests/test_train_rl_rs_ppo.py -q` passed with `15 passed, 3 warnings in 2.02s`; full suite `PYTHONPATH=2_experiment KMP_DUPLICATE_LIB_OK=TRUE pytest 2_experiment/forest_n3p/tests -q` passed with `512 passed, 2 xfailed, 3 warnings in 62.37s`.
