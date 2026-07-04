import json
from importlib import import_module


def test_formal_gate_gap_audit_blocks_current_pending_gate_and_lists_missing_artifacts(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_formal_gate_gap_audit")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing formal gate gap audit builder: {exc}") from exc

    manifest_path = tmp_path / "formal_gate_gap_audit.json"
    markdown_path = tmp_path / "formal_gate_gap_audit.md"
    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--contract",
            str(_contract(tmp_path)),
            "--decision-record",
            str(_decision_record(tmp_path, pending=True)),
            "--h01-manifest",
            str(_h01_manifest(tmp_path, ready=False)),
            "--remote-packet",
            str(_remote_packet(tmp_path, ready=False, artifacts_present=False)),
            "--h02-acceptance",
            str(_h02_acceptance(tmp_path, accepted=False)),
            "--claim-safety",
            str(_claim_safety(tmp_path, allowed=False)),
            "--readiness",
            str(_readiness(tmp_path, ready=False)),
            "--remote-readiness-refresh",
            str(_remote_readiness(tmp_path, good=True)),
            "--source-freshness-audit",
            str(_source_freshness(tmp_path, clean=True)),
            "--missing-artifacts-audit",
            str(_missing_artifacts(tmp_path, complete=True)),
            "--closure-checklist",
            str(_closure_checklist(tmp_path, complete=True)),
            "--status-report",
            str(_status_report(tmp_path, ready=True)),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_formal_gate_gap_audit"
    assert manifest["status"] == "blocked_formal_gate_gaps_open"
    assert manifest["not_paper_result_material"] is True
    assert manifest["local_training_allowed"] is False
    assert manifest["remote_training_resource"] == "gpu3070ti-relay"
    assert manifest["current_gate_state"]["formal_performance_claim_allowed"] is False
    assert manifest["remote_readiness"]["oracle_connector_results_match"] is True
    assert manifest["remote_readiness"]["obstacle_summary_bc_checkpoint_match"] is True
    assert manifest["source_freshness"]["regeneration_required_before_remote_formal_execution"] is False

    gap_ids = {
        gap["gap_id"]
        for key in (
            "missing_decision_items",
            "missing_training_artifacts",
            "missing_evaluation_artifacts",
            "missing_acceptance_artifacts",
        )
        for gap in manifest[key]
    }
    assert "f02_6_warm_start_decision_pending" in gap_ids
    assert "remote_training_packet_not_ready" in gap_ids
    assert "missing_remote_pullback_artifact" in gap_ids
    assert "missing_ppo_result_rows" in gap_ids
    assert "missing_ppo_checkpoint_hash" in gap_ids
    assert "h01_manifest_not_ready" in gap_ids
    assert "h02_verdict_not_formal" in gap_ids
    assert "h02_formal_output_not_accepted" in gap_ids
    assert "claim_safety_blocks_formal_performance" in gap_ids
    assert "readiness_blocks_formal_results" in gap_ids
    assert "Formal Gate Gap Audit" in markdown
    assert "not a paper result" in markdown
    assert "Source Freshness" in markdown
    assert "runs_training=`True`, host=`gpu3070ti-relay`" in markdown


