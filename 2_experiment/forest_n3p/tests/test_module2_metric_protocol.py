import json
from importlib import import_module


def test_module2_metric_protocol_freezes_contract_and_serialized_fields(tmp_path):
    try:
        protocol = import_module("forest_n3p.scripts.build_module2_metric_protocol")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing H01.2 metric protocol builder: {exc}") from exc

    manifest_path = tmp_path / "module2_metric_protocol.json"
    markdown_path = tmp_path / "module2_metric_protocol.md"
    rc = protocol.main(
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
    metrics = {metric["metric_id"]: metric for metric in manifest["metrics"]}

    assert manifest["schema_version"] == 1
    assert manifest["protocol_name"] == "module2_h01_metric_protocol"
    assert manifest["status"] == "frozen"
    assert set(metrics) >= {"total_expansions", "total_time_s", "timeout_failure_rate", "path_quality"}
    assert metrics["total_time_s"]["record_field"] == "records.csv.total_time_s"
    assert metrics["total_time_s"]["statistical_test"]["name"] == "paired_wilcoxon_signed_rank"
    assert metrics["total_time_s"]["statistical_test"]["p_threshold"] == 0.05
    assert metrics["total_expansions"]["summary_fields"] == [
        "summary_by_method_bucket.median_expansions",
        "summary_by_method_bucket.p95_expansions",
    ]
    assert metrics["timeout_failure_rate"]["record_derivation"]["source_field"] == "records.csv.failure_reason"
    assert metrics["timeout_failure_rate"]["summary_fields"] == [
        "summary_by_method_bucket.timeout_failure_count",
        "summary_by_method_bucket.timeout_failure_rate",
    ]
    assert {"path_inflation_ratio", "mean_abs_curvature", "min_clearance_m"}.issubset(
        {item["record_field"] for item in metrics["path_quality"]["submetrics"]}
    )
    assert "timeout_failure_rate" in manifest["serialized_outputs"]["summary_by_method_bucket_columns"]
    assert "failure_reason" in manifest["serialized_outputs"]["records_csv_columns"]
    assert not manifest["blockers"]
    assert "# Module2 H01.2 Metric Protocol" in markdown
    assert "timeout_failure_rate" in markdown
