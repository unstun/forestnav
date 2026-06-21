---
origin: ai+local
reviewed: false
created_at_utc: 2026-06-21T01:45:06.595401+00:00
updated_at_utc: 2026-06-21T03:30:00+00:00
task: T14
status: needs_human_review
---

# T14 Formal Gate Review Packet

## 直观结论

最新 k=20 collisionguard fullscale 已经把 T14 的核心数值门跑通：300 queries、1800 records、6 official methods、0 exceptions、0 collision violations，Complex/Extreme 两个目标桶均 pass。

但现在仍不能勾选 T14。原因已经从“只缺人工确认”升级为“先缺 T06 密度轴复核”：T06 放大验证显示密度轴 `bucket_separation_pass=false`，Extreme 下界从原 T06 的 `d03` 后移到 `d05`。因此，原 T06 cutpoint supplement 不能直接作为正式难度桶依据；runner 产物仍是 `formal_acceptance=false`，且 k=20/RS-verified segment 与 MD-DQN baseline 身份也还需要 Dr Sun 人工确认。

## Latest Candidate Evidence

- candidate run: `.pipeline/experiments/20260620_t14_candidate_6method_fullscale_rs_k20_collisionguard`
- source_head: `211e373e9be7f605a72ecbf5b0cae146d9cf06d4`
- execution_host: `ubuntu-OMEN-by-HP-Laptop-17-ck1xxx`
- status: `candidate_or_smoke`
- formal_acceptance: `False`
- record_count/query_count/method_count: 1800/300/6
- collision_violation_total: 0
- method_exception_total: 0
- preflight_warnings: `["T06 cutpoint supplement is not reviewed:true: .pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md"]`

## New T06 Validation Evidence

- validation run: `.pipeline/experiments/20260621_t06_review_validation_m6q10_d6q16`
- analysis: `.pipeline/experiments/20260621_t06_review_validation_analysis/analysis.md`
- total queries: 960
- density queries: 480
- distance queries: 480
- density validation status: `fail`
- distance validation status: `pass`
- density cutpoint change: original Extreme lower bound `d03`; validation Extreme lower bound `d05`
- direct implication: T14 formal rerun should stay on hold until Dr Sun either revises T06 cutpoints or explicitly accepts the original small-sample cutpoints despite the validation result.

## Contract Bucket Results

| bucket | status | median time reduction | success drop pp | median path inflation | checks |
|---|---|---:|---:|---:|---|
| Complex | pass | 0.919312 | -16.000 | 0.000000 | `{"median_time_reduction_ge_50pct": true, "success_drop_le_2pp": true, "median_path_inflation_le_5pct": true, "collision_violations_zero": true}` |
| Extreme | pass | 0.912134 | -15.000 | 0.001344 | `{"median_time_reduction_ge_50pct": true, "success_drop_le_2pp": true, "median_path_inflation_le_5pct": true, "collision_violations_zero": true}` |

## Blocking Gates

| gate | current status | blocking? | action |
|---|---|---|---|
| G02 T06 cutpoint supplement reviewed | fail | yes | Dr Sun review T06 supplement together with the later validation evidence; only after resolving D-T14-09 should reviewed:true be set. |
| G02b T06 validation consistency | fail | yes | Dr Sun decide whether to revise density buckets to validation cutpoints, run another validation, or explicitly retain the original T06 split with written justification. |
| G02c Density profile mode aligned | fail | yes | If D-T14-09 keeps original cutpoints, rerun with `DENSITY_PROFILE_BUCKETS=original_t06`; if D-T14-09 revises to validation cutpoints, rerun with `DENSITY_PROFILE_BUCKETS=validation_t06`. |
| G08 F-N3P implementation variant accepted | needs_human_review | yes | Dr Sun decide whether this is the formal F-N3P(KNN) config or only a candidate variant. |
| G09 MD-DQN baseline interpretation accepted | needs_human_review | yes | Dr Sun decide formal baseline vs adapter smoke/history-only baseline. |
| G10 Programmatic formal verdict | fail | yes | After G02/G02b/G02c/G08/G09 human decisions, rerun formal command without unreviewed override to produce formal_acceptance=true. |

## Dr Sun Decisions Needed

