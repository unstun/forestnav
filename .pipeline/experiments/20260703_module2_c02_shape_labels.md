---
date: 2026-07-03
status: visual_seed_complete_not_gate
origin: codex+experiment
reviewed: false
task: Module2 C02.2
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
input_record: .pipeline/experiments/20260703_module2_c02_oracle_connector_full.md
source_head: 833eb1a4
execution_host: MacBook-Pro.local
---

# Module2 C02.2 Oracle Shape Labels

## 直观结论

C02.2 首批可视化种子已经完成。它把 C02.1 full run 的数字拆成三种能直接看懂的机械形态:

1. `invalid_goal/start`: goal 或 failed node 本身落在障碍里, 这不是 RL connector 的负样本。
2. `timeout_saved_by_goal_annulus`: 直接 Oracle A 超时, 但 Oracle B 能先接到 goal 周围候选点, 再用 terminal RS 接到 goal。
3. `oracle_b_conservative_combined_collision_rejection`: Oracle A 能直接连通, 当前 Oracle B 的组合路径验收更保守。

这一步仍不是 Gate #2。它只证明 C02.1 的关键分层有可回看的图像证据, 并暴露一个必须继续审计的问题: full run 中 5 个 `voronoi_skeleton` B-only 行目前不能被当前重放脚本复现, 所以暂时不能作为形态正例使用。

## 输入

- Full run record: `.pipeline/experiments/20260703_module2_c02_oracle_connector_full.md`
- Full result table: `0_trials/module2_oracle_shape/oracle_connector_results.parquet`
- C02.1 committed state: `833eb1a4 验证：记录C02 oracle connector全量结果`
- Full result row source hash: `1f4f96f82bca68f06cc6e9a08adb9ea9aaf993a5`

## Rendering Command

```bash
PYTHONPATH=2_experiment python -m forest_n3p.scripts.render_oracle_connector_cases \
  --results 0_trials/module2_oracle_shape/oracle_connector_results.parquet \
  --output-dir 0_trials/module2_oracle_shape/c02_shape_labels \
  --source-head 833eb1a4
```

Render script:

- `2_experiment/forest_n3p/scripts/render_oracle_connector_cases.py`

Output directory:

- `0_trials/module2_oracle_shape/c02_shape_labels/`

Output files:

- `summary.json`
- `index.md`
- `invalid_goal_complex.png`
- `invalid_goal_extreme.png`
- `invalid_start_extreme.png`
- `b_only_complex_timeout.png`
- `b_only_extreme_goal_annulus.png`
- `a_only_complex_conservative_b.png`
- `a_only_extreme_conservative_b.png`

## Labeled Cases

| Case | Shape label | Query | Collision flags | A result | B result | Rendered B |
|---|---|---|---|---|---|---|
| `invalid_goal_complex` | `invalid_goal_in_collision` | `complex_s00_q0007` exp=0 | state=false, goal=true | failed: `goal_in_collision` | failed | false |
| `invalid_goal_extreme` | `invalid_goal_in_collision` | `extreme_s00_q0006` exp=432 | state=false, goal=true | failed: `goal_in_collision` | failed | false |
| `invalid_start_extreme` | `invalid_start_in_collision_goal_also_blocked` | `extreme_s00_q0006` exp=1024 | state=true, goal=true | failed: `start_in_collision` | failed | false |
| `b_only_complex_timeout` | `timeout_saved_by_goal_annulus` | `complex_s00_q0003` exp=4640 | state=false, goal=false | failed: `timeout` | success: `goal_annulus` | true |
| `b_only_extreme_goal_annulus` | `timeout_saved_by_goal_annulus` | `extreme_s00_q0003` exp=224 | state=false, goal=false | failed: `timeout` | success: `goal_annulus` | true |
| `a_only_complex_conservative_b` | `oracle_b_conservative_combined_collision_rejection` | `complex_s00_q0002` exp=3424 | state=false, goal=false | success | failed | false |
| `a_only_extreme_conservative_b` | `oracle_b_conservative_combined_collision_rejection` | `extreme_s00_q0003` exp=160 | state=false, goal=false | success | failed | false |

Image index:

- `0_trials/module2_oracle_shape/c02_shape_labels/index.md`

Machine-readable summary:

- `0_trials/module2_oracle_shape/c02_shape_labels/summary.json`

## Image QA

Checks performed:

```bash
python - <<'PY'
import json
from pathlib import Path
from PIL import Image

summary = json.loads(Path("0_trials/module2_oracle_shape/c02_shape_labels/summary.json").read_text())
print("case_count", summary["case_count"])
for case in summary["cases"]:
    image = Image.open(case["image"])
    colors = image.convert("RGB").getcolors(maxcolors=10_000_000)
    color_count = len(colors) if colors is not None else -1
    assert image.size[0] > 500 and image.size[1] > 500
    assert color_count > 50
    if case["oracle_b_success"]:
        assert case["rendered_b_success"], case["case_id"]
    print(case["case_id"], image.size, color_count, case["rendered_b_success"])
PY
```

