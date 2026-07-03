---
date: 2026-07-03
status: gate2_not_failed_scope_narrowed
origin: codex+experiment
reviewed: false
task: Module2 C02.3 Gate #2
contract: .pipeline/contracts/module2-ppo-funnel-expansion.md
inputs:
  - .pipeline/experiments/20260703_module2_c02_oracle_connector_full.md
  - .pipeline/experiments/20260703_module2_c02_shape_labels.md
  - 0_trials/module2_oracle_shape/oracle_connector_results.parquet
  - 0_trials/module2_oracle_shape/c02_shape_labels/summary.json
source_head: be2c7f14
execution_host: MacBook-Pro.local
---

# Module2 C02.3 Gate #2 Oracle Shape Decision

## 直观结论

Gate #2 的失败条件没有命中, 但 RL-RS funnel 的问题范围被明显压窄。

按 approved Contract, Gate #2 的失败定义是: Oracle 全图 HA* 显示失败节点本就无解, 导致任何学习型扩展都没用。C02.1 full run 证明: 剔除 invalid start/goal 后, 6289/6289 个 non-invalid RS failure nodes 都 oracle-connectable。因此不能说这个方向因为 "多数节点本来无解" 而失败。

但 C02.1/C02.2 也反过来证明: 不能把所有 7860 个 RS failure nodes 都包装成 RL 训练目标。1571 个是 invalid endpoint; 真正 B-only timeout 信号只有 63 个, 且当前可视化正例只保留可重放的 `goal_annulus` cases。下一步应该先做 D01/D02 成本账, 而不是直接开 PPO 训练。

## Decision

| Gate item | Decision | Evidence |
|---|---|---|
| Gate #2 failure: oracle says non-invalid nodes are mostly no-solution | **Not triggered** | Non-invalid rows: 6289; non-invalid connectable: 6289; non-invalid unresolved: 0 |
| Broad claim: most RS failures need a learned connector | **Rejected** | 1571/7860 rows are invalid endpoints; B-only is 63/6289 non-invalid rows |
| Narrow claim: there is a real connector-shape signal worth cost accounting | **Allowed** | B-only timeout rows exist: 63 total; selected source `goal_annulus=58`, `voronoi_skeleton=5`; two `goal_annulus` cases replay and render successfully |
| Move directly to RL environment/training | **Not allowed yet** | Contract success requires end-to-end speed/node/failure gains; D01/D02 cost accounting is still missing |
| Next allowed work | **Proceed to D01/D02** | Measure Dang multi-RS cost and NN/rollout budget before implementing RL-RS funnel |

## Contract Anchor

The approved Contract states:

- The module is a PPO + RS funnel architecture: medium-range PPO rollout, final 1-2 m RS mathematical fit (`.pipeline/contracts/module2-ppo-funnel-expansion.md:10-17`).
- Success requires node count, wall-clock time, and timeout failure rate to improve together (`.pipeline/contracts/module2-ppo-funnel-expansion.md:19-32`); the wall-clock requirement explicitly includes PPO forward inference, RS computation, and grid expansion (`.pipeline/contracts/module2-ppo-funnel-expansion.md:21-25`).
- Gate #2 failure is specifically "Oracle 全图 HA* 显示失败节点本就无解" (`.pipeline/contracts/module2-ppo-funnel-expansion.md:34-39`).
- The experiment pipeline also requires timing-protocol repair before later evaluation (`.pipeline/contracts/module2-ppo-funnel-expansion.md:41-45`).

Therefore C02.3 can only answer the oracle-shape question. It cannot certify speed, PPO necessity, or training viability.

## Evidence Inputs

### C02.1 Full Oracle

C02.1 full run covered all 7860 deduplicated RS failure nodes and explicitly framed the result as "problem shape narrowed", not "RL already replaces RS" (`.pipeline/experiments/20260703_module2_c02_oracle_connector_full.md:14-29`).

Integrity evidence:

