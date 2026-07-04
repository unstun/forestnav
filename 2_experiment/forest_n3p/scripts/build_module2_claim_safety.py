from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_claim_safety")
DEFAULT_PAPER_TABLES = Path("0_trials/module2_paper_tables/module2_paper_tables.json")
DEFAULT_H02_FORMAL_ACCEPTANCE = Path("0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json")
DEFAULT_H01_MANIFEST = Path("0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json")
DEFAULT_F02_6_PACKET = Path("0_trials/module2_f02_6_warm_start_decision_packet/f02_6_warm_start_decision_packet.json")
DEFAULT_GATE3_AUDIT = Path("0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/gate3_formal_audit.json")
DEFAULT_METHOD_ALGORITHMS = Path("0_trials/module2_method_algorithms/module2_method_algorithms.json")
DEFAULT_SYSTEM_DIAGRAM = Path("0_trials/module2_system_diagram/module2_system_diagram.json")


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    repo_root = _repo_root()
    manifest = build_manifest(
        repo_root=repo_root,
        paper_tables_path=args.paper_tables,
        h02_formal_acceptance_path=args.h02_formal_acceptance,
        h01_manifest_path=args.h01_manifest,
        f02_6_packet_path=args.f02_6_packet,
        gate3_audit_path=args.gate3_audit,
        method_algorithms_path=args.method_algorithms,
        system_diagram_path=args.system_diagram,
        draft_text_path=args.draft_text,
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = args.manifest_out or output_dir / "module2_claim_safety.json"
    markdown_out = args.markdown_out or output_dir / "module2_claim_safety.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]}, indent=2, ensure_ascii=False))
    return 0


def build_manifest(
    *,
    repo_root: Path,
    paper_tables_path: Path,
    h02_formal_acceptance_path: Path,
    h01_manifest_path: Path,
    f02_6_packet_path: Path,
    gate3_audit_path: Path,
    method_algorithms_path: Path,
    system_diagram_path: Path,
    draft_text_path: Path | None = None,
) -> dict[str, Any]:
    paper_tables = _read_json(paper_tables_path)
    h02_formal_acceptance = _read_json(h02_formal_acceptance_path)
    h01_manifest = _read_json(h01_manifest_path)
    f02_6_packet = _read_json(f02_6_packet_path)
    gate3_audit = _read_json(gate3_audit_path)
    method_algorithms = _read_json(method_algorithms_path)
    system_diagram = _read_json(system_diagram_path)

    formal_blockers = _formal_performance_blockers(
        paper_tables=paper_tables,
        h02_formal_acceptance=h02_formal_acceptance,
        h01_manifest=h01_manifest,
        f02_6_packet=f02_6_packet,
    )
    formal_allowed = not formal_blockers
    prohibited = _prohibited_claims()
    allowed = _allowed_claims(
        method_algorithms=method_algorithms,
        system_diagram=system_diagram,
        gate3_audit=gate3_audit,
    )
    draft_audit = _audit_draft(draft_text_path, prohibited)
    return {
        "schema_version": 1,
        "artifact_name": "module2_claim_safety",
        "status": "formal_performance_claims_allowed" if formal_allowed else "blocked_formal_performance_claims",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(repo_root),
        "formal_performance_claim_allowed": formal_allowed,
        "formal_performance_blockers": formal_blockers,
        "inputs": {
            "paper_tables": str(paper_tables_path),
            "h02_formal_acceptance": str(h02_formal_acceptance_path),
            "h01_manifest": str(h01_manifest_path),
            "f02_6_packet": str(f02_6_packet_path),
            "gate3_audit": str(gate3_audit_path),
            "method_algorithms": str(method_algorithms_path),
            "system_diagram": str(system_diagram_path),
            "draft_text": None if draft_text_path is None else str(draft_text_path),
        },
        "input_status": {
            "paper_tables_status": paper_tables.get("status"),
            "paper_tables_formal_claim_allowed": paper_tables.get("formal_claim_allowed"),
            "h02_formal_acceptance_status": h02_formal_acceptance.get("status"),
            "h02_formal_output_accepted": h02_formal_acceptance.get("formal_output_accepted"),
            "h02_paper_result_input_allowed": h02_formal_acceptance.get("paper_result_input_allowed"),
            "h01_manifest_status": h01_manifest.get("status"),
            "f02_6_status": f02_6_packet.get("status"),
            "gate3_formal_decision": gate3_audit.get("formal_decision"),
            "gate3_formal_claim_allowed": gate3_audit.get("formal_claim_allowed"),
            "method_algorithms_status": method_algorithms.get("status"),
            "system_diagram_status": system_diagram.get("status"),
        },
        "allowed_claims": allowed,
        "conditional_claims": _conditional_claims(),
        "prohibited_claims": prohibited,
        "draft_audit": draft_audit,
        "code_anchors": _code_anchors(repo_root),
        "claim_boundaries": [
            "Do not claim formal performance improvement until formal_performance_claim_allowed=true.",
            "No-warm Gate #3 failure is scoped to no-warm PPO only; it does not reject obstacle-summary warm-start.",
            "Method claims must say the learned policy is an analytic-expansion operator inside Hybrid A*, not a standalone global planner.",
            "Completeness/global-optimality/generalization claims are prohibited unless a future contract explicitly proves them.",
            "Formal PPO training/checkpoint production must run on gpu3070ti-relay or another explicitly approved remote GPU.",
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Module2 paper claim safety guard.")
    parser.add_argument("--paper-tables", type=Path, default=DEFAULT_PAPER_TABLES)
    parser.add_argument("--h02-formal-acceptance", type=Path, default=DEFAULT_H02_FORMAL_ACCEPTANCE)
    parser.add_argument("--h01-manifest", type=Path, default=DEFAULT_H01_MANIFEST)
    parser.add_argument("--f02-6-packet", type=Path, default=DEFAULT_F02_6_PACKET)
    parser.add_argument("--gate3-audit", type=Path, default=DEFAULT_GATE3_AUDIT)
    parser.add_argument("--method-algorithms", type=Path, default=DEFAULT_METHOD_ALGORITHMS)
    parser.add_argument("--system-diagram", type=Path, default=DEFAULT_SYSTEM_DIAGRAM)
    parser.add_argument("--draft-text", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    return parser.parse_args(list(argv) if argv is not None else None)


def _formal_performance_blockers(
    *,
    paper_tables: dict[str, Any],
    h02_formal_acceptance: dict[str, Any],
    h01_manifest: dict[str, Any],
    f02_6_packet: dict[str, Any],
) -> list[str]:
    blockers: list[str] = []
    if paper_tables.get("formal_claim_allowed") is not True:
        blockers.append("paper_tables_not_formal")
    for blocker in paper_tables.get("blockers") or ():
        _append_unique(blockers, str(blocker))
    if h02_formal_acceptance.get("formal_output_accepted") is not True or h02_formal_acceptance.get("paper_result_input_allowed") is not True:
        _append_unique(blockers, "h02_formal_acceptance_not_accepted")
    for blocker in h02_formal_acceptance.get("blockers") or ():
        _append_unique(blockers, str(blocker))
    if str(h01_manifest.get("status")) not in {"ready", "formal_ready", "ready_for_formal_evaluation"}:
        _append_unique(blockers, "h01_manifest_not_ready")
    for blocker in h01_manifest.get("blockers") or ():
        _append_unique(blockers, str(blocker))
    if str(f02_6_packet.get("status")) == "pending_human_decision":
        _append_unique(blockers, "f02_6_pending")
    for blocker in f02_6_packet.get("blockers") or ():
        _append_unique(blockers, str(blocker))
    return blockers


def _allowed_claims(*, method_algorithms: dict[str, Any], system_diagram: dict[str, Any], gate3_audit: dict[str, Any]) -> list[dict[str, Any]]:
    claims: list[dict[str, Any]] = []
    if method_algorithms.get("status") == "code_anchored" and system_diagram.get("status") == "code_anchored_drawio":
        claims.append(
            {
                "claim_id": "method_is_ha_star_analytic_operator",
                "scope": "method_structure",
                "claim_text": "Module2 implements a learned analytic-expansion operator inside Hybrid A*, with terminal RS certification and primitive fallback.",
                "required_qualifier": "Do not describe it as an end-to-end RL global planner.",
                "evidence": [
                    "0_trials/module2_method_algorithms/module2_method_algorithms.json",
                    "0_trials/module2_system_diagram/module2_system_diagram.json",
                ],
            }
        )
    if gate3_audit.get("formal_claim_allowed") is True and str(gate3_audit.get("formal_decision")) == "fail":
        rate = gate3_audit.get("terminal_rs_success_rate")
        episodes = gate3_audit.get("episodes")
        threshold = gate3_audit.get("success_threshold") or gate3_audit.get("required_success_threshold")
        claims.append(
            {
                "claim_id": "no_warm_gate3_formal_failure",
                "scope": "no_warm_only",
                "claim_text": f"No-warm PPO Gate #3 formal trial failed: terminal-RS success rate was {rate} over {episodes} episodes, below threshold {threshold}.",
                "required_qualifier": "This does not evaluate obstacle-summary warm-start PPO and does not reject the whole RL-RS direction.",
                "evidence": ["0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/gate3_formal_audit.json"],
            }
        )
    return claims


def _conditional_claims() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "formal_performance_improvement",
            "status": "blocked_until_formal_h02",
            "template": "On the approved procedural and real-map evaluation suite, RL-RS funnel reduces expansions/time/timeout relative to Dang multi-RS.",
            "required_evidence": [
                "H02 formal_acceptance=true",
                "H02 formal acceptance artifact has formal_output_accepted=true and paper_result_input_allowed=true",
                "H01 manifest ready/formal_ready",
                "real PPO checkpoint rows present",
                "paired Wilcoxon p<0.05 for total_time_s and total_expansions",
                "bootstrap CI for success/failure/timeout-rate differences",
            ],
        },
        {
            "claim_id": "warm_start_effect",
            "status": "blocked_until_f02_6_and_remote_formal",
            "template": "Obstacle-summary BC warm-start improves PPO analytic operator reliability.",
            "required_evidence": [
                "F02.6 approved by Dr Sun",
                "warm-start formal PPO run on gpu3070ti-relay",
                "formal audit without smoke blockers",
            ],
        },
    ]


def _prohibited_claims() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "global_optimality",
            "severity": "hard_block",
            "patterns": ["全局最优", "globally optimal", "global optimality"],
            "reason": "Current contract and evaluation do not prove global optimality.",
        },
        {
            "claim_id": "completeness_enhancement",
            "severity": "hard_block",
            "patterns": ["完备性增强", "提高完备性", "completeness enhancement", "improves completeness"],
            "reason": "The allowed claim is fallback safety semantics, not completeness improvement.",
        },
        {
            "claim_id": "rl_replaces_hybrid_astar",
            "severity": "hard_block",
            "patterns": ["RL 替代 Hybrid A*", "RL replaces Hybrid A*", "replace Hybrid A*", "替代 Hybrid A*"],
            "reason": "The learned policy is only an analytic-expansion operator inside Hybrid A*.",
        },
        {
            "claim_id": "universal_generalization",
            "severity": "hard_block",
            "patterns": ["泛化到所有森林", "all forest environments", "universal generalization", "generalizes to all"],
            "reason": "Current protocol is scoped to specified procedural and real-map evaluations.",
        },
        {
            "claim_id": "warm_start_approved",
            "severity": "hard_block",
            "patterns": ["warm-start approved", "热启动已批准", "obstacle-summary warm-start is approved"],
            "reason": "F02.6 remains pending until Dr Sun explicitly approves or rejects.",
        },
    ]


