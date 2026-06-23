# ForestNav 主线任务清单

> Codex 执行指引：读取本文件，找到第一个状态为 `[ ]` 的任务，执行它，
> 完成后将其状态改为 `[x]` 并在"完成记录"处追加一行日期+摘要，然后 git commit。
> 每次只做一个任务。遇到标记 `需人工确认` 的任务，完成后停下等 Dr Sun 审阅。
>
> 预注册文件：`.pipeline/contracts/v9-forest-n3p.md`（status: approved）
> 设计文档：`2_experiment/v9_forest_n3p/design.md`
> 术语规范：`.pipeline/terminology/terminology.md`

---

## 阶段 0：技术预研

### T01 项目结构搭建
- [x] **目标**：在 `2_experiment/` 下建立 F-N3P 的代码结构
- **具体步骤**：
  1. 创建 `2_experiment/forest_n3p/` 目录
  2. 从 DQN10 复制需要的模块：`maps/forest.py`（森林生成）、`third_party/pathplan`（Hybrid A* 规划器）、`forest_policy.py`（双圆碰撞+前向仿真）、`maps/pgm.py`（真实地图加载）
  3. 创建 `configs/` 目录，写一个 `default.json` 配置文件，包含所有参数（L_max=8, L_min=1.5, N_seg=2000, R_max=10, n_ray=32 等）
  4. 创建 `__init__.py`、`README.md`
  5. 验证 `import pathplan` 能正常工作
- **产出**：可运行的项目骨架
- **验收**：`python -c "from forest_n3p import configs; print('OK')"` 通过

### T02 RS 独立接口验证
- [x] **目标**：确认 pathplan 是否暴露独立的 RS 曲线生成 + 碰撞检测接口
- **具体步骤**：
  1. 阅读 `third_party/pathplan` 的 API，找 RS 相关函数
  2. 写一个测试脚本 `tests/test_rs_interface.py`：给定两个 SE(2) 位姿，生成 RS 曲线，检测是否无碰撞
  3. 如果没有独立接口，写一个 wrapper `rs_utils.py` 封装所需功能
  4. 测试：在一张简单地图上验证 RS 曲线生成 + 碰撞检测结果正确
- **产出**：`rs_utils.py`（如需要）+ 测试脚本
- **验收**：测试脚本通过，能独立调用 RS 生成和碰撞检测

### T03 特征提取实现
- [x] **目标**：实现 41 维手工特征提取
- **具体步骤**：
  1. 创建 `features.py`
  2. 实现射线投射距离剖面（32 维）：从当前位姿向 32 个方向发射射线，记录到最近障碍的距离，取 log(1+d)
  3. 实现目标相对量（5 维）：log 距离 + sin/cos 方位角 + sin/cos 朝向差
  4. 实现密度统计（3 维）：三个环带内占据栅格比例
  5. 实现运动学标志（1 维）：v1 固定为 0
  6. 写可视化脚本：在地图上画出射线和特征值，确认正确性
- **产出**：`features.py` + 可视化验证图
- **验收**：在 3 张不同密度的地图上可视化，射线方向和距离值与目视一致
- **参考**：设计文档 §4.3 特征设计表

### T04 标签提取实现（算法 1）
- [x] **目标**：实现前向贪心 RS 可达分段
- **具体步骤**：
  1. 创建 `labeling.py`
  2. 实现算法 1：输入一条教师路径（弧长参数化），输出子目标序列和样本对
  3. 关键逻辑：从当前子目标出发，沿路径找最远的 RS 无碰撞可达点
  4. 失败处理：推进距离 < L_min 时丢弃整条路径
  5. 输出样本对：(41 维特征, 车体系相对位姿 Δ)
  6. 写测试：在 1 张地图上用 Hybrid A* 求解 → 传入标签提取 → 可视化子目标序列
- **产出**：`labeling.py` + 测试可视化
- **验收**：可视化确认子目标点沿路径分布合理，相邻子目标间 RS 可达
- **参考**：设计文档 §4.2 算法 1 伪代码
- **依赖**：T02（RS 接口）、T03（特征提取）

