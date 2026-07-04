from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_formal_gate_gap_audit")
DEFAULT_CONTRACT = Path(".pipeline/contracts/module2-ppo-funnel-expansion.md")
DEFAULT_DECISION_RECORD = Path("0_trials/module2_f02_6_decision_record/f02_6_decision_record.json")
DEFAULT_H01_MANIFEST = Path("0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json")
DEFAULT_REMOTE_PACKET = Path("0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json")
DEFAULT_H02_ACCEPTANCE = Path("0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json")
DEFAULT_CLAIM_SAFETY = Path("0_trials/module2_claim_safety/module2_claim_safety.json")
DEFAULT_READINESS = Path("0_trials/module2_paper_readiness/module2_paper_readiness.json")


@dataclass(frozen=True)
class FormalGateGapAuditConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    contract_path: Path = DEFAULT_CONTRACT
    decision_record_path: Path = DEFAULT_DECISION_RECORD
    h01_manifest_path: Path = DEFAULT_H01_MANIFEST
    remote_packet_path: Path = DEFAULT_REMOTE_PACKET
    h02_acceptance_path: Path = DEFAULT_H02_ACCEPTANCE
    claim_safety_path: Path = DEFAULT_CLAIM_SAFETY
    readiness_path: Path = DEFAULT_READINESS


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = FormalGateGapAuditConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        contract_path=args.contract,
        decision_record_path=args.decision_record,
        h01_manifest_path=args.h01_manifest,
        remote_packet_path=args.remote_packet,
        h02_acceptance_path=args.h02_acceptance,
        claim_safety_path=args.claim_safety,
        readiness_path=args.readiness,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "formal_gate_gap_audit.json"
    markdown_out = config.markdown_out or output_dir / "formal_gate_gap_audit.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(
        json.dumps(
            {"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]},
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


def build_manifest(config: FormalGateGapAuditConfig) -> dict[str, Any]:
    contract = _frontmatter(config.contract_path)
    decision = _read_json(config.decision_record_path)
    h01 = _read_json(config.h01_manifest_path)
    remote = _read_json(config.remote_packet_path)
    h02 = _read_json(config.h02_acceptance_path)
    claim_safety = _read_json(config.claim_safety_path)
    readiness = _read_json(config.readiness_path)

    decision_gaps = _decision_gaps(decision=decision, h01=h01, remote=remote)
    training_gaps = _training_gaps(remote=remote, h02=h02)
    evaluation_gaps = _evaluation_gaps(h01=h01, h02=h02)
    acceptance_gaps = _acceptance_gaps(h02=h02, claim_safety=claim_safety, readiness=readiness)
    all_gaps = decision_gaps + training_gaps + evaluation_gaps + acceptance_gaps
    status = "formal_gate_ready_for_result_audit" if not all_gaps else "blocked_formal_gate_gaps_open"

    return {
        "schema_version": 1,
        "artifact_name": "module2_formal_gate_gap_audit",
        "status": status,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "not_paper_result_material": True,
        "local_training_allowed": False,
        "remote_training_resource": _remote_training_resource(remote),
        "contract": {
            "path": str(config.contract_path),
            "status": contract.get("status"),
            "version": contract.get("version"),
            "approved_by": contract.get("approved_by"),
            "approved_date": contract.get("approved_date"),
        },
        "current_gate_state": _current_gate_state(decision=decision, h01=h01, remote=remote, h02=h02, claim_safety=claim_safety),
        "missing_decision_items": decision_gaps,
        "missing_training_artifacts": training_gaps,
        "missing_evaluation_artifacts": evaluation_gaps,
        "missing_acceptance_artifacts": acceptance_gaps,
        "ordered_next_steps": _ordered_next_steps(decision_gaps, training_gaps, evaluation_gaps, acceptance_gaps, remote),
        "claim_boundaries": [
            "This audit is a formal-gate gap ledger, not a paper result, table, or appendix.",
            "Do not write performance-improvement or warm-start-effect claims from this artifact.",
            "No PPO/RL-RS formal training is allowed on the local Mac.",
            "Formal PPO checkpoint production must run on gpu3070ti-relay after F02.6 closes.",
            "Remote completion is insufficient until audit artifacts, checkpoint hashes, H01/H02 regeneration, and claim safety all pass.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Module2 PPO-RS formal gate gap audit without running training.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--decision-record", type=Path, default=DEFAULT_DECISION_RECORD)
    parser.add_argument("--h01-manifest", type=Path, default=DEFAULT_H01_MANIFEST)
    parser.add_argument("--remote-packet", type=Path, default=DEFAULT_REMOTE_PACKET)
    parser.add_argument("--h02-acceptance", type=Path, default=DEFAULT_H02_ACCEPTANCE)
    parser.add_argument("--claim-safety", type=Path, default=DEFAULT_CLAIM_SAFETY)
    parser.add_argument("--readiness", type=Path, default=DEFAULT_READINESS)
    return parser.parse_args(list(argv) if argv is not None else None)


def _decision_gaps(*, decision: dict[str, Any], h01: dict[str, Any], remote: dict[str, Any]) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []
    if decision.get("status") == "pending_human_decision":
        gaps.append(
            _gap(
                "decision",
                "f02_6_warm_start_decision_pending",
                "Dr Sun has not approved or rejected the F02.6 obstacle-summary warm-start protocol.",
                "0_trials/module2_f02_6_decision_record/f02_6_decision_record.json",
                "Set effective_warm_start_decision to an approved/rejected state through the decision protocol before remote formal PPO.",
            )
        )
    for blocker in _strings(h01.get("blockers")) + _strings(remote.get("blockers")):
        if blocker in {"requires_dr_sun_approval", "f02_6_warm_start_decision_pending", "f02_6_decision_record_pending"}:
            gaps.append(
                _gap(
                    "decision",
                    blocker,
                    f"Gate artifact still reports decision blocker: {blocker}.",
                    _source_for_blocker(blocker),
                    "Close F02.6 first; do not bypass it by running local training or writing result claims.",
                )
            )
    return _unique_gaps(gaps)


def _training_gaps(*, remote: dict[str, Any], h02: dict[str, Any]) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []
    if remote.get("ready_to_run_remote_training") is not True:
        gaps.append(
            _gap(
                "training",
                "remote_training_packet_not_ready",
                f"Remote execution packet status is {remote.get('status')}; training command is not allowed yet.",
                "0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json",
                "After F02.6 closes, regenerate approved remote preflight and require ready_to_run_remote_training=true.",
            )
        )
    if remote.get("local_training_allowed") is not False:
        gaps.append(
            _gap(
                "training",
                "local_training_guard_invalid",
                "A formal gate artifact did not explicitly forbid local training.",
                "0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json",
                "Keep local_training_allowed=false for all formal PPO paths.",
            )
        )
    pullback = remote.get("post_run_pullback") if isinstance(remote.get("post_run_pullback"), dict) else {}
    for path in _strings(pullback.get("expected_artifacts")):
        if not Path(path).is_file():
            gaps.append(
                _gap(
                    "training",
                    "missing_remote_pullback_artifact",
                    f"Required remote artifact has not been pulled back: {path}.",
                    path,
                    "Run formal PPO only on gpu3070ti-relay, then pull back the complete trial directory with hashes.",
                )
            )
    method_checks = h02.get("method_checks") if isinstance(h02.get("method_checks"), dict) else {}
    if method_checks.get("has_ppo_result_rows") is not True:
        gaps.append(
            _gap(
                "training",
                "missing_ppo_result_rows",
                "H02 acceptance sees no PPO/RL-RS formal result rows.",
                "0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json",
                "Generate formal evaluation outputs that include ppo_analytic_operator or ha_rl_rs_ppo rows from the audited checkpoint.",
            )
        )
    if method_checks.get("ppo_rows_have_checkpoint_hash") is not True:
        gaps.append(
            _gap(
                "training",
                "missing_ppo_checkpoint_hash",
                "PPO rows do not contain a non-empty rl_rs_checkpoint_sha256.",
                "0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json",
                "Record checkpoint path and SHA-256 in every PPO/RL-RS result row.",
            )
        )
    return _unique_gaps(gaps)


def _evaluation_gaps(*, h01: dict[str, Any], h02: dict[str, Any]) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []
    if str(h01.get("status")) not in {"ready", "formal_ready", "ready_for_formal_run", "ready_for_formal_evaluation"}:
        gaps.append(
            _gap(
                "evaluation",
                "h01_manifest_not_ready",
                f"H01 manifest status is {h01.get('status')}.",
                "0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json",
                "Regenerate H01 after F02.6 and checkpoint availability so the formal run command is unblocked.",
            )
        )
    run_command = h01.get("run_command") if isinstance(h01.get("run_command"), dict) else {}
    if not run_command.get("formal_main_evaluation"):
        gaps.append(
            _gap(
                "evaluation",
                "formal_main_evaluation_command_missing",
                "H01 does not expose a runnable formal_main_evaluation command.",
                "0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json",
                "Regenerate H01 with the audited checkpoint and formal scale so the main evaluation command is explicit.",
            )
        )
    formal_checks = h02.get("formal_checks") if isinstance(h02.get("formal_checks"), dict) else {}
    scale_checks = formal_checks.get("scale_checks") if isinstance(formal_checks.get("scale_checks"), dict) else {}
    for name, item in scale_checks.items():
        if isinstance(item, dict) and not item.get("satisfied"):
            gaps.append(
                _gap(
                    "evaluation",
                    f"h02_scale_below_h01_{name}",
                    f"H02 {name} observed={item.get('observed')} required={item.get('required')}.",
                    "0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json",
                    "Run formal evaluation at the H01 scale instead of the local smoke scale.",
                )
            )
    if formal_checks.get("h02_verdict_formal_acceptance") is not True:
        gaps.append(
            _gap(
                "evaluation",
                "h02_verdict_not_formal",
                f"H02 verdict status is {formal_checks.get('h02_verdict_status')}.",
                "0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json",
                "Produce formal evaluation outputs whose verdict marks formal_acceptance=true.",
            )
        )
    return _unique_gaps(gaps)


def _acceptance_gaps(*, h02: dict[str, Any], claim_safety: dict[str, Any], readiness: dict[str, Any]) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []
    formal_checks = h02.get("formal_checks") if isinstance(h02.get("formal_checks"), dict) else {}
    if formal_checks.get("gate3_formal_audit_passed") is not True:
        gaps.append(
            _gap(
                "acceptance",
                "missing_or_failed_gate3_formal_audit",
                "Gate3 formal audit for the approved warm-start trial is missing or not pass.",
                str(formal_checks.get("gate3_audit_path") or "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json"),
                "Run remote audit after training and require formal_decision=pass before H02 acceptance.",
            )
        )
    if h02.get("formal_output_accepted") is not True or h02.get("paper_result_input_allowed") is not True:
        gaps.append(
            _gap(
                "acceptance",
                "h02_formal_output_not_accepted",
                f"H02 status is {h02.get('status')}; paper_result_input_allowed={h02.get('paper_result_input_allowed')}.",
                "0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json",
                "Regenerate H02 acceptance after formal evaluation, checkpoint hash, and pullback artifacts are present.",
            )
        )
    if claim_safety.get("formal_performance_claim_allowed") is not True:
        gaps.append(
            _gap(
                "acceptance",
                "claim_safety_blocks_formal_performance",
                f"Claim safety status is {claim_safety.get('status')}.",
                "0_trials/module2_claim_safety/module2_claim_safety.json",
                "Regenerate claim safety only after H02 formal acceptance is true; do not manually override.",
            )
        )
    if readiness.get("formal_results_ready") is not True:
        gaps.append(
            _gap(
                "acceptance",
                "readiness_blocks_formal_results",
                f"Readiness status is {readiness.get('status')}; formal_results_ready={readiness.get('formal_results_ready')}.",
                "0_trials/module2_paper_readiness/module2_paper_readiness.json",
                "Use readiness only as a gate; do not write result material until it reports formal_results_ready=true.",
            )
        )
    return _unique_gaps(gaps)


def _ordered_next_steps(
    decision_gaps: Sequence[dict[str, Any]],
    training_gaps: Sequence[dict[str, Any]],
    evaluation_gaps: Sequence[dict[str, Any]],
    acceptance_gaps: Sequence[dict[str, Any]],
    remote: dict[str, Any],
) -> list[dict[str, Any]]:
    steps: list[dict[str, Any]] = []
    steps.append(
        {
            "step_id": "F02.6",
            "phase": "decision",
            "status": "blocked" if decision_gaps else "ready",
            "runs_training": False,
            "action": "Close Dr Sun's obstacle-summary warm-start decision record.",
            "evidence_to_update": "0_trials/module2_f02_6_decision_record/f02_6_decision_record.json",
        }
    )
    steps.append(
        {
            "step_id": "remote_preflight",
            "phase": "training",
            "status": "blocked" if decision_gaps else "pending_execution",
            "runs_training": False,
            "host": _remote_training_resource(remote),
            "action": "Regenerate approved gpu3070ti preflight and require formal_trial_ready=true.",
            "evidence_to_update": "0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_approved_remote_v1/gate3_preflight_manifest.json",
        }
    )
    steps.append(
        {
            "step_id": "gate3_remote_training",
            "phase": "training",
            "status": "blocked" if decision_gaps or training_gaps else "pending_execution",
            "runs_training": True,
            "host": _remote_training_resource(remote),
            "action": "Run formal PPO Gate3 trial remotely; never on local Mac.",
            "evidence_to_update": "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/",
        }
    )
    steps.append(
        {
            "step_id": "gate3_remote_audit_pullback",
            "phase": "acceptance",
            "status": "blocked" if training_gaps else "pending_execution",
            "runs_training": False,
            "host": _remote_training_resource(remote),
            "action": "Audit remote trial, pull back checkpoint/eval/audit artifacts, and record hashes.",
            "evidence_to_update": "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json",
        }
    )
    steps.append(
        {
            "step_id": "h01_h02_regeneration",
            "phase": "evaluation",
            "status": "blocked" if training_gaps or evaluation_gaps else "pending_execution",
            "runs_training": False,
            "action": "Regenerate H01 with checkpoint and run H02 formal evaluation at H01 scale.",
            "evidence_to_update": "0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json",
        }
    )
    steps.append(
        {
            "step_id": "claim_safety_final_gate",
            "phase": "acceptance",
            "status": "blocked" if acceptance_gaps else "ready",
            "runs_training": False,
            "action": "Regenerate claim safety/readiness; allow formal claims only if all gates pass.",
            "evidence_to_update": "0_trials/module2_claim_safety/module2_claim_safety.json",
        }
    )
    return steps


def _current_gate_state(
    *,
    decision: dict[str, Any],
    h01: dict[str, Any],
    remote: dict[str, Any],
    h02: dict[str, Any],
    claim_safety: dict[str, Any],
) -> dict[str, Any]:
    method_checks = h02.get("method_checks") if isinstance(h02.get("method_checks"), dict) else {}
    return {
        "f02_6_decision_status": decision.get("status"),
        "effective_warm_start_decision": decision.get("effective_warm_start_decision"),
        "remote_training_allowed": bool(decision.get("remote_training_allowed")),
        "h01_status": h01.get("status"),
        "remote_packet_status": remote.get("status"),
        "ready_to_run_remote_training": bool(remote.get("ready_to_run_remote_training")),
        "h02_status": h02.get("status"),
        "h02_formal_output_accepted": bool(h02.get("formal_output_accepted")),
        "ppo_row_count": method_checks.get("ppo_row_count"),
        "ppo_checkpoint_hashes": method_checks.get("ppo_checkpoint_hashes", []),
        "formal_performance_claim_allowed": bool(claim_safety.get("formal_performance_claim_allowed")),
    }


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 PPO-RS Formal Gate Gap Audit",
        "",
        "This file is a formal-gate gap ledger. It is not a paper result, table, or appendix.",
        "",
        f"- status: `{manifest['status']}`",
        f"- local_training_allowed: `{manifest['local_training_allowed']}`",
        f"- remote_training_resource: `{manifest['remote_training_resource']}`",
        f"- formal_performance_claim_allowed: `{manifest['current_gate_state']['formal_performance_claim_allowed']}`",
        "",
    ]
    for title, key in [
        ("Decision Gaps", "missing_decision_items"),
        ("Training Artifact Gaps", "missing_training_artifacts"),
        ("Evaluation Artifact Gaps", "missing_evaluation_artifacts"),
        ("Acceptance Artifact Gaps", "missing_acceptance_artifacts"),
    ]:
        lines.extend([f"## {title}", ""])
        gaps = manifest[key]
        if gaps:
            for gap in gaps:
                lines.extend(
                    [
                        f"- `{gap['gap_id']}`",
                        f"  - evidence: `{gap['evidence_path']}`",
                        f"  - why: {gap['why_missing']}",
                        f"  - needed: {gap['required_next_artifact']}",
                    ]
                )
        else:
            lines.append("- none")
        lines.append("")
    lines.extend(["## Ordered Next Steps", ""])
    for step in manifest["ordered_next_steps"]:
        host = f", host=`{step['host']}`" if step.get("host") else ""
        lines.append(
            f"- `{step['step_id']}` ({step['phase']}): status=`{step['status']}`, "
            f"runs_training=`{step['runs_training']}`{host}. {step['action']}"
        )
    lines.extend(["", "## Claim Boundaries", ""])
    for boundary in manifest["claim_boundaries"]:
        lines.append(f"- {boundary}")
    lines.append("")
    return "\n".join(lines)


def _gap(category: str, gap_id: str, why_missing: str, evidence_path: str, required_next_artifact: str) -> dict[str, Any]:
    return {
        "category": category,
        "gap_id": gap_id,
        "why_missing": why_missing,
        "evidence_path": evidence_path,
        "required_next_artifact": required_next_artifact,
    }


def _source_for_blocker(blocker: str) -> str:
    if blocker.startswith("f02_6"):
        return "0_trials/module2_f02_6_decision_record/f02_6_decision_record.json"
    return "0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json"


def _remote_training_resource(remote: dict[str, Any]) -> str:
    env = remote.get("execution_environment") if isinstance(remote.get("execution_environment"), dict) else {}
    return str(env.get("gpu_alias") or env.get("training_host_required") or "gpu3070ti-relay")


def _read_json(path: Path) -> dict[str, Any]:
    if not Path(path).is_file():
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _frontmatter(path: Path) -> dict[str, str]:
    if not Path(path).is_file():
        return {}
    text = Path(path).read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for line in text[3:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def _strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


def _unique_gaps(gaps: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str, str]] = set()
    unique: list[dict[str, Any]] = []
    for gap in gaps:
        key = (str(gap.get("category")), str(gap.get("gap_id")), str(gap.get("evidence_path")))
        if key in seen:
            continue
        seen.add(key)
        unique.append(gap)
    return unique


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        dirty = subprocess.run(["git", "diff", "--quiet"], check=False)
        staged_dirty = subprocess.run(["git", "diff", "--cached", "--quiet"], check=False)
        suffix = "+dirty" if dirty.returncode != 0 or staged_dirty.returncode != 0 else ""
        return f"{head}{suffix}"
    except Exception:
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
