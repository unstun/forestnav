---
origin: ai+web+local
reviewed: false
created: 2026-07-04
topic: module2 A01.5 license audit for RL-RS evidence repositories
---

# A01.5 许可证审计

## 直观结论

本轮把 A01/A01.4 中出现的代码仓库分成三档:

1. **可复制代码**: 许可证允许复制/修改/再发布, 但必须保留原许可证/版权声明, 并且复制前还要做行级技术适配审计。
2. **只能读思想**: 可以读论文、README、接口形态和算法思想, 但不能把代码并入 ForestNav, 也不能照着逐行改写。
3. **不可用作代码来源**: 当前证据不足或技术位置不匹配, 不作为 module2 实现代码来源。

真正有直接实现参考价值的可复制来源是:

- `karlkurzer/path_planner`: BSD-3-Clause, 可参考 Hybrid A* shot/fallback 控制流。
- `AtsushiSakai/PythonRobotics`: raw `LICENSE` 是 MIT, 可参考 RS 数据结构/公式, 但本项目已有 RS 实现, 不应无必要替换。
- `sldai/crl_kino`: MIT, 可参考 "RL policy as RRT local planner" 的代码形态, 但 dynamics 和 planner slot 不同。
- `omron-sinicx/neural-astar`, `ahq1993/MPNet`, `tedhuang96/nirrt_star`, `reiniscimurs/DRL-robot-navigation`: 许可证允许读写复用, 但技术上分别是 search guidance / whole neural planner / sampling guidance / differential-drive navigation, 不能当 module2 同槽实现。

最重要的禁止项:

- `jiamiya/HOPE` 是 GPL-3.0。它可以作为相关工作和独立重实现线索, 但不能直接复制到 ForestNav core。
- `MRSTechnion/DiTree`, `ucsdarclab/mpnet_local_planner`, `ucsdarclab/motion_planning_transformer`, `mihdalal/neuralmotionplanner`, `pkicki/neural_path_planning` 在 GitHub API/raw 根目录检查中没有可用许可证。默认不复制、不 vendor、不逐行移植。

## 判定规则

- 以 GitHub API `/repos/{owner}/{repo}`、`/license` 和 raw `LICENSE`/`LICENSE.txt` 为一手证据。
- GitHub API `license.spdx_id=NOASSERTION` 不等于无许可证; 需要打开 raw license 文件读文本。
- 无 license 文件或 GitHub license endpoint 404 时, 按 GitHub 文档 lines 161, 176-179 对无许可证 public repo 的说明处理: 默认版权仍保留, 只能在 GitHub 平台允许的范围内查看/fork, 不能当作开源代码并入本项目。
- GPL-3.0 是开源许可证, 但 copyleft 边界不适合直接并入 ForestNav core。除非以后改成隔离的 GPL-compatible 组件或取得作者许可, 否则只读思想。
- 宽松许可证不是技术批准。MIT/BSD 只解决复制权限, 不解决 dynamics、planner slot、collision checker、telemetry 和论文 claim 是否匹配。

## 仓库分档

| 仓库 | 许可证证据 | 分档 | 可做 | 禁止 |
|---|---|---|---|---|
| `jiamiya/HOPE` | GitHub API: GPL-3.0; `LICENSE#L1-L2` 是 GPL v3 标题 | 只能读思想 | 写 related work; 借鉴 action mask、RS-distance shaping、difficulty curriculum; 独立重实现概念 | 复制/移植 GPL core code; 把 HOPE parking result 写成 ForestNav result |
| `karlkurzer/path_planner` | GitHub API: BSD-3-Clause; `LICENSE.txt#L1-L18` 给出 BSD-3-Clause 条款 | 可复制代码 | 参考 shot success return / fallback control flow; 必须保留版权和条件 | 当作 RL 证据; 无审计直接复制 C++/ROS 代码 |
| `AtsushiSakai/PythonRobotics` | API `NOASSERTION/Other`; raw `LICENSE#L1-L14` 是 MIT 文本 | 可复制代码 | 参考 RS path 数据结构/公式; 小段复用需保留 MIT notice | 无必要替换本项目已有 RS; claim GitHub SPDX 自动识别为 MIT |
| `omron-sinicx/neural-astar` | API `NOASSERTION/Other`; raw `LICENSE#L1-L17` 是 MIT 文本 | 可复制代码, 但非 module2 同槽 | related work/search guidance 参考; 可借鉴 differentiable search framing | 写成 local connector/RS shot 替换 |
| `sldai/crl_kino` | GitHub API: MIT; `LICENSE#L1-L13` 是 MIT 文本 | 可复制代码 | 参考 RL policy rollout as local planner 的代码形态; 独立适配 ForestNav dynamics | 直接当 Ackermann HA* analytic expansion 实现 |
| `ahq1993/MPNet` | GitHub API: MIT; `LICENSE#L1-L13` 是 MIT 文本 | 可复制代码, 但非 module2 同槽 | related work; neural replanning baseline 参考 | 写成 HA* analytic connector |
| `tedhuang96/nirrt_star` | GitHub API: MIT; `LICENSE#L1-L13` 是 MIT 文本 | 可复制代码, 但非 connector | learned sampling/search guidance 参考 | 写成 local edge generator |
| `reiniscimurs/DRL-robot-navigation` | GitHub API: MIT; `LICENSE#L1-L13` 是 MIT 文本 | 可复制代码, 但不作为 module2 code | reward/logging/training-loop 风格参考 | 复制为 Ackermann/RS/HA* 实现 |
| `MRSTechnion/DiTree` | GitHub API license endpoint 404; raw `LICENSE`/`LICENSE.txt` 404 | 只能读思想 | 论文和高层架构可引用; diffusion action sampler 作为 future v2 线索 | 复制 `planners/` 或 `policies/` 代码 |
| `ucsdarclab/mpnet_local_planner` | GitHub API license endpoint 404; raw `LICENSE`/`LICENSE.txt` 404 | 只能读思想 | Dynamic MPNet/Dubins local planner 概念对比 | 复制 ROS/C++ local planner |
| `ucsdarclab/motion_planning_transformer` | GitHub API license endpoint 404; raw `LICENSE`/`LICENSE.txt` 404 | 只能读思想 | search-space restriction related work | 复制 transformer/planning code |
| `mihdalal/neuralmotionplanner` | GitHub API license endpoint 404; raw `LICENSE`/`LICENSE.txt` 404 | 不可用作 module2 code | 可作为 manipulator learned planning 背景 | 复制代码; 写成 vehicle planner |
| `pkicki/neural_path_planning` | GitHub API license endpoint 404; raw `LICENSE`/`LICENSE.txt` 404 | 不可用作 module2 code | 只保留为检索线索 | 复制 TensorFlow/custom planner code |
| `PRX-Kinodynamic/ML4KP` | 本轮 GitHub API 因 rate limit 未完成; 不在 A01.4 主证据表 | 暂不使用 | 后续若纳入, 重新做 API/raw 审计 | 在本轮实现中引用或复制 |