- Root summary status: `complete`
- Selected rows: 7860
- Chunk count: 79
- Merged parquet rows: 7860
- Merged `source_head`: all rows use `1f4f96f82bca68f06cc6e9a08adb9ea9aaf993a5`
- Source lines: `.pipeline/experiments/20260703_module2_c02_oracle_connector_full.md:75-88`

Full counts:

| Metric | Count |
|---|---:|
| Rows | 7860 |
| Oracle A success | 6226 |
| Oracle B success | 6287 |
| Oracle connectable | 6289 |
| Both A and B success | 6224 |
| B-only | 63 |
| A-only | 2 |
| Unresolved | 1571 |

Source lines: `.pipeline/experiments/20260703_module2_c02_oracle_connector_full.md:106-117`.

Invalid endpoint triage:

| Item | Count |
|---|---:|
| Invalid by Oracle A reason | 1571 |
| `goal_in_collision` | 1182 |
| `start_in_collision` | 389 |
| Non-invalid rows | 6289 |
| Non-invalid connectable | 6289 |
| Non-invalid unresolved | 0 |

Source lines: `.pipeline/experiments/20260703_module2_c02_oracle_connector_full.md:150-157`.

B-only connector signal:

- Count: 63
- Oracle A reason: all `timeout`
- Bucket split: Complex 1, Extreme 62
- Selected source: `goal_annulus=58`, `voronoi_skeleton=5`
- Source lines: `.pipeline/experiments/20260703_module2_c02_oracle_connector_full.md:169-178`.

### C02.2 Visual Seed

C02.2 rendered three human-auditable shape groups:

1. invalid endpoint,
2. reproducible `goal_annulus` B-only timeout rescue,
3. A-only conservative Oracle B rejection.

Source lines: `.pipeline/experiments/20260703_module2_c02_shape_labels.md:15-23`.

Rendered cases:

| Case type | Representative evidence |
|---|---|
| Invalid goal | `invalid_goal_complex`, `invalid_goal_extreme` |
| Invalid start and goal blocked | `invalid_start_extreme` |
| Timeout saved by goal annulus | `b_only_complex_timeout`, `b_only_extreme_goal_annulus` |
| Oracle B conservative rejection | `a_only_complex_conservative_b`, `a_only_extreme_conservative_b` |

Source lines: `.pipeline/experiments/20260703_module2_c02_shape_labels.md:61-71`.

Image QA:

- `case_count=7`
- all images are `1393 x 1292`
- both `oracle_b_success=true` cases replayed with `rendered_b_success=true`
- source lines: `.pipeline/experiments/20260703_module2_c02_shape_labels.md:81-111`.

Provenance warning:

- Five full-run `voronoi_skeleton` B-only rows currently replay to zero regenerated candidates and false B replay.
- They remain excluded from visual/paper evidence until audited.
- Source lines: `.pipeline/experiments/20260703_module2_c02_shape_labels.md:118-159`.

## Independent Verification Run

Command:

```bash
PYTHONPATH=2_experiment python - <<'PY'
from pathlib import Path
import json
import pandas as pd

df = pd.read_parquet("0_trials/module2_oracle_shape/oracle_connector_results.parquet")
full = json.loads(Path("0_trials/module2_oracle_shape/oracle_connector_full/summary.json").read_text())
shape = json.loads(Path("0_trials/module2_oracle_shape/c02_shape_labels/summary.json").read_text())

invalid = df["oracle_a_failure_reason"].isin(["goal_in_collision", "start_in_collision"])
connectable = df["oracle_connectable"].astype(bool)
a = df["oracle_a_success"].astype(bool)
b = df["oracle_b_success"].astype(bool)

print("full_status", full["status"])
print("chunk_count", full["chunk_count"])
print("rows", len(df))
print("source_heads", df["source_head"].value_counts(dropna=False).to_dict())
print("invalid", int(invalid.sum()))
print("non_invalid", int((~invalid).sum()))
print("non_invalid_connectable", int((connectable & ~invalid).sum()))
print("non_invalid_unresolved", int(((~connectable) & ~invalid).sum()))
print("b_only", int((~a & b).sum()))
print("a_only", int((a & ~b).sum()))
print("both_success", int((a & b).sum()))
print("unresolved_total", int((~a & ~b).sum()))
print("b_only_sources", df.loc[(~a & b), "oracle_b_selected_candidate_source"].value_counts(dropna=False).to_dict())
print("shape_status", shape["status"])
print("shape_case_count", shape["case_count"])
print("shape_labels", sorted({c["shape_label"] for c in shape["cases"]}))
print("rendered_b_success_count", sum(1 for c in shape["cases"] if c["rendered_b_success"]))
PY
```

