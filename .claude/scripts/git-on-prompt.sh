#!/usr/bin/env bash
# ============================================================
# UserPromptSubmit hook  --  git 状态按需注入
# ------------------------------------------------------------
# 触发条件 : 用户 prompt 中含 git 相关关键词
# 目的     : 避免每次 session 无脑灌 git 信息 (context 污染)
# 对照     : 原 SessionStart hook 无条件注入 git
# ============================================================
set -euo pipefail

# ------------------------------------------------------------
# 读 stdin  --  Claude Code UserPromptSubmit 注入的 JSON
# ------------------------------------------------------------
INPUT=$(cat)

# ------------------------------------------------------------
# 提取 prompt 字段
#   兼容常见别名避免踩坑
#   用管道传 stdin,不用 here-string(避免受限 /tmp 环境写临时文件失败)
# ------------------------------------------------------------
PROMPT=$(printf '%s' "$INPUT" | python3 -c "
import json, sys
try:
    d = json.loads(sys.stdin.read())
    print(d.get('prompt') or d.get('user_prompt') or d.get('message') or '')
except Exception:
    pass
" 2>/dev/null || echo "")

# ------------------------------------------------------------
# 关键词匹配  --  中英混合,覆盖 git 常见操作
# 取舍: 漏匹配(AI 拿不到 git 上下文)比过度匹配(多一段快照)影响更大
# TODO: 给 git/commit/reset/tag 加词边界,避免误触 digital/commitment
# ------------------------------------------------------------
KEYWORDS='git|commit|push|pull|merge|rebase|stash|checkout|branch|blame|revert|diff|status|tag|reset|提交|推送|拉取|合并|切分支|分支|冲突|回滚|版本'

if echo "$PROMPT" | grep -qiE "$KEYWORDS"; then
  if [ -d .git ]; then
    echo "=== Git (auto-injected on git-keyword) ==="
    git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "(no branch)"
    git log --oneline -5 2>/dev/null || echo "(no commits)"
    git status --short 2>/dev/null || true
  fi
fi

exit 0
