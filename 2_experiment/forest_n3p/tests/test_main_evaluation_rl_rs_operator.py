import json
from pathlib import Path

import numpy as np

from forest_n3p.main_evaluation import (
    MainEvaluationConfig,
    _run_hybrid_a_operator,
    preflight_main_evaluation,
    validation_main_evaluation_profiles,
)
from forest_n3p.scripts.run_main_evaluation import main as run_main_evaluation_main
from forest_n3p.third_party.pathplan import AckermannState, GridMap, TwoCircleFootprint
from forest_n3p.third_party.pathplan.hybrid_a_star.operators import AnalyticExpansionResult
from forest_n3p.third_party.pathplan.primitives import MotionPrimitive


class DirectCheckpointStubOperator:
    name = "rl_rs_funnel_ppo"
    checkpoint_path = "stub_model.zip"
    checkpoint_sha256 = "stub_sha256"
    last_telemetry = None

    def __init__(self):
        self.calls = []

    def try_connect(self, state, goal, context):
        self.calls.append((state, goal, context))
        return AnalyticExpansionResult(
            states=[goal],
            actions=[MotionPrimitive(steering=0.0, direction=1, step=abs(goal.x - state.x))],
            telemetry=None,
            terminal_rs_used=True,
            operator=self.name,
        )


def test_preflight_requires_checkpoint_for_rl_rs_ppo_method(tmp_path):
    cfg = _config(tmp_path, checkpoint=None)

    report = preflight_main_evaluation(cfg)

    assert report.ok_to_run is False
    assert any("module2_rl_rs_checkpoint is required" in issue for issue in report.blocking_issues)


def test_preflight_rejects_missing_rl_rs_ppo_checkpoint_path(tmp_path):
    missing = tmp_path / "missing_model.zip"
    cfg = _config(tmp_path, checkpoint=missing)

    report = preflight_main_evaluation(cfg)

    assert report.ok_to_run is False
    assert any("RL-RS checkpoint does not exist" in issue for issue in report.blocking_issues)


def test_preflight_requires_checkpoint_for_bc_analytic_operator(tmp_path):
    cfg = _config(tmp_path, methods=("bc_analytic_operator",), bc_checkpoint=None)

    report = preflight_main_evaluation(cfg)

    assert report.ok_to_run is False
    assert any("module2_bc_checkpoint is required" in issue for issue in report.blocking_issues)


def test_preflight_rejects_missing_bc_analytic_checkpoint_path(tmp_path):
    missing = tmp_path / "missing_bc_model.pt"
    cfg = _config(tmp_path, methods=("bc_analytic_operator",), bc_checkpoint=missing)

    report = preflight_main_evaluation(cfg)

    assert report.ok_to_run is False
    assert any("BC checkpoint does not exist" in issue for issue in report.blocking_issues)


def test_run_main_evaluation_cli_accepts_rl_rs_checkpoint_for_preflight(tmp_path, capsys):
    checkpoint = tmp_path / "model.zip"
    checkpoint.write_bytes(b"stub checkpoint")

    rc = run_main_evaluation_main(
        [
            "--output-dir",
            str(tmp_path / "out"),
            "--preflight-only",
            "--methods",
            "ha_rl_rs_ppo",
            "--module2-rl-rs-checkpoint",
            str(checkpoint),
            "--queries-per-bucket",
            "1",
            "--seed-count",
            "1",
            "--density-profile-buckets",
            "validation_t06",
            "--contract-path",
            str(_frontmatter(tmp_path, "contract.md", status="approved")),
            "--cutpoint-supplement-path",
            str(_frontmatter(tmp_path, "cutpoints.md", reviewed="true")),
            "--allow-unresolved-human-review",
            "--no-enforce-t14-scale",
        ]
    )
    payload = json.loads(capsys.readouterr().out)

    assert rc == 0
    assert payload["ok_to_run"] is True
    assert payload["available_methods"] == ["ha_rl_rs_ppo"]


def test_run_main_evaluation_cli_accepts_bc_checkpoint_for_preflight(tmp_path, capsys):
    checkpoint = tmp_path / "bc_model.pt"
    checkpoint.write_bytes(b"stub checkpoint")

    rc = run_main_evaluation_main(
        [
            "--output-dir",
            str(tmp_path / "out"),
            "--preflight-only",
            "--methods",
            "bc_analytic_operator",
            "--module2-bc-checkpoint",
            str(checkpoint),
            "--queries-per-bucket",
            "1",
            "--seed-count",
            "1",
            "--density-profile-buckets",
            "validation_t06",
            "--contract-path",
            str(_frontmatter(tmp_path, "contract.md", status="approved")),
            "--cutpoint-supplement-path",
            str(_frontmatter(tmp_path, "cutpoints.md", reviewed="true")),
            "--allow-unresolved-human-review",
            "--no-enforce-t14-scale",
        ]
    )
    payload = json.loads(capsys.readouterr().out)

    assert rc == 0
    assert payload["ok_to_run"] is True
    assert payload["available_methods"] == ["bc_analytic_operator"]