### T05 标签预实验
- [x] **目标**：在小规模数据上验证标签管线质量
- **需人工确认**
- **具体步骤**：
  1. 生成 20 张程序化森林地图（低/中/高密度各若干）
  2. 每张图跑 10 个随机查询的原版 Hybrid A*
  3. 对成功路径跑标签提取
  4. 统计并报告：
     - 教师求解成功率（按密度分）
     - 标签提取成功率（多少路径被 L_min 规则丢弃）
     - 每条路径平均段数
     - 段长分布（min/mean/max）
     - 总样本数
  5. 输出到 `.pipeline/experiments/` 目录
- **产出**：预实验报告 + 统计数据
- **验收**：标签失败率 < 20%（否则需调整 L_min/L_max）
- **依赖**：T04

### T06 难度轴标定
- [x] **目标**：确定 Easy/Complex/Extreme 的密度切点
- **需人工确认**
- **具体步骤**：
  1. 在多种树密度下（从稀疏到密集，至少 8 个密度级）批量跑原版 Hybrid A*
  2. 记录每个密度级的：求解时间分布、成功率、节点扩展数
  3. 找到密度阈值：
     - Easy: 原版 HA* 基本秒解
     - Complex: 原版 HA* 明显变慢但还能解
     - Extreme: 原版 HA* 经常超时
  4. 对起终距离做类似分析
  5. 输出切点数值，写入预注册补充
- **产出**：难度标定报告 + 切点数值
- **验收**：三个桶的原版 HA* 性能有明显区分度
- **依赖**：T01

### T07 RealMap 资产清点
- [x] **目标**：确认可用的真实 SLAM 地图
- **具体步骤**：
  1. 找到 DQN10 中的 RealMap 资产路径
  2. 检查格式兼容性（pgm/yaml）
  3. 用 `maps/pgm.py` 加载测试
  4. 记录可用地图数量、尺寸、分辨率
  5. 复制到 ForestNav 仓库
- **产出**：可用地图清单 + 已复制的地图文件
- **验收**：至少 2 张真实地图能正确加载和显示

---

## 阶段 1：主实验

### T08 大规模数据采集
- [x] **目标**：生成训练数据集
- **具体步骤**：
  1. 生成 ~2000 张程序化森林地图（覆盖全部难度桶）
  2. 每张图随机生成多个起终点查询
  3. 批量跑原版 Hybrid A*，保存成功路径 + 搜索元数据
  4. 对所有成功路径跑标签提取
  5. 特征化所有样本 → 保存为 numpy 数组
  6. 记录数据集统计：总样本数、各桶分布、标签失败率
- **产出**：训练数据集 + 统计报告
- **验收**：总样本数 ~10^5 量级，各桶有充足覆盖
- **依赖**：T05 预实验通过

### T09 KNN 库构建 + 在线推理实现
- [x] **目标**：构建 KNN 样本库 + 实现在线推理循环（算法 2）
- **具体步骤**：
  1. Z 分数标准化训练集特征
  2. 用 scipy/sklearn 构建 KD 树
  3. 实现算法 2（在线逐步推理）：`inference.py`
     - 停止判据：RS 可直达终点
     - KNN 预测 → 可行性校验 → 段内 HA* → 循环
     - 三级回退：F1 近邻重试 / F2 段内 HA* / F3 整题回退
     - 无进展哨：到终点距离连续 2 步不降
  4. 在 5 个查询上手动验证推理结果
- **产出**：`inference.py` + KNN 库文件 + 验证可视化
- **验收**：5 个查询中至少 4 个产出无碰撞可行路径
- **参考**：设计文档 §4.5 算法 2 伪代码

### T10 MLP 训练（消融用）
- [x] **目标**：训练 MLP 模型作为 KNN 的消融对照
- **具体步骤**：
  1. 4 层全连接网络，输入 41 维，输出 3 维（Δx, Δy, Δθ）
  2. L2 损失，Adam 优化器
  3. 训练/验证分割
  4. 保存模型 checkpoint
  5. 接入 inference.py（替换 KNN 查询部分）
