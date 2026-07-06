from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head
from forest_n3p.scripts.build_module2_v2_contract_promotion_packet import DEFAULT_OUTPUT_DIR as DEFAULT_PACKET_DIR
from forest_n3p.scripts.build_module2_v2_contract_readiness_gate import DEFAULT_CONTRACT_PATH


DEFAULT_PROMOTION_PACKET = DEFAULT_PACKET_DIR / "v2_contract_promotion_packet.json"
READY_PACKET_STATUS = "v2_contract_promotion_packet_ready_awaiting_dr_sun"
READY_STATUSES = {"approved", "frozen"}
EXPECTED_DECIDER = "Dr Sun"


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    result = build_promotion_result(args)
    manifest_out = Path(args.manifest_out) if args.manifest_out else None
    if manifest_out is not None:
        manifest_out.parent.mkdir(parents=True, exist_ok=True)
        manifest_out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if result["promotion_apply_allowed"] and not bool(args.dry_run):
        Path(args.contract_path).write_text(result["promoted_contract_text"], encoding="utf-8")
    print(json.dumps(_print_summary(result, manifest_out), indent=2, ensure_ascii=False))
    return 0


def build_promotion_result(args: argparse.Namespace) -> dict[str, Any]:
    contract_path = Path(args.contract_path)
    packet_path = Path(args.promotion_packet)
    contract_text = _read_text(contract_path)
    packet = _read_json(packet_path)
    frontmatter = _frontmatter(contract_text)
    blockers = _blockers(args=args, contract_path=contract_path, packet=packet, frontmatter=frontmatter)
    warnings = _warnings(args=args, packet=packet)
    promoted_text = _promoted_contract_text(
        contract_text=contract_text,
        frontmatter=frontmatter,
        status=str(args.status),
        decider=str(args.decider),
        remote_alias=str(args.remote_alias),
        packet_path=packet_path,
    )
    allowed = not blockers
    return {
        "schema_version": 1,
        "artifact_name": "module2_v2_contract_promotion_apply",
        "status": "promotion_apply_ready" if allowed else "promotion_apply_blocked",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": module2_source_head(),
        "not_paper_result_material": True,
        "executes_training": False,
        "runs_remote_preflight": False,
        "runs_remote_training": False,
        "formal_claim_allowed_now": False,
        "paper_result_material_allowed_now": False,
        "dry_run": bool(args.dry_run),
        "writes_contract": bool(allowed and not bool(args.dry_run)),
        "promotion_apply_allowed": bool(allowed),
        "inputs": {
            "contract_path": str(contract_path),
            "promotion_packet": str(packet_path),
            "target_status": str(args.status),
            "decider": str(args.decider),
            "remote_alias": str(args.remote_alias),
            "confirm_training_budget": bool(args.confirm_training_budget),
            "confirm_unsafe_failure_thresholds": bool(args.confirm_unsafe_failure_thresholds),
        },
        "current_contract_status": frontmatter.get("status"),
        "target_contract_status": str(args.status),
        "current_packet_status": packet.get("status"),
        "recommended_remote_alias": _recommended_alias(packet),
        "blocker_count": len(blockers),
        "blockers": blockers,
        "warning_count": len(warnings),
        "warnings": warnings,
        "next_action_if_applied": [
            "commit the promoted contract",
            "re-run module2 v2 contract readiness gate",
            "regenerate source-freshness artifacts",
            "generate the v2 remote execution packet",
            "run remote preflight only after the regenerated packet allows it",
        ],
        "promoted_contract_text": promoted_text,
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply or dry-run the Module2 v2 contract status promotion after Dr Sun approval.")
    parser.add_argument("--contract-path", type=Path, default=DEFAULT_CONTRACT_PATH)
    parser.add_argument("--promotion-packet", type=Path, default=DEFAULT_PROMOTION_PACKET)
    parser.add_argument("--status", choices=sorted(READY_STATUSES), required=True)
    parser.add_argument("--decider", required=True)
    parser.add_argument("--remote-alias", required=True)
    parser.add_argument("--confirm-training-budget", action="store_true")
    parser.add_argument("--confirm-unsafe-failure-thresholds", action="store_true")
    parser.add_argument("--allow-nonrecommended-alias", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--manifest-out", type=Path, default=None)
    return parser.parse_args(list(argv) if argv is not None else None)


def _blockers(
    *,
    args: argparse.Namespace,
    contract_path: Path,
    packet: dict[str, Any],
    frontmatter: dict[str, Any],
) -> list[dict[str, Any]]:
    blockers: list[dict[str, Any]] = []
    if not contract_path.exists():
        blockers.append(_issue("contract_missing", "contract file is missing", observed=str(contract_path)))
    if packet.get("status") != READY_PACKET_STATUS:
        blockers.append(
            _issue(
                "promotion_packet_not_ready",
                "promotion packet must be ready and awaiting Dr Sun before applying",
                observed=packet.get("status"),
                expected=READY_PACKET_STATUS,
            )
        )
    if int(packet.get("audit_issue_count", -1)) != 0:
        blockers.append(
            _issue(
                "promotion_packet_has_audit_issues",
                "promotion packet must have zero audit issues",
                observed=packet.get("audit_issue_count"),
                expected=0,
            )
        )
    if str(frontmatter.get("status")) != "draft":
        blockers.append(
            _issue(
                "contract_not_draft",
                "promotion apply expects the current contract to be draft",
                observed=frontmatter.get("status"),
                expected="draft",
            )
        )
    if str(args.decider) != EXPECTED_DECIDER:
        blockers.append(_issue("decider_not_dr_sun", "only Dr Sun can approve or freeze the v2 contract", observed=str(args.decider)))
    if str(args.status) not in READY_STATUSES:
        blockers.append(_issue("target_status_invalid", "target status must be approved or frozen", observed=str(args.status)))
    recommended_alias = _recommended_alias(packet)
    if str(args.remote_alias) != recommended_alias and not bool(args.allow_nonrecommended_alias):
        blockers.append(
            _issue(
                "remote_alias_not_recommended",
                "remote alias differs from the promotion packet recommendation",
                observed=str(args.remote_alias),
                expected=recommended_alias,
            )
        )
    if not bool(args.confirm_training_budget):
        blockers.append(_issue("training_budget_not_confirmed", "Dr Sun must confirm the locked v2 training budget"))
    if not bool(args.confirm_unsafe_failure_thresholds):
        blockers.append(_issue("unsafe_failure_thresholds_not_confirmed", "Dr Sun must confirm independent unsafe-rollout failure thresholds"))
    return _unique_issues(blockers)


def _warnings(*, args: argparse.Namespace, packet: dict[str, Any]) -> list[dict[str, Any]]:
    warnings: list[dict[str, Any]] = []
    recommended_alias = _recommended_alias(packet)
    if str(args.remote_alias) != recommended_alias and bool(args.allow_nonrecommended_alias):
        warnings.append(
            _issue(
                "nonrecommended_alias_allowed",
                "non-recommended alias was explicitly allowed; remote readiness must be regenerated before any remote preflight",
                observed=str(args.remote_alias),
                expected=recommended_alias,
            )
        )
    if str(args.status) == "frozen":
        warnings.append(_issue("frozen_contract_requires_successor_for_edits", "future changes require a successor contract"))
    return warnings


def _promoted_contract_text(
    *,
    contract_text: str,
    frontmatter: dict[str, Any],
    status: str,
    decider: str,
    remote_alias: str,
    packet_path: Path,
) -> str:
    if not contract_text.startswith("---\n"):
        return contract_text
    lines = contract_text.splitlines()
    end_idx = _frontmatter_end_index(lines)
    if end_idx is None:
        return contract_text
    new_frontmatter = dict(frontmatter)
    new_frontmatter["status"] = status
    new_frontmatter["promotion_decider"] = decider
    new_frontmatter["approved_remote_alias"] = remote_alias
    new_frontmatter["promotion_packet"] = str(packet_path)
    new_frontmatter["contract_approved_for_source_freshness"] = True
    rendered = _render_frontmatter(new_frontmatter)
    return "\n".join(["---", *rendered, "---", *lines[end_idx + 1 :]]) + "\n"


def _frontmatter(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end_idx = _frontmatter_end_index(lines)
    if end_idx is None:
        return {}
    values: dict[str, Any] = {}
    current_list_key: str | None = None
    for line in lines[1:end_idx]:
        stripped = line.strip()
        if stripped.startswith("- ") and current_list_key:
            values.setdefault(current_list_key, []).append(stripped[2:].strip())
            continue
        current_list_key = None
        if ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if raw_value:
            values[key] = _parse_scalar(raw_value)
        else:
            values[key] = []
            current_list_key = key
    return values


def _render_frontmatter(values: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for key, value in values.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            lines.extend(f"  - {item}" for item in value)
        elif isinstance(value, bool):
            lines.append(f"{key}: {str(value).lower()}")
        else:
            lines.append(f"{key}: {value}")
    return lines


def _frontmatter_end_index(lines: Sequence[str]) -> int | None:
    for idx, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return idx
    return None


def _parse_scalar(value: str) -> Any:
    lower = value.lower()
    if lower == "true":
        return True
    if lower == "false":
        return False
    return value


def _recommended_alias(packet: dict[str, Any]) -> str:
    evidence = packet.get("remote_alias_evidence") if isinstance(packet.get("remote_alias_evidence"), dict) else {}
    return str(evidence.get("recommended_alias") or "")


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _issue(issue_id: str, message: str, *, observed: Any | None = None, expected: Any | None = None) -> dict[str, Any]:
    issue = {"issue_id": issue_id, "message": message}
    if observed is not None:
        issue["observed"] = observed
    if expected is not None:
        issue["expected"] = expected
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


def _print_summary(result: dict[str, Any], manifest_out: Path | None) -> dict[str, Any]:
    return {
        "status": result["status"],
        "dry_run": result["dry_run"],
        "writes_contract": result["writes_contract"],
        "blocker_count": result["blocker_count"],
        "manifest": None if manifest_out is None else str(manifest_out),
    }


if __name__ == "__main__":
    raise SystemExit(main())