Observed output:

```text
full_status complete
chunk_count 79
rows 7860
source_heads {'1f4f96f82bca68f06cc6e9a08adb9ea9aaf993a5': 7860}
invalid 1571
non_invalid 6289
non_invalid_connectable 6289
non_invalid_unresolved 0
b_only 63
a_only 2
both_success 6224
unresolved_total 1571
b_only_sources {'goal_annulus': 58, 'voronoi_skeleton': 5}
shape_status complete
shape_case_count 7
shape_labels ['invalid_goal_in_collision', 'invalid_start_in_collision_goal_also_blocked', 'oracle_b_conservative_combined_collision_rejection', 'timeout_saved_by_goal_annulus']
rendered_b_success_count 2
```

## Interpretation

### What Gate #2 Proves

- The current C02 dataset is not dominated by non-invalid oracle-no-solution states.
- The Contract's Gate #2 no-solution failure condition is not triggered.
- It is legitimate to continue toward cost accounting and possibly an RL-RS funnel operator, because the local connector problem has at least a narrow positive signal.

### What Gate #2 Does Not Prove

- It does not prove RL is necessary.
- It does not prove PPO is the right policy optimization method.
- It does not prove most RS failures should become RL training episodes.
- It does not prove the final method will be faster; Contract success still requires end-to-end timing and node-count improvements.
- It does not validate the `voronoi_skeleton` B-only rows as paper evidence.

### Scope Narrowing

After C02.3, the permissible training/evaluation target is:

1. filter or separately label invalid endpoint rows before dataset extraction;
2. treat B-only timeout rows as the primary connector-positive seed;
3. treat A-only rows as conservative Oracle B diagnostics, not RL positives;
4. audit `voronoi_skeleton` replay before using those rows in any claim;
5. run D01/D02 cost accounting before implementing or training RL.

## Downstream Task Changes

Proceed to Phase D before Phase E:

- D01.1: split Dang multi-RS analytic expansion cost into RS solve time, sampling time, collision-check time, candidates attempted, and failure reason.
- D01.2: estimate the cost of failed RS analytic attempts on the same C01/C02 query set.
- D02.1: benchmark candidate policy forward budgets using input shapes derived from C02, not arbitrary network shapes.

Do not start E01 `rl_rs/` environment until D01/D02 show that the compute budget could plausibly beat the current RS/Dang baseline.

## Claim Boundary For Paper Drafting

Allowed:

- "In the C02 oracle audit, non-invalid RS analytic-expansion failure nodes were all connectable by the oracle budget, so the no-solution Gate #2 did not stop the line."
- "The target set is much narrower than all RS failures: invalid endpoints must be excluded, and the strongest current connector-positive signal is timeout rows rescued by intermediate candidates."

Disallowed:

- "RL replaces RS."
- "PPO is necessary."
- "Most RS failures require learned steering."
- "The `voronoi_skeleton` B-only rows prove bottleneck bypass."
- "Gate #1 or Gate #3 is passed."

## Final Gate #2 Status

`gate2_not_failed_scope_narrowed`

This permits D01/D02 cost accounting. It does not permit direct transition to RL training or paper performance claims.
