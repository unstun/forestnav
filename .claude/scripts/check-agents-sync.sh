#!/usr/bin/env bash
# ============================================================================
# check-agents-sync.sh — 校验 CLAUDE.md 通过 @AGENTS.md 引用 AGENTS.md(硬规则 #15)
# ----------------------------------------------------------------------------
# 设计:AGENTS.md 是内容真源,CLAUDE.md 是 Claude Code 入口 thin wrapper。
# Claude Code 启动 / /compact 后会自动展开 @AGENTS.md import 注入 context。
# ============================================================================
set -euo pipefail

A="CLAUDE.md"
B="AGENTS.md"

if [ ! -f "$A" ] || [ ! -f "$B" ]; then
  echo "❌ 缺少 $A 或 $B" >&2
  exit 2
fi

if [ ! -s "$B" ]; then
  echo "❌ $B 为空(应为内容真源)" >&2
  exit 2
fi

IMPORT_LINES=$(grep -c '^@AGENTS\.md$' "$A" || true)
if [ "$IMPORT_LINES" -ne 1 ]; then
  echo "❌ $A 应含且仅含一行独立的 \`@AGENTS.md\` 引用,实际匹配:$IMPORT_LINES" >&2
  echo "   修复: 在 $A 中放一行 '@AGENTS.md'(顶格,前后空行)" >&2
  exit 2
fi

echo "✅ CLAUDE.md → @AGENTS.md → AGENTS.md 引用正确"
exit 0
