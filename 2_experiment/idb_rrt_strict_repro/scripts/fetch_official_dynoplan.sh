#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
UPSTREAM_DIR="${ROOT_DIR}/upstream"
DYNOPLAN_DIR="${UPSTREAM_DIR}/dynoplan"

REPO_URL="${DYNOPLAN_REPO_URL:-https://github.com/quimortiz/dynoplan.git}"
COMMIT="${DYNOPLAN_COMMIT:-dc938a2ac7d6a699781e0bd80370f15b74b8b0eb}"

mkdir -p "${UPSTREAM_DIR}"

if [[ ! -d "${DYNOPLAN_DIR}/.git" ]]; then
  git clone "${REPO_URL}" "${DYNOPLAN_DIR}"
fi

git -C "${DYNOPLAN_DIR}" config url.https://github.com/.insteadOf git@github.com:
git -C "${DYNOPLAN_DIR}" fetch origin "${COMMIT}"
git -C "${DYNOPLAN_DIR}" checkout --detach "${COMMIT}"
git -C "${DYNOPLAN_DIR}" config submodule.dynobench.url https://github.com/quimortiz/dynobench.git
git -C "${DYNOPLAN_DIR}" config submodule.dynomotions.url https://github.com/quimortiz/dynomotions.git
git -C "${DYNOPLAN_DIR}" submodule update --init --recursive

echo "Dynoplan source ready: ${DYNOPLAN_DIR}"
git -C "${DYNOPLAN_DIR}" rev-parse HEAD
