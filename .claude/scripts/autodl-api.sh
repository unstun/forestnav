#!/usr/bin/env bash
# ============================================================================
# AutoDL OpenAPI helper (Legacy / non-Pro instance family)
#
# Endpoints verified via autodl-keeper (https://github.com/turbo-duck/autodl-keeper)
# and official docs (https://www.autodl.com/docs/instance_pro_api,
# https://www.autodl.com/docs/save_money/, https://www.autodl.com/docs/common_api).
#
# Token: AutoDL console -> 账号 -> 设置 -> 开发者Token
#   (https://www.autodl.com/console/center/settings/token)
#
# Why legacy not Pro: instance UUID does not start with `pro-`; host pattern
#   `connect.bjb2.seetacloud.com` matches the non-Pro family.
# ============================================================================

set -euo pipefail

# ---- Endpoints (legacy / non-Pro family) ------------------------------------
export AUTODL_BASE="https://www.autodl.com"
export AUTODL_POWER_ON="${AUTODL_BASE}/api/v1/instance/power_on"
export AUTODL_POWER_OFF="${AUTODL_BASE}/api/v1/instance/power_off"
export AUTODL_INSTANCE_LIST="${AUTODL_BASE}/api/v1/instance"

# ---- Token + Instance UUID load --------------------------------------------
# Token from ~/.ssh/autodl_4090_token (chmod 600)
# UUID  from ~/.ssh/autodl_4090_uuid  (chmod 600)
if [[ -z "${AUTODL_TOKEN:-}" ]]; then
  if [[ -f "$HOME/.ssh/autodl_4090_token" ]]; then
    export AUTODL_TOKEN="$(cat "$HOME/.ssh/autodl_4090_token")"
  else
    echo "ERR: AUTODL_TOKEN not set and ~/.ssh/autodl_4090_token missing" >&2
    echo "解决：登录 https://www.autodl.com/console/center/settings/token" >&2
    echo "      复制开发者 Token 写入 ~/.ssh/autodl_4090_token (chmod 600)" >&2
    return 1 2>/dev/null || exit 1
  fi
fi

if [[ -z "${AUTODL_UUID:-}" ]]; then
  if [[ -f "$HOME/.ssh/autodl_4090_uuid" ]]; then
    export AUTODL_UUID="$(cat "$HOME/.ssh/autodl_4090_uuid")"
  else
    echo "ERR: AUTODL_UUID not set and ~/.ssh/autodl_4090_uuid missing" >&2
    echo "解决：从 AutoDL 控制台 -> 容器实例页 -> 实例详情读取 UUID" >&2
    echo "      写入 ~/.ssh/autodl_4090_uuid (chmod 600)" >&2
    return 1 2>/dev/null || exit 1
  fi
fi

# ---- API call wrapper --------------------------------------------------------
autodl_api_call() {
  # Args: <method> <url> [json_body]
  local method="$1"
  local url="$2"
  local body="${3:-}"
  local curl_args=(
    -sS -X "$method"
    -H "Authorization: ${AUTODL_TOKEN}"
    -H "Content-Type: application/json;charset=UTF-8"
    --connect-timeout 10
    --max-time 30
  )
  if [[ -n "$body" ]]; then
    curl_args+=(-d "$body")
  fi
  curl "${curl_args[@]}" "$url"
}

# ---- Convenience: power on / off / status -----------------------------------
autodl_power_on() {
  # $1: "gpu" (default) or "non_gpu" (cheap mode)
  local payload="${1:-gpu}"
  local body
  body=$(printf '{"instance_uuid":"%s","payload":"%s","start_command":"sleep 1"}' \
                "$AUTODL_UUID" "$payload")
  autodl_api_call POST "$AUTODL_POWER_ON" "$body"
}

autodl_power_off() {
  local body
  body=$(printf '{"instance_uuid":"%s"}' "$AUTODL_UUID")
  autodl_api_call POST "$AUTODL_POWER_OFF" "$body"
}

autodl_list_instances() {
  # Returns all instances. Filter with jq on caller side.
  local body='{"date_from":"","date_to":"","page_index":1,"page_size":100,"status":[],"charge_type":[]}'
  autodl_api_call POST "$AUTODL_INSTANCE_LIST" "$body"
}

# ---- Get instance status (running / shutdown / ...) -------------------------
autodl_instance_status() {
  # Returns one of: running / shutdown / starting / stopping / unknown
  local resp
  resp="$(autodl_list_instances)"
  # Find our UUID in the response, extract `status`
  local status
  status="$(echo "$resp" | jq -r --arg u "$AUTODL_UUID" \
            '.data.list[] | select(.uuid == $u) | .status' 2>/dev/null || true)"
  if [[ -z "$status" || "$status" == "null" ]]; then
    echo "unknown"
  else
    echo "$status"
  fi
}

# ---- Get SSH endpoint (proxy host + port) -----------------------------------
# Returns "host:port" or "unknown:unknown" if not extractable.
autodl_ssh_endpoint() {
  local resp
  resp="$(autodl_list_instances)"
  local host port
  host="$(echo "$resp" | jq -r --arg u "$AUTODL_UUID" \
          '.data.list[] | select(.uuid == $u) | .proxy_host // .ssh_command // ""' 2>/dev/null || true)"
  port="$(echo "$resp" | jq -r --arg u "$AUTODL_UUID" \
          '.data.list[] | select(.uuid == $u) | .ssh_port // .proxy_port // ""' 2>/dev/null || true)"
  # Fallback: parse from ssh_command if structured fields are missing
  if [[ -z "$host" || "$host" == "null" || -z "$port" || "$port" == "null" ]]; then
    local cmd
    cmd="$(echo "$resp" | jq -r --arg u "$AUTODL_UUID" \
           '.data.list[] | select(.uuid == $u) | .ssh_command // ""' 2>/dev/null || true)"
    # ssh -p 13413 root@connect.bjb2.seetacloud.com -> extract port and host
    if [[ "$cmd" =~ -p[[:space:]]+([0-9]+)[[:space:]]+[a-z]+@([a-zA-Z0-9.-]+) ]]; then
      port="${BASH_REMATCH[1]}"
      host="${BASH_REMATCH[2]}"
    fi
  fi
  if [[ -z "$host" || "$host" == "null" ]]; then host="unknown"; fi
  if [[ -z "$port" || "$port" == "null" ]]; then port="unknown"; fi
  echo "${host}:${port}"
}
