from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import zipfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_formal_gate_proof_audit")
DEFAULT_REMAINING_DELIVERABLES = Path(
    "0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json"
)
STATUS_KEYS = ("passed", "failed", "blocked_missing_artifact")
CATEGORY_BLOCKER_PREFIX = {
    "training": "formal_training_artifacts",
    "evaluation": "formal_evaluation_artifacts",
    "acceptance": "formal_acceptance_artifacts",
    "formal_acceptance": "formal_h01_h02_acceptance_artifacts",
}


@dataclass(frozen=True)
class FormalGateProofAuditConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    remaining_deliverables_path: Path = DEFAULT_REMAINING_DELIVERABLES
    workspace_root: Path = Path(".")


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = FormalGateProofAuditConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        remaining_deliverables_path=args.remaining_deliverables,
        workspace_root=args.workspace_root,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "formal_gate_proof_audit.json"
    markdown_out = config.markdown_out or output_dir / "formal_gate_proof_audit.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: FormalGateProofAuditConfig) -> dict[str, Any]:
    remaining = _read_json(config.remaining_deliverables_path)
    plan = remaining.get("proof_command_plan") if isinstance(remaining.get("proof_command_plan"), dict) else {}
    matrix = remaining.get("deliverable_acceptance_matrix")
    matrix = matrix if isinstance(matrix, list) else []
    input_safety_issues = _input_safety_issues(remaining=remaining, plan=plan, matrix=matrix)
    results = _proof_command_results(matrix=matrix, workspace_root=Path(config.workspace_root))
    category_status_counts = _category_status_counts(results)
    blockers = _blockers(category_status_counts=category_status_counts, input_safety_issues=input_safety_issues)
    total_proof_command_count = len(results)
    passed_count = sum(1 for result in results if result["status"] == "passed")
    failed_count = sum(1 for result in results if result["status"] == "failed")
    blocked_count = sum(1 for result in results if result["status"] == "blocked_missing_artifact")
    proof_command_summary = {
        "total_matrix_rows": int(plan.get("total_matrix_rows") or len(matrix)),
        "total_proof_command_count": total_proof_command_count,
        "passed_proof_command_count": passed_count,
        "failed_proof_command_count": failed_count,
        "blocked_proof_command_count": blocked_count,
    }
    status = "formal_gate_proof_audit_passed" if not blockers and total_proof_command_count > 0 else "formal_gate_proof_audit_blocked"
    return {
        "schema_version": 1,
        "artifact_name": "module2_formal_gate_proof_audit",
        "status": status,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "inputs": {
            "formal_gate_remaining_deliverables": str(config.remaining_deliverables_path),
            "workspace_root": str(config.workspace_root),
        },
        "current_state": _current_state(remaining),
        "remaining_deliverables_top_level_summary": _remaining_deliverables_top_level_summary(remaining),
        "proof_command_plan_id": plan.get("plan_id"),
        "execution_boundary": plan.get("execution_boundary"),
        "total_matrix_rows": proof_command_summary["total_matrix_rows"],
        "total_proof_command_count": total_proof_command_count,
        "declared_total_proof_command_count": int(plan.get("total_proof_command_count") or 0),
        "passed_proof_command_count": passed_count,
        "failed_proof_command_count": failed_count,
        "blocked_proof_command_count": blocked_count,
        "proof_command_summary": proof_command_summary,
        "formal_gate_missing_evidence_summary": _formal_gate_missing_evidence_summary(results),
        "category_status_counts": category_status_counts,
        "blockers": blockers,
        "input_safety_issue_count": len(input_safety_issues),
        "input_safety_issues": input_safety_issues,
        "proof_command_results": results,
        "proof_command_results_by_id": {result["command_id"]: result for result in results},
        "claim_boundaries": [
            "This proof audit performs local read-only filesystem and metadata checks only.",
            "It does not execute proof command strings, run training, run remote preflight, ssh, rsync, evaluate, audit, or pull back artifacts.",
            "Missing proof-command evidence keeps the formal gate blocked and is not paper result material.",
            "Passing this audit alone would still not authorize a formal paper claim without the upstream contract, F02.6, H01/H02, and claim-safety gates.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate Module2 formal-gate proof commands with local read-only checks.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--remaining-deliverables", type=Path, default=DEFAULT_REMAINING_DELIVERABLES)
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    return parser.parse_args(list(argv) if argv is not None else None)


def _current_state(remaining: dict[str, Any]) -> dict[str, Any]:
    current_gate = (
        remaining.get("current_gate_summary")
        if isinstance(remaining.get("current_gate_summary"), dict)
        else {}
    )
    permissions = remaining.get("permissions_now") if isinstance(remaining.get("permissions_now"), dict) else {}
    gap = (
        remaining.get("deliverable_gap_summary")
        if isinstance(remaining.get("deliverable_gap_summary"), dict)
        else {}
    )
    return {
        "remaining_deliverables_status": remaining.get("status"),
        "remaining_missing_deliverable_count": _int_or_none(
            remaining.get("missing_deliverable_count", gap.get("total_missing_deliverables"))
        ),
        "remaining_open_category_count": _int_or_none(
            remaining.get("open_category_count", gap.get("open_category_count"))
        ),
        "source_freshness_ready_for_remote_preflight": permissions.get(
            "source_freshness_ready_for_remote_preflight",
            current_gate.get("source_freshness_ready_for_remote_preflight"),
        ),
        "source_freshness_status": current_gate.get("source_freshness_status"),
        "source_freshness_regeneration_required": current_gate.get(
            "source_freshness_regeneration_required"
        ),
        "source_freshness_non_self_changed_records": current_gate.get(
            "source_freshness_non_self_changed_records"
        ),
        "source_freshness_self_artifact_only_lag_records": current_gate.get(
            "source_freshness_self_artifact_only_lag_records"
        ),
    }


def _remaining_deliverables_top_level_summary(remaining: dict[str, Any]) -> dict[str, Any]:
    counts = (
        remaining.get("missing_counts_by_formal_category")
        if isinstance(remaining.get("missing_counts_by_formal_category"), dict)
        else {}
    )
    matrix_ids = (
        remaining.get("missing_matrix_ids_by_formal_category")
        if isinstance(remaining.get("missing_matrix_ids_by_formal_category"), dict)
        else {}
    )
    return {
        "present": bool(counts or matrix_ids),
        "missing_counts_by_formal_category": {
            str(category): int(count) for category, count in counts.items()
        },
        "missing_matrix_ids_by_formal_category": {
            str(category): [str(item) for item in items] if isinstance(items, list) else []
            for category, items in matrix_ids.items()
        },
        "next_blocked_lane": remaining.get("next_blocked_lane"),
        "h01_status": remaining.get("h01_status"),
        "h02_status": remaining.get("h02_status"),
        "h02_formal_output_accepted": remaining.get("h02_formal_output_accepted"),
        "h02_paper_result_input_allowed": remaining.get("h02_paper_result_input_allowed"),
    }


def _formal_gate_missing_evidence_summary(results: Sequence[dict[str, Any]]) -> dict[str, dict[str, list[str]]]:
    summary = {
        category: {"missing_artifact_ids": [], "failed_artifact_ids": []}
        for category in CATEGORY_BLOCKER_PREFIX
    }
    for result in results:
        category = str(result.get("category") or "unknown")
        if category not in summary:
            summary[category] = {"missing_artifact_ids": [], "failed_artifact_ids": []}
        artifact_id = str(result.get("artifact_id") or "")
        if not artifact_id:
            continue
        if result.get("status") == "blocked_missing_artifact":
            _append_unique(summary[category]["missing_artifact_ids"], artifact_id)
        elif result.get("status") == "failed":
            _append_unique(summary[category]["failed_artifact_ids"], artifact_id)
    return summary


def _append_unique(items: list[str], item: str) -> None:
    if item not in items:
        items.append(item)


def _int_or_none(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _input_safety_issues(*, remaining: dict[str, Any], plan: dict[str, Any], matrix: Sequence[Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for key in ("executes_commands", "runs_training", "runs_remote_preflight", "local_training_allowed", "formal_claim_allowed"):
        if remaining.get(key) is not False:
            issues.append({"issue_id": f"remaining_deliverables_{key}", "observed": remaining.get(key)})
    if remaining.get("not_paper_result_material") is not True:
        issues.append(
            {
                "issue_id": "remaining_deliverables_marked_as_paper_result_material",
                "observed": remaining.get("not_paper_result_material"),
            }
        )
    if plan.get("not_paper_result_material") is not True:
        issues.append({"issue_id": "proof_plan_marked_as_paper_result_material", "observed": plan.get("not_paper_result_material")})
    if plan.get("runs_training") is not False:
        issues.append({"issue_id": "proof_plan_runs_training", "observed": plan.get("runs_training")})
    if plan.get("runs_remote_preflight") is not False:
        issues.append({"issue_id": "proof_plan_runs_remote_preflight", "observed": plan.get("runs_remote_preflight")})
    if plan.get("execution_boundary") != "local_read_only_after_formal_remote_pullback":
        issues.append({"issue_id": "proof_plan_execution_boundary_invalid", "observed": plan.get("execution_boundary")})
    issues.extend(_proof_command_input_safety_issues(matrix))
    return issues


def _proof_command_input_safety_issues(matrix: Sequence[Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    forbidden_tokens = (
        "ssh ",
        "rsync ",
        "scp ",
        "preflight_rl_rs_gate3_formal_trial",
        "run_rl_rs_gate3_trial",
        "audit_rl_rs_gate3_trial",
    )
    for raw_row in matrix:
        if not isinstance(raw_row, dict):
            continue
        matrix_id = str(raw_row.get("matrix_id") or f"{raw_row.get('category', 'unknown')}:{raw_row.get('artifact_id', 'unknown')}")
        safe_matrix_id = _safe_issue_id(matrix_id)
        commands = raw_row.get("proof_commands")
        commands = commands if isinstance(commands, list) else []
        if int(raw_row.get("proof_command_count") or len(commands)) != len(commands):
            issues.append(
                {
                    "issue_id": f"proof_command_{safe_matrix_id}_count_mismatch",
                    "observed": raw_row.get("proof_command_count"),
                }
            )
        seen_command_ids: set[str] = set()
        for raw_command in commands:
            if not isinstance(raw_command, dict):
                issues.append({"issue_id": f"proof_command_{safe_matrix_id}_malformed"})
                continue
            command_id = str(raw_command.get("command_id") or "unknown_command")
            safe_command_id = _safe_issue_id(command_id)
            command_text = str(raw_command.get("command") or "")
            if command_id == "unknown_command":
                issues.append(
                    {
                        "issue_id": f"proof_command_{safe_matrix_id}_missing_id",
                        "observed": raw_command.get("command_id"),
                    }
                )
            elif command_id in seen_command_ids:
                issues.append(
                    {
                        "issue_id": f"proof_command_{safe_matrix_id}_{safe_command_id}_duplicate_id",
                        "observed": command_id,
                    }
                )
            seen_command_ids.add(command_id)
            if raw_command.get("execution_boundary") != "local_read_only_after_formal_remote_pullback":
                issues.append(
                    {
                        "issue_id": f"proof_command_{safe_matrix_id}_{safe_command_id}_wrong_boundary",
                        "observed": raw_command.get("execution_boundary"),
                    }
                )
            if not command_text.startswith("python -c "):
                issues.append(
                    {
                        "issue_id": f"proof_command_{safe_matrix_id}_{safe_command_id}_not_python_c",
                        "observed": command_text,
                    }
                )
            if " or " in command_text:
                issues.append(
                    {
                        "issue_id": f"proof_command_{safe_matrix_id}_{safe_command_id}_raw_or_path",
                        "observed": command_text,
                    }
                )
            if any(token in command_text for token in forbidden_tokens):
                issues.append(
                    {
                        "issue_id": f"proof_command_{safe_matrix_id}_{safe_command_id}_forbidden_execution_token",
                        "observed": command_text,
                    }
                )
    return issues


def _proof_command_results(*, matrix: Sequence[Any], workspace_root: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for raw_row in matrix:
        if not isinstance(raw_row, dict):
            continue
        category = str(raw_row.get("category") or "unknown")
        artifact_id = str(raw_row.get("artifact_id") or "unknown")
        matrix_id = str(raw_row.get("matrix_id") or f"{category}:{artifact_id}")
        expected_path = str(raw_row.get("expected_path") or "")
        resolved_paths = _resolve_path_candidates(workspace_root, expected_path)
        raw_commands = raw_row.get("proof_commands")
        commands = raw_commands if isinstance(raw_commands, list) else []
        for raw_command in commands:
            if not isinstance(raw_command, dict):
                continue
            command_id = str(raw_command.get("command_id") or "")
            if not command_id:
                continue
            result = _evaluate_command(
                command_id=command_id,
                expected_path=expected_path,
                resolved_paths=resolved_paths,
                expected_evidence=str(raw_command.get("expected_evidence") or ""),
            )
            result.update(
                {
                    "matrix_id": matrix_id,
                    "category": category,
                    "artifact_id": artifact_id,
                    "command_id": command_id,
                    "purpose": raw_command.get("purpose"),
                    "command": raw_command.get("command"),
                    "expected_path": expected_path,
                    "expected_evidence": raw_command.get("expected_evidence"),
                    "execution_boundary": raw_command.get("execution_boundary"),
                    "command_was_executed": False,
                }
            )
            results.append(result)
    return results


def _evaluate_command(*, command_id: str, expected_path: str, resolved_paths: Sequence[Path], expected_evidence: str) -> dict[str, Any]:
    resolved_path = next((path for path in resolved_paths if path.is_file()), resolved_paths[0] if resolved_paths else Path(expected_path))
    if not resolved_path.is_file():
        return {
            "status": "blocked_missing_artifact",
            "diagnostic": f"expected artifact is missing: {expected_path}",
        }
    if resolved_path.stat().st_size <= 0:
        return {
            "status": "failed",
            "diagnostic": f"expected artifact exists but is empty: {expected_path}",
        }
    checker = _checker(command_id)
    if checker is None:
        return {
            "status": "failed",
            "diagnostic": f"unknown proof command id: {command_id}",
        }
    try:
        checker(resolved_path)
    except Exception as exc:  # noqa: BLE001 - diagnostics must preserve failed proof reason.
        return {
            "status": "failed",
            "diagnostic": f"{command_id} failed: {exc}; expected {expected_evidence}",
        }
    return {
        "status": "passed",
        "diagnostic": f"{command_id} passed",
    }


def _checker(command_id: str) -> Callable[[Path], None] | None:
    checks: dict[str, Callable[[Path], None]] = {
        "train_final_model_zip_exists_nonempty": _check_exists_nonempty,
        "train_final_model_zip_valid_zip": _check_zip,
        "train_summary_json_exists_nonempty": _check_exists_nonempty,
        "train_summary_json_formal_warm_start_metadata": _check_train_summary,
        "train_training_manifest_json_exists_nonempty": _check_exists_nonempty,
        "train_training_manifest_json_provenance": _check_training_manifest,
        "eval_gate3_eval_episodes_csv_exists_nonempty": _check_exists_nonempty,
        "eval_gate3_eval_episodes_csv_schema": _check_eval_csv,
        "eval_gate3_summary_json_exists_nonempty": _check_exists_nonempty,
        "eval_gate3_summary_json_formal_scope": _check_eval_summary,
        "gate3_trial_manifest_json_exists_nonempty": _check_exists_nonempty,
        "gate3_trial_manifest_json_formal_warm_start_scope": _check_trial_manifest,
        "gate3_formal_audit_json_exists_nonempty": _check_exists_nonempty,
        "gate3_formal_audit_json_accepts_formal_scope": _check_formal_audit,
        "pulled_back_checkpoint_hash_record_exists_nonempty": _check_exists_nonempty,
        "pulled_back_checkpoint_hash_record_matches_model": _check_checkpoint_hash_record,
        "h01_ready_for_formal_run_exists_nonempty": _check_exists_nonempty,
        "h01_ready_for_formal_run_status": _check_h01_status,
        "h02_formal_output_acceptance_exists_nonempty": _check_exists_nonempty,
        "h02_formal_output_acceptance_status": _check_h02_status,
    }
    return checks.get(command_id)


def _check_exists_nonempty(path: Path) -> None:
    assert path.is_file() and path.stat().st_size > 0, path


def _check_zip(path: Path) -> None:
    assert zipfile.is_zipfile(path), path


def _check_train_summary(path: Path) -> None:
    data = _read_dict(path)
    assert data.get("status") == "complete"
    assert data.get("warm_start_status") == "applied_obstacle_summary_bc"
    assert data.get("config", {}).get("curriculum_preset") == "f03"
    assert data.get("config", {}).get("smoke") is False


def _check_training_manifest(path: Path) -> None:
    data = _read_dict(path)
    assert isinstance(data.get("command"), (str, list)) and data.get("command")
    assert isinstance(data.get("source_hashes"), dict) and data["source_hashes"]
    assert data.get("config", {}).get("curriculum_preset") == "f03"


def _check_eval_csv(path: Path) -> None:
    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) >= 64
    required = {"terminal_rs_success", "collision", "truncated", "nn_forward_time_s"}
    assert rows and required.issubset(rows[0])


def _check_eval_summary(path: Path) -> None:
    data = _read_dict(path)
    assert data.get("gate_name") == "module2_f03_gate3"
    assert data.get("contract") == ".pipeline/contracts/module2-ppo-funnel-expansion.md"
    assert int(data.get("episodes", 0)) >= int(data.get("min_episodes", 64)) >= 64
    assert data.get("config", {}).get("curriculum_preset") == "f03"


def _check_trial_manifest(path: Path) -> None:
    data = _read_dict(path)
    assert data.get("trial_name") == "module2_f03_gate3_train_eval"
    assert data.get("status") == "complete"
    assert data.get("smoke") is False
    assert data.get("formal_gate_claim") is False
    assert data.get("warm_start_status") == "applied_obstacle_summary_bc"


def _check_formal_audit(path: Path) -> None:
    data = _read_dict(path)
    assert data.get("audit_name") == "module2_f03_gate3_formal_audit"
    assert data.get("formal_decision") in {"pass", "fail"}
    assert data.get("formal_claim_allowed") is True
    assert not data.get("formal_blockers")


def _check_checkpoint_hash_record(path: Path) -> None:
    model_path = path.with_name("final_model.zip")
    digest = hashlib.sha256(model_path.read_bytes()).hexdigest()
    assert digest in path.read_text(encoding="utf-8")


def _check_h01_status(path: Path) -> None:
    data = _read_dict(path)
    assert data.get("status") in {"ready_for_formal_run", "ready_for_formal_evaluation"}


def _check_h02_status(path: Path) -> None:
    data = _read_dict(path)
    assert data.get("status") == "formal_output_accepted"
    assert data.get("formal_output_accepted") is True
    assert data.get("paper_result_input_allowed") is True


def _category_status_counts(results: Sequence[dict[str, Any]]) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    for result in results:
        category = str(result.get("category") or "unknown")
        counts.setdefault(category, {key: 0 for key in STATUS_KEYS})
        status = str(result.get("status"))
        if status not in counts[category]:
            counts[category][status] = 0
        counts[category][status] += 1
    return counts


def _blockers(
    *,
    category_status_counts: dict[str, dict[str, int]],
    input_safety_issues: Sequence[dict[str, Any]],
) -> list[str]:
    blockers: list[str] = []
    if input_safety_issues:
        blockers.append("proof_audit_input_safety_issues_open")
    for category, counts in category_status_counts.items():
        prefix = CATEGORY_BLOCKER_PREFIX.get(category, f"{category}_artifacts")
        if counts.get("blocked_missing_artifact", 0) > 0:
            blockers.append(f"missing_{prefix}")
        if counts.get("failed", 0) > 0:
            blockers.append(f"failed_{prefix}")
    return blockers


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 Formal Gate Proof Audit",
        "",
        f"- status: `{manifest['status']}`",
        f"- not_paper_result_material: `{manifest['not_paper_result_material']}`",
        f"- executes_commands: `{manifest['executes_commands']}`",
        f"- runs_training: `{manifest['runs_training']}`",
        f"- runs_remote_preflight: `{manifest['runs_remote_preflight']}`",
        f"- total_matrix_rows: `{manifest['total_matrix_rows']}`",
        f"- total_proof_command_count: `{manifest['total_proof_command_count']}`",
        f"- passed_proof_command_count: `{manifest['passed_proof_command_count']}`",
        f"- failed_proof_command_count: `{manifest['failed_proof_command_count']}`",
        f"- blocked_proof_command_count: `{manifest['blocked_proof_command_count']}`",
        "",
        "## Blockers",
        "",
    ]
    lines.extend(f"- `{blocker}`" for blocker in manifest["blockers"]) if manifest["blockers"] else lines.append("- none")
    current_state = manifest.get("current_state", {})
    lines.extend(["", "## Current Gate State", ""])
    for key in (
        "remaining_deliverables_status",
        "remaining_missing_deliverable_count",
        "remaining_open_category_count",
        "source_freshness_ready_for_remote_preflight",
        "source_freshness_status",
        "source_freshness_regeneration_required",
    ):
        lines.append(f"- {key}: `{current_state.get(key)}`")
    summary = manifest["remaining_deliverables_top_level_summary"]
    lines.extend(["", "## Remaining Deliverables Top-Level Summary", ""])
    lines.append(f"- present: `{summary['present']}`")
    lines.append(f"- missing_counts_by_formal_category: `{summary['missing_counts_by_formal_category']}`")
    lines.append(f"- next_blocked_lane: `{summary['next_blocked_lane']}`")
    lines.append(f"- h01_status: `{summary['h01_status']}`")
    lines.append(f"- h02_status: `{summary['h02_status']}`")
    lines.append(f"- h02_formal_output_accepted: `{summary['h02_formal_output_accepted']}`")
    lines.append(f"- h02_paper_result_input_allowed: `{summary['h02_paper_result_input_allowed']}`")
    for category, matrix_ids in summary["missing_matrix_ids_by_formal_category"].items():
        joined = ", ".join(matrix_ids) if matrix_ids else "none"
        lines.append(f"- {category}_missing_matrix_ids: `{joined}`")
    lines.extend(["", "## Missing Evidence Summary", ""])
    for category, summary in manifest["formal_gate_missing_evidence_summary"].items():
        missing = ", ".join(summary["missing_artifact_ids"]) or "none"
        failed = ", ".join(summary["failed_artifact_ids"]) or "none"
        lines.append(f"- `{category}`: missing=`{missing}`, failed=`{failed}`")
    lines.extend(["", "## Proof Command Results", ""])
    for result in manifest["proof_command_results"]:
        lines.append(f"### {result['command_id']}")
        lines.append(f"- matrix_id: `{result['matrix_id']}`")
        lines.append(f"- status: `{result['status']}`")
        lines.append(f"- command_was_executed: `{result['command_was_executed']}`")
        lines.append(f"- expected_path: `{result['expected_path']}`")
        lines.append(f"- diagnostic: `{result['diagnostic']}`")
        lines.append("")
    lines.extend(["## Claim Boundaries", ""])
    lines.extend(f"- {item}" for item in manifest["claim_boundaries"])
    return "\n".join(lines) + "\n"


def _read_dict(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"expected object JSON: {path}")
    return data


def _resolve_path_candidates(workspace_root: Path, expected_path: str) -> list[Path]:
    candidates = [item.strip() for item in expected_path.split(" or ") if item.strip()]
    paths = candidates or [expected_path]
    return [_resolve_path(workspace_root, path) for path in paths]


def _resolve_path(workspace_root: Path, expected_path: str) -> Path:
    path = Path(expected_path)
    return path if path.is_absolute() else workspace_root / path


def _safe_issue_id(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value).strip("_")


def _source_head() -> str:
    return module2_source_head()


if __name__ == "__main__":
    raise SystemExit(main())