- **产出**：MLP checkpoint + 训练日志
- **依赖**：T08

### T11 基线实现：Voronoi waypoint HA*
- [x] **目标**：实现规则分解基线
- **具体步骤**：
  1. 用 scipy.spatial.Voronoi 或 skimage.morphology.medial_axis 提取骨架
  2. 在骨架上放置 waypoint（间距类似 L_max）
  3. 用段内 HA* 连接相邻 waypoint
  4. 计时口径与主方法一致
- **产出**：`baselines/voronoi_waypoint.py`
- **验收**：在 10 个查询上能产出路径

### T12 基线实现：瓶颈规则 waypoint
- [x] **目标**：实现"证明学习必要性"的基线
- **具体步骤**：
  1. 用中轴变换找窄道位置
  2. 在窄道中心放 waypoint
  3. 段内 HA* 连接
- **产出**：`baselines/bottleneck_waypoint.py`
- **验收**：在 10 个查询上能产出路径

### T13 评测框架
- [x] **目标**：统一的评测脚本，计算全部 9 个指标
- **具体步骤**：
  1. 创建 `evaluation.py`
  2. 实现全部指标计算：T, E, SR, 路径膨胀率, 方向切换, 最小安全裕量, 碰撞违例, 回退触发率, 子目标可达率
  3. 计时协议：单线程、全部开销计入
  4. 输出格式：CSV + 按桶汇总表
  5. 统计检验：Wilcoxon + Bootstrap CI
- **产出**：`evaluation.py`
- **依赖**：T09

### T14 主评测
- [x] **目标**：全基线 × 全难度桶 × 多种子评测
- **需人工确认**
- **具体步骤**：
  1. 方法列表：F-N3P(KNN), 原版 HA*, N3P 式 K=1, Voronoi waypoint, 瓶颈 waypoint, MD-DQN
  2. 难度桶：按 T06 标定结果
  3. 每桶 >= 100 查询，>= 5 随机种子
  4. 跑评测脚本 → 输出 CSV
  5. 按预注册判定成功/失败
- **产出**：主评测 CSV + 判定报告
- **验收**：碰撞违例全为 0；数据完整无缺失
- **依赖**：T09, T11, T12, T13

### T15 消融实验
- [x] **目标**：8 组消融实验
- **需人工确认**
- **具体步骤**：按消融矩阵（见 plan-overview.html）逐组执行
  - A1 标签规则 / A2 KNN vs MLP / A3 k 值 / A4 特征组
  - A5 段长 / A6 序列策略 / A7 回退阶梯 / A8 鲁棒性
- **产出**：消融实验 CSV + 分析
- **依赖**：T14 基础设施

### T16 泛化测试
- [x] **目标**：分布外密度桶 + 真实 SLAM 地图
- **需人工确认**
- **具体步骤**：
  1. 在训练分布外的密度上评测
  2. 在真实 SLAM 地图上评测
  3. 按预注册失败判据 ② ④ 判定
- **产出**：泛化测试 CSV
- **依赖**：T09, T07

---

## 阶段 2：写作

### T17 论文 Method 节
- [x] 基于实验代码和设计文档，撰写 3_paper/main.tex 的 Method 节
- **依赖**：T09 完成

### T18 论文 Results 节
- [x] 基于 T14/T15/T16 的 CSV 数据，撰写 Results 节
- **需人工确认**
- **依赖**：T14, T15, T16

### T19 论文其余节
- [x] Introduction, Related Work, Conclusion, Abstract
- **依赖**：T17, T18

### T20 图表制作
- [x] 路径对比可视化、子目标序列图、消融柱状图等
- **依赖**：T14 数据

### T21 引用核查
- [x] 所有引用走四步核查流程，BibTeX 从 DOI 获取
- **依赖**：T19

---

## 完成记录

