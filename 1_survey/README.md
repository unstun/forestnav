# 文献库索引

490 篇论文（`papers/paper_list.csv`），530+ 篇 Markdown 全文（`papers/md/`）。

## 按研究路线导航

### 路线 A：Learned Heuristic

核心文献（6 篇全文中文翻译）：`learned-heuristic-key-papers/`

| 论文 | 方法 | 与 ForestNav 的关系 |
|------|------|-------------------|
| Veerapaneni2023Learning (LoHA*) | 局部残差启发函数 + focal search | 最直接的基础，需解决 wall-clock 瓶颈 |
| Veerapaneni2024DataEfficient (DE-LoHA*) | 数据高效收集 + 在线学习 | backward A* 标注策略可复用 |
| Hadar2026Beyond (LHBL) | 多步搜索标签训练 | 标签设计参考 |
| Yang2025PACHS | RL + 并行搜索推断 | actor-critic 训练框架参考 |
| Bokan2024SLOPE | 最优路径距离剪枝 | 替代目标函数参考 |
| Menon2026TSEASL | 时序自适应 lattice | 非完整约束实时重规划参考 |

可视化笔记：`learned-heuristic-notes.html`

相关 paper_list 标签：`L_learning_path_optimization`(49)、`E_bounded_suboptimal_search`(10)

### 路线 B：N3P 系列

无独立翻译子目录。核心参考论文在 `papers/md/` 中：

| 论文 | 与 ForestNav 的关系 |
|------|-------------------|
| N3P 原文（arXiv:2605.22722） | 环境抽象 + 子目标分解的原始框架 |
| Jurgenson2019SubGoal | 子目标发现参考 |
| Tang2018Subgoal | 子目标规划参考 |
| Bao2025Hybrid / Naik2025Hybrid | Hybrid A* 变体参考 |

相关 paper_list 标签：`G_subgoal_optimization`(32)、`F_hybrid_astar`(19)、
`I_corridor_planning`(38)、`O_dense_forest_narrow_passage`(44)、`J_homotopy_topology`(39)

### 共用

相关 paper_list 标签：`P_nonholonomic_constraints`(10)、`K_dubins_reeds_shepp`(8)

## 工具

- `scripts/search_papers.py` — 论文搜索
- `scripts/batch_convert.py` — arXiv 批量转 Markdown
- `scripts/batch_mineru_vlm.py` — MinerU VLM PDF 转 Markdown
