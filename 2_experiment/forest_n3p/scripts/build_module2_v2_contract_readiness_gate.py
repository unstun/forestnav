from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from forest_n3p.scripts import preflight_rl_rs_gate3_formal_trial as preflight
from forest_n3p.scripts._module2_source_head import source_head as module2_source_head


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_v2_contract_readiness_gate")
DEFAULT_CONTRACT_PATH = Path(".pipeline/contracts/module2-stronger_obstacle_summary_warm_start-v2.md")
DEFAULT_GAP_LEDGER_PATH = Path(".pipeline/experiments/20260706_module2_v2_formal_gate_gap_ledger.md")
DEFAULT_ATTEMPT_DIR = Path(
    "0_trials/module2_gate3_formal/gate3_stronger_obstacle_summary_warm_start_v2_seed20260706"
)
DEFAULT_ORACLE_PATH = Path("0_trials/module2_oracle_shape/oracle_connector_results.parquet")
DEFAULT_BC_CHECKPOINT = Path("2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt")
READY_CONTRACT_STATUSES = {"approved", "frozen"}
EXPECTED_PROTOCOL_LANE = "stronger_obstacle_summary_warm_start"
EXPECTED_CONTRACT_ACTION = "draft_new_contract"
EXPECTED_TRAINING_PARAMS = {
    "train_total_timesteps": 500000,
    "train_n_envs": 4,
    "train_n_steps": 256,
    "train_batch_size": 256,
    "train_n_epochs": 8,
    "train_learning_rate": 0.0001,
    "train_ent_coef": 0.01,
    "train_checkpoint_freq": 25000,
}
EXPECTED_RUNNER_ARGS = {
    "--train-total-timesteps": "500000",
    "--train-n-envs": "4",
    "--train-n-steps": "256",
    "--train-batch-size": "256",
    "--train-n-epochs": "8",
    "--train-learning-rate": "0.0001",
    "--train-ent-coef": "0.01",
    "--train-checkpoint-freq": "25000",
}
REQUIRED_CONTRACT_STRINGS = (
    "0.53125",
    "success_threshold=0.8",
    "gate3_stronger_obstacle_summary_warm_start_v2_seed20260706",
    "formal_output_accepted=true",
)


@dataclass(frozen=True)
class Module2V2ContractReadinessGateConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    contract_path: Path = DEFAULT_CONTRACT_PATH
    gap_ledger_path: Path = DEFAULT_GAP_LEDGER_PATH
    attempt_dir: Path = DEFAULT_ATTEMPT_DIR
    oracle_path: Path = DEFAULT_ORACLE_PATH
    bc_checkpoint: Path = DEFAULT_BC_CHECKPOINT


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = Module2V2ContractReadinessGateConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        contract_path=args.contract_path,
        gap_ledger_path=args.gap_ledger,
        attempt_dir=args.attempt_dir,
        oracle_path=args.oracle_path,
        bc_checkpoint=args.bc_checkpoint,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "v2_contract_readiness_gate.json"
    markdown_out = config.markdown_out or output_dir / "v2_contract_readiness_gate.md"
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


