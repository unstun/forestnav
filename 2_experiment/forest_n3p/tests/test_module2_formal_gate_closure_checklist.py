import json
from importlib import import_module
from pathlib import Path


def test_formal_gate_closure_checklist_blocks_pending_chain(tmp_path):
    try:
        builder = import_module("forest_n3p.scripts.build_module2_formal_gate_closure_checklist")
    except ModuleNotFoundError as exc:
        raise AssertionError(f"missing formal gate closure checklist builder: {exc}") from exc

    manifest = builder.build_manifest(_config(tmp_path, complete=False))

    assert manifest["schema_version"] == 1
    assert manifest["artifact_name"] == "module2_formal_gate_closure_checklist"
    assert manifest["status"] == "formal_gate_closure_blocked"
    assert manifest["not_paper_result_material"] is True
    assert manifest["executes_commands"] is False
    assert manifest["runs_training"] is False
    assert manifest["runs_remote_preflight"] is False
    assert manifest["local_training_allowed"] is False
    assert manifest["formal_claim_allowed"] is False
    assert manifest["open_item_count"] == 8
    assert manifest["remaining_deliverables_gap_summary"]["total_missing_deliverables"] == 10
    assert manifest["remaining_deliverables_gap_summary"]["open_category_count"] == 4
    assert manifest["remaining_deliverables_gap_summary"]["categories"]["training"]["missing_count"] == 3
    assert manifest["post_plan_remaining_deliverables_gap_summary"]["total_missing_deliverables"] == 10
    assert len(manifest["training_artifacts_required"]) == 3
    assert len(manifest["evaluation_artifacts_required"]) == 2
    assert len(manifest["acceptance_artifacts_required"]) == 3
    remote_stages = manifest["post_plan_remote_stage_summary"]
    assert remote_stages["approved_remote_preflight"]["allowed_now"] is False
    assert remote_stages["approved_remote_preflight"]["runs_remote_preflight"] is True
    assert remote_stages["approved_remote_preflight"]["host"] == "gpu3070ti-relay"
    assert "requires_dr_sun_approval" in remote_stages["approved_remote_preflight"]["blocked_by"]
    assert remote_stages["gate3_remote_training"]["allowed_now"] is False
    assert remote_stages["gate3_remote_training"]["runs_training"] is True
    assert "remote_packet_not_ready" in remote_stages["gate3_remote_training"]["blocked_by"]

    checklist = {item["checklist_id"]: item for item in manifest["closure_checklist"]}
    assert checklist["F02.6_decision"]["status"] == "blocked"
    assert "f02_6_decision_not_approved" in checklist["F02.6_decision"]["blocked_by"]
    assert checklist["gate3_remote_training_outputs"]["runs_training"] is True
    assert checklist["gate3_remote_training_outputs"]["host"] == "gpu3070ti-relay"
    assert checklist["claim_gate_regeneration"]["status"] == "blocked"


