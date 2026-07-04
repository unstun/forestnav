---
status: completed
origin: ai+web+local
reviewed: false
created: 2026-07-04
parent: .pipeline/mainline_module2_rl_rs_replacement.md
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
depends_on:
  - 0_trials/module2_rl_rs_evidence/sources.md
  - 0_trials/module2_rl_rs_evidence/github_repos.md
  - 0_trials/module2_rl_rs_evidence/learned_connector_survey.md
---

# A01.5 License Audit

## 直观结论

本轮完成 A01.5 许可证审计, 将 A01/A01.4 相关仓库按 "可复制代码 / 只能读思想 / 不可用作代码来源" 分档。

结果对后续实现很关键:

- 可复制代码不等于同槽实现。MIT/BSD 只能说明许可证允许复制/修改, 不能证明 dynamics、collision checker、planner slot 与 ForestNav 匹配。
- GPL/no-license 仓库不能作为 ForestNav core 代码来源。HOPE、DiTree、Dynamic MPNet local planner、MPT 等仍可用于 related work 和 clean-room 设计。
- A02/A03 若真的复制 MIT/BSD 片段, 必须追加来源、commit、许可证和改动说明。

## 产物

- `0_trials/module2_rl_rs_evidence/license_audit.md`
- 更新 `0_trials/module2_rl_rs_evidence/sources.md`
- 更新 `0_trials/module2_rl_rs_evidence/github_repos.md`
- 更新 `0_trials/module2_rl_rs_evidence/negative_results.md`
- 更新 `0_trials/module2_rl_rs_evidence/paper_claims.md`
- 更新 `.pipeline/mainline_module2_rl_rs_replacement.md`

## 核验范围

必查仓库:

- `jiamiya/HOPE`: GitHub API GPL-3.0; raw `LICENSE#L1-L2` GPL v3。
- `karlkurzer/path_planner`: GitHub API BSD-3-Clause; raw `LICENSE.txt#L1-L18` BSD terms。
- `AtsushiSakai/PythonRobotics`: GitHub API `NOASSERTION/Other`; raw `LICENSE#L1-L14` MIT text。
- `omron-sinicx/neural-astar`: GitHub API `NOASSERTION/Other`; raw `LICENSE#L1-L17` MIT text。

A01.4 追加仓库:

- MIT/raw permissive: `sldai/crl_kino`, `ahq1993/MPNet`, `tedhuang96/nirrt_star`, `reiniscimurs/DRL-robot-navigation`。
- No detected license: `MRSTechnion/DiTree`, `ucsdarclab/mpnet_local_planner`, `ucsdarclab/motion_planning_transformer`, `mihdalal/neuralmotionplanner`, `pkicki/neural_path_planning`。

## 关键判定

可复制代码:

- `karlkurzer/path_planner`: Hybrid A* shot/fallback 工程控制流参考。
- `AtsushiSakai/PythonRobotics`: RS path data structure/formula 参考; 本项目已有 RS 实现, 不建议无必要替换。
- `sldai/crl_kino`: RL policy as local planner inside RRT 的近正例代码; 需要独立适配 ForestNav HA* slot。
- `omron-sinicx/neural-astar`, `ahq1993/MPNet`, `tedhuang96/nirrt_star`, `reiniscimurs/DRL-robot-navigation`: 可读可复制, 但不是 module2 同槽实现。

只能读思想:

- `jiamiya/HOPE`: GPL-3.0, 只作为相关工作/设计线索。
- `MRSTechnion/DiTree`, `ucsdarclab/mpnet_local_planner`, `ucsdarclab/motion_planning_transformer`: 技术上有价值, 但无 license, 不能复制代码。

不可用作 module2 code:

- `mihdalal/neuralmotionplanner`: no license + manipulator domain。
- `pkicki/neural_path_planning`: no license + 未进入主证据链。
- `PRX-Kinodynamic/ML4KP`: 本轮 API 因 rate limit 未核验完成, 不纳入可复用集合。

## 验证

- Memory retrieval: confirmed A01.5 was the next open item; F02.6 remained pending; local training remains forbidden。
- ACE: `mcp__auggie__codebase-retrieval` returned `402 Payment Required`; used exact local reads and GitHub primary sources。
- GitHub API opened for 13 repositories before unauthenticated rate limit was reached。
- Raw license files opened for GPL/BSD/MIT repositories。
- Root raw `LICENSE`/`LICENSE.txt` 404 checks opened for no-license repositories。
- No local training or remote training was run。

## 边界

- This is not legal advice; it is a reproducibility/code-reuse guardrail for the research project。
- This does not approve F02.6。
- This does not produce a PPO checkpoint。
- This does not unlock formal performance claims。
- Any formal training remains restricted to `gpu3070ti-relay` or another explicitly approved remote GPU after Dr Sun approval。
