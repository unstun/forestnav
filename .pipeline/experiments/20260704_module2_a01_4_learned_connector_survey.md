---
status: completed
origin: ai+web+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - 0_trials/module2_rl_rs_evidence/sources.md
---

# A01.4 Learned Connector Survey

## 直观结论

本轮完成 A01.4 learned connector / learned goal shot / neural steering function 查重。

核心发现不是 "没人做过 learned local connector"。相反, S3F、RL-RRT、Learned Goal-Reaching Controllers、DiTree 都证明 learned/RL/generative local connector 可以嵌入 sampling-based kinodynamic planner。

但已核验来源里没有找到 ForestNav 同槽实现: 即在 Hybrid A* analytic expansion / RS shot 触发点, 用 learned/RL rollout 生成可验证 local edge, 成功直接拼接, 失败返回 `None` 并回落 primitive expansion, 末端再由 RS certificate 负责贴合。

## 产物

- `0_trials/module2_rl_rs_evidence/learned_connector_survey.md`
- 更新 `0_trials/module2_rl_rs_evidence/sources.md`
- 更新 `0_trials/module2_rl_rs_evidence/paper_claims.md`
- 更新 `0_trials/module2_rl_rs_evidence/negative_results.md`
- 更新 `0_trials/module2_rl_rs_evidence/github_repos.md`
- 更新 `.pipeline/mainline_module2_rl_rs_replacement.md`

## 核验范围

论文 8 个:

- `1_survey/papers/pdf/Atreya2022S3F.pdf`
- `1_survey/papers/pdf/Chiang2019RLRRT.pdf`
- `1_survey/papers/pdf/Sivaramakrishnan2021LearnedGoalReachingControllers.pdf`
- `1_survey/papers/pdf/Hassidof2025DiTree.pdf`
- `1_survey/papers/pdf/Johnson2020DynamicMPNet.pdf`
- `1_survey/papers/pdf/Li2021MPCMPNet.pdf`
- `1_survey/papers/pdf/Johnson2022MotionPlanningTransformers.pdf`
- `1_survey/papers/pdf/Qureshi2019MPNet.pdf`

代码仓库 7 个:

- `sldai/crl_kino`
- `MRSTechnion/DiTree`
- `ahq1993/MPNet`
- `ucsdarclab/mpnet_local_planner`
- `ucsdarclab/motion_planning_transformer`
- `tedhuang96/nirrt_star`
- `mihdalal/neuralmotionplanner`

## 关键判定

可用:

- S3F 支持 learned steering function as a replacement for expensive local connector。
- RL-RRT / `crl_kino` 支持 RL policy as local planner inside RRT expansion。
- Learned Goal-Reaching Controllers 支持 "local goal + learned controller" 的 tree expansion 设计。
- DiTree 支持 generative action sampler + classical tree collision checking。
- MPNet/Dynamic MPNet/MPC-MPNet/MPT/NIRRT*/NeuralMP 提供 related-work 背景和替代设计线索。

不可用:

- 不能 claim exact HA* analytic shot replacement 已被公开实现。
- 不能把 whole neural planner/search guidance 写成本项目同槽方法。
- 不能复制无 license 仓库代码。
- 不能启动训练或把外部论文数字当 ForestNav 结果。

## 验证

- Memory retrieval: confirmed A01.4 remained open; F02.6 remains pending; local training remains forbidden。
- ACE: `mcp__auggie__codebase-retrieval` returned `402 Payment Required`; used exact local reads, arXiv/PDF source extraction, GitHub raw/API reads。
- Downloaded PDFs into ignored local paper library `1_survey/papers/pdf/` and extracted line anchors with `pdftotext -layout ... | nl -ba`。
- GitHub license checked through GitHub API and raw `LICENSE` for MIT repositories。
- No local training or remote training was run。

## 边界

- This is evidence hardening, not implementation。
- This does not approve F02.6。
- This does not produce a formal PPO checkpoint。
- Future formal training remains restricted to `gpu3070ti-relay` after explicit approval。
- Next Phase A item is A01.5 license audit。
