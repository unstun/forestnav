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
DEFAULT_REMOTE_READINESS = Path("0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.json")
DEFAULT_SOURCE_FRESHNESS = Path("0_trials/module2_source_freshness_audit/source_freshness_audit.json")
DEFAULT_MISSING_ARTIFACTS = Path("0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json")


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

    decision_gaps = _decision_gaps(decision=decision, h01=h01, remote=remote)
    source_freshness_gaps = _source_freshness_gaps(source_freshness=source_freshness, source_freshness_path=config.source_freshness_path)
    training_gaps = _training_gaps(remote=remote, h02=h02, remote_readiness=remote_readiness, remote_readiness_path=config.remote_readiness_path)
    training_gaps = _unique_gaps(training_gaps + source_freshness_gaps)
    evaluation_gaps = _evaluation_gaps(h01=h01, h02=h02)
    acceptance_gaps = _acceptance_gaps(h02=h02, claim_safety=claim_safety, readiness=readiness)
    acceptance_gaps = _unique_gaps(
        acceptance_gaps
        + _missing_artifacts_gaps(missing_artifacts=missing_artifacts, missing_artifacts_path=config.missing_artifacts_path)
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
        "local_training_allowed": False,
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
        "current_gate_state": _current_gate_state(
            decision=decision,
            h01=h01,
            remote=remote,
            h02=h02,
            claim_safety=claim_safety,
            source_freshness=source_freshness,
            missing_artifacts=missing_artifacts,
        ),
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
            "Source freshness risks are regeneration blockers, not formal algorithm failures.",
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
    parser.add_argument("--remote-readiness-refresh", type=Path, default=DEFAULT_REMOTE_READINESS)
    parser.add_argument("--source-freshness-audit", type=Path, default=DEFAULT_SOURCE_FRESHNESS)
    parser.add_argument("--missing-artifacts-audit", type=Path, default=DEFAULT_MISSING_ARTIFACTS)
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
    if source_freshness.get("regeneration_required_before_remote_formal_execution") is True:
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
    audit_precondition_gaps = training_precondition_gaps + post_training_output_gaps
    evaluation_precondition_gaps = audit_precondition_gaps + list(evaluation_gaps)
    claim_precondition_gaps = evaluation_precondition_gaps + list(acceptance_gaps)
    steps.append(
        {
            "step_id": "F02.6",
            "phase": "decision",
            "status": "blocked" if decision_gaps else "ready",
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
        "source_freshness_status": source_freshness.get("status"),
        "source_freshness_regeneration_required": bool(source_freshness.get("regeneration_required_before_remote_formal_execution")),
        "formal_gate_missing_artifacts_status": missing_artifacts.get("status"),
        "formal_gate_missing_artifacts_open": missing_artifacts.get("all_required_evidence_present") is not True,
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
        "risk_counts": source_freshness.get("risk_counts") if isinstance(source_freshness.get("risk_counts"), dict) else {},
        "ordered_regeneration_target_count": len(ordered_targets),
        "ordered_regeneration_targets": ordered_targets,
    }


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


def _critical_input_matches(readiness: dict[str, Any], input_id: str) -> bool:
    critical_inputs = readiness.get("critical_inputs") if isinstance(readiness.get("critical_inputs"), dict) else {}
    item = critical_inputs.get(input_id) if isinstance(critical_inputs.get(input_id), dict) else {}
    return item.get("local_remote_match") is True


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
        ]
    )
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
