"""Aggregate the module2 planner calibration sweep (pre-registered analysis).

Reads records.csv from the three calibration sets and emits
calibration_summary.md / calibration_summary.csv with the quantities
pre-registered in calibration_protocol.md. No bands, no verdict: the output
is a stability/variance table that informs the lane-C contract draft.

Written and committed while set 1 was still running and before any set had
produced results, per the pre-registration rule.

Usage: python3 0_trials/module2_planner_calibration/aggregate_calibration.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parent
SETS = ("set_s20260810", "set_s20260910", "set_s20261010")
METHODS = {
    "M1": "ha_single_rs",
    "M2": "ha_dang_multi_rs",
    "M3": "ha_rl_rs_ppo",
}
BUCKETS = ("Easy", "Complex", "Extreme")


def _percentile(values: list[float], q: float) -> float:
    if not values:
        return float("nan")
    ordered = sorted(values)
    pos = (len(ordered) - 1) * q
    lower = int(pos)
    upper = min(lower + 1, len(ordered) - 1)
    frac = pos - lower
    return ordered[lower] * (1.0 - frac) + ordered[upper] * frac


def _f(row: dict, key: str) -> float:
    raw = row.get(key)
    if raw is None or raw == "":
        return 0.0
    return float(raw)


def load_records(set_name: str) -> list[dict]:
    path = ROOT / set_name / "records.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def method_bucket_stats(rows: list[dict], method: str, bucket: str) -> dict:
    rs = [r for r in rows if r["method"] == method and r["difficulty_bucket"] == bucket]
    n = len(rs)
    if n == 0:
        raise SystemExit(f"no rows for method={method} bucket={bucket}")
    times = [_f(r, "total_time_s") for r in rs]
    exps = [_f(r, "total_expansions") for r in rs]
    stats = {
        "n": n,
        "success_rate": sum(1 for r in rs if r["success"] == "True") / n,
        "timeout_rate": sum(1 for r in rs if (r.get("failure_reason") or "") == "timeout") / n,
        "median_time_s": median(times),
        "p95_time_s": _percentile(times, 0.95),
        "median_expansions": median(exps),
        "p95_expansions": _percentile(exps, 0.95),
        "collision_violations": int(sum(_f(r, "collision_violation_count") for r in rs)),
        "exception_count": sum(
            1 for r in rs if "exception" in (r.get("failure_reason") or "").lower()
        ),
    }
    if method == METHODS["M3"]:
        rl_attempts = int(sum(_f(r, "rl_attempts") for r in rs))
        rl_successes = int(sum(_f(r, "rl_successes") for r in rs))
        stats.update(
            {
                "rl_attempts": rl_attempts,
                "rl_successes": rl_successes,
                "rl_attempt_success_rate": (rl_successes / rl_attempts) if rl_attempts else None,
                "mean_nn_forward_time_s": (
                    sum(_f(r, "nn_forward_time_s") for r in rs) / n
                ),
                "fallbacks": int(sum(_f(r, "fallback_to_primitives_count") for r in rs)),
                "wins_backed_by_rl": sum(
                    1 for r in rs if r["success"] == "True" and _f(r, "rl_successes") >= 1
                ),
                "win_count": sum(1 for r in rs if r["success"] == "True"),
            }
        )
    return stats


def paired_m3_vs_m1(rows: list[dict], bucket: str) -> dict:
    m1 = {
        r["query_id"]: r
        for r in rows
        if r["method"] == METHODS["M1"] and r["difficulty_bucket"] == bucket
    }
    m3 = {
        r["query_id"]: r
        for r in rows
        if r["method"] == METHODS["M3"] and r["difficulty_bucket"] == bucket
    }
    if set(m1) != set(m3):
        raise SystemExit(f"paired query sets differ in bucket {bucket}")
    exp_ratios: list[float] = []
    time_ratios: list[float] = []
    path_ratios: list[float] = []
    for qid, r1 in m1.items():
        r3 = m3[qid]
        e1, e3 = _f(r1, "total_expansions"), _f(r3, "total_expansions")
        t1, t3 = _f(r1, "total_time_s"), _f(r3, "total_time_s")
        if e1 > 0:
            exp_ratios.append(e3 / e1)
        if t1 > 0:
            time_ratios.append(t3 / t1)
        if r1["success"] == "True" and r3["success"] == "True":
            p1, p3 = _f(r1, "path_length_m"), _f(r3, "path_length_m")
            if p1 > 0 and p3 > 0:
                path_ratios.append(p3 / p1)
    return {
        "paired_n": len(m1),
        "median_expansions_ratio": median(exp_ratios) if exp_ratios else None,
        "median_time_ratio": median(time_ratios) if time_ratios else None,
        "joint_success_n": len(path_ratios),
        "median_path_length_ratio": median(path_ratios) if path_ratios else None,
    }


def main() -> int:
    per_set: dict[str, dict] = {}
    for set_name in SETS:
        rows = load_records(set_name)
        entry: dict = {"method_bucket": {}, "paired": {}}
        for label, method in METHODS.items():
            for bucket in BUCKETS:
                entry["method_bucket"][(label, bucket)] = method_bucket_stats(rows, method, bucket)
        for bucket in BUCKETS:
            entry["paired"][bucket] = paired_m3_vs_m1(rows, bucket)
        per_set[set_name] = entry

    headline_defs = [
        ("complex_success_delta_pp", lambda e: 100.0 * (
            e["method_bucket"][("M3", "Complex")]["success_rate"]
            - e["method_bucket"][("M1", "Complex")]["success_rate"]
        )),
        ("complex_paired_median_time_ratio", lambda e: e["paired"]["Complex"]["median_time_ratio"]),
        ("complex_paired_median_expansions_ratio", lambda e: e["paired"]["Complex"]["median_expansions_ratio"]),
        ("extreme_success_delta_pp", lambda e: 100.0 * (
            e["method_bucket"][("M3", "Extreme")]["success_rate"]
            - e["method_bucket"][("M1", "Extreme")]["success_rate"]
        )),
        ("extreme_paired_median_time_ratio", lambda e: e["paired"]["Extreme"]["median_time_ratio"]),
        ("easy_success_delta_pp", lambda e: 100.0 * (
            e["method_bucket"][("M3", "Easy")]["success_rate"]
            - e["method_bucket"][("M1", "Easy")]["success_rate"]
        )),
    ]
    headline: dict[str, dict] = {}
    for name, fn in headline_defs:
        values = {s: fn(per_set[s]) for s in SETS}
        ordered = sorted(values.values())
        headline[name] = {
            "per_set": values,
            "min": ordered[0],
            "median": ordered[len(ordered) // 2],
            "max": ordered[-1],
        }

    csv_path = ROOT / "calibration_summary.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "set", "method_label", "method", "bucket", "n", "success_rate",
                "timeout_rate", "median_expansions", "p95_expansions",
                "median_time_s", "p95_time_s", "collision_violations",
                "exception_count", "rl_attempts", "rl_successes",
                "rl_attempt_success_rate", "mean_nn_forward_time_s", "fallbacks",
                "wins_backed_by_rl", "win_count",
            ]
        )
        for set_name in SETS:
            for label, method in METHODS.items():
                for bucket in BUCKETS:
                    st = per_set[set_name]["method_bucket"][(label, bucket)]
                    writer.writerow(
                        [
                            set_name, label, method, bucket, st["n"],
                            f"{st['success_rate']:.4f}", f"{st['timeout_rate']:.4f}",
                            st["median_expansions"], f"{st['p95_expansions']:.1f}",
                            f"{st['median_time_s']:.4f}", f"{st['p95_time_s']:.4f}",
                            st["collision_violations"], st["exception_count"],
                            st.get("rl_attempts", ""), st.get("rl_successes", ""),
                            (
                                f"{st['rl_attempt_success_rate']:.4f}"
                                if st.get("rl_attempt_success_rate") is not None
                                else ""
                            ),
                            (
                                f"{st['mean_nn_forward_time_s']:.4f}"
                                if st.get("mean_nn_forward_time_s") is not None
                                else ""
                            ),
                            st.get("fallbacks", ""), st.get("wins_backed_by_rl", ""),
                            st.get("win_count", ""),
                        ]
                    )

    lines = [
        "# Module2 Planner Calibration Sweep Summary",
        "",
        "Diagnostic, non-formal, no paper claims. Pre-registered analysis from",
        "calibration_protocol.md; informs the lane-C contract draft only.",
        "",
        "## Headline Stability (across three disjoint query-seed sets)",
        "",
        "| Quantity | " + " | ".join(s.removeprefix("set_") for s in SETS) + " | min | median | max |",
        "|---|" + "---:|" * (len(SETS) + 3),
    ]
    for name, agg in headline.items():
        row = [name]
        for s in SETS:
            row.append(f"{agg['per_set'][s]:.4f}")
        row += [f"{agg['min']:.4f}", f"{agg['median']:.4f}", f"{agg['max']:.4f}"]
        lines.append("| " + " | ".join(row) + " |")
    lines += [
        "",
        "## Per-Set Method x Bucket Table",
        "",
        "| Set | Method | Bucket | n | Success | Timeout | Med exp | P95 exp | Med time s | P95 time s | Collisions |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for set_name in SETS:
        for label in METHODS:
            for bucket in BUCKETS:
                st = per_set[set_name]["method_bucket"][(label, bucket)]
                lines.append(
                    f"| {set_name.removeprefix('set_')} | {label} | {bucket} | {st['n']} "
                    f"| {st['success_rate']:.3f} | {st['timeout_rate']:.3f} "
                    f"| {st['median_expansions']:.1f} | {st['p95_expansions']:.1f} "
                    f"| {st['median_time_s']:.4f} | {st['p95_time_s']:.4f} "
                    f"| {st['collision_violations']} |"
                )
    lines += [
        "",
        "## M3 Operator Telemetry",
        "",
        "| Set | Bucket | RL attempts | RL successes | Attempt success | Mean NN fwd s | Fallbacks | Wins backed by RL |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for set_name in SETS:
        for bucket in BUCKETS:
            st = per_set[set_name]["method_bucket"][("M3", bucket)]
            rate = st.get("rl_attempt_success_rate")
            rate_text = f"{rate:.4f}" if rate is not None else "NA"
            lines.append(
                f"| {set_name.removeprefix('set_')} | {bucket} | {st['rl_attempts']} "
                f"| {st['rl_successes']} | {rate_text} "
                f"| {st['mean_nn_forward_time_s']:.4f} | {st['fallbacks']} "
                f"| {st['wins_backed_by_rl']}/{st['win_count']} |"
            )
    lines += [
        "",
        "## Paired M3 vs M1",
        "",
        "| Set | Bucket | Paired n | Med expansions ratio | Med time ratio | Joint-success n | Med path-length ratio |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for set_name in SETS:
        for bucket in BUCKETS:
            p = per_set[set_name]["paired"][bucket]

            def fmt(value: float | None) -> str:
                return f"{value:.4f}" if value is not None else "NA"

            lines.append(
                f"| {set_name.removeprefix('set_')} | {bucket} | {p['paired_n']} "
                f"| {fmt(p['median_expansions_ratio'])} | {fmt(p['median_time_ratio'])} "
                f"| {p['joint_success_n']} | {fmt(p['median_path_length_ratio'])} |"
            )
    lines.append("")
    md_path = ROOT / "calibration_summary.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps({name: {k: v for k, v in agg.items() if k != "per_set"} for name, agg in headline.items()}, indent=2))
    print(f"wrote {md_path}")
    print(f"wrote {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
