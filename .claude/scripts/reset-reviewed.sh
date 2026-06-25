#!/usr/bin/env bash
# reviewed reset helper: AI 编辑试点目录内 reviewed:true 的文档后重置为 false
# 可由支持 hook 的客户端调用；Claude Code 无项目级 hook 时手动传文件路径。
# 试点目录: .pipeline/survey/, .pipeline/contracts/, .pipeline/experiments/,
#           bigmemory/冷区/调研记录/
set -euo pipefail

reset_one() {
  local file_path="$1"

  # ---- 白名单：只处理试点目录 ----
  # README.md 为模板文件，不纳入置信度管理（见 .pipeline/survey/document-confidence.md）
  case "$file_path" in
    */README.md|README.md)
      return 0
      ;;
    .pipeline/survey/*.md|*/.pipeline/survey/*.md|\
    .pipeline/contracts/*.md|*/.pipeline/contracts/*.md|\
    .pipeline/experiments/*.md|*/.pipeline/experiments/*.md|\
    bigmemory/冷区/调研记录/*.md|*/bigmemory/冷区/调研记录/*.md)
      ;;
    *)
      return 0
      ;;
  esac

  # ---- 检测并重置 reviewed: true ----
  python3 - "$file_path" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
if not path.exists():
    raise SystemExit(0)

text = path.read_text(encoding="utf-8")
if not text.startswith("---\n"):
    raise SystemExit(0)

parts = text.split("---\n", 2)
if len(parts) < 3:
    raise SystemExit(0)

frontmatter = parts[1]
body = parts[2]
if "reviewed: true" not in frontmatter:
    raise SystemExit(0)

frontmatter = frontmatter.replace("reviewed: true", "reviewed: false", 1)
path.write_text(f"---\n{frontmatter}---\n{body}", encoding="utf-8")
PY
}

if [ "$#" -gt 0 ]; then
  for file_path in "$@"; do
    reset_one "$file_path"
  done
  exit 0
fi

payload="$(cat)"
if [ -z "$payload" ]; then
  echo "用法: bash .claude/scripts/reset-reviewed.sh <file> [file...]" >&2
  exit 2
fi

file_path="$(printf '%s' "$payload" | python3 -c 'import json,sys; d=json.load(sys.stdin); print((d.get("tool_input") or {}).get("file_path",""))')"
reset_one "$file_path"
