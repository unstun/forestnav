from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head
from forest_n3p.scripts.build_module2_v2_contract_readiness_gate import DEFAULT_CONTRACT_PATH


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_v2_contract_promotion_readiness_audit")
DEFAULT_PROMOTION_PACKET = Path("0_trials/module2_v2_contract_promotion_packet/v2_contract_promotion_packet.json")
DEFAULT_PROMOTION_DRY_RUN = Path("0_trials/module2_v2_contract_promotion_dry_run/promotion_apply_dry_run.json")
DEFAULT_CHAIN_AUDIT = Path("0_trials/module2_v2_formal_gate_chain_audit/v2_formal_gate_chain_audit.json")
DEFAULT_POST_PROMOTION_PLAN = Path(
    "0_trials/module2_v2_post_promotion_regeneration_plan/v2_post_promotion_regeneration_plan.json"
)
READY_PACKET_STATUS = "v2_contract_promotion_packet_ready_awaiting_dr_sun"
READY_DRY_RUN_STATUS = "promotion_apply_ready"
EXPECTED_APPROVAL_ITEMS = {
    "remote_alias",
    "training_budget",
    "unsafe_failure_thresholds",
    "contract_status_action",
}


@dataclass(frozen=True)
class Module2V2ContractPromotionReadinessAuditConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    contract_path: Path = DEFAULT_CONTRACT_PATH
    promotion_packet_path: Path = DEFAULT_PROMOTION_PACKET
    promotion_dry_run_path: Path = DEFAULT_PROMOTION_DRY_RUN
    chain_audit_path: Path = DEFAULT_CHAIN_AUDIT
    post_promotion_plan_path: Path = DEFAULT_POST_PROMOTION_PLAN


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = Module2V2ContractPromotionReadinessAuditConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        contract_path=args.contract_path,
        promotion_packet_path=args.promotion_packet,
        promotion_dry_run_path=args.promotion_dry_run,
        chain_audit_path=args.chain_audit,
        post_promotion_plan_path=args.post_promotion_plan,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "v2_contract_promotion_readiness_audit.json"
    markdown_out = config.markdown_out or output_dir / "v2_contract_promotion_readiness_audit.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: Module2V2ContractPromotionReadinessAuditConfig) -> dict[str, Any]:
    contract_status = _contract_status(config.contract_path)
    packet = _read_json(config.promotion_packet_path)
    dry_run = _read_json(config.promotion_dry_run_path)
    chain = _read_json(config.chain_audit_path)
    post_plan = _read_json(config.post_promotion_plan_path)
    audit_issues = _audit_issues(
        contract_status=contract_status,
        packet=packet,
        dry_run=dry_run,
        chain=chain,
        post_plan=post_plan,
    )
    return {
        "schema_version": 1,
        "artifact_name": "module2_v2_contract_promotion_readiness_audit",
        "status": _status(contract_status=contract_status, audit_issues=audit_issues),
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": module2_source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "writes_contract": False,
        "approves_contract": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "runs_remote_audit": False,
        "local_training_allowed_now": False,
        "remote_preflight_allowed_now": False,
        "remote_training_allowed_now": False,
        "formal_claim_allowed_now": False,
        "paper_result_material_allowed_now": False,
        "inputs": {
            "contract": str(config.contract_path),
            "promotion_packet": str(config.promotion_packet_path),
            "promotion_dry_run": str(config.promotion_dry_run_path),
            "chain_audit": str(config.chain_audit_path),
            "post_promotion_plan": str(config.post_promotion_plan_path),
        },
        "contract_status": contract_status,
        "readiness_summary": {
            "promotion_packet_status": packet.get("status"),
            "promotion_packet_audit_issue_count": int(packet.get("audit_issue_count") or 0),
            "approval_item_ids": _approval_item_ids(packet),
            "promotion_dry_run_status": dry_run.get("status"),
            "promotion_dry_run_writes_contract": bool(dry_run.get("writes_contract")),
            "promotion_dry_run_target_status": dry_run.get("target_contract_status"),
            "chain_audit_status": chain.get("status"),
            "chain_current_blocking_stage_id": chain.get("current_blocking_stage_id"),
            "post_promotion_plan_status": post_plan.get("status"),
            "post_promotion_next_action": post_plan.get("next_action"),
        },
        "decision_required_from_dr_sun": contract_status == "draft" and not audit_issues,
        "recommended_decision_payload": _recommended_decision_payload(packet=packet, dry_run=dry_run),
        "post_decision_required_first_steps": [
            "apply and commit the v2 contract promotion",
            "re-run v2 contract readiness gate",
            "re-run source freshness audit",
            "regenerate v2 remote execution packet",
            "refresh v2 formal gate chain audit",
        ],
        "audit_issue_count": len(audit_issues),
        "audit_issues": audit_issues,
        "invalid_substitutes": [
            "promotion packet alone as approval",
            "promotion dry-run alone as approval",
            "chat-only approval without committed contract frontmatter",
            "remote preflight before source freshness and v2 packet regeneration",
            "remote training before ready preflight manifest",
            "paper result material before H02 formal acceptance",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit whether Module2 v2 contract promotion is ready for Dr Sun decision.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--contract-path", type=Path, default=DEFAULT_CONTRACT_PATH)
    parser.add_argument("--promotion-packet", type=Path, default=DEFAULT_PROMOTION_PACKET)
    parser.add_argument("--promotion-dry-run", type=Path, default=DEFAULT_PROMOTION_DRY_RUN)
    parser.add_argument("--chain-audit", type=Path, default=DEFAULT_CHAIN_AUDIT)
    parser.add_argument("--post-promotion-plan", type=Path, default=DEFAULT_POST_PROMOTION_PLAN)
    return parser.parse_args(list(argv) if argv is not None else None)


def _audit_issues(
    *,
    contract_status: str,
    packet: dict[str, Any],
    dry_run: dict[str, Any],
    chain: dict[str, Any],
    post_plan: dict[str, Any],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if contract_status != "draft":
        issues.append(_issue("contract_not_draft", observed=contract_status, expected="draft"))
    if packet.get("status") != READY_PACKET_STATUS:
        issues.append(_issue("promotion_packet_not_ready", observed=packet.get("status"), expected=READY_PACKET_STATUS))
    if int(packet.get("audit_issue_count") or 0) != 0:
        issues.append(_issue("promotion_packet_has_audit_issues", observed=packet.get("audit_issue_count"), expected=0))
    approval_items = set(_approval_item_ids(packet))
    if approval_items != EXPECTED_APPROVAL_ITEMS:
        issues.append(_issue("promotion_packet_approval_items_incomplete", observed=sorted(approval_items), expected=sorted(EXPECTED_APPROVAL_ITEMS)))
    if dry_run.get("status") != READY_DRY_RUN_STATUS:
        issues.append(_issue("promotion_dry_run_not_ready", observed=dry_run.get("status"), expected=READY_DRY_RUN_STATUS))
    if dry_run.get("dry_run") is not True:
        issues.append(_issue("promotion_result_not_dry_run", observed=dry_run.get("dry_run"), expected=True))
    if dry_run.get("writes_contract") is not False:
        issues.append(_issue("promotion_dry_run_would_write_contract", observed=dry_run.get("writes_contract"), expected=False))
    if dry_run.get("promotion_apply_allowed") is not True:
        issues.append(_issue("promotion_apply_not_allowed_by_dry_run", observed=dry_run.get("promotion_apply_allowed"), expected=True))
    if dry_run.get("blocker_count") not in (0, None):
        issues.append(_issue("promotion_dry_run_has_blockers", observed=dry_run.get("blocker_count"), expected=0))
    if chain.get("current_blocking_stage_id") != "v2_contract_promoted":
        issues.append(_issue("chain_audit_not_blocked_at_contract_promotion", observed=chain.get("current_blocking_stage_id"), expected="v2_contract_promoted"))
    if int(chain.get("audit_issue_count") or 0) != 0:
        issues.append(_issue("chain_audit_has_issues", observed=chain.get("audit_issue_count"), expected=0))
    if post_plan.get("next_action") != "await_dr_sun_before_apply_v2_contract_promotion":
        issues.append(
            _issue(
                "post_promotion_plan_next_action_mismatch",
                observed=post_plan.get("next_action"),
                expected="await_dr_sun_before_apply_v2_contract_promotion",
            )
        )
    if post_plan.get("remote_training_allowed_now") is True:
        issues.append(_issue("post_promotion_plan_allows_remote_training", observed=True, expected=False))
    return _unique_issues(issues)


def _status(*, contract_status: str, audit_issues: Sequence[dict[str, Any]]) -> str:
    if audit_issues:
        return "v2_contract_promotion_readiness_audit_failed"
    if contract_status == "draft":
        return "ready_for_dr_sun_v2_contract_promotion_decision"
    return "v2_contract_already_promoted_or_unexpected_status"


def _recommended_decision_payload(*, packet: dict[str, Any], dry_run: dict[str, Any]) -> dict[str, Any]:
    items = {str(item.get("item_id")): item for item in packet.get("approval_items", []) if isinstance(item, dict)}
    return {
        "target_status": dry_run.get("target_contract_status") or items.get("contract_status_action", {}).get("recommended_value"),
        "remote_alias": dry_run.get("inputs", {}).get("remote_alias") if isinstance(dry_run.get("inputs"), dict) else None,
        "training_budget": items.get("training_budget", {}).get("recommended_value"),
        "unsafe_failure_thresholds": items.get("unsafe_failure_thresholds", {}).get("recommended_value"),
    }


def _approval_item_ids(packet: dict[str, Any]) -> list[str]:
    return [str(item.get("item_id")) for item in packet.get("approval_items", []) if isinstance(item, dict)]


def _contract_status(path: Path) -> str:
    text = _read_text(path)
    for line in text.splitlines():
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing" if not path.exists() else "unknown"


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _issue(issue_id: str, *, observed: Any = None, expected: Any = None) -> dict[str, Any]:
    return {"issue_id": issue_id, "observed": observed, "expected": expected}


def _unique_issues(issues: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for issue in issues:
        issue_id = str(issue.get("issue_id"))
        if issue_id not in seen:
            seen.add(issue_id)
            out.append(issue)
    return out


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 V2 Contract Promotion Readiness Audit",
        "",
        "This artifact audits whether the v2 contract promotion packet is ready for Dr Sun's explicit decision. It does not approve the contract, write files, run preflight, train, or write paper results.",
        "",
        "## Status",
        "",
        f"- status: `{manifest['status']}`",
        f"- contract_status: `{manifest['contract_status']}`",
        f"- decision_required_from_dr_sun: `{manifest['decision_required_from_dr_sun']}`",
        f"- audit_issue_count: `{manifest['audit_issue_count']}`",
        f"- remote_training_allowed_now: `{manifest['remote_training_allowed_now']}`",
        "",
        "## Readiness Summary",
        "",
    ]
    for key, value in manifest["readiness_summary"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Recommended Decision Payload", ""])
    for key, value in manifest["recommended_decision_payload"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Audit Issues", ""])
    if manifest["audit_issues"]:
        lines.extend(f"- `{issue['issue_id']}`: observed=`{issue['observed']}`, expected=`{issue['expected']}`" for issue in manifest["audit_issues"])
    else:
        lines.append("- none")
    lines.extend(["", "## Invalid Substitutes", ""])
    lines.extend(f"- {item}" for item in manifest["invalid_substitutes"])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
