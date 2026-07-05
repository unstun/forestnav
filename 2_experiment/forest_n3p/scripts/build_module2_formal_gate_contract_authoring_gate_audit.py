from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_formal_gate_contract_authoring_gate_audit")
DEFAULT_DECISION_GATE_AUDIT = Path(
    "0_trials/module2_formal_gate_protocol_lane_decision_gate_audit/protocol_lane_decision_gate_audit.json"
)
DEFAULT_DECISION_RECORD = Path(
    "0_trials/module2_formal_gate_protocol_lane_decision_record/protocol_lane_decision_record.json"
)
DEFAULT_CONTRACT_INTAKE = Path("0_trials/module2_formal_gate_contract_intake/formal_gate_contract_intake.json")
DEFAULT_NEXT_ROUND_REQUIREMENTS = Path(
    "0_trials/module2_formal_gate_next_round_requirements/formal_gate_next_round_requirements.json"
)
DEFAULT_EXISTING_CONTRACT = Path(".pipeline/contracts/module2-ppo-funnel-expansion.md")
PENDING_DECISION_STATUS = "pending_protocol_lane_decision"
RECORDED_DECISION_STATUS = "protocol_lane_decision_recorded"
PENDING_GATE_STATUS = "protocol_lane_decision_gate_pending_clean"
RECORDED_GATE_STATUS = "protocol_lane_decision_gate_recorded_clean"


@dataclass(frozen=True)
class FormalGateContractAuthoringGateAuditConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    decision_gate_audit_path: Path = DEFAULT_DECISION_GATE_AUDIT
    decision_record_path: Path = DEFAULT_DECISION_RECORD
    contract_intake_path: Path = DEFAULT_CONTRACT_INTAKE
    next_round_requirements_path: Path = DEFAULT_NEXT_ROUND_REQUIREMENTS
    existing_contract_path: Path = DEFAULT_EXISTING_CONTRACT


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = FormalGateContractAuthoringGateAuditConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        decision_gate_audit_path=args.decision_gate_audit,
        decision_record_path=args.decision_record,
        contract_intake_path=args.contract_intake,
        next_round_requirements_path=args.next_round_requirements,
        existing_contract_path=args.existing_contract,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "contract_authoring_gate_audit.json"
    markdown_out = config.markdown_out or output_dir / "contract_authoring_gate_audit.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: FormalGateContractAuthoringGateAuditConfig) -> dict[str, Any]:
    decision_gate = _read_json(config.decision_gate_audit_path)
    decision_record = _read_json(config.decision_record_path)
    contract_intake = _read_json(config.contract_intake_path)
    next_round = _read_json(config.next_round_requirements_path)
    existing_contract = _contract_summary(config.existing_contract_path)
    contract_gate = _contract_gate(
        decision_gate=decision_gate,
        decision_record=decision_record,
        contract_intake=contract_intake,
        next_round=next_round,
        existing_contract=existing_contract,
    )
    issues = _audit_issues(
        decision_gate=decision_gate,
        decision_record=decision_record,
        contract_intake=contract_intake,
        next_round=next_round,
        existing_contract=existing_contract,
        contract_gate=contract_gate,
    )
    return {
        "schema_version": 1,
        "artifact_name": "module2_formal_gate_contract_authoring_gate_audit",
        "status": _status(issues=issues, contract_gate=contract_gate),
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
            "protocol_lane_decision_gate_audit": str(config.decision_gate_audit_path),
            "protocol_lane_decision_record": str(config.decision_record_path),
            "contract_intake": str(config.contract_intake_path),
            "next_round_requirements": str(config.next_round_requirements_path),
            "existing_contract": str(config.existing_contract_path),
        },
        "contract_gate": contract_gate,
        "existing_contract_summary": existing_contract,
        "required_contract_sections": _required_contract_sections(contract_intake),
        "audit_issue_count": len(issues),
        "audit_issues": issues,
        "claim_boundaries": [
            "This audit gates contract authoring after the protocol-lane decision; it does not draft or approve a contract.",
            "The approved v1 contract is historical input only and cannot authorize a new success attempt after the failed warm-start Gate3 run.",
            "A clean pending audit still blocks contract drafting, remote training, formal claims, and paper result material.",
            "A recorded lane decision can only open contract drafting, not training; training still requires an approved/frozen new or revised contract plus later gates.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit Module2 contract-authoring gate after protocol-lane decision state.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--decision-gate-audit", type=Path, default=DEFAULT_DECISION_GATE_AUDIT)
    parser.add_argument("--decision-record", type=Path, default=DEFAULT_DECISION_RECORD)
    parser.add_argument("--contract-intake", type=Path, default=DEFAULT_CONTRACT_INTAKE)
    parser.add_argument("--next-round-requirements", type=Path, default=DEFAULT_NEXT_ROUND_REQUIREMENTS)
    parser.add_argument("--existing-contract", type=Path, default=DEFAULT_EXISTING_CONTRACT)
    return parser.parse_args(list(argv) if argv is not None else None)


