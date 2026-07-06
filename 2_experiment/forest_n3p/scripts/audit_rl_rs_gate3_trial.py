from __future__ import annotations

import argparse
import json
import socket
import subprocess
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


DEFAULT_CONTRACT_PATH = ".pipeline/contracts/module2-ppo-funnel-expansion.md"


def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    args = _parse_args(raw_argv)
    trial_dir = Path(args.trial_dir)
    output_path = Path(args.output) if args.output else trial_dir / "gate3_formal_audit.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    result = audit_trial(
        trial_dir=trial_dir,
        min_formal_episodes=int(args.min_formal_episodes),
        required_success_threshold=float(args.required_success_threshold),
        required_train_curriculum=str(args.required_train_curriculum),
        required_eval_curriculum=str(args.required_eval_curriculum),
        warm_start_decision=str(args.warm_start_decision),
        expected_contract_path=str(args.contract_path),
        raw_argv=raw_argv,
    )
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit whether a Module2 F03 Gate #3 trial is formal evidence.")
    parser.add_argument("--trial-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--min-formal-episodes", type=int, default=64)
    parser.add_argument("--required-success-threshold", type=float, default=0.8)
    parser.add_argument("--required-train-curriculum", default="f03")
    parser.add_argument("--required-eval-curriculum", default="f03")
    parser.add_argument("--contract-path", default=DEFAULT_CONTRACT_PATH)
    parser.add_argument(
        "--warm-start-decision",
        choices=("pending", "approved_obstacle_summary", "not_used"),
        default="pending",
        help="Current F02.6 decision state; pending blocks formal claims when warm-start was used.",
    )
    return parser.parse_args(list(argv))


def audit_trial(
    *,
    trial_dir: Path,
    min_formal_episodes: int,
    required_success_threshold: float,
    required_train_curriculum: str,
    required_eval_curriculum: str,
    warm_start_decision: str,
    expected_contract_path: str = DEFAULT_CONTRACT_PATH,
    raw_argv: Sequence[str],
) -> dict[str, Any]:
    manifest_path = trial_dir / "gate3_trial_manifest.json"
    manifest = _read_json(manifest_path)
    train_summary = _read_optional_json(trial_dir / str(manifest.get("train_summary", "train/summary.json")))
    eval_summary = _read_optional_json(trial_dir / str(manifest.get("eval_summary", "eval/gate3_summary.json")))
    blockers: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    _check_artifacts(trial_dir=trial_dir, manifest=manifest, blockers=blockers)
    if manifest.get("status") != "complete":
        blockers.append(_reason("trial_not_complete", f"trial status is {manifest.get('status')!r}"))
    if bool(manifest.get("smoke")):
        blockers.append(_reason("smoke_trial", "runner manifest has smoke=true"))
    if bool(manifest.get("formal_gate_claim")):
        warnings.append(_reason("pre_audit_formal_claim_present", "runner manifest claimed formal status before audit"))

    train_cfg = _config_from(manifest, train_summary, "train_config")
    eval_cfg = _config_from(manifest, eval_summary, "eval_config")
    _check_contract_path(
        manifest=manifest,
        train_cfg=train_cfg,
        eval_summary=eval_summary,
        expected_contract_path=str(expected_contract_path),
        blockers=blockers,
    )
    train_curriculum = str(train_cfg.get("curriculum_preset", "unknown"))
    eval_curriculum = str(eval_cfg.get("curriculum_preset", "unknown"))
    if train_curriculum != str(required_train_curriculum):
        blockers.append(
            _reason(
                "train_curriculum_not_f03",
                f"train curriculum is {train_curriculum!r}, expected {required_train_curriculum!r}",
                observed=train_curriculum,
                expected=str(required_train_curriculum),
            )
        )
    if eval_curriculum != str(required_eval_curriculum):
        blockers.append(
            _reason(
                "eval_curriculum_not_f03",
                f"eval curriculum is {eval_curriculum!r}, expected {required_eval_curriculum!r}",
                observed=eval_curriculum,
                expected=str(required_eval_curriculum),
            )
        )

    episodes = int(_first_present(manifest, eval_summary, key="episodes", default=0))
    eval_min_episodes = int(_first_present(eval_summary, manifest, key="min_episodes", default=episodes))
    threshold = float(_first_present(manifest, eval_summary, key="success_threshold", default=0.0))
    success_rate = float(_first_present(manifest, eval_summary, key="terminal_rs_success_rate", default=0.0))
    if episodes < int(min_formal_episodes) or eval_min_episodes < int(min_formal_episodes):
        blockers.append(
            _reason(
                "insufficient_eval_episodes",
                f"episodes={episodes}, min_episodes={eval_min_episodes}, required={int(min_formal_episodes)}",
                observed={"episodes": episodes, "min_episodes": eval_min_episodes},
                expected={">=": int(min_formal_episodes)},
            )
        )
    if threshold < float(required_success_threshold):
        blockers.append(
            _reason(
                "success_threshold_too_low",
                f"success_threshold={threshold}, required={float(required_success_threshold)}",
                observed=threshold,
                expected={">=": float(required_success_threshold)},
            )
        )

    warm_start_status = str(manifest.get("warm_start_status", "unknown"))
    if warm_start_status.startswith("applied_") and warm_start_decision == "pending":
        blockers.append(
            _reason(
                "warm_start_decision_pending",
                "warm-start was used but F02.6 is still pending",
                observed=warm_start_status,
                expected="approved_obstacle_summary or not_used",
            )
        )
    evaluator_decision = str(manifest.get("gate3_decision", eval_summary.get("decision", "unknown")))
    formal_decision = "not_formal"
    if not blockers:
        formal_decision = "pass" if success_rate >= float(required_success_threshold) else "fail"
    return {
        "schema_version": 1,
        "audit_name": "module2_f03_gate3_formal_audit",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "execution_host": socket.gethostname(),
        "source_head": _source_head(),
        "command": " ".join(["python -m forest_n3p.scripts.audit_rl_rs_gate3_trial", *raw_argv]),
        "trial_dir": str(trial_dir),
        "contract": str(expected_contract_path),
        "formal_decision": formal_decision,
        "formal_claim_allowed": formal_decision in {"pass", "fail"},
        "formal_blockers": blockers,
        "formal_warnings": warnings,
        "evaluator_decision": evaluator_decision,
        "episodes": episodes,
        "min_formal_episodes": int(min_formal_episodes),
        "terminal_rs_success_rate": success_rate,
        "success_threshold": threshold,
        "required_success_threshold": float(required_success_threshold),
        "train_curriculum_preset": train_curriculum,
        "eval_curriculum_preset": eval_curriculum,
        "warm_start_status": warm_start_status,
        "warm_start_decision": warm_start_decision,
        "artifact_manifest": str(manifest_path),
    }


