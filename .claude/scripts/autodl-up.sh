#!/usr/bin/env bash
# ============================================================================
# AutoDL 4090 同步：Mac → 远端（上传）
# 用法：bash .claude/scripts/autodl-up.sh <相对路径>     [--dry-run]
#       bash .claude/scripts/autodl-up.sh 0_trials/2026-05-24/
#       bash .claude/scripts/autodl-up.sh 2_experiment/configs/dqfd_smoke.json
# ============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/autodl-ssh.sh"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <project-relative-path> [rsync-extra-opts...]" >&2
  echo "  e.g.  $0 0_trials/2026-05-24/" >&2
  echo "  e.g.  $0 2_experiment/configs/foo.json --dry-run" >&2
  exit 1
fi

REL_PATH="${1#/}"  # 剥前缀 /
shift || true
EXTRA_OPTS=("$@")

LOCAL_FULL="${LOCAL_PROJECT}/${REL_PATH%/}"
REMOTE_PARENT="$(dirname "${REL_PATH%/}")"
REMOTE_FULL="${AUTODL_PROJECT}/${REMOTE_PARENT}/"

if [[ ! -e "$LOCAL_FULL" ]]; then
  echo "ERR: 本地不存在 $LOCAL_FULL" >&2
  exit 1
fi

# 确保远端父目录存在
autodl_run "mkdir -p $REMOTE_FULL"

echo "↑ Mac → 4090"
echo "  src: $LOCAL_FULL"
echo "  dst: ${AUTODL_USER}@${AUTODL_HOST}:${REMOTE_FULL}"

# --update：远端文件较新时跳过（双向同步关键）
# --partial：断点续传
# -avz：archive + verbose + compress
sshpass -e rsync -avz --update --partial --progress \
  -e "ssh -p $AUTODL_PORT -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR" \
  ${EXTRA_OPTS[@]+"${EXTRA_OPTS[@]}"} \
  "$LOCAL_FULL" \
  "${AUTODL_USER}@${AUTODL_HOST}:${REMOTE_FULL}"
