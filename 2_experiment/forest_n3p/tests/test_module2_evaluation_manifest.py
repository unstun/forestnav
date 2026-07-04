import json
from pathlib import Path

from forest_n3p.scripts.build_module2_evaluation_manifest import (
    Module2EvaluationManifestConfig,
    build_manifest,
    main as build_manifest_main,
)


def test_module2_manifest_freezes_h01_methods_metrics_and_pending_decision_blockers(tmp_path):
    manifest = build_manifest(
        Module2EvaluationManifestConfig(
            output_dir=tmp_path,
            contract_path=_frontmatter(tmp_path, "contract.md", status="approved"),
            cutpoint_supplement_path=_frontmatter(tmp_path, "cutpoints.md", reviewed="true"),
            warm_start_decision="pending",
            bc_checkpoint=None,
            rl_rs_checkpoint=None,
            realmap_query_protocol_path=None,
            queries_per_bucket=100,
            seed_count=5,
        )
    )

    assert manifest["schema_version"] == 1
    assert manifest["manifest_name"] == "module2_v1_evaluation"
    assert manifest["status"] == "blocked_pending_decisions"
    assert manifest["scale"]["queries_per_bucket"] == 100
    assert manifest["scale"]["seed_count"] == 5
    assert manifest["scale"]["bucket_names"] == ["Easy", "Complex", "Extreme"]
    assert manifest["contract"]["path"].endswith("contract.md")
    assert manifest["contract"]["status"] == "approved"

    methods = {entry["method_id"]: entry for entry in manifest["methods"]}
    for method_id in (
        "ha_no_analytic",
        "ha_single_rs",
        "ha_dang_multi_rs",
        "f_n3p_knn",
        "mlp",
        "bc_analytic_operator",
        "ppo_analytic_operator",
        "ppo_rs_funnel",
    ):
        assert method_id in methods

    assert methods["ha_no_analytic"]["status"] == "ready"
    assert methods["ha_dang_multi_rs"]["main_evaluation_method"] == "ha_dang_multi_rs"
    assert methods["bc_analytic_operator"]["main_evaluation_method"] == "bc_analytic_operator"
    assert "missing_module2_bc_checkpoint" in methods["bc_analytic_operator"]["blockers"]
    assert methods["ppo_rs_funnel"]["main_evaluation_method"] == "ha_rl_rs_ppo"
    assert "missing_module2_rl_rs_checkpoint" in methods["ppo_rs_funnel"]["blockers"]
    assert "f02_6_warm_start_decision_pending" in methods["ppo_rs_funnel"]["blockers"]
    assert "missing_main_evaluation_method" in methods["ppo_analytic_operator"]["blockers"]

    metric_ids = {metric["metric_id"] for metric in manifest["metrics"]}
    assert {"total_time_s", "total_expansions", "timeout_failure_rate", "path_inflation_ratio"}.issubset(metric_ids)
    assert {"analytic_success_rate", "terminal_rs_success_rate", "fallback_count", "nn_forward_time_s"}.issubset(metric_ids)

    assert manifest["real_maps"]["manifest"].endswith("2_experiment/forest_n3p/assets/realmaps/manifest.json")
    assert manifest["real_maps"]["usable_map_count"] >= 2
    assert "realmap_query_generation_not_frozen" in manifest["blockers"]
    assert "f02_6_warm_start_decision_pending" in manifest["blockers"]
    assert manifest["run_command"]["formal_main_evaluation"] is None


