from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_formal_gate_protocol_lane_decision_packet")
DEFAULT_LANE_MATRIX = Path("0_trials/module2_formal_gate_protocol_lane_matrix/formal_gate_protocol_lane_matrix.json")
DEFAULT_CONTRACT_INTAKE = Path("0_trials/module2_formal_gate_contract_intake/formal_gate_contract_intake.json")


@dataclass(frozen=True)
class FormalGateProtocolLaneDecisionPacketConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    lane_matrix_path: Path = DEFAULT_LANE_MATRIX
    contract_intake_path: Path = DEFAULT_CONTRACT_INTAKE


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = FormalGateProtocolLaneDecisionPacketConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        lane_matrix_path=args.lane_matrix,
        contract_intake_path=args.contract_intake,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "formal_gate_protocol_lane_decision_packet.json"
    markdown_out = config.markdown_out or output_dir / "formal_gate_protocol_lane_decision_packet.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: FormalGateProtocolLaneDecisionPacketConfig) -> dict[str, Any]:
    lane_matrix = _read_json(config.lane_matrix_path)
    contract_intake = _read_json(config.contract_intake_path)
    lanes = _lane_options(lane_matrix)
    gate = _gate_summary(lane_matrix=lane_matrix, contract_intake=contract_intake)
    decision_schema = _decision_record_schema(lanes)
    audit_issues = _audit_issues(lane_matrix=lane_matrix, contract_intake=contract_intake, gate=gate, lanes=lanes)
    ready = not audit_issues
    return {
        "schema_version": 1,
        "artifact_name": "module2_formal_gate_protocol_lane_decision_packet",
        "status": "formal_gate_protocol_lane_decision_packet_ready_for_dr_sun" if ready else "formal_gate_protocol_lane_decision_packet_blocked",
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
            "lane_matrix": str(config.lane_matrix_path),
            "contract_intake": str(config.contract_intake_path),
        },
        "gate_summary": gate,
        "decision_required": True,
        "selected_lane": None,
        "valid_lane_ids": [lane["lane_id"] for lane in lanes],
        "lane_options": lanes,
        "decision_record_schema": decision_schema,
        "current_allowed_actions": [
            "record_protocol_lane_decision",
            "draft_new_or_revised_contract_after_lane_decision",
        ],
        "current_blocked_actions": [
            "local_training",
            "remote_success_training",
            "remote_preflight_for_new_success_attempt",
            "formal_claim",
            "paper_result_material",
        ],
        "post_decision_next_artifacts": [
            ".pipeline/contracts/module2-*.md with status approved or frozen",
            "updated remote execution packet for the selected protocol lane",
            "source freshness audit after the contract commit",
            "remote-only training/evaluation/acceptance bundle if the selected lane still requires a success attempt",
        ],
        "audit_issue_count": len(audit_issues),
        "audit_issues": audit_issues,
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Module2 protocol-lane decision packet after formal Gate3 failure.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--lane-matrix", type=Path, default=DEFAULT_LANE_MATRIX)
    parser.add_argument("--contract-intake", type=Path, default=DEFAULT_CONTRACT_INTAKE)
    return parser.parse_args(list(argv) if argv is not None else None)


def _gate_summary(*, lane_matrix: dict[str, Any], contract_intake: dict[str, Any]) -> dict[str, Any]:
    lane_gate = lane_matrix.get("gate_summary") if isinstance(lane_matrix.get("gate_summary"), dict) else {}
    contract_gate = contract_intake.get("current_gate") if isinstance(contract_intake.get("current_gate"), dict) else {}
    return {
        "lane_matrix_status": lane_matrix.get("status"),
        "lane_matrix_audit_issue_count": int(lane_matrix.get("audit_issue_count") or 0),
        "contract_intake_status": contract_intake.get("status"),
        "contract_intake_audit_issue_count": int(contract_intake.get("audit_issue_count") or 0),
        "current_formal_decision": lane_gate.get("current_formal_decision"),
        "current_failure_mode": lane_gate.get("current_failure_mode"),
        "terminal_rs_success_rate": _number(lane_gate.get("terminal_rs_success_rate")),
        "required_success_threshold": _number(lane_gate.get("required_success_threshold")),
        "new_success_training_allowed_now": bool(
            lane_gate.get("new_success_training_allowed_now") or contract_gate.get("new_success_training_allowed_now")
        ),
        "remote_training_allowed_now": bool(lane_gate.get("remote_training_allowed_now") or contract_intake.get("remote_training_allowed_now")),
        "local_training_allowed_now": bool(
            lane_gate.get("local_training_allowed_now") or contract_gate.get("local_training_allowed_now")
        ),
        "formal_claim_allowed_now": bool(
            lane_gate.get("formal_claim_allowed_now") or contract_gate.get("formal_claim_allowed_now")
        ),
        "paper_result_material_allowed_now": bool(lane_gate.get("paper_result_material_allowed_now")),
        "new_or_revised_contract_required_before_training": bool(
            lane_gate.get("new_or_revised_contract_required_before_training", True)
        ),
    }


