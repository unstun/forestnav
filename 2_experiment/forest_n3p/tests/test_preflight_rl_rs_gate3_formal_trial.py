import json
from importlib import import_module
from pathlib import Path


BC_CHECKPOINT = Path("2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt")
V2_DRAFT_CONTRACT = Path(".pipeline/contracts/module2-stronger_obstacle_summary_warm_start-v2.md")


def test_gate3_formal_preflight_writes_ready_no_warm_start_protocol(tmp_path):
    try:
        preflight = import_module("forest_n3p.scripts.preflight_rl_rs_gate3_formal_trial")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing Gate #3 formal preflight module: {exc}") from exc

    output_dir = tmp_path / "gate3_no_warm_trial"
    manifest_path = tmp_path / "gate3_preflight_manifest.json"
    rc = preflight.main(
        [
            "--output-dir",
            str(output_dir),
            "--manifest-out",
            str(manifest_path),
            "--seed",
            "20260704",
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["schema_version"] == 1
    assert manifest["contract"] == ".pipeline/contracts/module2-ppo-funnel-expansion.md"
    assert manifest["protocol"]["contract"] == ".pipeline/contracts/module2-ppo-funnel-expansion.md"
    assert manifest["preflight_status"] == "ready"
    assert manifest["formal_trial_ready"] is True
    assert manifest["formal_blockers"] == []
    assert manifest["warm_start_decision"] == "pending"
    assert manifest["protocol"]["bc_checkpoint"] is None
    assert manifest["protocol"]["train_curriculum_preset"] == "f03"
    assert manifest["protocol"]["eval_curriculum_preset"] == "f03"
    assert manifest["protocol"]["eval_episodes"] == 64
    assert manifest["protocol"]["eval_min_episodes"] == 64
    assert manifest["protocol"]["eval_success_threshold"] == 0.8
    assert "--smoke" not in manifest["runner_command"]
    assert "--train-curriculum-preset f03" in manifest["runner_command"]
    assert "--eval-curriculum-preset f03" in manifest["runner_command"]
    assert "--contract-path .pipeline/contracts/module2-ppo-funnel-expansion.md" in manifest["runner_command"]
    assert f"--output-dir {output_dir}" in manifest["runner_command"]
    assert "--contract-path .pipeline/contracts/module2-ppo-funnel-expansion.md" in manifest["audit_command"]
    assert "--warm-start-decision pending" in manifest["audit_command"]


def test_gate3_formal_preflight_blocks_pending_warm_start_decision(tmp_path):
    try:
        preflight = import_module("forest_n3p.scripts.preflight_rl_rs_gate3_formal_trial")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing Gate #3 formal preflight module: {exc}") from exc

    output_dir = tmp_path / "gate3_warm_trial"
    manifest_path = tmp_path / "gate3_warm_preflight.json"
    rc = preflight.main(
        [
            "--output-dir",
            str(output_dir),
            "--manifest-out",
            str(manifest_path),
            "--bc-checkpoint",
            str(BC_CHECKPOINT),
            "--warm-start-decision",
            "pending",
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    reason_codes = {reason["code"] for reason in manifest["formal_blockers"]}
    assert manifest["preflight_status"] == "blocked"
    assert manifest["formal_trial_ready"] is False
    assert manifest["protocol"]["bc_checkpoint"] == str(BC_CHECKPOINT)
    assert "warm_start_decision_pending" in reason_codes
    assert f"--bc-checkpoint {BC_CHECKPOINT}" in manifest["runner_command"]


def test_gate3_formal_preflight_propagates_v2_contract_but_blocks_draft_status(tmp_path):
    preflight = import_module("forest_n3p.scripts.preflight_rl_rs_gate3_formal_trial")

    output_dir = tmp_path / "gate3_v2_trial"
    manifest_path = tmp_path / "gate3_v2_preflight.json"
    rc = preflight.main(
        [
            "--output-dir",
            str(output_dir),
            "--manifest-out",
            str(manifest_path),
            "--contract-path",
            str(V2_DRAFT_CONTRACT),
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
            "--bc-checkpoint",
            str(BC_CHECKPOINT),
            "--warm-start-decision",
            "approved_obstacle_summary",
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    reason_codes = {reason["code"] for reason in manifest["formal_blockers"]}
    assert manifest["contract"] == str(V2_DRAFT_CONTRACT)
    assert manifest["contract_status"] == "draft"
    assert manifest["protocol"]["contract"] == str(V2_DRAFT_CONTRACT)
    assert manifest["protocol"]["train_total_timesteps"] == 500000
    assert manifest["protocol"]["train_n_envs"] == 4
    assert manifest["protocol"]["train_n_steps"] == 256
    assert manifest["protocol"]["train_batch_size"] == 256
    assert manifest["protocol"]["train_n_epochs"] == 8
    assert manifest["protocol"]["train_learning_rate"] == 0.0001
    assert manifest["protocol"]["train_ent_coef"] == 0.01
    assert manifest["protocol"]["train_checkpoint_freq"] == 25000
    assert manifest["preflight_status"] == "blocked"
    assert manifest["formal_trial_ready"] is False
    assert "contract_not_approved" in reason_codes
    assert f"--contract-path {V2_DRAFT_CONTRACT}" in manifest["runner_command"]
    assert "--train-total-timesteps 500000" in manifest["runner_command"]
    assert "--train-n-envs 4" in manifest["runner_command"]
    assert "--train-n-steps 256" in manifest["runner_command"]
    assert "--train-batch-size 256" in manifest["runner_command"]
    assert "--train-n-epochs 8" in manifest["runner_command"]
    assert "--train-learning-rate 0.0001" in manifest["runner_command"]
    assert "--train-ent-coef 0.01" in manifest["runner_command"]
    assert "--train-checkpoint-freq 25000" in manifest["runner_command"]
    assert f"--contract-path {V2_DRAFT_CONTRACT}" in manifest["audit_command"]
