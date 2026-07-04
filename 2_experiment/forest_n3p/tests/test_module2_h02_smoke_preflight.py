import json
from importlib import import_module


def test_h02_smoke_preflight_blocks_full_smoke_but_builds_available_subset_command(tmp_path):
    try:
        preflight = import_module("forest_n3p.scripts.build_module2_h02_smoke_preflight")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing H02.1 smoke preflight builder: {exc}") from exc

    h01_manifest = tmp_path / "module2_v1_evaluation_manifest.json"
    bc_checkpoint = tmp_path / "bc_model.pt"
    bc_checkpoint.write_bytes(b"stub")
    h01_manifest.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "manifest_name": "module2_v1_evaluation",
                "status": "blocked_pending_decisions",
                "methods": [
                    {"method_id": "ha_no_analytic", "main_evaluation_method": "ha_no_analytic", "status": "ready", "blockers": []},
                    {"method_id": "ha_single_rs", "main_evaluation_method": "ha_single_rs", "status": "ready", "blockers": []},
                    {"method_id": "ha_dang_multi_rs", "main_evaluation_method": "ha_dang_multi_rs", "status": "ready", "blockers": []},
                    {"method_id": "mlp", "main_evaluation_method": "mlp", "status": "ready", "blockers": []},
                    {
                        "method_id": "bc_analytic_operator",
                        "main_evaluation_method": "bc_analytic_operator",
                        "status": "ready",
                        "blockers": [],
                        "checkpoint": str(bc_checkpoint),
                    },
                    {
                        "method_id": "ppo_analytic_operator",
                        "main_evaluation_method": "ppo_analytic_operator",
                        "status": "blocked",
                        "blockers": ["missing_module2_rl_rs_checkpoint", "f02_6_decision_packet_pending"],
                    },
                    {
                        "method_id": "ppo_rs_funnel",
                        "main_evaluation_method": "ha_rl_rs_ppo",
                        "status": "blocked",
                        "blockers": ["missing_module2_rl_rs_checkpoint", "f02_6_decision_packet_pending"],
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    manifest_path = tmp_path / "h02_smoke_preflight.json"
    markdown_path = tmp_path / "h02_smoke_preflight.md"

    rc = preflight.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--h01-manifest",
            str(h01_manifest),
            "--bc-checkpoint",
            str(bc_checkpoint),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert manifest["schema_version"] == 1
    assert manifest["preflight_name"] == "module2_h02_local_smoke_preflight"
    assert manifest["status"] == "blocked_full_smoke_missing_required_methods"
    assert manifest["formal_claim_allowed"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["full_method_smoke_ready"] is False
    assert {item["method_id"] for item in manifest["blocked_methods"]} == {"ppo_analytic_operator", "ppo_rs_funnel"}
    assert manifest["available_subset"]["methods"] == [
        "ha_no_analytic",
        "ha_single_rs",
        "ha_dang_multi_rs",
        "mlp",
        "bc_analytic_operator",
    ]
    command = manifest["available_subset"]["run_command"]
    assert "--methods ha_no_analytic,ha_single_rs,ha_dang_multi_rs,mlp,bc_analytic_operator" in command
    assert "--module2-bc-checkpoint" in command
    assert "--module2-rl-rs-checkpoint" not in command
    assert "blocked_full_smoke_missing_required_methods" in markdown
