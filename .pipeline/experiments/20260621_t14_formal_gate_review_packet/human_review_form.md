# T14 Human Review Form

> Fill this file only after reading `review_packet.md`, `formal_gate_checklist.csv`, `decision_queue.csv`, and `.pipeline/experiments/20260621_t06_review_validation_analysis/analysis.md`.
> Do not set T06 reviewed:true until D-T14-09 resolves the density validation discrepancy.

| decision_id | decision | reviewer | date | notes |
|---|---|---|---|---|
| D-T14-09 | revise_to_validation_cutpoints | Dr Sun | 2026-06-23 | 先按放大验证切点推进整体框架：density Easy=d00-d01, Complex=d02-d04, Extreme=d05-d07；最终论文前仍可追加更大验证。 |
| D-T14-10 | approve | Dr Sun | 2026-06-23 | 接受 k=20 + commit_verified_rs_segments 作为当前 F-N3P(KNN) 主评测配置，先用于打通 T14/T15/T16 框架。 |
| D-T14-11 | formal_baseline | Dr Sun | 2026-06-23 | MD-DQN 暂按正式 baseline 纳入主评测表，但论文写作时需标注 checkpoint/adaptor 来源限制，避免过度声称复现。 |
| D-T14-12 | approve_after_rerun_passes | Dr Sun | 2026-06-23 | 允许按 validation_t06 重跑 formal T14；仅在 formal_acceptance=true 后勾选 T14。 |

Allowed values are listed in `decision_queue.csv`.