Result:

- `case_count=7`
- All images are `1393 x 1292`.
- All images have more than 50 unique RGB colors.
- Both `oracle_b_success=true` cases replayed with `rendered_b_success=true`.
- Invalid endpoint cases expose the expected collision flags in `summary.json`.

Manual visual spot-check:

- `b_only_complex_timeout.png`: orange Oracle B segment reaches a goal-annulus candidate and dashed terminal RS connects into the goal.
- `invalid_start_extreme.png`: failed node and goal are marked with collision crosses on occupied cells.

## Voronoi Provenance Issue

C02.1 full run reported 5 B-only rows whose selected candidate source is `voronoi_skeleton`:

| Query | Expansion | Full-run RS-reachable candidates | Current replay candidates | Current replay B |
|---|---:|---:|---:|---|
| `extreme_s00_q0006` | 64 | 38 | 0 | false |
| `extreme_s00_q0006` | 136 | 38 | 0 | false |
| `extreme_s00_q0006` | 288 | 38 | 0 | false |
| `extreme_s00_q0006` | 296 | 38 | 0 | false |
| `extreme_s00_q0006` | 336 | 38 | 0 | false |

Replay check:

```bash
PYTHONPATH=2_experiment python - <<'PY'
import pandas as pd
from forest_n3p.scripts.run_oracle_connector_analysis import _grid_for_row, _distance_field_m, _generate_candidate_set, _pose_from_row, _profiles_from_bucket_mode
from forest_n3p.scripts.render_oracle_connector_cases import _oracle_default_args, _run_oracle_b_path
from forest_n3p.main_evaluation import MainEvaluationConfig
from forest_n3p.third_party.pathplan import TwoCircleFootprint

df = pd.read_parquet("0_trials/module2_oracle_shape/oracle_connector_results.parquet")
rows = df[(df["oracle_b_selected_candidate_source"] == "voronoi_skeleton") & (~df["oracle_a_success"]) & (df["oracle_b_success"])]
cfg = MainEvaluationConfig(seed=20260620, profiles=_profiles_from_bucket_mode("validation_t06"), methods=("ha_no_analytic",), allow_unreviewed_cutpoints=True, allow_unresolved_human_review=True, enforce_t14_scale=False)
args = _oracle_default_args()
footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
cache = {}
for _, row in rows.sort_values(["query_id", "expansion_idx"]).iterrows():
    d = dict(row)
    grid = _grid_for_row(d, cfg, footprint, cache)
    candidates = _generate_candidate_set(grid, footprint, _distance_field_m(grid), args, _pose_from_row(d, "state"), _pose_from_row(d, "goal"))
    replay = _run_oracle_b_path(grid, footprint, cfg, args, _pose_from_row(d, "state"), _pose_from_row(d, "goal"), candidates)
    print(d["query_id"], int(d["expansion_idx"]), int(d["candidate_rs_reachable_count"]), len(candidates.candidates), replay.success)
PY
```

Interpretation:

- The full C02.1 aggregate counts remain recorded as C02.1 artifacts.
- The 5 `voronoi_skeleton` B-only rows must be audited before they are used as paper evidence.
- C02.2 visual positives currently use only reproducible `goal_annulus` B-only rows.

## Allowed Conclusions

- C02.2 has a first reproducible visual seed set covering invalid endpoints, reproducible B-only timeout rescue, and A-only conservative B rejection.
- Invalid endpoint rows should be filtered or separately labeled before any RL training dataset is extracted.
- There is at least one Complex and one Extreme non-invalid timeout case where an intermediate goal-annulus connector plus terminal RS succeeds while direct Oracle A timed out.

## Disallowed Conclusions

- Do not claim Gate #2 is complete.
- Do not claim most non-invalid RS failures need RL; C02.1 shows B-only is only 63 rows under the current oracle, and only two B-only `goal_annulus` examples are visualized here.
- Do not use the 5 `voronoi_skeleton` B-only rows as visual or paper evidence until their replay mismatch is resolved.
- Do not claim RL has been implemented or PPO is necessary before D01/D02 cost accounting and later RL experiments.

## Next Step

C02.3 should use this first visual seed set for a narrow Gate #2 statement. A conservative C02.3 statement should say:

- the current oracle dataset does not support training on all RS failures;
- the valid target is narrower: invalid endpoint cleanup plus timeout/operator-cost cases;
- D01/D02 cost accounting is required before implementing the RL-RS funnel.
