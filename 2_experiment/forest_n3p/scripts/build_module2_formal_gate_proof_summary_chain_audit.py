from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_formal_gate_proof_summary_chain_audit")
DEFAULT_REMAINING_DELIVERABLES = Path(
    "0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json"
)
DEFAULT_FORMAL_GATE_PROOF_AUDIT = Path(
    "0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json"
)
DEFAULT_FORMAL_GATE_STATUS_REPORT = Path(
    "0_trials/module2_formal_gate_status_report/formal_gate_status_report.json"
)
DEFAULT_POST_F02_6_PLAN_AUDIT = Path(
    "0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json"
)
DEFAULT_REMOTE_PACKET_SAFETY_AUDIT = Path(
    "0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json"
)
DEFAULT_FORMAL_GATE_GAP_AUDIT = Path(
    "0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json"
)
DEFAULT_CLAIM_SAFETY = Path("0_trials/module2_claim_safety/module2_claim_safety.json")
DEFAULT_PAPER_READINESS = Path("0_trials/module2_paper_readiness/module2_paper_readiness.json")

FORMAL_CATEGORIES = ("training", "evaluation", "acceptance", "formal_acceptance")


@dataclass(frozen=True)
class ProofSummarySource:
    row_id: str
    path: Path
    summary_key_path: tuple[str, ...]


@dataclass(frozen=True)
class FormalGateProofSummaryChainAuditConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    remaining_deliverables_path: Path = DEFAULT_REMAINING_DELIVERABLES
    formal_gate_proof_audit_path: Path = DEFAULT_FORMAL_GATE_PROOF_AUDIT
    formal_gate_status_report_path: Path = DEFAULT_FORMAL_GATE_STATUS_REPORT
    post_f02_6_plan_audit_path: Path = DEFAULT_POST_F02_6_PLAN_AUDIT
    remote_packet_safety_audit_path: Path = DEFAULT_REMOTE_PACKET_SAFETY_AUDIT
    formal_gate_gap_audit_path: Path = DEFAULT_FORMAL_GATE_GAP_AUDIT
    claim_safety_path: Path = DEFAULT_CLAIM_SAFETY
    paper_readiness_path: Path = DEFAULT_PAPER_READINESS


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = FormalGateProofSummaryChainAuditConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        remaining_deliverables_path=args.remaining_deliverables,
        formal_gate_proof_audit_path=args.formal_gate_proof_audit,
        formal_gate_status_report_path=args.formal_gate_status_report,
        post_f02_6_plan_audit_path=args.post_f02_6_plan_audit,
        remote_packet_safety_audit_path=args.remote_packet_safety_audit,
        formal_gate_gap_audit_path=args.formal_gate_gap_audit,
        claim_safety_path=args.claim_safety,
        paper_readiness_path=args.paper_readiness,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "formal_gate_proof_summary_chain_audit.json"
    markdown_out = config.markdown_out or output_dir / "formal_gate_proof_summary_chain_audit.md"
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


