from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_formal_gate_contract_intake")
DEFAULT_NEXT_ROUND_REQUIREMENTS = Path(
    "0_trials/module2_formal_gate_next_round_requirements/formal_gate_next_round_requirements.json"
)
DEFAULT_FAILURE_TRIAGE = Path("0_trials/module2_formal_gate_failure_triage/formal_gate_failure_triage.json")
DEFAULT_H02_ACCEPTANCE = Path("0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json")


@dataclass(frozen=True)
class FormalGateContractIntakeConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    next_round_requirements_path: Path = DEFAULT_NEXT_ROUND_REQUIREMENTS
    failure_triage_path: Path = DEFAULT_FAILURE_TRIAGE
    h02_acceptance_path: Path = DEFAULT_H02_ACCEPTANCE


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = FormalGateContractIntakeConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        next_round_requirements_path=args.next_round_requirements,
        failure_triage_path=args.failure_triage,
        h02_acceptance_path=args.h02_acceptance,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "formal_gate_contract_intake.json"
    markdown_out = config.markdown_out or output_dir / "formal_gate_contract_intake.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: FormalGateContractIntakeConfig) -> dict[str, Any]:
    next_round = _read_json(config.next_round_requirements_path)
    failure_triage = _read_json(config.failure_triage_path)
    h02 = _read_json(config.h02_acceptance_path)

    current_failure = _current_failure(next_round=next_round, failure_triage=failure_triage)
    current_gate = _current_gate(next_round=next_round, h02=h02)
    decision_fields = _decision_fields()
    required_fields_missing = [field["field_id"] for field in decision_fields if field["status"] != "awaiting_dr_sun_decision"]
    audit_issues = _audit_issues(next_round=next_round, current_failure=current_failure, current_gate=current_gate)
    ready = not audit_issues and not required_fields_missing
    return {
        "schema_version": 1,
        "artifact_name": "module2_formal_gate_contract_intake",
        "status": "formal_gate_contract_intake_ready_for_dr_sun" if ready else "formal_gate_contract_intake_blocked",
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
        "contract_status_required_before_training": ["approved", "frozen"],
        "contract_draft_is_not_execution_authorization": True,
        "inputs": {
            "next_round_requirements": str(config.next_round_requirements_path),
            "failure_triage": str(config.failure_triage_path),
            "h02_formal_acceptance": str(config.h02_acceptance_path),
        },
        "current_failed_run": current_failure,
        "current_gate": current_gate,
        "decision_fields_required_for_contract": decision_fields,
        "required_field_count": len(decision_fields),
        "required_fields_missing": required_fields_missing,
        "candidate_protocol_lanes": _candidate_protocol_lanes(),
        "contract_output_requirements": _contract_output_requirements(),
        "invalid_shortcuts": [
            "start another PPO success attempt from the failed checkpoint without a new or revised contract",
            "change reward, curriculum, architecture, observations, budget, seed policy, or threshold in code without pre-registration",
            "treat blocked H02 smoke rows as formal PPO result rows",
            "use local PPO training output as formal gate evidence",
            "write a paper success table before H02 formal_output_accepted=true",
        ],
        "audit_issue_count": len(audit_issues),
        "audit_issues": audit_issues,
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Module2 contract intake after a failed formal Gate3 run.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--next-round-requirements", type=Path, default=DEFAULT_NEXT_ROUND_REQUIREMENTS)
    parser.add_argument("--failure-triage", type=Path, default=DEFAULT_FAILURE_TRIAGE)
    parser.add_argument("--h02-acceptance", type=Path, default=DEFAULT_H02_ACCEPTANCE)
    return parser.parse_args(list(argv) if argv is not None else None)


def _current_failure(*, next_round: dict[str, Any], failure_triage: dict[str, Any]) -> dict[str, Any]:
    next_failure = next_round.get("current_failed_run") if isinstance(next_round.get("current_failed_run"), dict) else {}
    triage_failure = failure_triage.get("formal_gate_failure") if isinstance(failure_triage.get("formal_gate_failure"), dict) else {}
    success_rate = _number(next_failure.get("terminal_rs_success_rate"))
    if success_rate is None:
        success_rate = _number(triage_failure.get("terminal_rs_success_rate"))
    threshold = _number(next_failure.get("required_success_threshold"))
    if threshold is None:
        threshold = _number(triage_failure.get("required_success_threshold"))
    deficit = None
    if success_rate is not None and threshold is not None:
        deficit = round(max(0.0, threshold - success_rate), 12)
    return {
        "failure_triage_status": failure_triage.get("status"),
        "next_round_status": next_round.get("status"),
        "formal_decision": next_failure.get("formal_decision") or triage_failure.get("formal_decision"),
        "failure_mode": next_failure.get("failure_mode") or triage_failure.get("failure_mode"),
        "episodes": _int(next_failure.get("episodes") or triage_failure.get("episodes")),
        "terminal_rs_success_rate": success_rate,
        "required_success_threshold": threshold,
        "threshold_deficit": deficit,
        "negative_formal_evidence_recorded": bool(next_failure.get("negative_formal_evidence_recorded")),
    }


def _current_gate(*, next_round: dict[str, Any], h02: dict[str, Any]) -> dict[str, Any]:
    permissions = next_round.get("permissions_now") if isinstance(next_round.get("permissions_now"), dict) else {}
    blocked_acceptance = next_round.get("blocked_formal_acceptance") if isinstance(next_round.get("blocked_formal_acceptance"), dict) else {}
    return {
        "new_success_training_allowed_now": bool(permissions.get("new_success_training_allowed_now")),
        "local_training_allowed_now": bool(permissions.get("local_training_allowed_now")),
        "formal_claim_allowed_now": bool(permissions.get("formal_claim_allowed_now")),
        "new_or_revised_contract_required_before_new_success_training": bool(
            permissions.get("new_or_revised_contract_required_before_new_success_training", True)
        ),
        "h02_status": blocked_acceptance.get("h02_status") or h02.get("status"),
        "formal_output_accepted": bool(blocked_acceptance.get("formal_output_accepted") or h02.get("formal_output_accepted")),
        "paper_result_input_allowed": bool(blocked_acceptance.get("paper_result_input_allowed") or h02.get("paper_result_input_allowed")),
        "h02_blockers": _strings(blocked_acceptance.get("blockers") or h02.get("blockers")),
    }


def _decision_fields() -> list[dict[str, Any]]:
    return [
        _decision_field(
            "protocol_lane",
            "Choose the next protocol lane: stronger warm-start, full patch-CNN policy, hybrid PPO+analytic fallback, or abandon PPO replacement.",
            [
                "explicit lane name",
                "reason for changing or preserving the previous protocol after observing the failed run",
                "which prior failure evidence the lane is intended to address",
            ],
        ),
        _decision_field(
            "hypothesis",
            "Lock the next-round hypothesis before training.",
            [
                "one falsifiable hypothesis",
                "expected mechanism, not just expected metric increase",
                "scope statement for whether this is PPO replacing RS or PPO assisting RS",
            ],
        ),
        _decision_field(
            "success_signal",
            "Lock the success signal before training.",
            [
                "terminal-RS success threshold",
                "minimum evaluation episode count",
                "allowed comparison baseline and paired-test rule",
            ],
        ),
        _decision_field(
            "failure_signal",
            "Lock a failure signal that is not merely the negation of success.",
            [
                "collapse or unsafe-behavior criterion",
                "collision/truncation/timeout criterion",
                "criteria for stopping rather than extending budget after seeing weak results",
            ],
        ),
        _decision_field(
            "training_budget_and_seed_policy",
            "Lock budget and seed policy before training.",
            [
                "remote host",
                "total timesteps or wall-clock budget",
                "seed count and retry policy",
                "checkpoint cadence and retention rule",
            ],
        ),
        _decision_field(
            "protocol_delta",
            "Lock every protocol delta from the failed warm-start run.",
            [
                "reward changes",
                "curriculum changes",
                "observation or architecture changes",
                "warm-start source and admissible initialization",
            ],
        ),
        _decision_field(
            "h01_h02_acceptance_plan",
            "Lock how the next run will become paper-eligible if it passes.",
            [
                "H01 manifest scale",
                "H02 formal output schema",
                "PPO row naming and checkpoint hash fields",
                "paper-result gate condition",
            ],
        ),
    ]


def _decision_field(field_id: str, prompt: str, required_evidence: list[str]) -> dict[str, Any]:
    return {
        "field_id": field_id,
        "status": "awaiting_dr_sun_decision",
        "prompt": prompt,
        "required_evidence": required_evidence,
        "invalid_substitutes": [
            "chat summary without committed contract",
            "post-hoc explanation written after new training",
            "paper prose or appendix text",
        ],
    }


def _candidate_protocol_lanes() -> list[dict[str, Any]]:
    return [
        {
            "lane_id": "stronger_obstacle_summary_warm_start",
            "status": "candidate_requires_contract",
            "what_changes": "keep compact obstacle-summary policy family but strengthen warm-start dataset, curriculum, or PPO stabilization protocol",
            "must_justify": [
                "why the 0.53125 formal success rate is expected to improve",
                "which failure modes are addressed without changing the meaning of PPO-vs-RS",
            ],
        },
        {
            "lane_id": "full_patch_cnn_policy",
            "status": "candidate_requires_contract",
            "what_changes": "move from compact summary features toward a spatial patch/CNN observation policy",
            "must_justify": [
                "why spatial structure is necessary for the formal gate",
                "how observation and architecture changes preserve a fair RS replacement claim",
            ],
        },
        {
            "lane_id": "hybrid_ppo_analytic_fallback",
            "status": "candidate_requires_contract",
            "what_changes": "treat PPO as a learned selector or recovery layer instead of direct RS replacement",
            "must_justify": [
                "whether the claim changes from replacement to hybrid assistance",
                "how hybrid control is evaluated without hiding RS usage",
            ],
        },
        {
            "lane_id": "stop_or_reframe_module2_claim",
            "status": "candidate_requires_contract",
            "what_changes": "record the formal failure and stop pursuing PPO replacement under the current module2 claim",
            "must_justify": [
                "which negative evidence is sufficient to stop",
                "what paper claim remains defensible without formal PPO success",
            ],
        },
    ]


def _contract_output_requirements() -> dict[str, Any]:
    return {
        "required_location_pattern": ".pipeline/contracts/module2-*.md",
        "allowed_status_before_training": ["approved", "frozen"],
        "draft_status_allows_training": False,
        "required_sections": [
            "hypothesis",
            "success_signal",
            "failure_signal",
            "protocol_delta_from_failed_run",
            "training_budget_and_seed_policy",
            "evaluation_and_acceptance_plan",
            "paper_claim_boundary",
        ],
        "post_contract_next_artifacts": [
            "remote execution packet for the selected protocol",
            "source freshness audit after the contract commit",
            "remote-only training checkpoint bundle",
            "formal Gate3 eval CSV/summary",
            "Gate3 formal audit and checkpoint hash acceptance",
            "H02 formal output acceptance",
        ],
    }


def _audit_issues(
    *,
    next_round: dict[str, Any],
    current_failure: dict[str, Any],
    current_gate: dict[str, Any],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if next_round.get("status") != "formal_gate_next_round_requirements_ready":
        issues.append(_issue("next_round_requirements_not_ready", "Next-round requirements must be ready before contract intake."))
    if current_failure.get("formal_decision") != "fail":
        issues.append(_issue("current_formal_decision_not_fail", "Contract intake expects a failed formal Gate3 run."))
    if current_failure.get("failure_mode") != "threshold_failure":
        issues.append(_issue("current_failure_not_threshold_failure", "Contract intake expects threshold failure evidence."))
    if current_gate["new_success_training_allowed_now"]:
        issues.append(_issue("new_success_training_allowed_before_contract", "New success training must remain blocked before contract approval."))
    if current_gate["local_training_allowed_now"]:
        issues.append(_issue("local_training_allowed", "Local PPO training must remain disallowed."))
    if current_gate["formal_claim_allowed_now"]:
        issues.append(_issue("formal_claim_allowed", "Formal claim must remain blocked."))
    if current_gate["formal_output_accepted"] or current_gate["paper_result_input_allowed"]:
        issues.append(_issue("h02_accepts_failed_run", "H02 must not accept the failed run as paper result input."))
    if "gate3_formal_audit_not_passed" not in current_gate["h02_blockers"]:
        issues.append(_issue("h02_missing_gate3_failure_blocker", "H02 blockers must include gate3_formal_audit_not_passed."))
    return _unique_issues(issues)


def _markdown(manifest: dict[str, Any]) -> str:
    failure = manifest["current_failed_run"]
    gate = manifest["current_gate"]
    lines = [
        "# Module2 Formal Gate Contract Intake",
        "",
        "This file is a formal-gate decision intake artifact, not paper result material.",
        "",
        "## Current Failed Run",
        "",
        f"- formal_decision: `{failure['formal_decision']}`",
        f"- failure_mode: `{failure['failure_mode']}`",
        f"- terminal_rs_success_rate: `{failure['terminal_rs_success_rate']}`",
        f"- required_success_threshold: `{failure['required_success_threshold']}`",
        f"- threshold_deficit: `{failure['threshold_deficit']}`",
        "",
        "## Gate Boundaries",
        "",
        f"- new_success_training_allowed_now: `{gate['new_success_training_allowed_now']}`",
        f"- local_training_allowed_now: `{gate['local_training_allowed_now']}`",
        f"- formal_claim_allowed_now: `{gate['formal_claim_allowed_now']}`",
        f"- h02_status: `{gate['h02_status']}`",
        f"- h02_blockers: `{', '.join(gate['h02_blockers'])}`",
        "",
        "## Required Contract Decisions",
        "",
        "| field | status | prompt |",
        "|---|---|---|",
    ]
    for field in manifest["decision_fields_required_for_contract"]:
        lines.append(f"| `{field['field_id']}` | `{field['status']}` | {field['prompt']} |")
    lines.extend(["", "## Candidate Protocol Lanes", "", "| lane | status | change |", "|---|---|---|"])
    for lane in manifest["candidate_protocol_lanes"]:
        lines.append(f"| `{lane['lane_id']}` | `{lane['status']}` | {lane['what_changes']} |")
    lines.extend(["", "## Invalid Shortcuts"])
    for shortcut in manifest["invalid_shortcuts"]:
        lines.append(f"- {shortcut}")
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


def _int(value: Any) -> int | None:
    try:
        if value is None:
            return None
        return int(value)
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