def build_manifest(config: Module2V2ContractReadinessGateConfig) -> dict[str, Any]:
    contract_text = _read_text(config.contract_path)
    frontmatter = _frontmatter(contract_text)
    preflight_probe = _preflight_probe(config)
    blockers = _readiness_blockers(
        contract_path=config.contract_path,
        gap_ledger_path=config.gap_ledger_path,
        contract_text=contract_text,
        frontmatter=frontmatter,
        preflight_probe=preflight_probe,
    )
    contract_status = str(frontmatter.get("status", "missing"))
    ready_for_source_freshness = contract_status in READY_CONTRACT_STATUSES and not blockers
    return {
        "schema_version": 1,
        "artifact_name": "module2_v2_contract_readiness_gate",
        "status": "v2_contract_ready_for_source_freshness" if ready_for_source_freshness else "v2_contract_readiness_blocked",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": module2_source_head(),
        "not_paper_result_material": True,
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "runs_remote_audit": False,
        "local_training_allowed_now": False,
        "remote_preflight_allowed_now": False,
        "remote_training_allowed_now": False,
        "formal_claim_allowed_now": False,
        "paper_result_material_allowed_now": False,
        "source_freshness_regeneration_allowed_after_contract": bool(ready_for_source_freshness),
        "remote_packet_generation_allowed_after_source_freshness": bool(ready_for_source_freshness),
        "inputs": {
            "contract": str(config.contract_path),
            "gap_ledger": str(config.gap_ledger_path),
            "attempt_dir": str(config.attempt_dir),
            "oracle_path": str(config.oracle_path),
            "bc_checkpoint": str(config.bc_checkpoint),
        },
        "contract_summary": _contract_summary(frontmatter),
        "expected_training_params": EXPECTED_TRAINING_PARAMS,
        "preflight_probe": preflight_probe,
        "runner_command_contains_v2_params": _runner_command_contains_expected_args(preflight_probe),
        "next_action": _next_action(contract_status=contract_status, blocker_count=len(blockers)),
        "blocker_count": len(blockers),
        "blockers": blockers,
        "invalid_substitutes": [
            "local PPO training output",
            "failed gate3_obstacle_summary_warm_approved_v1 checkpoint",
            "old v1 contract audit",
            "H02 smoke rows",
            "paper table or appendix prose",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit whether the Module2 v2 stronger warm-start contract can enter source-freshness.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--contract-path", type=Path, default=DEFAULT_CONTRACT_PATH)
    parser.add_argument("--gap-ledger", type=Path, default=DEFAULT_GAP_LEDGER_PATH)
    parser.add_argument("--attempt-dir", type=Path, default=DEFAULT_ATTEMPT_DIR)
    parser.add_argument("--oracle-path", type=Path, default=DEFAULT_ORACLE_PATH)
    parser.add_argument("--bc-checkpoint", type=Path, default=DEFAULT_BC_CHECKPOINT)
    return parser.parse_args(list(argv) if argv is not None else None)


def _preflight_probe(config: Module2V2ContractReadinessGateConfig) -> dict[str, Any]:
    raw_argv = [
        "--output-dir",
        str(config.attempt_dir),
        "--contract-path",
        str(config.contract_path),
        "--seed",
        "20260706",
        "--device",
        "cuda",
        "--oracle-path",
        str(config.oracle_path),
        "--heldout-seed",
        "20260706",
        "--train-total-timesteps",
        "500000",
        "--train-n-envs",
        "4",
        "--train-n-steps",
        "256",
        "--train-batch-size",
        "256",
        "--train-n-epochs",
        "8",
        "--train-learning-rate",
        "0.0001",
        "--train-ent-coef",
        "0.01",
        "--train-checkpoint-freq",
        "25000",
        "--eval-episodes",
        "64",
        "--eval-min-episodes",
        "64",
        "--eval-success-threshold",
        "0.8",
        "--bc-checkpoint",
        str(config.bc_checkpoint),
        "--warm-start-decision",
        "approved_obstacle_summary",
    ]
    args = preflight._parse_args(raw_argv)
    manifest = preflight.build_preflight_manifest(
        args=args,
        raw_argv=raw_argv,
        output_dir=config.attempt_dir,
        manifest_out=config.output_dir / "v2_preflight_probe.json",
    )
    protocol = manifest.get("protocol") if isinstance(manifest.get("protocol"), dict) else {}
    return {
        "preflight_status": manifest.get("preflight_status"),
        "formal_trial_ready": bool(manifest.get("formal_trial_ready")),
        "contract": manifest.get("contract"),
        "contract_status": manifest.get("contract_status"),
        "formal_blockers": manifest.get("formal_blockers", []),
        "protocol": {key: protocol.get(key) for key in ["contract", *EXPECTED_TRAINING_PARAMS.keys()]},
        "runner_command": manifest.get("runner_command"),
        "audit_command": manifest.get("audit_command"),
    }


def _readiness_blockers(
    *,
    contract_path: Path,
    gap_ledger_path: Path,
    contract_text: str,
    frontmatter: dict[str, Any],
    preflight_probe: dict[str, Any],
) -> list[dict[str, Any]]:
    blockers: list[dict[str, Any]] = []
    contract_status = str(frontmatter.get("status", "missing"))
    if contract_status not in READY_CONTRACT_STATUSES:
        blockers.append(
            _issue(
                "contract_status_not_approved_or_frozen",
                "v2 contract cannot enter source-freshness until status is approved or frozen",
                observed=contract_status,
                expected=sorted(READY_CONTRACT_STATUSES),
            )
        )
    if str(frontmatter.get("selected_protocol_lane")) != EXPECTED_PROTOCOL_LANE:
        blockers.append(
            _issue(
                "selected_protocol_lane_mismatch",
                "contract does not name the selected protocol lane",
                observed=frontmatter.get("selected_protocol_lane"),
                expected=EXPECTED_PROTOCOL_LANE,
            )
        )
    if str(frontmatter.get("contract_action")) != EXPECTED_CONTRACT_ACTION:
        blockers.append(
            _issue(
                "contract_action_mismatch",
                "contract action must match Dr Sun's recorded lane decision",
                observed=frontmatter.get("contract_action"),
                expected=EXPECTED_CONTRACT_ACTION,
            )
        )
    if set(_strings(frontmatter.get("allowed_status_before_training"))) != READY_CONTRACT_STATUSES:
        blockers.append(
            _issue(
                "allowed_status_before_training_mismatch",
                "contract must list approved and frozen as the only statuses that can unlock the next gate",
                observed=frontmatter.get("allowed_status_before_training"),
                expected=sorted(READY_CONTRACT_STATUSES),
            )
        )
    if _truthy(frontmatter.get("local_training_allowed_now")):
        blockers.append(_issue("local_training_allowed_in_contract", "contract must not authorize local training"))
    if _truthy(frontmatter.get("paper_result_material_allowed_now")):
        blockers.append(_issue("paper_result_material_allowed_in_contract", "contract must not authorize result material"))
    if not contract_path.exists():
        blockers.append(_issue("contract_file_missing", "v2 contract file is missing", observed=str(contract_path)))
    if not gap_ledger_path.exists():
        blockers.append(_issue("gap_ledger_missing", "v2 formal gate gap ledger is missing", observed=str(gap_ledger_path)))
    for needle in REQUIRED_CONTRACT_STRINGS:
        if needle not in contract_text:
            blockers.append(
                _issue(
                    "required_contract_evidence_missing",
                    f"contract text does not contain required evidence marker {needle!r}",
                    observed=needle,
                )
            )
    blockers.extend(_preflight_blockers(preflight_probe=preflight_probe, contract_path=contract_path, contract_status=contract_status))
    return blockers


def _preflight_blockers(*, preflight_probe: dict[str, Any], contract_path: Path, contract_status: str) -> list[dict[str, Any]]:
    blockers: list[dict[str, Any]] = []
    protocol = preflight_probe.get("protocol") if isinstance(preflight_probe.get("protocol"), dict) else {}
    runner_command = str(preflight_probe.get("runner_command") or "")
    if preflight_probe.get("contract") != str(contract_path):
        blockers.append(
            _issue(
                "preflight_contract_path_mismatch",
                "preflight probe did not preserve the v2 contract path",
                observed=preflight_probe.get("contract"),
                expected=str(contract_path),
            )
        )
    for key, expected in EXPECTED_TRAINING_PARAMS.items():
        if protocol.get(key) != expected:
            blockers.append(
                _issue(
                    "preflight_training_param_mismatch",
                    f"preflight protocol field {key} drifted",
                    observed={key: protocol.get(key)},
                    expected={key: expected},
                )
            )
    for flag, expected_value in EXPECTED_RUNNER_ARGS.items():
        expected_fragment = f"{flag} {expected_value}"
        if expected_fragment not in runner_command:
            blockers.append(
                _issue(
                    "runner_command_missing_v2_arg",
                    f"runner command is missing {expected_fragment}",
                    observed=runner_command,
                    expected=expected_fragment,
                )
            )
    reason_codes = {
        str(reason.get("code"))
        for reason in preflight_probe.get("formal_blockers", [])
        if isinstance(reason, dict)
    }
    if contract_status in READY_CONTRACT_STATUSES and "contract_not_approved" in reason_codes:
        blockers.append(_issue("approved_contract_blocked_by_preflight", "preflight still sees the contract as unapproved"))
    if contract_status not in READY_CONTRACT_STATUSES and "contract_not_approved" not in reason_codes:
        blockers.append(_issue("draft_contract_not_blocked_by_preflight", "draft contract should be blocked by preflight"))
    extra_preflight_blockers = reason_codes - {"contract_not_approved"}
    if extra_preflight_blockers:
        blockers.append(
            _issue(
                "unexpected_preflight_blockers",
                "preflight probe found blockers other than the expected draft-contract blocker",
                observed=sorted(extra_preflight_blockers),
            )
        )
    return blockers


def _contract_summary(frontmatter: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": frontmatter.get("status", "missing"),
        "selected_protocol_lane": frontmatter.get("selected_protocol_lane"),
        "contract_action": frontmatter.get("contract_action"),
        "training_allowed": _truthy(frontmatter.get("training_allowed")),
        "remote_training_allowed_now": _truthy(frontmatter.get("remote_training_allowed_now")),
        "local_training_allowed_now": _truthy(frontmatter.get("local_training_allowed_now")),
        "formal_claim_allowed_now": _truthy(frontmatter.get("formal_claim_allowed_now")),
        "paper_result_material_allowed_now": _truthy(frontmatter.get("paper_result_material_allowed_now")),
        "allowed_status_before_training": _strings(frontmatter.get("allowed_status_before_training")),
    }


def _next_action(*, contract_status: str, blocker_count: int) -> str:
    if contract_status not in READY_CONTRACT_STATUSES:
        return "promote_or_edit_v2_contract_before_source_freshness"
    if blocker_count:
        return "fix_v2_contract_readiness_blockers"
    return "regenerate_source_freshness_then_remote_packet"


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 V2 Contract Readiness Gate",
        "",
        "This file is a pre-execution gate artifact, not paper result material.",
        "",
        "## Status",
        "",
        f"- status: `{manifest['status']}`",
        f"- next_action: `{manifest['next_action']}`",
        f"- source_freshness_regeneration_allowed_after_contract: `{manifest['source_freshness_regeneration_allowed_after_contract']}`",
        f"- remote_training_allowed_now: `{manifest['remote_training_allowed_now']}`",
        f"- blocker_count: `{manifest['blocker_count']}`",
        "",
        "## Contract Summary",
        "",
    ]
    for key, value in manifest["contract_summary"].items():
        lines.append(f"- {key}: `{_fmt(value)}`")
    lines.extend(["", "## Preflight Probe", ""])
    probe = manifest["preflight_probe"]
    lines.append(f"- preflight_status: `{probe['preflight_status']}`")
    lines.append(f"- formal_trial_ready: `{probe['formal_trial_ready']}`")
    lines.append(f"- contract_status: `{probe['contract_status']}`")
    lines.append(f"- runner_command_contains_v2_params: `{manifest['runner_command_contains_v2_params']}`")
    lines.extend(["", "## Blockers", ""])
    if manifest["blockers"]:
        for blocker in manifest["blockers"]:
            lines.append(f"- `{blocker['issue_id']}`: {blocker['message']}")
    else:
        lines.append("- none")
    lines.extend(["", "## Invalid Substitutes", ""])
    for item in manifest["invalid_substitutes"]:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def _frontmatter(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    values: dict[str, Any] = {}
    current_list_key: str | None = None
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            break
        if stripped.startswith("- ") and current_list_key:
            values.setdefault(current_list_key, []).append(stripped[2:].strip())
            continue
        current_list_key = None
        if ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if raw_value:
            values[key] = _parse_scalar(raw_value)
        else:
            values[key] = []
            current_list_key = key
    return values


def _runner_command_contains_expected_args(preflight_probe: dict[str, Any]) -> bool:
    runner_command = str(preflight_probe.get("runner_command") or "")
    return all(f"{flag} {expected_value}" in runner_command for flag, expected_value in EXPECTED_RUNNER_ARGS.items())


def _parse_scalar(value: str) -> Any:
    lower = value.lower()
    if lower == "true":
        return True
    if lower == "false":
        return False
    return value


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _issue(issue_id: str, message: str, *, observed: Any | None = None, expected: Any | None = None) -> dict[str, Any]:
    issue = {"issue_id": issue_id, "message": message}
    if observed is not None:
        issue["observed"] = observed
    if expected is not None:
        issue["expected"] = expected
    return issue


def _strings(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value is None:
        return []
    return [str(value)]


def _truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes"}


def _fmt(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return str(value)


if __name__ == "__main__":
    raise SystemExit(main())