def test_formal_gate_gap_audit_can_be_clean_only_after_remote_artifacts_and_acceptance(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_gap_audit")

    remote_packet = _remote_packet(tmp_path, ready=True, artifacts_present=True)
    manifest = builder.build_manifest(
        builder.FormalGateGapAuditConfig(
            output_dir=tmp_path,
            contract_path=_contract(tmp_path),
            decision_record_path=_decision_record(tmp_path, pending=False),
            h01_manifest_path=_h01_manifest(tmp_path, ready=True),
            remote_packet_path=remote_packet,
            h02_acceptance_path=_h02_acceptance(tmp_path, accepted=True),
            claim_safety_path=_claim_safety(tmp_path, allowed=True),
            readiness_path=_readiness(tmp_path, ready=True),
            remote_readiness_path=_remote_readiness(tmp_path, good=True),
            source_freshness_path=_source_freshness(tmp_path, clean=True),
            missing_artifacts_path=_missing_artifacts(tmp_path, complete=True),
            closure_checklist_path=_closure_checklist(tmp_path, complete=True),
            status_report_path=_status_report(tmp_path, ready=True),
            handoff_bundle_path=_handoff_bundle(tmp_path, ready=True, pending=False),
            remote_packet_safety_path=_remote_packet_safety(tmp_path, ready=True),
        )
    )

    assert manifest["status"] == "formal_gate_ready_for_result_audit"
    assert manifest["local_training_allowed"] is False
    assert manifest["missing_decision_items"] == []
    assert manifest["missing_training_artifacts"] == []
    assert manifest["missing_evaluation_artifacts"] == []
    assert manifest["missing_acceptance_artifacts"] == []
    assert manifest["ordered_next_steps"][-1]["status"] == "ready"


def test_formal_gate_gap_audit_does_not_treat_expected_training_outputs_as_training_preconditions(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_gap_audit")

    manifest = builder.build_manifest(
        builder.FormalGateGapAuditConfig(
            output_dir=tmp_path,
            contract_path=_contract(tmp_path),
            decision_record_path=_decision_record(tmp_path, pending=False),
            h01_manifest_path=_h01_manifest(tmp_path, ready=True),
            remote_packet_path=_remote_packet(tmp_path, ready=True, artifacts_present=False),
            h02_acceptance_path=_h02_acceptance(tmp_path, accepted=False),
            claim_safety_path=_claim_safety(tmp_path, allowed=False),
            readiness_path=_readiness(tmp_path, ready=False),
            remote_readiness_path=_remote_readiness(tmp_path, good=True),
            source_freshness_path=_source_freshness(tmp_path, clean=True),
            missing_artifacts_path=_missing_artifacts(tmp_path, complete=True),
            closure_checklist_path=_closure_checklist(tmp_path, complete=True),
            status_report_path=_status_report(tmp_path, ready=True),
            handoff_bundle_path=_handoff_bundle(tmp_path, ready=True, pending=False),
            remote_packet_safety_path=_remote_packet_safety(tmp_path, ready=True),
        )
    )

    steps = {step["step_id"]: step for step in manifest["ordered_next_steps"]}
    assert steps["remote_preflight"]["status"] == "pending_execution"
    assert steps["gate3_remote_training"]["status"] == "pending_execution"
    assert steps["gate3_remote_training"]["blocked_by"] == []
    assert steps["gate3_remote_audit_pullback"]["status"] == "blocked"
    assert "missing_remote_pullback_artifact" in steps["gate3_remote_audit_pullback"]["blocked_by"]
    assert steps["gate3_remote_audit_pullback"]["blocked_by"].count("missing_remote_pullback_artifact") == 1
    assert steps["h01_h02_regeneration"]["status"] == "blocked"
    assert "missing_ppo_result_rows" in steps["h01_h02_regeneration"]["blocked_by"]
    assert steps["claim_safety_final_gate"]["status"] == "blocked"


def test_formal_gate_gap_audit_blocks_remote_execution_when_readiness_inputs_do_not_match(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_gap_audit")

    manifest = builder.build_manifest(
        builder.FormalGateGapAuditConfig(
            output_dir=tmp_path,
            contract_path=_contract(tmp_path),
            decision_record_path=_decision_record(tmp_path, pending=False),
            h01_manifest_path=_h01_manifest(tmp_path, ready=True),
            remote_packet_path=_remote_packet(tmp_path, ready=True, artifacts_present=False),
            h02_acceptance_path=_h02_acceptance(tmp_path, accepted=False),
            claim_safety_path=_claim_safety(tmp_path, allowed=False),
            readiness_path=_readiness(tmp_path, ready=False),
            remote_readiness_path=_remote_readiness(tmp_path, good=False),
            source_freshness_path=_source_freshness(tmp_path, clean=True),
            missing_artifacts_path=_missing_artifacts(tmp_path, complete=True),
            closure_checklist_path=_closure_checklist(tmp_path, complete=True),
            status_report_path=_status_report(tmp_path, ready=True),
            handoff_bundle_path=_handoff_bundle(tmp_path, ready=True, pending=False),
            remote_packet_safety_path=_remote_packet_safety(tmp_path, ready=True),
        )
    )

    training_gap_ids = {gap["gap_id"] for gap in manifest["missing_training_artifacts"]}
    assert "remote_readiness_oracle_connector_results_mismatch" in training_gap_ids
    assert "remote_readiness_obstacle_summary_bc_checkpoint_mismatch" in training_gap_ids
    steps = {step["step_id"]: step for step in manifest["ordered_next_steps"]}
    assert steps["remote_preflight"]["status"] == "blocked"
    assert "remote_readiness_oracle_connector_results_mismatch" in steps["remote_preflight"]["blocked_by"]
    assert steps["gate3_remote_training"]["status"] == "blocked"


def test_formal_gate_gap_audit_blocks_remote_execution_when_source_freshness_requires_regeneration(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_gap_audit")

    manifest = builder.build_manifest(
        builder.FormalGateGapAuditConfig(
            output_dir=tmp_path,
            contract_path=_contract(tmp_path),
            decision_record_path=_decision_record(tmp_path, pending=False),
            h01_manifest_path=_h01_manifest(tmp_path, ready=True),
            remote_packet_path=_remote_packet(tmp_path, ready=True, artifacts_present=False),
            h02_acceptance_path=_h02_acceptance(tmp_path, accepted=False),
            claim_safety_path=_claim_safety(tmp_path, allowed=False),
            readiness_path=_readiness(tmp_path, ready=False),
            remote_readiness_path=_remote_readiness(tmp_path, good=True),
            source_freshness_path=_source_freshness(tmp_path, clean=False),
            missing_artifacts_path=_missing_artifacts(tmp_path, complete=True),
            closure_checklist_path=_closure_checklist(tmp_path, complete=True),
            status_report_path=_status_report(tmp_path, ready=True),
            handoff_bundle_path=_handoff_bundle(tmp_path, ready=True, pending=False),
            remote_packet_safety_path=_remote_packet_safety(tmp_path, ready=True),
        )
    )

    training_gap_ids = {gap["gap_id"] for gap in manifest["missing_training_artifacts"]}
    assert "source_freshness_regeneration_required" in training_gap_ids
    assert manifest["source_freshness"]["ordered_regeneration_target_count"] == 2
    steps = {step["step_id"]: step for step in manifest["ordered_next_steps"]}
    assert steps["remote_preflight"]["status"] == "blocked"
    assert "source_freshness_regeneration_required" in steps["remote_preflight"]["blocked_by"]
    assert steps["gate3_remote_training"]["status"] == "blocked"
    assert "source_freshness_regeneration_required" in steps["gate3_remote_training"]["blocked_by"]


def test_formal_gate_gap_audit_rejects_source_freshness_audit_that_runs_or_claims_results(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_gap_audit")

    manifest = builder.build_manifest(
        builder.FormalGateGapAuditConfig(
            output_dir=tmp_path,
            contract_path=_contract(tmp_path),
            decision_record_path=_decision_record(tmp_path, pending=False),
            h01_manifest_path=_h01_manifest(tmp_path, ready=True),
            remote_packet_path=_remote_packet(tmp_path, ready=True, artifacts_present=False),
            h02_acceptance_path=_h02_acceptance(tmp_path, accepted=False),
            claim_safety_path=_claim_safety(tmp_path, allowed=False),
            readiness_path=_readiness(tmp_path, ready=False),
            remote_readiness_path=_remote_readiness(tmp_path, good=True),
            source_freshness_path=_source_freshness(tmp_path, clean=True, invalid=True),
            missing_artifacts_path=_missing_artifacts(tmp_path, complete=True),
            closure_checklist_path=_closure_checklist(tmp_path, complete=True),
            status_report_path=_status_report(tmp_path, ready=True),
            handoff_bundle_path=_handoff_bundle(tmp_path, ready=True, pending=False),
            remote_packet_safety_path=_remote_packet_safety(tmp_path, ready=True),
        )
    )

    training_gap_ids = {gap["gap_id"] for gap in manifest["missing_training_artifacts"]}
    assert "source_freshness_audit_ran_training" in training_gap_ids
    assert "source_freshness_audit_ran_preflight" in training_gap_ids
    assert "source_freshness_allows_local_training" in training_gap_ids
    assert "source_freshness_allows_formal_claim" in training_gap_ids


def test_formal_gate_gap_audit_consumes_missing_artifacts_inventory(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_gap_audit")

    manifest = builder.build_manifest(
        builder.FormalGateGapAuditConfig(
            output_dir=tmp_path,
            contract_path=_contract(tmp_path),
            decision_record_path=_decision_record(tmp_path, pending=False),
            h01_manifest_path=_h01_manifest(tmp_path, ready=True),
            remote_packet_path=_remote_packet(tmp_path, ready=True, artifacts_present=True),
            h02_acceptance_path=_h02_acceptance(tmp_path, accepted=True),
            claim_safety_path=_claim_safety(tmp_path, allowed=True),
            readiness_path=_readiness(tmp_path, ready=True),
            remote_readiness_path=_remote_readiness(tmp_path, good=True),
            source_freshness_path=_source_freshness(tmp_path, clean=True),
            missing_artifacts_path=_missing_artifacts(tmp_path, complete=False),
            closure_checklist_path=_closure_checklist(tmp_path, complete=True),
            status_report_path=_status_report(tmp_path, ready=True),
            handoff_bundle_path=_handoff_bundle(tmp_path, ready=True, pending=False),
            remote_packet_safety_path=_remote_packet_safety(tmp_path, ready=True),
        )
    )

    assert manifest["status"] == "blocked_formal_gate_gaps_open"
    assert manifest["missing_artifacts_inventory"]["all_required_evidence_present"] is False
    acceptance_gap_ids = {gap["gap_id"] for gap in manifest["missing_acceptance_artifacts"]}
    assert "formal_gate_missing_artifacts_open" in acceptance_gap_ids
    steps = {step["step_id"]: step for step in manifest["ordered_next_steps"]}
    assert steps["gate3_remote_training"]["status"] == "pending_execution"
    assert steps["claim_safety_final_gate"]["status"] == "blocked"
    assert "formal_gate_missing_artifacts_open" in steps["claim_safety_final_gate"]["blocked_by"]


def test_formal_gate_gap_audit_rejects_missing_artifacts_inventory_that_runs_or_claims(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_gap_audit")

    manifest = builder.build_manifest(
        builder.FormalGateGapAuditConfig(
            output_dir=tmp_path,
            contract_path=_contract(tmp_path),
            decision_record_path=_decision_record(tmp_path, pending=False),
            h01_manifest_path=_h01_manifest(tmp_path, ready=True),
            remote_packet_path=_remote_packet(tmp_path, ready=True, artifacts_present=True),
            h02_acceptance_path=_h02_acceptance(tmp_path, accepted=True),
            claim_safety_path=_claim_safety(tmp_path, allowed=True),
            readiness_path=_readiness(tmp_path, ready=True),
            remote_readiness_path=_remote_readiness(tmp_path, good=True),
            source_freshness_path=_source_freshness(tmp_path, clean=True),
            missing_artifacts_path=_missing_artifacts(tmp_path, complete=True, invalid=True),
            closure_checklist_path=_closure_checklist(tmp_path, complete=True),
            status_report_path=_status_report(tmp_path, ready=True),
            handoff_bundle_path=_handoff_bundle(tmp_path, ready=True, pending=False),
            remote_packet_safety_path=_remote_packet_safety(tmp_path, ready=True),
        )
    )

    acceptance_gap_ids = {gap["gap_id"] for gap in manifest["missing_acceptance_artifacts"]}
    assert "formal_missing_artifacts_audit_executes_commands" in acceptance_gap_ids
    assert "formal_missing_artifacts_audit_runs_training" in acceptance_gap_ids
    assert "formal_missing_artifacts_audit_runs_preflight" in acceptance_gap_ids
    assert "formal_missing_artifacts_allows_local_training" in acceptance_gap_ids
    assert "formal_missing_artifacts_allows_claim" in acceptance_gap_ids


def test_formal_gate_gap_audit_consumes_closure_checklist(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_gap_audit")

    manifest = builder.build_manifest(
        builder.FormalGateGapAuditConfig(
            output_dir=tmp_path,
            contract_path=_contract(tmp_path),
            decision_record_path=_decision_record(tmp_path, pending=False),
            h01_manifest_path=_h01_manifest(tmp_path, ready=True),
            remote_packet_path=_remote_packet(tmp_path, ready=True, artifacts_present=True),
            h02_acceptance_path=_h02_acceptance(tmp_path, accepted=True),
            claim_safety_path=_claim_safety(tmp_path, allowed=True),
            readiness_path=_readiness(tmp_path, ready=True),
            remote_readiness_path=_remote_readiness(tmp_path, good=True),
            source_freshness_path=_source_freshness(tmp_path, clean=True),
            missing_artifacts_path=_missing_artifacts(tmp_path, complete=True),
            closure_checklist_path=_closure_checklist(tmp_path, complete=False),
            status_report_path=_status_report(tmp_path, ready=True),
            handoff_bundle_path=_handoff_bundle(tmp_path, ready=True, pending=False),
            remote_packet_safety_path=_remote_packet_safety(tmp_path, ready=True),
        )
    )

    assert manifest["status"] == "blocked_formal_gate_gaps_open"
    assert manifest["closure_checklist"]["status"] == "formal_gate_closure_blocked"
    acceptance_gap_ids = {gap["gap_id"] for gap in manifest["missing_acceptance_artifacts"]}
    assert "formal_gate_closure_checklist_open" in acceptance_gap_ids
    steps = {step["step_id"]: step for step in manifest["ordered_next_steps"]}
    assert steps["gate3_remote_training"]["status"] == "pending_execution"
    assert steps["claim_safety_final_gate"]["status"] == "blocked"
    assert "formal_gate_closure_checklist_open" in steps["claim_safety_final_gate"]["blocked_by"]


def test_formal_gate_gap_audit_rejects_closure_checklist_that_runs_or_claims(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_gap_audit")

    manifest = builder.build_manifest(
        builder.FormalGateGapAuditConfig(
            output_dir=tmp_path,
            contract_path=_contract(tmp_path),
            decision_record_path=_decision_record(tmp_path, pending=False),
            h01_manifest_path=_h01_manifest(tmp_path, ready=True),
            remote_packet_path=_remote_packet(tmp_path, ready=True, artifacts_present=True),
            h02_acceptance_path=_h02_acceptance(tmp_path, accepted=True),
            claim_safety_path=_claim_safety(tmp_path, allowed=True),
            readiness_path=_readiness(tmp_path, ready=True),
            remote_readiness_path=_remote_readiness(tmp_path, good=True),
            source_freshness_path=_source_freshness(tmp_path, clean=True),
            missing_artifacts_path=_missing_artifacts(tmp_path, complete=True),
            closure_checklist_path=_closure_checklist(tmp_path, complete=True, invalid=True),
            status_report_path=_status_report(tmp_path, ready=True),
            handoff_bundle_path=_handoff_bundle(tmp_path, ready=True, pending=False),
            remote_packet_safety_path=_remote_packet_safety(tmp_path, ready=True),
        )
    )

    acceptance_gap_ids = {gap["gap_id"] for gap in manifest["missing_acceptance_artifacts"]}
    assert "formal_closure_checklist_executes_commands" in acceptance_gap_ids
    assert "formal_closure_checklist_runs_training" in acceptance_gap_ids
    assert "formal_closure_checklist_runs_preflight" in acceptance_gap_ids
    assert "formal_closure_checklist_allows_local_training" in acceptance_gap_ids
    assert "formal_closure_checklist_allows_claim" in acceptance_gap_ids
    assert "formal_closure_checklist_safety_issues_open" in acceptance_gap_ids


def test_formal_gate_gap_audit_consumes_status_report(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_gap_audit")

    manifest = builder.build_manifest(
        builder.FormalGateGapAuditConfig(
            output_dir=tmp_path,
            contract_path=_contract(tmp_path),
            decision_record_path=_decision_record(tmp_path, pending=False),
            h01_manifest_path=_h01_manifest(tmp_path, ready=True),
            remote_packet_path=_remote_packet(tmp_path, ready=True, artifacts_present=True),
            h02_acceptance_path=_h02_acceptance(tmp_path, accepted=True),
            claim_safety_path=_claim_safety(tmp_path, allowed=True),
            readiness_path=_readiness(tmp_path, ready=True),
            remote_readiness_path=_remote_readiness(tmp_path, good=True),
            source_freshness_path=_source_freshness(tmp_path, clean=True),
            missing_artifacts_path=_missing_artifacts(tmp_path, complete=True),
            closure_checklist_path=_closure_checklist(tmp_path, complete=True),
            status_report_path=_status_report(tmp_path, ready=False),
            handoff_bundle_path=_handoff_bundle(tmp_path, ready=True, pending=False),
            remote_packet_safety_path=_remote_packet_safety(tmp_path, ready=True),
        )
    )

    assert manifest["status"] == "blocked_formal_gate_gaps_open"
    assert manifest["formal_gate_status_report"]["status"] == "formal_gate_status_blocked"
    assert manifest["current_gate_state"]["formal_gate_status_report_status"] == "formal_gate_status_blocked"
    acceptance_gap_ids = {gap["gap_id"] for gap in manifest["missing_acceptance_artifacts"]}
    assert "formal_gate_status_report_blocked" in acceptance_gap_ids
    steps = {step["step_id"]: step for step in manifest["ordered_next_steps"]}
    assert steps["claim_safety_final_gate"]["status"] == "blocked"
    assert "formal_gate_status_report_blocked" in steps["claim_safety_final_gate"]["blocked_by"]


def test_formal_gate_gap_audit_rejects_status_report_that_runs_or_claims(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_gap_audit")

    manifest = builder.build_manifest(
        builder.FormalGateGapAuditConfig(
            output_dir=tmp_path,
            contract_path=_contract(tmp_path),
            decision_record_path=_decision_record(tmp_path, pending=False),
            h01_manifest_path=_h01_manifest(tmp_path, ready=True),
            remote_packet_path=_remote_packet(tmp_path, ready=True, artifacts_present=True),
            h02_acceptance_path=_h02_acceptance(tmp_path, accepted=True),
            claim_safety_path=_claim_safety(tmp_path, allowed=True),
            readiness_path=_readiness(tmp_path, ready=True),
            remote_readiness_path=_remote_readiness(tmp_path, good=True),
            source_freshness_path=_source_freshness(tmp_path, clean=True),
            missing_artifacts_path=_missing_artifacts(tmp_path, complete=True),
            closure_checklist_path=_closure_checklist(tmp_path, complete=True),
            status_report_path=_status_report(tmp_path, ready=True, invalid=True),
            handoff_bundle_path=_handoff_bundle(tmp_path, ready=True, pending=False),
            remote_packet_safety_path=_remote_packet_safety(tmp_path, ready=True),
        )
    )

    acceptance_gap_ids = {gap["gap_id"] for gap in manifest["missing_acceptance_artifacts"]}
    assert "formal_status_report_executes_commands" in acceptance_gap_ids
    assert "formal_status_report_runs_training" in acceptance_gap_ids
    assert "formal_status_report_runs_preflight" in acceptance_gap_ids
    assert "formal_status_report_allows_local_training" in acceptance_gap_ids
    assert "formal_status_report_allows_claim" in acceptance_gap_ids
    assert "formal_status_report_allows_local_training_now" in acceptance_gap_ids
    assert "formal_status_report_safety_issues_open" in acceptance_gap_ids


def test_formal_gate_gap_audit_does_not_allow_local_training_even_when_remote_is_ready(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_gap_audit")

    manifest = builder.build_manifest(
        builder.FormalGateGapAuditConfig(
            output_dir=tmp_path,
            contract_path=_contract(tmp_path),
            decision_record_path=_decision_record(tmp_path, pending=False),
            h01_manifest_path=_h01_manifest(tmp_path, ready=True),
            remote_packet_path=_remote_packet(tmp_path, ready=True, artifacts_present=True),
            h02_acceptance_path=_h02_acceptance(tmp_path, accepted=True),
            claim_safety_path=_claim_safety(tmp_path, allowed=True),
            readiness_path=_readiness(tmp_path, ready=True),
            remote_readiness_path=_remote_readiness(tmp_path, good=True),
            source_freshness_path=_source_freshness(tmp_path, clean=True),
            missing_artifacts_path=_missing_artifacts(tmp_path, complete=True),
            closure_checklist_path=_closure_checklist(tmp_path, complete=True),
            status_report_path=_status_report(tmp_path, ready=True),
            handoff_bundle_path=_handoff_bundle(tmp_path, ready=True, pending=False),
            remote_packet_safety_path=_remote_packet_safety(tmp_path, ready=True),
        )
    )

    assert manifest["local_training_allowed"] is False
    assert "No PPO/RL-RS formal training is allowed on the local Mac." in manifest["claim_boundaries"]


def _contract(tmp_path):
    path = tmp_path / "contract.md"
    path.write_text(
        "\n".join(
            [
                "---",
                "status: approved",
                "version: v1",
                "approved_by: Dr Sun",
                "approved_date: 2026-07-02",
                "---",
                "",
                "# Contract",
            ]
        ),
        encoding="utf-8",
    )
    return path


def _decision_record(tmp_path, *, pending):
    path = tmp_path / f"decision_{pending}.json"
    path.write_text(
        json.dumps(
            {
                "status": "pending_human_decision" if pending else "approved",
                "effective_warm_start_decision": "pending" if pending else "approved_obstacle_summary",
                "remote_training_allowed": not pending,
                "local_training_allowed": False,
                "blockers": ["requires_dr_sun_approval"] if pending else [],
            }
        ),
        encoding="utf-8",
    )
    return path


def _h01_manifest(tmp_path, *, ready):
    path = tmp_path / f"h01_{ready}.json"
    path.write_text(
        json.dumps(
            {
                "status": "ready_for_formal_run" if ready else "blocked_pending_decisions",
                "blockers": [] if ready else ["f02_6_warm_start_decision_pending", "missing_module2_rl_rs_checkpoint"],
                "run_command": {
                    "formal_main_evaluation": "python -m forest_n3p.scripts.run_main_evaluation --methods ha_rl_rs_ppo"
                    if ready
                    else None
                },
            }
        ),
        encoding="utf-8",
    )
    return path


def _remote_packet(tmp_path, *, ready, artifacts_present):
    artifact_dir = tmp_path / f"remote_artifacts_{ready}_{artifacts_present}"
    expected = [
        artifact_dir / "train" / "final_model.zip",
        artifact_dir / "train" / "summary.json",
        artifact_dir / "train" / "training_manifest.json",
        artifact_dir / "eval" / "gate3_eval_episodes.csv",
        artifact_dir / "eval" / "gate3_summary.json",
        artifact_dir / "gate3_trial_manifest.json",
        artifact_dir / "gate3_formal_audit.json",
    ]
    if artifacts_present:
        for path in expected:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("ok\n", encoding="utf-8")
    path = tmp_path / f"remote_packet_{ready}_{artifacts_present}.json"
    path.write_text(
        json.dumps(
            {
                "status": "ready_for_gpu3070ti_remote_training" if ready else "blocked_until_f02_6_decision",
                "ready_to_run_remote_training": ready,
                "local_training_allowed": False,
                "blockers": [] if ready else ["requires_dr_sun_approval", "f02_6_warm_start_decision_pending"],
                "execution_environment": {
                    "gpu_alias": "gpu3070ti-relay",
                    "training_host_required": "gpu3070ti-relay",
                },
                "post_run_pullback": {
                    "required_before_local_claim": True,
                    "expected_artifacts": [str(item) for item in expected],
                },
            }
        ),
        encoding="utf-8",
    )
    return path


def _h02_acceptance(tmp_path, *, accepted):
    path = tmp_path / f"h02_{accepted}.json"
    path.write_text(
        json.dumps(
            {
                "status": "formal_output_accepted" if accepted else "blocked_formal_output_acceptance",
                "formal_output_accepted": accepted,
                "paper_result_input_allowed": accepted,
                "formal_checks": {
                    "h02_verdict_status": "formal_accepted" if accepted else "candidate_or_smoke",
                    "h02_verdict_formal_acceptance": accepted,
                    "gate3_audit_path": str(tmp_path / "gate3_formal_audit.json"),
                    "gate3_formal_audit_passed": accepted,
                    "scale_checks": {
                        "queries_per_bucket": {"observed": 100, "required": 100, "satisfied": accepted},
                        "seed_count": {"observed": 5, "required": 5, "satisfied": accepted},
                        "queries_per_map": {"observed": 5, "required": 5, "satisfied": accepted},
                    },
                },
                "method_checks": {
                    "ppo_row_count": 2 if accepted else 0,
                    "has_ppo_result_rows": accepted,
                    "ppo_checkpoint_hashes": ["abc123"] if accepted else [],
                    "ppo_rows_have_checkpoint_hash": accepted,
                },
            }
        ),
        encoding="utf-8",
    )
    return path


def _claim_safety(tmp_path, *, allowed):
    path = tmp_path / f"claim_safety_{allowed}.json"
    path.write_text(
        json.dumps(
            {
                "status": "formal_performance_claims_allowed" if allowed else "blocked_formal_performance_claims",
                "formal_performance_claim_allowed": allowed,
            }
        ),
        encoding="utf-8",
    )
    return path


def _readiness(tmp_path, *, ready):
    path = tmp_path / f"readiness_{ready}.json"
    path.write_text(
        json.dumps(
            {
                "status": "formal_results_ready" if ready else "partial_methods_ready_results_blocked",
                "formal_results_ready": ready,
            }
        ),
        encoding="utf-8",
    )
    return path


def _remote_readiness(tmp_path, *, good):
    path = tmp_path / f"remote_readiness_{good}.json"
    match = bool(good)
    path.write_text(
        json.dumps(
            {
                "status": "remote_readiness_refreshed_f02_6_still_blocked",
                "runs_training": False,
                "runs_remote_preflight": False,
                "local_training_allowed": False,
                "formal_claim_allowed": False,
                "remote_training_resource": "gpu3070ti-relay",
                "critical_inputs": {
                    "oracle_connector_results": {"local_remote_match": match},
                    "obstacle_summary_bc_checkpoint": {"local_remote_match": match},
                },
            }
        ),
        encoding="utf-8",
    )
    return path


def _source_freshness(tmp_path, *, clean, invalid=False):
    path = tmp_path / f"source_freshness_{clean}_{invalid}.json"
    targets = [] if clean else [
        {
            "artifact_id": "f02_6_decision_record",
            "path": str(tmp_path / "f02_6_decision_record.json"),
            "freshness_state": "historical_dirty",
            "required_before": "approved_remote_preflight",
        },
        {
            "artifact_id": "h02_formal_acceptance",
            "path": str(tmp_path / "h02_formal_acceptance.json"),
            "freshness_state": "historical_dirty",
            "required_before": "formal_h01_h02",
        },
    ]
    path.write_text(
        json.dumps(
            {
                "status": "source_freshness_clean_current" if clean else "source_freshness_risks_recorded_gate_still_blocked",
                "runs_training": bool(invalid),
                "runs_remote_preflight": bool(invalid),
                "local_training_allowed": bool(invalid),
                "formal_claim_allowed": bool(invalid),
                "regeneration_required_before_remote_formal_execution": not clean,
                "risk_counts": {"current_clean": 8} if clean else {"historical_dirty": 2},
                "ordered_regeneration_targets": targets,
            }
        ),
        encoding="utf-8",
    )
    return path


def _missing_artifacts(tmp_path, *, complete, invalid=False):
    path = tmp_path / f"missing_artifacts_{complete}_{invalid}.json"
    missing_counts = {} if complete else {"training": 3, "evaluation": 2, "acceptance": 3}
    path.write_text(
        json.dumps(
            {
                "status": "formal_gate_artifacts_complete" if complete else "formal_gate_missing_artifacts_open",
                "executes_commands": bool(invalid),
                "runs_training": bool(invalid),
                "runs_remote_preflight": bool(invalid),
                "local_training_allowed": bool(invalid),
                "formal_claim_allowed": bool(invalid),
                "all_required_evidence_present": complete,
                "audit_issue_count": 1 if invalid else 0,
                "missing_counts_by_category": missing_counts,
            }
        ),
        encoding="utf-8",
    )
    return path


def _closure_checklist(tmp_path, *, complete, invalid=False):
    path = tmp_path / f"closure_checklist_{complete}_{invalid}.json"
    path.write_text(
        json.dumps(
            {
                "status": "formal_gate_closure_ready_for_result_audit" if complete else "formal_gate_closure_blocked",
                "executes_commands": bool(invalid),
                "runs_training": bool(invalid),
                "runs_remote_preflight": bool(invalid),
                "local_training_allowed": bool(invalid),
                "formal_claim_allowed": bool(invalid),
                "closure_item_count": 8,
                "open_item_count": 0 if complete else 8,
                "input_safety_issue_count": 1 if invalid else 0,
            }
        ),
        encoding="utf-8",
    )
    return path


def _status_report(tmp_path, *, ready, invalid=False):
    path = tmp_path / f"status_report_{ready}_{invalid}.json"
    path.write_text(
        json.dumps(
            {
                "status": "formal_gate_status_ready_for_claim_audit" if ready else "formal_gate_status_blocked",
                "executes_commands": bool(invalid),
                "runs_training": bool(invalid),
                "runs_remote_preflight": bool(invalid),
                "local_training_allowed": bool(invalid),
                "formal_claim_allowed": bool(invalid),
                "input_safety_issue_count": 1 if invalid else 0,
                "permissions_now": {
                    "local_training_allowed_now": bool(invalid),
                    "remote_preflight_allowed_now": False,
                    "remote_training_allowed_now": False,
                    "formal_h01_evaluation_allowed_now": bool(ready),
                    "formal_h02_acceptance_allowed_now": bool(ready),
                    "formal_claim_allowed_now": bool(ready),
                },
                "next_blocked_lane": None if ready else {"lane_id": "decision"},
            }
        ),
        encoding="utf-8",
    )
    return path
