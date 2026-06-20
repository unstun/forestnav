---
origin: ai+local
reviewed: false
date: 2026-06-20
task: T14
status: pending_human_review
---

# T14 人工审阅包：主评测候选结果与决策门

## 一句话结论

T14 的工程运行链路已经跑到 6-method、300 queries、5 seeds、0 collision、0 exception。
但按当前证据，T14 不能勾完成，也不能写成正结果：T06 切点未人工确认，MD-DQN
checkpoint 是否正式可用未确认，而且 F-N3P 没有达到预注册的时间缩减成功判据。

## 审阅入口

| 材料 | 作用 |
|---|---|
| `.pipeline/contracts/v9-forest-n3p.md` | 父 Contract，定义成功/失败判据 |
| `.pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md` | T06 难度切点草案，当前 `reviewed:false` |
| `.pipeline/experiments/20260620_t14_candidate_6method_fullscale_md_dqn/analysis.md` | 当前最完整 6-method candidate 结果 |
| `.pipeline/experiments/20260620_t14_candidate_6method_fullscale_md_dqn/verdict.json` | 机器可读判定结果 |
| `.pipeline/experiments/20260620_t14_human_review_packet/decision_queue.csv` | Dr Sun 可填写的人工决策队列 |

## 当前完成度审计

| T14 要求 | 当前证据 | 状态 |
|---|---|---|
| F-N3P(KNN) | 6-method candidate 包含 `f_n3p_knn` | satisfied for candidate |
| 原版 HA* | 6-method candidate 包含 `vanilla_ha` | satisfied for candidate |
| N3P 式 K=1 | 6-method candidate 包含 `n3p_k1` | satisfied for candidate |
| Voronoi waypoint | 6-method candidate 包含 `voronoi_waypoint` | satisfied for candidate |
| 瓶颈 waypoint | 6-method candidate 包含 `bottleneck_waypoint` | satisfied for candidate |
| MD-DQN | 6-method candidate 包含 `md_dqn`，但 checkpoint 未确认正式性 | candidate only |
| 每桶 >=100 查询 | Easy/Complex/Extreme 各 100 | satisfied |
| >=5 随机种子 | seed_count=5 | satisfied |
| 碰撞违例全为 0 | `collision_violation_total=0` | satisfied |
| 数据完整无缺失 | record_count=1800, method_count=6, exception=0 | satisfied |
| T06 难度切点正式可用 | supplement 是 `reviewed:false` | not satisfied |
| 预注册成功判据 | Complex/Extreme 中位时间缩减为负 | failed in candidate |

## 6-method candidate 关键数字

| 项 | 数值 |
|---|---:|
| record_count | 1800 |
| query_count | 300 |
| method_count | 6 |
| seed_count | 5 |
| collision_violation_total | 0 |
| method_exception_total | 0 |
| formal_acceptance | false |

| bucket | Contract status | median_time_reduction | success_drop_pp | median_path_inflation_ratio |
|---|---|---:|---:|---:|
| Complex | fail | -0.2993 | -12.0 | 0.0000 |
| Extreme | fail | -0.2621 | -8.0 | 0.0005 |

解释：

- `success_drop_pp` 为负表示 F-N3P 成功率高于 vanilla HA*，这是好信号。
- 但 `median_time_reduction` 为负表示 F-N3P 中位规划时间比 vanilla HA* 更慢。
- 当前 Contract 要求时间缩减 `>=50%`，所以候选结果失败。

## MD-DQN 边界

本轮 MD-DQN 使用：

- source_dir: `/home/ubuntu/DQN10/2_experiment`
- checkpoint: `/home/ubuntu/DQN10/2_experiment/ugv_dqn/outputs/2026-05-12_train_load_external_demo_smoke/models/realmap_a/mlp-dqn.pt`
- algo: `mlp-dqn`

结果：

