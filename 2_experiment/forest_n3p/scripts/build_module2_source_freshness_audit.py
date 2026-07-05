from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_source_freshness_audit")
CHANGED_PATH_SAMPLE_LIMIT = 12


@dataclass(frozen=True)
class ArtifactTarget:
    artifact_id: str
    category: str
    path: Path
    required_before: str


DEFAULT_ARTIFACTS = (
    ArtifactTarget(
        "f02_6_warm_start_decision_packet",
        "decision",
        Path("0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json"),
        "approved_remote_preflight",
    ),
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
        "post_f02_6_regeneration_plan",
        "formal_gate",
        Path("0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json"),
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
        "formal_gate_proof_summary_chain_audit",
        "formal_gate",
        Path("0_trials/module2_formal_gate_proof_summary_chain_audit/formal_gate_proof_summary_chain_audit.json"),
        "formal_claim_gate",
    ),
    ArtifactTarget(
        "mainline_formal_gate_state_audit",
        "formal_gate",
        Path("0_trials/module2_mainline_formal_gate_state_audit/mainline_formal_gate_state_audit.json"),
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
    tracked_artifact_paths = _tracked_artifact_paths(config)
    records = [
        _artifact_record(
            target,
            current_head=current_head,
            tracked_artifact_paths=tracked_artifact_paths,
        )
        for target in config.artifacts
    ]
    risk_counts = _risk_counts(records)
    commit_lag_summary = _commit_lag_summary(records)
    freshness_risks = [record for record in records if record["freshness_state"] != "current_clean"]
    blocking_regeneration_records = [record for record in records if _blocks_remote_formal_execution(record)]
    if not freshness_risks:
        status = "source_freshness_clean_current"
    elif not blocking_regeneration_records:
        status = "source_freshness_tracked_artifact_lag_only_gate_ready"
    else:
        status = "source_freshness_risks_recorded_gate_still_blocked"
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
        "commit_lag_summary": commit_lag_summary,
        "audit_self_reference_policy": _audit_self_reference_policy(config),
        "regeneration_required_before_remote_formal_execution": bool(freshness_risks),
        "blocking_regeneration_required_before_remote_formal_execution": bool(blocking_regeneration_records),
        "blocking_regeneration_target_count": len(blocking_regeneration_records),
        "self_artifact_only_lag_target_count": sum(1 for record in records if record["self_artifact_only_lag"] is True),
        "tracked_artifact_only_lag_target_count": sum(
            1 for record in records if record["tracked_artifact_only_lag"] is True
        ),
        "artifact_records": records,
        "ordered_regeneration_targets": _ordered_regeneration_targets(records),
        "blocking_ordered_regeneration_targets": _blocking_regeneration_targets(records),
        "claim_boundaries": [
            "This audit records source-head freshness only; it is not a training run or paper result.",
            "Historical or dirty source_head values are regeneration risks, not formal experimental failures.",
            "The audit artifact's own post-commit source_head lag is expected and is not a formal gate blocker by itself.",
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


def _artifact_record(target: ArtifactTarget, *, current_head: str, tracked_artifact_paths: set[str]) -> dict[str, Any]:
    payload = _read_json(target.path)
    source_head = payload.get("source_head")
    source_info = _source_info(source_head, current_head=current_head)
    lag_info = _source_lag_info(
        source_info,
        artifact_path=target.path,
        current_head=current_head,
        tracked_artifact_paths=tracked_artifact_paths,
    )
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
        "commits_since_source": lag_info["commits_since_source"],
        "changed_path_count_since_source": lag_info["changed_path_count_since_source"],
        "artifact_path_changed_since_source": lag_info["artifact_path_changed_since_source"],
        "self_artifact_changed_path_count_since_source": lag_info["self_artifact_changed_path_count_since_source"],
        "tracked_artifact_changed_path_count_since_source": lag_info[
            "tracked_artifact_changed_path_count_since_source"
        ],
        "non_self_changed_path_count_since_source": lag_info["non_self_changed_path_count_since_source"],
        "blocking_changed_path_count_since_source": lag_info["blocking_changed_path_count_since_source"],
        "self_artifact_only_lag": lag_info["self_artifact_only_lag"],
        "tracked_artifact_only_lag": lag_info["tracked_artifact_only_lag"],
        "changed_paths_since_source_sample": lag_info["changed_paths_since_source_sample"],
        "non_self_changed_paths_since_source_sample": lag_info["non_self_changed_paths_since_source_sample"],
        "blocking_changed_paths_since_source_sample": lag_info["blocking_changed_paths_since_source_sample"],
        "required_before": target.required_before,
        "regenerate_before_formal_execution": source_info["freshness_state"] != "current_clean",
        "blocking_regeneration_required_before_remote_formal_execution": _blocks_remote_formal_execution_from_parts(
            source_info=source_info,
            lag_info=lag_info,
        ),
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


def _source_lag_info(
    source_info: dict[str, Any],
    *,
    artifact_path: Path,
    current_head: str,
    tracked_artifact_paths: set[str],
) -> dict[str, Any]:
    source_commit = source_info["source_commit"]
    if not source_commit or not source_info["source_commit_exists"]:
        return _unknown_lag_info()
    if source_commit == current_head:
        return {
            "commits_since_source": 0,
            "changed_path_count_since_source": 0,
            "artifact_path_changed_since_source": False,
            "self_artifact_changed_path_count_since_source": 0,
            "tracked_artifact_changed_path_count_since_source": 0,
            "non_self_changed_path_count_since_source": 0,
            "blocking_changed_path_count_since_source": 0,
            "self_artifact_only_lag": False,
            "tracked_artifact_only_lag": False,
            "changed_paths_since_source_sample": [],
            "non_self_changed_paths_since_source_sample": [],
            "blocking_changed_paths_since_source_sample": [],
        }

    commits_since_source = _commits_since_source(str(source_commit), current_head)
    changed_paths = _changed_paths_since_source(str(source_commit), current_head)
    if commits_since_source is None or changed_paths is None:
        return _unknown_lag_info()

    self_artifact_paths = _self_artifact_paths(artifact_path)
    changed_path_set = set(changed_paths)
    self_changed_paths = [path for path in changed_paths if path in self_artifact_paths]
    tracked_artifact_changed_paths = [path for path in changed_paths if path in tracked_artifact_paths]
    non_self_changed_paths = [path for path in changed_paths if path not in self_artifact_paths]
    blocking_changed_paths = [path for path in changed_paths if path not in tracked_artifact_paths]
    return {
        "commits_since_source": commits_since_source,
        "changed_path_count_since_source": len(changed_paths),
        "artifact_path_changed_since_source": artifact_path.as_posix() in changed_path_set,
        "self_artifact_changed_path_count_since_source": len(self_changed_paths),
        "tracked_artifact_changed_path_count_since_source": len(tracked_artifact_changed_paths),
        "non_self_changed_path_count_since_source": len(non_self_changed_paths),
        "blocking_changed_path_count_since_source": len(blocking_changed_paths),
        "self_artifact_only_lag": commits_since_source > 0 and bool(self_changed_paths) and not non_self_changed_paths,
        "tracked_artifact_only_lag": commits_since_source > 0
        and bool(tracked_artifact_changed_paths)
        and not blocking_changed_paths,
        "changed_paths_since_source_sample": changed_paths[:CHANGED_PATH_SAMPLE_LIMIT],
        "non_self_changed_paths_since_source_sample": non_self_changed_paths[:CHANGED_PATH_SAMPLE_LIMIT],
        "blocking_changed_paths_since_source_sample": blocking_changed_paths[:CHANGED_PATH_SAMPLE_LIMIT],
    }


def _unknown_lag_info() -> dict[str, Any]:
    return {
        "commits_since_source": None,
        "changed_path_count_since_source": None,
        "artifact_path_changed_since_source": None,
        "self_artifact_changed_path_count_since_source": None,
        "tracked_artifact_changed_path_count_since_source": None,
        "non_self_changed_path_count_since_source": None,
        "blocking_changed_path_count_since_source": None,
        "self_artifact_only_lag": None,
        "tracked_artifact_only_lag": None,
        "changed_paths_since_source_sample": [],
        "non_self_changed_paths_since_source_sample": [],
        "blocking_changed_paths_since_source_sample": [],
    }


def _self_artifact_paths(artifact_path: Path) -> set[str]:
    paths = {artifact_path.as_posix()}
    if artifact_path.suffix == ".json":
        paths.add(artifact_path.with_suffix(".md").as_posix())
    return paths


def _tracked_artifact_paths(config: SourceFreshnessAuditConfig) -> set[str]:
    paths: set[str] = set()
    for target in config.artifacts:
        paths.update(_self_artifact_paths(target.path))
    manifest_path = config.manifest_out or Path(config.output_dir) / "source_freshness_audit.json"
    markdown_path = config.markdown_out or Path(config.output_dir) / "source_freshness_audit.md"
    paths.add(Path(manifest_path).as_posix())
    paths.add(Path(markdown_path).as_posix())
    return paths


def _risk_counts(records: Sequence[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        state = str(record["freshness_state"])
        counts[state] = counts.get(state, 0) + 1
    return counts


def _commit_lag_summary(records: Sequence[dict[str, Any]]) -> dict[str, Any]:
    known_commit_lags = [record["commits_since_source"] for record in records if record["commits_since_source"] is not None]
    known_non_self_counts = [
        record["non_self_changed_path_count_since_source"]
        for record in records
        if record["non_self_changed_path_count_since_source"] is not None
    ]
    known_blocking_counts = [
        record["blocking_changed_path_count_since_source"]
        for record in records
        if record["blocking_changed_path_count_since_source"] is not None
    ]
    return {
        "records_with_commit_lag": sum(1 for record in records if _positive_int(record["commits_since_source"])),
        "records_with_unknown_commit_lag": sum(1 for record in records if record["commits_since_source"] is None),
        "records_with_changed_paths_since_source": sum(
            1 for record in records if _positive_int(record["changed_path_count_since_source"])
        ),
        "records_with_artifact_path_changed_since_source": sum(
            1 for record in records if record["artifact_path_changed_since_source"] is True
        ),
        "records_with_non_self_changed_paths_since_source": sum(
            1 for record in records if _positive_int(record["non_self_changed_path_count_since_source"])
        ),
        "records_with_blocking_changed_paths_since_source": sum(
            1 for record in records if _positive_int(record["blocking_changed_path_count_since_source"])
        ),
        "records_with_self_artifact_only_lag": sum(1 for record in records if record["self_artifact_only_lag"] is True),
        "records_with_tracked_artifact_only_lag": sum(
            1 for record in records if record["tracked_artifact_only_lag"] is True
        ),
        "max_commits_since_source": max(known_commit_lags) if known_commit_lags else None,
        "max_non_self_changed_path_count_since_source": max(known_non_self_counts) if known_non_self_counts else None,
        "max_blocking_changed_path_count_since_source": max(known_blocking_counts) if known_blocking_counts else None,
        "changed_path_sample_limit": CHANGED_PATH_SAMPLE_LIMIT,
    }


def _audit_self_reference_policy(config: SourceFreshnessAuditConfig) -> dict[str, Any]:
    manifest_path = config.manifest_out or Path(config.output_dir) / "source_freshness_audit.json"
    markdown_path = config.markdown_out or Path(config.output_dir) / "source_freshness_audit.md"
    return {
        "source_head_scope": "generation_time_repository_head",
        "commit_storing_this_audit_known_at_generation": False,
        "expected_post_commit_self_lag": True,
        "self_lag_is_formal_gate_blocker": False,
        "manifest_path": str(manifest_path),
        "markdown_path": str(markdown_path),
    }


def _blocks_remote_formal_execution(record: dict[str, Any]) -> bool:
    return _blocks_remote_formal_execution_from_parts(
        source_info={
            "freshness_state": record.get("freshness_state"),
            "source_head_dirty": record.get("source_head_dirty"),
            "source_commit_exists": record.get("source_commit_exists"),
        },
        lag_info={
            "self_artifact_only_lag": record.get("self_artifact_only_lag"),
            "tracked_artifact_only_lag": record.get("tracked_artifact_only_lag"),
            "non_self_changed_path_count_since_source": record.get("non_self_changed_path_count_since_source"),
            "blocking_changed_path_count_since_source": record.get("blocking_changed_path_count_since_source"),
        },
    )


def _blocks_remote_formal_execution_from_parts(*, source_info: dict[str, Any], lag_info: dict[str, Any]) -> bool:
    state = source_info.get("freshness_state")
    if state == "current_clean":
        return False
    if (
        state == "historical_clean"
        and (
            lag_info.get("tracked_artifact_only_lag") is True
            or lag_info.get("self_artifact_only_lag") is True
        )
        and not _positive_int(lag_info.get("blocking_changed_path_count_since_source"))
    ):
        return False
    return True


def _positive_int(value: Any) -> bool:
    return isinstance(value, int) and value > 0


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
            "commits_since_source": record["commits_since_source"],
            "changed_path_count_since_source": record["changed_path_count_since_source"],
            "artifact_path_changed_since_source": record["artifact_path_changed_since_source"],
            "non_self_changed_path_count_since_source": record["non_self_changed_path_count_since_source"],
            "blocking_changed_path_count_since_source": record["blocking_changed_path_count_since_source"],
            "self_artifact_only_lag": record["self_artifact_only_lag"],
            "tracked_artifact_only_lag": record["tracked_artifact_only_lag"],
            "blocking_regeneration_required_before_remote_formal_execution": record[
                "blocking_regeneration_required_before_remote_formal_execution"
            ],
            "required_before": record["required_before"],
        }
        for record in records
        if record["freshness_state"] != "current_clean" or record["artifact_id"] == "formal_gate_handoff_bundle"
    ]
    return sorted(targets, key=lambda item: (order.get(str(item["required_before"]), 99), str(item["artifact_id"])))


def _blocking_regeneration_targets(records: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    return [target for target in _ordered_regeneration_targets(records) if target["blocking_regeneration_required_before_remote_formal_execution"] is True]


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
        f"- blocking_regeneration_required_before_remote_formal_execution: `{manifest['blocking_regeneration_required_before_remote_formal_execution']}`",
        f"- blocking_regeneration_target_count: `{manifest['blocking_regeneration_target_count']}`",
        f"- self_artifact_only_lag_target_count: `{manifest['self_artifact_only_lag_target_count']}`",
        f"- tracked_artifact_only_lag_target_count: `{manifest['tracked_artifact_only_lag_target_count']}`",
        "",
        "## Risk Counts",
        "",
    ]
    for key, value in sorted(manifest["risk_counts"].items()):
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Commit Lag Diagnostics", ""])
    for key, value in manifest["commit_lag_summary"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Audit Self-Reference Policy", ""])
    for key, value in manifest["audit_self_reference_policy"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Regeneration Targets", ""])
    if manifest["ordered_regeneration_targets"]:
        for target in manifest["ordered_regeneration_targets"]:
            lines.append(
                f"- `{target['artifact_id']}`: `{target['freshness_state']}`, "
                f"source_head=`{target['source_head']}`, current_head=`{target['current_head']}`, "
                f"dirty=`{target['source_head_dirty']}`, commit_exists=`{target['source_commit_exists']}`, "
                f"commits_since_source=`{target['commits_since_source']}`, "
                f"changed_paths_since_source=`{target['changed_path_count_since_source']}`, "
                f"non_self_changed_paths_since_source=`{target['non_self_changed_path_count_since_source']}`, "
                f"blocking_changed_paths_since_source=`{target['blocking_changed_path_count_since_source']}`, "
                f"self_artifact_only_lag=`{target['self_artifact_only_lag']}`, "
                f"tracked_artifact_only_lag=`{target['tracked_artifact_only_lag']}`, "
                f"blocking_regeneration=`{target['blocking_regeneration_required_before_remote_formal_execution']}`, "
                f"artifact_path_changed=`{target['artifact_path_changed_since_source']}`, "
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
    return module2_source_head()


def _commit_exists(commit: str) -> bool:
    if not commit:
        return False
    result = subprocess.run(["git", "cat-file", "-e", f"{commit}^{{commit}}"], check=False)
    return result.returncode == 0


def _commits_since_source(source_commit: str, current_head: str) -> int | None:
    try:
        raw = subprocess.check_output(["git", "rev-list", "--count", f"{source_commit}..{current_head}"], text=True)
    except Exception:
        return None
    try:
        return int(raw.strip())
    except ValueError:
        return None


def _changed_paths_since_source(source_commit: str, current_head: str) -> list[str] | None:
    try:
        raw = subprocess.check_output(["git", "diff", "--name-only", f"{source_commit}..{current_head}"], text=True)
    except Exception:
        return None
    return [line.strip() for line in raw.splitlines() if line.strip()]


if __name__ == "__main__":
    raise SystemExit(main())
