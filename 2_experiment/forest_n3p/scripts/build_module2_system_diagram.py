from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from html import escape
from pathlib import Path
from typing import Any, Sequence


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_system_diagram")


@dataclass(frozen=True)
class DiagramNode:
    node_id: str
    title: str
    subtitle: str
    x: int
    y: int
    width: int
    height: int
    fill_color: str
    code_anchors: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class DiagramEdge:
    source: str
    target: str
    semantic: str
    label: str = ""
    dashed: bool = False


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    repo_root = _repo_root()
    manifest = build_manifest(repo_root=repo_root)
    drawio = _drawio(manifest)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = args.manifest_out or output_dir / "module2_system_diagram.json"
    markdown_out = args.markdown_out or output_dir / "module2_system_diagram.md"
    drawio_out = args.drawio_out or output_dir / "module2_system_diagram.drawio"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    drawio_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    drawio_out.write_text(drawio, encoding="utf-8")
    print(
        json.dumps(
            {
                "manifest": str(manifest_out),
                "markdown": str(markdown_out),
                "drawio": str(drawio_out),
                "status": manifest["status"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


def build_manifest(*, repo_root: Path) -> dict[str, Any]:
    nodes = _nodes(repo_root)
    edges = _edges()
    return {
        "schema_version": 1,
        "artifact_name": "module2_system_diagram",
        "status": "code_anchored_drawio",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(repo_root),
        "formal_claim_allowed": False,
        "local_training_allowed": False,
        "remote_training_resource": "gpu3070ti-relay",
        "figure_title": "Figure: RL-RS analytic expansion system inside Hybrid A*",
        "figure_intent": "Show that Module2 is a learned analytic-expansion operator inside Hybrid A*, with terminal RS certification and primitive fallback, not a standalone RL planner.",
        "nodes": [_node_record(node) for node in nodes],
        "edges": [_edge_record(edge) for edge in edges],
        "claim_boundaries": [
            "This system diagram is a code-anchored method artifact, not a formal result.",
            "F02.6 warm-start decision remains pending; obstacle-summary warm-start is not approved until Dr Sun closes that decision.",
            "The ppo_analytic_operator and ppo_rs_funnel branches still require a real PPO checkpoint before formal H01/H02 evaluation.",
            "Local PPO training is disallowed; formal training must run on gpu3070ti-relay or another explicitly approved remote GPU.",
            "Fallback primitive expansion is part of the safety semantics: a custom operator returning None must not be relabeled as planner failure.",
        ],
    }


def _nodes(repo_root: Path) -> tuple[DiagramNode, ...]:
    planner = "2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py"
    operator = "2_experiment/forest_n3p/rl_rs/operator.py"
    env = "2_experiment/forest_n3p/rl_rs/env.py"
    terminal = "2_experiment/forest_n3p/rl_rs/terminal.py"
    checkpoint = "2_experiment/forest_n3p/rl_rs/checkpoint_operator.py"
    gym_env = "2_experiment/forest_n3p/rl_rs/gym_env.py"
    obs = "2_experiment/forest_n3p/rl_rs/obs.py"
    reward = "2_experiment/forest_n3p/rl_rs/reward.py"
    main_eval = "2_experiment/forest_n3p/main_evaluation.py"
    h01 = "2_experiment/forest_n3p/scripts/build_module2_evaluation_manifest.py"
    return (
        DiagramNode(
            node_id="hybrid_astar_loop",
            title="Hybrid A* search loop",
            subtitle="Open/closed search; primitive fallback remains authoritative",
            x=60,
            y=140,
            width=190,
            height=70,
            fill_color="#FFFFFF",
            code_anchors=(
                _anchor(repo_root, planner, "def plan(", "HybridAStarPlanner.plan"),
                _anchor(repo_root, planner, "for prim in self.primitives:", "HybridAStarPlanner.plan"),
            ),
        ),
        DiagramNode(
            node_id="analytic_trigger",
            title="Analytic expansion trigger",
            subtitle="Distance-scaled interval decides when to try a shortcut",
            x=300,
            y=140,
            width=190,
            height=70,
            fill_color="#FFF2CC",
            code_anchors=(
                _anchor(repo_root, planner, "def _analytic_interval", "HybridAStarPlanner._analytic_interval"),
                _anchor(repo_root, planner, "if interval > 0 and expansion_idx % interval == 0", "HybridAStarPlanner.plan"),
            ),
        ),
        DiagramNode(
            node_id="custom_operator_dispatch",
            title="Custom analytic operator dispatch",
            subtitle="Call custom operator when provided; otherwise built-in RS",
            x=540,
            y=140,
            width=210,
            height=70,
            fill_color="#DAE8FC",
            code_anchors=(
                _anchor(repo_root, planner, "analytic_expansion_operator=None", "HybridAStarPlanner.__init__"),
                _anchor(repo_root, planner, "return self._try_custom_analytic_expansion(state, goal)", "HybridAStarPlanner._try_analytic_expansion"),
                _anchor(repo_root, planner, "result = self.analytic_expansion_operator.try_connect", "HybridAStarPlanner._try_custom_analytic_expansion"),
            ),
        ),
        DiagramNode(
            node_id="rl_rs_funnel_operator",
            title="RL-RS funnel operator",
            subtitle="Checkpoint policy rolls out timed steering from current HA* node",
            x=810,
            y=140,
            width=210,
            height=70,
            fill_color="#D5E8D4",
            code_anchors=(
                _anchor(repo_root, operator, "class RlRsFunnelOperator", "RlRsFunnelOperator"),
                _anchor(repo_root, operator, "def try_connect(", "RlRsFunnelOperator.try_connect"),
                _anchor(repo_root, operator, "step = env.step(action, nn_forward_time_s=policy_elapsed)", "RlRsFunnelOperator.try_connect"),
            ),
        ),
        DiagramNode(
            node_id="rl_rollout_env",
            title="Planner-side RL rollout env",
            subtitle="Shared Ackermann rollout, collision, no-progress, reward terms",
            x=810,
            y=260,
            width=210,
            height=86,
            fill_color="#E1D5E7",
            code_anchors=(
                _anchor(repo_root, env, "class AnalyticExpansionEnv", "AnalyticExpansionEnv"),
                _anchor(repo_root, env, "def reset(", "AnalyticExpansionEnv.reset"),
                _anchor(repo_root, env, "def step(", "AnalyticExpansionEnv.step"),
                _anchor(repo_root, env, "reward=compute_decomposed_reward(", "AnalyticExpansionEnv.step"),
            ),
        ),
        DiagramNode(
            node_id="terminal_rs_certificate",
            title="Terminal RS certificate",
            subtitle="Only accept a learned shortcut after RS-connectable check",
            x=540,
            y=260,
            width=210,
            height=86,
            fill_color="#F8CECC",
            code_anchors=(
                _anchor(repo_root, env, "check_terminal_rs_connectable(", "AnalyticExpansionEnv.step"),
                _anchor(repo_root, terminal, "def check_terminal_rs_connectable", "check_terminal_rs_connectable"),
                _anchor(repo_root, operator, "if step.terminal_rs.success:", "RlRsFunnelOperator.try_connect"),
            ),
        ),
        DiagramNode(
            node_id="accept_shortcut",
            title="Accept shortcut",
            subtitle="Return states/actions to HA* trace path when certified",
            x=300,
            y=270,
            width=190,
            height=70,
            fill_color="#D5E8D4",
            code_anchors=(
                _anchor(repo_root, operator, "return AnalyticExpansionResult(", "RlRsFunnelOperator.try_connect"),
                _anchor(repo_root, planner, "return result.to_legacy_tuple()", "HybridAStarPlanner._try_custom_analytic_expansion"),
            ),
        ),
        DiagramNode(
            node_id="fallback_primitives",
            title="Fallback primitive expansion",
            subtitle="None means no certified shortcut; HA* continues primitive search",
            x=60,
            y=270,
            width=190,
            height=70,
            fill_color="#F5F5F5",
            code_anchors=(
                _anchor(repo_root, operator, "return None", "RlRsFunnelOperator.try_connect"),
                _anchor(repo_root, planner, "if result is None:", "HybridAStarPlanner._try_custom_analytic_expansion", after="result = self.analytic_expansion_operator.try_connect"),
                _anchor(repo_root, planner, "for prim in self.primitives:", "HybridAStarPlanner.plan"),
            ),
        ),
        DiagramNode(
            node_id="gym_training_env",
            title="PPO training environment",
            subtitle="Gym adapter: scalar + occupancy/EDT patch, single steering action",
            x=810,
            y=430,
            width=210,
            height=86,
            fill_color="#DAE8FC",
            code_anchors=(
                _anchor(repo_root, gym_env, "class GymAnalyticExpansionEnv", "GymAnalyticExpansionEnv"),
                _anchor(repo_root, gym_env, "self.action_space = spaces.Box", "GymAnalyticExpansionEnv.__init__"),
                _anchor(repo_root, obs, "def build_observation", "build_observation"),
                _anchor(repo_root, reward, "def compute_decomposed_reward", "compute_decomposed_reward"),
            ),
        ),
        DiagramNode(
            node_id="checkpointed_policy",
            title="Checkpointed policy variants",
            subtitle="BC ready; PPO checkpoint missing until remote formal training",
            x=540,
            y=430,
            width=210,
            height=86,
            fill_color="#FFE6CC",
            code_anchors=(
                _anchor(repo_root, checkpoint, "def load_rl_rs_funnel_operator_from_checkpoint", "load_rl_rs_funnel_operator_from_checkpoint"),
                _anchor(repo_root, checkpoint, "def load_bc_funnel_operator_from_checkpoint", "load_bc_funnel_operator_from_checkpoint"),
                _anchor(repo_root, main_eval, "RL_RS_OPERATOR_METHODS = (", "main_evaluation.RL_RS_OPERATOR_METHODS"),
            ),
        ),
        DiagramNode(
            node_id="formal_evaluation_boundary",
            title="Formal evaluation boundary",
            subtitle="H01/H02 blocked: F02.6 pending + PPO checkpoint missing",
            x=270,
            y=430,
            width=220,
            height=86,
            fill_color="#F8CECC",
            code_anchors=(
                _anchor(repo_root, main_eval, 'elif method == "ha_rl_rs_ppo":', "_run_hybrid_a_operator"),
                _anchor(repo_root, main_eval, 'elif method == "ppo_analytic_operator":', "_run_hybrid_a_operator"),
                _anchor(repo_root, h01, "f02_6_decision_packet_pending", "build_module2_evaluation_manifest"),
            ),
        ),
    )


def _edges() -> tuple[DiagramEdge, ...]:
    return (
        DiagramEdge("hybrid_astar_loop", "analytic_trigger", "attempt_schedule", "interval"),
        DiagramEdge("analytic_trigger", "custom_operator_dispatch", "try_analytic_expansion", "try"),
        DiagramEdge("custom_operator_dispatch", "rl_rs_funnel_operator", "custom_operator", "operator"),
        DiagramEdge("rl_rs_funnel_operator", "rl_rollout_env", "rollout_step", "policy step"),
        DiagramEdge("rl_rollout_env", "terminal_rs_certificate", "terminal_check", "RS check"),
        DiagramEdge("terminal_rs_certificate", "accept_shortcut", "certified_success", "success"),
        DiagramEdge("terminal_rs_certificate", "fallback_primitives", "return_none_fallback", "fail / None", dashed=True),
        DiagramEdge("fallback_primitives", "hybrid_astar_loop", "continue_search", "continue", dashed=True),
        DiagramEdge("gym_training_env", "checkpointed_policy", "remote_training_export", "gpu3070ti-relay"),
        DiagramEdge("checkpointed_policy", "rl_rs_funnel_operator", "checkpoint_load", "load"),
        DiagramEdge("checkpointed_policy", "formal_evaluation_boundary", "formal_blocker", "PPO checkpoint missing", dashed=True),
    )


def _node_record(node: DiagramNode) -> dict[str, Any]:
    return {
        "node_id": node.node_id,
        "title": node.title,
        "subtitle": node.subtitle,
        "drawio": {
            "x": node.x,
            "y": node.y,
            "width": node.width,
            "height": node.height,
            "fill_color": node.fill_color,
        },
        "code_anchors": list(node.code_anchors),
    }


def _edge_record(edge: DiagramEdge) -> dict[str, Any]:
    return {
        "source": edge.source,
        "target": edge.target,
        "semantic": edge.semantic,
        "label": edge.label,
        "dashed": bool(edge.dashed),
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a code-anchored Draw.io system diagram for Module2.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    parser.add_argument("--drawio-out", type=Path, default=None)
    return parser.parse_args(list(argv) if argv is not None else None)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _anchor(
    repo_root: Path,
    path: str,
    pattern: str,
    symbol: str,
    *,
    after: str | None = None,
) -> dict[str, Any]:
    file_path = repo_root / path
    lines = file_path.read_text(encoding="utf-8").splitlines()
    start_index = 0
    if after is not None:
        start_index = _find_line_index(lines, after, path) + 1
    line_index = _find_line_index(lines[start_index:], pattern, path) + start_index
    return {
        "path": path,
        "line": int(line_index + 1),
        "symbol": symbol,
        "pattern": pattern,
    }


def _find_line_index(lines: Sequence[str], pattern: str, path: str) -> int:
    for index, line in enumerate(lines):
        if pattern in line:
            return index
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


def _drawio(manifest: dict[str, Any]) -> str:
    node_drawio_ids = {node["node_id"]: f"n{index}" for index, node in enumerate(manifest["nodes"], start=1)}
    edge_start = len(node_drawio_ids) + 1
    cells = [
        '<mxCell id="0"/>',
        '<mxCell id="1" parent="0"/>',
        _vertex_cell(
            "title",
            "RL-RS analytic expansion system inside Hybrid A*",
            60,
            40,
            960,
            50,
            "#FFFFFF",
            "fontSize=18;fontStyle=1;strokeColor=none;",
        ),
        _vertex_cell(
            "boundary",
            "Method artifact only | F02.6 pending | PPO checkpoint missing | Formal training on gpu3070ti-relay",
            60,
            95,
            960,
            34,
            "#FFF2CC",
            "fontSize=12;strokeColor=#D6B656;rounded=1;",
        ),
    ]

    for node in manifest["nodes"]:
        drawio = node["drawio"]
        label = f"{node['title']}\n{node['subtitle']}"
        style = (
            "rounded=1;whiteSpace=wrap;html=1;strokeColor=#333333;strokeWidth=1;"
            f"fillColor={drawio['fill_color']};fontColor=#333333;fontSize=12;"
        )
        cells.append(
            _vertex_cell(
                node_drawio_ids[node["node_id"]],
                label,
                int(drawio["x"]),
                int(drawio["y"]),
                int(drawio["width"]),
                int(drawio["height"]),
                str(drawio["fill_color"]),
                style,
            )
        )

    for index, edge in enumerate(manifest["edges"], start=edge_start):
        cells.append(
            _edge_cell(
                f"e{index}",
                str(edge["label"]),
                node_drawio_ids[str(edge["source"])],
                node_drawio_ids[str(edge["target"])],
                dashed=bool(edge["dashed"]),
            )
        )

    cell_xml = "\n        ".join(cells)
    return (
        '<mxfile host="app.diagrams.net">\n'
        '  <diagram name="Module2 System" id="module2-system-diagram">\n'
        '    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" '
        'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1100" pageHeight="600" background="#FFFFFF">\n'
        "      <root>\n"
        f"        {cell_xml}\n"
        "      </root>\n"
        "    </mxGraphModel>\n"
        "  </diagram>\n"
        "</mxfile>\n"
    )


def _vertex_cell(
    cell_id: str,
    label: str,
    x: int,
    y: int,
    width: int,
    height: int,
    fill_color: str,
    style: str,
) -> str:
    style_text = style
    if "fillColor=" not in style_text:
        style_text += f"fillColor={fill_color};"
    return (
        f'<mxCell id="{escape(cell_id, quote=True)}" value="{_label(label)}" style="{escape(style_text, quote=True)}" '
        'vertex="1" parent="1">\n'
        f'          <mxGeometry x="{x}" y="{y}" width="{width}" height="{height}" as="geometry"/>\n'
        "        </mxCell>"
    )


def _edge_cell(cell_id: str, label: str, source: str, target: str, *, dashed: bool = False) -> str:
    dashed_style = "dashed=1;" if dashed else ""
    style = (
        "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#333333;strokeWidth=2;"
        f"{dashed_style}endArrow=classic;"
    )
    return (
        f'<mxCell id="{escape(cell_id, quote=True)}" value="{_label(label)}" style="{escape(style, quote=True)}" '
        f'edge="1" parent="1" source="{escape(source, quote=True)}" target="{escape(target, quote=True)}">\n'
        '          <mxGeometry relative="1" as="geometry"/>\n'
        "        </mxCell>"
    )


def _label(value: str) -> str:
    return escape(value, quote=True).replace("\n", "&lt;br&gt;")


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 System Diagram",
        "",
        f"- Status: `{manifest['status']}`",
        f"- Source head: `{manifest['source_head']}`",
        f"- Figure: {manifest['figure_title']}",
        f"- Formal claim allowed: `{manifest['formal_claim_allowed']}`",
        f"- Local training allowed: `{manifest['local_training_allowed']}`",
        f"- Remote training resource: `{manifest['remote_training_resource']}`",
        "",
        "## Figure Caption",
        "",
        "Figure: RL-RS analytic expansion system inside Hybrid A*. The learned policy is used only as an analytic-expansion operator. A terminal RS certificate is required before accepting the shortcut; otherwise the planner falls back to primitive expansion.",
        "",
        "## Nodes And Anchors",
        "",
        "| Node | Role | Code anchors |",
        "| --- | --- | --- |",
    ]
    for node in manifest["nodes"]:
        anchors = "<br>".join(
            f"`{anchor['path']}:{anchor['line']}` `{anchor['symbol']}`" for anchor in node["code_anchors"]
        )
        lines.append(f"| `{node['node_id']}` | {node['title']}: {node['subtitle']} | {anchors} |")
    lines.extend(["", "## Claim Boundaries", ""])
    for boundary in manifest["claim_boundaries"]:
        lines.append(f"- {boundary}")
    lines.append("")
    lines.append("Draw.io file: `0_trials/module2_system_diagram/module2_system_diagram.drawio`.")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
