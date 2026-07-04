from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_formal_gate_status_report")
DEFAULT_FORMAL_GATE = Path("0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json")
DEFAULT_MISSING_ARTIFACTS = Path("0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json")
DEFAULT_CLOSURE_CHECKLIST = Path("0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json")
DEFAULT_DECISION_RECORD = Path("0_trials/module2_f02_6_decision_record/f02_6_decision_record.json")
DEFAULT_REMOTE_PACKET = Path("0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json")
DEFAULT_H01_MANIFEST = Path("0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json")
DEFAULT_H02_ACCEPTANCE = Path("0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json")
DEFAULT_CLAIM_SAFETY = Path("0_trials/module2_claim_safety/module2_claim_safety.json")
DEFAULT_PAPER_READINESS = Path("0_trials/module2_paper_readiness/module2_paper_readiness.json")
DEFAULT_HANDOFF_BUNDLE = Path("0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json")
REMOTE_EXECUTION_STEP_IDS = (
    "sync_to_remote",
    "run_remote_preflight",
    "run_remote_training",
    "run_remote_audit",
)
CLOSURE_REMOTE_STAGE_IDS = (
    "approved_remote_preflight",
    "gate3_remote_training",
    "gate3_remote_audit_pullback",
)


@dataclass(frozen=True)
class FormalGateStatusReportConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    formal_gate_path: Path = DEFAULT_FORMAL_GATE
    missing_artifacts_path: Path = DEFAULT_MISSING_ARTIFACTS
    closure_checklist_path: Path = DEFAULT_CLOSURE_CHECKLIST
    decision_record_path: Path = DEFAULT_DECISION_RECORD
    remote_packet_path: Path = DEFAULT_REMOTE_PACKET
    h01_manifest_path: Path = DEFAULT_H01_MANIFEST
    h02_acceptance_path: Path = DEFAULT_H02_ACCEPTANCE
    claim_safety_path: Path = DEFAULT_CLAIM_SAFETY
    paper_readiness_path: Path = DEFAULT_PAPER_READINESS
    handoff_bundle_path: Path = DEFAULT_HANDOFF_BUNDLE


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = FormalGateStatusReportConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        formal_gate_path=args.formal_gate,
        missing_artifacts_path=args.missing_artifacts,
        closure_checklist_path=args.closure_checklist,
        decision_record_path=args.decision_record,
        remote_packet_path=args.remote_packet,
        h01_manifest_path=args.h01_manifest,
        h02_acceptance_path=args.h02_acceptance,
        claim_safety_path=args.claim_safety,
        paper_readiness_path=args.paper_readiness,
        handoff_bundle_path=args.handoff_bundle,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "formal_gate_status_report.json"
    markdown_out = config.markdown_out or output_dir / "formal_gate_status_report.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: FormalGateStatusReportConfig) -> dict[str, Any]:
    formal_gate = _read_json(config.formal_gate_path)
    missing_artifacts = _read_json(config.missing_artifacts_path)
    closure_checklist = _read_json(config.closure_checklist_path)
    decision = _read_json(config.decision_record_path)
    remote_packet = _read_json(config.remote_packet_path)
    h01 = _read_json(config.h01_manifest_path)
    h02 = _read_json(config.h02_acceptance_path)
    claim_safety = _read_json(config.claim_safety_path)
    paper_readiness = _read_json(config.paper_readiness_path)
    handoff_bundle = _read_json(config.handoff_bundle_path)
    remote_execution_steps = _remote_execution_step_summary(remote_packet)
    closure_remote_stages = _closure_remote_stage_summary(closure_checklist)
    handoff_summary = _handoff_bundle_summary(handoff_bundle)

    input_safety_issues = _input_safety_issues(
        {
            "formal_gate": formal_gate,
            "missing_artifacts": missing_artifacts,
            "closure_checklist": closure_checklist,
            "decision_record": decision,
            "remote_packet": remote_packet,
            "h01_manifest": h01,
            "h02_acceptance": h02,
            "claim_safety": claim_safety,
            "paper_readiness": paper_readiness,
            "handoff_bundle": handoff_bundle,
        }
    )
    lanes = _lanes(
        formal_gate=formal_gate,
        missing_artifacts=missing_artifacts,
        closure_checklist=closure_checklist,
        decision=decision,
        remote_packet=remote_packet,
        h01=h01,
        h02=h02,
        claim_safety=claim_safety,
        paper_readiness=paper_readiness,
    )
    permissions = _permissions(
        formal_gate=formal_gate,
        closure_checklist=closure_checklist,
        decision=decision,
        remote_packet=remote_packet,
        h01=h01,
        h02=h02,
        claim_safety=claim_safety,
        paper_readiness=paper_readiness,
        input_safety_issues=input_safety_issues,
    )
    ready = all(lane["status"] == "complete" for lane in lanes) and not input_safety_issues and permissions["formal_claim_allowed_now"]
    return {
        "schema_version": 1,
        "artifact_name": "module2_formal_gate_status_report",
        "status": "formal_gate_status_ready_for_claim_audit" if ready else "formal_gate_status_blocked",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "inputs": {
            "formal_gate_gap_audit": str(config.formal_gate_path),
            "formal_gate_missing_artifacts": str(config.missing_artifacts_path),
            "formal_gate_closure_checklist": str(config.closure_checklist_path),
            "f02_6_decision_record": str(config.decision_record_path),
            "remote_formal_execution_packet": str(config.remote_packet_path),
            "h01_manifest": str(config.h01_manifest_path),
            "h02_formal_acceptance": str(config.h02_acceptance_path),
            "claim_safety": str(config.claim_safety_path),
            "paper_readiness": str(config.paper_readiness_path),
            "formal_gate_handoff_bundle": str(config.handoff_bundle_path),
        },
        "current_state": {
            "decision_status": decision.get("status"),
            "decision_decider": decision.get("decider"),
            "formal_gate_status": formal_gate.get("status"),
            "missing_artifacts_status": missing_artifacts.get("status"),
            "closure_checklist_status": closure_checklist.get("status"),
            "closure_open_item_count": closure_checklist.get("open_item_count"),
            "closure_remote_preflight_allowed_now": closure_remote_stages["approved_remote_preflight"]["allowed_now"],
            "closure_remote_training_allowed_now": closure_remote_stages["gate3_remote_training"]["allowed_now"],
            "closure_remote_audit_pullback_allowed_now": closure_remote_stages["gate3_remote_audit_pullback"]["allowed_now"],
            "remote_packet_status": remote_packet.get("status"),
            "ready_to_run_remote_training": remote_packet.get("ready_to_run_remote_training"),
            "remote_packet_sync_allowed_now": remote_execution_steps["sync_to_remote"]["allowed_now"],
            "remote_packet_preflight_allowed_now": remote_execution_steps["run_remote_preflight"]["allowed_now"],
            "remote_packet_training_allowed_now": remote_execution_steps["run_remote_training"]["allowed_now"],
            "remote_packet_audit_allowed_now": remote_execution_steps["run_remote_audit"]["allowed_now"],
            "h01_status": h01.get("status"),
            "h02_status": h02.get("status"),
            "h02_formal_output_accepted": h02.get("formal_output_accepted"),
            "claim_safety_status": claim_safety.get("status"),
            "claim_safety_formal_performance_claim_allowed": claim_safety.get("formal_performance_claim_allowed"),
            "paper_readiness_status": paper_readiness.get("status"),
            "paper_readiness_formal_results_ready": paper_readiness.get("formal_results_ready"),
            "handoff_bundle_status": handoff_bundle.get("status"),
            "handoff_bundle_next_action": handoff_summary["next_handoff_action_id"],
            "handoff_bundle_safety_issue_count": handoff_summary["safety_issue_count"],
            "handoff_bundle_remote_training_allowed_now": handoff_summary["remote_training_allowed_now"],
        },
        "permissions_now": permissions,
        "missing_counts_by_category": missing_artifacts.get("missing_counts_by_category") if isinstance(missing_artifacts.get("missing_counts_by_category"), dict) else {},
        "training_artifacts_required": _artifact_list(closure_checklist, "training_artifacts_required"),
        "evaluation_artifacts_required": _artifact_list(closure_checklist, "evaluation_artifacts_required"),
        "acceptance_artifacts_required": _artifact_list(closure_checklist, "acceptance_artifacts_required"),
        "evaluation_acceptance_required": _artifact_list(closure_checklist, "evaluation_acceptance_required"),
        "claim_gate_artifacts_required": _artifact_list(closure_checklist, "claim_gate_artifacts_required"),
        "closure_remote_stage_summary": closure_remote_stages,
        "remote_execution_step_summary": remote_execution_steps,
        "formal_gate_handoff_summary": handoff_summary,
        "formal_gate_lanes": lanes,
        "next_blocked_lane": _next_blocked_lane(lanes),
        "input_safety_issue_count": len(input_safety_issues),
        "input_safety_issues": input_safety_issues,
        "safe_work_without_f02_6_decision": [
            "Maintain or harden read-only gate artifacts.",
            "Add tests for gate ordering, artifact inventory, and claim blocking.",
            "Do not run approved remote preflight, formal PPO training, H02 formal evaluation, pullback, or result-claim writing.",
        ],
        "claim_boundaries": [
            "This status report is an execution-orientation artifact, not a result table or paper appendix.",
            "It does not execute commands, remote preflight, training, evaluation, sync, audit, or pullback.",
            "It must not be used to approve F02.6; only Dr Sun's decision record can do that.",
            "Formal PPO training remains gpu3070ti-relay-only and blocked until F02.6, source freshness, and remote packet gates close.",
            "Formal result writing remains blocked until H02 acceptance, claim safety, paper readiness, and the closure checklist all pass after audited pullback hashes.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a read-only Module2 formal gate status report.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--formal-gate", type=Path, default=DEFAULT_FORMAL_GATE)
    parser.add_argument("--missing-artifacts", type=Path, default=DEFAULT_MISSING_ARTIFACTS)
    parser.add_argument("--closure-checklist", type=Path, default=DEFAULT_CLOSURE_CHECKLIST)
    parser.add_argument("--decision-record", type=Path, default=DEFAULT_DECISION_RECORD)
    parser.add_argument("--remote-packet", type=Path, default=DEFAULT_REMOTE_PACKET)
    parser.add_argument("--h01-manifest", type=Path, default=DEFAULT_H01_MANIFEST)
    parser.add_argument("--h02-acceptance", type=Path, default=DEFAULT_H02_ACCEPTANCE)
    parser.add_argument("--claim-safety", type=Path, default=DEFAULT_CLAIM_SAFETY)
    parser.add_argument("--paper-readiness", type=Path, default=DEFAULT_PAPER_READINESS)
    parser.add_argument("--handoff-bundle", type=Path, default=DEFAULT_HANDOFF_BUNDLE)
    return parser.parse_args(list(argv) if argv is not None else None)


def _permissions(
    *,
    formal_gate: dict[str, Any],
    closure_checklist: dict[str, Any],
    decision: dict[str, Any],
    remote_packet: dict[str, Any],
    h01: dict[str, Any],
    h02: dict[str, Any],
    claim_safety: dict[str, Any],
    paper_readiness: dict[str, Any],
    input_safety_issues: Sequence[dict[str, str]],
) -> dict[str, bool]:
    decision_closed = decision.get("status") in {"approved", "rejected"} and decision.get("decider") == "Dr Sun"
    approved = decision.get("status") == "approved" and decision.get("decider") == "Dr Sun"
    remote_ready = remote_packet.get("ready_to_run_remote_training") is True
    h01_ready = h01.get("status") == "ready_for_formal_run"
    h02_accepted = h02.get("formal_output_accepted") is True and h02.get("paper_result_input_allowed") is True
    claim_ready = claim_safety.get("formal_performance_claim_allowed") is True
    readiness_ready = paper_readiness.get("formal_results_ready") is True
    closure_ready = closure_checklist.get("status") == "formal_gate_closure_ready_for_result_audit"
    formal_gate_ready = formal_gate.get("status") == "formal_gate_ready_for_result_audit"
    safe = not input_safety_issues
    return {
        "f02_6_decision_closed": decision_closed,
        "warm_start_formal_chain_approved": approved,
        "remote_preflight_allowed_now": approved and safe,
        "remote_training_allowed_now": approved and remote_ready and safe,
        "formal_h01_evaluation_allowed_now": h01_ready and remote_ready and safe,
        "formal_h02_acceptance_allowed_now": h01_ready and h02_accepted and safe,
        "formal_claim_allowed_now": formal_gate_ready and closure_ready and h02_accepted and claim_ready and readiness_ready and safe,
        "local_training_allowed_now": False,
    }


def _lanes(
    *,
    formal_gate: dict[str, Any],
    missing_artifacts: dict[str, Any],
    closure_checklist: dict[str, Any],
    decision: dict[str, Any],
    remote_packet: dict[str, Any],
    h01: dict[str, Any],
    h02: dict[str, Any],
    claim_safety: dict[str, Any],
    paper_readiness: dict[str, Any],
) -> list[dict[str, Any]]:
    checklist = {
        str(item.get("checklist_id")): item
        for item in closure_checklist.get("closure_checklist", ())
        if isinstance(item, dict)
    }
    gate_steps = {
        str(step.get("step_id")): step
        for step in formal_gate.get("ordered_next_steps", ())
        if isinstance(step, dict)
    }
    groups = {
        str(group.get("group_id")): group
        for group in missing_artifacts.get("missing_evidence_groups", ())
        if isinstance(group, dict)
    }
    return [
        _lane(
            lane_id="decision",
            phase="decision",
            primary_status=str(decision.get("status") or "missing"),
            checklist_item=checklist.get("F02.6_decision"),
            formal_step=gate_steps.get("F02.6"),
            group=groups.get("f02_6_decision_record"),
            completion_signal="F02.6 decision record is approved or rejected by Dr Sun.",
            action_when_blocked="Record Dr Sun's F02.6 decision before any formal preflight or training.",
        ),
        _lane(
            lane_id="source_fresh_preflight",
            phase="regeneration",
            primary_status=str(missing_artifacts.get("current_gate_summary", {}).get("source_freshness_status") if isinstance(missing_artifacts.get("current_gate_summary"), dict) else "unknown"),
            checklist_item=checklist.get("preflight_source_fresh_regeneration"),
            formal_step=gate_steps.get("remote_preflight"),
            group=groups.get("source_fresh_regeneration_targets"),
            completion_signal="Source-fresh preflight targets are regenerated from the current head.",
            action_when_blocked="After F02.6 closes, regenerate source-fresh gate artifacts before approved preflight.",
        ),
        _lane(
            lane_id="remote_packet_preflight",
            phase="remote_preflight",
            primary_status=str(remote_packet.get("status") or "missing"),
            checklist_item=checklist.get("approved_remote_preflight_and_packet"),
            formal_step=gate_steps.get("remote_preflight"),
            group=groups.get("post_f02_6_ordered_stages"),
            completion_signal="Approved gpu3070ti preflight passes and remote packet reports ready.",
            action_when_blocked="Run only approved remote preflight after F02.6 and source freshness close.",
        ),
        _lane(
            lane_id="gate3_remote_training",
            phase="training",
            primary_status=str(gate_steps.get("gate3_remote_training", {}).get("status") or "missing"),
            checklist_item=checklist.get("gate3_remote_training_outputs"),
            formal_step=gate_steps.get("gate3_remote_training"),
            group=groups.get("remote_training_outputs"),
            completion_signal="final_model.zip, train summary, and training manifest are pulled back.",
            action_when_blocked="Run formal PPO only on gpu3070ti-relay after remote packet is ready.",
            runs_training=True,
            host="gpu3070ti-relay",
        ),
        _lane(
            lane_id="gate3_eval_and_audit_pullback",
            phase="acceptance",
            primary_status=str(gate_steps.get("gate3_remote_audit_pullback", {}).get("status") or "missing"),
            checklist_item=checklist.get("gate3_audit_pullback_hashes"),
            formal_step=gate_steps.get("gate3_remote_audit_pullback"),
            group=groups.get("gate3_acceptance_pullback"),
            extra_group=groups.get("gate3_evaluation_outputs"),
            completion_signal="Gate3 eval outputs, trial manifest, formal audit, and checkpoint hash are present.",
            action_when_blocked="Audit remote trial and pull back the complete trial directory with hashes.",
        ),
        _lane(
            lane_id="h01_h02_formal_evaluation",
            phase="evaluation_acceptance",
            primary_status=f"h01={h01.get('status')}; h02={h02.get('status')}",
            checklist_item=checklist.get("h01_h02_formal_acceptance"),
            formal_step=gate_steps.get("h01_h02_regeneration"),
            group=groups.get("h01_h02_formal_evaluation_acceptance"),
            completion_signal="H01 is ready and H02 accepts formal-scale PPO outputs.",
            action_when_blocked="Regenerate H01/H02 only after audited checkpoint pullback is complete.",
        ),
        _lane(
            lane_id="claim_gate",
            phase="claim_gate",
            primary_status=f"claim_safety={claim_safety.get('status')}; paper_readiness={paper_readiness.get('status')}",
            checklist_item=checklist.get("claim_gate_regeneration"),
            formal_step=gate_steps.get("claim_safety_final_gate"),
            group=groups.get("claim_gate_regeneration"),
            completion_signal="Claim safety and paper readiness allow formal results after H02 acceptance.",
            action_when_blocked="Regenerate claim gates only after H02 formal acceptance passes.",
        ),
    ]


def _lane(
    *,
    lane_id: str,
    phase: str,
    primary_status: str,
    checklist_item: dict[str, Any] | None,
    formal_step: dict[str, Any] | None,
    group: dict[str, Any] | None,
    completion_signal: str,
    action_when_blocked: str,
    extra_group: dict[str, Any] | None = None,
    runs_training: bool = False,
    host: str | None = None,
) -> dict[str, Any]:
    checklist_item = checklist_item or {}
    formal_step = formal_step or {}
    group = group or {}
    missing_items = _group_missing_items(group) + _group_missing_items(extra_group or {})
    blocked_by = _unique(
        _strings(group.get("blocked_by"))
        + _strings((extra_group or {}).get("blocked_by"))
        + _strings(formal_step.get("blocked_by"))
        + _strings(checklist_item.get("blocked_by"))
    )
    complete = checklist_item.get("complete") is True and not missing_items and not blocked_by
    return {
        "lane_id": lane_id,
        "phase": phase,
        "status": "complete" if complete else "blocked",
        "primary_status": primary_status,
        "runs_training": runs_training,
        "host": host,
        "blocked_by": blocked_by,
        "missing_item_count": len(missing_items),
        "missing_items": missing_items,
        "completion_signal": completion_signal,
        "action_when_blocked": action_when_blocked,
    }


def _input_safety_issues(named_payloads: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for name, payload in named_payloads.items():
        if payload.get("executes_commands") is True:
            issues.append(_issue(f"{name}_executes_commands", f"{name} must be read-only for status reporting."))
        if payload.get("runs_training") is True:
            issues.append(_issue(f"{name}_runs_training", f"{name} must not run training as status input."))
        if payload.get("runs_remote_preflight") is True:
            issues.append(_issue(f"{name}_runs_remote_preflight", f"{name} must not run remote preflight as status input."))
        if payload.get("local_training_allowed") is True:
            issues.append(_issue(f"{name}_allows_local_training", f"{name} must preserve the local-training prohibition."))
        if payload.get("formal_claim_allowed") is True:
            issues.append(_issue(f"{name}_allows_formal_claim", f"{name} must not allow formal claims through status reporting."))
        if name == "remote_packet" and payload.get("formal_claim_allowed_before_audit") is True:
            issues.append(_issue("remote_packet_allows_claim_before_audit", "remote packet must not allow claims before audit."))
        if name == "closure_checklist":
            issues.extend(_closure_remote_stage_safety_issues(payload))
        if name == "remote_packet":
            issues.extend(_remote_execution_step_safety_issues(payload))
        if name == "handoff_bundle":
            issues.extend(_handoff_bundle_safety_issues(payload))
    return _unique_issues(issues)


def _handoff_bundle_summary(handoff_bundle: dict[str, Any]) -> dict[str, Any]:
    permissions = handoff_bundle.get("permissions_now") if isinstance(handoff_bundle.get("permissions_now"), dict) else {}
    next_action = handoff_bundle.get("next_handoff_action") if isinstance(handoff_bundle.get("next_handoff_action"), dict) else {}
    steps = handoff_bundle.get("remote_execution_steps") if isinstance(handoff_bundle.get("remote_execution_steps"), dict) else {}
    step_summary: dict[str, dict[str, Any]] = {}
    for step_id in REMOTE_EXECUTION_STEP_IDS:
        step = steps.get(step_id) if isinstance(steps.get(step_id), dict) else {}
        step_summary[step_id] = {
            "present": bool(step),
            "allowed_now": step.get("allowed_now") if isinstance(step.get("allowed_now"), bool) else None,
            "runs_training": step.get("runs_training") if isinstance(step.get("runs_training"), bool) else None,
            "blocked_by": _strings(step.get("blocked_by")),
        }
    return {
        "present": bool(handoff_bundle),
        "status": handoff_bundle.get("status"),
        "next_handoff_action_id": next_action.get("action_id"),
        "next_action_requires_dr_sun": next_action.get("requires_dr_sun"),
        "safety_issue_count": int(handoff_bundle.get("safety_issue_count") or 0),
        "remote_training_allowed_now": bool(permissions.get("remote_training_allowed_now")),
        "remote_preflight_allowed_now": bool(permissions.get("remote_preflight_allowed_now")),
        "formal_claim_allowed_now": bool(permissions.get("formal_claim_allowed_now")),
        "remote_execution_steps": step_summary,
    }


def _handoff_bundle_safety_issues(handoff_bundle: dict[str, Any]) -> list[dict[str, str]]:
    if not handoff_bundle:
        return [_issue("handoff_bundle_missing", "formal gate status report must consume the handoff bundle.")]
    issues: list[dict[str, str]] = []
    summary = _handoff_bundle_summary(handoff_bundle)
    if summary["safety_issue_count"] > 0:
        issues.append(_issue("handoff_bundle_safety_issues_open", "handoff bundle reports open safety issues."))
    pending = handoff_bundle.get("current_state", {}).get("decision_status") == "pending_human_decision" if isinstance(handoff_bundle.get("current_state"), dict) else False
    if pending:
        for step_id, step in summary["remote_execution_steps"].items():
            if step["allowed_now"] is True:
                issues.append(_issue(f"handoff_bundle_pending_allows_{step_id}", "handoff bundle must not allow remote steps while F02.6 is pending."))
    if summary["remote_training_allowed_now"] and handoff_bundle.get("status") != "ready_for_manual_remote_execution_review":
        issues.append(_issue("handoff_bundle_training_allowed_without_ready_status", "handoff bundle remote training permission requires ready_for_manual_remote_execution_review."))
    training_step = summary["remote_execution_steps"].get("run_remote_training", {})
    if training_step.get("present") and training_step.get("runs_training") is not True:
        issues.append(_issue("handoff_bundle_training_step_not_marked_training", "handoff bundle run_remote_training must remain marked as training."))
    for step_id, step in summary["remote_execution_steps"].items():
        if step_id != "run_remote_training" and step.get("runs_training") is True:
            issues.append(_issue(f"handoff_bundle_{step_id}_claims_training", f"handoff bundle {step_id} must not be marked as training."))
    return issues


def _closure_remote_stage_summary(closure_checklist: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw = closure_checklist.get("post_plan_remote_stage_summary")
    stages = raw if isinstance(raw, dict) else {}
    summary: dict[str, dict[str, Any]] = {}
    for stage_id in CLOSURE_REMOTE_STAGE_IDS:
        stage = stages.get(stage_id) if isinstance(stages.get(stage_id), dict) else {}
        summary[stage_id] = {
            "present": bool(stage),
            "status": stage.get("status"),
            "allowed_now": stage.get("allowed_now") if isinstance(stage.get("allowed_now"), bool) else None,
            "runs_training": stage.get("runs_training") if isinstance(stage.get("runs_training"), bool) else None,
            "runs_remote_preflight": stage.get("runs_remote_preflight") if isinstance(stage.get("runs_remote_preflight"), bool) else None,
            "host": stage.get("host"),
            "blocked_by": _strings(stage.get("blocked_by")),
        }
    return summary


def _closure_remote_stage_safety_issues(closure_checklist: dict[str, Any]) -> list[dict[str, str]]:
    raw = closure_checklist.get("post_plan_remote_stage_summary")
    if not isinstance(raw, dict):
        return [_issue("closure_checklist_missing_remote_stage_summary", "closure checklist must expose post_plan_remote_stage_summary.")]
    summary = _closure_remote_stage_summary(closure_checklist)
    issues: list[dict[str, str]] = []
    for stage_id, stage in summary.items():
        if not stage["present"]:
            issues.append(_issue(f"closure_checklist_missing_{stage_id}", f"closure checklist missing remote stage {stage_id}."))
            continue
        if stage["allowed_now"] is False and not stage["blocked_by"]:
            issues.append(_issue(f"closure_checklist_{stage_id}_missing_blocked_by", f"disabled closure remote stage {stage_id} must explain blocked_by."))
        if stage["allowed_now"] is True and stage["blocked_by"]:
            issues.append(_issue(f"closure_checklist_{stage_id}_allowed_with_blockers", f"allowed closure remote stage {stage_id} must not carry blocked_by."))
    training = summary.get("gate3_remote_training", {})
    if training.get("runs_training") is not True:
        issues.append(_issue("closure_checklist_training_stage_not_marked_training", "gate3_remote_training must remain marked as training."))
    for stage_id in ("approved_remote_preflight", "gate3_remote_audit_pullback"):
        if summary.get(stage_id, {}).get("runs_training") is True:
            issues.append(_issue(f"closure_checklist_{stage_id}_claims_training", f"{stage_id} must not be marked as training."))
    preflight = summary.get("approved_remote_preflight", {})
    if preflight.get("runs_remote_preflight") is not True:
        issues.append(_issue("closure_checklist_preflight_stage_not_marked_preflight", "approved_remote_preflight must remain marked as remote preflight."))
    for stage_id, stage in summary.items():
        if (stage.get("runs_training") is True or stage.get("runs_remote_preflight") is True) and stage.get("host") != "gpu3070ti-relay":
            issues.append(_issue(f"closure_checklist_{stage_id}_wrong_host", f"{stage_id} must run only on gpu3070ti-relay."))
    return issues


def _remote_execution_step_summary(remote_packet: dict[str, Any]) -> dict[str, dict[str, Any]]:
    steps = remote_packet.get("execution_steps") if isinstance(remote_packet.get("execution_steps"), dict) else {}
    summary: dict[str, dict[str, Any]] = {}
    for step_id in REMOTE_EXECUTION_STEP_IDS:
        step = steps.get(step_id) if isinstance(steps.get(step_id), dict) else {}
        summary[step_id] = {
            "present": bool(step),
            "allowed_now": step.get("allowed_now") if isinstance(step.get("allowed_now"), bool) else None,
            "runs_training": step.get("runs_training") if isinstance(step.get("runs_training"), bool) else None,
            "blocked_by": _strings(step.get("blocked_by")),
        }
    return summary


def _remote_execution_step_safety_issues(remote_packet: dict[str, Any]) -> list[dict[str, str]]:
    steps = remote_packet.get("execution_steps")
    if not isinstance(steps, dict):
        return [_issue("remote_packet_missing_execution_steps", "remote packet must expose execution_steps for status reporting.")]
    issues: list[dict[str, str]] = []
    for step_id in REMOTE_EXECUTION_STEP_IDS:
        step = steps.get(step_id)
        if not isinstance(step, dict):
            issues.append(_issue(f"remote_packet_missing_{step_id}", f"remote packet missing execution step {step_id}."))
            continue
        blockers = _strings(step.get("blocked_by"))
        if step.get("allowed_now") is False and not blockers:
            issues.append(_issue(f"remote_packet_{step_id}_missing_blocked_by", f"disabled remote step {step_id} must explain blocked_by."))
        if step.get("allowed_now") is True and blockers:
            issues.append(_issue(f"remote_packet_{step_id}_allowed_with_blockers", f"allowed remote step {step_id} must not carry blocked_by."))
        if step_id == "run_remote_training" and step.get("runs_training") is not True:
            issues.append(_issue("remote_packet_training_step_not_marked_training", "run_remote_training must remain marked as the only training step."))
        if step_id != "run_remote_training" and step.get("runs_training") is True:
            issues.append(_issue(f"remote_packet_{step_id}_claims_training", f"{step_id} must not be marked as a training step."))
    return issues


def _group_missing_items(group: dict[str, Any]) -> list[dict[str, Any]]:
    items = group.get("items")
    if not isinstance(items, list):
        return []
    out: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict) or item.get("missing") is not True:
            continue
        out.append(
            {
                "artifact_id": item.get("artifact_id"),
                "path": item.get("path"),
                "state": item.get("state"),
                "reason": item.get("reason"),
            }
        )
    return out


def _artifact_list(payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    items = payload.get(key)
    if not isinstance(items, list):
        return []
    return [item for item in items if isinstance(item, dict)]


def _next_blocked_lane(lanes: Sequence[dict[str, Any]]) -> dict[str, Any] | None:
    for lane in lanes:
        if lane.get("status") == "blocked":
            return {
                "lane_id": lane.get("lane_id"),
                "phase": lane.get("phase"),
                "action_when_blocked": lane.get("action_when_blocked"),
                "blocked_by": lane.get("blocked_by"),
            }
    return None


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
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:
        return "unknown"


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 Formal Gate Status Report",
        "",
        "This file is a read-only formal-gate status report. It does not execute commands, run remote preflight, train, evaluate, sync, audit, pull back artifacts, or write paper results.",
        "",
        f"- status: `{manifest['status']}`",
        f"- source_head: `{manifest['source_head']}`",
        f"- input_safety_issue_count: `{manifest['input_safety_issue_count']}`",
        f"- local_training_allowed_now: `{manifest['permissions_now']['local_training_allowed_now']}`",
        f"- remote_preflight_allowed_now: `{manifest['permissions_now']['remote_preflight_allowed_now']}`",
        f"- remote_training_allowed_now: `{manifest['permissions_now']['remote_training_allowed_now']}`",
        f"- formal_claim_allowed_now: `{manifest['permissions_now']['formal_claim_allowed_now']}`",
        "",
        "## Current State",
        "",
    ]
    for key, value in manifest["current_state"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Next Blocked Lane", ""])
    if manifest["next_blocked_lane"]:
        lane = manifest["next_blocked_lane"]
        lines.append(f"- lane_id: `{lane['lane_id']}`")
        lines.append(f"- phase: `{lane['phase']}`")
        lines.append(f"- blocked_by: `{', '.join(lane['blocked_by'])}`")
        lines.append(f"- action: {lane['action_when_blocked']}")
    else:
        lines.append("- none")
    lines.extend(["", "## Formal Gate Lanes", ""])
    for lane in manifest["formal_gate_lanes"]:
        host = f", host=`{lane['host']}`" if lane.get("host") else ""
        lines.append(
            f"- `{lane['lane_id']}` ({lane['phase']}): status=`{lane['status']}`, "
            f"missing=`{lane['missing_item_count']}`, runs_training=`{lane['runs_training']}`{host}"
        )
        if lane["blocked_by"]:
            lines.append(f"  - blocked_by: `{', '.join(lane['blocked_by'])}`")
        lines.append(f"  - completion_signal: {lane['completion_signal']}")
        lines.append(f"  - action_when_blocked: {lane['action_when_blocked']}")
    lines.extend(["", "## Remote Execution Steps", ""])
    for step_id, step in manifest["remote_execution_step_summary"].items():
        blocked_by = ", ".join(step["blocked_by"]) if step["blocked_by"] else "none"
        lines.append(
            f"- `{step_id}`: present=`{step['present']}`, allowed_now=`{step['allowed_now']}`, "
            f"runs_training=`{step['runs_training']}`, blocked_by=`{blocked_by}`"
        )
    lines.extend(["", "## Closure Remote Stages", ""])
    for stage_id, stage in manifest["closure_remote_stage_summary"].items():
        blocked_by = ", ".join(stage["blocked_by"]) if stage["blocked_by"] else "none"
        lines.append(
            f"- `{stage_id}`: present=`{stage['present']}`, allowed_now=`{stage['allowed_now']}`, "
            f"runs_training=`{stage['runs_training']}`, runs_remote_preflight=`{stage['runs_remote_preflight']}`, "
            f"host=`{stage['host']}`, blocked_by=`{blocked_by}`"
        )
    lines.extend(["", "## Required Training Artifacts", ""])
    _append_artifacts(lines, manifest["training_artifacts_required"])
    lines.extend(["", "## Required Evaluation Artifacts", ""])
    _append_artifacts(lines, manifest["evaluation_artifacts_required"])
    lines.extend(["", "## Required Acceptance Artifacts", ""])
    _append_artifacts(lines, manifest["acceptance_artifacts_required"])
    lines.extend(["", "## Input Safety Issues", ""])
    if manifest["input_safety_issues"]:
        lines.extend(f"- `{issue['issue_id']}`: {issue['message']}" for issue in manifest["input_safety_issues"])
    else:
        lines.append("- none")
    lines.extend(["", "## Safe Work Without F02.6 Decision", ""])
    lines.extend(f"- {item}" for item in manifest["safe_work_without_f02_6_decision"])
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