def _lane_options(lane_matrix: dict[str, Any]) -> list[dict[str, Any]]:
    rows = lane_matrix.get("protocol_lane_evidence_matrix")
    if not isinstance(rows, list):
        rows = []
    out: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict) or not row.get("lane_id"):
            continue
        lane_id = str(row["lane_id"])
        out.append(
            {
                "lane_id": lane_id,
                "status": "awaiting_dr_sun_selection",
                "claim_scope": row.get("claim_scope"),
                "training_allowed_now": False,
                "requires_new_or_revised_contract": True,
                "required_decision_justification": _decision_justification(lane_id),
                "must_carry_into_contract": {
                    "required_contract_deltas": _strings(row.get("required_contract_deltas")),
                    "required_training_evidence": _strings(row.get("required_training_evidence")),
                    "required_evaluation_evidence": _strings(row.get("required_evaluation_evidence")),
                    "required_acceptance_evidence": _strings(row.get("required_acceptance_evidence")),
                    "invalid_substitutes": _strings(row.get("invalid_substitutes")),
                },
            }
        )
    return out


def _decision_justification(lane_id: str) -> list[str]:
    common = [
        "why this lane is justified after observing the failed warm-start Gate3 run",
        "which claim wording remains allowed if this lane is selected",
        "which prior failed artifacts are only negative evidence and cannot be reused as success evidence",
    ]
    lane_specific = {
        "stronger_obstacle_summary_warm_start": [
            "why direct PPO replacement is still plausible under compact obstacle-summary features",
        ],
        "full_patch_cnn_policy": [
            "why architecture/observation change is necessary and how it changes fairness against RS",
        ],
        "hybrid_ppo_analytic_fallback": [
            "whether the target claim changes from replacement to analytic-assisted hybrid control",
        ],
        "stop_or_reframe_module2_claim": [
            "why no new success-attempt training is warranted and what negative-result claim remains",
        ],
    }
    return [*common, *lane_specific.get(lane_id, [])]


def _decision_record_schema(lanes: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "record_id": "module2_protocol_lane_decision",
        "required_fields": [
            "decider",
            "decision_timestamp_utc",
            "selected_lane_id",
            "decision_summary",
            "justification_against_failed_gate3",
            "claim_scope_after_decision",
            "contract_action",
            "training_authorization",
        ],
        "valid_selected_lane_ids": [lane["lane_id"] for lane in lanes],
        "allowed_contract_actions": [
            "draft_new_contract",
            "draft_revised_contract",
            "stop_success_attempts_and_record_negative_evidence",
        ],
        "training_authorization_must_be": "not_authorized_by_this_decision_packet",
        "invalid_records": [
            "selected_lane_id outside valid_lane_ids",
            "training_authorization that starts local or remote training directly",
            "decision_summary that rewrites the failed Gate3 result as success",
            "claim_scope_after_decision that hides hybrid fallback usage",
        ],
    }