def test_hybrid_a_rl_rs_ppo_method_uses_checkpoint_backed_operator(tmp_path, monkeypatch):
    checkpoint = tmp_path / "model.zip"
    checkpoint.write_bytes(b"stub checkpoint")
    loaded = {}
    stub_operator = DirectCheckpointStubOperator()

    def fake_loader(path, **kwargs):
        loaded["path"] = Path(path)
        loaded["kwargs"] = dict(kwargs)
        return stub_operator

    monkeypatch.setattr("forest_n3p.main_evaluation.load_rl_rs_funnel_operator_from_checkpoint", fake_loader)
    cfg = _config(tmp_path, checkpoint=checkpoint)
    grid_map = GridMap(np.zeros((30, 30), dtype=np.uint8), resolution=0.1, origin=(0.0, 0.0))
    footprint = TwoCircleFootprint.from_box(length=0.4, width=0.2)

    run = _run_hybrid_a_operator(
        "ha_rl_rs_ppo",
        _query(),
        grid_map,
        footprint,
        cfg,
        reference_path_length_m=None,
    )

    assert run.success is True
    assert loaded["path"] == checkpoint
    assert loaded["kwargs"]["device"] == "cpu"
    assert stub_operator.calls
    assert run.metadata["analytic_operator"] == "rl_rs_funnel_ppo"
    assert run.metadata["rl_rs_checkpoint"] == str(checkpoint)
    assert run.metadata["rl_rs_checkpoint_sha256"] == "stub_sha256"


def test_hybrid_a_bc_analytic_method_uses_checkpoint_backed_operator(tmp_path, monkeypatch):
    checkpoint = tmp_path / "bc_model.pt"
    checkpoint.write_bytes(b"stub checkpoint")
    loaded = {}
    stub_operator = DirectCheckpointStubOperator()
    stub_operator.name = "rl_rs_funnel_bc"
    stub_operator.checkpoint_path = str(checkpoint)
    stub_operator.checkpoint_sha256 = "bc_stub_sha256"

    def fake_loader(path, **kwargs):
        loaded["path"] = Path(path)
        loaded["kwargs"] = dict(kwargs)
        return stub_operator

    monkeypatch.setattr("forest_n3p.main_evaluation.load_bc_funnel_operator_from_checkpoint", fake_loader)
    cfg = _config(tmp_path, methods=("bc_analytic_operator",), bc_checkpoint=checkpoint)
    grid_map = GridMap(np.zeros((30, 30), dtype=np.uint8), resolution=0.1, origin=(0.0, 0.0))
    footprint = TwoCircleFootprint.from_box(length=0.4, width=0.2)

    run = _run_hybrid_a_operator(
        "bc_analytic_operator",
        _query(),
        grid_map,
        footprint,
        cfg,
        reference_path_length_m=None,
    )

    assert run.success is True
    assert loaded["path"] == checkpoint
    assert loaded["kwargs"]["device"] == "cpu"
    assert stub_operator.calls
    assert run.metadata["analytic_operator"] == "rl_rs_funnel_bc"
    assert run.metadata["bc_checkpoint"] == str(checkpoint)
    assert run.metadata["bc_checkpoint_sha256"] == "bc_stub_sha256"


def _config(
    tmp_path: Path,
    *,
    checkpoint: Path | None = None,
    bc_checkpoint: Path | None = None,
    methods: tuple[str, ...] = ("ha_rl_rs_ppo",),
) -> MainEvaluationConfig:
    return MainEvaluationConfig(
        methods=methods,
        profiles=validation_main_evaluation_profiles(),
        queries_per_bucket=1,
        seed_count=1,
        enforce_t14_scale=False,
        allow_unresolved_human_review=True,
        contract_path=_frontmatter(tmp_path, "contract.md", status="approved"),
        cutpoint_supplement_path=_frontmatter(tmp_path, "cutpoints.md", reviewed="true"),
        module2_rl_rs_checkpoint=checkpoint,
        module2_bc_checkpoint=bc_checkpoint,
        module2_rl_rs_device="cpu",
        module2_bc_device="cpu",
    )


def _frontmatter(tmp_path: Path, name: str, **fields) -> Path:
    path = tmp_path / name
    body = "---\n" + "".join(f"{key}: {value}\n" for key, value in fields.items()) + "---\n"
    path.write_text(body, encoding="utf-8")
    return path


def _query():
    from forest_n3p.main_evaluation import EvaluationQuery

    return EvaluationQuery(
        query_id="q0",
        difficulty_bucket="Easy",
        profile_name="easy_d00",
        map_seed=1,
        query_seed=2,
        seed_index=0,
        map_index=0,
        query_index=0,
        distance_bin_key="8:12",
        start=AckermannState(1.0, 1.0, 0.0).as_tuple(),
        goal=AckermannState(1.4, 1.0, 0.0).as_tuple(),
    )
