from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head
from forest_n3p.scripts.build_module2_v2_contract_readiness_gate import DEFAULT_CONTRACT_PATH


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_v2_contract_promotion_handoff_bundle")
DEFAULT_PROMOTION_READINESS = Path(
    "0_trials/module2_v2_contract_promotion_readiness_audit/v2_contract_promotion_readiness_audit.json"
)
DEFAULT_PROMOTION_PACKET = Path("0_trials/module2_v2_contract_promotion_packet/v2_contract_promotion_packet.json")
DEFAULT_PROMOTION_DRY_RUN = Path("0_trials/module2_v2_contract_promotion_dry_run/promotion_apply_dry_run.json")
DEFAULT_CHAIN_AUDIT = Path("0_trials/module2_v2_formal_gate_chain_audit/v2_formal_gate_chain_audit.json")
DEFAULT_POST_PROMOTION_PLAN = Path(
    "0_trials/module2_v2_post_promotion_regeneration_plan/v2_post_promotion_regeneration_plan.json"
)
DEFAULT_REMAINING_EVIDENCE = Path(
    "0_trials/module2_v2_formal_gate_remaining_evidence/v2_formal_gate_remaining_evidence.json"
)
READY_HANDOFF_STATUS = "ready_for_dr_sun_v2_contract_promotion_handoff"
BLOCKED_HANDOFF_STATUS = "v2_contract_promotion_handoff_blocked"
READY_READINESS_STATUS = "ready_for_dr_sun_v2_contract_promotion_decision"
READY_PACKET_STATUS = "v2_contract_promotion_packet_ready_awaiting_dr_sun"
READY_DRY_RUN_STATUS = "promotion_apply_ready"
EXPECTED_CHAIN_BLOCKER = "v2_contract_promoted"
EXPECTED_POST_PLAN_ACTION = "await_dr_sun_before_apply_v2_contract_promotion"
EXPECTED_APPROVAL_ITEM_IDS = {
    "remote_alias",
    "training_budget",
    "unsafe_failure_thresholds",
    "contract_status_action",
}


@dataclass(frozen=True)
class Module2V2ContractPromotionHandoffBundleConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    contract_path: Path = DEFAULT_CONTRACT_PATH
    promotion_readiness_path: Path = DEFAULT_PROMOTION_READINESS
    promotion_packet_path: Path = DEFAULT_PROMOTION_PACKET
    promotion_dry_run_path: Path = DEFAULT_PROMOTION_DRY_RUN
    chain_audit_path: Path = DEFAULT_CHAIN_AUDIT
    post_promotion_plan_path: Path = DEFAULT_POST_PROMOTION_PLAN
    remaining_evidence_path: Path = DEFAULT_REMAINING_EVIDENCE


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = Module2V2ContractPromotionHandoffBundleConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        contract_path=args.contract_path,
        promotion_readiness_path=args.promotion_readiness,
        promotion_packet_path=args.promotion_packet,
        promotion_dry_run_path=args.promotion_dry_run,
        chain_audit_path=args.chain_audit,
        post_promotion_plan_path=args.post_promotion_plan,
        remaining_evidence_path=args.remaining_evidence,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "v2_contract_promotion_handoff_bundle.json"
    markdown_out = config.markdown_out or output_dir / "v2_contract_promotion_handoff_bundle.md"
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


