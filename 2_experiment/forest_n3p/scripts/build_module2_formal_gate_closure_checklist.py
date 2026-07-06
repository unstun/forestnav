from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_formal_gate_closure_checklist")
DEFAULT_MISSING_ARTIFACTS = Path("0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json")
DEFAULT_FORMAL_GATE = Path("0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json")
DEFAULT_POST_PLAN = Path("0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json")
DEFAULT_SOURCE_FRESHNESS = Path("0_trials/module2_source_freshness_audit/source_freshness_audit.json")
DEFAULT_REMAINING_DELIVERABLES = Path(
    "0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json"
)
DEFAULT_PROTOCOL_LANE_STATUS = Path(
    "0_trials/module2_formal_gate_protocol_lane_status_report/protocol_lane_status_report.json"
)
DEFAULT_NEXT_ROUND_REQUIREMENTS = Path(
    "0_trials/module2_formal_gate_next_round_requirements/formal_gate_next_round_requirements.json"
)
REMOTE_POST_PLAN_STAGE_IDS = (
    "approved_remote_preflight",
    "gate3_remote_training",
    "gate3_remote_audit_pullback",
)


@dataclass(frozen=True)
class FormalGateClosureChecklistConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    missing_artifacts_path: Path = DEFAULT_MISSING_ARTIFACTS
    formal_gate_path: Path = DEFAULT_FORMAL_GATE
    post_plan_path: Path = DEFAULT_POST_PLAN
    source_freshness_path: Path = DEFAULT_SOURCE_FRESHNESS
    remaining_deliverables_path: Path = DEFAULT_REMAINING_DELIVERABLES
    protocol_lane_status_path: Path = DEFAULT_PROTOCOL_LANE_STATUS
    next_round_requirements_path: Path = DEFAULT_NEXT_ROUND_REQUIREMENTS


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = FormalGateClosureChecklistConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        missing_artifacts_path=args.missing_artifacts,
        formal_gate_path=args.formal_gate,
        post_plan_path=args.post_plan,
        source_freshness_path=args.source_freshness_audit,
        remaining_deliverables_path=args.remaining_deliverables,
        protocol_lane_status_path=args.protocol_lane_status_report,
        next_round_requirements_path=args.next_round_requirements,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "formal_gate_closure_checklist.json"
    markdown_out = config.markdown_out or output_dir / "formal_gate_closure_checklist.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: FormalGateClosureChecklistConfig) -> dict[str, Any]:
    missing_artifacts = _read_json(config.missing_artifacts_path)
    formal_gate = _read_json(config.formal_gate_path)
    post_plan = _read_json(config.post_plan_path)
    source_freshness = _read_json(config.source_freshness_path)
    remaining_deliverables = _read_json(config.remaining_deliverables_path)
    protocol_lane_status = _read_json(config.protocol_lane_status_path)
    next_round_requirements = _read_json(config.next_round_requirements_path)
    missing_groups = _missing_groups(missing_artifacts)
    checklist = _closure_checklist(
        missing_groups=missing_groups,
        formal_gate=formal_gate,
        post_plan=post_plan,
        protocol_lane_status=protocol_lane_status,
    )
    all_items_closed = all(item["complete"] for item in checklist)
    safety_issues = _input_safety_issues(
        missing_artifacts=missing_artifacts,
        formal_gate=formal_gate,
        post_plan=post_plan,
        source_freshness=source_freshness,
        remaining_deliverables=remaining_deliverables,
        protocol_lane_status=protocol_lane_status,
        next_round_requirements=next_round_requirements,
        all_items_closed=all_items_closed,
    )
    gate_status = str(formal_gate.get("status") or "")
    status = "formal_gate_closure_ready_for_result_audit" if all_items_closed and not safety_issues and gate_status == "formal_gate_ready_for_result_audit" else "formal_gate_closure_blocked"
    return {
        "schema_version": 1,
        "artifact_name": "module2_formal_gate_closure_checklist",
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
            "missing_artifacts": str(config.missing_artifacts_path),
            "formal_gate_gap_audit": str(config.formal_gate_path),
            "post_f02_6_regeneration_plan": str(config.post_plan_path),
            "source_freshness_audit": str(config.source_freshness_path),
            "formal_gate_remaining_deliverables": str(config.remaining_deliverables_path),
            "protocol_lane_status_report": str(config.protocol_lane_status_path),
            "formal_gate_next_round_requirements": str(config.next_round_requirements_path),
        },
        "current_gate_summary": {
            "formal_gate_status": formal_gate.get("status"),
            "missing_artifacts_status": missing_artifacts.get("status"),
            "post_plan_status": post_plan.get("status"),
            "source_freshness_status": source_freshness.get("status"),
            "missing_counts_by_category": missing_artifacts.get("missing_counts_by_category") if isinstance(missing_artifacts.get("missing_counts_by_category"), dict) else {},
            "formal_ordered_next_step_count": len(formal_gate.get("ordered_next_steps") if isinstance(formal_gate.get("ordered_next_steps"), list) else []),
            "post_plan_blocked_stage_ids": _post_plan_blocked_stage_ids(post_plan),
            "source_regeneration_target_count": len(source_freshness.get("ordered_regeneration_targets") if isinstance(source_freshness.get("ordered_regeneration_targets"), list) else []),
            "remaining_deliverables_gap_total_missing": _remaining_deliverables_gap_summary(remaining_deliverables)["total_missing_deliverables"],
            "remaining_deliverables_gap_open_category_count": _remaining_deliverables_gap_summary(remaining_deliverables)["open_category_count"],
            **_protocol_lane_current_summary(protocol_lane_status),
        },
        "closure_item_count": len(checklist),
        "open_item_count": sum(1 for item in checklist if not item["complete"]),
        "training_artifacts_required": _artifacts_for_category(missing_groups, "training"),
        "evaluation_artifacts_required": _artifacts_for_category(missing_groups, "evaluation"),
        "acceptance_artifacts_required": _artifacts_for_category(missing_groups, "acceptance"),
        "evaluation_acceptance_required": _artifacts_for_category(missing_groups, "evaluation_acceptance"),
        "claim_gate_artifacts_required": _artifacts_for_category(missing_groups, "claim_gate"),
        "post_plan_remote_stage_summary": _post_plan_remote_stage_summary(
            post_plan,
            protocol_lane_status=protocol_lane_status,
        ),
        "remaining_deliverables_gap_summary": _remaining_deliverables_gap_summary(remaining_deliverables),
        "post_plan_remaining_deliverables_gap_summary": _normalize_gap_summary(
            post_plan.get("remaining_deliverables_gap_summary")
        ),
        "next_round_requirements_summary": _next_round_requirements_summary(next_round_requirements),
        "closure_checklist": checklist,
        "input_safety_issue_count": len(safety_issues),
        "input_safety_issues": safety_issues,
        "claim_boundaries": [
            "This checklist is a formal-gate execution ledger, not a result table, paper appendix, or permission to train.",
            "It does not execute local commands, remote preflight, remote training, remote audit, sync, pullback, or evaluation.",
            "The only training item in the checklist remains gpu3070ti-relay-only and blocked until protocol-lane, contract, and source-fresh preflight gates close.",
            "A closed checklist is still not a paper claim unless H02 formal acceptance and claim safety pass after audited pullback hashes are recorded.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Module2 formal gate closure checklist without executing training or preflight.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--missing-artifacts", type=Path, default=DEFAULT_MISSING_ARTIFACTS)
    parser.add_argument("--formal-gate", type=Path, default=DEFAULT_FORMAL_GATE)
    parser.add_argument("--post-plan", type=Path, default=DEFAULT_POST_PLAN)
    parser.add_argument("--source-freshness-audit", type=Path, default=DEFAULT_SOURCE_FRESHNESS)
    parser.add_argument("--remaining-deliverables", type=Path, default=DEFAULT_REMAINING_DELIVERABLES)
    parser.add_argument("--protocol-lane-status-report", type=Path, default=DEFAULT_PROTOCOL_LANE_STATUS)
    parser.add_argument("--next-round-requirements", type=Path, default=DEFAULT_NEXT_ROUND_REQUIREMENTS)
    return parser.parse_args(list(argv) if argv is not None else None)


