from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence


DEFAULT_OUTPUT_DIR = Path("0_trials/module2_method_algorithms")


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    repo_root = _repo_root()
    manifest = build_manifest(repo_root=repo_root)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_out = args.manifest_out or output_dir / "module2_method_algorithms.json"
    markdown_out = args.markdown_out or output_dir / "module2_method_algorithms.md"
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_out.write_text(_markdown(manifest), encoding="utf-8")
    print(
        json.dumps(
            {"manifest": str(manifest_out), "markdown": str(markdown_out), "status": manifest["status"]},
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


def build_manifest(*, repo_root: Path) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "artifact_name": "module2_method_algorithms",
        "status": "code_anchored",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "source_head": _source_head(repo_root),
        "formal_claim_allowed": False,
        "local_training_allowed": False,
        "remote_training_resource": "gpu3070ti-relay",
        "algorithms": [
            _rl_rs_funnel_algorithm(repo_root),
            _training_environment_algorithm(repo_root),
        ],
        "claim_boundaries": [
            "This artifact is a code-anchored method description, not a formal result.",
            "F02.6 warm-start decision remains pending; formal PPO runs must not be claimed until that decision is approved and logged.",
            "Local PPO training is disallowed; formal training must run on gpu3070ti-relay or another explicitly approved remote GPU.",
            "The ppo_analytic_operator and ppo_rs_funnel paper claims remain blocked until a real RL-RS checkpoint is available.",
            "Algorithm 1 includes fallback semantics: returning None from the custom operator does not mean planner failure; it hands control back to normal Hybrid A* expansion.",
        ],
    }


def _rl_rs_funnel_algorithm(repo_root: Path) -> dict[str, Any]:
    planner = "2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py"
    operator = "2_experiment/forest_n3p/rl_rs/operator.py"
    env = "2_experiment/forest_n3p/rl_rs/env.py"
    terminal = "2_experiment/forest_n3p/rl_rs/terminal.py"
    checkpoint = "2_experiment/forest_n3p/rl_rs/checkpoint_operator.py"
    main_eval = "2_experiment/forest_n3p/main_evaluation.py"
    return {
        "algorithm_id": "rl_rs_funnel_analytic_expansion",
        "title": "Algorithm 1: RL-RS funnel analytic expansion inside Hybrid A*",
        "intent": "Replace the hand-crafted analytic RS expansion attempt with a learned steering rollout, then certify the rollout end with terminal RS before accepting the shortcut.",
        "paper_claim": "The learned component is an analytic-expansion operator, not a standalone global planner.",
        "steps": [
            {
                "step_id": "A1.1",
                "action": "Instantiate HybridAStarPlanner with a custom analytic_expansion_operator; the planner records the operator name and routes analytic expansion attempts through the custom hook.",
                "code_anchors": [
                    _anchor(repo_root, planner, "analytic_expansion_operator=None", "HybridAStarPlanner.__init__"),
                    _anchor(repo_root, planner, "self.analytic_expansion_operator = analytic_expansion_operator", "HybridAStarPlanner.__init__"),
                    _anchor(repo_root, main_eval, "RL_RS_OPERATOR_METHODS = (", "main_evaluation.RL_RS_OPERATOR_METHODS"),
                ],
            },
            {
                "step_id": "A1.2",
                "action": "During analytic expansion, dispatch to HybridAStarPlanner._try_custom_analytic_expansion when a custom operator exists.",
                "code_anchors": [
                    _anchor(repo_root, planner, "return self._try_custom_analytic_expansion(state, goal)", "HybridAStarPlanner._try_analytic_expansion"),
                    _anchor(repo_root, planner, "result = self.analytic_expansion_operator.try_connect", "HybridAStarPlanner._try_custom_analytic_expansion"),
                ],
            },
            {
                "step_id": "A1.3",
                "action": "Load a checkpoint-backed policy into RlRsFunnelOperator; the checkpoint SHA256 is captured as method provenance.",
                "code_anchors": [
                    _anchor(repo_root, checkpoint, "def load_rl_rs_funnel_operator_from_checkpoint", "load_rl_rs_funnel_operator_from_checkpoint"),
                    _anchor(repo_root, checkpoint, "sha256 = file_sha256(path)", "load_rl_rs_funnel_operator_from_checkpoint"),
                    _anchor(repo_root, checkpoint, "return RlRsFunnelOperator(", "load_rl_rs_funnel_operator_from_checkpoint"),
                ],
            },
            {
                "step_id": "A1.4",
                "action": "Convert the current Hybrid A* node and goal into AnalyticExpansionContext, reset AnalyticExpansionEnv, and start the rollout from the planner state.",
                "code_anchors": [
                    _anchor(repo_root, operator, "def try_connect(", "RlRsFunnelOperator.try_connect"),
                    _anchor(repo_root, operator, "env_context = self._env_context", "RlRsFunnelOperator.try_connect"),
                    _anchor(repo_root, operator, "observation = env.reset(env_context)", "RlRsFunnelOperator.try_connect"),
                    _anchor(repo_root, env, "def reset(", "AnalyticExpansionEnv.reset"),
                ],
            },
            {
                "step_id": "A1.5",
                "action": "Iteratively query the RL action policy, apply one constant-steer primitive, update observation, and stop only on terminal/truncated signals.",
                "code_anchors": [
                    _anchor(repo_root, operator, "step = env.step(self.action_policy(observation))", "RlRsFunnelOperator.try_connect"),
                    _anchor(repo_root, operator, "rollout_states.append(step.next_state)", "RlRsFunnelOperator.try_connect"),
                    _anchor(repo_root, env, "def step(", "AnalyticExpansionEnv.step"),
                    _anchor(repo_root, env, "rollout = rollout_constant_steer_step(", "AnalyticExpansionEnv.step"),
                ],
            },
            {
                "step_id": "A1.6",
                "action": "Use terminal RS as the acceptance certificate for the learned rollout when append_terminal_rs is enabled.",
                "code_anchors": [
                    _anchor(repo_root, env, "check_terminal_rs_connectable(", "AnalyticExpansionEnv.step"),
                    _anchor(repo_root, terminal, "def check_terminal_rs_connectable", "check_terminal_rs_connectable"),
                    _anchor(repo_root, operator, "if step.terminal_rs.success:", "RlRsFunnelOperator.try_connect"),
                    _anchor(repo_root, operator, "terminal_rs_used=True", "RlRsFunnelOperator.try_connect"),
                ],
            },
            {
                "step_id": "A1.7",
                "action": "Record fallback_to_builtin_search_on_none: if the learned/terminal-RS operator cannot certify a shortcut, it returns None and Hybrid A* continues normal search instead of accepting an unsafe path.",
                "code_anchors": [
                    _anchor(repo_root, operator, "return None", "RlRsFunnelOperator.try_connect"),
                    _anchor(
                        repo_root,
                        planner,
                        "if result is None:",
                        "HybridAStarPlanner._try_custom_analytic_expansion",
                        after="result = self.analytic_expansion_operator.try_connect",
                    ),
                    _anchor(repo_root, planner, "return None", "HybridAStarPlanner._try_custom_analytic_expansion", after="if result is None:"),
                ],
            },
            {
                "step_id": "A1.8",
                "action": "Expose two formal method variants: ppo_rs_funnel keeps terminal RS appended, while ppo_analytic_operator disables terminal RS append and evaluates the learned operator alone.",
                "code_anchors": [
                    _anchor(repo_root, main_eval, 'elif method == "ha_rl_rs_ppo":', "_run_hybrid_a_operator"),
                    _anchor(repo_root, main_eval, "append_terminal_rs=True", "_load_module2_rl_rs_operator"),
                    _anchor(repo_root, main_eval, 'elif method == "ppo_analytic_operator":', "_run_hybrid_a_operator"),
                    _anchor(repo_root, main_eval, "append_terminal_rs=False", "_load_module2_ppo_analytic_operator"),
                ],
            },
        ],
    }


def _training_environment_algorithm(repo_root: Path) -> dict[str, Any]:
    env = "2_experiment/forest_n3p/rl_rs/env.py"
    gym_env = "2_experiment/forest_n3p/rl_rs/gym_env.py"
    obs = "2_experiment/forest_n3p/rl_rs/obs.py"
    reward = "2_experiment/forest_n3p/rl_rs/reward.py"
    terminal = "2_experiment/forest_n3p/rl_rs/terminal.py"
    return {
        "algorithm_id": "analytic_expansion_training_environment",
        "title": "Algorithm 2: PPO training environment for analytic expansion",
        "intent": "Train a continuous steering policy on the same planner-side analytic expansion surface used at evaluation time.",
        "paper_claim": "The environment optimizes a local analytic-expansion policy with terminal-RS-aware reward shaping; it is not a separate end-to-end navigation policy.",
        "steps": [
            {
                "step_id": "A2.1",
                "action": "Create a GymAnalyticExpansionEnv around a context sampler; reset samples an AnalyticExpansionContext and forwards it to the planner-side environment.",
                "code_anchors": [
                    _anchor(repo_root, gym_env, "class GymAnalyticExpansionEnv", "GymAnalyticExpansionEnv"),
                    _anchor(repo_root, gym_env, "context = _context_from_options(options) or self.context_sampler", "GymAnalyticExpansionEnv.reset"),
                    _anchor(repo_root, gym_env, "observation = self._planner_env.reset(context)", "GymAnalyticExpansionEnv.reset"),
                ],
            },
            {
                "step_id": "A2.2",
                "action": "Represent observations as scalar geometry plus an egocentric occupancy/EDT patch.",
                "code_anchors": [
                    _anchor(repo_root, obs, "class ObservationConfig", "ObservationConfig"),
                    _anchor(repo_root, obs, "def build_scalar_observation", "build_scalar_observation"),
                    _anchor(repo_root, obs, "def build_patch_observation", "build_patch_observation"),
                    _anchor(repo_root, obs, "def build_observation", "build_observation"),
                ],
            },
            {
                "step_id": "A2.3",
                "action": "Define a single continuous normalized steering action and apply it through the same AnalyticExpansionEnv.step used by Algorithm 1.",
                "code_anchors": [
                    _anchor(repo_root, gym_env, "self.action_space = spaces.Box", "GymAnalyticExpansionEnv.__init__"),
                    _anchor(repo_root, gym_env, "normalized_steering = _single_action_value(action)", "GymAnalyticExpansionEnv.step"),
                    _anchor(repo_root, gym_env, "step = self._planner_env.step", "GymAnalyticExpansionEnv.step"),
                    _anchor(repo_root, env, "def step(", "AnalyticExpansionEnv.step"),
                ],
            },
            {
                "step_id": "A2.4",
                "action": "Evaluate each rollout primitive with collision checks, no-progress/oscillation truncation, and terminal RS reachability.",
                "code_anchors": [
                    _anchor(repo_root, env, "rollout = rollout_constant_steer_step(", "AnalyticExpansionEnv.step"),
                    _anchor(repo_root, env, "no_progress = (", "AnalyticExpansionEnv.step"),
                    _anchor(repo_root, env, "oscillation = _detect_oscillation(", "AnalyticExpansionEnv.step"),
                    _anchor(repo_root, terminal, "def check_terminal_rs_connectable", "check_terminal_rs_connectable"),
                ],
            },
            {
                "step_id": "A2.5",
                "action": "Compute decomposed reward terms for success, terminal failure, collision, goal progress, RS-distance progress, clearance, curvature change, path length, and step cost.",
                "code_anchors": [
                    _anchor(repo_root, env, "reward=compute_decomposed_reward(", "AnalyticExpansionEnv.step"),
                    _anchor(repo_root, reward, "def compute_decomposed_reward", "compute_decomposed_reward"),
                    _anchor(repo_root, reward, "total = success + terminal + collision + progress + rs_progress + clearance + curvature + path_length + step", "compute_decomposed_reward"),
                ],
            },
            {
                "step_id": "A2.6",
                "action": "Return Gymnasium observation, scalar reward, terminated/truncated flags, and telemetry info for PPO training logs.",
                "code_anchors": [
                    _anchor(repo_root, gym_env, "reward = float(step.reward.total)", "GymAnalyticExpansionEnv.step"),
                    _anchor(repo_root, gym_env, "terminated = bool(step.terminated)", "GymAnalyticExpansionEnv.step"),
                    _anchor(repo_root, gym_env, "return observation, reward, terminated, truncated, info", "GymAnalyticExpansionEnv.step"),
                ],
            },
            {
                "step_id": "A2.7",
                "action": "Enforce local_training_disallowed for this artifact: it documents the code contract only; PPO execution belongs on gpu3070ti-relay after F02.6 approval.",
                "code_anchors": [
                    _anchor(repo_root, gym_env, "class GymAnalyticExpansionEnv", "GymAnalyticExpansionEnv"),
                    _anchor(repo_root, reward, "def compute_decomposed_reward", "compute_decomposed_reward"),
                ],
            },
        ],
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build code-anchored Module2 method algorithms.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
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


def _markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Module2 Method Algorithms",
        "",
        f"- Status: `{manifest['status']}`",
        f"- Source head: `{manifest['source_head']}`",
        f"- Formal claim allowed: `{manifest['formal_claim_allowed']}`",
        f"- Local training allowed: `{manifest['local_training_allowed']}`",
        f"- Remote training resource: `{manifest['remote_training_resource']}`",
        "",
        "## Claim Boundaries",
        "",
    ]
    for boundary in manifest["claim_boundaries"]:
        lines.append(f"- {boundary}")
    lines.append("")

    for index, algorithm in enumerate(manifest["algorithms"], start=1):
        lines.extend(
            [
                f"## Algorithm {index}: {algorithm['title'].split(': ', 1)[-1]}",
                "",
                f"Intent: {algorithm['intent']}",
                "",
                f"Paper claim: {algorithm['paper_claim']}",
                "",
                "| Step | Action | Code anchors |",
                "| --- | --- | --- |",
            ]
        )
        for step in algorithm["steps"]:
            anchors = "<br>".join(
                f"`{anchor['path']}:{anchor['line']}` `{anchor['symbol']}`"
                for anchor in step["code_anchors"]
            )
            lines.append(f"| `{step['step_id']}` | {step['action']} | {anchors} |")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
