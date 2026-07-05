from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_mainline_formal_gate_state_audit")
DEFAULT_MAINLINE = Path(".pipeline/mainline_module2_rl_rs_replacement.md")
DEFAULT_FORMAL_GATE_STATUS_REPORT = Path(
    "0_trials/module2_formal_gate_status_report/formal_gate_status_report.json"
)
DEFAULT_PROOF_SUMMARY_CHAIN_AUDIT = Path(
    "0_trials/module2_formal_gate_proof_summary_chain_audit/formal_gate_proof_summary_chain_audit.json"
)

CURRENT_STATE_MARKER = "当前 formal gate 下一步清单已同步到主任务书"
REQUIRED_CURRENT_BOUNDARY_TOKENS = (
    "local training",
    "remote preflight",
    "remote training",
    "formal claim",
    "paper-result material",
    "gpu3070ti-relay",
)
FORBIDDEN_CURRENT_ALLOWED_TOKENS = (
    "local_training_allowed=true",
    "remote_preflight_allowed=true",
    "remote_training_allowed=true",
    "formal_claim_allowed=true",
    "paper_result_material_allowed=true",
    "formal_result_material_allowed=true",
)


@dataclass(frozen=True)
class MainlineFormalGateStateAuditConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    mainline_path: Path = DEFAULT_MAINLINE
    formal_gate_status_report_path: Path = DEFAULT_FORMAL_GATE_STATUS_REPORT
    proof_summary_chain_audit_path: Path = DEFAULT_PROOF_SUMMARY_CHAIN_AUDIT


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = MainlineFormalGateStateAuditConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        mainline_path=args.mainline,
        formal_gate_status_report_path=args.formal_gate_status_report,
        proof_summary_chain_audit_path=args.proof_summary_chain_audit,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "mainline_formal_gate_state_audit.json"
    markdown_out = config.markdown_out or output_dir / "mainline_formal_gate_state_audit.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(
        json.dumps(
            {"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]},
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


def build_manifest(config: MainlineFormalGateStateAuditConfig) -> dict[str, Any]:
    mainline_text = Path(config.mainline_path).read_text(encoding="utf-8")
    status_report = _read_json(config.formal_gate_status_report_path)
    proof_chain = _read_json(config.proof_summary_chain_audit_path)
    next_action_guard = _normalize_next_action_guard(status_report.get("next_action_guard_summary"))
    next_required = _normalize_next_required_deliverables(status_report.get("next_required_formal_deliverables"))
    current_section = _current_section(mainline_text)
    deliverable_rows = _deliverable_rows(next_required, mainline_text=mainline_text, current_section=current_section)
    issues = (
        _mainline_issues(
            mainline_text=mainline_text,
            current_section=current_section,
            next_action_guard=next_action_guard,
            next_required=next_required,
            deliverable_rows=deliverable_rows,
            proof_chain=proof_chain,
        )
        + _status_report_issues(next_action_guard=next_action_guard, next_required=next_required)
        + _proof_chain_issues(proof_chain)
    )
    issues = _unique_issues(issues)
    if issues:
        status = "mainline_formal_gate_state_audit_failed"
    elif status_report.get("status") == "formal_gate_status_blocked" or proof_chain.get("proof_open") is True:
        status = "mainline_formal_gate_state_consistent_blocked"
    else:
        status = "mainline_formal_gate_state_consistent_ready"

    return {
        "schema_version": 1,
        "artifact_name": "module2_mainline_formal_gate_state_audit",
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
            "mainline": str(config.mainline_path),
            "formal_gate_status_report": str(config.formal_gate_status_report_path),
            "proof_summary_chain_audit": str(config.proof_summary_chain_audit_path),
        },
        "mainline_current_state_section_present": bool(current_section),
        "expected_next_action_id": next_action_guard["expected_next_action_id"],
        "expected_next_action_mentioned": next_action_guard["expected_next_action_id"] in mainline_text,
        "all_execution_disabled_now": next_action_guard["all_execution_disabled_now"],
        "execution_leak_count": next_action_guard["execution_leak_count"],
        "next_required_formal_deliverables_status": next_required["status"],
        "total_missing_deliverables": next_required["total_missing_deliverables"],
        "blocked_category_count": next_required["blocked_category_count"],
        "mainline_missing_deliverable_mention_count": sum(1 for row in deliverable_rows if not row["mentioned"]),
        "deliverable_rows": deliverable_rows,
        "deliverable_rows_by_matrix_id": {row["matrix_id"]: row for row in deliverable_rows},
        "proof_summary_chain_status": proof_chain.get("status"),
        "proof_summary_chain_audit_issue_count": proof_chain.get("audit_issue_count"),
        "proof_summary_next_action_guard_consistency": {
            "row_count": proof_chain.get("next_action_guard_row_count"),
            "consistent_row_count": proof_chain.get("next_action_guard_consistent_row_count"),
        },
        "proof_summary_next_required_deliverables_consistency": {
            "row_count": proof_chain.get("next_required_deliverables_row_count"),
            "consistent_row_count": proof_chain.get("next_required_deliverables_consistent_row_count"),
        },
        "current_boundary_tokens": [
            {"token": token, "mentioned": token in current_section} for token in REQUIRED_CURRENT_BOUNDARY_TOKENS
        ],
        "forbidden_current_allowed_tokens": [
            {"token": token, "mentioned": token in current_section}
            for token in FORBIDDEN_CURRENT_ALLOWED_TOKENS
        ],
        "audit_issue_count": len(issues),
        "audit_issues": issues,
        "claim_boundaries": [
            "This audit only checks that the long-term mainline task book mirrors the current formal-gate state.",
            "It does not execute commands, run local training, run remote preflight, run remote PPO training, evaluate PPO, pull back artifacts, or write paper results.",
            "A consistent blocked audit does not prove PPO has replaced RS in formal evaluation.",
            "Formal PPO-vs-RS performance claims still require the missing training, evaluation, acceptance, and H01/H02 artifacts to be produced and audited.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit Module2 mainline task-book formal-gate state.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--mainline", type=Path, default=DEFAULT_MAINLINE)
    parser.add_argument("--formal-gate-status-report", type=Path, default=DEFAULT_FORMAL_GATE_STATUS_REPORT)
    parser.add_argument("--proof-summary-chain-audit", type=Path, default=DEFAULT_PROOF_SUMMARY_CHAIN_AUDIT)
    return parser.parse_args(list(argv) if argv is not None else None)


def _mainline_issues(
    *,
    mainline_text: str,
    current_section: str,
    next_action_guard: dict[str, Any],
    next_required: dict[str, Any],
    deliverable_rows: Sequence[dict[str, Any]],
    proof_chain: dict[str, Any],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if not current_section:
        issues.append(
            {
                "issue_id": "mainline_current_formal_gate_section_missing",
                "message": "Mainline task book must include the current formal-gate state section.",
            }
        )
    expected_next_action = next_action_guard["expected_next_action_id"]
    if expected_next_action and expected_next_action not in mainline_text:
        issues.append(
            {
                "issue_id": "mainline_missing_expected_next_action",
                "message": "Mainline task book must mention the current expected next action.",
                "expected_next_action_id": expected_next_action,
            }
        )
    for row in deliverable_rows:
        if not row["mentioned"]:
            issues.append(
                {
                    "issue_id": f"mainline_missing_deliverable_{row['safe_matrix_id']}",
                    "message": "Mainline task book must mention every missing formal deliverable artifact id.",
                    "matrix_id": row["matrix_id"],
                    "artifact_id": row["artifact_id"],
                }
            )
    for token in REQUIRED_CURRENT_BOUNDARY_TOKENS:
        if token not in current_section:
            issues.append(
                {
                    "issue_id": f"mainline_current_section_missing_boundary_{_safe_id(token)}",
                    "message": "Current formal-gate section must mention this blocked boundary.",
                    "token": token,
                }
            )
    for token in FORBIDDEN_CURRENT_ALLOWED_TOKENS:
        if token in current_section:
            issues.append(
                {
                    "issue_id": f"mainline_current_section_forbidden_allowed_token_{_safe_id(token)}",
                    "message": "Current formal-gate section must not mark a blocked execution or claim surface as allowed.",
                    "token": token,
                }
            )
    proof_status = str(proof_chain.get("status", ""))
    if proof_status and proof_status not in mainline_text:
        issues.append(
            {
                "issue_id": "mainline_missing_proof_chain_status",
                "message": "Mainline task book must mention the current proof-summary chain status.",
                "proof_summary_chain_status": proof_status,
            }
        )
    if next_required["total_missing_deliverables"] != len(deliverable_rows):
        issues.append(
            {
                "issue_id": "mainline_audit_deliverable_row_count_mismatch",
                "message": "Normalized deliverable row count must match total missing deliverables.",
                "total_missing_deliverables": next_required["total_missing_deliverables"],
                "row_count": len(deliverable_rows),
            }
        )
    return issues


def _status_report_issues(
    *, next_action_guard: dict[str, Any], next_required: dict[str, Any]
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if not next_action_guard["present"]:
        issues.append(
            {
                "issue_id": "status_report_next_action_guard_missing",
                "message": "Status report must expose next_action_guard_summary.",
            }
        )
    if next_action_guard["status"] != "next_action_guard_passed":
        issues.append(
            {
                "issue_id": "status_report_next_action_guard_not_passed",
                "message": "Status report next-action guard must be passed before the mainline can mirror it.",
                "observed_status": next_action_guard["status"],
            }
        )
    if next_action_guard["expected_next_action_id"] != "record_f02_6_decision":
        issues.append(
            {
                "issue_id": "status_report_unexpected_next_action",
                "message": "F02.6-pending mainline audit expects the next action to remain the human decision record.",
                "observed_next_action_id": next_action_guard["expected_next_action_id"],
            }
        )
    if next_action_guard["execution_leak_count"] > 0 or not next_action_guard["all_execution_disabled_now"]:
        issues.append(
            {
                "issue_id": "status_report_next_action_guard_execution_leak",
                "message": "Status report exposes an execution leak while F02.6 is pending.",
                "execution_leak_count": next_action_guard["execution_leak_count"],
                "all_execution_disabled_now": next_action_guard["all_execution_disabled_now"],
            }
        )
    if not next_required["present"]:
        issues.append(
            {
                "issue_id": "status_report_next_required_deliverables_missing",
                "message": "Status report must expose next_required_formal_deliverables.",
            }
        )
    if next_required["not_paper_result_material"] is not True:
        issues.append(
            {
                "issue_id": "status_report_next_required_marked_as_paper_result",
                "message": "Next-required formal deliverables must not be marked as paper-result material.",
            }
        )
    if next_required["runs_training"] is True or next_required["runs_remote_preflight"] is True:
        issues.append(
            {
                "issue_id": "status_report_next_required_executes_work",
                "message": "Next-required formal deliverables summary must remain read-only.",
                "runs_training": next_required["runs_training"],
                "runs_remote_preflight": next_required["runs_remote_preflight"],
            }
        )
    if next_required["total_missing_deliverables"] != next_required["row_count"]:
        issues.append(
            {
                "issue_id": "status_report_next_required_row_count_mismatch",
                "message": "Next-required formal deliverable rows must match the total missing deliverable count.",
                "total_missing_deliverables": next_required["total_missing_deliverables"],
                "row_count": next_required["row_count"],
            }
        )
    return issues


def _proof_chain_issues(proof_chain: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if proof_chain.get("audit_issue_count") != 0:
        issues.append(
            {
                "issue_id": "proof_summary_chain_has_audit_issues",
                "message": "Mainline task-book state should only mirror a clean proof-summary chain.",
                "audit_issue_count": proof_chain.get("audit_issue_count"),
            }
        )
    if proof_chain.get("next_action_guard_row_count") != proof_chain.get("next_action_guard_consistent_row_count"):
        issues.append(
            {
                "issue_id": "proof_summary_chain_next_action_guard_inconsistent",
                "message": "Proof-summary chain must agree on the next-action guard before mainline mirrors it.",
                "row_count": proof_chain.get("next_action_guard_row_count"),
                "consistent_row_count": proof_chain.get("next_action_guard_consistent_row_count"),
            }
        )
    if proof_chain.get("next_required_deliverables_row_count") != proof_chain.get(
        "next_required_deliverables_consistent_row_count"
    ):
        issues.append(
            {
                "issue_id": "proof_summary_chain_next_required_deliverables_inconsistent",
                "message": "Proof-summary chain must agree on next required formal deliverables before mainline mirrors them.",
                "row_count": proof_chain.get("next_required_deliverables_row_count"),
                "consistent_row_count": proof_chain.get("next_required_deliverables_consistent_row_count"),
            }
        )
    if proof_chain.get("runs_training") is True or proof_chain.get("runs_remote_preflight") is True:
        issues.append(
            {
                "issue_id": "proof_summary_chain_executes_work",
                "message": "Proof-summary chain audit must remain read-only.",
                "runs_training": proof_chain.get("runs_training"),
                "runs_remote_preflight": proof_chain.get("runs_remote_preflight"),
            }
        )
    if proof_chain.get("formal_claim_allowed") is True:
        issues.append(
            {
                "issue_id": "proof_summary_chain_allows_formal_claim",
                "message": "Proof-summary chain audit must not allow formal claims while proof is open.",
            }
        )
    return issues


def _deliverable_rows(
    next_required: dict[str, Any], *, mainline_text: str, current_section: str
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in next_required["rows"]:
        matrix_id = str(row.get("matrix_id", ""))
        artifact_id = str(row.get("artifact_id", ""))
        rows.append(
            {
                "matrix_id": matrix_id,
                "safe_matrix_id": _safe_id(matrix_id),
                "category": row.get("category"),
                "artifact_id": artifact_id,
                "mentioned": bool(artifact_id and artifact_id in mainline_text),
                "mentioned_in_current_section": bool(artifact_id and artifact_id in current_section),
                "responsible_stage_id": row.get("responsible_stage_id"),
                "responsible_stage_allowed_now": bool(row.get("responsible_stage_allowed_now")),
            }
        )
    return rows


def _current_section(mainline_text: str) -> str:
    marker_index = mainline_text.rfind(CURRENT_STATE_MARKER)
    if marker_index < 0:
        return ""
    return mainline_text[marker_index:]


def _normalize_next_action_guard(raw: Any) -> dict[str, Any]:
    raw = raw if isinstance(raw, dict) else {}
    return {
        "present": bool(raw),
        "status": raw.get("status"),
        "expected_next_action_id": raw.get("expected_next_action_id"),
        "all_execution_disabled_now": bool(raw.get("all_execution_disabled_now")),
        "execution_leak_count": int(raw.get("execution_leak_count") or 0),
    }


def _normalize_next_required_deliverables(raw: Any) -> dict[str, Any]:
    raw = raw if isinstance(raw, dict) else {}
    rows = raw.get("rows", [])
    if isinstance(rows, dict):
        normalized_rows = list(rows.values())
    elif isinstance(rows, list):
        normalized_rows = [row for row in rows if isinstance(row, dict)]
    else:
        normalized_rows = []
    return {
        "present": bool(raw),
        "status": raw.get("status"),
        "not_paper_result_material": raw.get("not_paper_result_material"),
        "runs_training": raw.get("runs_training"),
        "runs_remote_preflight": raw.get("runs_remote_preflight"),
        "total_missing_deliverables": int(raw.get("total_missing_deliverables") or 0),
        "blocked_category_count": int(raw.get("blocked_category_count") or 0),
        "row_count": len(normalized_rows),
        "rows": normalized_rows,
    }


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 Mainline Formal Gate State Audit",
        "",
        "This file checks that the long-term Module2 mainline task book mirrors the current formal-gate state. It is not a training run, remote preflight, formal evaluation, or paper result.",
        "",
        f"- status: `{manifest['status']}`",
        f"- audit_issue_count: `{manifest['audit_issue_count']}`",
        f"- expected_next_action_id: `{manifest['expected_next_action_id']}`",
        f"- expected_next_action_mentioned: `{manifest['expected_next_action_mentioned']}`",
        f"- total_missing_deliverables: `{manifest['total_missing_deliverables']}`",
        f"- mainline_missing_deliverable_mention_count: `{manifest['mainline_missing_deliverable_mention_count']}`",
        f"- proof_summary_chain_status: `{manifest['proof_summary_chain_status']}`",
        f"- executes_commands: `{manifest['executes_commands']}`",
        f"- runs_training: `{manifest['runs_training']}`",
        f"- runs_remote_preflight: `{manifest['runs_remote_preflight']}`",
        f"- formal_claim_allowed: `{manifest['formal_claim_allowed']}`",
        "",
        "## Audit Issues",
        "",
    ]
    if manifest["audit_issues"]:
        for issue in manifest["audit_issues"]:
            lines.append(f"- `{issue['issue_id']}`: {issue['message']}")
    else:
        lines.append("- none")
    lines.extend(["", "## Missing Formal Deliverables", ""])
    for row in manifest["deliverable_rows"]:
        lines.append(
            f"- `{row['matrix_id']}`: artifact_id=`{row['artifact_id']}`, mentioned=`{row['mentioned']}`, "
            f"mentioned_in_current_section=`{row['mentioned_in_current_section']}`"
        )
    lines.extend(["", "## Current Boundary Tokens", ""])
    for row in manifest["current_boundary_tokens"]:
        lines.append(f"- `{row['token']}`: mentioned=`{row['mentioned']}`")
    lines.extend(["", "## Claim Boundaries", ""])
    for boundary in manifest["claim_boundaries"]:
        lines.append(f"- {boundary}")
    return "\n".join(lines) + "\n"


def _read_json(path: Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True).strip()
    except Exception:
        return "unknown"
    return f"{head}+dirty" if dirty else head


def _safe_id(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value).strip("_") or "unknown"


def _unique_issues(issues: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for issue in issues:
        issue_id = str(issue.get("issue_id", "unknown_issue"))
        if issue_id in seen:
            continue
        seen.add(issue_id)
        unique.append(issue)
    return unique


if __name__ == "__main__":
    raise SystemExit(main())
