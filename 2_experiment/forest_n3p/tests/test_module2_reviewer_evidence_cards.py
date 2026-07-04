import json
from importlib import import_module


def test_reviewer_evidence_cards_build_traceable_cards(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_reviewer_evidence_cards")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing Module2 reviewer evidence cards builder: {exc}") from exc

    evidence_map = _write_json(tmp_path / "evidence_map.json", _evidence_map_payload(anchor=True))
    manifest_path = tmp_path / "cards.json"
    markdown_path = tmp_path / "cards.md"
    latex_path = tmp_path / "cards.tex"

    rc = builder.main(
        [
            "--evidence-map",
            str(evidence_map),
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--latex-out",
            str(latex_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    latex = latex_path.read_text(encoding="utf-8")

    assert manifest["artifact_name"] == "module2_reviewer_evidence_cards"
    assert manifest["status"] == "reviewer_evidence_cards_ready"
    assert manifest["local_training_allowed"] is False
    assert manifest["remote_training_resource"] == "gpu3070ti-relay"
    assert manifest["blocking_reasons"] == []

    cards = {item["card_id"]: item for item in manifest["cards"]}
    assert cards["method_is_ha_star_analytic_operator"]["reviewer_verdict"] == "claim_traceable_with_scope_limit"
    assert cards["method_is_ha_star_analytic_operator"]["manuscript_anchors"][0]["line"] == 8
    assert cards["formal_results_blocked"]["reviewer_verdict"] == "blocked_placeholder_traceable"
    assert "Do not write this as a result claim" in cards["formal_results_blocked"]["writing_instruction"]
    assert "module2_reviewer_evidence_cards" in markdown
    assert "3_paper/module2_section_seed/module2_paper_section_seed.tex:16" in markdown
    assert manifest["generated_outputs"]["latex"] == str(latex_path)
    assert r"\section{Module2 Reviewer Evidence Cards}" in latex
    assert r"3\_paper/module2\_section\_seed/module2\_paper\_section\_seed.tex:16" in latex
    assert "Do not write this as a result claim" in latex


def test_reviewer_evidence_cards_blocks_missing_anchors(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_reviewer_evidence_cards")
    evidence_map = _write_json(tmp_path / "evidence_map.json", _evidence_map_payload(anchor=False))

    manifest = builder.build_manifest(
        builder.ReviewerEvidenceCardsConfig(
            output_dir=tmp_path,
            evidence_map_path=evidence_map,
        )
    )

    assert manifest["status"] == "blocked_by_incomplete_reviewer_cards"
    assert "method_is_ha_star_analytic_operator:missing_manuscript_anchors" in manifest["blocking_reasons"]


def _evidence_map_payload(*, anchor):
    source_anchors = (
        [
            {
                "path": "3_paper/module2_section_seed/module2_paper_section_seed.tex",
                "line": 8,
                "cue_in_raw_line": True,
                "cue_in_comment_stripped_line": True,
                "excerpt": "Module2 is implemented as a learned analytic-expansion operator inside Hybrid A*.",
            }
        ]
        if anchor
        else []
    )
    return {
        "artifact_name": "module2_manuscript_evidence_map",
        "status": "module2_manuscript_evidence_mapped",
        "local_training_allowed": False,
        "remote_training_resource": "gpu3070ti-relay",
        "upstream_status": {
            "formal_performance_claim_allowed": False,
            "f02_6_decision_status": "pending_human_decision",
            "remote_execution_ready": False,
        },
        "claim_units": [
            {
                "unit_id": "method_is_ha_star_analytic_operator",
                "paper_scope": "methods",
                "claim_status": "allowed_method_structure",
                "evidence_state": "mapped",
                "manuscript_cues": [
                    {
                        "cue": "learned analytic-expansion operator inside",
                        "source_anchors": source_anchors,
                    }
                ],
                "evidence": [
                    {
                        "path": "0_trials/module2_method_algorithms/module2_method_algorithms.json",
                        "status": "code_anchored",
                    }
                ],
                "code_anchors": [
                    {
                        "path": "2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py",
                        "line": 129,
                        "symbol": "HybridAStarPlanner.__init__",
                    }
                ],
                "mapping_blockers": [],
            },
            {
                "unit_id": "formal_results_blocked",
                "paper_scope": "results_placeholder",
                "claim_status": "blocked_placeholder_not_a_result_claim",
                "evidence_state": "blocked_as_expected",
                "manuscript_cues": [
                    {
                        "cue": "% BLOCKED: formal_results",
                        "source_anchors": [
                            {
                                "path": "3_paper/module2_section_seed/module2_paper_section_seed.tex",
                                "line": 16,
                                "cue_in_raw_line": True,
                                "cue_in_comment_stripped_line": False,
                                "excerpt": "% BLOCKED: formal_results :: missing_module2_rl_rs_checkpoint",
                            }
                        ],
                    }
                ],
                "evidence": [
                    {
                        "path": "3_paper/module2_claim_audit/module2_manuscript_claim_audit.json",
                        "status": "maintex_module2_claim_audit_passed",
                    }
                ],
                "paper_blockers": ["missing_module2_rl_rs_checkpoint"],
                "mapping_blockers": [],
            },
        ],
    }


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path
