---
name: memory-retrieval
version: 4.0.0
description: |-
  按需记忆检索。AI 判断需要项目历史上下文时主动调用，不自动触发。
  调用时将具体查询意图作为 args 传入，委派 memory-retriever agent 执行定向检索。
argument-hint: "[具体查询意图 — 针对当前问题的定向 query]"
user-invocable: true
---

# memory-retrieval

由 CLAUDE.md 硬规则 #5 指引。AI 判断需要项目历史上下文时**主动调用**，不做会话开头的无条件触发。

## 执行方式

**MUST：用 Agent tool 委派，不要自己执行检索。**

```
Agent({
  description: "Memory retrieval for session",
  subagent_type: "memory-retriever",
  prompt: "查询意图: $ARGUMENTS\n项目路径: /Users/sun/tongbu/study/phdproject/ForestNav"
})
```

## 何时调用

当 AI 发现自己需要以下信息时主动调用,query 须针对具体问题:
- 之前的实验决策或配置
- pipeline 知识库中的调研结论
- 未关闭的研究决策
- Dr Sun 明确要求回忆/检索时

## 意图提取示例

| 当前需要 | 传给 agent 的查询意图 |
|---|---|
| 继续之前的实验 | "最近实验进展、未完成任务、实验配置" |
| 写论文某节 | "§4.5 消融实验结果、CNN-DQN vs CNN-DDQN 数据" |
| 调研背景 | "待读文献、文献库状态、近期调研" |

## 回退

如果 memory-retriever agent 失败或超时，主 AI 直接读取热区三个文件：
- `bigmemory/热区/状态简报.md`
- `bigmemory/热区/未关闭决策.md`
- `bigmemory/热区/近期改动.md`

## 约束

- 纯只读，不修改任何文件
- 返回结果 <= 800 字
