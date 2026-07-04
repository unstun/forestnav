from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_source_freshness_audit")


@dataclass(frozen=True)
class ArtifactTarget:
    artifact_id: str
    category: str
    path: Path
    required_before: str


DEFAULT_ARTIFACTS = (
    ArtifactTarget(
        "f02_6_decision_record",
        "decision",
        Path("0_trials/module2_f02_6_decision_record/f02_6_decision_record.json"),
        "approved_remote_preflight",
    ),
    ArtifactTarget(
        "f02_6_decision_intake",
        "decision",
        Path("0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json"),
        "approved_remote_preflight",
    ),
    ArtifactTarget(
        "f02_6_decision_gate_audit",
        "decision",
        Path("0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.json"),
        "approved_remote_preflight",
    ),
    ArtifactTarget(
        "f02_6_transition_gate_audit",
        "decision",
        Path("0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json"),
        "approved_remote_preflight",
    ),
    ArtifactTarget(
        "remote_formal_execution_packet",
        "remote_execution",
        Path("0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json"),
        "approved_remote_preflight",
    ),
    ArtifactTarget(
        "h01_evaluation_manifest",
        "evaluation",
        Path("0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json"),
        "formal_h01_h02",
    ),
    ArtifactTarget(
        "h02_formal_acceptance",
        "acceptance",
        Path("0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json"),
        "formal_h01_h02",
    ),
    ArtifactTarget(
        "claim_safety",
        "claim_gate",
        Path("0_trials/module2_claim_safety/module2_claim_safety.json"),
        "formal_claim_gate",
    ),
    ArtifactTarget(
        "paper_readiness",
        "claim_gate",
        Path("0_trials/module2_paper_readiness/module2_paper_readiness.json"),
        "formal_claim_gate",
    ),
    ArtifactTarget(
        "formal_gate_gap_audit",
        "formal_gate",
        Path("0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json"),
        "approved_remote_preflight",
    ),
    ArtifactTarget(
        "post_f02_6_plan_audit",
        "formal_gate",
        Path("0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json"),
        "approved_remote_preflight",
    ),
    ArtifactTarget(
        "remote_packet_safety_audit",
        "formal_gate",
        Path("0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json"),
        "approved_remote_preflight",
    ),
    ArtifactTarget(
        "formal_gate_closure_checklist",
        "formal_gate",
        Path("0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json"),
        "approved_remote_preflight",
    ),
    ArtifactTarget(
        "gpu3070ti_readiness_refresh",
        "remote_readiness",
        Path("0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.json"),
        "approved_remote_preflight",
    ),
    ArtifactTarget(
        "formal_gate_missing_artifacts",
        "formal_gate",
        Path("0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json"),
        "formal_claim_gate",
    ),
    ArtifactTarget(
        "formal_gate_status_report",
        "formal_gate",
        Path("0_trials/module2_formal_gate_status_report/formal_gate_status_report.json"),
        "formal_claim_gate",
    ),
    ArtifactTarget(
        "formal_gate_remaining_deliverables",
        "formal_gate",
        Path("0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json"),
        "formal_claim_gate",
    ),
    ArtifactTarget(
        "formal_gate_proof_audit",
        "formal_gate",
        Path("0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json"),
        "formal_claim_gate",
    ),
    ArtifactTarget(
        "formal_gate_handoff_bundle",
        "formal_gate",
        Path("0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json"),
        "approved_remote_preflight",
    ),
)


@dataclass(frozen=True)
class SourceFreshnessAuditConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    artifacts: Sequence[ArtifactTarget] = DEFAULT_ARTIFACTS


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = SourceFreshnessAuditConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "source_freshness_audit.json"
    markdown_out = config.markdown_out or output_dir / "source_freshness_audit.md"
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


