---
origin: ai+web
reviewed: false
updated: 2026-07-02
---

# ForestNav 术语规范表

> 论文写作、设计文档、代码注释全程对照此表。
> 2026-06-20 联网核查更新：修正 AI 黑话，补全领域标准译法。

## 核心方法术语

| 术语 | 正式英文 | 正式中文 | 禁止用法 | 来源/说明 |
|------|----------|----------|----------|-----------|
| 子目标分解 | subgoal decomposition | 子目标分解 | route decomposition / 路由分解 | 层次规划 + RL 文献标准术语 |
| 标签生成方式 | oracle-supervised | oracle 监督（首次出现括注"由规划器解提供真值标签"） | self-supervised / 自监督 | 自造复合词，N3P 原文用 offline data collection；规划器充当 oracle |
| 逐步预测 | sequential subgoal prediction | 逐步子目标预测 | autoregressive rolling prediction / 自回归滚动预测 | AI 造词"滚动预测"撞 MPC 专名，禁用 |
| 环境抽象 | environment abstraction | 环境抽象 | — | N3P 原文术语，保留 |

## 规划算法术语

| 术语 | 正式英文 | 正式中文 | 禁止用法 | 来源/说明 |
|------|----------|----------|----------|-----------|
| 混合A* | Hybrid A* | Hybrid A*（中文行文可写"混合 A*"） | 混合A星算法（冗余） | Dolgov et al., IJRR 2010 |
| RS 曲线 | Reeds-Shepp curve | Reeds-Shepp 曲线 | 芦苇谢普曲线 | Reeds & Shepp, 1990 Pacific J. Math. |
| 解析扩展 | analytic expansion | 解析扩展 | 解析延伸 / 分析性扩展 | Dolgov 2010 标准术语 |
| 节点扩展 | node expansion | 节点扩展 | 节点展开 | A* 搜索算法标准术语 |
| 回退 | fallback | 回退（分级回退 = fallback hierarchy） | 降级策略 | ROS2 行为树用"回退节点"，本文用"分级回退" |
| 运动基元 | motion primitive | 运动基元 | 运动原语 / 动作原语 | ICRA/pedestrian planning 标准术语；"基元"比"原语"更通用 |
| 运动基元剪枝 | motion primitive pruning | 运动基元剪枝 | action pruning（RL 专用） / 动作空间剪枝 | E³MoP, MeshA*；描述效果时用 branching factor reduction |
| 学习型运动基元选择 | learned motion primitive selection | 学习型运动基元选择 | learned action selection（RL 专用） / learned branching（无文献） | ICRA/IROS 多篇使用，motion planning 语境首选 |
| 学习型解析扩展 | learned analytic expansion | 学习型解析扩展 | neural RS / 神经 RS（非标准） | 基于 Dolgov 2010 "analytic expansion" 自然衍生 |
| 学习型局部规划器 | learned local planner | 学习型局部规划器 | neural path connector / neural local steering（无 top-venue 记录） | IROS 2020; kinodynamic 文献用 learned goal-reaching controller |
| RS 可对接域 | RS-connectable region | RS 可对接域（首次出现括注"存在无碰撞 Reeds-Shepp 曲线可直接连接目标的状态集合"） | reachable set / 可达域（与 reachability analysis 传统定义冲突）；goal region（笼统，丢失"RS 可连接"这一具体判据） | module2-ppo-analytic-expansion-design.md 项目内定义，是学习型转向 policy 的成功判据/训练 reward 核心项，非既有文献术语 |
| 闭环转向策略 | closed-loop steering policy | 闭环转向策略 | 生成式转向模型 / open-loop steering generator（与逐步观测-动作闭环机制矛盾） | module2 设计文档区分"闭环 policy（每步观测→动作→重新观测）"与"开环生成模型"；呼应 Sivaramakrishnan et al. 2021(arXiv:2110.04238)/Chiang et al. 2019(arXiv:1907.04799) 的闭环 controller/policy 范式 |
| 分支因子 | branching factor | 分支因子 | 分叉因子 / 分枝数 | AI/搜索算法教科书标准译法 |

