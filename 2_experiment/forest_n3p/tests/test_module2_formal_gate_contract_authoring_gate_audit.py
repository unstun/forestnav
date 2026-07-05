import json
from importlib import import_module
from pathlib import Path


def test_contract_authoring_gate_blocks_while_protocol_lane_pending(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_formal_gate_contract_authoring_gate_audit")

    manifest = auditor.build_manifest(_config(tmp_path, recorded=False))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_formal_gate_contract_authoring_gate_audit"
    assert manifest["status"] == "contract_authoring_gate_blocked_pending_lane_decision"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["remote_training_allowed_now"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["paper_result_material_allowed"] is False
    gate = manifest["contract_gate"]
    assert gate["decision_gate_status"] == "protocol_lane_decision_gate_pending_clean"
    assert gate["decision_record_status"] == "pending_protocol_lane_decision"
    assert gate["selected_lane_id"] is None
    assert gate["contract_action"] == "none"
    assert gate["contract_drafting_allowed_now"] is False
    assert gate["contract_approval_allowed_now"] is False
    assert gate["draft_contract_allows_training"] is False
    assert gate["allowed_next_action_ids"] == ["record_protocol_lane_decision"]
    assert "remote_success_training" in gate["blocked_action_ids"]
    existing = manifest["existing_contract_summary"]
    assert existing["status"] == "approved"
    assert existing["version"] == "v1"
    assert existing["usable_for_new_success_attempt"] is False
    assert manifest["required_contract_sections"] == ["hypothesis", "success_signal", "failure_signal"]
    assert manifest["audit_issue_count"] == 0
    assert manifest["audit_issues"] == []


def test_contract_authoring_gate_allows_draft_after_recorded_lane_but_not_training(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_formal_gate_contract_authoring_gate_audit")

    manifest = auditor.build_manifest(_config(tmp_path, recorded=True))

    assert manifest["status"] == "contract_authoring_gate_ready_for_contract_draft"
    gate = manifest["contract_gate"]
    assert gate["decision_gate_status"] == "protocol_lane_decision_gate_recorded_clean"
    assert gate["decision_record_status"] == "protocol_lane_decision_recorded"
    assert gate["selected_lane_id"] == "hybrid_ppo_analytic_fallback"
    assert gate["contract_action"] == "draft_revised_contract"
    assert gate["contract_drafting_allowed_now"] is True
    assert gate["contract_approval_allowed_now"] is False
    assert gate["draft_contract_allows_training"] is False
    assert gate["allowed_next_action_ids"] == ["draft_new_or_revised_contract_after_lane_decision"]
    assert manifest["audit_issue_count"] == 0


def test_contract_authoring_gate_catches_pending_decision_that_allows_contract_or_training(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_formal_gate_contract_authoring_gate_audit")
    config = _config(tmp_path, recorded=False)
    record = json.loads(config.decision_record_path.read_text(encoding="utf-8"))
    record["contract_action"] = "draft_revised_contract"
    record["remote_training_allowed_now"] = True
    config.decision_record_path.write_text(json.dumps(record), encoding="utf-8")

    manifest = auditor.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["audit_issues"]}
    assert manifest["status"] == "contract_authoring_gate_audit_failed"
    assert "pending_decision_has_contract_action" in issue_ids
    assert "decision_record_remote_training_allowed_now_not_false" in issue_ids


def test_contract_authoring_gate_cli_writes_json_and_markdown(tmp_path):
    auditor = import_module("forest_n3p.scripts.build_module2_formal_gate_contract_authoring_gate_audit")
    config = _config(tmp_path, recorded=False)
    manifest_path = tmp_path / "contract_gate.json"
    markdown_path = tmp_path / "contract_gate.md"

    rc = auditor.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--decision-gate-audit",
            str(config.decision_gate_audit_path),
            "--decision-record",
            str(config.decision_record_path),
            "--contract-intake",
            str(config.contract_intake_path),
            "--next-round-requirements",
            str(config.next_round_requirements_path),
            "--existing-contract",
            str(config.existing_contract_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "contract_authoring_gate_blocked_pending_lane_decision"
    assert "Module2 Formal Gate Contract Authoring Gate Audit" in markdown
    assert "not paper result material" in markdown
    assert "contract_drafting_allowed_now: `False`" in markdown
    assert "allowed_next_action_ids" in markdown
    assert "record_protocol_lane_decision" in markdown
    assert "blocked_action_ids" in markdown
    assert "remote_success_training" in markdown
    assert "Required Contract Sections" in markdown
    assert "failure_signal" in markdown
    assert "Claim Boundaries" in markdown
    assert "A recorded lane decision can only open contract drafting, not training" in markdown


def _config(tmp_path, *, recorded):
    auditor = import_module("forest_n3p.scripts.build_module2_formal_gate_contract_authoring_gate_audit")
    return auditor.FormalGateContractAuthoringGateAuditConfig(
        output_dir=tmp_path,
        decision_gate_audit_path=_json(tmp_path, "decision_gate.json", _decision_gate(recorded=recorded)),
        decision_record_path=_json(tmp_path, "decision_record.json", _decision_record(recorded=recorded)),
        contract_intake_path=_json(tmp_path, "contract_intake.json", _contract_intake()),
        next_round_requirements_path=_json(tmp_path, "next_round.json", _next_round()),
        existing_contract_path=_contract(tmp_path),
    )


def _json(tmp_path: Path, name: str, payload: dict):
    path = tmp_path / name
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _decision_gate(*, recorded):
    return {
        "status": "protocol_lane_decision_gate_recorded_clean" if recorded else "protocol_lane_decision_gate_pending_clean",
        "audit_issue_count": 0,
    }


def _decision_record(*, recorded):
    return {
        "status": "protocol_lane_decision_recorded" if recorded else "pending_protocol_lane_decision",
        "runs_training": False,
        "runs_remote_preflight": False,
        "formal_claim_allowed": False,
        "remote_training_allowed_now": False,
        "local_training_allowed_now": False,
        "formal_claim_allowed_now": False,
        "paper_result_material_allowed_now": False,
        "selected_lane_id": "hybrid_ppo_analytic_fallback" if recorded else None,
        "contract_action": "draft_revised_contract" if recorded else "none",
    }


def _contract_intake():
    return {
        "status": "formal_gate_contract_intake_ready_for_dr_sun",
        "contract_output_requirements": {
            "required_sections": ["hypothesis", "success_signal", "failure_signal"]
        },
    }


def _next_round():
    return {"status": "formal_gate_next_round_requirements_ready"}


def _contract(tmp_path):
    path = tmp_path / "module2-ppo-funnel-expansion.md"
    path.write_text(
        "---\nstatus: approved\nversion: v1\napproved_by: Dr Sun\napproved_date: 2026-07-02\norigin: ai+human\nreviewed: false\n---\n",
        encoding="utf-8",
    )
    return path
