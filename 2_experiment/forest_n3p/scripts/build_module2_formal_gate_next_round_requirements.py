from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_formal_gate_next_round_requirements")
DEFAULT_FAILURE_TRIAGE = Path("0_trials/module2_formal_gate_failure_triage/formal_gate_failure_triage.json")
DEFAULT_REMAINING_DELIVERABLES = Path(
    "0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json"
)
DEFAULT_H02_ACCEPTANCE = Path("0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json")
DEFAULT_STATUS_REPORT = Path("0_trials/module2_formal_gate_status_report/formal_gate_status_report.json")
DEFAULT_GATE3_AUDIT = Path(
    "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json"
)


@dataclass(frozen=True)
class FormalGateNextRoundRequirementsConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    failure_triage_path: Path = DEFAULT_FAILURE_TRIAGE
    remaining_deliverables_path: Path = DEFAULT_REMAINING_DELIVERABLES
    h02_acceptance_path: Path = DEFAULT_H02_ACCEPTANCE
    status_report_path: Path = DEFAULT_STATUS_REPORT
    gate3_audit_path: Path = DEFAULT_GATE3_AUDIT


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = FormalGateNextRoundRequirementsConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        failure_triage_path=args.failure_triage,
        remaining_deliverables_path=args.remaining_deliverables,
        h02_acceptance_path=args.h02_acceptance,
        status_report_path=args.status_report,
        gate3_audit_path=args.gate3_audit,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "formal_gate_next_round_requirements.json"
    markdown_out = config.markdown_out or output_dir / "formal_gate_next_round_requirements.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: FormalGateNextRoundRequirementsConfig) -> dict[str, Any]:
    failure_triage = _read_json(config.failure_triage_path)
    remaining = _read_json(config.remaining_deliverables_path)
    h02 = _read_json(config.h02_acceptance_path)
    status_report = _read_json(config.status_report_path)
    gate3_audit = _read_json(config.gate3_audit_path)

    current_failure = _current_failure(failure_triage=failure_triage, gate3_audit=gate3_audit)
    current_artifacts = _current_artifacts(remaining)
    formal_acceptance = _formal_acceptance(h02=h02, remaining=remaining)
    permissions = _permissions(status_report=status_report, failure_triage=failure_triage)
    next_round = _next_round_matrix()
    audit_issues = _audit_issues(
        failure_triage=failure_triage,
        current_failure=current_failure,
        current_artifacts=current_artifacts,
        formal_acceptance=formal_acceptance,
        permissions=permissions,
    )
    ready = not audit_issues
    return {
        "schema_version": 1,
        "artifact_name": "module2_formal_gate_next_round_requirements",
        "status": "formal_gate_next_round_requirements_ready" if ready else "formal_gate_next_round_requirements_blocked",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": module2_source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "runs_remote_audit": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "paper_result_material_allowed": False,
        "inputs": {
            "failure_triage": str(config.failure_triage_path),
            "remaining_deliverables": str(config.remaining_deliverables_path),
            "h02_formal_acceptance": str(config.h02_acceptance_path),
            "formal_gate_status_report": str(config.status_report_path),
            "gate3_formal_audit": str(config.gate3_audit_path),
        },
        "current_failed_run": current_failure,
        "current_run_artifacts": current_artifacts,
        "blocked_formal_acceptance": formal_acceptance,
        "permissions_now": permissions,
        "next_round_requirements": next_round,
        "audit_issue_count": len(audit_issues),
        "audit_issues": audit_issues,
        "claim_boundaries": [
            "This artifact is a formal-gate planning artifact, not a paper result table or appendix.",
            "The failed warm-start PPO Gate3 checkpoint is negative formal evidence, not a successful PPO replacement for RS.",
            "The failed checkpoint, failed audit, and smoke H02 rows are invalid substitutes for the next success-attempt evidence.",
            "Any new remote training intended to overturn this failure requires a new or revised Research Contract first.",
            "Local PPO training remains disallowed.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Module2 next-round formal gate requirements after a failed Gate3 run.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--failure-triage", type=Path, default=DEFAULT_FAILURE_TRIAGE)
    parser.add_argument("--remaining-deliverables", type=Path, default=DEFAULT_REMAINING_DELIVERABLES)
    parser.add_argument("--h02-acceptance", type=Path, default=DEFAULT_H02_ACCEPTANCE)
    parser.add_argument("--status-report", type=Path, default=DEFAULT_STATUS_REPORT)
    parser.add_argument("--gate3-audit", type=Path, default=DEFAULT_GATE3_AUDIT)
    return parser.parse_args(list(argv) if argv is not None else None)


def _current_failure(*, failure_triage: dict[str, Any], gate3_audit: dict[str, Any]) -> dict[str, Any]:
    triage_failure = failure_triage.get("formal_gate_failure") if isinstance(failure_triage.get("formal_gate_failure"), dict) else {}
    success_rate = _number(triage_failure.get("terminal_rs_success_rate"))
    if success_rate is None:
        success_rate = _number(gate3_audit.get("terminal_rs_success_rate"))
    threshold = _number(triage_failure.get("required_success_threshold"))
    if threshold is None:
        threshold = _number(gate3_audit.get("required_success_threshold"))
    deficit = None
    if success_rate is not None and threshold is not None:
        deficit = round(max(0.0, threshold - success_rate), 12)
    return {
        "failure_triage_status": failure_triage.get("status"),
        "failure_triage_audit_issue_count": int(failure_triage.get("audit_issue_count") or 0),
        "formal_decision": triage_failure.get("formal_decision") or gate3_audit.get("formal_decision"),
        "evaluator_decision": triage_failure.get("evaluator_decision") or gate3_audit.get("evaluator_decision"),
        "failure_mode": triage_failure.get("failure_mode"),
        "episodes": _int(triage_failure.get("episodes") or gate3_audit.get("episodes")),
        "terminal_rs_success_rate": success_rate,
        "required_success_threshold": threshold,
        "threshold_deficit": deficit,
        "warm_start_status": triage_failure.get("warm_start_status") or gate3_audit.get("warm_start_status"),
        "warm_start_decision": triage_failure.get("warm_start_decision") or gate3_audit.get("warm_start_decision"),
        "negative_formal_evidence_recorded": failure_triage.get("status") == "formal_gate_failure_triage_ready",
        "paper_success_claim_allowed": False,
    }


def _current_artifacts(remaining: dict[str, Any]) -> dict[str, Any]:
    categories = _remaining_categories(remaining)
    counts = {
        category: int(row.get("missing_count") or 0)
        for category, row in categories.items()
    }
    return {
        "remaining_deliverables_status": remaining.get("status"),
        "remaining_deliverables_audit_issue_count": int(remaining.get("audit_issue_count") or 0),
        "missing_counts_by_formal_category": counts,
        "training_complete_for_failed_run": counts.get("training") == 0,
        "evaluation_complete_for_failed_run": counts.get("evaluation") == 0,
        "acceptance_complete_for_failed_run": counts.get("acceptance") == 0,
        "formal_acceptance_complete_for_failed_run": counts.get("formal_acceptance") == 0,
        "present_counts_by_formal_category": {
            category: int(row.get("present_count") or 0)
            for category, row in categories.items()
        },
        "important_boundary": "current failed-run artifacts are complete enough to record the failure, not enough to support a success claim",
    }


def _formal_acceptance(*, h02: dict[str, Any], remaining: dict[str, Any]) -> dict[str, Any]:
    missing = []
    for row in _remaining_categories(remaining).get("formal_acceptance", {}).get("missing_artifacts", []) or []:
        if isinstance(row, dict):
            missing.append(
                {
                    "matrix_id": row.get("matrix_id"),
                    "artifact_id": row.get("artifact_id"),
                    "expected_path": row.get("expected_path"),
                    "missing_reason": row.get("missing_reason"),
                }
            )
    return {
        "h02_status": h02.get("status"),
        "formal_output_accepted": bool(h02.get("formal_output_accepted")),
        "paper_result_input_allowed": bool(h02.get("paper_result_input_allowed")),
        "blockers": _strings(h02.get("blockers")),
        "gate3_formal_decision": _nested(h02, "formal_checks", "gate3_formal_decision"),
        "gate3_formal_audit_passed": _nested(h02, "formal_checks", "gate3_formal_audit_passed"),
        "scale_satisfies_h01": _nested(h02, "formal_checks", "scale_satisfies_h01"),
        "has_ppo_result_rows": _nested(h02, "method_checks", "has_ppo_result_rows"),
        "ppo_rows_have_checkpoint_hash": _nested(h02, "method_checks", "ppo_rows_have_checkpoint_hash"),
        "missing_artifacts": missing,
    }


def _permissions(*, status_report: dict[str, Any], failure_triage: dict[str, Any]) -> dict[str, Any]:
    raw = status_report.get("permissions_now") if isinstance(status_report.get("permissions_now"), dict) else {}
    next_gate = failure_triage.get("next_gate") if isinstance(failure_triage.get("next_gate"), dict) else {}
    new_contract_required = bool(next_gate.get("new_or_revised_contract_required_before_new_training", True))
    return {
        "local_training_allowed_now": bool(raw.get("local_training_allowed_now")),
        "remote_preflight_allowed_now": bool(raw.get("remote_preflight_allowed_now")),
        "remote_training_allowed_now_for_existing_packet": bool(raw.get("remote_training_allowed_now")),
        "formal_h01_evaluation_allowed_now": bool(raw.get("formal_h01_evaluation_allowed_now")),
        "formal_h02_acceptance_allowed_now": bool(raw.get("formal_h02_acceptance_allowed_now")),
        "formal_claim_allowed_now": bool(raw.get("formal_claim_allowed_now")),
        "source_freshness_ready_for_remote_preflight": bool(raw.get("source_freshness_ready_for_remote_preflight")),
        "new_success_training_allowed_now": not new_contract_required,
        "new_or_revised_contract_required_before_new_success_training": new_contract_required,
        "failure_triage_next_gate_status": next_gate.get("status"),
    }


def _next_round_matrix() -> dict[str, Any]:
    rows = [
        _requirement(
            category="contract",
            requirement_id="new_or_revised_research_contract",
            status="missing_required_before_new_training",
            required_before="new_success_training",
            acceptable_evidence=[
                "a new or revised .pipeline/contracts/module2-* contract",
                "status is approved or frozen before the new success attempt starts",
                "hypothesis, success signal, failure signal, training budget, and protocol deltas are locked before training",
            ],
            invalid_substitutes=[
                "editing the previous formal result after seeing failure",
                "changing threshold, reward, curriculum, architecture, or observation without a new contract",
                "chat-only approval without a committed contract artifact",
            ],
        ),
        _requirement(
            category="training",
            requirement_id="new_remote_ppo_checkpoint_bundle",
            status="blocked_until_contract",
            required_before="new_gate3_formal_audit",
            acceptable_evidence=[
                "remote-produced train/final_model.zip under a new attempt directory",
                "train/summary.json records protocol label, training budget, seed, and terminal-RS training signals",
                "train/training_manifest.json records source head, host, command provenance, and warm-start decision",
            ],
            invalid_substitutes=[
                "local PPO training output",
                "the failed warm-start Gate3 checkpoint",
                "checkpoint file without summary, manifest, or hash provenance",
            ],
        ),
        _requirement(
            category="evaluation",
            requirement_id="new_formal_gate3_eval_bundle",
            status="blocked_until_new_checkpoint",
            required_before="new_gate3_formal_audit",
            acceptable_evidence=[
                "eval/gate3_eval_episodes.csv from the new approved formal run",
                "eval/gate3_summary.json with at least 64 formal episodes",
                "terminal-RS success rate, collision rate, truncation rate, timing, and seed/protocol provenance are present",
            ],
            invalid_substitutes=[
                "H02 available-subset smoke CSV",
                "no-warm failure rows for a warm-start claim",
                "summary without per-episode CSV",
            ],
        ),
        _requirement(
            category="acceptance",
            requirement_id="new_gate3_audit_and_hash_acceptance",
            status="blocked_until_new_eval",
            required_before="h02_formal_output_acceptance",
            acceptable_evidence=[
                "gate3_formal_audit.json for the new attempt records formal_decision=pass",
                "gate3_trial_manifest.json ties train/eval/audit to the approved contract",
                "train/final_model.zip.sha256 or equivalent hash manifest matches the pulled-back checkpoint",
            ],
            invalid_substitutes=[
                "formal_decision=fail reinterpreted as success",
                "remote stdout without local pullback",
                "checkpoint hash not tied to the evaluated checkpoint",
            ],
        ),
        _requirement(
            category="formal_acceptance",
            requirement_id="h02_formal_output_acceptance",
            status="blocked_until_new_gate3_pass",
            required_before="paper_result_material",
            acceptable_evidence=[
                "h02_formal_acceptance.json records formal_output_accepted=true",
                "paper_result_input_allowed=true",
                "formal PPO rows are present and include the accepted checkpoint hash",
                "H02 scale satisfies the frozen H01 manifest",
            ],
            invalid_substitutes=[
                "blocked H02 acceptance",
                "formal-looking tables generated from smoke scale",
                "PPO rows without checkpoint hash",
            ],
        ),
    ]
    return {
        "status": "new_or_revised_contract_required_before_any_new_success_attempt",
        "not_paper_result_material": True,
        "runs_training": False,
        "local_training_allowed": False,
        "new_success_training_allowed_now": False,
        "requirement_count": len(rows),
        "categories": ["contract", "training", "evaluation", "acceptance", "formal_acceptance"],
        "rows": rows,
    }


def _requirement(
    *,
    category: str,
    requirement_id: str,
    status: str,
    required_before: str,
    acceptable_evidence: list[str],
    invalid_substitutes: list[str],
) -> dict[str, Any]:
    return {
        "category": category,
        "requirement_id": requirement_id,
        "status": status,
        "required_before": required_before,
        "acceptable_evidence": acceptable_evidence,
        "invalid_substitutes": invalid_substitutes,
    }


def _audit_issues(
    *,
    failure_triage: dict[str, Any],
    current_failure: dict[str, Any],
    current_artifacts: dict[str, Any],
    formal_acceptance: dict[str, Any],
    permissions: dict[str, Any],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if failure_triage.get("status") != "formal_gate_failure_triage_ready":
        issues.append(_issue("failure_triage_not_ready", "Failure triage must be ready before next-round requirements are authoritative."))
    if current_failure.get("failure_mode") != "threshold_failure":
        issues.append(_issue("current_failure_not_threshold_failure", "Next-round requirements expect a threshold-failed formal Gate3 run."))
    if current_failure.get("formal_decision") != "fail":
        issues.append(_issue("current_formal_decision_not_fail", "Current formal Gate3 decision must be fail."))
    for category in ("training", "evaluation", "acceptance"):
        if current_artifacts["missing_counts_by_formal_category"].get(category, 0) != 0:
            issues.append(_issue(f"failed_run_{category}_artifacts_incomplete", f"{category} artifacts must be complete enough to record the failed run."))
    if current_artifacts["missing_counts_by_formal_category"].get("formal_acceptance", 0) == 0:
        issues.append(_issue("failed_run_formal_acceptance_unexpectedly_complete", "Failed run must not have formal acceptance complete."))
    if formal_acceptance["formal_output_accepted"] or formal_acceptance["paper_result_input_allowed"]:
        issues.append(_issue("h02_accepts_failed_run", "H02 must not accept a failed Gate3 run as paper result input."))
    if "gate3_formal_audit_not_passed" not in formal_acceptance["blockers"]:
        issues.append(_issue("h02_missing_gate3_failure_blocker", "H02 blockers must include gate3_formal_audit_not_passed."))
    if permissions["local_training_allowed_now"]:
        issues.append(_issue("local_training_allowed", "Local PPO training must remain disallowed."))
    if permissions["formal_claim_allowed_now"]:
        issues.append(_issue("formal_claim_allowed", "Formal claim must remain blocked after failed Gate3."))
    if permissions["new_success_training_allowed_now"]:
        issues.append(_issue("new_success_training_allowed_without_contract", "New success training must be blocked until a new or revised contract is approved/frozen."))
    return _unique_issues(issues)


def _markdown(manifest: dict[str, Any]) -> str:
    failure = manifest["current_failed_run"]
    artifacts = manifest["current_run_artifacts"]
    h02 = manifest["blocked_formal_acceptance"]
    permissions = manifest["permissions_now"]
    lines = [
        "# Module2 Formal Gate Next-Round Requirements",
        "",
        "This file is a formal-gate planning artifact, not paper result material.",
        "",
        "## Current Failed Run",
        "",
        f"- formal_decision: `{failure['formal_decision']}`",
        f"- failure_mode: `{failure['failure_mode']}`",
        f"- episodes: `{failure['episodes']}`",
        f"- terminal_rs_success_rate: `{failure['terminal_rs_success_rate']}`",
        f"- required_success_threshold: `{failure['required_success_threshold']}`",
        f"- threshold_deficit: `{failure['threshold_deficit']}`",
        "",
        "## Current Run Artifact Closure",
        "",
        f"- training_missing: `{artifacts['missing_counts_by_formal_category'].get('training')}`",
        f"- evaluation_missing: `{artifacts['missing_counts_by_formal_category'].get('evaluation')}`",
        f"- acceptance_missing: `{artifacts['missing_counts_by_formal_category'].get('acceptance')}`",
        f"- formal_acceptance_missing: `{artifacts['missing_counts_by_formal_category'].get('formal_acceptance')}`",
        "",
        "## Blocked Formal Acceptance",
        "",
        f"- h02_status: `{h02['h02_status']}`",
        f"- formal_output_accepted: `{h02['formal_output_accepted']}`",
        f"- paper_result_input_allowed: `{h02['paper_result_input_allowed']}`",
        f"- blockers: `{', '.join(h02['blockers'])}`",
        "",
        "## Permissions Now",
        "",
        f"- local_training_allowed_now: `{permissions['local_training_allowed_now']}`",
        f"- remote_preflight_allowed_now: `{permissions['remote_preflight_allowed_now']}`",
        f"- remote_training_allowed_now_for_existing_packet: `{permissions['remote_training_allowed_now_for_existing_packet']}`",
        f"- formal_h01_evaluation_allowed_now: `{permissions['formal_h01_evaluation_allowed_now']}`",
        f"- formal_h02_acceptance_allowed_now: `{permissions['formal_h02_acceptance_allowed_now']}`",
        f"- formal_claim_allowed_now: `{permissions['formal_claim_allowed_now']}`",
        f"- new_success_training_allowed_now: `{permissions['new_success_training_allowed_now']}`",
        f"- new_or_revised_contract_required_before_new_success_training: `{permissions['new_or_revised_contract_required_before_new_success_training']}`",
        f"- failure_triage_next_gate_status: `{permissions['failure_triage_next_gate_status']}`",
        "",
        "## Missing Current Formal Acceptance Artifacts",
        "",
    ]
    missing_artifacts = h02.get("missing_artifacts") or []
    if missing_artifacts:
        for row in missing_artifacts:
            lines.append(
                "- "
                f"`{row.get('matrix_id')}`: artifact_id=`{row.get('artifact_id')}`, "
                f"expected_path=`{row.get('expected_path')}`, missing_reason=`{row.get('missing_reason')}`"
            )
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Next-Round Requirements",
            "",
            "| category | requirement | status | required_before |",
            "|---|---|---|---|",
        ]
    )
    for row in manifest["next_round_requirements"]["rows"]:
        lines.append(
            f"| `{row['category']}` | `{row['requirement_id']}` | `{row['status']}` | `{row['required_before']}` |"
        )
    lines.extend(["", "## Missing Next-Round Deliverables"])
    for row in manifest["next_round_requirements"]["rows"]:
        lines.extend(
            [
                "",
                f"### `{row['category']}:{row['requirement_id']}`",
                "",
                f"- status: `{row['status']}`",
                f"- required_before: `{row['required_before']}`",
                "- acceptable_evidence:",
            ]
        )
        for item in row["acceptable_evidence"]:
            lines.append(f"  - {item}")
        lines.append("- invalid_substitutes:")
        for item in row["invalid_substitutes"]:
            lines.append(f"  - {item}")
    lines.extend(
        [
            "",
            "## Boundaries",
        ]
    )
    for boundary in manifest["claim_boundaries"]:
        lines.append(f"- {boundary}")
    lines.extend(["", "## Audit", "", f"- status: `{manifest['status']}`", f"- audit_issue_count: `{manifest['audit_issue_count']}`"])
    return "\n".join(lines) + "\n"


def _remaining_categories(remaining: dict[str, Any]) -> dict[str, dict[str, Any]]:
    gap = remaining.get("deliverable_gap_summary") if isinstance(remaining.get("deliverable_gap_summary"), dict) else {}
    categories = gap.get("categories") if isinstance(gap.get("categories"), list) else []
    return {
        str(row.get("category")): row
        for row in categories
        if isinstance(row, dict) and row.get("category")
    }


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


def _int(value: Any) -> int | None:
    try:
        if value is None:
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


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