def build_manifest(config: Module2V2ContractPromotionHandoffBundleConfig) -> dict[str, Any]:
    contract_status = _contract_status(config.contract_path)
    readiness = _read_json(config.promotion_readiness_path)
    packet = _read_json(config.promotion_packet_path)
    dry_run = _read_json(config.promotion_dry_run_path)
    chain = _read_json(config.chain_audit_path)
    post_plan = _read_json(config.post_promotion_plan_path)
    remaining = _read_json(config.remaining_evidence_path)
    audit_issues = _audit_issues(
        contract_status=contract_status,
        readiness=readiness,
        packet=packet,
        dry_run=dry_run,
        chain=chain,
        post_plan=post_plan,
        remaining=remaining,
    )
    recommended_command = _recommended_apply_command(dry_run=dry_run, packet=packet)
    return {
        "schema_version": 1,
        "artifact_name": "module2_v2_contract_promotion_handoff_bundle",
        "status": READY_HANDOFF_STATUS if not audit_issues else BLOCKED_HANDOFF_STATUS,
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
            "promotion_readiness": str(config.promotion_readiness_path),
            "promotion_packet": str(config.promotion_packet_path),
            "promotion_dry_run": str(config.promotion_dry_run_path),
            "chain_audit": str(config.chain_audit_path),
            "post_promotion_plan": str(config.post_promotion_plan_path),
            "remaining_evidence": str(config.remaining_evidence_path),
        },
        "handoff_intent": {
            "selected_lane_id": _decision_state(remaining).get("selected_lane_id"),
            "contract_action": _decision_state(remaining).get("contract_action"),
            "contract_status_now": contract_status,
            "decision_required_from_dr_sun": readiness.get("decision_required_from_dr_sun") is True,
            "recommended_apply_command_for_future_explicit_approval": recommended_command,
            "recommended_apply_command_must_not_run_now": True,
            "why_not_run_now": "This bundle is a handoff checklist; applying promotion still requires Dr Sun's explicit approval in the current turn.",
        },
        "handoff_checks": _handoff_checks(
            contract_status=contract_status,
            readiness=readiness,
            packet=packet,
            dry_run=dry_run,
            chain=chain,
            post_plan=post_plan,
            remaining=remaining,
        ),
        "post_apply_required_commands": _post_apply_required_commands(),
        "remaining_evidence_summary": _remaining_evidence_summary(remaining),
        "invalid_substitutes": [
            "chat-only approval without committed contract frontmatter",
            "promotion packet alone as approval",
            "promotion dry-run alone as approval",
            "old v1 contract or old v1 remote packet",
            "failed gate3_obstacle_summary_warm_approved_v1 checkpoint",
            "remote preflight smoke before regenerated source-freshness and v2 packet gates",
            "local PPO training output",
            "paper prose, result table, or appendix text before H02 formal acceptance",
        ],
        "audit_issue_count": len(audit_issues),
        "audit_issues": audit_issues,
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a Module2 v2 contract promotion handoff bundle.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--contract-path", type=Path, default=DEFAULT_CONTRACT_PATH)
    parser.add_argument("--promotion-readiness", type=Path, default=DEFAULT_PROMOTION_READINESS)
    parser.add_argument("--promotion-packet", type=Path, default=DEFAULT_PROMOTION_PACKET)
    parser.add_argument("--promotion-dry-run", type=Path, default=DEFAULT_PROMOTION_DRY_RUN)
    parser.add_argument("--chain-audit", type=Path, default=DEFAULT_CHAIN_AUDIT)
    parser.add_argument("--post-promotion-plan", type=Path, default=DEFAULT_POST_PROMOTION_PLAN)
    parser.add_argument("--remaining-evidence", type=Path, default=DEFAULT_REMAINING_EVIDENCE)
    return parser.parse_args(list(argv) if argv is not None else None)


