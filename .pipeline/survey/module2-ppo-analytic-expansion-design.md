---
origin: human+ai+web
reviewed: false
date: 2026-07-02
topic: 模块2 设计——PPO 转向策略替代 Reeds-Shepp 解析扩展
confidence: low
---

# 模块2 设计：PPO 转向策略替代 Reeds-Shepp 解析扩展

> 状态：本次方法设计会话（2026-07-02）收敛的模块2 骨架决策。
> 关键方向决策由 Dr Sun 拍板，文献佐证均经联网核验（附 URL + 原文片段），
> 但**尚无任何代码验证或实验数据**（reviewed: false, confidence: low）。
> 超参初值均标注"待 gate/试点校准"，不是拍死的常数。
> 上游背景见 `primitive-pruning-plus-learned-expansion-idea.md`（双模块叙事收敛）。

---

## 零、本次会话的决策记录（谁定的、为什么）

| 决策 | 谁定 | 理由 |
|---|---|---|
| 模块2 先行，模块1 挂起 | Dr Sun | 风险驱动：新颖性核心=不确定性核心，先验证。模块1 有 Franke2025 先例托底，晚做不慌。 |
| 问题定义 = A（直接替代 RS） | Dr Sun | 相信神经网络生成能力，保持对 RS 语义的忠实替代 + "提前终止"叙事完整。 |
| 训练方法 = PPO（RL） | Dr Sun | 见第三节论证：本问题落在 RL 舒适区（模拟器极快、短视野目标条件导航、成功判据可精确定义）。 |
| 输入 = 自适应局部地图（闭环 policy 每步局部观测） | Dr Sun | "走了一半就不用看全局"——闭环 rollout 观测跟车移动，化解视野/变长/漂移三难题。 |

---

## 一、问题定义（定义 A：直接替代）

模块2 = 一个**学习型局部转向策略（steering policy）**，放在 Hybrid A* 的
**解析扩展槽（analytic expansion）**，忠实替代 Reeds-Shepp：

- 解析扩展触发时，从当前弹出节点开始，在地图上**虚拟 rollout** 这个 policy，
  逐步走向最终目标；走出来的轨迹就是替代 RS 的连接曲线。
- rollout 无碰撞到达"RS 能对接目标的状态"即**提前终止搜索**（速度来源）；
  生成曲线比网格扩展平滑（质量来源）。
- rollout 碰撞或超预算即**中止回退**，落回正常基元扩展——不破坏搜索完备性。

**为什么定义 A 站得住（级联重试论证）**：解析扩展不是一锤子买卖，它在搜索中被
反复调用（`planner.py:454-457`，自适应 interval），搜索树不断向目标推进，每次
调用的剩余问题都在缩小。所以 policy 不需要"从 40m 外一次命中"，只要在"目标已进
中近程、RS 还够不着"的区间比 RS 早命中，收益就兑现。per-call 成功率不需很高，
架构天然是级联重试系统。这也与 Dolgov 原始设计一致——解析扩展本就是"临门一脚"
机制，远程命中从来不是主战场。

---

## 二、架构：闭环 PPO 转向策略

- **形态**：闭环 policy（不是开环生成模型）。每步：观测 → 输出下一步动作 → 运动学
  积分前进一步 → 重新观测。观测跟随虚拟 rollout 移动，因此天然"走到哪看到哪"，
  不需要大视野 / 变长解码 / 开环漂移补偿。
- **观测**：自车系局部占据 patch（以车体为中心、对齐车头方向）+ 目标相对位姿。
  平移旋转不变性好，训练数据效率高。
  - 待校准（gate #2）：patch 半径、分辨率；是否叠加 2D 距离场通道（给 policy 现成
    的"离障碍多远"，可能大幅降低学习难度，代价是一步预计算）——建议主方案含距离场，
    纯占据栅格作消融。
- **动作**：连续曲率，tanh 限幅到 [-κ_max, κ_max]。
  - **起步只前进，不带倒车**。森林穿越主体是前向运动；倒车让探索难度上一个台阶，
    留作扩展项。（Dr Sun 若认为森林场景倒车不可少，再议。）
- **rollout 步长**：初值与基元 step 一致（0.3m），可放大以省前向次数（代价：控制
  粒度变粗）。直接挂钩 gate #1 的成本账，待实测校准。
- **rollout 预算上限**：最长 ≈ 1.5× 当前到目标直线距离，超则判失败——防原地打转，
  同时是推理成本的硬上界。
