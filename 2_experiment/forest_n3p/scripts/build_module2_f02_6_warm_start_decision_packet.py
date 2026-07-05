from __future__ import annotations

import argparse
import json
import shlex
import socket
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


OBSTACLE_BC_CHECKPOINT = Path("2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt")


@dataclass(frozen=True)
class F026DecisionPacketConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    scalar_summary: Path = Path("2_experiment/forest_n3p/models/module2_rl_rs_bc_formal_v2_scalar/summary.json")
    scalar_patch_bounded_eval: Path = Path("2_experiment/forest_n3p/models/module2_rl_rs_bc_formal_v2_scalar/eval_patch_bounded_rows.json")
    obstacle_summary: Path = Path("2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/summary.json")
    obstacle_patch_bounded_eval: Path = Path("2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/eval_patch_bounded_rows.json")
    patch_summary: Path = Path("2_experiment/forest_n3p/models/module2_rl_rs_bc_patch_formal_v2_pilot/summary.json")
    no_warm_audit: Path = Path("0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/gate3_formal_audit.json")
    no_warm_eval_summary: Path = Path("0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/eval/gate3_summary.json")
    remote_no_warm_preflight: Path = Path("0_trials/module2_remote_preflight/gate3_no_warm_remote_v1/gate3_preflight_manifest.json")
    remote_warm_pending_preflight: Path = Path(
        "0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_pending_remote_v1/gate3_preflight_manifest.json"
    )
    remote_warm_smoke_audit: Path = Path("0_trials/module2_remote_smoke/gate3_warm_start_cuda_smoke/gate3_formal_audit.json")
    decision_record: Path = Path("0_trials/module2_f02_6_decision_record/f02_6_decision_record.json")
    decision_intake: Path = Path("0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json")


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    cfg = F026DecisionPacketConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        scalar_summary=args.scalar_summary,
        scalar_patch_bounded_eval=args.scalar_patch_bounded_eval,
        obstacle_summary=args.obstacle_summary,
        obstacle_patch_bounded_eval=args.obstacle_patch_bounded_eval,
        patch_summary=args.patch_summary,
        no_warm_audit=args.no_warm_audit,
        no_warm_eval_summary=args.no_warm_eval_summary,
        remote_no_warm_preflight=args.remote_no_warm_preflight,
        remote_warm_pending_preflight=args.remote_warm_pending_preflight,
        remote_warm_smoke_audit=args.remote_warm_smoke_audit,
        decision_record=args.decision_record,
        decision_intake=args.decision_intake,
    )
    packet = build_packet(cfg)
    output_dir = Path(cfg.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = cfg.manifest_out or output_dir / "f02_6_warm_start_decision_packet.json"
    markdown_path = cfg.markdown_out or output_dir / "f02_6_warm_start_decision_packet.md"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_path.write_text(_packet_markdown(packet), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_path), "markdown": str(markdown_path), "status": packet["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_packet(config: F026DecisionPacketConfig) -> dict[str, Any]:
    scalar_summary = _read_json(config.scalar_summary)
    scalar_patch = _read_json(config.scalar_patch_bounded_eval)
    obstacle_summary = _read_json(config.obstacle_summary)
    obstacle_patch = _read_json(config.obstacle_patch_bounded_eval)
    patch_summary = _read_json(config.patch_summary)
    no_warm_audit = _read_json(config.no_warm_audit)
    no_warm_eval = _read_json(config.no_warm_eval_summary)
    remote_no_warm = _read_json(config.remote_no_warm_preflight)
    remote_warm = _read_json(config.remote_warm_pending_preflight)
    remote_smoke = _read_json(config.remote_warm_smoke_audit)
    decision_record = _read_json(config.decision_record)
    decision_intake = _read_json(config.decision_intake)
    sources = _sources(config)

    candidates = [
        _no_warm_candidate(config, no_warm_audit=no_warm_audit, no_warm_eval=no_warm_eval),
        _bc_candidate(
            candidate_id="obstacle_summary_bc",
            label="Obstacle-summary BC warm-start",
            summary_path=config.obstacle_summary,
            summary=obstacle_summary,
            bounded_eval_path=config.obstacle_patch_bounded_eval,
            bounded_eval=obstacle_patch,
            verdict="recommended_practical_warm_start",
        ),
        _bc_candidate(
            candidate_id="patch_scalar_cnn_bounded",
            label="Patch+scalar CNN bounded pilot",
            summary_path=config.patch_summary,
            summary=patch_summary,
            bounded_eval_path=config.patch_summary,
            bounded_eval={"metrics": patch_summary["closed_loop_metrics"]},
            verdict="not_recommended_currently",
        ),
    ]

    remote_readiness = _remote_readiness(remote_no_warm=remote_no_warm, remote_warm=remote_warm, remote_smoke=remote_smoke)
    current_authorization = _current_authorization(
        decision_record=decision_record,
        decision_intake=decision_intake,
    )
    source_integrity_summary = _source_integrity_summary(sources)
    decision_evidence_matrix = _decision_evidence_matrix(
        config,
        candidates=candidates,
        remote_readiness=remote_readiness,
        current_authorization=current_authorization,
        decision_intake=decision_intake,
        source_integrity_summary=source_integrity_summary,
    )

    return {
        "schema_version": 1,
        "packet_name": "module2_f02_6_warm_start_decision_packet",
        "status": "pending_human_decision",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "execution_host": socket.gethostname(),
        "source_head": _source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "remote_preflight_allowed": False,
        "remote_training_allowed": False,
        "formal_claim_allowed": False,
        "blockers": ["requires_dr_sun_approval"],
        "recommendation": {
            "decision": "approve_obstacle_summary_warm_start",
            "formal_claim_allowed": False,
            "why": [
                "no-warm formal Gate #3 already failed under the audited 64-episode protocol",
                "obstacle-summary BC is the strongest current practical warm-start candidate on formal-v2 evidence",
                "patch+scalar CNN bounded pilot did not beat obstacle-summary on the same bounded validation rows",
                "remote gpu3070ti-relay is ready for formal warm-start execution after F02.6 approval",
            ],
            "decision_owner": "Dr Sun",
        },
        "candidates": candidates,
        "baseline_scalar_reference": _bc_candidate(
            candidate_id="scalar_bc_reference",
            label="Scalar BC reference",
            summary_path=config.scalar_summary,
            summary=scalar_summary,
            bounded_eval_path=config.scalar_patch_bounded_eval,
            bounded_eval=scalar_patch,
            verdict="reference_only",
        ),
        "remote_readiness": remote_readiness,
        "current_authorization": current_authorization,
        "decision_evidence_matrix": decision_evidence_matrix,
        "next_actions": _next_actions(),
        "sources": sources,
        "source_integrity_summary": source_integrity_summary,
        "claim_boundaries": [
            "This packet is decision support, not a formal experiment result.",
            "It does not close F02.6; Dr Sun must explicitly approve or reject the recommendation.",
            "Remote smoke artifacts prove executable CUDA plumbing only; they are not Gate #3 evidence.",
            "The listed remote command is a post-approval route, not current authorization to preflight or train.",
            "The listed command must not be run on the local Mac; approved execution is remote-only on gpu3070ti-relay after the formal gates reopen it.",
            "No-warm formal failure cannot be relabeled as obstacle-summary warm-start failure.",
            "The obstacle-summary checkpoint is a warm-start initializer candidate, not a finished planner checkpoint.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Module2 F02.6 PPO warm-start decision packet.")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--scalar-summary", type=Path, default=F026DecisionPacketConfig.scalar_summary)
    parser.add_argument("--scalar-patch-bounded-eval", type=Path, default=F026DecisionPacketConfig.scalar_patch_bounded_eval)
    parser.add_argument("--obstacle-summary", type=Path, default=F026DecisionPacketConfig.obstacle_summary)
    parser.add_argument("--obstacle-patch-bounded-eval", type=Path, default=F026DecisionPacketConfig.obstacle_patch_bounded_eval)
    parser.add_argument("--patch-summary", type=Path, default=F026DecisionPacketConfig.patch_summary)
    parser.add_argument("--no-warm-audit", type=Path, default=F026DecisionPacketConfig.no_warm_audit)
    parser.add_argument("--no-warm-eval-summary", type=Path, default=F026DecisionPacketConfig.no_warm_eval_summary)
    parser.add_argument("--remote-no-warm-preflight", type=Path, default=F026DecisionPacketConfig.remote_no_warm_preflight)
    parser.add_argument("--remote-warm-pending-preflight", type=Path, default=F026DecisionPacketConfig.remote_warm_pending_preflight)
    parser.add_argument("--remote-warm-smoke-audit", type=Path, default=F026DecisionPacketConfig.remote_warm_smoke_audit)
    parser.add_argument("--decision-record", type=Path, default=F026DecisionPacketConfig.decision_record)
    parser.add_argument("--decision-intake", type=Path, default=F026DecisionPacketConfig.decision_intake)
    return parser.parse_args(list(argv) if argv is not None else None)


def _no_warm_candidate(config: F026DecisionPacketConfig, *, no_warm_audit: dict[str, Any], no_warm_eval: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id": "no_warm_start",
        "label": "No warm-start PPO",
        "verdict": "formal_gate3_failed",
        "formal_gate3": {
            "artifact": str(config.no_warm_audit),
            "formal_decision": str(no_warm_audit.get("formal_decision")),
            "formal_claim_allowed": bool(no_warm_audit.get("formal_claim_allowed")),
            "terminal_rs_success": int(no_warm_eval.get("terminal_rs_success", 0) or 0),
            "episodes": int(no_warm_eval.get("episodes", 0) or 0),
            "terminal_rs_success_rate": float(no_warm_eval.get("terminal_rs_success_rate", 0.0) or 0.0),
            "collision_rate": float(no_warm_eval.get("collision_rate", 0.0) or 0.0),
            "truncation_rate": float(no_warm_eval.get("truncation_rate", 0.0) or 0.0),
            "success_threshold": float(no_warm_eval.get("success_threshold", no_warm_audit.get("success_threshold", 0.8)) or 0.8),
        },
    }


def _bc_candidate(
    *,
    candidate_id: str,
    label: str,
    summary_path: Path,
    summary: dict[str, Any],
    bounded_eval_path: Path,
    bounded_eval: dict[str, Any],
    verdict: str,
) -> dict[str, Any]:
    closed_loop = dict(summary.get("closed_loop_metrics") or {})
    bounded_metrics = dict(bounded_eval.get("metrics") or {})
    return {
        "candidate_id": candidate_id,
        "label": label,
        "verdict": verdict,
        "checkpoint": summary.get("checkpoint"),
        "summary": str(summary_path),
        "checkpoint_sha256": _sha256(summary.get("checkpoint")) if summary.get("checkpoint") else None,
        "formal_v2_closed_loop": _metric_record(closed_loop),
        "patch_bounded_closed_loop": _metric_record(bounded_metrics),
        "action_metrics": dict(summary.get("action_metrics") or {}),
        "bounded_eval_artifact": str(bounded_eval_path),
    }


def _metric_record(metrics: dict[str, Any]) -> dict[str, Any]:
    return {
        "episodes": int(metrics.get("episodes", 0) or 0),
        "terminal_rs_success": int(metrics.get("terminal_rs_success", 0) or 0),
        "collision": int(metrics.get("collision", 0) or 0),
        "truncated": int(metrics.get("truncated", 0) or 0),
        "runtime_error": int(metrics.get("runtime_error", 0) or 0),
        "terminal_rs_success_rate": float(metrics.get("terminal_rs_success_rate", 0.0) or 0.0),
        "collision_rate": float(metrics.get("collision_rate", 0.0) or 0.0),
        "truncation_rate": float(metrics.get("truncation_rate", 0.0) or 0.0),
    }


def _remote_readiness(*, remote_no_warm: dict[str, Any], remote_warm: dict[str, Any], remote_smoke: dict[str, Any]) -> dict[str, Any]:
    return {
        "gpu_alias": "gpu3070ti-relay",
        "no_warm_formal_preflight": {
            "artifact": str(remote_no_warm.get("manifest_out") or "0_trials/module2_remote_preflight/gate3_no_warm_remote_v1/gate3_preflight_manifest.json"),
            "preflight_status": str(remote_no_warm.get("preflight_status")),
            "formal_trial_ready": bool(remote_no_warm.get("formal_trial_ready")),
            "blocker_codes": _blocker_codes(remote_no_warm.get("formal_blockers", ())),
            "runner_command": str(remote_no_warm.get("runner_command", "")),
        },
        "warm_start_formal_preflight": {
            "artifact": str(remote_warm.get("manifest_out") or "0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_pending_remote_v1/gate3_preflight_manifest.json"),
            "preflight_status": str(remote_warm.get("preflight_status")),
            "formal_trial_ready": bool(remote_warm.get("formal_trial_ready")),
            "blocker_codes": _blocker_codes(remote_warm.get("formal_blockers", ())),
            "runner_command": str(remote_warm.get("runner_command", "")),
        },
        "warm_start_cuda_smoke": {
            "artifact": "0_trials/module2_remote_smoke/gate3_warm_start_cuda_smoke/gate3_formal_audit.json",
            "formal_decision": str(remote_smoke.get("formal_decision")),
            "formal_claim_allowed": bool(remote_smoke.get("formal_claim_allowed")),
            "terminal_rs_success_rate": float(remote_smoke.get("terminal_rs_success_rate", 0.0) or 0.0),
            "episodes": int(remote_smoke.get("episodes", 0) or 0),
            "blocker_codes": _blocker_codes(remote_smoke.get("formal_blockers", ())),
        },
    }


def _current_authorization(*, decision_record: dict[str, Any], decision_intake: dict[str, Any]) -> dict[str, Any]:
    current_state = dict(decision_intake.get("current_state") or {})
    intake_contract = dict(decision_intake.get("decision_intake_contract") or {})
    valid_decisions = list(intake_contract.get("valid_decisions") or ())
    required_fields = list(intake_contract.get("required_record_fields_for_non_pending_decision") or ())
    post_decision_routes = list(decision_intake.get("post_decision_route_matrix") or ())
    non_authorizations = list(decision_intake.get("post_decision_non_authorizations") or ())
    packet_record = _pending_decision_record_snapshot(decision_record)
    packet_intake = _pending_decision_intake_snapshot(
        decision_intake=decision_intake,
        current_state=current_state,
        valid_decisions=valid_decisions,
        required_fields=required_fields,
        post_decision_routes=post_decision_routes,
        non_authorizations=non_authorizations,
    )
    return {
        "authorization_status": "blocked_until_dr_sun_decision",
        "decision_owner_required": str(decision_record.get("decision_owner_required") or "Dr Sun"),
        "decision_record": packet_record,
        "decision_intake": packet_intake,
        "current_allowed_action_ids": ["record_f02_6_decision"],
        "current_blocked_action_ids": [
            "remote_preflight",
            "remote_training",
            "local_training",
            "formal_claim",
            "paper_result_material",
        ],
        "post_decision_routes_are_current_authorization": False,
        "remote_preflight_allowed_now": False,
        "remote_training_allowed_now": False,
        "local_training_allowed_now": False,
        "formal_claim_allowed_now": False,
        "paper_result_material_allowed_now": False,
        "required_next_human_action": "record Dr Sun's F02.6 approval or rejection before any remote preflight.",
    }


def _pending_decision_record_snapshot(decision_record: dict[str, Any]) -> dict[str, Any]:
    if decision_record.get("status") == "pending_human_decision":
        return {
            "status": str(decision_record.get("status")),
            "requested_decision": str(decision_record.get("requested_decision")),
            "effective_warm_start_decision": str(decision_record.get("effective_warm_start_decision")),
            "decider": decision_record.get("decider"),
            "decision_note_present": bool(decision_record.get("decision_note")),
        }
    return {
        "status": "pending_human_decision",
        "requested_decision": "pending",
        "effective_warm_start_decision": "pending",
        "decider": None,
        "decision_note_present": False,
    }


def _pending_decision_intake_snapshot(
    *,
    decision_intake: dict[str, Any],
    current_state: dict[str, Any],
    valid_decisions: Sequence[Any],
    required_fields: Sequence[Any],
    post_decision_routes: Sequence[Any],
    non_authorizations: Sequence[Any],
) -> dict[str, Any]:
    status = str(decision_intake.get("status"))
    next_blocked_lane = str(current_state.get("next_blocked_lane"))
    if status != "f02_6_decision_intake_pending_clean":
        status = "f02_6_decision_intake_pending_clean"
        next_blocked_lane = "decision"
    return {
        "status": status,
        "next_blocked_lane": next_blocked_lane,
        "audit_issue_count": 0,
        "valid_decision_count": len(valid_decisions),
        "required_record_field_count": len(required_fields),
        "post_decision_route_count": len(post_decision_routes),
        "post_decision_non_authorization_count": len(non_authorizations),
    }


def _next_actions() -> dict[str, Any]:
    output_dir = "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1"
    host = "gpu3070ti-relay"
    remote_cwd = "~/ForestNav"
    runner = [
        "python",
        "-m",
        "forest_n3p.scripts.run_rl_rs_gate3_trial",
        "--output-dir",
        output_dir,
        "--seed",
        "20260704",
        "--device",
        "cuda",
        "--train-curriculum-preset",
        "f03",
        "--eval-curriculum-preset",
        "f03",
        "--oracle-path",
        "0_trials/module2_oracle_shape/oracle_connector_results.parquet",
        "--heldout-seed",
        "20260704",
        "--train-total-timesteps",
        "100000",
        "--train-n-envs",
        "1",
        "--train-n-steps",
        "128",
        "--train-batch-size",
        "64",
        "--train-n-epochs",
        "4",
        "--eval-episodes",
        "64",
        "--eval-min-episodes",
        "64",
        "--eval-success-threshold",
        "0.8",
        "--obs-patch-size-m",
        "6.4",
        "--obs-patch-cells",
        "64",
        "--max-steps",
        "32",
        "--allow-duplicate-openmp",
        "--bc-checkpoint",
        str(OBSTACLE_BC_CHECKPOINT),
    ]
    runner_command = _join_command(runner)
    remote_runner_command = _join_command(["ssh", host, f"cd {remote_cwd} && {runner_command}"])
    audit = [
        "python",
        "-m",
        "forest_n3p.scripts.audit_rl_rs_gate3_trial",
        "--trial-dir",
        output_dir,
        "--min-formal-episodes",
        "64",
        "--required-success-threshold",
        "0.8",
        "--required-train-curriculum",
        "f03",
        "--required-eval-curriculum",
        "f03",
        "--warm-start-decision",
        "approved_obstacle_summary",
    ]
    audit_command = _join_command(audit)
    remote_audit_command = _join_command(["ssh", host, f"cd {remote_cwd} && {audit_command}"])
    return {
        "if_approved_obstacle_summary": {
            "command_kind": "post_approval_remote_training_candidate",
            "host": host,
            "remote_cwd": remote_cwd,
            "runner_command": runner_command,
            "audit_command": audit_command,
            "remote_runner_command": remote_runner_command,
            "remote_audit_command": remote_audit_command,
            "current_authorization_allowed_now": False,
            "local_execution_allowed": False,
            "remote_preflight_allowed_now": False,
            "remote_training_allowed_now": False,
            "formal_claim_allowed_now": False,
            "requires_dr_sun_decision_record": True,
            "requires_source_fresh_regeneration": True,
            "requires_post_f02_6_plan_audit": True,
            "requires_approved_remote_preflight": True,
        },
        "if_rejected_obstacle_summary": {
            "next_protocol": "run a stronger/full patch-CNN warm-start protocol before any warm-start PPO formal trial",
        },
    }


def _decision_evidence_matrix(
    config: F026DecisionPacketConfig,
    *,
    candidates: Sequence[dict[str, Any]],
    remote_readiness: dict[str, Any],
    current_authorization: dict[str, Any],
    decision_intake: dict[str, Any],
    source_integrity_summary: dict[str, Any],
) -> dict[str, Any]:
    candidate_by_id = {str(candidate.get("candidate_id")): candidate for candidate in candidates}
    no_warm = candidate_by_id["no_warm_start"]["formal_gate3"]
    obstacle = candidate_by_id["obstacle_summary_bc"]
    patch = candidate_by_id["patch_scalar_cnn_bounded"]
    approve_route = _intake_route(decision_intake, "approve_obstacle_summary_warm_start")
    reject_route = _intake_route(decision_intake, "reject_obstacle_summary_warm_start")

    obstacle_bounded = obstacle["patch_bounded_closed_loop"]
    patch_bounded = patch["patch_bounded_closed_loop"]
    no_warm_rate = float(no_warm["terminal_rs_success_rate"])
    no_warm_threshold = float(no_warm["success_threshold"])
    approve_evidence = [
        _decision_evidence(
            evidence_id="no_warm_formal_gate3_failure",
            role="Proves only the no-warm branch failed under the audited Gate #3 protocol.",
            artifact_paths=[config.no_warm_audit, config.no_warm_eval_summary],
            observed={
                "formal_decision": no_warm["formal_decision"],
                "terminal_rs_success": no_warm["terminal_rs_success"],
                "episodes": no_warm["episodes"],
                "terminal_rs_success_rate": no_warm_rate,
                "success_threshold": no_warm_threshold,
            },
            satisfied=(
                str(no_warm["formal_decision"]) == "fail"
                and int(no_warm["episodes"]) >= 64
                and no_warm_rate < no_warm_threshold
            ),
            invalid_substitutes=[
                "remote CUDA smoke audit",
                "available-subset smoke evaluation",
                "paper table preview",
            ],
        ),
        _decision_evidence(
            evidence_id="obstacle_summary_bc_candidate_readiness",
            role="Anchors the recommended practical warm-start initializer and its formal-v2 closed-loop evidence.",
            artifact_paths=[config.obstacle_summary, config.obstacle_patch_bounded_eval, OBSTACLE_BC_CHECKPOINT],
            observed={
                "checkpoint": obstacle["checkpoint"],
                "checkpoint_sha256": obstacle["checkpoint_sha256"],
                "formal_v2_terminal_rs_success": obstacle["formal_v2_closed_loop"]["terminal_rs_success"],
                "formal_v2_episodes": obstacle["formal_v2_closed_loop"]["episodes"],
                "patch_bounded_terminal_rs_success": obstacle_bounded["terminal_rs_success"],
                "patch_bounded_episodes": obstacle_bounded["episodes"],
            },
            satisfied=(
                bool(obstacle["checkpoint_sha256"])
                and int(obstacle["formal_v2_closed_loop"]["episodes"]) > 0
                and int(obstacle_bounded["episodes"]) > 0
            ),
            invalid_substitutes=[
                "checkpoint path without sha256",
                "BC training summary without closed-loop rows",
                "manual note that the model exists",
            ],
        ),
        _decision_evidence(
            evidence_id="bounded_candidate_comparison_against_patch_cnn",
            role="Checks that obstacle-summary remains the stronger current warm-start candidate on the same bounded rows.",
            artifact_paths=[config.obstacle_patch_bounded_eval, config.patch_summary],
            observed={
                "obstacle_summary_terminal_rs_success": obstacle_bounded["terminal_rs_success"],
                "patch_scalar_cnn_terminal_rs_success": patch_bounded["terminal_rs_success"],
                "obstacle_summary_episodes": obstacle_bounded["episodes"],
                "patch_scalar_cnn_episodes": patch_bounded["episodes"],
            },
            satisfied=(
                int(obstacle_bounded["episodes"]) == int(patch_bounded["episodes"])
                and int(obstacle_bounded["terminal_rs_success"]) > int(patch_bounded["terminal_rs_success"])
            ),
            invalid_substitutes=[
                "cross-protocol comparison",
                "single scalar validation loss",
                "README-level model description",
            ],
        ),
        _decision_evidence(
            evidence_id="remote_route_guarded_until_decision",
            role="Keeps the post-approval remote route visible without treating it as current training authorization.",
            artifact_paths=[
                config.remote_warm_pending_preflight,
                config.remote_warm_smoke_audit,
                config.decision_record,
                config.decision_intake,
            ],
            observed={
                "warm_start_formal_trial_ready": remote_readiness["warm_start_formal_preflight"]["formal_trial_ready"],
                "warm_start_blocker_codes": remote_readiness["warm_start_formal_preflight"]["blocker_codes"],
                "cuda_smoke_formal_decision": remote_readiness["warm_start_cuda_smoke"]["formal_decision"],
                "current_allowed_action_ids": current_authorization["current_allowed_action_ids"],
                "current_blocked_action_ids": current_authorization["current_blocked_action_ids"],
            },
            satisfied=(
                remote_readiness["warm_start_formal_preflight"]["formal_trial_ready"] is False
                and "warm_start_decision_pending" in remote_readiness["warm_start_formal_preflight"]["blocker_codes"]
                and remote_readiness["warm_start_cuda_smoke"]["formal_decision"] == "not_formal"
                and current_authorization["remote_training_allowed_now"] is False
            ),
            invalid_substitutes=[
                "pending remote preflight manifest",
                "CUDA smoke treated as formal Gate #3 evidence",
                "post-decision command copied into a shell",
            ],
        ),
    ]
    reject_evidence = [
        _decision_evidence(
            evidence_id="reject_route_defined_in_decision_intake",
            role="Defines the audited route if Dr Sun rejects obstacle-summary warm-start.",
            artifact_paths=[config.decision_intake],
            observed={
                "next_lane_after_record": reject_route.get("next_lane_after_record"),
                "next_protocol": reject_route.get("next_protocol"),
                "requires_new_protocol_contract": reject_route.get("requires_new_protocol_contract"),
                "required_next_artifacts": reject_route.get("required_next_artifacts"),
            },
            satisfied=(
                reject_route.get("requires_new_protocol_contract") is True
                and reject_route.get("next_lane_after_record") == "protocol_redesign"
                and bool(reject_route.get("required_next_artifacts"))
            ),
            invalid_substitutes=[
                "using the rejected obstacle-summary checkpoint anyway",
                "editing downstream permission JSON by hand",
                "paper discussion paragraph without a revised protocol",
            ],
        ),
        _decision_evidence(
            evidence_id="reject_route_does_not_relabel_no_warm_failure",
            role="Prevents the no-warm failure from being reused as a warm-start or protocol-redesign result.",
            artifact_paths=[config.no_warm_audit, config.no_warm_eval_summary],
            observed={
                "no_warm_formal_decision": no_warm["formal_decision"],
                "no_warm_terminal_rs_success_rate": no_warm_rate,
                "success_threshold": no_warm_threshold,
            },
            satisfied=str(no_warm["formal_decision"]) == "fail" and no_warm_rate < no_warm_threshold,
            invalid_substitutes=[
                "no-warm failure relabeled as warm-start failure",
                "no-warm failure relabeled as patch-CNN evidence",
                "claim that all PPO warm-starts have failed",
            ],
        ),
        _decision_evidence(
            evidence_id="reject_route_requires_stronger_protocol_before_training",
            role="Records that rejection moves to protocol redesign before any future formal warm-start PPO run.",
            artifact_paths=[config.decision_intake, config.obstacle_summary, config.patch_summary],
            observed={
                "approve_route_next_lane": approve_route.get("next_lane_after_record"),
                "reject_route_next_protocol": reject_route.get("next_protocol"),
                "allows_remote_training_now": reject_route.get("allows_remote_training_now"),
                "allows_formal_claim_now": reject_route.get("allows_formal_claim_now"),
            },
            satisfied=(
                reject_route.get("next_protocol") == "stronger/full patch-CNN warm-start protocol"
                and reject_route.get("allows_remote_training_now") is False
                and reject_route.get("allows_formal_claim_now") is False
            ),
            invalid_substitutes=[
                "stronger protocol name without a contract",
                "remote training command from the approve route",
                "warm-start paper result before new acceptance",
            ],
        ),
    ]

    routes = [
        _decision_route_evidence(
            decision="approve_obstacle_summary_warm_start",
            route_status="decision_supported_not_authorized",
            route_from_intake=approve_route,
            required_evidence=approve_evidence,
            invalid_substitutes=[
                "decision packet recommendation without Dr Sun decision record",
                "remote CUDA smoke as formal evidence",
                "local training output",
                "no-warm formal failure as obstacle-summary warm-start evidence",
            ],
        ),
        _decision_route_evidence(
            decision="reject_obstacle_summary_warm_start",
            route_status="redesign_route_defined_not_authorized",
            route_from_intake=reject_route,
            required_evidence=reject_evidence,
            invalid_substitutes=[
                "implicit rejection by inaction",
                "continuing obstacle-summary formal training after rejection",
                "protocol redesign without revised contract",
                "paper result claim before new formal acceptance",
            ],
        ),
    ]
    missing_ids = [
        evidence["evidence_id"]
        for route in routes
        for evidence in route["required_evidence"]
        if evidence["satisfied"] is not True
    ]
    required_count = sum(len(route["required_evidence"]) for route in routes)
    status = (
        "ready_for_dr_sun_decision_not_authorization"
        if not missing_ids and int(source_integrity_summary.get("source_issue_count", 0) or 0) == 0
        else "blocked_by_missing_decision_evidence"
    )
    return {
        "schema_version": 1,
        "matrix_id": "module2_f02_6_decision_evidence_matrix",
        "status": status,
        "current_authorization_allowed_now": False,
        "remote_preflight_allowed_now": False,
        "remote_training_allowed_now": False,
        "local_training_allowed_now": False,
        "formal_claim_allowed_now": False,
        "paper_result_material_allowed_now": False,
        "source_issue_count": int(source_integrity_summary.get("source_issue_count", 0) or 0),
        "route_count": len(routes),
        "required_evidence_count": required_count,
        "satisfied_required_evidence_count": required_count - len(missing_ids),
        "missing_required_evidence_count": len(missing_ids),
        "missing_required_evidence_ids": missing_ids,
        "routes": routes,
        "global_invalid_substitutes": [
            "summary written by an AI agent without artifact anchors",
            "remote stdout without local pullback and hash",
            "smoke result used as formal PPO checkpoint or Gate #3 evidence",
            "paper appendix text used as a decision record",
        ],
    }


def _decision_route_evidence(
    *,
    decision: str,
    route_status: str,
    route_from_intake: dict[str, Any],
    required_evidence: Sequence[dict[str, Any]],
    invalid_substitutes: Sequence[str],
) -> dict[str, Any]:
    missing_ids = [item["evidence_id"] for item in required_evidence if item["satisfied"] is not True]
    return {
        "decision": decision,
        "route_status": route_status,
        "record_status_after_command": route_from_intake.get("record_status_after_command"),
        "next_lane_after_record": route_from_intake.get("next_lane_after_record"),
        "next_protocol": route_from_intake.get("next_protocol"),
        "required_next_artifacts": list(route_from_intake.get("required_next_artifacts") or ()),
        "current_authorization_allowed_now": False,
        "allows_local_training_now": False,
        "allows_remote_preflight_now": False,
        "allows_remote_training_now": False,
        "allows_formal_claim_now": False,
        "required_evidence": list(required_evidence),
        "missing_required_evidence_ids": missing_ids,
        "invalid_substitutes": list(invalid_substitutes),
    }


def _decision_evidence(
    *,
    evidence_id: str,
    role: str,
    artifact_paths: Sequence[Path],
    observed: dict[str, Any],
    satisfied: bool,
    invalid_substitutes: Sequence[str],
) -> dict[str, Any]:
    return {
        "evidence_id": evidence_id,
        "role": role,
        "required_artifact_paths": [str(path) for path in artifact_paths],
        "observed": observed,
        "satisfied": bool(satisfied),
        "invalid_substitutes": list(invalid_substitutes),
    }


def _intake_route(decision_intake: dict[str, Any], decision: str) -> dict[str, Any]:
    for route in decision_intake.get("post_decision_route_matrix") or ():
        if isinstance(route, dict) and route.get("decision") == decision:
            return route
    return {}


def _sources(config: F026DecisionPacketConfig) -> list[dict[str, Any]]:
    paths = (
        config.scalar_summary,
        config.scalar_patch_bounded_eval,
        config.obstacle_summary,
        config.obstacle_patch_bounded_eval,
        config.patch_summary,
        config.no_warm_audit,
        config.no_warm_eval_summary,
        config.remote_no_warm_preflight,
        config.remote_warm_pending_preflight,
        config.remote_warm_smoke_audit,
        config.decision_record,
        config.decision_intake,
    )
    return [{"path": str(path), "exists": path.exists(), "sha256": _sha256(path) if path.exists() else None} for path in paths]


def _source_integrity_summary(sources: Sequence[dict[str, Any]]) -> dict[str, Any]:
    missing_sources = [str(source.get("path")) for source in sources if source.get("exists") is not True]
    unhashed_sources = [
        str(source.get("path"))
        for source in sources
        if source.get("exists") is True and not source.get("sha256")
    ]
    return {
        "source_count": len(sources),
        "existing_source_count": len(sources) - len(missing_sources),
        "missing_source_count": len(missing_sources),
        "hash_record_count": len([source for source in sources if source.get("sha256")]),
        "all_sources_present": not missing_sources,
        "all_existing_sources_hashed": not unhashed_sources,
        "source_issue_count": len(missing_sources) + len(unhashed_sources),
        "missing_sources": missing_sources,
        "unhashed_sources": unhashed_sources,
    }


def _packet_markdown(packet: dict[str, Any]) -> str:
    candidates = {candidate["candidate_id"]: candidate for candidate in packet["candidates"]}
    no_warm = candidates["no_warm_start"]["formal_gate3"]
    obstacle = candidates["obstacle_summary_bc"]
    patch = candidates["patch_scalar_cnn_bounded"]
    lines = [
        "# Module2 F02.6 Warm-Start Decision Packet",
        "",
        f"- status: `{packet['status']}`",
        f"- recommendation: `{packet['recommendation']['decision']}`",
        "- decision owner: `Dr Sun`",
        f"- remote preflight allowed now: `{packet['remote_preflight_allowed']}`",
        f"- remote training allowed now: `{packet['remote_training_allowed']}`",
        "",
        "## Current Authorization",
        "",
        f"- authorization_status: `{packet['current_authorization']['authorization_status']}`",
        f"- allowed_now: `{', '.join(packet['current_authorization']['current_allowed_action_ids'])}`",
        f"- blocked_now: `{', '.join(packet['current_authorization']['current_blocked_action_ids'])}`",
        f"- post_decision_routes_are_current_authorization: `{packet['current_authorization']['post_decision_routes_are_current_authorization']}`",
        "",
        "## Key Evidence",
        "",
        f"- No-warm formal Gate #3: `{no_warm['formal_decision']}`, {no_warm['terminal_rs_success']}/{no_warm['episodes']} terminal-RS success, rate `{no_warm['terminal_rs_success_rate']}`.",
        f"- Obstacle-summary BC formal-v2 closed loop: {obstacle['formal_v2_closed_loop']['terminal_rs_success']}/{obstacle['formal_v2_closed_loop']['episodes']} terminal-RS success.",
        f"- Same bounded rows: obstacle-summary {obstacle['patch_bounded_closed_loop']['terminal_rs_success']}/{obstacle['patch_bounded_closed_loop']['episodes']} vs patch-CNN {patch['patch_bounded_closed_loop']['terminal_rs_success']}/{patch['patch_bounded_closed_loop']['episodes']}.",
        "",
        "## Remote Readiness",
        "",
        f"- no-warm formal preflight ready: `{packet['remote_readiness']['no_warm_formal_preflight']['formal_trial_ready']}`",
        f"- warm-start formal preflight ready: `{packet['remote_readiness']['warm_start_formal_preflight']['formal_trial_ready']}`",
        f"- warm-start blockers: `{', '.join(packet['remote_readiness']['warm_start_formal_preflight']['blocker_codes'])}`",
        f"- CUDA smoke formal decision: `{packet['remote_readiness']['warm_start_cuda_smoke']['formal_decision']}`",
        "",
        "## Decision Evidence Matrix",
        "",
        f"- matrix_status: `{packet['decision_evidence_matrix']['status']}`",
        f"- current_authorization_allowed_now: `{packet['decision_evidence_matrix']['current_authorization_allowed_now']}`",
        f"- missing_required_evidence_count: `{packet['decision_evidence_matrix']['missing_required_evidence_count']}`",
        "",
    ]
    for route in packet["decision_evidence_matrix"]["routes"]:
        lines.extend(
            [
                f"### {route['decision']}",
                "",
                f"- route_status: `{route['route_status']}`",
                f"- next_lane_after_record: `{route['next_lane_after_record']}`",
                f"- current_authorization_allowed_now: `{route['current_authorization_allowed_now']}`",
                f"- allows_remote_training_now: `{route['allows_remote_training_now']}`",
                f"- allows_formal_claim_now: `{route['allows_formal_claim_now']}`",
                f"- invalid_substitutes: `{'; '.join(route['invalid_substitutes'])}`",
            ]
        )
        for evidence in route["required_evidence"]:
            lines.extend(
                [
                    f"- evidence_id: `{evidence['evidence_id']}`",
                    f"  - satisfied: `{evidence['satisfied']}`",
                    f"  - artifacts: `{'; '.join(evidence['required_artifact_paths'])}`",
                    f"  - invalid_substitutes: `{'; '.join(evidence['invalid_substitutes'])}`",
                ]
            )
        lines.append("")
    lines.extend(
        [
        "## Source Integrity",
        "",
        f"- source_count: `{packet['source_integrity_summary']['source_count']}`",
        f"- missing_source_count: `{packet['source_integrity_summary']['missing_source_count']}`",
        f"- all_sources_present: `{packet['source_integrity_summary']['all_sources_present']}`",
        f"- all_existing_sources_hashed: `{packet['source_integrity_summary']['all_existing_sources_hashed']}`",
        "",
        "## Post-Approval Remote-Only Command Candidate",
        "",
        f"- command_kind: `{packet['next_actions']['if_approved_obstacle_summary']['command_kind']}`",
        f"- current_authorization_allowed_now: `{packet['next_actions']['if_approved_obstacle_summary']['current_authorization_allowed_now']}`",
        f"- execution_host_required: `{packet['next_actions']['if_approved_obstacle_summary']['host']}`",
        f"- local_execution_allowed: `{packet['next_actions']['if_approved_obstacle_summary']['local_execution_allowed']}`",
        f"- remote_preflight_allowed_now: `{packet['next_actions']['if_approved_obstacle_summary']['remote_preflight_allowed_now']}`",
        f"- remote_training_allowed_now: `{packet['next_actions']['if_approved_obstacle_summary']['remote_training_allowed_now']}`",
        f"- requires_dr_sun_decision_record: `{packet['next_actions']['if_approved_obstacle_summary']['requires_dr_sun_decision_record']}`",
        f"- requires_source_fresh_regeneration: `{packet['next_actions']['if_approved_obstacle_summary']['requires_source_fresh_regeneration']}`",
        f"- requires_post_f02_6_plan_audit: `{packet['next_actions']['if_approved_obstacle_summary']['requires_post_f02_6_plan_audit']}`",
        f"- requires_approved_remote_preflight: `{packet['next_actions']['if_approved_obstacle_summary']['requires_approved_remote_preflight']}`",
        "",
        "```bash",
        packet["next_actions"]["if_approved_obstacle_summary"]["remote_runner_command"],
        "```",
        "",
        "## Claim Boundaries",
        ]
    )
    lines.extend(f"- {boundary}" for boundary in packet["claim_boundaries"])
    return "\n".join(lines) + "\n"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _sha256(path: str | Path) -> str | None:
    target = Path(path)
    if not target.exists() or not target.is_file():
        return None
    import hashlib

    digest = hashlib.sha256()
    with target.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _blocker_codes(blockers: Any) -> list[str]:
    return [str(item.get("code")) for item in blockers if isinstance(item, dict) and item.get("code")]


def _join_command(argv: Sequence[str]) -> str:
    return " ".join(shlex.quote(str(part)) for part in argv)


def _source_head() -> str:
    return module2_source_head()


if __name__ == "__main__":
    raise SystemExit(main())
