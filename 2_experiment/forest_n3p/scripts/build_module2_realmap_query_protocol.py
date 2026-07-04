from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.difficulty_calibration import parse_distance_bins
from forest_n3p.generalization import GeneralizationConfig, _append_realmap_queries
from forest_n3p.third_party.pathplan import GridMap, TwoCircleFootprint
from forest_n3p.third_party.pathplan.geometry import GridFootprintChecker


@dataclass(frozen=True)
class Module2RealmapQueryProtocolConfig:
    output_dir: Path
    manifest_out: Path | None = None
    queries_out: Path | None = None
    markdown_out: Path | None = None
    realmap_manifest_path: Path = Path("2_experiment/forest_n3p/assets/realmaps/manifest.json")
    seed: int = 20260623
    queries_per_map: int = 5
    include_canonical_query: bool = True
    distance_bins: str = "4:8,8:12,12:16,16:20,20:"
    max_query_sample_attempts: int = 800
    theta_bins: int = 72


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    cfg = Module2RealmapQueryProtocolConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        queries_out=args.queries_out,
        markdown_out=args.markdown_out,
        realmap_manifest_path=args.realmap_manifest_path,
        seed=int(args.seed),
        queries_per_map=int(args.queries_per_map),
        include_canonical_query=bool(args.include_canonical_query),
        distance_bins=str(args.distance_bins),
        max_query_sample_attempts=int(args.max_query_sample_attempts),
        theta_bins=int(args.theta_bins),
    )
    manifest, rows = build_realmap_query_protocol(cfg)
    output_dir = Path(cfg.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    queries_path = cfg.queries_out or output_dir / "module2_realmap_queries.csv"
    manifest_path = cfg.manifest_out or output_dir / "module2_realmap_query_protocol.json"
    markdown_path = cfg.markdown_out or output_dir / "module2_realmap_query_protocol.md"
    _write_query_csv(queries_path, rows)
    manifest = {
        **manifest,
        "queries_csv": str(queries_path),
        "queries_csv_sha256": _file_sha256(queries_path),
        "markdown": str(markdown_path),
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_path.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_path), "queries": str(queries_path), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_realmap_query_protocol(
    config: Module2RealmapQueryProtocolConfig,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    cfg = _validate_config(config)
    footprint = TwoCircleFootprint.from_box(length=0.924, width=0.740)
    gen_cfg = GeneralizationConfig(
        seed=int(cfg.seed),
        ood_queries_per_bucket=1,
        seed_count=1,
        realmap_queries_per_map=int(cfg.queries_per_map),
        include_realmap_canonical_query=bool(cfg.include_canonical_query),
        realmap_distance_bins=parse_distance_bins(str(cfg.distance_bins)),
        realmap_manifest_path=cfg.realmap_manifest_path,
        max_query_sample_attempts=int(cfg.max_query_sample_attempts),
    )
    queries = []
    maps: dict[str, GridMap] = {}
    _append_realmap_queries(queries, maps, gen_cfg, footprint)
    inventory = _realmap_inventory(cfg.realmap_manifest_path)
    rows = [_query_row(query, maps[query.map_key], inventory[str(query.map_id)], footprint, cfg) for query in queries]
    query_count_by_map = _count_by(rows, "map_id")
    manifest = {
        "schema_version": 1,
        "protocol_name": "module2_realmap_query_protocol",
        "status": "frozen",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "realmap_manifest": str(cfg.realmap_manifest_path),
        "realmap_manifest_sha256": _file_sha256(cfg.realmap_manifest_path),
        "map_count": len(inventory),
        "map_ids": sorted(inventory),
        "query_count": len(rows),
        "query_count_by_map": query_count_by_map,
        "query_rows_sha256": _rows_sha256(rows),
        "config": {
            "seed": int(cfg.seed),
            "queries_per_map": int(cfg.queries_per_map),
            "include_canonical_query": bool(cfg.include_canonical_query),
            "distance_bins": str(cfg.distance_bins),
            "max_query_sample_attempts": int(cfg.max_query_sample_attempts),
            "theta_bins": int(cfg.theta_bins),
        },
        "endpoint_audit": _endpoint_audit(rows),
        "claim_boundaries": [
            "This artifact freezes RealMap query generation only; it is not an evaluation result.",
            "All later RealMap method evaluations must cite the query CSV hash to be comparable.",
            "The canonical query comes from the RealMap inventory start_xy/goal_xy pair.",
        ],
    }
    return manifest, rows


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Freeze Module2 RealMap query generation without running planners.")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--queries-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--realmap-manifest-path", type=Path, default=Module2RealmapQueryProtocolConfig.realmap_manifest_path)
    parser.add_argument("--seed", type=int, default=Module2RealmapQueryProtocolConfig.seed)
    parser.add_argument("--queries-per-map", type=int, default=Module2RealmapQueryProtocolConfig.queries_per_map)
    parser.add_argument("--include-canonical-query", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--distance-bins", default=Module2RealmapQueryProtocolConfig.distance_bins)
    parser.add_argument("--max-query-sample-attempts", type=int, default=Module2RealmapQueryProtocolConfig.max_query_sample_attempts)
    parser.add_argument("--theta-bins", type=int, default=Module2RealmapQueryProtocolConfig.theta_bins)
    return parser.parse_args(list(argv) if argv is not None else None)


def _validate_config(config: Module2RealmapQueryProtocolConfig) -> Module2RealmapQueryProtocolConfig:
    if int(config.queries_per_map) <= 0:
        raise ValueError("queries_per_map must be positive")
    if int(config.max_query_sample_attempts) <= 0:
        raise ValueError("max_query_sample_attempts must be positive")
    if int(config.theta_bins) <= 0:
        raise ValueError("theta_bins must be positive")
    if not Path(config.realmap_manifest_path).is_file():
        raise FileNotFoundError(f"realmap manifest not found: {config.realmap_manifest_path}")
    parse_distance_bins(str(config.distance_bins))
    return config


def _query_row(query: Any, grid_map: GridMap, inventory: dict[str, Any], footprint: TwoCircleFootprint, config: Module2RealmapQueryProtocolConfig) -> dict[str, Any]:
    start = tuple(float(value) for value in query.start)
    goal = tuple(float(value) for value in query.goal)
    checker = GridFootprintChecker(grid_map, footprint, theta_bins=int(config.theta_bins))
    return {
        "query_id": str(query.query_id),
        "split": str(query.split),
        "difficulty_bucket": str(query.difficulty_bucket),
        "profile_name": str(query.profile_name),
        "map_id": str(query.map_id),
        "map_key": str(query.map_key),
        "map_seed": int(query.map_seed),
        "query_seed": int(query.query_seed),
        "seed_index": int(query.seed_index),
        "map_index": int(query.map_index),
        "query_index": int(query.query_index),
        "distance_bin_key": str(query.distance_bin_key),
        "start": start,
        "goal": goal,
        "start_x": start[0],
        "start_y": start[1],
        "start_theta": start[2],
        "goal_x": goal[0],
        "goal_y": goal[1],
        "goal_theta": goal[2],
        "euclidean_distance_m": math.hypot(goal[0] - start[0], goal[1] - start[1]),
        "start_collision": bool(checker.collides_pose(*start)),
        "goal_collision": bool(checker.collides_pose(*goal)),
        "map_grid_sha256": str(inventory.get("loader_grid_sha256")),
        "pgm_sha256": str(inventory.get("pgm_sha256")),
        "yaml": str(inventory.get("yaml")),
        "pgm": str(inventory.get("pgm")),
    }


def _realmap_inventory(path: Path) -> dict[str, dict[str, Any]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    maps = payload.get("maps")
    if not isinstance(maps, list) or not maps:
        raise ValueError(f"realmap manifest has no maps: {path}")
    out: dict[str, dict[str, Any]] = {}
    for item in maps:
        map_id = str(item.get("id"))
        if not map_id:
            raise ValueError(f"realmap manifest map has no id: {path}")
        out[map_id] = dict(item)
    return out


def _write_query_csv(path: Path, rows: Sequence[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: _csv_value(value) for key, value in row.items()})


def _csv_value(value: Any) -> Any:
    if isinstance(value, (tuple, list, dict)):
        return json.dumps(value, ensure_ascii=False)
    return value


def _rows_sha256(rows: Sequence[dict[str, Any]]) -> str:
    payload = json.dumps(rows, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _count_by(rows: Sequence[dict[str, Any]], key: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in rows:
        out[str(row[key])] = out.get(str(row[key]), 0) + 1
    return dict(sorted(out.items()))


def _endpoint_audit(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    start_collision_count = sum(1 for row in rows if bool(row["start_collision"]))
    goal_collision_count = sum(1 for row in rows if bool(row["goal_collision"]))
    return {
        "start_collision_count": int(start_collision_count),
        "goal_collision_count": int(goal_collision_count),
        "pass": bool(start_collision_count == 0 and goal_collision_count == 0),
    }


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 RealMap Query Protocol",
        "",
        f"- status: {manifest['status']}",
        f"- query_count: {manifest['query_count']}",
        f"- map_count: {manifest['map_count']}",
        f"- queries_csv: `{manifest.get('queries_csv')}`",
        f"- queries_csv_sha256: `{manifest.get('queries_csv_sha256')}`",
        f"- query_rows_sha256: `{manifest['query_rows_sha256']}`",
        "",
        "## Maps",
    ]
    for map_id, count in manifest["query_count_by_map"].items():
        lines.append(f"- {map_id}: {count}")
    lines.extend(
        [
            "",
            "## Endpoint Audit",
            f"- start_collision_count: {manifest['endpoint_audit']['start_collision_count']}",
            f"- goal_collision_count: {manifest['endpoint_audit']['goal_collision_count']}",
            f"- pass: {manifest['endpoint_audit']['pass']}",
            "",
        ]
    )
    return "\n".join(lines)


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop protocol generation.
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
