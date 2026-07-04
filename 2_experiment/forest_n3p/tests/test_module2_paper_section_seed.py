import json
from importlib import import_module


def test_paper_section_seed_writes_allowed_sections_and_blocks_results(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_paper_section_seed")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing Module2 paper section seed builder: {exc}") from exc

    paths = _write_inputs(tmp_path, methods_ready=True)
    manifest_path = tmp_path / "section_seed.json"
    markdown_path = tmp_path / "section_seed.md"

    rc = builder.main(
        [
            "--paper-readiness",
            str(paths["readiness"]),
            "--method-algorithms",
            str(paths["method_algorithms"]),
            "--system-diagram",
            str(paths["system_diagram"]),
            "--claim-safety",
            str(paths["claim_safety"]),
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

    assert manifest["artifact_name"] == "module2_paper_section_seed"
    assert manifest["status"] == "method_sections_ready_results_blocked"
    assert manifest["local_training_allowed"] is False
    assert manifest["remote_training_resource"] == "gpu3070ti-relay"
    assert manifest["draft_audit"]["status"] == "clean"

    sections = {item["section_id"]: item for item in manifest["sections"]}
    assert sections["methods_rl_rs_operator"]["status"] == "draft_ready"
    assert sections["system_figure_caption"]["status"] == "draft_ready"
    assert sections["no_warm_gate3_failure_note"]["status"] == "draft_ready_with_scope_limit"
    assert sections["formal_results"]["status"] == "blocked"
    assert sections["warm_start_effect"]["status"] == "blocked"
    assert "0.453125" in sections["no_warm_gate3_failure_note"]["draft_text"]
    assert "does not evaluate obstacle-summary warm-start" in sections["no_warm_gate3_failure_note"]["draft_text"]
    assert "Formal performance claims remain blocked" in markdown


def test_paper_section_seed_blocks_when_readiness_does_not_allow_methods(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_paper_section_seed")
    paths = _write_inputs(tmp_path, methods_ready=False)

    manifest = builder.build_manifest(
        builder.PaperSectionSeedConfig(
            output_dir=tmp_path,
            paper_readiness_path=paths["readiness"],
            method_algorithms_path=paths["method_algorithms"],
            system_diagram_path=paths["system_diagram"],
            claim_safety_path=paths["claim_safety"],
        )
    )

    assert manifest["status"] == "blocked_by_readiness_or_claim_audit"
    sections = {item["section_id"]: item for item in manifest["sections"]}
    assert sections["methods_rl_rs_operator"]["status"] == "blocked"
    assert "method_algorithm_not_ready" in sections["methods_rl_rs_operator"]["blockers"]


def _write_inputs(tmp_path, *, methods_ready):
    paths = {}
    paths["readiness"] = _write_json(
        tmp_path / "readiness.json",
        {
            "artifact_name": "module2_paper_readiness",
            "status": "partial_methods_ready_results_blocked",
            "local_training_allowed": False,
            "remote_training_resource": "gpu3070ti-relay",
            "section_readiness": [
                {
                    "section_id": "method_algorithm",
                    "status": "ready_to_write" if methods_ready else "blocked",
                    "evidence": ["method_algorithms.json"],
                    "blockers": [] if methods_ready else ["method_algorithms_not_code_anchored"],
                },
                {
                    "section_id": "system_figure",
                    "status": "ready_to_write",
                    "evidence": ["system_diagram.json"],
                    "blockers": [],
                },
                {
                    "section_id": "no_warm_failure_claim",
                    "status": "ready_with_scope_limit",
                    "evidence": ["claim_safety.json"],
                    "blockers": [],
                },
                {
                    "section_id": "formal_results",
                    "status": "blocked",
                    "evidence": ["claim_safety.json"],
                    "blockers": ["missing_module2_rl_rs_checkpoint"],
                },
                {
                    "section_id": "warm_start_effect",
                    "status": "blocked",
                    "evidence": ["decision_record.json"],
                    "blockers": ["f02_6_not_approved"],
                },
            ],
        },
    )
    paths["method_algorithms"] = _write_json(
        tmp_path / "method_algorithms.json",
        {
            "artifact_name": "module2_method_algorithms",
            "status": "code_anchored",
            "algorithms": [
                {
                    "algorithm_id": "rl_rs_funnel_analytic_expansion",
                    "title": "Algorithm 1",
                    "paper_claim": "The learned component is an analytic-expansion operator, not a standalone global planner.",
                    "steps": [
                        {
                            "step_id": "A1.1",
                            "action": "Install a custom analytic-expansion operator.",
                            "code_anchors": [{"path": "planner.py", "line": 10, "symbol": "planner", "pattern": "operator"}],
                        },
                        {
                            "step_id": "A1.6",
                            "action": "Use terminal RS as the acceptance certificate.",
                            "code_anchors": [{"path": "terminal.py", "line": 20, "symbol": "terminal", "pattern": "check"}],
                        },
                    ],
                }
            ],
        },
    )
    paths["system_diagram"] = _write_json(
        tmp_path / "system_diagram.json",
        {
            "artifact_name": "module2_system_diagram",
            "status": "code_anchored_drawio",
            "figure_title": "Figure: RL-RS analytic expansion system inside Hybrid A*",
            "figure_intent": "Show Module2 as a learned analytic-expansion operator inside Hybrid A*.",
            "nodes": [
                {"node_id": "hybrid_astar_loop", "title": "Hybrid A* search loop"},
                {"node_id": "terminal_rs_certificate", "title": "Terminal RS certificate"},
                {"node_id": "fallback_primitives", "title": "Fallback primitive expansion"},
            ],
        },
    )
    paths["claim_safety"] = _write_json(
        tmp_path / "claim_safety.json",
        {
            "artifact_name": "module2_claim_safety",
            "status": "blocked_formal_performance_claims",
            "formal_performance_claim_allowed": False,
            "allowed_claims": [
                {
                    "claim_id": "no_warm_gate3_formal_failure",
                    "scope": "no_warm_only",
                    "claim_text": "No-warm PPO Gate #3 formal trial failed: terminal-RS success rate was 0.453125 over 64 episodes, below threshold 0.8.",
                    "required_qualifier": "This does not evaluate obstacle-summary warm-start PPO and does not reject the whole RL-RS direction.",
                    "evidence": ["gate3_formal_audit.json"],
                }
            ],
            "prohibited_claims": [
                {
                    "claim_id": "rl_replaces_hybrid_astar",
                    "severity": "hard_block",
                    "patterns": ["RL replaces Hybrid A*", "replace Hybrid A*"],
                    "reason": "The learned policy is only an analytic-expansion operator inside Hybrid A*.",
                }
            ],
            "formal_performance_blockers": ["missing_module2_rl_rs_checkpoint"],
        },
    )
    return paths


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path
