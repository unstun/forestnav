---
origin: ai+web+local
reviewed: false
created: 2026-07-04
topic: module2 A01.3 Dang 2022 analytic expansion deep read
source: Dang et al. 2022, Applied Sciences 12(12):5999
doi: 10.3390/app12125999
---

# A01.3 Dang 2022 Deep Read

## 直观结论

Dang et al. 2022 是本项目当前 classical analytic-expansion baseline 的直接相邻工作, 但它不是 RL 替换 RS。

它做的事情很具体: 在 Hybrid A* analytic expansion 触发时, 不只生成一条最小转弯半径 RS curve, 而是用多个曲率/转弯半径生成多条 RS candidate, 每条做碰撞检查, 再用 "Voronoi-field risk + movement cost" 选一条更安全的 RS path。若没有可用 RS candidate, 搜索继续走 forward expansion。

本地 `dang_multi_rs` 已实现这个控制流骨架, 但不是严格复现 Dang 原公式:

- 匹配: analytic slot、multi-curvature RS candidates、collision filtering、lowest-cost selection、success returns path、failure fallback to primitives、per-candidate timing telemetry。
- 偏离: Dang Eq.2 用最近障碍距离 `d0` 和 generalized Voronoi edge distance `dv`; 本地只用 mean EDT clearance 的倒数近似 risk, 丢失通道中心线信息。
- 偏离: Dang Eq.4 的 `w1/w2/w3` 是三项 movement cost 权重; 本地固定为 `1.0/1.0/1.0`, 没有 normalization/calibration。
- 偏离: Dang 的 forward-search motion-primitive tuning 是另一项贡献; 本地当前 A01.3 只审计 analytic expansion, 不能 claim 复现了 motion primitive fine tuning。

因此论文里更稳的写法是: "Dang-style multi-curvature RS analytic expansion baseline", 而不是 "exact Dang implementation"。

## 核验范围

已打开来源:

- MDPI HTML: `https://www.mdpi.com/2076-3417/12/12/5999`
- ResearchGate full-text mirror: `https://www.researchgate.net/publication/361291293_Improved_Analytic_Expansions_in_Hybrid_A-Star_Path_Planning_for_Non-Holonomic_Robots`
- 本地代码: `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py`

PDF 落盘状态:

- 尝试下载 `https://www.mdpi.com/2076-3417/12/12/5999/pdf` 到 `1_survey/papers/Dang2022_Improved_Analytic_Expansions_Hybrid_A_Star.pdf`。
- 结果: MDPI `/pdf` 返回 HTTP 403; ResearchGate "Download full-text PDF" 链接打开失败/无可用 PDF。
- 本轮没有伪造本地 PDF 文件; 依据来自已打开 HTML/full-text 页面和本地代码行号。

## 论文证据

| 主题 | 已核验锚点 | 对 ForestNav 的含义 |
|---|---|---|
| 问题位置 | MDPI lines 330-337; ResearchGate full-text lines 328-334 | Hybrid A* 的 analytic expansion 用 RS 提高准确性和速度, 这是本模块要替换/增强的槽位。 |
| RS 贴障碍问题 | MDPI lines 380-381; ResearchGate lines 641-652 | 论文明确观察到 green RS path 在角落贴墙, 测量/控制误差下可能碰撞。 |
| Hybrid A* 两阶段 | ResearchGate lines 422-493, 514-554 | Forward search 负责连续 successor; analytic expansion 负责精确到连续 goal。 |
| Eq.2 Voronoi field | ResearchGate lines 556-621 | `v(x,y)` 依赖 nearest obstacle distance `d0` 和 generalized Voronoi edge distance `dv`, 目标是让路径趋向通道中线。 |
| Section 3 多曲率依据 | MDPI lines 382-387; ResearchGate lines 658-755 | 多条 RS 路径来自不同曲率/转弯半径, 较小曲率可能更长但更安全。 |
| Eq.3/Eq.4 cost | MDPI lines 387-394; ResearchGate lines 758-844 | Objective 是 risk cost `v` 与 movement cost `m` 的加权组合; `m` 包含 path length、steering angle、steer switching。 |
| 三步 analytic method | MDPI lines 396-402; ResearchGate lines 846-867 | 先生成多曲率 RS, 做碰撞检查, 再按 Eq.3 选最低成本; 若无可用 RS, 继续 forward search。 |
| 实验参数 | ResearchGate lines 887-900 | 论文仿真用 binary occupancy grid, car-like robot 参数, 曲率 resolution 0.05。 |
| Table 1 | MDPI lines 414-419; ResearchGate lines 935-944, 956-960 | 小图上 improved RS 降低 risk cost, 但 analytic expansion 时间增加。 |
| Benchmark Table 2 | ResearchGate lines 1082-1086, 1109-1126, 1143-1149 | benchmark maps 上 risk reduction 为 24% 和 10% 等; 时间随 curvature step size 近似线性增加。 |
| 结论边界 | MDPI lines 433-435; ResearchGate lines 1153-1174 | 方法是在 analytic expansion phase 内生成不同曲率 RS 并选最小 risk; 缺点是 analytic expansion computation 增加不到约 10 倍。 |

## 本地实现对照

