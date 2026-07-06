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
EXPECTED_NEXT_SUCCESS_CATEGORY_COUNTS = {
    "contract": 1,
    "training": 3,
    "evaluation": 2,
    "acceptance": 3,
    "formal_acceptance": 1,
}


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
    issues.extend(_next_success_attempt_requirement_issues(record))
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
        for key in (
            "mentions_selected_lane",
            "mentions_failed_gate3",
            "mentions_contract_action",
            "mentions_rejected_lanes",
            "mentions_evidence_artifacts",
        ):
            if audit.get(key) is not True:
                issues.append(_issue(f"recorded_note_missing_{key}", f"Recorded decision note must satisfy {key}."))
        if audit.get("quality_warning") is not None:
            issues.append(_issue("recorded_note_quality_warning", "Recorded decision note must clear quality warnings.", observed=audit.get("quality_warning")))
    return issues


def _next_success_attempt_requirement_issues(record: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    summary = record.get("next_success_attempt_requirements")
    if not isinstance(summary, dict):
        return [
            _issue(
                "record_missing_next_success_attempt_requirements",
                "Decision record must carry next-success-attempt artifact requirements.",
            )
        ]
    if summary.get("source_status") != "formal_gate_next_round_requirements_ready":
        issues.append(
            _issue(
                "record_next_success_requirements_not_ready",
                "Decision record must consume a ready next-round requirements artifact.",
                observed=summary.get("source_status"),
            )
        )
    if summary.get("next_success_attempt_status") != "blocked_until_protocol_lane_decision_and_contract":
        issues.append(
            _issue(
                "record_next_success_status_drift",
                "Next success attempt must remain blocked until protocol lane decision and contract.",
                observed=summary.get("next_success_attempt_status"),
            )
        )
    if summary.get("next_success_attempt_artifact_count") != 10:
        issues.append(
            _issue(
                "record_next_success_artifact_count_drift",
                "Decision record must require exactly 10 next-success-attempt artifacts.",
                observed=summary.get("next_success_attempt_artifact_count"),
            )
        )
    category_counts = (
        summary.get("next_success_attempt_artifact_category_counts")
        if isinstance(summary.get("next_success_attempt_artifact_category_counts"), dict)
        else {}
    )
    if category_counts != EXPECTED_NEXT_SUCCESS_CATEGORY_COUNTS:
        issues.append(
            _issue(
                "record_next_success_category_counts_drift",
                "Next-success artifact category counts must remain contract/training/evaluation/acceptance/formal_acceptance=1/3/2/3/1.",
                observed=category_counts,
            )
        )
    ids_by_category = (
        summary.get("next_success_attempt_artifact_ids_by_category")
        if isinstance(summary.get("next_success_attempt_artifact_ids_by_category"), dict)
        else {}
    )
    expected_ids = {
        "contract": ["new_or_revised_research_contract"],
        "training": ["train_final_model_zip", "train_summary_json", "train_training_manifest_json"],
        "evaluation": ["eval_gate3_eval_episodes_csv", "eval_gate3_summary_json"],
        "acceptance": [
            "gate3_trial_manifest_json",
            "gate3_formal_audit_json",
            "pulled_back_checkpoint_hash_record",
        ],
        "formal_acceptance": ["h02_formal_output_acceptance"],
    }
    for category, expected in expected_ids.items():
        if _strings(ids_by_category.get(category)) != expected:
            issues.append(
                _issue(
                    f"record_next_success_{category}_artifact_ids_drift",
                    f"Next-success {category} artifact ids drifted.",
                    observed=ids_by_category.get(category),
                )
            )
    if summary.get("old_failed_run_artifacts_invalid_for_next_success_attempt") is not True:
        issues.append(
            _issue(
                "record_old_failed_run_artifacts_not_marked_invalid",
                "Decision record must mark old failed-run artifacts invalid for the next success attempt.",
                observed=summary.get("old_failed_run_artifacts_invalid_for_next_success_attempt"),
            )
        )
    if summary.get("new_success_training_allowed_now") is not False:
        issues.append(
            _issue(
                "record_next_success_training_allowed_now",
                "Decision record must not allow new success training now.",
                observed=summary.get("new_success_training_allowed_now"),
            )
        )
    req = record.get("post_decision_requirements") if isinstance(record.get("post_decision_requirements"), dict) else {}
    if req.get("next_success_attempt_artifact_count") != 10:
        issues.append(
            _issue(
                "record_post_decision_next_artifact_count_missing",
                "Post-decision requirements must mirror the 10 next-success artifacts.",
                observed=req.get("next_success_attempt_artifact_count"),
            )
        )
    if req.get("old_failed_run_artifacts_invalid_for_next_success_attempt") is not True:
        issues.append(
            _issue(
                "record_post_decision_old_failed_run_invalid_missing",
                "Post-decision requirements must state old failed-run artifacts are invalid substitutes.",
                observed=req.get("old_failed_run_artifacts_invalid_for_next_success_attempt"),
            )
        )
    return issues


def _decision_state(*, packet: dict[str, Any], record: dict[str, Any]) -> dict[str, Any]:
    next_success = (
        record.get("next_success_attempt_requirements")
        if isinstance(record.get("next_success_attempt_requirements"), dict)
        else {}
    )
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
        "next_success_attempt_artifact_count": next_success.get("next_success_attempt_artifact_count"),
        "old_failed_run_artifacts_invalid_for_next_success_attempt": next_success.get(
            "old_failed_run_artifacts_invalid_for_next_success_attempt"
        ),
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
        "mentions_selected_lane": bool(audit.get("mentions_selected_lane")),
        "mentions_failed_gate3": bool(audit.get("mentions_failed_gate3")),
        "mentions_contract_action": bool(audit.get("mentions_contract_action")),
        "mentions_rejected_lanes": bool(audit.get("mentions_rejected_lanes")),
        "mentions_evidence_artifacts": bool(audit.get("mentions_evidence_artifacts")),
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
        "next_success_attempt_artifact_count": req.get("next_success_attempt_artifact_count"),
        "next_success_attempt_artifact_category_counts": req.get("next_success_attempt_artifact_category_counts")
        if isinstance(req.get("next_success_attempt_artifact_category_counts"), dict)
        else {},
        "old_failed_run_artifacts_invalid_for_next_success_attempt": req.get(
            "old_failed_run_artifacts_invalid_for_next_success_attempt"
        ),
        "formal_training_still_requires": _strings(req.get("formal_training_still_requires")),
        "paper_result_still_requires": _strings(req.get("paper_result_still_requires")),
    }