def _closure_checklist(
    *,
    missing_groups: Sequence[dict[str, Any]],
    formal_gate: dict[str, Any],
    post_plan: dict[str, Any],
    protocol_lane_status: dict[str, Any],
) -> list[dict[str, Any]]:
    groups = {str(group.get("group_id")): group for group in missing_groups}
    ordered_next_steps = {
        str(step.get("step_id")): step
        for step in formal_gate.get("ordered_next_steps", ())
        if isinstance(step, dict)
    }
    post_stages = {
        str(stage.get("stage_id")): stage
        for stage in post_plan.get("ordered_stages", ())
        if isinstance(stage, dict)
    }
    protocol_pending = _protocol_lane_pending(protocol_lane_status)
    protocol_blockers = ["protocol_lane_decision_pending"] if protocol_pending else []
    return [
        _item(
            checklist_id="protocol_lane_decision",
            phase="decision",
            group=None,
            formal_step=None,
            post_stage=None,
            completion_signal="Dr Sun records selected_lane_id, failed Gate3 basis, rejected-lane rationales, evidence basis, and contract action.",
            next_action="Record protocol_lane_decision before contract drafting, remote preflight, remote training, formal claim, or paper result material.",
            extra_blockers=protocol_blockers,
        ),
        _item(
            checklist_id="F02.6_decision",
            phase="decision",
            group=groups.get("f02_6_decision_record"),
            formal_step=ordered_next_steps.get("F02.6"),
            post_stage=post_stages.get("f02_6_decision_record"),
            completion_signal="Dr Sun approved/rejected decision record is present and source-fresh.",
            next_action="Close the F02.6 warm-start decision record before any approved preflight.",
        ),
        _item(
            checklist_id="preflight_source_fresh_regeneration",
            phase="regeneration",
            group=groups.get("source_fresh_regeneration_targets"),
            formal_step=ordered_next_steps.get("remote_preflight"),
            post_stage=post_stages.get("regenerate_preflight_gate_artifacts"),
            completion_signal="All approved_remote_preflight source-fresh targets are regenerated from the current head.",
            next_action="Regenerate source freshness targets only after F02.6 is closed.",
            extra_blockers=protocol_blockers,
        ),
        _item(
            checklist_id="approved_remote_preflight_and_packet",
            phase="remote_preflight",
            group=groups.get("post_f02_6_ordered_stages"),
            formal_step=ordered_next_steps.get("remote_preflight"),
            post_stage=post_stages.get("approved_remote_preflight"),
            completion_signal="Approved gpu3070ti preflight passes and the remote execution packet becomes ready.",
            next_action="Run only the approved remote preflight path; do not train locally.",
            extra_blockers=protocol_blockers,
        ),
        _item(
            checklist_id="gate3_remote_training_outputs",
            phase="training",
            group=groups.get("remote_training_outputs"),
            formal_step=ordered_next_steps.get("gate3_remote_training"),
            post_stage=post_stages.get("gate3_remote_training"),
            completion_signal="Remote formal Gate3 PPO training returns final_model.zip, summary.json, and training_manifest.json.",
            next_action="Run formal PPO only on gpu3070ti-relay after the packet reports ready.",
            runs_training=True,
            host="gpu3070ti-relay",
            extra_blockers=protocol_blockers,
        ),
        _item(
            checklist_id="gate3_formal_eval_outputs",
            phase="evaluation",
            group=groups.get("gate3_evaluation_outputs"),
            formal_step=ordered_next_steps.get("gate3_remote_audit_pullback"),
            post_stage=post_stages.get("gate3_remote_audit_pullback"),
            completion_signal="Formal Gate3 eval CSV and summary are present in the pulled-back trial directory.",
            next_action="Audit and pull back evaluation outputs with the remote formal trial.",
            extra_blockers=protocol_blockers,
        ),
        _item(
            checklist_id="gate3_audit_pullback_hashes",
            phase="acceptance",
            group=groups.get("gate3_acceptance_pullback"),
            formal_step=ordered_next_steps.get("gate3_remote_audit_pullback"),
            post_stage=post_stages.get("gate3_remote_audit_pullback"),
            completion_signal="Trial manifest, formal audit, and checkpoint SHA-256 record are present.",
            next_action="Record pullback hashes before any H01/H02 or claim gate regeneration.",
            extra_blockers=protocol_blockers,
        ),
        _item(
            checklist_id="h01_h02_formal_acceptance",
            phase="evaluation_acceptance",
            group=groups.get("h01_h02_formal_evaluation_acceptance"),
            formal_step=ordered_next_steps.get("h01_h02_regeneration"),
            post_stage=post_stages.get("regenerate_h01_h02_formal_artifacts"),
            completion_signal="H01 exposes the formal run command and H02 accepts formal-scale PPO outputs.",
            next_action="Regenerate H01/H02 after audited checkpoint pullback, not before.",
            extra_blockers=protocol_blockers,
        ),
        _item(
            checklist_id="claim_gate_regeneration",
            phase="claim_gate",
            group=groups.get("claim_gate_regeneration"),
            formal_step=ordered_next_steps.get("claim_safety_final_gate"),
            post_stage=post_stages.get("regenerate_claim_gate_artifacts"),
            completion_signal="Claim safety, missing-artifacts inventory, and paper readiness are regenerated after H02 acceptance.",
            next_action="Only then can formal result writing be considered; this checklist itself does not allow claims.",
            extra_blockers=protocol_blockers,
        ),
    ]


