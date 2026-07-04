from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence


DEFAULT_OUTPUT_DIR = Path("3_paper/module2_reviewer_evidence_cards")
DEFAULT_EVIDENCE_MAP = Path("3_paper/module2_evidence_map/module2_manuscript_evidence_map.json")


@dataclass(frozen=True)
class ReviewerEvidenceCardsConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    latex_out: Path | None = None
    evidence_map_path: Path = DEFAULT_EVIDENCE_MAP


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = ReviewerEvidenceCardsConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        latex_out=args.latex_out,
        evidence_map_path=args.evidence_map,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "module2_reviewer_evidence_cards.json"
    markdown_out = config.markdown_out or output_dir / "module2_reviewer_evidence_cards.md"
    latex_out = config.latex_out or output_dir / "module2_reviewer_evidence_cards.tex"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    latex_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    latex_out.write_text(_latex(manifest), encoding="utf-8")
    print(
        json.dumps(
            {
                "manifest": str(manifest_out),
                "markdown": str(markdown_out),
                "latex": str(latex_out),
                "status": manifest["status"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


def build_manifest(config: ReviewerEvidenceCardsConfig) -> dict[str, Any]:
    evidence_map = _read_json(config.evidence_map_path)
    cards = [_claim_card(unit) for unit in evidence_map.get("claim_units", []) if isinstance(unit, dict)]
    blocking_reasons = _blocking_reasons(evidence_map=evidence_map, cards=cards)
    manifest = {
        "schema_version": 1,
        "artifact_name": "module2_reviewer_evidence_cards",
        "status": "pending_supplement_audit",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "local_training_allowed": False,
        "remote_training_resource": evidence_map.get("remote_training_resource", "gpu3070ti-relay"),
        "inputs": {"evidence_map": str(config.evidence_map_path)},
        "generated_outputs": {
            "manifest": str(config.manifest_out or config.output_dir / "module2_reviewer_evidence_cards.json"),
            "markdown": str(config.markdown_out or config.output_dir / "module2_reviewer_evidence_cards.md"),
            "latex": str(config.latex_out or config.output_dir / "module2_reviewer_evidence_cards.tex"),
        },
        "upstream_status": {
            "evidence_map_status": evidence_map.get("status"),
            "formal_performance_claim_allowed": evidence_map.get("upstream_status", {}).get("formal_performance_claim_allowed"),
            "f02_6_decision_status": evidence_map.get("upstream_status", {}).get("f02_6_decision_status"),
            "remote_execution_ready": evidence_map.get("upstream_status", {}).get("remote_execution_ready"),
        },
        "cards": cards,
        "blocking_reasons": blocking_reasons,
        "verification_commands": [
            "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_manuscript_evidence_map",
            "PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_reviewer_evidence_cards",
            "PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_manuscript_evidence_map.py 2_experiment/forest_n3p/tests/test_module2_reviewer_evidence_cards.py",
            "pdflatex wrapper input for 3_paper/module2_reviewer_evidence_cards/module2_reviewer_evidence_cards.tex",
            "KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests",
            "cd 3_paper && pdflatex -interaction=nonstopmode -halt-on-error -draftmode -output-directory=/tmp/forestnav_module2_texcheck main.tex",
        ],
        "review_boundaries": [
            "These cards are for reviewer-facing traceability, not formal performance evidence.",
            "Cards with claim_status beginning with blocked_ are placeholders only and must not be rewritten as result claims.",
            "No local training is allowed; formal PPO checkpoint production remains gated on F02.6 and gpu3070ti-relay.",
        ],
    }
    supplement_audit = _supplement_latex_audit(_latex(manifest))
    manifest["supplement_latex_audit"] = supplement_audit
    if supplement_audit["status"] != "clean":
        blocking_reasons.append("supplement_latex_audit_not_clean")
    manifest["blocking_reasons"] = _unique(blocking_reasons)
    manifest["status"] = "reviewer_evidence_cards_ready" if not manifest["blocking_reasons"] else "blocked_by_incomplete_reviewer_cards"
    return manifest


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build reviewer-facing Module2 claim evidence cards without running training.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--latex-out", type=Path, default=None)
    parser.add_argument("--evidence-map", type=Path, default=DEFAULT_EVIDENCE_MAP)
    return parser.parse_args(list(argv) if argv is not None else None)


def _claim_card(unit: dict[str, Any]) -> dict[str, Any]:
    claim_status = str(unit.get("claim_status"))
    evidence_state = str(unit.get("evidence_state"))
    manuscript_anchors = _manuscript_anchors(unit)
    card = {
        "card_id": unit.get("unit_id"),
        "paper_scope": unit.get("paper_scope"),
        "claim_status": claim_status,
        "evidence_state": evidence_state,
        "reviewer_verdict": _reviewer_verdict(claim_status, evidence_state),
        "manuscript_anchors": manuscript_anchors,
        "primary_evidence": unit.get("evidence", []),
        "code_anchors": unit.get("code_anchors", []),
        "metric_values": unit.get("metric_values", {}),
        "paper_blockers": unit.get("paper_blockers", []),
        "mapping_blockers": unit.get("mapping_blockers", []),
        "writing_instruction": _writing_instruction(claim_status, evidence_state),
    }
    return card


def _manuscript_anchors(unit: dict[str, Any]) -> list[dict[str, Any]]:
    anchors: list[dict[str, Any]] = []
    seen: set[tuple[str, int, str]] = set()
    for cue in unit.get("manuscript_cues", []):
        if not isinstance(cue, dict):
            continue
        cue_text = str(cue.get("cue"))
        for anchor in cue.get("source_anchors", []):
            if not isinstance(anchor, dict):
                continue
            key = (str(anchor.get("path")), int(anchor.get("line", 0)), cue_text)
            if key in seen:
                continue
            seen.add(key)
            anchors.append(
                {
                    "cue": cue_text,
                    "path": anchor.get("path"),
                    "line": anchor.get("line"),
                    "cue_in_raw_line": anchor.get("cue_in_raw_line"),
                    "cue_in_comment_stripped_line": anchor.get("cue_in_comment_stripped_line"),
                    "excerpt": anchor.get("excerpt"),
                }
            )
    return anchors


def _reviewer_verdict(claim_status: str, evidence_state: str) -> str:
    if claim_status.startswith("blocked_") and evidence_state == "blocked_as_expected":
        return "blocked_placeholder_traceable"
    if evidence_state == "mapped":
        return "claim_traceable_with_scope_limit"
    return "needs_attention"


def _writing_instruction(claim_status: str, evidence_state: str) -> str:
    if claim_status.startswith("blocked_"):
        return "Do not write this as a result claim; keep it as a blocked placeholder until the listed blockers close."
    if evidence_state == "mapped":
        return "Can be used only with the listed scope/qualifier and cited against the primary evidence artifacts."
    return "Do not use until mapping blockers are resolved."


def _blocking_reasons(*, evidence_map: dict[str, Any], cards: Sequence[dict[str, Any]]) -> list[str]:
    blockers: list[str] = []
    if evidence_map.get("status") != "module2_manuscript_evidence_mapped":
        blockers.append("evidence_map_not_mapped")
    for card in cards:
        if not card.get("manuscript_anchors"):
            blockers.append(f"{card.get('card_id')}:missing_manuscript_anchors")
        if card.get("mapping_blockers"):
            blockers.append(f"{card.get('card_id')}:mapping_blockers_present")
    return _unique(blockers)


def _supplement_latex_audit(latex_text: str) -> dict[str, Any]:
    required_fragments = [
        "not formal performance evidence",
        r"Formal performance claim allowed: \texttt{False}",
        "Do not write this as a result claim",
        r"blocked\_placeholder\_traceable",
    ]
    prohibited_fragments = [
        "warm-start approved",
        "formal performance improvement",
        "RL replaces Hybrid A*",
    ]
    missing = [fragment for fragment in required_fragments if fragment not in latex_text]
    matched_prohibited = [fragment for fragment in prohibited_fragments if fragment in latex_text]
    return {
        "status": "clean" if not missing and not matched_prohibited else "violations_found",
        "required_fragments_present": [fragment for fragment in required_fragments if fragment in latex_text],
        "missing_required_fragments": missing,
        "matched_prohibited_fragments": matched_prohibited,
    }


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _unique(items: Sequence[str]) -> list[str]:
    out: list[str] = []
    for item in items:
        if item and item not in out:
            out.append(item)
    return out


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not block reviewer-card generation.
        return "unknown"


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 Reviewer Evidence Cards",
        "",
        f"- status: `{manifest['status']}`",
        f"- local training allowed: `{manifest['local_training_allowed']}`",
        f"- remote training resource: `{manifest['remote_training_resource']}`",
        f"- evidence map status: `{manifest['upstream_status']['evidence_map_status']}`",
        f"- formal performance claim allowed: `{manifest['upstream_status']['formal_performance_claim_allowed']}`",
        "",
        "## Blocking Reasons",
        "",
    ]
    if manifest["blocking_reasons"]:
        lines.extend(f"- `{item}`" for item in manifest["blocking_reasons"])
    else:
        lines.append("- none")
    lines.extend(["", "## Cards", ""])
    for card in manifest["cards"]:
        lines.append(f"### {card['card_id']}")
        lines.append(f"- reviewer verdict: `{card['reviewer_verdict']}`")
        lines.append(f"- claim status: `{card['claim_status']}`")
        lines.append(f"- evidence state: `{card['evidence_state']}`")
        lines.append(f"- writing instruction: {card['writing_instruction']}")
        lines.append("- manuscript anchors:")
        for anchor in card.get("manuscript_anchors", []):
            lines.append(
                f"  - `{anchor['cue']}` -> `{anchor['path']}:{anchor['line']}` "
                f"raw=`{anchor['cue_in_raw_line']}` stripped=`{anchor['cue_in_comment_stripped_line']}`"
            )
        lines.append("- primary evidence:")
        for evidence in card.get("primary_evidence", []):
            lines.append(f"  - `{evidence.get('path')}` status=`{evidence.get('status')}`")
        if card.get("metric_values"):
            metrics = ", ".join(f"{key}={value}" for key, value in card["metric_values"].items())
            lines.append(f"- metric values: `{metrics}`")
        if card.get("paper_blockers"):
            lines.append("- paper blockers: " + ", ".join(f"`{item}`" for item in card["paper_blockers"]))
        if card.get("code_anchors"):
            lines.append("- code anchors:")
            for anchor in card["code_anchors"][:8]:
                lines.append(f"  - `{anchor.get('path')}:{anchor.get('line')}` `{anchor.get('symbol')}`")
        lines.append("")
    lines.extend(["## Verification Commands", ""])
    for command in manifest["verification_commands"]:
        lines.append(f"- `{command}`")
    lines.extend(["", "## Review Boundaries", ""])
    for boundary in manifest["review_boundaries"]:
        lines.append(f"- {boundary}")
    lines.append("")
    return "\n".join(lines)


def _latex(manifest: dict[str, Any]) -> str:
    lines = [
        "% Auto-generated Module2 reviewer evidence appendix.",
        f"% Source manifest: {manifest['generated_outputs']['manifest']}",
        "% This appendix is traceability material, not formal performance evidence.",
        "",
        r"\section{Module2 Reviewer Evidence Cards}",
        r"\label{app:module2_reviewer_evidence_cards}",
        "",
        "This appendix records source-level traceability for the Module2 manuscript text. "
        "It is generated from the reviewer evidence-card manifest and should be read as a claim-audit aid, not as a formal result.",
        "",
        r"\begin{itemize}",
        rf"\item Status: \texttt{{{_latex_escape(str(manifest['status']))}}}.",
        rf"\item Local training allowed: \texttt{{{_latex_escape(str(manifest['local_training_allowed']))}}}.",
        rf"\item Remote training resource: \texttt{{{_latex_escape(str(manifest['remote_training_resource']))}}}.",
        rf"\item Formal performance claim allowed: \texttt{{{_latex_escape(str(manifest['upstream_status']['formal_performance_claim_allowed']))}}}.",
        r"\end{itemize}",
        "",
    ]
    for card in manifest["cards"]:
        lines.extend(_latex_card(card))
    lines.extend(
        [
            r"\subsection{Verification Commands}",
            r"\begin{itemize}",
        ]
    )
    for command in manifest["verification_commands"]:
        lines.append(rf"\item \texttt{{{_latex_escape(command)}}}")
    lines.extend([r"\end{itemize}", "", r"\subsection{Review Boundaries}", r"\begin{itemize}"])
    for boundary in manifest["review_boundaries"]:
        lines.append(rf"\item {_latex_escape(boundary)}")
    lines.extend([r"\end{itemize}", ""])
    return "\n".join(lines)


def _latex_card(card: dict[str, Any]) -> list[str]:
    lines = [
        rf"\subsection{{{_latex_escape(str(card['card_id']))}}}",
        r"\begin{itemize}",
        rf"\item Reviewer verdict: \texttt{{{_latex_escape(str(card['reviewer_verdict']))}}}.",
        rf"\item Claim status: \texttt{{{_latex_escape(str(card['claim_status']))}}}.",
        rf"\item Evidence state: \texttt{{{_latex_escape(str(card['evidence_state']))}}}.",
        rf"\item Writing instruction: {_latex_escape(str(card['writing_instruction']))}",
        r"\end{itemize}",
        r"\paragraph{Manuscript anchors.}",
        r"\begin{itemize}",
    ]
    for anchor in card.get("manuscript_anchors", []):
        lines.append(
            rf"\item \texttt{{{_latex_escape(str(anchor['cue']))}}} "
            rf"$\rightarrow$ \texttt{{{_latex_escape(str(anchor['path']))}:{_latex_escape(str(anchor['line']))}}} "
            rf"(raw=\texttt{{{_latex_escape(str(anchor['cue_in_raw_line']))}}}, "
            rf"stripped=\texttt{{{_latex_escape(str(anchor['cue_in_comment_stripped_line']))}}})."
        )
    lines.extend([r"\end{itemize}", r"\paragraph{Primary evidence.}", r"\begin{itemize}"])
    for evidence in card.get("primary_evidence", []):
        lines.append(
            rf"\item \texttt{{{_latex_escape(str(evidence.get('path')))}}}, "
            rf"status=\texttt{{{_latex_escape(str(evidence.get('status')))}}}."
        )
    lines.append(r"\end{itemize}")
    if card.get("metric_values"):
        metrics = ", ".join(f"{key}={value}" for key, value in card["metric_values"].items())
        lines.extend([r"\paragraph{Metric values.}", rf"\texttt{{{_latex_escape(metrics)}}}", ""])
    if card.get("paper_blockers"):
        lines.extend([r"\paragraph{Paper blockers.}", r"\begin{itemize}"])
        for blocker in card["paper_blockers"]:
            lines.append(rf"\item \texttt{{{_latex_escape(str(blocker))}}}")
        lines.append(r"\end{itemize}")
    if card.get("code_anchors"):
        lines.extend([r"\paragraph{Code anchors.}", r"\begin{itemize}"])
        for anchor in card["code_anchors"][:8]:
            path_line = f"{anchor.get('path')}:{anchor.get('line')}"
            lines.append(rf"\item \texttt{{{_latex_escape(path_line)}}} \texttt{{{_latex_escape(str(anchor.get('symbol')))}}}")
        lines.append(r"\end{itemize}")
    lines.append("")
    return lines


def _latex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)


if __name__ == "__main__":
    raise SystemExit(main())
