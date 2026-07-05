from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_formal_gate_protocol_lane_matrix")
DEFAULT_CONTRACT_INTAKE = Path("0_trials/module2_formal_gate_contract_intake/formal_gate_contract_intake.json")
DEFAULT_NEXT_ROUND_REQUIREMENTS = Path(
    "0_trials/module2_formal_gate_next_round_requirements/formal_gate_next_round_requirements.json"
)


@dataclass(frozen=True)
class FormalGateProtocolLaneMatrixConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    contract_intake_path: Path = DEFAULT_CONTRACT_INTAKE
    next_round_requirements_path: Path = DEFAULT_NEXT_ROUND_REQUIREMENTS


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = FormalGateProtocolLaneMatrixConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        contract_intake_path=args.contract_intake,
        next_round_requirements_path=args.next_round_requirements,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "formal_gate_protocol_lane_matrix.json"
    markdown_out = config.markdown_out or output_dir / "formal_gate_protocol_lane_matrix.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: FormalGateProtocolLaneMatrixConfig) -> dict[str, Any]:
    contract_intake = _read_json(config.contract_intake_path)
    next_round = _read_json(config.next_round_requirements_path)
    lane_rows = _lane_rows(contract_intake=contract_intake)
    gate = _gate_summary(contract_intake=contract_intake, next_round=next_round)
    audit_issues = _audit_issues(contract_intake=contract_intake, next_round=next_round, gate=gate, lane_rows=lane_rows)
    ready = not audit_issues
    return {
        "schema_version": 1,
        "artifact_name": "module2_formal_gate_protocol_lane_matrix",
        "status": "formal_gate_protocol_lane_matrix_ready" if ready else "formal_gate_protocol_lane_matrix_blocked",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": module2_source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "runs_remote_audit": False,
        "local_training_allowed": False,
        "remote_training_allowed_now": False,
        "formal_claim_allowed": False,
        "paper_result_material_allowed": False,
        "inputs": {
            "contract_intake": str(config.contract_intake_path),
            "next_round_requirements": str(config.next_round_requirements_path),
        },
        "gate_summary": gate,
        "lane_count": len(lane_rows),
        "protocol_lane_evidence_matrix": lane_rows,
        "cross_lane_invariants": _cross_lane_invariants(),
        "audit_issue_count": len(audit_issues),
        "audit_issues": audit_issues,
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Module2 protocol-lane evidence matrix after formal Gate3 failure.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--contract-intake", type=Path, default=DEFAULT_CONTRACT_INTAKE)
    parser.add_argument("--next-round-requirements", type=Path, default=DEFAULT_NEXT_ROUND_REQUIREMENTS)
    return parser.parse_args(list(argv) if argv is not None else None)


def _gate_summary(*, contract_intake: dict[str, Any], next_round: dict[str, Any]) -> dict[str, Any]:
    current_gate = contract_intake.get("current_gate") if isinstance(contract_intake.get("current_gate"), dict) else {}
    current_failure = contract_intake.get("current_failed_run") if isinstance(contract_intake.get("current_failed_run"), dict) else {}
    permissions = next_round.get("permissions_now") if isinstance(next_round.get("permissions_now"), dict) else {}
    return {
        "contract_intake_status": contract_intake.get("status"),
        "contract_intake_audit_issue_count": int(contract_intake.get("audit_issue_count") or 0),
        "next_round_requirements_status": next_round.get("status"),
        "next_round_audit_issue_count": int(next_round.get("audit_issue_count") or 0),
        "current_formal_decision": current_failure.get("formal_decision"),
        "current_failure_mode": current_failure.get("failure_mode"),
        "terminal_rs_success_rate": _number(current_failure.get("terminal_rs_success_rate")),
        "required_success_threshold": _number(current_failure.get("required_success_threshold")),
        "threshold_deficit": _number(current_failure.get("threshold_deficit")),
        "new_success_training_allowed_now": bool(
            current_gate.get("new_success_training_allowed_now")
            or permissions.get("new_success_training_allowed_now")
        ),
        "remote_training_allowed_now": bool(contract_intake.get("remote_training_allowed_now")),
        "local_training_allowed_now": bool(current_gate.get("local_training_allowed_now") or permissions.get("local_training_allowed_now")),
        "formal_claim_allowed_now": bool(current_gate.get("formal_claim_allowed_now") or permissions.get("formal_claim_allowed_now")),
        "paper_result_material_allowed_now": bool(contract_intake.get("paper_result_material_allowed")),
        "new_or_revised_contract_required_before_training": bool(
            current_gate.get("new_or_revised_contract_required_before_new_success_training", True)
        ),
    }


def _lane_rows(*, contract_intake: dict[str, Any]) -> list[dict[str, Any]]:
    intake_lanes = {
        str(row.get("lane_id")): row
        for row in contract_intake.get("candidate_protocol_lanes", [])
        if isinstance(row, dict) and row.get("lane_id")
    }
    rows = []
    for lane_id in (
        "stronger_obstacle_summary_warm_start",
        "full_patch_cnn_policy",
        "hybrid_ppo_analytic_fallback",
        "stop_or_reframe_module2_claim",
    ):
        source = intake_lanes.get(lane_id, {})
        row = _lane_template(lane_id)
        row["contract_intake_status"] = source.get("status")
        row["what_changes"] = source.get("what_changes") or row["what_changes"]
        row["must_justify"] = _strings(source.get("must_justify")) or row["must_justify"]
        rows.append(row)
    return rows


def _lane_template(lane_id: str) -> dict[str, Any]:
    templates = {
        "stronger_obstacle_summary_warm_start": {
            "claim_scope": "direct PPO replacement attempt remains possible only if the new contract preserves the replacement claim boundary",
            "what_changes": "strengthen compact obstacle-summary warm-start, PPO stabilization, curriculum, or demonstration coverage",
            "must_justify": [
                "why the failed 0.53125 success rate is expected to improve without changing the claim",
                "which failure modes are addressed by stronger warm-start evidence",
            ],
            "required_contract_deltas": [
                "warm-start dataset source and acceptance checks",
                "PPO stabilization changes",
                "curriculum and reward deltas",
                "budget and seed policy",
            ],
            "required_training_evidence": [
                "new remote checkpoint bundle under a new attempt directory",
                "new train/summary.json with protocol label and terminal-RS training signals",
                "new training_manifest.json with source head, remote host, command, seed, and warm-start provenance",
            ],
            "required_evaluation_evidence": [
                "new formal Gate3 eval CSV with at least 64 episodes",
                "new gate3_summary.json with terminal-RS success, collision, truncation, and timing fields",
            ],
            "required_acceptance_evidence": [
                "formal_decision=pass in the new gate3_formal_audit.json",
                "checkpoint hash tied to the evaluated checkpoint",
                "H02 formal_output_accepted=true with PPO rows and checkpoint hash",
            ],
            "invalid_substitutes": [
                "the failed warm-start checkpoint",
                "more prose explaining the failed result",
                "local PPO training output",
                "H02 smoke rows without formal PPO rows",
            ],
        },
        "full_patch_cnn_policy": {
            "claim_scope": "direct PPO replacement claim changes substantially and must be re-registered as an observation/architecture delta",
            "what_changes": "replace compact summary inputs with spatial patch/CNN observation policy",
            "must_justify": [
                "why spatial structure is required by the observed failure",
                "how the architecture delta remains a fair PPO-vs-RS test",
            ],
            "required_contract_deltas": [
                "observation tensor definition",
                "CNN architecture and inference budget",
                "comparison fairness against RS/analytic baselines",
                "new H01/H02 schema fields if telemetry changes",
            ],
            "required_training_evidence": [
                "remote training packet with CNN dependencies and deterministic config",
                "checkpoint bundle with architecture metadata",
                "training manifest recording observation schema version",
            ],
            "required_evaluation_evidence": [
                "formal Gate3 eval using the same observation schema as training",
                "timing budget evidence for CNN inference",
                "per-episode records exposing failure modes beyond success rate",
            ],
            "required_acceptance_evidence": [
                "audit proving formal pass under the CNN protocol",
                "H02 rows that identify the CNN PPO method and checkpoint hash",
                "claim boundary stating this is not the same protocol as the failed compact policy",
            ],
            "invalid_substitutes": [
                "using compact-policy failure as CNN success evidence",
                "architecture change without revised contract",
                "timing-unchecked CNN results",
                "paper table without method/schema distinction",
            ],
        },
        "hybrid_ppo_analytic_fallback": {
            "claim_scope": "claim likely changes from PPO replacing RS to PPO assisting/selecting/recovering around analytic planning",
            "what_changes": "use PPO as selector, recovery, or fallback layer with explicit analytic planner involvement",
            "must_justify": [
                "whether RS is still being replaced or only assisted",
                "how analytic fallback usage is exposed and not hidden in success metrics",
            ],
            "required_contract_deltas": [
                "hybrid control handoff rule",
                "fallback usage metric",
                "success signal that separates PPO-only from analytic-assisted success",
                "paper claim boundary for hybrid assistance",
            ],
            "required_training_evidence": [
                "remote checkpoint for the learned selector/recovery policy",
                "training manifest recording analytic fallback interface",
                "logs that expose fallback-trigger distribution",
            ],
            "required_evaluation_evidence": [
                "formal eval with fallback usage columns",
                "paired PPO-only / hybrid / RS baseline comparison if claiming assistance",
                "collision and recovery metrics tied to fallback events",
            ],
            "required_acceptance_evidence": [
                "formal audit using hybrid-specific success and failure signals",
                "H02 rows that expose fallback usage and checkpoint hash",
                "claim safety artifact that prevents wording as pure RS replacement unless proven",
            ],
            "invalid_substitutes": [
                "calling hybrid success direct PPO replacement",
                "hiding RS/analytic fallback calls inside aggregate success",
                "using direct-replacement threshold without a hybrid contract",
                "paper prose that omits fallback usage",
            ],
        },
        "stop_or_reframe_module2_claim": {
            "claim_scope": "no new success-attempt training; use failure as negative evidence or reframe the module2 contribution",
            "what_changes": "stop pursuing PPO replacement under current claim or turn module2 into a bounded negative result / design lesson",
            "must_justify": [
                "why current negative evidence is sufficient to stop",
                "what claim remains defensible without formal PPO pass",
            ],
            "required_contract_deltas": [
                "stop criterion",
                "negative-result scope",
                "allowed paper claim after failure",
                "archival requirements for failed checkpoint and audit",
            ],
            "required_training_evidence": [
                "no new training evidence required if the contract explicitly stops success attempts",
            ],
            "required_evaluation_evidence": [
                "existing failed formal Gate3 audit retained as negative evidence",
                "failure-mode analysis from existing eval CSV/logs only",
            ],
            "required_acceptance_evidence": [
                "claim safety audit blocks success wording",
                "H02 remains blocked for success results",
                "paper-readiness artifact, if later used, is scoped to negative evidence only",
            ],
            "invalid_substitutes": [
                "quietly dropping failed PPO without recording the stop decision",
                "writing a positive replacement claim from failed evidence",
                "running new training while pretending the lane was stop/reframe",
            ],
        },
    }
    row = dict(templates[lane_id])
    row.update(
        {
            "lane_id": lane_id,
            "status": "candidate_requires_dr_sun_decision_and_contract",
            "training_allowed_now": False,
            "paper_result_material_allowed_now": False,
            "requires_new_or_revised_contract": True,
        }
    )
    return row


def _cross_lane_invariants() -> list[dict[str, Any]]:
    return [
        {
            "invariant_id": "no_local_training",
            "status": "active",
            "rule": "Local PPO training output is not formal evidence for any lane.",
        },
        {
            "invariant_id": "contract_before_new_success_training",
            "status": "active",
            "rule": "Any new success-attempt remote training requires an approved or frozen new/revised contract first.",
        },
        {
            "invariant_id": "failed_checkpoint_not_success_evidence",
            "status": "active",
            "rule": "The failed warm-start checkpoint can be negative evidence only, not a success checkpoint.",
        },
        {
            "invariant_id": "h02_before_paper_results",
            "status": "active",
            "rule": "Paper result material requires H02 formal_output_accepted=true and paper_result_input_allowed=true.",
        },
    ]


def _audit_issues(
    *,
    contract_intake: dict[str, Any],
    next_round: dict[str, Any],
    gate: dict[str, Any],
    lane_rows: list[dict[str, Any]],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if contract_intake.get("status") != "formal_gate_contract_intake_ready_for_dr_sun":
        issues.append(_issue("contract_intake_not_ready", "Contract intake must be ready before lane matrix is authoritative."))
    if next_round.get("status") != "formal_gate_next_round_requirements_ready":
        issues.append(_issue("next_round_requirements_not_ready", "Next-round requirements must be ready before lane matrix."))
    if gate["current_formal_decision"] != "fail":
        issues.append(_issue("current_formal_decision_not_fail", "Lane matrix expects a failed formal Gate3 run."))
    if gate["current_failure_mode"] != "threshold_failure":
        issues.append(_issue("current_failure_not_threshold_failure", "Lane matrix expects threshold-failure evidence."))
    if gate["new_success_training_allowed_now"] or gate["remote_training_allowed_now"]:
        issues.append(_issue("training_allowed_before_lane_decision", "No lane may authorize training before Dr Sun decision and contract."))
    if gate["local_training_allowed_now"]:
        issues.append(_issue("local_training_allowed", "Local PPO training must remain disallowed."))
    if gate["formal_claim_allowed_now"] or gate["paper_result_material_allowed_now"]:
        issues.append(_issue("claim_or_paper_result_allowed", "Formal claim and paper result material must remain blocked."))
    expected_lanes = {
        "stronger_obstacle_summary_warm_start",
        "full_patch_cnn_policy",
        "hybrid_ppo_analytic_fallback",
        "stop_or_reframe_module2_claim",
    }
    observed_lanes = {row.get("lane_id") for row in lane_rows}
    if observed_lanes != expected_lanes:
        issues.append(_issue("lane_set_mismatch", "Protocol lane matrix must contain the four contract-intake lanes."))
    for row in lane_rows:
        lane_id = str(row.get("lane_id"))
        if row.get("training_allowed_now"):
            issues.append(_issue(f"{lane_id}_training_allowed", "Lane row must not authorize training."))
        for key in ("required_contract_deltas", "required_training_evidence", "required_evaluation_evidence", "required_acceptance_evidence", "invalid_substitutes"):
            if not row.get(key):
                issues.append(_issue(f"{lane_id}_{key}_empty", f"Lane row must define {key}."))
    return _unique_issues(issues)


def _markdown(manifest: dict[str, Any]) -> str:
    gate = manifest["gate_summary"]
    lines = [
        "# Module2 Formal Gate Protocol Lane Matrix",
        "",
        "This file is a formal-gate lane evidence artifact, not paper result material.",
        "",
        "## Gate Summary",
        "",
        f"- current_formal_decision: `{gate['current_formal_decision']}`",
        f"- current_failure_mode: `{gate['current_failure_mode']}`",
        f"- terminal_rs_success_rate: `{gate['terminal_rs_success_rate']}`",
        f"- required_success_threshold: `{gate['required_success_threshold']}`",
        f"- new_success_training_allowed_now: `{gate['new_success_training_allowed_now']}`",
        f"- remote_training_allowed_now: `{gate['remote_training_allowed_now']}`",
        f"- local_training_allowed_now: `{gate['local_training_allowed_now']}`",
        f"- formal_claim_allowed_now: `{gate['formal_claim_allowed_now']}`",
        "",
        "## Lane Matrix",
        "",
        "| lane | claim_scope | training_allowed_now |",
        "|---|---|---:|",
    ]
    for row in manifest["protocol_lane_evidence_matrix"]:
        lines.append(f"| `{row['lane_id']}` | {row['claim_scope']} | `{row['training_allowed_now']}` |")
    lines.extend(["", "## Cross-Lane Invariants"])
    for invariant in manifest["cross_lane_invariants"]:
        lines.append(f"- `{invariant['invariant_id']}`: {invariant['rule']}")
    lines.extend(["", "## Audit", "", f"- status: `{manifest['status']}`", f"- audit_issue_count: `{manifest['audit_issue_count']}`"])
    return "\n".join(lines) + "\n"


def _read_json(path: Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def _number(value: Any) -> float | None:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _strings(value: Any) -> list[str]:
    if not isinstance(value, (list, tuple)):
        return []
    return [str(item) for item in value if item]


def _issue(issue_id: str, message: str) -> dict[str, str]:
    return {"issue_id": issue_id, "message": message}


def _unique_issues(issues: Sequence[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    out: list[dict[str, str]] = []
    for issue in issues:
        issue_id = str(issue.get("issue_id") or "")
        if issue_id and issue_id not in seen:
            seen.add(issue_id)
            out.append(dict(issue))
    return out


if __name__ == "__main__":
    raise SystemExit(main())
