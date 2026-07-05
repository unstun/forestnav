from __future__ import annotations

import argparse
import copy
import json
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head
from forest_n3p.scripts import build_module2_f02_6_decision_gate_audit as decision_gate_builder
from forest_n3p.scripts import build_module2_f02_6_decision_record as decision_record_builder
from forest_n3p.scripts import build_module2_formal_gate_status_report as status_report_builder
from forest_n3p.scripts import build_module2_post_f02_6_plan_audit as post_plan_audit_builder
from forest_n3p.scripts import build_module2_post_f02_6_regeneration_plan as post_plan_builder
from forest_n3p.scripts import build_module2_remote_packet_safety_audit as remote_safety_builder


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_f02_6_transition_gate_audit")
DEFAULT_PACKET = Path("0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json")
DEFAULT_REMOTE_WARM_PREFLIGHT = Path(
    "0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_pending_remote_v1/gate3_preflight_manifest.json"
)
DEFAULT_FORMAL_GATE = Path("0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json")
DEFAULT_SOURCE_FRESHNESS = Path("0_trials/module2_source_freshness_audit/source_freshness_audit.json")
DEFAULT_MISSING_ARTIFACTS = Path("0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json")
DEFAULT_CLOSURE_CHECKLIST = Path("0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json")
DEFAULT_REMAINING_DELIVERABLES = Path(
    "0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json"
)
DEFAULT_REMOTE_PACKET = Path("0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json")
DEFAULT_H01_MANIFEST = Path("0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json")
DEFAULT_H02_ACCEPTANCE = Path("0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json")
DEFAULT_CLAIM_SAFETY = Path("0_trials/module2_claim_safety/module2_claim_safety.json")
DEFAULT_PAPER_READINESS = Path("0_trials/module2_paper_readiness/module2_paper_readiness.json")
DEFAULT_HANDOFF_BUNDLE = Path("0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json")
DEFAULT_DECISION_INTAKE = Path("0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json")
APPROVE_OBSTACLE_SUMMARY = "approve_obstacle_summary_warm_start"
REJECT_OBSTACLE_SUMMARY = "reject_obstacle_summary_warm_start"
DECISION_OWNER = "Dr Sun"
SCENARIOS = ("pending", "approved", "rejected")
ACTION_ROWS = ("local_training", "remote_preflight", "remote_training", "remote_audit", "formal_claim")
REMOTE_STEP_IDS = ("sync_to_remote", "run_remote_preflight", "run_remote_training", "run_remote_audit")
POST_PLAN_STAGE_IDS = (
    "f02_6_decision_record",
    "regenerate_preflight_gate_artifacts",
    "approved_remote_preflight",
    "regenerate_remote_execution_packet",
    "gate3_remote_training",
    "gate3_remote_audit_pullback",
    "regenerate_h01_h02_formal_artifacts",
    "regenerate_claim_gate_artifacts",
)
F02_PENDING_BLOCKERS = {
    "f02_6_warm_start_decision_pending",
    "requires_dr_sun_approval",
    "f02_6_decision_not_approved",
}
REQUIRED_F02_6_BLOCKED_ACTION_IDS = (
    "remote_preflight",
    "remote_training",
    "local_training",
    "formal_claim",
    "paper_result_material",
)


