from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence


@dataclass(frozen=True)
class Module2EvaluationManifestConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    contract_path: Path = Path(".pipeline/contracts/module2-ppo-funnel-expansion.md")
    cutpoint_supplement_path: Path = Path(".pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md")
    realmap_manifest_path: Path = Path("2_experiment/forest_n3p/assets/realmaps/manifest.json")
    realmap_query_protocol_path: Path | None = None
    warm_start_decision: str = "pending"
    bc_checkpoint: Path | None = None
    rl_rs_checkpoint: Path | None = None
    queries_per_bucket: int = 100
    seed_count: int = 5
    queries_per_map: int = 5
    density_profile_buckets: str = "validation_t06"
    distance_bins: str = "8:12,12:16,16:20,20:"
    bootstrap_resamples: int = 10_000


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    cfg = Module2EvaluationManifestConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        contract_path=args.contract_path,
        cutpoint_supplement_path=args.cutpoint_supplement_path,
        realmap_manifest_path=args.realmap_manifest_path,
        realmap_query_protocol_path=args.realmap_query_protocol_path,
        warm_start_decision=str(args.warm_start_decision),
        bc_checkpoint=args.bc_checkpoint,
        rl_rs_checkpoint=args.rl_rs_checkpoint,
        queries_per_bucket=int(args.queries_per_bucket),
        seed_count=int(args.seed_count),
        queries_per_map=int(args.queries_per_map),
        density_profile_buckets=str(args.density_profile_buckets),
        distance_bins=str(args.distance_bins),
        bootstrap_resamples=int(args.bootstrap_resamples),
    )
    manifest = build_manifest(cfg)
    output_dir = Path(cfg.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = cfg.manifest_out or output_dir / "module2_v1_evaluation_manifest.json"
    markdown_path = cfg.markdown_out or output_dir / "module2_v1_evaluation_manifest.md"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_path.write_text(_manifest_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_path), "markdown": str(markdown_path), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: Module2EvaluationManifestConfig) -> dict[str, Any]:
    contract = _frontmatter_record(config.contract_path, keys=("status", "version", "approved_by", "approved_date", "reviewed"))
    cutpoints = _frontmatter_record(config.cutpoint_supplement_path, keys=("reviewed", "status"))
    real_maps = _realmap_record(config.realmap_manifest_path)
    realmap_query_protocol = _realmap_query_protocol_record(config.realmap_query_protocol_path)
    methods = _method_records(config)
    blockers = _global_blockers(config, methods, realmap_query_protocol)
    status = _manifest_status(config, methods, blockers)
    return {
        "schema_version": 1,
        "manifest_name": "module2_v1_evaluation",
        "status": status,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "contract": contract,
        "cutpoint_supplement": cutpoints,
        "scale": {
            "queries_per_bucket": int(config.queries_per_bucket),
            "seed_count": int(config.seed_count),
            "queries_per_map": int(config.queries_per_map),
            "bucket_names": ["Easy", "Complex", "Extreme"],
            "density_profile_buckets": str(config.density_profile_buckets),
            "distance_bins": str(config.distance_bins),
            "minimum_total_procedural_queries": int(config.queries_per_bucket) * 3,
        },
        "methods": methods,
        "metrics": _metric_records(),
        "real_maps": real_maps,
        "realmap_query_protocol": realmap_query_protocol,
        "blockers": blockers,
        "run_command": _run_command(config, methods),
        "claim_boundaries": [
            "manifest is a protocol artifact, not an experiment result",
            "F02.6 warm-start decision remains external unless warm_start_decision is not pending",
            "real SLAM map query generation is inventoried but not frozen here",
            "missing method implementations cannot be counted as evaluated methods",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Module2 v1 evaluation manifest without running experiments.")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--contract-path", type=Path, default=Module2EvaluationManifestConfig.contract_path)
    parser.add_argument("--cutpoint-supplement-path", type=Path, default=Module2EvaluationManifestConfig.cutpoint_supplement_path)
    parser.add_argument("--realmap-manifest-path", type=Path, default=Module2EvaluationManifestConfig.realmap_manifest_path)
    parser.add_argument("--realmap-query-protocol-path", type=Path, default=None)
    parser.add_argument("--warm-start-decision", choices=("pending", "approved_obstacle_summary", "no_warm_only"), default="pending")
    parser.add_argument("--bc-checkpoint", type=Path, default=None)
    parser.add_argument("--rl-rs-checkpoint", type=Path, default=None)
    parser.add_argument("--queries-per-bucket", type=int, default=100)
    parser.add_argument("--seed-count", type=int, default=5)
    parser.add_argument("--queries-per-map", type=int, default=5)
    parser.add_argument("--density-profile-buckets", choices=("validation_t06", "original_t06"), default="validation_t06")
    parser.add_argument("--distance-bins", default="8:12,12:16,16:20,20:")
    parser.add_argument("--bootstrap-resamples", type=int, default=10_000)
    return parser.parse_args(list(argv) if argv is not None else None)


def _method_records(config: Module2EvaluationManifestConfig) -> list[dict[str, Any]]:
    bc_blockers: list[str] = []
    if config.bc_checkpoint is None:
        bc_blockers.append("missing_module2_bc_checkpoint")
    elif not Path(config.bc_checkpoint).is_file():
        bc_blockers.append("missing_module2_bc_checkpoint")

    records = [
        _method("ha_no_analytic", "HA* no analytic", "ha_no_analytic", "ready"),
        _method("ha_single_rs", "HA* single RS analytic expansion", "ha_single_rs", "ready"),
        _method("ha_dang_multi_rs", "HA* Dang multi-RS analytic expansion", "ha_dang_multi_rs", "ready"),
        _method("f_n3p_knn", "F-N3P KNN subgoal baseline", "f_n3p_knn", "ready_if_preflight_passes"),
        _method("mlp", "F-N3P MLP subgoal baseline", "mlp", "ready"),
        _method(
            "bc_analytic_operator",
            "BC analytic operator",
            "bc_analytic_operator",
            "ready" if not bc_blockers else "blocked",
            blockers=tuple(bc_blockers),
            checkpoint=None if config.bc_checkpoint is None else str(config.bc_checkpoint),
        ),
        _method(
            "ppo_analytic_operator",
            "PPO analytic operator without terminal RS",
            None,
            "blocked",
            blockers=("missing_main_evaluation_method", "outside_current_funnel_contract_until_explicitly_added"),
        ),
    ]
    ppo_blockers: list[str] = []
    if config.rl_rs_checkpoint is None:
        ppo_blockers.append("missing_module2_rl_rs_checkpoint")
    elif not Path(config.rl_rs_checkpoint).is_file():
        ppo_blockers.append("missing_module2_rl_rs_checkpoint")
    if str(config.warm_start_decision) == "pending":
        ppo_blockers.append("f02_6_warm_start_decision_pending")
    records.append(
        _method(
            "ppo_rs_funnel",
            "PPO + terminal RS funnel analytic operator",
            "ha_rl_rs_ppo",
            "ready" if not ppo_blockers else "blocked",
            blockers=tuple(ppo_blockers),
            checkpoint=None if config.rl_rs_checkpoint is None else str(config.rl_rs_checkpoint),
        )
    )
    return records


def _method(
    method_id: str,
    label: str,
    main_evaluation_method: str | None,
    status: str,
    *,
    blockers: Sequence[str] = (),
    checkpoint: str | None = None,
) -> dict[str, Any]:
    return {
        "method_id": method_id,
        "label": label,
        "main_evaluation_method": main_evaluation_method,
        "status": status,
        "blockers": list(blockers),
        "checkpoint": checkpoint,
    }


def _metric_records() -> list[dict[str, str]]:
    return [
        {"metric_id": "total_expansions", "role": "contract_primary", "definition": "Hybrid A* node expansions per query"},
        {"metric_id": "total_time_s", "role": "contract_primary", "definition": "end-to-end wall-clock planning time per query"},
        {"metric_id": "timeout_failure_rate", "role": "contract_primary", "definition": "fraction of queries failing by timeout"},
        {"metric_id": "path_inflation_ratio", "role": "contract_primary", "definition": "path length / reference length - 1 for feasible paths"},
        {"metric_id": "mean_abs_curvature", "role": "path_quality", "definition": "mean absolute heading change per meter"},
        {"metric_id": "min_clearance_m", "role": "path_quality", "definition": "minimum footprint clearance along densified path"},
        {"metric_id": "analytic_success_rate", "role": "diagnostic", "definition": "analytic_successes / analytic_attempts"},
        {"metric_id": "terminal_rs_success_rate", "role": "diagnostic", "definition": "terminal_rs_success_count / analytic_attempts for RL-RS operators"},
        {"metric_id": "fallback_count", "role": "diagnostic", "definition": "F-N3P fallback usage and planner primitive fallback evidence"},
        {"metric_id": "nn_forward_time_s", "role": "diagnostic", "definition": "neural policy forward wall-clock time when available"},
    ]


def _global_blockers(
    config: Module2EvaluationManifestConfig,
    methods: Sequence[dict[str, Any]],
    realmap_query_protocol: dict[str, Any],
) -> list[str]:
    blockers: list[str] = []
    if str(config.warm_start_decision) == "pending":
        blockers.append("f02_6_warm_start_decision_pending")
    if any("missing_module2_bc_checkpoint" in method.get("blockers", ()) for method in methods):
        blockers.append("missing_module2_bc_checkpoint")
    if any("missing_main_evaluation_method" in method.get("blockers", ()) for method in methods):
        blockers.append("missing_required_method_implementation")
    if not bool(realmap_query_protocol.get("frozen")):
        blockers.append("realmap_query_generation_not_frozen")
    return blockers


def _manifest_status(config: Module2EvaluationManifestConfig, methods: Sequence[dict[str, Any]], blockers: Sequence[str]) -> str:
    if str(config.warm_start_decision) == "pending":
        return "blocked_pending_decisions"
    if "missing_required_method_implementation" in blockers:
        return "blocked_missing_implementation"
    if blockers:
        return "blocked_protocol_gap"
    return "ready_for_formal_run"


def _run_command(config: Module2EvaluationManifestConfig, methods: Sequence[dict[str, Any]]) -> dict[str, Any]:
    bc = next(method for method in methods if method["method_id"] == "bc_analytic_operator")
    ppo = next(method for method in methods if method["method_id"] == "ppo_rs_funnel")
    if bc["status"] != "ready":
        return {"formal_main_evaluation": None, "blocked_reasons": list(bc["blockers"])}
    if ppo["status"] != "ready":
        return {"formal_main_evaluation": None, "blocked_reasons": list(ppo["blockers"])}
    method_order = ["ha_no_analytic", "ha_single_rs", "ha_dang_multi_rs", "mlp", "bc_analytic_operator", "ha_rl_rs_ppo"]
    command = (
        "python -m forest_n3p.scripts.run_main_evaluation "
        "--output-dir 0_trials/module2_v1_evaluation/formal_run "
        f"--methods {','.join(method_order)} "
        f"--module2-bc-checkpoint {config.bc_checkpoint} "
        f"--module2-rl-rs-checkpoint {config.rl_rs_checkpoint} "
        f"--queries-per-bucket {int(config.queries_per_bucket)} "
        f"--seed-count {int(config.seed_count)} "
        f"--queries-per-map {int(config.queries_per_map)} "
        f"--density-profile-buckets {config.density_profile_buckets} "
        f"--distance-bins {config.distance_bins} "
        f"--contract-path {config.contract_path} "
        f"--cutpoint-supplement-path {config.cutpoint_supplement_path} "
        f"--bootstrap-resamples {int(config.bootstrap_resamples)}"
    )
    return {
        "formal_main_evaluation": command,
        "blocked_reasons": [],
        "note": "This command covers implemented procedural-map methods only; real-map evaluation remains a separate protocol item.",
    }


def _realmap_record(path: Path) -> dict[str, Any]:
    if not Path(path).exists():
        return {"manifest": str(path), "usable_map_count": 0, "maps": [], "status": "missing_manifest"}
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return {
        "manifest": str(path),
        "usable_map_count": int(payload.get("usable_map_count", 0) or 0),
        "maps": [
            {
                "id": str(item.get("id")),
                "pgm": str(item.get("pgm")),
                "yaml": str(item.get("yaml")),
                "loader_grid_sha256": str(item.get("loader_grid_sha256")),
            }
            for item in payload.get("maps", ())
        ],
        "status": "inventory_available",
    }


def _realmap_query_protocol_record(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {"path": None, "status": "missing", "frozen": False, "endpoint_audit_pass": False}
    protocol_path = Path(path)
    if not protocol_path.is_file():
        return {"path": str(protocol_path), "status": "missing", "frozen": False, "endpoint_audit_pass": False}
    payload = json.loads(protocol_path.read_text(encoding="utf-8"))
    endpoint_audit = payload.get("endpoint_audit") if isinstance(payload.get("endpoint_audit"), dict) else {}
    endpoint_audit_pass = bool(endpoint_audit.get("pass"))
    frozen = str(payload.get("status")) == "frozen" and endpoint_audit_pass
    return {
        "path": str(protocol_path),
        "status": str(payload.get("status")),
        "frozen": bool(frozen),
        "endpoint_audit_pass": bool(endpoint_audit_pass),
        "query_count": int(payload.get("query_count", 0) or 0),
        "query_count_by_map": dict(payload.get("query_count_by_map") or {}),
        "queries_csv": payload.get("queries_csv"),
        "queries_csv_sha256": payload.get("queries_csv_sha256"),
        "query_rows_sha256": payload.get("query_rows_sha256"),
    }


def _frontmatter_record(path: Path, *, keys: Sequence[str]) -> dict[str, Any]:
    record: dict[str, Any] = {"path": str(path), "exists": Path(path).exists()}
    for key in keys:
        record[key] = _frontmatter_value(path, key)
    return record


def _frontmatter_value(path: Path, key: str) -> str | None:
    if not Path(path).exists():
        return None
    text = Path(path).read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    for line in text.splitlines()[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        name, value = line.split(":", 1)
        if name.strip() == key:
            return value.strip().strip('"').strip("'")
    return None




def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop manifest generation.
        return "unknown"


def _manifest_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 v1 Evaluation Manifest",
        "",
        f"- status: `{manifest['status']}`",
        f"- contract: `{manifest['contract']['path']}`",
        f"- scale: `{manifest['scale']['queries_per_bucket']}` queries/bucket, `{manifest['scale']['seed_count']}` seeds",
        "",
        "## Methods",
    ]
    for method in manifest["methods"]:
        blockers = ", ".join(method["blockers"]) if method["blockers"] else "none"
        lines.append(f"- `{method['method_id']}`: {method['status']} (blockers: {blockers})")
    lines.extend(["", "## Blockers"])
    if manifest["blockers"]:
        lines.extend(f"- `{blocker}`" for blocker in manifest["blockers"])
    else:
        lines.append("- none")
    lines.extend(["", "## Formal Command", ""])
    command = manifest["run_command"]["formal_main_evaluation"]
    lines.append("```bash")
    lines.append(command or "# blocked: see blockers above")
    lines.append("```")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
