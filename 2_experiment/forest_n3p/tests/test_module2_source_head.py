from importlib import import_module


def test_source_head_ignores_tracked_gate_artifact_dirty_paths():
    helper = import_module("forest_n3p.scripts._module2_source_head")

    value = helper.source_head_from_dirty_paths(
        head="a" * 40,
        dirty_paths=[
            "0_trials/module2_formal_gate_status_report/formal_gate_status_report.json",
            "0_trials/module2_formal_gate_status_report/formal_gate_status_report.md",
            "0_trials/module2_source_freshness_audit/source_freshness_audit.json",
        ],
        ignored_paths=helper.module2_gate_artifact_paths(),
    )

    assert value == "a" * 40


def test_source_head_marks_non_artifact_dirty_paths():
    helper = import_module("forest_n3p.scripts._module2_source_head")

    value = helper.source_head_from_dirty_paths(
        head="b" * 40,
        dirty_paths=[
            "0_trials/module2_formal_gate_status_report/formal_gate_status_report.json",
            "2_experiment/forest_n3p/scripts/build_module2_formal_gate_status_report.py",
        ],
        ignored_paths=helper.module2_gate_artifact_paths(),
    )

    assert value == f"{'b' * 40}+dirty"


def test_source_head_can_ignore_builder_specific_output_paths():
    helper = import_module("forest_n3p.scripts._module2_source_head")

    value = helper.source_head_from_dirty_paths(
        head="c" * 40,
        dirty_paths=["custom/out.json", "custom/out.md"],
        ignored_paths=helper.module2_gate_artifact_paths(["custom/out.json"]),
    )

    assert value == "c" * 40