def _item(
    *,
    checklist_id: str,
    phase: str,
    group: dict[str, Any] | None,
    formal_step: dict[str, Any] | None,
    post_stage: dict[str, Any] | None,
    completion_signal: str,
    next_action: str,
    runs_training: bool = False,
    host: str | None = None,
    extra_blockers: Sequence[str] = (),
) -> dict[str, Any]:
    group = group or {}
    required_items = _group_items(group)
    missing_items = [item for item in required_items if item.get("missing")]
    formal_blockers = _strings((formal_step or {}).get("blocked_by"))
    post_blockers = _strings((post_stage or {}).get("blocked_by"))
    blocked_by = _unique(_strings(group.get("blocked_by")) + formal_blockers + post_blockers + list(extra_blockers))
    formal_step_complete = (formal_step or {}).get("status") == "complete"
    if formal_step_complete and not extra_blockers:
        missing_items = []
        blocked_by = []
    complete = (formal_step_complete and not extra_blockers) or (
        bool(group.get("complete")) and not missing_items and not blocked_by
    )
    return {
        "checklist_id": checklist_id,
        "phase": phase,
        "status": "complete" if complete else "blocked",
        "complete": complete,
        "runs_training": bool(runs_training),
        "host": host,
        "group_id": group.get("group_id"),
        "formal_step_status": (formal_step or {}).get("status"),
        "post_plan_stage_status": (post_stage or {}).get("status"),
        "blocked_by": blocked_by,
        "missing_item_count": len(missing_items),
        "required_items": required_items,
        "completion_signal": completion_signal,
        "next_action": next_action,
    }