def test_module2_manifest_cli_writes_json_and_markdown_with_checkpoint_unblocked(tmp_path):
    bc_checkpoint = tmp_path / "bc_model.pt"
    bc_checkpoint.write_bytes(b"not a real model; manifest preflight only checks presence")
    checkpoint = tmp_path / "final_model.zip"
    checkpoint.write_bytes(b"not a real model; manifest preflight only checks presence")
    manifest_path = tmp_path / "module2_manifest.json"
    markdown_path = tmp_path / "module2_manifest.md"

    rc = build_manifest_main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--contract-path",
            str(_frontmatter(tmp_path, "contract.md", status="approved")),
            "--cutpoint-supplement-path",
            str(_frontmatter(tmp_path, "cutpoints.md", reviewed="true")),
            "--warm-start-decision",
            "approved_obstacle_summary",
            "--realmap-query-protocol-path",
            str(_realmap_protocol(tmp_path)),
            "--bc-checkpoint",
            str(bc_checkpoint),
            "--rl-rs-checkpoint",
            str(checkpoint),
            "--queries-per-bucket",
            "100",
            "--seed-count",
            "5",
        ]
    )
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    bc = next(method for method in payload["methods"] if method["method_id"] == "bc_analytic_operator")
    ppo_rs = next(method for method in payload["methods"] if method["method_id"] == "ppo_rs_funnel")

    assert rc == 0
    assert payload["status"] == "blocked_missing_implementation"
    assert bc["status"] == "ready"
    assert bc["main_evaluation_method"] == "bc_analytic_operator"
    assert bc["checkpoint"] == str(bc_checkpoint)
    assert "missing_module2_rl_rs_checkpoint" not in ppo_rs["blockers"]
    assert "f02_6_warm_start_decision_pending" not in ppo_rs["blockers"]
    assert ppo_rs["checkpoint"] == str(checkpoint)
    assert "--methods ha_no_analytic,ha_single_rs,ha_dang_multi_rs,mlp,bc_analytic_operator,ha_rl_rs_ppo" in payload["run_command"]["formal_main_evaluation"]
    assert "--module2-bc-checkpoint" in payload["run_command"]["formal_main_evaluation"]
    assert "--module2-rl-rs-checkpoint" in payload["run_command"]["formal_main_evaluation"]
    assert "# Module2 v1 Evaluation Manifest" in markdown
    assert "blocked_missing_implementation" in markdown


def test_module2_manifest_unblocks_realmap_gap_when_query_protocol_is_frozen(tmp_path):
    checkpoint = tmp_path / "final_model.zip"
    checkpoint.write_bytes(b"not a real model; manifest preflight only checks presence")
    bc_checkpoint = tmp_path / "bc_model.pt"
    bc_checkpoint.write_bytes(b"not a real model; manifest preflight only checks presence")
    protocol = _realmap_protocol(tmp_path)

    manifest = build_manifest(
        Module2EvaluationManifestConfig(
            output_dir=tmp_path,
            contract_path=_frontmatter(tmp_path, "contract.md", status="approved"),
            cutpoint_supplement_path=_frontmatter(tmp_path, "cutpoints.md", reviewed="true"),
            warm_start_decision="approved_obstacle_summary",
            realmap_query_protocol_path=protocol,
            bc_checkpoint=bc_checkpoint,
            rl_rs_checkpoint=checkpoint,
            queries_per_bucket=100,
            seed_count=5,
        )
    )

    assert manifest["realmap_query_protocol"]["status"] == "frozen"
    assert manifest["realmap_query_protocol"]["endpoint_audit_pass"] is True
    assert "realmap_query_generation_not_frozen" not in manifest["blockers"]
    assert "missing_module2_bc_checkpoint" not in manifest["blockers"]
    assert manifest["run_command"]["formal_main_evaluation"] is not None


def _frontmatter(tmp_path: Path, name: str, **fields) -> Path:
    path = tmp_path / name
    body = "---\n" + "".join(f"{key}: {value}\n" for key, value in fields.items()) + "---\n"
    path.write_text(body, encoding="utf-8")
    return path


def _realmap_protocol(tmp_path: Path) -> Path:
    queries = tmp_path / "realmap_queries.csv"
    queries.write_text("query_id,map_id\nq0,dqn_realmap_a\n", encoding="utf-8")
    path = tmp_path / "realmap_protocol.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "protocol_name": "module2_realmap_query_protocol",
                "status": "frozen",
                "query_count": 4,
                "query_count_by_map": {"dqn_realmap_a": 2, "willow_garage_0p10": 2},
                "queries_csv": str(queries),
                "queries_csv_sha256": "abc123",
                "endpoint_audit": {"pass": True, "start_collision_count": 0, "goal_collision_count": 0},
            }
        ),
        encoding="utf-8",
    )
    return path
