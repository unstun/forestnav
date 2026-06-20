---
origin: human
reviewed: false
---

# 文档置信度矩阵

## origin 字段

| 值 | 含义 | 信任等级 |
|----|------|----------|
| `human` | Dr Sun 手动撰写或核验 | 高 |
| `ai+web` | AI 撰写，附有可追溯外部来源（URL/DOI/CitationKey） | 中 |
| `ai+local` | AI 基于项目内部文件撰写 | 中低 |
| `ai_only` | AI 纯凭训练知识撰写，无外部来源 | 低 |

## reviewed 字段

| 值 | 含义 |
|----|------|
| `true` | Dr Sun 已审阅确认 |
| `false` | 未经 Dr Sun 审阅 |

## 引用规则

| origin | reviewed | 可用场景 |
|--------|----------|----------|
| human | true | 可作为决策依据、论文 claim 依据 |
| ai+web | true | 可作为决策依据，论文引用须核查原文 |
| ai+web | false | 可作为检索线索，不可作为决策/论文依据 |
| ai+local | false | 仅供内部参考 |
| ai_only | false | 仅供检索线索，高概率幻觉 |