| 日期 | 任务 | 摘要 |
|------|------|------|
| 2026-06-20 | 预注册 | 数字锁定，Contract v1 approved |
| 2026-06-20 | T01 项目结构搭建 | 建立 `2_experiment/forest_n3p/` 骨架，迁入 DQN10 森林地图、PGM 加载、pathplan 和 forest_policy，新增默认配置与 import 兼容入口；`import pathplan` 与 `from forest_n3p import configs` 验证通过 |
| 2026-06-20 | T02 RS 独立接口验证 | 新增 `forest_n3p.rs_utils`，封装 RS 曲线生成、曲线采样和 GridFootprintChecker 碰撞检测；新增 `tests/test_rs_interface.py`，验证自由空间可通行和障碍阻断可检测 |
| 2026-06-20 | T03 特征提取实现 | 新增 `forest_n3p.features`，实现 41 维 ray-cast clearance profile、目标相对量、环带密度和运动学标志；新增 `tests/test_features.py` 与 `forest_n3p.scripts.visualize_features`，生成 3 张不同密度森林可视化图并完成目视验收 |
| 2026-06-20 | T04 标签提取实现 | 新增 `forest_n3p.labeling`，实现前向贪心 Reeds-Shepp 无碰撞可达分段、车体系相对位姿标签和 41 维特征样本输出；新增 `tests/test_labeling.py` 与 `forest_n3p.scripts.visualize_labeling`，用 Hybrid A* 教师路径生成并可视化 3 个 SE(2) 子目标 |
| 2026-06-20 | T05 标签预实验 | 新增 `forest_n3p.pilot_labeling` 与 `run_label_pilot`，在 `gpu3070ti-relay` 跑 20 张程序化森林地图 × 10 查询；默认 `L_min=1.5m` 标签失败率 23.6%，据失败原因降为 `L_min=1.0m` 后失败率 16.2%，报告与 CSV 写入 `.pipeline/experiments/20260620_t05_label_pilot_lmin1p0/`，需 Dr Sun 人工确认参数是否进入后续正式实验 |
| 2026-06-20 | T06 难度轴标定 | 新增 `forest_n3p.difficulty_calibration` 与 `run_difficulty_calibration`，在 `gpu3070ti-relay` 用原版 Hybrid A* 跑 8 个密度级共 120 个查询、距离轴 90 个查询；按轴向单调切点得到密度 Easy≤55 trees / Complex=70 trees / Extreme≥85 trees，距离 Easy<12m / Complex=12–20m / Extreme≥20m，报告、CSV、`summary.json` 与预注册补充草案写入 `.pipeline/experiments/20260620_t06_difficulty_calibration/` 和 `.pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md`，需 Dr Sun 人工确认后才能作为后续正式桶依据 |
| 2026-06-20 | T07 RealMap 资产清点 | 新增 ROS PGM/YAML loader 与 `forest_n3p.scripts.realmap_inventory`；确认 DQN10 的 20 个 `realmap_a` NPZ 快照只有 1 个唯一数组哈希，复制 DQN9 原始 `map_a.pgm/yaml` 为 `dqn_realmap_a`，补入 BSD 许可 TurtleBot Willow Garage ROS 地图 `willow_garage_0p10`；两张地图均通过 `maps/pgm.py` 加载、起终点 known-free 校验与预览图生成，manifest 写入 `2_experiment/forest_n3p/assets/realmaps/manifest.json` |
| 2026-06-20 | T08 大规模数据采集 | 新增 `forest_n3p.training_data` 与 `run_training_data_collection`，复用真实程序化森林生成、原版 Hybrid A* teacher、T04 RS 标签提取与 41 维特征管线；在 `gpu3070ti-relay` 跑 2000 张地图 × 40 查询，生成 100,531 个训练样本，Easy/Complex/Extreme 分别 37,386 / 34,183 / 28,962，标签失败率 6.8%，`acceptance_pass=true`；数据集写入 `2_experiment/forest_n3p/datasets/t08_training_dataset/`，报告写入 `.pipeline/experiments/20260620_t08_training_dataset.md` |
| 2026-06-20 | T09 KNN 库构建 + 在线推理实现 | 新增 `forest_n3p.inference`、`build_knn_library` 和 `verify_inference`，对 T08 的 100,531×41 特征做 Z 分数标准化并构建 scikit-learn `KDTree` KNN 库；实现算法 2 在线循环、F1 近邻重试、F2 段内 Hybrid A*、F3 整题回退与无进展哨；5 个未见查询验收 `feasible_count=5/5`、碰撞复核全通过，KNN 库写入 `2_experiment/forest_n3p/models/t09_knn_library/`，报告和可视化写入 `.pipeline/experiments/20260620_t09_inference_verification/` |
| 2026-06-20 | T10 MLP 训练（消融用） | 新增 `forest_n3p.mlp` 与 `train_mlp`，训练 4 个 Linear 层的 MLP 消融模型（41→256→256→128→3，109,827 参数），使用 PyTorch `MSELoss` + Adam、90/10 train/val split 和 train-split Z 分数标准化；在 `gpu3070ti-relay` 的 RTX 3070 Ti 上训练，best_epoch=31、normalized val MSE=0.4016、val RMSE dx/dy/dtheta=1.352m/0.666m/0.181rad；checkpoint 与训练日志写入 `2_experiment/forest_n3p/models/t10_mlp_subgoal/`，训练报告写入 `.pipeline/experiments/20260620_t10_mlp_training.md`，MLP 接入在线推理 5-query smoke `feasible_count=5/5` |
| 2026-06-20 | T11 基线实现：Voronoi waypoint HA* | 新增 `forest_n3p.baselines.voronoi_waypoint` 与 `verify_voronoi_waypoint`，用 EDT 安全裕量过滤后的中轴构建规则 waypoint 图，按 6m 间距放置 waypoint，并复用段内 Hybrid A* 逐段连接；10 个未见查询验收 `feasible_count=10/10`、碰撞复核全通过、平均 waypoint 数 2.6，正式报告与可视化写入 `.pipeline/experiments/20260620_t11_voronoi_waypoint_verification/` |
| 2026-06-20 | T12 基线实现：瓶颈规则 waypoint | 新增 `forest_n3p.baselines.bottleneck_waypoint` 与 `verify_bottleneck_waypoint`，沿安全中轴路径读取 EDT 安全裕量，用 `find_peaks(-clearance)` 选择局部低谷作为瓶颈 waypoint，并在超长 skeleton 区间取最窄点作段长守卫；10 个未见查询验收 `feasible_count=10/10`、碰撞复核全通过、平均 waypoint 数 2.8，正式报告与可视化写入 `.pipeline/experiments/20260620_t12_bottleneck_waypoint_verification/` |
| 2026-06-20 | T13 评测框架 | 新增 `forest_n3p.evaluation` 与 `verify_evaluation_framework`，统一 `EvaluationRun`/`EvaluationRecord`，计算 T/E/SR（基于无碰可行路径）/路径膨胀/方向切换/最小安全裕量/碰撞违例/fallback 触发率/子目标可达率，支持按 method+difficulty bucket 汇总 CSV/JSON、逐查询 Wilcoxon 与 Bootstrap SR CI；合成验证生成 8 条记录并写入 `.pipeline/experiments/20260620_t13_evaluation_framework_verification/`，全测试 40/40 通过 |
| 2026-06-23 | T14 主评测 | Dr Sun 确认先采用放大验证切点 `validation_t06` 推进整体框架；在 `gpu3070ti-relay` 重跑 6 方法 × Easy/Complex/Extreme × 5 seeds 主评测，生成 300 queries / 1800 records，`formal_acceptance=true`、`status=formal_pass`、方法异常 0、碰撞违例 0；Complex/Extreme Contract gate 均通过，产物写入 `.pipeline/experiments/20260621_t14_formal_6method_rs_k20_collisionguard_validation_t06/` |
| 2026-06-23 | T15 消融实验 | 新增 T15 消融框架与 runner，覆盖 A1-A8 变体登记；在 `gpu3070ti-relay` 按框架规模运行 30 个变体，其中 25 个真实运行、5 个明确登记为需后续重切标签/重提特征，生成 90 行 `ablation_summary.csv`、30 行 manifest、25 个子报告，exit=0、stderr 为空、碰撞违例 0；产物写入 `.pipeline/experiments/20260623_t15_ablation_framework_validation_t06/`，该结果用于论文框架和趋势检查，不作为最终大样本结论 |
| 2026-06-23 | T16 泛化测试 | 新增 `forest_n3p.generalization` 与 `run_generalization_evaluation`，覆盖 OOD-Sparse/OOD-Dense 两个训练外密度桶和 T07 两张真实 SLAM 地图；本次框架规模运行 16 queries / 32 records，query seed 全唯一、方法异常 0、碰撞违例 0，判据② OOD 成功率跌幅通过，判据④ RealMap 20% 时间收益未通过；产物写入 `.pipeline/experiments/20260623_t16_generalization_framework_t06/`，需 Dr Sun 审阅后决定是否放大到论文最终规模 |
| 2026-06-23 | T17 论文 Method 节 | 新建 `3_paper/main.tex` 与 `3_paper/references.bib`，基于实验代码、T08/T09/T14/T16 记录和术语规范撰写 Method：定义 F-N3P 为 oracle-supervised subgoal decomposition，说明 41 维 map feature、RS 可达标签、KNN-KDTree 子目标预测与 F1/F2/F3 回退；核验 N3P、Hybrid A*、Reeds-Shepp 三条外部依据并完成 `pdflatex+bibtex+pdflatex+pdflatex` 编译；T16 仍按框架规模描述，未写成最终泛化结论 |
| 2026-06-23 | T18 论文 Results 节 | 基于 T14 正式主评测、T15 消融框架和 T16 泛化框架 CSV/JSON 撰写 `3_paper/main.tex` 的 Results and Discussion：新增主评测表、Contract gate 表、消融框架快照表、泛化框架快照表；明确 T14 支持 Complex/Extreme gate 通过，T15 仅作为趋势，T16 RealMap 20% 时间收益未通过且不能写成最终泛化成功；临时目录完成 `pdflatex+bibtex+pdflatex+pdflatex` 编译，引用与交叉引用通过 |
| 2026-06-23 | T19 论文其余节 | 补写 `3_paper/main.tex` 的 Abstract、Introduction、Related Work 和 Conclusion，围绕 Hybrid A* 搜索负担、N3P preparatory-pose 思路到森林 sequential subgoal prediction 的转化、roadmap/waypoint 基线和 learning-assisted planning 定位展开；补入 Bonetti2023Roadmap、Kavraki1996PRM、Wang2021LearningMotionPlanning、Sormoli2024HybridSurvey 四条 DOI/arXiv BibTeX 线索；保留 T16 RealMap 未通过 20% 时间收益的 limitation，未把引用全审冒充为完成；临时目录 `pdflatex+bibtex+pdflatex+pdflatex` 编译通过 |
| 2026-06-23 | T20 图表制作 | 新增可复现脚本 `3_paper/scripts/make_t20_figures.py`，从 T14/T15/T16 CSV/JSON 生成主评测柱状图、Extreme 消融柱状图、T16 泛化边界图，并重放 T14 Extreme query `extreme_s02_q0051` 生成路径对比和 F-N3P SE(2) 子目标序列图；产物写入 `3_paper/figures/t20_*.{pdf,png}` 与 `t20_manifest.json`，4 张图已接入 `3_paper/main.tex`，临时目录完整 LaTeX 编译通过；T15/T16 图均保持 framework-scale 边界，不写成最终结论 |
| 2026-06-23 | T21 引用核查 | 对 `3_paper/main.tex` 当前 7 个引用 key 全量执行四步核查：正文 key 与 BibTeX key 一致性检查、官方网页/arXiv 页面核验、`curl -H "Accept: application/x-bibtex" https://doi.org/<DOI>` 拉取 raw BibTeX、逐条 claim 支撑检查；审计报告、raw BibTeX 和 Crossref/arXiv 元数据写入 `.pipeline/experiments/20260623_t21_reference_audit/`；收紧 Wang2021 引用附近正文，避免把本文保守设计选择强行归因给 survey；临时目录 `pdflatex+bibtex+pdflatex+pdflatex` 编译通过，正文无缺失引用或未使用 BibTeX |
