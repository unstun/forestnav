import csv
import hashlib
import json

from forest_n3p.scripts.build_module2_realmap_query_protocol import (
    Module2RealmapQueryProtocolConfig,
    build_realmap_query_protocol,
    main as realmap_protocol_main,
)


def test_realmap_query_protocol_freezes_canonical_and_sampled_queries(tmp_path):
    manifest, rows = build_realmap_query_protocol(
        Module2RealmapQueryProtocolConfig(
            output_dir=tmp_path,
            queries_per_map=3,
            distance_bins="4:8",
        )
    )
    manifest_again, rows_again = build_realmap_query_protocol(
        Module2RealmapQueryProtocolConfig(
            output_dir=tmp_path,
            queries_per_map=3,
            distance_bins="4:8",
        )
    )

    assert manifest["schema_version"] == 1
    assert manifest["status"] == "frozen"
    assert manifest["realmap_manifest"].endswith("2_experiment/forest_n3p/assets/realmaps/manifest.json")
    assert manifest["query_count"] == 6
    assert manifest["query_count_by_map"] == {"dqn_realmap_a": 3, "willow_garage_0p10": 3}
    assert manifest["config"]["queries_per_map"] == 3
    assert manifest["config"]["distance_bins"] == "4:8"
    assert manifest["map_count"] == 2
    assert [row["query_id"] for row in rows] == [row["query_id"] for row in rows_again]
    assert [row["start"] for row in rows] == [row["start"] for row in rows_again]
    assert manifest["query_rows_sha256"] == manifest_again["query_rows_sha256"]

    by_map = {}
    for row in rows:
        by_map.setdefault(row["map_id"], []).append(row)
        assert row["split"] == "realmap"
        assert row["difficulty_bucket"] == "RealMap"
        assert row["map_grid_sha256"]
        assert row["start_collision"] is False
        assert row["goal_collision"] is False
        assert row["euclidean_distance_m"] > 0.0

    for map_rows in by_map.values():
        assert map_rows[0]["query_index"] == 0
        assert map_rows[0]["distance_bin_key"] == "manifest_canonical"
        assert all(row["distance_bin_key"] == "d04_08" for row in map_rows[1:])


def test_realmap_query_protocol_cli_writes_json_csv_and_markdown(tmp_path):
    manifest_path = tmp_path / "realmap_protocol.json"
    csv_path = tmp_path / "realmap_queries.csv"
    markdown_path = tmp_path / "realmap_protocol.md"

    rc = realmap_protocol_main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--queries-out",
            str(csv_path),
            "--markdown-out",
            str(markdown_path),
            "--queries-per-map",
            "2",
            "--distance-bins",
            "4:8",
        ]
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows = list(csv.DictReader(csv_path.open(newline="", encoding="utf-8")))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert rc == 0
    assert manifest["status"] == "frozen"
    assert manifest["query_count"] == 4
    assert manifest["queries_csv"] == str(csv_path)
    assert manifest["queries_csv_sha256"] == _sha256(csv_path)
    assert len(rows) == 4
    assert rows[0]["distance_bin_key"] == "manifest_canonical"
    assert rows[0]["start_collision"] == "False"
    assert rows[0]["goal_collision"] == "False"
    assert "# Module2 RealMap Query Protocol" in markdown
    assert "status: frozen" in markdown


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()