## 对实现的约束

1. 如果后续 A02/A03 复制任何 MIT/BSD 代码, 必须在目标文件头或 `NOTICE`/`THIRD_PARTY` 记录来源、commit、许可证和改动说明。
2. GPL-3.0 / no-license 仓库只允许 "clean-room" 级别借鉴: 先写需求和接口, 再按 ForestNav 本地 API 独立实现, 不保留外部代码结构。
3. 当前 module2 直接实现应优先从本地接口出发: `local_slot_api.md` 已固定 operator 需要返回 validated edge 或 `None`。
4. 许可证审计不批准训练, 不批准 F02.6 warm-start, 不产生 formal performance claim。后续训练仍必须等 Dr Sun 批准, 并使用 `gpu3070ti-relay` 或明确批准的远端 GPU。

## 可写进论文的方法边界

可写:

- "We used permissively licensed classical Hybrid A* / RS codebases as implementation references where needed, while treating GPL/no-license learned planners as conceptual related work only."
- "No public repository audited here provides a permissively licensed, same-slot implementation of a learned/RL Hybrid A* analytic-expansion operator with terminal RS certification."

不可写:

- "PythonRobotics is MIT according to GitHub SPDX metadata." 事实更精确: GitHub API returned `NOASSERTION`, raw license text is MIT。
- "Neural A* license is unknown." 事实更精确: API returned `NOASSERTION`, raw license text is MIT。
- "DiTree/Dynamic MPNet/MPT code can be reused because it is public on GitHub." 无 license 不等于开源可复制。

## 核验记录

- GitHub API opened on 2026-07-04 for: `jiamiya/HOPE`, `karlkurzer/path_planner`, `AtsushiSakai/PythonRobotics`, `omron-sinicx/neural-astar`, `sldai/crl_kino`, `MRSTechnion/DiTree`, `ahq1993/MPNet`, `ucsdarclab/mpnet_local_planner`, `ucsdarclab/motion_planning_transformer`, `tedhuang96/nirrt_star`, `mihdalal/neuralmotionplanner`, `pkicki/neural_path_planning`, `reiniscimurs/DRL-robot-navigation`。
- Raw license files opened on 2026-07-04:
  - `https://github.com/jiamiya/HOPE/blob/main/LICENSE#L1-L2`
  - `https://github.com/karlkurzer/path_planner/blob/master/LICENSE.txt#L1-L18`
  - `https://github.com/AtsushiSakai/PythonRobotics/blob/master/LICENSE#L1-L14`
  - `https://github.com/omron-sinicx/neural-astar/blob/minimal/LICENSE#L1-L17`
  - `https://github.com/sldai/crl_kino/blob/master/LICENSE#L1-L13`
  - `https://github.com/ahq1993/MPNet/blob/master/LICENSE#L1-L13`
  - `https://github.com/tedhuang96/nirrt_star/blob/main/LICENSE#L1-L13`
  - `https://github.com/reiniscimurs/DRL-robot-navigation/blob/main/LICENSE#L1-L13`
- Raw missing checks opened on 2026-07-04 and returned 404 for root `LICENSE`/`LICENSE.txt`: `MRSTechnion/DiTree`, `ucsdarclab/mpnet_local_planner`, `ucsdarclab/motion_planning_transformer`, `mihdalal/neuralmotionplanner`, `pkicki/neural_path_planning`。
- GitHub no-license policy reference opened on 2026-07-04: `https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository#choosing-the-right-license`, lines 161, 176-179, 240-242。