def _markdown(manifest: dict[str, Any]) -> str:
    state = manifest["decision_state"]
    note = manifest["decision_note_audit_summary"]
    requirements = manifest["post_decision_gate_requirements"]
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
        f"- next_success_attempt_artifact_count: `{state['next_success_attempt_artifact_count']}`",
        f"- old_failed_run_artifacts_invalid_for_next_success_attempt: `{state['old_failed_run_artifacts_invalid_for_next_success_attempt']}`",
        "",
        "## Decision Note Audit",
        "",
        f"- gate_review_status: `{note['gate_review_status']}`",
        f"- gate_requires_note_quality: `{note['gate_requires_note_quality']}`",
        f"- decision_note_present: `{note['decision_note_present']}`",
        f"- mentions_selected_lane: `{note['mentions_selected_lane']}`",
        f"- mentions_failed_gate3: `{note['mentions_failed_gate3']}`",
        f"- mentions_contract_action: `{note['mentions_contract_action']}`",
        f"- mentions_rejected_lanes: `{note['mentions_rejected_lanes']}`",
        f"- mentions_evidence_artifacts: `{note['mentions_evidence_artifacts']}`",
        f"- quality_warning: `{note['quality_warning']}`",
        "",
        "## Allowed Next Human Actions",
    ]
    for action in manifest["allowed_next_human_actions"]:
        lines.append(f"- `{action['action_id']}`")
        lines.append(f"  - requires_dr_sun: `{action['requires_dr_sun']}`")
        lines.append(f"  - runs_training: `{action['runs_training']}`")
        lines.append(f"  - runs_remote_preflight: `{action['runs_remote_preflight']}`")
        if "valid_lane_ids" in action:
            lines.append("  - valid_lane_ids:")
            for lane in action["valid_lane_ids"]:
                lines.append(f"    - `{lane}`")
        if "selected_lane_id" in action:
            lines.append(f"  - selected_lane_id: `{action['selected_lane_id']}`")
    lines.extend(
        [
            "",
            "## Post-Decision Gate Requirements",
            "",
            f"- new_or_revised_contract_required: `{requirements['new_or_revised_contract_required']}`",
            f"- contract_status_required_before_training: `{', '.join(requirements['contract_status_required_before_training'])}`",
            f"- draft_contract_allows_training: `{requirements['draft_contract_allows_training']}`",
            f"- next_success_attempt_artifact_count: `{requirements['next_success_attempt_artifact_count']}`",
            f"- next_success_attempt_artifact_category_counts: `{requirements['next_success_attempt_artifact_category_counts']}`",
            f"- old_failed_run_artifacts_invalid_for_next_success_attempt: `{requirements['old_failed_run_artifacts_invalid_for_next_success_attempt']}`",
            "- formal_training_still_requires:",
        ]
    )
    for item in requirements["formal_training_still_requires"]:
        lines.append(f"  - {item}")
    lines.append("- paper_result_still_requires:")
    for item in requirements["paper_result_still_requires"]:
        lines.append(f"  - {item}")
    lines.extend(["", "## Claim Boundaries"])
    for boundary in manifest["claim_boundaries"]:
        lines.append(f"- {boundary}")
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