- **网络规模**：必须小（小 MLP 级别 / 轻量 CNN 编码 patch），因为每次调用 = N 步前向。

---

## 三、为什么 PPO 成立（对抗"RL 又贵又不稳"的通用先验）

1. **模拟器几乎不要钱**：rollout = 运动学积分 + 网格 footprint 碰撞检查
   （`geometry.py:398` 现成），无物理引擎，CPU 每小时千万步量级。RL 最大软肋（采样贵）
   在此不存在。程序化森林生成器（`maps/forest.py:494`）无限出图 = 天然域随机化。
2. **短视野目标条件导航**是 RL 被验证最充分的任务型，非 exotic 应用。
3. **PPO 直接在部署分布上训练**：规避 BC 的两大痛点——oracle 偏置（HA* 路径带网格
   量化风格）和 rollout 分布偏移（BC 要上 DAgger 补丁）。
4. **成功判据可精确定义**（最关键）：reward 成功判据 = "到达一个 RS 能无碰撞对接
   目标的状态"。训练目标精确等于 policy 在系统里的实际使命，训练判据 = 部署判据，
   模拟器里跑个 RS 检查即可算，无需人工设计"多近算成功"。
5. 项目已有 RL 基础（`forest_policy.py` DQN 家族），管线非从零搭。

**风险对冲**：
- 训练不稳/调参坑 → **BC 预热 + PPO 精调**（oracle 数据几乎白拿，现成
  `training_data.py` 管线）。纯 BC 顺手留作消融，论文里"PPO > BC 因分布匹配"是现成
  分析点。
- reward 被钻空子（贴树皮换最短路）→ reward 加 clearance 项 + 距离场进度 shaping。

---

## 四、reward 配方（初值，gate/试点后校准）

| 项 | 方向 | 作用 |
|---|---|---|
| 到达 RS 可对接域 | 大正 | 成功信号 = 部署使命 |
| 碰撞 | 大负 + 终止 | 可行性 |
| 距离场进度 shaping | 小正/步 | 引导向目标，用现成 2D 距离场 |
| clearance | 小正 | 防贴障碍，保安全裕度 |
| 曲率变化率惩罚 | 小负 | **直接挂钩"质量"叙事**——我们声称生成曲线比网格路径平滑，必须在 reward 里体现，不能指望免费得到 |
| 步数/弧长 | 小负/步 | 促短路径，防打转 |

---

## 五、与 HA* 的集成

- 插入点：`planner.py` 解析扩展的 None 分支之后（`_try_analytic_expansion` 返回
  None → 当前落回基元扩展循环 L476）。模块2 插在这个 None 分支上：**RS 先试，RS 失败
  才轮到 policy rollout**，rollout 也失败才回退基元扩展。天然不破坏完备性。
- 沿用现有自适应 interval（`_analytic_interval` L197，离目标近则更频繁）。
- **末端 RS 数值收尾**：policy homing 到目标附近后残差已小，末段用 RS 精确对接目标
  位姿。注意——这里 RS 只是端点对接的数值工具，不是分担路程的接力者，"直接替代"
  语义不变。
- **计时口径修正（必做）**：现有 F-N3P 把 RS 验证段耗时记为 0（`inference.py`
  L484/L635）。我们要做**含推理的端到端 wall-clock 诚实口径**，这处必须先修。
  这也正是与 Franke2025 的评测差异点——它把推理时间明确剔除在 duration 之外
  （"excluding inference time of the diffusion model"），我们不这么记账。

---

## 六、三级 kill-fast gate（每级独立止损判据）

| Gate | 内容 | 止损判据 | 成本 | 阶段 |
|---|---|---|---|---|
| **#2 oracle 形态分析** | 不训练网络。Complex/Extreme 桶 RS 失败节点上跑全图 HA*，统计"存在可行平滑连接"的比例 + 形态（长度/转向点分布/是否过一瓶颈即开阔） | 若多数失败节点根本无像样连接曲线 → 问题病态，止损 | 1-2 天 | Contract 前可做 |
| **#1 成本账 microbenchmark** | 单步 policy 前向耗时 × 典型 rollout 步数 vs 省下的搜索扩展时间 | 账算不平且无架构可救 → 止损 | 几小时 | Contract 前可做 |
| **#3 PPO 收敛试点** | 单一密度档小地图训一版，确认奖励配方能收敛 | 奖励配方调不收敛 → 回退 BC，或重审问题 | 数天（训练） | **须 Contract approved 后**（硬规则#20） |

