import json
from importlib import import_module
from pathlib import Path


SMOKE_TRIAL = Path("0_trials/module2_ppo_smoke/f03_gate3_trial_runner_smoke")


def test_gate3_audit_marks_open_connector_smoke_as_not_formal(tmp_path):
    try:
        audit = import_module("forest_n3p.scripts.audit_rl_rs_gate3_trial")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing Gate #3 formal audit module: {exc}") from exc

    output_path = tmp_path / "gate3_formal_audit.json"
    rc = audit.main(
        [
            "--trial-dir",
            str(SMOKE_TRIAL),
            "--output",
            str(output_path),
        ]
    )

    assert rc == 0
    result = json.loads(output_path.read_text(encoding="utf-8"))
    reason_codes = {reason["code"] for reason in result["formal_blockers"]}
    assert result["schema_version"] == 1
    assert result["formal_decision"] == "not_formal"
    assert result["evaluator_decision"] == "pass"
    assert result["formal_claim_allowed"] is False
    assert result["trial_dir"] == str(SMOKE_TRIAL)
    assert "smoke_trial" in reason_codes
    assert "insufficient_eval_episodes" in reason_codes
    assert "train_curriculum_not_f03" in reason_codes
    assert "eval_curriculum_not_f03" in reason_codes
    assert "warm_start_decision_pending" in reason_codes


def test_gate3_audit_allows_formal_pass_only_when_protocol_evidence_is_sufficient(tmp_path):
    try:
        audit = import_module("forest_n3p.scripts.audit_rl_rs_gate3_trial")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing Gate #3 formal audit module: {exc}") from exc

    trial_dir = tmp_path / "formal_trial"
    _write_formal_trial_fixture(trial_dir, success_rate=0.8125)
    output_path = trial_dir / "gate3_formal_audit.json"

    rc = audit.main(["--trial-dir", str(trial_dir), "--output", str(output_path)])

    assert rc == 0
    result = json.loads(output_path.read_text(encoding="utf-8"))
    assert result["formal_decision"] == "pass"
    assert result["formal_claim_allowed"] is True
    assert result["formal_blockers"] == []
    assert result["evaluator_decision"] == "pass"
    assert result["episodes"] == 64
    assert result["terminal_rs_success_rate"] == 0.8125
    assert result["success_threshold"] == 0.8


def _write_formal_trial_fixture(trial_dir: Path, *, success_rate: float) -> None:
    (trial_dir / "train").mkdir(parents=True)
    (trial_dir / "eval").mkdir(parents=True)
    (trial_dir / "train" / "final_model.zip").write_bytes(b"fake-model")
    (trial_dir / "train" / "summary.json").write_text(
        json.dumps(
            {
                "status": "complete",
                "warm_start_status": "not_applied_f02_6_pending",
                "config": {
                    "smoke": False,
                    "curriculum_preset": "f03",
                    "total_timesteps": 100000,
                },
            }
        ),
        encoding="utf-8",
    )
    (trial_dir / "train" / "training_manifest.json").write_text(
        json.dumps({"schema_version": 1, "config": {"smoke": False}}),
        encoding="utf-8",
    )
    (trial_dir / "eval" / "gate3_eval_episodes.csv").write_text("episode_index,terminal_rs_success\n0,True\n", encoding="utf-8")
    (trial_dir / "eval" / "gate3_summary.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "gate_name": "module2_f03_gate3",
                "contract": ".pipeline/contracts/module2-ppo-funnel-expansion.md",
                "decision": "pass",
                "success_threshold": 0.8,
                "min_episodes": 64,
                "episodes": 64,
                "terminal_rs_success": int(round(success_rate * 64)),
                "terminal_rs_success_rate": success_rate,
                "config": {
                    "curriculum_preset": "f03",
                    "episodes": 64,
                },
            }
        ),
        encoding="utf-8",
    )
    (trial_dir / "gate3_trial_manifest.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "trial_name": "module2_f03_gate3_train_eval",
                "status": "complete",
                "smoke": False,
                "formal_gate_claim": False,
                "warm_start_status": "not_applied_f02_6_pending",
                "bc_checkpoint": None,
                "train_output_dir": "train",
                "eval_output_dir": "eval",
                "train_model": "train/final_model.zip",
                "train_summary": "train/summary.json",
                "train_manifest": "train/training_manifest.json",
                "eval_summary": "eval/gate3_summary.json",
                "eval_episodes_csv": "eval/gate3_eval_episodes.csv",
                "gate3_decision": "pass",
                "terminal_rs_success_rate": success_rate,
                "terminal_rs_success": int(round(success_rate * 64)),
                "episodes": 64,
                "success_threshold": 0.8,
                "train_config": {
                    "smoke": False,
                    "curriculum_preset": "f03",
                    "total_timesteps": 100000,
                },
                "eval_config": {
                    "curriculum_preset": "f03",
                    "episodes": 64,
                },
            }
        ),
        encoding="utf-8",
    )
