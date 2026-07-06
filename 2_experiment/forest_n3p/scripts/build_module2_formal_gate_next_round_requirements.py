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
DEFAULT_PROTOCOL_LANE_STATUS_REPORT = Path(
    "0_trials/module2_formal_gate_protocol_lane_status_report/protocol_lane_status_report.json"
)
DEFAULT_REMOTE_PACKET_SAFETY = Path("0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json")
EXPECTED_NEXT_ATTEMPT_CATEGORY_COUNTS = {
    "contract": 1,
    "training": 3,
    "evaluation": 2,
    "acceptance": 3,
    "formal_acceptance": 1,
}


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
    protocol_lane_status_report_path: Path = DEFAULT_PROTOCOL_LANE_STATUS_REPORT
    remote_packet_safety_path: Path = DEFAULT_REMOTE_PACKET_SAFETY


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
        protocol_lane_status_report_path=args.protocol_lane_status_report,
        remote_packet_safety_path=args.remote_packet_safety_audit,
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
    protocol_lane_status = _read_json(config.protocol_lane_status_report_path)
    remote_packet_safety = _read_json(config.remote_packet_safety_path)

    current_failure = _current_failure(failure_triage=failure_triage, gate3_audit=gate3_audit)
    current_artifacts = _current_artifacts(remaining)
    formal_acceptance = _formal_acceptance(h02=h02, remaining=remaining)
    permissions = _permissions(status_report=status_report, failure_triage=failure_triage)
    next_round = _next_round_matrix()
    next_artifacts = _next_success_attempt_artifact_index()
    protocol_gate = _protocol_gate_summary(
        protocol_lane_status=protocol_lane_status,
        remote_packet_safety=remote_packet_safety,
        next_artifacts=next_artifacts,
    )
    reconciliation = _current_vs_next_attempt_reconciliation(
        current_artifacts=current_artifacts,
        next_artifacts=next_artifacts,
        protocol_gate=protocol_gate,
    )
    audit_issues = _audit_issues(
        failure_triage=failure_triage,
        current_failure=current_failure,
        current_artifacts=current_artifacts,
        formal_acceptance=formal_acceptance,
        permissions=permissions,
        protocol_gate=protocol_gate,
        reconciliation=reconciliation,
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
            "protocol_lane_status_report": str(config.protocol_lane_status_report_path),
            "remote_packet_safety_audit": str(config.remote_packet_safety_path),
        },
        "current_failed_run": current_failure,
        "current_run_artifacts": current_artifacts,
        "blocked_formal_acceptance": formal_acceptance,
        "permissions_now": permissions,
        "protocol_gate_summary": protocol_gate,
        "current_vs_next_attempt_reconciliation": reconciliation,
        "next_round_requirements": next_round,
        "next_success_attempt_artifact_index": next_artifacts,
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
    parser.add_argument("--protocol-lane-status-report", type=Path, default=DEFAULT_PROTOCOL_LANE_STATUS_REPORT)
    parser.add_argument("--remote-packet-safety-audit", type=Path, default=DEFAULT_REMOTE_PACKET_SAFETY)
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
    next_gate_status = next_gate.get("status")
    gate_blocks_execution = bool(
        new_contract_required
        or next_gate_status == "requires_protocol_decision_before_new_success_attempt"
    )
    raw_remote_preflight_allowed = bool(raw.get("remote_preflight_allowed_now"))
    raw_remote_training_allowed = bool(raw.get("remote_training_allowed_now"))
    raw_formal_h01_allowed = bool(raw.get("formal_h01_evaluation_allowed_now"))
    return {
        "local_training_allowed_now": bool(raw.get("local_training_allowed_now")),
        "remote_preflight_allowed_now": raw_remote_preflight_allowed and not gate_blocks_execution,
        "remote_training_allowed_now_for_existing_packet": raw_remote_training_allowed and not gate_blocks_execution,
        "formal_h01_evaluation_allowed_now": raw_formal_h01_allowed and not gate_blocks_execution,
        "formal_h02_acceptance_allowed_now": bool(raw.get("formal_h02_acceptance_allowed_now")),
        "formal_claim_allowed_now": bool(raw.get("formal_claim_allowed_now")),
        "source_freshness_ready_for_remote_preflight": bool(raw.get("source_freshness_ready_for_remote_preflight"))
        and not gate_blocks_execution,
        "new_success_training_allowed_now": not new_contract_required,
        "new_or_revised_contract_required_before_new_success_training": new_contract_required,
        "failure_triage_next_gate_status": next_gate_status,
        "execution_veto_reason": "protocol_lane_or_contract_gate_blocks_execution"
        if gate_blocks_execution
        else "none",
        "legacy_remote_packet_readiness": {
            "remote_preflight_allowed_by_status_report": raw_remote_preflight_allowed,
            "remote_training_allowed_by_status_report": raw_remote_training_allowed,
            "formal_h01_evaluation_allowed_by_status_report": raw_formal_h01_allowed,
            "superseded_by_next_gate": gate_blocks_execution,
        },
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


def _next_success_attempt_artifact_index() -> dict[str, Any]:
    rows = [
        _artifact(
            category="contract",
            artifact_id="new_or_revised_research_contract",
            status="missing_required_before_new_success_training",
            expected_path=".pipeline/contracts/module2-<selected_protocol_lane>-<version>.md",
            required_before="new_success_training",
            blocked_until="record_protocol_lane_decision",
            proof_requirement="contract status is approved or frozen and locks hypothesis, success signal, failure signal, budget, and protocol deltas",
            invalid_substitutes=[
                "chat-only approval",
                "draft contract",
                "editing the failed Gate3 result after seeing failure",
            ],
        ),
        _artifact(
            category="training",
            artifact_id="train_final_model_zip",
            status="not_created_for_next_success_attempt",
            expected_path="0_trials/module2_gate3_formal/<next_attempt_id>/train/final_model.zip",
            required_before="new_gate3_formal_audit",
            blocked_until="approved_or_frozen_new_or_revised_contract",
            proof_requirement="remote-produced PPO checkpoint pulled back from gpu3070ti-relay",
            invalid_substitutes=[
                "local PPO training output",
                "failed warm-start checkpoint",
                "checkpoint without manifest or hash provenance",
            ],
        ),
        _artifact(
            category="training",
            artifact_id="train_summary_json",
            status="not_created_for_next_success_attempt",
            expected_path="0_trials/module2_gate3_formal/<next_attempt_id>/train/summary.json",
            required_before="new_gate3_formal_audit",
            blocked_until="approved_or_frozen_new_or_revised_contract",
            proof_requirement="summary records protocol label, training budget, seed, and terminal-RS training signals",
            invalid_substitutes=[
                "stdout-only training summary",
                "summary from the failed Gate3 attempt",
                "summary without protocol label",
            ],
        ),
        _artifact(
            category="training",
            artifact_id="train_training_manifest_json",
            status="not_created_for_next_success_attempt",
            expected_path="0_trials/module2_gate3_formal/<next_attempt_id>/train/training_manifest.json",
            required_before="new_gate3_formal_audit",
            blocked_until="approved_or_frozen_new_or_revised_contract",
            proof_requirement="manifest records source head, host, command provenance, seed, and selected protocol lane",
            invalid_substitutes=[
                "manifest without source head",
                "manifest from a different protocol lane",
                "uncommitted chat note",
            ],
        ),
        _artifact(
            category="evaluation",
            artifact_id="eval_gate3_eval_episodes_csv",
            status="blocked_until_new_checkpoint",
            expected_path="0_trials/module2_gate3_formal/<next_attempt_id>/eval/gate3_eval_episodes.csv",
            required_before="new_gate3_formal_audit",
            blocked_until="new_remote_ppo_checkpoint_bundle",
            proof_requirement="per-episode formal Gate3 CSV with at least 64 episodes and protocol provenance",
            invalid_substitutes=[
                "H02 available-subset smoke CSV",
                "no-warm failure rows reused for a warm-start claim",
                "aggregate summary without per-episode rows",
            ],
        ),
        _artifact(
            category="evaluation",
            artifact_id="eval_gate3_summary_json",
            status="blocked_until_new_checkpoint",
            expected_path="0_trials/module2_gate3_formal/<next_attempt_id>/eval/gate3_summary.json",
            required_before="new_gate3_formal_audit",
            blocked_until="new_remote_ppo_checkpoint_bundle",
            proof_requirement="summary records terminal-RS success, collision, truncation, timing, seed, and protocol label",
            invalid_substitutes=[
                "summary from failed run",
                "summary without timing fields",
                "paper table preview",
            ],
        ),
        _artifact(
            category="acceptance",
            artifact_id="gate3_trial_manifest_json",
            status="blocked_until_new_eval",
            expected_path="0_trials/module2_gate3_formal/<next_attempt_id>/gate3_trial_manifest.json",
            required_before="h02_formal_output_acceptance",
            blocked_until="new_formal_gate3_eval_bundle",
            proof_requirement="trial manifest ties contract, train, eval, audit, source head, and selected protocol lane",
            invalid_substitutes=[
                "trial manifest from failed run",
                "manifest without contract reference",
                "manifest without evaluated checkpoint identity",
            ],
        ),
        _artifact(
            category="acceptance",
            artifact_id="gate3_formal_audit_json",
            status="blocked_until_new_eval",
            expected_path="0_trials/module2_gate3_formal/<next_attempt_id>/gate3_formal_audit.json",
            required_before="h02_formal_output_acceptance",
            blocked_until="new_formal_gate3_eval_bundle",
            proof_requirement="audit records formal_decision=pass for the new approved protocol attempt",
            invalid_substitutes=[
                "formal_decision=fail reinterpreted as success",
                "audit marked smoke, preview, or candidate",
                "audit from a different protocol lane",
            ],
        ),
        _artifact(
            category="acceptance",
            artifact_id="pulled_back_checkpoint_hash_record",
            status="blocked_until_new_eval",
            expected_path="0_trials/module2_gate3_formal/<next_attempt_id>/train/final_model.zip.sha256 or .sha256.json",
            required_before="h02_formal_output_acceptance",
            blocked_until="new_formal_gate3_eval_bundle",
            proof_requirement="hash record matches the pulled-back final_model.zip evaluated by Gate3",
            invalid_substitutes=[
                "checkpoint without hash record",
                "hash for a different checkpoint",
                "remote stdout without local pullback",
            ],
        ),
        _artifact(
            category="formal_acceptance",
            artifact_id="h02_formal_output_acceptance",
            status="blocked_until_new_gate3_pass",
            expected_path="0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json",
            required_before="paper_result_material",
            blocked_until="new_gate3_audit_and_hash_acceptance",
            proof_requirement="H02 records formal_output_accepted=true, paper_result_input_allowed=true, PPO rows, and accepted checkpoint hash",
            invalid_substitutes=[
                "blocked H02 acceptance",
                "formal-looking smoke table",
                "PPO rows without checkpoint hash",
            ],
        ),
    ]
    return {
        "status": "blocked_until_protocol_lane_decision_and_contract",
        "artifact_count": len(rows),
        "categories": ["contract", "training", "evaluation", "acceptance", "formal_acceptance"],
        "rows": rows,
    }


def _protocol_gate_summary(
    *,
    protocol_lane_status: dict[str, Any],
    remote_packet_safety: dict[str, Any],
    next_artifacts: dict[str, Any],
) -> dict[str, Any]:
    current = (
        protocol_lane_status.get("current_status")
        if isinstance(protocol_lane_status.get("current_status"), dict)
        else {}
    )
    remote_cross = (
        remote_packet_safety.get("cross_gate_summary")
        if isinstance(remote_packet_safety.get("cross_gate_summary"), dict)
        else {}
    )
    remote_protocol = (
        remote_cross.get("post_plan_protocol_lane_status_summary")
        if isinstance(remote_cross.get("post_plan_protocol_lane_status_summary"), dict)
        else {}
    )
    protocol_counts = _int_dict(current.get("next_success_attempt_artifact_category_counts"))
    artifact_counts = _artifact_category_counts(next_artifacts)
    return {
        "protocol_status": protocol_lane_status.get("status"),
        "protocol_audit_issue_count": int(protocol_lane_status.get("audit_issue_count") or 0),
        "next_blocked_lane": current.get("next_blocked_lane"),
        "decision_record_status": current.get("decision_record_status"),
        "selected_lane_id": current.get("selected_lane_id"),
        "allowed_next_action_ids": _strings(current.get("allowed_next_action_ids")),
        "blocked_action_ids": _strings(current.get("blocked_action_ids")),
        "new_success_training_allowed_now": current.get("new_success_training_allowed_now")
        if isinstance(current.get("new_success_training_allowed_now"), bool)
        else None,
        "contract_drafting_allowed_now": current.get("contract_drafting_allowed_now")
        if isinstance(current.get("contract_drafting_allowed_now"), bool)
        else None,
        "contract_approval_allowed_now": current.get("contract_approval_allowed_now")
        if isinstance(current.get("contract_approval_allowed_now"), bool)
        else None,
        "post_decision_contract_plan_status": current.get("post_decision_contract_plan_status"),
        "post_decision_contract_plan_required_section_count": int(current.get("post_decision_contract_plan_required_section_count") or 0),
        "post_decision_contract_plan_shared_artifact_count": int(current.get("post_decision_contract_plan_shared_artifact_count") or 0),
        "post_decision_contract_plan_lane_count": int(current.get("post_decision_contract_plan_lane_count") or 0),
        "next_success_attempt_artifact_status": current.get("next_success_attempt_artifact_status"),
        "next_success_attempt_artifact_count": int(current.get("next_success_attempt_artifact_count") or 0),
        "next_success_attempt_artifact_category_counts": protocol_counts,
        "next_success_attempt_artifact_ids_by_category": _string_list_dict(
            current.get("next_success_attempt_artifact_ids_by_category")
        ),
        "artifact_index_category_counts": artifact_counts,
        "artifact_index_count": int(next_artifacts.get("artifact_count") or 0),
        "remote_safety_protocol_summary_present": bool(remote_protocol),
        "remote_safety_protocol_status": remote_protocol.get("status"),
        "remote_safety_protocol_next_blocked": remote_protocol.get("next_blocked_lane"),
        "remote_safety_allowed_next_action_ids": _strings(remote_protocol.get("allowed_next_action_ids")),
        "remote_safety_new_success_training_allowed_now": remote_protocol.get("new_success_training_allowed_now")
        if isinstance(remote_protocol.get("new_success_training_allowed_now"), bool)
        else None,
        "remote_safety_category_counts": _int_dict(remote_protocol.get("next_success_attempt_artifact_category_counts")),
    }


def _current_vs_next_attempt_reconciliation(
    *,
    current_artifacts: dict[str, Any],
    next_artifacts: dict[str, Any],
    protocol_gate: dict[str, Any],
) -> dict[str, Any]:
    current_missing = current_artifacts.get("missing_counts_by_formal_category")
    current_missing = current_missing if isinstance(current_missing, dict) else {}
    next_counts = _artifact_category_counts(next_artifacts)
    return {
        "current_failed_run_missing_counts": {
            str(category): int(count or 0)
            for category, count in current_missing.items()
            if category
        },
        "current_failed_run_training_eval_acceptance_closed": all(
            int(current_missing.get(category) or 0) == 0
            for category in ("training", "evaluation", "acceptance")
        ),
        "current_failed_run_formal_acceptance_open": int(current_missing.get("formal_acceptance") or 0) > 0,
        "next_success_attempt_status": next_artifacts.get("status"),
        "next_success_attempt_artifact_count": int(next_artifacts.get("artifact_count") or 0),
        "next_success_attempt_category_counts": next_counts,
        "protocol_lane_artifact_counts_match_index": protocol_gate.get("next_success_attempt_artifact_category_counts") == next_counts,
        "old_failed_run_artifacts_invalid_for_next_success_attempt": True,
        "next_success_attempt_requires_protocol_lane_decision": protocol_gate.get("next_blocked_lane") == "protocol_lane_decision",
        "next_success_attempt_allowed_action": protocol_gate.get("allowed_next_action_ids"),
        "explanation": (
            "The current failed-run ledger may show training/evaluation/acceptance present, "
            "but a new success attempt still requires a new/revised contract plus fresh training, "
            "evaluation, acceptance, and H02 formal acceptance artifacts under the selected protocol lane."
        ),
    }


def _artifact_category_counts(next_artifacts: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in next_artifacts.get("rows", []) if isinstance(next_artifacts.get("rows"), list) else []:
        if not isinstance(row, dict):
            continue
        category = row.get("category")
        if not category:
            continue
        counts[str(category)] = counts.get(str(category), 0) + 1
    return counts


def _artifact(
    *,
    category: str,
    artifact_id: str,
    status: str,
    expected_path: str,
    required_before: str,
    blocked_until: str,
    proof_requirement: str,
    invalid_substitutes: list[str],
) -> dict[str, Any]:
    return {
        "category": category,
        "artifact_id": artifact_id,
        "status": status,
        "expected_path": expected_path,
        "required_before": required_before,
        "blocked_until": blocked_until,
        "proof_requirement": proof_requirement,
        "invalid_substitutes": invalid_substitutes,
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
    protocol_gate: dict[str, Any],
    reconciliation: dict[str, Any],
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
    if permissions["remote_preflight_allowed_now"]:
        issues.append(_issue("remote_preflight_allowed", "Remote preflight must remain blocked until the protocol lane and contract gates allow it."))
    if permissions["remote_training_allowed_now_for_existing_packet"]:
        issues.append(_issue("remote_training_allowed", "Remote training must remain blocked until the protocol lane and contract gates allow it."))
    if permissions["formal_h01_evaluation_allowed_now"]:
        issues.append(_issue("formal_h01_evaluation_allowed", "Formal H01 evaluation must remain blocked until the protocol lane and contract gates allow it."))
    if permissions["formal_claim_allowed_now"]:
        issues.append(_issue("formal_claim_allowed", "Formal claim must remain blocked after failed Gate3."))
    if permissions["new_success_training_allowed_now"]:
        issues.append(_issue("new_success_training_allowed_without_contract", "New success training must be blocked until a new or revised contract is approved/frozen."))
    if protocol_gate.get("protocol_status") != "protocol_lane_status_blocked_pending_lane_decision":
        issues.append(_issue("protocol_lane_status_not_blocked", "Protocol lane status must stay blocked pending Dr Sun's lane decision."))
    if protocol_gate.get("protocol_audit_issue_count") != 0:
        issues.append(_issue("protocol_lane_audit_issues_open", "Protocol lane status report must have zero audit issues."))
    if protocol_gate.get("next_blocked_lane") != "protocol_lane_decision":
        issues.append(_issue("protocol_lane_next_blocked_drift", "Protocol lane next blocked lane must be protocol_lane_decision."))
    if protocol_gate.get("decision_record_status") != "pending_protocol_lane_decision":
        issues.append(_issue("protocol_lane_decision_record_not_pending", "Decision record must remain pending before Dr Sun selects a protocol lane."))
    if protocol_gate.get("selected_lane_id") is not None:
        issues.append(_issue("protocol_lane_selected_before_decision", "No protocol lane may be selected before record_protocol_lane_decision."))
    if protocol_gate.get("allowed_next_action_ids") != ["record_protocol_lane_decision"]:
        issues.append(_issue("protocol_lane_allowed_action_drift", "Only record_protocol_lane_decision is allowed now."))
    for action_id in (
        "local_training",
        "remote_success_training",
        "remote_preflight_for_new_success_attempt",
        "formal_claim",
        "paper_result_material",
    ):
        if action_id not in set(protocol_gate.get("blocked_action_ids", [])):
            issues.append(_issue(f"protocol_lane_missing_blocked_{action_id}", f"Protocol lane status must block {action_id}."))
    if protocol_gate.get("new_success_training_allowed_now") is not False:
        issues.append(_issue("protocol_lane_allows_new_success_training", "Protocol lane status must not allow new success training yet."))
    if protocol_gate.get("contract_drafting_allowed_now") is not False:
        issues.append(_issue("protocol_lane_allows_contract_drafting", "Contract drafting must remain blocked until the lane decision is recorded."))
    if protocol_gate.get("contract_approval_allowed_now") is not False:
        issues.append(_issue("protocol_lane_allows_contract_approval", "Contract approval must remain blocked until the lane decision is recorded."))
    if protocol_gate.get("post_decision_contract_plan_required_section_count") != 8:
        issues.append(_issue("post_decision_contract_section_count_drift", "Post-decision contract plan must keep eight required sections."))
    if protocol_gate.get("post_decision_contract_plan_shared_artifact_count") != 10:
        issues.append(_issue("post_decision_shared_artifact_count_drift", "Post-decision contract plan must keep ten shared artifacts."))
    if protocol_gate.get("post_decision_contract_plan_lane_count") != 4:
        issues.append(_issue("post_decision_lane_count_drift", "Post-decision contract plan must keep four lanes."))
    if protocol_gate.get("next_success_attempt_artifact_status") != "blocked_until_protocol_lane_decision_and_contract":
        issues.append(_issue("protocol_next_attempt_status_drift", "Next success attempt artifacts must stay blocked until lane decision and contract."))
    if protocol_gate.get("next_success_attempt_artifact_count") != 10:
        issues.append(_issue("protocol_next_attempt_count_drift", "Protocol lane status must still require ten next-attempt artifacts."))
    if protocol_gate.get("next_success_attempt_artifact_category_counts") != EXPECTED_NEXT_ATTEMPT_CATEGORY_COUNTS:
        issues.append(_issue("protocol_next_attempt_category_counts_drift", "Protocol next-attempt artifact category counts drifted."))
    if not protocol_gate.get("remote_safety_protocol_summary_present"):
        issues.append(_issue("remote_safety_missing_protocol_summary", "Remote packet safety must echo protocol lane status before next-round requirements can pass."))
    if protocol_gate.get("remote_safety_protocol_status") != protocol_gate.get("protocol_status"):
        issues.append(_issue("remote_safety_protocol_status_mismatch", "Remote packet safety protocol status must match protocol lane status."))
    if protocol_gate.get("remote_safety_protocol_next_blocked") != protocol_gate.get("next_blocked_lane"):
        issues.append(_issue("remote_safety_protocol_next_blocked_mismatch", "Remote packet safety next-blocked lane must match protocol lane status."))
    if protocol_gate.get("remote_safety_allowed_next_action_ids") != protocol_gate.get("allowed_next_action_ids"):
        issues.append(_issue("remote_safety_allowed_action_mismatch", "Remote packet safety allowed action list must match protocol lane status."))
    if protocol_gate.get("remote_safety_new_success_training_allowed_now") is not False:
        issues.append(_issue("remote_safety_allows_new_success_training", "Remote packet safety must not allow new success training."))
    if protocol_gate.get("remote_safety_category_counts") != protocol_gate.get("next_success_attempt_artifact_category_counts"):
        issues.append(_issue("remote_safety_protocol_counts_mismatch", "Remote packet safety artifact counts must match protocol lane status."))
    if not reconciliation.get("protocol_lane_artifact_counts_match_index"):
        issues.append(_issue("protocol_artifact_counts_do_not_match_index", "Protocol lane category counts must match next success attempt artifact index."))
    if not reconciliation.get("current_failed_run_training_eval_acceptance_closed"):
        issues.append(_issue("current_failed_run_not_closed_for_failure_record", "Current failed run must have training/evaluation/acceptance closed before this handoff is authoritative."))
    if not reconciliation.get("current_failed_run_formal_acceptance_open"):
        issues.append(_issue("current_failed_run_formal_acceptance_not_open", "Failed run should remain blocked at formal acceptance, not accepted as paper input."))
    if not reconciliation.get("old_failed_run_artifacts_invalid_for_next_success_attempt"):
        issues.append(_issue("failed_run_artifacts_reusable_for_next_attempt", "Failed-run artifacts must be invalid substitutes for the next success attempt."))
    return _unique_issues(issues)


def _markdown(manifest: dict[str, Any]) -> str:
    failure = manifest["current_failed_run"]
    artifacts = manifest["current_run_artifacts"]
    h02 = manifest["blocked_formal_acceptance"]
    permissions = manifest["permissions_now"]
    protocol = manifest["protocol_gate_summary"]
    reconciliation = manifest["current_vs_next_attempt_reconciliation"]
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
        f"- execution_veto_reason: `{permissions['execution_veto_reason']}`",
        "- legacy_remote_packet_readiness:",
        f"  - remote_preflight_allowed_by_status_report: `{permissions['legacy_remote_packet_readiness']['remote_preflight_allowed_by_status_report']}`",
        f"  - remote_training_allowed_by_status_report: `{permissions['legacy_remote_packet_readiness']['remote_training_allowed_by_status_report']}`",
        f"  - formal_h01_evaluation_allowed_by_status_report: `{permissions['legacy_remote_packet_readiness']['formal_h01_evaluation_allowed_by_status_report']}`",
        f"  - superseded_by_next_gate: `{permissions['legacy_remote_packet_readiness']['superseded_by_next_gate']}`",
        "",
        "## Protocol Gate Summary",
        "",
        f"- protocol_status: `{protocol['protocol_status']}`",
        f"- next_blocked_lane: `{protocol['next_blocked_lane']}`",
        f"- decision_record_status: `{protocol['decision_record_status']}`",
        f"- selected_lane_id: `{protocol['selected_lane_id']}`",
        f"- allowed_next_action_ids: `{protocol['allowed_next_action_ids']}`",
        f"- blocked_action_ids: `{protocol['blocked_action_ids']}`",
        f"- new_success_training_allowed_now: `{protocol['new_success_training_allowed_now']}`",
        f"- post_decision_contract_plan_required_section_count: `{protocol['post_decision_contract_plan_required_section_count']}`",
        f"- post_decision_contract_plan_shared_artifact_count: `{protocol['post_decision_contract_plan_shared_artifact_count']}`",
        f"- post_decision_contract_plan_lane_count: `{protocol['post_decision_contract_plan_lane_count']}`",
        f"- next_success_attempt_artifact_count: `{protocol['next_success_attempt_artifact_count']}`",
        f"- next_success_attempt_artifact_category_counts: `{protocol['next_success_attempt_artifact_category_counts']}`",
        f"- remote_safety_protocol_summary_present: `{protocol['remote_safety_protocol_summary_present']}`",
        f"- remote_safety_category_counts: `{protocol['remote_safety_category_counts']}`",
        "",
        "## Current Vs Next Attempt Reconciliation",
        "",
        f"- current_failed_run_missing_counts: `{reconciliation['current_failed_run_missing_counts']}`",
        f"- current_failed_run_training_eval_acceptance_closed: `{reconciliation['current_failed_run_training_eval_acceptance_closed']}`",
        f"- current_failed_run_formal_acceptance_open: `{reconciliation['current_failed_run_formal_acceptance_open']}`",
        f"- next_success_attempt_artifact_count: `{reconciliation['next_success_attempt_artifact_count']}`",
        f"- next_success_attempt_category_counts: `{reconciliation['next_success_attempt_category_counts']}`",
        f"- protocol_lane_artifact_counts_match_index: `{reconciliation['protocol_lane_artifact_counts_match_index']}`",
        f"- old_failed_run_artifacts_invalid_for_next_success_attempt: `{reconciliation['old_failed_run_artifacts_invalid_for_next_success_attempt']}`",
        f"- explanation: {reconciliation['explanation']}",
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
    artifact_index = manifest["next_success_attempt_artifact_index"]
    lines.extend(
        [
            "",
            "## Next Success Attempt Artifact Index",
            "",
            f"- status: `{artifact_index['status']}`",
            f"- artifact_count: `{artifact_index['artifact_count']}`",
            "",
            "| category | artifact_id | status | expected_path | blocked_until |",
            "|---|---|---|---|---|",
        ]
    )
    for row in artifact_index["rows"]:
        lines.append(
            f"| `{row['category']}` | `{row['artifact_id']}` | `{row['status']}` | "
            f"`{row['expected_path']}` | `{row['blocked_until']}` |"
        )
    lines.extend(["", "### Artifact Proof Requirements"])
    for row in artifact_index["rows"]:
        lines.extend(
            [
                "",
                f"#### `{row['category']}:{row['artifact_id']}`",
                f"- required_before: `{row['required_before']}`",
                f"- proof_requirement: {row['proof_requirement']}",
                "- invalid_substitutes:",
            ]
        )
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


def _int_dict(value: Any) -> dict[str, int]:
    if not isinstance(value, dict):
        return {}
    return {str(key): int(raw or 0) for key, raw in value.items() if key}


def _string_list_dict(value: Any) -> dict[str, list[str]]:
    if not isinstance(value, dict):
        return {}
    return {
        str(key): [str(item) for item in items if item]
        for key, items in value.items()
        if key and isinstance(items, list)
    }


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
