import json
from importlib import import_module

import pyarrow as pa
import pyarrow.parquet as pq


def test_gpu3070ti_readiness_refresh_builds_read_only_manifest(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_gpu3070ti_readiness_refresh")
    files = _write_local_inputs(tmp_path)
    runner = _fake_runner(builder, files=files)
    manifest = builder.build_manifest(_config(builder, tmp_path), runner=runner)

    assert manifest["status"] == "remote_readiness_refreshed_f02_6_still_blocked"
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["current_gate_state"] == {
        "f02_6_decision_status": "pending_human_decision",
        "remote_packet_status": "blocked_until_f02_6_decision",
        "ready_to_run_remote_training": False,
        "formal_performance_claim_allowed": False,
    }
    assert manifest["readiness_checks"] == {
        "ssh_alias_resolves_to_expected_relay": True,
        "jump_listener_present": True,
        "cuda_available": True,
        "critical_inputs_match": True,
        "remote_scripts_present": True,
        "f02_6_still_pending": True,
        "remote_packet_still_blocked": True,
    }
    assert manifest["critical_inputs"]["oracle_connector_results"]["local_remote_match"] is True
    assert manifest["critical_inputs"]["oracle_connector_results"]["local_rows"] == 2
    assert all(command["runs_training"] is False for command in manifest["commands_executed"])
    assert all(command["runs_remote_preflight"] is False for command in manifest["commands_executed"])


def test_gpu3070ti_readiness_refresh_fails_on_remote_hash_mismatch(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_gpu3070ti_readiness_refresh")
    files = _write_local_inputs(tmp_path)
    runner = _fake_runner(builder, files=files, checkpoint_sha="0" * 64)
    manifest = builder.build_manifest(_config(builder, tmp_path), runner=runner)

    assert manifest["status"] == "remote_readiness_refresh_failed"
    assert manifest["critical_inputs"]["obstacle_summary_bc_checkpoint"]["local_remote_match"] is False
    assert manifest["readiness_checks"]["critical_inputs_match"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False


def test_gpu3070ti_readiness_refresh_markdown_keeps_gate_boundary(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_gpu3070ti_readiness_refresh")
    files = _write_local_inputs(tmp_path)
    manifest = builder.build_manifest(_config(builder, tmp_path), runner=_fake_runner(builder, files=files))
    markdown = builder._markdown(manifest)

    assert "not a training run" in markdown
    assert "not an approved preflight" in markdown
    assert "F02.6 is still `pending_human_decision`" in markdown


def _config(builder, tmp_path):
    _write_json(tmp_path / "decision.json", {"status": "pending_human_decision"})
    _write_json(tmp_path / "remote_packet.json", {"status": "blocked_until_f02_6_decision", "ready_to_run_remote_training": False})
    _write_json(tmp_path / "claim_safety.json", {"formal_claim_allowed": False})
    _write_json(tmp_path / "h02.json", {"paper_result_input_allowed": False})
    return builder.Gpu3070TiReadinessRefreshConfig(
        output_dir=tmp_path / "out",
        local_root=tmp_path,
        decision_record_path=tmp_path / "decision.json",
        remote_packet_path=tmp_path / "remote_packet.json",
        claim_safety_path=tmp_path / "claim_safety.json",
        h02_acceptance_path=tmp_path / "h02.json",
    )


def _write_local_inputs(tmp_path):
    oracle = tmp_path / "0_trials/module2_oracle_shape/oracle_connector_results.parquet"
    checkpoint = tmp_path / "2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt"
    oracle.parent.mkdir(parents=True)
    checkpoint.parent.mkdir(parents=True)
    pq.write_table(pa.table({"node_id": [1, 2], "clearance": [0.5, 0.7]}), oracle)
    checkpoint.write_bytes(b"checkpoint-bytes")
    return {"oracle": oracle, "checkpoint": checkpoint}


def _fake_runner(builder, *, files, checkpoint_sha=None):
    oracle_sha = builder._sha256(files["oracle"])
    checkpoint_sha = checkpoint_sha or builder._sha256(files["checkpoint"])

    def run(args):
        joined = " ".join(args)
        if args[:2] == ("ssh", "-G"):
            return "\n".join(
                [
                    "user ubuntu",
                    "hostname 127.0.0.1",
                    "port 23070",
                    "hostkeyalias gpu3070ti-relay",
                    "proxyjump ubuntu-obgx",
                ]
            )
        if "ss -ltnp" in joined:
            return 'LISTEN 0 128 127.0.0.1:23070 0.0.0.0:* users:(("sshd",pid=1,fd=5))\n'
        if "nvidia-smi" in joined:
            return "\n".join(
                [
                    "ubuntu-OMEN-by-HP-Laptop-17-ck1xxx",
                    "ubuntu",
                    "Linux 6.17.0-35-generic x86_64 GNU/Linux",
                    "NVIDIA GeForce RTX 3070 Ti Laptop GPU, 8192, 7000, 595.71.05",
                ]
            )
        if "pyarrow.parquet" in joined or "<<'PY'" in joined:
            return json.dumps(
                {
                    "remote_python_stack": {
                        "python": "3.12.3",
                        "torch": "2.12.1+cu130",
                        "cuda_available": True,
                        "cuda_device_name": "NVIDIA GeForce RTX 3070 Ti Laptop GPU",
                        "stable_baselines3": "2.9.0",
                        "pyarrow": "24.0.0",
                        "gymnasium": "1.3.0",
                    },
                    "critical_inputs": {
                        "oracle_connector_results": {
                            "path": "0_trials/module2_oracle_shape/oracle_connector_results.parquet",
                            "exists": True,
                            "bytes": files["oracle"].stat().st_size,
                            "rows": 2,
                            "sha256": oracle_sha,
                        },
                        "obstacle_summary_bc_checkpoint": {
                            "path": "2_experiment/forest_n3p/models/module2_rl_rs_bc_obstacle_summary_formal_v2/checkpoint.pt",
                            "exists": True,
                            "bytes": files["checkpoint"].stat().st_size,
                            "sha256": checkpoint_sha,
                        },
                    },
                    "remote_script_presence": {
                        "preflight_rl_rs_gate3_formal_trial.py": {"exists": True, "bytes": 1},
                        "run_rl_rs_gate3_trial.py": {"exists": True, "bytes": 1},
                        "audit_rl_rs_gate3_trial.py": {"exists": True, "bytes": 1},
                    },
                }
            )
        raise AssertionError(f"unexpected command: {args!r}")

    return run


def _write_json(path, payload):
    path.write_text(json.dumps(payload) + "\n", encoding="utf-8")
