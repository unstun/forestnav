# 调研文档索引

按研究路线分组，标注来源和可信度。

## 路线 A：Learned Heuristic（微调启发式）

在 HA* 现有启发函数上学习残差修正，加速搜索。

| 文档 | 内容 | origin | confidence |
|------|------|--------|------------|
| [learned-heuristic-for-search-planning.md](learned-heuristic-for-search-planning.md) | 6 篇核心论文综述 + ForestNav 启示分析 | ai+web | medium |

对应文献翻译：`1_survey/learned-heuristic-key-papers/`（6 篇全文中文翻译）

## 路线 B：N3P 系列（子目标分解）

将 N3P 的环境抽象思想迁移到森林，学习引导 HA* 搜索。

| 文档 | 内容 | origin | confidence |
|------|------|--------|------------|
| [fn3p-v2-architecture-design.md](fn3p-v2-architecture-design.md) | 方案 B1：瓶颈姿态预测 + 走廊约束 HA* | ai_only | low |
| [fn3p-v2-gate-constrained-ha.md](fn3p-v2-gate-constrained-ha.md) | 方案 B2：Gate 序列预测 + 全局 HA* | ai_only | low |
| [corridor-constrained-ha-architecture-review.md](corridor-constrained-ha-architecture-review.md) | GPT Pro 对走廊约束架构的审核意见（翻译） | ai+web | medium |
| [gptpro-env-abstraction-prompt.md](gptpro-env-abstraction-prompt.md) | 给 GPT Pro 的完整上下文包（prompt 存档） | human | — |

对应 Contract：`.pipeline/contracts/v9-forest-n3p.md`（status: approved）

## 通用

| 文档 | 内容 | origin | confidence |
|------|------|--------|------------|
| [dqn10-baseline-inventory.md](dqn10-baseline-inventory.md) | DQN10 可移植车式基线盘点 | ai_only | low |
| [document-confidence.md](document-confidence.md) | 文档置信度矩阵（origin/reviewed 规范） | human | — |

## 路线交叉点

两条路线不互斥，可能的组合方式：

- A 独立：learned residual heuristic for HA* in dense forests
- B1 独立：走廊约束 HA* + 学习瓶颈姿态
- B2 独立：gate-constrained HA* + 学习 gate 序列
- **A + B2**：gate-constrained HA* 的启发函数用 learned residual 实现
