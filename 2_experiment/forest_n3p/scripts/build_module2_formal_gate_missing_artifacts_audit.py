from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_formal_gate_missing_artifacts")
DEFAULT_DECISION_RECORD = Path("0_trials/module2_f02_6_decision_record/f02_6_decision_record.json")
DEFAULT_DECISION_GATE_AUDIT = Path("0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.json")
DEFAULT_TRANSITION_GATE_AUDIT = Path("0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json")
DEFAULT_POST_PLAN = Path("0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json")
DEFAULT_SOURCE_FRESHNESS = Path("0_trials/module2_source_freshness_audit/source_freshness_audit.json")
DEFAULT_REMOTE_PACKET = Path("0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json")
DEFAULT_REMOTE_PACKET_AUDIT = Path("0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json")
DEFAULT_H01_MANIFEST = Path("0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json")
DEFAULT_H02_ACCEPTANCE = Path("0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json")
DEFAULT_PROTOCOL_LANE_STATUS_REPORT = Path(
    "0_trials/module2_formal_gate_protocol_lane_status_report/protocol_lane_status_report.json"
)

TRAINING_SUFFIXES = (
    "train/final_model.zip",
    "train/summary.json",
    "train/training_manifest.json",
)
GATE3_EVAL_SUFFIXES = (
    "eval/gate3_eval_episodes.csv",
    "eval/gate3_summary.json",
)
GATE3_ACCEPTANCE_SUFFIXES = (
    "gate3_trial_manifest.json",
    "gate3_formal_audit.json",
)


