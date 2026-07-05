from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_post_f02_6_plan_audit")
DEFAULT_PLAN = Path("0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json")
DEFAULT_FORMAL_GATE = Path("0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json")
DEFAULT_SOURCE_FRESHNESS = Path("0_trials/module2_source_freshness_audit/source_freshness_audit.json")
DEFAULT_MISSING_ARTIFACTS = Path("0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json")
DEFAULT_CLOSURE_CHECKLIST = Path("0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json")
DEFAULT_STATUS_REPORT = Path("0_trials/module2_formal_gate_status_report/formal_gate_status_report.json")
DEFAULT_REMAINING_DELIVERABLES = Path(
    "0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json"
)
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
REQUIRED_F02_6_ALLOWED_ACTION_IDS = ("record_f02_6_decision",)
REQUIRED_F02_6_BLOCKED_ACTION_IDS = (
    "remote_preflight",
    "remote_training",
    "local_training",
    "formal_claim",
    "paper_result_material",
)
F02_6_DISABLED_PERMISSION_FIELDS = (
    "remote_preflight_allowed_now",
    "remote_training_allowed_now",
    "formal_claim_allowed_now",
    "local_training_allowed_now",
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
    remaining_deliverables_path: Path | None = None


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
        remaining_deliverables_path=args.remaining_deliverables,
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
    remaining_deliverables = _read_json(config.remaining_deliverables_path) if config.remaining_deliverables_path else {}
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
        remaining_deliverables=remaining_deliverables,
        remaining_deliverables_path=config.remaining_deliverables_path,
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
        "formal_gate_remaining_deliverables": str(config.remaining_deliverables_path)
        if config.remaining_deliverables_path
        else None,
        },
        "plan_status": plan.get("status"),
        "source_regeneration_command_index_summary": _source_regeneration_command_index_summary(plan, source_freshness),
        "missing_artifacts_summary": _missing_artifacts_summary(config.missing_artifacts_path, missing_artifacts),
        "closure_checklist_summary": _closure_checklist_summary(config.closure_checklist_path, closure_checklist),
        "status_report_summary": _status_report_summary(config.status_report_path, status_report),
        "status_report_proof_audit_deliverables_summary": _status_report_proof_audit_deliverables_summary(status_report),
        "f02_6_human_decision_request_summary": _f02_6_human_decision_request_summary(plan),
        "remaining_deliverables_gap_summary": _remaining_deliverables_gap_summary(
            config.remaining_deliverables_path,
            remaining_deliverables,
        ),
        "remaining_deliverables_unlock_chain_summary": _remaining_deliverables_unlock_chain_summary(
            config.remaining_deliverables_path,
            remaining_deliverables,
        ),
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
    parser.add_argument("--remaining-deliverables", type=Path, default=DEFAULT_REMAINING_DELIVERABLES)
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
    remaining_deliverables: dict[str, Any],
    remaining_deliverables_path: Path | None,
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    issues.extend(_top_level_issues(plan))
    issues.extend(_stage_order_issues(plan))
    issues.extend(_stage_safety_issues(plan))
    issues.extend(_pending_gate_issues(plan))
    issues.extend(_cross_artifact_issues(plan=plan, formal_gate=formal_gate, source_freshness=source_freshness))
    issues.extend(_source_regeneration_command_index_issues(plan=plan, source_freshness=source_freshness))
    issues.extend(_missing_artifacts_issues(plan=plan, missing_artifacts=missing_artifacts, missing_artifacts_path=missing_artifacts_path))
    issues.extend(_closure_checklist_issues(plan=plan, closure_checklist=closure_checklist, closure_checklist_path=closure_checklist_path))
    issues.extend(_status_report_issues(plan=plan, status_report=status_report, status_report_path=status_report_path))
    issues.extend(
        _remaining_deliverables_gap_issues(
            plan=plan,
            status_report=status_report,
            remaining_deliverables=remaining_deliverables,
            remaining_deliverables_path=remaining_deliverables_path,
        )
    )
    issues.extend(
        _remaining_deliverables_unlock_chain_issues(
            plan=plan,
            remaining_deliverables=remaining_deliverables,
            remaining_deliverables_path=remaining_deliverables_path,
        )
    )
    issues.extend(
        _proof_audit_deliverables_summary_issues(
            status_report=status_report,
            remaining_deliverables=remaining_deliverables,
            remaining_deliverables_path=remaining_deliverables_path,
        )
    )
    issues.extend(_handoff_coverage_issues(plan=plan, source_freshness=source_freshness, status_report=status_report))
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
    request_summary = _f02_6_human_decision_request_summary(plan)
    if request_summary["present"] is not True:
        issues.append(_issue("pending_f02_6_human_decision_request_missing", "Pending F02.6 must expose the human decision request summary."))
    if request_summary["status"] != "awaiting_dr_sun_decision":
        issues.append(
            _issue(
                "pending_f02_6_human_decision_request_not_awaiting_dr_sun",
                "Pending F02.6 request must await Dr Sun's decision.",
                observed=request_summary["status"],
            )
        )
    if request_summary["decision_owner_required"] != "Dr Sun":
        issues.append(
            _issue(
                "pending_f02_6_human_decision_request_owner_not_dr_sun",
                "Pending F02.6 request must require Dr Sun as decision owner.",
                observed=request_summary["decision_owner_required"],
            )
        )
    allowed_actions = request_summary["current_allowed_action_ids"]
    if allowed_actions != list(REQUIRED_F02_6_ALLOWED_ACTION_IDS):
        issues.append(
            _issue(
                "pending_f02_6_human_decision_request_allowed_actions_not_decision_only",
                "Pending F02.6 request must allow only the decision-record action.",
                observed=allowed_actions,
            )
        )
    blocked_actions = set(request_summary["current_blocked_action_ids"])
    missing_blocked = [action_id for action_id in REQUIRED_F02_6_BLOCKED_ACTION_IDS if action_id not in blocked_actions]
    if missing_blocked:
        issues.append(
            _issue(
                "pending_f02_6_human_decision_request_missing_blocked_actions",
                "Pending F02.6 request must explicitly block execution and paper-result actions.",
                observed=missing_blocked,
            )
        )
    if request_summary["post_decision_routes_are_current_authorization"] is not False:
        issues.append(
            _issue(
                "pending_f02_6_human_decision_request_treats_routes_as_authorization",
                "Post-decision routes must not be treated as current authorization while F02.6 is pending.",
                observed=request_summary["post_decision_routes_are_current_authorization"],
            )
        )
    if request_summary["all_execution_disabled_now"] is not True:
        issues.append(
            _issue(
                "pending_f02_6_human_decision_request_execution_not_disabled",
                "Pending F02.6 request must mark all execution disabled now.",
                observed=request_summary["all_execution_disabled_now"],
            )
        )
    for field in F02_6_DISABLED_PERMISSION_FIELDS:
        if request_summary[field] is not False:
            issues.append(
                _issue(
                    f"pending_f02_6_human_decision_request_{field}_not_false",
                    f"Pending F02.6 request must keep {field}=false.",
                    observed=request_summary[field],
                )
            )
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
    source_required = _source_freshness_blocking_regeneration_required(source_freshness)
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


