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

# A01.3 Dang 2022 Deep Read

## 直观结论

本轮完成 A01.3 Dang 2022 analytic expansion 深读。

Dang 是 ForestNav 当前 `dang_multi_rs` baseline 的直接邻居: 它在 Hybrid A* analytic expansion 槽位中生成多条不同曲率 RS path, 逐条碰撞检查, 再用 risk + movement cost 选最低成本。这个证据支持 "RS analytic expansion 的安全性问题是真问题", 也支持 Dang-style multi-RS 作为 classical baseline。

但它不是 RL, 也不是 learned connector。它仍然只在 RS family 内选曲线。

## 产物

- `0_trials/module2_rl_rs_evidence/dang2022_deep_read.md`
- 更新 `0_trials/module2_rl_rs_evidence/sources.md`
- 更新 `0_trials/module2_rl_rs_evidence/paper_claims.md`
- 更新 `0_trials/module2_rl_rs_evidence/negative_results.md`
- 更新 `.pipeline/mainline_module2_rl_rs_replacement.md`

## 核验来源

论文/全文:

- MDPI HTML: `https://www.mdpi.com/2076-3417/12/12/5999`
- ResearchGate full-text mirror: `https://www.researchgate.net/publication/361291293_Improved_Analytic_Expansions_in_Hybrid_A-Star_Path_Planning_for_Non-Holonomic_Robots`
- 已核行段:
  - MDPI lines 330-337, 380-402, 414-419, 433-435。
  - ResearchGate full-text lines 556-621, 758-867, 887-900, 935-960, 1082-1086, 1109-1174。

本地代码:

- `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py`
- 已核行段:
  - `:17`, `:132-139`, `:294-375`, `:425-458`, `:460-573`, `:598-612`, `:724-805`。

PDF:

- 尝试下载 MDPI PDF 到 `1_survey/papers/Dang2022_Improved_Analytic_Expansions_Hybrid_A_Star.pdf`, 源站返回 HTTP 403。
- ResearchGate download link 也未返回可用 PDF。
- 本轮没有落盘 PDF, 也没有用未打开 PDF 作为依据。

## 关键判定

可用:

- Dang 支持 "single RS analytic expansion 会贴障碍/角落, 需要 safety-aware selection" 这个问题动机。
- Dang 支持 "classical multi-curvature RS baseline"。
- Dang 的 Table 1/2 和 conclusion 支持记录 compute overhead: 多曲率 RS 会增加 analytic expansion computation。

不可用:

- 不能把 Dang 写成 RL 或 learned policy。
- 不能把 Dang benchmark risk reduction 写成 ForestNav 结果。
- 不能把当前本地实现写成 exact Dang Eq.2; 本地是 mean EDT clearance inverse approximation, 缺 `dv`。
- 不能 claim 已复现 Dang forward-search motion-primitive fine tuning。

## 验证

- Memory retrieval: confirmed A01.3 remained open and F02.6/H01/H02 remain blocked by human decision and missing PPO checkpoint.
- ACE: `mcp__auggie__codebase-retrieval` returned `402 Payment Required`; used exact local reads and web source reads.
- Web: opened MDPI HTML and ResearchGate full-text mirror, with line anchors listed above.
- Local: read exact `planner.py` line ranges for builtin analytic expansion, multi-radius generation, Dang-style cost, RS sampling/collision check, and fallback to primitives.

## 边界

- This is evidence hardening, not implementation.
- This does not approve F02.6.
- This does not run local training.
- If training starts later, formal runs must use `gpu3070ti-relay`; local machine remains no-training.
- Next external evidence task is A01.4 learned connector / learned goal shot / neural steering function search.
