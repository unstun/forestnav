from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence


DEFAULT_OUTPUT_DIR = Path("3_paper/module2_section_seed")
DEFAULT_PAPER_READINESS = Path("0_trials/module2_paper_readiness/module2_paper_readiness.json")
DEFAULT_METHOD_ALGORITHMS = Path("0_trials/module2_method_algorithms/module2_method_algorithms.json")
DEFAULT_SYSTEM_DIAGRAM = Path("0_trials/module2_system_diagram/module2_system_diagram.json")
DEFAULT_CLAIM_SAFETY = Path("0_trials/module2_claim_safety/module2_claim_safety.json")


@dataclass(frozen=True)
class PaperSectionSeedConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    paper_readiness_path: Path = DEFAULT_PAPER_READINESS
    method_algorithms_path: Path = DEFAULT_METHOD_ALGORITHMS
    system_diagram_path: Path = DEFAULT_SYSTEM_DIAGRAM
    claim_safety_path: Path = DEFAULT_CLAIM_SAFETY


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = PaperSectionSeedConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        paper_readiness_path=args.paper_readiness,
        method_algorithms_path=args.method_algorithms,
        system_diagram_path=args.system_diagram,
        claim_safety_path=args.claim_safety,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "module2_paper_section_seed.json"
    markdown_out = config.markdown_out or output_dir / "module2_paper_section_seed.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: PaperSectionSeedConfig) -> dict[str, Any]:
    readiness = _read_json(config.paper_readiness_path)
    method_algorithms = _read_json(config.method_algorithms_path)
    system_diagram = _read_json(config.system_diagram_path)
    claim_safety = _read_json(config.claim_safety_path)

    readiness_by_id = {str(item.get("section_id")): item for item in readiness.get("section_readiness", []) if isinstance(item, dict)}
    no_warm_claim = _find_claim(claim_safety.get("allowed_claims", []), "no_warm_gate3_formal_failure")
    method_section = _method_section(
        readiness=readiness_by_id.get("method_algorithm", {}),
        method_algorithms=method_algorithms,
        evidence=str(config.method_algorithms_path),
    )
    figure_section = _system_figure_section(
        readiness=readiness_by_id.get("system_figure", {}),
        system_diagram=system_diagram,
        evidence=str(config.system_diagram_path),
    )
    no_warm_section = _no_warm_section(
        readiness=readiness_by_id.get("no_warm_failure_claim", {}),
        claim=no_warm_claim,
        evidence=str(config.claim_safety_path),
    )
    formal_section = _blocked_section(
        section_id="formal_results",
        title="Formal performance results",
        readiness=readiness_by_id.get("formal_results", {}),
    )
    warm_section = _blocked_section(
        section_id="warm_start_effect",
        title="Warm-start effect",
        readiness=readiness_by_id.get("warm_start_effect", {}),
    )
    sections = [method_section, figure_section, no_warm_section, formal_section, warm_section]
    draft_audit = _audit_generated_sections(sections, claim_safety.get("prohibited_claims", []))
    blocked = [item for item in sections if item["status"] == "blocked" and item["section_id"] in {"methods_rl_rs_operator", "system_figure_caption", "no_warm_gate3_failure_note"}]
    status = "method_sections_ready_results_blocked"
    if blocked or draft_audit["status"] != "clean":
        status = "blocked_by_readiness_or_claim_audit"
    return {
        "schema_version": 1,
        "artifact_name": "module2_paper_section_seed",
        "status": status,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "local_training_allowed": False,
        "remote_training_resource": "gpu3070ti-relay",
        "inputs": {
            "paper_readiness": str(config.paper_readiness_path),
            "method_algorithms": str(config.method_algorithms_path),
            "system_diagram": str(config.system_diagram_path),
            "claim_safety": str(config.claim_safety_path),
        },
        "input_status": {
            "paper_readiness_status": readiness.get("status"),
            "method_algorithms_status": method_algorithms.get("status"),
            "system_diagram_status": system_diagram.get("status"),
            "claim_safety_status": claim_safety.get("status"),
            "formal_performance_claim_allowed": claim_safety.get("formal_performance_claim_allowed"),
        },
        "sections": sections,
        "draft_audit": draft_audit,
        "writing_boundaries": [
            "These drafts may seed paper Methods and scoped failure text only.",
            "Formal performance claims remain blocked until H02 formal acceptance and claim safety both pass.",
            "Warm-start effect text remains blocked until F02.6 closes and a gpu3070ti-relay formal run is audited and pulled back.",
            "Do not describe Module2 as a standalone RL planner or as a replacement for Hybrid A*.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build evidence-bound Module2 manuscript section seeds without running training.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--paper-readiness", type=Path, default=DEFAULT_PAPER_READINESS)
    parser.add_argument("--method-algorithms", type=Path, default=DEFAULT_METHOD_ALGORITHMS)
    parser.add_argument("--system-diagram", type=Path, default=DEFAULT_SYSTEM_DIAGRAM)
    parser.add_argument("--claim-safety", type=Path, default=DEFAULT_CLAIM_SAFETY)
    return parser.parse_args(list(argv) if argv is not None else None)


def _method_section(*, readiness: dict[str, Any], method_algorithms: dict[str, Any], evidence: str) -> dict[str, Any]:
    blockers = []
    if readiness.get("status") != "ready_to_write":
        blockers.append("method_algorithm_not_ready")
    if method_algorithms.get("status") != "code_anchored":
        blockers.append("method_algorithms_not_code_anchored")
    algorithm = _find_algorithm(method_algorithms.get("algorithms", []), "rl_rs_funnel_analytic_expansion")
    anchors = _first_anchors(algorithm, limit=8)
    text = (
        "Module2 is implemented as a learned analytic-expansion operator inside the existing Hybrid A* search loop. "
        "The operator is invoked only at the planner's analytic-expansion hook; it rolls out steering actions from the current search node, "
        "then accepts a shortcut only when the terminal Reeds-Shepp check certifies a collision-free connection to the goal. "
        "If this certificate is absent, the operator returns no shortcut and Hybrid A* continues primitive expansion. "
        "This section should therefore describe a planner-side analytic operator with fallback semantics, not a standalone global planner."
    )
    return {
        "section_id": "methods_rl_rs_operator",
        "title": "Methods: RL-RS analytic-expansion operator",
        "status": "blocked" if blockers else "draft_ready",
        "draft_text": "" if blockers else text,
        "evidence": [evidence],
        "code_anchors": anchors,
        "blockers": blockers,
    }


def _system_figure_section(*, readiness: dict[str, Any], system_diagram: dict[str, Any], evidence: str) -> dict[str, Any]:
    blockers = []
    if readiness.get("status") != "ready_to_write":
        blockers.append("system_figure_not_ready")
    if system_diagram.get("status") != "code_anchored_drawio":
        blockers.append("system_diagram_not_code_anchored")
    nodes = [str(item.get("title")) for item in system_diagram.get("nodes", []) if isinstance(item, dict) and item.get("title")]
    text = (
        "Figure caption seed: RL-RS analytic expansion is placed inside the Hybrid A* loop. "
        "The figure should show the analytic trigger, custom operator dispatch, checkpoint-policy rollout, terminal RS certificate, "
        "accepted shortcut path, and fallback primitive expansion. "
        "The visual boundary is important: the learned policy proposes a local analytic expansion, while Hybrid A* remains the global search authority."
    )
    return {
        "section_id": "system_figure_caption",
        "title": "Figure: system architecture and fallback semantics",
        "status": "blocked" if blockers else "draft_ready",
        "draft_text": "" if blockers else text,
        "evidence": [evidence],
        "figure_nodes": nodes,
        "blockers": blockers,
    }


def _no_warm_section(*, readiness: dict[str, Any], claim: dict[str, Any] | None, evidence: str) -> dict[str, Any]:
    blockers = []
    if readiness.get("status") != "ready_with_scope_limit":
        blockers.append("no_warm_failure_claim_not_ready")
    if not claim:
        blockers.append("no_warm_failure_claim_missing")
    claim_text = str(claim.get("claim_text")) if claim else ""
    qualifier = str(claim.get("required_qualifier")) if claim else ""
    text = (
        f"{claim_text} "
        f"{qualifier} "
        "This scoped result can be used as a negative training-dynamics observation, not as evidence against the approved-or-pending warm-start branch. "
        "Formal performance claims remain blocked."
    ).strip()
    return {
        "section_id": "no_warm_gate3_failure_note",
        "title": "Scoped result note: no-warm Gate #3 failure",
        "status": "blocked" if blockers else "draft_ready_with_scope_limit",
        "draft_text": "" if blockers else text,
        "evidence": [evidence, *list(claim.get("evidence", []))] if claim else [evidence],
        "blockers": blockers,
    }


def _blocked_section(*, section_id: str, title: str, readiness: dict[str, Any]) -> dict[str, Any]:
    blockers = [str(item) for item in readiness.get("blockers", []) if item]
    if not blockers:
        blockers = ["readiness_not_formal"]
    return {
        "section_id": section_id,
        "title": title,
        "status": "blocked",
        "draft_text": "",
        "evidence": [str(item) for item in readiness.get("evidence", []) if item],
        "blockers": blockers,
    }


def _find_algorithm(algorithms: Sequence[Any], algorithm_id: str) -> dict[str, Any]:
    for item in algorithms:
        if isinstance(item, dict) and item.get("algorithm_id") == algorithm_id:
            return item
    return {}


def _find_claim(claims: Sequence[Any], claim_id: str) -> dict[str, Any] | None:
    for item in claims:
        if isinstance(item, dict) and item.get("claim_id") == claim_id:
            return item
    return None


def _first_anchors(algorithm: dict[str, Any], *, limit: int) -> list[dict[str, Any]]:
    anchors: list[dict[str, Any]] = []
    for step in algorithm.get("steps", []):
        if not isinstance(step, dict):
            continue
        for anchor in step.get("code_anchors", []):
            if isinstance(anchor, dict):
                anchors.append(anchor)
                if len(anchors) >= limit:
                    return anchors
    return anchors


def _audit_generated_sections(sections: Sequence[dict[str, Any]], prohibited_claims: Sequence[Any]) -> dict[str, Any]:
    draft_text = "\n".join(str(item.get("draft_text", "")) for item in sections)
    lower = draft_text.lower()
    violations: list[dict[str, Any]] = []
    for claim in prohibited_claims:
        if not isinstance(claim, dict):
            continue
        patterns = [str(item) for item in claim.get("patterns", []) if item]
        matched = [pattern for pattern in patterns if pattern.lower() in lower]
        if matched:
            violations.append(
                {
                    "claim_id": claim.get("claim_id"),
                    "severity": claim.get("severity"),
                    "matched_patterns": matched,
                    "reason": claim.get("reason"),
                }
            )
    return {"status": "violations_found" if violations else "clean", "violations": violations}


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not block draft generation.
        return "unknown"


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 Paper Section Seed",
        "",
        f"- status: `{manifest['status']}`",
        f"- local training allowed: `{manifest['local_training_allowed']}`",
        f"- remote training resource: `{manifest['remote_training_resource']}`",
        f"- draft audit: `{manifest['draft_audit']['status']}`",
        "",
        "## Allowed Draft Sections",
        "",
    ]
    for section in manifest["sections"]:
        lines.extend(
            [
                f"### {section['section_id']}",
                f"- status: `{section['status']}`",
                f"- evidence: `{', '.join(section.get('evidence', []))}`",
                f"- blockers: `{', '.join(section.get('blockers', [])) or 'none'}`",
                "",
            ]
        )
        text = section.get("draft_text")
        if text:
            lines.extend([str(text), ""])
    lines.extend(["## Writing Boundaries", ""])
    for item in manifest["writing_boundaries"]:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