def _audit_draft(draft_text_path: Path | None, prohibited_claims: Sequence[dict[str, Any]]) -> dict[str, Any]:
    if draft_text_path is None:
        return {"status": "not_requested", "draft_text": None, "violations": []}
    text = Path(draft_text_path).read_text(encoding="utf-8")
    lower = text.lower()
    violations: list[dict[str, Any]] = []
    for claim in prohibited_claims:
        matched = [pattern for pattern in claim["patterns"] if pattern.lower() in lower]
        if matched:
            violations.append(
                {
                    "claim_id": claim["claim_id"],
                    "severity": claim["severity"],
                    "matched_patterns": matched,
                    "reason": claim["reason"],
                }
            )
    return {
        "status": "violations_found" if violations else "clean",
        "draft_text": str(draft_text_path),
        "violations": violations,
    }


def _code_anchors(repo_root: Path) -> list[dict[str, Any]]:
    return [
        _anchor(repo_root, "2_experiment/forest_n3p/scripts/build_module2_paper_tables.py", "formal_claim_allowed = not blockers", "paper_table_formal_gate"),
        _anchor(repo_root, "2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py", "f02_6_decision_packet_pending", "h01_f02_6_guard"),
        _anchor(repo_root, "2_experiment/forest_n3p/scripts/audit_rl_rs_gate3_trial.py", '"formal_claim_allowed": formal_decision in {"pass", "fail"}', "gate3_formal_claim_gate"),
        _anchor(repo_root, "2_experiment/forest_n3p/scripts/build_module2_method_algorithms.py", "The learned component is an analytic-expansion operator", "method_claim_boundary"),
        _anchor(repo_root, "2_experiment/forest_n3p/scripts/build_module2_system_diagram.py", "not a standalone RL planner", "system_diagram_claim_boundary"),
    ]


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _append_unique(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _anchor(repo_root: Path, path: str, pattern: str, symbol: str) -> dict[str, Any]:
    lines = (repo_root / path).read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines, start=1):
        if pattern in line:
            return {"path": path, "line": index, "symbol": symbol, "pattern": pattern}
    raise RuntimeError(f"Could not find pattern {pattern!r} in {path}")


