from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_formal_gate_protocol_lane_decision_record")
DEFAULT_DECISION_PACKET = Path(
    "0_trials/module2_formal_gate_protocol_lane_decision_packet/formal_gate_protocol_lane_decision_packet.json"
)
PENDING = "pending"
DECISION_OWNER = "Dr Sun"
TRAINING_AUTHORIZATION = "not_authorized_by_this_decision_record"


@dataclass(frozen=True)
class FormalGateProtocolLaneDecisionRecordConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    decision_packet_path: Path = DEFAULT_DECISION_PACKET
    selected_lane: str = PENDING
    decider: str | None = None
    decision_note: str | None = None
    contract_action: str = "none"


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = FormalGateProtocolLaneDecisionRecordConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        decision_packet_path=args.decision_packet,
        selected_lane=args.selected_lane,
        decider=args.decider,
        decision_note=args.decision_note,
        contract_action=args.contract_action,
    )
    record = build_record(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "protocol_lane_decision_record.json"
    markdown_out = config.markdown_out or output_dir / "protocol_lane_decision_record.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(record), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": record["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_record(config: FormalGateProtocolLaneDecisionRecordConfig) -> dict[str, Any]:
    packet = _read_json(config.decision_packet_path)
    valid_lanes = _strings(packet.get("valid_lane_ids"))
    selected_lane = str(config.selected_lane)
    _validate_packet(packet)
    _validate_selected_lane(selected_lane=selected_lane, valid_lanes=valid_lanes)
    decision_note_audit = _decision_note_audit(
        selected_lane=selected_lane,
        valid_lanes=valid_lanes,
        decision_note=config.decision_note,
    )
    _validate_non_pending_decision(config=config, packet=packet, decision_note_audit=decision_note_audit)
    pending = selected_lane == PENDING
    status = "pending_protocol_lane_decision" if pending else "protocol_lane_decision_recorded"
    effective_contract_action = "none" if pending else config.contract_action
    return {
        "schema_version": 1,
        "record_name": "module2_formal_gate_protocol_lane_decision_record",
        "status": status,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": module2_source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "runs_remote_audit": False,
        "local_training_allowed": False,
        "local_training_allowed_now": False,
        "remote_training_allowed_now": False,
        "formal_claim_allowed": False,
        "formal_claim_allowed_now": False,
        "paper_result_material_allowed_now": False,
        "decision_owner_required": DECISION_OWNER,
        "requested_selected_lane": selected_lane,
        "selected_lane_id": None if pending else selected_lane,
        "valid_lane_ids": valid_lanes,
        "decider": config.decider,
        "decision_note": config.decision_note,
        "decision_note_audit": decision_note_audit,
        "contract_action": effective_contract_action,
        "training_authorization": TRAINING_AUTHORIZATION,
        "decision_record_is_not_training_authorization": True,
        "decision_record_is_not_paper_result_material": True,
        "packet": _packet_summary(config.decision_packet_path, packet),
        "selected_lane_summary": _selected_lane_summary(packet=packet, selected_lane=selected_lane),
        "current_authorization": _current_authorization(pending=pending),
        "post_decision_requirements": _post_decision_requirements(selected_lane=selected_lane),
        "record_command_templates": _record_command_templates(valid_lanes),
        "audit_issue_count": 0,
        "audit_issues": [],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Module2 protocol-lane decision record.")
    parser.add_argument("--decision-packet", type=Path, default=DEFAULT_DECISION_PACKET)
    parser.add_argument("--selected-lane", default=PENDING)
    parser.add_argument("--decider", default=None)
    parser.add_argument("--decision-note", default=None)
    parser.add_argument("--contract-action", default="none")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    return parser.parse_args(list(argv) if argv is not None else None)


def _validate_packet(packet: dict[str, Any]) -> None:
    if packet.get("status") != "formal_gate_protocol_lane_decision_packet_ready_for_dr_sun":
        raise ValueError("protocol lane decision packet must be ready for Dr Sun before recording a decision")
    if bool(packet.get("runs_training")):
        raise ValueError("protocol lane decision packet must not run training")
    if bool(packet.get("remote_training_allowed_now")):
        raise ValueError("protocol lane decision packet must not allow remote training now")


def _validate_selected_lane(*, selected_lane: str, valid_lanes: Sequence[str]) -> None:
    allowed = {PENDING, *valid_lanes}
    if selected_lane not in allowed:
        raise ValueError(f"unsupported protocol lane {selected_lane!r}; expected one of {sorted(allowed)}")


def _validate_non_pending_decision(
    *,
    config: FormalGateProtocolLaneDecisionRecordConfig,
    packet: dict[str, Any],
    decision_note_audit: dict[str, Any],
) -> None:
    if config.selected_lane == PENDING:
        if config.contract_action != "none":
            raise ValueError("pending protocol lane decision must use --contract-action none")
        return
    if config.decider != DECISION_OWNER:
        raise ValueError(f"protocol lane decision can only be recorded with decider={DECISION_OWNER!r}; got {config.decider!r}")
    if not isinstance(config.decision_note, str) or not config.decision_note.strip():
        raise ValueError("non-pending protocol lane decisions require a non-empty --decision-note")
    allowed_contract_actions = set(_strings(_nested(packet, "decision_record_schema", "allowed_contract_actions")))
    if config.contract_action not in allowed_contract_actions:
        raise ValueError(f"unsupported contract action {config.contract_action!r}; expected one of {sorted(allowed_contract_actions)}")
    if decision_note_audit.get("quality_warning") is not None:
        raise ValueError(f"protocol lane decision note is incomplete: {decision_note_audit['quality_warning']}")


def _decision_note_audit(*, selected_lane: str, valid_lanes: Sequence[str], decision_note: str | None) -> dict[str, Any]:
    note = decision_note.strip() if isinstance(decision_note, str) else ""
    normalized = note.lower()
    rejected_lane_ids = [lane for lane in valid_lanes if lane != selected_lane]
    return {
        "required_for_non_pending_decision": selected_lane != PENDING,
        "present": bool(note),
        "character_count": len(note),
        "word_count": len(note.split()),
        "rejected_lane_ids_required": [] if selected_lane == PENDING else rejected_lane_ids,
        "mentions_selected_lane": selected_lane == PENDING or selected_lane.replace("_", "-") in normalized or selected_lane in normalized,
        "mentions_failed_gate3": selected_lane == PENDING or _mentions_failed_gate3_basis(normalized),
        "mentions_contract_action": selected_lane == PENDING or "contract" in normalized,
        "mentions_rejected_lanes": _mentions_rejected_lanes(
            selected_lane=selected_lane,
            rejected_lane_ids=rejected_lane_ids,
            normalized=normalized,
        ),
        "mentions_evidence_artifacts": _mentions_evidence_artifacts(selected_lane=selected_lane, normalized=normalized),
        "quality_warning": _quality_warning(
            selected_lane=selected_lane,
            rejected_lane_ids=rejected_lane_ids,
            note=note,
            normalized=normalized,
        ),
    }


def _mentions_rejected_lanes(*, selected_lane: str, rejected_lane_ids: Sequence[str], normalized: str) -> bool:
    if selected_lane == PENDING:
        return True
    has_rejection_signal = any(token in normalized for token in ("reject", "rejected", "not select", "not choose", "unselected"))
    mentions_all_other_lanes = all(lane in normalized or lane.replace("_", "-") in normalized for lane in rejected_lane_ids)
    return has_rejection_signal and mentions_all_other_lanes


def _mentions_failed_gate3_basis(normalized: str) -> bool:
    has_failed_gate3 = "gate3" in normalized and any(token in normalized for token in ("fail", "failed", "failure"))
    has_failure_metric = "0.53125" in normalized
    has_threshold = "0.8" in normalized
    return has_failed_gate3 and has_failure_metric and has_threshold


def _mentions_evidence_artifacts(*, selected_lane: str, normalized: str) -> bool:
    if selected_lane == PENDING:
        return True
    artifact_markers = (
        "protocol_lane_matrix",
        "formal_gate_protocol_lane_matrix",
        "gate3_formal_audit",
        "formal_gate_next_round_requirements",
        "next_round_requirements",
        "h02_formal_acceptance",
    )
    return any(marker in normalized for marker in artifact_markers)


def _quality_warning(*, selected_lane: str, rejected_lane_ids: Sequence[str], note: str, normalized: str) -> str | None:
    if selected_lane == PENDING:
        return None
    missing: list[str] = []
    if not note:
        return "missing_required_decision_note"
    if selected_lane not in normalized and selected_lane.replace("_", "-") not in normalized:
        missing.append("selected_lane")
    if not _mentions_failed_gate3_basis(normalized):
        missing.append("failed_gate3_basis_0.53125_vs_0.8")
    if "contract" not in normalized:
        missing.append("contract_action")
    if not _mentions_rejected_lanes(
        selected_lane=selected_lane,
        rejected_lane_ids=rejected_lane_ids,
        normalized=normalized,
    ):
        missing.append("rejected_lanes")
    if not _mentions_evidence_artifacts(selected_lane=selected_lane, normalized=normalized):
        missing.append("evidence_artifacts")
    if missing:
        return "decision_note_should_mention_" + "_".join(missing)
    return None


def _packet_summary(path: Path, packet: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": str(path),
        "status": packet.get("status"),
        "decision_required": bool(packet.get("decision_required")),
        "selected_lane": packet.get("selected_lane"),
        "valid_lane_ids": _strings(packet.get("valid_lane_ids")),
        "current_allowed_actions": _strings(packet.get("current_allowed_actions")),
        "current_blocked_actions": _strings(packet.get("current_blocked_actions")),
        "training_authorization_must_be": _nested(packet, "decision_record_schema", "training_authorization_must_be"),
    }


def _selected_lane_summary(*, packet: dict[str, Any], selected_lane: str) -> dict[str, Any] | None:
    if selected_lane == PENDING:
        return None
    for lane in packet.get("lane_options", []):
        if isinstance(lane, dict) and lane.get("lane_id") == selected_lane:
            return {
                "lane_id": selected_lane,
                "claim_scope": lane.get("claim_scope"),
                "requires_new_or_revised_contract": bool(lane.get("requires_new_or_revised_contract")),
                "training_allowed_now": False,
                "required_decision_justification": _strings(lane.get("required_decision_justification")),
                "must_carry_into_contract": lane.get("must_carry_into_contract"),
            }
    return None


def _current_authorization(*, pending: bool) -> dict[str, Any]:
    return {
        "authorization_status": "blocked_until_dr_sun_lane_decision" if pending else "decision_recorded_not_execution_authorization",
        "current_allowed_action_ids": ["record_protocol_lane_decision"] if pending else ["draft_new_or_revised_contract_after_lane_decision"],
        "current_blocked_action_ids": [
            "local_training",
            "remote_success_training",
            "remote_preflight_for_new_success_attempt",
            "formal_claim",
            "paper_result_material",
        ],
        "remote_training_allowed_now": False,
        "local_training_allowed_now": False,
        "formal_claim_allowed_now": False,
        "paper_result_material_allowed_now": False,
    }


def _post_decision_requirements(*, selected_lane: str) -> dict[str, Any]:
    return {
        "selected_lane": selected_lane,
        "new_or_revised_contract_required": selected_lane != PENDING,
        "contract_status_required_before_training": ["approved", "frozen"],
        "draft_contract_allows_training": False,
        "formal_training_still_requires": [
            "approved_or_frozen_contract",
            "source_freshness_audit_after_contract",
            "remote_execution_packet_for_selected_lane",
            "approved_remote_preflight_for_selected_lane",
        ],
        "paper_result_still_requires": [
            "new_gate3_formal_audit_pass",
            "h02_formal_output_accepted_true",
            "paper_result_input_allowed_true",
        ],
    }


def _record_command_templates(valid_lanes: Sequence[str]) -> list[dict[str, Any]]:
    return [
        {
            "selected_lane": lane,
            "allowed_for_agent_now": False,
            "requires_dr_sun_decision": True,
            "runs_training": False,
            "runs_remote_preflight": False,
            "template": (
                "PYTHONPATH=2_experiment python -m "
                "forest_n3p.scripts.build_module2_formal_gate_protocol_lane_decision_record "
                f"--selected-lane {lane} --decider 'Dr Sun' --contract-action <action> "
                f"--decision-note '{_decision_note_template(lane)}'"
            ),
        }
        for lane in valid_lanes
    ]


def _decision_note_template(selected_lane: str) -> str:
    return (
        f"Select {selected_lane} because the failed Gate3 0.53125 result is below the 0.8 threshold; "
        "reject <all other lane ids with one rationale each>; "
        "use protocol_lane_matrix, gate3_formal_audit, formal_gate_next_round_requirements, "
        "and h02_formal_acceptance artifacts as the evidence basis; "
        "contract action is <draft_new_contract|draft_revised_contract|stop_success_attempts_and_record_negative_evidence>; "
        "this decision does not authorize local training, remote preflight, remote training, formal claim, or paper result material."
    )


def _markdown(record: dict[str, Any]) -> str:
    lines = [
        "# Module2 Formal Gate Protocol Lane Decision Record",
        "",
        "This file records the lane-decision state; it is not paper result material.",
        "",
        "## Decision State",
        "",
        f"- status: `{record['status']}`",
        f"- requested_selected_lane: `{record['requested_selected_lane']}`",
        f"- selected_lane_id: `{record['selected_lane_id']}`",
        f"- decider: `{record['decider']}`",
        f"- contract_action: `{record['contract_action']}`",
        f"- training_authorization: `{record['training_authorization']}`",
        f"- decision_record_is_not_training_authorization: `{record['decision_record_is_not_training_authorization']}`",
        f"- decision_record_is_not_paper_result_material: `{record['decision_record_is_not_paper_result_material']}`",
        "",
        "## Authorization",
        "",
        f"- remote_training_allowed_now: `{record['remote_training_allowed_now']}`",
        f"- local_training_allowed_now: `{record['local_training_allowed_now']}`",
        f"- formal_claim_allowed_now: `{record['formal_claim_allowed_now']}`",
        f"- paper_result_material_allowed_now: `{record['paper_result_material_allowed_now']}`",
        "",
        "## Valid Lanes",
    ]
    for lane in record["valid_lane_ids"]:
        lines.append(f"- `{lane}`")
    lines.extend(["", "## Record Command Templates"])
    for template in record["record_command_templates"]:
        lines.extend(
            [
                f"- selected_lane: `{template['selected_lane']}`",
                f"  - allowed_for_agent_now: `{template['allowed_for_agent_now']}`",
                f"  - runs_training: `{template['runs_training']}`",
                f"  - runs_remote_preflight: `{template['runs_remote_preflight']}`",
                f"  - template: `{template['template']}`",
            ]
        )
    requirements = record["post_decision_requirements"]
    lines.extend(
        [
            "",
            "## Post-Decision Requirements",
            "",
            f"- new_or_revised_contract_required: `{requirements['new_or_revised_contract_required']}`",
            f"- contract_status_required_before_training: `{', '.join(requirements['contract_status_required_before_training'])}`",
            f"- draft_contract_allows_training: `{requirements['draft_contract_allows_training']}`",
            "- formal_training_still_requires:",
        ]
    )
    for item in requirements["formal_training_still_requires"]:
        lines.append(f"  - {item}")
    lines.append("- paper_result_still_requires:")
    for item in requirements["paper_result_still_requires"]:
        lines.append(f"  - {item}")
    lines.extend(["", "## Audit", "", f"- audit_issue_count: `{record['audit_issue_count']}`"])
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


def _nested(payload: dict[str, Any], *keys: str) -> Any:
    current: Any = payload
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


if __name__ == "__main__":
    raise SystemExit(main())
