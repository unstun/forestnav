#!/usr/bin/env bash
# ============================================================================
# Wake AutoDL instance (full GPU mode by default; --no-gpu = cheap mode).
#
# Usage:
#   bash .claude/scripts/autodl-start.sh           # GPU mode (full price)
#   bash .claude/scripts/autodl-start.sh --no-gpu  # 无卡模式 (~¥0.1/h, no GPU)
#   bash .claude/scripts/autodl-start.sh --wait    # GPU + poll until SSH ready
# ============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/autodl-api.sh"

MODE="gpu"
WAIT_SSH=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-gpu) MODE="non_gpu"; shift ;;
    --wait)   WAIT_SSH=true; shift ;;
    -h|--help)
      grep '^#' "$0" | head -20
      exit 0
      ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

status="$(autodl_instance_status)"
echo "Current status: $status"

case "$status" in
  running)
    echo "Already running. No action."
    exit 0
    ;;
  starting)
    echo "Instance is already starting. Wait ~60s."
    ;;
  shutdown|stopped|unknown)
    echo "Powering on (mode=$MODE)..."
    resp="$(autodl_power_on "$MODE")"
    code="$(echo "$resp" | jq -r '.code // "no-code"' 2>/dev/null || echo "parse-fail")"
    if [[ "$code" != "Success" ]]; then
      echo "FAIL: power_on returned code=$code" >&2
      echo "Raw response: $resp" >&2
      exit 1
    fi
    echo "OK: power_on accepted (code=Success)"
    ;;
  *)
    echo "Unhandled status: $status" >&2
    exit 1
    ;;
esac

# Optional: poll until SSH is responsive
if [[ "$WAIT_SSH" == "true" ]]; then
  echo "Polling SSH endpoint..."
  for i in $(seq 1 12); do
    sleep 10
    endpoint="$(autodl_ssh_endpoint)"
    host="${endpoint%:*}"; port="${endpoint##*:}"
    if [[ "$host" == "unknown" || "$port" == "unknown" ]]; then
      echo "  [$((i*10))s] endpoint not yet exposed in instance list"
      continue
    fi
    if timeout 5 bash -c "</dev/tcp/${host}/${port}" 2>/dev/null; then
      echo "  [$((i*10))s] TCP OK on ${host}:${port}"
      echo "Endpoint: ssh -p $port root@$host"
      # Compare against cached endpoint
      if [[ -f "$HOME/.ssh/autodl_4090_endpoint" ]]; then
        cached="$(cat "$HOME/.ssh/autodl_4090_endpoint")"
        if [[ "$cached" != "${host}:${port}" ]]; then
          echo "WARN: endpoint changed from $cached to ${host}:${port}"
          echo "      update .claude/scripts/autodl-ssh.sh AUTODL_HOST/PORT or"
          echo "      cache via:  echo '${host}:${port}' > ~/.ssh/autodl_4090_endpoint"
        fi
      else
        echo "  cache endpoint: echo '${host}:${port}' > ~/.ssh/autodl_4090_endpoint"
      fi
      exit 0
    else
      echo "  [$((i*10))s] TCP not yet up"
    fi
  done
  echo "WARN: SSH not responsive within 120s, instance may need longer" >&2
  exit 1
fi

echo "Use --wait to poll until SSH is ready, or check via:"
echo "  bash .claude/scripts/autodl-status.sh"