def _source_head(repo_root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:  # noqa: BLE001 - provenance is best-effort for generated artifacts.
        return "unknown"


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 Claim Safety",
        "",
        f"- Status: `{manifest['status']}`",
        f"- Formal performance claim allowed: `{manifest['formal_performance_claim_allowed']}`",
        "",
        "## Formal Performance Blockers",
        "",
    ]
    if manifest["formal_performance_blockers"]:
        for blocker in manifest["formal_performance_blockers"]:
            lines.append(f"- {blocker}")
    else:
        lines.append("- none")
    lines.extend(["", "## Allowed Claims", ""])
    for claim in manifest["allowed_claims"]:
        lines.append(f"- `{claim['claim_id']}` ({claim['scope']}): {claim['claim_text']}")
        lines.append(f"  - qualifier: {claim['required_qualifier']}")
    lines.extend(["", "## Conditional Claims", ""])
    for claim in manifest["conditional_claims"]:
        lines.append(f"- `{claim['claim_id']}`: {claim['status']}")
    lines.extend(["", "## Prohibited Claims", ""])
    for claim in manifest["prohibited_claims"]:
        lines.append(f"- `{claim['claim_id']}`: not allowed; patterns={', '.join(claim['patterns'])}")
    lines.extend(["", "## Draft Audit", ""])
    draft = manifest["draft_audit"]
    lines.append(f"- status: `{draft['status']}`")
    for violation in draft["violations"]:
        lines.append(f"- violation `{violation['claim_id']}`: {', '.join(violation['matched_patterns'])}")
    lines.extend(["", "## Claim Boundaries", ""])
    for boundary in manifest["claim_boundaries"]:
        lines.append(f"- {boundary}")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