def _audit_issues(
    *,
    contract_status: str,
    readiness: dict[str, Any],
    packet: dict[str, Any],
    dry_run: dict[str, Any],
    chain: dict[str, Any],
    post_plan: dict[str, Any],
    remaining: dict[str, Any],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if contract_status != "draft":
        issues.append(_issue("contract_not_draft", observed=contract_status, expected="draft"))
    if readiness.get("status") != READY_READINESS_STATUS:
        issues.append(_issue("promotion_readiness_not_ready", observed=readiness.get("status"), expected=READY_READINESS_STATUS))
    if int(readiness.get("audit_issue_count") or 0) != 0:
        issues.append(_issue("promotion_readiness_has_audit_issues", observed=readiness.get("audit_issue_count"), expected=0))
    if readiness.get("decision_required_from_dr_sun") is not True:
        issues.append(_issue("readiness_does_not_require_dr_sun_decision", observed=readiness.get("decision_required_from_dr_sun"), expected=True))
    if packet.get("status") != READY_PACKET_STATUS:
        issues.append(_issue("promotion_packet_not_ready", observed=packet.get("status"), expected=READY_PACKET_STATUS))
    if int(packet.get("audit_issue_count") or 0) != 0:
        issues.append(_issue("promotion_packet_has_audit_issues", observed=packet.get("audit_issue_count"), expected=0))
    approval_item_ids = set(_approval_item_ids(packet))
    if approval_item_ids != EXPECTED_APPROVAL_ITEM_IDS:
        issues.append(_issue("promotion_packet_approval_items_incomplete", observed=sorted(approval_item_ids), expected=sorted(EXPECTED_APPROVAL_ITEM_IDS)))
    if dry_run.get("status") != READY_DRY_RUN_STATUS:
        issues.append(_issue("promotion_dry_run_not_ready", observed=dry_run.get("status"), expected=READY_DRY_RUN_STATUS))
    if dry_run.get("dry_run") is not True:
        issues.append(_issue("promotion_result_not_dry_run", observed=dry_run.get("dry_run"), expected=True))
    if dry_run.get("writes_contract") is not False:
        issues.append(_issue("promotion_dry_run_would_write_contract", observed=dry_run.get("writes_contract"), expected=False))
    if dry_run.get("promotion_apply_allowed") is not True:
        issues.append(_issue("promotion_apply_not_allowed_by_dry_run", observed=dry_run.get("promotion_apply_allowed"), expected=True))
    if chain.get("current_blocking_stage_id") != EXPECTED_CHAIN_BLOCKER:
        issues.append(_issue("chain_audit_not_blocked_at_contract_promotion", observed=chain.get("current_blocking_stage_id"), expected=EXPECTED_CHAIN_BLOCKER))
    if int(chain.get("audit_issue_count") or 0) != 0:
        issues.append(_issue("chain_audit_has_issues", observed=chain.get("audit_issue_count"), expected=0))
    if post_plan.get("next_action") != EXPECTED_POST_PLAN_ACTION:
        issues.append(_issue("post_promotion_plan_next_action_mismatch", observed=post_plan.get("next_action"), expected=EXPECTED_POST_PLAN_ACTION))
    permissions = remaining.get("permissions_now") if isinstance(remaining.get("permissions_now"), dict) else {}
    for key in (
        "local_training_allowed_now",
        "remote_preflight_allowed_now",
        "remote_training_allowed_now",
        "paper_result_material_allowed_now",
    ):
        if bool(readiness.get(key)) or bool(packet.get(key)) or bool(post_plan.get(key)) or bool(permissions.get(key)):
            issues.append(_issue(f"{key}_unexpectedly_allowed", observed=True, expected=False))
    return _unique_issues(issues)


def _handoff_checks(
    *,
    contract_status: str,
    readiness: dict[str, Any],
    packet: dict[str, Any],
    dry_run: dict[str, Any],
    chain: dict[str, Any],
    post_plan: dict[str, Any],
    remaining: dict[str, Any],
) -> list[dict[str, Any]]:
    return [
        _check("contract_remains_draft", contract_status == "draft", observed=contract_status, expected="draft"),
        _check("promotion_readiness_ready", readiness.get("status") == READY_READINESS_STATUS, observed=readiness.get("status"), expected=READY_READINESS_STATUS),
        _check("promotion_packet_ready", packet.get("status") == READY_PACKET_STATUS, observed=packet.get("status"), expected=READY_PACKET_STATUS),
        _check("promotion_packet_has_four_approval_items", set(_approval_item_ids(packet)) == EXPECTED_APPROVAL_ITEM_IDS, observed=sorted(_approval_item_ids(packet)), expected=sorted(EXPECTED_APPROVAL_ITEM_IDS)),
        _check("promotion_dry_run_ready_and_read_only", dry_run.get("status") == READY_DRY_RUN_STATUS and dry_run.get("dry_run") is True and dry_run.get("writes_contract") is False, observed={"status": dry_run.get("status"), "dry_run": dry_run.get("dry_run"), "writes_contract": dry_run.get("writes_contract")}, expected={"status": READY_DRY_RUN_STATUS, "dry_run": True, "writes_contract": False}),
        _check("chain_waits_at_contract_promotion", chain.get("current_blocking_stage_id") == EXPECTED_CHAIN_BLOCKER, observed=chain.get("current_blocking_stage_id"), expected=EXPECTED_CHAIN_BLOCKER),
        _check("post_promotion_plan_waits_for_dr_sun", post_plan.get("next_action") == EXPECTED_POST_PLAN_ACTION, observed=post_plan.get("next_action"), expected=EXPECTED_POST_PLAN_ACTION),
        _check("remaining_evidence_still_missing_before_training", _remaining_missing_total(remaining) > 0, observed=_remaining_missing_total(remaining), expected="> 0"),
    ]


def _recommended_apply_command(*, dry_run: dict[str, Any], packet: dict[str, Any]) -> str:
    target_status = str(dry_run.get("target_contract_status") or _contract_status_recommendation(packet) or "approved")
    inputs = dry_run.get("inputs") if isinstance(dry_run.get("inputs"), dict) else {}
    remote_alias = str(inputs.get("remote_alias") or _remote_alias_recommendation(packet) or "gpu3070ti-relay")
    return (
        "PYTHONPATH=2_experiment python -m forest_n3p.scripts.apply_module2_v2_contract_promotion "
        f"--status {target_status} --decider 'Dr Sun' --remote-alias {remote_alias} "
        "--confirm-training-budget --confirm-unsafe-failure-thresholds"
    )


def _post_apply_required_commands() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "rerun_v2_contract_readiness_gate",
            "command": "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_v2_contract_readiness_gate",
            "runs_training": False,
            "runs_remote_preflight": False,
        },
        {
            "step_id": "rerun_source_freshness_audit",
            "command": "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_source_freshness_audit",
            "runs_training": False,
            "runs_remote_preflight": False,
        },
        {
            "step_id": "regenerate_v2_remote_execution_packet",
            "command": "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_v2_remote_execution_packet",
            "runs_training": False,
            "runs_remote_preflight": False,
        },
        {
            "step_id": "refresh_v2_remaining_evidence",
            "command": "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_v2_formal_gate_remaining_evidence",
            "runs_training": False,
            "runs_remote_preflight": False,
        },
        {
            "step_id": "refresh_v2_formal_gate_chain_audit",
            "command": "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_v2_formal_gate_chain_audit",
            "runs_training": False,
            "runs_remote_preflight": False,
        },
        {
            "step_id": "refresh_post_promotion_regeneration_plan",
            "command": "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_v2_post_promotion_regeneration_plan",
            "runs_training": False,
            "runs_remote_preflight": False,
        },
    ]