@dataclass(frozen=True)
class F026TransitionGateAuditConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    packet_path: Path = DEFAULT_PACKET
    remote_warm_preflight_path: Path = DEFAULT_REMOTE_WARM_PREFLIGHT
    formal_gate_path: Path = DEFAULT_FORMAL_GATE
    source_freshness_path: Path = DEFAULT_SOURCE_FRESHNESS
    missing_artifacts_path: Path = DEFAULT_MISSING_ARTIFACTS
    closure_checklist_path: Path = DEFAULT_CLOSURE_CHECKLIST
    remaining_deliverables_path: Path = DEFAULT_REMAINING_DELIVERABLES
    remote_packet_path: Path = DEFAULT_REMOTE_PACKET
    h01_manifest_path: Path = DEFAULT_H01_MANIFEST
    h02_acceptance_path: Path = DEFAULT_H02_ACCEPTANCE
    claim_safety_path: Path = DEFAULT_CLAIM_SAFETY
    paper_readiness_path: Path = DEFAULT_PAPER_READINESS
    handoff_bundle_path: Path = DEFAULT_HANDOFF_BUNDLE
    decision_intake_path: Path = DEFAULT_DECISION_INTAKE


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = F026TransitionGateAuditConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        packet_path=args.packet,
        remote_warm_preflight_path=args.remote_warm_preflight,
        formal_gate_path=args.formal_gate,
        source_freshness_path=args.source_freshness_audit,
        missing_artifacts_path=args.missing_artifacts,
        closure_checklist_path=args.closure_checklist,
        remaining_deliverables_path=args.remaining_deliverables,
        remote_packet_path=args.remote_packet,
        h01_manifest_path=args.h01_manifest,
        h02_acceptance_path=args.h02_acceptance,
        claim_safety_path=args.claim_safety,
        paper_readiness_path=args.paper_readiness,
        handoff_bundle_path=args.handoff_bundle,
        decision_intake_path=args.decision_intake,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "f02_6_transition_gate_audit.json"
    markdown_out = config.markdown_out or output_dir / "f02_6_transition_gate_audit.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: F026TransitionGateAuditConfig) -> dict[str, Any]:
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    scenario_summaries: list[dict[str, Any]] = []
    audit_issues: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="_synthetic_transition_", dir=output_dir) as tmp_name:
        tmp_root = Path(tmp_name)
        for scenario_id in SCENARIOS:
            summary = _run_scenario(config=config, scenario_id=scenario_id, work_root=tmp_root / scenario_id)
            scenario_summaries.append(summary)
            audit_issues.extend(_scenario_issues(summary))
    audit_issues = _unique_issues(audit_issues)
    return {
        "schema_version": 1,
        "artifact_name": "module2_f02_6_transition_gate_audit",
        "status": "f02_6_transition_gate_audit_passed" if not audit_issues else "f02_6_transition_gate_audit_failed",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "inputs": {
            "f02_6_decision_packet": str(config.packet_path),
            "pending_remote_warm_preflight": str(config.remote_warm_preflight_path),
            "formal_gate_gap_audit": str(config.formal_gate_path),
            "source_freshness_audit": str(config.source_freshness_path),
            "formal_gate_missing_artifacts": str(config.missing_artifacts_path),
            "formal_gate_closure_checklist": str(config.closure_checklist_path),
            "formal_gate_remaining_deliverables": str(config.remaining_deliverables_path),
            "remote_formal_execution_packet": str(config.remote_packet_path),
            "h01_manifest": str(config.h01_manifest_path),
            "h02_formal_acceptance": str(config.h02_acceptance_path),
            "claim_safety": str(config.claim_safety_path),
            "paper_readiness": str(config.paper_readiness_path),
            "formal_gate_handoff_bundle": str(config.handoff_bundle_path),
        },
        "synthetic_inputs_persisted": False,
        "scenario_count": len(scenario_summaries),
        "scenario_summaries": scenario_summaries,
        "audit_issue_count": len(audit_issues),
        "audit_issues": audit_issues,
        "transition_invariants": [
            "pending keeps local training, remote preflight, remote training, remote audit, and formal claim vetoed.",
            "approved closes the human decision gate; once source freshness and the remote packet are ready, remote preflight/training may open while audit, H01/H02, claim, and paper-result material stay blocked.",
            "rejected keeps the obstacle-summary warm-start formal path blocked and routes to a stronger/full patch-CNN protocol.",
            "No synthetic scenario writes a real decision, executes commands, runs preflight, trains, audits, pulls back artifacts, or writes paper results.",
        ],
        "claim_boundaries": [
            "This audit is a transition-safety check, not Dr Sun's F02.6 decision record.",
            "A passing approved synthetic scenario is not a result claim; it only proves the post-decision gates expose the correct remote-training entry without opening audit, H01/H02, or claim lanes.",
            "Formal PPO remains gpu3070ti-relay-only; local training, formal claims, and paper-result material stay blocked until remote audit, pullback, H01/H02, and claim gates close.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit synthetic pending/approved/rejected F02.6 transition gates without recording a decision.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--remote-warm-preflight", type=Path, default=DEFAULT_REMOTE_WARM_PREFLIGHT)
    parser.add_argument("--formal-gate", type=Path, default=DEFAULT_FORMAL_GATE)
    parser.add_argument("--source-freshness-audit", type=Path, default=DEFAULT_SOURCE_FRESHNESS)
    parser.add_argument("--missing-artifacts", type=Path, default=DEFAULT_MISSING_ARTIFACTS)
    parser.add_argument("--closure-checklist", type=Path, default=DEFAULT_CLOSURE_CHECKLIST)
    parser.add_argument("--remaining-deliverables", type=Path, default=DEFAULT_REMAINING_DELIVERABLES)
    parser.add_argument("--remote-packet", type=Path, default=DEFAULT_REMOTE_PACKET)
    parser.add_argument("--h01-manifest", type=Path, default=DEFAULT_H01_MANIFEST)
    parser.add_argument("--h02-acceptance", type=Path, default=DEFAULT_H02_ACCEPTANCE)
    parser.add_argument("--claim-safety", type=Path, default=DEFAULT_CLAIM_SAFETY)
    parser.add_argument("--paper-readiness", type=Path, default=DEFAULT_PAPER_READINESS)
    parser.add_argument("--handoff-bundle", type=Path, default=DEFAULT_HANDOFF_BUNDLE)
    parser.add_argument("--decision-intake", type=Path, default=DEFAULT_DECISION_INTAKE)
    return parser.parse_args(list(argv) if argv is not None else None)


def _run_scenario(*, config: F026TransitionGateAuditConfig, scenario_id: str, work_root: Path) -> dict[str, Any]:
    work_root.mkdir(parents=True, exist_ok=True)
    record = decision_record_builder.build_record(
        decision_record_builder.F026DecisionRecordConfig(
            output_dir=work_root,
            packet_path=config.packet_path,
            remote_warm_preflight_path=config.remote_warm_preflight_path,
            decision=_decision_arg(scenario_id),
            decider=DECISION_OWNER if scenario_id in {"approved", "rejected"} else None,
            decision_note=_synthetic_decision_note(scenario_id),
        )
    )
    record_path = _write_json(work_root / "f02_6_decision_record.json", record)

    formal_gate = _scenario_formal_gate(_read_json(config.formal_gate_path), scenario_id, record)
    missing_artifacts = _scenario_missing_artifacts(_read_json(config.missing_artifacts_path), scenario_id, record)
    closure_checklist = _scenario_closure_checklist(_read_json(config.closure_checklist_path), scenario_id, record)
    decision_intake = _scenario_decision_intake(_read_json(config.decision_intake_path), scenario_id, record)
    source_freshness = _scenario_source_freshness(_read_json(config.source_freshness_path), scenario_id)
    remote_packet = _scenario_remote_packet(_read_json(config.remote_packet_path), scenario_id)
    handoff_bundle = _scenario_handoff_bundle(_read_json(config.handoff_bundle_path), scenario_id, remote_packet)
    remaining_deliverables = _scenario_remaining_deliverables(
        _read_json(config.remaining_deliverables_path),
        scenario_id,
    )
    formal_gate_path = _write_json(work_root / "formal_gate_gap_audit.json", formal_gate)
    missing_artifacts_path = _write_json(work_root / "formal_gate_missing_artifacts.json", missing_artifacts)
    closure_checklist_path = _write_json(work_root / "formal_gate_closure_checklist.json", closure_checklist)
    decision_intake_path = _write_json(work_root / "f02_6_decision_intake.json", decision_intake)
    source_freshness_path = _write_json(work_root / "source_freshness_audit.json", source_freshness)
    remote_packet_path = _write_json(work_root / "remote_formal_execution_packet.json", remote_packet)
    handoff_bundle_path = _write_json(work_root / "formal_gate_handoff_bundle.json", handoff_bundle)
    remaining_deliverables_path = _write_json(
        work_root / "formal_gate_remaining_deliverables.json",
        remaining_deliverables,
    )

    status_report = status_report_builder.build_manifest(
        status_report_builder.FormalGateStatusReportConfig(
            output_dir=work_root,
            formal_gate_path=formal_gate_path,
            missing_artifacts_path=missing_artifacts_path,
            closure_checklist_path=closure_checklist_path,
            decision_record_path=record_path,
            decision_intake_path=decision_intake_path,
            remote_packet_path=remote_packet_path,
            h01_manifest_path=config.h01_manifest_path,
            h02_acceptance_path=config.h02_acceptance_path,
            claim_safety_path=config.claim_safety_path,
            paper_readiness_path=config.paper_readiness_path,
            handoff_bundle_path=handoff_bundle_path,
            remaining_deliverables_path=remaining_deliverables_path,
            source_freshness_path=source_freshness_path,
        )
    )
    status_report_path = _write_json(work_root / "formal_gate_status_report.json", status_report)

    plan = post_plan_builder.build_manifest(
        post_plan_builder.PostF026RegenerationPlanConfig(
            output_dir=work_root,
            decision_record_path=record_path,
            formal_gate_path=formal_gate_path,
            status_report_path=status_report_path,
            source_freshness_path=source_freshness_path,
            remote_packet_path=remote_packet_path,
            remaining_deliverables_path=remaining_deliverables_path,
        )
    )
    plan_path = _write_json(work_root / "post_f02_6_regeneration_plan.json", plan)

    decision_gate = decision_gate_builder.build_manifest(
        decision_gate_builder.F026DecisionGateAuditConfig(
            output_dir=work_root,
            packet_path=config.packet_path,
            decision_record_path=record_path,
            post_plan_path=plan_path,
        )
    )
    decision_gate_path = _write_json(work_root / "f02_6_decision_gate_audit.json", decision_gate)

    post_plan_audit = post_plan_audit_builder.build_manifest(
        post_plan_audit_builder.PostF026PlanAuditConfig(
            output_dir=work_root,
            plan_path=plan_path,
            formal_gate_path=formal_gate_path,
            source_freshness_path=source_freshness_path,
            missing_artifacts_path=missing_artifacts_path,
            closure_checklist_path=closure_checklist_path,
            status_report_path=status_report_path,
            remaining_deliverables_path=remaining_deliverables_path,
        )
    )
    post_plan_audit_path = _write_json(work_root / "post_f02_6_plan_audit.json", post_plan_audit)

    remote_safety = remote_safety_builder.build_manifest(
        remote_safety_builder.RemotePacketSafetyAuditConfig(
            output_dir=work_root,
            remote_packet_path=remote_packet_path,
            decision_gate_audit_path=decision_gate_path,
            post_plan_audit_path=post_plan_audit_path,
        )
    )
    return _scenario_summary(
        scenario_id=scenario_id,
        record=record,
        plan=plan,
        status_report=status_report,
        decision_gate=decision_gate,
        post_plan_audit=post_plan_audit,
        remote_safety=remote_safety,
        missing_artifacts=missing_artifacts,
        closure_checklist=closure_checklist,
    )


def _synthetic_decision_note(scenario_id: str) -> str | None:
    if scenario_id == "approved":
        return (
            "Approve obstacle-summary warm-start because the evidence packet supports formal-v2 BC risk; "
            "next run source-fresh regeneration before any remote preflight."
        )
    if scenario_id == "rejected":
        return (
            "Reject obstacle-summary warm-start because the risk is unacceptable; "
            "next require a stronger/full patch-CNN protocol before any warm-start PPO formal trial."
        )
    return None


def _scenario_summary(
    *,
    scenario_id: str,
    record: dict[str, Any],
    plan: dict[str, Any],
    status_report: dict[str, Any],
    decision_gate: dict[str, Any],
    post_plan_audit: dict[str, Any],
    remote_safety: dict[str, Any],
    missing_artifacts: dict[str, Any],
    closure_checklist: dict[str, Any],
) -> dict[str, Any]:
    permissions = status_report.get("permissions_now") if isinstance(status_report.get("permissions_now"), dict) else {}
    plan_blocking = plan.get("blocking_summary") if isinstance(plan.get("blocking_summary"), dict) else {}
    next_lane = status_report.get("next_blocked_lane") if isinstance(status_report.get("next_blocked_lane"), dict) else {}
    return {
        "scenario_id": scenario_id,
        "requested_decision": record.get("requested_decision"),
        "record_status": record.get("status"),
        "effective_warm_start_decision": record.get("effective_warm_start_decision"),
        "record_remote_training_allowed": record.get("remote_training_allowed"),
        "record_remote_preflight_allowed_now": record.get("remote_preflight_allowed_now"),
        "record_remote_training_allowed_now": record.get("remote_training_allowed_now"),
        "record_local_training_allowed": record.get("local_training_allowed"),
        "record_formal_claim_allowed": record.get("formal_claim_allowed"),
        "decision_gate_status": decision_gate.get("status"),
        "decision_gate_audit_issue_count": decision_gate.get("audit_issue_count"),
        "post_plan_status": plan.get("status"),
        "post_plan_ready_stage_ids": _strings(plan_blocking.get("ready_stage_ids")),
        "post_plan_blocked_stage_ids": _strings(plan_blocking.get("blocked_stage_ids")),
        "post_plan_training_allowed_now": plan_blocking.get("training_allowed_now"),
        "post_plan_remote_preflight_allowed_now": plan_blocking.get("remote_preflight_allowed_now"),
        "post_plan_stage_summary": _post_plan_stage_summary(plan),
        "formal_gate_status_report_status": status_report.get("status"),
        "formal_gate_status_report_input_safety_issue_count": status_report.get("input_safety_issue_count"),
        "formal_gate_status_report_permissions_now": {
            "local_training_allowed_now": permissions.get("local_training_allowed_now"),
            "remote_preflight_allowed_now": permissions.get("remote_preflight_allowed_now"),
            "remote_training_allowed_now": permissions.get("remote_training_allowed_now"),
            "formal_claim_allowed_now": permissions.get("formal_claim_allowed_now"),
        },
        "formal_gate_status_report_next_blocked_lane_id": next_lane.get("lane_id"),
        "post_plan_audit_status": post_plan_audit.get("status"),
        "post_plan_audit_issue_count": post_plan_audit.get("audit_issue_count"),
        "remote_packet_safety_status": remote_safety.get("status"),
        "remote_packet_safety_issue_count": remote_safety.get("audit_issue_count"),
        "missing_counts_by_category": missing_artifacts.get("missing_counts_by_category")
        if isinstance(missing_artifacts.get("missing_counts_by_category"), dict)
        else {},
        "closure_open_item_count": closure_checklist.get("open_item_count"),
    }


def _scenario_issues(summary: dict[str, Any]) -> list[dict[str, Any]]:
    scenario_id = str(summary.get("scenario_id"))
    issues: list[dict[str, Any]] = []
    issues.extend(_common_scenario_issues(summary))
    if scenario_id == "pending":
        issues.extend(_pending_scenario_issues(summary))
    elif scenario_id == "approved":
        issues.extend(_approved_scenario_issues(summary))
    elif scenario_id == "rejected":
        issues.extend(_rejected_scenario_issues(summary))
    else:
        issues.append(_issue(scenario_id, "unknown_scenario", f"Unexpected synthetic scenario {scenario_id!r}."))
    return issues


def _common_scenario_issues(summary: dict[str, Any]) -> list[dict[str, Any]]:
    scenario_id = str(summary.get("scenario_id"))
    permissions = summary.get("formal_gate_status_report_permissions_now") if isinstance(summary.get("formal_gate_status_report_permissions_now"), dict) else {}
    issues: list[dict[str, Any]] = []
    if summary.get("record_local_training_allowed") is not False:
        issues.append(_issue(scenario_id, "record_allows_local_training", "Synthetic decision record must never allow local training."))
    if summary.get("record_formal_claim_allowed") is not False:
        issues.append(_issue(scenario_id, "record_allows_formal_claim", "Synthetic decision record must never allow formal claims."))
    if summary.get("record_remote_preflight_allowed_now") is not False:
        issues.append(_issue(scenario_id, "record_allows_remote_preflight_now", "Synthetic decision record alone must never allow remote preflight now."))
    if summary.get("record_remote_training_allowed_now") is not False:
        issues.append(_issue(scenario_id, "record_allows_remote_training_now", "Synthetic decision record alone must never allow remote training now."))
    if permissions.get("local_training_allowed_now") is not False:
        issues.append(_issue(scenario_id, "status_report_allows_local_training", "Status report must keep local training blocked."))
    if permissions.get("remote_training_allowed_now") is not False:
        issues.append(_issue(scenario_id, "status_report_allows_remote_training", "Synthetic transition must not directly allow formal PPO training."))
    if permissions.get("formal_claim_allowed_now") is not False:
        issues.append(_issue(scenario_id, "status_report_allows_formal_claim", "Synthetic transition must not directly allow formal claims."))
    if int(summary.get("decision_gate_audit_issue_count") or 0) != 0:
        issues.append(
            _issue(
                scenario_id,
                "decision_gate_audit_issue_count",
                "decision_gate_audit_issue_count must be zero.",
                observed=summary.get("decision_gate_audit_issue_count"),
            )
        )
    expected_gate_status = "f02_6_decision_gate_pending_clean" if scenario_id == "pending" else "f02_6_decision_gate_audit_passed"
    if summary.get("decision_gate_status") != expected_gate_status:
        issues.append(_issue(scenario_id, "unexpected_decision_gate_status", "Decision gate status drifted.", observed=summary.get("decision_gate_status")))
    return issues


def _pending_scenario_issues(summary: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    permissions = summary["formal_gate_status_report_permissions_now"]
    if summary.get("record_status") != "pending_human_decision":
        issues.append(_issue("pending", "pending_record_status_drift", "Pending scenario must keep a pending decision record.", observed=summary.get("record_status")))
    if summary.get("post_plan_status") != "blocked_until_f02_6_decision":
        issues.append(_issue("pending", "pending_post_plan_not_blocked", "Pending scenario must keep post-plan blocked.", observed=summary.get("post_plan_status")))
    if permissions.get("remote_preflight_allowed_now") is not False:
        issues.append(_issue("pending", "pending_allows_remote_preflight", "Pending scenario must not allow remote preflight."))
    if summary.get("post_plan_remote_preflight_allowed_now") is not False:
        issues.append(_issue("pending", "pending_plan_allows_remote_preflight", "Pending post-plan must not allow remote preflight."))
    if summary.get("post_plan_training_allowed_now") is not False:
        issues.append(_issue("pending", "pending_plan_allows_training", "Pending post-plan must not allow training."))
    ready = set(_strings(summary.get("post_plan_ready_stage_ids")))
    if ready != {"f02_6_decision_record"}:
        issues.append(_issue("pending", "pending_ready_stages_drift", "Only the human decision stage should be ready while pending.", observed=sorted(ready)))
    return issues


def _approved_scenario_issues(summary: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    permissions = summary["formal_gate_status_report_permissions_now"]
    stages = summary["post_plan_stage_summary"]
    if summary.get("record_status") != "approved":
        issues.append(_issue("approved", "approved_record_status_drift", "Approved scenario must synthesize an approved record.", observed=summary.get("record_status")))
    allowed_post_plan_statuses = {
        "ready_to_execute_post_f02_6_regeneration_plan",
        "ready_for_remote_training_packet_execution",
        "blocked_formal_gate_preconditions",
    }
    if summary.get("post_plan_status") not in allowed_post_plan_statuses:
        issues.append(
            _issue(
                "approved",
                "approved_post_plan_wrong_status",
                "Approved scenario should advance only to local gate regeneration or remain blocked by formal gate preconditions.",
                observed=summary.get("post_plan_status"),
            )
        )
    remote_training_entry_ready = summary.get("post_plan_status") == "ready_for_remote_training_packet_execution"
    if not remote_training_entry_ready and permissions.get("remote_preflight_allowed_now") is not False:
        issues.append(_issue("approved", "approved_status_report_allows_remote_preflight_too_early", "Approved decision alone must not bypass remote packet/source freshness."))
    if not remote_training_entry_ready and stages.get("regenerate_preflight_gate_artifacts", {}).get("allowed_now") is not True:
        issues.append(_issue("approved", "approved_regeneration_not_ready", "Approved scenario should expose source-fresh preflight regeneration as the next local gate."))
    if not remote_training_entry_ready and stages.get("approved_remote_preflight", {}).get("allowed_now") is not False:
        issues.append(_issue("approved", "approved_remote_preflight_ready_too_early", "Approved scenario must still block remote preflight until source-fresh targets close."))
    if not remote_training_entry_ready and stages.get("gate3_remote_training", {}).get("allowed_now") is not False:
        issues.append(_issue("approved", "approved_training_ready_too_early", "Approved scenario must still block formal PPO training."))
    if stages.get("gate3_remote_audit_pullback", {}).get("allowed_now") is not False:
        issues.append(_issue("approved", "approved_remote_audit_ready_too_early", "Approved scenario must still block audit and pullback until remote training completes."))
    if stages.get("regenerate_claim_gate_artifacts", {}).get("allowed_now") is not False:
        issues.append(_issue("approved", "approved_claim_gate_ready_too_early", "Approved scenario must not expose claim gate regeneration."))
    if summary.get("formal_gate_status_report_next_blocked_lane_id") == "decision":
        issues.append(_issue("approved", "approved_still_reports_decision_lane", "Approved scenario should move the next blocked lane beyond the human decision."))
    return issues


def _rejected_scenario_issues(summary: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    permissions = summary["formal_gate_status_report_permissions_now"]
    stages = summary["post_plan_stage_summary"]
    if summary.get("record_status") != "rejected":
        issues.append(_issue("rejected", "rejected_record_status_drift", "Rejected scenario must synthesize a rejected record.", observed=summary.get("record_status")))
    if summary.get("post_plan_status") != "blocked_by_f02_6_rejected":
        issues.append(_issue("rejected", "rejected_post_plan_wrong_status", "Rejected scenario must route away from obstacle-summary warm-start.", observed=summary.get("post_plan_status")))
    if permissions.get("remote_preflight_allowed_now") is not False:
        issues.append(_issue("rejected", "rejected_allows_remote_preflight", "Rejected scenario must not allow obstacle-summary remote preflight."))
    if stages.get("regenerate_preflight_gate_artifacts", {}).get("allowed_now") is not False:
        issues.append(_issue("rejected", "rejected_regeneration_ready", "Rejected scenario must not regenerate the obstacle-summary warm-start formal path."))
    if stages.get("gate3_remote_training", {}).get("allowed_now") is not False:
        issues.append(_issue("rejected", "rejected_training_ready", "Rejected scenario must not allow warm-start formal PPO training."))
    return issues


def _scenario_formal_gate(base: dict[str, Any], scenario_id: str, record: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(base)
    decision_status = str(record.get("status"))
    current = out.setdefault("current_gate_state", {})
    current["f02_6_decision_status"] = decision_status
    current["effective_warm_start_decision"] = record.get("effective_warm_start_decision")
    current["remote_training_allowed"] = False
    veto = out.get("execution_veto_matrix") if isinstance(out.get("execution_veto_matrix"), dict) else {}
    veto["f02_6_decision_status"] = decision_status
    for row in veto.get("rows", []):
        if not isinstance(row, dict):
            continue
        sources = row.get("allowed_now_by_source") if isinstance(row.get("allowed_now_by_source"), dict) else {}
        for key in list(sources):
            sources[key] = False
        row["consistent"] = True
        row["consensus_allowed_now"] = False
    veto["all_rows_consistent"] = True
    veto["mismatch_rows"] = []
    out["execution_veto_matrix"] = veto
    if scenario_id == "pending":
        return out
    rejected = scenario_id == "rejected"
    for step in out.get("ordered_next_steps", []):
        if not isinstance(step, dict):
            continue
        if step.get("step_id") == "F02.6":
            step["status"] = "complete"
            step["blocked_by"] = []
            continue
        step["blocked_by"] = _scenario_blockers(_strings(step.get("blocked_by")), rejected=rejected)
    return out


def _scenario_missing_artifacts(base: dict[str, Any], scenario_id: str, record: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(base)
    _block_missing_artifacts_handoff(out, scenario_id)
    if scenario_id == "pending":
        for group in out.get("missing_evidence_groups", []):
            if not isinstance(group, dict) or group.get("group_id") != "f02_6_decision_record":
                continue
            group["complete"] = False
            group["blocked_by"] = ["requires_dr_sun_approval"]
            for item in group.get("items", []):
                if isinstance(item, dict):
                    item["state"] = record.get("status")
                    item["missing"] = True
                    item["reason"] = "requires_dr_sun_approval"
        out["missing_counts_by_category"] = _missing_counts(out.get("missing_evidence_groups", []))
        return out
    rejected = scenario_id == "rejected"
    for group in out.get("missing_evidence_groups", []):
        if not isinstance(group, dict):
            continue
        group_id = str(group.get("group_id"))
        if group_id == "f02_6_decision_record":
            group["complete"] = True
            group["blocked_by"] = []
            for item in group.get("items", []):
                if isinstance(item, dict):
                    item["state"] = record.get("status")
                    item["missing"] = False
                    item["reason"] = ""
        else:
            group["blocked_by"] = _scenario_blockers(_strings(group.get("blocked_by")), rejected=rejected)
            for item in group.get("items", []):
                if not isinstance(item, dict):
                    continue
                item["reason"] = _scenario_reason(str(item.get("reason") or ""), rejected=rejected)
    out["missing_counts_by_category"] = _missing_counts(out.get("missing_evidence_groups", []))
    return out


def _scenario_closure_checklist(base: dict[str, Any], scenario_id: str, record: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(base)
    _block_remote_stage_summary(out, _scenario_execution_blockers(scenario_id, for_training=False))
    rejected = scenario_id == "rejected"
    for item in out.get("closure_checklist", []):
        if not isinstance(item, dict):
            continue
        if item.get("checklist_id") == "F02.6_decision":
            if scenario_id == "pending":
                item["status"] = "blocked"
                item["complete"] = False
                item["formal_step_status"] = "blocked"
                item["blocked_by"] = ["requires_dr_sun_approval"]
                item["missing_item_count"] = 1
                for required in item.get("required_items", []):
                    if isinstance(required, dict):
                        required["state"] = record.get("status")
                        required["missing"] = True
                        required["reason"] = "requires_dr_sun_approval"
                continue
            item["status"] = "complete"
            item["complete"] = True
            item["formal_step_status"] = "complete"
            item["blocked_by"] = []
            item["missing_item_count"] = 0
            for required in item.get("required_items", []):
                if isinstance(required, dict):
                    required["state"] = record.get("status")
                    required["missing"] = False
                    required["reason"] = ""
            continue
        item["blocked_by"] = _scenario_blockers(_strings(item.get("blocked_by")), rejected=rejected)
        for required in item.get("required_items", []):
            if isinstance(required, dict):
                required["reason"] = _scenario_reason(str(required.get("reason") or ""), rejected=rejected)
    out["open_item_count"] = sum(1 for item in out.get("closure_checklist", []) if isinstance(item, dict) and item.get("complete") is not True)
    return out


def _scenario_source_freshness(base: dict[str, Any], scenario_id: str) -> dict[str, Any]:
    out = copy.deepcopy(base)
    out["status"] = "source_freshness_requires_regeneration_before_remote_formal_execution"
    out["regeneration_required_before_remote_formal_execution"] = True
    out["blocking_regeneration_required_before_remote_formal_execution"] = True
    targets = out.get("ordered_regeneration_targets") if isinstance(out.get("ordered_regeneration_targets"), list) else []
    if not any(isinstance(item, dict) and item.get("artifact_id") == "formal_gate_handoff_bundle" for item in targets):
        targets.append(
            {
                "artifact_id": "formal_gate_handoff_bundle",
                "path": "0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json",
                "freshness_state": "synthetic_requires_regeneration",
                "required_before": "approved_remote_preflight",
            }
        )
    for target in targets:
        if not isinstance(target, dict):
            continue
        if target.get("required_before") == "approved_remote_preflight":
            target["freshness_state"] = "synthetic_requires_regeneration"
            target["blocking_regeneration_required_before_remote_formal_execution"] = True
    out["ordered_regeneration_targets"] = targets
    out["artifact_records"] = copy.deepcopy(targets)
    return out


def _scenario_remote_packet(base: dict[str, Any], scenario_id: str) -> dict[str, Any]:
    out = copy.deepcopy(base)
    out["status"] = (
        "blocked_until_f02_6_decision"
        if scenario_id == "pending"
        else "blocked_by_f02_6_rejected"
        if scenario_id == "rejected"
        else "blocked_until_source_fresh_regeneration"
    )
    out["ready_to_run_remote_training"] = False
    preflight = out.setdefault("remote_preflight", {})
    preflight["formal_trial_ready"] = False
    preflight["preflight_status"] = "blocked"
    preflight["warm_start_decision"] = "pending" if scenario_id == "pending" else scenario_id
    preflight["blocker_codes"] = _unique_strings(
        _strings(preflight.get("blocker_codes"))
        + (["warm_start_decision_pending"] if scenario_id == "pending" else [])
        + _scenario_execution_blockers(scenario_id, for_training=False)
    )

    steps = out.setdefault("execution_steps", {})
    _block_remote_step(steps, "sync_to_remote", _scenario_execution_blockers(scenario_id, for_training=False))
    _block_remote_step(steps, "run_remote_preflight", _scenario_execution_blockers(scenario_id, for_training=False))
    _block_remote_step(steps, "run_remote_training", _scenario_execution_blockers(scenario_id, for_training=True))
    _block_remote_step(steps, "run_remote_audit", ["remote_training_not_completed", "remote_packet_not_ready"])

    for requirement in out.get("remote_preflight_requirements", []):
        if not isinstance(requirement, dict):
            continue
        requirement["execution_allowed_now"] = False
        if scenario_id == "pending" or requirement.get("requirement_id") != "f02_6_decision_closed_for_preflight":
            requirement["complete"] = False
            requirement["status"] = "blocked"
            requirement["missing_artifact_ids"] = _unique_strings(
                _strings(requirement.get("missing_artifact_ids")) + [str(requirement.get("requirement_id"))]
            )
    for requirement in out.get("post_run_acceptance_requirements", []):
        if not isinstance(requirement, dict):
            continue
        requirement["execution_allowed_now"] = False
        requirement["complete"] = False
        requirement["status"] = "blocked"
    _refresh_requirement_counts(out, "remote_preflight_requirements", "remote_preflight_requirement_counts")
    _refresh_requirement_counts(out, "post_run_acceptance_requirements", "post_run_acceptance_requirement_counts")
    return out


def _scenario_handoff_bundle(base: dict[str, Any], scenario_id: str, remote_packet: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(base)
    current = out.setdefault("current_state", {})
    current["decision_status"] = "pending_human_decision" if scenario_id == "pending" else scenario_id
    current["ready_to_run_remote_training"] = False
    current["remote_packet_status"] = remote_packet.get("status")
    current["next_blocked_lane"] = (
        "decision" if scenario_id == "pending" else "protocol_redesign" if scenario_id == "rejected" else "source_fresh_preflight"
    )
    permissions = out.setdefault("permissions_now", {})
    for key in (
        "remote_preflight_allowed_now",
        "remote_training_allowed_now",
        "formal_h01_evaluation_allowed_now",
        "formal_h02_acceptance_allowed_now",
        "formal_claim_allowed_now",
        "local_training_allowed_now",
        "source_freshness_ready_for_remote_preflight",
    ):
        permissions[key] = False
    next_action = out.setdefault("next_handoff_action", {})
    next_action["action_id"] = (
        "record_f02_6_decision"
        if scenario_id == "pending"
        else "revise_protocol_contract"
        if scenario_id == "rejected"
        else "resolve_source_fresh_preflight"
    )
    next_action["requires_dr_sun"] = scenario_id == "pending"
    next_action["allowed_for_agent_now"] = False

    index = out.setdefault("single_next_action_index", {})
    index["next_action_id"] = next_action["action_id"]
    index["current_allowed_action_ids"] = ["record_f02_6_decision"] if scenario_id == "pending" else []
    index["current_blocked_action_ids"] = list(REQUIRED_F02_6_BLOCKED_ACTION_IDS)
    index["remote_preflight_allowed_now"] = False
    index["remote_training_allowed_now"] = False
    index["local_training_allowed_now"] = False
    index["formal_claim_allowed_now"] = False
    index["paper_result_material_allowed_now"] = False

    out["remote_execution_steps"] = _remote_step_projection(remote_packet)
    for requirement in out.get("formal_gate_requirements", []):
        if not isinstance(requirement, dict):
            continue
        requirement["execution_allowed_now"] = False
        requirement["responsible_stage_allowed_now"] = False
        blockers = _strings(requirement.get("responsible_stage_blocked_by"))
        if not blockers:
            requirement["responsible_stage_blocked_by"] = _scenario_execution_blockers(scenario_id, for_training=True)
    for stage in out.get("handoff_stages", []):
        if not isinstance(stage, dict):
            continue
        stage["source_allowed_now"] = False
        stage["allowed_now"] = False
        stage["blocked_by"] = _unique_strings(
            _strings(stage.get("blocked_by")) + _scenario_execution_blockers(scenario_id, for_training=stage.get("runs_training") is True)
        )
    out["safety_issue_count"] = 0
    out["safety_issues"] = []
    return out


def _scenario_decision_intake(base: dict[str, Any], scenario_id: str, record: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(base)
    current = out.setdefault("current_state", {})
    current["record_status"] = record.get("status")
    current["record_requested_decision"] = record.get("requested_decision")
    current["record_decider"] = record.get("decider")
    current["effective_warm_start_decision"] = record.get("effective_warm_start_decision")
    current["record_remote_training_allowed"] = record.get("remote_training_allowed")
    current["record_remote_preflight_allowed_now"] = record.get("remote_preflight_allowed_now")
    current["record_remote_training_allowed_now"] = record.get("remote_training_allowed_now")
    current["record_local_training_allowed"] = record.get("local_training_allowed")
    current["record_formal_claim_allowed"] = record.get("formal_claim_allowed")
    current["record_authorization_status"] = record.get("current_authorization", {}).get("authorization_status")
    current["record_authorization_current_allowed_action_ids"] = list(
        record.get("current_authorization", {}).get("current_allowed_action_ids") or []
    )
    current["record_authorization_current_blocked_action_ids"] = list(
        record.get("current_authorization", {}).get("current_blocked_action_ids") or []
    )
    current["record_authorization_post_decision_routes_are_current_authorization"] = record.get(
        "current_authorization", {}
    ).get("post_decision_routes_are_current_authorization")
    current["record_authorization_remote_preflight_allowed_now"] = record.get("current_authorization", {}).get(
        "remote_preflight_allowed_now"
    )
    current["record_authorization_remote_training_allowed_now"] = record.get("current_authorization", {}).get(
        "remote_training_allowed_now"
    )
    current["record_authorization_formal_claim_allowed_now"] = record.get("current_authorization", {}).get(
        "formal_claim_allowed_now"
    )
    current["record_authorization_paper_result_material_allowed_now"] = record.get("current_authorization", {}).get(
        "paper_result_material_allowed_now"
    )
    current["status_report_local_training_allowed_now"] = False
    current["status_report_formal_claim_allowed_now"] = False
    if scenario_id == "pending":
        out["status"] = "f02_6_decision_intake_pending_clean"
        current["next_blocked_lane"] = "decision"
        current["status_report_remote_preflight_allowed_now"] = False
        current["status_report_remote_training_allowed_now"] = False
        current["missing_deliverable_count"] = 10
        request = out.setdefault("next_human_decision_request", {})
        request["status"] = "awaiting_dr_sun_decision"
        request["all_execution_disabled_now"] = True
        request["current_allowed_action_ids"] = ["record_f02_6_decision"]
        request["current_blocked_action_ids"] = list(REQUIRED_F02_6_BLOCKED_ACTION_IDS)
        request["post_decision_routes_are_current_authorization"] = False
    elif scenario_id == "approved":
        out["status"] = "f02_6_decision_intake_closed_clean"
        current["next_blocked_lane"] = "source_fresh_preflight"
        current["status_report_remote_preflight_allowed_now"] = False
        current["status_report_remote_training_allowed_now"] = False
        current["missing_deliverable_count"] = 10
        request = out.setdefault("next_human_decision_request", {})
        request["status"] = "decision_recorded"
        request["all_execution_disabled_now"] = False
    else:
        out["status"] = "f02_6_decision_intake_closed_clean"
        current["next_blocked_lane"] = "protocol_redesign"
        current["status_report_remote_preflight_allowed_now"] = False
        current["status_report_remote_training_allowed_now"] = False
        current["missing_deliverable_count"] = 10
        request = out.setdefault("next_human_decision_request", {})
        request["status"] = "decision_recorded"
        request["all_execution_disabled_now"] = False
    out["audit_issue_count"] = 0
    out["audit_issues"] = []
    return out


def _scenario_blockers(blockers: Sequence[str], *, rejected: bool) -> list[str]:
    filtered = [blocker for blocker in blockers if blocker not in F02_PENDING_BLOCKERS]
    if rejected and "f02_6_decision_rejected" not in filtered:
        filtered.insert(0, "f02_6_decision_rejected")
    return _unique_strings(filtered)


def _scenario_execution_blockers(scenario_id: str, *, for_training: bool) -> list[str]:
    if scenario_id == "pending":
        blockers = ["requires_dr_sun_approval"]
    elif scenario_id == "rejected":
        blockers = ["f02_6_decision_rejected"]
    else:
        blockers = ["source_fresh_preflight_targets_open"]
    if for_training and "remote_packet_not_ready" not in blockers:
        blockers.append("remote_packet_not_ready")
    return blockers


def _block_remote_step(steps: dict[str, Any], step_id: str, blockers: Sequence[str]) -> None:
    step = steps.setdefault(step_id, {})
    step["allowed_now"] = False
    step["blocked_by"] = _unique_strings([str(item) for item in blockers if item])


def _remote_step_projection(remote_packet: dict[str, Any]) -> dict[str, dict[str, Any]]:
    steps = remote_packet.get("execution_steps") if isinstance(remote_packet.get("execution_steps"), dict) else {}
    out: dict[str, dict[str, Any]] = {}
    for step_id in REMOTE_STEP_IDS:
        step = steps.get(step_id) if isinstance(steps.get(step_id), dict) else {}
        out[step_id] = {
            "allowed_now": step.get("allowed_now"),
            "runs_training": step.get("runs_training"),
            "blocked_by": _strings(step.get("blocked_by")),
        }
    return out


def _block_remote_stage_summary(payload: dict[str, Any], blockers: Sequence[str]) -> None:
    stages = payload.setdefault("post_plan_remote_stage_summary", {})
    defaults = {
        "approved_remote_preflight": {"runs_training": False, "runs_remote_preflight": True},
        "gate3_remote_training": {"runs_training": True, "runs_remote_preflight": False},
        "gate3_remote_audit_pullback": {"runs_training": False, "runs_remote_preflight": False},
    }
    for stage_id, fields in defaults.items():
        stage = stages.setdefault(stage_id, {})
        stage["status"] = "blocked"
        stage["allowed_now"] = False
        stage["host"] = "gpu3070ti-relay"
        stage["blocked_by"] = _unique_strings(_strings(stage.get("blocked_by")) + list(blockers))
        stage["runs_training"] = fields["runs_training"]
        stage["runs_remote_preflight"] = fields["runs_remote_preflight"]


def _block_missing_artifacts_handoff(payload: dict[str, Any], scenario_id: str) -> None:
    handoff = payload.setdefault("formal_gate_handoff_index", {})
    next_action = handoff.setdefault("next_action", {})
    next_action["action_id"] = (
        "record_f02_6_decision"
        if scenario_id == "pending"
        else "revise_protocol_contract"
        if scenario_id == "rejected"
        else "resolve_source_fresh_preflight"
    )
    next_action["requires_dr_sun"] = scenario_id == "pending"
    next_action["allowed_for_agent_now"] = False
    handoff["local_training_allowed_now"] = False
    handoff["remote_training_allowed_now"] = False
    handoff["formal_result_material_allowed_now"] = False
    for requirement in handoff.get("requirements", []):
        if not isinstance(requirement, dict):
            continue
        requirement["execution_allowed_now"] = False
        requirement["responsible_stage_allowed_now"] = False
        blockers = _strings(requirement.get("responsible_stage_blocked_by"))
        if not blockers:
            requirement["responsible_stage_blocked_by"] = _scenario_execution_blockers(scenario_id, for_training=True)


def _refresh_requirement_counts(payload: dict[str, Any], list_key: str, count_key: str) -> None:
    requirements = payload.get(list_key) if isinstance(payload.get(list_key), list) else []
    counts: dict[str, int] = {}
    for requirement in requirements:
        if not isinstance(requirement, dict):
            continue
        status = str(requirement.get("status") or "unknown")
        counts[status] = counts.get(status, 0) + 1
    payload[count_key] = counts


def _scenario_reason(reason: str, *, rejected: bool) -> str:
    for blocker in F02_PENDING_BLOCKERS:
        reason = reason.replace(blocker, "").strip(" ,")
    if rejected:
        return "f02_6_decision_rejected" if not reason else f"f02_6_decision_rejected, {reason}"
    return reason


def _decision_arg(scenario_id: str) -> str:
    if scenario_id == "pending":
        return "pending"
    if scenario_id == "approved":
        return APPROVE_OBSTACLE_SUMMARY
    if scenario_id == "rejected":
        return REJECT_OBSTACLE_SUMMARY
    raise ValueError(f"unknown scenario {scenario_id!r}")


def _post_plan_stage_summary(plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    stages = plan.get("ordered_stages") if isinstance(plan.get("ordered_stages"), list) else []
    out: dict[str, dict[str, Any]] = {}
    for stage in stages:
        if not isinstance(stage, dict) or not stage.get("stage_id"):
            continue
        if str(stage["stage_id"]) not in POST_PLAN_STAGE_IDS:
            continue
        out[str(stage["stage_id"])] = {
            "status": stage.get("status"),
            "allowed_now": stage.get("allowed_now"),
            "runs_training": stage.get("runs_training"),
            "runs_remote_preflight": stage.get("runs_remote_preflight"),
            "host": stage.get("host"),
            "blocked_by": _strings(stage.get("blocked_by")),
        }
    return out


def _missing_counts(groups: Any) -> dict[str, int]:
    counts: dict[str, int] = {}
    if not isinstance(groups, list):
        return counts
    for group in groups:
        if not isinstance(group, dict):
            continue
        category = str(group.get("category") or "unknown")
        items = group.get("items") if isinstance(group.get("items"), list) else []
        counts[category] = sum(1 for item in items if isinstance(item, dict) and item.get("missing") is True)
    return counts


def _write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def _read_json(path: Path) -> dict[str, Any]:
    if not Path(path).is_file():
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _unique_strings(items: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def _issue(scenario_id: str, issue_id: str, message: str, *, observed: Any | None = None) -> dict[str, Any]:
    issue = {"scenario_id": scenario_id, "issue_id": issue_id, "message": message}
    if observed is not None:
        issue["observed"] = observed
    return issue


def _unique_issues(issues: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str]] = set()
    out: list[dict[str, Any]] = []
    for issue in issues:
        key = (str(issue.get("scenario_id")), str(issue.get("issue_id")))
        if not key[0] or not key[1] or key in seen:
            continue
        seen.add(key)
        out.append(issue)
    return out


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 F02.6 Transition Gate Audit",
        "",
        "This file audits synthetic pending/approved/rejected F02.6 gate transitions. It does not record a decision, run preflight, train, audit, pull back artifacts, or write paper results.",
        "A passing transition audit is not permission to train.",
        "",
        f"- status: `{manifest['status']}`",
        f"- audit_issue_count: `{manifest['audit_issue_count']}`",
        f"- scenario_count: `{manifest['scenario_count']}`",
        f"- synthetic_inputs_persisted: `{manifest['synthetic_inputs_persisted']}`",
        "",
        "## Scenario Summary",
        "",
    ]
    for scenario in manifest["scenario_summaries"]:
        permissions = scenario["formal_gate_status_report_permissions_now"]
        stages = scenario["post_plan_stage_summary"]
        lines.extend(
            [
                f"### {scenario['scenario_id']}",
                "",
                f"- record_status: `{scenario['record_status']}`",
                f"- post_plan_status: `{scenario['post_plan_status']}`",
                f"- status_report_status: `{scenario['formal_gate_status_report_status']}`",
                f"- decision_gate_status: `{scenario['decision_gate_status']}`",
                f"- post_plan_audit_status: `{scenario['post_plan_audit_status']}`",
                f"- remote_packet_safety_status: `{scenario['remote_packet_safety_status']}`",
                f"- next_blocked_lane_id: `{scenario['formal_gate_status_report_next_blocked_lane_id']}`",
                f"- remote_preflight_allowed_now: `{permissions['remote_preflight_allowed_now']}`",
                f"- remote_training_allowed_now: `{permissions['remote_training_allowed_now']}`",
                f"- formal_claim_allowed_now: `{permissions['formal_claim_allowed_now']}`",
                f"- regenerate_preflight_gate_artifacts_allowed: `{stages.get('regenerate_preflight_gate_artifacts', {}).get('allowed_now')}`",
                f"- approved_remote_preflight_allowed: `{stages.get('approved_remote_preflight', {}).get('allowed_now')}`",
                f"- gate3_remote_training_allowed: `{stages.get('gate3_remote_training', {}).get('allowed_now')}`",
                "",
            ]
        )
    lines.extend(["## Audit Issues", ""])
    if manifest["audit_issues"]:
        for issue in manifest["audit_issues"]:
            lines.append(f"- `{issue['scenario_id']}.{issue['issue_id']}`: {issue['message']}")
    else:
        lines.append("- none")
    lines.extend(["", "## Claim Boundaries", ""])
    lines.extend(f"- {item}" for item in manifest["claim_boundaries"])
    return "\n".join(lines) + "\n"


def _source_head() -> str:
    return module2_source_head()


if __name__ == "__main__":
    raise SystemExit(main())
