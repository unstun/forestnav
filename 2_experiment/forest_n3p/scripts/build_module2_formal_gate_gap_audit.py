from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_formal_gate_gap_audit")
DEFAULT_CONTRACT = Path(".pipeline/contracts/module2-ppo-funnel-expansion.md")
DEFAULT_DECISION_RECORD = Path("0_trials/module2_f02_6_decision_record/f02_6_decision_record.json")
DEFAULT_H01_MANIFEST = Path("0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json")
DEFAULT_REMOTE_PACKET = Path("0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json")
DEFAULT_H02_ACCEPTANCE = Path("0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json")
DEFAULT_CLAIM_SAFETY = Path("0_trials/module2_claim_safety/module2_claim_safety.json")
DEFAULT_READINESS = Path("0_trials/module2_paper_readiness/module2_paper_readiness.json")
DEFAULT_REMOTE_READINESS = Path("0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.json")
DEFAULT_SOURCE_FRESHNESS = Path("0_trials/module2_source_freshness_audit/source_freshness_audit.json")
DEFAULT_MISSING_ARTIFACTS = Path("0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json")
DEFAULT_CLOSURE_CHECKLIST = Path("0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json")
DEFAULT_STATUS_REPORT = Path("0_trials/module2_formal_gate_status_report/formal_gate_status_report.json")
DEFAULT_REMAINING_DELIVERABLES = Path(
    "0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json"
)
DEFAULT_HANDOFF_BUNDLE = Path("0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json")
DEFAULT_REMOTE_PACKET_SAFETY = Path("0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json")
REMOTE_EXECUTION_STEP_IDS = (
    "sync_to_remote",
    "run_remote_preflight",
    "run_remote_training",
    "run_remote_audit",
)
REMOTE_PACKET_SAFETY_STEP_MAP = {
    "sync_to_remote": ("sync_allowed_now", "sync_blocked_by"),
    "run_remote_preflight": ("remote_preflight_allowed_now", "remote_preflight_blocked_by"),
    "run_remote_training": ("remote_training_allowed_now", "remote_training_blocked_by"),
    "run_remote_audit": ("remote_audit_allowed_now", "remote_audit_blocked_by"),
}
CLAIM_GATE_REGENERATION_ARTIFACT_IDS = (
    "formal_gate_proof_summary_chain_audit",
    "mainline_formal_gate_state_audit",
    "claim_safety",
    "paper_readiness",
)


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
    remote_readiness_path: Path = DEFAULT_REMOTE_READINESS
    source_freshness_path: Path = DEFAULT_SOURCE_FRESHNESS
    missing_artifacts_path: Path = DEFAULT_MISSING_ARTIFACTS
    closure_checklist_path: Path = DEFAULT_CLOSURE_CHECKLIST
    status_report_path: Path = DEFAULT_STATUS_REPORT
    remaining_deliverables_path: Path = DEFAULT_REMAINING_DELIVERABLES
    handoff_bundle_path: Path = DEFAULT_HANDOFF_BUNDLE
    remote_packet_safety_path: Path = DEFAULT_REMOTE_PACKET_SAFETY


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
        remote_readiness_path=args.remote_readiness_refresh,
        source_freshness_path=args.source_freshness_audit,
        missing_artifacts_path=args.missing_artifacts_audit,
        closure_checklist_path=args.closure_checklist,
        status_report_path=args.status_report,
        remaining_deliverables_path=args.remaining_deliverables,
        handoff_bundle_path=args.handoff_bundle,
        remote_packet_safety_path=args.remote_packet_safety_audit,
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
    remote_readiness = _read_json(config.remote_readiness_path)
    source_freshness = _read_json(config.source_freshness_path)
    missing_artifacts = _read_json(config.missing_artifacts_path)
    closure_checklist = _read_json(config.closure_checklist_path)
    status_report = _read_json(config.status_report_path)
    remaining_deliverables = _read_json(config.remaining_deliverables_path)
    handoff_bundle = _read_json(config.handoff_bundle_path)
    remote_packet_safety = _read_json(config.remote_packet_safety_path)

    decision_gaps = _decision_gaps(decision=decision, h01=h01, remote=remote)
    source_freshness_gaps = _source_freshness_gaps(source_freshness=source_freshness, source_freshness_path=config.source_freshness_path)
    execution_veto_gaps = _unique_gaps(
        _handoff_bundle_gaps(
            handoff_bundle=handoff_bundle,
            handoff_bundle_path=config.handoff_bundle_path,
            remote=remote,
        )
        + _remote_packet_safety_gaps(
            remote_packet_safety=remote_packet_safety,
            remote_packet_safety_path=config.remote_packet_safety_path,
            remote=remote,
        )
    )
    training_gaps = _training_gaps(remote=remote, h02=h02, remote_readiness=remote_readiness, remote_readiness_path=config.remote_readiness_path)
    training_gaps = _unique_gaps(training_gaps + source_freshness_gaps)
    training_gaps = _unique_gaps(training_gaps + execution_veto_gaps)
    evaluation_gaps = _evaluation_gaps(h01=h01, h02=h02)
    acceptance_gaps = _acceptance_gaps(h02=h02, claim_safety=claim_safety, readiness=readiness)
    acceptance_gaps = _unique_gaps(
        acceptance_gaps
        + _missing_artifacts_gaps(missing_artifacts=missing_artifacts, missing_artifacts_path=config.missing_artifacts_path)
        + _closure_checklist_gaps(closure_checklist=closure_checklist, closure_checklist_path=config.closure_checklist_path)
        + _status_report_gaps(status_report=status_report, status_report_path=config.status_report_path)
        + _remaining_deliverables_gaps(
            remaining_deliverables=remaining_deliverables,
            remaining_deliverables_path=config.remaining_deliverables_path,
            closure_checklist=closure_checklist,
            status_report=status_report,
        )
    )
    all_gaps = decision_gaps + training_gaps + evaluation_gaps + acceptance_gaps
    status = "formal_gate_ready_for_result_audit" if not all_gaps else "blocked_formal_gate_gaps_open"

    return {
        "schema_version": 1,
        "artifact_name": "module2_formal_gate_gap_audit",
        "status": status,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "remote_training_resource": _remote_training_resource(remote),
        "contract": {
            "path": str(config.contract_path),
            "status": contract.get("status"),
            "version": contract.get("version"),
            "approved_by": contract.get("approved_by"),
            "approved_date": contract.get("approved_date"),
        },
        "remote_readiness": _remote_readiness_record(config.remote_readiness_path, remote_readiness),
        "source_freshness": _source_freshness_record(config.source_freshness_path, source_freshness),
        "missing_artifacts_inventory": _missing_artifacts_record(config.missing_artifacts_path, missing_artifacts),
        "closure_checklist": _closure_checklist_record(config.closure_checklist_path, closure_checklist),
        "formal_gate_status_report": _status_report_record(config.status_report_path, status_report),
        "remaining_deliverables_ledger": _remaining_deliverables_record(config.remaining_deliverables_path, remaining_deliverables),
        "remaining_deliverables_gap_summary": _remaining_deliverables_gap_summary(remaining_deliverables),
        "status_report_remaining_deliverables_gap_summary": _normalize_gap_summary(
            status_report.get("remaining_deliverables_gap_summary")
        ),
        "closure_checklist_remaining_deliverables_gap_summary": _normalize_gap_summary(
            closure_checklist.get("remaining_deliverables_gap_summary")
        ),
        "current_gate_state": _current_gate_state(
            decision=decision,
            h01=h01,
            remote=remote,
            h02=h02,
            claim_safety=claim_safety,
            source_freshness=source_freshness,
            missing_artifacts=missing_artifacts,
            closure_checklist=closure_checklist,
            status_report=status_report,
            remaining_deliverables=remaining_deliverables,
            handoff_bundle=handoff_bundle,
            remote_packet_safety=remote_packet_safety,
        ),
        "missing_decision_items": decision_gaps,
        "missing_training_artifacts": training_gaps,
        "missing_evaluation_artifacts": evaluation_gaps,
        "missing_acceptance_artifacts": acceptance_gaps,
        "formal_gate_handoff": _handoff_bundle_record(config.handoff_bundle_path, handoff_bundle),
        "remote_packet_safety": _remote_packet_safety_record(config.remote_packet_safety_path, remote_packet_safety),
        "execution_veto_matrix": _execution_veto_matrix(
            decision=decision,
            remote=remote,
            status_report=status_report,
            handoff_bundle=handoff_bundle,
            remote_packet_safety=remote_packet_safety,
        ),
        "ordered_next_steps": _ordered_next_steps(decision_gaps, training_gaps, evaluation_gaps, acceptance_gaps, remote),
        "claim_boundaries": [
            "This audit is a formal-gate gap ledger, not a paper result, table, or appendix.",
            "Do not write performance-improvement or warm-start-effect claims from this artifact.",
            "No PPO/RL-RS formal training is allowed on the local Mac.",
            "Formal PPO checkpoint production must run on gpu3070ti-relay after F02.6 closes.",
            "Source freshness risks are regeneration blockers, not formal algorithm failures.",
            "Remote completion is insufficient until audit artifacts, checkpoint hashes, H01/H02 regeneration, and claim safety all pass.",
            "The closure checklist must be complete before the final claim gate can be treated as ready.",
            "The formal gate status report must be ready before the final claim gate can be treated as ready.",
            "The handoff bundle and remote packet safety audit must agree with the remote packet before any remote execution.",
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
    parser.add_argument("--remote-readiness-refresh", type=Path, default=DEFAULT_REMOTE_READINESS)
    parser.add_argument("--source-freshness-audit", type=Path, default=DEFAULT_SOURCE_FRESHNESS)
    parser.add_argument("--missing-artifacts-audit", type=Path, default=DEFAULT_MISSING_ARTIFACTS)
    parser.add_argument("--closure-checklist", type=Path, default=DEFAULT_CLOSURE_CHECKLIST)
    parser.add_argument("--status-report", type=Path, default=DEFAULT_STATUS_REPORT)
    parser.add_argument("--remaining-deliverables", type=Path, default=DEFAULT_REMAINING_DELIVERABLES)
    parser.add_argument("--handoff-bundle", type=Path, default=DEFAULT_HANDOFF_BUNDLE)
    parser.add_argument("--remote-packet-safety-audit", type=Path, default=DEFAULT_REMOTE_PACKET_SAFETY)
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


def _training_gaps(*, remote: dict[str, Any], h02: dict[str, Any], remote_readiness: dict[str, Any], remote_readiness_path: Path) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []
    gaps.extend(_remote_readiness_gaps(remote_readiness=remote_readiness, remote_readiness_path=remote_readiness_path))
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


def _remote_readiness_gaps(*, remote_readiness: dict[str, Any], remote_readiness_path: Path) -> list[dict[str, Any]]:
    if not Path(remote_readiness_path).is_file():
        return [
            _gap(
                "training",
                "remote_readiness_refresh_missing",
                "No gpu3070ti readiness refresh artifact is available for the formal gate.",
                str(remote_readiness_path),
                "Run a read-only gpu3070ti readiness refresh before approved remote preflight or training.",
            )
        ]
    gaps: list[dict[str, Any]] = []
    if remote_readiness.get("runs_training") is not False:
        gaps.append(
            _gap(
                "training",
                "remote_readiness_ran_training",
                "Readiness artifact claims it ran training; readiness checks must be read-only.",
                str(remote_readiness_path),
                "Replace with a read-only readiness refresh before using it as gate evidence.",
            )
        )
    if remote_readiness.get("runs_remote_preflight") is not False:
        gaps.append(
            _gap(
                "training",
                "remote_readiness_ran_preflight",
                "Readiness artifact claims it ran remote preflight while F02.6 may still be pending.",
                str(remote_readiness_path),
                "Keep readiness refresh separate from approved preflight execution.",
            )
        )
    if remote_readiness.get("local_training_allowed") is not False:
        gaps.append(
            _gap(
                "training",
                "remote_readiness_allows_local_training",
                "Readiness artifact does not preserve the local-training prohibition.",
                str(remote_readiness_path),
                "Regenerate readiness with local_training_allowed=false.",
            )
        )
    if remote_readiness.get("formal_claim_allowed") is not False:
        gaps.append(
            _gap(
                "training",
                "remote_readiness_allows_formal_claim",
                "Readiness artifact incorrectly allows formal claims.",
                str(remote_readiness_path),
                "Regenerate readiness as non-result evidence only.",
            )
        )
    if str(remote_readiness.get("remote_training_resource")) != "gpu3070ti-relay":
        gaps.append(
            _gap(
                "training",
                "remote_readiness_wrong_training_resource",
                f"Readiness artifact points at {remote_readiness.get('remote_training_resource')!r}, not gpu3070ti-relay.",
                str(remote_readiness_path),
                "Use gpu3070ti-relay for Module2 formal PPO unless the contract is explicitly changed.",
            )
        )
    for input_id in ("oracle_connector_results", "obstacle_summary_bc_checkpoint"):
        if not _critical_input_matches(remote_readiness, input_id):
            gaps.append(
                _gap(
                    "training",
                    f"remote_readiness_{input_id}_mismatch",
                    f"Readiness artifact does not prove local/remote match for {input_id}.",
                    str(remote_readiness_path),
                    "Refresh readiness and require local/remote bytes and SHA-256 to match before approved remote execution.",
                )
            )
    return gaps


def _source_freshness_gaps(*, source_freshness: dict[str, Any], source_freshness_path: Path) -> list[dict[str, Any]]:
    if not Path(source_freshness_path).is_file():
        return [
            _gap(
                "training",
                "source_freshness_audit_missing",
                "No source freshness audit is available for the formal gate.",
                str(source_freshness_path),
                "Regenerate the source freshness audit before approved remote preflight, H01/H02 regeneration, or formal claims.",
            )
        ]
    gaps: list[dict[str, Any]] = []
    if source_freshness.get("runs_training") is not False:
        gaps.append(
            _gap(
                "training",
                "source_freshness_audit_ran_training",
                "Source freshness audit claims it ran training; freshness checks must be read-only.",
                str(source_freshness_path),
                "Replace with a read-only source freshness audit before using it as gate evidence.",
            )
        )
    if source_freshness.get("runs_remote_preflight") is not False:
        gaps.append(
            _gap(
                "training",
                "source_freshness_audit_ran_preflight",
                "Source freshness audit claims it ran remote preflight; this audit must not execute preflight.",
                str(source_freshness_path),
                "Keep source freshness checks separate from approved remote preflight execution.",
            )
        )
    if source_freshness.get("local_training_allowed") is not False:
        gaps.append(
            _gap(
                "training",
                "source_freshness_allows_local_training",
                "Source freshness audit does not preserve the local-training prohibition.",
                str(source_freshness_path),
                "Regenerate source freshness with local_training_allowed=false.",
            )
        )
    if source_freshness.get("formal_claim_allowed") is not False:
        gaps.append(
            _gap(
                "training",
                "source_freshness_allows_formal_claim",
                "Source freshness audit incorrectly allows formal claims.",
                str(source_freshness_path),
                "Regenerate source freshness as non-result evidence only.",
            )
        )
    if _source_freshness_blocking_regeneration_required(source_freshness):
        gaps.append(
            _gap(
                "training",
                "source_freshness_regeneration_required",
                "Source freshness audit reports stale or dirty gate artifacts that must be regenerated before formal execution.",
                str(source_freshness_path),
                "After F02.6 closes, regenerate the listed targets before approved remote preflight, H01/H02, and formal claim gates.",
            )
        )
    return _unique_gaps(gaps)


def _handoff_bundle_gaps(*, handoff_bundle: dict[str, Any], handoff_bundle_path: Path, remote: dict[str, Any]) -> list[dict[str, Any]]:
    if not Path(handoff_bundle_path).is_file():
        return [
            _gap(
                "training",
                "handoff_bundle_missing",
                "No formal gate handoff bundle is available for execution veto cross-checking.",
                str(handoff_bundle_path),
                "Regenerate the read-only handoff bundle before approved remote preflight or formal training.",
            )
        ]
    gaps: list[dict[str, Any]] = []
    for key, gap_id, why in (
        ("executes_commands", "handoff_bundle_executes_commands", "Handoff bundle must be read-only and must not execute commands."),
        ("runs_training", "handoff_bundle_runs_training", "Handoff bundle claims it ran training; handoff must remain non-executing."),
        ("runs_remote_preflight", "handoff_bundle_runs_preflight", "Handoff bundle claims it ran remote preflight; handoff must remain non-executing."),
        ("local_training_allowed", "handoff_bundle_allows_local_training", "Handoff bundle does not preserve the local-training prohibition."),
        ("formal_claim_allowed", "handoff_bundle_allows_formal_claim", "Handoff bundle incorrectly allows formal claims."),
    ):
        if handoff_bundle.get(key) is not False:
            gaps.append(_gap("training", gap_id, why, str(handoff_bundle_path), "Regenerate handoff as a read-only non-result gate artifact."))

    if int(handoff_bundle.get("safety_issue_count") or 0) > 0:
        gaps.append(
            _gap(
                "training",
                "handoff_safety_issues_open",
                f"Handoff bundle reports {handoff_bundle.get('safety_issue_count')} safety issues.",
                str(handoff_bundle_path),
                "Resolve handoff safety issues before approved remote execution.",
            )
        )

    permissions = handoff_bundle.get("permissions_now") if isinstance(handoff_bundle.get("permissions_now"), dict) else {}
    current_state = handoff_bundle.get("current_state") if isinstance(handoff_bundle.get("current_state"), dict) else {}
    if current_state.get("decision_status") == "pending_human_decision":
        for permission_key in ("remote_preflight_allowed_now", "remote_training_allowed_now", "formal_claim_allowed_now"):
            if permissions.get(permission_key) is True:
                gaps.append(
                    _gap(
                        "training",
                        f"handoff_pending_allows_{permission_key}",
                        f"Handoff permission {permission_key} is true while F02.6 is still pending.",
                        str(handoff_bundle_path),
                        "Keep all executable and formal-claim permissions false until Dr Sun closes F02.6.",
                    )
                )

    handoff_steps = handoff_bundle.get("remote_execution_steps") if isinstance(handoff_bundle.get("remote_execution_steps"), dict) else {}
    if not handoff_steps:
        gaps.append(
            _gap(
                "training",
                "handoff_missing_remote_execution_steps",
                "Handoff bundle does not expose remote_execution_steps for cross-checking.",
                str(handoff_bundle_path),
                "Regenerate handoff with sync/preflight/training/audit step summaries.",
            )
        )
        return _unique_gaps(gaps)

    for step_id in REMOTE_EXECUTION_STEP_IDS:
        handoff_step = _step(handoff_steps, step_id)
        remote_step = _remote_packet_step(remote, step_id)
        if not handoff_step:
            gaps.append(
                _gap(
                    "training",
                    f"handoff_missing_{step_id}",
                    f"Handoff bundle is missing remote execution step {step_id}.",
                    str(handoff_bundle_path),
                    "Regenerate handoff with every remote packet step represented.",
                )
            )
            continue
        if step_id == "run_remote_training" and handoff_step.get("runs_training") is not True:
            gaps.append(
                _gap(
                    "training",
                    "handoff_training_step_not_marked_training",
                    "Handoff run_remote_training is not marked as the training step.",
                    str(handoff_bundle_path),
                    "Keep exactly the remote training step marked runs_training=true.",
                )
            )
        if step_id != "run_remote_training" and handoff_step.get("runs_training") is True:
            gaps.append(
                _gap(
                    "training",
                    f"handoff_{step_id}_claims_training",
                    f"Handoff {step_id} is incorrectly marked as training.",
                    str(handoff_bundle_path),
                    "Only run_remote_training may be marked as training.",
                )
            )
        if handoff_step.get("allowed_now") != remote_step.get("allowed_now"):
            gaps.append(
                _gap(
                    "training",
                    f"handoff_step_allowed_mismatch_{step_id}",
                    f"Handoff {step_id}.allowed_now={handoff_step.get('allowed_now')} does not match remote packet {remote_step.get('allowed_now')}.",
                    str(handoff_bundle_path),
                    "Regenerate handoff from the current remote execution packet.",
                )
            )
        if _strings(handoff_step.get("blocked_by")) != _strings(remote_step.get("blocked_by")):
            gaps.append(
                _gap(
                    "training",
                    f"handoff_step_blockers_mismatch_{step_id}",
                    f"Handoff {step_id}.blocked_by does not match the remote packet.",
                    str(handoff_bundle_path),
                    "Regenerate handoff from the current remote execution packet blockers.",
                )
            )
    return _unique_gaps(gaps)


def _remote_packet_safety_gaps(
    *,
    remote_packet_safety: dict[str, Any],
    remote_packet_safety_path: Path,
    remote: dict[str, Any],
) -> list[dict[str, Any]]:
    if not Path(remote_packet_safety_path).is_file():
        return [
            _gap(
                "training",
                "remote_packet_safety_audit_missing",
                "No remote packet safety audit is available for execution veto cross-checking.",
                str(remote_packet_safety_path),
                "Regenerate remote packet safety audit before approved remote preflight or formal training.",
            )
        ]
    gaps: list[dict[str, Any]] = []
    for key, gap_id, why in (
        ("executes_commands", "remote_packet_safety_executes_commands", "Remote packet safety audit must be read-only."),
        ("runs_training", "remote_packet_safety_runs_training", "Remote packet safety audit must not run training."),
        ("runs_remote_preflight", "remote_packet_safety_runs_preflight", "Remote packet safety audit must not run remote preflight."),
        ("local_training_allowed", "remote_packet_safety_allows_local_training", "Remote packet safety audit must preserve local-training prohibition."),
        ("formal_claim_allowed", "remote_packet_safety_allows_formal_claim", "Remote packet safety audit must not allow formal claims."),
    ):
        if remote_packet_safety.get(key) is not False:
            gaps.append(_gap("training", gap_id, why, str(remote_packet_safety_path), "Regenerate the audit as a read-only non-result gate artifact."))

    if remote_packet_safety.get("status") != "remote_packet_safety_audit_passed":
        gaps.append(
            _gap(
                "training",
                "remote_packet_safety_audit_failed",
                f"Remote packet safety audit status is {remote_packet_safety.get('status')}.",
                str(remote_packet_safety_path),
                "Fix the remote execution packet or post-plan/status cross-gates before approved remote execution.",
            )
        )
    if int(remote_packet_safety.get("audit_issue_count") or 0) > 0:
        gaps.append(
            _gap(
                "training",
                "remote_packet_safety_audit_issues_open",
                f"Remote packet safety audit reports {remote_packet_safety.get('audit_issue_count')} issues.",
                str(remote_packet_safety_path),
                "Resolve every remote packet safety issue before approved remote execution.",
            )
        )

    packet_summary = remote_packet_safety.get("packet_summary") if isinstance(remote_packet_safety.get("packet_summary"), dict) else {}
    command_index_summary = _remote_packet_safety_claim_gate_command_index_summary(remote_packet_safety)
    proof_summary = _remote_packet_safety_proof_deliverables_summary(remote_packet_safety)
    status_proof_summary = _remote_packet_safety_status_report_proof_deliverables_summary(remote_packet_safety)
    if not command_index_summary["present"]:
        gaps.append(
            _gap(
                "training",
                "remote_packet_safety_missing_claim_gate_command_index_summary",
                "Remote packet safety audit does not expose the post-plan source regeneration command index.",
                str(remote_packet_safety_path),
                "Regenerate remote packet safety audit from the current post-F02.6 plan audit.",
            )
        )
    if command_index_summary["missing_target_ids"]:
        gaps.append(
            _gap(
                "training",
                "remote_packet_safety_command_index_missing_targets",
                "Remote packet safety command index is missing source freshness targets.",
                str(remote_packet_safety_path),
                "Regenerate post-F02.6 plan and remote packet safety audit before formal gate use.",
            )
        )
    if command_index_summary["unknown_manual_count"] > 0:
        gaps.append(
            _gap(
                "training",
                "remote_packet_safety_command_index_unknown_manual_rows",
                "Remote packet safety command index contains unknown manual rows.",
                str(remote_packet_safety_path),
                "Keep claim-gate regeneration commands machine-resolved or explicitly whitelisted.",
            )
        )
    if command_index_summary["forbidden_command_count"] > 0:
        gaps.append(
            _gap(
                "training",
                "remote_packet_safety_command_index_forbidden_commands",
                "Remote packet safety command index contains execution/training commands.",
                str(remote_packet_safety_path),
                "Source-regeneration command index must remain read-only builder commands.",
            )
        )
    for artifact_id, row in command_index_summary["claim_gate_rows"].items():
        if not row["present"]:
            gaps.append(
                _gap(
                    "training",
                    f"remote_packet_safety_command_index_missing_{artifact_id}",
                    f"Remote packet safety command index does not include {artifact_id}.",
                    str(remote_packet_safety_path),
                    "Regenerate post-F02.6 plan and safety audit so claim-gate artifacts stay source-fresh before formal claims.",
                )
            )
            continue
        if row["stage_id"] != "regenerate_claim_gate_artifacts":
            gaps.append(
                _gap(
                    "training",
                    f"remote_packet_safety_command_index_{artifact_id}_wrong_stage",
                    f"{artifact_id} is assigned to {row['stage_id']} instead of regenerate_claim_gate_artifacts.",
                    str(remote_packet_safety_path),
                    "Keep claim-safety and paper-readiness regeneration in the claim-gate stage.",
                )
            )
        if row["required_before"] != "formal_claim_gate":
            gaps.append(
                _gap(
                    "training",
                    f"remote_packet_safety_command_index_{artifact_id}_wrong_required_before",
                    f"{artifact_id} has required_before={row['required_before']} instead of formal_claim_gate.",
                    str(remote_packet_safety_path),
                    "Keep claim-gate artifacts required before the formal claim gate.",
                )
            )
        if row["command_kind"] == "unknown_manual":
            gaps.append(
                _gap(
                    "training",
                    f"remote_packet_safety_command_index_{artifact_id}_manual_command",
                    f"{artifact_id} command is unknown/manual in the safety command index.",
                    str(remote_packet_safety_path),
                    "Use the known builder command for claim-gate artifact regeneration.",
                )
            )

    if not proof_summary["present"]:
        gaps.append(
            _gap(
                "training",
                "remote_packet_safety_missing_proof_deliverables_summary",
                "Remote packet safety audit does not expose post-plan proof-audit deliverables summary.",
                str(remote_packet_safety_path),
                "Regenerate remote packet safety audit from the current post-F02.6 plan audit.",
            )
        )
    if not status_proof_summary["present"]:
        gaps.append(
            _gap(
                "training",
                "remote_packet_safety_missing_status_report_proof_deliverables_summary",
                "Remote packet safety audit does not expose status-report proof-audit deliverables summary.",
                str(remote_packet_safety_path),
                "Regenerate remote packet safety audit from the current post-F02.6 plan audit and status report.",
            )
        )
    if (
        proof_summary["present"]
        and status_proof_summary["present"]
        and _proof_deliverables_signature(proof_summary) != _proof_deliverables_signature(status_proof_summary)
    ):
        gaps.append(
            _gap(
                "training",
                "remote_packet_safety_proof_deliverables_summary_mismatch",
                "Remote packet safety post-plan and status-report proof deliverable summaries disagree.",
                str(remote_packet_safety_path),
                "Regenerate remote packet safety audit after refreshing post-plan audit and status report.",
            )
        )
    if _proof_deliverables_open(proof_summary) and proof_summary.get("h02_paper_result_input_allowed") is True:
        gaps.append(
            _gap(
                "training",
                "remote_packet_safety_proof_deliverables_allow_h02_paper_input",
                "Remote packet safety proof summary allows H02 paper-result input while formal deliverables remain missing.",
                str(remote_packet_safety_path),
                "Keep H02 paper-result input blocked until the proof deliverables summary is closed.",
            )
        )

    if not packet_summary:
        gaps.append(
            _gap(
                "training",
                "remote_packet_safety_missing_packet_summary",
                "Remote packet safety audit does not expose packet_summary.",
                str(remote_packet_safety_path),
                "Regenerate safety audit with a remote packet summary.",
            )
        )
        return _unique_gaps(gaps)

    if packet_summary.get("status") != remote.get("status"):
        gaps.append(
            _gap(
                "training",
                "remote_packet_safety_stale_status",
                f"Safety audit packet status {packet_summary.get('status')} does not match remote packet {remote.get('status')}.",
                str(remote_packet_safety_path),
                "Regenerate safety audit from the current remote execution packet.",
            )
        )
    for step_id, (allowed_key, blocked_key) in REMOTE_PACKET_SAFETY_STEP_MAP.items():
        remote_step = _remote_packet_step(remote, step_id)
        if packet_summary.get(allowed_key) != remote_step.get("allowed_now"):
            gaps.append(
                _gap(
                    "training",
                    f"remote_packet_safety_allowed_mismatch_{step_id}",
                    f"Safety audit {allowed_key}={packet_summary.get(allowed_key)} does not match remote packet {remote_step.get('allowed_now')}.",
                    str(remote_packet_safety_path),
                    "Regenerate safety audit from the current remote execution packet.",
                )
            )
        if _strings(packet_summary.get(blocked_key)) != _strings(remote_step.get("blocked_by")):
            gaps.append(
                _gap(
                    "training",
                    f"remote_packet_safety_blockers_mismatch_{step_id}",
                    f"Safety audit {blocked_key} does not match remote packet blockers.",
                    str(remote_packet_safety_path),
                    "Regenerate safety audit from the current remote execution packet blockers.",
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


def _missing_artifacts_gaps(*, missing_artifacts: dict[str, Any], missing_artifacts_path: Path) -> list[dict[str, Any]]:
    if not Path(missing_artifacts_path).is_file():
        return [
            _gap(
                "acceptance",
                "formal_gate_missing_artifacts_audit_missing",
                "No formal gate missing-artifacts inventory is available for the final gate cross-check.",
                str(missing_artifacts_path),
                "Regenerate the missing-artifacts audit before treating the formal gate as complete.",
            )
        ]
    gaps: list[dict[str, Any]] = []
    if missing_artifacts.get("executes_commands") is not False:
        gaps.append(
            _gap(
                "acceptance",
                "formal_missing_artifacts_audit_executes_commands",
                "Missing-artifacts audit must be read-only and must not execute commands.",
                str(missing_artifacts_path),
                "Regenerate the inventory with executes_commands=false.",
            )
        )
    if missing_artifacts.get("runs_training") is not False:
        gaps.append(
            _gap(
                "acceptance",
                "formal_missing_artifacts_audit_runs_training",
                "Missing-artifacts audit claims it ran training; the inventory must remain non-executing.",
                str(missing_artifacts_path),
                "Replace it with a read-only inventory before using it as formal gate evidence.",
            )
        )
    if missing_artifacts.get("runs_remote_preflight") is not False:
        gaps.append(
            _gap(
                "acceptance",
                "formal_missing_artifacts_audit_runs_preflight",
                "Missing-artifacts audit claims it ran remote preflight; the inventory must remain non-executing.",
                str(missing_artifacts_path),
                "Replace it with a read-only inventory before using it as formal gate evidence.",
            )
        )
    if missing_artifacts.get("local_training_allowed") is not False:
        gaps.append(
            _gap(
                "acceptance",
                "formal_missing_artifacts_allows_local_training",
                "Missing-artifacts audit does not preserve the local-training prohibition.",
                str(missing_artifacts_path),
                "Regenerate the inventory with local_training_allowed=false.",
            )
        )
    if missing_artifacts.get("formal_claim_allowed") is not False:
        gaps.append(
            _gap(
                "acceptance",
                "formal_missing_artifacts_allows_claim",
                "Missing-artifacts audit incorrectly allows formal claims.",
                str(missing_artifacts_path),
                "Regenerate the inventory as non-result gate evidence.",
            )
        )
    if int(missing_artifacts.get("audit_issue_count") or 0) > 0:
        gaps.append(
            _gap(
                "acceptance",
                "formal_missing_artifacts_audit_issues_open",
                f"Missing-artifacts audit reports {missing_artifacts.get('audit_issue_count')} audit issues.",
                str(missing_artifacts_path),
                "Resolve the inventory audit issues before treating the formal gate as complete.",
            )
        )
    if missing_artifacts.get("all_required_evidence_present") is not True:
        counts = missing_artifacts.get("missing_counts_by_category") if isinstance(missing_artifacts.get("missing_counts_by_category"), dict) else {}
        gaps.append(
            _gap(
                "acceptance",
                "formal_gate_missing_artifacts_open",
                f"Formal gate inventory still reports missing evidence counts: {counts}.",
                str(missing_artifacts_path),
                "Close every missing-artifacts group before final H02/claim readiness can pass.",
            )
        )
    return _unique_gaps(gaps)


def _closure_checklist_gaps(*, closure_checklist: dict[str, Any], closure_checklist_path: Path) -> list[dict[str, Any]]:
    if not Path(closure_checklist_path).is_file():
        return [
            _gap(
                "acceptance",
                "formal_gate_closure_checklist_missing",
                "No formal gate closure checklist is available for the final gate cross-check.",
                str(closure_checklist_path),
                "Regenerate the closure checklist before treating the formal gate as complete.",
            )
        ]
    gaps: list[dict[str, Any]] = []
    if closure_checklist.get("executes_commands") is not False:
        gaps.append(
            _gap(
                "acceptance",
                "formal_closure_checklist_executes_commands",
                "Closure checklist must be read-only and must not execute commands.",
                str(closure_checklist_path),
                "Regenerate the checklist with executes_commands=false.",
            )
        )
    if closure_checklist.get("runs_training") is not False:
        gaps.append(
            _gap(
                "acceptance",
                "formal_closure_checklist_runs_training",
                "Closure checklist claims it ran training; the checklist must remain non-executing.",
                str(closure_checklist_path),
                "Replace it with a read-only checklist before using it as formal gate evidence.",
            )
        )
    if closure_checklist.get("runs_remote_preflight") is not False:
        gaps.append(
            _gap(
                "acceptance",
                "formal_closure_checklist_runs_preflight",
                "Closure checklist claims it ran remote preflight; the checklist must remain non-executing.",
                str(closure_checklist_path),
                "Replace it with a read-only checklist before using it as formal gate evidence.",
            )
        )
    if closure_checklist.get("local_training_allowed") is not False:
        gaps.append(
            _gap(
                "acceptance",
                "formal_closure_checklist_allows_local_training",
                "Closure checklist does not preserve the local-training prohibition.",
                str(closure_checklist_path),
                "Regenerate the checklist with local_training_allowed=false.",
            )
        )
    if closure_checklist.get("formal_claim_allowed") is not False:
        gaps.append(
            _gap(
                "acceptance",
                "formal_closure_checklist_allows_claim",
                "Closure checklist incorrectly allows formal claims.",
                str(closure_checklist_path),
                "Regenerate the checklist as non-result gate evidence.",
            )
        )
    if int(closure_checklist.get("input_safety_issue_count") or 0) > 0:
        gaps.append(
            _gap(
                "acceptance",
                "formal_closure_checklist_safety_issues_open",
                f"Closure checklist reports {closure_checklist.get('input_safety_issue_count')} input safety issues.",
                str(closure_checklist_path),
                "Resolve checklist input safety issues before treating the formal gate as complete.",
            )
        )
    if closure_checklist.get("status") != "formal_gate_closure_ready_for_result_audit":
        gaps.append(
            _gap(
                "acceptance",
                "formal_gate_closure_checklist_open",
                f"Closure checklist status is {closure_checklist.get('status')}; open_item_count={closure_checklist.get('open_item_count')}.",
                str(closure_checklist_path),
                "Close every checklist item before final H02/claim readiness can pass.",
            )
        )
    return _unique_gaps(gaps)


def _status_report_gaps(*, status_report: dict[str, Any], status_report_path: Path) -> list[dict[str, Any]]:
    if not Path(status_report_path).is_file():
        return [
            _gap(
                "acceptance",
                "formal_gate_status_report_missing",
                "No formal gate status report is available for the final gate cross-check.",
                str(status_report_path),
                "Regenerate the status report before treating the formal gate as complete.",
            )
        ]
    gaps: list[dict[str, Any]] = []
    if status_report.get("executes_commands") is not False:
        gaps.append(
            _gap(
                "acceptance",
                "formal_status_report_executes_commands",
                "Status report must be read-only and must not execute commands.",
                str(status_report_path),
                "Regenerate the status report with executes_commands=false.",
            )
        )
    if status_report.get("runs_training") is not False:
        gaps.append(
            _gap(
                "acceptance",
                "formal_status_report_runs_training",
                "Status report claims it ran training; the report must remain non-executing.",
                str(status_report_path),
                "Replace it with a read-only status report before using it as formal gate evidence.",
            )
        )
    if status_report.get("runs_remote_preflight") is not False:
        gaps.append(
            _gap(
                "acceptance",
                "formal_status_report_runs_preflight",
                "Status report claims it ran remote preflight; the report must remain non-executing.",
                str(status_report_path),
                "Replace it with a read-only status report before using it as formal gate evidence.",
            )
        )
    if status_report.get("local_training_allowed") is not False:
        gaps.append(
            _gap(
                "acceptance",
                "formal_status_report_allows_local_training",
                "Status report does not preserve the local-training prohibition.",
                str(status_report_path),
                "Regenerate the status report with local_training_allowed=false.",
            )
        )
    if status_report.get("formal_claim_allowed") is not False:
        gaps.append(
            _gap(
                "acceptance",
                "formal_status_report_allows_claim",
                "Status report artifact itself must not allow formal claims.",
                str(status_report_path),
                "Regenerate the status report as non-result gate evidence.",
            )
        )
    permissions = status_report.get("permissions_now") if isinstance(status_report.get("permissions_now"), dict) else {}
    if permissions.get("local_training_allowed_now") is True:
        gaps.append(
            _gap(
                "acceptance",
                "formal_status_report_allows_local_training_now",
                "Status report permissions allow local training.",
                str(status_report_path),
                "Regenerate status report and keep local_training_allowed_now=false.",
            )
        )
    if int(status_report.get("input_safety_issue_count") or 0) > 0:
        gaps.append(
            _gap(
                "acceptance",
                "formal_status_report_safety_issues_open",
                f"Status report has {status_report.get('input_safety_issue_count')} input safety issues.",
                str(status_report_path),
                "Resolve status report input safety issues before treating the formal gate as complete.",
            )
        )
    if status_report.get("status") != "formal_gate_status_ready_for_claim_audit":
        gaps.append(
            _gap(
                "acceptance",
                "formal_gate_status_report_blocked",
                f"Status report status is {status_report.get('status')}; formal_claim_allowed_now={permissions.get('formal_claim_allowed_now')}.",
                str(status_report_path),
                "Regenerate the status report only after all formal gate lanes are complete.",
            )
        )
    return _unique_gaps(gaps)


def _remaining_deliverables_gaps(
    *,
    remaining_deliverables: dict[str, Any],
    remaining_deliverables_path: Path,
    closure_checklist: dict[str, Any],
    status_report: dict[str, Any],
) -> list[dict[str, Any]]:
    if not Path(remaining_deliverables_path).is_file():
        return [
            _gap(
                "acceptance",
                "formal_gate_remaining_deliverables_missing",
                "No formal gate remaining-deliverables ledger is available for the final gate cross-check.",
                str(remaining_deliverables_path),
                "Regenerate the remaining-deliverables ledger before treating the formal gate as complete.",
            )
        ]
    gaps: list[dict[str, Any]] = []
    for key, gap_id, why in (
        ("executes_commands", "formal_remaining_deliverables_executes_commands", "Remaining-deliverables ledger must be read-only and must not execute commands."),
        ("runs_training", "formal_remaining_deliverables_runs_training", "Remaining-deliverables ledger claims it ran training; the ledger must remain non-executing."),
        ("runs_remote_preflight", "formal_remaining_deliverables_runs_preflight", "Remaining-deliverables ledger claims it ran remote preflight; the ledger must remain non-executing."),
        ("local_training_allowed", "formal_remaining_deliverables_allows_local_training", "Remaining-deliverables ledger does not preserve the local-training prohibition."),
        ("formal_claim_allowed", "formal_remaining_deliverables_allows_claim", "Remaining-deliverables ledger incorrectly allows formal claims."),
    ):
        if remaining_deliverables.get(key) is not False:
            gaps.append(
                _gap(
                    "acceptance",
                    gap_id,
                    why,
                    str(remaining_deliverables_path),
                    "Regenerate the ledger as a read-only non-result gate artifact.",
                )
            )
    if remaining_deliverables.get("not_paper_result_material") is not True:
        gaps.append(
            _gap(
                "acceptance",
                "formal_remaining_deliverables_marked_as_paper_result",
                "Remaining-deliverables ledger must be explicitly marked as non-paper-result material.",
                str(remaining_deliverables_path),
                "Regenerate the ledger with not_paper_result_material=true.",
            )
        )

    ledger_gap = _remaining_deliverables_gap_summary(remaining_deliverables)
    status_gap = _normalize_gap_summary(status_report.get("remaining_deliverables_gap_summary"))
    closure_gap = _normalize_gap_summary(closure_checklist.get("remaining_deliverables_gap_summary"))
    if not ledger_gap["present"]:
        gaps.append(
            _gap(
                "acceptance",
                "formal_remaining_deliverables_gap_summary_missing",
                "Remaining-deliverables ledger does not expose deliverable_gap_summary.",
                str(remaining_deliverables_path),
                "Regenerate the ledger with a normalized deliverable_gap_summary.",
            )
        )
    else:
        if ledger_gap.get("execution_boundary") != "read_only_no_execution":
            gaps.append(
                _gap(
                    "acceptance",
                    "formal_remaining_deliverables_gap_summary_execution_boundary_invalid",
                    "Remaining-deliverables gap summary must be read-only.",
                    str(remaining_deliverables_path),
                    "Regenerate the gap summary with execution_boundary=read_only_no_execution.",
                )
            )
        if ledger_gap.get("not_paper_result_material") is not True:
            gaps.append(
                _gap(
                    "acceptance",
                    "formal_remaining_deliverables_gap_summary_marked_as_paper_result",
                    "Remaining-deliverables gap summary must not be paper result material.",
                    str(remaining_deliverables_path),
                    "Regenerate the gap summary with not_paper_result_material=true.",
                )
            )
        if _gap_open(ledger_gap):
            gaps.append(
                _gap(
                    "acceptance",
                    "formal_gate_remaining_deliverables_open",
                    (
                        "Remaining-deliverables ledger still reports "
                        f"{ledger_gap['total_missing_deliverables']} missing deliverables across "
                        f"{ledger_gap['open_category_count']} open categories."
                    ),
                    str(remaining_deliverables_path),
                    "Produce the formal training, evaluation, acceptance, and H01/H02 acceptance artifacts before final claim readiness.",
                )
            )
    if not status_gap["present"]:
        gaps.append(
            _gap(
                "acceptance",
                "formal_status_report_missing_remaining_deliverables_gap_summary",
                "Status report does not expose remaining_deliverables_gap_summary for final gate cross-checking.",
                "0_trials/module2_formal_gate_status_report/formal_gate_status_report.json",
                "Regenerate the status report after the remaining-deliverables ledger.",
            )
        )
    elif ledger_gap["present"] and _gap_signature(status_gap) != _gap_signature(ledger_gap):
        gaps.append(
            _gap(
                "acceptance",
                "formal_status_report_remaining_deliverables_gap_summary_mismatch",
                "Status report remaining-deliverables gap summary disagrees with the ledger.",
                "0_trials/module2_formal_gate_status_report/formal_gate_status_report.json",
                "Regenerate the status report from the current remaining-deliverables ledger.",
            )
        )
    if not closure_gap["present"]:
        gaps.append(
            _gap(
                "acceptance",
                "formal_closure_checklist_missing_remaining_deliverables_gap_summary",
                "Closure checklist does not expose remaining_deliverables_gap_summary for final gate cross-checking.",
                "0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json",
                "Regenerate the closure checklist after the remaining-deliverables ledger.",
            )
        )
    elif ledger_gap["present"] and _gap_signature(closure_gap) != _gap_signature(ledger_gap):
        gaps.append(
            _gap(
                "acceptance",
                "formal_closure_checklist_remaining_deliverables_gap_summary_mismatch",
                "Closure checklist remaining-deliverables gap summary disagrees with the ledger.",
                "0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json",
                "Regenerate the closure checklist from the current remaining-deliverables ledger.",
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
    remote_readiness_gaps = _gaps_with_ids(
        training_gaps,
        {
            "remote_readiness_refresh_missing",
            "remote_readiness_ran_training",
            "remote_readiness_ran_preflight",
            "remote_readiness_allows_local_training",
            "remote_readiness_allows_formal_claim",
            "remote_readiness_wrong_training_resource",
            "remote_readiness_oracle_connector_results_mismatch",
            "remote_readiness_obstacle_summary_bc_checkpoint_mismatch",
        },
    )
    source_freshness_gaps = _gaps_with_ids(
        training_gaps,
        {
            "source_freshness_audit_missing",
            "source_freshness_audit_ran_training",
            "source_freshness_audit_ran_preflight",
            "source_freshness_allows_local_training",
            "source_freshness_allows_formal_claim",
            "source_freshness_regeneration_required",
        },
    )
    execution_veto_gaps = [
        gap
        for gap in training_gaps
        if str(gap.get("gap_id", "")).startswith("handoff_")
        or str(gap.get("gap_id", "")).startswith("remote_packet_safety_")
    ]
    remote_preflight_gaps = _gaps_with_ids(training_gaps, {"remote_training_packet_not_ready"})
    post_training_output_gaps = _gaps_with_ids(
        training_gaps,
        {
            "missing_remote_pullback_artifact",
            "missing_ppo_result_rows",
            "missing_ppo_checkpoint_hash",
        },
    )
    training_precondition_gaps = list(decision_gaps) + remote_readiness_gaps + source_freshness_gaps + remote_preflight_gaps
    audit_precondition_gaps = training_precondition_gaps + execution_veto_gaps + post_training_output_gaps
    evaluation_precondition_gaps = audit_precondition_gaps + list(evaluation_gaps)
    claim_precondition_gaps = evaluation_precondition_gaps + list(acceptance_gaps)
    steps.append(
        {
            "step_id": "F02.6",
            "phase": "decision",
            "status": "blocked" if decision_gaps else "complete",
            "blocked_by": _gap_ids(decision_gaps),
            "runs_training": False,
            "action": "Close Dr Sun's obstacle-summary warm-start decision record.",
            "evidence_to_update": "0_trials/module2_f02_6_decision_record/f02_6_decision_record.json",
        }
    )
    steps.append(
        {
            "step_id": "remote_preflight",
            "phase": "training",
            "status": "blocked" if decision_gaps or remote_readiness_gaps or source_freshness_gaps else "pending_execution",
            "blocked_by": _gap_ids(list(decision_gaps) + remote_readiness_gaps + source_freshness_gaps),
            "runs_training": False,
            "host": _remote_training_resource(remote),
            "action": "Regenerate source-fresh gate artifacts, then approved gpu3070ti preflight and require formal_trial_ready=true.",
            "evidence_to_update": "0_trials/module2_remote_preflight/gate3_obstacle_summary_warm_approved_remote_v1/gate3_preflight_manifest.json",
        }
    )
    steps.append(
        {
            "step_id": "gate3_remote_training",
            "phase": "training",
            "status": "blocked" if training_precondition_gaps else "pending_execution",
            "blocked_by": _gap_ids(training_precondition_gaps),
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
            "status": "blocked" if audit_precondition_gaps else "pending_execution",
            "blocked_by": _gap_ids(audit_precondition_gaps),
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
            "status": "blocked" if evaluation_precondition_gaps else "pending_execution",
            "blocked_by": _gap_ids(evaluation_precondition_gaps),
            "runs_training": False,
            "action": "Regenerate H01 with checkpoint and run H02 formal evaluation at H01 scale.",
            "evidence_to_update": "0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json",
        }
    )
    steps.append(
        {
            "step_id": "claim_safety_final_gate",
            "phase": "acceptance",
            "status": "blocked" if claim_precondition_gaps else "ready",
            "blocked_by": _gap_ids(claim_precondition_gaps),
            "runs_training": False,
            "action": "Regenerate claim safety/readiness; allow formal claims only if all gates pass.",
            "evidence_to_update": "0_trials/module2_claim_safety/module2_claim_safety.json",
        }
    )
    return steps


def _gaps_with_ids(gaps: Sequence[dict[str, Any]], ids: set[str]) -> list[dict[str, Any]]:
    return [gap for gap in gaps if str(gap.get("gap_id")) in ids]


def _gap_ids(gaps: Sequence[dict[str, Any]]) -> list[str]:
    seen: set[str] = set()
    ids: list[str] = []
    for gap in gaps:
        gap_id = str(gap.get("gap_id")) if gap.get("gap_id") else ""
        if not gap_id or gap_id in seen:
            continue
        seen.add(gap_id)
        ids.append(gap_id)
    return ids


def _current_gate_state(
    *,
    decision: dict[str, Any],
    h01: dict[str, Any],
    remote: dict[str, Any],
    h02: dict[str, Any],
    claim_safety: dict[str, Any],
    source_freshness: dict[str, Any],
    missing_artifacts: dict[str, Any],
    closure_checklist: dict[str, Any],
    status_report: dict[str, Any],
    remaining_deliverables: dict[str, Any],
    handoff_bundle: dict[str, Any],
    remote_packet_safety: dict[str, Any],
) -> dict[str, Any]:
    method_checks = h02.get("method_checks") if isinstance(h02.get("method_checks"), dict) else {}
    status_permissions = status_report.get("permissions_now") if isinstance(status_report.get("permissions_now"), dict) else {}
    handoff_permissions = handoff_bundle.get("permissions_now") if isinstance(handoff_bundle.get("permissions_now"), dict) else {}
    remaining_gap = _remaining_deliverables_gap_summary(remaining_deliverables)
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
        "source_freshness_status": source_freshness.get("status"),
        "source_freshness_regeneration_required": bool(source_freshness.get("regeneration_required_before_remote_formal_execution")),
        "source_freshness_blocking_regeneration_required": _source_freshness_blocking_regeneration_required(source_freshness),
        "formal_gate_missing_artifacts_status": missing_artifacts.get("status"),
        "formal_gate_missing_artifacts_open": missing_artifacts.get("all_required_evidence_present") is not True,
        "formal_gate_closure_checklist_status": closure_checklist.get("status"),
        "formal_gate_closure_checklist_open": closure_checklist.get("status") != "formal_gate_closure_ready_for_result_audit",
        "formal_gate_status_report_status": status_report.get("status"),
        "formal_gate_status_report_formal_claim_allowed_now": status_permissions.get("formal_claim_allowed_now"),
        "remaining_deliverables_status": remaining_deliverables.get("status"),
        "remaining_deliverables_gap_total_missing": remaining_gap.get("total_missing_deliverables"),
        "remaining_deliverables_gap_open_category_count": remaining_gap.get("open_category_count"),
        "formal_gate_handoff_status": handoff_bundle.get("status"),
        "formal_gate_handoff_safety_issue_count": handoff_bundle.get("safety_issue_count"),
        "formal_gate_handoff_remote_training_allowed_now": handoff_permissions.get("remote_training_allowed_now"),
        "remote_packet_safety_status": remote_packet_safety.get("status"),
        "remote_packet_safety_audit_issue_count": remote_packet_safety.get("audit_issue_count"),
    }


def _remote_readiness_record(path: Path, readiness: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": str(path),
        "exists": Path(path).is_file(),
        "status": readiness.get("status"),
        "runs_training": readiness.get("runs_training"),
        "runs_remote_preflight": readiness.get("runs_remote_preflight"),
        "local_training_allowed": readiness.get("local_training_allowed"),
        "formal_claim_allowed": readiness.get("formal_claim_allowed"),
        "remote_training_resource": readiness.get("remote_training_resource"),
        "oracle_connector_results_match": _critical_input_matches(readiness, "oracle_connector_results"),
        "obstacle_summary_bc_checkpoint_match": _critical_input_matches(readiness, "obstacle_summary_bc_checkpoint"),
    }


def _source_freshness_record(path: Path, source_freshness: dict[str, Any]) -> dict[str, Any]:
    targets = source_freshness.get("ordered_regeneration_targets")
    ordered_targets = targets if isinstance(targets, list) else []
    return {
        "path": str(path),
        "exists": Path(path).is_file(),
        "status": source_freshness.get("status"),
        "runs_training": source_freshness.get("runs_training"),
        "runs_remote_preflight": source_freshness.get("runs_remote_preflight"),
        "local_training_allowed": source_freshness.get("local_training_allowed"),
        "formal_claim_allowed": source_freshness.get("formal_claim_allowed"),
        "regeneration_required_before_remote_formal_execution": source_freshness.get("regeneration_required_before_remote_formal_execution"),
        "blocking_regeneration_required_before_remote_formal_execution": _source_freshness_blocking_regeneration_required(source_freshness),
        "risk_counts": source_freshness.get("risk_counts") if isinstance(source_freshness.get("risk_counts"), dict) else {},
        "ordered_regeneration_target_count": len(ordered_targets),
        "ordered_regeneration_targets": ordered_targets,
    }


def _source_freshness_blocking_regeneration_required(source_freshness: dict[str, Any]) -> bool:
    if "blocking_regeneration_required_before_remote_formal_execution" in source_freshness:
        return source_freshness.get("blocking_regeneration_required_before_remote_formal_execution") is True
    return source_freshness.get("regeneration_required_before_remote_formal_execution") is True


def _missing_artifacts_record(path: Path, missing_artifacts: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": str(path),
        "exists": Path(path).is_file(),
        "status": missing_artifacts.get("status"),
        "executes_commands": missing_artifacts.get("executes_commands"),
        "runs_training": missing_artifacts.get("runs_training"),
        "runs_remote_preflight": missing_artifacts.get("runs_remote_preflight"),
        "local_training_allowed": missing_artifacts.get("local_training_allowed"),
        "formal_claim_allowed": missing_artifacts.get("formal_claim_allowed"),
        "all_required_evidence_present": missing_artifacts.get("all_required_evidence_present"),
        "audit_issue_count": missing_artifacts.get("audit_issue_count"),
        "missing_counts_by_category": missing_artifacts.get("missing_counts_by_category")
        if isinstance(missing_artifacts.get("missing_counts_by_category"), dict)
        else {},
    }


def _closure_checklist_record(path: Path, closure_checklist: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": str(path),
        "exists": Path(path).is_file(),
        "status": closure_checklist.get("status"),
        "executes_commands": closure_checklist.get("executes_commands"),
        "runs_training": closure_checklist.get("runs_training"),
        "runs_remote_preflight": closure_checklist.get("runs_remote_preflight"),
        "local_training_allowed": closure_checklist.get("local_training_allowed"),
        "formal_claim_allowed": closure_checklist.get("formal_claim_allowed"),
        "closure_item_count": closure_checklist.get("closure_item_count"),
        "open_item_count": closure_checklist.get("open_item_count"),
        "input_safety_issue_count": closure_checklist.get("input_safety_issue_count"),
    }


def _status_report_record(path: Path, status_report: dict[str, Any]) -> dict[str, Any]:
    permissions = status_report.get("permissions_now") if isinstance(status_report.get("permissions_now"), dict) else {}
    next_blocked_lane = status_report.get("next_blocked_lane") if isinstance(status_report.get("next_blocked_lane"), dict) else {}
    return {
        "path": str(path),
        "exists": Path(path).is_file(),
        "status": status_report.get("status"),
        "executes_commands": status_report.get("executes_commands"),
        "runs_training": status_report.get("runs_training"),
        "runs_remote_preflight": status_report.get("runs_remote_preflight"),
        "local_training_allowed": status_report.get("local_training_allowed"),
        "formal_claim_allowed": status_report.get("formal_claim_allowed"),
        "formal_claim_allowed_now": permissions.get("formal_claim_allowed_now"),
        "local_training_allowed_now": permissions.get("local_training_allowed_now"),
        "next_blocked_lane_id": next_blocked_lane.get("lane_id"),
        "input_safety_issue_count": status_report.get("input_safety_issue_count"),
    }


def _remaining_deliverables_record(path: Path, remaining_deliverables: dict[str, Any]) -> dict[str, Any]:
    gap = _remaining_deliverables_gap_summary(remaining_deliverables)
    return {
        "path": str(path),
        "exists": Path(path).is_file(),
        "status": remaining_deliverables.get("status"),
        "executes_commands": remaining_deliverables.get("executes_commands"),
        "runs_training": remaining_deliverables.get("runs_training"),
        "runs_remote_preflight": remaining_deliverables.get("runs_remote_preflight"),
        "local_training_allowed": remaining_deliverables.get("local_training_allowed"),
        "formal_claim_allowed": remaining_deliverables.get("formal_claim_allowed"),
        "not_paper_result_material": remaining_deliverables.get("not_paper_result_material"),
        "gap_summary_present": gap["present"],
        "gap_total_missing_deliverables": gap["total_missing_deliverables"],
        "gap_open_category_count": gap["open_category_count"],
    }


def _handoff_bundle_record(path: Path, handoff_bundle: dict[str, Any]) -> dict[str, Any]:
    permissions = handoff_bundle.get("permissions_now") if isinstance(handoff_bundle.get("permissions_now"), dict) else {}
    next_action = handoff_bundle.get("next_handoff_action") if isinstance(handoff_bundle.get("next_handoff_action"), dict) else {}
    return {
        "path": str(path),
        "exists": Path(path).is_file(),
        "status": handoff_bundle.get("status"),
        "executes_commands": handoff_bundle.get("executes_commands"),
        "runs_training": handoff_bundle.get("runs_training"),
        "runs_remote_preflight": handoff_bundle.get("runs_remote_preflight"),
        "local_training_allowed": handoff_bundle.get("local_training_allowed"),
        "formal_claim_allowed": handoff_bundle.get("formal_claim_allowed"),
        "safety_issue_count": handoff_bundle.get("safety_issue_count"),
        "next_handoff_action_id": next_action.get("action_id"),
        "remote_preflight_allowed_now": permissions.get("remote_preflight_allowed_now"),
        "remote_training_allowed_now": permissions.get("remote_training_allowed_now"),
        "formal_claim_allowed_now": permissions.get("formal_claim_allowed_now"),
        "remote_execution_steps": _remote_steps_record(handoff_bundle.get("remote_execution_steps")),
    }


def _remote_packet_safety_record(path: Path, remote_packet_safety: dict[str, Any]) -> dict[str, Any]:
    packet_summary = remote_packet_safety.get("packet_summary") if isinstance(remote_packet_safety.get("packet_summary"), dict) else {}
    return {
        "path": str(path),
        "exists": Path(path).is_file(),
        "status": remote_packet_safety.get("status"),
        "executes_commands": remote_packet_safety.get("executes_commands"),
        "runs_training": remote_packet_safety.get("runs_training"),
        "runs_remote_preflight": remote_packet_safety.get("runs_remote_preflight"),
        "local_training_allowed": remote_packet_safety.get("local_training_allowed"),
        "formal_claim_allowed": remote_packet_safety.get("formal_claim_allowed"),
        "audit_issue_count": remote_packet_safety.get("audit_issue_count"),
        "packet_status": packet_summary.get("status"),
        "remote_preflight_allowed_now": packet_summary.get("remote_preflight_allowed_now"),
        "remote_training_allowed_now": packet_summary.get("remote_training_allowed_now"),
        "remote_audit_allowed_now": packet_summary.get("remote_audit_allowed_now"),
        "claim_gate_command_index_summary": _remote_packet_safety_claim_gate_command_index_summary(remote_packet_safety),
        "proof_deliverables_summary": _remote_packet_safety_proof_deliverables_summary(remote_packet_safety),
        "status_report_proof_deliverables_summary": _remote_packet_safety_status_report_proof_deliverables_summary(remote_packet_safety),
    }


def _remote_packet_safety_claim_gate_command_index_summary(remote_packet_safety: dict[str, Any]) -> dict[str, Any]:
    cross_gate = remote_packet_safety.get("cross_gate_summary") if isinstance(remote_packet_safety.get("cross_gate_summary"), dict) else {}
    summary = (
        cross_gate.get("post_plan_source_regeneration_command_index_summary")
        if isinstance(cross_gate.get("post_plan_source_regeneration_command_index_summary"), dict)
        else {}
    )
    rows = summary.get("rows") if isinstance(summary.get("rows"), dict) else {}
    claim_gate_rows: dict[str, dict[str, Any]] = {}
    for artifact_id in CLAIM_GATE_REGENERATION_ARTIFACT_IDS:
        row = rows.get(artifact_id) if isinstance(rows.get(artifact_id), dict) else {}
        claim_gate_rows[artifact_id] = {
            "present": bool(row),
            "stage_id": row.get("stage_id"),
            "required_before": row.get("required_before"),
            "command_kind": row.get("command_kind"),
            "command_template": row.get("command_template"),
        }
    return {
        "present": bool(summary),
        "index_row_count": int(summary.get("index_row_count") or 0),
        "source_target_count": int(summary.get("source_target_count") or 0),
        "missing_target_ids": _strings(summary.get("missing_target_ids")),
        "unknown_manual_count": int(summary.get("unknown_manual_count") or 0),
        "unknown_manual_ids": _strings(summary.get("unknown_manual_ids")),
        "forbidden_command_count": int(summary.get("forbidden_command_count") or 0),
        "forbidden_command_ids": _strings(summary.get("forbidden_command_ids")),
        "claim_gate_rows": claim_gate_rows,
    }


def _remote_packet_safety_proof_deliverables_summary(remote_packet_safety: dict[str, Any]) -> dict[str, Any]:
    cross_gate = remote_packet_safety.get("cross_gate_summary") if isinstance(remote_packet_safety.get("cross_gate_summary"), dict) else {}
    return _normalize_proof_deliverables_summary(cross_gate.get("post_plan_proof_audit_deliverables_summary"))


def _remote_packet_safety_status_report_proof_deliverables_summary(remote_packet_safety: dict[str, Any]) -> dict[str, Any]:
    cross_gate = remote_packet_safety.get("cross_gate_summary") if isinstance(remote_packet_safety.get("cross_gate_summary"), dict) else {}
    return _normalize_proof_deliverables_summary(cross_gate.get("post_plan_status_report_proof_audit_deliverables_summary"))


def _normalize_proof_deliverables_summary(raw: Any) -> dict[str, Any]:
    summary = raw if isinstance(raw, dict) else {}
    counts = summary.get("missing_counts_by_formal_category")
    ids_by_category = summary.get("missing_matrix_ids_by_formal_category")
    return {
        "present": bool(summary),
        "missing_counts_by_formal_category": {
            str(category): int(count or 0)
            for category, count in counts.items()
            if category
        }
        if isinstance(counts, dict)
        else {},
        "missing_matrix_ids_by_formal_category": {
            str(category): [str(item) for item in ids if item]
            for category, ids in ids_by_category.items()
            if category and isinstance(ids, list)
        }
        if isinstance(ids_by_category, dict)
        else {},
        "next_blocked_lane": summary.get("next_blocked_lane"),
        "h01_status": summary.get("h01_status"),
        "h02_status": summary.get("h02_status"),
        "h02_formal_output_accepted": summary.get("h02_formal_output_accepted")
        if isinstance(summary.get("h02_formal_output_accepted"), bool)
        else None,
        "h02_paper_result_input_allowed": summary.get("h02_paper_result_input_allowed")
        if isinstance(summary.get("h02_paper_result_input_allowed"), bool)
        else None,
    }


def _proof_deliverables_signature(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "missing_counts_by_formal_category": {
            key: summary["missing_counts_by_formal_category"].get(key)
            for key in sorted(summary.get("missing_counts_by_formal_category", {}))
        },
        "missing_matrix_ids_by_formal_category": {
            key: summary["missing_matrix_ids_by_formal_category"].get(key, [])
            for key in sorted(summary.get("missing_matrix_ids_by_formal_category", {}))
        },
        "next_blocked_lane": summary.get("next_blocked_lane"),
        "h01_status": summary.get("h01_status"),
        "h02_status": summary.get("h02_status"),
        "h02_formal_output_accepted": summary.get("h02_formal_output_accepted"),
        "h02_paper_result_input_allowed": summary.get("h02_paper_result_input_allowed"),
    }


def _proof_deliverables_open(summary: dict[str, Any]) -> bool:
    return sum(int(count) for count in summary.get("missing_counts_by_formal_category", {}).values()) > 0


def _execution_veto_matrix(
    *,
    decision: dict[str, Any],
    remote: dict[str, Any],
    status_report: dict[str, Any],
    handoff_bundle: dict[str, Any],
    remote_packet_safety: dict[str, Any],
) -> dict[str, Any]:
    status_permissions = status_report.get("permissions_now") if isinstance(status_report.get("permissions_now"), dict) else {}
    handoff_permissions = handoff_bundle.get("permissions_now") if isinstance(handoff_bundle.get("permissions_now"), dict) else {}
    safety_summary = remote_packet_safety.get("packet_summary") if isinstance(remote_packet_safety.get("packet_summary"), dict) else {}
    rows = [
        _veto_row(
            "local_training",
            {
                "formal_gate_gap_audit": False,
                "status_report": status_permissions.get("local_training_allowed_now"),
                "handoff_bundle": handoff_permissions.get("local_training_allowed_now"),
                "remote_packet": remote.get("local_training_allowed"),
            },
        ),
        _veto_row(
            "remote_preflight",
            {
                "status_report": status_permissions.get("remote_preflight_allowed_now"),
                "remote_packet": _remote_packet_step(remote, "run_remote_preflight").get("allowed_now"),
            },
        ),
        _veto_row(
            "remote_training",
            {
                "decision_record": decision.get("remote_training_allowed"),
                "status_report": status_permissions.get("remote_training_allowed_now"),
                "remote_packet": _remote_packet_step(remote, "run_remote_training").get("allowed_now"),
            },
        ),
        _veto_row(
            "remote_audit",
            {
                "handoff_bundle": _step(handoff_bundle.get("remote_execution_steps"), "run_remote_audit").get("allowed_now"),
                "remote_packet": _remote_packet_step(remote, "run_remote_audit").get("allowed_now"),
                "remote_packet_safety": safety_summary.get("remote_audit_allowed_now"),
            },
        ),
        _veto_row(
            "formal_claim",
            {
                "status_report": status_permissions.get("formal_claim_allowed_now"),
                "handoff_bundle": handoff_permissions.get("formal_claim_allowed_now"),
            },
        ),
    ]
    mismatches = [row["row_id"] for row in rows if not row["consistent"]]
    return {
        "matrix_version": 1,
        "f02_6_decision_status": decision.get("status"),
        "all_rows_consistent": not mismatches,
        "mismatch_rows": mismatches,
        "rows": rows,
    }


def _veto_row(row_id: str, sources: dict[str, Any]) -> dict[str, Any]:
    normalized = {
        key: value if isinstance(value, bool) else None
        for key, value in sources.items()
    }
    observed = [value for value in normalized.values() if value is not None]
    distinct = set(observed)
    return {
        "row_id": row_id,
        "allowed_now_by_source": normalized,
        "consistent": len(distinct) <= 1,
        "consensus_allowed_now": bool(observed) and distinct == {True},
    }


def _remote_steps_record(steps: Any) -> dict[str, dict[str, Any]]:
    return {
        step_id: {
            "present": bool(_step(steps, step_id)),
            "allowed_now": _step(steps, step_id).get("allowed_now"),
            "runs_training": _step(steps, step_id).get("runs_training"),
            "blocked_by": _strings(_step(steps, step_id).get("blocked_by")),
        }
        for step_id in REMOTE_EXECUTION_STEP_IDS
    }


def _critical_input_matches(readiness: dict[str, Any], input_id: str) -> bool:
    critical_inputs = readiness.get("critical_inputs") if isinstance(readiness.get("critical_inputs"), dict) else {}
    item = critical_inputs.get(input_id) if isinstance(critical_inputs.get(input_id), dict) else {}
    return item.get("local_remote_match") is True


def _remaining_deliverables_gap_summary(remaining_deliverables: dict[str, Any]) -> dict[str, Any]:
    return _normalize_gap_summary(remaining_deliverables.get("deliverable_gap_summary"))


def _normalize_gap_summary(raw: Any) -> dict[str, Any]:
    summary = raw if isinstance(raw, dict) else {}
    categories = _normalize_gap_categories(summary.get("categories"))
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


def _normalize_gap_categories(raw_categories: Any) -> dict[str, dict[str, Any]]:
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
        matrix_ids = raw.get("missing_artifact_matrix_ids")
        if not isinstance(matrix_ids, list):
            missing_artifacts = raw.get("missing_artifacts") if isinstance(raw.get("missing_artifacts"), list) else []
            matrix_ids = [item.get("matrix_id") for item in missing_artifacts if isinstance(item, dict)]
        out[str(category)] = {
            "missing_count": int(raw.get("missing_count") or 0),
            "responsible_stage_id": raw.get("responsible_stage_id"),
            "responsible_stage_allowed_now": raw.get("responsible_stage_allowed_now"),
            "missing_artifact_matrix_ids": [str(item) for item in matrix_ids if item],
        }
    return out


def _gap_signature(summary: dict[str, Any]) -> dict[str, Any]:
    categories = summary.get("categories") if isinstance(summary.get("categories"), dict) else {}
    return {
        "summary_id": summary.get("summary_id"),
        "total_missing_deliverables": summary.get("total_missing_deliverables"),
        "open_category_count": summary.get("open_category_count"),
        "categories": {
            key: {
                "missing_count": value.get("missing_count"),
                "responsible_stage_id": value.get("responsible_stage_id"),
                "missing_artifact_matrix_ids": value.get("missing_artifact_matrix_ids", []),
            }
            for key, value in sorted(categories.items())
            if isinstance(value, dict)
        },
    }


def _gap_open(summary: dict[str, Any]) -> bool:
    return int(summary.get("total_missing_deliverables") or 0) > 0 or int(summary.get("open_category_count") or 0) > 0


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
        "## Remote Readiness",
        "",
        f"- path: `{manifest['remote_readiness']['path']}`",
        f"- status: `{manifest['remote_readiness']['status']}`",
        f"- runs_training: `{manifest['remote_readiness']['runs_training']}`",
        f"- runs_remote_preflight: `{manifest['remote_readiness']['runs_remote_preflight']}`",
        f"- oracle_connector_results_match: `{manifest['remote_readiness']['oracle_connector_results_match']}`",
        f"- obstacle_summary_bc_checkpoint_match: `{manifest['remote_readiness']['obstacle_summary_bc_checkpoint_match']}`",
        "",
        "## Source Freshness",
        "",
        f"- path: `{manifest['source_freshness']['path']}`",
        f"- status: `{manifest['source_freshness']['status']}`",
        f"- runs_training: `{manifest['source_freshness']['runs_training']}`",
        f"- runs_remote_preflight: `{manifest['source_freshness']['runs_remote_preflight']}`",
        f"- formal_claim_allowed: `{manifest['source_freshness']['formal_claim_allowed']}`",
        f"- regeneration_required_before_remote_formal_execution: `{manifest['source_freshness']['regeneration_required_before_remote_formal_execution']}`",
        f"- ordered_regeneration_target_count: `{manifest['source_freshness']['ordered_regeneration_target_count']}`",
        "",
    ]
    if manifest["source_freshness"]["ordered_regeneration_targets"]:
        lines.extend(["### Source Freshness Regeneration Targets", ""])
        for target in manifest["source_freshness"]["ordered_regeneration_targets"]:
            if not isinstance(target, dict):
                continue
            lines.append(
                f"- `{target.get('artifact_id')}`: `{target.get('freshness_state')}`, "
                f"required before `{target.get('required_before')}`, path `{target.get('path')}`"
            )
        lines.append("")
    lines.extend(
        [
            "## Missing Artifacts Inventory",
            "",
            f"- path: `{manifest['missing_artifacts_inventory']['path']}`",
            f"- status: `{manifest['missing_artifacts_inventory']['status']}`",
            f"- executes_commands: `{manifest['missing_artifacts_inventory']['executes_commands']}`",
            f"- runs_training: `{manifest['missing_artifacts_inventory']['runs_training']}`",
            f"- runs_remote_preflight: `{manifest['missing_artifacts_inventory']['runs_remote_preflight']}`",
            f"- all_required_evidence_present: `{manifest['missing_artifacts_inventory']['all_required_evidence_present']}`",
            f"- audit_issue_count: `{manifest['missing_artifacts_inventory']['audit_issue_count']}`",
            f"- missing_counts_by_category: `{manifest['missing_artifacts_inventory']['missing_counts_by_category']}`",
            "",
            "## Closure Checklist",
            "",
            f"- path: `{manifest['closure_checklist']['path']}`",
            f"- status: `{manifest['closure_checklist']['status']}`",
            f"- executes_commands: `{manifest['closure_checklist']['executes_commands']}`",
            f"- runs_training: `{manifest['closure_checklist']['runs_training']}`",
            f"- runs_remote_preflight: `{manifest['closure_checklist']['runs_remote_preflight']}`",
            f"- open_item_count: `{manifest['closure_checklist']['open_item_count']}`",
            f"- input_safety_issue_count: `{manifest['closure_checklist']['input_safety_issue_count']}`",
            "",
            "## Formal Gate Status Report",
            "",
            f"- path: `{manifest['formal_gate_status_report']['path']}`",
            f"- status: `{manifest['formal_gate_status_report']['status']}`",
            f"- executes_commands: `{manifest['formal_gate_status_report']['executes_commands']}`",
            f"- runs_training: `{manifest['formal_gate_status_report']['runs_training']}`",
            f"- runs_remote_preflight: `{manifest['formal_gate_status_report']['runs_remote_preflight']}`",
            f"- local_training_allowed_now: `{manifest['formal_gate_status_report']['local_training_allowed_now']}`",
            f"- formal_claim_allowed_now: `{manifest['formal_gate_status_report']['formal_claim_allowed_now']}`",
            f"- next_blocked_lane_id: `{manifest['formal_gate_status_report']['next_blocked_lane_id']}`",
            f"- input_safety_issue_count: `{manifest['formal_gate_status_report']['input_safety_issue_count']}`",
            "",
            "## Remaining Deliverables Ledger",
            "",
            f"- path: `{manifest['remaining_deliverables_ledger']['path']}`",
            f"- status: `{manifest['remaining_deliverables_ledger']['status']}`",
            f"- executes_commands: `{manifest['remaining_deliverables_ledger']['executes_commands']}`",
            f"- runs_training: `{manifest['remaining_deliverables_ledger']['runs_training']}`",
            f"- runs_remote_preflight: `{manifest['remaining_deliverables_ledger']['runs_remote_preflight']}`",
            f"- formal_claim_allowed: `{manifest['remaining_deliverables_ledger']['formal_claim_allowed']}`",
            f"- gap_total_missing_deliverables: `{manifest['remaining_deliverables_ledger']['gap_total_missing_deliverables']}`",
            f"- gap_open_category_count: `{manifest['remaining_deliverables_ledger']['gap_open_category_count']}`",
            "",
            "## Remaining Deliverables Gap Summary",
            "",
            f"- total_missing_deliverables: `{manifest['remaining_deliverables_gap_summary']['total_missing_deliverables']}`",
            f"- open_category_count: `{manifest['remaining_deliverables_gap_summary']['open_category_count']}`",
            f"- status_report_total_missing: `{manifest['status_report_remaining_deliverables_gap_summary']['total_missing_deliverables']}`",
            f"- closure_total_missing: `{manifest['closure_checklist_remaining_deliverables_gap_summary']['total_missing_deliverables']}`",
            "",
        ]
    )
    for category in manifest["remaining_deliverables_gap_summary"]["category_order"]:
        item = manifest["remaining_deliverables_gap_summary"]["categories"].get(category, {})
        lines.append(
            f"- `{category}`: missing=`{item.get('missing_count')}`, "
            f"responsible_stage=`{item.get('responsible_stage_id')}`"
        )
    lines.extend(
        [
            "",
            "## Formal Gate Handoff",
            "",
            f"- path: `{manifest['formal_gate_handoff']['path']}`",
            f"- status: `{manifest['formal_gate_handoff']['status']}`",
            f"- executes_commands: `{manifest['formal_gate_handoff']['executes_commands']}`",
            f"- runs_training: `{manifest['formal_gate_handoff']['runs_training']}`",
            f"- runs_remote_preflight: `{manifest['formal_gate_handoff']['runs_remote_preflight']}`",
            f"- remote_training_allowed_now: `{manifest['formal_gate_handoff']['remote_training_allowed_now']}`",
            f"- formal_claim_allowed_now: `{manifest['formal_gate_handoff']['formal_claim_allowed_now']}`",
            f"- safety_issue_count: `{manifest['formal_gate_handoff']['safety_issue_count']}`",
            f"- next_handoff_action_id: `{manifest['formal_gate_handoff']['next_handoff_action_id']}`",
            "",
            "## Remote Packet Safety",
            "",
            f"- path: `{manifest['remote_packet_safety']['path']}`",
            f"- status: `{manifest['remote_packet_safety']['status']}`",
            f"- executes_commands: `{manifest['remote_packet_safety']['executes_commands']}`",
            f"- runs_training: `{manifest['remote_packet_safety']['runs_training']}`",
            f"- runs_remote_preflight: `{manifest['remote_packet_safety']['runs_remote_preflight']}`",
            f"- packet_status: `{manifest['remote_packet_safety']['packet_status']}`",
            f"- remote_training_allowed_now: `{manifest['remote_packet_safety']['remote_training_allowed_now']}`",
            f"- audit_issue_count: `{manifest['remote_packet_safety']['audit_issue_count']}`",
            f"- command_index_present: `{manifest['remote_packet_safety']['claim_gate_command_index_summary']['present']}`",
            f"- command_index_row_count: `{manifest['remote_packet_safety']['claim_gate_command_index_summary']['index_row_count']}`",
            f"- command_index_missing_target_ids: `{manifest['remote_packet_safety']['claim_gate_command_index_summary']['missing_target_ids']}`",
            f"- proof_deliverables_missing_counts: `{manifest['remote_packet_safety']['proof_deliverables_summary']['missing_counts_by_formal_category']}`",
            f"- proof_deliverables_h02_paper_result_input_allowed: `{manifest['remote_packet_safety']['proof_deliverables_summary']['h02_paper_result_input_allowed']}`",
            "",
            "## Execution Veto Matrix",
            "",
            f"- all_rows_consistent: `{manifest['execution_veto_matrix']['all_rows_consistent']}`",
            f"- mismatch_rows: `{manifest['execution_veto_matrix']['mismatch_rows']}`",
            "",
        ]
    )
    for row in manifest["execution_veto_matrix"]["rows"]:
        lines.append(
            f"- `{row['row_id']}`: consistent=`{row['consistent']}`, "
            f"consensus_allowed_now=`{row['consensus_allowed_now']}`, sources=`{row['allowed_now_by_source']}`"
        )
    lines.append("")
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


def _step(steps: Any, step_id: str) -> dict[str, Any]:
    if not isinstance(steps, dict):
        return {}
    item = steps.get(step_id)
    return item if isinstance(item, dict) else {}


def _remote_packet_step(remote: dict[str, Any], step_id: str) -> dict[str, Any]:
    steps = remote.get("execution_steps") if isinstance(remote.get("execution_steps"), dict) else {}
    return _step(steps, step_id)


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
    return module2_source_head()


if __name__ == "__main__":
    raise SystemExit(main())
