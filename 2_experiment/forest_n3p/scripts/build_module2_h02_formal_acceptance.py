from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_h02_formal_acceptance")
DEFAULT_EVALUATION_DIR = Path("0_trials/module2_h02_local_smoke/h02_1_available_subset")
DEFAULT_H01_MANIFEST = Path("0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json")
DEFAULT_REMOTE_EXECUTION_PACKET = Path("0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json")
DEFAULT_GATE3_AUDIT = Path("0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json")
READY_H01_STATUSES = {"ready", "formal_ready", "ready_for_formal_run", "ready_for_formal_evaluation"}
PPO_METHODS = {"ha_rl_rs_ppo", "ppo_analytic_operator"}


@dataclass(frozen=True)
class H02FormalAcceptanceConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    evaluation_dir: Path = DEFAULT_EVALUATION_DIR
    h01_manifest_path: Path = DEFAULT_H01_MANIFEST
    remote_execution_packet_path: Path = DEFAULT_REMOTE_EXECUTION_PACKET
    gate3_audit_path: Path = DEFAULT_GATE3_AUDIT


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = H02FormalAcceptanceConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        evaluation_dir=args.evaluation_dir,
        h01_manifest_path=args.h01_manifest,
        remote_execution_packet_path=args.remote_execution_packet,
        gate3_audit_path=args.gate3_audit,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "h02_formal_acceptance.json"
    markdown_out = config.markdown_out or output_dir / "h02_formal_acceptance.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: H02FormalAcceptanceConfig) -> dict[str, Any]:
    evaluation_dir = Path(config.evaluation_dir)
    paths = _evaluation_paths(evaluation_dir)
    h01_manifest = _read_json(config.h01_manifest_path)
    remote_packet = _read_json(config.remote_execution_packet_path)
    gate3_audit = _read_json_if_exists(config.gate3_audit_path)
    records = _read_records(paths["records_csv"]) if paths["records_csv"].is_file() else []
    summary_rows = _read_records(paths["summary_by_method_bucket_csv"]) if paths["summary_by_method_bucket_csv"].is_file() else []
    summary_json = _read_json_if_exists(paths["summary_json"])
    verdict = _read_json_if_exists(paths["verdict_json"])
    run_config = _read_json_if_exists(paths["run_config_json"])

    schema_checks = _schema_checks(
        h01_manifest=h01_manifest,
        records_path=paths["records_csv"],
        summary_csv_path=paths["summary_by_method_bucket_csv"],
        summary_json_path=paths["summary_json"],
        records=records,
        summary_rows=summary_rows,
        summary_json=summary_json,
    )
    formal_checks = _formal_checks(
        h01_manifest=h01_manifest,
        verdict=verdict,
        run_config=run_config,
        remote_packet=remote_packet,
        gate3_audit=gate3_audit,
        gate3_audit_path=config.gate3_audit_path,
    )
    method_checks = _method_checks(records)
    pullback_checks = _pullback_checks(remote_packet)
    formal_checks["remote_pullback_artifacts_present"] = pullback_checks["remote_pullback_artifacts_present"]
    blockers = _blockers(
        schema_checks=schema_checks,
        formal_checks=formal_checks,
        method_checks=method_checks,
        pullback_checks=pullback_checks,
        h01_manifest=h01_manifest,
        remote_packet=remote_packet,
    )
    accepted = not blockers
    formal_requirements = _formal_acceptance_requirements(
        schema_checks=schema_checks,
        formal_checks=formal_checks,
        method_checks=method_checks,
        pullback_checks=pullback_checks,
        accepted=accepted,
    )
    return {
        "schema_version": 1,
        "artifact_name": "module2_h02_formal_acceptance",
        "status": "formal_output_accepted" if accepted else "blocked_formal_output_acceptance",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "formal_output_accepted": accepted,
        "paper_result_input_allowed": accepted,
        "local_training_allowed": False,
        "inputs": {
            "evaluation_dir": str(evaluation_dir),
            "records_csv": str(paths["records_csv"]),
            "summary_by_method_bucket_csv": str(paths["summary_by_method_bucket_csv"]),
            "summary_json": str(paths["summary_json"]),
            "verdict_json": str(paths["verdict_json"]),
            "run_config_json": str(paths["run_config_json"]),
            "h01_manifest": str(config.h01_manifest_path),
            "remote_execution_packet": str(config.remote_execution_packet_path),
            "gate3_audit": str(config.gate3_audit_path),
        },
        "blockers": blockers,
        "schema_checks": schema_checks,
        "formal_checks": formal_checks,
        "method_checks": method_checks,
        "pullback_checks": pullback_checks,
        "formal_acceptance_requirements": formal_requirements,
        "formal_acceptance_requirement_counts": _requirement_counts(formal_requirements),
        "claim_boundaries": [
            "This audit accepts or rejects H02 formal output inputs; it is not itself a paper result table.",
            "Candidate/smoke H02 outputs must remain blocked even if their CSV schema is valid.",
            "Gate3 formal audit must pass and be pulled back before H02 outputs can feed paper tables.",
            "All formal records and summaries must satisfy H01 required_output_schema.",
            "PPO checkpoint rows must include a non-empty checkpoint hash before formal performance claims.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit Module2 H02 formal output acceptance without running training.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--evaluation-dir", type=Path, default=DEFAULT_EVALUATION_DIR)
    parser.add_argument("--h01-manifest", type=Path, default=DEFAULT_H01_MANIFEST)
    parser.add_argument("--remote-execution-packet", type=Path, default=DEFAULT_REMOTE_EXECUTION_PACKET)
    parser.add_argument("--gate3-audit", type=Path, default=DEFAULT_GATE3_AUDIT)
    return parser.parse_args(list(argv) if argv is not None else None)


def _evaluation_paths(evaluation_dir: Path) -> dict[str, Path]:
    return {
        "records_csv": evaluation_dir / "records.csv",
        "summary_by_method_bucket_csv": evaluation_dir / "summary_by_method_bucket.csv",
        "summary_json": evaluation_dir / "summary.json",
        "verdict_json": evaluation_dir / "verdict.json",
        "run_config_json": evaluation_dir / "run_config.json",
    }


def _schema_checks(
    *,
    h01_manifest: dict[str, Any],
    records_path: Path,
    summary_csv_path: Path,
    summary_json_path: Path,
    records: Sequence[dict[str, str]],
    summary_rows: Sequence[dict[str, str]],
    summary_json: dict[str, Any],
) -> dict[str, Any]:
    required = h01_manifest.get("required_output_schema") if isinstance(h01_manifest.get("required_output_schema"), dict) else {}
    record_required = [str(item) for item in required.get("records_csv_required_columns", ()) if item]
    summary_required = [str(item) for item in required.get("summary_by_method_bucket_required_columns", ()) if item]
    section_required = [str(item) for item in required.get("summary_json_required_sections", ()) if item]
    record_columns = list(records[0].keys()) if records else _csv_columns(records_path)
    summary_columns = list(summary_rows[0].keys()) if summary_rows else _csv_columns(summary_csv_path)
    return {
        "h01_schema_status": required.get("schema_status"),
        "records_csv": {
            "path": str(records_path),
            "exists": records_path.is_file(),
            "row_count": len(records),
            "required_count": len(record_required),
            "observed_count": len(record_columns),
            "missing_columns": [column for column in record_required if column not in record_columns],
        },
        "summary_by_method_bucket_csv": {
            "path": str(summary_csv_path),
            "exists": summary_csv_path.is_file(),
            "row_count": len(summary_rows),
            "required_count": len(summary_required),
            "observed_count": len(summary_columns),
            "missing_columns": [column for column in summary_required if column not in summary_columns],
        },
        "summary_json": {
            "path": str(summary_json_path),
            "exists": summary_json_path.is_file(),
            "missing_sections": [section for section in section_required if section not in summary_json],
        },
    }


def _formal_checks(
    *,
    h01_manifest: dict[str, Any],
    verdict: dict[str, Any],
    run_config: dict[str, Any],
    remote_packet: dict[str, Any],
    gate3_audit: dict[str, Any],
    gate3_audit_path: Path,
) -> dict[str, Any]:
    h01_scale = h01_manifest.get("scale") if isinstance(h01_manifest.get("scale"), dict) else {}
    cfg = run_config.get("config") if isinstance(run_config.get("config"), dict) else {}
    scale_checks = {
        "queries_per_bucket": _scale_item(cfg, h01_scale, "queries_per_bucket"),
        "seed_count": _scale_item(cfg, h01_scale, "seed_count"),
        "queries_per_map": _scale_item(cfg, h01_scale, "queries_per_map"),
    }
    return {
        "h02_verdict_status": verdict.get("status"),
        "h02_verdict_formal_acceptance": verdict.get("formal_acceptance") is True,
        "h01_manifest_status": h01_manifest.get("status"),
        "h01_manifest_ready": str(h01_manifest.get("status")) in READY_H01_STATUSES,
        "h01_blockers": [str(item) for item in h01_manifest.get("blockers", ()) if item],
        "remote_execution_packet_status": remote_packet.get("status"),
        "remote_execution_packet_ready": bool(remote_packet.get("ready_to_run_remote_training")),
        "remote_packet_blockers": [str(item) for item in remote_packet.get("blockers", ()) if item],
        "gate3_audit_path": str(gate3_audit_path),
        "gate3_audit_exists": gate3_audit_path.is_file(),
        "gate3_formal_decision": gate3_audit.get("formal_decision"),
        "gate3_formal_claim_allowed": gate3_audit.get("formal_claim_allowed"),
        "gate3_formal_audit_passed": gate3_audit.get("formal_decision") == "pass" and gate3_audit.get("formal_claim_allowed") is True,
        "scale_checks": scale_checks,
        "scale_satisfies_h01": all(item["satisfied"] for item in scale_checks.values()),
    }


def _method_checks(records: Sequence[dict[str, str]]) -> dict[str, Any]:
    methods = sorted({str(row.get("method", "")) for row in records if row.get("method")})
    ppo_rows = [row for row in records if str(row.get("method", "")) in PPO_METHODS]
    hashes = sorted({str(row.get("rl_rs_checkpoint_sha256", "")).strip() for row in ppo_rows if str(row.get("rl_rs_checkpoint_sha256", "")).strip()})
    return {
        "record_count": len(records),
        "methods": methods,
        "ppo_methods": sorted({str(row.get("method", "")) for row in ppo_rows if row.get("method")}),
        "ppo_row_count": len(ppo_rows),
        "has_ppo_result_rows": bool(ppo_rows),
        "ppo_checkpoint_hashes": hashes,
        "ppo_rows_have_checkpoint_hash": bool(ppo_rows) and len(hashes) > 0,
    }


def _pullback_checks(remote_packet: dict[str, Any]) -> dict[str, Any]:
    pullback = remote_packet.get("post_run_pullback") if isinstance(remote_packet.get("post_run_pullback"), dict) else {}
    expected = [str(item) for item in pullback.get("expected_artifacts", ()) if item]
    missing = [path for path in expected if not Path(path).is_file()]
    return {
        "required_before_local_claim": bool(pullback.get("required_before_local_claim")),
        "expected_artifact_count": len(expected),
        "missing_artifacts": missing,
        "remote_pullback_artifacts_present": bool(expected) and not missing,
    }


def _blockers(
    *,
    schema_checks: dict[str, Any],
    formal_checks: dict[str, Any],
    method_checks: dict[str, Any],
    pullback_checks: dict[str, Any],
    h01_manifest: dict[str, Any],
    remote_packet: dict[str, Any],
) -> list[str]:
    blockers: list[str] = []
    if schema_checks["h01_schema_status"] != "frozen_for_module2_v1":
        blockers.append("h01_required_output_schema_not_frozen")
    if schema_checks["records_csv"]["missing_columns"]:
        blockers.append("records_csv_missing_required_columns")
    if not schema_checks["records_csv"]["exists"] or schema_checks["records_csv"]["row_count"] == 0:
        blockers.append("missing_records_csv_rows")
    if schema_checks["summary_by_method_bucket_csv"]["missing_columns"]:
        blockers.append("summary_by_method_bucket_csv_missing_required_columns")
    if not schema_checks["summary_by_method_bucket_csv"]["exists"] or schema_checks["summary_by_method_bucket_csv"]["row_count"] == 0:
        blockers.append("missing_summary_by_method_bucket_rows")
    if schema_checks["summary_json"]["missing_sections"]:
        blockers.append("summary_json_missing_required_sections")
    if not formal_checks["h02_verdict_formal_acceptance"]:
        blockers.append("h02_verdict_not_formal")
    if not formal_checks["h01_manifest_ready"]:
        blockers.append("h01_manifest_not_ready")
    for blocker in formal_checks["h01_blockers"]:
        _append_unique(blockers, blocker)
    if not formal_checks["remote_execution_packet_ready"]:
        blockers.append("remote_execution_packet_not_ready")
    for blocker in formal_checks["remote_packet_blockers"]:
        _append_unique(blockers, blocker)
    if not formal_checks["gate3_audit_exists"]:
        blockers.append("missing_gate3_formal_audit")
    elif not formal_checks["gate3_formal_audit_passed"]:
        blockers.append("gate3_formal_audit_not_passed")
    if not formal_checks["scale_satisfies_h01"]:
        blockers.append("h02_scale_below_h01_manifest")
    if not method_checks["has_ppo_result_rows"]:
        blockers.append("missing_ppo_result_rows")
    elif not method_checks["ppo_rows_have_checkpoint_hash"]:
        blockers.append("ppo_rows_missing_checkpoint_hash")
    if pullback_checks["required_before_local_claim"] and not pullback_checks["remote_pullback_artifacts_present"]:
        blockers.append("missing_remote_pullback_artifacts")
    if h01_manifest.get("status") == "blocked_pending_decisions" and remote_packet.get("status") == "blocked_until_f02_6_decision":
        _append_unique(blockers, "f02_6_formal_chain_pending")
    return _unique(blockers)


def _formal_acceptance_requirements(
    *,
    schema_checks: dict[str, Any],
    formal_checks: dict[str, Any],
    method_checks: dict[str, Any],
    pullback_checks: dict[str, Any],
    accepted: bool,
) -> list[dict[str, Any]]:
    schema_missing = _schema_missing_artifacts(schema_checks)
    scope_missing = _scope_missing_artifacts(formal_checks)
    audit_missing = _audit_pullback_missing_artifacts(formal_checks, pullback_checks)
    ppo_missing = _ppo_missing_artifacts(method_checks)
    return [
        _requirement(
            requirement_id="h01_schema_and_h02_output_schema_match",
            phase="schema_acceptance",
            complete=not schema_missing,
            paper_result_input_allowed_now=accepted,
            required_before="h02_formal_output_acceptance",
            missing_artifact_ids=schema_missing,
            acceptable_evidence=[
                "H01 required_output_schema has schema_status=frozen_for_module2_v1",
                "records.csv contains all H01 required columns",
                "summary_by_method_bucket.csv and summary.json contain all H01 required fields",
            ],
            invalid_substitutes=[
                "CSV files with extra columns but missing required telemetry",
                "paper table preview generated before H02 acceptance",
                "summary JSON missing paired tests or bootstrap CI sections",
            ],
        ),
        _requirement(
            requirement_id="h02_formal_scope_and_scale_match_h01",
            phase="formal_scope",
            complete=not scope_missing,
            paper_result_input_allowed_now=accepted,
            required_before="paper_table_generation",
            missing_artifact_ids=scope_missing,
            acceptable_evidence=[
                "verdict.json has formal_acceptance=true",
                "H01 manifest status is ready for formal run/evaluation",
                "run_config scale satisfies H01 queries_per_bucket, seed_count, and queries_per_map",
            ],
            invalid_substitutes=[
                "candidate_or_smoke verdict",
                "available-subset smoke scale",
                "blocked H01 manifest with pending F02.6 or missing checkpoint blockers",
            ],
        ),
        _requirement(
            requirement_id="gate3_audit_and_pullback_acceptance",
            phase="remote_acceptance",
            complete=not audit_missing,
            paper_result_input_allowed_now=accepted,
            required_before="h02_formal_output_acceptance",
            missing_artifact_ids=audit_missing,
            acceptable_evidence=[
                "gate3_formal_audit.json exists locally and records formal_decision=pass",
                "remote packet pullback artifacts are all present locally",
                "formal audit and pullback correspond to approved_obstacle_summary warm-start run",
            ],
            invalid_substitutes=[
                "remote stdout without local pullback",
                "not_formal, candidate, smoke, preview, or no-warm Gate3 audit",
                "partial pullback without train/eval/audit artifacts",
            ],
        ),
        _requirement(
            requirement_id="ppo_rows_and_checkpoint_hash_present",
            phase="result_rows",
            complete=not ppo_missing,
            paper_result_input_allowed_now=accepted,
            required_before="paper_result_gate",
            missing_artifact_ids=ppo_missing,
            acceptable_evidence=[
                "records.csv includes ha_rl_rs_ppo or ppo_analytic_operator rows",
                "PPO rows include non-empty rl_rs_checkpoint_sha256",
                "checkpoint hash matches the pulled-back formal checkpoint used by H01/H02",
            ],
            invalid_substitutes=[
                "BC analytic rows used as PPO result rows",
                "PPO rows with empty checkpoint hash",
                "checkpoint hash from a smoke or no-warm run",
            ],
        ),
    ]


def _requirement(
    *,
    requirement_id: str,
    phase: str,
    complete: bool,
    paper_result_input_allowed_now: bool,
    required_before: str,
    missing_artifact_ids: Sequence[str],
    acceptable_evidence: Sequence[str],
    invalid_substitutes: Sequence[str],
) -> dict[str, Any]:
    return {
        "requirement_id": requirement_id,
        "phase": phase,
        "status": "satisfied" if complete else "blocked_formal_acceptance",
        "complete": complete,
        "paper_result_input_allowed_now": paper_result_input_allowed_now and complete,
        "required_before": required_before,
        "missing_artifact_ids": list(missing_artifact_ids),
        "acceptable_evidence": list(acceptable_evidence),
        "invalid_substitutes": list(invalid_substitutes),
    }


def _schema_missing_artifacts(schema_checks: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    if schema_checks.get("h01_schema_status") != "frozen_for_module2_v1":
        missing.append("h01_required_output_schema_frozen")
    records = schema_checks.get("records_csv") if isinstance(schema_checks.get("records_csv"), dict) else {}
    if not records.get("exists") or int(records.get("row_count") or 0) == 0:
        missing.append("records_csv_rows")
    missing.extend(f"records_csv_column_{column}" for column in records.get("missing_columns", ()) if column)
    summary_csv = schema_checks.get("summary_by_method_bucket_csv") if isinstance(schema_checks.get("summary_by_method_bucket_csv"), dict) else {}
    if not summary_csv.get("exists") or int(summary_csv.get("row_count") or 0) == 0:
        missing.append("summary_by_method_bucket_rows")
    missing.extend(f"summary_by_method_bucket_column_{column}" for column in summary_csv.get("missing_columns", ()) if column)
    summary_json = schema_checks.get("summary_json") if isinstance(schema_checks.get("summary_json"), dict) else {}
    if not summary_json.get("exists"):
        missing.append("summary_json")
    missing.extend(f"summary_json_section_{section}" for section in summary_json.get("missing_sections", ()) if section)
    return _unique(missing)


def _scope_missing_artifacts(formal_checks: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    if formal_checks.get("h02_verdict_formal_acceptance") is not True:
        missing.append("h02_verdict_formal_acceptance_true")
    if formal_checks.get("h01_manifest_ready") is not True:
        missing.append("h01_manifest_ready")
    missing.extend(f"h01_blocker_{blocker}" for blocker in formal_checks.get("h01_blockers", ()) if blocker)
    if formal_checks.get("remote_execution_packet_ready") is not True:
        missing.append("remote_execution_packet_ready")
    missing.extend(f"remote_packet_blocker_{blocker}" for blocker in formal_checks.get("remote_packet_blockers", ()) if blocker)
    if formal_checks.get("scale_satisfies_h01") is not True:
        missing.append("h02_scale_satisfies_h01")
    return _unique(missing)


def _audit_pullback_missing_artifacts(formal_checks: dict[str, Any], pullback_checks: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    if formal_checks.get("gate3_audit_exists") is not True:
        missing.append("gate3_formal_audit_json")
    elif formal_checks.get("gate3_formal_audit_passed") is not True:
        missing.append("gate3_formal_audit_pass")
    if pullback_checks.get("required_before_local_claim") is True and pullback_checks.get("remote_pullback_artifacts_present") is not True:
        missing.append("remote_pullback_artifacts")
    missing.extend(f"pullback_missing_{index}" for index, _ in enumerate(pullback_checks.get("missing_artifacts", ()), start=1))
    return _unique(missing)


def _ppo_missing_artifacts(method_checks: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    if method_checks.get("has_ppo_result_rows") is not True:
        missing.append("ppo_result_rows")
    elif method_checks.get("ppo_rows_have_checkpoint_hash") is not True:
        missing.append("ppo_checkpoint_hash")
    return missing


def _requirement_counts(requirements: Sequence[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for requirement in requirements:
        status = str(requirement.get("status") or "unknown")
        counts[status] = counts.get(status, 0) + 1
    return counts


def _scale_item(run_config: dict[str, Any], h01_scale: dict[str, Any], key: str) -> dict[str, Any]:
    observed = _to_number(run_config.get(key))
    required = _to_number(h01_scale.get(key))
    if required is None:
        return {"observed": observed, "required": required, "satisfied": True}
    return {"observed": observed, "required": required, "satisfied": observed is not None and observed >= required}


def _read_records(path: Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _csv_columns(path: Path) -> list[str]:
    if not Path(path).is_file():
        return []
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle).fieldnames or [])


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _read_json_if_exists(path: Path) -> dict[str, Any]:
    return _read_json(path) if Path(path).is_file() else {}


def _to_number(value: Any) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _append_unique(items: list[str], item: str) -> None:
    if item and item not in items:
        items.append(item)


def _unique(items: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop audit generation.
        return "unknown"


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 H02 Formal Acceptance",
        "",
        f"- status: `{manifest['status']}`",
        f"- formal output accepted: `{manifest['formal_output_accepted']}`",
        f"- paper result input allowed: `{manifest['paper_result_input_allowed']}`",
        f"- local training allowed: `{manifest['local_training_allowed']}`",
        "",
        "## Blockers",
        "",
    ]
    if manifest["blockers"]:
        lines.extend(f"- `{item}`" for item in manifest["blockers"])
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Schema Checks",
            "",
            f"- records missing columns: `{manifest['schema_checks']['records_csv']['missing_columns']}`",
            f"- summary CSV missing columns: `{manifest['schema_checks']['summary_by_method_bucket_csv']['missing_columns']}`",
            f"- summary JSON missing sections: `{manifest['schema_checks']['summary_json']['missing_sections']}`",
            "",
            "## Formal Checks",
            "",
            f"- H02 verdict formal: `{manifest['formal_checks']['h02_verdict_formal_acceptance']}`",
            f"- H01 ready: `{manifest['formal_checks']['h01_manifest_ready']}`",
            f"- remote packet ready: `{manifest['formal_checks']['remote_execution_packet_ready']}`",
            f"- Gate3 audit passed: `{manifest['formal_checks']['gate3_formal_audit_passed']}`",
            f"- scale satisfies H01: `{manifest['formal_checks']['scale_satisfies_h01']}`",
            f"- PPO result rows: `{manifest['method_checks']['ppo_row_count']}`",
            f"- pullback artifacts present: `{manifest['pullback_checks']['remote_pullback_artifacts_present']}`",
            "",
            "## Formal Acceptance Requirements",
            "",
        ]
    )
    for requirement in manifest["formal_acceptance_requirements"]:
        lines.append(
            f"- `{requirement['requirement_id']}` ({requirement['phase']}): "
            f"status=`{requirement['status']}`, paper_result_input_allowed_now=`{requirement['paper_result_input_allowed_now']}`"
        )
        if requirement["missing_artifact_ids"]:
            lines.append(f"  - missing_artifact_ids: `{', '.join(requirement['missing_artifact_ids'])}`")
        lines.append(f"  - invalid_substitutes: `{'; '.join(requirement['invalid_substitutes'])}`")
    lines.extend(
        [
            "## Claim Boundaries",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in manifest["claim_boundaries"])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
