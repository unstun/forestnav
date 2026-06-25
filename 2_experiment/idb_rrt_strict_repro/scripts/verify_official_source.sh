#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
DYNOPLAN_DIR="${DYNOPLAN_ROOT:-${ROOT_DIR}/upstream/dynoplan}"
EXPECTED_COMMIT="${DYNOPLAN_COMMIT:-dc938a2ac7d6a699781e0bd80370f15b74b8b0eb}"

if [[ ! -d "${DYNOPLAN_DIR}/.git" ]]; then
  echo "Dynoplan repository not found: ${DYNOPLAN_DIR}" >&2
  exit 1
fi

ACTUAL_COMMIT="$(git -C "${DYNOPLAN_DIR}" rev-parse HEAD)"
if [[ "${ACTUAL_COMMIT}" != "${EXPECTED_COMMIT}" ]]; then
  echo "Unexpected Dynoplan commit: ${ACTUAL_COMMIT}" >&2
  echo "Expected: ${EXPECTED_COMMIT}" >&2
  exit 1
fi

test -f "${DYNOPLAN_DIR}/README.md"
test -f "${DYNOPLAN_DIR}/dynobench/models/car1_v0.yaml"
test -f "${DYNOPLAN_DIR}/dynobench/envs/car1_v0/parallelpark_0.yaml"

if [[ ! -f "${DYNOPLAN_DIR}/dynomotions/car1_v0_all.bin.sp.bin.small5000.msgpack" ]] \
  && [[ ! -f "${DYNOPLAN_DIR}/dynobench/envs/car1_v0/motions/car1_v0_all.bin.sp.bin.small.msgpack" ]]; then
  echo "No official car1_v0 motion primitive bundle found." >&2
  exit 1
fi

grep -q "iDb-A\\*" "${DYNOPLAN_DIR}/README.md"
grep -q "dynamics: car_with_trailers" "${DYNOPLAN_DIR}/dynobench/models/car1_v0.yaml"

echo "Dynoplan source verified: ${DYNOPLAN_DIR}"
echo "Commit: ${ACTUAL_COMMIT}"