| 项 | Dang 2022 | ForestNav 当前实现 | 判定 |
|---|---|---|---|
| 插槽 | analytic expansion phase 内改 RS path selection。 | `_try_analytic_expansion()` 在有 custom operator 时走 custom, 否则走 `_try_builtin_analytic_expansion()`: `planner.py:294-297`。 | 匹配槽位。 |
| operator 类型 | 多曲率 RS candidate, 不是 learned policy。 | `ANALYTIC_OPERATORS = ("disabled", "single_rs", "dang_multi_rs")`: `planner.py:17`。 | 匹配 classical baseline。 |
| 参数 | curvature range/resolution; Eq.3 sigma weights。 | `curvature_step=0.05`, `max_curvature_ratio=2.0`, `sigma1=0.4`, `sigma2=0.6`: `planner.py:132-139`。 | 部分匹配; range 是项目化参数。 |
| 曲率扫描 | 不同 curvature values 生成 RS。 | `_analytic_radii()` 在 curvature space 等步长采样并转 radius: `planner.py:359-375`。 | 匹配核心思想。 |
| 多候选求解 | 对每个 curvature 生成 RS path。 | for each radius 调 `_try_rs_with_radius()`: `planner.py:322-347`。 | 匹配。 |
| 碰撞检查 | candidate curve 沿途碰撞检查, collision-free 才可进入 cost selection。 | `_try_rs_with_radius()` 对每段 `sample_constant_steer_motion()` 后 `collides_path()`: `planner.py:506-533`。 | 匹配。 |
| lowest-cost selection | 按 objective function 选最低 cost curve。 | `_dang2022_cost()` 后比较 `best_cost`: `planner.py:340-347`。 | 匹配。 |
| Eq.2 risk | Voronoi field, 使用 `d0` 和 `dv`, 偏向通道中线。 | `_dang2022_cost()` 注释承认用 mean EDT clearance inverse 近似; `_path_mean_clearance()` 只查询 obstacle distance: `planner.py:425-439`, `598-612`。 | 重要偏离。 |
| Eq.4 movement | length、steering angle、steer switching, 带 `w1/w2/w3`。 | local 统计 `l_p/s_p/c_p`, 但 `_w1/_w2/_w3 = 1.0`: `planner.py:441-456`。 | 部分匹配; 缺 normalization。 |
| fallback 语义 | 没有可用 RS curve 就继续 forward search。 | analytic failure 只 append failure record, 然后进入 primitive expansion loop: `planner.py:767-805`。 | 匹配。 |
| success 语义 | 可用 RS curve 成为到 goal 的 path, search ends。 | analytic success 拼接 `extra_states/extra_actions` 并返回 stats: `planner.py:745-766`。 | 匹配。 |
| timing/cost accounting | paper 承认多 candidate 使 analytic computation 增加。 | 本地 `AnalyticCandidateTelemetry`/`AnalyticExpansionTelemetry` 记录 per-candidate solve/sample/collision/cost time: `planner.py:34-80`, `349-356`, `563-573`。 | 项目增强。 |
| fine tuning | 论文另做 forward-search motion-primitive tuning。 | A01.3 未发现本地以 Dang Section 4.2 名义复现 motion-primitive tuning; 本地 primitives 属独立 planner 配置。 | 不能 claim 复现。 |

## 对 Module2 的设计影响

1. Dang 是必须保留的 classical baseline: 它已经处在正确 analytic slot, 能证明单条 RS shot 的安全问题和多曲率 RS 的 classical remedy。
2. Dang 不能替代本项目的创新点: 它仍然只在 RS family 内选曲线, 不是闭环 RL steering rollout; 不能学习绕开 RS family 无法穿过的局部瓶颈。
3. 本项目 RL-RS operator 必须在同一 slot 与 Dang 公平比较: 同样要记录 policy forward、rollout sampling、collision check、terminal RS、fallback count, 不能只报 neural inference time。
4. 若论文需要把 Dang 写成 baseline, 当前代码应写成 "Dang-style"。要写 "Dang exact" 前必须补 generalized Voronoi distance `dv` 或明确证明 mean EDT approximation 与论文 Eq.2 在本数据上的影响。
5. Dang 的时间负担是一个天然 reviewer 问题: 本地 D01/D02 的成本账应直接回应 paper 中 "多曲率 RS 增加 analytic computation" 的边界。

## 不可 claim

- 不能说 Dang 是 RL 或 learned connector。
- 不能说本地已经严格实现 Dang Eq.2, 因为没有 `dv`/generalized Voronoi edge distance。
- 不能把 Dang 的 benchmark-map risk reduction 当 ForestNav 森林地图结果。
- 不能把本地 `curvature_step=0.05` 等同于论文完整参数复现; 论文 robot size/wheelbase/max steer 与 ForestNav Ackermann 参数不同。
- 不能把 Section 4.2 motion-primitive tuning 写成本地 A01.3 已完成事项。
- 本报告是证据硬化, 不启动训练; 后续若进入正式 PPO/remote smoke, 只能使用 `gpu3070ti-relay`, 不在本地训练。

## A01.3 判定

A01.3 可以标为完成: 已深读 Dang 2022 Section 2.1、Section 3、Eq.2-4、Table 1/2 和 conclusion, 并和本地 `planner.py` 做逐项匹配/偏离。

下一项应进入 A01.4: learned connector / learned goal shot / neural steering function 检索。Dang 只支持 classical baseline 和问题动机, 不能回答 "有没有人已经用 learning 替代 analytic connector"。