| decision_id | question | allowed values | evidence |
|---|---|---|---|
| D-T14-09 | 是否确认 T06 难度轴补充 reviewed:true，可作为 T14 正式难度桶依据？ | `approve_original_with_justification|revise_to_validation_cutpoints|run_more_validation|reject` | `.pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md; .pipeline/experiments/20260620_t06_difficulty_calibration/report.md; .pipeline/experiments/20260621_t06_review_validation_analysis/analysis.md` |
| D-T14-10 | 是否接受 k=20 + commit_verified_rs_segments 作为正式 F-N3P(KNN) 主评测配置？ | `approve|revise_required|reject` | `.pipeline/experiments/20260620_t14_knn_k_sweep_analysis/analysis.md; .pipeline/experiments/20260620_t14_k20_collisionguard_analysis/analysis.md` |
| D-T14-11 | MD-DQN historical checkpoint 是否作为正式 baseline，还是只能标为 historical adapter smoke？ | `formal_baseline|history_only_smoke|revise_required` | `.pipeline/experiments/20260620_t14_candidate_6method_fullscale_rs_k20_collisionguard/summary_by_method_bucket.csv` |
| D-T14-12 | 在 D-T14-09/10/11 通过后，是否允许 rerun formal T14 并在 formal_acceptance=true 后勾选 T14？ | `approve_after_rerun_passes|hold` | `.pipeline/experiments/20260620_t14_candidate_6method_fullscale_rs_k20_collisionguard/verdict.json` |

## Relation To Earlier T14 Review Queues

The earlier review packets remain useful history, but their numerical status was superseded by the k=20 collisionguard run. Use the mapping below when reviewing old D-T14 IDs.

| earlier decision | old meaning | current replacement | current status |
|---|---|---|---|
| D-T14-01 / D-T14-07 | T06 cutpoint supplement acceptance | D-T14-09 | still blocking; reviewed:false |
| D-T14-02 / D-T14-08 | MD-DQN baseline status | D-T14-11 | still needs human interpretation |
| D-T14-03 / D-T14-06 | old candidate failed Contract time gate | superseded by k20 collisionguard evidence | no longer the numerical blocker |
| D-T14-04 | T14 completion gate | D-T14-12 | still blocked until formal rerun passes |
| D-T14-05 | commit_verified_rs_segments as formal F-N3P | D-T14-10 | still needs human acceptance |

## After Human Approval

If D-T14-09/10/11 are approved, run the command in `post_review_formal_rerun_command.sh` on `gpu3070ti-relay` after resolving the T06 validation discrepancy, setting T06 `reviewed:true`, setting `DENSITY_PROFILE_BUCKETS` according to D-T14-09, and setting `SOURCE_HEAD` to the post-review source commit. The expected success condition is a new `verdict.json` with `status=formal_pass` and `formal_acceptance=true`.

The script first runs `python -m forest_n3p.scripts.run_main_evaluation --preflight-only` with the same formal configuration and writes `${LOG}.preflight.json`. If preflight fails, the long evaluation is not started.

Example:

```bash
SOURCE_HEAD=<post-review-commit> DENSITY_PROFILE_BUCKETS=validation_t06 \
  bash .pipeline/experiments/20260621_t14_formal_gate_review_packet/post_review_formal_rerun_command.sh
```

D-T14-09 to command mapping:

- `approve_original_with_justification` -> `DENSITY_PROFILE_BUCKETS=original_t06`
- `revise_to_validation_cutpoints` -> `DENSITY_PROFILE_BUCKETS=validation_t06`
- `run_more_validation` or `reject` -> do not run formal T14.

Only after that formal rerun passes should `.pipeline/mainline.md` T14 be changed from `[ ]` to `[x]` and a T14 completion record be appended.

## Files

- `.pipeline/experiments/20260621_t14_formal_gate_review_packet/formal_gate_checklist.csv`
- `.pipeline/experiments/20260621_t14_formal_gate_review_packet/decision_queue.csv`
- `.pipeline/experiments/20260621_t14_formal_gate_review_packet/legacy_decision_map.csv`
- `.pipeline/experiments/20260621_t14_formal_gate_review_packet/human_review_form.md`
- `.pipeline/experiments/20260621_t14_formal_gate_review_packet/post_review_formal_rerun_command.sh`
- `.pipeline/experiments/20260621_t14_formal_gate_review_packet/evidence_manifest.json`

## Boundary

This packet is an audit and review handoff, not a completion record. It does not modify `.pipeline/mainline.md` and does not assert T14 complete.
