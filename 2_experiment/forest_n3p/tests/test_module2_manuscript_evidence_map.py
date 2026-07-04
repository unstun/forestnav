import json
from importlib import import_module


def test_manuscript_evidence_map_links_claim_units_to_sources(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_manuscript_evidence_map")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing Module2 manuscript evidence map builder: {exc}") from exc

    paths = _write_inputs(tmp_path, include_method_cue=True)
    manifest_path = tmp_path / "evidence_map.json"
    markdown_path = tmp_path / "evidence_map.md"

    rc = builder.main(
        [
            "--main-tex",
            str(paths["main_tex"]),
            "--claim-audit",
            str(paths["claim_audit"]),
            "--section-seed",
            str(paths["section_seed"]),
            "--paper-readiness",
            str(paths["paper_readiness"]),
            "--claim-safety",
            str(paths["claim_safety"]),
            "--method-algorithms",
            str(paths["method_algorithms"]),
            "--system-diagram",
            str(paths["system_diagram"]),
            "--gate3-audit",
            str(paths["gate3_audit"]),
            "--f02-6-decision-record",
            str(paths["decision_record"]),
            "--remote-execution-packet",
            str(paths["remote_packet"]),
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

    assert manifest["artifact_name"] == "module2_manuscript_evidence_map"
    assert manifest["status"] == "module2_manuscript_evidence_mapped"
    assert manifest["local_training_allowed"] is False
    assert manifest["remote_training_resource"] == "gpu3070ti-relay"
    assert manifest["blocking_reasons"] == []
    assert manifest["upstream_status"]["claim_audit_status"] == "maintex_module2_claim_audit_passed"
    assert manifest["upstream_status"]["formal_performance_claim_allowed"] is False

    units = {item["unit_id"]: item for item in manifest["claim_units"]}
    assert units["method_is_ha_star_analytic_operator"]["evidence_state"] == "mapped"
    assert units["method_is_ha_star_analytic_operator"]["code_anchors"]
    method_cue = units["method_is_ha_star_analytic_operator"]["manuscript_cues"][0]
    assert method_cue["source_anchors"]
    assert method_cue["source_anchors"][0]["path"].endswith("module2_paper_section_seed.tex")
    assert method_cue["source_anchors"][0]["line"] == 3
    assert method_cue["source_anchors"][0]["cue_in_comment_stripped_line"] is True
    assert units["no_warm_gate3_formal_failure"]["evidence_state"] == "mapped"
    assert units["no_warm_gate3_formal_failure"]["metric_values"]["terminal_rs_success_rate"] == 0.453125
    assert units["formal_results_blocked"]["evidence_state"] == "blocked_as_expected"
    assert "missing_module2_rl_rs_checkpoint" in units["formal_results_blocked"]["paper_blockers"]
    formal_comment_cue = units["formal_results_blocked"]["manuscript_cues"][1]
    assert formal_comment_cue["source_anchors"][0]["line"] == 8
    assert formal_comment_cue["source_anchors"][0]["cue_in_raw_line"] is True
    assert formal_comment_cue["source_anchors"][0]["cue_in_comment_stripped_line"] is False
    assert units["warm_start_effect_blocked"]["evidence_state"] == "blocked_as_expected"
    assert "requires_dr_sun_approval" in units["warm_start_effect_blocked"]["paper_blockers"]
    assert "module2_manuscript_evidence_mapped" in markdown


def test_manuscript_evidence_map_blocks_missing_method_cue(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_manuscript_evidence_map")
    paths = _write_inputs(tmp_path, include_method_cue=False)

    manifest = builder.build_manifest(
        builder.ManuscriptEvidenceMapConfig(
            output_dir=tmp_path,
            main_tex_path=paths["main_tex"],
            claim_audit_path=paths["claim_audit"],
            section_seed_path=paths["section_seed"],
            paper_readiness_path=paths["paper_readiness"],
            claim_safety_path=paths["claim_safety"],
            method_algorithms_path=paths["method_algorithms"],
            system_diagram_path=paths["system_diagram"],
            gate3_audit_path=paths["gate3_audit"],
            f02_6_decision_record_path=paths["decision_record"],
            remote_execution_packet_path=paths["remote_packet"],
        )
    )

    assert manifest["status"] == "blocked_by_missing_manuscript_evidence"
    units = {item["unit_id"]: item for item in manifest["claim_units"]}
    blockers = units["method_is_ha_star_analytic_operator"]["mapping_blockers"]
    assert "method_is_ha_star_analytic_operator:missing_manuscript_cue:learned analytic-expansion operator inside" in blockers
    assert manifest["missing_evidence"]


def _write_inputs(tmp_path, *, include_method_cue):
    seed_dir = tmp_path / "module2_section_seed"
    seed_dir.mkdir()
    seed_tex = seed_dir / "module2_paper_section_seed.tex"
    method_sentence = (
        "Module2 is implemented as a learned analytic-expansion operator inside Hybrid A*, "
        "not a standalone global planner, with a terminal RS certificate."
        if include_method_cue
        else "Module2 is described here without the required method-boundary phrase."
    )
    seed_tex.write_text(
        "\n".join(
            [
                r"\subsection{RL-RS Analytic Expansion Operator}",
                r"\label{sec:module2_rl_rs_operator}",
                method_sentence,
                "No-warm PPO Gate \\#3 formal trial failed: terminal-RS success rate was 0.453125 over 64 episodes, below threshold 0.8.",
                "This does not evaluate obstacle-summary warm-start PPO and does not reject the whole RL-RS direction.",
                "Formal performance claims remain blocked.",
                "% BLOCKED: formal_results :: missing_module2_rl_rs_checkpoint",
                "% BLOCKED: warm_start_effect :: f02_6_not_approved",
            ]
        ),
        encoding="utf-8",
    )
    main_tex = tmp_path / "main.tex"
    main_tex.write_text(
        "\n".join(
            [
                r"\section{Method}",
                r"\input{module2_section_seed/module2_paper_section_seed.tex}",
                r"\section{Results}",
            ]
        ),
        encoding="utf-8",
    )
    paths = {
        "main_tex": main_tex,
        "claim_audit": _write_json(
            tmp_path / "claim_audit.json",
            {
                "artifact_name": "module2_manuscript_claim_audit",
                "status": "maintex_module2_claim_audit_passed",
                "prohibited_claim_audit": {"status": "clean", "violations": []},
            },
        ),
        "section_seed": _write_json(
            tmp_path / "section_seed.json",
            {
                "artifact_name": "module2_paper_section_seed",
                "status": "method_sections_ready_results_blocked",
                "sections": [
                    {"section_id": "methods_rl_rs_operator", "status": "draft_ready", "blockers": []},
                    {"section_id": "no_warm_gate3_failure_note", "status": "draft_ready_with_scope_limit", "blockers": []},
                    {"section_id": "formal_results", "status": "blocked", "blockers": ["missing_module2_rl_rs_checkpoint"]},
                    {"section_id": "warm_start_effect", "status": "blocked", "blockers": ["f02_6_not_approved"]},
                ],
            },
        ),
        "paper_readiness": _write_json(
            tmp_path / "paper_readiness.json",
            {
                "artifact_name": "module2_paper_readiness",
                "status": "partial_methods_ready_results_blocked",
                "section_readiness": [
                    {"section_id": "method_algorithm", "status": "ready_to_write", "blockers": []},
                    {"section_id": "no_warm_failure_claim", "status": "ready_with_scope_limit", "blockers": []},
                    {"section_id": "formal_results", "status": "blocked", "blockers": ["missing_module2_rl_rs_checkpoint"]},
                    {"section_id": "warm_start_effect", "status": "blocked", "blockers": ["f02_6_not_approved"]},
                ],
            },
        ),
        "claim_safety": _write_json(
            tmp_path / "claim_safety.json",
            {
                "artifact_name": "module2_claim_safety",
                "status": "blocked_formal_performance_claims",
                "formal_performance_claim_allowed": False,
                "allowed_claims": [
                    {
                        "claim_id": "method_is_ha_star_analytic_operator",
                        "claim_text": "Module2 implements a learned analytic-expansion operator inside Hybrid A*.",
                        "required_qualifier": "Do not describe it as an end-to-end RL global planner.",
                    },
                    {
                        "claim_id": "no_warm_gate3_formal_failure",
                        "claim_text": "No-warm PPO Gate #3 formal trial failed.",
                        "required_qualifier": "This does not evaluate obstacle-summary warm-start PPO.",
                    },
                ],
                "code_anchors": [{"path": "claim_safety.py", "line": 1, "symbol": "claim_guard", "pattern": "guard"}],
            },
        ),
        "method_algorithms": _write_json(
            tmp_path / "method_algorithms.json",
            {
                "artifact_name": "module2_method_algorithms",
                "status": "code_anchored",
                "algorithms": [
                    {
                        "algorithm_id": "rl_rs_funnel_analytic_expansion",
                        "steps": [
                            {
                                "step_id": "A1.1",
                                "code_anchors": [{"path": "planner.py", "line": 10, "symbol": "planner", "pattern": "operator"}],
                            }
                        ],
                    }
                ],
            },
        ),
        "system_diagram": _write_json(
            tmp_path / "system_diagram.json",
            {
                "artifact_name": "module2_system_diagram",
                "status": "code_anchored_drawio",
                "nodes": [
                    {
                        "node_id": "terminal_rs_certificate",
                        "code_anchors": [{"path": "terminal.py", "line": 20, "symbol": "terminal", "pattern": "check"}],
                    }
                ],
            },
        ),
        "gate3_audit": _write_json(
            tmp_path / "gate3_audit.json",
            {
                "formal_claim_allowed": True,
                "formal_decision": "fail",
                "terminal_rs_success_rate": 0.453125,
                "episodes": 64,
                "success_threshold": 0.8,
            },
        ),
        "decision_record": _write_json(
            tmp_path / "decision_record.json",
            {
                "record_name": "module2_f02_6_decision_record",
                "status": "pending_human_decision",
                "blockers": ["requires_dr_sun_approval"],
            },
        ),
        "remote_packet": _write_json(
            tmp_path / "remote_packet.json",
            {
                "packet_name": "module2_remote_formal_execution_packet",
                "status": "blocked_until_f02_6_decision",
                "ready_to_run_remote_training": False,
                "blockers": ["requires_dr_sun_approval"],
            },
        ),
    }
    return paths


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path