def test_formal_gate_closure_checklist_accepts_synthetic_complete_chain(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_closure_checklist")

    manifest = builder.build_manifest(_config(tmp_path, complete=True))

    assert manifest["status"] == "formal_gate_closure_ready_for_result_audit"
    assert manifest["open_item_count"] == 0
    assert manifest["input_safety_issue_count"] == 0
    assert manifest["remaining_deliverables_gap_summary"]["total_missing_deliverables"] == 0
    assert manifest["remaining_deliverables_gap_summary"]["open_category_count"] == 0
    assert all(item["complete"] for item in manifest["closure_checklist"])
    assert all(stage["allowed_now"] is True for stage in manifest["post_plan_remote_stage_summary"].values())
    assert all(stage["blocked_by"] == [] for stage in manifest["post_plan_remote_stage_summary"].values())
    assert manifest["formal_claim_allowed"] is False


def test_formal_gate_closure_checklist_catches_read_only_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_closure_checklist")

    manifest = builder.build_manifest(_config(tmp_path, complete=False, drift=True))

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert manifest["status"] == "formal_gate_closure_blocked"
    assert "missing_artifacts_runs_training" in issue_ids
    assert "post_plan_runs_remote_preflight" in issue_ids
    assert "source_freshness_allows_local_training" in issue_ids


def test_formal_gate_closure_checklist_requires_remote_stage_blockers(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_closure_checklist")
    config = _config(tmp_path, complete=False)
    post_plan = json.loads(config.post_plan_path.read_text(encoding="utf-8"))
    for stage in post_plan["ordered_stages"]:
        if stage["stage_id"] in {"approved_remote_preflight", "gate3_remote_training"}:
            stage["blocked_by"] = []
    config.post_plan_path.write_text(json.dumps(post_plan), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert manifest["status"] == "formal_gate_closure_blocked"
    assert "post_plan_approved_remote_preflight_missing_blocked_by" in issue_ids
    assert "post_plan_gate3_remote_training_missing_blocked_by" in issue_ids


def test_formal_gate_closure_checklist_rejects_gap_summary_drift(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_closure_checklist")
    config = _config(tmp_path, complete=False)
    post_plan = json.loads(config.post_plan_path.read_text(encoding="utf-8"))
    post_plan["remaining_deliverables_gap_summary"]["categories"]["training"]["missing_count"] = 2
    config.post_plan_path.write_text(json.dumps(post_plan), encoding="utf-8")

    manifest = builder.build_manifest(config)

    issue_ids = {issue["issue_id"] for issue in manifest["input_safety_issues"]}
    assert manifest["status"] == "formal_gate_closure_blocked"
    assert "post_plan_remaining_deliverables_gap_summary_mismatch" in issue_ids


def test_formal_gate_closure_checklist_cli_writes_json_and_markdown(tmp_path):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_closure_checklist")
    config = _config(tmp_path, complete=False)
    manifest_path = tmp_path / "closure.json"
    markdown_path = tmp_path / "closure.md"

    rc = builder.main(
        [
            "--output-dir",
            str(tmp_path),
            "--manifest-out",
            str(manifest_path),
            "--markdown-out",
            str(markdown_path),
            "--missing-artifacts",
            str(config.missing_artifacts_path),
            "--formal-gate",
            str(config.formal_gate_path),
            "--post-plan",
            str(config.post_plan_path),
            "--source-freshness-audit",
            str(config.source_freshness_path),
            "--remaining-deliverables",
            str(config.remaining_deliverables_path),
        ]
    )

    assert rc == 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    assert manifest["status"] == "formal_gate_closure_blocked"
    assert "Module2 Formal Gate Closure Checklist" in markdown
    assert "gate3_remote_training_outputs" in markdown
    assert "Post-Plan Remote Stages" in markdown
    assert "Remaining Deliverables Gap Summary" in markdown
    assert "does not execute commands" in markdown


def _config(tmp_path, *, complete, drift=False):
    builder = import_module("forest_n3p.scripts.build_module2_formal_gate_closure_checklist")
    missing_artifacts = _missing_artifacts(tmp_path, complete=complete, drift=drift)
    formal_gate = _formal_gate(complete=complete)
    post_plan = _post_plan(complete=complete, drift=drift)
    source_freshness = _source_freshness(complete=complete, drift=drift)
    remaining_deliverables = _remaining_deliverables(complete=complete)
    return builder.FormalGateClosureChecklistConfig(
        output_dir=tmp_path,
        missing_artifacts_path=_json(tmp_path, "missing_artifacts.json", missing_artifacts),
        formal_gate_path=_json(tmp_path, "formal_gate.json", formal_gate),
        post_plan_path=_json(tmp_path, "post_plan.json", post_plan),
        source_freshness_path=_json(tmp_path, "source_freshness.json", source_freshness),
        remaining_deliverables_path=_json(tmp_path, "remaining_deliverables.json", remaining_deliverables),
    )


def _missing_artifacts(tmp_path, *, complete, drift=False):
    trial = tmp_path / "gate3_obstacle_summary_warm_approved_v1"
    groups = [
        _group("f02_6_decision_record", "decision", ["f02_6_decision_record"], complete=complete),
        _group("source_fresh_regeneration_targets", "regeneration", ["formal_gate_gap_audit"], complete=complete),
        _group("post_f02_6_ordered_stages", "gate_sequence", ["gate3_remote_training"], complete=complete),
        _path_group(
            "remote_training_outputs",
            "training",
            [
                trial / "train/final_model.zip",
                trial / "train/summary.json",
                trial / "train/training_manifest.json",
            ],
            complete=complete,
        ),
        _path_group(
            "gate3_evaluation_outputs",
            "evaluation",
            [
                trial / "eval/gate3_eval_episodes.csv",
                trial / "eval/gate3_summary.json",
            ],
            complete=complete,
        ),
        _path_group(
            "gate3_acceptance_pullback",
            "acceptance",
            [
                trial / "gate3_trial_manifest.json",
                trial / "gate3_formal_audit.json",
                trial / "train/final_model.zip.sha256",
            ],
            complete=complete,
        ),
        _group("h01_h02_formal_evaluation_acceptance", "evaluation_acceptance", ["h02_formal_output_acceptance"], complete=complete),
        _group("claim_gate_regeneration", "claim_gate", ["claim_safety"], complete=complete),
    ]
    counts = {}
    for group in groups:
        counts[group["category"]] = sum(1 for item in group["items"] if item["missing"])
    payload = {
        "status": "formal_gate_artifacts_complete" if complete else "formal_gate_missing_artifacts_open",
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "all_required_evidence_present": complete,
        "missing_counts_by_category": counts,
        "missing_evidence_groups": groups,
    }
    if drift:
        payload["runs_training"] = True
    return payload


def _group(group_id, category, artifact_ids, *, complete):
    return {
        "group_id": group_id,
        "category": category,
        "complete": complete,
        "blocked_by": [] if complete else artifact_ids,
        "items": [
            {
                "artifact_id": artifact_id,
                "path": f"0_trials/module2/{artifact_id}.json",
                "exists": True,
                "state": "present" if complete else "blocked",
                "missing": not complete,
                "reason": "" if complete else "required before formal closure",
            }
            for artifact_id in artifact_ids
        ],
    }


def _path_group(group_id, category, paths, *, complete):
    return {
        "group_id": group_id,
        "category": category,
        "complete": complete,
        "blocked_by": [] if complete else [path.name.replace(".", "_") for path in paths],
        "items": [
            {
                "artifact_id": path.name.replace(".", "_"),
                "path": str(path),
                "exists": complete,
                "state": "present" if complete else "missing",
                "missing": not complete,
                "reason": "" if complete else f"required {category} artifact",
            }
            for path in paths
        ],
    }


def _formal_gate(*, complete):
    return {
        "status": "formal_gate_ready_for_result_audit" if complete else "blocked_formal_gate_gaps_open",
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "ordered_next_steps": [
            {"step_id": "F02.6", "status": "ready" if complete else "blocked", "blocked_by": [] if complete else ["f02_6_decision_not_approved"]},
            {"step_id": "gate3_remote_training", "status": "ready" if complete else "blocked", "blocked_by": [] if complete else ["remote_training_packet_not_ready"]},
            {"step_id": "claim_safety_final_gate", "status": "ready" if complete else "blocked", "blocked_by": [] if complete else ["h02_formal_acceptance_not_ready"]},
        ],
    }


def _post_plan(*, complete, drift=False):
    stage_blockers = [] if complete else ["requires_dr_sun_approval"]
    training_blockers = [] if complete else ["requires_dr_sun_approval", "remote_packet_not_ready"]
    payload = {
        "status": "formal_chain_complete" if complete else "blocked_until_f02_6_decision",
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "blocking_summary": {
            "blocked_stage_ids": [] if complete else ["gate3_remote_training"],
        },
        "remaining_deliverables_gap_summary": _gap_summary(open_gaps=not complete),
        "ordered_stages": [
            {"stage_id": "f02_6_decision_record", "status": "complete" if complete else "ready", "blocked_by": []},
            {
                "stage_id": "approved_remote_preflight",
                "status": "complete" if complete else "blocked",
                "allowed_now": complete,
                "blocked_by": stage_blockers,
                "runs_training": False,
                "runs_remote_preflight": True,
                "host": "gpu3070ti-relay",
            },
            {
                "stage_id": "gate3_remote_training",
                "status": "complete" if complete else "blocked",
                "allowed_now": complete,
                "blocked_by": training_blockers,
                "runs_training": True,
                "runs_remote_preflight": False,
                "host": "gpu3070ti-relay",
            },
            {
                "stage_id": "gate3_remote_audit_pullback",
                "status": "complete" if complete else "blocked",
                "allowed_now": complete,
                "blocked_by": training_blockers,
                "runs_training": False,
                "runs_remote_preflight": False,
                "host": "gpu3070ti-relay",
            },
            {"stage_id": "regenerate_claim_gate_artifacts", "status": "complete" if complete else "blocked", "blocked_by": [] if complete else ["h02_formal_acceptance_not_ready"]},
        ],
    }
    if drift:
        payload["runs_remote_preflight"] = True
    return payload


def _remaining_deliverables(*, complete):
    return {
        "status": "formal_gate_deliverables_complete" if complete else "formal_gate_deliverables_blocked",
        "executes_commands": False,
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "deliverable_gap_summary": _gap_summary(open_gaps=not complete),
    }


def _gap_summary(*, open_gaps):
    return {
        "summary_id": "module2_formal_gate_missing_training_eval_acceptance_summary",
        "execution_boundary": "read_only_no_execution",
        "not_paper_result_material": True,
        "total_missing_deliverables": 10 if open_gaps else 0,
        "open_category_count": 4 if open_gaps else 0,
        "category_order": ["training", "evaluation", "acceptance", "formal_acceptance"],
        "categories": {
            "training": _gap_category("training", 3 if open_gaps else 0, "gate3_remote_training", open_gaps=open_gaps),
            "evaluation": _gap_category("evaluation", 2 if open_gaps else 0, "gate3_remote_audit_pullback", open_gaps=open_gaps),
            "acceptance": _gap_category("acceptance", 3 if open_gaps else 0, "gate3_remote_audit_pullback", open_gaps=open_gaps),
            "formal_acceptance": _gap_category(
                "formal_acceptance",
                2 if open_gaps else 0,
                "regenerate_h01_h02_formal_artifacts",
                open_gaps=open_gaps,
            ),
        },
    }


def _gap_category(category, missing_count, stage_id, *, open_gaps):
    return {
        "missing_count": missing_count,
        "responsible_stage_id": stage_id,
        "responsible_stage_allowed_now": not open_gaps,
        "missing_artifact_matrix_ids": [f"{category}:artifact_{index}" for index in range(missing_count)],
    }


def _source_freshness(*, complete, drift=False):
    payload = {
        "status": "source_freshness_clean_current" if complete else "source_freshness_risks_recorded_gate_still_blocked",
        "runs_training": False,
        "runs_remote_preflight": False,
        "local_training_allowed": False,
        "formal_claim_allowed": False,
        "ordered_regeneration_targets": [] if complete else [{"artifact_id": "formal_gate_gap_audit"}],
    }
    if drift:
        payload["local_training_allowed"] = True
    return payload


def _json(tmp_path, name, payload):
    path = tmp_path / name
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path
