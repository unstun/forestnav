# Module2 Gate3 Formal v3 Summary

Verdict: FAIL.

Gate seed 20260706 completed 256 eval episodes with verified provenance, but terminal-RS success_rate was 0.6836, below the pre-registered 0.80 threshold. Collision and truncation rates passed their thresholds. Robustness seeds are reported only as supplementary evidence and do not enter the gate verdict.

A pass certifies formal training convergence (Gate #3) only. It is NOT an RS-replacement performance claim; H01/H02 planner-integration experiments are still required and are not authorized by this contract.

## Gate Criteria

| Criterion | Required | Gate seed 20260706 | Result |
|---|---:|---:|---|
| Episodes | == 256 | 256 | PASS |
| Terminal-RS success rate | >= 0.8000 | 0.6836 | FAIL |
| Collision rate | < 0.3000 | 0.2695 | PASS |
| Truncation rate | < 0.2000 | 0.0469 | PASS |
| Provenance verified | true | true | PASS |

## Per-Seed Results

| Seed | Role | Episodes | Success | Wilson 95% CI | Collision | Truncation | Mean nn_forward_time_s | Verdict |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 20260706 | gate | 256 | 0.6836 (175/256) | [0.6243, 0.7375] | 0.2695 (69/256) | 0.0469 (12/256) | 0.005320 | FAIL |
| 20260708 | robustness only, not gate evidence | 256 | 0.6641 (170/256) | [0.6042, 0.7191] | 0.2656 (68/256) | 0.0703 (18/256) | 0.005628 | ROBUSTNESS_ONLY |
| 20260709 | robustness only, not gate evidence | 256 | 0.7109 (182/256) | [0.6526, 0.7630] | 0.2461 (63/256) | 0.0430 (11/256) | 0.005465 | ROBUSTNESS_ONLY |

## Stage Breakdown

| Seed | Role | Curriculum stage | Episodes | Success | Collision | Truncation | Mean nn_forward_time_s |
|---:|---|---|---:|---:|---:|---:|---:|
| 20260706 | gate | heldout_procedural | 48 | 0.5000 (24/48) | 0.3958 (19/48) | 0.1042 (5/48) | 0.008469 |
| 20260706 | gate | obstacle_bypass | 56 | 0.5179 (29/56) | 0.4821 (27/56) | 0.0000 (0/56) | 0.000935 |
| 20260706 | gate | open_connector | 49 | 1.0000 (49/49) | 0.0000 (0/49) | 0.0000 (0/49) | 0.000631 |
| 20260706 | gate | rs_failure_node | 103 | 0.7087 (73/103) | 0.2233 (23/103) | 0.0680 (7/103) | 0.008468 |
| 20260708 | robustness only | heldout_procedural | 49 | 0.4286 (21/49) | 0.3878 (19/49) | 0.1837 (9/49) | 0.010074 |
| 20260708 | robustness only | obstacle_bypass | 56 | 0.5179 (29/56) | 0.4821 (27/56) | 0.0000 (0/56) | 0.000939 |
| 20260708 | robustness only | open_connector | 48 | 1.0000 (48/48) | 0.0000 (0/48) | 0.0000 (0/48) | 0.003322 |
| 20260708 | robustness only | rs_failure_node | 103 | 0.6990 (72/103) | 0.2136 (22/103) | 0.0874 (9/103) | 0.007138 |
| 20260709 | robustness only | heldout_procedural | 49 | 0.7551 (37/49) | 0.2245 (11/49) | 0.0204 (1/49) | 0.010372 |
| 20260709 | robustness only | obstacle_bypass | 56 | 0.5179 (29/56) | 0.4821 (27/56) | 0.0000 (0/56) | 0.000970 |
| 20260709 | robustness only | open_connector | 47 | 1.0000 (47/47) | 0.0000 (0/47) | 0.0000 (0/47) | 0.000636 |
| 20260709 | robustness only | rs_failure_node | 104 | 0.6635 (69/104) | 0.2404 (25/104) | 0.0962 (10/104) | 0.007756 |

## Provenance

- Contract: `.pipeline/contracts/module2-rl-rs-gate3-formal-v3.md` (`status: approved_by_dr_sun`).
- Formal run source_head: `b4b7360634efa82dcf68f3769563e69a01092746`.
- `FORESTNAV_SOURCE_HEAD` was unset in all three manifests.
- Remote git verification in each manifest reports the same source head and a clean worktree before artifact manifest generation.
- No BC checkpoint or warm-start was used; `bc_checkpoint` is null in all manifests.
- The gate audit artifact exists for seed 20260706, but the current audit script reports `formal_decision: not_formal` because its allowed contract statuses are `approved`/`frozen` while this human-approved contract uses `approved_by_dr_sun`. The evaluator decision is still `fail` because success_rate < 0.80.

## Artifacts

- `seed20260706`: `eval/gate3_summary.json`, `eval/gate3_eval_episodes.csv`, `gate3_trial_manifest.json`, `checkpoint_sha256.csv`, train logs, and local/remote `train/final_model.zip` verified by SHA256 below.
- `seed20260708`: `eval/gate3_summary.json`, `eval/gate3_eval_episodes.csv`, `gate3_trial_manifest.json`, `checkpoint_sha256.csv`, train logs, and local/remote `train/final_model.zip` verified by SHA256 below.
- `seed20260709`: `eval/gate3_summary.json`, `eval/gate3_eval_episodes.csv`, `gate3_trial_manifest.json`, `checkpoint_sha256.csv`, train logs, and local/remote `train/final_model.zip` verified by SHA256 below.
- `seed20260706`: additionally includes `gate3_formal_audit.json` and audit stdout/stderr log.
- `pre_fix_crash_seed20260706`: archived crash evidence from the invalid heldout query failure before the sampler fix.
- The three `train/final_model.zip` binaries are synced locally and remain on `/home/ubuntu/ForestNav`; they are Git-ignored after repeated GitHub LFS/HTTPS upload failures. The committed manifests and summary record their exact SHA256 and size.

## Model SHA256

| Seed | final_model.zip SHA256 |
|---:|---|
| 20260706 | `406295b3034d5c6a5834d2f0080ecf47d2874a7a7ccda3edf9eb57af55089001` |
| 20260708 | `b910bee9c25c49716d0e3c9b3a843ae5ebfb04083b5369ad50927b246e90c839` |
| 20260709 | `ae97501bd75f4d832bd400c9a6b42e8f73b71ab6a955fa1cb956a155357fc1a2` |
