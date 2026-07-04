from __future__ import annotations

import argparse
import hashlib
import json
import socket
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

import pyarrow.parquet as pq

from forest_n3p.main_evaluation import MainEvaluationConfig
from forest_n3p.scripts.run_oracle_connector_analysis import MapCacheKey, _grid_for_row, _profiles_from_bucket_mode
from forest_n3p.third_party.pathplan import GridMap, TwoCircleFootprint
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker


def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    args = _parse_args(raw_argv)
    rows = pq.read_table(args.dataset).to_pylist()
    cfg = MainEvaluationConfig(
        seed=int(args.seed),
        profiles=_profiles_from_bucket_mode(str(args.density_profile_buckets)),
        methods=("ha_no_analytic",),
        allow_unreviewed_cutpoints=True,
        allow_unresolved_human_review=True,
        enforce_t14_scale=False,
    )
    footprint = TwoCircleFootprint.from_box(length=float(args.footprint_length_m), width=float(args.footprint_width_m))
    map_cache: dict[MapCacheKey, GridMap] = {}
    checker_cache: dict[MapCacheKey, GridFootprintChecker] = {}
    counts: Counter[str] = Counter()
    by_profile: Counter[str] = Counter()
    by_oracle: Counter[str] = Counter()
    by_source: dict[int, Counter[str]] = defaultdict(Counter)
    examples: list[dict[str, Any]] = []

    for row in rows:
        grid_map = _grid_for_row(row, cfg, footprint, map_cache)
        cache_key = (str(row["profile_name"]), int(row["map_seed"]))
        checker = checker_cache.get(cache_key)
        if checker is None:
            checker = GridFootprintChecker(grid_map, footprint, theta_bins=int(args.theta_bins))
            checker_cache[cache_key] = checker

        current_collision = bool(
            checker.collides_pose(float(row["current_x"]), float(row["current_y"]), float(row["current_theta"]))
        )
        next_collision = bool(
            checker.collides_pose(float(row["next_x"]), float(row["next_y"]), float(row["next_theta"]))
        )
        if current_collision:
            counts["current_collision_rows"] += 1
        if next_collision:
            counts["next_collision_rows"] += 1
        if current_collision or next_collision:
            counts["any_collision_rows"] += 1
            profile_name = str(row["profile_name"])
            oracle_type = str(row["oracle_type"])
            source_row_index = int(row["source_row_index"])
            by_profile[profile_name] += 1
            by_oracle[oracle_type] += 1
            by_source[source_row_index]["rows"] += 1
            by_source[source_row_index][profile_name] += 1
            if len(examples) < int(args.max_examples):
                examples.append(_example_row(row, current_collision=current_collision, next_collision=next_collision))

    payload = {
        "status": "complete",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "execution_host": socket.gethostname(),
        "source_head": str(args.source_head) if args.source_head else _source_head(),
        "command": " ".join(["python -m forest_n3p.scripts.audit_bc_demonstration_collisions", *raw_argv]),
        "dataset": str(args.dataset),
        "dataset_sha256": _sha256(args.dataset),
        "rows": int(len(rows)),
        "density_profile_buckets": str(args.density_profile_buckets),
        "theta_bins": int(args.theta_bins),
        "map_cache_keys_seen": [list(key) for key in sorted(map_cache)],
        "checker_cache_size": int(len(checker_cache)),
        "counts": dict(sorted(counts.items())),
        "collision_rows_by_profile": dict(sorted(by_profile.items())),
        "collision_rows_by_oracle": dict(sorted(by_oracle.items())),
        "source_rows_with_any_collision": int(len(by_source)),
        "top_collision_sources": [
            {"source_row_index": int(source), **dict(counter)}
            for source, counter in sorted(by_source.items(), key=lambda item: item[1]["rows"], reverse=True)[: int(args.max_sources)]
        ],
        "examples": examples,
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit BC demonstration current/next poses against true profile maps.")
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-head", default=None)
    parser.add_argument("--seed", type=int, default=20260620)
    parser.add_argument("--density-profile-buckets", default="validation_t06")
    parser.add_argument("--theta-bins", type=int, default=72)
    parser.add_argument("--footprint-length-m", type=float, default=0.924)
    parser.add_argument("--footprint-width-m", type=float, default=0.740)
    parser.add_argument("--max-examples", type=int, default=20)
    parser.add_argument("--max-sources", type=int, default=20)
    args = parser.parse_args(argv)
    _validate_args(args)
    return args


def _validate_args(args: argparse.Namespace) -> None:
    if not args.dataset.exists():
        raise FileNotFoundError(args.dataset)
    if int(args.theta_bins) <= 0:
        raise ValueError("--theta-bins must be positive")
    if int(args.max_examples) < 0:
        raise ValueError("--max-examples must be non-negative")
    if int(args.max_sources) < 0:
        raise ValueError("--max-sources must be non-negative")
    if float(args.footprint_length_m) <= 0.0 or float(args.footprint_width_m) <= 0.0:
        raise ValueError("footprint dimensions must be positive")


def _example_row(row: dict[str, Any], *, current_collision: bool, next_collision: bool) -> dict[str, Any]:
    return {
        "sample_id": int(row["sample_id"]),
        "source_row_index": int(row["source_row_index"]),
        "query_id": str(row["query_id"]),
        "difficulty_bucket": str(row["difficulty_bucket"]),
        "profile_name": str(row["profile_name"]),
        "map_seed": int(row["map_seed"]),
        "oracle_type": str(row["oracle_type"]),
        "current_collision": bool(current_collision),
        "next_collision": bool(next_collision),
        "current": [float(row["current_x"]), float(row["current_y"]), float(row["current_theta"])],
        "next": [float(row["next_x"]), float(row["next_y"]), float(row["next_theta"])],
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
    except Exception:  # noqa: BLE001 - audit provenance should not stop the audit.
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