def _missing_groups(missing_artifacts: dict[str, Any]) -> list[dict[str, Any]]:
    groups = missing_artifacts.get("missing_evidence_groups")
    if not isinstance(groups, list):
        return []
    return [group for group in groups if isinstance(group, dict)]


def _group_items(group: dict[str, Any]) -> list[dict[str, Any]]:
    items = group.get("items")
    if not isinstance(items, list):
        return []
    out = []
    for item in items:
        if not isinstance(item, dict):
            continue
        out.append(
            {
                "artifact_id": item.get("artifact_id"),
                "path": item.get("path"),
                "exists": bool(item.get("exists")),
                "state": item.get("state"),
                "missing": bool(item.get("missing")),
                "reason": item.get("reason"),
            }
        )
    return out


def _artifacts_for_category(groups: Sequence[dict[str, Any]], category: str) -> list[dict[str, Any]]:
    artifacts: list[dict[str, Any]] = []
    for group in groups:
        if str(group.get("category")) != category:
            continue
        artifacts.extend(_group_items(group))
    return artifacts


def _input_safety_issues(
    *,
    missing_artifacts: dict[str, Any],
    formal_gate: dict[str, Any],
    post_plan: dict[str, Any],
    source_freshness: dict[str, Any],
    remaining_deliverables: dict[str, Any],
    protocol_lane_status: dict[str, Any],
    next_round_requirements: dict[str, Any],
    all_items_closed: bool,
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for name, payload in (
        ("missing_artifacts", missing_artifacts),
        ("formal_gate", formal_gate),
        ("post_plan", post_plan),
        ("source_freshness", source_freshness),
        ("remaining_deliverables", remaining_deliverables),
        ("protocol_lane_status", protocol_lane_status),
        ("next_round_requirements", next_round_requirements),
    ):
        if payload.get("executes_commands") is True:
            issues.append(_issue(f"{name}_executes_commands", f"{name} must be read-only for closure checklist input."))
        if payload.get("runs_training") is True:
            issues.append(_issue(f"{name}_runs_training", f"{name} must not run training as checklist input."))
        if payload.get("runs_remote_preflight") is True:
            issues.append(_issue(f"{name}_runs_remote_preflight", f"{name} must not run remote preflight as checklist input."))
        if payload.get("local_training_allowed") is True:
            issues.append(_issue(f"{name}_allows_local_training", f"{name} must preserve local-training prohibition."))
        if payload.get("formal_claim_allowed") is True:
            issues.append(_issue(f"{name}_allows_formal_claim", f"{name} must not allow formal claims."))
    issues.extend(
        _post_plan_remote_stage_safety_issues(
            post_plan,
            protocol_lane_status=protocol_lane_status,
        )
    )
    issues.extend(
        _remaining_deliverables_gap_issues(
            remaining_deliverables=remaining_deliverables,
            post_plan=post_plan,
            all_items_closed=all_items_closed,
        )
    )
    return _unique_issues(issues)


def _remaining_deliverables_gap_issues(
    *,
    remaining_deliverables: dict[str, Any],
    post_plan: dict[str, Any],
    all_items_closed: bool,
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    ledger_gap = _remaining_deliverables_gap_summary(remaining_deliverables)
    post_plan_gap = _normalize_gap_summary(post_plan.get("remaining_deliverables_gap_summary"))
    if not ledger_gap["present"]:
        issues.append(_issue("remaining_deliverables_gap_summary_missing", "remaining-deliverables ledger must expose deliverable_gap_summary."))
    else:
        if ledger_gap["execution_boundary"] != "read_only_no_execution":
            issues.append(_issue("remaining_deliverables_gap_summary_execution_boundary_invalid", "remaining-deliverables gap summary must be read-only."))
        if ledger_gap["not_paper_result_material"] is not True:
            issues.append(_issue("remaining_deliverables_gap_summary_marked_as_paper_result", "remaining-deliverables gap summary must not be paper result material."))
    if not post_plan_gap["present"]:
        issues.append(_issue("post_plan_missing_remaining_deliverables_gap_summary", "post-plan must expose remaining_deliverables_gap_summary."))
    if ledger_gap["present"] and post_plan_gap["present"] and _gap_signature(ledger_gap) != _gap_signature(post_plan_gap):
        issues.append(_issue("post_plan_remaining_deliverables_gap_summary_mismatch", "post-plan gap summary must match the remaining-deliverables ledger."))
    if all_items_closed and _gap_open(ledger_gap):
        issues.append(_issue("closure_ready_with_remaining_deliverables_gap_open", "closure checklist cannot be ready while remaining-deliverables gaps are open."))
    return issues


def _post_plan_blocked_stage_ids(post_plan: dict[str, Any]) -> list[str]:
    summary = post_plan.get("blocking_summary") if isinstance(post_plan.get("blocking_summary"), dict) else {}
    blocked = summary.get("blocked_stage_ids")
    if isinstance(blocked, list):
        return [str(item) for item in blocked if item]
    return []


def _post_plan_remote_stage_summary(
    post_plan: dict[str, Any],
    *,
    protocol_lane_status: dict[str, Any] | None = None,
) -> dict[str, dict[str, Any]]:
    stages = {
        str(stage.get("stage_id")): stage
        for stage in post_plan.get("ordered_stages", ())
        if isinstance(stage, dict)
    }
    protocol_pending = _protocol_lane_pending(protocol_lane_status or {})
    summary: dict[str, dict[str, Any]] = {}
    for stage_id in REMOTE_POST_PLAN_STAGE_IDS:
        stage = stages.get(stage_id, {})
        raw_allowed_now = stage.get("allowed_now") if isinstance(stage.get("allowed_now"), bool) else None
        blocked_by = _strings(stage.get("blocked_by"))
        if protocol_pending and (stage.get("runs_training") is True or stage.get("runs_remote_preflight") is True):
            blocked_by = _unique(blocked_by + ["protocol_lane_decision_pending"])
        allowed_now = False if protocol_pending and stage_id in {"approved_remote_preflight", "gate3_remote_training"} else raw_allowed_now
        summary[stage_id] = {
            "present": bool(stage),
            "status": stage.get("status"),
            "raw_allowed_now": raw_allowed_now,
            "allowed_now": allowed_now,
            "vetoed_by_protocol_lane": bool(protocol_pending and raw_allowed_now is True),
            "runs_training": stage.get("runs_training") if isinstance(stage.get("runs_training"), bool) else None,
            "runs_remote_preflight": stage.get("runs_remote_preflight") if isinstance(stage.get("runs_remote_preflight"), bool) else None,
            "host": stage.get("host"),
            "blocked_by": blocked_by,
        }
    return summary


def _post_plan_remote_stage_safety_issues(
    post_plan: dict[str, Any],
    *,
    protocol_lane_status: dict[str, Any],
) -> list[dict[str, str]]:
    summary = _post_plan_remote_stage_summary(post_plan, protocol_lane_status=protocol_lane_status)
    issues: list[dict[str, str]] = []
    for stage_id, stage in summary.items():
        if not stage["present"]:
            issues.append(_issue(f"post_plan_missing_{stage_id}", f"post plan must include remote stage {stage_id}."))
            continue
        if stage["allowed_now"] is False and not stage["blocked_by"]:
            issues.append(_issue(f"post_plan_{stage_id}_missing_blocked_by", f"disabled post-plan stage {stage_id} must explain blocked_by."))
        if stage["allowed_now"] is True and stage["blocked_by"]:
            issues.append(_issue(f"post_plan_{stage_id}_allowed_with_blockers", f"allowed post-plan stage {stage_id} must not carry blocked_by."))
    training = summary.get("gate3_remote_training", {})
    if training.get("runs_training") is not True:
        issues.append(_issue("post_plan_training_stage_not_marked_training", "gate3_remote_training must remain marked as the training stage."))
    for stage_id in ("approved_remote_preflight", "gate3_remote_audit_pullback"):
        if summary.get(stage_id, {}).get("runs_training") is True:
            issues.append(_issue(f"post_plan_{stage_id}_claims_training", f"{stage_id} must not be marked as training."))
    preflight = summary.get("approved_remote_preflight", {})
    if preflight.get("runs_remote_preflight") is not True:
        issues.append(_issue("post_plan_preflight_stage_not_marked_preflight", "approved_remote_preflight must remain marked as a remote preflight stage."))
    for stage_id, stage in summary.items():
        if (stage.get("runs_training") is True or stage.get("runs_remote_preflight") is True) and stage.get("host") != "gpu3070ti-relay":
            issues.append(_issue(f"post_plan_{stage_id}_wrong_host", f"{stage_id} must run only on gpu3070ti-relay."))
    return issues


def _protocol_lane_current(protocol_lane_status: dict[str, Any]) -> dict[str, Any]:
    current = protocol_lane_status.get("current_status")
    return current if isinstance(current, dict) else {}


def _protocol_lane_pending(protocol_lane_status: dict[str, Any]) -> bool:
    current = _protocol_lane_current(protocol_lane_status)
    return (
        protocol_lane_status.get("status") == "protocol_lane_status_blocked_pending_lane_decision"
        or current.get("decision_record_status") == "pending_protocol_lane_decision"
        or current.get("next_blocked_lane") == "protocol_lane_decision"
    )


def _protocol_lane_current_summary(protocol_lane_status: dict[str, Any]) -> dict[str, Any]:
    current = _protocol_lane_current(protocol_lane_status)
    return {
        "protocol_lane_status": protocol_lane_status.get("status"),
        "protocol_lane_pending": _protocol_lane_pending(protocol_lane_status),
        "protocol_lane_next_blocked_lane": current.get("next_blocked_lane"),
        "protocol_lane_decision_record_status": current.get("decision_record_status"),
        "protocol_lane_selected_lane_id": current.get("selected_lane_id"),
        "protocol_lane_contract_drafting_allowed_now": current.get("contract_drafting_allowed_now"),
        "protocol_lane_remote_training_allowed_now": current.get("remote_training_allowed_now"),
        "protocol_lane_allowed_next_action_ids": _strings(current.get("allowed_next_action_ids")),
        "protocol_lane_blocked_action_ids": _strings(current.get("blocked_action_ids")),
    }


def _next_round_requirements_summary(next_round_requirements: dict[str, Any]) -> dict[str, Any]:
    permissions = (
        next_round_requirements.get("permissions_now")
        if isinstance(next_round_requirements.get("permissions_now"), dict)
        else {}
    )
    requirements = (
        next_round_requirements.get("next_round_requirements")
        if isinstance(next_round_requirements.get("next_round_requirements"), dict)
        else {}
    )
    rows = requirements.get("rows") if isinstance(requirements.get("rows"), list) else []
    return {
        "status": next_round_requirements.get("status"),
        "requirements_status": requirements.get("status"),
        "requirement_count": int(requirements.get("requirement_count") or 0),
        "local_training_allowed_now": permissions.get("local_training_allowed_now"),
        "remote_preflight_allowed_now": permissions.get("remote_preflight_allowed_now"),
        "new_success_training_allowed_now": permissions.get("new_success_training_allowed_now"),
        "new_or_revised_contract_required_before_new_success_training": permissions.get(
            "new_or_revised_contract_required_before_new_success_training"
        ),
        "execution_veto_reason": permissions.get("execution_veto_reason"),
        "rows": [
            {
                "category": row.get("category"),
                "requirement_id": row.get("requirement_id"),
                "status": row.get("status"),
                "required_before": row.get("required_before"),
            }
            for row in rows
            if isinstance(row, dict)
        ],
    }


def _remaining_deliverables_gap_summary(remaining_deliverables: dict[str, Any]) -> dict[str, Any]:
    return _normalize_gap_summary(remaining_deliverables.get("deliverable_gap_summary"))


def _normalize_gap_summary(raw: Any) -> dict[str, Any]:
    summary = raw if isinstance(raw, dict) else {}
    categories = _normalize_gap_categories(summary.get("categories"))
    return {
        "present": bool(summary),
        "summary_id": summary.get("summary_id"),
        "execution_boundary": summary.get("execution_boundary"),
        "not_paper_result_material": summary.get("not_paper_result_material"),
        "total_missing_deliverables": int(summary.get("total_missing_deliverables") or 0),
        "open_category_count": int(summary.get("open_category_count") or 0),
        "category_order": [str(item) for item in summary.get("category_order", []) if item]
        if isinstance(summary.get("category_order"), list)
        else list(categories),
        "categories": categories,
    }


def _normalize_gap_categories(raw_categories: Any) -> dict[str, dict[str, Any]]:
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


def _gap_open(summary: dict[str, Any]) -> bool:
    return int(summary.get("total_missing_deliverables") or 0) > 0 or int(summary.get("open_category_count") or 0) > 0


def _strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _issue(issue_id: str, message: str) -> dict[str, str]:
    return {"issue_id": issue_id, "message": message}


def _unique(items: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def _unique_issues(issues: Sequence[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    out: list[dict[str, str]] = []
    for issue in issues:
        issue_id = issue.get("issue_id") or ""
        if not issue_id or issue_id in seen:
            continue
        seen.add(issue_id)
        out.append(issue)
    return out


def _read_json(path: Path) -> dict[str, Any]:
    if not Path(path).is_file():
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _source_head() -> str:
    return module2_source_head()


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 Formal Gate Closure Checklist",
        "",
        "This file is a formal-gate closure checklist. It does not execute commands, train, preflight, audit, pull back artifacts, or write paper results.",
        "",
        f"- status: `{manifest['status']}`",
        f"- closure_item_count: `{manifest['closure_item_count']}`",
        f"- open_item_count: `{manifest['open_item_count']}`",
        f"- input_safety_issue_count: `{manifest['input_safety_issue_count']}`",
        f"- runs_training: `{manifest['runs_training']}`",
        f"- runs_remote_preflight: `{manifest['runs_remote_preflight']}`",
        f"- formal_claim_allowed: `{manifest['formal_claim_allowed']}`",
        "",
        "## Current Gate Summary",
        "",
    ]
    for key, value in manifest["current_gate_summary"].items():
        lines.append(f"- {key}: `{value}`")
    gap = manifest["remaining_deliverables_gap_summary"]
    lines.extend(
        [
            "",
            "## Remaining Deliverables Gap Summary",
            "",
            f"- total_missing_deliverables: `{gap['total_missing_deliverables']}`",
            f"- open_category_count: `{gap['open_category_count']}`",
        ]
    )
    for category in gap["category_order"]:
        item = gap["categories"].get(category, {})
        lines.append(
            f"- `{category}`: missing=`{item.get('missing_count')}`, "
            f"responsible_stage=`{item.get('responsible_stage_id')}`"
        )
    next_round = manifest["next_round_requirements_summary"]
    lines.extend(
        [
            "",
            "## Protocol Lane And Next-Round Gate",
            "",
            f"- protocol_lane_status: `{manifest['current_gate_summary'].get('protocol_lane_status')}`",
            f"- protocol_lane_pending: `{manifest['current_gate_summary'].get('protocol_lane_pending')}`",
            f"- protocol_lane_selected_lane_id: `{manifest['current_gate_summary'].get('protocol_lane_selected_lane_id')}`",
            "- protocol_lane_allowed_next_action_ids: "
            f"`{', '.join(manifest['current_gate_summary'].get('protocol_lane_allowed_next_action_ids', []))}`",
            "- protocol_lane_blocked_action_ids: "
            f"`{', '.join(manifest['current_gate_summary'].get('protocol_lane_blocked_action_ids', []))}`",
            f"- next_round_requirements_status: `{next_round['requirements_status']}`",
            f"- new_success_training_allowed_now: `{next_round['new_success_training_allowed_now']}`",
            "- new_or_revised_contract_required_before_new_success_training: "
            f"`{next_round['new_or_revised_contract_required_before_new_success_training']}`",
            f"- execution_veto_reason: `{next_round['execution_veto_reason']}`",
            "",
            "### Next-Round Requirement Rows",
            "",
        ]
    )
    for row in next_round["rows"]:
        lines.append(
            f"- `{row['category']}:{row['requirement_id']}`: status=`{row['status']}`, "
            f"required_before=`{row['required_before']}`"
        )
    lines.extend(["", "## Closure Checklist", ""])
    for item in manifest["closure_checklist"]:
        host = f", host=`{item['host']}`" if item.get("host") else ""
        lines.append(
            f"- `{item['checklist_id']}` ({item['phase']}): status=`{item['status']}`, "
            f"missing=`{item['missing_item_count']}`, runs_training=`{item['runs_training']}`{host}"
        )
        if item["blocked_by"]:
            lines.append(f"  - blocked_by: `{', '.join(item['blocked_by'])}`")
        lines.append(f"  - completion_signal: {item['completion_signal']}")
        lines.append(f"  - next_action: {item['next_action']}")
    lines.extend(["", "## Required Training Artifacts", ""])
    _append_artifacts(lines, manifest["training_artifacts_required"])
    lines.extend(["", "## Required Evaluation Artifacts", ""])
    _append_artifacts(lines, manifest["evaluation_artifacts_required"])
    lines.extend(["", "## Required Acceptance Artifacts", ""])
    _append_artifacts(lines, manifest["acceptance_artifacts_required"])
    lines.extend(["", "## Post-Plan Remote Stages", ""])
    for stage_id, stage in manifest["post_plan_remote_stage_summary"].items():
        blocked_by = ", ".join(stage["blocked_by"]) if stage["blocked_by"] else "none"
        lines.append(
            f"- `{stage_id}`: present=`{stage['present']}`, raw_allowed_now=`{stage['raw_allowed_now']}`, "
            f"allowed_now=`{stage['allowed_now']}`, vetoed_by_protocol_lane=`{stage['vetoed_by_protocol_lane']}`, "
            f"runs_training=`{stage['runs_training']}`, runs_remote_preflight=`{stage['runs_remote_preflight']}`, "
            f"host=`{stage['host']}`, blocked_by=`{blocked_by}`"
        )
    lines.extend(["", "## Input Safety Issues", ""])
    if manifest["input_safety_issues"]:
        lines.extend(f"- `{issue['issue_id']}`: {issue['message']}" for issue in manifest["input_safety_issues"])
    else:
        lines.append("- none")
    lines.extend(["", "## Claim Boundaries", ""])
    lines.extend(f"- {item}" for item in manifest["claim_boundaries"])
    return "\n".join(lines) + "\n"


def _append_artifacts(lines: list[str], artifacts: Sequence[dict[str, Any]]) -> None:
    if not artifacts:
        lines.append("- none")
        return
    for artifact in artifacts:
        lines.append(
            f"- `{artifact.get('artifact_id')}`: missing=`{artifact.get('missing')}`, "
            f"path=`{artifact.get('path')}`"
        )


if __name__ == "__main__":
    raise SystemExit(main())
