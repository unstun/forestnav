from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_formal_gate_handoff_bundle")
DEFAULT_DECISION_RECORD = Path("0_trials/module2_f02_6_decision_record/f02_6_decision_record.json")
DEFAULT_DECISION_INTAKE = Path("0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json")
DEFAULT_TRANSITION_GATE_AUDIT = Path("0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json")
DEFAULT_POST_PLAN = Path("0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json")
DEFAULT_STATUS_REPORT = Path("0_trials/module2_formal_gate_status_report/formal_gate_status_report.json")
DEFAULT_REMOTE_PACKET = Path("0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json")
DEFAULT_MISSING_ARTIFACTS = Path("0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json")
DEFAULT_H02_ACCEPTANCE = Path("0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json")
DEFAULT_SOURCE_FRESHNESS = Path("0_trials/module2_source_freshness_audit/source_freshness_audit.json")
REMOTE_STEP_IDS = ("sync_to_remote", "run_remote_preflight", "run_remote_training", "run_remote_audit")
FORMAL_STAGE_IDS = (
    "f02_6_decision_record",
    "regenerate_preflight_gate_artifacts",
    "approved_remote_preflight",
    "regenerate_remote_execution_packet",
    "gate3_remote_training",
    "gate3_remote_audit_pullback",
    "regenerate_h01_h02_formal_artifacts",
    "regenerate_claim_gate_artifacts",
)


@dataclass(frozen=True)
class FormalGateHandoffBundleConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    decision_record_path: Path = DEFAULT_DECISION_RECORD
    decision_intake_path: Path = DEFAULT_DECISION_INTAKE
    transition_gate_audit_path: Path = DEFAULT_TRANSITION_GATE_AUDIT
    post_plan_path: Path = DEFAULT_POST_PLAN
    status_report_path: Path = DEFAULT_STATUS_REPORT
    remote_packet_path: Path = DEFAULT_REMOTE_PACKET
    missing_artifacts_path: Path = DEFAULT_MISSING_ARTIFACTS
    h02_acceptance_path: Path = DEFAULT_H02_ACCEPTANCE
    source_freshness_path: Path = DEFAULT_SOURCE_FRESHNESS


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = FormalGateHandoffBundleConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        decision_record_path=args.decision_record,
        decision_intake_path=args.decision_intake,
        transition_gate_audit_path=args.transition_gate_audit,
        post_plan_path=args.post_plan,
        status_report_path=args.status_report,
        remote_packet_path=args.remote_packet,
        missing_artifacts_path=args.missing_artifacts,
        h02_acceptance_path=args.h02_acceptance,
        source_freshness_path=args.source_freshness,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "formal_gate_handoff_bundle.json"
    markdown_out = config.markdown_out or output_dir / "formal_gate_handoff_bundle.md"
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


def build_manifest(config: FormalGateHandoffBundleConfig) -> dict[str, Any]:
    decision = _read_json(config.decision_record_path)
    decision_intake = _read_json(config.decision_intake_path)
    transition_gate = _read_json(config.transition_gate_audit_path)
    post_plan = _read_json(config.post_plan_path)
    status_report = _read_json(config.status_report_path)
    remote_packet = _read_json(config.remote_packet_path)
    missing_artifacts = _read_json(config.missing_artifacts_path)
    h02_acceptance = _read_json(config.h02_acceptance_path)
    source_freshness = _read_json(config.source_freshness_path)

    stages = _handoff_stages(post_plan)
    remote_steps = _remote_steps(remote_packet)
    route_summary = _f02_6_route_handoff_summary(status_report)
    source_freshness_summary = _source_freshness_summary(source_freshness)
    permissions = _permissions(status_report, source_freshness=source_freshness)
    remaining_gap = _remaining_deliverables_gap_summary(status_report)
    single_next_action_index = _single_next_action_index(
        decision=decision,
        decision_intake=decision_intake,
        permissions=permissions,
        remaining_gap=remaining_gap,
        route_summary=route_summary,
        source_freshness_summary=source_freshness_summary,
    )
    safety_issues = _safety_issues(
        decision=decision,
        decision_intake=decision_intake,
        transition_gate=transition_gate,
        post_plan=post_plan,
        status_report=status_report,
        remote_packet=remote_packet,
        missing_artifacts=missing_artifacts,
        h02_acceptance=h02_acceptance,
        source_freshness=source_freshness,
        stages=stages,
        remote_steps=remote_steps,
        route_summary=route_summary,
        single_next_action_index=single_next_action_index,
    )
    status = _status(
        decision=decision,
        permissions=permissions,
        remote_packet=remote_packet,
        safety_issues=safety_issues,
    )
    return {
        "schema_version": 1,
        "artifact_name": "module2_formal_gate_handoff_bundle",
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
            "decision_record": str(config.decision_record_path),
            "decision_intake": str(config.decision_intake_path),
            "f02_6_transition_gate_audit": str(config.transition_gate_audit_path),
            "post_f02_6_regeneration_plan": str(config.post_plan_path),
            "formal_gate_status_report": str(config.status_report_path),
            "remote_formal_execution_packet": str(config.remote_packet_path),
            "formal_gate_missing_artifacts": str(config.missing_artifacts_path),
            "h02_formal_acceptance": str(config.h02_acceptance_path),
            "source_freshness_audit": str(config.source_freshness_path),
        },
        "current_state": {
            "decision_status": decision.get("status"),
            "decision_decider": decision.get("decider"),
            "transition_gate_status": transition_gate.get("status"),
            "transition_gate_audit_issue_count": transition_gate.get("audit_issue_count"),
            "post_plan_status": post_plan.get("status"),
            "status_report_status": status_report.get("status"),
            "remote_packet_status": remote_packet.get("status"),
            "ready_to_run_remote_training": bool(remote_packet.get("ready_to_run_remote_training")),
            "missing_artifacts_status": missing_artifacts.get("status"),
            "h02_status": h02_acceptance.get("status"),
            "h02_formal_output_accepted": bool(h02_acceptance.get("formal_output_accepted")),
            "h02_paper_result_input_allowed": bool(h02_acceptance.get("paper_result_input_allowed")),
            "next_blocked_lane": _next_blocked_lane_id(status_report),
            **source_freshness_summary,
        },
        "permissions_now": permissions,
        "next_handoff_action": _next_handoff_action(decision=decision, status_report=status_report),
        "single_next_action_index": single_next_action_index,
        "f02_6_route_handoff_summary": route_summary,
        "remaining_deliverables_gap_summary": remaining_gap,
        "status_report_proof_audit_deliverables_summary": _status_report_proof_audit_deliverables_summary(
            status_report
        ),
        "post_plan_remaining_deliverables_gap_summary": _remaining_deliverables_gap_summary(post_plan),
        "formal_gate_requirements": _requirements(missing_artifacts, "formal_gate_requirements"),
        "h02_formal_acceptance_requirements": _requirements(h02_acceptance, "formal_acceptance_requirements"),
        "remote_execution_steps": remote_steps,
        "handoff_stages": stages,
        "post_run_expected_artifacts": _post_run_expected_artifacts(remote_packet),
        "safety_issue_count": len(safety_issues),
        "safety_issues": safety_issues,
        "claim_boundaries": [
            "This handoff bundle is read-only and does not execute shell, ssh, rsync, preflight, training, audit, or pullback.",
            "Pending F02.6 means all remote execution steps must remain disabled.",
            "Any formal training command remains gpu3070ti-relay-only after Dr Sun approval and source-fresh regeneration.",
            "Pulled-back checkpoint, audit, hash, H01, and H02 evidence are required before paper result claims.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a read-only Module2 formal gate handoff bundle.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--decision-record", type=Path, default=DEFAULT_DECISION_RECORD)
    parser.add_argument("--decision-intake", type=Path, default=DEFAULT_DECISION_INTAKE)
    parser.add_argument("--transition-gate-audit", type=Path, default=DEFAULT_TRANSITION_GATE_AUDIT)
    parser.add_argument("--post-plan", type=Path, default=DEFAULT_POST_PLAN)
    parser.add_argument("--status-report", type=Path, default=DEFAULT_STATUS_REPORT)
    parser.add_argument("--remote-packet", type=Path, default=DEFAULT_REMOTE_PACKET)
    parser.add_argument("--missing-artifacts", type=Path, default=DEFAULT_MISSING_ARTIFACTS)
    parser.add_argument("--h02-acceptance", type=Path, default=DEFAULT_H02_ACCEPTANCE)
    parser.add_argument("--source-freshness", type=Path, default=DEFAULT_SOURCE_FRESHNESS)
    return parser.parse_args(list(argv) if argv is not None else None)


