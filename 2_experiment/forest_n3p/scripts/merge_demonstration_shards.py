from __future__ import annotations

import argparse
import hashlib
import json
import socket
import subprocess
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

import pyarrow as pa
import pyarrow.parquet as pq


def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    args = _parse_args(raw_argv)
    source_head = str(args.source_head) if args.source_head else _source_head()

    tables = [pq.read_table(path) for path in args.inputs]
    if not tables:
        raise ValueError("--inputs must contain at least one shard")
    schema = tables[0].schema
    for path, table in zip(args.inputs, tables, strict=True):
        if table.schema != schema:
            raise ValueError(f"schema mismatch for shard: {path}")

    rows: list[dict[str, Any]] = []
    for table in tables:
        rows.extend(table.to_pylist())
    for sample_id, row in enumerate(rows):
        row["sample_id"] = int(sample_id)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    merged = pa.Table.from_pylist(rows, schema=schema)
    pq.write_table(merged, output)
    summary = _summary_payload(args=args, raw_argv=raw_argv, output=output, source_head=source_head, rows=rows)
    summary_path = output.with_name(output.stem + "_summary.json")
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Merge Module2 RL-RS BC demonstration parquet shards.")
    parser.add_argument("--inputs", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-head", default=None)
    return parser.parse_args(argv)


def _summary_payload(
    *,
    args: argparse.Namespace,
    raw_argv: Sequence[str],
    output: Path,
    source_head: str,
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    oracle_counts = Counter(str(row.get("oracle_type")) for row in rows)
    bucket_counts = Counter(str(row.get("difficulty_bucket")) for row in rows)
    source_rows_by_oracle: dict[str, set[int]] = {}
    for row in rows:
        source_rows_by_oracle.setdefault(str(row.get("oracle_type")), set()).add(int(row["source_row_index"]))
    return {
        "status": "complete",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "execution_host": socket.gethostname(),
        "source_head": str(source_head),
        "command": " ".join(["python -m forest_n3p.scripts.merge_demonstration_shards", *raw_argv]),
        "inputs": [
            {
                "path": str(path),
                "sha256": _sha256(path),
                "rows": int(pq.read_table(path).num_rows),
            }
            for path in args.inputs
        ],
        "output": str(output),
        "output_sha256": _sha256(output),
        "rows": int(len(rows)),
        "source_row_count": int(len({int(row["source_row_index"]) for row in rows})),
        "oracle_type_counts": dict(sorted(oracle_counts.items())),
        "difficulty_bucket_counts": dict(sorted(bucket_counts.items())),
        "source_row_counts_by_oracle": {
            key: int(len(value)) for key, value in sorted(source_rows_by_oracle.items())
        },
        "sample_id_policy": "rewritten_contiguous_after_merge",
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop merging.
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
