---
origin: ai+local
reviewed: false
date: 2026-06-20
task: T14
status: needs_human_review
---

# T14 RS-verified Fullscale Review Packet

## 直观结论

RS-verified segment 候选值得继续审，但还不能把 T14 勾掉。它把原先的 T14 速度失败大幅缩小：Complex 已经通过 Contract 速度门槛，Extreme 仍差 7.8 个百分点。

## 本轮证据

- 新 rerun：`.pipeline/experiments/20260620_t14_candidate_6method_fullscale_rs_segments/`
- 对比分析：`.pipeline/experiments/20260620_t14_rs_fullscale_comparison/analysis.md`
- 远端日志：`.pipeline/experiments/logs/20260620_t14_candidate_6method_fullscale_rs_segments.{out,err,exit}`
- source head：`98faaba69dfe79fe6c8f9d41f3fb59cf249f3987`
- 远端主机：`ubuntu-OMEN-by-HP-Laptop-17-ck1xxx` (`gpu3070ti-relay`)

## Contract 状态

| bucket | old median time reduction | RS-verified reduction | Contract gate |
|---|---:|---:|---|
| Complex | -29.9% | 90.8% | pass |
| Extreme | -26.2% | 42.2% | fail |

完整性：300 queries、1800 records、6 methods、0 method exceptions、0 collision violations。

## 仍不能完成 T14 的原因

1. T06 cutpoint supplement 仍是 `reviewed:false`，只能作候选证据。
2. Extreme 桶未达到 `median_time_reduction >= 50%`。
3. RS-verified segment 是方法实现变体，是否纳入正式 F-N3P 方法需要 Dr Sun 审。
4. MD-DQN 历史 checkpoint 仍只能说明 adapter 可运行，不能自动成为公平正式 RL baseline。

## 建议审阅顺序

1. 先审 `commit_verified_rs_segments` 是否符合 F-N3P 方法定义。
2. 再决定 Extreme 的处理：继续方法重设计、记录负结果，或建立 Contract v2。
3. 再审 T06 cutpoints 和 MD-DQN baseline 身份。

## 禁止外推

- 不能写 T14 complete。
- 不能写 paper main result passed。
- 不能把 Extreme 结果说成通过。
- 不能把 MD-DQN historical checkpoint 当公平 RL baseline，除非 Dr Sun 明确确认。
