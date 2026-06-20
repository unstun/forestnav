#!/usr/bin/env bash
# ============================================================================
# Stop AutoDL instance (releases GPU; storage persists at ~free cost).
#
# Usage: bash .claude/scripts/autodl-stop.sh
# ============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/autodl-api.sh"

status="$(autodl_instance_status)"
echo "Current status: $status"

case "$status" in
  shutdown|stopped)
    echo "Already stopped. No action."
    exit 0
    ;;
  stopping)
    echo "Already stopping."
    exit 0
    ;;
  running|starting)
    echo "Powering off..."
    resp="$(autodl_power_off)"
    code="$(echo "$resp" | jq -r '.code // "no-code"' 2>/dev/null || echo "parse-fail")"
    if [[ "$code" != "Success" ]]; then
      echo "FAIL: power_off returned code=$code" >&2
      echo "Raw response: $resp" >&2
      exit 1
    fi
    echo "OK: power_off accepted"
    echo "GPU billing stops within seconds. Storage continues at low cost."
    ;;
  *)
    echo "Unhandled status: $status" >&2
    exit 1
    ;;
esac