def _source_freshness_blocking_regeneration_required(source_freshness: dict[str, Any]) -> bool:
    if "blocking_regeneration_required_before_remote_formal_execution" in source_freshness:
        return source_freshness.get("blocking_regeneration_required_before_remote_formal_execution") is True
    return source_freshness.get("regeneration_required_before_remote_formal_execution") is True


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
    execution_veto = _status_report_execution_veto(status_report)
    if not execution_veto["present"]:
        issues.append(_issue("formal_gate_status_report_missing_execution_veto_summary", "Status report must expose formal_gate_execution_veto_summary."))
    else:
        if execution_veto["all_rows_consistent"] is not True:
            issues.append(_issue("formal_gate_status_report_execution_veto_inconsistent", "Status report execution veto matrix must have all_rows_consistent=true."))
        if execution_veto["mismatch_rows"]:
            issues.append(_issue("formal_gate_status_report_execution_veto_mismatch_rows_open", "Status report execution veto matrix reports mismatch rows."))
        for row_id in sorted({"local_training", "remote_preflight", "remote_training", "remote_audit", "formal_claim"} - set(execution_veto["row_consensus"])):
            issues.append(_issue(f"formal_gate_status_report_execution_veto_missing_{row_id}", f"Status report execution veto matrix missing row {row_id}."))
        if status_report.get("status") != "formal_gate_status_ready_for_claim_audit":
            for row_id in ("local_training", "remote_preflight", "remote_training", "remote_audit", "formal_claim"):
                if execution_veto["row_consensus"].get(row_id) is True:
                    issues.append(
                        _issue(
                            f"formal_gate_status_report_blocked_veto_allows_{row_id}",
                            f"Blocked status report must not allow {row_id} in execution veto matrix.",
                        )
                    )
        permission_map = {
            "local_training": "local_training_allowed_now",
            "remote_preflight": "remote_preflight_allowed_now",
            "remote_training": "remote_training_allowed_now",
            "formal_claim": "formal_claim_allowed_now",
        }
        for row_id, permission_key in permission_map.items():
            row_value = execution_veto["row_consensus"].get(row_id)
            permission_value = permissions.get(permission_key)
            if isinstance(row_value, bool) and isinstance(permission_value, bool) and row_value != permission_value:
                issues.append(
                    _issue(
                        f"formal_gate_status_report_execution_veto_permission_mismatch_{row_id}",
                        "Status report execution veto consensus must match permissions_now.",
                        observed={"row_consensus": row_value, permission_key: permission_value},
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


def _remaining_deliverables_gap_issues(
    *,
    plan: dict[str, Any],
    status_report: dict[str, Any],
    remaining_deliverables: dict[str, Any],
    remaining_deliverables_path: Path,
) -> list[dict[str, Any]]:
    if remaining_deliverables_path is None:
        return []
    if not Path(remaining_deliverables_path).is_file():
        return [
            _issue(
                "remaining_deliverables_absent",
                "Post-F02.6 plan audit requires the remaining-deliverables ledger for gap-summary cross-check.",
                observed=str(remaining_deliverables_path),
            )
        ]
    issues: list[dict[str, Any]] = []
    remaining_gap = _normalize_gap_summary(remaining_deliverables.get("deliverable_gap_summary"))
    plan_gap = _normalize_gap_summary(plan.get("remaining_deliverables_gap_summary"))
    status_gap = _normalize_gap_summary(status_report.get("remaining_deliverables_gap_summary"))

    if not remaining_gap["present"]:
        issues.append(_issue("remaining_deliverables_gap_summary_missing", "Remaining-deliverables ledger must expose deliverable_gap_summary."))
    else:
        if remaining_gap["execution_boundary"] != "read_only_no_execution":
            issues.append(_issue("remaining_deliverables_gap_summary_execution_boundary_invalid", "Gap summary must be read-only."))
        if remaining_gap["not_paper_result_material"] is not True:
            issues.append(_issue("remaining_deliverables_gap_summary_marked_as_paper_result", "Gap summary must not be paper result material."))

    if not plan_gap["present"]:
        issues.append(_issue("plan_missing_remaining_deliverables_gap_summary", "Post-F02.6 plan must carry remaining_deliverables_gap_summary."))
    if not status_gap["present"]:
        issues.append(_issue("status_report_missing_remaining_deliverables_gap_summary", "Status report must carry remaining_deliverables_gap_summary."))

    remaining_signature = _gap_signature(remaining_gap)
    plan_signature = _gap_signature(plan_gap)
    status_signature = _gap_signature(status_gap)
    if remaining_gap["present"] and plan_gap["present"] and plan_signature != remaining_signature:
        issues.append(
            _issue(
                "plan_remaining_deliverables_gap_summary_mismatch",
                "Plan gap summary must match the remaining-deliverables ledger.",
                observed={"plan": plan_signature, "remaining_deliverables": remaining_signature},
            )
        )
    if remaining_gap["present"] and status_gap["present"] and status_signature != remaining_signature:
        issues.append(
            _issue(
                "status_report_remaining_deliverables_gap_summary_mismatch",
                "Status-report gap summary must match the remaining-deliverables ledger.",
                observed={"status_report": status_signature, "remaining_deliverables": remaining_signature},
            )
        )

    gap_open = remaining_gap["total_missing_deliverables"] > 0 or remaining_gap["open_category_count"] > 0
    claim_stage = _stage_by_id(plan, "regenerate_claim_gate_artifacts")
    if gap_open and claim_stage.get("allowed_now") is True:
        issues.append(
            _issue(
                "claim_gate_ready_with_remaining_deliverables_gap_open",
                "Claim gate regeneration must not be ready while formal deliverable gaps remain open.",
                observed=remaining_signature,
            )
        )
    if gap_open and status_report.get("status") == "formal_gate_status_ready_for_claim_audit":
        issues.append(
            _issue(
                "status_report_ready_with_remaining_deliverables_gap_open",
                "Status report must not be ready for claim audit while formal deliverable gaps remain open.",
                observed=remaining_signature,
            )
        )
    return issues


def _remaining_deliverables_unlock_chain_issues(
    *,
    plan: dict[str, Any],
    remaining_deliverables: dict[str, Any],
    remaining_deliverables_path: Path | None,
) -> list[dict[str, Any]]:
    if remaining_deliverables_path is None:
        return []
    if not Path(remaining_deliverables_path).is_file():
        return []

    issues: list[dict[str, Any]] = []
    ledger_chain = _normalize_unlock_chain_summary(remaining_deliverables.get("deliverable_unlock_chain"))
    plan_chain = _normalize_unlock_chain_summary(plan.get("remaining_deliverables_unlock_chain_summary"))

    if not ledger_chain["present"]:
        issues.append(
            _issue(
                "remaining_deliverables_unlock_chain_missing",
                "Remaining-deliverables ledger must expose deliverable_unlock_chain.",
            )
        )
    else:
        issues.extend(_unlock_chain_safety_issues("remaining_deliverables_unlock_chain", ledger_chain))

    if not plan_chain["present"]:
        issues.append(
            _issue(
                "plan_missing_remaining_deliverables_unlock_chain_summary",
                "Post-F02.6 plan must carry remaining_deliverables_unlock_chain_summary.",
            )
        )
    else:
        issues.extend(_unlock_chain_safety_issues("plan_remaining_deliverables_unlock_chain", plan_chain))

    ledger_signature = _unlock_chain_signature(ledger_chain)
    plan_signature = _unlock_chain_signature(plan_chain)
    if ledger_chain["present"] and plan_chain["present"] and plan_signature != ledger_signature:
        issues.append(
            _issue(
                "plan_remaining_deliverables_unlock_chain_summary_mismatch",
                "Plan unlock-chain summary must match the remaining-deliverables ledger.",
                observed={"plan": plan_signature, "remaining_deliverables": ledger_signature},
            )
        )

    claim_stage = _stage_by_id(plan, "regenerate_claim_gate_artifacts")
    chain_open = (
        ledger_chain["blocked_row_count"] > 0
        or ledger_chain["rows_with_missing_required_blockers"] > 0
        or ledger_chain["rows_allowed_while_missing"] > 0
    )
    if chain_open and claim_stage.get("allowed_now") is True:
        issues.append(
            _issue(
                "claim_gate_ready_with_remaining_deliverables_unlock_chain_blocked",
                "Claim gate regeneration must not be ready while the remaining-deliverables unlock chain is blocked.",
                observed=ledger_signature,
            )
        )
    return issues


def _unlock_chain_safety_issues(prefix: str, chain: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if chain["execution_boundary"] != "read_only_no_execution":
        issues.append(_issue(f"{prefix}_execution_boundary_invalid", "Unlock chain must be read-only."))
    if chain["not_paper_result_material"] is not True:
        issues.append(_issue(f"{prefix}_marked_as_paper_result", "Unlock chain must not be paper result material."))
    if chain["rows_with_missing_required_blockers"] > 0:
        issues.append(
            _issue(
                f"{prefix}_rows_missing_required_blockers",
                "Unlock chain rows must include every required current blocker while formal deliverables are missing.",
                observed=chain["rows_with_missing_required_blockers"],
            )
        )
    if chain["rows_allowed_while_missing"] > 0:
        issues.append(
            _issue(
                f"{prefix}_rows_allowed_while_missing",
                "Unlock chain must not allow responsible stages while their formal deliverables are missing.",
                observed=chain["rows_allowed_while_missing"],
            )
        )
    return issues


def _proof_audit_deliverables_summary_issues(
    *,
    status_report: dict[str, Any],
    remaining_deliverables: dict[str, Any],
    remaining_deliverables_path: Path | None,
) -> list[dict[str, Any]]:
    if remaining_deliverables_path is None:
        return []
    if not Path(remaining_deliverables_path).is_file():
        return []
    issues: list[dict[str, Any]] = []
    ledger_summary = _remaining_deliverables_top_level_summary(remaining_deliverables)
    status_summary = _status_report_proof_audit_deliverables_summary(status_report)

    if not ledger_summary["present"]:
        issues.append(
            _issue(
                "remaining_deliverables_top_level_summary_missing",
                "Remaining-deliverables ledger must expose the top-level 3/2/3/2 formal deliverable summary.",
            )
        )
    if not status_summary["present"]:
        issues.append(
            _issue(
                "status_report_missing_proof_audit_deliverables_summary",
                "Status report must forward proof-audit remaining-deliverables top-level summary.",
            )
        )

    ledger_signature = _deliverables_top_level_signature(ledger_summary)
    status_signature = _deliverables_top_level_signature(status_summary)
    if ledger_summary["present"] and status_summary["present"] and ledger_signature != status_signature:
        issues.append(
            _issue(
                "status_report_proof_audit_deliverables_summary_mismatch",
                "Status-report proof-audit deliverable summary must match the remaining-deliverables ledger.",
                observed={"status_report": status_signature, "remaining_deliverables": ledger_signature},
            )
        )

    missing_total = sum(int(count) for count in ledger_summary["missing_counts_by_formal_category"].values())
    if missing_total > 0 and status_report.get("status") == "formal_gate_status_ready_for_claim_audit":
        issues.append(
            _issue(
                "status_report_ready_with_proof_deliverables_missing",
                "Status report must not be ready for claim audit while proof-audit deliverable summary still has missing formal artifacts.",
                observed=ledger_signature,
            )
        )
    return issues


def _handoff_coverage_issues(
    *,
    plan: dict[str, Any],
    source_freshness: dict[str, Any],
    status_report: dict[str, Any],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    source_target = _source_freshness_target(source_freshness, "formal_gate_handoff_bundle")
    if not source_target:
        issues.append(
            _issue(
                "handoff_bundle_missing_from_source_freshness",
                "formal_gate_handoff_bundle must be tracked by source freshness before approved remote preflight.",
            )
        )
    elif source_target.get("required_before") != "approved_remote_preflight":
        issues.append(
            _issue(
                "handoff_bundle_wrong_source_freshness_gate",
                "formal_gate_handoff_bundle must be required before approved_remote_preflight.",
                observed=source_target.get("required_before"),
            )
        )

    preflight_targets = _target_ids_for_gate(plan, "approved_remote_preflight")
    if "formal_gate_handoff_bundle" not in preflight_targets:
        issues.append(
            _issue(
                "handoff_bundle_missing_from_plan_preflight_targets",
                "Post-F02.6 plan must list formal_gate_handoff_bundle under approved_remote_preflight source-regeneration targets.",
                observed=sorted(preflight_targets),
            )
        )
    regen_stage = _stage_by_id(plan, "regenerate_preflight_gate_artifacts")
    regen_commands = "\n".join(_strings(regen_stage.get("command_templates")))
    if "build_module2_formal_gate_handoff_bundle" not in regen_commands:
        issues.append(
            _issue(
                "handoff_bundle_missing_regeneration_command",
                "Post-F02.6 regeneration stage must include build_module2_formal_gate_handoff_bundle.",
            )
        )

    handoff_summary = status_report.get("formal_gate_handoff_summary")
    if not isinstance(handoff_summary, dict):
        issues.append(
            _issue(
                "status_report_missing_handoff_summary",
                "Formal gate status report must expose formal_gate_handoff_summary.",
            )
        )
    else:
        if int(handoff_summary.get("safety_issue_count") or 0) > 0:
            issues.append(_issue("status_report_handoff_safety_issues_open", "Status report handoff summary reports open safety issues."))
        if status_report.get("status") != "formal_gate_status_ready_for_claim_audit" and handoff_summary.get("remote_training_allowed_now") is True:
            issues.append(
                _issue(
                    "status_report_handoff_training_allowed_while_blocked",
                    "Status report must not show handoff remote training allowed while the formal gate is blocked.",
                    observed={"status": status_report.get("status"), "remote_training_allowed_now": handoff_summary.get("remote_training_allowed_now")},
                )
            )
    return issues


def _source_freshness_target(source_freshness: dict[str, Any], artifact_id: str) -> dict[str, Any]:
    for key in ("artifact_records", "ordered_regeneration_targets"):
        items = source_freshness.get(key)
        if not isinstance(items, list):
            continue
        for item in items:
            if isinstance(item, dict) and item.get("artifact_id") == artifact_id:
                return item
    return {}


def _target_ids_for_gate(plan: dict[str, Any], gate: str) -> set[str]:
    groups = plan.get("source_regeneration_targets_by_gate")
    if not isinstance(groups, dict):
        return set()
    items = groups.get(gate)
    if not isinstance(items, list):
        return set()
    return {str(item.get("artifact_id")) for item in items if isinstance(item, dict) and item.get("artifact_id")}


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


def _source_regeneration_command_index_issues(*, plan: dict[str, Any], source_freshness: dict[str, Any]) -> list[dict[str, Any]]:
    summary = _source_regeneration_command_index_summary(plan, source_freshness)
    issues: list[dict[str, Any]] = []
    if not summary["present"]:
        return [
            _issue(
                "source_regeneration_command_index_missing",
                "Post-F02.6 plan must expose source_regeneration_command_index.",
            )
        ]
    if summary["missing_target_ids"]:
        issues.append(
            _issue(
                "source_regeneration_command_index_missing_source_targets",
                "Command index must cover every source-freshness regeneration target.",
                observed=summary["missing_target_ids"],
            )
        )
    if summary["extra_index_ids"]:
        issues.append(
            _issue(
                "source_regeneration_command_index_has_extra_rows",
                "Command index should not contain rows absent from source freshness targets.",
                observed=summary["extra_index_ids"],
            )
        )
    if summary["unknown_manual_count"] > 0:
        issues.append(
            _issue(
                "source_regeneration_command_index_unknown_manual_rows",
                "Known gate artifacts must not fall back to unknown manual regeneration.",
                observed=summary["unknown_manual_ids"],
            )
        )
    if summary["stage_mismatch_ids"]:
        issues.append(
            _issue(
                "source_regeneration_command_index_stage_mismatch",
                "Command index stage_id must match each target's required_before gate.",
                observed=summary["stage_mismatch_ids"],
            )
        )
    if summary["command_not_in_stage_ids"]:
        issues.append(
            _issue(
                "source_regeneration_command_index_command_missing_from_stage",
                "Each command-index command must be present in its corresponding ordered stage.",
                observed=summary["command_not_in_stage_ids"],
            )
        )
    if summary["forbidden_command_ids"]:
        issues.append(
            _issue(
                "source_regeneration_command_index_contains_execution_commands",
                "Source-regeneration command index must not contain remote preflight, training, audit, ssh, or rsync commands.",
                observed=summary["forbidden_command_ids"],
            )
        )
    if summary["missing_required_field_ids"]:
        issues.append(
            _issue(
                "source_regeneration_command_index_rows_missing_required_fields",
                "Command-index rows must include artifact_id, required_before, stage_id, command_kind, and command_template.",
                observed=summary["missing_required_field_ids"],
            )
        )
    return issues


def _source_regeneration_command_index_summary(plan: dict[str, Any], source_freshness: dict[str, Any]) -> dict[str, Any]:
    source_targets = _source_targets(source_freshness)
    source_ids = {str(item.get("artifact_id")) for item in source_targets if item.get("artifact_id")}
    index_rows = _source_regeneration_command_index(plan)
    index_ids = {str(item.get("artifact_id")) for item in index_rows if item.get("artifact_id")}
    rows_by_id = {str(item.get("artifact_id")): item for item in index_rows if item.get("artifact_id")}
    stage_commands = _stage_commands_by_id(plan)
    unknown_manual_ids: list[str] = []
    stage_mismatch_ids: list[str] = []
    command_not_in_stage_ids: list[str] = []
    forbidden_command_ids: list[str] = []
    missing_required_field_ids: list[str] = []
    stage_counts: dict[str, int] = {}
    for row in index_rows:
        artifact_id = str(row.get("artifact_id") or "")
        stage_id = str(row.get("stage_id") or "")
        required_before = str(row.get("required_before") or "")
        command_kind = str(row.get("command_kind") or "")
        command_template = str(row.get("command_template") or "")
        if not all((artifact_id, required_before, stage_id, command_kind, command_template)):
            missing_required_field_ids.append(artifact_id or "<missing-artifact-id>")
        if command_kind == "unknown_manual":
            unknown_manual_ids.append(artifact_id)
        if stage_id != _expected_stage_for_required_before(required_before):
            stage_mismatch_ids.append(artifact_id)
        if command_template and command_template not in stage_commands.get(stage_id, set()):
            command_not_in_stage_ids.append(artifact_id)
        if _is_forbidden_regeneration_command(command_template):
            forbidden_command_ids.append(artifact_id)
        stage_counts[stage_id] = stage_counts.get(stage_id, 0) + 1
    return {
        "present": bool(index_rows),
        "index_row_count": len(index_rows),
        "source_target_count": len(source_targets),
        "missing_target_ids": sorted(source_ids - index_ids),
        "extra_index_ids": sorted(index_ids - source_ids),
        "unknown_manual_count": len(unknown_manual_ids),
        "unknown_manual_ids": sorted(unknown_manual_ids),
        "stage_mismatch_count": len(stage_mismatch_ids),
        "stage_mismatch_ids": sorted(stage_mismatch_ids),
        "command_not_in_stage_count": len(command_not_in_stage_ids),
        "command_not_in_stage_ids": sorted(command_not_in_stage_ids),
        "forbidden_command_count": len(forbidden_command_ids),
        "forbidden_command_ids": sorted(forbidden_command_ids),
        "missing_required_field_count": len(missing_required_field_ids),
        "missing_required_field_ids": sorted(missing_required_field_ids),
        "stage_counts": dict(sorted(stage_counts.items())),
        "rows": rows_by_id,
    }


def _source_regeneration_command_index(plan: dict[str, Any]) -> list[dict[str, Any]]:
    rows = plan.get("source_regeneration_command_index")
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict)]


def _source_targets(source_freshness: dict[str, Any]) -> list[dict[str, Any]]:
    targets = source_freshness.get("ordered_regeneration_targets")
    if not isinstance(targets, list):
        return []
    return [target for target in targets if isinstance(target, dict)]


def _stage_commands_by_id(plan: dict[str, Any]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for stage in _stages(plan):
        stage_id = str(stage.get("stage_id") or "")
        if not stage_id:
            continue
        out[stage_id] = set(_strings(stage.get("command_templates")))
    return out


def _expected_stage_for_required_before(required_before: str) -> str:
    if required_before == "approved_remote_preflight":
        return "regenerate_preflight_gate_artifacts"
    if required_before == "formal_h01_h02":
        return "regenerate_h01_h02_formal_artifacts"
    if required_before == "formal_claim_gate":
        return "regenerate_claim_gate_artifacts"
    return "manual_review"


def _is_forbidden_regeneration_command(command: str) -> bool:
    forbidden_tokens = (
        "preflight_rl_rs_gate3_formal_trial",
        "run_rl_rs_gate3_trial",
        "audit_rl_rs_gate3_trial",
        "ssh ",
        "rsync ",
    )
    return any(token in command for token in forbidden_tokens)


def _current_blocking_summary(plan: dict[str, Any]) -> dict[str, Any]:
    summary = plan.get("blocking_summary") if isinstance(plan.get("blocking_summary"), dict) else {}
    return {
        "plan_status": plan.get("status"),
        "training_allowed_now": summary.get("training_allowed_now"),
        "remote_preflight_allowed_now": summary.get("remote_preflight_allowed_now"),
        "ready_stage_ids": summary.get("ready_stage_ids", []),
        "blocked_stage_ids": summary.get("blocked_stage_ids", []),
    }


def _f02_6_human_decision_request_summary(plan: dict[str, Any]) -> dict[str, Any]:
    raw = plan.get("f02_6_human_decision_request_summary")
    summary = raw if isinstance(raw, dict) else {}
    out: dict[str, Any] = {
        "present": bool(summary) and summary.get("present") is not False,
        "status": summary.get("status"),
        "decision_owner_required": summary.get("decision_owner_required"),
        "current_allowed_action_ids": _strings(summary.get("current_allowed_action_ids")),
        "current_blocked_action_ids": _strings(summary.get("current_blocked_action_ids")),
    }
    for field in (
        "post_decision_routes_are_current_authorization",
        "all_execution_disabled_now",
        *F02_6_DISABLED_PERMISSION_FIELDS,
    ):
        value = summary.get(field)
        out[field] = value if isinstance(value, bool) else None
    return out


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
    execution_veto = _status_report_execution_veto(status_report)
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
        "formal_gate_handoff_summary": status_report.get("formal_gate_handoff_summary")
        if isinstance(status_report.get("formal_gate_handoff_summary"), dict)
        else {},
        "remaining_deliverables_gap_summary": _normalize_gap_summary(status_report.get("remaining_deliverables_gap_summary")),
        "proof_audit_deliverables_summary": _status_report_proof_audit_deliverables_summary(status_report),
        "formal_gate_execution_veto_summary": execution_veto,
    }


def _remaining_deliverables_gap_summary(path: Path | None, remaining_deliverables: dict[str, Any]) -> dict[str, Any]:
    summary = _normalize_gap_summary(remaining_deliverables.get("deliverable_gap_summary"))
    summary["path"] = str(path) if path else None
    summary["exists"] = Path(path).is_file() if path else False
    return summary


def _remaining_deliverables_unlock_chain_summary(path: Path | None, remaining_deliverables: dict[str, Any]) -> dict[str, Any]:
    summary = _normalize_unlock_chain_summary(remaining_deliverables.get("deliverable_unlock_chain"))
    summary["path"] = str(path) if path else None
    summary["exists"] = Path(path).is_file() if path else False
    return summary


def _remaining_deliverables_top_level_summary(remaining_deliverables: dict[str, Any]) -> dict[str, Any]:
    raw = {
        "missing_counts_by_formal_category": remaining_deliverables.get("missing_counts_by_formal_category"),
        "missing_matrix_ids_by_formal_category": remaining_deliverables.get("missing_matrix_ids_by_formal_category"),
        "next_blocked_lane": remaining_deliverables.get("next_blocked_lane"),
        "h01_status": remaining_deliverables.get("h01_status"),
        "h02_status": remaining_deliverables.get("h02_status"),
        "h02_formal_output_accepted": remaining_deliverables.get("h02_formal_output_accepted"),
        "h02_paper_result_input_allowed": remaining_deliverables.get("h02_paper_result_input_allowed"),
    }
    return _normalize_deliverables_top_level_summary(raw)


def _status_report_proof_audit_deliverables_summary(status_report: dict[str, Any]) -> dict[str, Any]:
    raw = status_report.get("formal_gate_proof_audit_remaining_deliverables_top_level_summary")
    return _normalize_deliverables_top_level_summary(raw)


def _normalize_deliverables_top_level_summary(raw: Any) -> dict[str, Any]:
    summary = raw if isinstance(raw, dict) else {}
    counts = summary.get("missing_counts_by_formal_category")
    ids_by_category = summary.get("missing_matrix_ids_by_formal_category")
    return {
        "present": bool(summary),
        "missing_counts_by_formal_category": {
            str(category): int(count or 0)
            for category, count in counts.items()
            if category
        }
        if isinstance(counts, dict)
        else {},
        "missing_matrix_ids_by_formal_category": {
            str(category): [str(item) for item in ids if item]
            for category, ids in ids_by_category.items()
            if category and isinstance(ids, list)
        }
        if isinstance(ids_by_category, dict)
        else {},
        "next_blocked_lane": summary.get("next_blocked_lane"),
        "h01_status": summary.get("h01_status"),
        "h02_status": summary.get("h02_status"),
        "h02_formal_output_accepted": summary.get("h02_formal_output_accepted")
        if isinstance(summary.get("h02_formal_output_accepted"), bool)
        else None,
        "h02_paper_result_input_allowed": summary.get("h02_paper_result_input_allowed")
        if isinstance(summary.get("h02_paper_result_input_allowed"), bool)
        else None,
    }


def _deliverables_top_level_signature(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "missing_counts_by_formal_category": {
            key: summary["missing_counts_by_formal_category"].get(key)
            for key in sorted(summary.get("missing_counts_by_formal_category", {}))
        },
        "missing_matrix_ids_by_formal_category": {
            key: summary["missing_matrix_ids_by_formal_category"].get(key, [])
            for key in sorted(summary.get("missing_matrix_ids_by_formal_category", {}))
        },
        "next_blocked_lane": summary.get("next_blocked_lane"),
        "h01_status": summary.get("h01_status"),
        "h02_status": summary.get("h02_status"),
        "h02_formal_output_accepted": summary.get("h02_formal_output_accepted"),
        "h02_paper_result_input_allowed": summary.get("h02_paper_result_input_allowed"),
    }


def _normalize_gap_summary(raw: Any) -> dict[str, Any]:
    summary = raw if isinstance(raw, dict) else {}
    categories = _normalize_gap_categories(summary.get("categories"))
    return {
        "present": bool(summary),
        "summary_id": summary.get("summary_id"),
        "execution_boundary": summary.get("execution_boundary"),
        "not_paper_result_material": summary.get("not_paper_result_material"),
        "total_missing_deliverables": int(summary.get("total_missing_deliverables") or 0),
        "open_category_count": int(summary.get("open_category_count") or 0),
        "category_order": [str(item) for item in summary.get("category_order", []) if item]
        if isinstance(summary.get("category_order"), list)
        else list(categories),
        "categories": categories,
    }


def _normalize_gap_categories(raw_categories: Any) -> dict[str, dict[str, Any]]:
    if isinstance(raw_categories, dict):
        items = raw_categories.items()
    elif isinstance(raw_categories, list):
        items = ((item.get("category"), item) for item in raw_categories if isinstance(item, dict))
    else:
        items = ()
    out: dict[str, dict[str, Any]] = {}
    for category, raw in items:
        if not category or not isinstance(raw, dict):
            continue
        matrix_ids = raw.get("missing_artifact_matrix_ids")
        if not isinstance(matrix_ids, list):
            missing_artifacts = raw.get("missing_artifacts") if isinstance(raw.get("missing_artifacts"), list) else []
            matrix_ids = [item.get("matrix_id") for item in missing_artifacts if isinstance(item, dict)]
        out[str(category)] = {
            "present": True,
            "missing_count": int(raw.get("missing_count") or 0),
            "responsible_stage_id": raw.get("responsible_stage_id"),
            "responsible_stage_allowed_now": raw.get("responsible_stage_allowed_now"),
            "missing_artifact_matrix_ids": [str(item) for item in matrix_ids if item],
        }
    return out


def _gap_signature(summary: dict[str, Any]) -> dict[str, Any]:
    categories = summary.get("categories") if isinstance(summary.get("categories"), dict) else {}
    return {
        "summary_id": summary.get("summary_id"),
        "total_missing_deliverables": summary.get("total_missing_deliverables"),
        "open_category_count": summary.get("open_category_count"),
        "categories": {
            key: {
                "missing_count": value.get("missing_count"),
                "responsible_stage_id": value.get("responsible_stage_id"),
                "missing_artifact_matrix_ids": value.get("missing_artifact_matrix_ids", []),
            }
            for key, value in sorted(categories.items())
            if isinstance(value, dict)
        },
    }


def _normalize_unlock_chain_summary(raw: Any) -> dict[str, Any]:
    chain = raw if isinstance(raw, dict) else {}
    rows = _normalize_unlock_chain_rows(chain.get("rows"))
    categories = _normalize_unlock_chain_categories(chain.get("categories"))
    if not categories and rows:
        categories = _derive_unlock_chain_categories(rows)
    derived_missing_blockers = sum(1 for row in rows if row["missing_required_current_blockers"])
    derived_allowed_while_missing = sum(
        1 for row in rows if row["missing"] is True and row["responsible_stage_allowed_now"] is True
    )
    derived_blocked_rows = sum(
        1 for row in rows if row["missing"] is True and row["responsible_stage_allowed_now"] is not True
    )
    return {
        "present": bool(chain),
        "chain_id": chain.get("chain_id"),
        "status": chain.get("status"),
        "execution_boundary": chain.get("execution_boundary"),
        "not_paper_result_material": chain.get("not_paper_result_material"),
        "row_count": int(chain.get("row_count") or len(rows) or sum(category["row_count"] for category in categories.values())),
        "blocked_row_count": int(chain.get("blocked_row_count") if chain.get("blocked_row_count") is not None else derived_blocked_rows),
        "rows_with_missing_required_blockers": derived_missing_blockers
        if rows
        else int(chain.get("rows_with_missing_required_blockers") or 0),
        "rows_allowed_while_missing": derived_allowed_while_missing
        if rows
        else int(chain.get("rows_allowed_while_missing") or 0),
        "categories": categories,
    }


def _normalize_unlock_chain_rows(raw_rows: Any) -> list[dict[str, Any]]:
    if not isinstance(raw_rows, list):
        return []
    rows: list[dict[str, Any]] = []
    for raw in raw_rows:
        if not isinstance(raw, dict):
            continue
        rows.append(
            {
                "category": str(raw.get("category") or "unknown"),
                "missing": raw.get("missing") if isinstance(raw.get("missing"), bool) else raw.get("current_state") == "missing",
                "responsible_stage_allowed_now": raw.get("responsible_stage_allowed_now")
                if isinstance(raw.get("responsible_stage_allowed_now"), bool)
                else None,
                "required_current_blockers": _strings(raw.get("required_current_blockers")),
                "missing_required_current_blockers": _strings(raw.get("missing_required_current_blockers")),
                "unlock_sequence_before_stage_allowed": _strings(raw.get("unlock_sequence_before_stage_allowed")),
            }
        )
    return rows


def _normalize_unlock_chain_categories(raw_categories: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(raw_categories, dict):
        return {}
    categories: dict[str, dict[str, Any]] = {}
    for category, raw in raw_categories.items():
        if not category or not isinstance(raw, dict):
            continue
        categories[str(category)] = {
            "row_count": int(raw.get("row_count") or 0),
            "blocked_row_count": int(raw.get("blocked_row_count") or 0),
            "rows_with_missing_required_blockers": int(raw.get("rows_with_missing_required_blockers") or 0),
            "rows_allowed_while_missing": int(raw.get("rows_allowed_while_missing") or 0),
            "required_current_blockers": _dedupe_strings(raw.get("required_current_blockers")),
            "unlock_sequence_before_stage_allowed": _dedupe_strings(raw.get("unlock_sequence_before_stage_allowed")),
        }
    return categories


def _derive_unlock_chain_categories(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    categories: dict[str, dict[str, Any]] = {}
    for row in rows:
        category = str(row.get("category") or "unknown")
        summary = categories.setdefault(
            category,
            {
                "row_count": 0,
                "blocked_row_count": 0,
                "rows_with_missing_required_blockers": 0,
                "rows_allowed_while_missing": 0,
                "required_current_blockers": [],
                "unlock_sequence_before_stage_allowed": [],
            },
        )
        summary["row_count"] += 1
        if row["missing"] is True and row["responsible_stage_allowed_now"] is not True:
            summary["blocked_row_count"] += 1
        if row["missing_required_current_blockers"]:
            summary["rows_with_missing_required_blockers"] += 1
        if row["missing"] is True and row["responsible_stage_allowed_now"] is True:
            summary["rows_allowed_while_missing"] += 1
        summary["required_current_blockers"] = _dedupe_strings(
            [*summary["required_current_blockers"], *row["required_current_blockers"]]
        )
        summary["unlock_sequence_before_stage_allowed"] = _dedupe_strings(
            [*summary["unlock_sequence_before_stage_allowed"], *row["unlock_sequence_before_stage_allowed"]]
        )
    return categories


def _unlock_chain_signature(summary: dict[str, Any]) -> dict[str, Any]:
    categories = summary.get("categories") if isinstance(summary.get("categories"), dict) else {}
    return {
        "chain_id": summary.get("chain_id"),
        "status": summary.get("status"),
        "execution_boundary": summary.get("execution_boundary"),
        "not_paper_result_material": summary.get("not_paper_result_material"),
        "row_count": summary.get("row_count"),
        "blocked_row_count": summary.get("blocked_row_count"),
        "rows_with_missing_required_blockers": summary.get("rows_with_missing_required_blockers"),
        "rows_allowed_while_missing": summary.get("rows_allowed_while_missing"),
        "categories": {
            key: {
                "row_count": value.get("row_count"),
                "blocked_row_count": value.get("blocked_row_count"),
                "rows_with_missing_required_blockers": value.get("rows_with_missing_required_blockers"),
                "rows_allowed_while_missing": value.get("rows_allowed_while_missing"),
                "required_current_blockers": value.get("required_current_blockers", []),
                "unlock_sequence_before_stage_allowed": value.get("unlock_sequence_before_stage_allowed", []),
            }
            for key, value in sorted(categories.items())
            if isinstance(value, dict)
        },
    }


def _dedupe_strings(value: Any) -> list[str]:
    items = value if isinstance(value, list) else []
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        text = str(item)
        if not text or text in seen:
            continue
        seen.add(text)
        out.append(text)
    return out


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


def _status_report_execution_veto(status_report: dict[str, Any]) -> dict[str, Any]:
    raw = status_report.get("formal_gate_execution_veto_summary")
    veto = raw if isinstance(raw, dict) else {}
    row_consensus = veto.get("row_consensus") if isinstance(veto.get("row_consensus"), dict) else {}
    rows = veto.get("rows") if isinstance(veto.get("rows"), dict) else {}
    normalized_rows: dict[str, dict[str, Any]] = {}
    for row_id, row in rows.items():
        if not isinstance(row, dict):
            continue
        normalized_rows[str(row_id)] = {
            "consistent": row.get("consistent") if isinstance(row.get("consistent"), bool) else None,
            "consensus_allowed_now": row.get("consensus_allowed_now") if isinstance(row.get("consensus_allowed_now"), bool) else None,
            "allowed_now_by_source": row.get("allowed_now_by_source") if isinstance(row.get("allowed_now_by_source"), dict) else {},
        }
    normalized_consensus = {
        str(row_id): value if isinstance(value, bool) else None
        for row_id, value in row_consensus.items()
    }
    for row_id, row in normalized_rows.items():
        normalized_consensus.setdefault(row_id, row["consensus_allowed_now"])
    return {
        "present": bool(veto) and veto.get("present") is not False,
        "matrix_version": veto.get("matrix_version"),
        "all_rows_consistent": veto.get("all_rows_consistent") if isinstance(veto.get("all_rows_consistent"), bool) else None,
        "mismatch_rows": _strings(veto.get("mismatch_rows")),
        "row_count": int(veto.get("row_count") or len(normalized_rows)),
        "row_consensus": normalized_consensus,
        "rows": normalized_rows,
    }


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
    decision_request = manifest["f02_6_human_decision_request_summary"]
    lines.extend(
        [
            "",
            "## F02.6 Human Decision Request",
            "",
            f"- present: `{decision_request['present']}`",
            f"- status: `{decision_request['status']}`",
            f"- decision_owner_required: `{decision_request['decision_owner_required']}`",
            f"- current_allowed_action_ids: `{decision_request['current_allowed_action_ids']}`",
            f"- current_blocked_action_ids: `{decision_request['current_blocked_action_ids']}`",
            f"- post_decision_routes_are_current_authorization: `{decision_request['post_decision_routes_are_current_authorization']}`",
            f"- all_execution_disabled_now: `{decision_request['all_execution_disabled_now']}`",
            f"- remote_preflight_allowed_now: `{decision_request['remote_preflight_allowed_now']}`",
            f"- remote_training_allowed_now: `{decision_request['remote_training_allowed_now']}`",
            f"- formal_claim_allowed_now: `{decision_request['formal_claim_allowed_now']}`",
            f"- local_training_allowed_now: `{decision_request['local_training_allowed_now']}`",
        ]
    )
    command_index = manifest["source_regeneration_command_index_summary"]
    lines.extend(
        [
            "",
            "## Source Regeneration Command Index",
            "",
            f"- present: `{command_index['present']}`",
            f"- index_row_count: `{command_index['index_row_count']}`",
            f"- source_target_count: `{command_index['source_target_count']}`",
            f"- unknown_manual_count: `{command_index['unknown_manual_count']}`",
            f"- stage_mismatch_count: `{command_index['stage_mismatch_count']}`",
            f"- command_not_in_stage_count: `{command_index['command_not_in_stage_count']}`",
            f"- forbidden_command_count: `{command_index['forbidden_command_count']}`",
        ]
    )
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
            "### Remaining Deliverables Gap Summary",
            "",
            f"- ledger_path: `{manifest['remaining_deliverables_gap_summary']['path']}`",
            f"- ledger_exists: `{manifest['remaining_deliverables_gap_summary']['exists']}`",
            f"- ledger_total_missing_deliverables: `{manifest['remaining_deliverables_gap_summary']['total_missing_deliverables']}`",
            f"- ledger_open_category_count: `{manifest['remaining_deliverables_gap_summary']['open_category_count']}`",
            f"- status_report_total_missing_deliverables: `{manifest['status_report_summary']['remaining_deliverables_gap_summary']['total_missing_deliverables']}`",
            f"- status_report_open_category_count: `{manifest['status_report_summary']['remaining_deliverables_gap_summary']['open_category_count']}`",
            "",
            "### Remaining Deliverables Unlock Chain",
            "",
            f"- ledger_path: `{manifest['remaining_deliverables_unlock_chain_summary']['path']}`",
            f"- ledger_exists: `{manifest['remaining_deliverables_unlock_chain_summary']['exists']}`",
            f"- status: `{manifest['remaining_deliverables_unlock_chain_summary']['status']}`",
            f"- row_count: `{manifest['remaining_deliverables_unlock_chain_summary']['row_count']}`",
            f"- blocked_row_count: `{manifest['remaining_deliverables_unlock_chain_summary']['blocked_row_count']}`",
            f"- rows_with_missing_required_blockers: `{manifest['remaining_deliverables_unlock_chain_summary']['rows_with_missing_required_blockers']}`",
            f"- rows_allowed_while_missing: `{manifest['remaining_deliverables_unlock_chain_summary']['rows_allowed_while_missing']}`",
            "",
            "### Status Report Proof-Audit Deliverables Summary",
            "",
            f"- present: `{manifest['status_report_proof_audit_deliverables_summary']['present']}`",
            f"- missing_counts_by_formal_category: `{manifest['status_report_proof_audit_deliverables_summary']['missing_counts_by_formal_category']}`",
            f"- next_blocked_lane: `{manifest['status_report_proof_audit_deliverables_summary']['next_blocked_lane']}`",
            f"- h01_status: `{manifest['status_report_proof_audit_deliverables_summary']['h01_status']}`",
            f"- h02_status: `{manifest['status_report_proof_audit_deliverables_summary']['h02_status']}`",
            f"- h02_paper_result_input_allowed: `{manifest['status_report_proof_audit_deliverables_summary']['h02_paper_result_input_allowed']}`",
            "",
            "### Status Report Handoff Summary",
            "",
            f"- status: `{manifest['status_report_summary']['formal_gate_handoff_summary'].get('status')}`",
            f"- remote_training_allowed_now: `{manifest['status_report_summary']['formal_gate_handoff_summary'].get('remote_training_allowed_now')}`",
            f"- safety_issue_count: `{manifest['status_report_summary']['formal_gate_handoff_summary'].get('safety_issue_count')}`",
            "",
            "### Status Report Execution Veto Matrix",
            "",
            f"- present: `{manifest['status_report_summary']['formal_gate_execution_veto_summary'].get('present')}`",
            f"- all_rows_consistent: `{manifest['status_report_summary']['formal_gate_execution_veto_summary'].get('all_rows_consistent')}`",
            f"- mismatch_rows: `{manifest['status_report_summary']['formal_gate_execution_veto_summary'].get('mismatch_rows')}`",
            "",
            "### Status Report Remote Execution Steps",
            "",
        ]
    )
    for row_id, allowed_now in manifest["status_report_summary"]["formal_gate_execution_veto_summary"].get("row_consensus", {}).items():
        lines.append(f"- `{row_id}`: consensus_allowed_now=`{allowed_now}`")
    lines.append("")
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
    return module2_source_head()


if __name__ == "__main__":
    raise SystemExit(main())
