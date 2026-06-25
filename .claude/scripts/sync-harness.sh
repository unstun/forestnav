#!/usr/bin/env bash
# ============================================================================
# sync-harness.sh — Harness 完整性四项检查
# ----------------------------------------------------------------------------
# 检查项:
#   1. symlink 完整性: .factory/commands → .claude/commands
#                       .factory/skills  → .claude/skills
#   2. CLAUDE.md → @AGENTS.md → AGENTS.md 引用正确(硬规则 #15)
#   3. agents/droids 文件名覆盖: .claude/agents/ vs .factory/droids/
#      （跨 CLI 命名不一致的 agent 通过 CROSS_MAP 建立等价映射）
#   4. agents/droids 内容漂移: 正文(去 frontmatter)是否一致
#      （含 CROSS_MAP 映射对的正文比较；漂移计为失败）
# ----------------------------------------------------------------------------
# 用法: bash .claude/scripts/sync-harness.sh
# 返回: 全部通过 → exit 0; 有失败 → exit 2
# 兼容: macOS /bin/bash 3.2 与 GNU bash 4+（未使用关联数组）
# ============================================================================
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

FAIL=0

# ── 跨 CLI 命名映射 ────────────────────────────────────────────────────────
# Claude Code (.claude/agents/) 与 Factory AI (.factory/droids/) 对同一 agent
# 使用不同文件名时，在此登记映射对 "agent名:droid名"，空格分隔多个。
# 登记后：§3 不报"仅在 XX"；§4 按映射做正文比较。
CROSS_MAP_PAIRS="memory-retriever:memory-worker"

# agent 名 → droid 名（未映射则返回空字符串）
map_agent_to_droid() {
    local name="$1" pair a d
    for pair in $CROSS_MAP_PAIRS; do
        a="${pair%%:*}"
        d="${pair##*:}"
        if [ "$a" = "$name" ]; then
            printf '%s' "$d"
            return 0
        fi
    done
    return 1
}

# droid 名 → agent 名（未映射则返回空字符串）
map_droid_to_agent() {
    local name="$1" pair a d
    for pair in $CROSS_MAP_PAIRS; do
        a="${pair%%:*}"
        d="${pair##*:}"
        if [ "$d" = "$name" ]; then
            printf '%s' "$a"
            return 0
        fi
    done
    return 1
}

# ── 1. Symlink 完整性 ──────────────────────────────────────────────────────
check_symlink() {
    local link="$1" target="$2"
    if [ -L "$link" ]; then
        actual=$(readlink "$link")
        if [ "$actual" = "$target" ]; then
            echo "  ✅ $link → $target"
        else
            echo "  ❌ $link → $actual (期望 $target)" >&2
            FAIL=1
        fi
    else
        echo "  ❌ $link 不是 symlink" >&2
        FAIL=1
    fi
}

echo "== 1. Symlink 完整性 =="
check_symlink ".factory/commands" "../.claude/commands"
check_symlink ".factory/skills"   "../.claude/skills"

# ── 2. CLAUDE.md → @AGENTS.md → AGENTS.md ────────────────────────────────
echo "== 2. CLAUDE.md → @AGENTS.md → AGENTS.md =="
if [ ! -f "CLAUDE.md" ] || [ ! -f "AGENTS.md" ]; then
    echo "  ❌ 缺少 CLAUDE.md 或 AGENTS.md" >&2
    FAIL=1
elif [ ! -s "AGENTS.md" ]; then
    echo "  ❌ AGENTS.md 为空(应为内容真源)" >&2
    FAIL=1
else
    IMPORT_LINES=$(grep -c '^@AGENTS\.md$' "CLAUDE.md" || true)
    if [ "$IMPORT_LINES" -eq 1 ]; then
        echo "  ✅ CLAUDE.md → @AGENTS.md → AGENTS.md"
    else
        echo "  ❌ CLAUDE.md 应含且仅含一行独立的 \`@AGENTS.md\` 引用,实际匹配:$IMPORT_LINES" >&2
        FAIL=1
    fi
fi

echo "== 2b. Claude Code 项目级 settings =="
if [ -e ".claude/settings.json" ]; then
    echo "  ❌ .claude/settings.json 仍存在；本项目采用无项目 hook 模式" >&2
    FAIL=1
