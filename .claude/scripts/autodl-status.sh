#!/usr/bin/env bash
# ============================================================================
# Show current AutoDL instance state + SSH endpoint + cost mode.
# Usage: bash .claude/scripts/autodl-status.sh
# ============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/autodl-api.sh"

status="$(autodl_instance_status)"
endpoint="$(autodl_ssh_endpoint)"

echo "AutoDL instance ${AUTODL_UUID:0:12}..."
echo "  status   : $status"
echo "  endpoint : $endpoint"

case "$status" in
  running)
    echo "  hint     : alive — try \`source .claude/scripts/autodl-ssh.sh && autodl_run 'hostname'\`"
    ;;
  shutdown)
    echo "  hint     : stopped — wake with \`bash .claude/scripts/autodl-start.sh\` (gpu) or \`--no-gpu\` (cheap mode)"
    ;;
  starting|stopping)
    echo "  hint     : in transition — wait ~60s and re-run status"
    ;;
  *)
    echo "  hint     : unknown state — check AutoDL web console"
    ;;
esac
