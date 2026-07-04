from __future__ import annotations

import argparse
import json
import shlex
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_remote_packet_safety_audit")
DEFAULT_REMOTE_PACKET = Path("0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json")
DEFAULT_DECISION_GATE_AUDIT = Path("0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.json")
DEFAULT_POST_PLAN_AUDIT = Path("0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json")
EXPECTED_PULLBACK_SUFFIXES = (
    "train/final_model.zip",
    "train/summary.json",
    "train/training_manifest.json",
    "eval/gate3_eval_episodes.csv",
    "eval/gate3_summary.json",
    "gate3_trial_manifest.json",
    "gate3_formal_audit.json",
)


@dataclass(frozen=True)
class RemotePacketSafetyAuditConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    remote_packet_path: Path = DEFAULT_REMOTE_PACKET
    decision_gate_audit_path: Path = DEFAULT_DECISION_GATE_AUDIT
    post_plan_audit_path: Path = DEFAULT_POST_PLAN_AUDIT


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = RemotePacketSafetyAuditConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        remote_packet_path=args.remote_packet,
        decision_gate_audit_path=args.decision_gate_audit,
        post_plan_audit_path=args.post_plan_audit,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "remote_packet_safety_audit.json"
    markdown_out = config.markdown_out or output_dir / "remote_packet_safety_audit.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: RemotePacketSafetyAuditConfig) -> dict[str, Any]:
    packet = _read_json(config.remote_packet_path)
    decision_gate = _read_json(config.decision_gate_audit_path)
    plan_audit = _read_json(config.post_plan_audit_path)
    issues = _audit_issues(packet=packet, decision_gate=decision_gate, plan_audit=plan_audit)
    return {
        "schema_version": 1,
        "artifact_name": "module2_remote_packet_safety_audit",
        "status": "remote_packet_safety_audit_passed" if not issues else "remote_packet_safety_audit_failed",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "inputs": {
            "remote_formal_execution_packet": str(config.remote_packet_path),
            "f02_6_decision_gate_audit": str(config.decision_gate_audit_path),
            "post_f02_6_plan_audit": str(config.post_plan_audit_path),
        },
        "packet_summary": _packet_summary(packet),
        "cross_gate_summary": _cross_gate_summary(decision_gate=decision_gate, plan_audit=plan_audit),
        "audit_issue_count": len(issues),
        "audit_issues": issues,
        "expected_pullback_suffixes": list(EXPECTED_PULLBACK_SUFFIXES),
        "claim_boundaries": [
            "This audit validates the remote execution packet; it does not execute sync, preflight, training, audit, or pullback commands.",
            "A passing audit is not permission to train while F02.6 remains pending.",
            "A passing audit is not a paper result or formal performance claim.",
            "Remote training must remain gpu3070ti-relay-only and must still be followed by audit, pullback, H01/H02 regeneration, and claim gates.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit Module2 remote formal execution packet safety without executing it.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--remote-packet", type=Path, default=DEFAULT_REMOTE_PACKET)
    parser.add_argument("--decision-gate-audit", type=Path, default=DEFAULT_DECISION_GATE_AUDIT)
    parser.add_argument("--post-plan-audit", type=Path, default=DEFAULT_POST_PLAN_AUDIT)
    return parser.parse_args(list(argv) if argv is not None else None)


def _audit_issues(*, packet: dict[str, Any], decision_gate: dict[str, Any], plan_audit: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    issues.extend(_packet_top_level_issues(packet))
    issues.extend(_environment_issues(packet))
    issues.extend(_execution_step_issues(packet))
    issues.extend(_pullback_issues(packet))
    issues.extend(_downstream_issues(packet))
    issues.extend(_cross_gate_issues(packet=packet, decision_gate=decision_gate, plan_audit=plan_audit))
    return _unique_issues(issues)


def _packet_top_level_issues(packet: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if packet.get("packet_name") != "module2_remote_formal_execution_packet":
        issues.append(_issue("packet_wrong_name", "Unexpected remote packet name.", observed=packet.get("packet_name")))
    if packet.get("local_training_allowed") is not False:
        issues.append(_issue("packet_allows_local_training", "Remote packet must preserve local-training prohibition."))
    if packet.get("formal_claim_allowed_before_audit") is not False:
        issues.append(_issue("packet_allows_claim_before_audit", "Remote packet must not allow claims before formal audit and pullback."))
    if packet.get("status") == "blocked_until_f02_6_decision" and packet.get("ready_to_run_remote_training") is not False:
        issues.append(_issue("pending_packet_ready_to_train", "Packet blocked by F02.6 must not be ready to run remote training."))
    return issues


def _environment_issues(packet: dict[str, Any]) -> list[dict[str, Any]]:
    env = packet.get("execution_environment") if isinstance(packet.get("execution_environment"), dict) else {}
    issues: list[dict[str, Any]] = []
    if env.get("gpu_alias") != "gpu3070ti-relay":
        issues.append(_issue("packet_wrong_gpu_alias", "gpu_alias must be gpu3070ti-relay.", observed=env.get("gpu_alias")))
    if env.get("training_host_required") != "gpu3070ti-relay":
        issues.append(_issue("packet_wrong_training_host", "training_host_required must be gpu3070ti-relay.", observed=env.get("training_host_required")))
    if env.get("remote_workdir") != "~/ForestNav":
        issues.append(_issue("packet_wrong_remote_workdir", "remote_workdir must remain ~/ForestNav.", observed=env.get("remote_workdir")))
    if env.get("remote_python") != ".venv/bin/python":
        issues.append(_issue("packet_wrong_remote_python", "remote_python must remain .venv/bin/python.", observed=env.get("remote_python")))
    return issues


def _execution_step_issues(packet: dict[str, Any]) -> list[dict[str, Any]]:
    steps = packet.get("execution_steps") if isinstance(packet.get("execution_steps"), dict) else {}
    issues: list[dict[str, Any]] = []
    sync = _step(steps, "sync_to_remote")
    sync_command = str(sync.get("command") or "")
    if sync.get("runs_training") is not False:
        issues.append(_issue("sync_step_runs_training", "sync_to_remote must be non-training."))
    if "--delete" in _split(sync_command):
        issues.append(_issue("sync_uses_delete", "sync_to_remote must not use --delete."))
    for required in ("--exclude .git", "--exclude '.venv*'", "--exclude __pycache__", "--exclude .pytest_cache", "--exclude 1_survey"):
        if required not in sync_command:
            issues.append(_issue(f"sync_missing_{_slug(required)}", f"sync_to_remote missing {required}."))
    preflight = _step(steps, "run_remote_preflight")
    if preflight.get("runs_training") is not False:
        issues.append(_issue("remote_preflight_claims_training", "run_remote_preflight must not be marked as training."))
    if preflight.get("allowed_now") is True and "ssh gpu3070ti-relay" not in str(preflight.get("command") or ""):
        issues.append(_issue("ready_preflight_not_remote_ssh", "Allowed preflight must execute through ssh gpu3070ti-relay."))
    training = _step(steps, "run_remote_training")
    train_command = str(training.get("command") or "")
    if training.get("runs_training") is not True:
        issues.append(_issue("training_step_not_marked_training", "run_remote_training must be explicitly marked as training."))
    if "ssh gpu3070ti-relay" not in train_command:
        issues.append(_issue("training_not_remote_ssh", "Training command must execute through ssh gpu3070ti-relay."))
    for required in ("run_rl_rs_gate3_trial", "--device cuda", "--bc-checkpoint", "--eval-episodes 64", "--eval-min-episodes 64", "--eval-success-threshold 0.8"):
        if required not in train_command:
            issues.append(_issue(f"training_missing_{_slug(required)}", f"Training command missing {required}."))
    if packet.get("status") == "blocked_until_f02_6_decision" and training.get("allowed_now") is not False:
        issues.append(_issue("pending_packet_training_step_allowed", "Training step must remain disallowed while F02.6 is pending."))
    audit = _step(steps, "run_remote_audit")
    audit_command = str(audit.get("command") or "")
    if audit.get("runs_training") is not False:
        issues.append(_issue("remote_audit_claims_training", "run_remote_audit must not be marked as training."))
    for required in ("ssh gpu3070ti-relay", "audit_rl_rs_gate3_trial", "--warm-start-decision approved_obstacle_summary"):
        if required not in audit_command:
            issues.append(_issue(f"audit_missing_{_slug(required)}", f"Remote audit command missing {required}."))
    if packet.get("status") == "blocked_until_f02_6_decision" and audit.get("allowed_now") is not False:
        issues.append(_issue("pending_packet_audit_step_allowed", "Audit step must remain disallowed while F02.6 is pending."))
    return issues


def _pullback_issues(packet: dict[str, Any]) -> list[dict[str, Any]]:
    pullback = packet.get("post_run_pullback") if isinstance(packet.get("post_run_pullback"), dict) else {}
    artifacts = _strings(pullback.get("expected_artifacts"))
    issues: list[dict[str, Any]] = []
    if pullback.get("required_before_local_claim") is not True:
        issues.append(_issue("pullback_not_required_before_claim", "Pullback must be required before any local claim."))
    if pullback.get("hash_manifest_required") is not True:
        issues.append(_issue("pullback_hash_manifest_not_required", "Pullback must require a hash manifest."))
    if len(artifacts) != len(EXPECTED_PULLBACK_SUFFIXES):
        issues.append(_issue("pullback_wrong_artifact_count", "Pullback artifact count must stay at seven.", observed=len(artifacts)))
    joined = "\n".join(artifacts)
    for suffix in EXPECTED_PULLBACK_SUFFIXES:
        if suffix not in joined:
            issues.append(_issue(f"pullback_missing_{_slug(suffix)}", f"Missing pullback artifact suffix {suffix}."))
    command = str(pullback.get("pullback_command") or "")
    if "gpu3070ti-relay:~/ForestNav/" not in command:
        issues.append(_issue("pullback_not_from_gpu3070ti", "Pullback command must read from gpu3070ti-relay:~/ForestNav/."))
    if "--delete" in _split(command):
        issues.append(_issue("pullback_uses_delete", "Pullback command must not use --delete."))
    return issues


def _downstream_issues(packet: dict[str, Any]) -> list[dict[str, Any]]:
    downstream = packet.get("downstream_after_successful_audit") if isinstance(packet.get("downstream_after_successful_audit"), dict) else {}
    issues: list[dict[str, Any]] = []
    for key in ("h01_manifest_must_be_regenerated", "h02_full_smoke_must_be_regenerated", "paper_tables_must_be_regenerated_from_h02_formal_outputs"):
        if downstream.get(key) is not True:
            issues.append(_issue(f"downstream_missing_{key}", f"Downstream requirement {key} must be true."))
    requirements = "\n".join(_strings(downstream.get("formal_claim_requires")))
    for required in ("gate3_formal_audit.formal_decision is pass", "pulled-back checkpoint hash is recorded", "H01 manifest status becomes ready_for_formal_run", "H02 full all-method smoke"):
        if required not in requirements:
            issues.append(_issue(f"claim_requirement_missing_{_slug(required)}", f"Formal claim requirement missing {required}."))
    return issues


def _cross_gate_issues(*, packet: dict[str, Any], decision_gate: dict[str, Any], plan_audit: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    decision = decision_gate.get("decision_state") if isinstance(decision_gate.get("decision_state"), dict) else {}
    status_summary = plan_audit.get("status_report_summary") if isinstance(plan_audit.get("status_report_summary"), dict) else {}
    plan_inputs = plan_audit.get("inputs") if isinstance(plan_audit.get("inputs"), dict) else {}
    if decision_gate and decision_gate.get("status") == "f02_6_decision_gate_pending_clean":
        if packet.get("status") != "blocked_until_f02_6_decision":
            issues.append(_issue("pending_decision_packet_not_blocked", "Remote packet must be blocked while F02.6 is pending.", observed=packet.get("status")))
        if packet.get("ready_to_run_remote_training") is not False:
            issues.append(_issue("pending_decision_packet_ready", "Remote packet must not be ready while F02.6 is pending."))
        if _step(packet.get("execution_steps", {}), "sync_to_remote").get("allowed_now") is True:
            issues.append(_issue("pending_decision_packet_allows_sync", "Remote sync must remain disallowed while F02.6 is pending."))
    if decision and decision.get("training_allowed_now") is False and _step(packet.get("execution_steps", {}), "run_remote_training").get("allowed_now") is True:
        issues.append(_issue("decision_gate_blocks_but_packet_allows_training", "Decision gate blocks training but remote packet allows it."))
    blocking = plan_audit.get("current_blocking_summary") if isinstance(plan_audit.get("current_blocking_summary"), dict) else {}
    if plan_audit and blocking.get("training_allowed_now") is False and _step(packet.get("execution_steps", {}), "run_remote_training").get("allowed_now") is True:
        issues.append(_issue("post_plan_blocks_but_packet_allows_training", "Post-F02.6 plan audit blocks training but remote packet allows it."))
    if plan_audit and "formal_gate_status_report" not in plan_inputs:
        issues.append(_issue("post_plan_missing_status_report_input", "Post-F02.6 plan audit must consume the formal gate status report before remote packet safety can pass."))
    if plan_audit and not status_summary:
        issues.append(_issue("post_plan_missing_status_report_summary", "Post-F02.6 plan audit must expose status_report_summary before remote packet safety can pass."))
    if status_summary.get("local_training_allowed_now") is not False:
        issues.append(_issue("status_report_allows_local_training_now", "Remote packet safety requires status report to preserve local-training prohibition."))
    if status_summary.get("status") != "formal_gate_status_ready_for_claim_audit":
        steps = packet.get("execution_steps", {}) if isinstance(packet.get("execution_steps"), dict) else {}
        if packet.get("ready_to_run_remote_training") is True:
            issues.append(_issue("blocked_status_report_packet_ready", "Remote packet must not be ready while the formal gate status report is blocked."))
        if _step(steps, "sync_to_remote").get("allowed_now") is True:
            issues.append(_issue("blocked_status_report_allows_remote_sync", "Remote sync must remain disallowed while the formal gate status report is blocked."))
        if _step(steps, "run_remote_preflight").get("allowed_now") is True:
            issues.append(_issue("blocked_status_report_allows_remote_preflight", "Remote preflight must remain disallowed while the formal gate status report is blocked."))
        if _step(steps, "run_remote_training").get("allowed_now") is True:
            issues.append(_issue("blocked_status_report_allows_remote_training", "Remote training must remain disallowed while the formal gate status report is blocked."))
        if _step(steps, "run_remote_audit").get("allowed_now") is True:
            issues.append(_issue("blocked_status_report_allows_remote_audit", "Remote audit must remain disallowed while the formal gate status report is blocked."))
    return issues


def _packet_summary(packet: dict[str, Any]) -> dict[str, Any]:
    steps = packet.get("execution_steps") if isinstance(packet.get("execution_steps"), dict) else {}
    pullback = packet.get("post_run_pullback") if isinstance(packet.get("post_run_pullback"), dict) else {}
    env = packet.get("execution_environment") if isinstance(packet.get("execution_environment"), dict) else {}
    return {
        "status": packet.get("status"),
        "ready_to_run_remote_training": packet.get("ready_to_run_remote_training"),
        "gpu_alias": env.get("gpu_alias"),
        "training_host_required": env.get("training_host_required"),
        "sync_allowed_now": _step(steps, "sync_to_remote").get("allowed_now"),
        "remote_preflight_allowed_now": _step(steps, "run_remote_preflight").get("allowed_now"),
        "remote_training_allowed_now": _step(steps, "run_remote_training").get("allowed_now"),
        "remote_audit_allowed_now": _step(steps, "run_remote_audit").get("allowed_now"),
        "pullback_artifact_count": len(_strings(pullback.get("expected_artifacts"))),
        "hash_manifest_required": pullback.get("hash_manifest_required"),
    }


def _cross_gate_summary(*, decision_gate: dict[str, Any], plan_audit: dict[str, Any]) -> dict[str, Any]:
    decision = decision_gate.get("decision_state") if isinstance(decision_gate.get("decision_state"), dict) else {}
    blocking = plan_audit.get("current_blocking_summary") if isinstance(plan_audit.get("current_blocking_summary"), dict) else {}
    status_summary = plan_audit.get("status_report_summary") if isinstance(plan_audit.get("status_report_summary"), dict) else {}
    return {
        "decision_gate_status": decision_gate.get("status"),
        "f02_6_record_status": decision.get("record_status"),
        "decision_training_allowed_now": decision.get("training_allowed_now"),
        "post_plan_audit_status": plan_audit.get("status"),
        "post_plan_training_allowed_now": blocking.get("training_allowed_now"),
        "post_plan_remote_preflight_allowed_now": blocking.get("remote_preflight_allowed_now"),
        "post_plan_status_report_status": status_summary.get("status"),
        "post_plan_status_report_formal_claim_allowed_now": status_summary.get("formal_claim_allowed_now"),
        "post_plan_status_report_local_training_allowed_now": status_summary.get("local_training_allowed_now"),
        "post_plan_status_report_next_blocked_lane_id": status_summary.get("next_blocked_lane_id"),
    }


def _step(steps: Any, name: str) -> dict[str, Any]:
    if not isinstance(steps, dict):
        return {}
    item = steps.get(name)
    return item if isinstance(item, dict) else {}


def _strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _split(command: str) -> list[str]:
    try:
        return shlex.split(command)
    except ValueError:
        return command.split()


def _slug(value: str) -> str:
    out = []
    for char in value.lower():
        out.append(char if char.isalnum() else "_")
    return "".join(out).strip("_")


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
        "# Module2 Remote Packet Safety Audit",
        "",
        "This file audits the remote formal execution packet. It does not execute any command.",
        "",
        f"- status: `{manifest['status']}`",
        f"- audit_issue_count: `{manifest['audit_issue_count']}`",
        f"- packet_status: `{manifest['packet_summary']['status']}`",
        f"- remote_training_allowed_now: `{manifest['packet_summary']['remote_training_allowed_now']}`",
        f"- pullback_artifact_count: `{manifest['packet_summary']['pullback_artifact_count']}`",
        f"- post_plan_status_report_status: `{manifest['cross_gate_summary']['post_plan_status_report_status']}`",
        f"- post_plan_status_report_next_blocked_lane_id: `{manifest['cross_gate_summary']['post_plan_status_report_next_blocked_lane_id']}`",
        "",
        "## Audit Issues",
        "",
    ]
    if manifest["audit_issues"]:
        lines.extend(f"- `{issue['issue_id']}`: {issue['message']}" for issue in manifest["audit_issues"])
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