| bucket | success_rate | feasible_rate | median_time_s |
|---|---:|---:|---:|
| Easy | 0.00 | 0.00 | 0.1727 |
| Complex | 0.02 | 0.02 | 0.1712 |
| Extreme | 0.01 | 0.01 | 0.1701 |

MD-DQN 300 条记录中只有 3 条成功，297 条为 `md_dqn_not_reached`。这说明 adapter
可运行，但旧 checkpoint 对 v9 ForestNav 分布基本不可用。是否仍把它作为“历史 RL
基线”写入论文，需要 Dr Sun 明确确认。

## 可以说

- T14 runner 已经能跑全 6 方法候选评测。
- 当前 6-method candidate 数据完整：300 queries、5 seeds、1800 records、0 exception、0 collision。
- F-N3P 在 Complex/Extreme 的候选成功率高于 vanilla HA*，路径膨胀满足当前阈值。
- 当前候选中，F-N3P 未达到预注册的时间缩减成功判据。
- 旧 MD-DQN checkpoint 在 v9 ForestNav query distribution 上成功率极低。

## 不能说

- 不能说 T14 已完成。
- 不能说 T14 formal_acceptance 通过。
- 不能把 `reviewed:false` 的 T06 supplement 当论文 claim 依据。
- 不能把旧 MD-DQN checkpoint 描述为“公平训练的正式 RL baseline”，除非 Dr Sun 明确接受它的历史基线定位。
- 不能在当前 Contract 不变时把 T14 写成正结果。

## 需要 Dr Sun 决策

| ID | 决策 | 选项 | 影响 |
|---|---|---|---|
| D-T14-01 | T06 cutpoint supplement 是否确认 | accept / revise / reject | accept 后才允许正式使用当前 Easy/Complex/Extreme 切点 |
| D-T14-02 | 旧 `mlp-dqn.pt` 是否作为 MD-DQN baseline | accept_as_historical_baseline / reject_and_retrain / drop_or_redefine | 决定 MD-DQN 能否进入正式 T14 |
| D-T14-03 | 当前 Contract 判定失败后下一步 | write_negative_result / redesign_method / create_contract_v2 | 决定是否进入 T15/T16 或回到方法设计 |

## 推荐的最小下一步

先不要勾 T14，也不要进入 T15。建议 Dr Sun 先填 `decision_queue.csv`：

1. 若 T06 不确认，则 T14 只能继续保持 candidate。
2. 若 MD-DQN 不接受为历史 baseline，需要补训练或重新定义 baseline。
3. 若 Contract 不改，当前 T14 应记录为 candidate fail，并转入失败分析或方法重设计。

## 证据锚点

| Claim | Evidence |
|---|---|
| 父 Contract 要求 Complex/Extreme 时间缩减 >=50%、SR 下降 <=2pp、路径膨胀 <=5% | `.pipeline/contracts/v9-forest-n3p.md:14-20` |
| 父 Contract 一旦 approved 禁止直接修改 | `.pipeline/contracts/v9-forest-n3p.md:50-52` |
| T06 supplement 只有 Dr Sun 确认后才可作为正式桶依据 | `.pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md:12-15` |
| T06 supplement 当前 `reviewed:false` | `.pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md:1-5` |
| 6-method candidate 完整性 | `.pipeline/experiments/20260620_t14_candidate_6method_fullscale_md_dqn/analysis.md:56-67` |
| 6-method candidate 方法与规模 | `.pipeline/experiments/20260620_t14_candidate_6method_fullscale_md_dqn/analysis.md:24-35` |
| 6-method candidate Contract fail | `.pipeline/experiments/20260620_t14_candidate_6method_fullscale_md_dqn/analysis.md:102-110` |
| MD-DQN 成功率极低 | `.pipeline/experiments/20260620_t14_candidate_6method_fullscale_md_dqn/analysis.md:92-100` |
| `reviewed:false` 文档不可作为决策/论文依据 | `.pipeline/survey/document-confidence.md:24-32` |
