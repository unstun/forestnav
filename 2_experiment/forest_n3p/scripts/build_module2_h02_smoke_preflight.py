from __future__ import annotations

import argparse
import json
import shlex
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence


DEFAULT_H01_MANIFEST = Path("0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json")
DEFAULT_METRIC_PROTOCOL = Path("0_trials/module2_metric_protocol/module2_metric_protocol.json")
DEFAULT_BC_CHECKPOINT = Path("2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt")
DEFAULT_OUTPUT_DIR = Path("0_trials/module2_h02_local_smoke/h02_1_available_subset")
REQUIRED_METHOD_IDS = (
    "ha_no_analytic",
    "ha_single_rs",
    "ha_dang_multi_rs",
    "mlp",
    "bc_analytic_operator",
    "ppo_analytic_operator",
    "ppo_rs_funnel",
)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    manifest = build_preflight(
        output_dir=args.output_dir,
        h01_manifest_path=args.h01_manifest,
        metric_protocol_path=args.metric_protocol,
        bc_checkpoint=args.bc_checkpoint,
        rl_rs_checkpoint=args.rl_rs_checkpoint,
        smoke_run_output_dir=args.smoke_run_output_dir,
    )
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = args.manifest_out or output_dir / "h02_local_smoke_preflight.json"
    markdown_out = args.markdown_out or output_dir / "h02_local_smoke_preflight.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_preflight(
    *,
    output_dir: Path,
    h01_manifest_path: Path = DEFAULT_H01_MANIFEST,
    metric_protocol_path: Path = DEFAULT_METRIC_PROTOCOL,
    bc_checkpoint: Path | None = DEFAULT_BC_CHECKPOINT,
    rl_rs_checkpoint: Path | None = None,
    smoke_run_output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    h01_manifest = _read_json(h01_manifest_path)
    metric_protocol = _read_json(metric_protocol_path) if Path(metric_protocol_path).is_file() else {}
    method_records = {str(item.get("method_id")): item for item in h01_manifest.get("methods", ()) if isinstance(item, dict)}
    required_methods = [_method_status(method_id, method_records.get(method_id)) for method_id in REQUIRED_METHOD_IDS]
    blocked_methods = [item for item in required_methods if item["status"] != "ready"]
    available_methods = [item for item in required_methods if item["status"] == "ready"]
    available_eval_methods = [str(item["main_evaluation_method"]) for item in available_methods if item.get("main_evaluation_method")]

    blockers: list[str] = []
    if blocked_methods:
        blockers.append("missing_required_methods_for_full_h02_1_smoke")
    if not metric_protocol or metric_protocol.get("status") != "frozen":
        blockers.append("metric_protocol_not_frozen")
    if bc_checkpoint is None or not Path(bc_checkpoint).is_file():
        blockers.append("missing_bc_checkpoint_for_available_subset")
    if rl_rs_checkpoint is not None and not Path(rl_rs_checkpoint).is_file():
        blockers.append("missing_rl_rs_checkpoint_path")

    return {
        "schema_version": 1,
        "preflight_name": "module2_h02_local_smoke_preflight",
        "status": "ready_for_full_smoke" if not blockers else "blocked_full_smoke_missing_required_methods",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "h01_manifest": str(h01_manifest_path),
        "metric_protocol": str(metric_protocol_path),
        "formal_claim_allowed": False,
        "local_training_allowed": False,
        "full_method_smoke_ready": not blockers,
        "required_methods": required_methods,
        "blocked_methods": blocked_methods,
        "blockers": blockers,
        "available_subset": {
            "status": "ready" if available_eval_methods and "missing_bc_checkpoint_for_available_subset" not in blockers else "blocked",
            "methods": available_eval_methods,
            "run_output_dir": str(smoke_run_output_dir),
            "run_command": _available_subset_command(
                methods=available_eval_methods,
                output_dir=smoke_run_output_dir,
                bc_checkpoint=bc_checkpoint,
            ),
        },
        "claim_boundaries": [
            "This is a local smoke protocol/preflight artifact, not a formal evaluation result.",
            "It must not run local PPO training.",
            "Full H02.1 remains blocked until ppo_analytic_operator and ppo_rs_funnel have a real RL-RS checkpoint.",
            "Available-subset smoke cannot be relabeled as all-method smoke.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Module2 H02.1 local targeted smoke preflight.")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--h01-manifest", type=Path, default=DEFAULT_H01_MANIFEST)
    parser.add_argument("--metric-protocol", type=Path, default=DEFAULT_METRIC_PROTOCOL)
    parser.add_argument("--bc-checkpoint", type=Path, default=DEFAULT_BC_CHECKPOINT)
    parser.add_argument("--rl-rs-checkpoint", type=Path, default=None)
    parser.add_argument("--smoke-run-output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(list(argv) if argv is not None else None)


def _method_status(method_id: str, record: dict[str, Any] | None) -> dict[str, Any]:
    if record is None:
        return {
            "method_id": method_id,
            "main_evaluation_method": None,
            "status": "blocked",
            "blockers": ["missing_from_h01_manifest"],
        }
    return {
        "method_id": method_id,
        "main_evaluation_method": record.get("main_evaluation_method"),
        "status": str(record.get("status")),
        "blockers": list(record.get("blockers") or ()),
        "checkpoint": record.get("checkpoint"),
    }


def _available_subset_command(*, methods: Sequence[str], output_dir: Path, bc_checkpoint: Path | None) -> str:
    argv = [
        "python",
        "-m",
        "forest_n3p.scripts.run_main_evaluation",
        "--output-dir",
        str(output_dir),
        "--methods",
        ",".join(methods),
        "--queries-per-bucket",
        "1",
        "--seed-count",
        "1",
        "--queries-per-map",
        "1",
        "--density-profile-buckets",
        "validation_t06",
        "--contract-path",
        ".pipeline/contracts/module2-ppo-funnel-expansion.md",
        "--cutpoint-supplement-path",
        ".pipeline/contracts/v9-forest-n3p-t06-calibration-supplement.md",
        "--allow-unresolved-human-review",
        "--no-enforce-t14-scale",
    ]
    if bc_checkpoint is not None and "bc_analytic_operator" in methods:
        argv.extend(["--module2-bc-checkpoint", str(bc_checkpoint)])
    return " ".join(shlex.quote(str(part)) for part in argv)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop preflight generation.
        return "unknown"


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 H02.1 Local Smoke Preflight",
        "",
        f"- status: `{manifest['status']}`",
        f"- full method smoke ready: `{manifest['full_method_smoke_ready']}`",
        f"- local training allowed: `{manifest['local_training_allowed']}`",
        "",
        "## Blocked Methods",
    ]
    if manifest["blocked_methods"]:
        for method in manifest["blocked_methods"]:
            blockers = ", ".join(method["blockers"]) if method["blockers"] else "none"
            lines.append(f"- `{method['method_id']}`: {blockers}")
    else:
        lines.append("- none")
    lines.extend(["", "## Available Subset Command", "", "```bash", manifest["available_subset"]["run_command"], "```"])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
