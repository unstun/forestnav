import json
import os
from importlib import import_module

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")


def test_run_rl_rs_gate3_trial_smoke_trains_evaluates_and_writes_manifest(tmp_path):
    try:
        runner = import_module("forest_n3p.scripts.run_rl_rs_gate3_trial")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing Gate #3 trial runner module: {exc}") from exc

    rc = runner.main(
        [
            "--allow-duplicate-openmp",
            "--smoke",
            "--output-dir",
            str(tmp_path),
            "--seed",
            "20260704",
        ]
    )

    assert rc == 0
    assert (tmp_path / "train" / "final_model.zip").exists()
    assert (tmp_path / "eval" / "gate3_summary.json").exists()
    assert (tmp_path / "gate3_trial_manifest.json").exists()

    manifest = json.loads((tmp_path / "gate3_trial_manifest.json").read_text(encoding="utf-8"))
    assert manifest["schema_version"] == 1
    assert manifest["status"] == "complete"
    assert manifest["smoke"] is True
    assert manifest["formal_gate_claim"] is False
    assert manifest["contract"] == "0_trials/custom_contract.md"
    assert manifest["warm_start_status"] == "not_applied_f02_6_pending"
    assert manifest["train_output_dir"] == "train"
    assert manifest["eval_output_dir"] == "eval"
    assert manifest["train_model"] == "train/final_model.zip"
    assert manifest["eval_summary"] == "eval/gate3_summary.json"
    assert manifest["gate3_decision"] == "pass"
    assert manifest["terminal_rs_success_rate"] >= 0.8
    assert manifest["train_config"]["contract"] == "0_trials/custom_contract.md"
    assert manifest["eval_config"]["contract"] == "0_trials/custom_contract.md"
