from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_post_f02_6_plan_audit")
DEFAULT_PLAN = Path("0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json")
DEFAULT_FORMAL_GATE = Path("0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json")
DEFAULT_SOURCE_FRESHNESS = Path("0_trials/module2_source_freshness_audit/source_freshness_audit.json")
DEFAULT_MISSING_ARTIFACTS = Path("0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json")
DEFAULT_CLOSURE_CHECKLIST = Path("0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json")
DEFAULT_STATUS_REPORT = Path("0_trials/module2_formal_gate_status_report/formal_gate_status_report.json")
REMOTE_EXECUTION_STEP_IDS = (
    "sync_to_remote",
    "run_remote_preflight",
    "run_remote_training",
    "run_remote_audit",
)
REQUIRED_STAGE_ORDER = (
    "f02_6_decision_record",
    "regenerate_preflight_gate_artifacts",
    "approved_remote_preflight",
    "regenerate_remote_execution_packet",
    "gate3_remote_training",
    "gate3_remote_audit_pullback",
    "regenerate_h01_h02_formal_artifacts",
    "regenerate_claim_gate_artifacts",
)


@dataclass(frozen=True)
class PostF026PlanAuditConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    plan_path: Path = DEFAULT_PLAN
    formal_gate_path: Path = DEFAULT_FORMAL_GATE
    source_freshness_path: Path = DEFAULT_SOURCE_FRESHNESS
    missing_artifacts_path: Path = DEFAULT_MISSING_ARTIFACTS
    closure_checklist_path: Path = DEFAULT_CLOSURE_CHECKLIST
    status_report_path: Path = DEFAULT_STATUS_REPORT


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = PostF026PlanAuditConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        plan_path=args.plan,
        formal_gate_path=args.formal_gate,
        source_freshness_path=args.source_freshness_audit,
        missing_artifacts_path=args.missing_artifacts_audit,
        closure_checklist_path=args.closure_checklist,
        status_report_path=args.status_report,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "post_f02_6_plan_audit.json"
    markdown_out = config.markdown_out or output_dir / "post_f02_6_plan_audit.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: PostF026PlanAuditConfig) -> dict[str, Any]:
    plan = _read_json(config.plan_path)
    formal_gate = _read_json(config.formal_gate_path)
    source_freshness = _read_json(config.source_freshness_path)
    missing_artifacts = _read_json(config.missing_artifacts_path)
    closure_checklist = _read_json(config.closure_checklist_path)
    status_report = _read_json(config.status_report_path)
    issues = _audit_issues(
        plan=plan,
        formal_gate=formal_gate,
        source_freshness=source_freshness,
        missing_artifacts=missing_artifacts,
        missing_artifacts_path=config.missing_artifacts_path,
        closure_checklist=closure_checklist,
        closure_checklist_path=config.closure_checklist_path,
        status_report=status_report,
        status_report_path=config.status_report_path,
    )
    return {
        "schema_version": 1,
        "artifact_name": "module2_post_f02_6_plan_audit",
        "status": "post_f02_6_plan_audit_passed" if not issues else "post_f02_6_plan_audit_failed",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "inputs": {
            "post_f02_6_regeneration_plan": str(config.plan_path),
            "formal_gate_gap_audit": str(config.formal_gate_path),
            "source_freshness_audit": str(config.source_freshness_path),
            "formal_gate_missing_artifacts_audit": str(config.missing_artifacts_path),
            "formal_gate_closure_checklist": str(config.closure_checklist_path),
            "formal_gate_status_report": str(config.status_report_path),
        },
        "plan_status": plan.get("status"),
        "missing_artifacts_summary": _missing_artifacts_summary(config.missing_artifacts_path, missing_artifacts),
        "closure_checklist_summary": _closure_checklist_summary(config.closure_checklist_path, closure_checklist),
        "status_report_summary": _status_report_summary(config.status_report_path, status_report),
        "audit_issue_count": len(issues),
        "audit_issues": issues,
        "required_stage_order": list(REQUIRED_STAGE_ORDER),
        "current_blocking_summary": _current_blocking_summary(plan),
        "claim_boundaries": [
            "This audit validates a plan artifact; it does not execute the plan.",
            "A passing audit is not permission to train while F02.6 remains pending.",
            "A passing audit is not a paper result or formal performance claim.",
            "Training stages must remain remote-only on gpu3070ti-relay and blocked until upstream gates pass.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit the Module2 post-F02.6 regeneration plan without executing it.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--formal-gate", type=Path, default=DEFAULT_FORMAL_GATE)
    parser.add_argument("--source-freshness-audit", type=Path, default=DEFAULT_SOURCE_FRESHNESS)
    parser.add_argument("--missing-artifacts-audit", type=Path, default=DEFAULT_MISSING_ARTIFACTS)
    parser.add_argument("--closure-checklist", type=Path, default=DEFAULT_CLOSURE_CHECKLIST)
    parser.add_argument("--status-report", type=Path, default=DEFAULT_STATUS_REPORT)
    return parser.parse_args(list(argv) if argv is not None else None)


def _audit_issues(
    *,
    plan: dict[str, Any],
    formal_gate: dict[str, Any],
    source_freshness: dict[str, Any],
    missing_artifacts: dict[str, Any],
    missing_artifacts_path: Path,
    closure_checklist: dict[str, Any],
    closure_checklist_path: Path,
    status_report: dict[str, Any],
    status_report_path: Path,
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    issues.extend(_top_level_issues(plan))
    issues.extend(_stage_order_issues(plan))
    issues.extend(_stage_safety_issues(plan))
    issues.extend(_pending_gate_issues(plan))
    issues.extend(_cross_artifact_issues(plan=plan, formal_gate=formal_gate, source_freshness=source_freshness))
    issues.extend(_missing_artifacts_issues(plan=plan, missing_artifacts=missing_artifacts, missing_artifacts_path=missing_artifacts_path))
    issues.extend(_closure_checklist_issues(plan=plan, closure_checklist=closure_checklist, closure_checklist_path=closure_checklist_path))
    issues.extend(_status_report_issues(plan=plan, status_report=status_report, status_report_path=status_report_path))
    return _unique_issues(issues)


def _top_level_issues(plan: dict[str, Any]) -> list[dict[str, Any]]:
    expected_false = {
        "executes_commands": "Plan artifact must not execute commands.",
        "runs_training": "Plan artifact must not run training.",
        "runs_remote_preflight": "Plan artifact must not run remote preflight.",
        "local_training_allowed": "Plan artifact must preserve local-training prohibition.",
        "formal_claim_allowed": "Plan artifact must not allow formal claims.",
    }
    issues: list[dict[str, Any]] = []
    if plan.get("artifact_name") != "module2_post_f02_6_regeneration_plan":
        issues.append(_issue("plan_wrong_artifact_name", f"artifact_name={plan.get('artifact_name')!r}"))
    if plan.get("not_paper_result_material") is not True:
        issues.append(_issue("plan_not_marked_non_result", "not_paper_result_material must be true"))
    for key, message in expected_false.items():
        if plan.get(key) is not False:
            issues.append(_issue(f"plan_top_level_{key}_not_false", message, observed=plan.get(key)))
    return issues


def _stage_order_issues(plan: dict[str, Any]) -> list[dict[str, Any]]:
    stages = _stages(plan)
    ids = [str(stage.get("stage_id")) for stage in stages]
    issues: list[dict[str, Any]] = []
    for required in REQUIRED_STAGE_ORDER:
        if required not in ids:
            issues.append(_issue(f"missing_stage_{required}", "Required stage is absent.", observed=ids))
    present_required = [stage_id for stage_id in ids if stage_id in REQUIRED_STAGE_ORDER]
    if present_required != [stage_id for stage_id in REQUIRED_STAGE_ORDER if stage_id in present_required]:
        issues.append(_issue("stage_order_invalid", "Required stages are not in the expected order.", observed=present_required))
    return issues


def _stage_safety_issues(plan: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for stage in _stages(plan):
        stage_id = str(stage.get("stage_id"))
        if stage.get("runs_training") is True:
            if stage.get("host") != "gpu3070ti-relay":
                issues.append(_issue("training_stage_not_gpu3070ti", f"{stage_id} host must be gpu3070ti-relay.", observed=stage.get("host")))
            if stage.get("allowed_now") is True and "ssh gpu3070ti-relay" not in "\n".join(_strings(stage.get("command_templates"))):
                issues.append(_issue("ready_training_stage_missing_remote_ssh", f"{stage_id} is ready but command is not an ssh gpu3070ti-relay command."))
        if stage.get("runs_remote_preflight") is True and stage.get("host") != "gpu3070ti-relay":
            issues.append(_issue("remote_preflight_stage_not_gpu3070ti", f"{stage_id} host must be gpu3070ti-relay.", observed=stage.get("host")))
        if stage.get("phase") == "claim_gate" and stage.get("allowed_now") is True:
            issues.append(_issue("claim_gate_ready_before_formal_acceptance", f"{stage_id} must not be ready before formal acceptance."))
    return issues


def _pending_gate_issues(plan: dict[str, Any]) -> list[dict[str, Any]]:
    summary = plan.get("current_gate_summary") if isinstance(plan.get("current_gate_summary"), dict) else {}
    blocking = plan.get("blocking_summary") if isinstance(plan.get("blocking_summary"), dict) else {}
    decision_status = str(summary.get("f02_6_decision_status"))
    if decision_status != "pending_human_decision":
        return []
    issues: list[dict[str, Any]] = []
    if plan.get("status") != "blocked_until_f02_6_decision":
        issues.append(_issue("pending_f02_6_wrong_plan_status", "Pending F02.6 must keep the plan blocked.", observed=plan.get("status")))
    if blocking.get("training_allowed_now") is not False:
        issues.append(_issue("pending_f02_6_allows_training", "Training must not be allowed while F02.6 is pending."))
    if blocking.get("remote_preflight_allowed_now") is not False:
        issues.append(_issue("pending_f02_6_allows_remote_preflight", "Remote preflight must not be allowed while F02.6 is pending."))
    training = _stage_by_id(plan, "gate3_remote_training")
    if training.get("allowed_now") is True:
        issues.append(_issue("training_stage_allowed_before_f02_6", "Training stage is ready while F02.6 is pending."))
    for blocker in ("f02_6_decision_not_approved", "remote_packet_not_ready"):
        if blocker not in _strings(training.get("blocked_by")):
            issues.append(_issue(f"training_stage_missing_{blocker}", f"Training stage must include {blocker}."))
    if summary.get("source_freshness_regeneration_required") is True and "source_fresh_preflight_targets_open" not in _strings(training.get("blocked_by")):
        issues.append(_issue("training_stage_missing_source_fresh_blocker", "Training stage must reflect source freshness regeneration blocker."))
    decision = _stage_by_id(plan, "f02_6_decision_record")
    if decision.get("allowed_now") is not True or decision.get("requires_human_input") is not True:
        issues.append(_issue("pending_decision_stage_not_human_ready", "Pending F02.6 should expose only the human decision-record stage as ready."))
    return issues


def _cross_artifact_issues(*, plan: dict[str, Any], formal_gate: dict[str, Any], source_freshness: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    summary = plan.get("current_gate_summary") if isinstance(plan.get("current_gate_summary"), dict) else {}
    formal_state = formal_gate.get("current_gate_state") if isinstance(formal_gate.get("current_gate_state"), dict) else {}
    if formal_state and summary.get("f02_6_decision_status") != formal_state.get("f02_6_decision_status"):
        issues.append(
            _issue(
                "plan_formal_gate_decision_status_mismatch",
                "Plan F02.6 status does not match formal gate.",
                observed={"plan": summary.get("f02_6_decision_status"), "formal_gate": formal_state.get("f02_6_decision_status")},
            )
        )
    source_required = source_freshness.get("regeneration_required_before_remote_formal_execution")
    if source_freshness and summary.get("source_freshness_regeneration_required") != source_required:
        issues.append(
            _issue(
                "plan_source_freshness_requirement_mismatch",
                "Plan source freshness flag does not match source freshness audit.",
                observed={"plan": summary.get("source_freshness_regeneration_required"), "source_freshness": source_required},
            )
        )
    if source_freshness:
        plan_counts = _target_counts_by_gate(plan)
        source_counts = _source_target_counts_by_gate(source_freshness)
        if plan_counts != source_counts:
            issues.append(
                _issue(
                    "plan_source_regeneration_target_counts_mismatch",
                    "Plan target counts by gate do not match source freshness audit.",
                    observed={"plan": plan_counts, "source_freshness": source_counts},
                )
            )
    return issues


def _missing_artifacts_issues(
    *,
    plan: dict[str, Any],
    missing_artifacts: dict[str, Any],
    missing_artifacts_path: Path,
) -> list[dict[str, Any]]:
    if not Path(missing_artifacts_path).is_file():
        return [
            _issue(
                "missing_artifacts_inventory_absent",
                "Post-F02.6 plan audit requires the missing-artifacts inventory for final gate cross-check.",
                observed=str(missing_artifacts_path),
            )
        ]
    issues: list[dict[str, Any]] = []
    if missing_artifacts.get("executes_commands") is not False:
        issues.append(_issue("missing_artifacts_inventory_executes_commands", "Missing-artifacts inventory must be read-only."))
    if missing_artifacts.get("runs_training") is not False:
        issues.append(_issue("missing_artifacts_inventory_runs_training", "Missing-artifacts inventory must not run training."))
    if missing_artifacts.get("runs_remote_preflight") is not False:
        issues.append(_issue("missing_artifacts_inventory_runs_preflight", "Missing-artifacts inventory must not run remote preflight."))
    if missing_artifacts.get("local_training_allowed") is not False:
        issues.append(_issue("missing_artifacts_inventory_allows_local_training", "Missing-artifacts inventory must preserve local-training prohibition."))
    if missing_artifacts.get("formal_claim_allowed") is not False:
        issues.append(_issue("missing_artifacts_inventory_allows_claim", "Missing-artifacts inventory must not allow formal claims."))
    if int(missing_artifacts.get("audit_issue_count") or 0) > 0:
        issues.append(_issue("missing_artifacts_inventory_has_audit_issues", "Missing-artifacts inventory reports open audit issues."))
    claim_stage = _stage_by_id(plan, "regenerate_claim_gate_artifacts")
    if missing_artifacts.get("all_required_evidence_present") is not True and claim_stage.get("allowed_now") is True:
        issues.append(
            _issue(
                "claim_gate_ready_with_missing_artifacts",
                "Claim gate regeneration must not be ready while the missing-artifacts inventory is open.",
                observed=missing_artifacts.get("missing_counts_by_category"),
            )
        )
    return issues


def _closure_checklist_issues(
    *,
    plan: dict[str, Any],
    closure_checklist: dict[str, Any],
    closure_checklist_path: Path,
) -> list[dict[str, Any]]:
    if not Path(closure_checklist_path).is_file():
        return [
            _issue(
                "closure_checklist_absent",
                "Post-F02.6 plan audit requires the closure checklist for final gate cross-check.",
                observed=str(closure_checklist_path),
            )
        ]
    issues: list[dict[str, Any]] = []
    if closure_checklist.get("executes_commands") is not False:
        issues.append(_issue("closure_checklist_executes_commands", "Closure checklist must be read-only."))
    if closure_checklist.get("runs_training") is not False:
        issues.append(_issue("closure_checklist_runs_training", "Closure checklist must not run training."))
    if closure_checklist.get("runs_remote_preflight") is not False:
        issues.append(_issue("closure_checklist_runs_preflight", "Closure checklist must not run remote preflight."))
    if closure_checklist.get("local_training_allowed") is not False:
        issues.append(_issue("closure_checklist_allows_local_training", "Closure checklist must preserve local-training prohibition."))
    if closure_checklist.get("formal_claim_allowed") is not False:
        issues.append(_issue("closure_checklist_allows_claim", "Closure checklist must not allow formal claims."))
    if int(closure_checklist.get("input_safety_issue_count") or 0) > 0:
        issues.append(_issue("closure_checklist_has_input_safety_issues", "Closure checklist reports open input safety issues."))
    claim_stage = _stage_by_id(plan, "regenerate_claim_gate_artifacts")
    if closure_checklist.get("status") != "formal_gate_closure_ready_for_result_audit" and claim_stage.get("allowed_now") is True:
        issues.append(
            _issue(
                "claim_gate_ready_with_open_closure_checklist",
                "Claim gate regeneration must not be ready while the closure checklist is open.",
                observed={"status": closure_checklist.get("status"), "open_item_count": closure_checklist.get("open_item_count")},
            )
        )
    return issues


def _status_report_issues(
    *,
    plan: dict[str, Any],
    status_report: dict[str, Any],
    status_report_path: Path,
) -> list[dict[str, Any]]:
    if not Path(status_report_path).is_file():
        return [
            _issue(
                "formal_gate_status_report_absent",
                "Post-F02.6 plan audit requires the formal gate status report for final gate cross-check.",
                observed=str(status_report_path),
            )
        ]
    issues: list[dict[str, Any]] = []
    if status_report.get("executes_commands") is not False:
        issues.append(_issue("formal_gate_status_report_executes_commands", "Status report must be read-only."))
    if status_report.get("runs_training") is not False:
        issues.append(_issue("formal_gate_status_report_runs_training", "Status report must not run training."))
    if status_report.get("runs_remote_preflight") is not False:
        issues.append(_issue("formal_gate_status_report_runs_preflight", "Status report must not run remote preflight."))
    if status_report.get("local_training_allowed") is not False:
        issues.append(_issue("formal_gate_status_report_allows_local_training", "Status report must preserve local-training prohibition."))
    if status_report.get("formal_claim_allowed") is not False:
        issues.append(_issue("formal_gate_status_report_allows_claim", "Status report must not allow formal claims."))
    permissions = status_report.get("permissions_now") if isinstance(status_report.get("permissions_now"), dict) else {}
    if permissions.get("local_training_allowed_now") is True:
        issues.append(_issue("formal_gate_status_report_allows_local_training_now", "Status report must never allow local training now."))
    if permissions.get("formal_claim_allowed_now") is True and status_report.get("status") != "formal_gate_status_ready_for_claim_audit":
        issues.append(
            _issue(
                "formal_gate_status_report_claim_permission_inconsistent",
                "Status report may allow formal claims only when it is ready for claim audit.",
                observed={"status": status_report.get("status"), "formal_claim_allowed_now": permissions.get("formal_claim_allowed_now")},
            )
        )
    if int(status_report.get("input_safety_issue_count") or 0) > 0:
        issues.append(_issue("formal_gate_status_report_has_input_safety_issues", "Status report reports open input safety issues."))
    remote_steps = _status_report_remote_steps(status_report)
    if not remote_steps:
        issues.append(_issue("formal_gate_status_report_missing_remote_step_summary", "Status report must expose remote execution step blockers."))
    elif status_report.get("status") != "formal_gate_status_ready_for_claim_audit":
        for step_id, step in remote_steps.items():
            if step.get("allowed_now") is True:
                issues.append(
                    _issue(
                        f"formal_gate_status_report_blocked_but_{step_id}_allowed",
                        "Status report must not allow remote execution steps while the formal gate is blocked.",
                    )
                )
    claim_stage = _stage_by_id(plan, "regenerate_claim_gate_artifacts")
    if status_report.get("status") != "formal_gate_status_ready_for_claim_audit" and claim_stage.get("allowed_now") is True:
        issues.append(
            _issue(
                "claim_gate_ready_with_blocked_status_report",
                "Claim gate regeneration must not be ready while the formal gate status report is blocked.",
                observed={
                    "status": status_report.get("status"),
                    "formal_claim_allowed_now": permissions.get("formal_claim_allowed_now"),
                    "next_blocked_lane": status_report.get("next_blocked_lane"),
                },
            )
        )
    return issues


def _target_counts_by_gate(plan: dict[str, Any]) -> dict[str, int]:
    groups = plan.get("source_regeneration_targets_by_gate") if isinstance(plan.get("source_regeneration_targets_by_gate"), dict) else {}
    return {str(key): len(value) for key, value in sorted(groups.items()) if isinstance(value, list)}


def _source_target_counts_by_gate(source_freshness: dict[str, Any]) -> dict[str, int]:
    targets = source_freshness.get("ordered_regeneration_targets")
    if not isinstance(targets, list):
        return {}
    counts: dict[str, int] = {}
    for item in targets:
        if not isinstance(item, dict):
            continue
        gate = str(item.get("required_before") or "unknown")
        counts[gate] = counts.get(gate, 0) + 1
    return dict(sorted(counts.items()))


def _current_blocking_summary(plan: dict[str, Any]) -> dict[str, Any]:
    summary = plan.get("blocking_summary") if isinstance(plan.get("blocking_summary"), dict) else {}
    return {
        "plan_status": plan.get("status"),
        "training_allowed_now": summary.get("training_allowed_now"),
        "remote_preflight_allowed_now": summary.get("remote_preflight_allowed_now"),
        "ready_stage_ids": summary.get("ready_stage_ids", []),
        "blocked_stage_ids": summary.get("blocked_stage_ids", []),
    }


def _missing_artifacts_summary(path: Path, missing_artifacts: dict[str, Any]) -> dict[str, Any]:
    counts = missing_artifacts.get("missing_counts_by_category")
    return {
        "path": str(path),
        "exists": Path(path).is_file(),
        "status": missing_artifacts.get("status"),
        "executes_commands": missing_artifacts.get("executes_commands"),
        "runs_training": missing_artifacts.get("runs_training"),
        "runs_remote_preflight": missing_artifacts.get("runs_remote_preflight"),
        "local_training_allowed": missing_artifacts.get("local_training_allowed"),
        "formal_claim_allowed": missing_artifacts.get("formal_claim_allowed"),
        "all_required_evidence_present": missing_artifacts.get("all_required_evidence_present"),
        "audit_issue_count": missing_artifacts.get("audit_issue_count"),
        "missing_counts_by_category": counts if isinstance(counts, dict) else {},
    }


def _closure_checklist_summary(path: Path, closure_checklist: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": str(path),
        "exists": Path(path).is_file(),
        "status": closure_checklist.get("status"),
        "executes_commands": closure_checklist.get("executes_commands"),
        "runs_training": closure_checklist.get("runs_training"),
        "runs_remote_preflight": closure_checklist.get("runs_remote_preflight"),
        "local_training_allowed": closure_checklist.get("local_training_allowed"),
        "formal_claim_allowed": closure_checklist.get("formal_claim_allowed"),
        "closure_item_count": closure_checklist.get("closure_item_count"),
        "open_item_count": closure_checklist.get("open_item_count"),
        "input_safety_issue_count": closure_checklist.get("input_safety_issue_count"),
    }


def _status_report_summary(path: Path, status_report: dict[str, Any]) -> dict[str, Any]:
    permissions = status_report.get("permissions_now") if isinstance(status_report.get("permissions_now"), dict) else {}
    next_lane = status_report.get("next_blocked_lane") if isinstance(status_report.get("next_blocked_lane"), dict) else {}
    remote_steps = _status_report_remote_steps(status_report)
    return {
        "path": str(path),
        "exists": Path(path).is_file(),
        "status": status_report.get("status"),
        "executes_commands": status_report.get("executes_commands"),
        "runs_training": status_report.get("runs_training"),
        "runs_remote_preflight": status_report.get("runs_remote_preflight"),
        "local_training_allowed": status_report.get("local_training_allowed"),
        "formal_claim_allowed": status_report.get("formal_claim_allowed"),
        "formal_claim_allowed_now": permissions.get("formal_claim_allowed_now"),
        "local_training_allowed_now": permissions.get("local_training_allowed_now"),
        "input_safety_issue_count": status_report.get("input_safety_issue_count"),
        "next_blocked_lane_id": next_lane.get("lane_id"),
        "remote_execution_step_summary": remote_steps,
    }


def _status_report_remote_steps(status_report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw = status_report.get("remote_execution_step_summary")
    if not isinstance(raw, dict):
        return {}
    out: dict[str, dict[str, Any]] = {}
    for step_id in REMOTE_EXECUTION_STEP_IDS:
        step = raw.get(step_id)
        if not isinstance(step, dict):
            continue
        blocked_by = step.get("blocked_by")
        out[step_id] = {
            "present": bool(step.get("present")),
            "allowed_now": step.get("allowed_now") if isinstance(step.get("allowed_now"), bool) else None,
            "runs_training": step.get("runs_training") if isinstance(step.get("runs_training"), bool) else None,
            "blocked_by": [str(item) for item in blocked_by if item] if isinstance(blocked_by, list) else [],
        }
    return out


def _stage_by_id(plan: dict[str, Any], stage_id: str) -> dict[str, Any]:
    for stage in _stages(plan):
        if stage.get("stage_id") == stage_id:
            return stage
    return {}


def _stages(plan: dict[str, Any]) -> list[dict[str, Any]]:
    stages = plan.get("ordered_stages")
    if not isinstance(stages, list):
        return []
    return [stage for stage in stages if isinstance(stage, dict)]


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
        "# Module2 Post-F02.6 Plan Audit",
        "",
        "This file audits the ordered post-F02.6 plan. It does not execute the plan.",
        "",
        f"- status: `{manifest['status']}`",
        f"- audit_issue_count: `{manifest['audit_issue_count']}`",
        f"- executes_commands: `{manifest['executes_commands']}`",
        f"- runs_training: `{manifest['runs_training']}`",
        f"- runs_remote_preflight: `{manifest['runs_remote_preflight']}`",
        "",
        "## Current Blocking Summary",
        "",
    ]
    for key, value in manifest["current_blocking_summary"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(
        [
            "",
            "## Missing Artifacts Inventory",
            "",
            f"- path: `{manifest['missing_artifacts_summary']['path']}`",
            f"- status: `{manifest['missing_artifacts_summary']['status']}`",
            f"- runs_training: `{manifest['missing_artifacts_summary']['runs_training']}`",
            f"- runs_remote_preflight: `{manifest['missing_artifacts_summary']['runs_remote_preflight']}`",
            f"- all_required_evidence_present: `{manifest['missing_artifacts_summary']['all_required_evidence_present']}`",
            f"- audit_issue_count: `{manifest['missing_artifacts_summary']['audit_issue_count']}`",
            f"- missing_counts_by_category: `{manifest['missing_artifacts_summary']['missing_counts_by_category']}`",
            "",
            "## Closure Checklist",
            "",
            f"- path: `{manifest['closure_checklist_summary']['path']}`",
            f"- status: `{manifest['closure_checklist_summary']['status']}`",
            f"- runs_training: `{manifest['closure_checklist_summary']['runs_training']}`",
            f"- runs_remote_preflight: `{manifest['closure_checklist_summary']['runs_remote_preflight']}`",
            f"- open_item_count: `{manifest['closure_checklist_summary']['open_item_count']}`",
            f"- input_safety_issue_count: `{manifest['closure_checklist_summary']['input_safety_issue_count']}`",
            "",
            "## Formal Gate Status Report",
            "",
            f"- path: `{manifest['status_report_summary']['path']}`",
            f"- status: `{manifest['status_report_summary']['status']}`",
            f"- runs_training: `{manifest['status_report_summary']['runs_training']}`",
            f"- runs_remote_preflight: `{manifest['status_report_summary']['runs_remote_preflight']}`",
            f"- formal_claim_allowed_now: `{manifest['status_report_summary']['formal_claim_allowed_now']}`",
            f"- local_training_allowed_now: `{manifest['status_report_summary']['local_training_allowed_now']}`",
            f"- input_safety_issue_count: `{manifest['status_report_summary']['input_safety_issue_count']}`",
            f"- next_blocked_lane_id: `{manifest['status_report_summary']['next_blocked_lane_id']}`",
            "",
            "### Status Report Remote Execution Steps",
            "",
        ]
    )
    for step_id, step in manifest["status_report_summary"]["remote_execution_step_summary"].items():
        blocked_by = ", ".join(step["blocked_by"]) if step["blocked_by"] else "none"
        lines.append(
            f"- `{step_id}`: allowed_now=`{step['allowed_now']}`, runs_training=`{step['runs_training']}`, blocked_by=`{blocked_by}`"
        )
    lines.extend(
        [
            "",
            "## Audit Issues",
            "",
        ]
    )
    if manifest["audit_issues"]:
        for issue in manifest["audit_issues"]:
            lines.append(f"- `{issue['issue_id']}`: {issue['message']}")
    else:
        lines.append("- none")
    lines.extend(["", "## Claim Boundaries", ""])
    lines.extend(f"- {item}" for item in manifest["claim_boundaries"])
    return "\n".join(lines) + "\n"


def _read_json(path: Path) -> dict[str, Any]:
    if not Path(path).is_file():
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
