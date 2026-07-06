from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head
from forest_n3p.scripts.build_module2_v2_contract_readiness_gate import DEFAULT_CONTRACT_PATH


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_v2_formal_gate_remaining_evidence")
DEFAULT_DECISION_RECORD = Path(
    "0_trials/module2_formal_gate_protocol_lane_decision_record/protocol_lane_decision_record.json"
)
DEFAULT_READINESS_GATE = Path("0_trials/module2_v2_contract_readiness_gate/v2_contract_readiness_gate.json")
DEFAULT_PROMOTION_PACKET = Path("0_trials/module2_v2_contract_promotion_packet/v2_contract_promotion_packet.json")
DEFAULT_PROMOTION_DRY_RUN = Path("0_trials/module2_v2_contract_promotion_dry_run/promotion_apply_dry_run.json")
DEFAULT_SOURCE_FRESHNESS = Path("0_trials/module2_source_freshness_audit/source_freshness_audit.json")
DEFAULT_REMOTE_PACKET = Path("0_trials/module2_v2_remote_execution_packet/v2_remote_execution_packet.json")
DEFAULT_PREFLIGHT_MANIFEST = Path(
    "0_trials/module2_remote_preflight/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706/"
    "gate3_preflight_manifest.json"
)
DEFAULT_FAILED_GATE3_SUMMARY = Path(
    "0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json"
)
DEFAULT_H02_ACCEPTANCE = Path("0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json")
DEFAULT_ATTEMPT_DIR = Path(
    "0_trials/module2_gate3_formal/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706"
)

EXPECTED_LANE = "stronger_obstacle_summary_warm_start"
EXPECTED_CONTRACT_ACTION = "draft_new_contract"
READY_CONTRACT_STATUSES = {"approved", "frozen"}
READY_READINESS_STATUS = "v2_contract_ready_for_source_freshness"
READY_REMOTE_PACKET_STATUS = "ready_for_v2_remote_preflight"
SOURCE_FRESHNESS_READY_STATUSES = {
    "source_freshness_clean_current",
    "source_freshness_tracked_artifact_lag_only_gate_ready",
    "source_freshness_remote_preflight_scope_ready_with_later_risks",
}


