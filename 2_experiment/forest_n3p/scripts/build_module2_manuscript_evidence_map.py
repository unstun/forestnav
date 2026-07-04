from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence


DEFAULT_OUTPUT_DIR = Path("3_paper/module2_evidence_map")
DEFAULT_MAIN_TEX = Path("3_paper/main.tex")
DEFAULT_CLAIM_AUDIT = Path("3_paper/module2_claim_audit/module2_manuscript_claim_audit.json")
DEFAULT_SECTION_SEED = Path("3_paper/module2_section_seed/module2_paper_section_seed.json")
DEFAULT_PAPER_READINESS = Path("0_trials/module2_paper_readiness/module2_paper_readiness.json")
DEFAULT_CLAIM_SAFETY = Path("0_trials/module2_claim_safety/module2_claim_safety.json")
DEFAULT_METHOD_ALGORITHMS = Path("0_trials/module2_method_algorithms/module2_method_algorithms.json")
DEFAULT_SYSTEM_DIAGRAM = Path("0_trials/module2_system_diagram/module2_system_diagram.json")
DEFAULT_GATE3_AUDIT = Path("0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/gate3_formal_audit.json")
DEFAULT_F02_6_DECISION_RECORD = Path("0_trials/module2_f02_6_decision_record/f02_6_decision_record.json")
DEFAULT_REMOTE_EXECUTION_PACKET = Path("0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json")