## 环境与车辆术语

| 术语 | 正式英文 | 正式中文 | 禁止用法 | 来源/说明 |
|------|----------|----------|----------|-----------|
| 占据栅格图 | occupancy grid map | 占据栅格图（先验→"先验占据栅格图"） | 占据网格 / 占据地图 | Elfes, 1989 IEEE；"栅格"比"网格"更标准 |
| SE(2) | SE(2) | SE(2)（首次出现括注"特殊欧氏群"） | SE2（缺括号） | 数学符号保留，无标准中文替代 |
| 阿克曼转向 | Ackermann steering | 阿克曼转向 | 阿卡曼 | 汽车工程标准译名 |
| 最小转弯半径 | minimum turning radius | 最小转弯半径 | 最小转向半径 | "转弯"比"转向"更通用 |
| 运动学可行性 | kinematic feasibility | 运动学可行性 / 满足运动学约束 | 动力学可行性 | kinematic ≠ dynamic；运动学不含力 |
| 无碰撞 | collision-free | 无碰撞 | 无碰（过于简略） | 规划文献标准 |
| 碰撞检测 | collision checking / detection | 碰撞检测 | 碰撞检查（工程口语） | 学术文献用"检测"更规范 |
| 双圆近似 | dual-circle approximation | 双圆近似（首次出现说明"车体足迹近似"） | 双圆模型 | 描述性术语，非正式标准名；指用两个圆覆盖车体足迹 |
| 中轴 | medial axis | 中轴 | 中轴线（冗余） | 计算几何标准术语 |
| Voronoi 图 | Voronoi diagram | Voronoi 图 | 维诺图 / 泰森多边形 | 路径规划文献统一用法；"泰森多边形"是 GIS 专用 |

## 特征与学习术语

| 术语 | 正式英文 | 正式中文 | 禁止用法 | 来源/说明 |
|------|----------|----------|----------|-----------|
| 射线投射距离剖面 | ray-cast clearance profile | 射线投射距离剖面 | 净空轮廓 / LiDAR 轮廓 | ~~"净空"是航空术语~~；这是先验图上的几何查询，与传感器无关 |
| 安全裕量 | clearance | 安全裕量（指路径到障碍的最小距离） | 净空（航空专用） | 路径规划语境用"安全裕量"或"安全间距" |
| Z 分数标准化 | z-score normalization | Z 分数标准化 | 零均值归一化 | scikit-learn/Paddle 中文文档统一 |
| KD 树 | k-d tree | KD 树 | — | 正式论文中 k-d tree 带连字符 |
| KNN | k-nearest neighbors | K 近邻 | — | 机器学习标准术语 |

## 实验设计与统计术语