@dataclass(frozen=True)
class Module2V2FormalGateRemainingEvidenceConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    contract_path: Path = DEFAULT_CONTRACT_PATH
    decision_record_path: Path = DEFAULT_DECISION_RECORD
    readiness_gate_path: Path = DEFAULT_READINESS_GATE
    promotion_packet_path: Path = DEFAULT_PROMOTION_PACKET
    promotion_dry_run_path: Path = DEFAULT_PROMOTION_DRY_RUN
    source_freshness_path: Path = DEFAULT_SOURCE_FRESHNESS
    remote_packet_path: Path = DEFAULT_REMOTE_PACKET
    preflight_manifest_path: Path = DEFAULT_PREFLIGHT_MANIFEST
    failed_gate3_summary_path: Path = DEFAULT_FAILED_GATE3_SUMMARY
    h02_acceptance_path: Path = DEFAULT_H02_ACCEPTANCE
    attempt_dir: Path = DEFAULT_ATTEMPT_DIR


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = Module2V2FormalGateRemainingEvidenceConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        contract_path=args.contract_path,
        decision_record_path=args.decision_record,
        readiness_gate_path=args.readiness_gate,
        promotion_packet_path=args.promotion_packet,
        promotion_dry_run_path=args.promotion_dry_run,
        source_freshness_path=args.source_freshness,
        remote_packet_path=args.remote_packet,
        preflight_manifest_path=args.preflight_manifest,
        failed_gate3_summary_path=args.failed_gate3_summary,
        h02_acceptance_path=args.h02_acceptance,
        attempt_dir=args.attempt_dir,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "v2_formal_gate_remaining_evidence.json"
    markdown_out = config.markdown_out or output_dir / "v2_formal_gate_remaining_evidence.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: Module2V2FormalGateRemainingEvidenceConfig) -> dict[str, Any]:
    contract_text = _read_text(config.contract_path)
    contract_frontmatter = _frontmatter(contract_text)
    decision = _read_json(config.decision_record_path)
    readiness = _read_json(config.readiness_gate_path)
    promotion = _read_json(config.promotion_packet_path)
    dry_run = _read_json(config.promotion_dry_run_path)
    source_freshness = _read_json(config.source_freshness_path)
    remote_packet = _read_json(config.remote_packet_path)
    preflight = _read_json(config.preflight_manifest_path)
    failed_summary = _read_json(config.failed_gate3_summary_path)
    h02 = _read_json(config.h02_acceptance_path)

    gate_blockers = _gate_blockers(
        contract_frontmatter=contract_frontmatter,
        decision=decision,
        readiness=readiness,
        promotion=promotion,
        dry_run=dry_run,
        source_freshness=source_freshness,
        remote_packet=remote_packet,
        preflight=preflight,
    )
    deliverables = _deliverables(config=config, h02=h02)
    group_summary = _group_summary(deliverables)
    status = _status(gate_blockers=gate_blockers, group_summary=group_summary)
    permissions = _permissions(remote_packet=remote_packet, gate_blockers=gate_blockers)
    return {
        "schema_version": 1,
        "artifact_name": "module2_v2_formal_gate_remaining_evidence",
        "status": status,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": module2_source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "runs_remote_audit": False,
        "inputs": {
            "contract": str(config.contract_path),
            "decision_record": str(config.decision_record_path),
            "readiness_gate": str(config.readiness_gate_path),
            "promotion_packet": str(config.promotion_packet_path),
            "promotion_dry_run": str(config.promotion_dry_run_path),
            "source_freshness": str(config.source_freshness_path),
            "remote_packet": str(config.remote_packet_path),
            "preflight_manifest": str(config.preflight_manifest_path),
            "failed_gate3_summary": str(config.failed_gate3_summary_path),
            "h02_acceptance": str(config.h02_acceptance_path),
            "attempt_dir": str(config.attempt_dir),
        },
        "failed_gate3_basis": _failed_gate3_basis(failed_summary),
        "decision_state": {
            "record_status": decision.get("status"),
            "selected_lane_id": decision.get("selected_lane_id"),
            "contract_action": decision.get("contract_action"),
            "contract_path": str(config.contract_path),
            "contract_status": contract_frontmatter.get("status", "missing"),
        },
        "gate_state": {
            "readiness_status": readiness.get("status"),
            "promotion_packet_status": promotion.get("status"),
            "promotion_dry_run_status": dry_run.get("status"),
            "source_freshness_status": source_freshness.get("status"),
            "remote_packet_status": remote_packet.get("status"),
            "preflight_status": preflight.get("preflight_status"),
            "preflight_formal_trial_ready": bool(preflight.get("formal_trial_ready")),
        },
        "permissions_now": permissions,
        "gate_blocker_count": len(gate_blockers),
        "gate_blockers": gate_blockers,
        "remaining_evidence_summary": group_summary,
        "deliverables": deliverables,
        "next_ordered_actions": _next_ordered_actions(gate_blockers=gate_blockers),
        "invalid_substitutes": [
            "local PPO training output",
            "failed gate3_obstacle_summary_warm_approved_v1 checkpoint or summary",
            "old v1 remote execution packet",
            "remote preflight smoke without formal_trial_ready",
            "H02 smoke rows or blocked H02 acceptance",
            "paper result table, appendix prose, or narrative reinterpretation",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a v2-specific Module2 formal gate missing-evidence ledger.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--contract-path", type=Path, default=DEFAULT_CONTRACT_PATH)
    parser.add_argument("--decision-record", type=Path, default=DEFAULT_DECISION_RECORD)
    parser.add_argument("--readiness-gate", type=Path, default=DEFAULT_READINESS_GATE)
    parser.add_argument("--promotion-packet", type=Path, default=DEFAULT_PROMOTION_PACKET)
    parser.add_argument("--promotion-dry-run", type=Path, default=DEFAULT_PROMOTION_DRY_RUN)
    parser.add_argument("--source-freshness", type=Path, default=DEFAULT_SOURCE_FRESHNESS)
    parser.add_argument("--remote-packet", type=Path, default=DEFAULT_REMOTE_PACKET)
    parser.add_argument("--preflight-manifest", type=Path, default=DEFAULT_PREFLIGHT_MANIFEST)
    parser.add_argument("--failed-gate3-summary", type=Path, default=DEFAULT_FAILED_GATE3_SUMMARY)
    parser.add_argument("--h02-acceptance", type=Path, default=DEFAULT_H02_ACCEPTANCE)
    parser.add_argument("--attempt-dir", type=Path, default=DEFAULT_ATTEMPT_DIR)
    return parser.parse_args(list(argv) if argv is not None else None)


def _gate_blockers(
    *,
    contract_frontmatter: dict[str, str],
    decision: dict[str, Any],
    readiness: dict[str, Any],
    promotion: dict[str, Any],
    dry_run: dict[str, Any],
    source_freshness: dict[str, Any],
    remote_packet: dict[str, Any],
    preflight: dict[str, Any],
) -> list[dict[str, Any]]:
    blockers: list[dict[str, Any]] = []
    if decision.get("selected_lane_id") != EXPECTED_LANE:
        blockers.append(_issue("selected_lane_not_recorded", decision.get("selected_lane_id"), EXPECTED_LANE))
    if decision.get("contract_action") != EXPECTED_CONTRACT_ACTION:
        blockers.append(_issue("contract_action_not_draft_new_contract", decision.get("contract_action"), EXPECTED_CONTRACT_ACTION))
    contract_status = contract_frontmatter.get("status", "missing")
    if contract_status not in READY_CONTRACT_STATUSES:
        blockers.append(_issue("v2_contract_not_promoted", contract_status, sorted(READY_CONTRACT_STATUSES)))
    if readiness.get("status") != READY_READINESS_STATUS:
        blockers.append(_issue("v2_contract_readiness_not_ready", readiness.get("status"), READY_READINESS_STATUS))
    if not promotion or promotion.get("status") != "v2_contract_promotion_packet_ready_awaiting_dr_sun":
        blockers.append(_issue("promotion_packet_not_ready", promotion.get("status"), "v2_contract_promotion_packet_ready_awaiting_dr_sun"))
    if not dry_run or dry_run.get("status") != "promotion_apply_ready":
        blockers.append(_issue("promotion_dry_run_not_ready", dry_run.get("status"), "promotion_apply_ready"))
    if source_freshness.get("status") not in SOURCE_FRESHNESS_READY_STATUSES:
        blockers.append(_issue("source_freshness_not_ready", source_freshness.get("status"), sorted(SOURCE_FRESHNESS_READY_STATUSES)))
    if remote_packet.get("status") != READY_REMOTE_PACKET_STATUS:
        blockers.append(_issue("v2_remote_execution_packet_not_ready", remote_packet.get("status"), READY_REMOTE_PACKET_STATUS))
    if preflight.get("preflight_status") != "ready" or preflight.get("formal_trial_ready") is not True:
        blockers.append(_issue("v2_remote_preflight_manifest_not_ready", preflight.get("preflight_status") or "missing", "ready + formal_trial_ready=true"))
    return blockers


def _deliverables(*, config: Module2V2FormalGateRemainingEvidenceConfig, h02: dict[str, Any]) -> list[dict[str, Any]]:
    attempt = config.attempt_dir
    rows = [
        _row(
            "contract",
            "v2_contract_promoted",
            config.contract_path,
            "approved_or_frozen_contract_before_any_new_training",
            "new_success_training",
            ["contract frontmatter status is approved or frozen", "hypothesis, success signal, failure signal, budget, and protocol deltas are locked"],
            ["draft contract", "chat-only approval", "editing thresholds after training"],
        ),
        _row(
            "gate_precondition",
            "source_freshness_ready",
            config.source_freshness_path,
            "source freshness gate ready for the v2 contract/source head",
            "remote_preflight",
            ["source_freshness status is a ready state", "blocking targets are regenerated or explicitly non-blocking"],
            ["historical source freshness audit", "packet generated against stale source head"],
        ),
        _row(
            "gate_precondition",
            "v2_remote_preflight_manifest",
            config.preflight_manifest_path,
            "remote preflight manifest reports ready and formal_trial_ready=true",
            "remote_training",
            ["preflight manifest exists", "contract path and stronger v2 parameters match", "formal_trial_ready=true"],
            ["remote smoke", "missing preflight JSON", "preflight tied to v1 contract"],
        ),
        _row(
            "training",
            "train_final_model_zip",
            attempt / "train" / "final_model.zip",
            "remote-produced PPO checkpoint pulled back from gpu3070ti-relay",
            "new_gate3_formal_audit",
            ["non-empty final_model.zip under the fresh v2 attempt directory", "checkpoint hash recorded"],
            ["local checkpoint", "failed v1 warm-start checkpoint", "checkpoint without hash/manifest"],
        ),
        _row(
            "training",
            "train_summary_json",
            attempt / "train" / "summary.json",
            "training summary records complete v2 remote PPO run",
            "new_gate3_formal_audit",
            ["status=complete", "smoke=false", "v2 contract path", "seed/source head/host", "500000 timestep PPO block"],
            ["stdout-only log", "summary from failed v1 run", "summary without protocol label"],
        ),
        _row(
            "training",
            "train_training_manifest_json",
            attempt / "train" / "training_manifest.json",
            "training manifest records source, command, host, and checkpoint provenance",
            "new_gate3_formal_audit",
            ["source head is non-unknown", "command provenance", "BC checkpoint hash", "final PPO checkpoint hash"],
            ["manifest without source head", "manifest from another lane", "uncommitted chat note"],
        ),
        _row(
            "evaluation",
            "eval_gate3_eval_episodes_csv",
            attempt / "eval" / "gate3_eval_episodes.csv",
            "per-episode formal Gate3 CSV from the new v2 attempt",
            "new_gate3_formal_audit",
            ["at least 64 rows", "terminal-RS success/collision/truncation fields", "v2 protocol provenance"],
            ["aggregate summary only", "H02 smoke CSV", "no-warm rows reused for warm-start"],
        ),
        _row(
            "evaluation",
            "eval_gate3_summary_json",
            attempt / "eval" / "gate3_summary.json",
            "formal Gate3 summary reaches the locked threshold",
            "new_gate3_formal_audit",
            ["success_threshold=0.8", "terminal_rs_success_rate >= 0.8", "timing and model hash fields"],
            ["0.53125 failed summary", "paper table preview", "summary without per-episode CSV"],
        ),
        _row(
            "acceptance",
            "gate3_trial_manifest_json",
            attempt / "gate3_trial_manifest.json",
            "trial manifest ties train/eval/audit to the v2 contract",
            "h02_formal_output_acceptance",
            ["fresh attempt directory", "v2 contract path", "train/eval/audit pointers", "source head"],
            ["manifest from failed v1 run", "manifest without evaluated checkpoint identity"],
        ),
        _row(
            "acceptance",
            "gate3_formal_audit_json",
            attempt / "gate3_formal_audit.json",
            "formal audit passes for the new v2 attempt",
            "h02_formal_output_acceptance",
            ["formal_decision=pass", "required_success_threshold=0.8", "v2 contract path", "matching checkpoint hash"],
            ["formal_decision=fail reinterpreted as success", "audit marked smoke/preview", "audit from another contract"],
        ),
        _row(
            "acceptance",
            "pulled_back_checkpoint_hash_record",
            attempt / "train" / "final_model.zip.sha256",
            "pulled-back checkpoint hash matches the evaluated model",
            "h02_formal_output_acceptance",
            ["hash record exists", "hash matches final_model.zip", "same hash appears in eval/audit/H02"],
            ["remote stdout without pullback", "hash for a different checkpoint"],
        ),
        _h02_row(config.h02_acceptance_path, h02),
    ]
    return [_evaluate_row(row) for row in rows]


def _row(
    category: str,
    artifact_id: str,
    path: Path,
    proof_requirement: str,
    required_before: str,
    acceptable_evidence: list[str],
    invalid_substitutes: list[str],
) -> dict[str, Any]:
    return {
        "category": category,
        "artifact_id": artifact_id,
        "expected_path": str(path),
        "proof_requirement": proof_requirement,
        "required_before": required_before,
        "acceptable_evidence": acceptable_evidence,
        "invalid_substitutes": invalid_substitutes,
    }


def _h02_row(path: Path, h02: dict[str, Any]) -> dict[str, Any]:
    row = _row(
        "formal_acceptance",
        "h02_formal_output_acceptance",
        path,
        "H02 accepts the new v2 PPO rows for paper-result input",
        "paper_result_material",
        ["formal_output_accepted=true", "paper_result_input_allowed=true", "formal PPO rows include checkpoint hash", "H02 scale satisfies H01"],
        ["blocked H02 acceptance", "formal-looking smoke table", "PPO rows without checkpoint hash"],
    )
    row["current_h02_status"] = h02.get("status")
    row["formal_output_accepted"] = bool(h02.get("formal_output_accepted"))
    row["paper_result_input_allowed"] = bool(h02.get("paper_result_input_allowed"))
    return row


def _evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    path = Path(str(row["expected_path"]).split(" or ", 1)[0])
    exists = path.exists()
    satisfied = bool(exists)
    if row["artifact_id"] == "v2_contract_promoted":
        frontmatter = _frontmatter(_read_text(path))
        satisfied = frontmatter.get("status") in READY_CONTRACT_STATUSES
        state = f"contract_status_{frontmatter.get('status', 'missing')}"
    elif row["artifact_id"] == "source_freshness_ready":
        data = _read_json(path)
        satisfied = data.get("status") in SOURCE_FRESHNESS_READY_STATUSES
        state = str(data.get("status") or "missing")
    elif row["artifact_id"] == "v2_remote_preflight_manifest":
        data = _read_json(path)
        satisfied = data.get("preflight_status") == "ready" and data.get("formal_trial_ready") is True
        state = str(data.get("preflight_status") or "missing")
    elif row["artifact_id"] == "h02_formal_output_acceptance":
        satisfied = bool(row.get("formal_output_accepted")) and bool(row.get("paper_result_input_allowed"))
        state = str(row.get("current_h02_status") or "missing")
    else:
        state = "present" if exists else "missing"
    return {
        **row,
        "exists": exists,
        "satisfied_for_v2_success_attempt": satisfied,
        "state": state,
    }


def _group_summary(deliverables: Sequence[dict[str, Any]]) -> dict[str, Any]:
    categories = sorted({str(row["category"]) for row in deliverables})
    by_category: dict[str, dict[str, int]] = {}
    for category in categories:
        rows = [row for row in deliverables if row["category"] == category]
        unsatisfied = [row for row in rows if not row["satisfied_for_v2_success_attempt"]]
        by_category[category] = {
            "total": len(rows),
            "satisfied": len(rows) - len(unsatisfied),
            "missing_or_unsatisfied": len(unsatisfied),
        }
    return {
        "total_required_evidence_items": len(deliverables),
        "total_missing_or_unsatisfied": sum(1 for row in deliverables if not row["satisfied_for_v2_success_attempt"]),
        "by_category": by_category,
        "training_missing_or_unsatisfied": by_category.get("training", {}).get("missing_or_unsatisfied", 0),
        "evaluation_missing_or_unsatisfied": by_category.get("evaluation", {}).get("missing_or_unsatisfied", 0),
        "acceptance_missing_or_unsatisfied": by_category.get("acceptance", {}).get("missing_or_unsatisfied", 0),
        "formal_acceptance_missing_or_unsatisfied": by_category.get("formal_acceptance", {}).get("missing_or_unsatisfied", 0),
    }


def _status(*, gate_blockers: Sequence[dict[str, Any]], group_summary: dict[str, Any]) -> str:
    issue_ids = {str(blocker["issue_id"]) for blocker in gate_blockers}
    if "v2_contract_not_promoted" in issue_ids:
        return "blocked_until_v2_contract_promotion"
    if "source_freshness_not_ready" in issue_ids:
        return "blocked_until_source_freshness"
    if "v2_remote_execution_packet_not_ready" in issue_ids:
        return "blocked_until_v2_remote_execution_packet"
    if "v2_remote_preflight_manifest_not_ready" in issue_ids:
        return "blocked_until_v2_remote_preflight"
    if int(group_summary["total_missing_or_unsatisfied"]) > 0:
        return "blocked_until_fresh_v2_training_eval_acceptance"
    return "v2_formal_gate_evidence_complete"


def _permissions(*, remote_packet: dict[str, Any], gate_blockers: Sequence[dict[str, Any]]) -> dict[str, bool]:
    no_blockers = len(gate_blockers) == 0
    return {
        "local_training_allowed_now": False,
        "remote_preflight_allowed_now": bool(remote_packet.get("remote_preflight_allowed_now")) and no_blockers,
        "remote_training_allowed_now": False,
        "formal_h02_acceptance_allowed_now": False,
        "formal_claim_allowed_now": False,
        "paper_result_material_allowed_now": False,
    }


def _next_ordered_actions(*, gate_blockers: Sequence[dict[str, Any]]) -> list[str]:
    issue_ids = [str(blocker["issue_id"]) for blocker in gate_blockers]
    if "v2_contract_not_promoted" in issue_ids:
        return [
            "Dr Sun explicitly promotes the v2 contract to approved or frozen",
            "Apply the promotion dry-run for real and commit the contract status change",
            "Re-run the v2 contract readiness gate",
            "Re-run source freshness and regenerate the v2 remote execution packet",
        ]
    if "source_freshness_not_ready" in issue_ids:
        return ["Regenerate blocking source-freshness targets", "Rebuild the v2 remote execution packet"]
    if "v2_remote_preflight_manifest_not_ready" in issue_ids:
        return ["Run the allowed remote preflight only", "Commit/pull back the preflight manifest before any training"]
    return ["Run remote training only after a ready preflight manifest", "Pull back train/eval/audit/hash artifacts", "Regenerate H02 acceptance"]


def _failed_gate3_basis(summary: dict[str, Any]) -> dict[str, Any]:
    rate = _number(summary.get("terminal_rs_success_rate"))
    threshold = _number(summary.get("success_threshold") or summary.get("required_success_threshold"))
    return {
        "decision": summary.get("decision") or summary.get("formal_decision"),
        "episodes": _int(summary.get("episodes") or summary.get("episode_count")),
        "terminal_rs_successes": _int(summary.get("terminal_rs_successes") or summary.get("terminal_rs_success")),
        "terminal_rs_success_rate": rate,
        "required_success_threshold": threshold,
        "threshold_deficit": None if rate is None or threshold is None else round(max(0.0, threshold - rate), 12),
        "basis_path": str(DEFAULT_FAILED_GATE3_SUMMARY),
        "usable_as_success_evidence": False,
    }


def _issue(issue_id: str, observed: Any, expected: Any) -> dict[str, Any]:
    return {"issue_id": issue_id, "observed": observed, "expected": expected}


def _frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    out: dict[str, str] = {}
    for line in text.splitlines()[1:]:
        if line.strip() == "---":
            break
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            out[key.strip()] = value.strip().strip("'\"")
    return out


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _number(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 V2 Formal Gate Remaining Evidence",
        "",
        "This is a formal-gate evidence ledger. It does not run local training, remote preflight, remote training, audit, pullback, or paper-result writing.",
        "",
        "## Status",
        "",
        f"- status: `{manifest['status']}`",
        f"- source_head: `{manifest['source_head']}`",
        f"- remote_preflight_allowed_now: `{manifest['permissions_now']['remote_preflight_allowed_now']}`",
        f"- remote_training_allowed_now: `{manifest['permissions_now']['remote_training_allowed_now']}`",
        f"- paper_result_material_allowed_now: `{manifest['permissions_now']['paper_result_material_allowed_now']}`",
        "",
        "## Failed Gate3 Basis",
        "",
    ]
    basis = manifest["failed_gate3_basis"]
    lines.extend(
        [
            f"- decision: `{basis['decision']}`",
            f"- terminal_rs_success_rate: `{basis['terminal_rs_success_rate']}`",
            f"- required_success_threshold: `{basis['required_success_threshold']}`",
            f"- threshold_deficit: `{basis['threshold_deficit']}`",
            "",
            "## Gate Blockers",
            "",
        ]
    )
    if manifest["gate_blockers"]:
        lines.extend(f"- `{item['issue_id']}`: observed=`{item['observed']}`, expected=`{item['expected']}`" for item in manifest["gate_blockers"])
    else:
        lines.append("- none")
    lines.extend(["", "## Remaining Evidence Summary", ""])
    summary = manifest["remaining_evidence_summary"]
    for category, counts in summary["by_category"].items():
        lines.append(
            f"- `{category}`: missing_or_unsatisfied=`{counts['missing_or_unsatisfied']}` / total=`{counts['total']}`"
        )
    lines.extend(["", "## Deliverables", ""])
    for row in manifest["deliverables"]:
        lines.append(f"### `{row['category']}:{row['artifact_id']}`")
        lines.append(f"- expected_path: `{row['expected_path']}`")
        lines.append(f"- state: `{row['state']}`")
        lines.append(f"- satisfied_for_v2_success_attempt: `{row['satisfied_for_v2_success_attempt']}`")
        lines.append(f"- required_before: `{row['required_before']}`")
        lines.append(f"- proof_requirement: {row['proof_requirement']}")
        lines.append("")
    lines.extend(["## Next Ordered Actions", ""])
    lines.extend(f"- {item}" for item in manifest["next_ordered_actions"])
    lines.extend(["", "## Invalid Substitutes", ""])
    lines.extend(f"- {item}" for item in manifest["invalid_substitutes"])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
