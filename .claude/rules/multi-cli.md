---
paths: [".pipeline/survey/multi-ai-workflow.md", "**/*codex*", "**/*gemini*", "**/*rescue*", "**/*delegate*"]
---

# 多 CLI 协作

Claude Code 主会话负责统筹；Codex 通过官方插件 `openai/codex-plugin-cc` 接入（指令 `/codex:rescue`、子 agent `codex:codex-rescue`），走 app-server JSON-RPC 协议，自动继承 AGENTS.md；Gemini CLI（skill `gemini-do`）负责长上下文分析。
审查用 `/codex:review` 或 `/codex:adversarial-review`（Codex 侧）、`gemini-review`（Gemini 侧）、`dual-review`（两者并行交叉）。
任务外派用 `/delegate`（B 模式：spawn `codex:codex-rescue` 子 agent 后台执行）或 `/delegate-offline`（A 模式：生成 prompt 供独立终端运行 `codex` CLI）。
详见 `.pipeline/survey/multi-ai-workflow.md`。
