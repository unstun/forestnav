import csv
import json
import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

from forest_n3p.scripts.eval_rl_rs_gate3 import main as eval_gate3_main
from forest_n3p.scripts.train_rl_rs_ppo import main as train_rl_rs_ppo_main


def test_eval_rl_rs_gate3_smoke_loads_model_runs_deterministic_episodes_and_writes_decision(tmp_path):
    train_dir = tmp_path / "train"
    eval_dir = tmp_path / "eval"
    train_rc = train_rl_rs_ppo_main(
        [
            "--allow-duplicate-openmp",
            "--smoke",
            "--output-dir",
            str(train_dir),
            "--seed",
            "20260704",
        ]
    )
    assert train_rc == 0

    eval_rc = eval_gate3_main(
        [
            "--allow-duplicate-openmp",
            "--model",
            str(train_dir / "final_model.zip"),
            "--output-dir",
            str(eval_dir),
            "--curriculum-preset",
            "open",
            "--episodes",
            "4",
            "--success-threshold",
            "0.8",
            "--min-episodes",
            "4",
            "--seed",
            "20260704",
            "--obs-patch-size-m",
            "0.4",
            "--obs-patch-cells",
            "5",
            "--max-steps",
            "4",
        ]
    )

    assert eval_rc == 0
    summary = json.loads((eval_dir / "gate3_summary.json").read_text(encoding="utf-8"))
    assert summary["schema_version"] == 1
    assert summary["gate_name"] == "module2_f03_gate3"
    assert summary["decision"] == "pass"
    assert summary["episodes"] == 4
    assert summary["terminal_rs_success_rate"] >= 0.8
    assert summary["model"] == str(train_dir / "final_model.zip")

    rows = list(csv.DictReader((eval_dir / "gate3_eval_episodes.csv").open(newline="", encoding="utf-8")))
    assert len(rows) == 4
    assert rows[0]["terminal_rs_success"] == "True"
