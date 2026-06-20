#!/usr/bin/env bash
# ============================================================================
# AutoDL 4090 同步：远端 → Mac（下载）
# 用法：bash .claude/scripts/autodl-down.sh <相对路径>     [--dry-run]
#       bash .claude/scripts/autodl-down.sh 2_experiment/runs/dqfd_smoke_20260525/
# ============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/autodl-ssh.sh"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <project-relative-path> [rsync-extra-opts...]" >&2
  echo "  e.g.  $0 2_experiment/runs/" >&2
  echo "  e.g.  $0 0_trials/2026-05-24/ --dry-run" >&2
  exit 1
fi

REL_PATH="${1#/}"
shift || true
EXTRA_OPTS=("$@")

REMOTE_FULL="${AUTODL_PROJECT}/${REL_PATH%/}"
LOCAL_PARENT="$(dirname "${REL_PATH%/}")"
LOCAL_FULL="${LOCAL_PROJECT}/${LOCAL_PARENT}/"

# 确保本地父目录存在
mkdir -p "$LOCAL_FULL"

echo "↓ 4090 → Mac"
echo "  src: ${AUTODL_USER}@${AUTODL_HOST}:${REMOTE_FULL}"
echo "  dst: $LOCAL_FULL"

# --update：本地文件较新时跳过（双向同步关键）
sshpass -e rsync -avz --update --partial --progress \
  -e "ssh -p $AUTODL_PORT -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR" \
  ${EXTRA_OPTS[@]+"${EXTRA_OPTS[@]}"} \
  "${AUTODL_USER}@${AUTODL_HOST}:${REMOTE_FULL}" \
  "$LOCAL_FULL"
