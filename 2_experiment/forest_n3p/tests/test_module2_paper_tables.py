import csv
import json
from importlib import import_module


def test_paper_table_builder_blocks_formal_claims_without_formal_h02_data(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_paper_tables")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing Module2 paper table builder: {exc}") from exc

    eval_dir = tmp_path / "eval"
    eval_dir.mkdir()
    _write_records(eval_dir / "records.csv")
    (eval_dir / "summary.json").write_text(
        json.dumps(
            {
                "record_count": 4,
                "summary_by_method_bucket": [
                    {
                        "method": "ha_dang_multi_rs",
                        "difficulty_bucket": "Complex",
                        "count": 2,
                        "success_count": 1,
                        "success_rate": 0.5,
                        "timeout_failure_count": 1,
                        "timeout_failure_rate": 0.5,
                        "median_time_s": 5.0,
                        "p95_time_s": 7.0,
                        "median_expansions": 100.0,
                        "p95_expansions": 120.0,
                        "median_path_inflation_ratio": 1.1,
                        "median_min_clearance_m": 0.2,
                    }
                ],
                "paired_time_tests": [],
                "paired_expansion_tests": [],
                "success_rate_bootstrap_ci": [],
                "failure_rate_bootstrap_ci": [],
                "timeout_failure_rate_bootstrap_ci": [],
            }
        ),
        encoding="utf-8",
    )
    verdict_path = tmp_path / "verdict.json"
    verdict_path.write_text(
        json.dumps(
            {
                "status": "candidate_or_smoke",
                "formal_acceptance": False,
                "record_count": 4,
                "query_count": 2,
                "method_count": 2,
            }
        ),
        encoding="utf-8",
    )
    h01_path = tmp_path / "h01.json"
    h01_path.write_text(
        json.dumps(
            {
                "status": "blocked_pending_decisions",
                "blockers": ["f02_6_decision_packet_pending", "missing_module2_rl_rs_checkpoint"],
                "methods": [
                    {"method_id": "ha_dang_multi_rs", "status": "ready"},
                    {"method_id": "ppo_rs_funnel", "status": "blocked", "blockers": ["missing_module2_rl_rs_checkpoint"]},
                ],
            }
        ),
        encoding="utf-8",
    )
    metric_protocol_path = tmp_path / "metric_protocol.json"
    metric_protocol_path.write_text(
        json.dumps(
            {
                "status": "frozen",
                "metrics": [
                    {"metric_id": "total_expansions"},
                    {"metric_id": "total_time_s"},
                    {"metric_id": "timeout_failure_rate"},
                    {"metric_id": "path_quality"},
                ],
            }
        ),
        encoding="utf-8",
    )
    manifest_path = tmp_path / "module2_paper_tables.json"
    markdown_path = tmp_path / "module2_paper_tables.md"

    rc = builder.main(
        [
            "--evaluation-dir",
            str(eval_dir),
            "--verdict",
            str(verdict_path),
            "--h01-manifest",
            str(h01_path),
            "--metric-protocol",
            str(metric_protocol_path),
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
    assert manifest["artifact_name"] == "module2_paper_tables"
    assert manifest["status"] == "blocked_no_formal_h02_data"
    assert manifest["formal_claim_allowed"] is False
    assert manifest["local_training_allowed"] is False
    assert "h02_verdict_not_formal" in manifest["blockers"]
    assert "h01_manifest_not_ready" in manifest["blockers"]
    assert "missing_module2_rl_rs_checkpoint" in manifest["blockers"]

    assert manifest["tables"]["main_table"]["status"] == "preview_not_formal"
    main_rows = manifest["tables"]["main_table"]["rows"]
    assert {row["method"] for row in main_rows} == {"ha_dang_multi_rs", "bc_analytic_operator"}
    assert {"method", "success_rate", "timeout_failure_rate", "time_p50_s", "time_p95_s", "expansions_p50", "expansions_p95", "path_inflation_p50", "clearance_p50_m"}.issubset(
        set(manifest["tables"]["main_table"]["columns"])
    )
    assert manifest["tables"]["ablation_table"]["status"] == "blocked_missing_formal_data"
    assert manifest["tables"]["failure_analysis_table"]["status"] == "preview_not_formal"
    assert manifest["code_anchors"]

    assert "# Module2 Paper Tables Protocol" in markdown
    assert "not formal" in markdown
    assert "I02.1" in markdown
    assert "missing_module2_rl_rs_checkpoint" in markdown


def _write_records(path):
    rows = [
        {
            "query_id": "q1",
            "method": "ha_dang_multi_rs",
            "difficulty_bucket": "Complex",
            "success": "True",
            "feasible": "True",
            "total_time_s": "4.0",
            "total_expansions": "90",
            "path_inflation_ratio": "1.1",
            "min_clearance_m": "0.2",
            "failure_reason": "",
        },
        {
            "query_id": "q2",
            "method": "ha_dang_multi_rs",
            "difficulty_bucket": "Complex",
            "success": "False",
            "feasible": "False",
            "total_time_s": "7.0",
            "total_expansions": "120",
            "path_inflation_ratio": "",
            "min_clearance_m": "0.0",
            "failure_reason": "timeout",
        },
        {
            "query_id": "q1",
            "method": "bc_analytic_operator",
            "difficulty_bucket": "Complex",
            "success": "True",
            "feasible": "True",
            "total_time_s": "3.0",
            "total_expansions": "80",
            "path_inflation_ratio": "1.05",
            "min_clearance_m": "0.25",
            "failure_reason": "",
        },
        {
            "query_id": "q2",
            "method": "bc_analytic_operator",
            "difficulty_bucket": "Complex",
            "success": "False",
            "feasible": "False",
            "total_time_s": "6.0",
            "total_expansions": "110",
            "path_inflation_ratio": "",
            "min_clearance_m": "0.0",
            "failure_reason": "collision",
        },
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
