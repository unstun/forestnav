from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_formal_gate_failure_triage")
DEFAULT_GATE3_AUDIT = Path(
    "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json"
)
DEFAULT_GATE3_EVAL_SUMMARY = Path(
    "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json"
)
DEFAULT_REMAINING_DELIVERABLES = Path(
    "0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json"
)
DEFAULT_H02_ACCEPTANCE = Path("0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json")
DEFAULT_STATUS_REPORT = Path("0_trials/module2_formal_gate_status_report/formal_gate_status_report.json")
DEFAULT_REMOTE_PACKET_SAFETY = Path("0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json")
DEFAULT_SOURCE_FRESHNESS = Path("0_trials/module2_source_freshness_audit/source_freshness_audit.json")


@dataclass(frozen=True)
class FormalGateFailureTriageConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    gate3_audit_path: Path = DEFAULT_GATE3_AUDIT
    gate3_eval_summary_path: Path = DEFAULT_GATE3_EVAL_SUMMARY
    remaining_deliverables_path: Path = DEFAULT_REMAINING_DELIVERABLES
    h02_acceptance_path: Path = DEFAULT_H02_ACCEPTANCE
    status_report_path: Path = DEFAULT_STATUS_REPORT
    remote_packet_safety_path: Path = DEFAULT_REMOTE_PACKET_SAFETY
    source_freshness_path: Path = DEFAULT_SOURCE_FRESHNESS


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = FormalGateFailureTriageConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        gate3_audit_path=args.gate3_audit,
        gate3_eval_summary_path=args.gate3_eval_summary,
        remaining_deliverables_path=args.remaining_deliverables,
        h02_acceptance_path=args.h02_acceptance,
        status_report_path=args.status_report,
        remote_packet_safety_path=args.remote_packet_safety,
        source_freshness_path=args.source_freshness,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "formal_gate_failure_triage.json"
    markdown_out = config.markdown_out or output_dir / "formal_gate_failure_triage.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: FormalGateFailureTriageConfig) -> dict[str, Any]:
    gate3_audit = _read_json(config.gate3_audit_path)
    eval_summary = _read_json(config.gate3_eval_summary_path)
    remaining = _read_json(config.remaining_deliverables_path)
    h02 = _read_json(config.h02_acceptance_path)
    status_report = _read_json(config.status_report_path)
    remote_safety = _read_json(config.remote_packet_safety_path)
    source_freshness = _read_json(config.source_freshness_path)

    failure = _failure_summary(gate3_audit=gate3_audit, eval_summary=eval_summary)
    deliverables = _deliverable_summary(remaining)
    h02_summary = _h02_summary(h02)
    permissions = _permissions(status_report)
    next_gate = _next_gate(failure=failure, deliverables=deliverables, h02_summary=h02_summary)
    audit_issues = _audit_issues(
        failure=failure,
        deliverables=deliverables,
        h02_summary=h02_summary,
        permissions=permissions,
        remaining=remaining,
        remote_safety=remote_safety,
        source_freshness=source_freshness,
    )
    ready = not audit_issues and failure["failure_mode"] == "threshold_failure"
    return {
        "schema_version": 1,
        "artifact_name": "module2_formal_gate_failure_triage",
        "status": "formal_gate_failure_triage_ready" if ready else "formal_gate_failure_triage_blocked",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "runs_remote_audit": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "paper_result_material_allowed": False,
        "inputs": {
            "gate3_formal_audit": str(config.gate3_audit_path),
            "gate3_eval_summary": str(config.gate3_eval_summary_path),
            "remaining_deliverables": str(config.remaining_deliverables_path),
            "h02_formal_acceptance": str(config.h02_acceptance_path),
            "formal_gate_status_report": str(config.status_report_path),
            "remote_packet_safety_audit": str(config.remote_packet_safety_path),
            "source_freshness_audit": str(config.source_freshness_path),
        },
        "formal_gate_failure": failure,
        "training_evaluation_acceptance_artifacts": deliverables,
        "h02_formal_acceptance_summary": h02_summary,
        "permissions_now": permissions,
        "next_gate": next_gate,
        "audit_issue_count": len(audit_issues),
        "audit_issues": audit_issues,
        "claim_boundaries": [
            "This triage is a formal-gate operations artifact, not a paper result table, appendix, or success claim.",
            "The current warm-start PPO Gate3 run is a threshold failure and must not be reframed as PPO replacing RS successfully.",
            "New training intended to overturn this failure requires a new or revised Research Contract before execution.",
            "Local PPO training remains disallowed; remote-only evidence must keep checkpoint, eval, audit, and hash provenance.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Module2 formal Gate3 failure triage without running experiments.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--gate3-audit", type=Path, default=DEFAULT_GATE3_AUDIT)
    parser.add_argument("--gate3-eval-summary", type=Path, default=DEFAULT_GATE3_EVAL_SUMMARY)
    parser.add_argument("--remaining-deliverables", type=Path, default=DEFAULT_REMAINING_DELIVERABLES)
    parser.add_argument("--h02-acceptance", type=Path, default=DEFAULT_H02_ACCEPTANCE)
    parser.add_argument("--status-report", type=Path, default=DEFAULT_STATUS_REPORT)
    parser.add_argument("--remote-packet-safety", type=Path, default=DEFAULT_REMOTE_PACKET_SAFETY)
    parser.add_argument("--source-freshness", type=Path, default=DEFAULT_SOURCE_FRESHNESS)
    return parser.parse_args(list(argv) if argv is not None else None)


def _failure_summary(*, gate3_audit: dict[str, Any], eval_summary: dict[str, Any]) -> dict[str, Any]:
    success_rate = _number(gate3_audit.get("terminal_rs_success_rate"))
    if success_rate is None:
        success_rate = _number(eval_summary.get("terminal_rs_success_rate"))
    threshold = _number(gate3_audit.get("required_success_threshold"))
    if threshold is None:
        threshold = _number(gate3_audit.get("success_threshold"))
    episodes = _int(gate3_audit.get("episodes"))
    if episodes is None:
        episodes = _int(eval_summary.get("episodes"))
    deficit = None
    if success_rate is not None and threshold is not None:
        deficit = round(max(0.0, threshold - success_rate), 12)
    formal_decision = str(gate3_audit.get("formal_decision") or "unknown")
    failure_mode = "not_failure"
    if formal_decision == "fail" and success_rate is not None and threshold is not None and success_rate < threshold:
        failure_mode = "threshold_failure"
    elif formal_decision == "fail":
        failure_mode = "failed_without_rate_proof"
    return {
        "gate3_audit_name": gate3_audit.get("audit_name"),
        "formal_decision": formal_decision,
        "evaluator_decision": gate3_audit.get("evaluator_decision"),
        "failure_mode": failure_mode,
        "episodes": episodes,
        "terminal_rs_success_rate": success_rate,
        "required_success_threshold": threshold,
        "threshold_deficit": deficit,
        "warm_start_status": gate3_audit.get("warm_start_status"),
        "warm_start_decision": gate3_audit.get("warm_start_decision"),
        "formal_blockers": _strings(gate3_audit.get("formal_blockers")),
        "formal_claim_allowed_field": gate3_audit.get("formal_claim_allowed"),
        "paper_success_claim_allowed": False,
    }


def _deliverable_summary(remaining: dict[str, Any]) -> dict[str, Any]:
    gap = remaining.get("deliverable_gap_summary") if isinstance(remaining.get("deliverable_gap_summary"), dict) else {}
    categories = gap.get("categories") if isinstance(gap.get("categories"), list) else []
    rows: list[dict[str, Any]] = []
    missing_by_category: dict[str, int] = {}
    present_by_category: dict[str, int] = {}
    missing_artifacts: list[dict[str, Any]] = []
    for category in categories:
        if not isinstance(category, dict):
            continue
        category_id = str(category.get("category") or "")
        missing_count = int(category.get("missing_count") or 0)
        present_count = int(category.get("present_count") or 0)
        row = {
            "category": category_id,
            "status": category.get("status"),
            "missing_count": missing_count,
            "present_count": present_count,
            "responsible_stage_id": category.get("responsible_stage_id"),
            "responsible_stage_allowed_now": category.get("responsible_stage_allowed_now"),
            "responsible_stage_blocked_by": _strings(category.get("responsible_stage_blocked_by")),
        }
        rows.append(row)
        missing_by_category[category_id] = missing_count
        present_by_category[category_id] = present_count
        for item in category.get("missing_artifacts", ()) if isinstance(category.get("missing_artifacts"), list) else ():
            if isinstance(item, dict):
                missing_artifacts.append(
                    {
                        "category": category_id,
                        "artifact_id": item.get("artifact_id"),
                        "expected_path": item.get("expected_path"),
                        "missing_reason": item.get("missing_reason"),
                    }
                )
    return {
        "status": remaining.get("status"),
        "audit_issue_count": int(remaining.get("audit_issue_count") or 0),
        "total_missing_deliverables": int(gap.get("total_missing_deliverables") or 0),
        "open_category_count": int(gap.get("open_category_count") or 0),
        "categories": rows,
        "missing_counts_by_category": missing_by_category,
        "present_counts_by_category": present_by_category,
        "missing_artifacts": missing_artifacts,
        "training_complete": missing_by_category.get("training") == 0,
        "evaluation_complete": missing_by_category.get("evaluation") == 0,
        "acceptance_complete": missing_by_category.get("acceptance") == 0,
        "formal_acceptance_complete": missing_by_category.get("formal_acceptance") == 0,
    }


def _h02_summary(h02: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": h02.get("status"),
        "formal_output_accepted": bool(h02.get("formal_output_accepted")),
        "paper_result_input_allowed": bool(h02.get("paper_result_input_allowed")),
        "blockers": _strings(h02.get("blockers")),
        "gate3_formal_decision": _nested(h02, "formal_checks", "gate3_formal_decision"),
        "gate3_formal_audit_passed": _nested(h02, "formal_checks", "gate3_formal_audit_passed"),
        "remote_pullback_artifacts_present": _nested(h02, "formal_checks", "remote_pullback_artifacts_present"),
    }


def _permissions(status_report: dict[str, Any]) -> dict[str, Any]:
    permissions = status_report.get("permissions_now") if isinstance(status_report.get("permissions_now"), dict) else {}
    return {
        "local_training_allowed_now": bool(permissions.get("local_training_allowed_now")),
        "remote_preflight_allowed_now": bool(permissions.get("remote_preflight_allowed_now")),
        "remote_training_allowed_now": bool(permissions.get("remote_training_allowed_now")),
        "formal_h01_evaluation_allowed_now": bool(permissions.get("formal_h01_evaluation_allowed_now")),
        "formal_h02_acceptance_allowed_now": bool(permissions.get("formal_h02_acceptance_allowed_now")),
        "formal_claim_allowed_now": bool(permissions.get("formal_claim_allowed_now")),
        "source_freshness_ready_for_remote_preflight": bool(permissions.get("source_freshness_ready_for_remote_preflight")),
    }


def _next_gate(*, failure: dict[str, Any], deliverables: dict[str, Any], h02_summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "requires_protocol_decision_before_new_success_attempt"
        if failure["failure_mode"] == "threshold_failure"
        else "requires_failure_audit_cleanup",
        "current_failure_can_be_recorded_as_negative_formal_evidence": failure["failure_mode"] == "threshold_failure",
        "same_contract_success_rerun_allowed": False,
        "new_or_revised_contract_required_before_new_training": True,
        "read_only_actions_allowed_now": [
            "record this warm-start Gate3 threshold failure in experiment ledger",
            "draft v2 protocol options without changing the current formal result",
            "audit failure modes from existing eval CSV/logs without training",
        ],
        "actions_requiring_new_or_revised_contract": [
            "change success threshold, reward, curriculum, architecture, observation, or training budget",
            "train a new PPO checkpoint intended to replace the failed checkpoint",
            "rerun formal Gate3 as a new success attempt",
        ],
        "explicitly_disallowed_now": [
            "local PPO training",
            "paper success claim that PPO replaces RS",
            "threshold or protocol reinterpretation after seeing this failure",
            "using H02/paper tables as formal result input while H02 acceptance is blocked",
        ],
        "remaining_formal_blocker": {
            "artifact_id": "h02_formal_output_acceptance",
            "missing": not deliverables["formal_acceptance_complete"],
            "h02_status": h02_summary["status"],
            "h02_blockers": h02_summary["blockers"],
        },
    }


def _audit_issues(
    *,
    failure: dict[str, Any],
    deliverables: dict[str, Any],
    h02_summary: dict[str, Any],
    permissions: dict[str, Any],
    remaining: dict[str, Any],
    remote_safety: dict[str, Any],
    source_freshness: dict[str, Any],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if failure["formal_decision"] == "pass":
        issues.append(_issue("gate3_passed_not_failure_triage", "Failure triage must not be used for a passing Gate3 audit."))
    if failure["failure_mode"] != "threshold_failure":
        issues.append(_issue("gate3_failure_not_proven_by_threshold", "Gate3 failure must be backed by rate below threshold."))
    if failure["episodes"] is None or int(failure["episodes"]) < 64:
        issues.append(_issue("gate3_episode_count_below_formal_minimum", "Formal Gate3 triage expects at least 64 evaluation episodes."))
    for category in ("training", "evaluation", "acceptance"):
        if deliverables["missing_counts_by_category"].get(category, 0) != 0:
            issues.append(_issue(f"{category}_deliverables_not_complete", f"{category} deliverables must be complete before failure triage is authoritative."))
    if deliverables["formal_acceptance_complete"]:
        issues.append(_issue("formal_acceptance_unexpectedly_complete", "Failed Gate3 triage should not have H02 formal acceptance complete."))
    if h02_summary["formal_output_accepted"] or h02_summary["paper_result_input_allowed"]:
        issues.append(_issue("h02_accepts_failed_gate3", "H02 must not accept formal paper inputs from a failed Gate3 audit."))
    if "gate3_formal_audit_not_passed" not in h02_summary["blockers"]:
        issues.append(_issue("h02_missing_gate3_failure_blocker", "H02 blockers must include gate3_formal_audit_not_passed."))
    if permissions["local_training_allowed_now"]:
        issues.append(_issue("local_training_allowed", "Local PPO training must remain disallowed."))
    if permissions["formal_claim_allowed_now"]:
        issues.append(_issue("formal_claim_allowed", "Formal performance claims must remain disallowed."))
    if int(remaining.get("audit_issue_count") or 0) != 0:
        issues.append(_issue("remaining_deliverables_audit_issues_open", "Remaining deliverables audit issues must be closed."))
    if remote_safety.get("status") != "remote_packet_safety_audit_passed":
        issues.append(_issue("remote_packet_safety_not_passed", "Remote packet safety audit must pass before failure triage can be trusted."))
    if bool(source_freshness.get("blocking_regeneration_required_before_remote_formal_execution")):
        issues.append(_issue("source_freshness_blocking_regeneration_required", "Source freshness must not require blocking regeneration."))
    return _unique_issues(issues)


def _markdown(manifest: dict[str, Any]) -> str:
    failure = manifest["formal_gate_failure"]
    deliverables = manifest["training_evaluation_acceptance_artifacts"]
    lines = [
        "# Module2 Formal Gate Failure Triage",
        "",
        "This file is a gate-control artifact, not paper result material.",
        "",
        "## Gate3 Outcome",
        "",
        f"- formal_decision: `{failure['formal_decision']}`",
        f"- evaluator_decision: `{failure['evaluator_decision']}`",
        f"- episodes: `{failure['episodes']}`",
        f"- terminal_rs_success_rate: `{failure['terminal_rs_success_rate']}`",
        f"- required_success_threshold: `{failure['required_success_threshold']}`",
        f"- threshold_deficit: `{failure['threshold_deficit']}`",
        f"- failure_mode: `{failure['failure_mode']}`",
        "",
        "## Deliverable Status",
        "",
        "| category | status | present | missing |",
        "|---|---:|---:|---:|",
    ]
    for row in deliverables["categories"]:
        lines.append(
            f"| `{row['category']}` | `{row['status']}` | `{row['present_count']}` | `{row['missing_count']}` |"
        )
    lines.extend(["", "## Missing Formal Acceptance"])
    if deliverables["missing_artifacts"]:
        for item in deliverables["missing_artifacts"]:
            lines.append(f"- `{item['category']}:{item['artifact_id']}`: {item['missing_reason']}")
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Next Gate",
            "",
            f"- status: `{manifest['next_gate']['status']}`",
            f"- new_or_revised_contract_required_before_new_training: `{manifest['next_gate']['new_or_revised_contract_required_before_new_training']}`",
            f"- same_contract_success_rerun_allowed: `{manifest['next_gate']['same_contract_success_rerun_allowed']}`",
            "",
            "## Boundaries",
        ]
    )
    for boundary in manifest["claim_boundaries"]:
        lines.append(f"- {boundary}")
    lines.extend(["", "## Audit", "", f"- status: `{manifest['status']}`", f"- audit_issue_count: `{manifest['audit_issue_count']}`"])
    return "\n".join(lines) + "\n"


def _read_json(path: Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def _source_head() -> str:
    return module2_source_head()


def _number(value: Any) -> float | None:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _int(value: Any) -> int | None:
    try:
        if value is None:
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def _strings(value: Any) -> list[str]:
    if not isinstance(value, (list, tuple)):
        return []
    return [str(item) for item in value if item]


def _nested(payload: dict[str, Any], *keys: str) -> Any:
    current: Any = payload
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _issue(issue_id: str, message: str) -> dict[str, str]:
    return {"issue_id": issue_id, "message": message}


def _unique_issues(issues: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for issue in issues:
        issue_id = str(issue.get("issue_id") or "")
        if issue_id and issue_id not in seen:
            seen.add(issue_id)
            out.append(dict(issue))
    return out


if __name__ == "__main__":
    raise SystemExit(main())