gate #2 顺带校准：patch 尺寸、rollout 步长、预算上限、D_max（若引入作用半径）。

---

## 七、新颖性边界与差异表述（联网核验，2026-07-02）

**总判定**：HA* 的解析扩展槽仍是空白。所有已核验的"RL policy 当 steering 子例程"
工作全部落在采样式规划器（RRT/roadmap），无一碰 HA* 解析扩展。HA* 内被学习组件
动过的唯一槽位是 node expansion（Neural Hybrid A*，CVAE 引导，非 RL，非解析扩展）。

**必须写进 related work 的差异表述**（差异恰好落在两个已定决策上）：

- **Sivaramakrishnan et al. 2021**（arXiv:2110.04238，最近邻）：RL 训练"**无障碍**
  下到达局部航点"的控制器，嵌入**采样式**规划器扩展步。原文核验（WebFetch）：
  "a reinforcement learning process is trained offline to return a low-cost control
  that reaches a local goal state (i.e., a waypoint) in the absence of obstacles"。
  → 差异：(a) 槽位不同——我们在 HA* 解析扩展槽，保留网格搜索完备性骨架 + RS 对接
  检查；它在采样树扩展步，无网格骨架。(b) 障碍感知位置不同——它无障碍训练、避障
  靠外部航点；我们 **policy 每步观测局部 patch，rollout 本身障碍感知**（= Dr Sun 定的
  "自适应地图输入"，成为划清界限的关键轴）。
- **RL-RRT**（arXiv:1907.04799，2019 RA-L）：RL 避障 policy 当 RRT local planner。
  原文核验："we use deep reinforcement learning to learn an obstacle-avoiding policy
  ... which is used as a local planner during planning" / "RL-RRT that uses the RL
  policy as a local planner"。→ 同 Sivaramakrishnan：RRT steering，非 HA* 解析扩展。
- **Neural Hybrid A***（Kim2021Neural，arXiv:2111.06739，本地库已核验方法节）：CVAE
  引导 **node expansion**（gate 动作集合，"80% of the node expansion proceeds with
  the help of a neural network model"），全文无 analytic expansion/RS/Dubins 字样。
  → 不同槽位（扩展 vs 解析扩展）+ 不同范式（CVAE vs RL）。（注：它其实更接近**模块1**
  的剪枝范式，模块1 会话再用。）
- **HOPE**（arXiv:2405.20579，2024）：端到端 RL + RS 曲线经 action-mask 融合，非搜索式
  HA*。→ 弱相关。

**查重遗留（下次文献会话补，不阻塞设计）**：
1. "learned one-shot connection / learned goal-connect search"角度只扫 2 轮，负面结论
   建议再补 1-2 轮确认。
2. 2024-2026 森林/off-road HA* + 学习组件最新预印本未专门扫。
3. Roadmaps with Gaps（arXiv:2310.03239，Bekris 组）edge 机制仅凭搜索摘要，需开
   HTML 逐字核验后才能写进 related work。
4. 纯 IL（非 RL）steering 直接嵌 HA* 的小众工作未查（RRT-CoLearn 等只查了 RRT 版）。

---

## 八、挂起项（本会话未决，留待后续）

1. **模块1**（学习型运动基元剪枝）——剪枝对象、推理范式、训练信号全部未定。开放问题：
   是否统一用 RL 框架（叙事"双 RL 模块"更整齐）还是维持独立监督学习设计。
   注：Kim2021Neural 的 CVAE gate 动作集合是模块1 的直接相邻先例，届时纳入。
2. 倒车动作扩展（模块2 起步不含）。
3. 多模态处理（左绕/右绕）——闭环 policy 比开环缓和（每步看障碍不对称自然 committed
   一边），但训练数据同场景两种绕法混着会互相打架，可能需随机策略采 K 条 rollout 或
   数据清洗。
4. 模块1↔模块2 组合是否互相干扰（剪枝后模块2 输入分布漂移）——组合阶段评估。

---

## 九、相关文档

- 双模块叙事收敛：`primitive-pruning-plus-learned-expansion-idea.md`
- 放弃的路线 A（learned heuristic）：`learned-heuristic-for-search-planning.md`
- 实验数据来源：`gptpro-env-abstraction-prompt.md`（F-N3P vs HA*/N3P）
- 代码事实来源：`2_experiment/forest_n3p/`（planner.py / inference.py / primitives.py /
  maps/forest.py / mlp.py / training_data.py / forest_policy.py）
- 新增文献：`.pipeline/literature/index.md` → `Franke2025Accelerating`
