from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Iterable


MODULE2_GATE_ARTIFACTS = (
    "0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json",
    "0_trials/module2_f02_6_decision_record/f02_6_decision_record.json",
    "0_trials/module2_f02_6_decision_intake/f02_6_decision_intake.json",
    "0_trials/module2_f02_6_decision_gate_audit/f02_6_decision_gate_audit.json",
    "0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json",
    "0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json",
    "0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json",
    "0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json",
    "0_trials/module2_claim_safety/module2_claim_safety.json",
    "0_trials/module2_paper_readiness/module2_paper_readiness.json",
    "0_trials/module2_formal_gate_gap_audit/formal_gate_gap_audit.json",
    "0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json",
    "0_trials/module2_post_f02_6_plan_audit/post_f02_6_plan_audit.json",
    "0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json",
    "0_trials/module2_formal_gate_closure_checklist/formal_gate_closure_checklist.json",
    "0_trials/module2_gpu3070ti_readiness_refresh/readiness_refresh.json",
    "0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json",
    "0_trials/module2_formal_gate_status_report/formal_gate_status_report.json",
    "0_trials/module2_formal_gate_remaining_deliverables/formal_gate_remaining_deliverables.json",
    "0_trials/module2_formal_gate_proof_audit/formal_gate_proof_audit.json",
    "0_trials/module2_formal_gate_proof_summary_chain_audit/formal_gate_proof_summary_chain_audit.json",
    "0_trials/module2_mainline_formal_gate_state_audit/mainline_formal_gate_state_audit.json",
    "0_trials/module2_formal_gate_handoff_bundle/formal_gate_handoff_bundle.json",
    "0_trials/module2_formal_gate_failure_triage/formal_gate_failure_triage.json",
    "0_trials/module2_formal_gate_next_round_requirements/formal_gate_next_round_requirements.json",
    "0_trials/module2_formal_gate_contract_intake/formal_gate_contract_intake.json",
    "0_trials/module2_formal_gate_protocol_lane_matrix/formal_gate_protocol_lane_matrix.json",
    "0_trials/module2_formal_gate_protocol_lane_decision_packet/formal_gate_protocol_lane_decision_packet.json",
    "0_trials/module2_formal_gate_protocol_lane_decision_record/protocol_lane_decision_record.json",
    "0_trials/module2_source_freshness_audit/source_freshness_audit.json",
)


def module2_gate_artifact_paths(extra_paths: Iterable[str | Path] = ()) -> set[str]:
    paths: set[str] = set()
    for raw_path in [*MODULE2_GATE_ARTIFACTS, *extra_paths]:
        path = Path(raw_path)
        paths.add(_normalize_repo_path(path))
        if path.suffix == ".json":
            paths.add(_normalize_repo_path(path.with_suffix(".md")))
    return paths


def source_head(
    *,
    repo_root: Path | None = None,
    ignore_paths: Iterable[str | Path] = (),
    ignore_module2_gate_artifacts: bool = True,
) -> str:
    try:
        root = _repo_root(repo_root)
        head = _git_output(["rev-parse", "HEAD"], cwd=root)
        dirty_paths = _dirty_paths(root)
        ignored_paths = set(_normalize_repo_path(path, repo_root=root) for path in ignore_paths)
        if ignore_module2_gate_artifacts:
            ignored_paths.update(module2_gate_artifact_paths())
        return source_head_from_dirty_paths(head=head, dirty_paths=dirty_paths, ignored_paths=ignored_paths)
    except Exception:  # noqa: BLE001 - source provenance must not stop read-only artifact generation.
        return "unknown"


def source_head_from_dirty_paths(*, head: str, dirty_paths: Iterable[str | Path], ignored_paths: Iterable[str | Path]) -> str:
    dirty = {_normalize_repo_path(path) for path in dirty_paths}
    ignored = {_normalize_repo_path(path) for path in ignored_paths}
    blocking_dirty = dirty - ignored
    return f"{head}+dirty" if blocking_dirty else head


def _repo_root(repo_root: Path | None) -> Path:
    if repo_root is not None:
        return Path(repo_root)
    return Path(_git_output(["rev-parse", "--show-toplevel"], cwd=None))


def _dirty_paths(repo_root: Path) -> set[str]:
    paths: set[str] = set()
    for args in (
        ["diff", "--name-only"],
        ["diff", "--cached", "--name-only"],
        ["ls-files", "--others", "--exclude-standard"],
    ):
        raw = _git_output(args, cwd=repo_root)
        paths.update(_normalize_repo_path(line) for line in raw.splitlines() if line.strip())
    return paths


def _git_output(args: list[str], *, cwd: Path | None) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL).strip()


def _normalize_repo_path(path: str | Path, *, repo_root: Path | None = None) -> str:
    raw = Path(path)
    if raw.is_absolute() and repo_root is not None:
        try:
            raw = raw.relative_to(repo_root)
        except ValueError:
            pass
    return raw.as_posix().removeprefix("./")