def _check_contract_path(
    *,
    manifest: dict[str, Any],
    train_cfg: dict[str, Any],
    eval_summary: dict[str, Any],
    expected_contract_path: str,
    blockers: list[dict[str, Any]],
) -> None:
    contract_fields = {
        "trial_manifest_contract": manifest.get("contract"),
        "train_config_contract": train_cfg.get("contract"),
        "eval_summary_contract": eval_summary.get("contract"),
    }
    for field_id, observed in contract_fields.items():
        if observed is None and expected_contract_path == DEFAULT_CONTRACT_PATH:
            continue
        if observed != expected_contract_path:
            blockers.append(
                _reason(
                    "contract_path_mismatch",
                    f"{field_id} is {observed!r}, expected {expected_contract_path!r}",
                    observed={field_id: observed},
                    expected=expected_contract_path,
                )
            )


def _check_artifacts(*, trial_dir: Path, manifest: dict[str, Any], blockers: list[dict[str, Any]]) -> None:
    required = (
        "train_model",
        "train_summary",
        "train_manifest",
        "eval_summary",
        "eval_episodes_csv",
    )
    for key in required:
        raw = manifest.get(key)
        if raw is None:
            blockers.append(_reason("missing_artifact_pointer", f"manifest missing {key}", expected=key))
            continue
        path = trial_dir / str(raw)
        if not path.exists():
            blockers.append(_reason("missing_artifact", f"{key} does not exist: {path}", observed=str(path)))


def _config_from(manifest: dict[str, Any], side_summary: dict[str, Any], manifest_key: str) -> dict[str, Any]:
    cfg = manifest.get(manifest_key)
    if isinstance(cfg, dict) and cfg:
        return cfg
    nested = side_summary.get("config")
    return nested if isinstance(nested, dict) else {}


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def _read_optional_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return _read_json(path)


def _first_present(primary: dict[str, Any], secondary: dict[str, Any], *, key: str, default: Any) -> Any:
    if key in primary:
        return primary[key]
    if key in secondary:
        return secondary[key]
    return default


def _reason(code: str, message: str, *, observed: Any | None = None, expected: Any | None = None) -> dict[str, Any]:
    reason = {"code": code, "message": message}
    if observed is not None:
        reason["observed"] = observed
    if expected is not None:
        reason["expected"] = expected
    return reason


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not stop audit.
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