@dataclass(frozen=True)
class FormalGateMissingArtifactsAuditConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    decision_record_path: Path = DEFAULT_DECISION_RECORD
    decision_gate_audit_path: Path = DEFAULT_DECISION_GATE_AUDIT
    transition_gate_audit_path: Path = DEFAULT_TRANSITION_GATE_AUDIT
    post_plan_path: Path = DEFAULT_POST_PLAN
    source_freshness_path: Path = DEFAULT_SOURCE_FRESHNESS
    remote_packet_path: Path = DEFAULT_REMOTE_PACKET
    remote_packet_audit_path: Path = DEFAULT_REMOTE_PACKET_AUDIT
    h01_manifest_path: Path = DEFAULT_H01_MANIFEST
    h02_acceptance_path: Path = DEFAULT_H02_ACCEPTANCE
    protocol_lane_status_report_path: Path = DEFAULT_PROTOCOL_LANE_STATUS_REPORT


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = FormalGateMissingArtifactsAuditConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        decision_record_path=args.decision_record,
        decision_gate_audit_path=args.decision_gate_audit,
        transition_gate_audit_path=args.transition_gate_audit,
        post_plan_path=args.post_plan,
        source_freshness_path=args.source_freshness_audit,
        remote_packet_path=args.remote_packet,
        remote_packet_audit_path=args.remote_packet_audit,
        h01_manifest_path=args.h01_manifest,
        h02_acceptance_path=args.h02_acceptance,
        protocol_lane_status_report_path=args.protocol_lane_status_report,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "formal_gate_missing_artifacts.json"
    markdown_out = config.markdown_out or output_dir / "formal_gate_missing_artifacts.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: FormalGateMissingArtifactsAuditConfig) -> dict[str, Any]:
    decision = _read_json(config.decision_record_path)
    decision_gate = _read_json(config.decision_gate_audit_path)
    transition_gate = _read_json(config.transition_gate_audit_path)
    post_plan = _read_json(config.post_plan_path)
    source_freshness = _read_json(config.source_freshness_path)
    remote_packet = _read_json(config.remote_packet_path)
    remote_packet_audit = _read_json(config.remote_packet_audit_path)
    h01_manifest = _read_json(config.h01_manifest_path)
    h02_acceptance = _read_json(config.h02_acceptance_path)
    protocol_lane_status = _read_json(config.protocol_lane_status_report_path)

    groups = _missing_evidence_groups(
        decision=decision,
        transition_gate=transition_gate,
        post_plan=post_plan,
        source_freshness=source_freshness,
        remote_packet=remote_packet,
        h01_manifest=h01_manifest,
        h02_acceptance=h02_acceptance,
    )
    current_gate_summary = _current_gate_summary(
        decision=decision,
        decision_gate=decision_gate,
        transition_gate=transition_gate,
        post_plan=post_plan,
        source_freshness=source_freshness,
        remote_packet=remote_packet,
        remote_packet_audit=remote_packet_audit,
        h01_manifest=h01_manifest,
        h02_acceptance=h02_acceptance,
        protocol_lane_status=protocol_lane_status,
    )
    formal_requirements = _formal_gate_requirements(
        groups=groups,
        current_gate_summary=current_gate_summary,
        post_plan=post_plan,
    )
    inputs = {
        "decision_record": str(config.decision_record_path),
        "f02_6_decision_gate_audit": str(config.decision_gate_audit_path),
        "f02_6_transition_gate_audit": str(config.transition_gate_audit_path),
        "post_f02_6_regeneration_plan": str(config.post_plan_path),
        "source_freshness_audit": str(config.source_freshness_path),
        "remote_formal_execution_packet": str(config.remote_packet_path),
        "remote_packet_safety_audit": str(config.remote_packet_audit_path),
        "h01_manifest": str(config.h01_manifest_path),
        "h02_formal_acceptance": str(config.h02_acceptance_path),
        "protocol_lane_status_report": str(config.protocol_lane_status_report_path),
    }
    handoff_index = _formal_gate_handoff_index(
        current_gate_summary=current_gate_summary,
        formal_requirements=formal_requirements,
        inputs=inputs,
    )
    audit_issues = _audit_issues(
        decision=decision,
        decision_gate=decision_gate,
        transition_gate=transition_gate,
        post_plan=post_plan,
        source_freshness=source_freshness,
        remote_packet=remote_packet,
        remote_packet_audit=remote_packet_audit,
        h01_manifest=h01_manifest,
        h02_acceptance=h02_acceptance,
        groups=groups,
    )
    missing_counts = _missing_counts(groups)
    all_required_evidence_present = all(count == 0 for count in missing_counts.values())
    return {
        "schema_version": 1,
        "artifact_name": "module2_formal_gate_missing_artifacts_audit",
        "status": "formal_gate_artifacts_complete" if all_required_evidence_present and not audit_issues else "formal_gate_missing_artifacts_open",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "inputs": inputs,
        "current_gate_summary": current_gate_summary,
        "formal_gate_handoff_index": handoff_index,
        "missing_counts_by_category": missing_counts,
        "all_required_evidence_present": all_required_evidence_present,
        "missing_evidence_groups": groups,
        "formal_gate_requirements": formal_requirements,
        "formal_gate_requirement_counts": _requirement_counts(formal_requirements),
        "audit_issue_count": len(audit_issues),
        "audit_issues": audit_issues,
        "claim_boundaries": [
            "This audit lists missing formal-gate evidence; it does not run training, preflight, sync, audit, pullback, or evaluation.",
            "A complete file list is still not a paper claim unless Gate3 audit passes, hashes are recorded, H01 is ready, and H02 accepts formal outputs.",
            "F02.6 approval by Dr Sun is required before obstacle-summary warm-start formal training.",
            "PPO formal training remains gpu3070ti-relay-only; local training remains prohibited.",
            "This artifact is a gate inventory, not result-table or appendix material.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit missing Module2 formal-gate training/evaluation/acceptance artifacts without executing commands.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--decision-record", type=Path, default=DEFAULT_DECISION_RECORD)
    parser.add_argument("--decision-gate-audit", type=Path, default=DEFAULT_DECISION_GATE_AUDIT)
    parser.add_argument("--transition-gate-audit", type=Path, default=DEFAULT_TRANSITION_GATE_AUDIT)
    parser.add_argument("--post-plan", type=Path, default=DEFAULT_POST_PLAN)
    parser.add_argument("--source-freshness-audit", type=Path, default=DEFAULT_SOURCE_FRESHNESS)
    parser.add_argument("--remote-packet", type=Path, default=DEFAULT_REMOTE_PACKET)
    parser.add_argument("--remote-packet-audit", type=Path, default=DEFAULT_REMOTE_PACKET_AUDIT)
    parser.add_argument("--h01-manifest", type=Path, default=DEFAULT_H01_MANIFEST)
    parser.add_argument("--h02-acceptance", type=Path, default=DEFAULT_H02_ACCEPTANCE)
    parser.add_argument("--protocol-lane-status-report", type=Path, default=DEFAULT_PROTOCOL_LANE_STATUS_REPORT)
    return parser.parse_args(list(argv) if argv is not None else None)


def _missing_evidence_groups(
    *,
    decision: dict[str, Any],
    transition_gate: dict[str, Any],
    post_plan: dict[str, Any],
    source_freshness: dict[str, Any],
    remote_packet: dict[str, Any],
    h01_manifest: dict[str, Any],
    h02_acceptance: dict[str, Any],
) -> list[dict[str, Any]]:
    return [
        _decision_group(decision),
        _transition_gate_group(transition_gate),
        _source_regeneration_group(source_freshness),
        _post_plan_group(post_plan),
        _remote_artifact_group(
            group_id="remote_training_outputs",
            category="training",
            remote_packet=remote_packet,
            suffixes=TRAINING_SUFFIXES,
            required_before="gate3_remote_audit_pullback",
        ),
        _remote_artifact_group(
            group_id="gate3_evaluation_outputs",
            category="evaluation",
            remote_packet=remote_packet,
            suffixes=GATE3_EVAL_SUFFIXES,
            required_before="gate3_remote_audit_pullback",
        ),
        _remote_artifact_group(
            group_id="gate3_acceptance_pullback",
            category="acceptance",
            remote_packet=remote_packet,
            suffixes=GATE3_ACCEPTANCE_SUFFIXES,
            required_before="h01_h02_formal_regeneration",
            extra_items=_hash_items(remote_packet),
        ),
        _h01_h02_group(h01_manifest=h01_manifest, h02_acceptance=h02_acceptance),
        _claim_gate_group(source_freshness=source_freshness, h02_acceptance=h02_acceptance),
    ]


def _decision_group(decision: dict[str, Any]) -> dict[str, Any]:
    status = str(decision.get("status") or "missing")
    complete = status == "approved" and decision.get("decider") == "Dr Sun"
    return {
        "group_id": "f02_6_decision_record",
        "category": "decision",
        "required_before": "source_fresh_regeneration",
        "complete": complete,
        "blocked_by": [] if complete else ["f02_6_decision_not_approved"],
        "items": [
            {
                "artifact_id": "f02_6_decision_record",
                "path": "0_trials/module2_f02_6_decision_record/f02_6_decision_record.json",
                "exists": bool(decision),
                "state": status,
                "missing": not complete,
                "reason": "requires Dr Sun approval record before warm-start formal chain",
            }
        ],
    }


def _transition_gate_group(transition_gate: dict[str, Any]) -> dict[str, Any]:
    status = str(transition_gate.get("status") or "missing")
    issue_count = int(transition_gate.get("audit_issue_count") or 0)
    complete = bool(transition_gate) and status == "f02_6_transition_gate_audit_passed" and issue_count == 0
    blocked_by = [] if complete else ["f02_6_transition_gate_audit_not_passed"]
    if issue_count > 0:
        blocked_by.append("f02_6_transition_gate_audit_issues_open")
    return {
        "group_id": "f02_6_transition_gate_audit",
        "category": "decision_gate",
        "required_before": "source_fresh_regeneration",
        "complete": complete,
        "blocked_by": blocked_by,
        "items": [
            {
                "artifact_id": "f02_6_transition_gate_audit",
                "path": "0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json",
                "exists": bool(transition_gate),
                "state": status,
                "missing": not complete,
                "reason": "transition audit must pass before the missing-artifacts inventory can represent the formal gate chain",
            }
        ],
    }


def _source_regeneration_group(source_freshness: dict[str, Any]) -> dict[str, Any]:
    targets = _source_targets(source_freshness)
    required = _source_freshness_blocking_regeneration_required(source_freshness)
    items = []
    for target in targets:
        items.append(
            {
                "artifact_id": target.get("artifact_id"),
                "path": target.get("path"),
                "exists": Path(str(target.get("path") or "")).is_file(),
                "state": target.get("freshness_state"),
                "missing": required,
                "required_before": target.get("required_before"),
                "reason": "source freshness audit requires regeneration before the corresponding formal gate",
            }
        )
    return {
        "group_id": "source_fresh_regeneration_targets",
        "category": "regeneration",
        "required_before": "approved_remote_preflight",
        "complete": not required,
        "blocked_by": ["source_freshness_regeneration_required"] if required else [],
        "items": items,
    }


def _post_plan_group(post_plan: dict[str, Any]) -> dict[str, Any]:
    stages = post_plan.get("ordered_stages") if isinstance(post_plan.get("ordered_stages"), list) else []
    blocked = [str(stage.get("stage_id")) for stage in stages if isinstance(stage, dict) and stage.get("status") == "blocked"]
    return {
        "group_id": "post_f02_6_ordered_stages",
        "category": "gate_sequence",
        "required_before": "remote_training",
        "complete": not blocked,
        "blocked_by": blocked,
        "items": [
            {
                "artifact_id": str(stage.get("stage_id")),
                "path": "; ".join(str(item) for item in stage.get("evidence_paths", ()) if item),
                "exists": True,
                "state": stage.get("status"),
                "missing": stage.get("status") == "blocked",
                "reason": ", ".join(str(item) for item in stage.get("blocked_by", ()) if item),
            }
            for stage in stages
            if isinstance(stage, dict)
        ],
    }


def _remote_artifact_group(
    *,
    group_id: str,
    category: str,
    remote_packet: dict[str, Any],
    suffixes: Sequence[str],
    required_before: str,
    extra_items: Sequence[dict[str, Any]] = (),
) -> dict[str, Any]:
    artifacts = _expected_artifacts(remote_packet)
    items = []
    for suffix in suffixes:
        path = _artifact_for_suffix(artifacts, suffix)
        exists = bool(path) and Path(path).is_file()
        items.append(
            {
                "artifact_id": _slug(suffix),
                "path": path,
                "exists": exists,
                "state": "present" if exists else "missing",
                "missing": not exists,
                "reason": f"required formal Gate3 {category} artifact",
            }
        )
    items.extend(extra_items)
    missing = [item for item in items if item.get("missing")]
    return {
        "group_id": group_id,
        "category": category,
        "required_before": required_before,
        "complete": not missing,
        "blocked_by": [str(item.get("artifact_id")) for item in missing],
        "items": items,
    }


def _hash_items(remote_packet: dict[str, Any]) -> list[dict[str, Any]]:
    pullback = remote_packet.get("post_run_pullback") if isinstance(remote_packet.get("post_run_pullback"), dict) else {}
    required = pullback.get("hash_manifest_required") is True
    artifact_paths = _expected_artifacts(remote_packet)
    final_model = _artifact_for_suffix(artifact_paths, "train/final_model.zip")
    candidate_paths = [f"{final_model}.sha256", f"{final_model}.sha256.json"] if final_model else []
    exists = any(Path(path).is_file() for path in candidate_paths)
    return [
        {
            "artifact_id": "pulled_back_checkpoint_hash_record",
            "path": " or ".join(candidate_paths) if candidate_paths else "",
            "exists": exists,
            "state": "present" if exists else "missing",
            "missing": required and not exists,
            "reason": "remote packet requires checkpoint hash before any local formal claim",
        }
    ]


def _h01_h02_group(*, h01_manifest: dict[str, Any], h02_acceptance: dict[str, Any]) -> dict[str, Any]:
    h01_ready = str(h01_manifest.get("status")) in {"ready", "formal_ready", "ready_for_formal_run", "ready_for_formal_evaluation"}
    h02_accepted = h02_acceptance.get("formal_output_accepted") is True and h02_acceptance.get("paper_result_input_allowed") is True
    h02_blockers = _strings(h02_acceptance.get("blockers"))
    items = [
        {
            "artifact_id": "h01_ready_for_formal_run",
            "path": "0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json",
            "exists": bool(h01_manifest),
            "state": h01_manifest.get("status"),
            "missing": not h01_ready,
            "reason": ", ".join(_strings(h01_manifest.get("blockers"))) or "H01 manifest must become ready for formal run",
        },
        {
            "artifact_id": "h02_formal_output_acceptance",
            "path": "0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json",
            "exists": bool(h02_acceptance),
            "state": h02_acceptance.get("status"),
            "missing": not h02_accepted,
            "reason": ", ".join(h02_blockers) or "H02 must accept formal outputs",
        },
    ]
    missing = [item for item in items if item["missing"]]
    return {
        "group_id": "h01_h02_formal_evaluation_acceptance",
        "category": "evaluation_acceptance",
        "required_before": "claim_gate",
        "complete": not missing,
        "blocked_by": [str(item["artifact_id"]) for item in missing],
        "items": items,
    }


def _claim_gate_group(*, source_freshness: dict[str, Any], h02_acceptance: dict[str, Any]) -> dict[str, Any]:
    claim_targets = [target for target in _source_targets(source_freshness) if str(target.get("required_before")) == "formal_claim_gate"]
    h02_accepted = h02_acceptance.get("formal_output_accepted") is True
    items = [
        {
            "artifact_id": str(target.get("artifact_id")),
            "path": str(target.get("path") or ""),
            "exists": Path(str(target.get("path") or "")).is_file(),
            "state": target.get("freshness_state"),
            "missing": True,
            "reason": "claim gate artifact must be regenerated after H02 formal acceptance",
        }
        for target in claim_targets
    ]
    if not h02_accepted:
        items.append(
            {
                "artifact_id": "h02_formal_acceptance_before_claim_gate",
                "path": "0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json",
                "exists": bool(h02_acceptance),
                "state": h02_acceptance.get("status"),
                "missing": True,
                "reason": "claim gate cannot be regenerated from blocked H02 outputs",
            }
        )
    missing = [item for item in items if item.get("missing")]
    return {
        "group_id": "claim_gate_regeneration",
        "category": "claim_gate",
        "required_before": "formal_claim",
        "complete": not missing,
        "blocked_by": [str(item.get("artifact_id")) for item in missing],
        "items": items,
    }


def _formal_gate_requirements(
    *,
    groups: Sequence[dict[str, Any]],
    current_gate_summary: dict[str, Any],
    post_plan: dict[str, Any],
) -> list[dict[str, Any]]:
    groups_by_id = {str(group.get("group_id")): group for group in groups}
    stages_by_id = _post_plan_stages_by_id(post_plan)
    remote_training_allowed = current_gate_summary.get("ready_to_run_remote_training") is True
    protocol_lane_pending = _protocol_lane_pending(current_gate_summary)
    stage_blocker = "protocol_lane_decision_pending" if protocol_lane_pending else None
    return [
        _requirement(
            requirement_id="training_remote_ppo_checkpoint",
            phase="training",
            group=groups_by_id.get("remote_training_outputs", {}),
            responsible_stage=_blocked_stage_context(
                _stage_context(stages_by_id, "gate3_remote_training"),
                blocker=stage_blocker,
            ),
            execution_allowed_now=remote_training_allowed,
            required_before="gate3_remote_audit_pullback",
            acceptable_evidence=[
                "remote-produced train/final_model.zip pulled back to the local formal Gate3 trial directory",
                "train/summary.json with PPO run metadata and terminal-RS training signals",
                "train/training_manifest.json with protocol label, source head, host, seed, and command provenance",
            ],
            invalid_substitutes=[
                "local training output",
                "available-subset smoke model",
                "no-warm Gate3 failed checkpoint",
                "stdout without pulled-back checkpoint and manifest",
            ],
        ),
        _requirement(
            requirement_id="evaluation_gate3_episode_outputs",
            phase="evaluation",
            group=groups_by_id.get("gate3_evaluation_outputs", {}),
            responsible_stage=_blocked_stage_context(
                _stage_context(stages_by_id, "gate3_remote_audit_pullback"),
                blocker=stage_blocker,
            ),
            execution_allowed_now=remote_training_allowed,
            required_before="h01_h02_formal_regeneration",
            acceptable_evidence=[
                "eval/gate3_eval_episodes.csv from the approved formal remote run",
                "eval/gate3_summary.json with formal terminal-RS success, collision, truncation, and timing fields",
            ],
            invalid_substitutes=[
                "H02 available-subset smoke CSV",
                "paper table preview",
                "no-warm formal failure eval reused as warm-start evidence",
            ],
        ),
        _requirement(
            requirement_id="acceptance_remote_pullback_and_audit",
            phase="acceptance",
            group=groups_by_id.get("gate3_acceptance_pullback", {}),
            responsible_stage=_blocked_stage_context(
                _stage_context(stages_by_id, "gate3_remote_audit_pullback"),
                blocker=stage_blocker,
            ),
            execution_allowed_now=remote_training_allowed,
            required_before="h02_formal_acceptance",
            acceptable_evidence=[
                "gate3_trial_manifest.json copied back from the formal remote run",
                "gate3_formal_audit.json marking the run formal, scoped, and non-smoke",
                "checkpoint SHA-256 record for the pulled-back final_model.zip",
            ],
            invalid_substitutes=[
                "remote command success without local pullback",
                "checkpoint file without hash record",
                "audit marked candidate, smoke, preview, or not_formal",
            ],
        ),
        _requirement(
            requirement_id="h01_h02_formal_evaluation_acceptance",
            phase="evaluation_acceptance",
            group=groups_by_id.get("h01_h02_formal_evaluation_acceptance", {}),
            responsible_stage=_stage_context(stages_by_id, "regenerate_h01_h02_formal_artifacts"),
            execution_allowed_now=False,
            required_before="formal_claim_gate",
            acceptable_evidence=[
                "H01 manifest status ready_for_formal_run or ready_for_formal_evaluation after F02.6 is closed",
                "H02 acceptance with formal_output_accepted=true and paper_result_input_allowed=true",
                "formal PPO rows present and accepted against the H01 required output schema",
            ],
            invalid_substitutes=[
                "blocked H01 manifest",
                "blocked H02 acceptance audit",
                "formal-looking tables generated from smoke or missing PPO rows",
            ],
        ),
    ]


def _formal_gate_handoff_index(
    *,
    current_gate_summary: dict[str, Any],
    formal_requirements: Sequence[dict[str, Any]],
    inputs: dict[str, str],
) -> dict[str, Any]:
    decision_status = str(current_gate_summary.get("f02_6_decision_record_status") or "missing")
    decision_closed = decision_status == "approved"
    remote_training_allowed_now = current_gate_summary.get("ready_to_run_remote_training") is True
    requirements = [_decision_handoff_requirement(decision_status=decision_status, inputs=inputs)]
    for requirement in formal_requirements:
        requirements.append(_formal_requirement_handoff_row(requirement=requirement, inputs=inputs))
    unresolved = [item for item in requirements if item["status"] != "satisfied"]
    protocol_lane_pending = _protocol_lane_pending(current_gate_summary)
    if protocol_lane_pending:
        status = "blocked_until_protocol_lane_decision"
    elif unresolved and not decision_closed:
        status = "blocked_until_f02_6_decision"
    elif unresolved:
        status = "formal_gate_requirements_open"
    else:
        status = "formal_gate_evidence_ready_for_h01_h02_claim_gates"
    next_item = unresolved[0] if unresolved else None
    return {
        "status": status,
        "next_action": _next_handoff_action(next_item, protocol_lane_pending=protocol_lane_pending),
        "local_training_allowed_now": False,
        "remote_training_allowed_now": remote_training_allowed_now,
        "formal_result_material_allowed_now": False,
        "requirement_count": len(requirements),
        "open_requirement_count": len(unresolved),
        "requirements": requirements,
        "authority_artifacts": {
            "decision_record": inputs["decision_record"],
            "transition_gate_audit": inputs["f02_6_transition_gate_audit"],
            "post_f02_6_regeneration_plan": inputs["post_f02_6_regeneration_plan"],
            "remote_formal_execution_packet": inputs["remote_formal_execution_packet"],
            "formal_missing_artifacts_inventory": "0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json",
            "h01_manifest": inputs["h01_manifest"],
            "h02_formal_acceptance": inputs["h02_formal_acceptance"],
            "protocol_lane_status_report": inputs["protocol_lane_status_report"],
        },
        "claim_boundary": "This handoff index is a gate-navigation aid; it is not a training command, evaluation command, result table, or paper-result source.",
    }


def _decision_handoff_requirement(*, decision_status: str, inputs: dict[str, str]) -> dict[str, Any]:
    complete = decision_status == "approved"
    return {
        "order": 1,
        "requirement_id": "f02_6_human_decision",
        "phase": "decision",
        "status": "satisfied" if complete else "blocked_missing_decision",
        "execution_allowed_now": False,
        "missing_artifact_ids": [] if complete else ["f02_6_decision_record"],
        "missing_artifact_count": 0 if complete else 1,
        "source_artifacts": [inputs["decision_record"], inputs["f02_6_transition_gate_audit"]],
        "downstream_consumers": [
            inputs["post_f02_6_regeneration_plan"],
            inputs["remote_formal_execution_packet"],
            inputs["h01_manifest"],
            inputs["h02_formal_acceptance"],
        ],
        "acceptable_evidence": [
            "Dr Sun approval or rejection recorded in f02_6_decision_record.json",
            "transition gate audit remains passed with zero open issues",
        ],
        "invalid_substitutes": [
            "assistant inference from prior chat",
            "remote readiness smoke",
            "no-warm formal failure result",
        ],
    }


def _formal_requirement_handoff_row(*, requirement: dict[str, Any], inputs: dict[str, str]) -> dict[str, Any]:
    source_artifacts = {
        "training_remote_ppo_checkpoint": [
            inputs["remote_formal_execution_packet"],
            inputs["remote_packet_safety_audit"],
        ],
        "evaluation_gate3_episode_outputs": [
            inputs["remote_formal_execution_packet"],
            inputs["h02_formal_acceptance"],
        ],
        "acceptance_remote_pullback_and_audit": [
            inputs["remote_formal_execution_packet"],
            inputs["remote_packet_safety_audit"],
            inputs["h02_formal_acceptance"],
        ],
        "h01_h02_formal_evaluation_acceptance": [
            inputs["h01_manifest"],
            inputs["h02_formal_acceptance"],
        ],
    }
    downstream_consumers = {
        "training_remote_ppo_checkpoint": [inputs["h01_manifest"], inputs["h02_formal_acceptance"]],
        "evaluation_gate3_episode_outputs": [inputs["h02_formal_acceptance"]],
        "acceptance_remote_pullback_and_audit": [inputs["h02_formal_acceptance"]],
        "h01_h02_formal_evaluation_acceptance": [
            "0_trials/module2_claim_safety/module2_claim_safety.json",
            "0_trials/module2_paper_readiness/module2_paper_readiness.json",
        ],
    }
    requirement_id = str(requirement.get("requirement_id") or "unknown_requirement")
    missing_ids = _strings(requirement.get("missing_artifact_ids"))
    return {
        "order": _handoff_order(requirement_id),
        "requirement_id": requirement_id,
        "phase": str(requirement.get("phase") or "unknown"),
        "status": str(requirement.get("status") or "unknown"),
        "execution_allowed_now": bool(requirement.get("execution_allowed_now")),
        "missing_artifact_ids": missing_ids,
        "missing_artifact_count": len(missing_ids),
        "missing_paths": _strings(requirement.get("missing_paths")),
        "source_artifacts": source_artifacts.get(requirement_id, []),
        "downstream_consumers": downstream_consumers.get(requirement_id, []),
        "responsible_stage_id": requirement.get("responsible_stage_id"),
        "responsible_stage_status": requirement.get("responsible_stage_status"),
        "responsible_stage_allowed_now": requirement.get("responsible_stage_allowed_now"),
        "responsible_stage_blocked_by": _strings(requirement.get("responsible_stage_blocked_by")),
        "responsible_stage_evidence_paths": _strings(requirement.get("responsible_stage_evidence_paths")),
        "acceptable_evidence": _strings(requirement.get("acceptable_evidence")),
        "invalid_substitutes": _strings(requirement.get("invalid_substitutes")),
    }


def _handoff_order(requirement_id: str) -> int:
    order = {
        "training_remote_ppo_checkpoint": 2,
        "evaluation_gate3_episode_outputs": 3,
        "acceptance_remote_pullback_and_audit": 4,
        "h01_h02_formal_evaluation_acceptance": 5,
    }
    return order.get(requirement_id, 99)


def _next_handoff_action(next_item: dict[str, Any] | None, *, protocol_lane_pending: bool = False) -> dict[str, Any]:
    if protocol_lane_pending:
        return {
            "action_id": "record_protocol_lane_decision",
            "allowed_for_agent_now": False,
            "requires_dr_sun": True,
            "description": "Dr Sun must select the protocol lane before any new success training, preflight, audit, or result material.",
        }
    if next_item is None:
        return {
            "action_id": "no_open_formal_gate_handoff_requirements",
            "allowed_for_agent_now": False,
            "requires_dr_sun": False,
            "description": "All indexed formal gate evidence rows are satisfied; claim gates must still be regenerated and audited separately.",
        }
    if next_item["requirement_id"] == "f02_6_human_decision":
        return {
            "action_id": "record_f02_6_decision",
            "allowed_for_agent_now": False,
            "requires_dr_sun": True,
            "description": "Dr Sun must approve obstacle-summary warm-start or reject it before remote formal execution can proceed.",
        }
    return {
        "action_id": f"resolve_{next_item['requirement_id']}",
        "allowed_for_agent_now": bool(next_item.get("execution_allowed_now")),
        "requires_dr_sun": False,
        "description": f"Resolve {next_item['requirement_id']} with acceptable evidence; invalid substitutes remain disallowed.",
    }


def _requirement(
    *,
    requirement_id: str,
    phase: str,
    group: dict[str, Any],
    responsible_stage: dict[str, Any],
    execution_allowed_now: bool,
    required_before: str,
    acceptable_evidence: Sequence[str],
    invalid_substitutes: Sequence[str],
) -> dict[str, Any]:
    complete = group.get("complete") is True
    missing_items = [item for item in group.get("items", ()) if isinstance(item, dict) and item.get("missing")]
    if complete:
        status = "satisfied"
    elif execution_allowed_now:
        status = "ready_to_execute_missing_outputs"
    else:
        status = "blocked_missing_outputs"
    return {
        "requirement_id": requirement_id,
        "phase": phase,
        "status": status,
        "complete": complete,
        "execution_allowed_now": execution_allowed_now,
        "required_before": required_before,
        "missing_artifact_ids": [str(item.get("artifact_id")) for item in missing_items],
        "missing_paths": [str(item.get("path") or "") for item in missing_items],
        "blocked_by": _strings(group.get("blocked_by")),
        "responsible_stage_id": responsible_stage.get("stage_id"),
        "responsible_stage_status": responsible_stage.get("status"),
        "responsible_stage_allowed_now": responsible_stage.get("allowed_now"),
        "responsible_stage_blocked_by": _strings(responsible_stage.get("blocked_by")),
        "responsible_stage_evidence_paths": _strings(responsible_stage.get("evidence_paths")),
        "acceptable_evidence": list(acceptable_evidence),
        "invalid_substitutes": list(invalid_substitutes),
    }


def _requirement_counts(requirements: Sequence[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for requirement in requirements:
        status = str(requirement.get("status") or "unknown")
        counts[status] = counts.get(status, 0) + 1
    return counts


def _audit_issues(
    *,
    decision: dict[str, Any],
    decision_gate: dict[str, Any],
    transition_gate: dict[str, Any],
    post_plan: dict[str, Any],
    source_freshness: dict[str, Any],
    remote_packet: dict[str, Any],
    remote_packet_audit: dict[str, Any],
    h01_manifest: dict[str, Any],
    h02_acceptance: dict[str, Any],
    groups: Sequence[dict[str, Any]],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    inputs = [
        decision,
        decision_gate,
        transition_gate,
        post_plan,
        source_freshness,
        remote_packet,
        remote_packet_audit,
        h01_manifest,
        h02_acceptance,
    ]
    for name, payload in zip(
        (
            "decision",
            "decision_gate",
            "transition_gate",
            "post_plan",
            "source_freshness",
            "remote_packet",
            "remote_packet_audit",
            "h01_manifest",
            "h02_acceptance",
        ),
        inputs,
    ):
        if payload.get("local_training_allowed") is True:
            issues.append(_issue(f"{name}_allows_local_training", f"{name} must not allow local training."))
        if payload.get("formal_claim_allowed") is True or payload.get("formal_claim_allowed_before_audit") is True:
            issues.append(_issue(f"{name}_allows_formal_claim", f"{name} must not allow formal claims before acceptance."))
        if payload.get("runs_training") is True:
            issues.append(_issue(f"{name}_runs_training", f"{name} must be an audit artifact, not a training entrypoint."))
        if payload.get("runs_remote_preflight") is True:
            issues.append(_issue(f"{name}_runs_remote_preflight", f"{name} must not execute remote preflight."))
    if not transition_gate:
        issues.append(_issue("transition_gate_audit_missing", "F02.6 transition gate audit must feed the missing-artifacts inventory."))
    elif transition_gate.get("status") != "f02_6_transition_gate_audit_passed":
        issues.append(_issue("transition_gate_audit_not_passed", "F02.6 transition gate audit must pass before listing downstream formal artifacts as executable."))
    if int(transition_gate.get("audit_issue_count") or 0) > 0:
        issues.append(_issue("transition_gate_audit_issues_open", "F02.6 transition gate audit reports open issues."))
    decision_status = str(decision.get("status") or "")
    if decision_status in {"pending_human_decision", "pending"} and remote_packet.get("ready_to_run_remote_training") is True:
        issues.append(_issue("pending_decision_remote_packet_ready", "Remote packet must not be ready while F02.6 is pending."))
    if remote_packet_audit and remote_packet_audit.get("status") != "remote_packet_safety_audit_passed":
        issues.append(_issue("remote_packet_safety_audit_not_passed", "Remote packet safety audit must pass before formal execution."))
    if h02_acceptance.get("formal_output_accepted") is True and _group_missing(groups, "gate3_acceptance_pullback"):
        issues.append(_issue("h02_accepts_missing_pullback_artifacts", "H02 cannot accept formal output while Gate3 audit/pullback artifacts are missing."))
    if h01_manifest.get("status") in {"ready", "ready_for_formal_run"} and _group_missing(groups, "remote_training_outputs"):
        issues.append(_issue("h01_ready_without_remote_training_outputs", "H01 should not be ready without remote PPO training artifacts."))
    return _unique_issues(issues)


def _current_gate_summary(
    *,
    decision: dict[str, Any],
    decision_gate: dict[str, Any],
    transition_gate: dict[str, Any],
    post_plan: dict[str, Any],
    source_freshness: dict[str, Any],
    remote_packet: dict[str, Any],
    remote_packet_audit: dict[str, Any],
    h01_manifest: dict[str, Any],
    h02_acceptance: dict[str, Any],
    protocol_lane_status: dict[str, Any],
) -> dict[str, Any]:
    post_summary = post_plan.get("blocking_summary") if isinstance(post_plan.get("blocking_summary"), dict) else {}
    protocol_summary = _protocol_lane_status_summary(protocol_lane_status)
    protocol_lane_pending = _protocol_lane_pending(protocol_summary)
    ready_to_run_remote_training = remote_packet.get("ready_to_run_remote_training")
    if protocol_lane_pending:
        ready_to_run_remote_training = False
    return {
        "f02_6_decision_record_status": decision.get("status"),
        **protocol_summary,
        "f02_6_decision_gate_status": decision_gate.get("status"),
        "f02_6_transition_gate_status": transition_gate.get("status"),
        "f02_6_transition_gate_audit_issue_count": transition_gate.get("audit_issue_count"),
        "post_f02_6_plan_status": post_plan.get("status"),
        "post_plan_training_allowed_now": post_summary.get("training_allowed_now"),
        "post_plan_remote_preflight_allowed_now": post_summary.get("remote_preflight_allowed_now"),
        "source_freshness_status": source_freshness.get("status"),
        "source_freshness_regeneration_required": source_freshness.get("regeneration_required_before_remote_formal_execution"),
        "source_freshness_blocking_regeneration_required": _source_freshness_blocking_regeneration_required(source_freshness),
        "remote_packet_status": remote_packet.get("status"),
        "ready_to_run_remote_training": ready_to_run_remote_training,
        "remote_packet_safety_audit_status": remote_packet_audit.get("status"),
        "h01_manifest_status": h01_manifest.get("status"),
        "h01_blockers": _strings(h01_manifest.get("blockers")),
        "h02_acceptance_status": h02_acceptance.get("status"),
        "h02_blockers": _strings(h02_acceptance.get("blockers")),
    }


def _protocol_lane_status_summary(protocol_lane_status: dict[str, Any]) -> dict[str, Any]:
    current_status = (
        protocol_lane_status.get("current_status")
        if isinstance(protocol_lane_status.get("current_status"), dict)
        else {}
    )
    return {
        "protocol_lane_status": protocol_lane_status.get("status"),
        "protocol_lane_next_blocked_lane": current_status.get("next_blocked_lane"),
        "protocol_lane_decision_record_status": current_status.get("decision_record_status"),
        "protocol_lane_selected_lane_id": current_status.get("selected_lane_id"),
        "protocol_lane_allowed_next_action_ids": _strings(current_status.get("allowed_next_action_ids")),
        "protocol_lane_blocked_action_ids": _strings(current_status.get("blocked_action_ids")),
        "protocol_lane_new_success_training_allowed_now": current_status.get("new_success_training_allowed_now"),
    }


def _protocol_lane_pending(summary: dict[str, Any]) -> bool:
    return (
        summary.get("protocol_lane_status") == "protocol_lane_status_blocked_pending_lane_decision"
        or summary.get("protocol_lane_next_blocked_lane") == "protocol_lane_decision"
        or summary.get("protocol_lane_decision_record_status") == "pending_protocol_lane_decision"
    )


def _source_freshness_blocking_regeneration_required(source_freshness: dict[str, Any]) -> bool:
    if "blocking_regeneration_required_before_remote_formal_execution" in source_freshness:
        return source_freshness.get("blocking_regeneration_required_before_remote_formal_execution") is True
    return source_freshness.get("regeneration_required_before_remote_formal_execution") is True


def _missing_counts(groups: Sequence[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for group in groups:
        category = str(group.get("category") or "unknown")
        counts[category] = counts.get(category, 0) + sum(1 for item in group.get("items", ()) if isinstance(item, dict) and item.get("missing"))
    return counts


def _expected_artifacts(remote_packet: dict[str, Any]) -> list[str]:
    pullback = remote_packet.get("post_run_pullback") if isinstance(remote_packet.get("post_run_pullback"), dict) else {}
    artifacts = pullback.get("expected_artifacts") if isinstance(pullback.get("expected_artifacts"), list) else []
    return [str(item) for item in artifacts if item]


def _artifact_for_suffix(paths: Sequence[str], suffix: str) -> str:
    for path in paths:
        if path.endswith(suffix):
            return path
    return ""


def _source_targets(source_freshness: dict[str, Any]) -> list[dict[str, Any]]:
    targets = source_freshness.get("ordered_regeneration_targets")
    if not isinstance(targets, list):
        return []
    return [target for target in targets if isinstance(target, dict)]


def _post_plan_stages_by_id(post_plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    stages = post_plan.get("ordered_stages")
    if not isinstance(stages, list):
        return {}
    return {
        str(stage.get("stage_id")): stage
        for stage in stages
        if isinstance(stage, dict) and stage.get("stage_id")
    }


def _stage_context(stages_by_id: dict[str, dict[str, Any]], stage_id: str) -> dict[str, Any]:
    stage = stages_by_id.get(stage_id)
    if not stage:
        return {
            "stage_id": stage_id,
            "status": "missing_stage",
            "allowed_now": False,
            "blocked_by": ["post_f02_6_ordered_stage_missing"],
            "evidence_paths": [],
        }
    return {
        "stage_id": stage_id,
        "status": stage.get("status"),
        "allowed_now": stage.get("allowed_now"),
        "blocked_by": _strings(stage.get("blocked_by")),
        "evidence_paths": _strings(stage.get("evidence_paths")),
    }


def _blocked_stage_context(stage: dict[str, Any], *, blocker: str | None) -> dict[str, Any]:
    if not blocker:
        return stage
    blocked_by = _strings(stage.get("blocked_by"))
    if blocker not in blocked_by:
        blocked_by.append(blocker)
    return {
        **stage,
        "status": "blocked",
        "allowed_now": False,
        "blocked_by": blocked_by,
    }


def _group_missing(groups: Sequence[dict[str, Any]], group_id: str) -> bool:
    for group in groups:
        if group.get("group_id") == group_id:
            return any(isinstance(item, dict) and item.get("missing") for item in group.get("items", ()))
    return False


def _strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _issue(issue_id: str, message: str) -> dict[str, str]:
    return {"issue_id": issue_id, "message": message}


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


def _slug(value: str) -> str:
    out = []
    for char in value.lower():
        out.append(char if char.isalnum() else "_")
    return "".join(out).strip("_")


def _read_json(path: Path) -> dict[str, Any]:
    if not Path(path).is_file():
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _source_head() -> str:
    return module2_source_head()


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 Formal Gate Missing Artifacts Audit",
        "",
        "This file inventories missing formal-gate evidence. It does not execute commands or write paper results.",
        "",
        f"- status: `{manifest['status']}`",
        f"- all_required_evidence_present: `{manifest['all_required_evidence_present']}`",
        f"- audit_issue_count: `{manifest['audit_issue_count']}`",
        f"- local_training_allowed: `{manifest['local_training_allowed']}`",
        f"- formal_claim_allowed: `{manifest['formal_claim_allowed']}`",
        "",
        "## Current Gate Summary",
        "",
    ]
    for key, value in manifest["current_gate_summary"].items():
        lines.append(f"- {key}: `{value}`")
    handoff_index = manifest["formal_gate_handoff_index"]
    lines.extend(["", "## Formal Gate Handoff Index", ""])
    lines.append(f"- status: `{handoff_index['status']}`")
    lines.append(f"- open_requirement_count: `{handoff_index['open_requirement_count']}`")
    lines.append(f"- local_training_allowed_now: `{handoff_index['local_training_allowed_now']}`")
    lines.append(f"- remote_training_allowed_now: `{handoff_index['remote_training_allowed_now']}`")
    lines.append(f"- formal_result_material_allowed_now: `{handoff_index['formal_result_material_allowed_now']}`")
    next_action = handoff_index["next_action"]
    lines.append(
        f"- next_action: `{next_action['action_id']}` "
        f"(requires_dr_sun=`{next_action['requires_dr_sun']}`, "
        f"allowed_for_agent_now=`{next_action['allowed_for_agent_now']}`)"
    )
    lines.append(f"- next_action_description: {next_action['description']}")
    lines.append(f"- claim_boundary: {handoff_index['claim_boundary']}")
    lines.extend(["", "### Authority Artifacts", ""])
    for key, value in handoff_index["authority_artifacts"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "### Handoff Requirements", ""])
    for requirement in handoff_index["requirements"]:
        lines.append(
            f"- `{requirement['requirement_id']}` ({requirement['phase']}): "
            f"status=`{requirement['status']}`, missing_count=`{requirement['missing_artifact_count']}`, "
            f"execution_allowed_now=`{requirement['execution_allowed_now']}`"
        )
        if requirement["missing_artifact_ids"]:
            lines.append(f"  - missing_artifact_ids: `{', '.join(requirement['missing_artifact_ids'])}`")
        if requirement.get("source_artifacts"):
            lines.append(f"  - source_artifacts: `{'; '.join(requirement['source_artifacts'])}`")
        if requirement.get("downstream_consumers"):
            lines.append(f"  - downstream_consumers: `{'; '.join(requirement['downstream_consumers'])}`")
        if requirement.get("responsible_stage_id"):
            lines.append(
                f"  - responsible_stage: `{requirement['responsible_stage_id']}` "
                f"(status=`{requirement.get('responsible_stage_status')}`, "
                f"allowed_now=`{requirement.get('responsible_stage_allowed_now')}`)"
            )
    lines.extend(["", "## Missing Counts", ""])
    for category, count in sorted(manifest["missing_counts_by_category"].items()):
        lines.append(f"- {category}: `{count}`")
    lines.extend(["", "## Formal Gate Requirements", ""])
    for requirement in manifest["formal_gate_requirements"]:
        lines.append(
            f"- `{requirement['requirement_id']}` ({requirement['phase']}): "
            f"status=`{requirement['status']}`, execution_allowed_now=`{requirement['execution_allowed_now']}`"
        )
        if requirement["missing_artifact_ids"]:
            lines.append(f"  - missing_artifact_ids: `{', '.join(requirement['missing_artifact_ids'])}`")
        if requirement["blocked_by"]:
            lines.append(f"  - blocked_by: `{', '.join(requirement['blocked_by'])}`")
        if requirement.get("responsible_stage_id"):
            lines.append(
                f"  - responsible_stage: `{requirement['responsible_stage_id']}` "
                f"(status=`{requirement.get('responsible_stage_status')}`, "
                f"allowed_now=`{requirement.get('responsible_stage_allowed_now')}`)"
            )
        if requirement.get("responsible_stage_blocked_by"):
            lines.append(f"  - responsible_stage_blocked_by: `{', '.join(requirement['responsible_stage_blocked_by'])}`")
        lines.append(f"  - acceptable_evidence: `{'; '.join(requirement['acceptable_evidence'])}`")
        lines.append(f"  - invalid_substitutes: `{'; '.join(requirement['invalid_substitutes'])}`")
    lines.extend(["", "## Evidence Groups", ""])
    for group in manifest["missing_evidence_groups"]:
        lines.append(
            f"- `{group['group_id']}` ({group['category']}): complete=`{group['complete']}`, "
            f"blocked_by=`{', '.join(group['blocked_by'])}`"
        )
        for item in group["items"]:
            if item.get("missing"):
                lines.append(f"  - missing `{item.get('artifact_id')}`: `{item.get('path')}` ({item.get('reason')})")
    lines.extend(["", "## Audit Issues", ""])
    if manifest["audit_issues"]:
        lines.extend(f"- `{issue['issue_id']}`: {issue['message']}" for issue in manifest["audit_issues"])
    else:
        lines.append("- none")
    lines.extend(["", "## Claim Boundaries", ""])
    lines.extend(f"- {item}" for item in manifest["claim_boundaries"])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