def build_manifest(config: FormalGateProofSummaryChainAuditConfig) -> dict[str, Any]:
    baseline_payload = _read_json(config.remaining_deliverables_path)
    baseline_summary = _remaining_deliverables_summary(baseline_payload)
    baseline_signature = _signature(baseline_summary)
    rows = [
        _row_from_summary(
            row_id="remaining_deliverables_top_level",
            path=config.remaining_deliverables_path,
            summary=baseline_summary,
            baseline_signature=baseline_signature,
        )
    ]
    for source in _sources(config):
        rows.append(_row(source=source, baseline_signature=baseline_signature))

    next_action_guard_rows = _next_action_guard_rows(config)
    next_action_guard_baseline_signature = next_action_guard_rows[0]["signature"] if next_action_guard_rows else {}
    next_required_deliverables_rows = _next_required_deliverables_rows(config)
    next_required_deliverables_baseline_signature = (
        next_required_deliverables_rows[0]["signature"] if next_required_deliverables_rows else {}
    )
    issues = (
        _audit_issues(rows=rows, baseline_summary=baseline_summary)
        + _next_action_guard_issues(rows=next_action_guard_rows)
        + _next_required_deliverables_issues(rows=next_required_deliverables_rows)
    )
    proof_open = _proof_open(baseline_summary)
    if issues:
        status = "formal_gate_proof_summary_chain_audit_failed"
    elif proof_open:
        status = "formal_gate_proof_summary_chain_consistent_blocked"
    else:
        status = "formal_gate_proof_summary_chain_consistent_ready"

    return {
        "schema_version": 1,
        "artifact_name": "module2_formal_gate_proof_summary_chain_audit",
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
            "remaining_deliverables": str(config.remaining_deliverables_path),
            "formal_gate_proof_audit": str(config.formal_gate_proof_audit_path),
            "formal_gate_status_report": str(config.formal_gate_status_report_path),
            "post_f02_6_plan_audit": str(config.post_f02_6_plan_audit_path),
            "remote_packet_safety_audit": str(config.remote_packet_safety_audit_path),
            "formal_gate_gap_audit": str(config.formal_gate_gap_audit_path),
            "claim_safety": str(config.claim_safety_path),
            "paper_readiness": str(config.paper_readiness_path),
        },
        "baseline_summary": baseline_summary,
        "baseline_signature": baseline_signature,
        "proof_open": proof_open,
        "row_count": len(rows),
        "consistent_row_count": sum(1 for row in rows if row["signature_matches_baseline"]),
        "missing_row_count": sum(1 for row in rows if not row["present"]),
        "mismatch_row_count": sum(1 for row in rows if row["present"] and not row["signature_matches_baseline"]),
        "next_action_guard_row_count": len(next_action_guard_rows),
        "next_action_guard_consistent_row_count": sum(
            1 for row in next_action_guard_rows if row["signature_matches_baseline"]
        ),
        "next_required_deliverables_row_count": len(next_required_deliverables_rows),
        "next_required_deliverables_consistent_row_count": sum(
            1 for row in next_required_deliverables_rows if row["signature_matches_baseline"]
        ),
        "h02_paper_result_input_allowed": baseline_summary["h02_paper_result_input_allowed"],
        "audit_issue_count": len(issues),
        "audit_issues": issues,
        "chain_rows": rows,
        "chain_rows_by_id": {row["row_id"]: row for row in rows},
        "next_action_guard_baseline_signature": next_action_guard_baseline_signature,
        "next_action_guard_rows": next_action_guard_rows,
        "next_action_guard_rows_by_id": {row["row_id"]: row for row in next_action_guard_rows},
        "next_required_deliverables_baseline_signature": next_required_deliverables_baseline_signature,
        "next_required_deliverables_rows": next_required_deliverables_rows,
        "next_required_deliverables_rows_by_id": {row["row_id"]: row for row in next_required_deliverables_rows},
        "claim_boundaries": [
            "This audit is a local read-only consistency check over existing formal-gate summary fields.",
            "It does not execute proof commands, run training, run remote preflight, evaluate PPO, pull back artifacts, or write paper results.",
            "A consistent blocked chain only proves the downstream artifacts agree that the formal gate is still blocked.",
            "Next-action and next-required-deliverable consistency does not authorize the next action; it only checks that the artifacts agree on the current blocked lane.",
            "Formal PPO-vs-RS performance claims still require the missing training, evaluation, acceptance, and H01/H02 artifacts to be produced and audited.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit Module2 formal-gate proof summary propagation across downstream artifacts."
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--remaining-deliverables", type=Path, default=DEFAULT_REMAINING_DELIVERABLES)
    parser.add_argument("--formal-gate-proof-audit", type=Path, default=DEFAULT_FORMAL_GATE_PROOF_AUDIT)
    parser.add_argument("--formal-gate-status-report", type=Path, default=DEFAULT_FORMAL_GATE_STATUS_REPORT)
    parser.add_argument("--post-f02-6-plan-audit", type=Path, default=DEFAULT_POST_F02_6_PLAN_AUDIT)
    parser.add_argument("--remote-packet-safety-audit", type=Path, default=DEFAULT_REMOTE_PACKET_SAFETY_AUDIT)
    parser.add_argument("--formal-gate-gap-audit", type=Path, default=DEFAULT_FORMAL_GATE_GAP_AUDIT)
    parser.add_argument("--claim-safety", type=Path, default=DEFAULT_CLAIM_SAFETY)
    parser.add_argument("--paper-readiness", type=Path, default=DEFAULT_PAPER_READINESS)
    return parser.parse_args(list(argv) if argv is not None else None)


def _sources(config: FormalGateProofSummaryChainAuditConfig) -> list[ProofSummarySource]:
    return [
        ProofSummarySource(
            "formal_gate_proof_audit_remaining_summary",
            config.formal_gate_proof_audit_path,
            ("remaining_deliverables_top_level_summary",),
        ),
        ProofSummarySource(
            "formal_gate_status_report_proof_summary",
            config.formal_gate_status_report_path,
            ("formal_gate_proof_audit_remaining_deliverables_top_level_summary",),
        ),
        ProofSummarySource(
            "status_report_remote_safety_proof_summary",
            config.formal_gate_status_report_path,
            ("remote_packet_safety_proof_deliverables_summary",),
        ),
        ProofSummarySource(
            "status_report_remote_safety_status_report_proof_summary",
            config.formal_gate_status_report_path,
            ("remote_packet_safety_status_report_proof_deliverables_summary",),
        ),
        ProofSummarySource(
            "post_plan_status_report_proof_summary",
            config.post_f02_6_plan_audit_path,
            ("status_report_proof_audit_deliverables_summary",),
        ),
        ProofSummarySource(
            "remote_safety_post_plan_proof_summary",
            config.remote_packet_safety_audit_path,
            ("cross_gate_summary", "post_plan_proof_audit_deliverables_summary"),
        ),
        ProofSummarySource(
            "remote_safety_post_plan_status_report_proof_summary",
            config.remote_packet_safety_audit_path,
            ("cross_gate_summary", "post_plan_status_report_proof_audit_deliverables_summary"),
        ),
        ProofSummarySource(
            "gap_audit_remote_safety_proof_summary",
            config.formal_gate_gap_audit_path,
            ("remote_packet_safety", "proof_deliverables_summary"),
        ),
        ProofSummarySource(
            "gap_audit_remote_safety_status_report_proof_summary",
            config.formal_gate_gap_audit_path,
            ("remote_packet_safety", "status_report_proof_deliverables_summary"),
        ),
        ProofSummarySource(
            "claim_safety_remote_safety_proof_summary",
            config.claim_safety_path,
            ("status_report_remote_packet_safety_proof_deliverables_summary",),
        ),
        ProofSummarySource(
            "claim_safety_remote_safety_status_report_proof_summary",
            config.claim_safety_path,
            ("status_report_remote_packet_safety_status_report_proof_deliverables_summary",),
        ),
        ProofSummarySource(
            "paper_readiness_remote_safety_proof_summary",
            config.paper_readiness_path,
            ("claim_safety_remote_packet_safety_proof_deliverables_summary",),
        ),
        ProofSummarySource(
            "paper_readiness_remote_safety_status_report_proof_summary",
            config.paper_readiness_path,
            ("claim_safety_remote_packet_safety_status_report_proof_deliverables_summary",),
        ),
    ]


def _row(*, source: ProofSummarySource, baseline_signature: dict[str, Any]) -> dict[str, Any]:
    payload = _read_json(source.path)
    raw_summary = _get_nested(payload, source.summary_key_path)
    summary = _normalize_summary(raw_summary)
    return _row_from_summary(
        row_id=source.row_id,
        path=source.path,
        summary=summary,
        baseline_signature=baseline_signature,
        summary_key_path=".".join(source.summary_key_path),
    )


def _row_from_summary(
    *,
    row_id: str,
    path: Path,
    summary: dict[str, Any],
    baseline_signature: dict[str, Any],
    summary_key_path: str = "top_level",
) -> dict[str, Any]:
    signature = _signature(summary)
    present = summary["present"]
    return {
        "row_id": row_id,
        "path": str(path),
        "summary_key_path": summary_key_path,
        "present": present,
        "signature_matches_baseline": present and signature == baseline_signature,
        "missing_counts_by_formal_category": summary["missing_counts_by_formal_category"],
        "missing_matrix_ids_by_formal_category": summary["missing_matrix_ids_by_formal_category"],
        "next_blocked_lane": summary["next_blocked_lane"],
        "h01_status": summary["h01_status"],
        "h02_status": summary["h02_status"],
        "h02_formal_output_accepted": summary["h02_formal_output_accepted"],
        "h02_paper_result_input_allowed": summary["h02_paper_result_input_allowed"],
        "signature": signature,
    }


def _next_action_guard_rows(config: FormalGateProofSummaryChainAuditConfig) -> list[dict[str, Any]]:
    sources = [
        (
            "status_report_next_action_guard",
            config.formal_gate_status_report_path,
            ("next_action_guard_summary",),
        ),
        (
            "claim_safety_status_report_next_action_guard",
            config.claim_safety_path,
            ("status_report_next_action_guard_summary",),
        ),
        (
            "paper_readiness_claim_safety_next_action_guard",
            config.paper_readiness_path,
            ("claim_safety_next_action_guard_summary",),
        ),
    ]
    baseline_signature: dict[str, Any] | None = None
    rows: list[dict[str, Any]] = []
    for row_id, path, key_path in sources:
        summary = _normalize_next_action_guard(_get_nested(_read_json(path), key_path))
        signature = _next_action_guard_signature(summary)
        if baseline_signature is None:
            baseline_signature = signature
        rows.append(
            {
                "row_id": row_id,
                "path": str(path),
                "summary_key_path": ".".join(key_path),
                "present": summary["present"],
                "status": summary["status"],
                "expected_next_action_id": summary["expected_next_action_id"],
                "all_execution_disabled_now": summary["all_execution_disabled_now"],
                "execution_leak_count": summary["execution_leak_count"],
                "remote_execution_allowed_count": summary["remote_execution_allowed_count"],
                "remote_stage_allowed_count": summary["remote_stage_allowed_count"],
                "signature": signature,
                "signature_matches_baseline": summary["present"] and signature == baseline_signature,
            }
        )
    return rows


def _next_required_deliverables_rows(config: FormalGateProofSummaryChainAuditConfig) -> list[dict[str, Any]]:
    sources = [
        (
            "status_report_next_required_formal_deliverables",
            config.formal_gate_status_report_path,
            ("next_required_formal_deliverables",),
        ),
        (
            "claim_safety_status_report_next_required_formal_deliverables",
            config.claim_safety_path,
            ("status_report_next_required_formal_deliverables",),
        ),
        (
            "paper_readiness_claim_safety_next_required_formal_deliverables",
            config.paper_readiness_path,
            ("claim_safety_next_required_formal_deliverables",),
        ),
    ]
    baseline_signature: dict[str, Any] | None = None
    rows: list[dict[str, Any]] = []
    for row_id, path, key_path in sources:
        summary = _normalize_next_required_deliverables(_get_nested(_read_json(path), key_path))
        signature = _next_required_deliverables_signature(summary)
        if baseline_signature is None:
            baseline_signature = signature
        rows.append(
            {
                "row_id": row_id,
                "path": str(path),
                "summary_key_path": ".".join(key_path),
                "present": summary["present"],
                "status": summary["status"],
                "not_paper_result_material": summary["not_paper_result_material"],
                "runs_training": summary["runs_training"],
                "runs_remote_preflight": summary["runs_remote_preflight"],
                "total_missing_deliverables": summary["total_missing_deliverables"],
                "blocked_category_count": summary["blocked_category_count"],
                "row_count": summary["row_count"],
                "signature": signature,
                "signature_matches_baseline": summary["present"] and signature == baseline_signature,
            }
        )
    return rows


def _audit_issues(*, rows: Sequence[dict[str, Any]], baseline_summary: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if not baseline_summary["present"]:
        issues.append(
            {
                "issue_id": "missing_baseline_remaining_deliverables_summary",
                "message": "Remaining-deliverables artifact must expose the baseline proof summary.",
            }
        )
    proof_open = _proof_open(baseline_summary)
    for row in rows:
        row_id = row["row_id"]
        if not row["present"]:
            issues.append(
                {
                    "issue_id": f"{row_id}_missing_summary",
                    "message": "Downstream artifact is missing the propagated proof-deliverables summary.",
                    "path": row["path"],
                    "summary_key_path": row["summary_key_path"],
                }
            )
            continue
        if not row["signature_matches_baseline"]:
            issues.append(
                {
                    "issue_id": f"{row_id}_summary_mismatch",
                    "message": "Downstream proof-deliverables summary does not match the remaining-deliverables baseline.",
                    "path": row["path"],
                    "summary_key_path": row["summary_key_path"],
                    "observed_signature": row["signature"],
                    "expected_signature": _signature(baseline_summary),
                }
            )
        if proof_open and row["h02_paper_result_input_allowed"] is True:
            issues.append(
                {
                    "issue_id": f"{row_id}_allows_h02_paper_input_while_proof_open",
                    "message": "H02 paper-result input must remain false while formal proof deliverables are missing.",
                    "path": row["path"],
                }
            )
        if proof_open and row["h02_formal_output_accepted"] is True:
            issues.append(
                {
                    "issue_id": f"{row_id}_accepts_h02_output_while_proof_open",
                    "message": "H02 formal output must remain unaccepted while formal proof deliverables are missing.",
                    "path": row["path"],
                }
            )
    return _unique_issues(issues)


def _next_action_guard_issues(*, rows: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for row in rows:
        row_id = row["row_id"]
        if not row["present"]:
            issues.append(
                {
                    "issue_id": f"{row_id}_missing_summary",
                    "message": "Downstream artifact is missing the propagated next-action guard summary.",
                    "path": row["path"],
                    "summary_key_path": row["summary_key_path"],
                }
            )
            continue
        if not row["signature_matches_baseline"]:
            issues.append(
                {
                    "issue_id": f"{row_id}_summary_mismatch",
                    "message": "Downstream next-action guard summary does not match the status-report baseline.",
                    "path": row["path"],
                    "summary_key_path": row["summary_key_path"],
                    "observed_signature": row["signature"],
                    "expected_signature": rows[0]["signature"] if rows else {},
                }
            )
        if row["status"] != "next_action_guard_passed":
            issues.append(
                {
                    "issue_id": f"{row_id}_not_passed",
                    "message": "Next-action guard must remain passed before downstream formal-claim artifacts can rely on it.",
                    "path": row["path"],
                }
            )
        if row["execution_leak_count"] > 0 or row["remote_execution_allowed_count"] > 0 or row["remote_stage_allowed_count"] > 0:
            issues.append(
                {
                    "issue_id": f"{row_id}_execution_leak",
                    "message": "Next-action guard reports execution leakage while F02.6 is pending.",
                    "path": row["path"],
                }
            )
    return _unique_issues(issues)


def _next_required_deliverables_issues(*, rows: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for row in rows:
        row_id = row["row_id"]
        if not row["present"]:
            issues.append(
                {
                    "issue_id": f"{row_id}_missing_summary",
                    "message": "Downstream artifact is missing the propagated next-required formal deliverables summary.",
                    "path": row["path"],
                    "summary_key_path": row["summary_key_path"],
                }
            )
            continue
        if not row["signature_matches_baseline"]:
            issues.append(
                {
                    "issue_id": f"{row_id}_summary_mismatch",
                    "message": "Downstream next-required formal deliverables summary does not match the status-report baseline.",
                    "path": row["path"],
                    "summary_key_path": row["summary_key_path"],
                    "observed_signature": row["signature"],
                    "expected_signature": rows[0]["signature"] if rows else {},
                }
            )
        if row["not_paper_result_material"] is not True:
            issues.append(
                {
                    "issue_id": f"{row_id}_marked_as_paper_result",
                    "message": "Next-required deliverables summary must remain non-result audit material.",
                    "path": row["path"],
                }
            )
        if row["runs_training"] is True:
            issues.append(
                {
                    "issue_id": f"{row_id}_runs_training",
                    "message": "Next-required deliverables summary must not run or authorize training.",
                    "path": row["path"],
                }
            )
        if row["runs_remote_preflight"] is True:
            issues.append(
                {
                    "issue_id": f"{row_id}_runs_remote_preflight",
                    "message": "Next-required deliverables summary must not run or authorize remote preflight.",
                    "path": row["path"],
                }
            )
    return _unique_issues(issues)


def _remaining_deliverables_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return _normalize_summary(
        {
            "present": bool(
                payload.get("missing_counts_by_formal_category")
                or payload.get("missing_matrix_ids_by_formal_category")
            ),
            "missing_counts_by_formal_category": payload.get("missing_counts_by_formal_category"),
            "missing_matrix_ids_by_formal_category": payload.get("missing_matrix_ids_by_formal_category"),
            "next_blocked_lane": payload.get("next_blocked_lane"),
            "h01_status": payload.get("h01_status"),
            "h02_status": payload.get("h02_status"),
            "h02_formal_output_accepted": payload.get("h02_formal_output_accepted"),
            "h02_paper_result_input_allowed": payload.get("h02_paper_result_input_allowed"),
        }
    )


def _normalize_next_action_guard(raw: Any) -> dict[str, Any]:
    summary = raw if isinstance(raw, dict) else {}
    return {
        "present": bool(summary.get("present")) or bool(summary),
        "status": summary.get("status"),
        "pending_f02_6_decision": summary.get("pending_f02_6_decision")
        if isinstance(summary.get("pending_f02_6_decision"), bool)
        else None,
        "next_blocked_lane_id": summary.get("next_blocked_lane_id"),
        "expected_next_action_id": summary.get("expected_next_action_id"),
        "handoff_next_action_id": summary.get("handoff_next_action_id"),
        "handoff_next_action_requires_dr_sun": summary.get("handoff_next_action_requires_dr_sun")
        if isinstance(summary.get("handoff_next_action_requires_dr_sun"), bool)
        else None,
        "missing_artifacts_next_action_id": summary.get("missing_artifacts_next_action_id"),
        "decision_intake_next_blocked_lane": summary.get("decision_intake_next_blocked_lane"),
        "all_execution_disabled_now": summary.get("all_execution_disabled_now")
        if isinstance(summary.get("all_execution_disabled_now"), bool)
        else None,
        "execution_leak_count": int(summary.get("execution_leak_count") or 0),
        "remote_execution_allowed_count": int(summary.get("remote_execution_allowed_count") or 0),
        "remote_stage_allowed_count": int(summary.get("remote_stage_allowed_count") or 0),
        "violation_count": int(summary.get("violation_count") or 0),
        "execution_leak_surface_ids": _strings(summary.get("execution_leak_surface_ids")),
    }


def _next_action_guard_signature(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": summary["status"],
        "pending_f02_6_decision": summary["pending_f02_6_decision"],
        "next_blocked_lane_id": summary["next_blocked_lane_id"],
        "expected_next_action_id": summary["expected_next_action_id"],
        "handoff_next_action_id": summary["handoff_next_action_id"],
        "handoff_next_action_requires_dr_sun": summary["handoff_next_action_requires_dr_sun"],
        "missing_artifacts_next_action_id": summary["missing_artifacts_next_action_id"],
        "decision_intake_next_blocked_lane": summary["decision_intake_next_blocked_lane"],
        "all_execution_disabled_now": summary["all_execution_disabled_now"],
        "execution_leak_count": summary["execution_leak_count"],
        "remote_execution_allowed_count": summary["remote_execution_allowed_count"],
        "remote_stage_allowed_count": summary["remote_stage_allowed_count"],
        "violation_count": summary["violation_count"],
        "execution_leak_surface_ids": sorted(summary["execution_leak_surface_ids"]),
    }


def _normalize_next_required_deliverables(raw: Any) -> dict[str, Any]:
    summary = raw if isinstance(raw, dict) else {}
    rows = _normalize_deliverable_rows(summary.get("rows"))
    return {
        "present": bool(summary.get("present")) or bool(summary),
        "status": summary.get("status"),
        "execution_boundary": summary.get("execution_boundary"),
        "not_paper_result_material": summary.get("not_paper_result_material")
        if isinstance(summary.get("not_paper_result_material"), bool)
        else None,
        "runs_training": summary.get("runs_training") if isinstance(summary.get("runs_training"), bool) else None,
        "runs_remote_preflight": summary.get("runs_remote_preflight")
        if isinstance(summary.get("runs_remote_preflight"), bool)
        else None,
        "total_missing_deliverables": int(summary.get("total_missing_deliverables") or 0),
        "blocked_category_count": int(summary.get("blocked_category_count") or 0),
        "blocked_categories": _strings(summary.get("blocked_categories")),
        "category_order": _strings(summary.get("category_order")),
        "row_count": len(rows),
        "rows": rows,
    }


def _normalize_deliverable_rows(raw_rows: Any) -> dict[str, dict[str, Any]]:
    if isinstance(raw_rows, dict):
        iterable_rows = (
            dict(raw_row, matrix_id=matrix_id) if isinstance(raw_row, dict) and "matrix_id" not in raw_row else raw_row
            for matrix_id, raw_row in raw_rows.items()
        )
    elif isinstance(raw_rows, list):
        iterable_rows = (raw_row for raw_row in raw_rows if isinstance(raw_row, dict))
    else:
        iterable_rows = ()
    rows: dict[str, dict[str, Any]] = {}
    for raw_row in iterable_rows:
        if not isinstance(raw_row, dict):
            continue
        matrix_id = raw_row.get("matrix_id")
        if not matrix_id:
            continue
        rows[str(matrix_id)] = {
            "category": raw_row.get("category"),
            "current_state": raw_row.get("current_state"),
            "responsible_stage_id": raw_row.get("responsible_stage_id"),
            "responsible_stage_allowed_now": raw_row.get("responsible_stage_allowed_now")
            if isinstance(raw_row.get("responsible_stage_allowed_now"), bool)
            else None,
            "proof_command_ids": _strings(raw_row.get("proof_command_ids")),
            "invalid_substitute_count": int(raw_row.get("invalid_substitute_count") or 0),
        }
    return rows


def _next_required_deliverables_signature(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": summary["status"],
        "execution_boundary": summary["execution_boundary"],
        "not_paper_result_material": summary["not_paper_result_material"],
        "runs_training": summary["runs_training"],
        "runs_remote_preflight": summary["runs_remote_preflight"],
        "total_missing_deliverables": summary["total_missing_deliverables"],
        "blocked_category_count": summary["blocked_category_count"],
        "blocked_categories": summary["blocked_categories"],
        "category_order": summary["category_order"],
        "row_count": summary["row_count"],
        "rows": {
            matrix_id: {
                "category": row["category"],
                "current_state": row["current_state"],
                "responsible_stage_id": row["responsible_stage_id"],
                "responsible_stage_allowed_now": row["responsible_stage_allowed_now"],
                "proof_command_ids": sorted(row["proof_command_ids"]),
                "invalid_substitute_count": row["invalid_substitute_count"],
            }
            for matrix_id, row in sorted(summary["rows"].items())
        },
    }


def _normalize_summary(raw: Any) -> dict[str, Any]:
    summary = raw if isinstance(raw, dict) else {}
    counts = summary.get("missing_counts_by_formal_category")
    ids_by_category = summary.get("missing_matrix_ids_by_formal_category")
    normalized_counts = {
        category: int(counts.get(category, 0) or 0) for category in FORMAL_CATEGORIES
    } if isinstance(counts, dict) else {}
    normalized_ids = {
        category: [str(item) for item in ids_by_category.get(category, []) if item]
        for category in FORMAL_CATEGORIES
    } if isinstance(ids_by_category, dict) else {}
    return {
        "present": bool(summary.get("present", bool(normalized_counts or normalized_ids))),
        "missing_counts_by_formal_category": normalized_counts,
        "missing_matrix_ids_by_formal_category": normalized_ids,
        "next_blocked_lane": summary.get("next_blocked_lane"),
        "h01_status": summary.get("h01_status"),
        "h02_status": summary.get("h02_status"),
        "h02_formal_output_accepted": summary.get("h02_formal_output_accepted")
        if isinstance(summary.get("h02_formal_output_accepted"), bool)
        else None,
        "h02_paper_result_input_allowed": summary.get("h02_paper_result_input_allowed")
        if isinstance(summary.get("h02_paper_result_input_allowed"), bool)
        else None,
    }


def _signature(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "missing_counts_by_formal_category": {
            category: int(summary.get("missing_counts_by_formal_category", {}).get(category, 0) or 0)
            for category in FORMAL_CATEGORIES
        },
        "missing_matrix_ids_by_formal_category": {
            category: list(summary.get("missing_matrix_ids_by_formal_category", {}).get(category, []))
            for category in FORMAL_CATEGORIES
        },
        "next_blocked_lane": summary.get("next_blocked_lane"),
        "h01_status": summary.get("h01_status"),
        "h02_status": summary.get("h02_status"),
        "h02_formal_output_accepted": summary.get("h02_formal_output_accepted"),
        "h02_paper_result_input_allowed": summary.get("h02_paper_result_input_allowed"),
    }


def _proof_open(summary: dict[str, Any]) -> bool:
    return sum(int(value) for value in summary["missing_counts_by_formal_category"].values()) > 0


def _get_nested(payload: dict[str, Any], key_path: Sequence[str]) -> Any:
    current: Any = payload
    for key in key_path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _unique_issues(issues: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for issue in issues:
        issue_id = str(issue.get("issue_id") or "")
        if not issue_id or issue_id in seen:
            continue
        seen.add(issue_id)
        out.append(issue)
    return out


def _markdown(manifest: dict[str, Any]) -> str:
    baseline = manifest["baseline_summary"]
    lines = [
        "# Module2 Formal Gate Proof Summary Chain Audit",
        "",
        "This file checks that formal-gate proof-deliverables summaries remain consistent across downstream gate artifacts. It is not a training run, evaluation, remote preflight, paper table, or paper result.",
        "",
        f"- status: `{manifest['status']}`",
        f"- audit_issue_count: `{manifest['audit_issue_count']}`",
        f"- proof_open: `{manifest['proof_open']}`",
        f"- row_count: `{manifest['row_count']}`",
        f"- consistent_row_count: `{manifest['consistent_row_count']}`",
        f"- missing_row_count: `{manifest['missing_row_count']}`",
        f"- mismatch_row_count: `{manifest['mismatch_row_count']}`",
        f"- next_action_guard_row_count: `{manifest['next_action_guard_row_count']}`",
        f"- next_action_guard_consistent_row_count: `{manifest['next_action_guard_consistent_row_count']}`",
        f"- next_required_deliverables_row_count: `{manifest['next_required_deliverables_row_count']}`",
        f"- next_required_deliverables_consistent_row_count: `{manifest['next_required_deliverables_consistent_row_count']}`",
        f"- executes_commands: `{manifest['executes_commands']}`",
        f"- runs_training: `{manifest['runs_training']}`",
        f"- runs_remote_preflight: `{manifest['runs_remote_preflight']}`",
        f"- formal_claim_allowed: `{manifest['formal_claim_allowed']}`",
        "",
        "## Baseline Summary",
        "",
        f"- missing_counts_by_formal_category: `{baseline['missing_counts_by_formal_category']}`",
        f"- next_blocked_lane: `{baseline['next_blocked_lane']}`",
        f"- h01_status: `{baseline['h01_status']}`",
        f"- h02_status: `{baseline['h02_status']}`",
        f"- h02_formal_output_accepted: `{baseline['h02_formal_output_accepted']}`",
        f"- h02_paper_result_input_allowed: `{baseline['h02_paper_result_input_allowed']}`",
        "",
        "## Audit Issues",
        "",
    ]
    if manifest["audit_issues"]:
        lines.extend(f"- `{issue['issue_id']}`: {issue['message']}" for issue in manifest["audit_issues"])
    else:
        lines.append("- none")
    lines.extend(["", "## Chain Rows", ""])
    for row in manifest["chain_rows"]:
        lines.append(
            f"- `{row['row_id']}`: present=`{row['present']}`, "
            f"matches=`{row['signature_matches_baseline']}`, "
            f"h02_paper_result_input_allowed=`{row['h02_paper_result_input_allowed']}`, "
            f"path=`{row['path']}`, key=`{row['summary_key_path']}`"
        )
    lines.extend(["", "## Next-Action Guard Chain Rows", ""])
    for row in manifest["next_action_guard_rows"]:
        lines.append(
            f"- `{row['row_id']}`: present=`{row['present']}`, "
            f"matches=`{row['signature_matches_baseline']}`, "
            f"expected_next_action_id=`{row['expected_next_action_id']}`, "
            f"execution_leak_count=`{row['execution_leak_count']}`, "
            f"path=`{row['path']}`, key=`{row['summary_key_path']}`"
        )
    lines.extend(["", "## Next Required Formal Deliverables Chain Rows", ""])
    for row in manifest["next_required_deliverables_rows"]:
        lines.append(
            f"- `{row['row_id']}`: present=`{row['present']}`, "
            f"matches=`{row['signature_matches_baseline']}`, "
            f"total_missing_deliverables=`{row['total_missing_deliverables']}`, "
            f"row_count=`{row['row_count']}`, "
            f"runs_training=`{row['runs_training']}`, "
            f"path=`{row['path']}`, key=`{row['summary_key_path']}`"
        )
    lines.extend(["", "## Claim Boundaries", ""])
    lines.extend(f"- {item}" for item in manifest["claim_boundaries"])
    return "\n".join(lines) + "\n"


def _read_json(path: Path) -> dict[str, Any]:
    if not Path(path).is_file():
        return {}
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
