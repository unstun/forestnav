---
name: dual-review
description: Codex + Gemini 双重审核 Claude 的改动，交叉比较后综合输出
version: "2.0"
user-invocable: true
---

# 双重审核

同时调用 Codex（官方插件 `openai/codex-plugin-cc`）和 Gemini CLI（`gemini-3.1-pro-preview`）审核 Claude 的改动，利用两个模型的正交视角互补盲点。

## v2.0 变更

- Codex 调用从自写 `codex exec` 切换到官方 `codex:codex-rescue` 子 agent
- 子 agent 走 app-server JSON-RPC 协议，自动加载 AGENTS.md（硬规则 + 术语），无需手工塞 prompt
- 子 agent 在独立 context 中执行，主会话只接收摘要，token 成本显著下降

## 执行步骤

### 1. 收集上下文

```bash
DIFF=$(git diff HEAD)
[ -z "$DIFF" ] && DIFF=$(git diff HEAD~1)
```

从会话上下文里提炼 Claude 做这些改动的理由（prompt 要原样同时发给两个 AI，保证公平比较）。

### 2. 并行调用两个 AI

**必须在同一个 message 里同时发出两个工具调用**：

- **Agent 工具**（Codex 侧）：
  - `subagent_type`: `codex:codex-rescue`
  - `description`: ≤6 字任务名，例如 "审核 X 改动"
  - `prompt`: 完整审核上下文 = diff + 改动理由 + 要审核的维度（正确性 / 安全 / 风格 / 遗漏）
- **Bash 工具**（Gemini 侧）：
  - `(echo "<同一份审核 prompt>") | gemini -m gemini-3.1-pro-preview -p "审核以上 AI 改动" 2>&1`

两边 prompt 必须逐字相同。

### 3. 综合两份审核

收到两份结果后，Claude 自己做综合：

```
## 审核综合报告

### Codex（官方插件 / gpt-5.4）发现
{Codex 的审核要点}

### Gemini（3.1 Pro Preview）发现
{Gemini 的审核要点}

### 交叉分析
- 两者一致的问题：{列出}（高置信度，应修复）
- 仅 Codex 发现：{列出}（通常偏代码细节）
- 仅 Gemini 发现：{列出}（通常偏架构 / 文档 / 长链路）

### 建议行动
{按优先级排列的修复建议}
```

### 4. 展示并等待指令

将综合报告展示给 Dr Sun，询问是否需要修复。

## 注意

- 双重审核消耗两倍 token，只对重要改动用
- Gemini 429 降级链：`gemini-3.1-pro-preview` → `gemini-2.5-pro` → Flash
- 如需单独跑 Codex 审核（不走本 skill），Dr Sun 可直接在 Claude Code 里发 `/codex:review` 或 `/codex:adversarial-review`
