#!/usr/bin/env bash
# ============================================================================
# AutoDL 4090 服务器 SSH 助手（共享配置）
# 用法：source 本文件取得 ssh / scp / rsync 一致配置
# ============================================================================

set -euo pipefail

export AUTODL_HOST="connect.bjb2.seetacloud.com"
export AUTODL_PORT="13413"
export AUTODL_USER="root"
export AUTODL_PROJECT="/root/autodl-tmp/ForestNav"
export LOCAL_PROJECT="/Users/sun/tongbu/study/phdproject/ForestNav"

# 密码加载顺序：环境变量 SSHPASS > ~/.ssh/autodl_4090_pass
if [[ -z "${SSHPASS:-}" ]]; then
  if [[ -f "$HOME/.ssh/autodl_4090_pass" ]]; then
    export SSHPASS="$(cat "$HOME/.ssh/autodl_4090_pass")"
  else
    echo "ERR: SSHPASS 未设置且 ~/.ssh/autodl_4090_pass 不存在" >&2
    echo "解决：echo '<password>' > ~/.ssh/autodl_4090_pass && chmod 600 ~/.ssh/autodl_4090_pass" >&2
    return 1 2>/dev/null || exit 1
  fi
fi

# 单命令远端执行：autodl_run "<cmd>"
# ssh -o 参数直接传递，避免字符串 quoting 问题
autodl_run() {
  sshpass -e ssh \
    -p "$AUTODL_PORT" \
    -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null \
    -o LogLevel=ERROR \
    "${AUTODL_USER}@${AUTODL_HOST}" "$@"
}

# 远端进入 conda env 跑命令：autodl_conda "<cmd>"
autodl_conda() {
  autodl_run "source /root/miniconda3/etc/profile.d/conda.sh && conda activate ros2py310 && cd $AUTODL_PROJECT/2_experiment && $*"
}