def _contract_gate(
    *,
    decision_gate: dict[str, Any],
    decision_record: dict[str, Any],
    contract_intake: dict[str, Any],
    next_round: dict[str, Any],
    existing_contract: dict[str, Any],
) -> dict[str, Any]:
    record_status = decision_record.get("status")
    selected_lane = decision_record.get("selected_lane_id")
    decision_gate_status = decision_gate.get("status")
    pending = record_status == PENDING_DECISION_STATUS
    recorded = record_status == RECORDED_DECISION_STATUS
    return {
        "decision_gate_status": decision_gate_status,
        "decision_record_status": record_status,
        "selected_lane_id": selected_lane,
        "contract_action": decision_record.get("contract_action"),
        "contract_intake_status": contract_intake.get("status"),
        "next_round_requirements_status": next_round.get("status"),
        "existing_contract_status": existing_contract.get("status"),
        "existing_contract_version": existing_contract.get("version"),
        "existing_contract_usable_for_new_success_attempt": False,
        "contract_drafting_allowed_now": bool(recorded and decision_gate_status == RECORDED_GATE_STATUS),
        "contract_approval_allowed_now": False,
        "draft_contract_allows_training": False,
        "new_or_revised_contract_required_before_training": True,
        "allowed_next_action_ids": ["record_protocol_lane_decision"] if pending else ["draft_new_or_revised_contract_after_lane_decision"],
        "blocked_action_ids": [
            "local_training",
            "remote_success_training",
            "remote_preflight_for_new_success_attempt",
            "formal_claim",
            "paper_result_material",
        ],
    }


def _status(*, issues: list[dict[str, Any]], contract_gate: dict[str, Any]) -> str:
    if issues:
        return "contract_authoring_gate_audit_failed"
    if contract_gate["decision_record_status"] == PENDING_DECISION_STATUS:
        return "contract_authoring_gate_blocked_pending_lane_decision"
    if contract_gate["contract_drafting_allowed_now"]:
        return "contract_authoring_gate_ready_for_contract_draft"
    return "contract_authoring_gate_blocked_unknown"


