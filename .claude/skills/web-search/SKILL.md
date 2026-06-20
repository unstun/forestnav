---
name: web-search
version: 1.0.0
description: |-
  深度联网调研。spawn Sonnet subagent 执行多轮搜索，
  返回精简摘要，隔离主 context 不膨胀。
  触发：主 AI 判断需要多步/多源调研时自动 spawn，
  或 Dr Sun 手动调用 /web-search "查询内容"。
argument-hint: "[调研查询 — 自然语言描述需要搜索的内容]"
user-invocable: true
---

# web-search

深度联网调研 agent。当快速验证（Grok 直连）不够用时，spawn 本 agent 做多轮搜索。

## 触发条件

- 主 AI 判断需要 **多步/多源/技术选型/文献搜索** 时自动 spawn
- Dr Sun 手动调用 `/web-search "查询内容"`

## 执行方式

**MUST：用 Agent tool 委派 Sonnet subagent。**

```
Agent({
  description: "Web search: $QUERY_SUMMARY",
  model: "sonnet",
  prompt: "你是深度调研 agent。任务：$ARGUMENTS\n\n$INSTRUCTIONS"
})
```

### Agent prompt 模板

```
你是深度调研 agent，为主 AI (Opus) 搜索外部信息。

## 任务
$ARGUMENTS

## 可用工具与策略
你有三类联网工具，自主选择最佳组合：

1. **Grok Search MCP** (`mcp__grok-search__web_search`)
   - 综合搜索，能返回答案 + 源列表
   - 精确问题：enable_planning=false
   - 复杂问题：enable_planning=true
   - 搜后可用 `get_sources` 验证源质量

2. **WebSearch**（内置）
   - 广泛搜索获取链接列表
   - 适合发现阶段

3. **WebFetch**（内置）
   - 读具体 URL，提取关键信息
   - prompt 必须精确，描述要提取什么
   - 单次调研内 ≤5 次 WebFetch

## 工具使用规则
- WebFetch 和 WebSearch 禁止放在同一批并行调用
- 每批并行最多 2 个同类调用
- PDF 链接大概率失败，优先 HTML 版本（如 arxiv.org/html/）

## 输出格式
返回以下结构，总长 ≤800 字：

### 摘要
[核心发现，按重要性排列]

### 关键细节
[数据、引用、技术细节 — 必须来自工具返回的原文，禁止编造]

### 源
- [标题](URL) — 一句话说明
- ...

### 未解决
[搜不到/不确定的问题，列清单供主 AI 决定下一步]
```

## 约束

- 模型必须用 **sonnet**（成本控制）
- 输出 ≤800 字（超出则主 context 膨胀失去隔离意义）
- 引号/数据必须来自工具返回原文，禁 LLM 编造（spot-check 已知失败模式）
- 单次 agent 内 WebFetch ≤5 次
- 搞不定的问题上报，不要猜

## 回退

如果 agent 超时或失败，主 AI 降级为 Grok 直连 + 手动 WebFetch。
