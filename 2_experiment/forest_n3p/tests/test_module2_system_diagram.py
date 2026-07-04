import json
import xml.etree.ElementTree as ET
from importlib import import_module


def test_system_diagram_artifact_is_drawio_and_code_anchored(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_system_diagram")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing Module2 system diagram builder: {exc}") from exc

    manifest_path = tmp_path / "module2_system_diagram.json"
    markdown_path = tmp_path / "module2_system_diagram.md"
    drawio_path = tmp_path / "module2_system_diagram.drawio"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--drawio-out",
            str(drawio_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    root = ET.fromstring(drawio_path.read_text(encoding="utf-8"))

    assert root.tag == "mxfile"
    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_system_diagram"
    assert manifest["status"] == "code_anchored_drawio"
    assert manifest["formal_claim_allowed"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["remote_training_resource"] == "gpu3070ti-relay"

    node_ids = {node["node_id"] for node in manifest["nodes"]}
    for expected in (
        "hybrid_astar_loop",
        "analytic_trigger",
        "custom_operator_dispatch",
        "rl_rs_funnel_operator",
        "rl_rollout_env",
        "terminal_rs_certificate",
        "accept_shortcut",
        "fallback_primitives",
        "gym_training_env",
        "checkpointed_policy",
        "formal_evaluation_boundary",
    ):
        assert expected in node_ids

    edges = {(edge["source"], edge["target"], edge["semantic"]) for edge in manifest["edges"]}
    assert ("terminal_rs_certificate", "accept_shortcut", "certified_success") in edges
    assert ("terminal_rs_certificate", "fallback_primitives", "return_none_fallback") in edges
    assert ("gym_training_env", "checkpointed_policy", "remote_training_export") in edges

    for node in manifest["nodes"]:
        assert node["code_anchors"], f"{node['node_id']} lacks anchors"
        for anchor in node["code_anchors"]:
            assert anchor["path"].startswith("2_experiment/forest_n3p/")
            assert isinstance(anchor["line"], int) and anchor["line"] > 0
            assert anchor["symbol"]

    assert "F02.6" in "\n".join(manifest["claim_boundaries"])
    assert "gpu3070ti-relay" in "\n".join(manifest["claim_boundaries"])
    assert "PPO checkpoint" in "\n".join(manifest["claim_boundaries"])
    assert "# Module2 System Diagram" in markdown
    assert "Figure: RL-RS analytic expansion system" in markdown
    assert "2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:" in markdown

    drawio_text = drawio_path.read_text(encoding="utf-8")
    for expected in (
        "Hybrid A* search loop",
        "Analytic expansion trigger",
        "RL-RS funnel operator",
        "Terminal RS certificate",
        "Fallback primitive expansion",
        "gpu3070ti-relay",
    ):
        assert expected in drawio_text
