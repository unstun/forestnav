import json
from importlib import import_module


def test_manuscript_claim_audit_passes_expanded_module2_seed(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_manuscript_claim_audit")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing Module2 manuscript claim audit builder: {exc}") from exc

    paths = _write_inputs(tmp_path, prohibited=False)
    manifest_path = tmp_path / "audit.json"
    markdown_path = tmp_path / "audit.md"

    rc = builder.main(
        [
            "--main-tex",
            str(paths["main_tex"]),
            "--claim-safety",
            str(paths["claim_safety"]),
            "--paper-readiness",
            str(paths["paper_readiness"]),
            "--section-seed",
            str(paths["section_seed"]),
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

    assert manifest["artifact_name"] == "module2_manuscript_claim_audit"
    assert manifest["status"] == "maintex_module2_claim_audit_passed"
    assert manifest["local_training_allowed"] is False
    assert manifest["remote_training_resource"] == "gpu3070ti-relay"
    assert manifest["prohibited_claim_audit"]["status"] == "clean"
    assert manifest["module2_input_checks"]["module2_seed_input_present"] is True
    assert manifest["module2_input_checks"]["formal_results_blocked_comment_present"] is True
    assert manifest["module2_input_checks"]["warm_start_blocked_comment_present"] is True
    assert manifest["section_seed_checks"]["method_section_status"] == "draft_ready"
    assert manifest["readiness_checks"]["formal_results_status"] == "blocked"
    assert manifest["readiness_checks"]["warm_start_effect_status"] == "blocked"
    assert "maintex_module2_claim_audit_passed" in markdown


def test_manuscript_claim_audit_flags_prohibited_expanded_claim(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_manuscript_claim_audit")
    paths = _write_inputs(tmp_path, prohibited=True)

    manifest = builder.build_manifest(
        builder.ManuscriptClaimAuditConfig(
            output_dir=tmp_path,
            main_tex_path=paths["main_tex"],
            claim_safety_path=paths["claim_safety"],
            paper_readiness_path=paths["paper_readiness"],
            section_seed_path=paths["section_seed"],
        )
    )

    assert manifest["status"] == "blocked_by_manuscript_claim_audit"
    assert manifest["prohibited_claim_audit"]["status"] == "violations_found"
    assert {item["claim_id"] for item in manifest["prohibited_claim_audit"]["violations"]} == {"rl_replaces_hybrid_astar"}


def _write_inputs(tmp_path, *, prohibited):
    seed_dir = tmp_path / "module2_section_seed"
    seed_dir.mkdir()
    seed_tex = seed_dir / "module2_paper_section_seed.tex"
    extra = "\nRL replaces Hybrid A*." if prohibited else ""
    seed_tex.write_text(
        "\n".join(
            [
                r"\subsection{RL-RS Analytic Expansion Operator}",
                r"\label{sec:module2_rl_rs_operator}",
                "Module2 is implemented as a learned analytic-expansion operator inside Hybrid A*.",
                "This does not evaluate obstacle-summary warm-start PPO. Formal performance claims remain blocked.",
                "% BLOCKED: formal_results :: missing_module2_rl_rs_checkpoint",
                "% BLOCKED: warm_start_effect :: f02_6_not_approved",
                extra,
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
    claim_safety = _write_json(
        tmp_path / "claim_safety.json",
        {
            "artifact_name": "module2_claim_safety",
            "status": "blocked_formal_performance_claims",
            "formal_performance_claim_allowed": False,
            "allowed_claims": [
                {"claim_id": "method_is_ha_star_analytic_operator"},
                {"claim_id": "no_warm_gate3_formal_failure"},
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
    paper_readiness = _write_json(
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
    )
    section_seed = _write_json(
        tmp_path / "section_seed.json",
        {
            "artifact_name": "module2_paper_section_seed",
            "status": "method_sections_ready_results_blocked",
            "generated_outputs": {"latex": str(seed_tex)},
            "sections": [
                {"section_id": "methods_rl_rs_operator", "status": "draft_ready", "blockers": []},
                {"section_id": "no_warm_gate3_failure_note", "status": "draft_ready_with_scope_limit", "blockers": []},
                {"section_id": "formal_results", "status": "blocked", "blockers": ["missing_module2_rl_rs_checkpoint"]},
                {"section_id": "warm_start_effect", "status": "blocked", "blockers": ["f02_6_not_approved"]},
            ],
        },
    )
    return {
        "main_tex": main_tex,
        "claim_safety": claim_safety,
        "paper_readiness": paper_readiness,
        "section_seed": section_seed,
    }


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path