@dataclass(frozen=True)
class ManuscriptEvidenceMapConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    main_tex_path: Path = DEFAULT_MAIN_TEX
    claim_audit_path: Path = DEFAULT_CLAIM_AUDIT
    section_seed_path: Path = DEFAULT_SECTION_SEED
    paper_readiness_path: Path = DEFAULT_PAPER_READINESS
    claim_safety_path: Path = DEFAULT_CLAIM_SAFETY
    method_algorithms_path: Path = DEFAULT_METHOD_ALGORITHMS
    system_diagram_path: Path = DEFAULT_SYSTEM_DIAGRAM
    gate3_audit_path: Path = DEFAULT_GATE3_AUDIT
    f02_6_decision_record_path: Path = DEFAULT_F02_6_DECISION_RECORD
    remote_execution_packet_path: Path = DEFAULT_REMOTE_EXECUTION_PACKET


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = ManuscriptEvidenceMapConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        main_tex_path=args.main_tex,
        claim_audit_path=args.claim_audit,
        section_seed_path=args.section_seed,
        paper_readiness_path=args.paper_readiness,
        claim_safety_path=args.claim_safety,
        method_algorithms_path=args.method_algorithms,
        system_diagram_path=args.system_diagram,
        gate3_audit_path=args.gate3_audit,
        f02_6_decision_record_path=args.f02_6_decision_record,
        remote_execution_packet_path=args.remote_execution_packet,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "module2_manuscript_evidence_map.json"
    markdown_out = config.markdown_out or output_dir / "module2_manuscript_evidence_map.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: ManuscriptEvidenceMapConfig) -> dict[str, Any]:
    claim_audit = _read_json(config.claim_audit_path)
    section_seed = _read_json(config.section_seed_path)
    readiness = _read_json(config.paper_readiness_path)
    claim_safety = _read_json(config.claim_safety_path)
    method_algorithms = _read_json(config.method_algorithms_path)
    system_diagram = _read_json(config.system_diagram_path)
    gate3_audit = _read_json(config.gate3_audit_path)
    decision_record = _read_json(config.f02_6_decision_record_path)
    remote_packet = _read_json(config.remote_execution_packet_path)
    expanded = _expand_latex(config.main_tex_path)
    stripped_text = _strip_latex_comments(expanded["text"])
    source_files = [str(item) for item in expanded["input_files"]]

    inputs = {
        "main_tex": str(config.main_tex_path),
        "claim_audit": str(config.claim_audit_path),
        "section_seed": str(config.section_seed_path),
        "paper_readiness": str(config.paper_readiness_path),
        "claim_safety": str(config.claim_safety_path),
        "method_algorithms": str(config.method_algorithms_path),
        "system_diagram": str(config.system_diagram_path),
        "gate3_audit": str(config.gate3_audit_path),
        "f02_6_decision_record": str(config.f02_6_decision_record_path),
        "remote_execution_packet": str(config.remote_execution_packet_path),
    }
    section_by_id = {str(item.get("section_id")): item for item in readiness.get("section_readiness", []) if isinstance(item, dict)}
    seed_section_by_id = {str(item.get("section_id")): item for item in section_seed.get("sections", []) if isinstance(item, dict)}
    allowed_claim_ids = [str(item.get("claim_id")) for item in claim_safety.get("allowed_claims", []) if isinstance(item, dict) and item.get("claim_id")]

    claim_units = [
        _method_claim_unit(
            text=stripped_text,
            raw_text=expanded["text"],
            claim_safety=claim_safety,
            method_algorithms=method_algorithms,
            system_diagram=system_diagram,
            readiness=section_by_id.get("method_algorithm", {}),
            seed_section=seed_section_by_id.get("methods_rl_rs_operator", {}),
            inputs=inputs,
            source_files=source_files,
        ),
        _no_warm_claim_unit(
            text=stripped_text,
            raw_text=expanded["text"],
            claim_safety=claim_safety,
            gate3_audit=gate3_audit,
            readiness=section_by_id.get("no_warm_failure_claim", {}),
            seed_section=seed_section_by_id.get("no_warm_gate3_failure_note", {}),
            inputs=inputs,
            source_files=source_files,
        ),
        _formal_results_blocked_unit(
            text=stripped_text,
            raw_text=expanded["text"],
            claim_audit=claim_audit,
            claim_safety=claim_safety,
            readiness=section_by_id.get("formal_results", {}),
            seed_section=seed_section_by_id.get("formal_results", {}),
            inputs=inputs,
            source_files=source_files,
        ),
        _warm_start_blocked_unit(
            text=stripped_text,
            raw_text=expanded["text"],
            readiness=section_by_id.get("warm_start_effect", {}),
            seed_section=seed_section_by_id.get("warm_start_effect", {}),
            decision_record=decision_record,
            remote_packet=remote_packet,
            inputs=inputs,
            source_files=source_files,
        ),
    ]
    blocking_reasons = _blocking_reasons(claim_audit=claim_audit, claim_units=claim_units)
    status = "module2_manuscript_evidence_mapped" if not blocking_reasons else "blocked_by_missing_manuscript_evidence"
    return {
        "schema_version": 1,
        "artifact_name": "module2_manuscript_evidence_map",
        "status": status,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "local_training_allowed": False,
        "remote_training_resource": "gpu3070ti-relay",
        "inputs": inputs,
        "expanded_manuscript": {
            "sha256": hashlib.sha256(expanded["text"].encode("utf-8")).hexdigest(),
            "expanded_input_files": expanded["input_files"],
            "comment_stripped_char_count": len(stripped_text),
        },
        "upstream_status": {
            "claim_audit_status": claim_audit.get("status"),
            "claim_audit_prohibited_status": claim_audit.get("prohibited_claim_audit", {}).get("status"),
            "paper_readiness_status": readiness.get("status"),
            "section_seed_status": section_seed.get("status"),
            "claim_safety_status": claim_safety.get("status"),
            "formal_performance_claim_allowed": claim_safety.get("formal_performance_claim_allowed"),
            "allowed_claim_ids": allowed_claim_ids,
            "f02_6_decision_status": decision_record.get("status"),
            "remote_execution_packet_status": remote_packet.get("status"),
            "remote_execution_ready": remote_packet.get("ready_to_run_remote_training"),
        },
        "claim_units": claim_units,
        "missing_evidence": [
            {
                "unit_id": unit["unit_id"],
                "mapping_blockers": list(unit["mapping_blockers"]),
            }
            for unit in claim_units
            if unit["mapping_blockers"]
        ],
        "blocking_reasons": blocking_reasons,
        "writing_boundaries": [
            "Use this artifact as a claim-to-evidence map, not as a formal result.",
            "The method/system/no-warm units are mapped because their manuscript cues and upstream evidence are present.",
            "Formal result and warm-start units are mapped only as blocked placeholders; they are not paper claims yet.",
            "No local training is allowed; formal PPO checkpoint production remains gated on F02.6 and gpu3070ti-relay.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Map Module2 manuscript claim units to audited evidence without running training.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--main-tex", type=Path, default=DEFAULT_MAIN_TEX)
    parser.add_argument("--claim-audit", type=Path, default=DEFAULT_CLAIM_AUDIT)
    parser.add_argument("--section-seed", type=Path, default=DEFAULT_SECTION_SEED)
    parser.add_argument("--paper-readiness", type=Path, default=DEFAULT_PAPER_READINESS)
    parser.add_argument("--claim-safety", type=Path, default=DEFAULT_CLAIM_SAFETY)
    parser.add_argument("--method-algorithms", type=Path, default=DEFAULT_METHOD_ALGORITHMS)
    parser.add_argument("--system-diagram", type=Path, default=DEFAULT_SYSTEM_DIAGRAM)
    parser.add_argument("--gate3-audit", type=Path, default=DEFAULT_GATE3_AUDIT)
    parser.add_argument("--f02-6-decision-record", type=Path, default=DEFAULT_F02_6_DECISION_RECORD)
    parser.add_argument("--remote-execution-packet", type=Path, default=DEFAULT_REMOTE_EXECUTION_PACKET)
    return parser.parse_args(list(argv) if argv is not None else None)


def _method_claim_unit(
    *,
    text: str,
    raw_text: str,
    claim_safety: dict[str, Any],
    method_algorithms: dict[str, Any],
    system_diagram: dict[str, Any],
    readiness: dict[str, Any],
    seed_section: dict[str, Any],
    inputs: dict[str, str],
    source_files: Sequence[str],
) -> dict[str, Any]:
    cues = [
        "learned analytic-expansion operator inside",
        "not a standalone global planner",
        "terminal RS",
    ]
    claim = _find_claim(claim_safety.get("allowed_claims", []), "method_is_ha_star_analytic_operator")
    mapping_blockers = _cue_blockers(text, cues, unit_id="method_is_ha_star_analytic_operator")
    if claim is None:
        mapping_blockers.append("method_is_ha_star_analytic_operator:allowed_claim_missing")
    if method_algorithms.get("status") != "code_anchored":
        mapping_blockers.append("method_is_ha_star_analytic_operator:method_algorithms_not_code_anchored")
    if system_diagram.get("status") != "code_anchored_drawio":
        mapping_blockers.append("method_is_ha_star_analytic_operator:system_diagram_not_code_anchored")
    if readiness.get("status") != "ready_to_write":
        mapping_blockers.append("method_is_ha_star_analytic_operator:readiness_not_ready_to_write")
    if seed_section.get("status") != "draft_ready":
        mapping_blockers.append("method_is_ha_star_analytic_operator:section_seed_not_draft_ready")
    return {
        "unit_id": "method_is_ha_star_analytic_operator",
        "paper_scope": "methods",
        "claim_status": "allowed_method_structure",
        "manuscript_cues": _cue_results(raw_text=raw_text, text=text, cues=cues, source_files=source_files),
        "evidence_state": "mapped" if not mapping_blockers else "missing_mapping_evidence",
        "claim_text": None if claim is None else claim.get("claim_text"),
        "required_qualifier": None if claim is None else claim.get("required_qualifier"),
        "evidence": [
            _evidence(inputs["claim_safety"], claim_safety, {"allowed_claim_present": claim is not None}),
            _evidence(inputs["method_algorithms"], method_algorithms, {"status_required": "code_anchored"}),
            _evidence(inputs["system_diagram"], system_diagram, {"status_required": "code_anchored_drawio"}),
            _evidence(inputs["paper_readiness"], readiness, {"section_id": "method_algorithm"}),
            _evidence(inputs["section_seed"], seed_section, {"section_id": "methods_rl_rs_operator"}),
        ],
        "code_anchors": _first_method_code_anchors(method_algorithms, system_diagram, claim_safety, limit=14),
        "mapping_blockers": mapping_blockers,
    }


def _no_warm_claim_unit(
    *,
    text: str,
    raw_text: str,
    claim_safety: dict[str, Any],
    gate3_audit: dict[str, Any],
    readiness: dict[str, Any],
    seed_section: dict[str, Any],
    inputs: dict[str, str],
    source_files: Sequence[str],
) -> dict[str, Any]:
    cues = [
        "No-warm PPO Gate",
        "0.453125",
        "does not evaluate obstacle-summary warm-start",
        "Formal performance claims remain blocked",
    ]
    claim = _find_claim(claim_safety.get("allowed_claims", []), "no_warm_gate3_formal_failure")
    mapping_blockers = _cue_blockers(text, cues, unit_id="no_warm_gate3_formal_failure")
    if claim is None:
        mapping_blockers.append("no_warm_gate3_formal_failure:allowed_claim_missing")
    if gate3_audit.get("formal_claim_allowed") is not True or str(gate3_audit.get("formal_decision")) != "fail":
        mapping_blockers.append("no_warm_gate3_formal_failure:gate3_formal_fail_claim_not_available")
    if readiness.get("status") != "ready_with_scope_limit":
        mapping_blockers.append("no_warm_gate3_formal_failure:readiness_not_scoped_ready")
    if seed_section.get("status") != "draft_ready_with_scope_limit":
        mapping_blockers.append("no_warm_gate3_formal_failure:section_seed_not_scoped_ready")
    return {
        "unit_id": "no_warm_gate3_formal_failure",
        "paper_scope": "scoped_negative_training_dynamics_note",
        "claim_status": "allowed_with_no_warm_scope_limit",
        "manuscript_cues": _cue_results(raw_text=raw_text, text=text, cues=cues, source_files=source_files),
        "evidence_state": "mapped" if not mapping_blockers else "missing_mapping_evidence",
        "claim_text": None if claim is None else claim.get("claim_text"),
        "required_qualifier": None if claim is None else claim.get("required_qualifier"),
        "evidence": [
            _evidence(inputs["claim_safety"], claim_safety, {"allowed_claim_present": claim is not None}),
            _evidence(
                inputs["gate3_audit"],
                gate3_audit,
                {
                    "formal_decision": gate3_audit.get("formal_decision"),
                    "terminal_rs_success_rate": gate3_audit.get("terminal_rs_success_rate"),
                    "episodes": gate3_audit.get("episodes"),
                    "success_threshold": gate3_audit.get("success_threshold") or gate3_audit.get("required_success_threshold"),
                },
            ),
            _evidence(inputs["paper_readiness"], readiness, {"section_id": "no_warm_failure_claim"}),
            _evidence(inputs["section_seed"], seed_section, {"section_id": "no_warm_gate3_failure_note"}),
        ],
        "metric_values": {
            "terminal_rs_success_rate": gate3_audit.get("terminal_rs_success_rate"),
            "episodes": gate3_audit.get("episodes"),
            "success_threshold": gate3_audit.get("success_threshold") or gate3_audit.get("required_success_threshold"),
        },
        "mapping_blockers": mapping_blockers,
    }


def _formal_results_blocked_unit(
    *,
    text: str,
    raw_text: str,
    claim_audit: dict[str, Any],
    claim_safety: dict[str, Any],
    readiness: dict[str, Any],
    seed_section: dict[str, Any],
    inputs: dict[str, str],
    source_files: Sequence[str],
) -> dict[str, Any]:
    cues = ["Formal performance claims remain blocked", "% BLOCKED: formal_results"]
    mapping_blockers = _cue_blockers(raw_text, cues, unit_id="formal_results_blocked")
    if "Formal performance claims remain blocked" not in text:
        _append_unique(mapping_blockers, "formal_results_blocked:missing_uncommented_blocked_sentence")
    if readiness.get("status") != "blocked":
        mapping_blockers.append("formal_results_blocked:readiness_not_blocked")
    if seed_section.get("status") != "blocked":
        mapping_blockers.append("formal_results_blocked:section_seed_not_blocked")
    if claim_safety.get("formal_performance_claim_allowed") is not False:
        mapping_blockers.append("formal_results_blocked:claim_safety_not_blocking_formal_performance")
    if claim_audit.get("status") != "maintex_module2_claim_audit_passed":
        mapping_blockers.append("formal_results_blocked:claim_audit_not_passed")
    return {
        "unit_id": "formal_results_blocked",
        "paper_scope": "results_placeholder",
        "claim_status": "blocked_placeholder_not_a_result_claim",
        "manuscript_cues": _cue_results(raw_text=raw_text, text=text, cues=cues, source_files=source_files),
        "evidence_state": "blocked_as_expected" if not mapping_blockers else "missing_mapping_evidence",
        "evidence": [
            _evidence(inputs["claim_audit"], claim_audit, {"required_status": "maintex_module2_claim_audit_passed"}),
            _evidence(inputs["claim_safety"], claim_safety, {"formal_performance_claim_allowed": claim_safety.get("formal_performance_claim_allowed")}),
            _evidence(inputs["paper_readiness"], readiness, {"section_id": "formal_results"}),
            _evidence(inputs["section_seed"], seed_section, {"section_id": "formal_results"}),
        ],
        "paper_blockers": list(readiness.get("blockers", [])),
        "mapping_blockers": mapping_blockers,
    }


def _warm_start_blocked_unit(
    *,
    text: str,
    raw_text: str,
    readiness: dict[str, Any],
    seed_section: dict[str, Any],
    decision_record: dict[str, Any],
    remote_packet: dict[str, Any],
    inputs: dict[str, str],
    source_files: Sequence[str],
) -> dict[str, Any]:
    cues = ["% BLOCKED: warm_start_effect", "does not evaluate obstacle-summary warm-start"]
    mapping_blockers = _cue_blockers(raw_text, cues, unit_id="warm_start_effect_blocked")
    if "does not evaluate obstacle-summary warm-start" not in text:
        _append_unique(mapping_blockers, "warm_start_effect_blocked:missing_uncommented_scope_sentence")
    if readiness.get("status") != "blocked":
        mapping_blockers.append("warm_start_effect_blocked:readiness_not_blocked")
    if seed_section.get("status") != "blocked":
        mapping_blockers.append("warm_start_effect_blocked:section_seed_not_blocked")
    if str(decision_record.get("status")) != "pending_human_decision":
        mapping_blockers.append("warm_start_effect_blocked:f02_6_not_pending_human_decision")
    if remote_packet.get("ready_to_run_remote_training") is not False:
        mapping_blockers.append("warm_start_effect_blocked:remote_packet_not_blocked")
    return {
        "unit_id": "warm_start_effect_blocked",
        "paper_scope": "warm_start_placeholder",
        "claim_status": "blocked_placeholder_pending_f02_6",
        "manuscript_cues": _cue_results(raw_text=raw_text, text=text, cues=cues, source_files=source_files),
        "evidence_state": "blocked_as_expected" if not mapping_blockers else "missing_mapping_evidence",
        "evidence": [
            _evidence(inputs["paper_readiness"], readiness, {"section_id": "warm_start_effect"}),
            _evidence(inputs["section_seed"], seed_section, {"section_id": "warm_start_effect"}),
            _evidence(inputs["f02_6_decision_record"], decision_record, {"required_status": "pending_human_decision"}),
            _evidence(inputs["remote_execution_packet"], remote_packet, {"ready_to_run_remote_training": remote_packet.get("ready_to_run_remote_training")}),
        ],
        "paper_blockers": _unique([str(item) for item in readiness.get("blockers", [])] + [str(item) for item in remote_packet.get("blockers", [])]),
        "mapping_blockers": mapping_blockers,
    }


def _cue_results(*, raw_text: str, text: str, cues: Sequence[str], source_files: Sequence[str]) -> list[dict[str, Any]]:
    return [
        {
            "cue": cue,
            "present_in_comment_stripped_text": cue in text,
            "present_in_expanded_text": cue in raw_text,
            "source_anchors": _source_anchors_for_cue(cue, source_files),
        }
        for cue in cues
    ]


def _source_anchors_for_cue(cue: str, source_files: Sequence[str]) -> list[dict[str, Any]]:
    anchors: list[dict[str, Any]] = []
    for source_file in source_files:
        path = Path(source_file)
        if not path.is_file():
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            stripped_line = _strip_latex_comments(line)
            cue_in_raw_line = cue in line
            cue_in_comment_stripped_line = cue in stripped_line
            if not cue_in_raw_line and not cue_in_comment_stripped_line:
                continue
            anchors.append(
                {
                    "path": _display_path(path),
                    "line": line_number,
                    "cue_in_raw_line": cue_in_raw_line,
                    "cue_in_comment_stripped_line": cue_in_comment_stripped_line,
                    "excerpt": line.strip()[:240],
                }
            )
    return anchors


def _cue_blockers(text: str, cues: Sequence[str], *, unit_id: str) -> list[str]:
    return [f"{unit_id}:missing_manuscript_cue:{cue}" for cue in cues if cue not in text]


def _evidence(path: str, data: dict[str, Any], extra: dict[str, Any] | None = None) -> dict[str, Any]:
    record = {
        "path": path,
        "artifact_name": data.get("artifact_name") or data.get("record_name") or data.get("packet_name") or data.get("manifest_name"),
        "status": data.get("status") or data.get("formal_decision"),
    }
    if extra:
        record.update(extra)
    blockers = data.get("blockers")
    if isinstance(blockers, list):
        record["blockers"] = blockers
    return record


def _blocking_reasons(*, claim_audit: dict[str, Any], claim_units: Sequence[dict[str, Any]]) -> list[str]:
    blockers: list[str] = []
    if claim_audit.get("status") != "maintex_module2_claim_audit_passed":
        blockers.append("upstream_claim_audit_not_passed")
    if claim_audit.get("prohibited_claim_audit", {}).get("status") != "clean":
        blockers.append("upstream_prohibited_claim_audit_not_clean")
    for unit in claim_units:
        for blocker in unit.get("mapping_blockers", []):
            _append_unique(blockers, str(blocker))
    return blockers


def _find_claim(claims: Sequence[Any], claim_id: str) -> dict[str, Any] | None:
    for item in claims:
        if isinstance(item, dict) and item.get("claim_id") == claim_id:
            return item
    return None


def _first_method_code_anchors(
    method_algorithms: dict[str, Any],
    system_diagram: dict[str, Any],
    claim_safety: dict[str, Any],
    *,
    limit: int,
) -> list[dict[str, Any]]:
    anchors: list[dict[str, Any]] = []
    for algorithm in method_algorithms.get("algorithms", []):
        if not isinstance(algorithm, dict):
            continue
        for step in algorithm.get("steps", []):
            if not isinstance(step, dict):
                continue
            for anchor in step.get("code_anchors", []):
                _append_anchor(anchors, anchor, source_artifact="module2_method_algorithms")
                if len(anchors) >= limit:
                    return anchors
    for node in system_diagram.get("nodes", []):
        if not isinstance(node, dict):
            continue
        for anchor in node.get("code_anchors", []):
            _append_anchor(anchors, anchor, source_artifact="module2_system_diagram")
            if len(anchors) >= limit:
                return anchors
    for anchor in claim_safety.get("code_anchors", []):
        _append_anchor(anchors, anchor, source_artifact="module2_claim_safety")
        if len(anchors) >= limit:
            return anchors
    return anchors


def _append_anchor(anchors: list[dict[str, Any]], anchor: Any, *, source_artifact: str) -> None:
    if not isinstance(anchor, dict):
        return
    item = dict(anchor)
    item["source_artifact"] = source_artifact
    key = (item.get("path"), item.get("line"), item.get("symbol"), item.get("pattern"), source_artifact)
    existing = {(a.get("path"), a.get("line"), a.get("symbol"), a.get("pattern"), a.get("source_artifact")) for a in anchors}
    if key not in existing:
        anchors.append(item)


def _expand_latex(path: Path, seen: set[Path] | None = None) -> dict[str, Any]:
    seen = set() if seen is None else seen
    path = Path(path).resolve()
    if path in seen:
        return {"text": "", "input_files": []}
    seen.add(path)
    text = path.read_text(encoding="utf-8")
    input_files = [str(path)]

    def replace(match: re.Match[str]) -> str:
        raw = match.group(1).strip()
        input_path = _resolve_latex_input(path.parent, raw)
        expanded = _expand_latex(input_path, seen)
        input_files.extend(expanded["input_files"])
        return expanded["text"]

    expanded_text = re.sub(r"\\input\{([^}]+)\}", replace, text)
    return {"text": expanded_text, "input_files": _unique(input_files)}


def _resolve_latex_input(base_dir: Path, raw: str) -> Path:
    candidate = base_dir / raw
    if candidate.suffix:
        return candidate
    tex_candidate = candidate.with_suffix(".tex")
    if tex_candidate.is_file():
        return tex_candidate
    return candidate


def _strip_latex_comments(text: str) -> str:
    stripped: list[str] = []
    for line in text.splitlines():
        index = _unescaped_percent_index(line)
        stripped.append(line if index is None else line[:index])
    return "\n".join(stripped)


def _unescaped_percent_index(line: str) -> int | None:
    for index, char in enumerate(line):
        if char != "%":
            continue
        backslash_count = 0
        cursor = index - 1
        while cursor >= 0 and line[cursor] == "\\":
            backslash_count += 1
            cursor -= 1
        if backslash_count % 2 == 0:
            return index
    return None


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _append_unique(items: list[str], value: str) -> None:
    if value and value not in items:
        items.append(value)


def _unique(items: Sequence[str]) -> list[str]:
    out: list[str] = []
    for item in items:
        _append_unique(out, item)
    return out


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not block evidence-map generation.
        return "unknown"


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 Manuscript Evidence Map",
        "",
        f"- status: `{manifest['status']}`",
        f"- local training allowed: `{manifest['local_training_allowed']}`",
        f"- remote training resource: `{manifest['remote_training_resource']}`",
        f"- claim audit status: `{manifest['upstream_status']['claim_audit_status']}`",
        f"- formal performance claim allowed: `{manifest['upstream_status']['formal_performance_claim_allowed']}`",
        "",
        "## Blocking Reasons",
        "",
    ]
    if manifest["blocking_reasons"]:
        lines.extend(f"- `{item}`" for item in manifest["blocking_reasons"])
    else:
        lines.append("- none")
    lines.extend(["", "## Claim Units", ""])
    for unit in manifest["claim_units"]:
        lines.append(f"### {unit['unit_id']}")
        lines.append(f"- claim status: `{unit['claim_status']}`")
        lines.append(f"- evidence state: `{unit['evidence_state']}`")
        if unit.get("mapping_blockers"):
            lines.append("- mapping blockers: " + ", ".join(f"`{item}`" for item in unit["mapping_blockers"]))
        else:
            lines.append("- mapping blockers: none")
        lines.append("- evidence:")
        for evidence in unit.get("evidence", []):
            status = evidence.get("status")
            lines.append(f"  - `{evidence['path']}` status=`{status}`")
        if unit.get("metric_values"):
            metrics = ", ".join(f"{key}={value}" for key, value in unit["metric_values"].items())
            lines.append(f"- metric values: `{metrics}`")
        if unit.get("paper_blockers"):
            lines.append("- paper blockers: " + ", ".join(f"`{item}`" for item in unit["paper_blockers"]))
        lines.append("")
    lines.extend(["## Writing Boundaries", ""])
    for boundary in manifest["writing_boundaries"]:
        lines.append(f"- {boundary}")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
