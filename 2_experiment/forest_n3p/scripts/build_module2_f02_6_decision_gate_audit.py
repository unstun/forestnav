from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_f02_6_decision_gate_audit")
DEFAULT_PACKET = Path("0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json")
DEFAULT_RECORD = Path("0_trials/module2_f02_6_decision_record/f02_6_decision_record.json")
DEFAULT_POST_PLAN = Path("0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json")
DECISION_OWNER = "Dr Sun"
APPROVE_OBSTACLE_SUMMARY = "approve_obstacle_summary_warm_start"
REJECT_OBSTACLE_SUMMARY = "reject_obstacle_summary_warm_start"


@dataclass(frozen=True)
class F026DecisionGateAuditConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    packet_path: Path = DEFAULT_PACKET
    decision_record_path: Path = DEFAULT_RECORD
    post_plan_path: Path = DEFAULT_POST_PLAN


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = F026DecisionGateAuditConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        packet_path=args.packet,
        decision_record_path=args.decision_record,
        post_plan_path=args.post_plan,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "f02_6_decision_gate_audit.json"
    markdown_out = config.markdown_out or output_dir / "f02_6_decision_gate_audit.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: F026DecisionGateAuditConfig) -> dict[str, Any]:
    packet = _read_json(config.packet_path)
    record = _read_json(config.decision_record_path)
    plan = _read_json(config.post_plan_path)
    issues = _audit_issues(packet=packet, record=record, plan=plan)
    pending = record.get("status") == "pending_human_decision"
    return {
        "schema_version": 1,
        "artifact_name": "module2_f02_6_decision_gate_audit",
        "status": _status(issues=issues, pending=pending),
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "inputs": {
            "decision_packet": str(config.packet_path),
            "decision_record": str(config.decision_record_path),
            "post_f02_6_regeneration_plan": str(config.post_plan_path),
        },
        "decision_state": _decision_state(packet=packet, record=record, plan=plan),
        "audit_issue_count": len(issues),
        "audit_issues": issues,
        "allowed_next_human_actions": _allowed_next_human_actions(record),
        "post_decision_gate_requirements": _post_decision_gate_requirements(plan),
        "claim_boundaries": [
            "This audit validates the F02.6 decision gate; it does not record Dr Sun's decision.",
            "A passing pending audit is not approval for warm-start training.",
            "Approval can only unlock source-fresh regeneration and approved remote preflight, not a paper claim.",
            "Formal PPO warm-start training remains remote-only on gpu3070ti-relay after all upstream gates pass.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit Module2 F02.6 decision gate without recording a decision.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--decision-record", type=Path, default=DEFAULT_RECORD)
    parser.add_argument("--post-plan", type=Path, default=DEFAULT_POST_PLAN)
    return parser.parse_args(list(argv) if argv is not None else None)


def _audit_issues(*, packet: dict[str, Any], record: dict[str, Any], plan: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    issues.extend(_packet_issues(packet))
    issues.extend(_record_issues(record))
    issues.extend(_plan_alignment_issues(record=record, plan=plan))
    return _unique_issues(issues)


def _packet_issues(packet: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    recommendation = packet.get("recommendation") if isinstance(packet.get("recommendation"), dict) else {}
    if packet.get("status") != "pending_human_decision":
        issues.append(_issue("packet_not_pending_human_decision", "Decision packet must remain pending until Dr Sun records F02.6.", observed=packet.get("status")))
    if recommendation.get("decision_owner") != DECISION_OWNER:
        issues.append(_issue("packet_wrong_decision_owner", "Decision packet must name Dr Sun as decision owner.", observed=recommendation.get("decision_owner")))
    if recommendation.get("formal_claim_allowed") is not False:
        issues.append(_issue("packet_allows_formal_claim", "Decision support packet must not allow formal claims."))
    if recommendation.get("decision") != APPROVE_OBSTACLE_SUMMARY:
        issues.append(_issue("packet_unexpected_recommendation", "Current packet should explicitly recommend obstacle-summary approval or be regenerated.", observed=recommendation.get("decision")))
    if "requires_dr_sun_approval" not in _strings(packet.get("blockers")):
        issues.append(_issue("packet_missing_dr_sun_approval_blocker", "Decision packet must keep requires_dr_sun_approval blocker."))
    approved = _branch(packet, "if_approved_obstacle_summary")
    if approved.get("host") != "gpu3070ti-relay":
        issues.append(_issue("packet_approved_branch_wrong_host", "Approved branch must target gpu3070ti-relay.", observed=approved.get("host")))
    runner = str(approved.get("runner_command") or "")
    if "--bc-checkpoint" not in runner:
        issues.append(_issue("packet_approved_runner_missing_bc_checkpoint", "Approved runner must include obstacle-summary BC checkpoint."))
    if "--device cuda" not in runner:
        issues.append(_issue("packet_approved_runner_missing_cuda", "Approved runner must request CUDA execution."))
    rejected = _branch(packet, "if_rejected_obstacle_summary")
    if "patch-CNN" not in str(rejected.get("next_protocol") or ""):
        issues.append(_issue("packet_reject_branch_missing_stronger_protocol", "Rejected branch must route to stronger/full patch-CNN protocol."))
    return issues


def _record_issues(record: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    status = record.get("status")
    if record.get("decision_owner_required") != DECISION_OWNER:
        issues.append(_issue("record_wrong_required_decision_owner", "Decision record must require Dr Sun.", observed=record.get("decision_owner_required")))
    if record.get("local_training_allowed") is not False:
        issues.append(_issue("record_allows_local_training", "Decision record must never allow local training."))
    if record.get("formal_claim_allowed") is not False:
        issues.append(_issue("record_allows_formal_claim", "Decision record must not allow formal claims."))
    if record.get("remote_preflight_allowed_now") is not False:
        issues.append(_issue("record_allows_remote_preflight_now", "Decision record alone must not allow remote preflight now."))
    if record.get("remote_training_allowed_now") is not False:
        issues.append(_issue("record_allows_remote_training_now", "Decision record alone must not allow remote training now."))
    if status == "pending_human_decision":
        if record.get("decider") is not None:
            issues.append(_issue("pending_record_has_decider", "Pending record must not name a decider.", observed=record.get("decider")))
        if record.get("decision_note") not in {None, ""}:
            issues.append(_issue("pending_record_has_decision_note", "Pending record must not contain a decision note.", observed=record.get("decision_note")))
        if record.get("remote_training_allowed") is not False:
            issues.append(_issue("pending_record_allows_remote_training", "Pending F02.6 must not allow remote training."))
        if record.get("effective_warm_start_decision") != "pending":
            issues.append(_issue("pending_record_effective_decision_not_pending", "Pending record must keep effective decision pending.", observed=record.get("effective_warm_start_decision")))
        if "requires_dr_sun_approval" not in _strings(record.get("blockers")):
            issues.append(_issue("pending_record_missing_dr_sun_blocker", "Pending record must include requires_dr_sun_approval."))
    elif status == "approved":
        if record.get("decider") != DECISION_OWNER:
            issues.append(_issue("approved_record_decider_not_dr_sun", "Approved record must have decider Dr Sun.", observed=record.get("decider")))
        if not str(record.get("decision_note") or "").strip():
            issues.append(_issue("approved_record_missing_decision_note", "Approved F02.6 record must include Dr Sun's decision note."))
        if record.get("remote_training_allowed") is not True:
            issues.append(_issue("approved_record_does_not_allow_remote_training", "Approved record should allow the remote-only downstream path."))
        approved = _branch(record, "if_approved_obstacle_summary", key="conditional_actions")
        if approved.get("runs_training") is not False:
            issues.append(_issue("approved_preflight_action_claims_training", "Decision approval action must only regenerate preflight, not train."))
    elif status == "rejected":
        if record.get("decider") != DECISION_OWNER:
            issues.append(_issue("rejected_record_decider_not_dr_sun", "Rejected record must have decider Dr Sun.", observed=record.get("decider")))
        if not str(record.get("decision_note") or "").strip():
            issues.append(_issue("rejected_record_missing_decision_note", "Rejected F02.6 record must include Dr Sun's decision note."))
        if record.get("remote_training_allowed") is not False:
            issues.append(_issue("rejected_record_allows_remote_training", "Rejected obstacle-summary warm-start must not allow remote training."))
        if "obstacle_summary_warm_start_rejected" not in _strings(record.get("blockers")):
            issues.append(_issue("rejected_record_missing_rejection_blocker", "Rejected record must keep warm-start rejected blocker."))
    else:
        issues.append(_issue("record_unknown_status", "Decision record status must be pending_human_decision, approved, or rejected.", observed=status))
    return issues


def _plan_alignment_issues(*, record: dict[str, Any], plan: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    summary = plan.get("current_gate_summary") if isinstance(plan.get("current_gate_summary"), dict) else {}
    blocking = plan.get("blocking_summary") if isinstance(plan.get("blocking_summary"), dict) else {}
    if summary and summary.get("f02_6_decision_status") != record.get("status"):
        issues.append(
            _issue(
                "plan_record_decision_status_mismatch",
                "Post-F02.6 plan decision status must match decision record.",
                observed={"record": record.get("status"), "plan": summary.get("f02_6_decision_status")},
            )
        )
    if record.get("status") == "pending_human_decision":
        if plan.get("status") != "blocked_until_f02_6_decision":
            issues.append(_issue("pending_plan_not_blocked", "Post-F02.6 plan must be blocked while F02.6 is pending.", observed=plan.get("status")))
        if blocking.get("training_allowed_now") is not False:
            issues.append(_issue("pending_plan_allows_training", "Plan must not allow training while F02.6 is pending."))
        if blocking.get("remote_preflight_allowed_now") is not False:
            issues.append(_issue("pending_plan_allows_remote_preflight", "Plan must not allow remote preflight while F02.6 is pending."))
        if _stage(plan, "f02_6_decision_record").get("requires_human_input") is not True:
            issues.append(_issue("pending_plan_decision_stage_not_human_input", "Pending plan must keep decision stage human-input gated."))
    return issues


def _decision_state(*, packet: dict[str, Any], record: dict[str, Any], plan: dict[str, Any]) -> dict[str, Any]:
    recommendation = packet.get("recommendation") if isinstance(packet.get("recommendation"), dict) else {}
    blocking = plan.get("blocking_summary") if isinstance(plan.get("blocking_summary"), dict) else {}
    return {
        "packet_status": packet.get("status"),
        "packet_recommendation": recommendation.get("decision"),
        "decision_owner": recommendation.get("decision_owner"),
        "record_status": record.get("status"),
        "record_requested_decision": record.get("requested_decision"),
        "record_decider": record.get("decider"),
        "effective_warm_start_decision": record.get("effective_warm_start_decision"),
        "remote_training_allowed": record.get("remote_training_allowed"),
        "remote_preflight_allowed_now": record.get("remote_preflight_allowed_now"),
        "remote_training_allowed_now": record.get("remote_training_allowed_now"),
        "local_training_allowed": record.get("local_training_allowed"),
        "formal_claim_allowed": record.get("formal_claim_allowed"),
        "post_plan_status": plan.get("status"),
        "training_allowed_now": blocking.get("training_allowed_now"),
        "remote_preflight_allowed_now": blocking.get("remote_preflight_allowed_now"),
    }


def _allowed_next_human_actions(record: dict[str, Any]) -> list[dict[str, Any]]:
    if record.get("status") != "pending_human_decision":
        return []
    return [
        {
            "decision": APPROVE_OBSTACLE_SUMMARY,
            "effect": "Allows source-fresh regeneration and approved remote preflight regeneration; does not allow paper claims.",
            "records_command_template": "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_decision_record --decision approve_obstacle_summary_warm_start --decider 'Dr Sun' --decision-note '<Dr Sun approval note>'",
        },
        {
            "decision": REJECT_OBSTACLE_SUMMARY,
            "effect": "Keeps obstacle-summary warm-start formal training blocked and routes to stronger/full patch-CNN protocol.",
            "records_command_template": "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_decision_record --decision reject_obstacle_summary_warm_start --decider 'Dr Sun' --decision-note '<Dr Sun rejection note>'",
        },
    ]


def _post_decision_gate_requirements(plan: dict[str, Any]) -> list[dict[str, Any]]:
    requirements: list[dict[str, Any]] = []
    for stage_id in (
        "regenerate_preflight_gate_artifacts",
        "approved_remote_preflight",
        "regenerate_remote_execution_packet",
        "gate3_remote_training",
        "gate3_remote_audit_pullback",
        "regenerate_h01_h02_formal_artifacts",
        "regenerate_claim_gate_artifacts",
    ):
        stage = _stage(plan, stage_id)
        if not stage:
            continue
        requirements.append(
            {
                "stage_id": stage_id,
                "runs_training": bool(stage.get("runs_training")),
                "runs_remote_preflight": bool(stage.get("runs_remote_preflight")),
                "host": stage.get("host"),
                "blocked_by": _strings(stage.get("blocked_by")),
                "evidence_paths": _strings(stage.get("evidence_paths")),
            }
        )
    return requirements


def _status(*, issues: Sequence[dict[str, Any]], pending: bool) -> str:
    if issues:
        return "f02_6_decision_gate_audit_failed"
    return "f02_6_decision_gate_pending_clean" if pending else "f02_6_decision_gate_audit_passed"


def _branch(payload: dict[str, Any], name: str, *, key: str = "next_actions") -> dict[str, Any]:
    parent = payload.get(key) if isinstance(payload.get(key), dict) else {}
    branch = parent.get(name) if isinstance(parent.get(name), dict) else {}
    return branch


def _stage(plan: dict[str, Any], stage_id: str) -> dict[str, Any]:
    stages = plan.get("ordered_stages")
    if not isinstance(stages, list):
        return {}
    for stage in stages:
        if isinstance(stage, dict) and stage.get("stage_id") == stage_id:
            return stage
    return {}


def _strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _issue(issue_id: str, message: str, *, observed: Any | None = None) -> dict[str, Any]:
    out = {"issue_id": issue_id, "message": message}
    if observed is not None:
        out["observed"] = observed
    return out


def _unique_issues(issues: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for issue in issues:
        issue_id = str(issue.get("issue_id"))
        if not issue_id or issue_id in seen:
            continue
        seen.add(issue_id)
        out.append(issue)
    return out


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 F02.6 Decision Gate Audit",
        "",
        "This file audits the human decision gate. It does not record a decision, train, preflight, or claim results.",
        "",
        f"- status: `{manifest['status']}`",
        f"- audit_issue_count: `{manifest['audit_issue_count']}`",
        f"- record_status: `{manifest['decision_state']['record_status']}`",
        f"- packet_recommendation: `{manifest['decision_state']['packet_recommendation']}`",
        f"- training_allowed_now: `{manifest['decision_state']['training_allowed_now']}`",
        f"- remote_preflight_allowed_now: `{manifest['decision_state']['remote_preflight_allowed_now']}`",
        "",
        "## Audit Issues",
        "",
    ]
    if manifest["audit_issues"]:
        lines.extend(f"- `{issue['issue_id']}`: {issue['message']}" for issue in manifest["audit_issues"])
    else:
        lines.append("- none")
    lines.extend(["", "## Allowed Human Actions", ""])
    for action in manifest["allowed_next_human_actions"]:
        lines.append(f"- `{action['decision']}`: {action['effect']}")
    lines.extend(["", "## Claim Boundaries", ""])
    lines.extend(f"- {item}" for item in manifest["claim_boundaries"])
    return "\n".join(lines) + "\n"


def _read_json(path: Path) -> dict[str, Any]:
    if not Path(path).is_file():
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _source_head() -> str:
    return module2_source_head()


if __name__ == "__main__":
    raise SystemExit(main())