def _audit_issues(
    *,
    decision_gate: dict[str, Any],
    decision_record: dict[str, Any],
    contract_intake: dict[str, Any],
    next_round: dict[str, Any],
    existing_contract: dict[str, Any],
    contract_gate: dict[str, Any],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if decision_gate.get("status") not in {PENDING_GATE_STATUS, RECORDED_GATE_STATUS}:
        issues.append(_issue("decision_gate_not_clean", "Protocol-lane decision gate must be clean before contract authoring audit.", observed=decision_gate.get("status")))
    if decision_record.get("status") not in {PENDING_DECISION_STATUS, RECORDED_DECISION_STATUS}:
        issues.append(_issue("decision_record_unknown_status", "Protocol-lane decision record must be pending or recorded.", observed=decision_record.get("status")))
    if contract_intake.get("status") != "formal_gate_contract_intake_ready_for_dr_sun":
        issues.append(_issue("contract_intake_not_ready", "Contract intake must be ready before contract authoring gate."))
    if next_round.get("status") != "formal_gate_next_round_requirements_ready":
        issues.append(_issue("next_round_requirements_not_ready", "Next-round requirements must be ready before contract authoring gate."))
    for key in ("runs_training", "runs_remote_preflight", "formal_claim_allowed"):
        if decision_record.get(key) is not False:
            issues.append(_issue(f"decision_record_{key}_not_false", f"Decision record must keep {key}=false.", observed=decision_record.get(key)))
    for key in ("remote_training_allowed_now", "local_training_allowed_now", "formal_claim_allowed_now", "paper_result_material_allowed_now"):
        if decision_record.get(key) is not False:
            issues.append(_issue(f"decision_record_{key}_not_false", f"Decision record must keep {key}=false.", observed=decision_record.get(key)))
    if contract_gate["decision_record_status"] == PENDING_DECISION_STATUS:
        if contract_gate["selected_lane_id"] is not None:
            issues.append(_issue("pending_decision_has_selected_lane", "Pending decision must not select a protocol lane.", observed=contract_gate["selected_lane_id"]))
        if contract_gate["contract_action"] != "none":
            issues.append(_issue("pending_decision_has_contract_action", "Pending decision must not choose a contract action.", observed=contract_gate["contract_action"]))
        if contract_gate["contract_drafting_allowed_now"]:
            issues.append(_issue("contract_drafting_allowed_while_lane_pending", "Contract drafting must remain blocked while lane decision is pending."))
    if contract_gate["decision_record_status"] == RECORDED_DECISION_STATUS:
        if not contract_gate["selected_lane_id"]:
            issues.append(_issue("recorded_decision_missing_selected_lane", "Recorded decision must include selected_lane_id."))
        if contract_gate["contract_action"] == "none":
            issues.append(_issue("recorded_decision_missing_contract_action", "Recorded decision must choose a contract action."))
    if contract_gate["contract_approval_allowed_now"]:
        issues.append(_issue("contract_approval_allowed_too_early", "This gate may allow drafting, not approval."))
    if contract_gate["draft_contract_allows_training"]:
        issues.append(_issue("draft_contract_allows_training", "Draft contract must not authorize training."))
    if existing_contract.get("status") == "approved" and existing_contract.get("usable_for_new_success_attempt") is True:
        issues.append(_issue("existing_contract_misused_for_new_attempt", "Existing approved v1 contract must not authorize the new success attempt."))
    return _unique_issues(issues)


def _contract_summary(path: Path) -> dict[str, Any]:
    p = Path(path)
    frontmatter = _frontmatter(p)
    return {
        "path": str(path),
        "exists": p.is_file(),
        "status": frontmatter.get("status"),
        "version": frontmatter.get("version"),
        "approved_by": frontmatter.get("approved_by"),
        "approved_date": frontmatter.get("approved_date"),
        "origin": frontmatter.get("origin"),
        "reviewed": _bool(frontmatter.get("reviewed")),
        "usable_for_new_success_attempt": False,
        "reason_not_sufficient": "v1 predates the failed warm-start Gate3 result and cannot encode the required protocol-lane decision",
    }


def _frontmatter(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    out: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, value = line.split(":", 1)
            out[key.strip()] = value.strip()
    return out


def _required_contract_sections(contract_intake: dict[str, Any]) -> list[str]:
    output = contract_intake.get("contract_output_requirements")
    if not isinstance(output, dict):
        return []
    return _strings(output.get("required_sections"))


def _markdown(manifest: dict[str, Any]) -> str:
    gate = manifest["contract_gate"]
    lines = [
        "# Module2 Formal Gate Contract Authoring Gate Audit",
        "",
        "This file audits whether contract authoring may proceed; it is not paper result material.",
        "",
        "## Contract Gate",
        "",
        f"- decision_record_status: `{gate['decision_record_status']}`",
        f"- selected_lane_id: `{gate['selected_lane_id']}`",
        f"- contract_action: `{gate['contract_action']}`",
        f"- contract_drafting_allowed_now: `{gate['contract_drafting_allowed_now']}`",
        f"- contract_approval_allowed_now: `{gate['contract_approval_allowed_now']}`",
        f"- draft_contract_allows_training: `{gate['draft_contract_allows_training']}`",
        "",
        "## Existing Contract",
        "",
        f"- status: `{manifest['existing_contract_summary']['status']}`",
        f"- version: `{manifest['existing_contract_summary']['version']}`",
        f"- usable_for_new_success_attempt: `{manifest['existing_contract_summary']['usable_for_new_success_attempt']}`",
        "",
        "## Audit",
        "",
        f"- status: `{manifest['status']}`",
        f"- audit_issue_count: `{manifest['audit_issue_count']}`",
    ]
    return "\n".join(lines) + "\n"


def _read_json(path: Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def _bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "1"}:
            return True
        if lowered in {"false", "no", "0"}:
            return False
    return None


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
