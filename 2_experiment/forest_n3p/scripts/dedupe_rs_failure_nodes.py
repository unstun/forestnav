from __future__ import annotations

import argparse
import json
import math
import socket
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

import pyarrow as pa
import pyarrow.parquet as pq


def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(description="Deduplicate Module2 RS failure nodes by query/grid/theta bin.")
    parser.add_argument("--input", type=Path, default=Path("0_trials/module2_oracle_shape/rs_failure_nodes.parquet"))
    parser.add_argument("--output", type=Path, default=Path("0_trials/module2_oracle_shape/rs_failure_nodes_dedup.parquet"))
    parser.add_argument("--resolution-m", type=float, default=0.1)
    parser.add_argument("--origin-x", type=float, default=0.0)
    parser.add_argument("--origin-y", type=float, default=0.0)
    parser.add_argument("--theta-bins", type=int, default=72)
    parser.add_argument("--source-head", default=None)
    args = parser.parse_args(argv)

    source_head = str(args.source_head) if args.source_head else _source_head()
    rows = pq.read_table(args.input).to_pylist()
    by_key: dict[tuple[Any, ...], dict[str, Any]] = {}
    duplicate_counts: dict[tuple[Any, ...], int] = {}

    for row in rows:
        gx = int(math.floor((float(row["state_x"]) - float(args.origin_x)) / float(args.resolution_m)))
        gy = int(math.floor((float(row["state_y"]) - float(args.origin_y)) / float(args.resolution_m)))
        theta_bin = _theta_bin(float(row["state_theta"]), int(args.theta_bins))
        key = (row["query_id"], gx, gy, theta_bin)
        duplicate_counts[key] = duplicate_counts.get(key, 0) + 1
        candidate = dict(row)
        candidate["state_gx"] = gx
        candidate["state_gy"] = gy
        candidate["state_theta_bin"] = theta_bin
        if key not in by_key or int(candidate["expansion_idx"]) < int(by_key[key]["expansion_idx"]):
            by_key[key] = candidate

    dedup_rows = []
    for key, row in sorted(by_key.items(), key=lambda item: (str(item[0][0]), int(item[1]["expansion_idx"]))):
        out = dict(row)
        out["duplicate_count"] = int(duplicate_counts[key])
        out["dedup_key"] = f"{key[0]}:{key[1]}:{key[2]}:{key[3]}"
        out["dedup_source_head"] = source_head
        dedup_rows.append(out)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    table = pa.Table.from_pylist(dedup_rows)
    pq.write_table(table, output)

    summary = {
        "status": "complete",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "execution_host": socket.gethostname(),
        "source_head": source_head,
        "command": " ".join(["python -m forest_n3p.scripts.dedupe_rs_failure_nodes", *raw_argv]),
        "input": str(args.input),
        "output": str(output),
        "input_row_count": len(rows),
        "dedup_row_count": len(dedup_rows),
        "dropped_duplicate_count": len(rows) - len(dedup_rows),
        "resolution_m": float(args.resolution_m),
        "theta_bins": int(args.theta_bins),
    }
    summary_path = output.with_name(output.stem + "_summary.json")
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


def _theta_bin(theta: float, theta_bins: int) -> int:
    wrapped = float(theta) % (2.0 * math.pi)
    return int(math.floor((wrapped / (2.0 * math.pi)) * int(theta_bins))) % int(theta_bins)


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop collection.
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