def _audit_issues(
    *,
    lane_matrix: dict[str, Any],
    contract_intake: dict[str, Any],
    gate: dict[str, Any],
    lanes: list[dict[str, Any]],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if lane_matrix.get("status") != "formal_gate_protocol_lane_matrix_ready":
        issues.append(_issue("lane_matrix_not_ready", "Protocol lane matrix must be ready before decision packet."))
    if contract_intake.get("status") != "formal_gate_contract_intake_ready_for_dr_sun":
        issues.append(_issue("contract_intake_not_ready", "Contract intake must be ready before decision packet."))
    if gate["current_formal_decision"] != "fail":
        issues.append(_issue("current_formal_decision_not_fail", "Decision packet expects a failed formal Gate3 run."))
    if gate["current_failure_mode"] != "threshold_failure":
        issues.append(_issue("current_failure_not_threshold_failure", "Decision packet expects threshold failure evidence."))
    if gate["new_success_training_allowed_now"] or gate["remote_training_allowed_now"]:
        issues.append(_issue("training_allowed_before_decision", "Decision packet must not authorize new success training."))
    if gate["local_training_allowed_now"]:
        issues.append(_issue("local_training_allowed", "Local PPO training must remain disallowed."))
    if gate["formal_claim_allowed_now"] or gate["paper_result_material_allowed_now"]:
        issues.append(_issue("claim_or_paper_result_allowed", "Formal claim and paper result material must remain blocked."))
    expected = {
        "stronger_obstacle_summary_warm_start",
        "full_patch_cnn_policy",
        "hybrid_ppo_analytic_fallback",
        "stop_or_reframe_module2_claim",
    }
    observed = {lane["lane_id"] for lane in lanes}
    if observed != expected:
        issues.append(_issue("valid_lane_set_mismatch", "Decision packet must expose the four protocol lanes."))
    for lane in lanes:
        lane_id = lane["lane_id"]
        evidence = lane["must_carry_into_contract"]
        if lane["training_allowed_now"]:
            issues.append(_issue(f"{lane_id}_training_allowed", "Lane option must not authorize training."))
        if not lane["required_decision_justification"]:
            issues.append(_issue(f"{lane_id}_missing_justification_requirements", "Lane option must define justification requirements."))
        if not evidence["required_contract_deltas"]:
            issues.append(_issue(f"{lane_id}_missing_contract_deltas", "Lane option must define contract deltas."))
        if not evidence["required_training_evidence"]:
            issues.append(_issue(f"{lane_id}_missing_training_evidence", "Lane option must define required training evidence."))
        if not evidence["required_evaluation_evidence"]:
            issues.append(_issue(f"{lane_id}_missing_evaluation_evidence", "Lane option must define required evaluation evidence."))
        if not evidence["required_acceptance_evidence"]:
            issues.append(_issue(f"{lane_id}_missing_acceptance_evidence", "Lane option must define required acceptance evidence."))
        if not evidence["invalid_substitutes"]:
            issues.append(_issue(f"{lane_id}_missing_invalid_substitutes", "Lane option must define invalid substitutes."))
    return _unique_issues(issues)


def _markdown(manifest: dict[str, Any]) -> str:
    gate = manifest["gate_summary"]
    lines = [
        "# Module2 Formal Gate Protocol Lane Decision Packet",
        "",
        "This file is a formal-gate decision packet, not paper result material.",
        "",
        "## Gate Summary",
        "",
        f"- current_formal_decision: `{gate['current_formal_decision']}`",
        f"- current_failure_mode: `{gate['current_failure_mode']}`",
        f"- terminal_rs_success_rate: `{gate['terminal_rs_success_rate']}`",
        f"- required_success_threshold: `{gate['required_success_threshold']}`",
        f"- new_success_training_allowed_now: `{gate['new_success_training_allowed_now']}`",
        f"- remote_training_allowed_now: `{gate['remote_training_allowed_now']}`",
        f"- local_training_allowed_now: `{gate['local_training_allowed_now']}`",
        f"- formal_claim_allowed_now: `{gate['formal_claim_allowed_now']}`",
        "",
        "## Valid Lane Decisions",
        "",
        "| lane | status | training_allowed_now |",
        "|---|---|---:|",
    ]
    for lane in manifest["lane_options"]:
        lines.append(f"| `{lane['lane_id']}` | `{lane['status']}` | `{lane['training_allowed_now']}` |")
    lines.extend(["", "## Decision Record Schema", ""])
    lines.append(f"- required_fields: `{', '.join(manifest['decision_record_schema']['required_fields'])}`")
    lines.append(f"- training_authorization_must_be: `{manifest['decision_record_schema']['training_authorization_must_be']}`")
    lines.extend(["", "## Current Blocked Actions"])
    for action in manifest["current_blocked_actions"]:
        lines.append(f"- `{action}`")
    lines.extend(["", "## Audit", "", f"- status: `{manifest['status']}`", f"- audit_issue_count: `{manifest['audit_issue_count']}`"])
    return "\n".join(lines) + "\n"


def _read_json(path: Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def _number(value: Any) -> float | None:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _strings(value: Any) -> list[str]:
    if not isinstance(value, (list, tuple)):
        return []
    return [str(item) for item in value if item]


def _issue(issue_id: str, message: str) -> dict[str, str]:
    return {"issue_id": issue_id, "message": message}


def _unique_issues(issues: Sequence[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    out: list[dict[str, str]] = []
    for issue in issues:
        issue_id = str(issue.get("issue_id") or "")
        if issue_id and issue_id not in seen:
            seen.add(issue_id)
            out.append(dict(issue))
    return out


if __name__ == "__main__":
    raise SystemExit(main())
