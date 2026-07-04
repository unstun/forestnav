from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_formal_gate_remaining_deliverables")
DEFAULT_STATUS_REPORT = Path("0_trials/module2_formal_gate_status_report/formal_gate_status_report.json")
DEFAULT_MISSING_ARTIFACTS = Path("0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json")
DEFAULT_CLOSURE_CHECKLIST = Path("0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json")
DEFAULT_REMOTE_PACKET = Path("0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json")
DEFAULT_H01_MANIFEST = Path("0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json")
DEFAULT_H02_ACCEPTANCE = Path("0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json")

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
    category_counts = _category_counts(deliverable_groups)
    permissions_now = _permissions(status_report=status_report, remote_packet=remote_packet)
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
    }
    audit_issues = _audit_issues(
        status_report=status_report,
        missing_artifacts=missing_artifacts,
        closure_checklist=closure_checklist,
        remote_packet=remote_packet,
        h01_manifest=h01_manifest,
        h02_acceptance=h02_acceptance,
        deliverable_groups=deliverable_groups,
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
        "inputs": {
            "formal_gate_status_report": str(config.status_report_path),
            "formal_gate_missing_artifacts": str(config.missing_artifacts_path),
            "formal_gate_closure_checklist": str(config.closure_checklist_path),
            "remote_formal_execution_packet": str(config.remote_packet_path),
            "h01_manifest": str(config.h01_manifest_path),
            "h02_formal_acceptance": str(config.h02_acceptance_path),
        },
        "current_gate_summary": current_gate_summary,
        "permissions_now": permissions_now,
        "category_counts": category_counts,
        "deliverable_gap_summary": deliverable_gap_summary,
        "proof_command_plan": proof_command_plan,
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
    common = [
        _proof_command(
            command_id=f"{artifact_id}_exists_nonempty",
            purpose="verify the expected formal artifact exists locally after pullback",
            command=_python_exists_nonempty_command(expected_path),
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


def _python_sha256_match_command(path: str) -> str:
    model_path = str(Path(path).with_name("final_model.zip"))
    return (
        "python -c "
        f"\"from pathlib import Path; import hashlib; record=Path({path!r}); model=Path({model_path!r}); "
        "digest=hashlib.sha256(model.read_bytes()).hexdigest(); assert digest in record.read_text(encoding='utf-8')\""
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


def _permissions(*, status_report: dict[str, Any], remote_packet: dict[str, Any]) -> dict[str, Any]:
    permissions = status_report.get("permissions_now") if isinstance(status_report.get("permissions_now"), dict) else {}
    return {
        "local_training_allowed_now": False,
        "remote_preflight_allowed_now": permissions.get("remote_preflight_allowed_now"),
        "remote_training_allowed_now": permissions.get("remote_training_allowed_now"),
        "formal_h01_evaluation_allowed_now": permissions.get("formal_h01_evaluation_allowed_now"),
        "formal_h02_acceptance_allowed_now": permissions.get("formal_h02_acceptance_allowed_now"),
        "formal_claim_allowed_now": permissions.get("formal_claim_allowed_now"),
        "remote_packet_ready_to_run_remote_training": remote_packet.get("ready_to_run_remote_training"),
    }


def _audit_issues(
    *,
    status_report: dict[str, Any],
    missing_artifacts: dict[str, Any],
    closure_checklist: dict[str, Any],
    remote_packet: dict[str, Any],
    h01_manifest: dict[str, Any],
    h02_acceptance: dict[str, Any],
    deliverable_groups: Sequence[dict[str, Any]],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for name, payload in (
        ("status_report", status_report),
        ("missing_artifacts", missing_artifacts),
        ("closure_checklist", closure_checklist),
        ("remote_packet", remote_packet),
        ("h01_manifest", h01_manifest),
        ("h02_acceptance", h02_acceptance),
    ):
        issues.extend(_read_only_payload_issues(name, payload))
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
    return _unique_issues(issues)


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


def _next_blocked_lane_id(status_report: dict[str, Any]) -> str | None:
    lane = status_report.get("next_blocked_lane")
    return lane.get("lane_id") if isinstance(lane, dict) else None


def _strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


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
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:
        return "unknown"


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
        f"- audit_issue_count: `{manifest['audit_issue_count']}`",
        f"- local_training_allowed_now: `{manifest['permissions_now']['local_training_allowed_now']}`",
        f"- remote_training_allowed_now: `{manifest['permissions_now']['remote_training_allowed_now']}`",
        f"- formal_claim_allowed_now: `{manifest['permissions_now']['formal_claim_allowed_now']}`",
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
        lines.append(
            f"- `{category['category']}`: missing=`{category['missing_count']}`, "
            f"stage=`{category['responsible_stage_id']}`, stage_allowed_now=`{category['responsible_stage_allowed_now']}`, "
            f"missing_artifacts=`{missing_ids}`, blocked_by=`{blocked_by}`"
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
                    f"path=`{item['expected_path']}`, acceptance_predicate_count=`{item['acceptance_predicate_count']}`"
                )
        else:
            lines.append("  - none")
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
