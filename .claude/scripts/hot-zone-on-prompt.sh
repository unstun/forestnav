#!/usr/bin/env bash
# ============================================================
# UserPromptSubmit hook  --  热区新鲜度按需注入
# ------------------------------------------------------------
# 触发条件 : 用户 prompt 中含"上下文/进度/状态/记忆"类关键词
# 目的     : 迁出 SessionStart,避免每次会话启动都注入
#            (硬规则 #2 注意事项 Context Is All You Need)
# 对照     : 原 session-start-lite.sh 无条件注入热区检查
# ============================================================
set -euo pipefail

# ------------------------------------------------------------
# 读 stdin  --  Claude Code UserPromptSubmit 注入的 JSON
# 用管道传 stdin,不用 here-string(避免受限 /tmp 环境写临时文件失败)
# ------------------------------------------------------------
INPUT=$(cat)

PROMPT=$(printf '%s' "$INPUT" | python3 -c "
import json, sys
try:
    d = json.loads(sys.stdin.read())
    print(d.get('prompt') or d.get('user_prompt') or d.get('message') or '')
except Exception:
    pass
" 2>/dev/null || echo "")

# ------------------------------------------------------------
# 关键词匹配  --  中英混合,严格对齐硬规则 #5 白名单 A
# 设计: 优先覆盖白名单 A 的显式词,去掉偏宽词(项目/status/context)
#       避免与 git-on-prompt 的 status 关键词重合导致 context 双注入
# ------------------------------------------------------------
KEYWORDS='进度|现在|未关闭|上次|昨天|最近|记忆|历史|做到哪|到哪了|之前|前几天|待办|没做完|回忆|翻一下|状态怎样|检索|还有什么|还有哪些|recall|memory|progress'

if ! echo "$PROMPT" | grep -qiE "$KEYWORDS"; then
  exit 0
fi

# ------------------------------------------------------------
# 热区新鲜度检查  --  超过 24h 未更新则提醒 /archive
# ------------------------------------------------------------
STALE_HOURS=24
HOT_FILES=(
  "bigmemory/热区/状态简报.md"
  "bigmemory/热区/未关闭决策.md"
  "bigmemory/热区/近期改动.md"
)

mtime_epoch() {
  if stat -f %m "$1" >/dev/null 2>&1; then
    stat -f %m "$1"
  else
    stat -c %Y "$1"
  fi
}

now=$(date +%s)
stale_found=false
declare -a STALE_LINES=()

for f in "${HOT_FILES[@]}"; do
  if [ ! -f "$f" ]; then
    STALE_LINES+=("⚠ 热区缺失: $f")
    stale_found=true
    continue
  fi
  mtime=$(mtime_epoch "$f")
  age_hours=$(( (now - mtime) / 3600 ))
  if [ "$age_hours" -ge "$STALE_HOURS" ]; then
    STALE_LINES+=("⚠ 热区过期: $f (${age_hours}h 未更新)")
    stale_found=true
  fi
done

# ------------------------------------------------------------
# 输出策略  --  热区新鲜则静默不注入,节约 context
# 只有过期/缺失时输出, 并明确边界避免被当作记忆检索替代品
# ------------------------------------------------------------
if [ "$stale_found" = true ]; then
  # ------------------------------------------------------------
  # 边界声明用 echo 而非 here-doc
  # Why: 受限 /tmp 环境不允许创建临时文件, here-doc 会报
  #      "cannot create temp file for here document" 并触发
  #      set -euo pipefail 提前退出
  # ------------------------------------------------------------
  echo "=== 热区新鲜度提示 (auto-injected on memory-keyword) ==="
  echo "【注意】本提示仅 mtime 检查, 不是记忆检索结果"
  echo "命中硬规则 #5 白名单时仍必须调用 memory-retrieval skill 做定向检索"
  for line in "${STALE_LINES[@]}"; do
    echo "$line"
  done
  echo "建议: 运行 /archive 刷新热区"
fi

exit 0
