import json
from importlib import import_module


def test_method_algorithm_artifact_is_code_anchored(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_method_algorithms")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing Module2 method algorithm builder: {exc}") from exc

    manifest_path = tmp_path / "module2_method_algorithms.json"
    markdown_path = tmp_path / "module2_method_algorithms.md"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_method_algorithms"
    assert manifest["status"] == "code_anchored"
    assert manifest["formal_claim_allowed"] is False
    assert manifest["local_training_allowed"] is False

    algorithms = {item["algorithm_id"]: item for item in manifest["algorithms"]}
    assert set(algorithms) == {
        "rl_rs_funnel_analytic_expansion",
        "analytic_expansion_training_environment",
    }

    algorithm_1 = algorithms["rl_rs_funnel_analytic_expansion"]
    algorithm_1_text = json.dumps(algorithm_1, ensure_ascii=False)
    for expected in (
        "HybridAStarPlanner._try_custom_analytic_expansion",
        "RlRsFunnelOperator.try_connect",
        "AnalyticExpansionEnv.reset",
        "AnalyticExpansionEnv.step",
        "check_terminal_rs_connectable",
        "terminal_rs_used",
        "fallback_to_builtin_search_on_none",
    ):
        assert expected in algorithm_1_text

    algorithm_2 = algorithms["analytic_expansion_training_environment"]
    algorithm_2_text = json.dumps(algorithm_2, ensure_ascii=False)
    for expected in (
        "GymAnalyticExpansionEnv.reset",
        "GymAnalyticExpansionEnv.step",
        "ObservationConfig",
        "build_observation",
        "compute_decomposed_reward",
        "local_training_disallowed",
    ):
        assert expected in algorithm_2_text

    for algorithm in manifest["algorithms"]:
        for step in algorithm["steps"]:
            assert step["code_anchors"], f"{algorithm['algorithm_id']} {step['step_id']} lacks anchors"
            for anchor in step["code_anchors"]:
                assert anchor["path"].startswith("2_experiment/forest_n3p/")
                assert isinstance(anchor["line"], int) and anchor["line"] > 0
                assert anchor["symbol"]

    assert "F02.6" in "\n".join(manifest["claim_boundaries"])
    assert "# Module2 Method Algorithms" in markdown
    assert "Algorithm 1" in markdown
    assert "Algorithm 2" in markdown
    assert "2_experiment/forest_n3p/rl_rs/operator.py:" in markdown