def _status(
    *,
    decision: dict[str, Any],
    permissions: dict[str, bool],
    remote_packet: dict[str, Any],
    safety_issues: Sequence[dict[str, str]],
) -> str:
    if safety_issues:
        return "blocked_handoff_input_safety_issues"
    if decision.get("status") == "pending_human_decision":
        return "blocked_until_f02_6_decision"
    if permissions.get("remote_training_allowed_now") is True and remote_packet.get("ready_to_run_remote_training") is True:
        return "ready_for_manual_remote_execution_review"
    return "blocked_formal_gate_handoff"


def _handoff_stages(post_plan: dict[str, Any]) -> list[dict[str, Any]]:
    stages_by_id = {
        str(stage.get("stage_id")): stage
        for stage in post_plan.get("ordered_stages", [])
        if isinstance(stage, dict) and stage.get("stage_id")
    }
    handoff: list[dict[str, Any]] = []
    for index, stage_id in enumerate(FORMAL_STAGE_IDS, start=1):
        stage = stages_by_id.get(stage_id, {})
        handoff.append(
            {
                "order": index,
                "stage_id": stage_id,
                "phase": stage.get("phase"),
                "status": stage.get("status", "missing"),
                "source_allowed_now": bool(stage.get("allowed_now")),
                "runs_training": bool(stage.get("runs_training")),
                "runs_remote_preflight": bool(stage.get("runs_remote_preflight")),
                "host": stage.get("host"),
                "blocked_by": [str(item) for item in stage.get("blocked_by", []) if item],
                "evidence_paths": [str(item) for item in stage.get("evidence_paths", []) if item],
                "command_templates": [str(item) for item in stage.get("command_templates", []) if item],
            }
        )
    return handoff


def _remote_steps(remote_packet: dict[str, Any]) -> dict[str, dict[str, Any]]:
    steps = remote_packet.get("execution_steps") if isinstance(remote_packet.get("execution_steps"), dict) else {}
    out: dict[str, dict[str, Any]] = {}
    for step_id in REMOTE_STEP_IDS:
        step = steps.get(step_id) if isinstance(steps.get(step_id), dict) else {}
        out[step_id] = {
            "allowed_now": bool(step.get("allowed_now")),
            "runs_training": bool(step.get("runs_training")),
            "command": str(step.get("command") or ""),
            "blocked_by": [str(item) for item in step.get("blocked_by", []) if item],
        }
    return out


