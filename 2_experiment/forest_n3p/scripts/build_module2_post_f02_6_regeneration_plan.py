from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_post_f02_6_regeneration_plan")
DEFAULT_DECISION_RECORD = Path("0_trials/module2_f02_6_decision_record/f02_6_decision_record.json")
DEFAULT_FORMAL_GATE = Path("0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json")
DEFAULT_STATUS_REPORT = Path("0_trials/module2_formal_gate_status_report/formal_gate_status_report.json")
DEFAULT_SOURCE_FRESHNESS = Path("0_trials/module2_source_freshness_audit/source_freshness_audit.json")
DEFAULT_REMOTE_PACKET = Path("0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json")
DEFAULT_REMAINING_DELIVERABLES = Path(
    "0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json"
)


@dataclass(frozen=True)
class PostF026RegenerationPlanConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    decision_record_path: Path = DEFAULT_DECISION_RECORD
    formal_gate_path: Path = DEFAULT_FORMAL_GATE
    status_report_path: Path = DEFAULT_STATUS_REPORT
    source_freshness_path: Path = DEFAULT_SOURCE_FRESHNESS
    remote_packet_path: Path = DEFAULT_REMOTE_PACKET
    remaining_deliverables_path: Path = DEFAULT_REMAINING_DELIVERABLES


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = PostF026RegenerationPlanConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        decision_record_path=args.decision_record,
        formal_gate_path=args.formal_gate,
        status_report_path=args.status_report,
        source_freshness_path=args.source_freshness_audit,
        remote_packet_path=args.remote_packet,
        remaining_deliverables_path=args.remaining_deliverables,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "post_f02_6_regeneration_plan.json"
    markdown_out = config.markdown_out or output_dir / "post_f02_6_regeneration_plan.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: PostF026RegenerationPlanConfig) -> dict[str, Any]:
    decision = _read_json(config.decision_record_path)
    formal_gate = _read_json(config.formal_gate_path)
    status_report = _read_json(config.status_report_path)
    source_freshness = _read_json(config.source_freshness_path)
    remote_packet = _read_json(config.remote_packet_path)
    remaining_deliverables = _read_json(config.remaining_deliverables_path)

    decision_status = str(decision.get("status") or formal_gate.get("current_gate_state", {}).get("f02_6_decision_status") or "unknown")
    source_targets = _source_targets(source_freshness)
    stages = _ordered_stages(
        decision=decision,
        decision_status=decision_status,
        formal_gate=formal_gate,
        source_targets=source_targets,
        remote_packet=remote_packet,
    )
    return {
        "schema_version": 1,
        "artifact_name": "module2_post_f02_6_regeneration_plan",
        "status": _status(decision_status=decision_status, stages=stages, source_freshness=source_freshness),
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "inputs": {
            "decision_record": str(config.decision_record_path),
            "formal_gate_gap_audit": str(config.formal_gate_path),
            "formal_gate_status_report": str(config.status_report_path),
            "source_freshness_audit": str(config.source_freshness_path),
            "remote_formal_execution_packet": str(config.remote_packet_path),
            "formal_gate_remaining_deliverables": str(config.remaining_deliverables_path),
        },
        "current_gate_summary": {
            "f02_6_decision_status": decision_status,
            "formal_gate_status": formal_gate.get("status"),
            "source_freshness_status": source_freshness.get("status"),
            "source_freshness_regeneration_required": bool(source_freshness.get("regeneration_required_before_remote_formal_execution")),
            "remote_packet_status": remote_packet.get("status"),
            "ready_to_run_remote_training": bool(remote_packet.get("ready_to_run_remote_training")),
        },
        "f02_6_human_decision_request_summary": _f02_6_human_decision_request_summary(status_report),
        "remaining_deliverables_gap_summary": _remaining_deliverables_gap_summary(remaining_deliverables),
        "source_regeneration_targets_by_gate": _targets_by_gate(source_targets),
        "source_regeneration_command_index": _source_regeneration_command_index(source_targets),
        "ordered_stages": stages,
        "blocking_summary": _blocking_summary(stages),
        "claim_boundaries": [
            "This artifact is an ordered plan, not an executor, result table, or paper appendix.",
            "It must not be used to bypass Dr Sun's F02.6 decision record.",
            "It does not run local training, remote preflight, remote training, or remote audit.",
            "The only training stage in the plan is remote-only on gpu3070ti-relay after all upstream gates pass.",
            "Source freshness risks are regeneration requirements, not formal algorithm failures.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the post-F02.6 Module2 regeneration and formal execution plan.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--decision-record", type=Path, default=DEFAULT_DECISION_RECORD)
    parser.add_argument("--formal-gate", type=Path, default=DEFAULT_FORMAL_GATE)
    parser.add_argument("--status-report", type=Path, default=DEFAULT_STATUS_REPORT)
    parser.add_argument("--source-freshness-audit", type=Path, default=DEFAULT_SOURCE_FRESHNESS)
    parser.add_argument("--remote-packet", type=Path, default=DEFAULT_REMOTE_PACKET)
    parser.add_argument("--remaining-deliverables", type=Path, default=DEFAULT_REMAINING_DELIVERABLES)
    return parser.parse_args(list(argv) if argv is not None else None)


def _ordered_stages(
    *,
    decision: dict[str, Any],
    decision_status: str,
    formal_gate: dict[str, Any],
    source_targets: Sequence[dict[str, Any]],
    remote_packet: dict[str, Any],
) -> list[dict[str, Any]]:
    approved = decision_status == "approved"
    preflight_targets = _targets_required_before(source_targets, "approved_remote_preflight")
    h01_h02_targets = _targets_required_before(source_targets, "formal_h01_h02")
    claim_targets = _targets_required_before(source_targets, "formal_claim_gate")
    preflight_command = _approved_action(decision, "preflight_command")
    packet_steps = remote_packet.get("execution_steps") if isinstance(remote_packet.get("execution_steps"), dict) else {}
    preflight_blockers = _preflight_blockers(approved=approved, preflight_targets=preflight_targets)
    remote_packet_blockers = [] if remote_packet.get("ready_to_run_remote_training") is True else ["remote_packet_not_ready"]
    remote_execution_blockers = _unique(preflight_blockers + remote_packet_blockers)
    stages = [
        _stage(
            "f02_6_decision_record",
            "decision",
            "Record Dr Sun's F02.6 approve/reject decision without running training.",
            allowed_now=decision_status == "pending_human_decision",
            blocked_by=[] if decision_status == "pending_human_decision" else [f"current_decision_status_{decision_status}"],
            evidence_paths=["0_trials/module2_f02_6_decision_record/f02_6_decision_record.json"],
            command_templates=[
                "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_decision_record --decision approve_obstacle_summary_warm_start --decider 'Dr Sun' --decision-note '<Dr Sun approval note>'"
            ],
            requires_human_input=True,
        ),
        _stage(
            "regenerate_preflight_gate_artifacts",
            "regeneration",
            "Regenerate source-stale artifacts required before approved remote preflight.",
            allowed_now=approved,
            blocked_by=[] if approved else ["f02_6_decision_not_approved"],
            evidence_paths=[str(item.get("path")) for item in preflight_targets],
            command_templates=_regeneration_commands(preflight_targets),
        ),
        _stage(
            "approved_remote_preflight",
            "remote_preflight",
            "Run approved gpu3070ti preflight after decision and source-fresh regeneration.",
            allowed_now=approved and not preflight_targets,
            blocked_by=preflight_blockers,
            runs_remote_preflight=True,
            host="gpu3070ti-relay",
            evidence_paths=[
                "0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_approved_remote_v1/gate3_preflight_manifest.json"
            ],
            command_templates=[_with_pythonpath(preflight_command)] if preflight_command else [],
        ),
        _stage(
            "regenerate_remote_execution_packet",
            "regeneration",
            "Regenerate remote formal execution packet from the approved preflight manifest.",
            allowed_now=approved and not preflight_targets,
            blocked_by=preflight_blockers,
            evidence_paths=["0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json"],
            command_templates=["PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_remote_formal_execution_packet"],
        ),
        _stage(
            "gate3_remote_training",
            "training",
            "Run the formal PPO Gate3 trial remotely only after the packet reports ready.",
            allowed_now=remote_packet.get("ready_to_run_remote_training") is True,
            blocked_by=remote_execution_blockers,
            runs_training=True,
            host=_remote_host(remote_packet),
            evidence_paths=_expected_pullback_artifacts(remote_packet),
            command_templates=[_packet_command(packet_steps, "run_remote_training")],
        ),
        _stage(
            "gate3_remote_audit_pullback",
            "acceptance",
            "Audit the remote trial and pull back all required artifacts with hashes.",
            allowed_now=remote_packet.get("ready_to_run_remote_training") is True,
            blocked_by=remote_execution_blockers,
            host=_remote_host(remote_packet),
            evidence_paths=_expected_pullback_artifacts(remote_packet),
            command_templates=[
                _packet_command(packet_steps, "run_remote_audit"),
                _pullback_command(remote_packet),
            ],
        ),
        _stage(
            "regenerate_h01_h02_formal_artifacts",
            "evaluation",
            "Regenerate H01/H02 with the audited checkpoint and formal-scale outputs.",
            allowed_now=False,
            blocked_by=["missing_remote_audit_pullback"] + (["source_fresh_h01_h02_targets_open"] if h01_h02_targets else []),
            evidence_paths=[str(item.get("path")) for item in h01_h02_targets]
            + ["0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json"],
            command_templates=_unique(
                [
                "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_evaluation_manifest --module2-rl-rs-checkpoint <pulled-back-final_model.zip>",
                "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_h02_formal_acceptance",
                ]
                + _regeneration_commands(h01_h02_targets)
            ),
        ),
        _stage(
            "regenerate_claim_gate_artifacts",
            "claim_gate",
            "Regenerate claim safety and paper readiness only after H02 formal acceptance.",
            allowed_now=False,
            blocked_by=["h02_formal_acceptance_not_ready"] + (["source_fresh_claim_targets_open"] if claim_targets else []),
            evidence_paths=[str(item.get("path")) for item in claim_targets],
            command_templates=_unique(
                [
                "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_claim_safety",
                "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_paper_readiness",
                ]
                + _regeneration_commands(claim_targets)
            ),
        ),
    ]
    formal_blockers = _formal_gate_blockers(formal_gate)
    for stage in stages:
        if stage["stage_id"] in {"approved_remote_preflight", "gate3_remote_training"}:
            stage["formal_gate_blockers_snapshot"] = formal_blockers
    return stages


def _stage(
    stage_id: str,
    phase: str,
    action: str,
    *,
    allowed_now: bool,
    blocked_by: Sequence[str],
    evidence_paths: Sequence[str],
    command_templates: Sequence[str],
    runs_training: bool = False,
    runs_remote_preflight: bool = False,
    host: str | None = None,
    requires_human_input: bool = False,
) -> dict[str, Any]:
    return {
        "stage_id": stage_id,
        "phase": phase,
        "status": "ready" if allowed_now else "blocked",
        "allowed_now": bool(allowed_now),
        "blocked_by": _unique([str(item) for item in blocked_by if item]),
        "runs_training": bool(runs_training),
        "runs_remote_preflight": bool(runs_remote_preflight),
        "host": host,
        "requires_human_input": bool(requires_human_input),
        "action": action,
        "evidence_paths": [str(item) for item in evidence_paths if item],
        "command_templates": [str(item) for item in command_templates if item],
    }


def _status(*, decision_status: str, stages: Sequence[dict[str, Any]], source_freshness: dict[str, Any]) -> str:
    if decision_status == "pending_human_decision":
        return "blocked_until_f02_6_decision"
    if decision_status != "approved":
        return f"blocked_by_f02_6_{decision_status}"
    if source_freshness.get("regeneration_required_before_remote_formal_execution") is True:
        return "ready_to_execute_post_f02_6_regeneration_plan"
    if any(stage["stage_id"] == "gate3_remote_training" and stage["allowed_now"] for stage in stages):
        return "ready_for_remote_training_packet_execution"
    return "blocked_formal_gate_preconditions"


def _source_targets(source_freshness: dict[str, Any]) -> list[dict[str, Any]]:
    targets = source_freshness.get("ordered_regeneration_targets")
    if not isinstance(targets, list):
        return []
    return [target for target in targets if isinstance(target, dict)]


def _targets_required_before(targets: Sequence[dict[str, Any]], gate: str) -> list[dict[str, Any]]:
    return [target for target in targets if str(target.get("required_before")) == gate]


def _targets_by_gate(targets: Sequence[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    for target in targets:
        key = str(target.get("required_before") or "unknown")
        out.setdefault(key, []).append(
            {
                "artifact_id": target.get("artifact_id"),
                "path": target.get("path"),
                "freshness_state": target.get("freshness_state"),
            }
        )
    return out


def _regeneration_commands(targets: Sequence[dict[str, Any]]) -> list[str]:
    return _unique([entry["command_template"] for entry in _source_regeneration_command_index(targets)])


def _source_regeneration_command_index(targets: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for target in targets:
        entries.append(_regeneration_command_entry(target))
    return entries


def _regeneration_command_entry(target: dict[str, Any]) -> dict[str, Any]:
    artifact_id = str(target.get("artifact_id"))
    command_template: str
    command_kind = "known_builder"
    if artifact_id == "f02_6_decision_record":
        command_kind = "human_decision_record"
        command_template = (
            "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_decision_record "
            "--decision approve_obstacle_summary_warm_start --decider 'Dr Sun' --decision-note '<Dr Sun approval note>'"
        )
    elif artifact_id == "f02_6_warm_start_decision_packet":
        command_template = "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_warm_start_decision_packet"
    elif artifact_id == "f02_6_decision_intake":
        command_template = "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_decision_intake"
    elif artifact_id == "f02_6_decision_gate_audit":
        command_template = "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_decision_gate_audit"
    elif artifact_id == "f02_6_transition_gate_audit":
        command_template = "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_transition_gate_audit"
    elif artifact_id == "formal_gate_gap_audit":
        command_template = "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_gap_audit"
    elif artifact_id == "remote_formal_execution_packet":
        command_template = "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_remote_formal_execution_packet"
    elif artifact_id == "remote_packet_safety_audit":
        command_template = "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_remote_packet_safety_audit"
    elif artifact_id == "formal_gate_closure_checklist":
        command_template = "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_closure_checklist"
    elif artifact_id == "post_f02_6_plan_audit":
        command_template = "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_plan_audit"
    elif artifact_id == "post_f02_6_regeneration_plan":
        command_template = "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_post_f02_6_regeneration_plan"
    elif artifact_id == "formal_gate_missing_artifacts":
        command_template = "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_missing_artifacts_audit"
    elif artifact_id == "formal_gate_handoff_bundle":
        command_template = "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_handoff_bundle"
    elif artifact_id == "formal_gate_status_report":
        command_template = "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_status_report"
    elif artifact_id == "formal_gate_remaining_deliverables":
        command_template = "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_remaining_deliverables"
    elif artifact_id == "formal_gate_proof_audit":
        command_template = "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_proof_audit"
    elif artifact_id == "formal_gate_proof_summary_chain_audit":
        command_template = "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_formal_gate_proof_summary_chain_audit"
    elif artifact_id == "h01_evaluation_manifest":
        command_template = (
            "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_evaluation_manifest "
            "--module2-rl-rs-checkpoint <pulled-back-final_model.zip>"
        )
    elif artifact_id == "h02_formal_acceptance":
        command_template = "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_h02_formal_acceptance"
    elif artifact_id == "claim_safety":
        command_template = "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_claim_safety"
    elif artifact_id == "paper_readiness":
        command_template = "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_paper_readiness"
    elif artifact_id == "gpu3070ti_readiness_refresh":
        command_kind = "manual_read_only"
        command_template = "manual read-only gpu3070ti readiness refresh; no local training, no approved preflight"
    else:
        command_kind = "unknown_manual"
        command_template = f"manual regeneration required for {artifact_id}: {target.get('path')}"
    return {
        "artifact_id": artifact_id,
        "required_before": target.get("required_before"),
        "freshness_state": target.get("freshness_state"),
        "path": target.get("path"),
        "stage_id": _regeneration_stage_for_target(target),
        "command_kind": command_kind,
        "command_template": command_template,
    }


def _regeneration_stage_for_target(target: dict[str, Any]) -> str:
    required_before = str(target.get("required_before") or "")
    if required_before == "approved_remote_preflight":
        return "regenerate_preflight_gate_artifacts"
    if required_before == "formal_h01_h02":
        return "regenerate_h01_h02_formal_artifacts"
    if required_before == "formal_claim_gate":
        return "regenerate_claim_gate_artifacts"
    return "manual_review"


def _preflight_blockers(*, approved: bool, preflight_targets: Sequence[dict[str, Any]]) -> list[str]:
    blockers: list[str] = []
    if not approved:
        blockers.append("f02_6_decision_not_approved")
    if preflight_targets:
        blockers.append("source_fresh_preflight_targets_open")
    return blockers


def _formal_gate_blockers(formal_gate: dict[str, Any]) -> list[str]:
    steps = formal_gate.get("ordered_next_steps") if isinstance(formal_gate.get("ordered_next_steps"), list) else []
    blockers: list[str] = []
    for step in steps:
        if not isinstance(step, dict) or step.get("step_id") not in {"remote_preflight", "gate3_remote_training"}:
            continue
        blockers.extend(str(item) for item in step.get("blocked_by", ()) if item)
    return _unique(blockers)


def _approved_action(decision: dict[str, Any], key: str) -> str:
    actions = decision.get("conditional_actions") if isinstance(decision.get("conditional_actions"), dict) else {}
    approved = actions.get("if_approved_obstacle_summary") if isinstance(actions.get("if_approved_obstacle_summary"), dict) else {}
    return str(approved.get(key) or "")


def _with_pythonpath(command: str) -> str:
    if not command:
        return ""
    if command.startswith("PYTHONPATH="):
        return command
    return f"PYTHONPATH=2_experiment {command}"


def _packet_command(packet_steps: dict[str, Any], key: str) -> str:
    item = packet_steps.get(key) if isinstance(packet_steps.get(key), dict) else {}
    return str(item.get("command") or "")


def _pullback_command(remote_packet: dict[str, Any]) -> str:
    pullback = remote_packet.get("post_run_pullback") if isinstance(remote_packet.get("post_run_pullback"), dict) else {}
    return str(pullback.get("pullback_command") or "")


def _expected_pullback_artifacts(remote_packet: dict[str, Any]) -> list[str]:
    pullback = remote_packet.get("post_run_pullback") if isinstance(remote_packet.get("post_run_pullback"), dict) else {}
    artifacts = pullback.get("expected_artifacts") if isinstance(pullback.get("expected_artifacts"), list) else []
    return [str(item) for item in artifacts if item]


def _remote_host(remote_packet: dict[str, Any]) -> str:
    env = remote_packet.get("execution_environment") if isinstance(remote_packet.get("execution_environment"), dict) else {}
    return str(env.get("gpu_alias") or env.get("training_host_required") or "gpu3070ti-relay")


def _blocking_summary(stages: Sequence[dict[str, Any]]) -> dict[str, Any]:
    return {
        "blocked_stage_ids": [stage["stage_id"] for stage in stages if not stage["allowed_now"]],
        "ready_stage_ids": [stage["stage_id"] for stage in stages if stage["allowed_now"]],
        "training_allowed_now": any(stage["runs_training"] and stage["allowed_now"] for stage in stages),
        "remote_preflight_allowed_now": any(stage["runs_remote_preflight"] and stage["allowed_now"] for stage in stages),
    }


def _remaining_deliverables_gap_summary(remaining_deliverables: dict[str, Any]) -> dict[str, Any]:
    raw = remaining_deliverables.get("deliverable_gap_summary")
    summary = raw if isinstance(raw, dict) else {}
    categories = _gap_categories(summary.get("categories"))
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


def _gap_categories(raw_categories: Any) -> dict[str, dict[str, Any]]:
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
        missing_artifacts = raw.get("missing_artifacts") if isinstance(raw.get("missing_artifacts"), list) else []
        out[str(category)] = {
            "present": True,
            "status": raw.get("status"),
            "missing_count": int(raw.get("missing_count") or 0),
            "present_count": int(raw.get("present_count") or 0),
            "responsible_stage_id": raw.get("responsible_stage_id"),
            "responsible_stage_allowed_now": raw.get("responsible_stage_allowed_now"),
            "responsible_stage_blocked_by": [str(item) for item in raw.get("responsible_stage_blocked_by", []) if item]
            if isinstance(raw.get("responsible_stage_blocked_by"), list)
            else [],
            "missing_artifact_matrix_ids": [
                str(item.get("matrix_id"))
                for item in missing_artifacts
                if isinstance(item, dict) and item.get("matrix_id")
            ],
        }
    return out


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 Post-F02.6 Regeneration Plan",
        "",
        "This file is an ordered plan. It does not execute commands, train, preflight, audit, or write paper results.",
        "",
        f"- status: `{manifest['status']}`",
        f"- executes_commands: `{manifest['executes_commands']}`",
        f"- runs_training: `{manifest['runs_training']}`",
        f"- runs_remote_preflight: `{manifest['runs_remote_preflight']}`",
        f"- local_training_allowed: `{manifest['local_training_allowed']}`",
        f"- formal_claim_allowed: `{manifest['formal_claim_allowed']}`",
        "",
        "## Current Gate Summary",
        "",
    ]
    for key, value in manifest["current_gate_summary"].items():
        lines.append(f"- {key}: `{value}`")
    gap = manifest["remaining_deliverables_gap_summary"]
    lines.extend(
        [
            "",
            "## Remaining Deliverables Gap Summary",
            "",
            f"- present: `{gap['present']}`",
            f"- total_missing_deliverables: `{gap['total_missing_deliverables']}`",
            f"- open_category_count: `{gap['open_category_count']}`",
        ]
    )
    for category in gap["category_order"]:
        item = gap["categories"].get(category, {})
        lines.append(
            f"- `{category}`: missing=`{item.get('missing_count')}`, "
            f"responsible_stage=`{item.get('responsible_stage_id')}`, "
            f"allowed_now=`{item.get('responsible_stage_allowed_now')}`"
        )
    lines.extend(["", "## Ordered Stages", ""])
    for stage in manifest["ordered_stages"]:
        host = f", host=`{stage['host']}`" if stage.get("host") else ""
        lines.append(
            f"- `{stage['stage_id']}` ({stage['phase']}): status=`{stage['status']}`, "
            f"allowed_now=`{stage['allowed_now']}`, runs_training=`{stage['runs_training']}`, "
            f"runs_remote_preflight=`{stage['runs_remote_preflight']}`{host}"
        )
        if stage["blocked_by"]:
            lines.append(f"  - blocked_by: `{', '.join(stage['blocked_by'])}`")
        if stage["evidence_paths"]:
            lines.append(f"  - evidence: `{'; '.join(stage['evidence_paths'])}`")
    lines.extend(["", "## Source Regeneration Command Index", ""])
    for entry in manifest["source_regeneration_command_index"]:
        lines.append(
            f"- `{entry['artifact_id']}` -> `{entry['stage_id']}` "
            f"kind=`{entry['command_kind']}`, required_before=`{entry['required_before']}`"
        )
        lines.append(f"  - command: `{entry['command_template']}`")
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


def _unique(items: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


if __name__ == "__main__":
    raise SystemExit(main())
