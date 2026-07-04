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

# A01.2 HOPE Deep Read

## 直观结论

本轮完成 A01.2 HOPE 深读。

HOPE 是必须在 related work 里正面处理的强相关工作, 因为它确实把 RL agent 和 Reeds-Shepp curve 结合起来做 parking path planning。但逐行读论文和代码后, 它不是 ForestNav module2 的同一插槽:

- HOPE 的 RS route 由 parking env 在接近目标时发现, 作为 `info['path_to_dest']` 交给 `ParkingAgent` 执行。
- ForestNav module2 的目标是在 Hybrid A* analytic expansion trigger 处, 用 learned RL-RS operator 替换/补充 RS shot, operator 失败必须返回 `None` 并回落 primitive expansion。

## 产物

- `0_trials/module2_rl_rs_evidence/hope_deep_read.md`
- 更新 `0_trials/module2_rl_rs_evidence/sources.md`
- 更新 `0_trials/module2_rl_rs_evidence/github_repos.md`
- 更新 `0_trials/module2_rl_rs_evidence/paper_claims.md`
- 更新 `0_trials/module2_rl_rs_evidence/negative_results.md`
- 更新 `.pipeline/mainline_module2_rl_rs_replacement.md`

## 核验来源

论文:

- HOPE arXiv HTML `https://arxiv.org/html/2405.20579v1`
- 已核行段: lines 39-41, 113-172, 173-200, 247-267, 293-339, 340-353。

代码:

- repo: `https://github.com/jiamiya/HOPE`
- pinned HEAD: `2accab93e8602bd7dac780078a012574cc2cb4d7`
- license: GPL-3.0, `LICENSE:1-2`
- 已读文件:
  - `src/model/agent/parking_agent.py`
  - `src/train/train_HOPE_ppo.py`
  - `src/train/train_HOPE_sac.py`
  - `src/env/car_parking_base.py`
  - `src/env/env_wrapper.py`
  - `src/env/vehicle.py`
  - `src/model/action_mask.py`
  - `src/evaluation/eval_mix_scene.py`
  - `src/evaluation/eval_utils.py`

## 关键判定

可用:

- HOPE 可作为 RL+RS 组合的强相关 related work。
- HOPE 支持 action mask/safe-action prior、RS-distance shaping、difficulty curriculum、RS hybrid ablation、成本拆分这些设计线索。
- HOPE 证明 naive PPO/SAC 和 RS/Hybrid A* baseline 都是 reviewer 可能要求解释的对象。

不可用:

- 不能复制 HOPE GPL-3.0 代码。
- 不能把 HOPE 的 parking success rate 当 ForestNav 森林场景证据。
- 不能说 HOPE 已经替换 HA* analytic expansion slot。
- 不能用 HOPE 的 action mask 作为 ForestNav 安全证明; ForestNav 必须用自己的 EDT/Grid footprint checker 验证。

## 验证

- Memory retrieval: confirmed A01.2 remained open and F02.6/H01/H02 remain blocked by human decision and missing PPO checkpoint.
- ACE: `mcp__auggie__codebase-retrieval` returned `402 Payment Required`; used exact local reads and web/raw source reads.
- Web: opened HOPE arXiv HTML and GitHub repository/license/code pages.
- Raw code line audit:
  - `git ls-remote https://github.com/jiamiya/HOPE HEAD` -> `2accab93e8602bd7dac780078a012574cc2cb4d7`.
  - `curl -L -s .../parking_agent.py | nl -ba | sed -n '1,130p'`
  - `curl -L -s .../train_HOPE_ppo.py | nl -ba | sed -n '1,220p'`
  - `curl -L -s .../car_parking_base.py | nl -ba | sed -n '1,520p'`
  - `curl -L -s .../action_mask.py | nl -ba | sed -n '1,280p'`
  - `curl -L -s .../eval_mix_scene.py | nl -ba | sed -n '1,220p'`

## 边界

- This is evidence hardening, not implementation.
- This does not approve F02.6.
- This does not run local training.
- This does not produce formal H02 results.
- Next external evidence task is A01.3 Dang 2022 analytic expansion deep read.