else
    echo "  ✅ 未保留 .claude/settings.json"
fi

# ── 3. agents/droids 文件名覆盖 ───────────────────────────────────────────
echo "== 3. agents/droids 覆盖 =="
AGENTS_DIR=".claude/agents"
DROIDS_DIR=".factory/droids"

if [ ! -d "$AGENTS_DIR" ] || [ ! -d "$DROIDS_DIR" ]; then
    echo "  ⚠️  $AGENTS_DIR 或 $DROIDS_DIR 不存在, 跳过" >&2
else
    agents=$(ls "$AGENTS_DIR"/*.md 2>/dev/null | xargs -I{} basename {} .md | sort)
    droids=$(ls "$DROIDS_DIR"/*.md 2>/dev/null | xargs -I{} basename {} .md | sort)

    only_agents=$(comm -23 <(echo "$agents") <(echo "$droids") || true)
    only_droids=$(comm -13 <(echo "$agents") <(echo "$droids") || true)

    # ── 按 CROSS_MAP 过滤：映射对两侧齐全不算"缺件" ──
    missing_a=""
    for name in $only_agents; do
        mapped=$(map_agent_to_droid "$name" || true)
        if [ -n "$mapped" ] && echo "$only_droids" | grep -qx "$mapped"; then
            continue
        fi
        missing_a="$missing_a $name"
    done

    missing_d=""
    for dname in $only_droids; do
        agent=$(map_droid_to_agent "$dname" || true)
        if [ -n "$agent" ] && echo "$only_agents" | grep -qx "$agent"; then
            continue
        fi
        missing_d="$missing_d $dname"
    done

    if [ -z "$missing_a" ] && [ -z "$missing_d" ]; then
        if [ -z "$only_agents" ] && [ -z "$only_droids" ]; then
            echo "  ✅ agents 与 droids 文件名完全覆盖"
        else
            echo "  ✅ agents 与 droids 覆盖（已应用 CROSS_MAP 跨名映射）"
        fi
    else
        [ -n "$missing_a" ] && echo "  ❌ .claude/agents/ 有但 .factory/droids/ 缺:${missing_a}" >&2
        [ -n "$missing_d" ] && echo "  ❌ .factory/droids/ 有但 .claude/agents/ 缺:${missing_d}" >&2
        FAIL=1
    fi
fi

# ── 4. agents/droids 内容漂移检测 ─────────────────────────────────────────
echo "== 4. agents/droids 内容漂移 =="
if [ -d "$AGENTS_DIR" ] && [ -d "$DROIDS_DIR" ]; then
    DRIFT=0
    for agent_file in "$AGENTS_DIR"/*.md; do
        name=$(basename "$agent_file" .md)
        droid_file="$DROIDS_DIR/$name.md"
        display_name="$name"
        # 同名不存在时，回退到 CROSS_MAP 映射
        if [ ! -f "$droid_file" ]; then
            mapped=$(map_agent_to_droid "$name" || true)
            [ -z "$mapped" ] && continue
            droid_file="$DROIDS_DIR/$mapped.md"
            [ -f "$droid_file" ] || continue
            display_name="$name → $mapped"
        fi

        # 剥除 YAML frontmatter(如有)后比较正文,忽略空行差异
        agent_body=$(awk 'NR==1&&/^---$/{s=1;next} s==1&&/^---$/{s=2;next} s!=1' "$agent_file" | sed '/^$/d')
        droid_body=$(awk 'NR==1&&/^---$/{s=1;next} s==1&&/^---$/{s=2;next} s!=1' "$droid_file" | sed '/^$/d')

        if [ "$agent_body" != "$droid_body" ]; then
            echo "  ⚠️  $display_name: agents 与 droids 正文不一致" >&2
            DRIFT=1
        fi
    done
    if [ "$DRIFT" -eq 0 ]; then
        echo "  ✅ agents 与 droids 正文一致"
    else
        FAIL=1
    fi
else
    echo "  ⚠️  跳过(目录不存在)"
fi

# ── 结果 ──────────────────────────────────────────────────────────────────
echo ""
if [ "$FAIL" -eq 0 ]; then
    echo "🟢 Harness 检查全部通过"
    exit 0
else
    echo "🔴 Harness 检查有失败项" >&2
    exit 2
fi
