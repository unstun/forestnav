#!/usr/bin/env bash
# ============================================================
# search reminder helper -- 搜索工具调用前注入策略提醒
# ------------------------------------------------------------
# 用法     : 可由支持 hook 的客户端调用；Claude Code 无项目级 hook 时手动查看
# 匹配     : WebSearch | WebFetch | mcp__grok-search__.*
# 目的     : AI 调搜索工具前就地提醒硬规则 #12 / gotchas,
#            防止(a) WebFetch/WebSearch 同批并行 403 级联
#                (b) 忘了走 Search Agent 隔离深度调研
#                (c) PDF 链接直抓导致解析失败
#                (d) 付费墙/403 页面浪费 token
# 对照     : 原方案是 search-strategy.md 全文常驻 (context 污染)
# ============================================================
set -euo pipefail

# ------------------------------------------------------------
# 极简提醒 (≤150 字)
#   完整策略见 .claude/rules/search-strategy.md (常驻精简版)
#   或 .claude/rules/search-strategy-full.md (按需加载全文)
# ------------------------------------------------------------
# 用 echo 而非 here-doc
# Why: 受限 /tmp 环境不允许 here-doc 创建临时文件,
#      set -euo pipefail 会提前退出
# ------------------------------------------------------------
echo "=== 搜索策略提醒 (auto on search-tool) ==="
echo "- 项目内信息 → ACE 语义检索优先 (mcp__auggie__codebase-retrieval)"
echo "- 快速验证 1-2 条事实 → grok web_search 直连 (enable_planning=false)"
echo "- 复杂问题 → grok web_search (enable_planning=true)"
echo "- 深度/多源调研 → spawn Search Agent (model=sonnet), 主会话只收 ≤800 字摘要"
echo "- 库/框架文档 → context7 MCP; JS 渲染页面 → Playwright (最后手段)"
echo "- WebFetch 与 WebSearch 禁同批并行 (403 级联), 各自独立批次, 每批 ≤2"
echo "- PDF 链接大概率失败 → 换 HTML (arxiv.org/html/ 或 ar5iv)"
echo "- 付费墙/403 → 列检索项交 Dr Sun 用 Super Grok 网页处理"
echo "- 禁凭记忆答专业问题; 引号必须来自 WebFetch 原文或 Grok 返回, 禁 LLM 编造"
echo "- 详细决策流 → .claude/rules/search-strategy.md"

exit 0
