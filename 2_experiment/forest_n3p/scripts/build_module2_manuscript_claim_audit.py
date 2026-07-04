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


DEFAULT_OUTPUT_DIR = Path("3_paper/module2_claim_audit")
DEFAULT_MAIN_TEX = Path("3_paper/main.tex")
DEFAULT_CLAIM_SAFETY = Path("0_trials/module2_claim_safety/module2_claim_safety.json")
DEFAULT_PAPER_READINESS = Path("0_trials/module2_paper_readiness/module2_paper_readiness.json")
DEFAULT_SECTION_SEED = Path("3_paper/module2_section_seed/module2_paper_section_seed.json")
MODULE2_SEED_INPUT = "module2_section_seed/module2_paper_section_seed.tex"


@dataclass(frozen=True)
class ManuscriptClaimAuditConfig:
    output_dir: Path
    manifest_out: Path | None = None
    markdown_out: Path | None = None
    main_tex_path: Path = DEFAULT_MAIN_TEX
    claim_safety_path: Path = DEFAULT_CLAIM_SAFETY
    paper_readiness_path: Path = DEFAULT_PAPER_READINESS
    section_seed_path: Path = DEFAULT_SECTION_SEED


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = ManuscriptClaimAuditConfig(
        output_dir=args.output_dir,
        manifest_out=args.manifest_out,
        markdown_out=args.markdown_out,
        main_tex_path=args.main_tex,
        claim_safety_path=args.claim_safety,
        paper_readiness_path=args.paper_readiness,
        section_seed_path=args.section_seed,
    )
    manifest = build_manifest(config)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = config.manifest_out or output_dir / "module2_manuscript_claim_audit.json"
    markdown_out = config.markdown_out or output_dir / "module2_manuscript_claim_audit.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(config: ManuscriptClaimAuditConfig) -> dict[str, Any]:
    claim_safety = _read_json(config.claim_safety_path)
    readiness = _read_json(config.paper_readiness_path)
    section_seed = _read_json(config.section_seed_path)
    expanded = _expand_latex(config.main_tex_path)
    manuscript_text = _strip_latex_comments(expanded["text"])
    prohibited_audit = _audit_text(
        manuscript_text,
        [item for item in claim_safety.get("prohibited_claims", []) if isinstance(item, dict)],
    )
    readiness_checks = _readiness_checks(readiness)
    section_seed_checks = _section_seed_checks(section_seed)
    module2_input_checks = _module2_input_checks(
        raw_main_tex=Path(config.main_tex_path).read_text(encoding="utf-8"),
        expanded_text=expanded["text"],
        section_seed=section_seed,
    )
    blocking_reasons = _blocking_reasons(
        prohibited_audit=prohibited_audit,
        readiness_checks=readiness_checks,
        section_seed_checks=section_seed_checks,
        module2_input_checks=module2_input_checks,
    )
    return {
        "schema_version": 1,
        "artifact_name": "module2_manuscript_claim_audit",
        "status": "maintex_module2_claim_audit_passed" if not blocking_reasons else "blocked_by_manuscript_claim_audit",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(),
        "local_training_allowed": False,
        "remote_training_resource": "gpu3070ti-relay",
        "inputs": {
            "main_tex": str(config.main_tex_path),
            "claim_safety": str(config.claim_safety_path),
            "paper_readiness": str(config.paper_readiness_path),
            "section_seed": str(config.section_seed_path),
        },
        "expanded_manuscript": {
            "sha256": hashlib.sha256(expanded["text"].encode("utf-8")).hexdigest(),
            "expanded_input_files": expanded["input_files"],
            "comment_stripped_char_count": len(manuscript_text),
        },
        "claim_safety_status": {
            "status": claim_safety.get("status"),
            "formal_performance_claim_allowed": claim_safety.get("formal_performance_claim_allowed"),
            "allowed_claim_ids": [str(item.get("claim_id")) for item in claim_safety.get("allowed_claims", []) if isinstance(item, dict)],
        },
        "prohibited_claim_audit": prohibited_audit,
        "readiness_checks": readiness_checks,
        "section_seed_checks": section_seed_checks,
        "module2_input_checks": module2_input_checks,
        "blocking_reasons": blocking_reasons,
        "claim_boundaries": [
            "This audit expands LaTeX inputs before scanning Module2 claims.",
            "LaTeX comments are ignored for prohibited-claim matching so BLOCKED comments can document missing evidence without becoming claims.",
            "Formal Module2 results and warm-start effect remain blocked until paper readiness, H02 acceptance, and claim safety are formal-ready.",
            "No local training is allowed; formal PPO training remains gated on F02.6 and gpu3070ti-relay.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit the expanded manuscript for Module2 claim-safety violations.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--main-tex", type=Path, default=DEFAULT_MAIN_TEX)
    parser.add_argument("--claim-safety", type=Path, default=DEFAULT_CLAIM_SAFETY)
    parser.add_argument("--paper-readiness", type=Path, default=DEFAULT_PAPER_READINESS)
    parser.add_argument("--section-seed", type=Path, default=DEFAULT_SECTION_SEED)
    return parser.parse_args(list(argv) if argv is not None else None)


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


def _audit_text(text: str, prohibited_claims: Sequence[dict[str, Any]]) -> dict[str, Any]:
    lower = text.lower()
    violations: list[dict[str, Any]] = []
    for claim in prohibited_claims:
        patterns = [str(pattern) for pattern in claim.get("patterns", []) if pattern]
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


def _readiness_checks(readiness: dict[str, Any]) -> dict[str, Any]:
    by_id = {str(item.get("section_id")): item for item in readiness.get("section_readiness", []) if isinstance(item, dict)}
    formal = by_id.get("formal_results", {})
    warm = by_id.get("warm_start_effect", {})
    return {
        "paper_readiness_status": readiness.get("status"),
        "formal_results_status": formal.get("status"),
        "formal_results_blockers": list(formal.get("blockers", [])),
        "warm_start_effect_status": warm.get("status"),
        "warm_start_effect_blockers": list(warm.get("blockers", [])),
    }


def _section_seed_checks(section_seed: dict[str, Any]) -> dict[str, Any]:
    by_id = {str(item.get("section_id")): item for item in section_seed.get("sections", []) if isinstance(item, dict)}
    method = by_id.get("methods_rl_rs_operator", {})
    no_warm = by_id.get("no_warm_gate3_failure_note", {})
    formal = by_id.get("formal_results", {})
    warm = by_id.get("warm_start_effect", {})
    return {
        "section_seed_status": section_seed.get("status"),
        "latex_output": section_seed.get("generated_outputs", {}).get("latex"),
        "method_section_status": method.get("status"),
        "no_warm_section_status": no_warm.get("status"),
        "formal_results_status": formal.get("status"),
        "warm_start_effect_status": warm.get("status"),
    }


def _module2_input_checks(*, raw_main_tex: str, expanded_text: str, section_seed: dict[str, Any]) -> dict[str, Any]:
    latex_path = str(section_seed.get("generated_outputs", {}).get("latex") or MODULE2_SEED_INPUT)
    return {
        "module2_seed_input_present": f"\\input{{{MODULE2_SEED_INPUT}}}" in raw_main_tex or f"\\input{{{latex_path}}}" in raw_main_tex,
        "module2_label_present": r"\label{sec:module2_rl_rs_operator}" in expanded_text,
        "method_boundary_present": "learned analytic-expansion operator inside" in expanded_text,
        "no_warm_scope_present": "does not evaluate obstacle-summary warm-start" in expanded_text,
        "formal_blocked_sentence_present": "Formal performance claims remain blocked" in expanded_text,
        "formal_results_blocked_comment_present": "% BLOCKED: formal_results" in expanded_text,
        "warm_start_blocked_comment_present": "% BLOCKED: warm_start_effect" in expanded_text,
    }


def _blocking_reasons(
    *,
    prohibited_audit: dict[str, Any],
    readiness_checks: dict[str, Any],
    section_seed_checks: dict[str, Any],
    module2_input_checks: dict[str, Any],
) -> list[str]:
    blockers: list[str] = []
    if prohibited_audit["status"] != "clean":
        blockers.append("prohibited_claims_found")
    required_input_checks = (
        "module2_seed_input_present",
        "module2_label_present",
        "method_boundary_present",
        "no_warm_scope_present",
        "formal_blocked_sentence_present",
        "formal_results_blocked_comment_present",
        "warm_start_blocked_comment_present",
    )
    for check in required_input_checks:
        if module2_input_checks.get(check) is not True:
            blockers.append(f"missing_{check}")
    if readiness_checks.get("formal_results_status") != "blocked":
        blockers.append("formal_results_not_blocked_in_readiness")
    if readiness_checks.get("warm_start_effect_status") != "blocked":
        blockers.append("warm_start_effect_not_blocked_in_readiness")
    if section_seed_checks.get("method_section_status") != "draft_ready":
        blockers.append("method_section_not_draft_ready")
    if section_seed_checks.get("no_warm_section_status") != "draft_ready_with_scope_limit":
        blockers.append("no_warm_section_not_scoped_ready")
    if section_seed_checks.get("formal_results_status") != "blocked":
        blockers.append("formal_results_not_blocked_in_section_seed")
    if section_seed_checks.get("warm_start_effect_status") != "blocked":
        blockers.append("warm_start_effect_not_blocked_in_section_seed")
    return blockers


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _unique(items: Sequence[str]) -> list[str]:
    out: list[str] = []
    for item in items:
        if item not in out:
            out.append(item)
    return out


def _source_head() -> str:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        return f"{head}+dirty" if dirty else head
    except Exception:  # noqa: BLE001 - provenance should not block audit generation.
        return "unknown"


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 Manuscript Claim Audit",
        "",
        f"- status: `{manifest['status']}`",
        f"- prohibited claim audit: `{manifest['prohibited_claim_audit']['status']}`",
        f"- local training allowed: `{manifest['local_training_allowed']}`",
        f"- remote training resource: `{manifest['remote_training_resource']}`",
        "",
        "## Blocking Reasons",
        "",
    ]
    if manifest["blocking_reasons"]:
        for reason in manifest["blocking_reasons"]:
            lines.append(f"- {reason}")
    else:
        lines.append("- none")
    lines.extend(["", "## Module2 Input Checks", ""])
    for key, value in manifest["module2_input_checks"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Readiness Checks", ""])
    for key, value in manifest["readiness_checks"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Prohibited Claim Violations", ""])
    for violation in manifest["prohibited_claim_audit"]["violations"]:
        lines.append(f"- `{violation['claim_id']}`: {', '.join(violation['matched_patterns'])}")
    if not manifest["prohibited_claim_audit"]["violations"]:
        lines.append("- none")
    lines.extend(["", "## Claim Boundaries", ""])
    for boundary in manifest["claim_boundaries"]:
        lines.append(f"- {boundary}")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
