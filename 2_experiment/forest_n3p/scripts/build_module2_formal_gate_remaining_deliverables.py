from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_formal_gate_remaining_deliverables")
DEFAULT_STATUS_REPORT = Path("0_trials/module2_formal_gate_status_report/formal_gate_status_report.json")
DEFAULT_MISSING_ARTIFACTS = Path("0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json")
DEFAULT_CLOSURE_CHECKLIST = Path("0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json")
DEFAULT_REMOTE_PACKET = Path("0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json")
DEFAULT_H01_MANIFEST = Path("0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json")
DEFAULT_H02_ACCEPTANCE = Path("0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json")
DEFAULT_SOURCE_FRESHNESS = Path("0_trials/module2_source_freshness_audit/source_freshness_audit.json")
DEFAULT_POST_F02_6_PLAN = Path("0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json")

DELIVERABLE_CATEGORIES = (
    ("training", "training_artifacts_required"),
    ("evaluation", "evaluation_artifacts_required"),
    ("acceptance", "acceptance_artifacts_required"),
    ("formal_acceptance", "evaluation_acceptance_required"),
)
FORMAL_REQUIREMENT_PHASE_BY_CATEGORY = {
    "training": "training",
    "evaluation": "evaluation",
    "acceptance": "acceptance",
    "formal_acceptance": "evaluation_acceptance",
}
CURRENT_BLOCKER_REQUIREMENTS_BY_CATEGORY = {
    "training": ("f02_6_decision_not_approved", "remote_packet_not_ready"),
    "evaluation": ("f02_6_decision_not_approved", "remote_packet_not_ready"),
    "acceptance": ("f02_6_decision_not_approved", "remote_packet_not_ready"),
    "formal_acceptance": ("missing_remote_audit_pullback",),
}
UNLOCK_SEQUENCE_BY_CATEGORY = {
    "training": (
        "record_f02_6_decision",
        "source_freshness_ready_for_remote_preflight",
        "remote_formal_execution_packet_ready",
        "approved_remote_preflight",
        "gate3_remote_training",
    ),
    "evaluation": (
        "record_f02_6_decision",
        "source_freshness_ready_for_remote_preflight",
        "remote_formal_execution_packet_ready",
        "approved_remote_preflight",
        "gate3_remote_training_complete",
        "gate3_remote_audit_pullback",
    ),
    "acceptance": (
        "record_f02_6_decision",
        "source_freshness_ready_for_remote_preflight",
        "remote_formal_execution_packet_ready",
        "approved_remote_preflight",
        "gate3_remote_training_complete",
        "gate3_remote_audit_pullback",
    ),
    "formal_acceptance": (
        "gate3_remote_audit_pullback_complete",
        "regenerate_h01_h02_formal_artifacts",
        "h01_h02_formal_acceptance_audit",
    ),
}
REMOTE_GENERATION_STAGE_BY_ARTIFACT = {
    "train_final_model_zip": "gate3_remote_training",
    "train_summary_json": "gate3_remote_training",
    "train_training_manifest_json": "gate3_remote_training",
    "eval_gate3_eval_episodes_csv": "gate3_remote_training",
    "eval_gate3_summary_json": "gate3_remote_training",
    "gate3_trial_manifest_json": "gate3_remote_training",
    "gate3_formal_audit_json": "gate3_remote_audit_pullback",
    "pulled_back_checkpoint_hash_record": "gate3_remote_audit_pullback",
    "h01_ready_for_formal_run": "regenerate_h01_h02_formal_artifacts",
    "h02_formal_output_acceptance": "regenerate_h01_h02_formal_artifacts",
}
LOCAL_MATERIALIZATION_STAGE_BY_CATEGORY = {
    "training": "gate3_remote_audit_pullback",
    "evaluation": "gate3_remote_audit_pullback",
    "acceptance": "gate3_remote_audit_pullback",
    "formal_acceptance": "regenerate_h01_h02_formal_artifacts",
}


