from __future__ import annotations

import argparse
import json
import shlex
import socket
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_f02_6_decision_record")
DEFAULT_PACKET = Path("0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json")
DEFAULT_REMOTE_WARM_PREFLIGHT = Path(
    "0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_pending_remote_v1/gate3_preflight_manifest.json"
)
DEFAULT_BC_CHECKPOINT = Path("2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt")
APPROVE_OBSTACLE_SUMMARY = "approve_obstacle_summary_warm_start"
REJECT_OBSTACLE_SUMMARY = "reject_obstacle_summary_warm_start"
DECISION_OWNER = "Dr Sun"
DECISION_NOTE_GUIDANCE = (
    "selected decision",
    "human rationale",
    "evidence basis",
    "risk accepted or avoided",
    "next gated action",
)
EXECUTION_BLOCKED_ACTION_IDS = (
    "remote_preflight",
    "remote_training",
    "local_training",
    "formal_claim",
    "paper_result_material",
)
POST_DECISION_STILL_REQUIRES = (
    "source_freshness_audit",
    "post_f02_6_regeneration_plan",
    "post_f02_6_plan_audit",
    "remote_formal_execution_packet_ready",
    "approved_remote_preflight",
)


@dataclass(frozen=True)
class F026DecisionRecordConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    packet_path: Path = DEFAULT_PACKET
    remote_warm_preflight_path: Path = DEFAULT_REMOTE_WARM_PREFLIGHT
    decision: str = "pending"
    decider: str | None = None
    decision_note: str | None = None
    bc_checkpoint: Path = DEFAULT_BC_CHECKPOINT


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    cfg = F026DecisionRecordConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        packet_path=args.packet,
        remote_warm_preflight_path=args.remote_warm_preflight,
        decision=args.decision,
        decider=args.decider,
        decision_note=args.decision_note,
        bc_checkpoint=args.bc_checkpoint,
    )
    record = build_record(cfg)
    output_dir = Path(cfg.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = cfg.manifest_out or output_dir / "f02_6_decision_record.json"
    markdown_out = cfg.markdown_out or output_dir / "f02_6_decision_record.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(record), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": record["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_record(config: F026DecisionRecordConfig) -> dict[str, Any]:
    packet = _read_json(config.packet_path)
    remote_warm_preflight = _read_json(config.remote_warm_preflight_path)
    requested_decision = str(config.decision)
    _validate_requested_decision(requested_decision)
    _validate_decision_note(requested_decision=requested_decision, decision_note=config.decision_note)
    normalized = _normalize_decision(
        requested_decision=requested_decision,
        decider=config.decider,
        packet=packet,
    )
    observed_preflight = _preflight_record(config.remote_warm_preflight_path, remote_warm_preflight)
    conditional_actions = _conditional_actions(config, packet=packet, observed_preflight=observed_preflight)
    return {
        "schema_version": 1,
        "record_name": "module2_f02_6_decision_record",
        "status": normalized["status"],
        "created_at_utc": datetime.now(UTC).isoformat(),
        "execution_host": socket.gethostname(),
        "source_head": _source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "runs_remote_audit": False,
        "decision_owner_required": DECISION_OWNER,
        "requested_decision": requested_decision,
        "decider": config.decider,
        "decision_note": config.decision_note,
        "decision_note_audit": _decision_note_audit(
            requested_decision=requested_decision,
            decision_note=config.decision_note,
        ),
        "packet": _packet_record(config.packet_path, packet),
        "decision_mapping": _decision_mapping(),
        "effective_warm_start_decision": normalized["effective_warm_start_decision"],
        "remote_training_allowed": normalized["remote_training_allowed"],
        "remote_preflight_allowed_now": False,
        "remote_training_allowed_now": False,
        "local_training_allowed": False,
        "local_training_allowed_now": False,
        "formal_claim_allowed": False,
        "formal_claim_allowed_now": False,
        "paper_result_material_allowed_now": False,
        "decision_record_is_not_training_authorization": True,
        "decision_record_is_not_paper_result_material": True,
        "current_authorization": _current_authorization(normalized["status"]),
        "record_command_templates": _record_command_templates(),
        "post_decision_non_authorization_invariants": _post_decision_non_authorization_invariants(),
        "next_remote_preflight_status": normalized["next_remote_preflight_status"],
        "blockers": normalized["blockers"],
        "remote_preflight_observed": observed_preflight,
        "conditional_actions": conditional_actions,
        "downstream_consumption": {
            "h01_manifest_decision_value": normalized["effective_warm_start_decision"],
            "preflight_warm_start_decision_value": normalized["preflight_warm_start_decision"],
            "audit_warm_start_decision_value": normalized["audit_warm_start_decision"],
            "record_is_sufficient_to_claim_performance": False,
            "record_is_sufficient_to_run_remote_preflight_now": False,
            "record_is_sufficient_to_run_remote_training_now": False,
        },
        "claim_boundaries": [
            "This record only stores Dr Sun's F02.6 decision state; it is not a training result.",
            "Approval unlocks source-fresh regeneration and approved preflight regeneration, but does not itself allow remote execution now.",
            "Formal PPO warm-start training must run on gpu3070ti-relay, not on the local Mac.",
            "A rejected obstacle-summary warm-start requires a stronger/full patch-CNN protocol before a warm-start formal run.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Module2 F02.6 machine-readable decision record.")
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--remote-warm-preflight", type=Path, default=DEFAULT_REMOTE_WARM_PREFLIGHT)
    parser.add_argument("--bc-checkpoint", type=Path, default=DEFAULT_BC_CHECKPOINT)
    parser.add_argument("--decision", choices=("pending", APPROVE_OBSTACLE_SUMMARY, REJECT_OBSTACLE_SUMMARY), default="pending")
    parser.add_argument("--decider", default=None)
    parser.add_argument("--decision-note", default=None)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    return parser.parse_args(list(argv) if argv is not None else None)


def _validate_requested_decision(decision: str) -> None:
    allowed = {"pending", APPROVE_OBSTACLE_SUMMARY, REJECT_OBSTACLE_SUMMARY}
    if decision not in allowed:
        raise ValueError(f"unsupported F02.6 decision {decision!r}; expected one of {sorted(allowed)}")


def _validate_decision_note(*, requested_decision: str, decision_note: str | None) -> None:
    if requested_decision == "pending":
        return
    if not isinstance(decision_note, str) or not decision_note.strip():
        raise ValueError("non-pending F02.6 decisions require a non-empty --decision-note")


def _decision_note_audit(*, requested_decision: str, decision_note: str | None) -> dict[str, Any]:
    note = decision_note.strip() if isinstance(decision_note, str) else ""
    normalized_note = note.lower()
    selected_route_terms = {
        "pending": ("pending",),
        APPROVE_OBSTACLE_SUMMARY: ("approve", "approved", "obstacle-summary", "warm-start"),
        REJECT_OBSTACLE_SUMMARY: ("reject", "rejected", "patch-cnn", "stronger"),
    }.get(requested_decision, ())
    evidence_terms = ("evidence", "packet", "bc", "formal-v2", "patch-cnn", "gate", "risk", "because")
    next_step_terms = ("source-fresh", "preflight", "protocol", "contract", "gate", "next")
    return {
        "required_for_non_pending_decision": requested_decision != "pending",
        "present": bool(note),
        "character_count": len(note),
        "word_count": len(note.split()),
        "guidance_items": list(DECISION_NOTE_GUIDANCE),
        "mentions_selected_route": any(term in normalized_note for term in selected_route_terms),
        "mentions_evidence_or_risk_basis": any(term in normalized_note for term in evidence_terms),
        "mentions_next_gated_action": any(term in normalized_note for term in next_step_terms),
        "quality_warning": _decision_note_quality_warning(
            requested_decision=requested_decision,
            present=bool(note),
            mentions_selected_route=any(term in normalized_note for term in selected_route_terms),
            mentions_evidence_or_risk_basis=any(term in normalized_note for term in evidence_terms),
            mentions_next_gated_action=any(term in normalized_note for term in next_step_terms),
        ),
    }


def _decision_note_quality_warning(
    *,
    requested_decision: str,
    present: bool,
    mentions_selected_route: bool,
    mentions_evidence_or_risk_basis: bool,
    mentions_next_gated_action: bool,
) -> str | None:
    if requested_decision == "pending":
        return None
    if not present:
        return "missing_required_decision_note"
    missing: list[str] = []
    if not mentions_selected_route:
        missing.append("selected_route")
    if not mentions_evidence_or_risk_basis:
        missing.append("evidence_or_risk_basis")
    if not mentions_next_gated_action:
        missing.append("next_gated_action")
    if missing:
        return "decision_note_should_mention_" + "_".join(missing)
    return None


def _normalize_decision(*, requested_decision: str, decider: str | None, packet: dict[str, Any]) -> dict[str, Any]:
    packet_status = str(packet.get("status"))
    recommendation = packet.get("recommendation") if isinstance(packet.get("recommendation"), dict) else {}
    recommended_decision = str(recommendation.get("decision"))
    packet_blockers = [str(item) for item in packet.get("blockers", ()) if item]

    if requested_decision == "pending":
        blockers = list(packet_blockers)
        if "requires_dr_sun_approval" not in blockers:
            blockers.append("requires_dr_sun_approval")
        return {
            "status": "pending_human_decision",
            "effective_warm_start_decision": "pending",
            "preflight_warm_start_decision": "pending",
            "audit_warm_start_decision": "pending",
            "remote_training_allowed": False,
            "next_remote_preflight_status": "blocked_until_decision",
            "blockers": blockers,
        }

    if decider != DECISION_OWNER:
        raise ValueError(f"F02.6 decision can only be recorded with decider={DECISION_OWNER!r}; got {decider!r}")

    if packet_status != "pending_human_decision":
        raise ValueError(f"expected pending decision packet before recording F02.6 decision, got {packet_status!r}")

    if recommended_decision != APPROVE_OBSTACLE_SUMMARY:
        raise ValueError(f"unexpected F02.6 packet recommendation {recommended_decision!r}")

    if requested_decision == APPROVE_OBSTACLE_SUMMARY:
        return {
            "status": "approved",
            "effective_warm_start_decision": "approved_obstacle_summary",
            "preflight_warm_start_decision": "approved_obstacle_summary",
            "audit_warm_start_decision": "approved_obstacle_summary",
            "remote_training_allowed": True,
            "next_remote_preflight_status": "ready_to_regenerate_approved_warm_start_preflight",
            "blockers": [],
        }

    return {
        "status": "rejected",
        "effective_warm_start_decision": "no_warm_only",
        "preflight_warm_start_decision": "not_used",
        "audit_warm_start_decision": "not_used",
        "remote_training_allowed": False,
        "next_remote_preflight_status": "blocked_rejected_requires_stronger_patch_cnn_protocol",
        "blockers": ["obstacle_summary_warm_start_rejected"],
    }


def _packet_record(path: Path, packet: dict[str, Any]) -> dict[str, Any]:
    recommendation = packet.get("recommendation") if isinstance(packet.get("recommendation"), dict) else {}
    return {
        "path": str(path),
        "exists": Path(path).is_file(),
        "status": str(packet.get("status")),
        "recommendation": recommendation.get("decision"),
        "decision_owner": recommendation.get("decision_owner"),
        "blockers": [str(item) for item in packet.get("blockers", ()) if item],
        "formal_claim_allowed": bool(recommendation.get("formal_claim_allowed")),
        "source_head": packet.get("source_head"),
    }


def _preflight_record(path: Path, preflight: dict[str, Any]) -> dict[str, Any]:
    blockers = preflight.get("formal_blockers") if isinstance(preflight.get("formal_blockers"), list) else []
    return {
        "path": str(path),
        "exists": Path(path).is_file(),
        "preflight_status": str(preflight.get("preflight_status")),
        "formal_trial_ready": bool(preflight.get("formal_trial_ready")),
        "warm_start_decision": str(preflight.get("warm_start_decision")),
        "blocker_codes": [str(item.get("code")) for item in blockers if isinstance(item, dict) and item.get("code")],
        "runner_command": str(preflight.get("runner_command", "")),
        "audit_command": str(preflight.get("audit_command", "")),
    }


def _decision_mapping() -> dict[str, Any]:
    return {
        APPROVE_OBSTACLE_SUMMARY: {
            "h01_manifest_value": "approved_obstacle_summary",
            "preflight_value": "approved_obstacle_summary",
            "audit_value": "approved_obstacle_summary",
        },
        REJECT_OBSTACLE_SUMMARY: {
            "h01_manifest_value": "no_warm_only",
            "preflight_value": "not_used",
            "audit_value": "not_used",
        },
    }


def _current_authorization(record_status: str) -> dict[str, Any]:
    if record_status == "pending_human_decision":
        allowed_actions = ["record_f02_6_decision"]
        status = "blocked_until_dr_sun_decision"
    elif record_status == "approved":
        allowed_actions = ["regenerate_post_f02_6_gate_artifacts"]
        status = "decision_recorded_not_execution_authorization"
    else:
        allowed_actions = ["draft_stronger_patch_cnn_protocol_contract"]
        status = "decision_recorded_not_execution_authorization"
    return {
        "authorization_status": status,
        "current_allowed_action_ids": allowed_actions,
        "current_blocked_action_ids": list(EXECUTION_BLOCKED_ACTION_IDS),
        "post_decision_routes_are_current_authorization": False,
        "record_scope": "local_decision_record_only",
        "remote_preflight_allowed_now": False,
        "remote_training_allowed_now": False,
        "local_training_allowed_now": False,
        "formal_claim_allowed_now": False,
        "paper_result_material_allowed_now": False,
    }


def _record_command_templates() -> list[dict[str, Any]]:
    return [_record_command_template(APPROVE_OBSTACLE_SUMMARY), _record_command_template(REJECT_OBSTACLE_SUMMARY)]


def _record_command_template(decision: str) -> dict[str, Any]:
    note = "<Dr Sun approval note>" if decision == APPROVE_OBSTACLE_SUMMARY else "<Dr Sun rejection note>"
    return {
        "decision": decision,
        "command": (
            "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_f02_6_decision_record "
            f"--decision {decision} --decider 'Dr Sun' --decision-note '{note}'"
        ),
        "execution_boundary": "local_decision_record_only",
        "requires_dr_sun_note": True,
        "allowed_for_agent_now": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "runs_remote_audit": False,
        "runs_remote_training": False,
        "formal_claim_allowed_now": False,
        "paper_result_material_allowed_now": False,
    }


def _post_decision_non_authorization_invariants() -> dict[str, Any]:
    return {
        "decision_record_is_not_training_authorization": True,
        "decision_record_is_not_paper_result_material": True,
        "local_training_allowed_now": False,
        "remote_preflight_allowed_now": False,
        "remote_training_allowed_now": False,
        "formal_claim_allowed_now": False,
        "paper_result_material_allowed_now": False,
        "formal_training_still_requires": list(POST_DECISION_STILL_REQUIRES),
        "blocked_after_decision_record": [
            {
                "action": "local_training",
                "allowed_after_decision_record": False,
                "reason": "Formal PPO training is remote-only on gpu3070ti-relay.",
            },
            {
                "action": "remote_preflight",
                "allowed_after_decision_record": False,
                "reason": "Approved decisions still require source-fresh gate regeneration before remote preflight.",
            },
            {
                "action": "remote_training",
                "allowed_after_decision_record": False,
                "reason": "Remote training still requires approved preflight, packet safety, formal manifest, and pullback protocol.",
            },
            {
                "action": "paper_formal_result_claim",
                "allowed_after_decision_record": False,
                "reason": "A decision record is not a PPO checkpoint, evaluation CSV, H02 acceptance, or paper-result input.",
            },
        ],
    }


def _conditional_actions(
    config: F026DecisionRecordConfig,
    *,
    packet: dict[str, Any],
    observed_preflight: dict[str, Any],
) -> dict[str, Any]:
    output_dir = "0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_approved_remote_v1"
    preflight_argv = [
        "python",
        "-m",
        "forest_n3p.scripts.preflight_rl_rs_gate3_formal_trial",
        "--output-dir",
        output_dir,
        "--manifest-out",
        f"{output_dir}/gate3_preflight_manifest.json",
        "--warm-start-decision",
        "approved_obstacle_summary",
        "--bc-checkpoint",
        str(config.bc_checkpoint),
        "--device",
        "cuda",
        "--allow-duplicate-openmp",
        "--allow-existing-output-dir",
    ]
    next_actions = packet.get("next_actions") if isinstance(packet.get("next_actions"), dict) else {}
    approved = next_actions.get("if_approved_obstacle_summary") if isinstance(next_actions.get("if_approved_obstacle_summary"), dict) else {}
    rejected = next_actions.get("if_rejected_obstacle_summary") if isinstance(next_actions.get("if_rejected_obstacle_summary"), dict) else {}
    return {
        "if_pending": {
            "allowed_now": False,
            "reason": "Dr Sun has not approved or rejected F02.6.",
            "observed_remote_preflight_status": observed_preflight["preflight_status"],
        },
        "if_approved_obstacle_summary": {
            "host": "gpu3070ti-relay",
            "preflight_command": _join_command(preflight_argv),
            "runner_command_after_ready_preflight": approved.get("runner_command"),
            "audit_command_after_ready_preflight": approved.get("audit_command"),
            "runs_training": False,
        },
        "if_rejected_obstacle_summary": {
            "host": "gpu3070ti-relay",
            "next_protocol": rejected.get(
                "next_protocol",
                "run a stronger/full patch-CNN warm-start protocol before any warm-start PPO formal trial",
            ),
            "runs_training": False,
        },
    }


def _markdown(record: dict[str, Any]) -> str:
    lines = [
        "# Module2 F02.6 Decision Record",
        "",
        f"- status: `{record['status']}`",
        f"- requested decision: `{record['requested_decision']}`",
        f"- effective warm-start decision: `{record['effective_warm_start_decision']}`",
        f"- decider: `{record['decider']}`",
        f"- decision note audit: `{record['decision_note_audit']}`",
        f"- remote training allowed: `{record['remote_training_allowed']}`",
        f"- remote preflight allowed now: `{record['remote_preflight_allowed_now']}`",
	        f"- remote training allowed now: `{record['remote_training_allowed_now']}`",
	        f"- local training allowed: `{record['local_training_allowed']}`",
	        f"- formal claim allowed: `{record['formal_claim_allowed']}`",
	        f"- paper result material allowed now: `{record['paper_result_material_allowed_now']}`",
	        f"- decision_record_is_not_training_authorization: `{record['decision_record_is_not_training_authorization']}`",
	        f"- decision_record_is_not_paper_result_material: `{record['decision_record_is_not_paper_result_material']}`",
	        f"- next remote preflight status: `{record['next_remote_preflight_status']}`",
	        "",
	        "## Blockers",
    ]
    if record["blockers"]:
        lines.extend(f"- `{blocker}`" for blocker in record["blockers"])
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Packet",
            f"- path: `{record['packet']['path']}`",
            f"- status: `{record['packet']['status']}`",
	            f"- recommendation: `{record['packet']['recommendation']}`",
	            "",
	            "## Current Authorization Boundary",
	            f"- authorization_status: `{record['current_authorization']['authorization_status']}`",
	            f"- current_allowed_action_ids: `{', '.join(record['current_authorization']['current_allowed_action_ids'])}`",
	            f"- current_blocked_action_ids: `{', '.join(record['current_authorization']['current_blocked_action_ids'])}`",
	            f"- post_decision_routes_are_current_authorization: `{record['current_authorization']['post_decision_routes_are_current_authorization']}`",
	            f"- remote_preflight_allowed_now: `{record['current_authorization']['remote_preflight_allowed_now']}`",
	            f"- remote_training_allowed_now: `{record['current_authorization']['remote_training_allowed_now']}`",
	            f"- formal_claim_allowed_now: `{record['current_authorization']['formal_claim_allowed_now']}`",
	            "",
	            "## Post-Decision Non-Authorization Invariants",
	            f"- formal_training_still_requires: `{', '.join(record['post_decision_non_authorization_invariants']['formal_training_still_requires'])}`",
	            f"- blocked_after_decision_record_count: `{len(record['post_decision_non_authorization_invariants']['blocked_after_decision_record'])}`",
	            "",
	            "## Remote Preflight Intent",
	            f"- host: `{record['conditional_actions']['if_approved_obstacle_summary']['host']}`",
	            f"- observed pending preflight: `{record['remote_preflight_observed']['preflight_status']}`",
            "",
            "```bash",
            record["conditional_actions"]["if_approved_obstacle_summary"]["preflight_command"],
            "```",
            "",
            "## Claim Boundaries",
        ]
    )
    lines.extend(f"- {boundary}" for boundary in record["claim_boundaries"])
    return "\n".join(lines) + "\n"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _join_command(argv: Sequence[str]) -> str:
    return " ".join(shlex.quote(str(part)) for part in argv)


def _source_head() -> str:
    return module2_source_head()


if __name__ == "__main__":
    raise SystemExit(main())