def _remaining_evidence_summary(remaining: dict[str, Any]) -> dict[str, Any]:
    summary = remaining.get("remaining_evidence_summary")
    if not isinstance(summary, dict):
        return {}
    return {
        "total_required_evidence_items": summary.get("total_required_evidence_items"),
        "total_missing_or_unsatisfied": summary.get("total_missing_or_unsatisfied"),
        "training_missing_or_unsatisfied": summary.get("training_missing_or_unsatisfied"),
        "evaluation_missing_or_unsatisfied": summary.get("evaluation_missing_or_unsatisfied"),
        "acceptance_missing_or_unsatisfied": summary.get("acceptance_missing_or_unsatisfied"),
        "formal_acceptance_missing_or_unsatisfied": summary.get("formal_acceptance_missing_or_unsatisfied"),
    }


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 V2 Contract Promotion Handoff Bundle",
        "",
        "This artifact packages the next human decision boundary for the v2 stronger obstacle-summary warm-start contract. It does not approve the contract, write files, run remote preflight, train, or create paper result material.",
        "",
        "## Status",
        "",
        f"- status: `{manifest['status']}`",
        f"- contract_status_now: `{manifest['handoff_intent']['contract_status_now']}`",
        f"- selected_lane_id: `{manifest['handoff_intent']['selected_lane_id']}`",
        f"- contract_action: `{manifest['handoff_intent']['contract_action']}`",
        f"- audit_issue_count: `{manifest['audit_issue_count']}`",
        f"- remote_preflight_allowed_now: `{manifest['remote_preflight_allowed_now']}`",
        f"- remote_training_allowed_now: `{manifest['remote_training_allowed_now']}`",
        "",
        "## Future Apply Command",
        "",
        "Only run this after Dr Sun explicitly approves the promotion decision in the current gate.",
        "",
        "```bash",
        manifest["handoff_intent"]["recommended_apply_command_for_future_explicit_approval"],
        "```",
        "",
        "## Handoff Checks",
        "",
    ]
    for check in manifest["handoff_checks"]:
        lines.append(f"- {check['check_id']}: passed=`{check['passed']}` observed=`{check['observed']}` expected=`{check['expected']}`")
    lines.extend(["", "## Post-Apply Required Commands", ""])
    for step in manifest["post_apply_required_commands"]:
        lines.append(f"- {step['step_id']}: `{step['command']}`")
    lines.extend(["", "## Remaining Evidence Summary", ""])
    for key, value in manifest["remaining_evidence_summary"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Invalid Substitutes", ""])
    lines.extend(f"- {item}" for item in manifest["invalid_substitutes"])
    lines.extend(["", "## Audit Issues", ""])
    if manifest["audit_issues"]:
        lines.extend(f"- `{issue['issue_id']}`: observed=`{issue['observed']}`, expected=`{issue['expected']}`" for issue in manifest["audit_issues"])
    else:
        lines.append("- none")
    return "\n".join(lines) + "\n"


def _approval_item_ids(packet: dict[str, Any]) -> list[str]:
    return [str(item.get("item_id")) for item in packet.get("approval_items", []) if isinstance(item, dict)]


def _contract_status_recommendation(packet: dict[str, Any]) -> str | None:
    for item in packet.get("approval_items", []):
        if isinstance(item, dict) and item.get("item_id") == "contract_status_action":
            value = item.get("recommended_value")
            return str(value) if value else None
    return None


def _remote_alias_recommendation(packet: dict[str, Any]) -> str | None:
    for item in packet.get("approval_items", []):
        if isinstance(item, dict) and item.get("item_id") == "remote_alias":
            value = item.get("recommended_value")
            return str(value) if value else None
    evidence = packet.get("remote_alias_evidence")
    if isinstance(evidence, dict) and evidence.get("recommended_alias"):
        return str(evidence.get("recommended_alias"))
    return None


def _contract_status(path: Path) -> str:
    text = _read_text(path)
    for line in text.splitlines():
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing" if not path.exists() else "unknown"


def _decision_state(remaining: dict[str, Any]) -> dict[str, Any]:
    state = remaining.get("decision_state")
    return state if isinstance(state, dict) else {}


def _remaining_missing_total(remaining: dict[str, Any]) -> int:
    summary = remaining.get("remaining_evidence_summary")
    if not isinstance(summary, dict):
        return 0
    return int(summary.get("total_missing_or_unsatisfied") or 0)


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _issue(issue_id: str, *, observed: Any = None, expected: Any = None) -> dict[str, Any]:
    return {"issue_id": issue_id, "observed": observed, "expected": expected}


def _check(check_id: str, passed: bool, *, observed: Any, expected: Any) -> dict[str, Any]:
    return {"check_id": check_id, "passed": bool(passed), "observed": observed, "expected": expected}


def _unique_issues(issues: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for issue in issues:
        issue_id = str(issue.get("issue_id"))
        if issue_id not in seen:
            seen.add(issue_id)
            out.append(issue)
    return out


if __name__ == "__main__":
    raise SystemExit(main())
