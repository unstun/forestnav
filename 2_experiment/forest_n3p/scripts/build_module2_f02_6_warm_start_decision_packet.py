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
        "remote_readiness": _remote_readiness(remote_no_warm=remote_no_warm, remote_warm=remote_warm, remote_smoke=remote_smoke),
        "current_authorization": _current_authorization(
            decision_record=decision_record,
            decision_intake=decision_intake,
        ),
        "next_actions": _next_actions(),
        "sources": sources,
        "source_integrity_summary": _source_integrity_summary(sources),
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
    return {
        "authorization_status": "blocked_until_dr_sun_decision",
        "decision_owner_required": str(decision_record.get("decision_owner_required") or "Dr Sun"),
        "decision_record": {
            "status": str(decision_record.get("status")),
            "requested_decision": str(decision_record.get("requested_decision")),
            "effective_warm_start_decision": str(decision_record.get("effective_warm_start_decision")),
            "decider": decision_record.get("decider"),
            "decision_note_present": bool(decision_record.get("decision_note")),
        },
        "decision_intake": {
            "status": str(decision_intake.get("status")),
            "next_blocked_lane": str(current_state.get("next_blocked_lane")),
            "audit_issue_count": int(decision_intake.get("audit_issue_count", 0) or 0),
            "valid_decision_count": len(valid_decisions),
            "required_record_field_count": len(required_fields),
            "post_decision_route_count": len(post_decision_routes),
            "post_decision_non_authorization_count": len(non_authorizations),
        },
        "current_allowed_action_ids": ["record_f02_6_decision"],
        "current_blocked_action_ids": [
            "remote_preflight",
            "remote_training",
            "local_training",
            "formal_claim",
            "paper_result_material",
        ],
        "post_decision_routes_are_current_authorization": False,
        "remote_preflight_allowed_now": bool(decision_record.get("remote_preflight_allowed_now")),
        "remote_training_allowed_now": bool(decision_record.get("remote_training_allowed_now")),
        "local_training_allowed_now": bool(decision_record.get("local_training_allowed")),
        "formal_claim_allowed_now": bool(decision_record.get("formal_claim_allowed")),
        "paper_result_material_allowed_now": False,
        "required_next_human_action": "record Dr Sun's F02.6 approval or rejection before any remote preflight.",
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
        "## Source Integrity",
        "",
        f"- source_count: `{packet['source_integrity_summary']['source_count']}`",
        f"- missing_source_count: `{packet['source_integrity_summary']['missing_source_count']}`",
        f"- all_sources_present: `{packet['source_integrity_summary']['all_sources_present']}`",
        f"- all_existing_sources_hashed: `{packet['source_integrity_summary']['all_existing_sources_hashed']}`",
        "",
        "## Next Command If Approved",
        "",
        "```bash",
        packet["next_actions"]["if_approved_obstacle_summary"]["runner_command"],
        "```",
        "",
        "## Claim Boundaries",
    ]
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