| 术语 | 正式英文 | 正式中文 | 禁止用法 | 来源/说明 |
|------|----------|----------|----------|-----------|
| 研究假设 | hypothesis | 研究假设（H₀ = 零假设，H₁ = 备择假设） | 假说（偏生物学） | 统计学教材通用 |
| 实验预注册 | pre-registration | 实验预注册（首次出现括注 pre-registration） | Research Contract（项目内术语，对外禁用） | AsPredicted/OSF 中文文档 |
| 成功判据 / 失败判据 | success criterion / failure criterion | 成功判据 / 失败判据 | 成功信号 / 失败信号（偏工程电信） | 项目内可用 signal，论文中用 criterion |
| 基线算法 | baseline | 基线算法 / 基线方法 | 基准（偏性能测试 benchmark） | 中文 ML/规划论文高频用法；baseline ≠ benchmark |
| 消融实验 | ablation study | 消融实验 | 控制变量实验（语义不等价） | 中文计算机论文高度共识 |
| 中位数 | median | 中位数 | 中间值 | 统计学教材 |
| 第 95 百分位数 | P95 / 95th percentile | 第 95 百分位数（工程场景可缩写 P95） | — | 统计学教材 |
| 百分点 | percentage point (pp) | 百分点 | "提升 2%"（当实际从 60% 升到 62% 时应说"提升 2 百分点"） | 统计/经济学教材；% 和 pp 不可混用 |
| 分布外 | out-of-distribution (OOD) | 分布外（首次出现括注 OOD） | 域外 / 超分布 | 智源社区、中文 ML 论文统一用法；OOD ≠ distribution shift |
| 备用规划器 | fallback planner | 备用规划器（路径规划语境）/ 回退（一般语境） | 降级策略（偏系统工程） | 路径规划场景"备用规划器"更精确 |
| Wilcoxon 符号秩检验 | Wilcoxon signed-rank test | Wilcoxon 符号秩检验 | 威尔科克森（音译几乎不见于正式论文） | JMP 中文文档、统计教材 |
| 自举置信区间 | Bootstrap confidence interval | 自举置信区间（首次出现括注 Bootstrap CI） | 引导程序（机翻误用） | 统计学学术规范；"自助法"偶见，"自举"更通行 |
| p 值 | p-value | p 值（小写斜体 p） | P 值（大写非规范） | 统计学教材无争议 |
| 预实验 | pilot experiment | 预实验 | 先导实验（偏医学） | 中文科研方法文献 |
| 技术预研 | engineering spike | 技术预研 | 探针 / spike（直接用英文对中文读者不友好） | 敏捷开发社区（知乎/CSDN） |
| 随机种子 | random seed | 随机种子 | 种子（不完整） | 深度学习复现文献 |
| 合理性验证 | sanity check | 合理性验证（或保留英文 sanity check） | 健全性检查（机翻） | 无固定中文译法，建议括注英文 |

## 高危黑话速查（论文/文档中一旦写出立即修正）

| 一旦写出 | 改为 | 错误性质 |
|----------|------|----------|
| 随机森林（指场景） | 程序化生成森林 | 撞 random forest 分类器名 |
| 激光雷达/LiDAR（指特征） | 射线投射距离剖面 | 无传感器环节，事实错误 |
| 净空轮廓 | 射线投射距离剖面 | "净空"是航空术语，路径规划不用 |
| 检索增强/RAG | KNN(k=1) 回归 | 机制描述错误 |
| 滚动预测/自回归滚动 | 逐步子目标预测 | 撞 MPC 专名 / AI 造词 |
| waypoint（指我方输出） | SE(2) 子目标 | subgoal/waypoint/preparatory pose 三分 |
| Dubins 曲线 | Reeds-Shepp 曲线 | Dubins 不含倒车，另一种曲线 |
| Waypoints Hybrid A* | Waypoints Hybrid B* | Bonetti 原文算法名（核验附注） |
| 概率完备 | 完备性（继承 vanilla 级别） | 概率完备是 sampling planner 专义 |
| 语义特征/嵌入/表征 | 手工特征 | 无语义模块 |
| 首次……（五类） | 删除，改具体差异陈述 | 查重报告五禁 |
| 占据图（缺"栅格"） | 占据栅格图 | 术语不完整 |
| 无碰（缺"撞"） | 无碰撞 | 过于简略 |
| 碰撞检查 | 碰撞检测 | 工程口语，学术不规范 |
| action pruning（规划语境） | motion primitive pruning / 运动基元剪枝 | action pruning 是 RL 术语，不用于搜索式规划 |
| neural RS / 神经 RS | learned analytic expansion / 学习型解析扩展 | 自造术语，无文献依据 |
| 运动原语 | 运动基元 | "基元"比"原语"更通用 |
| learned branching | learned motion primitive selection | 无 top-venue 使用记录 |
