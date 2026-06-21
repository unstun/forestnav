#!/usr/bin/env bash
set -euo pipefail

# Run on gpu3070ti-relay after:
# 1. Dr Sun resolves D-T14-09 using the T06 validation analysis.
# 2. Dr Sun approves D-T14-10/11.
# 3. T06 supplement is revised or explicitly approved, set to reviewed:true, and committed.
# 4. DENSITY_PROFILE_BUCKETS is set from D-T14-09:
#    - approve_original_with_justification -> original_t06
#    - revise_to_validation_cutpoints -> validation_t06
# 5. SOURCE_HEAD is set to that post-review commit hash.

SOURCE_HEAD="${SOURCE_HEAD:-POST_T06_REVIEW_HEAD}"
DENSITY_PROFILE_BUCKETS="${DENSITY_PROFILE_BUCKETS:-SET_BY_D_T14_09}"

if [[ "$SOURCE_HEAD" == "POST_T06_REVIEW_HEAD" ]]; then
  echo "ERROR: set SOURCE_HEAD to the post-review commit hash" >&2
  exit 2
fi

case "$DENSITY_PROFILE_BUCKETS" in
  original_t06|validation_t06)
    ;;
  *)
    echo "ERROR: set DENSITY_PROFILE_BUCKETS to original_t06 or validation_t06 according to D-T14-09" >&2
    exit 2
    ;;
esac

cd ~/ForestNav
source .venv/bin/activate

OUT=".pipeline/experiments/20260621_t14_formal_6method_rs_k20_collisionguard_${DENSITY_PROFILE_BUCKETS}"
LOG=".pipeline/experiments/logs/20260621_t14_formal_6method_rs_k20_collisionguard_${DENSITY_PROFILE_BUCKETS}"

mkdir -p "$(dirname "$LOG")"
rm -rf "$OUT"

env PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_main_evaluation \
  --output-dir "$OUT" \
  --queries-per-bucket 100 \
  --seed-count 5 \
  --queries-per-map 5 \
  --methods f_n3p_knn,vanilla_ha,n3p_k1,voronoi_waypoint,bottleneck_waypoint,md_dqn \
  --density-profile-buckets "$DENSITY_PROFILE_BUCKETS" \
  --distance-bins 8:12,12:16,16:20,20: \
  --bootstrap-resamples 5000 \
  --md-dqn-source-dir /home/ubuntu/DQN10/2_experiment \
  --md-dqn-checkpoint /home/ubuntu/DQN10/2_experiment/ugv_dqn/outputs/2026-05-12_train_load_external_demo_smoke/models/realmap_a/mlp-dqn.pt \
  --md-dqn-algo mlp-dqn \
  --md-dqn-device cpu \
  --md-dqn-max-steps 600 \
  --k-neighbors 20 \
  --commit-verified-rs-segments \
  --source-head "$SOURCE_HEAD" \
  --preflight-only \
  > "${LOG}.preflight.json" 2> "${LOG}.preflight.err"

set +e
/usr/bin/time -p env PYTHONPATH=2_experiment python -m forest_n3p.scripts.run_main_evaluation \
  --output-dir "$OUT" \
  --queries-per-bucket 100 \
  --seed-count 5 \
  --queries-per-map 5 \
  --methods f_n3p_knn,vanilla_ha,n3p_k1,voronoi_waypoint,bottleneck_waypoint,md_dqn \
  --density-profile-buckets "$DENSITY_PROFILE_BUCKETS" \
  --distance-bins 8:12,12:16,16:20,20: \
  --bootstrap-resamples 5000 \
  --md-dqn-source-dir /home/ubuntu/DQN10/2_experiment \
  --md-dqn-checkpoint /home/ubuntu/DQN10/2_experiment/ugv_dqn/outputs/2026-05-12_train_load_external_demo_smoke/models/realmap_a/mlp-dqn.pt \
  --md-dqn-algo mlp-dqn \
  --md-dqn-device cpu \
  --md-dqn-max-steps 600 \
  --k-neighbors 20 \
  --commit-verified-rs-segments \
  --source-head "$SOURCE_HEAD" \
  > "${LOG}.out" 2> "${LOG}.err"

rc=$?
set -e
echo "$rc" > "${LOG}.exit"
exit "$rc"
