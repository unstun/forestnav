from __future__ import annotations

import argparse
import json
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
    parser = argparse.ArgumentParser(
        description=(
            "Run Module2 C02 oracle connector analysis in resumable chunks. "
            "Unknown arguments are forwarded to run_oracle_connector_analysis."
        )
    )
    parser.add_argument("--input", type=Path, default=Path("0_trials/module2_oracle_shape/rs_failure_nodes_dedup.parquet"))
    parser.add_argument("--output-dir", type=Path, default=Path("0_trials/module2_oracle_shape/oracle_connector_full"))
    parser.add_argument("--merged-output", type=Path, default=Path("0_trials/module2_oracle_shape/oracle_connector_results.parquet"))
    parser.add_argument("--row-offset", type=int, default=0)
    parser.add_argument("--max-records", type=int, default=None)
    parser.add_argument("--chunk-size", type=int, default=100)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--source-head", default=None)
    args, child_args = parser.parse_known_args(argv)

    _validate_args(args)
    source_head = str(args.source_head) if args.source_head else _source_head()
    input_row_count = pq.read_table(args.input).num_rows
    selected = _selected_count(input_row_count, int(args.row_offset), args.max_records)
    if selected <= 0:
        raise ValueError("selected row count is zero")

    output_dir = Path(args.output_dir)
    chunk_dir = output_dir / "chunks"
    chunk_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    chunk_records: list[dict[str, Any]] = []
    failed: dict[str, Any] | None = None
    for offset, limit in _chunk_ranges(int(args.row_offset), selected, int(args.chunk_size)):
        record = _run_chunk(
            args,
            child_args,
            source_head=source_head,
            chunk_dir=chunk_dir,
            offset=offset,
            limit=limit,
        )
        chunk_records.append(record)
        if int(record["returncode"]) != 0:
            failed = record
            break

    status = "failed" if failed is not None else "complete"
    merged_output = None
    aggregate = {}
    if failed is None:
        chunk_paths = [Path(record["parquet"]) for record in chunk_records]
        merged_output = Path(args.merged_output)
        aggregate = _merge_chunks(chunk_paths, merged_output)

    summary = {
        "status": status,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "execution_host": socket.gethostname(),
        "source_head": source_head,
        "command": " ".join(["python -m forest_n3p.scripts.run_oracle_connector_chunks", *raw_argv]),
        "input": str(args.input),
        "input_row_count": int(input_row_count),
        "row_offset": int(args.row_offset),
        "selected_row_count": int(selected),
        "chunk_size": int(args.chunk_size),
        "chunk_count": len(chunk_records),
        "output_dir": str(output_dir),
        "merged_output": str(merged_output) if merged_output is not None else None,
        "failed_chunk": failed,
        "chunks": chunk_records,
        "aggregate": aggregate,
        "forwarded_child_args": list(child_args),
    }
    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if failed is None else int(failed["returncode"])


def _run_chunk(
    args: argparse.Namespace,
    child_args: Sequence[str],
    *,
    source_head: str,
    chunk_dir: Path,
    offset: int,
    limit: int,
) -> dict[str, Any]:
    stem = f"chunk_{offset:06d}_{offset + limit - 1:06d}"
    parquet_path = chunk_dir / f"{stem}.parquet"
    stdout_path = chunk_dir / f"{stem}_stdout.txt"
    stderr_path = chunk_dir / f"{stem}_stderr.txt"
    summary_path = chunk_dir / f"{stem}_summary.json"
    if (
        not bool(args.force)
        and parquet_path.exists()
        and stdout_path.exists()
        and stderr_path.exists()
        and summary_path.exists()
    ):
        return {
            "offset": int(offset),
            "limit": int(limit),
            "returncode": 0,
            "skipped_existing": True,
            "parquet": str(parquet_path),
            "stdout": str(stdout_path),
            "stderr": str(stderr_path),
            "summary": str(summary_path),
        }

    cmd = [
        sys.executable,
        "-m",
        "forest_n3p.scripts.run_oracle_connector_analysis",
        "--input",
        str(args.input),
        "--output",
        str(parquet_path),
        "--row-offset",
        str(offset),
        "--max-records",
        str(limit),
        "--source-head",
        str(source_head),
        *child_args,
    ]
    with stdout_path.open("w", encoding="utf-8") as stdout_f, stderr_path.open("w", encoding="utf-8") as stderr_f:
        completed = subprocess.run(cmd, stdout=stdout_f, stderr=stderr_f, text=True, check=False)

    generated_summary = parquet_path.with_name(parquet_path.stem + "_summary.json")
    if generated_summary.exists() and generated_summary != summary_path:
        generated_summary.replace(summary_path)

    return {
        "offset": int(offset),
        "limit": int(limit),
        "returncode": int(completed.returncode),
        "skipped_existing": False,
        "parquet": str(parquet_path),
        "stdout": str(stdout_path),
        "stderr": str(stderr_path),
        "summary": str(summary_path),
    }


def _merge_chunks(chunk_paths: Sequence[Path], output: Path) -> dict[str, Any]:
    tables = [pq.read_table(path) for path in chunk_paths]
    table = pa.concat_tables(tables) if tables else pa.table({})
    output.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, output)
    rows = table.to_pylist()
    oracle_a_success = sum(int(bool(row["oracle_a_success"])) for row in rows)
    oracle_b_success = sum(int(bool(row["oracle_b_success"])) for row in rows)
    connectable = sum(int(bool(row["oracle_connectable"])) for row in rows)
    by_bucket: dict[str, dict[str, int]] = {}
    for row in rows:
        bucket = str(row["difficulty_bucket"])
        item = by_bucket.setdefault(bucket, {"record_count": 0, "oracle_a_success": 0, "oracle_b_success": 0, "oracle_connectable": 0})
        item["record_count"] += 1
        item["oracle_a_success"] += int(bool(row["oracle_a_success"]))
        item["oracle_b_success"] += int(bool(row["oracle_b_success"]))
        item["oracle_connectable"] += int(bool(row["oracle_connectable"]))
    return {
        "result_row_count": len(rows),
        "oracle_a_success_count": int(oracle_a_success),
        "oracle_b_success_count": int(oracle_b_success),
        "oracle_connectable_count": int(connectable),
        "oracle_connectable_rate": None if not rows else float(connectable) / float(len(rows)),
        "by_bucket": by_bucket,
    }


def _chunk_ranges(start: int, selected: int, chunk_size: int) -> list[tuple[int, int]]:
    out = []
    end = int(start) + int(selected)
    offset = int(start)
    while offset < end:
        limit = min(int(chunk_size), end - offset)
        out.append((offset, limit))
        offset += limit
    return out


def _selected_count(input_row_count: int, row_offset: int, max_records: int | None) -> int:
    available = max(0, int(input_row_count) - int(row_offset))
    return available if max_records is None else min(available, int(max_records))


def _validate_args(args: argparse.Namespace) -> None:
    if int(args.row_offset) < 0:
        raise ValueError("--row-offset must be non-negative")
    if args.max_records is not None and int(args.max_records) <= 0:
        raise ValueError("--max-records must be positive when set")
    if int(args.chunk_size) <= 0:
        raise ValueError("--chunk-size must be positive")


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop chunk execution.
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
