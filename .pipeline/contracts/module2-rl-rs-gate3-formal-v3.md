---
topic: module2-rl-rs-gate3-formal-v3
status: approved_by_dr_sun
version: v3-formal
approved_by: Dr Sun
approved_date: 2026-07-06
origin: human-approved-goal
reviewed: false
basis: encoder pilot R3 (52/64 = 0.8125, only variant >= 0.80; pilot contract module2-encoder-pilot-v3)
training_allowed: true
remote_training_allowed_now: true
local_training_allowed_now: false
formal_claim_allowed_now: gate3_only_after_pass
paper_result_material_allowed_now: false
---

# Research Contract: Module2 Gate3 Formal v3 (frozen R3 config)

Hypothesis: the R3 pilot configuration (patch-CNN extractor, no warm-start,
sparse default reward, 500k timesteps) formally reaches terminal-RS success
>= 0.80 on the f03 curriculum under a pre-locked seed and a 256-episode
deterministic evaluation.

Success signal: seed-20260706 eval with episodes==256 achieves
terminal_rs_success_rate >= 0.80 with collision_rate < 0.30 and
truncation_rate < 0.20, with verified provenance (remote git HEAD equals the
pinned local commit; FORESTNAV_SOURCE_HEAD unset).

Failure signals (each independent): success_rate < 0.80; collision_rate
>= 0.30; truncation_rate >= 0.20; any provenance failure; any deviation from
the frozen config. A failure is a formal negative result. Retrying the same
config under a different seed requires a new contract.

Seed policy: gate seed 20260706, locked before any formal output exists.
Supplementary robustness seeds 20260708/20260709 are reported but never enter
the gate verdict.

Scope: a pass certifies formal training convergence (Gate #3 of the module2
program) and unlocks drafting the H01/H02 planner-integration formal protocol
using the passing checkpoint. It does not authorize any RS-replacement
performance claim or paper results material.

## Progress
(appended one line per completed D-item)
