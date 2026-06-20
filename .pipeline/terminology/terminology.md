---
origin: ai+web
reviewed: false
updated: 2026-06-20
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