def _safety_issues(
    *,
    decision: dict[str, Any],
    decision_intake: dict[str, Any],
    transition_gate: dict[str, Any],
    post_plan: dict[str, Any],
    status_report: dict[str, Any],
    remote_packet: dict[str, Any],
    missing_artifacts: dict[str, Any],
    h02_acceptance: dict[str, Any],
    source_freshness: dict[str, Any],
    stages: Sequence[dict[str, Any]],
    remote_steps: dict[str, dict[str, Any]],
    route_summary: dict[str, Any],
    single_next_action_index: dict[str, Any],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    issues.extend(_transition_gate_issues(transition_gate))
    issues.extend(_f02_6_route_handoff_issues(route_summary))
    issues.extend(_single_next_action_index_issues(single_next_action_index))
    for name, artifact in (
        ("decision_intake", decision_intake),
        ("post_plan", post_plan),
        ("status_report", status_report),
        ("missing_artifacts", missing_artifacts),
        ("h02_acceptance", h02_acceptance),
        ("source_freshness", source_freshness),
    ):
        if artifact.get("executes_commands") is True:
            issues.append(_issue(f"{name}_executes_commands", f"{name} must remain read-only"))
        if artifact.get("runs_training") is True:
            issues.append(_issue(f"{name}_runs_training", f"{name} must not run training"))
        if artifact.get("runs_remote_preflight") is True:
            issues.append(_issue(f"{name}_runs_remote_preflight", f"{name} must not run remote preflight"))
        if artifact.get("local_training_allowed") is True:
            issues.append(_issue(f"{name}_allows_local_training", f"{name} must not allow local training"))
        if artifact.get("formal_claim_allowed") is True:
            issues.append(_issue(f"{name}_allows_formal_claim", f"{name} must not allow formal claims"))

    permissions = _permissions(status_report, source_freshness=source_freshness)
    pending = decision.get("status") == "pending_human_decision"
    if pending:
        for step_id, step in remote_steps.items():
            if step["allowed_now"]:
                issues.append(_issue(f"pending_decision_allows_{step_id}", "remote steps must be disabled while F02.6 is pending"))
    if permissions.get("local_training_allowed_now") is True:
        issues.append(_issue("status_report_allows_local_training", "local training is forbidden for formal PPO"))
    if permissions.get("remote_training_allowed_now") is True and remote_packet.get("ready_to_run_remote_training") is not True:
        issues.append(_issue("status_report_allows_training_without_ready_packet", "remote training needs a ready remote packet"))
    if not _source_freshness_ready_for_remote_preflight(source_freshness) and _remote_execution_allowed(
        remote_steps=remote_steps,
        stages=stages,
        status_permissions=status_report.get("permissions_now") if isinstance(status_report.get("permissions_now"), dict) else {},
    ):
        issues.append(
            _issue(
                "source_freshness_blocks_remote_execution",
                "remote preflight/training cannot be allowed while source freshness requires regeneration",
            )
        )
    issues.extend(_remaining_gap_issues(post_plan=post_plan, status_report=status_report))

    for stage in stages:
        if stage["runs_training"] and stage["host"] not in {None, "gpu3070ti-relay"}:
            issues.append(_issue(f"{stage['stage_id']}_wrong_training_host", "formal training stage must target gpu3070ti-relay"))
        if not stage["source_allowed_now"] and stage["stage_id"] in {"approved_remote_preflight", "gate3_remote_training"} and not stage["blocked_by"]:
            issues.append(_issue(f"{stage['stage_id']}_missing_blocked_by", "disabled remote stages must explain their blockers"))
    return issues


def _single_next_action_index(
    *,
    decision: dict[str, Any],
    decision_intake: dict[str, Any],
    permissions: dict[str, bool],
    remaining_gap: dict[str, Any],
    route_summary: dict[str, Any],
    source_freshness_summary: dict[str, Any],
) -> dict[str, Any]:
    pending = decision.get("status") == "pending_human_decision"
    intake_contract = (
        decision_intake.get("decision_intake_contract")
        if isinstance(decision_intake.get("decision_intake_contract"), dict)
        else {}
    )
    next_request = (
        decision_intake.get("next_human_decision_request")
        if isinstance(decision_intake.get("next_human_decision_request"), dict)
        else {}
    )
    record_templates = _record_command_templates(intake_contract) if pending else []
    missing_by_category = {
        str(category): int(payload.get("missing_count") or 0)
        for category, payload in remaining_gap.get("categories", {}).items()
        if isinstance(payload, dict)
    }
    return {
        "index_id": "module2_formal_gate_single_next_action_index",
        "status": "awaiting_dr_sun_f02_6_decision" if pending else "follow_handoff_stages",
        "single_current_human_entry": bool(pending),
        "next_action_id": "record_f02_6_decision" if pending else "manual_handoff_stage_review",
        "decision_owner_required": next_request.get("decision_owner_required")
        or intake_contract.get("decision_owner_required"),
        "valid_decisions": _strings(next_request.get("valid_decisions") or intake_contract.get("valid_decisions")),
        "required_record_fields": _strings(
            next_request.get("required_record_fields")
            or intake_contract.get("required_record_fields_for_non_pending_decision")
        ),
        "current_allowed_action_ids": _strings(next_request.get("current_allowed_action_ids")),
        "current_blocked_action_ids": _strings(next_request.get("current_blocked_action_ids")),
        "post_decision_routes_are_current_authorization": next_request.get(
            "post_decision_routes_are_current_authorization"
        )
        is True,
        "all_execution_disabled_now": next_request.get("all_execution_disabled_now") is True if pending else False,
        "record_command_templates": record_templates,
        "record_command_template_count": len(record_templates),
        "local_training_allowed_now": permissions.get("local_training_allowed_now") is True,
        "remote_preflight_allowed_now": permissions.get("remote_preflight_allowed_now") is True,
        "remote_training_allowed_now": permissions.get("remote_training_allowed_now") is True,
        "formal_claim_allowed_now": permissions.get("formal_claim_allowed_now") is True,
        "paper_result_material_allowed_now": False,
        "missing_deliverable_count": int(remaining_gap.get("total_missing_deliverables") or 0),
        "open_category_count": int(remaining_gap.get("open_category_count") or 0),
        "missing_by_category": missing_by_category,
        "source_freshness_status": source_freshness_summary.get("source_freshness_status"),
        "source_freshness_blocking_regeneration_required": source_freshness_summary.get(
            "source_freshness_blocking_regeneration_required"
        ),
        "approved_route_next_lane": route_summary.get("approved_route_next_lane"),
        "rejected_route_next_lane": route_summary.get("rejected_route_next_lane"),
        "after_approval_still_requires": list(route_summary.get("decision_impact_formal_training_still_requires", [])),
        "claim_boundaries": [
            "This index is a read-only handoff pointer, not a decision record.",
            "The listed command templates only record Dr Sun's F02.6 decision; they do not run preflight, training, audit, sync, pullback, or paper-result generation.",
            "Approval does not directly authorize remote preflight or remote training.",
            "Local PPO training remains prohibited.",
        ],
    }


def _record_command_templates(intake_contract: dict[str, Any]) -> list[dict[str, Any]]:
    raw = intake_contract.get("record_command_templates")
    raw = raw if isinstance(raw, list) else []
    out: list[dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict) or not item.get("decision") or not item.get("command"):
            continue
        out.append(
            {
                "decision": str(item["decision"]),
                "command": str(item["command"]),
                "execution_boundary": "local_decision_record_only",
                "requires_dr_sun_note": True,
                "runs_training": False,
                "runs_remote_preflight": False,
                "allowed_for_agent_now": False,
            }
        )
    return out


def _single_next_action_index_issues(index: dict[str, Any]) -> list[dict[str, str]]:
    if not index:
        return [_issue("single_next_action_index_missing", "handoff bundle must expose a single next-action index")]
    issues: list[dict[str, str]] = []
    if index.get("index_id") != "module2_formal_gate_single_next_action_index":
        issues.append(_issue("single_next_action_index_id_invalid", "single next-action index id is invalid"))
    pending = index.get("status") == "awaiting_dr_sun_f02_6_decision"
    if pending:
        if index.get("single_current_human_entry") is not True:
            issues.append(_issue("single_next_action_not_marked_human_entry", "pending F02.6 must be a single human-entry gate"))
        if index.get("next_action_id") != "record_f02_6_decision":
            issues.append(_issue("single_next_action_wrong_action", "pending F02.6 next action must be record_f02_6_decision"))
        if index.get("decision_owner_required") != "Dr Sun":
            issues.append(_issue("single_next_action_wrong_owner", "F02.6 decision owner must be Dr Sun"))
        if "record_f02_6_decision" not in index.get("current_allowed_action_ids", []):
            issues.append(_issue("single_next_action_missing_allowed_record", "record_f02_6_decision must be the only allowed lane"))
        for blocked in ("remote_preflight", "remote_training", "local_training", "formal_claim", "paper_result_material"):
            if blocked not in index.get("current_blocked_action_ids", []):
                issues.append(_issue(f"single_next_action_missing_blocked_{blocked}", f"{blocked} must remain blocked"))
        if index.get("post_decision_routes_are_current_authorization") is not False:
            issues.append(_issue("single_next_action_routes_authorize_execution", "post-decision routes are not current authorization"))
        if index.get("all_execution_disabled_now") is not True:
            issues.append(_issue("single_next_action_execution_not_disabled", "all execution must be disabled while F02.6 is pending"))
        if int(index.get("record_command_template_count") or 0) != 2:
            issues.append(_issue("single_next_action_command_template_count", "approve and reject command templates are required"))
    for field, issue_id in (
        ("local_training_allowed_now", "single_next_action_allows_local_training"),
        ("remote_preflight_allowed_now", "single_next_action_allows_remote_preflight"),
        ("remote_training_allowed_now", "single_next_action_allows_remote_training"),
        ("formal_claim_allowed_now", "single_next_action_allows_formal_claim"),
        ("paper_result_material_allowed_now", "single_next_action_allows_paper_result_material"),
    ):
        if pending and index.get(field) is not False:
            issues.append(_issue(issue_id, "single next-action index must not authorize execution or result material"))
    forbidden_tokens = (
        "ssh ",
        "rsync ",
        "scp ",
        "preflight_rl_rs_gate3_formal_trial",
        "run_rl_rs_gate3_trial",
        "audit_rl_rs_gate3_trial",
        "build_module2_paper",
    )
    for template in index.get("record_command_templates", []):
        if not isinstance(template, dict):
            issues.append(_issue("single_next_action_template_malformed", "record command template must be an object"))
            continue
        decision = str(template.get("decision") or "unknown")
        command = str(template.get("command") or "")
        safe_decision = decision.replace("_", "")
        if "build_module2_f02_6_decision_record" not in command:
            issues.append(_issue(f"single_next_action_{safe_decision}_wrong_command", "template must record F02.6 decision only"))
        if any(token in command for token in forbidden_tokens):
            issues.append(_issue(f"single_next_action_{safe_decision}_forbidden_command", "template must not execute remote, training, audit, or paper commands"))
        if template.get("execution_boundary") != "local_decision_record_only":
            issues.append(_issue(f"single_next_action_{safe_decision}_wrong_boundary", "template boundary must be local decision record only"))
        if template.get("runs_training") is not False or template.get("runs_remote_preflight") is not False:
            issues.append(_issue(f"single_next_action_{safe_decision}_executes", "template must not run training or remote preflight"))
        if template.get("allowed_for_agent_now") is not False:
            issues.append(_issue(f"single_next_action_{safe_decision}_agent_allowed", "agent must not self-close F02.6"))
    return issues


def _f02_6_route_handoff_summary(status_report: dict[str, Any]) -> dict[str, Any]:
    summary = (
        status_report.get("f02_6_decision_intake_summary")
        if isinstance(status_report.get("f02_6_decision_intake_summary"), dict)
        else {}
    )
    route_decisions = summary.get("post_decision_route_decisions")
    if not isinstance(route_decisions, list):
        route_decisions = []
    return {
        "present": bool(summary),
        "post_decision_route_count": int(summary.get("post_decision_route_count") or 0),
        "post_decision_route_decisions": [str(item) for item in route_decisions if item],
        "approved_route_next_lane": summary.get("approved_route_next_lane"),
        "approved_route_allows_remote_training_now": summary.get("approved_route_allows_remote_training_now"),
        "rejected_route_next_lane": summary.get("rejected_route_next_lane"),
        "rejected_route_requires_new_protocol_contract": summary.get("rejected_route_requires_new_protocol_contract"),
        "decision_impact_present": summary.get("decision_impact_present"),
        "decision_record_is_not_training_authorization": summary.get(
            "decision_record_is_not_training_authorization"
        ),
        "decision_record_is_not_paper_result_material": summary.get(
            "decision_record_is_not_paper_result_material"
        ),
        "decision_impact_remote_preflight_allowed_now": summary.get(
            "decision_impact_remote_preflight_allowed_now"
        ),
        "decision_impact_remote_training_allowed_now": summary.get(
            "decision_impact_remote_training_allowed_now"
        ),
        "decision_impact_formal_claim_allowed_now": summary.get(
            "decision_impact_formal_claim_allowed_now"
        ),
        "decision_impact_paper_result_material_allowed_now": summary.get(
            "decision_impact_paper_result_material_allowed_now"
        ),
        "decision_impact_formal_training_still_requires": [
            str(item)
            for item in summary.get("decision_impact_formal_training_still_requires", [])
            if item
        ]
        if isinstance(summary.get("decision_impact_formal_training_still_requires"), list)
        else [],
    }


def _f02_6_route_handoff_issues(route_summary: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    expected = {"approve_obstacle_summary_warm_start", "reject_obstacle_summary_warm_start"}
    if not route_summary["present"]:
        return [_issue("f02_6_route_summary_missing", "handoff bundle must consume F02.6 approve/reject route summary")]
    if int(route_summary["post_decision_route_count"] or 0) < 2:
        issues.append(_issue("f02_6_route_count_incomplete", "handoff bundle must see both approve and reject routes"))
    if not expected.issubset(set(route_summary["post_decision_route_decisions"])):
        issues.append(_issue("f02_6_route_decisions_incomplete", "F02.6 routes must include approve and reject decisions"))
    if route_summary["approved_route_next_lane"] != "source_fresh_regeneration":
        issues.append(_issue("f02_6_approved_route_next_lane_invalid", "approval must route first to source-fresh regeneration"))
    if route_summary["approved_route_allows_remote_training_now"] is not False:
        issues.append(_issue("f02_6_approved_route_allows_remote_training", "approval route must not directly allow remote training"))
    if route_summary["rejected_route_next_lane"] != "protocol_redesign":
        issues.append(_issue("f02_6_rejected_route_next_lane_invalid", "rejection must route to protocol redesign"))
    if route_summary["rejected_route_requires_new_protocol_contract"] is not True:
        issues.append(_issue("f02_6_rejected_route_missing_protocol_contract", "rejection route must require a new or revised protocol contract"))
    if route_summary["decision_impact_present"] is not True:
        issues.append(_issue("f02_6_decision_impact_missing", "handoff bundle must consume F02.6 decision-impact summary"))
    if route_summary["decision_record_is_not_training_authorization"] is not True:
        issues.append(_issue("f02_6_decision_record_may_authorize_training", "F02.6 decision record must not be training authorization"))
    if route_summary["decision_record_is_not_paper_result_material"] is not True:
        issues.append(_issue("f02_6_decision_record_may_be_paper_result_material", "F02.6 decision record must not be paper result material"))
    for field, issue_id in (
        ("decision_impact_remote_preflight_allowed_now", "f02_6_decision_impact_allows_remote_preflight"),
        ("decision_impact_remote_training_allowed_now", "f02_6_decision_impact_allows_remote_training"),
        ("decision_impact_formal_claim_allowed_now", "f02_6_decision_impact_allows_formal_claim"),
        ("decision_impact_paper_result_material_allowed_now", "f02_6_decision_impact_allows_paper_result_material"),
    ):
        if route_summary[field] is not False:
            issues.append(_issue(issue_id, "F02.6 decision-impact summary must not authorize execution or result material"))
    for required in (
        "source_freshness_audit",
        "post_f02_6_regeneration_plan",
        "post_f02_6_plan_audit",
        "remote_formal_execution_packet_ready",
        "approved_remote_preflight",
    ):
        if required not in route_summary["decision_impact_formal_training_still_requires"]:
            issues.append(
                _issue(
                    f"f02_6_decision_impact_missing_required_{required}",
                    "decision-impact summary must list every pre-training gate still required",
                )
            )
    return issues


def _remaining_gap_issues(*, post_plan: dict[str, Any], status_report: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    plan_gap = _remaining_deliverables_gap_summary(post_plan)
    status_gap = _remaining_deliverables_gap_summary(status_report)
    if not plan_gap["present"]:
        issues.append(_issue("post_plan_missing_remaining_deliverables_gap_summary", "post-plan must expose remaining deliverables gap summary"))
    if not status_gap["present"]:
        issues.append(_issue("status_report_missing_remaining_deliverables_gap_summary", "status report must expose remaining deliverables gap summary"))
    if plan_gap["present"] and status_gap["present"] and _gap_signature(plan_gap) != _gap_signature(status_gap):
        issues.append(_issue("remaining_deliverables_gap_summary_mismatch", "post-plan and status report gap summaries must match"))
    if status_gap["total_missing_deliverables"] > 0 or status_gap["open_category_count"] > 0:
        permissions = _permissions(status_report)
        if permissions.get("formal_claim_allowed_now") is True:
            issues.append(_issue("formal_claim_allowed_with_remaining_deliverables_gap_open", "formal claim must stay blocked while deliverable gaps are open"))
    return issues


def _transition_gate_issues(transition_gate: dict[str, Any]) -> list[dict[str, str]]:
    if not transition_gate:
        return [_issue("transition_gate_audit_missing", "F02.6 transition gate audit must be present in the handoff bundle")]
    issues: list[dict[str, str]] = []
    for key, issue_id, detail in (
        ("executes_commands", "transition_gate_executes_commands", "transition audit must be read-only"),
        ("runs_training", "transition_gate_runs_training", "transition audit must not run training"),
        ("runs_remote_preflight", "transition_gate_runs_remote_preflight", "transition audit must not run remote preflight"),
        ("local_training_allowed", "transition_gate_allows_local_training", "transition audit must preserve local-training prohibition"),
        ("formal_claim_allowed", "transition_gate_allows_formal_claim", "transition audit must not allow formal claims"),
    ):
        if transition_gate.get(key) is not False:
            issues.append(_issue(issue_id, detail))
    if transition_gate.get("status") != "f02_6_transition_gate_audit_passed":
        issues.append(_issue("transition_gate_audit_not_passed", "F02.6 transition gate audit must pass before handoff is safe"))
    if int(transition_gate.get("audit_issue_count") or 0) > 0:
        issues.append(_issue("transition_gate_audit_issues_open", "F02.6 transition gate audit has open issues"))

    scenarios = transition_gate.get("scenario_summaries") if isinstance(transition_gate.get("scenario_summaries"), list) else []
    by_id = {str(item.get("scenario_id")): item for item in scenarios if isinstance(item, dict)}
    for scenario_id in ("pending", "approved", "rejected"):
        if scenario_id not in by_id:
            issues.append(_issue(f"transition_gate_missing_{scenario_id}_scenario", f"transition audit missing {scenario_id} scenario"))
    for scenario_id, scenario in by_id.items():
        permissions = scenario.get("formal_gate_status_report_permissions_now") if isinstance(scenario.get("formal_gate_status_report_permissions_now"), dict) else {}
        if permissions.get("remote_training_allowed_now") is True:
            issues.append(_issue(f"transition_gate_{scenario_id}_allows_remote_training", "transition audit scenario must not directly allow remote training"))
        if permissions.get("formal_claim_allowed_now") is True:
            issues.append(_issue(f"transition_gate_{scenario_id}_allows_formal_claim", "transition audit scenario must not directly allow formal claims"))
        if scenario_id in {"pending", "rejected"} and permissions.get("remote_preflight_allowed_now") is True:
            issues.append(_issue(f"transition_gate_{scenario_id}_allows_remote_preflight", "pending/rejected transition scenarios must not allow remote preflight"))

    approved = by_id.get("approved", {})
    approved_stages = approved.get("post_plan_stage_summary") if isinstance(approved.get("post_plan_stage_summary"), dict) else {}
    if approved_stages.get("regenerate_preflight_gate_artifacts", {}).get("allowed_now") is not True:
        issues.append(_issue("transition_gate_approved_regeneration_not_ready", "approved scenario should expose source-fresh regeneration as next local gate"))
    for stage_id in ("approved_remote_preflight", "gate3_remote_training", "regenerate_claim_gate_artifacts"):
        if approved_stages.get(stage_id, {}).get("allowed_now") is True:
            issues.append(_issue(f"transition_gate_approved_{stage_id}_ready_too_early", "approved scenario must not bypass downstream formal gates"))

    rejected = by_id.get("rejected", {})
    if rejected and rejected.get("post_plan_status") != "blocked_by_f02_6_rejected":
        issues.append(_issue("transition_gate_rejected_not_routed_away", "rejected scenario must block the obstacle-summary warm-start formal path"))
    return issues


def _next_handoff_action(*, decision: dict[str, Any], status_report: dict[str, Any]) -> dict[str, Any]:
    if decision.get("status") == "pending_human_decision":
        return {
            "action_id": "record_f02_6_decision",
            "requires_dr_sun": True,
            "allowed_for_agent_now": False,
            "description": "Dr Sun must approve obstacle-summary warm-start or reject it before remote formal execution can proceed.",
        }
    lane = _next_blocked_lane_id(status_report)
    return {
        "action_id": f"resolve_{lane}" if lane else "manual_execution_review",
        "requires_dr_sun": False,
        "allowed_for_agent_now": False,
        "description": "Use the handoff stages as an audit checklist; this artifact does not execute commands.",
    }


def _source_freshness_summary(source_freshness: dict[str, Any]) -> dict[str, Any]:
    commit_lag = (
        source_freshness.get("commit_lag_summary")
        if isinstance(source_freshness.get("commit_lag_summary"), dict)
        else {}
    )
    return {
        "source_freshness_status": source_freshness.get("status"),
        "source_freshness_regeneration_required": source_freshness.get(
            "regeneration_required_before_remote_formal_execution"
        ),
        "source_freshness_blocking_regeneration_required": _source_freshness_blocking_regeneration_required(
            source_freshness
        ),
        "source_freshness_non_self_changed_records": commit_lag.get(
            "records_with_non_self_changed_paths_since_source"
        ),
        "source_freshness_self_artifact_only_lag_records": commit_lag.get("records_with_self_artifact_only_lag"),
    }


def _source_freshness_ready_for_remote_preflight(source_freshness: dict[str, Any]) -> bool:
    return (
        source_freshness.get("status")
        in {
            "source_freshness_clean_current",
            "source_freshness_self_artifact_lag_only_gate_ready",
            "source_freshness_tracked_artifact_lag_only_gate_ready",
        }
        and _source_freshness_blocking_regeneration_required(source_freshness) is False
    )


def _source_freshness_blocking_regeneration_required(source_freshness: dict[str, Any]) -> bool:
    if "blocking_regeneration_required_before_remote_formal_execution" in source_freshness:
        return source_freshness.get("blocking_regeneration_required_before_remote_formal_execution") is True
    return source_freshness.get("regeneration_required_before_remote_formal_execution") is True


def _remote_execution_allowed(
    *,
    remote_steps: dict[str, dict[str, Any]],
    stages: Sequence[dict[str, Any]],
    status_permissions: dict[str, Any],
) -> bool:
    if any(bool(step.get("allowed_now")) for step in remote_steps.values()):
        return True
    for key in ("remote_preflight_allowed_now", "remote_training_allowed_now"):
        if status_permissions.get(key) is True:
            return True
    for stage in stages:
        if (
            stage.get("stage_id") in {"approved_remote_preflight", "gate3_remote_training"}
            and stage.get("source_allowed_now") is True
        ):
            return True
    return False


def _permissions(status_report: dict[str, Any], *, source_freshness: dict[str, Any] | None = None) -> dict[str, bool]:
    permissions = status_report.get("permissions_now") if isinstance(status_report.get("permissions_now"), dict) else {}
    out = {str(key): bool(value) for key, value in permissions.items()}
    if source_freshness is None:
        return out
    source_ready = _source_freshness_ready_for_remote_preflight(source_freshness)
    out["source_freshness_ready_for_remote_preflight"] = source_ready
    if not source_ready:
        out["remote_preflight_allowed_now"] = False
        out["remote_training_allowed_now"] = False
        out["formal_claim_allowed_now"] = False
    out["local_training_allowed_now"] = False
    return out


def _next_blocked_lane_id(status_report: dict[str, Any]) -> str | None:
    lane = status_report.get("next_blocked_lane")
    if isinstance(lane, dict) and lane.get("lane_id"):
        return str(lane["lane_id"])
    return None


def _strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _requirements(artifact: dict[str, Any], key: str) -> list[dict[str, Any]]:
    reqs = artifact.get(key) if isinstance(artifact.get(key), list) else []
    out: list[dict[str, Any]] = []
    for req in reqs:
        if not isinstance(req, dict):
            continue
        out.append(
            {
                "requirement_id": req.get("requirement_id"),
                "phase": req.get("phase"),
                "status": req.get("status"),
                "complete": bool(req.get("complete")),
                "execution_allowed_now": bool(req.get("execution_allowed_now")),
                "missing_artifact_ids": [str(item) for item in req.get("missing_artifact_ids", []) if item],
                "responsible_stage_id": req.get("responsible_stage_id"),
                "responsible_stage_status": req.get("responsible_stage_status"),
                "responsible_stage_allowed_now": req.get("responsible_stage_allowed_now"),
                "responsible_stage_blocked_by": [str(item) for item in req.get("responsible_stage_blocked_by", []) if item],
                "responsible_stage_evidence_paths": [str(item) for item in req.get("responsible_stage_evidence_paths", []) if item],
                "acceptable_evidence": [str(item) for item in req.get("acceptable_evidence", []) if item],
                "invalid_substitutes": [str(item) for item in req.get("invalid_substitutes", []) if item],
            }
        )
    return out


def _remaining_deliverables_gap_summary(artifact: dict[str, Any]) -> dict[str, Any]:
    raw = artifact.get("remaining_deliverables_gap_summary")
    summary = raw if isinstance(raw, dict) else {}
    categories = _gap_categories(summary.get("categories"))
    return {
        "present": bool(summary),
        "summary_id": summary.get("summary_id"),
        "total_missing_deliverables": int(summary.get("total_missing_deliverables") or 0),
        "open_category_count": int(summary.get("open_category_count") or 0),
        "category_order": [str(item) for item in summary.get("category_order", []) if item]
        if isinstance(summary.get("category_order"), list)
        else list(categories),
        "categories": categories,
    }


def _status_report_proof_audit_deliverables_summary(status_report: dict[str, Any]) -> dict[str, Any]:
    raw = status_report.get("formal_gate_proof_audit_remaining_deliverables_top_level_summary")
    raw = raw if isinstance(raw, dict) else {}
    counts = raw.get("missing_counts_by_formal_category")
    counts = counts if isinstance(counts, dict) else {}
    matrix_ids = raw.get("missing_matrix_ids_by_formal_category")
    matrix_ids = matrix_ids if isinstance(matrix_ids, dict) else {}
    return {
        "present": raw.get("present") is True or bool(counts or matrix_ids),
        "missing_counts_by_formal_category": {
            str(category): int(count) for category, count in counts.items()
        },
        "missing_matrix_ids_by_formal_category": {
            str(category): [str(item) for item in items] if isinstance(items, list) else []
            for category, items in matrix_ids.items()
        },
        "next_blocked_lane": raw.get("next_blocked_lane"),
        "h01_status": raw.get("h01_status"),
        "h02_status": raw.get("h02_status"),
        "h02_formal_output_accepted": raw.get("h02_formal_output_accepted"),
        "h02_paper_result_input_allowed": raw.get("h02_paper_result_input_allowed"),
    }


def _gap_categories(raw_categories: Any) -> dict[str, dict[str, Any]]:
    if isinstance(raw_categories, dict):
        items = raw_categories.items()
    elif isinstance(raw_categories, list):
        items = ((item.get("category"), item) for item in raw_categories if isinstance(item, dict))
    else:
        items = ()
    out: dict[str, dict[str, Any]] = {}
    for category, raw in items:
        if not category or not isinstance(raw, dict):
            continue
        matrix_ids = raw.get("missing_artifact_matrix_ids")
        if not isinstance(matrix_ids, list):
            missing_artifacts = raw.get("missing_artifacts") if isinstance(raw.get("missing_artifacts"), list) else []
            matrix_ids = [item.get("matrix_id") for item in missing_artifacts if isinstance(item, dict)]
        out[str(category)] = {
            "missing_count": int(raw.get("missing_count") or 0),
            "responsible_stage_id": raw.get("responsible_stage_id"),
            "responsible_stage_allowed_now": raw.get("responsible_stage_allowed_now"),
            "missing_artifact_matrix_ids": [str(item) for item in matrix_ids if item],
        }
    return out


def _gap_signature(summary: dict[str, Any]) -> dict[str, Any]:
    categories = summary.get("categories") if isinstance(summary.get("categories"), dict) else {}
    return {
        "summary_id": summary.get("summary_id"),
        "total_missing_deliverables": summary.get("total_missing_deliverables"),
        "open_category_count": summary.get("open_category_count"),
        "categories": {
            key: {
                "missing_count": value.get("missing_count"),
                "responsible_stage_id": value.get("responsible_stage_id"),
                "missing_artifact_matrix_ids": value.get("missing_artifact_matrix_ids", []),
            }
            for key, value in sorted(categories.items())
            if isinstance(value, dict)
        },
    }


def _post_run_expected_artifacts(remote_packet: dict[str, Any]) -> list[str]:
    pullback = remote_packet.get("post_run_pullback") if isinstance(remote_packet.get("post_run_pullback"), dict) else {}
    return [str(item) for item in pullback.get("expected_artifacts", []) if item]


def _read_json(path: Path) -> dict[str, Any]:
    if not Path(path).is_file():
        return {}
    with Path(path).open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    return data if isinstance(data, dict) else {}


def _issue(issue_id: str, detail: str) -> dict[str, str]:
    return {"issue_id": issue_id, "detail": detail}


def _source_head() -> str | None:
    value = module2_source_head()
    return None if value == "unknown" else value


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 Formal Gate Handoff Bundle",
        "",
        f"- status: `{manifest['status']}`",
        f"- executes commands: `{manifest['executes_commands']}`",
        f"- runs training: `{manifest['runs_training']}`",
        f"- local training allowed: `{manifest['local_training_allowed']}`",
        f"- next action: `{manifest['next_handoff_action']['action_id']}`",
        "",
        "## Remote Steps",
        "",
    ]
    for step_id, step in manifest["remote_execution_steps"].items():
        blockers = ", ".join(step["blocked_by"]) or "none"
        lines.append(f"- `{step_id}`: allowed_now=`{step['allowed_now']}`, blocked_by=`{blockers}`")
    route = manifest["f02_6_route_handoff_summary"]
    lines.extend(["", "## F02.6 Route Handoff", ""])
    lines.append(f"- present: `{route['present']}`")
    lines.append(f"- post_decision_route_count: `{route['post_decision_route_count']}`")
    lines.append(f"- post_decision_route_decisions: `{', '.join(route['post_decision_route_decisions'])}`")
    lines.append(f"- approved_route_next_lane: `{route['approved_route_next_lane']}`")
    lines.append(f"- approved_route_allows_remote_training_now: `{route['approved_route_allows_remote_training_now']}`")
    lines.append(f"- rejected_route_next_lane: `{route['rejected_route_next_lane']}`")
    lines.append(
        f"- rejected_route_requires_new_protocol_contract: `{route['rejected_route_requires_new_protocol_contract']}`"
    )
    lines.append(f"- decision_impact_present: `{route['decision_impact_present']}`")
    lines.append(
        f"- decision_record_is_not_training_authorization: `{route['decision_record_is_not_training_authorization']}`"
    )
    lines.append(
        f"- decision_record_is_not_paper_result_material: `{route['decision_record_is_not_paper_result_material']}`"
    )
    lines.append(
        f"- decision_impact_remote_training_allowed_now: `{route['decision_impact_remote_training_allowed_now']}`"
    )
    lines.append(
        f"- decision_impact_formal_claim_allowed_now: `{route['decision_impact_formal_claim_allowed_now']}`"
    )
    lines.append(
        "- decision_impact_paper_result_material_allowed_now: "
        f"`{route['decision_impact_paper_result_material_allowed_now']}`"
    )
    lines.append(
        "- decision_impact_formal_training_still_requires: "
        f"`{', '.join(route['decision_impact_formal_training_still_requires'])}`"
    )
    lines.extend(["", "## Source Freshness Gate", ""])
    current_state = manifest["current_state"]
    for key in (
        "source_freshness_status",
        "source_freshness_regeneration_required",
        "source_freshness_non_self_changed_records",
        "source_freshness_self_artifact_only_lag_records",
    ):
        lines.append(f"- {key}: `{current_state.get(key)}`")
    lines.extend(["", "## Handoff Stages", ""])
    for stage in manifest["handoff_stages"]:
        blockers = ", ".join(stage["blocked_by"]) or "none"
        lines.append(f"- {stage['order']}. `{stage['stage_id']}`: allowed_now=`{stage['source_allowed_now']}`, blocked_by=`{blockers}`")
    lines.extend(["", "## Requirement Summary", ""])
    gap = manifest["remaining_deliverables_gap_summary"]
    lines.append(
        f"- remaining deliverables gap: total_missing=`{gap['total_missing_deliverables']}`, "
        f"open_categories=`{gap['open_category_count']}`"
    )
    for category in gap["category_order"]:
        item = gap["categories"].get(category, {})
        lines.append(
            f"  - `{category}`: missing=`{item.get('missing_count')}`, "
            f"responsible_stage=`{item.get('responsible_stage_id')}`"
        )
    proof_summary = manifest["status_report_proof_audit_deliverables_summary"]
    lines.extend(["", "## Status Report Proof-Audit Deliverables Summary", ""])
    lines.append(f"- present: `{proof_summary['present']}`")
    lines.append(f"- missing_counts_by_formal_category: `{proof_summary['missing_counts_by_formal_category']}`")
    lines.append(f"- next_blocked_lane: `{proof_summary['next_blocked_lane']}`")
    lines.append(f"- h01_status: `{proof_summary['h01_status']}`")
    lines.append(f"- h02_status: `{proof_summary['h02_status']}`")
    for category, matrix_ids in proof_summary["missing_matrix_ids_by_formal_category"].items():
        joined = ", ".join(matrix_ids) if matrix_ids else "none"
        lines.append(f"- {category}_missing_matrix_ids: `{joined}`")
    lines.append(f"- formal gate requirements: `{len(manifest['formal_gate_requirements'])}`")
    for requirement in manifest["formal_gate_requirements"]:
        stage = requirement.get("responsible_stage_id") or "unmapped"
        lines.append(
            f"  - `{requirement.get('requirement_id')}`: status=`{requirement.get('status')}`, "
            f"responsible_stage=`{stage}`"
        )
    lines.append(f"- H02 acceptance requirements: `{len(manifest['h02_formal_acceptance_requirements'])}`")
    lines.append(f"- safety issues: `{manifest['safety_issue_count']}`")
    lines.extend(["", "This artifact is read-only and does not execute commands."])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
