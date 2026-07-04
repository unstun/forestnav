from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_post_f02_6_plan_audit")
DEFAULT_PLAN = Path("0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json")
DEFAULT_FORMAL_GATE = Path("0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json")
DEFAULT_SOURCE_FRESHNESS = Path("0_trials/module2_source_freshness_audit/source_freshness_audit.json")
DEFAULT_MISSING_ARTIFACTS = Path("0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json")
REQUIRED_STAGE_ORDER = (
    "f02_6_decision_record",
    "regenerate_preflight_gate_artifacts",
    "approved_remote_preflight",
    "regenerate_remote_execution_packet",
    "gate3_remote_training",
    "gate3_remote_audit_pullback",
    "regenerate_h01_h02_formal_artifacts",
    "regenerate_claim_gate_artifacts",
)


@dataclass(frozen=True)
class PostF026PlanAuditConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    plan_path: Path = DEFAULT_PLAN
    formal_gate_path: Path = DEFAULT_FORMAL_GATE
    source_freshness_path: Path = DEFAULT_SOURCE_FRESHNESS
    missing_artifacts_path: Path = DEFAULT_MISSING_ARTIFACTS


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = PostF026PlanAuditConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        plan_path=args.plan,
        formal_gate_path=args.formal_gate,
        source_freshness_path=args.source_freshness_audit,
        missing_artifacts_path=args.missing_artifacts_audit,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "post_f02_6_plan_audit.json"
    markdown_out = config.markdown_out or output_dir / "post_f02_6_plan_audit.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: PostF026PlanAuditConfig) -> dict[str, Any]:
    plan = _read_json(config.plan_path)
    formal_gate = _read_json(config.formal_gate_path)
    source_freshness = _read_json(config.source_freshness_path)
    missing_artifacts = _read_json(config.missing_artifacts_path)
    issues = _audit_issues(
        plan=plan,
        formal_gate=formal_gate,
        source_freshness=source_freshness,
        missing_artifacts=missing_artifacts,
        missing_artifacts_path=config.missing_artifacts_path,
    )
    return {
        "schema_version": 1,
        "artifact_name": "module2_post_f02_6_plan_audit",
        "status": "post_f02_6_plan_audit_passed" if not issues else "post_f02_6_plan_audit_failed",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "inputs": {
            "post_f02_6_regeneration_plan": str(config.plan_path),
            "formal_gate_gap_audit": str(config.formal_gate_path),
            "source_freshness_audit": str(config.source_freshness_path),
            "formal_gate_missing_artifacts_audit": str(config.missing_artifacts_path),
        },
        "plan_status": plan.get("status"),
        "missing_artifacts_summary": _missing_artifacts_summary(config.missing_artifacts_path, missing_artifacts),
        "audit_issue_count": len(issues),
        "audit_issues": issues,
        "required_stage_order": list(REQUIRED_STAGE_ORDER),
        "current_blocking_summary": _current_blocking_summary(plan),
        "claim_boundaries": [
            "This audit validates a plan artifact; it does not execute the plan.",
            "A passing audit is not permission to train while F02.6 remains pending.",
            "A passing audit is not a paper result or formal performance claim.",
            "Training stages must remain remote-only on gpu3070ti-relay and blocked until upstream gates pass.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit the Module2 post-F02.6 regeneration plan without executing it.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--formal-gate", type=Path, default=DEFAULT_FORMAL_GATE)
    parser.add_argument("--source-freshness-audit", type=Path, default=DEFAULT_SOURCE_FRESHNESS)
    parser.add_argument("--missing-artifacts-audit", type=Path, default=DEFAULT_MISSING_ARTIFACTS)
    return parser.parse_args(list(argv) if argv is not None else None)


def _audit_issues(
    *,
    plan: dict[str, Any],
    formal_gate: dict[str, Any],
    source_freshness: dict[str, Any],
    missing_artifacts: dict[str, Any],
    missing_artifacts_path: Path,
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    issues.extend(_top_level_issues(plan))
    issues.extend(_stage_order_issues(plan))
    issues.extend(_stage_safety_issues(plan))
    issues.extend(_pending_gate_issues(plan))
    issues.extend(_cross_artifact_issues(plan=plan, formal_gate=formal_gate, source_freshness=source_freshness))
    issues.extend(_missing_artifacts_issues(plan=plan, missing_artifacts=missing_artifacts, missing_artifacts_path=missing_artifacts_path))
    return _unique_issues(issues)


def _top_level_issues(plan: dict[str, Any]) -> list[dict[str, Any]]:
    expected_false = {
        "executes_commands": "Plan artifact must not execute commands.",
        "runs_training": "Plan artifact must not run training.",
        "runs_remote_preflight": "Plan artifact must not run remote preflight.",
        "local_training_allowed": "Plan artifact must preserve local-training prohibition.",
        "formal_claim_allowed": "Plan artifact must not allow formal claims.",
    }
    issues: list[dict[str, Any]] = []
    if plan.get("artifact_name") != "module2_post_f02_6_regeneration_plan":
        issues.append(_issue("plan_wrong_artifact_name", f"artifact_name={plan.get('artifact_name')!r}"))
    if plan.get("not_paper_result_material") is not True:
        issues.append(_issue("plan_not_marked_non_result", "not_paper_result_material must be true"))
    for key, message in expected_false.items():
        if plan.get(key) is not False:
            issues.append(_issue(f"plan_top_level_{key}_not_false", message, observed=plan.get(key)))
    return issues


def _stage_order_issues(plan: dict[str, Any]) -> list[dict[str, Any]]:
    stages = _stages(plan)
    ids = [str(stage.get("stage_id")) for stage in stages]
    issues: list[dict[str, Any]] = []
    for required in REQUIRED_STAGE_ORDER:
        if required not in ids:
            issues.append(_issue(f"missing_stage_{required}", "Required stage is absent.", observed=ids))
    present_required = [stage_id for stage_id in ids if stage_id in REQUIRED_STAGE_ORDER]
    if present_required != [stage_id for stage_id in REQUIRED_STAGE_ORDER if stage_id in present_required]:
        issues.append(_issue("stage_order_invalid", "Required stages are not in the expected order.", observed=present_required))
    return issues


def _stage_safety_issues(plan: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for stage in _stages(plan):
        stage_id = str(stage.get("stage_id"))
        if stage.get("runs_training") is True:
            if stage.get("host") != "gpu3070ti-relay":
                issues.append(_issue("training_stage_not_gpu3070ti", f"{stage_id} host must be gpu3070ti-relay.", observed=stage.get("host")))
            if stage.get("allowed_now") is True and "ssh gpu3070ti-relay" not in "\n".join(_strings(stage.get("command_templates"))):
                issues.append(_issue("ready_training_stage_missing_remote_ssh", f"{stage_id} is ready but command is not an ssh gpu3070ti-relay command."))
        if stage.get("runs_remote_preflight") is True and stage.get("host") != "gpu3070ti-relay":
            issues.append(_issue("remote_preflight_stage_not_gpu3070ti", f"{stage_id} host must be gpu3070ti-relay.", observed=stage.get("host")))
        if stage.get("phase") == "claim_gate" and stage.get("allowed_now") is True:
            issues.append(_issue("claim_gate_ready_before_formal_acceptance", f"{stage_id} must not be ready before formal acceptance."))
    return issues


def _pending_gate_issues(plan: dict[str, Any]) -> list[dict[str, Any]]:
    summary = plan.get("current_gate_summary") if isinstance(plan.get("current_gate_summary"), dict) else {}
    blocking = plan.get("blocking_summary") if isinstance(plan.get("blocking_summary"), dict) else {}
    decision_status = str(summary.get("f02_6_decision_status"))
    if decision_status != "pending_human_decision":
        return []
    issues: list[dict[str, Any]] = []
    if plan.get("status") != "blocked_until_f02_6_decision":
        issues.append(_issue("pending_f02_6_wrong_plan_status", "Pending F02.6 must keep the plan blocked.", observed=plan.get("status")))
    if blocking.get("training_allowed_now") is not False:
        issues.append(_issue("pending_f02_6_allows_training", "Training must not be allowed while F02.6 is pending."))
    if blocking.get("remote_preflight_allowed_now") is not False:
        issues.append(_issue("pending_f02_6_allows_remote_preflight", "Remote preflight must not be allowed while F02.6 is pending."))
    training = _stage_by_id(plan, "gate3_remote_training")
    if training.get("allowed_now") is True:
        issues.append(_issue("training_stage_allowed_before_f02_6", "Training stage is ready while F02.6 is pending."))
    for blocker in ("f02_6_decision_not_approved", "remote_packet_not_ready"):
        if blocker not in _strings(training.get("blocked_by")):
            issues.append(_issue(f"training_stage_missing_{blocker}", f"Training stage must include {blocker}."))
    if summary.get("source_freshness_regeneration_required") is True and "source_fresh_preflight_targets_open" not in _strings(training.get("blocked_by")):
        issues.append(_issue("training_stage_missing_source_fresh_blocker", "Training stage must reflect source freshness regeneration blocker."))
    decision = _stage_by_id(plan, "f02_6_decision_record")
    if decision.get("allowed_now") is not True or decision.get("requires_human_input") is not True:
        issues.append(_issue("pending_decision_stage_not_human_ready", "Pending F02.6 should expose only the human decision-record stage as ready."))
    return issues


def _cross_artifact_issues(*, plan: dict[str, Any], formal_gate: dict[str, Any], source_freshness: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    summary = plan.get("current_gate_summary") if isinstance(plan.get("current_gate_summary"), dict) else {}
    formal_state = formal_gate.get("current_gate_state") if isinstance(formal_gate.get("current_gate_state"), dict) else {}
    if formal_state and summary.get("f02_6_decision_status") != formal_state.get("f02_6_decision_status"):
        issues.append(
            _issue(
                "plan_formal_gate_decision_status_mismatch",
                "Plan F02.6 status does not match formal gate.",
                observed={"plan": summary.get("f02_6_decision_status"), "formal_gate": formal_state.get("f02_6_decision_status")},
            )
        )
    source_required = source_freshness.get("regeneration_required_before_remote_formal_execution")
    if source_freshness and summary.get("source_freshness_regeneration_required") != source_required:
        issues.append(
            _issue(
                "plan_source_freshness_requirement_mismatch",
                "Plan source freshness flag does not match source freshness audit.",
                observed={"plan": summary.get("source_freshness_regeneration_required"), "source_freshness": source_required},
            )
        )
    if source_freshness:
        plan_counts = _target_counts_by_gate(plan)
        source_counts = _source_target_counts_by_gate(source_freshness)
        if plan_counts != source_counts:
            issues.append(
                _issue(
                    "plan_source_regeneration_target_counts_mismatch",
                    "Plan target counts by gate do not match source freshness audit.",
                    observed={"plan": plan_counts, "source_freshness": source_counts},
                )
            )
    return issues


def _target_counts_by_gate(plan: dict[str, Any]) -> dict[str, int]:
    groups = plan.get("source_regeneration_targets_by_gate") if isinstance(plan.get("source_regeneration_targets_by_gate"), dict) else {}
    return {str(key): len(value) for key, value in sorted(groups.items()) if isinstance(value, list)}


def _source_target_counts_by_gate(source_freshness: dict[str, Any]) -> dict[str, int]:
    targets = source_freshness.get("ordered_regeneration_targets")
    if not isinstance(targets, list):
        return {}
    counts: dict[str, int] = {}
    for item in targets:
        if not isinstance(item, dict):
            continue
        gate = str(item.get("required_before") or "unknown")
        counts[gate] = counts.get(gate, 0) + 1
    return dict(sorted(counts.items()))


def _current_blocking_summary(plan: dict[str, Any]) -> dict[str, Any]:
    summary = plan.get("blocking_summary") if isinstance(plan.get("blocking_summary"), dict) else {}
    return {
        "plan_status": plan.get("status"),
        "training_allowed_now": summary.get("training_allowed_now"),
        "remote_preflight_allowed_now": summary.get("remote_preflight_allowed_now"),
        "ready_stage_ids": summary.get("ready_stage_ids", []),
        "blocked_stage_ids": summary.get("blocked_stage_ids", []),
    }


def _stage_by_id(plan: dict[str, Any], stage_id: str) -> dict[str, Any]:
    for stage in _stages(plan):
        if stage.get("stage_id") == stage_id:
            return stage
    return {}


def _stages(plan: dict[str, Any]) -> list[dict[str, Any]]:
    stages = plan.get("ordered_stages")
    if not isinstance(stages, list):
        return []
    return [stage for stage in stages if isinstance(stage, dict)]


def _strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item]


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
        "# Module2 Post-F02.6 Plan Audit",
        "",
        "This file audits the ordered post-F02.6 plan. It does not execute the plan.",
        "",
        f"- status: `{manifest['status']}`",
        f"- audit_issue_count: `{manifest['audit_issue_count']}`",
        f"- executes_commands: `{manifest['executes_commands']}`",
        f"- runs_training: `{manifest['runs_training']}`",
        f"- runs_remote_preflight: `{manifest['runs_remote_preflight']}`",
        "",
        "## Current Blocking Summary",
        "",
    ]
    for key, value in manifest["current_blocking_summary"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Audit Issues", ""])
    if manifest["audit_issues"]:
        for issue in manifest["audit_issues"]:
            lines.append(f"- `{issue['issue_id']}`: {issue['message']}")
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