def build_manifest(config: SourceFreshnessAuditConfig) -> dict[str, Any]:
    current_head = _current_head()
    records = [_artifact_record(target, current_head=current_head) for target in config.artifacts]
    risk_counts = _risk_counts(records)
    freshness_risks = [record for record in records if record["freshness_state"] != "current_clean"]
    status = "source_freshness_clean_current" if not freshness_risks else "source_freshness_risks_recorded_gate_still_blocked"
    return {
        "schema_version": 1,
        "artifact_name": "module2_source_freshness_audit",
        "status": status,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "not_paper_result_material": True,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "current_head": current_head,
        "artifact_count": len(records),
        "risk_counts": risk_counts,
        "regeneration_required_before_remote_formal_execution": bool(freshness_risks),
        "artifact_records": records,
        "ordered_regeneration_targets": _ordered_regeneration_targets(records),
        "claim_boundaries": [
            "This audit records source-head freshness only; it is not a training run or paper result.",
            "Historical or dirty source_head values are regeneration risks, not formal experimental failures.",
            "F02.6 remains the human approval gate before approved remote preflight or formal PPO training.",
            "Regenerate stale/dirty gate artifacts after F02.6 closes and before H01/H02 formal evaluation or formal claims.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit Module2 gate artifact source_head freshness without running training.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    return parser.parse_args(list(argv) if argv is not None else None)


def _artifact_record(target: ArtifactTarget, *, current_head: str) -> dict[str, Any]:
    payload = _read_json(target.path)
    source_head = payload.get("source_head")
    source_info = _source_info(source_head, current_head=current_head)
    return {
        "artifact_id": target.artifact_id,
        "category": target.category,
        "path": str(target.path),
        "exists": target.path.is_file(),
        "status": payload.get("status"),
        "source_head": source_head,
        "source_commit": source_info["source_commit"],
        "current_head": current_head,
        "source_head_dirty": source_info["source_head_dirty"],
        "source_commit_exists": source_info["source_commit_exists"],
        "matches_current_head": source_info["matches_current_head"],
        "freshness_state": source_info["freshness_state"],
        "required_before": target.required_before,
        "regenerate_before_formal_execution": source_info["freshness_state"] != "current_clean",
    }


def _source_info(source_head: Any, *, current_head: str) -> dict[str, Any]:
    if not source_head:
        return {
            "source_commit": None,
            "source_head_dirty": None,
            "source_commit_exists": False,
            "matches_current_head": False,
            "freshness_state": "missing_source_head",
        }
    raw = str(source_head)
    dirty = raw.endswith("+dirty")
    commit = raw.removesuffix("+dirty")
    commit_exists = _commit_exists(commit)
    matches = commit == current_head
    if matches and not dirty:
        state = "current_clean"
    elif matches and dirty:
        state = "current_dirty"
    elif commit_exists and dirty:
        state = "historical_dirty"
    elif commit_exists:
        state = "historical_clean"
    else:
        state = "unknown_or_missing_commit"
    return {
        "source_commit": commit,
        "source_head_dirty": dirty,
        "source_commit_exists": commit_exists,
        "matches_current_head": matches,
        "freshness_state": state,
    }


def _risk_counts(records: Sequence[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        state = str(record["freshness_state"])
        counts[state] = counts.get(state, 0) + 1
    return counts


def _ordered_regeneration_targets(records: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    order = {"approved_remote_preflight": 0, "formal_h01_h02": 1, "formal_claim_gate": 2}
    targets = [
        {
            "artifact_id": record["artifact_id"],
            "path": record["path"],
            "freshness_state": record["freshness_state"],
            "source_head": record["source_head"],
            "source_commit": record["source_commit"],
            "source_head_dirty": record["source_head_dirty"],
            "source_commit_exists": record["source_commit_exists"],
            "matches_current_head": record["matches_current_head"],
            "current_head": record["current_head"],
            "required_before": record["required_before"],
        }
        for record in records
        if record["freshness_state"] != "current_clean" or record["artifact_id"] == "formal_gate_handoff_bundle"
    ]
    return sorted(targets, key=lambda item: (order.get(str(item["required_before"]), 99), str(item["artifact_id"])))


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 Source Freshness Audit",
        "",
        "This file records gate artifact source-head freshness. It is not a training run, remote preflight, paper table, or result claim.",
        "",
        f"- status: `{manifest['status']}`",
        f"- current_head: `{manifest['current_head']}`",
        f"- runs_training: `{manifest['runs_training']}`",
        f"- runs_remote_preflight: `{manifest['runs_remote_preflight']}`",
        f"- formal_claim_allowed: `{manifest['formal_claim_allowed']}`",
        f"- regeneration_required_before_remote_formal_execution: `{manifest['regeneration_required_before_remote_formal_execution']}`",
        "",
        "## Risk Counts",
        "",
    ]
    for key, value in sorted(manifest["risk_counts"].items()):
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Regeneration Targets", ""])
    if manifest["ordered_regeneration_targets"]:
        for target in manifest["ordered_regeneration_targets"]:
            lines.append(
                f"- `{target['artifact_id']}`: `{target['freshness_state']}`, "
                f"source_head=`{target['source_head']}`, current_head=`{target['current_head']}`, "
                f"dirty=`{target['source_head_dirty']}`, commit_exists=`{target['source_commit_exists']}`, "
                f"required before `{target['required_before']}`, path `{target['path']}`"
            )
    else:
        lines.append("- none")
    lines.extend(["", "## Artifact Records", ""])
    for record in manifest["artifact_records"]:
        lines.append(
            f"- `{record['artifact_id']}`: status=`{record['status']}`, "
            f"freshness=`{record['freshness_state']}`, source_head=`{record['source_head']}`"
        )
    lines.extend(["", "## Claim Boundaries", ""])
    for boundary in manifest["claim_boundaries"]:
        lines.append(f"- {boundary}")
    lines.append("")
    return "\n".join(lines)


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _current_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()


def _source_head() -> str:
    try:
        head = _current_head()
        dirty = subprocess.run(["git", "diff", "--quiet"], check=False)
        staged_dirty = subprocess.run(["git", "diff", "--cached", "--quiet"], check=False)
        suffix = "+dirty" if dirty.returncode != 0 or staged_dirty.returncode != 0 else ""
        return f"{head}{suffix}"
    except Exception:
        return "unknown"


def _commit_exists(commit: str) -> bool:
    if not commit:
        return False
    result = subprocess.run(["git", "cat-file", "-e", f"{commit}^{{commit}}"], check=False)
    return result.returncode == 0


if __name__ == "__main__":
    raise SystemExit(main())
