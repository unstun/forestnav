from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_formal_gate_protocol_lane_decision_gate_audit")
DEFAULT_DECISION_PACKET = Path(
    "0_trials/module2_formal_gate_protocol_lane_decision_packet/formal_gate_protocol_lane_decision_packet.json"
)
DEFAULT_DECISION_RECORD = Path(
    "0_trials/module2_formal_gate_protocol_lane_decision_record/protocol_lane_decision_record.json"
)
DECISION_OWNER = "Dr Sun"
PENDING_STATUS = "pending_protocol_lane_decision"
RECORDED_STATUS = "protocol_lane_decision_recorded"


@dataclass(frozen=True)
class FormalGateProtocolLaneDecisionGateAuditConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    decision_packet_path: Path = DEFAULT_DECISION_PACKET
    decision_record_path: Path = DEFAULT_DECISION_RECORD


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = FormalGateProtocolLaneDecisionGateAuditConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        decision_packet_path=args.decision_packet,
        decision_record_path=args.decision_record,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "protocol_lane_decision_gate_audit.json"
    markdown_out = config.markdown_out or output_dir / "protocol_lane_decision_gate_audit.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: FormalGateProtocolLaneDecisionGateAuditConfig) -> dict[str, Any]:
    packet = _read_json(config.decision_packet_path)
    record = _read_json(config.decision_record_path)
    issues = _audit_issues(packet=packet, record=record)
    record_status = str(record.get("status") or "unknown")
    return {
        "schema_version": 1,
        "artifact_name": "module2_formal_gate_protocol_lane_decision_gate_audit",
        "status": _status(issues=issues, record_status=record_status),
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": module2_source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "runs_remote_audit": False,
        "local_training_allowed": False,
        "remote_training_allowed_now": False,
        "formal_claim_allowed": False,
        "paper_result_material_allowed": False,
        "inputs": {
            "decision_packet": str(config.decision_packet_path),
            "decision_record": str(config.decision_record_path),
        },
        "decision_state": _decision_state(packet=packet, record=record),
        "decision_note_audit_summary": _decision_note_audit_summary(record),
        "audit_issue_count": len(issues),
        "audit_issues": issues,
        "allowed_next_human_actions": _allowed_next_human_actions(record),
        "post_decision_gate_requirements": _post_decision_gate_requirements(record),
        "claim_boundaries": [
            "This audit validates the protocol-lane decision gate; it does not select a lane.",
            "A clean pending audit is not training authorization.",
            "A recorded lane decision can only unlock new/revised contract drafting, not remote execution.",
            "Formal claims and paper result material remain blocked until new formal acceptance passes.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit Module2 protocol-lane decision gate without recording a decision.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--decision-packet", type=Path, default=DEFAULT_DECISION_PACKET)
    parser.add_argument("--decision-record", type=Path, default=DEFAULT_DECISION_RECORD)
    return parser.parse_args(list(argv) if argv is not None else None)


def _status(*, issues: list[dict[str, Any]], record_status: str) -> str:
    if issues:
        return "protocol_lane_decision_gate_audit_failed"
    if record_status == PENDING_STATUS:
        return "protocol_lane_decision_gate_pending_clean"
    if record_status == RECORDED_STATUS:
        return "protocol_lane_decision_gate_recorded_clean"
    return "protocol_lane_decision_gate_unknown_state"


def _audit_issues(*, packet: dict[str, Any], record: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    issues.extend(_packet_issues(packet))
    issues.extend(_record_issues(record=record, packet=packet))
    return _unique_issues(issues)


def _packet_issues(packet: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if packet.get("status") != "formal_gate_protocol_lane_decision_packet_ready_for_dr_sun":
        issues.append(_issue("packet_not_ready_for_dr_sun", "Decision packet must be ready for Dr Sun.", observed=packet.get("status")))
    if packet.get("not_paper_result_material") is not True:
        issues.append(_issue("packet_not_marked_non_paper", "Decision packet must be marked not_paper_result_material."))
    for key in ("executes_commands", "runs_training", "runs_remote_preflight", "runs_remote_audit"):
        if packet.get(key) is not False:
            issues.append(_issue(f"packet_{key}_not_false", f"Decision packet must keep {key}=false.", observed=packet.get(key)))
    if packet.get("remote_training_allowed_now") is not False:
        issues.append(_issue("packet_allows_remote_training_now", "Decision packet must not allow remote training now."))
    if packet.get("formal_claim_allowed") is not False:
        issues.append(_issue("packet_allows_formal_claim", "Decision packet must not allow formal claim."))
    if packet.get("paper_result_material_allowed") is not False:
        issues.append(_issue("packet_allows_paper_result_material", "Decision packet must not allow paper result material."))
    expected_blocked = {
        "local_training",
        "remote_success_training",
        "remote_preflight_for_new_success_attempt",
        "formal_claim",
        "paper_result_material",
    }
    if not expected_blocked.issubset(set(_strings(packet.get("current_blocked_actions")))):
        issues.append(_issue("packet_missing_blocked_actions", "Decision packet must block training, claim, and paper result actions."))
    if "record_protocol_lane_decision" not in _strings(packet.get("current_allowed_actions")):
        issues.append(_issue("packet_missing_record_action", "Decision packet must expose record_protocol_lane_decision as a current action."))
    if not _strings(packet.get("valid_lane_ids")):
        issues.append(_issue("packet_missing_valid_lane_ids", "Decision packet must expose valid lane ids."))
    return issues


def _record_issues(*, record: dict[str, Any], packet: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    status = record.get("status")
    if status not in {PENDING_STATUS, RECORDED_STATUS}:
        issues.append(_issue("record_unknown_status", "Decision record status must be pending or recorded.", observed=status))
    if record.get("decision_owner_required") != DECISION_OWNER:
        issues.append(_issue("record_wrong_decision_owner", "Decision record must require Dr Sun.", observed=record.get("decision_owner_required")))
    if record.get("not_paper_result_material") is not True:
        issues.append(_issue("record_not_marked_non_paper", "Decision record must be marked not_paper_result_material."))
    for key in ("executes_commands", "runs_training", "runs_remote_preflight", "runs_remote_audit"):
        if record.get(key) is not False:
            issues.append(_issue(f"record_{key}_not_false", f"Decision record must keep {key}=false.", observed=record.get(key)))
    for key in ("local_training_allowed_now", "remote_training_allowed_now", "formal_claim_allowed_now", "paper_result_material_allowed_now"):
        if record.get(key) is not False:
            issues.append(_issue(f"record_{key}_not_false", f"Decision record must keep {key}=false.", observed=record.get(key)))
    if record.get("training_authorization") != "not_authorized_by_this_decision_record":
        issues.append(_issue("record_training_authorization_drift", "Decision record must not authorize training.", observed=record.get("training_authorization")))
    if record.get("decision_record_is_not_training_authorization") is not True:
        issues.append(_issue("record_not_training_authorization_flag_missing", "Decision record must explicitly not be training authorization."))
    if record.get("decision_record_is_not_paper_result_material") is not True:
        issues.append(_issue("record_not_paper_result_flag_missing", "Decision record must explicitly not be paper result material."))
    if set(_strings(record.get("valid_lane_ids"))) != set(_strings(packet.get("valid_lane_ids"))):
        issues.append(_issue("record_packet_lane_set_mismatch", "Decision record valid lanes must match decision packet."))
    issues.extend(_authorization_issues(record))
    issues.extend(_decision_note_issues(record))
    return issues


def _authorization_issues(record: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    status = record.get("status")
    auth = record.get("current_authorization") if isinstance(record.get("current_authorization"), dict) else {}
    blocked = set(_strings(auth.get("current_blocked_action_ids")))
    expected_blocked = {
        "local_training",
        "remote_success_training",
        "remote_preflight_for_new_success_attempt",
        "formal_claim",
        "paper_result_material",
    }
    if not expected_blocked.issubset(blocked):
        issues.append(_issue("record_authorization_missing_blocked_actions", "Current authorization must keep training, claim, and paper actions blocked."))
    for key in ("remote_training_allowed_now", "local_training_allowed_now", "formal_claim_allowed_now", "paper_result_material_allowed_now"):
        if auth.get(key) is not False:
            issues.append(_issue(f"record_authorization_{key}_not_false", f"Current authorization must keep {key}=false.", observed=auth.get(key)))
    if status == PENDING_STATUS:
        if record.get("selected_lane_id") is not None:
            issues.append(_issue("pending_record_has_selected_lane", "Pending protocol-lane record must not select a lane.", observed=record.get("selected_lane_id")))
        if record.get("requested_selected_lane") != "pending":
            issues.append(_issue("pending_record_requested_lane_not_pending", "Pending protocol-lane record must request pending.", observed=record.get("requested_selected_lane")))
        if record.get("contract_action") != "none":
            issues.append(_issue("pending_record_contract_action_not_none", "Pending protocol-lane record must not choose a contract action.", observed=record.get("contract_action")))
        if auth.get("authorization_status") != "blocked_until_dr_sun_lane_decision":
            issues.append(_issue("pending_authorization_status_drift", "Pending record must be blocked until Dr Sun lane decision.", observed=auth.get("authorization_status")))
        if auth.get("current_allowed_action_ids") != ["record_protocol_lane_decision"]:
            issues.append(_issue("pending_allowed_actions_drift", "Pending record should only allow recording the protocol lane decision.", observed=auth.get("current_allowed_action_ids")))
    elif status == RECORDED_STATUS:
        if record.get("decider") != DECISION_OWNER:
            issues.append(_issue("recorded_decider_not_dr_sun", "Recorded lane decision must have decider Dr Sun.", observed=record.get("decider")))
        if record.get("selected_lane_id") not in _strings(record.get("valid_lane_ids")):
            issues.append(_issue("recorded_selected_lane_invalid", "Recorded selected lane must be in valid_lane_ids.", observed=record.get("selected_lane_id")))
        if record.get("contract_action") == "none":
            issues.append(_issue("recorded_contract_action_missing", "Recorded lane decision must choose a contract action."))
        if auth.get("authorization_status") != "decision_recorded_not_execution_authorization":
            issues.append(_issue("recorded_authorization_status_drift", "Recorded decision must still not be execution authorization.", observed=auth.get("authorization_status")))
        if auth.get("current_allowed_action_ids") != ["draft_new_or_revised_contract_after_lane_decision"]:
            issues.append(_issue("recorded_allowed_actions_drift", "Recorded decision should only allow drafting the new/revised contract.", observed=auth.get("current_allowed_action_ids")))
    return issues


def _decision_note_issues(record: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    status = record.get("status")
    audit = record.get("decision_note_audit")
    if not isinstance(audit, dict):
        return [_issue("record_missing_decision_note_audit", "Decision record must expose decision_note_audit.")]
    if status == PENDING_STATUS:
        if audit.get("required_for_non_pending_decision") is not False:
            issues.append(_issue("pending_note_marked_required", "Pending record must not require decision note yet."))
        if audit.get("present") is not False:
            issues.append(_issue("pending_note_present", "Pending record must not contain a decision note."))
        if audit.get("quality_warning") is not None:
            issues.append(_issue("pending_note_quality_warning", "Pending record must not carry non-pending note quality warning.", observed=audit.get("quality_warning")))
    elif status == RECORDED_STATUS:
        if audit.get("required_for_non_pending_decision") is not True:
            issues.append(_issue("recorded_note_not_required", "Recorded decision must require a decision note."))
        if audit.get("present") is not True:
            issues.append(_issue("recorded_note_not_present", "Recorded decision must contain a decision note."))
        for key in ("mentions_selected_lane", "mentions_failed_gate3", "mentions_contract_action"):
            if audit.get(key) is not True:
                issues.append(_issue(f"recorded_note_missing_{key}", f"Recorded decision note must satisfy {key}."))
        if audit.get("quality_warning") is not None:
            issues.append(_issue("recorded_note_quality_warning", "Recorded decision note must clear quality warnings.", observed=audit.get("quality_warning")))
    return issues


def _decision_state(*, packet: dict[str, Any], record: dict[str, Any]) -> dict[str, Any]:
    return {
        "packet_status": packet.get("status"),
        "record_status": record.get("status"),
        "decision_required": bool(packet.get("decision_required")),
        "selected_lane_id": record.get("selected_lane_id"),
        "requested_selected_lane": record.get("requested_selected_lane"),
        "valid_lane_count": len(_strings(packet.get("valid_lane_ids"))),
        "decider": record.get("decider"),
        "contract_action": record.get("contract_action"),
        "training_authorization": record.get("training_authorization"),
        "remote_training_allowed_now": bool(record.get("remote_training_allowed_now")),
        "local_training_allowed_now": bool(record.get("local_training_allowed_now")),
        "formal_claim_allowed_now": bool(record.get("formal_claim_allowed_now")),
        "paper_result_material_allowed_now": bool(record.get("paper_result_material_allowed_now")),
    }


def _decision_note_audit_summary(record: dict[str, Any]) -> dict[str, Any]:
    audit = record.get("decision_note_audit") if isinstance(record.get("decision_note_audit"), dict) else {}
    status = record.get("status")
    if status == PENDING_STATUS:
        review_status = "not_required_while_pending"
    elif audit.get("quality_warning") is None and audit.get("present") is True:
        review_status = "recorded_decision_note_audit_clean"
    else:
        review_status = "recorded_decision_note_audit_incomplete"
    return {
        "audit_present": bool(audit),
        "gate_review_status": review_status,
        "gate_requires_note_quality": status == RECORDED_STATUS,
        "decision_note_present": bool(audit.get("present")),
        "quality_warning": audit.get("quality_warning"),
    }


def _allowed_next_human_actions(record: dict[str, Any]) -> list[dict[str, Any]]:
    if record.get("status") == PENDING_STATUS:
        return [
            {
                "action_id": "record_protocol_lane_decision",
                "requires_dr_sun": True,
                "runs_training": False,
                "runs_remote_preflight": False,
                "valid_lane_ids": _strings(record.get("valid_lane_ids")),
            }
        ]
    if record.get("status") == RECORDED_STATUS:
        return [
            {
                "action_id": "draft_new_or_revised_contract_after_lane_decision",
                "requires_dr_sun": False,
                "runs_training": False,
                "runs_remote_preflight": False,
                "selected_lane_id": record.get("selected_lane_id"),
            }
        ]
    return []


def _post_decision_gate_requirements(record: dict[str, Any]) -> dict[str, Any]:
    req = record.get("post_decision_requirements") if isinstance(record.get("post_decision_requirements"), dict) else {}
    return {
        "new_or_revised_contract_required": bool(req.get("new_or_revised_contract_required")),
        "contract_status_required_before_training": _strings(req.get("contract_status_required_before_training")),
        "draft_contract_allows_training": bool(req.get("draft_contract_allows_training")),
        "formal_training_still_requires": _strings(req.get("formal_training_still_requires")),
        "paper_result_still_requires": _strings(req.get("paper_result_still_requires")),
    }


def _markdown(manifest: dict[str, Any]) -> str:
    state = manifest["decision_state"]
    lines = [
        "# Module2 Formal Gate Protocol Lane Decision Gate Audit",
        "",
        "This file audits the protocol-lane decision gate; it is not paper result material.",
        "",
        "## Decision State",
        "",
        f"- packet_status: `{state['packet_status']}`",
        f"- record_status: `{state['record_status']}`",
        f"- selected_lane_id: `{state['selected_lane_id']}`",
        f"- training_authorization: `{state['training_authorization']}`",
        f"- remote_training_allowed_now: `{state['remote_training_allowed_now']}`",
        f"- formal_claim_allowed_now: `{state['formal_claim_allowed_now']}`",
        "",
        "## Allowed Next Human Actions",
    ]
    for action in manifest["allowed_next_human_actions"]:
        lines.append(f"- `{action['action_id']}`")
    lines.extend(["", "## Audit", "", f"- status: `{manifest['status']}`", f"- audit_issue_count: `{manifest['audit_issue_count']}`"])
    return "\n".join(lines) + "\n"


def _read_json(path: Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def _strings(value: Any) -> list[str]:
    if not isinstance(value, (list, tuple)):
        return []
    return [str(item) for item in value if item]


def _issue(issue_id: str, message: str, *, observed: Any = None) -> dict[str, Any]:
    issue: dict[str, Any] = {"issue_id": issue_id, "message": message}
    if observed is not None:
        issue["observed"] = observed
    return issue


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