@dataclass(frozen=True)
class FormalGateRemainingDeliverablesConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    status_report_path: Path = DEFAULT_STATUS_REPORT
    missing_artifacts_path: Path = DEFAULT_MISSING_ARTIFACTS
    closure_checklist_path: Path = DEFAULT_CLOSURE_CHECKLIST
    remote_packet_path: Path = DEFAULT_REMOTE_PACKET
    h01_manifest_path: Path = DEFAULT_H01_MANIFEST
    h02_acceptance_path: Path = DEFAULT_H02_ACCEPTANCE
    source_freshness_path: Path = DEFAULT_SOURCE_FRESHNESS
    post_f02_6_plan_path: Path = DEFAULT_POST_F02_6_PLAN


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = FormalGateRemainingDeliverablesConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        status_report_path=args.status_report,
        missing_artifacts_path=args.missing_artifacts,
        closure_checklist_path=args.closure_checklist,
        remote_packet_path=args.remote_packet,
        h01_manifest_path=args.h01_manifest,
        h02_acceptance_path=args.h02_acceptance,
        source_freshness_path=args.source_freshness,
        post_f02_6_plan_path=args.post_f02_6_plan,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "formal_gate_remaining_deliverables.json"
    markdown_out = config.markdown_out or output_dir / "formal_gate_remaining_deliverables.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: FormalGateRemainingDeliverablesConfig) -> dict[str, Any]:
    status_report = _read_json(config.status_report_path)
    missing_artifacts = _read_json(config.missing_artifacts_path)
    closure_checklist = _read_json(config.closure_checklist_path)
    remote_packet = _read_json(config.remote_packet_path)
    h01_manifest = _read_json(config.h01_manifest_path)
    h02_acceptance = _read_json(config.h02_acceptance_path)
    source_freshness = _read_json(config.source_freshness_path)
    post_f02_6_plan = _read_json(config.post_f02_6_plan_path)

    deliverable_groups = _deliverable_groups(
        status_report=status_report,
        closure_checklist=closure_checklist,
        missing_artifacts=missing_artifacts,
    )
    deliverable_acceptance_matrix = _deliverable_acceptance_matrix(deliverable_groups)
    deliverable_gap_summary = _deliverable_gap_summary(
        deliverable_groups=deliverable_groups,
        deliverable_acceptance_matrix=deliverable_acceptance_matrix,
    )
    proof_command_plan = _proof_command_plan(deliverable_acceptance_matrix)
    deliverable_production_plan = _deliverable_production_plan(
        deliverable_acceptance_matrix=deliverable_acceptance_matrix,
        post_f02_6_plan=post_f02_6_plan,
        remote_packet=remote_packet,
    )
    deliverable_unlock_chain = _deliverable_unlock_chain(deliverable_acceptance_matrix)
    category_counts = _category_counts(deliverable_groups)
    missing_counts_by_formal_category = {
        category: counts["missing_count"] for category, counts in category_counts.items()
    }
    permissions_now = _permissions(status_report=status_report, remote_packet=remote_packet, source_freshness=source_freshness)
    source_freshness_summary = _source_freshness_summary(source_freshness)
    source_freshness_blocking_targets_summary = _source_freshness_blocking_targets_summary(source_freshness)
    current_gate_summary = {
        "status_report_status": status_report.get("status"),
        "next_blocked_lane": _next_blocked_lane_id(status_report),
        "missing_counts_by_category": status_report.get("missing_counts_by_category")
        if isinstance(status_report.get("missing_counts_by_category"), dict)
        else {},
        "remote_packet_status": remote_packet.get("status"),
        "ready_to_run_remote_training": remote_packet.get("ready_to_run_remote_training"),
        "h01_status": h01_manifest.get("status"),
        "h02_status": h02_acceptance.get("status"),
        "h02_formal_output_accepted": h02_acceptance.get("formal_output_accepted"),
        "h02_paper_result_input_allowed": h02_acceptance.get("paper_result_input_allowed"),
        **source_freshness_summary,
        "source_freshness_blocking_target_count": source_freshness_blocking_targets_summary["blocking_target_count"],
        "source_freshness_blocking_target_ids": source_freshness_blocking_targets_summary["blocking_target_ids"],
    }
    audit_issues = _audit_issues(
        status_report=status_report,
        missing_artifacts=missing_artifacts,
        closure_checklist=closure_checklist,
        remote_packet=remote_packet,
        h01_manifest=h01_manifest,
        h02_acceptance=h02_acceptance,
        source_freshness=source_freshness,
        post_f02_6_plan=post_f02_6_plan,
        deliverable_groups=deliverable_groups,
        deliverable_acceptance_matrix=deliverable_acceptance_matrix,
        deliverable_production_plan=deliverable_production_plan,
        deliverable_unlock_chain=deliverable_unlock_chain,
    )
    missing_count = sum(group["missing_count"] for group in deliverable_groups)
    ready = missing_count == 0 and not audit_issues and status_report.get("status") == "formal_gate_status_ready_for_claim_audit"
    return {
        "schema_version": 1,
        "artifact_name": "module2_formal_gate_remaining_deliverables",
        "status": "formal_gate_deliverables_ready_for_claim_audit" if ready else "formal_gate_deliverables_blocked",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "local_training_allowed_now": permissions_now["local_training_allowed_now"],
        "remote_preflight_allowed_now": permissions_now["remote_preflight_allowed_now"],
        "remote_training_allowed_now": permissions_now["remote_training_allowed_now"],
        "formal_h01_evaluation_allowed_now": permissions_now["formal_h01_evaluation_allowed_now"],
        "formal_h02_acceptance_allowed_now": permissions_now["formal_h02_acceptance_allowed_now"],
        "formal_claim_allowed_now": permissions_now["formal_claim_allowed_now"],
        "paper_result_material_allowed_now": bool(current_gate_summary["h02_paper_result_input_allowed"])
        and bool(permissions_now["formal_claim_allowed_now"]),
        "inputs": {
            "formal_gate_status_report": str(config.status_report_path),
            "formal_gate_missing_artifacts": str(config.missing_artifacts_path),
            "formal_gate_closure_checklist": str(config.closure_checklist_path),
            "remote_formal_execution_packet": str(config.remote_packet_path),
            "h01_manifest": str(config.h01_manifest_path),
            "h02_formal_acceptance": str(config.h02_acceptance_path),
            "source_freshness_audit": str(config.source_freshness_path),
            "post_f02_6_regeneration_plan": str(config.post_f02_6_plan_path),
        },
        "current_gate_summary": current_gate_summary,
        "permissions_now": permissions_now,
        "category_counts": category_counts,
        "missing_counts_by_formal_category": missing_counts_by_formal_category,
        "missing_matrix_ids_by_formal_category": _missing_matrix_ids_by_category(deliverable_gap_summary),
        "next_blocked_lane": current_gate_summary["next_blocked_lane"],
        "h01_status": current_gate_summary["h01_status"],
        "h02_status": current_gate_summary["h02_status"],
        "h02_formal_output_accepted": current_gate_summary["h02_formal_output_accepted"],
        "h02_paper_result_input_allowed": current_gate_summary["h02_paper_result_input_allowed"],
        "deliverable_gap_summary": deliverable_gap_summary,
        "source_freshness_blocking_targets_summary": source_freshness_blocking_targets_summary,
        "proof_command_plan": proof_command_plan,
        "deliverable_production_plan": deliverable_production_plan,
        "deliverable_unlock_chain": deliverable_unlock_chain,
        "plain_formal_gate_closure_checklist": _plain_formal_gate_closure_checklist(
            current_gate_summary=current_gate_summary,
            permissions_now=permissions_now,
            deliverable_gap_summary=deliverable_gap_summary,
        ),
        "deliverable_groups": deliverable_groups,
        "deliverable_acceptance_matrix": deliverable_acceptance_matrix,
        "missing_deliverable_count": missing_count,
        "open_category_count": sum(1 for group in deliverable_groups if group["missing_count"] > 0),
        "audit_issue_count": len(audit_issues),
        "audit_issues": audit_issues,
        "claim_boundaries": [
            "This ledger lists remaining formal training, evaluation, and acceptance deliverables only.",
            "It does not approve F02.6, run ssh/rsync, run remote preflight, train, evaluate, audit, or pull back artifacts.",
            "Local training remains prohibited; formal PPO training remains gpu3070ti-relay-only after the formal gate opens.",
            "Smoke, preview, no-warm failure, stdout-only logs, and partial pullbacks are invalid substitutes for the listed deliverables.",
            "This ledger is not paper result material and must not be cited as a performance result.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a read-only ledger of remaining Module2 formal gate deliverables.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--status-report", type=Path, default=DEFAULT_STATUS_REPORT)
    parser.add_argument("--missing-artifacts", type=Path, default=DEFAULT_MISSING_ARTIFACTS)
    parser.add_argument("--closure-checklist", type=Path, default=DEFAULT_CLOSURE_CHECKLIST)
    parser.add_argument("--remote-packet", type=Path, default=DEFAULT_REMOTE_PACKET)
    parser.add_argument("--h01-manifest", type=Path, default=DEFAULT_H01_MANIFEST)
    parser.add_argument("--h02-acceptance", type=Path, default=DEFAULT_H02_ACCEPTANCE)
    parser.add_argument("--source-freshness", type=Path, default=DEFAULT_SOURCE_FRESHNESS)
    parser.add_argument("--post-f02-6-plan", type=Path, default=DEFAULT_POST_F02_6_PLAN)
    return parser.parse_args(list(argv) if argv is not None else None)


def _deliverable_groups(
    *,
    status_report: dict[str, Any],
    closure_checklist: dict[str, Any],
    missing_artifacts: dict[str, Any],
) -> list[dict[str, Any]]:
    requirement_by_phase = _formal_requirement_by_phase(missing_artifacts)
    groups: list[dict[str, Any]] = []
    for category, artifact_key in DELIVERABLE_CATEGORIES:
        raw_items = status_report.get(artifact_key)
        if not isinstance(raw_items, list):
            raw_items = closure_checklist.get(artifact_key)
        raw_list = raw_items if isinstance(raw_items, list) else []
        items = [_deliverable_item(item) for item in raw_list if isinstance(item, dict)]
        requirement = requirement_by_phase.get(FORMAL_REQUIREMENT_PHASE_BY_CATEGORY[category], {})
        invalid_substitutes = _strings(requirement.get("invalid_substitutes"))
        acceptable_evidence = _strings(requirement.get("acceptable_evidence"))
        groups.append(
            {
                "category": category,
                "status": "complete" if items and all(not item["missing"] for item in items) else "blocked",
                "item_count": len(items),
                "missing_count": sum(1 for item in items if item["missing"]),
                "present_count": sum(1 for item in items if item["exists"] and not item["missing"]),
                "responsible_stage_id": requirement.get("responsible_stage_id"),
                "responsible_stage_status": requirement.get("responsible_stage_status"),
                "responsible_stage_allowed_now": requirement.get("responsible_stage_allowed_now")
                if isinstance(requirement.get("responsible_stage_allowed_now"), bool)
                else None,
                "responsible_stage_blocked_by": _strings(requirement.get("responsible_stage_blocked_by")),
                "acceptable_evidence": acceptable_evidence,
                "invalid_substitutes": invalid_substitutes,
                "items": items,
            }
        )
    return groups


def _deliverable_item(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_id": item.get("artifact_id"),
        "path": item.get("path"),
        "exists": item.get("exists") if isinstance(item.get("exists"), bool) else None,
        "state": item.get("state"),
        "missing": item.get("missing") is True,
        "reason": item.get("reason"),
    }


def _deliverable_acceptance_matrix(deliverable_groups: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group in deliverable_groups:
        category = str(group["category"])
        for item in group["items"]:
            artifact_id = str(item.get("artifact_id"))
            proof_commands = _acceptance_proof_commands(
                category=category,
                artifact_id=artifact_id,
                expected_path=str(item.get("path") or ""),
            )
            rows.append(
                {
                    "matrix_id": f"{category}:{artifact_id}",
                    "category": category,
                    "artifact_id": artifact_id,
                    "expected_path": item.get("path"),
                    "current_exists": item.get("exists"),
                    "current_state": item.get("state"),
                    "missing": item.get("missing"),
                    "missing_reason": item.get("reason"),
                    "responsible_stage_id": group.get("responsible_stage_id"),
                    "responsible_stage_status": group.get("responsible_stage_status"),
                    "responsible_stage_allowed_now": group.get("responsible_stage_allowed_now"),
                    "responsible_stage_blocked_by": list(group.get("responsible_stage_blocked_by", [])),
                    "acceptance_predicates": _acceptance_predicates(category=category, artifact_id=artifact_id),
                    "proof_commands": proof_commands,
                    "proof_command_count": len(proof_commands),
                    "acceptable_evidence": list(group.get("acceptable_evidence", [])),
                    "invalid_substitutes": list(group.get("invalid_substitutes", [])),
                    "execution_boundary": "read_only_no_execution",
                }
            )
    return rows


def _proof_command_plan(deliverable_acceptance_matrix: Sequence[dict[str, Any]]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for row in deliverable_acceptance_matrix:
        proof_commands = row.get("proof_commands")
        proof_commands = proof_commands if isinstance(proof_commands, list) else []
        rows.append(
            {
                "matrix_id": row.get("matrix_id"),
                "category": row.get("category"),
                "artifact_id": row.get("artifact_id"),
                "expected_path": row.get("expected_path"),
                "proof_command_count": len(proof_commands),
                "proof_command_ids": [
                    str(command.get("command_id"))
                    for command in proof_commands
                    if isinstance(command, dict) and command.get("command_id")
                ],
            }
        )
    return {
        "plan_id": "module2_formal_gate_local_read_only_proof_commands",
        "execution_boundary": "local_read_only_after_formal_remote_pullback",
        "not_paper_result_material": True,
        "runs_training": False,
        "runs_remote_preflight": False,
        "total_matrix_rows": len(rows),
        "total_proof_command_count": sum(int(row["proof_command_count"]) for row in rows),
        "rows": rows,
    }


def _deliverable_production_plan(
    *,
    deliverable_acceptance_matrix: Sequence[dict[str, Any]],
    post_f02_6_plan: dict[str, Any],
    remote_packet: dict[str, Any],
) -> dict[str, Any]:
    stage_by_id = _post_plan_stage_by_id(post_f02_6_plan)
    rows: list[dict[str, Any]] = []
    for item in deliverable_acceptance_matrix:
        artifact_id = str(item.get("artifact_id") or "")
        category = str(item.get("category") or "")
        expected_path = str(item.get("expected_path") or "")
        remote_stage_id = REMOTE_GENERATION_STAGE_BY_ARTIFACT.get(artifact_id)
        materialization_stage_id = LOCAL_MATERIALIZATION_STAGE_BY_CATEGORY.get(category)
        remote_stage = stage_by_id.get(str(remote_stage_id or ""), {})
        materialization_stage = stage_by_id.get(str(materialization_stage_id or ""), {})
        rows.append(
            {
                "matrix_id": item.get("matrix_id"),
                "category": category,
                "artifact_id": artifact_id,
                "expected_path": expected_path,
                "current_missing": item.get("missing"),
                "remote_generation_stage_id": remote_stage_id,
                "local_materialization_stage_id": materialization_stage_id,
                "remote_generation_stage": _stage_summary(remote_stage),
                "local_materialization_stage": _stage_summary(materialization_stage),
                "expected_path_listed_in_remote_generation_stage": _stage_lists_expected_path(
                    stage=remote_stage,
                    expected_path=expected_path,
                ),
                "expected_path_listed_in_local_materialization_stage": _stage_lists_expected_path(
                    stage=materialization_stage,
                    expected_path=expected_path,
                ),
                "hash_manifest_required_by_remote_packet": bool(
                    remote_packet.get("post_run_pullback", {}).get("hash_manifest_required")
                )
                if isinstance(remote_packet.get("post_run_pullback"), dict)
                else False,
                "post_plan_input_status": post_f02_6_plan.get("status"),
                "execution_boundary": "reference_only_no_execution",
                "not_paper_result_material": True,
            }
        )
    return {
        "plan_id": "module2_formal_gate_deliverable_production_plan",
        "source_plan": "post_f02_6_regeneration_plan",
        "post_plan_status": post_f02_6_plan.get("status"),
        "execution_boundary": "reference_only_no_execution",
        "not_paper_result_material": True,
        "runs_training": False,
        "runs_remote_preflight": False,
        "row_count": len(rows),
        "rows_missing_production_stage": sum(
            1 for row in rows if not row["remote_generation_stage_id"] or not row["remote_generation_stage"]
        ),
        "rows_missing_materialization_stage": sum(
            1 for row in rows if not row["local_materialization_stage_id"] or not row["local_materialization_stage"]
        ),
        "rows_allowed_while_missing": sum(
            1
            for row in rows
            if row["current_missing"] is True
            and (
                row["remote_generation_stage"].get("allowed_now") is True
                or row["local_materialization_stage"].get("allowed_now") is True
            )
        ),
        "rows": rows,
    }


def _post_plan_stage_by_id(post_f02_6_plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    stages = post_f02_6_plan.get("ordered_stages")
    stages = stages if isinstance(stages, list) else []
    out: dict[str, dict[str, Any]] = {}
    for stage in stages:
        if isinstance(stage, dict) and stage.get("stage_id"):
            out[str(stage["stage_id"])] = stage
    return out


def _stage_summary(stage: dict[str, Any]) -> dict[str, Any]:
    if not stage:
        return {}
    command_templates = stage.get("command_templates")
    evidence_paths = stage.get("evidence_paths")
    return {
        "stage_id": stage.get("stage_id"),
        "phase": stage.get("phase"),
        "status": stage.get("status"),
        "allowed_now": stage.get("allowed_now"),
        "blocked_by": _strings(stage.get("blocked_by")),
        "runs_training": stage.get("runs_training"),
        "runs_remote_preflight": stage.get("runs_remote_preflight"),
        "host": stage.get("host"),
        "command_template_count": len(command_templates) if isinstance(command_templates, list) else 0,
        "evidence_path_count": len(evidence_paths) if isinstance(evidence_paths, list) else 0,
    }


def _stage_lists_expected_path(*, stage: dict[str, Any], expected_path: str) -> bool:
    if not stage or not expected_path:
        return False
    candidate_paths = _path_candidate_literals(expected_path)
    evidence_paths = stage.get("evidence_paths")
    evidence = {str(item) for item in evidence_paths} if isinstance(evidence_paths, list) else set()
    return any(candidate in evidence for candidate in candidate_paths)


def _deliverable_unlock_chain(deliverable_acceptance_matrix: Sequence[dict[str, Any]]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for row in deliverable_acceptance_matrix:
        category = str(row.get("category") or "")
        observed_blockers = _strings(row.get("responsible_stage_blocked_by"))
        required_blockers = list(CURRENT_BLOCKER_REQUIREMENTS_BY_CATEGORY.get(category, ()))
        missing_required_blockers = [
            blocker
            for blocker in required_blockers
            if row.get("missing") is True and blocker not in observed_blockers
        ]
        rows.append(
            {
                "matrix_id": row.get("matrix_id"),
                "category": category,
                "artifact_id": row.get("artifact_id"),
                "missing": row.get("missing"),
                "current_state": row.get("current_state"),
                "responsible_stage_id": row.get("responsible_stage_id"),
                "responsible_stage_allowed_now": row.get("responsible_stage_allowed_now"),
                "responsible_stage_blocked_by": observed_blockers,
                "required_current_blockers": required_blockers,
                "missing_required_current_blockers": missing_required_blockers,
                "unlock_sequence_before_stage_allowed": list(UNLOCK_SEQUENCE_BY_CATEGORY.get(category, ())),
                "execution_boundary": row.get("execution_boundary"),
            }
        )
    blocked_rows = [row for row in rows if row["missing"] is True]
    return {
        "chain_id": "module2_formal_gate_missing_deliverable_unlock_chain",
        "status": "blocked_missing_formal_deliverables" if blocked_rows else "ready_for_claim_audit",
        "not_paper_result_material": True,
        "execution_boundary": "read_only_no_execution",
        "row_count": len(rows),
        "blocked_row_count": len(blocked_rows),
        "rows_with_missing_required_blockers": sum(
            1 for row in rows if row["missing_required_current_blockers"]
        ),
        "rows_allowed_while_missing": sum(
            1 for row in rows if row["missing"] is True and row["responsible_stage_allowed_now"] is True
        ),
        "rows": rows,
    }


def _acceptance_predicates(*, category: str, artifact_id: str) -> list[str]:
    generic = [
        "expected_path exists in the local pulled-back formal Gate3 artifact tree",
        "artifact state is not missing, blocked, smoke, preview, or candidate",
        "artifact provenance traces to the approved gpu3070ti-relay formal run after F02.6 closure",
    ]
    specific = {
        "train_final_model_zip": [
            "final_model.zip is non-empty and paired with summary.json plus training_manifest.json from the same run",
            "checkpoint is later referenced by the pulled-back SHA-256 record",
        ],
        "train_summary_json": [
            "summary.json parses as JSON and records formal PPO run metadata plus terminal-RS training signals",
            "summary protocol label matches the approved obstacle-summary warm-start formal Gate3 run",
        ],
        "train_training_manifest_json": [
            "training_manifest.json parses as JSON and records command provenance, source head, seed, and run host",
            "training host is gpu3070ti-relay and local_training_allowed remains false",
        ],
        "eval_gate3_eval_episodes_csv": [
            "gate3_eval_episodes.csv contains formal episode rows for the approved PPO/RL-RS method",
            "episode rows satisfy the H01 output schema including success, collision, truncation, and timing fields",
        ],
        "eval_gate3_summary_json": [
            "gate3_summary.json parses as JSON and summarizes the pulled-back formal evaluation CSV",
            "summary scope and row counts match the H01 formal evaluation manifest",
        ],
        "gate3_trial_manifest_json": [
            "gate3_trial_manifest.json records a formal non-smoke, non-preview, non-candidate trial",
            "manifest records source head, protocol label, host, seed, command provenance, and pullback paths",
        ],
        "gate3_formal_audit_json": [
            "gate3_formal_audit.json accepts the pulled-back run as formal and scoped to the approved protocol",
            "audit is generated after checkpoint, eval CSV, summary, manifest, and hash records are present",
        ],
        "pulled_back_checkpoint_hash_record": [
            "SHA-256 file or JSON exists for train/final_model.zip",
            "recorded digest matches the locally pulled-back final_model.zip",
        ],
        "h01_ready_for_formal_run": [
            "module2_v1_evaluation_manifest status is ready_for_formal_run or ready_for_formal_evaluation",
            "manifest references the audited PPO checkpoint and requires formal PPO result rows",
        ],
        "h02_formal_output_acceptance": [
            "h02_formal_acceptance has formal_output_accepted=true and paper_result_input_allowed=true",
            "acceptance is regenerated from audited remote artifacts and rejects smoke or preview substitutes",
        ],
    }
    return generic + specific.get(artifact_id, [f"{category} artifact has an explicit formal acceptance check"])


def _acceptance_proof_commands(*, category: str, artifact_id: str, expected_path: str) -> list[dict[str, str]]:
    exists_command = _python_exists_nonempty_command(expected_path)
    if artifact_id == "pulled_back_checkpoint_hash_record":
        exists_command = _python_sha256_record_exists_command(expected_path)
    common = [
        _proof_command(
            command_id=f"{artifact_id}_exists_nonempty",
            purpose="verify the expected formal artifact exists locally after pullback",
            command=exists_command,
            expected_evidence="exit_code=0",
        )
    ]
    specific = {
        "train_final_model_zip": [
            _proof_command(
                command_id="train_final_model_zip_valid_zip",
                purpose="verify the pulled-back PPO checkpoint is a readable SB3 zip",
                command=_python_zipfile_command(expected_path),
                expected_evidence="zipfile.is_zipfile(path) is true",
            )
        ],
        "train_summary_json": [
            _proof_command(
                command_id="train_summary_json_formal_warm_start_metadata",
                purpose="verify PPO training summary metadata matches the approved warm-start formal run",
                command=_python_json_assert_command(
                    expected_path,
                    "assert data.get('status') == 'complete'; "
                    "assert data.get('warm_start_status') == 'applied_obstacle_summary_bc'; "
                    "assert data.get('config', {}).get('curriculum_preset') == 'f03'; "
                    "assert data.get('config', {}).get('smoke') is False",
                ),
                expected_evidence="status=complete, warm_start_status=applied_obstacle_summary_bc, curriculum=f03, smoke=false",
            )
        ],
        "train_training_manifest_json": [
            _proof_command(
                command_id="train_training_manifest_json_provenance",
                purpose="verify training manifest records command provenance and source hashes",
                command=_python_json_assert_command(
                    expected_path,
                    "assert isinstance(data.get('command'), (str, list)); "
                    "assert data.get('command'); "
                    "assert isinstance(data.get('source_hashes'), dict) and data['source_hashes']; "
                    "assert data.get('config', {}).get('curriculum_preset') == 'f03'",
                ),
                expected_evidence="command provenance, source_hashes, and f03 curriculum are present",
            )
        ],
        "eval_gate3_eval_episodes_csv": [
            _proof_command(
                command_id="eval_gate3_eval_episodes_csv_schema",
                purpose="verify formal episode CSV row count and telemetry columns",
                command=_python_eval_csv_command(expected_path),
                expected_evidence="rows>=64 and terminal_rs_success/collision/truncated/nn_forward_time_s columns are present",
            )
        ],
        "eval_gate3_summary_json": [
            _proof_command(
                command_id="eval_gate3_summary_json_formal_scope",
                purpose="verify formal evaluation summary scope and minimum episode count",
                command=_python_json_assert_command(
                    expected_path,
                    "assert data.get('gate_name') == 'module2_f03_gate3'; "
                    "assert data.get('contract') == '.pipeline/contracts/module2-ppo-funnel-expansion.md'; "
                    "assert int(data.get('episodes', 0)) >= int(data.get('min_episodes', 64)) >= 64; "
                    "assert data.get('config', {}).get('curriculum_preset') == 'f03'",
                ),
                expected_evidence="gate_name, contract, f03 curriculum, and >=64 formal episodes are present",
            )
        ],
        "gate3_trial_manifest_json": [
            _proof_command(
                command_id="gate3_trial_manifest_json_formal_warm_start_scope",
                purpose="verify trial manifest is complete, non-smoke, and warm-start scoped",
                command=_python_json_assert_command(
                    expected_path,
                    "assert data.get('trial_name') == 'module2_f03_gate3_train_eval'; "
                    "assert data.get('status') == 'complete'; "
                    "assert data.get('smoke') is False; "
                    "assert data.get('formal_gate_claim') is False; "
                    "assert data.get('warm_start_status') == 'applied_obstacle_summary_bc'",
                ),
                expected_evidence="complete non-smoke trial with applied_obstacle_summary_bc warm start",
            )
        ],
        "gate3_formal_audit_json": [
            _proof_command(
                command_id="gate3_formal_audit_json_accepts_formal_scope",
                purpose="verify Gate3 audit accepts the pulled-back run as formal evidence",
                command=_python_json_assert_command(
                    expected_path,
                    "assert data.get('audit_name') == 'module2_f03_gate3_formal_audit'; "
                    "assert data.get('formal_decision') in {'pass', 'fail'}; "
                    "assert data.get('formal_claim_allowed') is True; "
                    "assert not data.get('formal_blockers')",
                ),
                expected_evidence="formal_decision is pass/fail and formal_blockers is empty",
            )
        ],
        "pulled_back_checkpoint_hash_record": [
            _proof_command(
                command_id="pulled_back_checkpoint_hash_record_matches_model",
                purpose="verify SHA-256 record matches the pulled-back final_model.zip",
                command=_python_sha256_match_command(expected_path),
                expected_evidence="recorded digest contains sha256(train/final_model.zip)",
            )
        ],
        "h01_ready_for_formal_run": [
            _proof_command(
                command_id="h01_ready_for_formal_run_status",
                purpose="verify H01 manifest is regenerated into formal-run-ready state",
                command=_python_json_assert_command(
                    expected_path,
                    "assert data.get('status') in {'ready_for_formal_run', 'ready_for_formal_evaluation'}",
                ),
                expected_evidence="H01 status is ready_for_formal_run or ready_for_formal_evaluation",
            )
        ],
        "h02_formal_output_acceptance": [
            _proof_command(
                command_id="h02_formal_output_acceptance_status",
                purpose="verify H02 accepts formal outputs for paper-result input",
                command=_python_json_assert_command(
                    expected_path,
                    "assert data.get('status') == 'formal_output_accepted'; "
                    "assert data.get('formal_output_accepted') is True; "
                    "assert data.get('paper_result_input_allowed') is True",
                ),
                expected_evidence="formal_output_accepted=true and paper_result_input_allowed=true",
            )
        ],
    }
    fallback = [
        _proof_command(
            command_id=f"{artifact_id}_{category}_explicit_acceptance",
            purpose="verify the artifact has an explicit formal acceptance check",
            command=_python_exists_nonempty_command(expected_path),
            expected_evidence="exit_code=0",
        )
    ]
    return common + specific.get(artifact_id, fallback)


def _proof_command(*, command_id: str, purpose: str, command: str, expected_evidence: str) -> dict[str, str]:
    return {
        "command_id": command_id,
        "purpose": purpose,
        "command": command,
        "expected_evidence": expected_evidence,
        "execution_boundary": "local_read_only_after_formal_remote_pullback",
    }


def _python_exists_nonempty_command(path: str) -> str:
    return f"python -c \"from pathlib import Path; p=Path({path!r}); assert p.is_file() and p.stat().st_size > 0, p\""


def _python_zipfile_command(path: str) -> str:
    return f"python -c \"from pathlib import Path; import zipfile; p=Path({path!r}); assert p.is_file() and zipfile.is_zipfile(p), p\""


def _python_json_assert_command(path: str, assertion_source: str) -> str:
    return (
        "python -c "
        f"\"import json; from pathlib import Path; p=Path({path!r}); "
        "data=json.loads(p.read_text(encoding='utf-8')); assert isinstance(data, dict); "
        f"{assertion_source}\""
    )


def _python_eval_csv_command(path: str) -> str:
    required = "{'terminal_rs_success','collision','truncated','nn_forward_time_s'}"
    return (
        "python -c "
        f"\"import csv; from pathlib import Path; p=Path({path!r}); "
        "rows=list(csv.DictReader(p.open(newline='', encoding='utf-8'))); "
        f"required={required}; assert len(rows) >= 64; assert required.issubset(rows[0])\""
    )


def _path_candidate_literals(path: str) -> list[str]:
    candidates = [candidate.strip() for candidate in path.split(" or ") if candidate.strip()]
    if len(candidates) <= 1:
        return candidates or [path]
    first = Path(candidates[0])
    normalized = [str(first)]
    for candidate in candidates[1:]:
        candidate_path = Path(candidate)
        if candidate_path.is_absolute() or candidate.startswith("0_trials/"):
            normalized.append(str(candidate_path))
        elif first.parent != Path(".") and candidate_path.parts and candidate_path.parts[0] == first.parent.name:
            normalized.append(str(first.parent.parent / candidate_path))
        elif first.parent != Path("."):
            normalized.append(str(first.parent / candidate_path))
        else:
            normalized.append(str(candidate_path))
    return normalized


def _python_sha256_record_exists_command(path: str) -> str:
    candidates = _path_candidate_literals(path)
    return (
        "python -c "
        f"\"from pathlib import Path; records=[Path(item) for item in {candidates!r}]; "
        "record=next((item for item in records if item.is_file()), None); "
        "assert record is not None and record.stat().st_size > 0, records\""
    )


def _python_sha256_match_command(path: str) -> str:
    candidates = _path_candidate_literals(path)
    model_path = str(Path(candidates[0]).with_name("final_model.zip"))
    return (
        "python -c "
        f"\"from pathlib import Path; import hashlib; records=[Path(item) for item in {candidates!r}]; "
        f"model=Path({model_path!r}); record=next((item for item in records if item.is_file()), None); "
        "assert record is not None and record.stat().st_size > 0, records; "
        "digest=hashlib.sha256(model.read_bytes()).hexdigest(); "
        "assert digest in record.read_text(encoding='utf-8')\""
    )


def _formal_requirement_by_phase(missing_artifacts: dict[str, Any]) -> dict[str, dict[str, Any]]:
    requirements = missing_artifacts.get("formal_gate_requirements")
    requirements = requirements if isinstance(requirements, list) else []
    out: dict[str, dict[str, Any]] = {}
    for item in requirements:
        if isinstance(item, dict) and item.get("phase"):
            out[str(item["phase"])] = item
    return out


def _category_counts(deliverable_groups: Sequence[dict[str, Any]]) -> dict[str, dict[str, int]]:
    return {
        str(group["category"]): {
            "item_count": int(group["item_count"]),
            "missing_count": int(group["missing_count"]),
            "present_count": int(group["present_count"]),
        }
        for group in deliverable_groups
    }


def _missing_matrix_ids_by_category(deliverable_gap_summary: dict[str, Any]) -> dict[str, list[str]]:
    categories = deliverable_gap_summary.get("categories")
    out: dict[str, list[str]] = {}
    for category in categories if isinstance(categories, list) else []:
        if not isinstance(category, dict) or not category.get("category"):
            continue
        missing_artifacts = category.get("missing_artifacts")
        matrix_ids: list[str] = []
        for item in missing_artifacts if isinstance(missing_artifacts, list) else []:
            if isinstance(item, dict) and item.get("matrix_id"):
                matrix_ids.append(str(item["matrix_id"]))
        out[str(category["category"])] = matrix_ids
    return out


def _deliverable_gap_summary(
    *,
    deliverable_groups: Sequence[dict[str, Any]],
    deliverable_acceptance_matrix: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    matrix_by_artifact_id = {
        str(row.get("artifact_id")): row for row in deliverable_acceptance_matrix if row.get("artifact_id")
    }
    categories: list[dict[str, Any]] = []
    for group in deliverable_groups:
        missing_artifacts: list[dict[str, Any]] = []
        for item in group["items"]:
            if item.get("missing") is not True:
                continue
            artifact_id = str(item.get("artifact_id"))
            row = matrix_by_artifact_id.get(artifact_id, {})
            acceptance_predicates = row.get("acceptance_predicates")
            invalid_substitutes = row.get("invalid_substitutes")
            proof_commands = row.get("proof_commands")
            proof_commands = proof_commands if isinstance(proof_commands, list) else []
            missing_artifacts.append(
                {
                    "matrix_id": row.get("matrix_id"),
                    "artifact_id": artifact_id,
                    "expected_path": item.get("path"),
                    "current_state": item.get("state"),
                    "missing_reason": item.get("reason"),
                    "acceptance_predicate_count": len(acceptance_predicates)
                    if isinstance(acceptance_predicates, list)
                    else 0,
                    "proof_command_count": len(proof_commands),
                    "proof_command_ids": [
                        str(command.get("command_id"))
                        for command in proof_commands
                        if isinstance(command, dict) and command.get("command_id")
                    ],
                    "invalid_substitutes": list(invalid_substitutes) if isinstance(invalid_substitutes, list) else [],
                }
            )
        categories.append(
            {
                "category": group.get("category"),
                "status": group.get("status"),
                "missing_count": group.get("missing_count"),
                "present_count": group.get("present_count"),
                "responsible_stage_id": group.get("responsible_stage_id"),
                "responsible_stage_allowed_now": group.get("responsible_stage_allowed_now"),
                "responsible_stage_blocked_by": list(group.get("responsible_stage_blocked_by", [])),
                "next_required_evidence": list(group.get("acceptable_evidence", [])),
                "missing_artifacts": missing_artifacts,
            }
        )
    return {
        "summary_id": "module2_formal_gate_missing_training_eval_acceptance_summary",
        "execution_boundary": "read_only_no_execution",
        "not_paper_result_material": True,
        "total_missing_deliverables": sum(int(group.get("missing_count", 0)) for group in deliverable_groups),
        "open_category_count": sum(1 for group in deliverable_groups if int(group.get("missing_count", 0)) > 0),
        "category_order": [str(group.get("category")) for group in deliverable_groups],
        "categories": categories,
    }


def _plain_formal_gate_closure_checklist(
    *,
    current_gate_summary: dict[str, Any],
    permissions_now: dict[str, Any],
    deliverable_gap_summary: dict[str, Any],
) -> dict[str, Any]:
    categories: list[dict[str, Any]] = []
    raw_categories = deliverable_gap_summary.get("categories")
    for category in raw_categories if isinstance(raw_categories, list) else []:
        if not isinstance(category, dict):
            continue
        missing_artifacts = category.get("missing_artifacts")
        missing_artifacts = missing_artifacts if isinstance(missing_artifacts, list) else []
        categories.append(
            {
                "category": category.get("category"),
                "missing_count": category.get("missing_count"),
                "responsible_stage_id": category.get("responsible_stage_id"),
                "responsible_stage_allowed_now": category.get("responsible_stage_allowed_now"),
                "responsible_stage_blocked_by": list(category.get("responsible_stage_blocked_by", [])),
                "missing_matrix_ids": [
                    str(item.get("matrix_id")) for item in missing_artifacts if isinstance(item, dict) and item.get("matrix_id")
                ],
                "expected_paths": [
                    str(item.get("expected_path")) for item in missing_artifacts if isinstance(item, dict) and item.get("expected_path")
                ],
                "invalid_substitutes": _unique_strings(
                    substitute
                    for item in missing_artifacts
                    if isinstance(item, dict)
                    for substitute in item.get("invalid_substitutes", [])
                ),
                "proof_command_ids": _unique_strings(
                    command_id
                    for item in missing_artifacts
                    if isinstance(item, dict)
                    for command_id in item.get("proof_command_ids", [])
                ),
            }
        )
    return {
        "purpose": "human_readable_formal_gate_missing_deliverables_only",
        "not_paper_result_material": True,
        "execution_boundary": deliverable_gap_summary.get("execution_boundary"),
        "next_blocked_lane": current_gate_summary.get("next_blocked_lane"),
        "total_missing_deliverables": deliverable_gap_summary.get("total_missing_deliverables"),
        "open_category_count": deliverable_gap_summary.get("open_category_count"),
        "local_training_allowed_now": permissions_now.get("local_training_allowed_now"),
        "remote_training_allowed_now": permissions_now.get("remote_training_allowed_now"),
        "formal_claim_allowed_now": permissions_now.get("formal_claim_allowed_now"),
        "categories": categories,
    }


def _permissions(*, status_report: dict[str, Any], remote_packet: dict[str, Any], source_freshness: dict[str, Any]) -> dict[str, Any]:
    permissions = status_report.get("permissions_now") if isinstance(status_report.get("permissions_now"), dict) else {}
    source_fresh = _source_freshness_ready_for_remote_preflight(source_freshness)
    return {
        "local_training_allowed_now": False,
        "remote_preflight_allowed_now": bool(permissions.get("remote_preflight_allowed_now")) and source_fresh,
        "remote_training_allowed_now": bool(permissions.get("remote_training_allowed_now")) and source_fresh,
        "formal_h01_evaluation_allowed_now": permissions.get("formal_h01_evaluation_allowed_now"),
        "formal_h02_acceptance_allowed_now": permissions.get("formal_h02_acceptance_allowed_now"),
        "formal_claim_allowed_now": permissions.get("formal_claim_allowed_now"),
        "remote_packet_ready_to_run_remote_training": remote_packet.get("ready_to_run_remote_training"),
        "source_freshness_ready_for_remote_preflight": source_fresh,
    }


def _audit_issues(
    *,
    status_report: dict[str, Any],
    missing_artifacts: dict[str, Any],
    closure_checklist: dict[str, Any],
    remote_packet: dict[str, Any],
    h01_manifest: dict[str, Any],
    h02_acceptance: dict[str, Any],
    source_freshness: dict[str, Any],
    post_f02_6_plan: dict[str, Any],
    deliverable_groups: Sequence[dict[str, Any]],
    deliverable_acceptance_matrix: Sequence[dict[str, Any]],
    deliverable_production_plan: dict[str, Any],
    deliverable_unlock_chain: dict[str, Any],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for name, payload in (
        ("status_report", status_report),
        ("missing_artifacts", missing_artifacts),
        ("closure_checklist", closure_checklist),
        ("remote_packet", remote_packet),
        ("h01_manifest", h01_manifest),
        ("h02_acceptance", h02_acceptance),
        ("source_freshness", source_freshness),
        ("post_f02_6_plan", post_f02_6_plan),
    ):
        issues.extend(_read_only_payload_issues(name, payload))
    if _source_freshness_ready_for_remote_preflight(source_freshness) is False:
        permissions = status_report.get("permissions_now") if isinstance(status_report.get("permissions_now"), dict) else {}
        if permissions.get("remote_preflight_allowed_now") is True or permissions.get("remote_training_allowed_now") is True:
            issues.append(
                _issue(
                    "remote_allowed_while_source_freshness_blocked",
                    "remote preflight/training cannot be allowed while source freshness requires regeneration.",
                )
            )
    categories = {str(group["category"]): group for group in deliverable_groups}
    for category, _artifact_key in DELIVERABLE_CATEGORIES:
        group = categories.get(category)
        if not group:
            issues.append(_issue(f"{category}_deliverable_group_missing", f"{category} deliverable group is missing."))
            continue
        if group["item_count"] == 0:
            issues.append(_issue(f"{category}_deliverable_items_missing", f"{category} deliverable group has no items."))
        if group["missing_count"] > 0 and group["status"] == "complete":
            issues.append(_issue(f"{category}_marked_complete_with_missing_items", f"{category} cannot be complete with missing items."))
        if category == "training":
            if group["responsible_stage_id"] != "gate3_remote_training":
                issues.append(_issue("training_wrong_responsible_stage", "training deliverables must be owned by gate3_remote_training."))
            if group["responsible_stage_allowed_now"] is True and status_report.get("status") != "formal_gate_status_ready_for_claim_audit":
                issues.append(_issue("training_allowed_while_status_report_blocked", "training stage cannot be allowed while status report is blocked."))
        if category in {"evaluation", "acceptance"} and group["responsible_stage_id"] != "gate3_remote_audit_pullback":
            issues.append(_issue(f"{category}_wrong_responsible_stage", f"{category} deliverables must be owned by gate3_remote_audit_pullback."))
        if category == "formal_acceptance" and group["responsible_stage_id"] != "regenerate_h01_h02_formal_artifacts":
            issues.append(_issue("formal_acceptance_wrong_responsible_stage", "formal acceptance must be owned by regenerate_h01_h02_formal_artifacts."))
        if group["missing_count"] > 0 and not group["invalid_substitutes"]:
            issues.append(_issue(f"{category}_missing_invalid_substitutes", f"{category} group must list invalid substitutes while blocked."))
    issues.extend(
        _acceptance_matrix_integrity_issues(
            deliverable_groups=deliverable_groups,
            deliverable_acceptance_matrix=deliverable_acceptance_matrix,
        )
    )
    issues.extend(_proof_command_safety_issues(deliverable_acceptance_matrix))
    issues.extend(_production_plan_safety_issues(deliverable_production_plan))
    issues.extend(_unlock_chain_safety_issues(deliverable_unlock_chain))
    return _unique_issues(issues)


def _acceptance_matrix_integrity_issues(
    *,
    deliverable_groups: Sequence[dict[str, Any]],
    deliverable_acceptance_matrix: Sequence[dict[str, Any]],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    expected_row_count = sum(int(group.get("item_count") or 0) for group in deliverable_groups if isinstance(group, dict))
    if len(deliverable_acceptance_matrix) != expected_row_count:
        issues.append(
            _issue(
                "acceptance_matrix_row_count_mismatch",
                "Acceptance matrix row count must match the deliverable group item count.",
            )
        )
    expected_missing_counts = {
        str(group.get("category")): int(group.get("missing_count") or 0)
        for group in deliverable_groups
        if isinstance(group, dict) and group.get("category")
    }
    actual_missing_counts = {category: 0 for category in expected_missing_counts}
    seen_matrix_ids: set[str] = set()
    seen_category_artifacts: set[tuple[str, str]] = set()
    for index, row in enumerate(deliverable_acceptance_matrix):
        if not isinstance(row, dict):
            issues.append(_issue(f"acceptance_matrix_row_{index}_malformed", "Acceptance matrix rows must be objects."))
            continue
        matrix_id = str(row.get("matrix_id") or "")
        category = str(row.get("category") or "")
        artifact_id = str(row.get("artifact_id") or "")
        safe_matrix_id = _safe_issue_id(matrix_id or f"row_{index}")
        if not matrix_id:
            issues.append(_issue(f"acceptance_matrix_row_{index}_missing_matrix_id", "Acceptance matrix row is missing matrix_id."))
        elif matrix_id in seen_matrix_ids:
            issues.append(
                _issue(
                    f"acceptance_matrix_{safe_matrix_id}_duplicate_matrix_id",
                    f"{matrix_id} appears more than once in the acceptance matrix.",
                )
            )
        seen_matrix_ids.add(matrix_id)
        if not category:
            issues.append(_issue(f"acceptance_matrix_{safe_matrix_id}_missing_category", f"{matrix_id} is missing category."))
        elif category not in expected_missing_counts:
            issues.append(
                _issue(
                    f"acceptance_matrix_{safe_matrix_id}_unknown_category",
                    f"{matrix_id} uses category {category}, which is not in deliverable groups.",
                )
            )
        if not artifact_id:
            issues.append(_issue(f"acceptance_matrix_{safe_matrix_id}_missing_artifact_id", f"{matrix_id} is missing artifact_id."))
        if category and artifact_id:
            expected_matrix_id = f"{category}:{artifact_id}"
            if matrix_id != expected_matrix_id:
                issues.append(
                    _issue(
                        f"acceptance_matrix_{safe_matrix_id}_identity_mismatch",
                        f"{matrix_id} must equal {expected_matrix_id}.",
                    )
                )
            category_artifact = (category, artifact_id)
            if category_artifact in seen_category_artifacts:
                issues.append(
                    _issue(
                        f"acceptance_matrix_{_safe_issue_id(expected_matrix_id)}_duplicate_category_artifact",
                        f"{expected_matrix_id} appears more than once in the acceptance matrix.",
                    )
                )
            seen_category_artifacts.add(category_artifact)
        if row.get("missing") is True:
            actual_missing_counts[category] = actual_missing_counts.get(category, 0) + 1
            if not _strings(row.get("invalid_substitutes")):
                issues.append(
                    _issue(
                        f"acceptance_matrix_{safe_matrix_id}_missing_invalid_substitutes",
                        f"{matrix_id} must list invalid substitutes while the deliverable is missing.",
                    )
                )
        if row.get("execution_boundary") != "read_only_no_execution":
            issues.append(
                _issue(
                    f"acceptance_matrix_{safe_matrix_id}_wrong_boundary",
                    f"{matrix_id} must remain read_only_no_execution.",
                )
            )
    for category, expected_count in expected_missing_counts.items():
        actual_count = actual_missing_counts.get(category, 0)
        if actual_count != expected_count:
            issues.append(
                _issue(
                    f"acceptance_matrix_{_safe_issue_id(category)}_missing_count_mismatch",
                    f"{category} acceptance matrix missing count must match deliverable group missing count.",
                )
            )
    return issues


def _production_plan_safety_issues(deliverable_production_plan: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if deliverable_production_plan.get("execution_boundary") != "reference_only_no_execution":
        issues.append(
            _issue(
                "deliverable_production_plan_wrong_boundary",
                "Deliverable production plan must only reference post-F02.6 stages and must not execute them.",
            )
        )
    if deliverable_production_plan.get("runs_training") is not False:
        issues.append(_issue("deliverable_production_plan_runs_training", "Production plan must not run training."))
    if deliverable_production_plan.get("runs_remote_preflight") is not False:
        issues.append(
            _issue(
                "deliverable_production_plan_runs_remote_preflight",
                "Production plan must not run remote preflight.",
            )
        )
    rows = deliverable_production_plan.get("rows")
    rows = rows if isinstance(rows, list) else []
    if int(deliverable_production_plan.get("row_count") or 0) != len(rows):
        issues.append(_issue("deliverable_production_plan_row_count_mismatch", "Production plan row count must match rows."))
    for row in rows:
        if not isinstance(row, dict):
            issues.append(_issue("deliverable_production_plan_malformed_row", "Production plan rows must be objects."))
            continue
        matrix_id = str(row.get("matrix_id") or "unknown_matrix")
        safe_matrix_id = _safe_issue_id(matrix_id)
        category = str(row.get("category") or "")
        artifact_id = str(row.get("artifact_id") or "")
        if row.get("execution_boundary") != "reference_only_no_execution":
            issues.append(
                _issue(
                    f"production_plan_{safe_matrix_id}_wrong_boundary",
                    f"{matrix_id} production row must remain reference-only.",
                )
            )
        expected_remote_stage = REMOTE_GENERATION_STAGE_BY_ARTIFACT.get(artifact_id)
        expected_materialization_stage = LOCAL_MATERIALIZATION_STAGE_BY_CATEGORY.get(category)
        if row.get("remote_generation_stage_id") != expected_remote_stage:
            issues.append(
                _issue(
                    f"production_plan_{safe_matrix_id}_wrong_generation_stage",
                    f"{matrix_id} must be generated by {expected_remote_stage}.",
                )
            )
        if row.get("local_materialization_stage_id") != expected_materialization_stage:
            issues.append(
                _issue(
                    f"production_plan_{safe_matrix_id}_wrong_materialization_stage",
                    f"{matrix_id} must be materialized by {expected_materialization_stage}.",
                )
            )
        remote_stage = row.get("remote_generation_stage") if isinstance(row.get("remote_generation_stage"), dict) else {}
        materialization_stage = (
            row.get("local_materialization_stage")
            if isinstance(row.get("local_materialization_stage"), dict)
            else {}
        )
        if not remote_stage:
            issues.append(
                _issue(
                    f"production_plan_{safe_matrix_id}_missing_generation_stage",
                    f"{matrix_id} is not mapped to a post-F02.6 generation stage.",
                )
            )
        if not materialization_stage:
            issues.append(
                _issue(
                    f"production_plan_{safe_matrix_id}_missing_materialization_stage",
                    f"{matrix_id} is not mapped to a post-F02.6 local materialization stage.",
                )
            )
        if row.get("current_missing") is True and remote_stage.get("allowed_now") is True:
            issues.append(
                _issue(
                    f"production_plan_{safe_matrix_id}_generation_allowed_while_missing",
                    f"{matrix_id} generation stage cannot already be allowed while the gate still records the deliverable as missing.",
                )
            )
        if row.get("current_missing") is True and materialization_stage.get("allowed_now") is True:
            issues.append(
                _issue(
                    f"production_plan_{safe_matrix_id}_materialization_allowed_while_missing",
                    f"{matrix_id} materialization stage cannot already be allowed while the gate still records the deliverable as missing.",
                )
            )
        if artifact_id == "pulled_back_checkpoint_hash_record" and row.get("hash_manifest_required_by_remote_packet") is not True:
            issues.append(
                _issue(
                    "production_plan_hash_record_not_required_by_remote_packet",
                    "Checkpoint hash record must be backed by remote packet post-run pullback hash_manifest_required=true.",
                )
            )
    return issues


def _unlock_chain_safety_issues(deliverable_unlock_chain: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if deliverable_unlock_chain.get("execution_boundary") != "read_only_no_execution":
        issues.append(
            _issue(
                "deliverable_unlock_chain_wrong_boundary",
                "Deliverable unlock chain must remain a local read-only audit.",
            )
        )
    rows = deliverable_unlock_chain.get("rows")
    rows = rows if isinstance(rows, list) else []
    for row in rows:
        if not isinstance(row, dict):
            issues.append(_issue("deliverable_unlock_chain_malformed_row", "Unlock-chain rows must be objects."))
            continue
        matrix_id = str(row.get("matrix_id") or "unknown_matrix")
        safe_matrix_id = _safe_issue_id(matrix_id)
        if row.get("missing") is True and row.get("responsible_stage_allowed_now") is True:
            issues.append(
                _issue(
                    f"unlock_chain_{safe_matrix_id}_allowed_while_missing",
                    f"{matrix_id} cannot have its responsible stage allowed while the formal deliverable is missing.",
                )
            )
        if row.get("missing") is True and row.get("missing_required_current_blockers"):
            issues.append(
                _issue(
                    f"unlock_chain_{safe_matrix_id}_missing_current_blockers",
                    f"{matrix_id} is missing required current blockers for its formal-gate category.",
                )
            )
        if row.get("missing") is True and row.get("execution_boundary") != "read_only_no_execution":
            issues.append(
                _issue(
                    f"unlock_chain_{safe_matrix_id}_wrong_boundary",
                    f"{matrix_id} must remain read-only while missing.",
                )
            )
        sequence = row.get("unlock_sequence_before_stage_allowed")
        if row.get("missing") is True and not sequence:
            issues.append(
                _issue(
                    f"unlock_chain_{safe_matrix_id}_missing_unlock_sequence",
                    f"{matrix_id} must declare the ordered prerequisites before the stage can be allowed.",
                )
            )
    return issues


def _proof_command_safety_issues(deliverable_acceptance_matrix: Sequence[dict[str, Any]]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    forbidden_tokens = (
        "ssh ",
        "rsync ",
        "scp ",
        "preflight_rl_rs_gate3_formal_trial",
        "run_rl_rs_gate3_trial",
        "audit_rl_rs_gate3_trial",
    )
    for row in deliverable_acceptance_matrix:
        matrix_id = str(row.get("matrix_id") or "unknown_matrix")
        safe_matrix_id = _safe_issue_id(matrix_id)
        proof_commands = row.get("proof_commands")
        proof_commands = proof_commands if isinstance(proof_commands, list) else []
        if not proof_commands:
            issues.append(_issue(f"proof_command_{safe_matrix_id}_missing", f"{matrix_id} must define proof commands."))
            continue
        if int(row.get("proof_command_count") or 0) != len(proof_commands):
            issues.append(_issue(f"proof_command_{safe_matrix_id}_count_mismatch", f"{matrix_id} proof command count must match commands."))
        seen_command_ids: set[str] = set()
        for command in proof_commands:
            if not isinstance(command, dict):
                issues.append(_issue(f"proof_command_{safe_matrix_id}_malformed", f"{matrix_id} proof command row must be an object."))
                continue
            command_id = str(command.get("command_id") or "unknown_command")
            safe_command_id = _safe_issue_id(command_id)
            command_text = str(command.get("command") or "")
            if command_id == "unknown_command":
                issues.append(_issue(f"proof_command_{safe_matrix_id}_missing_id", f"{matrix_id} proof command is missing command_id."))
            elif command_id in seen_command_ids:
                issues.append(
                    _issue(
                        f"proof_command_{safe_matrix_id}_{safe_command_id}_duplicate_id",
                        f"{matrix_id}:{command_id} must be unique within the proof command plan.",
                    )
                )
            seen_command_ids.add(command_id)
            if command.get("execution_boundary") != "local_read_only_after_formal_remote_pullback":
                issues.append(
                    _issue(
                        f"proof_command_{safe_matrix_id}_{safe_command_id}_wrong_boundary",
                        f"{matrix_id}:{command_id} must remain local read-only after formal remote pullback.",
                    )
                )
            if not command_text.startswith("python -c "):
                issues.append(
                    _issue(
                        f"proof_command_{safe_matrix_id}_{safe_command_id}_not_python_c",
                        f"{matrix_id}:{command_id} must be a local python -c proof command.",
                    )
                )
            if " or " in command_text:
                issues.append(
                    _issue(
                        f"proof_command_{safe_matrix_id}_{safe_command_id}_raw_or_path",
                        f"{matrix_id}:{command_id} must normalize alternative paths instead of embedding a raw 'or' path.",
                    )
                )
            if any(token in command_text for token in forbidden_tokens):
                issues.append(
                    _issue(
                        f"proof_command_{safe_matrix_id}_{safe_command_id}_forbidden_execution_token",
                        f"{matrix_id}:{command_id} must not contain remote, training, or audit execution commands.",
                    )
                )
    return issues


def _read_only_payload_issues(name: str, payload: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if payload.get("executes_commands") is True:
        issues.append(_issue(f"{name}_executes_commands", f"{name} must be read-only."))
    if payload.get("runs_training") is True:
        issues.append(_issue(f"{name}_runs_training", f"{name} must not run training."))
    if payload.get("runs_remote_preflight") is True:
        issues.append(_issue(f"{name}_runs_remote_preflight", f"{name} must not run remote preflight."))
    if payload.get("local_training_allowed") is True:
        issues.append(_issue(f"{name}_allows_local_training", f"{name} must preserve the local-training prohibition."))
    if payload.get("formal_claim_allowed") is True:
        issues.append(_issue(f"{name}_allows_formal_claim", f"{name} must not allow formal claims."))
    return issues


def _source_freshness_summary(source_freshness: dict[str, Any]) -> dict[str, Any]:
    commit_lag_summary = (
        source_freshness.get("commit_lag_summary")
        if isinstance(source_freshness.get("commit_lag_summary"), dict)
        else {}
    )
    return {
        "source_freshness_status": source_freshness.get("status"),
        "source_freshness_regeneration_required": source_freshness.get(
            "regeneration_required_before_remote_formal_execution"
        ),
        "source_freshness_blocking_regeneration_required": _source_freshness_blocking_regeneration_required(
            source_freshness
        ),
        "source_freshness_non_self_changed_records": commit_lag_summary.get(
            "records_with_non_self_changed_paths_since_source"
        ),
        "source_freshness_self_artifact_only_lag_records": commit_lag_summary.get(
            "records_with_self_artifact_only_lag"
        ),
    }


def _source_freshness_blocking_targets_summary(source_freshness: dict[str, Any]) -> dict[str, Any]:
    raw_targets = source_freshness.get("blocking_ordered_regeneration_targets")
    targets = raw_targets if isinstance(raw_targets, list) else []
    rows: list[dict[str, Any]] = []
    for item in targets:
        if not isinstance(item, dict):
            continue
        rows.append(
            {
                "artifact_id": item.get("artifact_id"),
                "path": item.get("path"),
                "freshness_state": item.get("freshness_state"),
                "source_head": item.get("source_head"),
                "required_before": item.get("required_before"),
                "commits_since_source": item.get("commits_since_source"),
                "blocking_changed_path_count_since_source": item.get(
                    "blocking_changed_path_count_since_source"
                ),
            }
        )
    blocking_target_ids = [str(row["artifact_id"]) for row in rows if row.get("artifact_id")]
    remote_readiness_ids = [
        target_id
        for target_id in blocking_target_ids
        if "readiness" in target_id or "gpu3070ti" in target_id
    ]
    return {
        "summary_id": "module2_source_freshness_blocking_targets_summary",
        "execution_boundary": "read_only_no_execution",
        "not_paper_result_material": True,
        "status": source_freshness.get("status"),
        "source_head": source_freshness.get("source_head"),
        "current_head": source_freshness.get("current_head"),
        "blocking_regeneration_required_before_remote_formal_execution": _source_freshness_blocking_regeneration_required(
            source_freshness
        ),
        "blocking_target_count": len(rows),
        "blocking_target_ids": blocking_target_ids,
        "remote_readiness_blocking_target_ids": remote_readiness_ids,
        "remote_readiness_blocking_target_count": len(remote_readiness_ids),
        "remote_readiness_refresh_requires_external_ssh": bool(remote_readiness_ids),
        "remote_readiness_refresh_allowed_now": False,
        "remote_preflight_allowed_now": False,
        "remote_training_allowed_now": False,
        "formal_claim_allowed_now": False,
        "rows": rows,
    }


def _source_freshness_ready_for_remote_preflight(source_freshness: dict[str, Any]) -> bool:
    return (
        source_freshness.get("status")
        in {
            "source_freshness_clean_current",
            "source_freshness_self_artifact_lag_only_gate_ready",
            "source_freshness_tracked_artifact_lag_only_gate_ready",
        }
        and _source_freshness_blocking_regeneration_required(source_freshness) is False
    )


def _source_freshness_blocking_regeneration_required(source_freshness: dict[str, Any]) -> bool:
    if "blocking_regeneration_required_before_remote_formal_execution" in source_freshness:
        return source_freshness.get("blocking_regeneration_required_before_remote_formal_execution") is True
    return source_freshness.get("regeneration_required_before_remote_formal_execution") is True


def _next_blocked_lane_id(status_report: dict[str, Any]) -> str | None:
    lane = status_report.get("next_blocked_lane")
    return lane.get("lane_id") if isinstance(lane, dict) else None


def _strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _safe_issue_id(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value).strip("_")


def _unique_strings(values: Any) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        text = str(value)
        if not text or text in seen:
            continue
        seen.add(text)
        out.append(text)
    return out


def _issue(issue_id: str, message: str) -> dict[str, str]:
    return {"issue_id": issue_id, "message": message}


def _unique_issues(issues: Sequence[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    out: list[dict[str, str]] = []
    for issue in issues:
        issue_id = issue.get("issue_id") or ""
        if not issue_id or issue_id in seen:
            continue
        seen.add(issue_id)
        out.append(issue)
    return out


def _read_json(path: Path) -> dict[str, Any]:
    if not Path(path).is_file():
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _source_head() -> str:
    return module2_source_head()


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 Formal Gate Remaining Deliverables",
        "",
        "This ledger is read-only. It lists remaining formal training, evaluation, and acceptance deliverables; it does not execute commands or write paper results.",
        "",
        f"- status: `{manifest['status']}`",
        f"- source_head: `{manifest['source_head']}`",
        f"- missing_deliverable_count: `{manifest['missing_deliverable_count']}`",
        f"- open_category_count: `{manifest['open_category_count']}`",
        f"- missing_counts_by_formal_category: `{manifest['missing_counts_by_formal_category']}`",
        f"- next_blocked_lane: `{manifest['next_blocked_lane']}`",
        f"- h01_status: `{manifest['h01_status']}`",
        f"- h02_status: `{manifest['h02_status']}`",
        f"- h02_formal_output_accepted: `{manifest['h02_formal_output_accepted']}`",
        f"- h02_paper_result_input_allowed: `{manifest['h02_paper_result_input_allowed']}`",
        f"- proof_command_count: `{manifest['proof_command_plan']['total_proof_command_count']}`",
        f"- production_plan_row_count: `{manifest['deliverable_production_plan']['row_count']}`",
        f"- audit_issue_count: `{manifest['audit_issue_count']}`",
        f"- local_training_allowed_now: `{manifest['local_training_allowed_now']}`",
        f"- remote_preflight_allowed_now: `{manifest['remote_preflight_allowed_now']}`",
        f"- remote_training_allowed_now: `{manifest['remote_training_allowed_now']}`",
        f"- formal_h01_evaluation_allowed_now: `{manifest['formal_h01_evaluation_allowed_now']}`",
        f"- formal_h02_acceptance_allowed_now: `{manifest['formal_h02_acceptance_allowed_now']}`",
        f"- formal_claim_allowed_now: `{manifest['formal_claim_allowed_now']}`",
        f"- paper_result_material_allowed_now: `{manifest['paper_result_material_allowed_now']}`",
        "",
        "## Human-Readable Gate Closure Checklist",
        "",
    ]
    checklist = manifest["plain_formal_gate_closure_checklist"]
    lines.append(f"- next_blocked_lane: `{checklist['next_blocked_lane']}`")
    lines.append(f"- total_missing_deliverables: `{checklist['total_missing_deliverables']}`")
    lines.append(f"- open_category_count: `{checklist['open_category_count']}`")
    lines.append(f"- local_training_allowed_now: `{checklist['local_training_allowed_now']}`")
    lines.append(f"- remote_training_allowed_now: `{checklist['remote_training_allowed_now']}`")
    lines.append(f"- formal_claim_allowed_now: `{checklist['formal_claim_allowed_now']}`")
    for category in checklist["categories"]:
        blocked_by = ", ".join(category["responsible_stage_blocked_by"]) if category["responsible_stage_blocked_by"] else "none"
        missing_ids = ", ".join(category["missing_matrix_ids"]) if category["missing_matrix_ids"] else "none"
        proof_ids = ", ".join(category["proof_command_ids"]) if category["proof_command_ids"] else "none"
        lines.append(
            f"- `{category['category']}`: missing=`{category['missing_count']}`, "
            f"stage=`{category['responsible_stage_id']}`, stage_allowed_now=`{category['responsible_stage_allowed_now']}`, "
            f"missing_artifacts=`{missing_ids}`, proof_commands=`{proof_ids}`, blocked_by=`{blocked_by}`"
        )
    lines.extend(
        [
            "",
        "## Current Gate Summary",
        "",
        ]
    )
    for key, value in manifest["current_gate_summary"].items():
        lines.append(f"- {key}: `{value}`")
    gap_summary = manifest["deliverable_gap_summary"]
    lines.extend(["", "## Formal Gate Gap Summary", ""])
    lines.append(f"- summary_id: `{gap_summary['summary_id']}`")
    lines.append(f"- total_missing_deliverables: `{gap_summary['total_missing_deliverables']}`")
    lines.append(f"- open_category_count: `{gap_summary['open_category_count']}`")
    lines.append(f"- execution_boundary: `{gap_summary['execution_boundary']}`")
    for category in gap_summary["categories"]:
        lines.append(f"### gap:{category['category']}")
        lines.append(f"- missing_count: `{category['missing_count']}`")
        lines.append(f"- responsible_stage_id: `{category['responsible_stage_id']}`")
        lines.append(f"- responsible_stage_allowed_now: `{category['responsible_stage_allowed_now']}`")
        blocked_by = ", ".join(category["responsible_stage_blocked_by"]) if category["responsible_stage_blocked_by"] else "none"
        lines.append(f"- responsible_stage_blocked_by: `{blocked_by}`")
        lines.append("- missing_artifacts:")
        if category["missing_artifacts"]:
            for item in category["missing_artifacts"]:
                lines.append(
                    f"  - `{item['matrix_id']}`: state=`{item['current_state']}`, "
                    f"path=`{item['expected_path']}`, acceptance_predicate_count=`{item['acceptance_predicate_count']}`, "
                    f"proof_command_count=`{item['proof_command_count']}`"
                )
        else:
            lines.append("  - none")
    proof_plan = manifest["proof_command_plan"]
    lines.extend(["", "## Proof Command Plan", ""])
    lines.append(f"- plan_id: `{proof_plan['plan_id']}`")
    lines.append(f"- execution_boundary: `{proof_plan['execution_boundary']}`")
    lines.append(f"- total_matrix_rows: `{proof_plan['total_matrix_rows']}`")
    lines.append(f"- total_proof_command_count: `{proof_plan['total_proof_command_count']}`")
    for row in proof_plan["rows"]:
        command_ids = ", ".join(row["proof_command_ids"]) if row["proof_command_ids"] else "none"
        lines.append(f"- `{row['matrix_id']}`: proof_command_count=`{row['proof_command_count']}`, command_ids=`{command_ids}`")
    production_plan = manifest["deliverable_production_plan"]
    lines.extend(["", "## Deliverable Production Plan", ""])
    lines.append(f"- plan_id: `{production_plan['plan_id']}`")
    lines.append(f"- source_plan: `{production_plan['source_plan']}`")
    lines.append(f"- post_plan_status: `{production_plan['post_plan_status']}`")
    lines.append(f"- execution_boundary: `{production_plan['execution_boundary']}`")
    lines.append(f"- row_count: `{production_plan['row_count']}`")
    lines.append(f"- rows_missing_production_stage: `{production_plan['rows_missing_production_stage']}`")
    lines.append(f"- rows_missing_materialization_stage: `{production_plan['rows_missing_materialization_stage']}`")
    lines.append(f"- rows_allowed_while_missing: `{production_plan['rows_allowed_while_missing']}`")
    for row in production_plan["rows"]:
        generation_stage = row["remote_generation_stage"]
        materialization_stage = row["local_materialization_stage"]
        lines.append(
            f"- `{row['matrix_id']}`: generation_stage=`{row['remote_generation_stage_id']}`, "
            f"generation_allowed_now=`{generation_stage.get('allowed_now')}`, "
            f"materialization_stage=`{row['local_materialization_stage_id']}`, "
            f"materialization_allowed_now=`{materialization_stage.get('allowed_now')}`, "
            f"host=`{generation_stage.get('host') or materialization_stage.get('host')}`, "
            f"generation_evidence_path_listed=`{row['expected_path_listed_in_remote_generation_stage']}`, "
            f"materialization_evidence_path_listed=`{row['expected_path_listed_in_local_materialization_stage']}`"
        )
    unlock_chain = manifest["deliverable_unlock_chain"]
    lines.extend(["", "## Deliverable Unlock Chain", ""])
    lines.append(f"- chain_id: `{unlock_chain['chain_id']}`")
    lines.append(f"- status: `{unlock_chain['status']}`")
    lines.append(f"- row_count: `{unlock_chain['row_count']}`")
    lines.append(f"- blocked_row_count: `{unlock_chain['blocked_row_count']}`")
    lines.append(
        f"- rows_with_missing_required_blockers: `{unlock_chain['rows_with_missing_required_blockers']}`"
    )
    lines.append(f"- rows_allowed_while_missing: `{unlock_chain['rows_allowed_while_missing']}`")
    for row in unlock_chain["rows"]:
        required_blockers = ", ".join(row["required_current_blockers"]) if row["required_current_blockers"] else "none"
        missing_blockers = (
            ", ".join(row["missing_required_current_blockers"])
            if row["missing_required_current_blockers"]
            else "none"
        )
        unlock_sequence = (
            " -> ".join(row["unlock_sequence_before_stage_allowed"])
            if row["unlock_sequence_before_stage_allowed"]
            else "none"
        )
        lines.append(
            f"- `{row['matrix_id']}`: missing=`{row['missing']}`, "
            f"stage_allowed_now=`{row['responsible_stage_allowed_now']}`, "
            f"required_current_blockers=`{required_blockers}`, "
            f"missing_required_current_blockers=`{missing_blockers}`, "
            f"unlock_sequence=`{unlock_sequence}`"
        )
    lines.extend(["", "## Deliverable Groups", ""])
    for group in manifest["deliverable_groups"]:
        lines.append(f"### {group['category']}")
        lines.append(f"- status: `{group['status']}`")
        lines.append(f"- missing_count: `{group['missing_count']}`")
        lines.append(f"- responsible_stage_id: `{group['responsible_stage_id']}`")
        lines.append(f"- responsible_stage_allowed_now: `{group['responsible_stage_allowed_now']}`")
        blocked_by = ", ".join(group["responsible_stage_blocked_by"]) if group["responsible_stage_blocked_by"] else "none"
        lines.append(f"- responsible_stage_blocked_by: `{blocked_by}`")
        lines.append("- items:")
        for item in group["items"]:
            lines.append(
                f"  - `{item['artifact_id']}`: missing=`{item['missing']}`, exists=`{item['exists']}`, "
                f"state=`{item['state']}`, path=`{item['path']}`"
            )
        if group["acceptable_evidence"]:
            lines.append("- acceptable_evidence:")
            lines.extend(f"  - {item}" for item in group["acceptable_evidence"])
        if group["invalid_substitutes"]:
            lines.append("- invalid_substitutes:")
            lines.extend(f"  - {item}" for item in group["invalid_substitutes"])
    lines.extend(["", "## Deliverable Acceptance Matrix", ""])
    for row in manifest["deliverable_acceptance_matrix"]:
        lines.append(f"### {row['matrix_id']}")
        lines.append(f"- expected_path: `{row['expected_path']}`")
        lines.append(f"- missing: `{row['missing']}`")
        lines.append(f"- current_state: `{row['current_state']}`")
        lines.append(f"- responsible_stage_id: `{row['responsible_stage_id']}`")
        lines.append(f"- responsible_stage_allowed_now: `{row['responsible_stage_allowed_now']}`")
        blocked_by = ", ".join(row["responsible_stage_blocked_by"]) if row["responsible_stage_blocked_by"] else "none"
        lines.append(f"- responsible_stage_blocked_by: `{blocked_by}`")
        lines.append("- acceptance_predicates:")
        lines.extend(f"  - {item}" for item in row["acceptance_predicates"])
        lines.append("- proof_commands:")
        for command in row["proof_commands"]:
            lines.append(f"  - `{command['command_id']}`: {command['command']}")
            lines.append(f"    - expected_evidence: `{command['expected_evidence']}`")
        lines.append("- invalid_substitutes:")
        lines.extend(f"  - {item}" for item in row["invalid_substitutes"])
    lines.extend(["", "## Audit Issues", ""])
    if manifest["audit_issues"]:
        for issue in manifest["audit_issues"]:
            lines.append(f"- `{issue['issue_id']}`: {issue['message']}")
    else:
        lines.append("- none")
    lines.extend(["", "## Claim Boundaries", ""])
    lines.extend(f"- {item}" for item in manifest["claim_boundaries"])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
