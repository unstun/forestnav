#!/usr/bin/env python3
"""Run official Dynoplan car1_v0 smoke experiments and draw trajectories."""

from __future__ import annotations

import argparse
import csv
import subprocess
import time
from pathlib import Path
from typing import Any, NamedTuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[3]
STRICT_ROOT = PROJECT_ROOT / "2_experiment" / "idb_rrt_strict_repro"
SURVEY_DYNOPLAN_ROOT = (
    PROJECT_ROOT / "1_survey" / "papers" / "baselines" / "OrtizHaro2024_iDbRRT" / "repo" / "dynoplan"
)
DEFAULT_UPSTREAM_ROOT = STRICT_ROOT / "upstream" / "dynoplan"
DEFAULT_OUT_DIR = STRICT_ROOT / "outputs" / "2026-05-15_official_car1_smoke"
DEFAULT_PROBLEMS = ("parallelpark_0", "kink_0", "bugtrap_0")


class ParsedTrajectory(NamedTuple):
    xy: list[tuple[float, float]]
    duration_s: float
    state_count: int


def default_dynoplan_root() -> Path:
    if DEFAULT_UPSTREAM_ROOT.is_dir():
        return DEFAULT_UPSTREAM_ROOT
    return SURVEY_DYNOPLAN_ROOT


def find_car1_motion_file(dynoplan_root: Path) -> Path:
    candidates = [
        dynoplan_root / "dynomotions" / "car1_v0_all.bin.sp.bin.small5000.msgpack",
        dynoplan_root / "dynomotions_full" / "car1_v0_all.bin.sp.bin.msgpack",
        dynoplan_root
        / "dynobench"
        / "envs"
        / "car1_v0"
        / "motions"
        / "car1_v0_all.bin.sp.bin.small.msgpack",
    ]
    for path in candidates:
        if path.is_file():
            return path
    searched = "\n".join(str(p) for p in candidates)
    raise FileNotFoundError(f"car1_v0 motion primitive file not found. Searched:\n{searched}")


def build_idbastar_cfg(*, motion_file: Path, timelimit_s: float, seed: int) -> dict[str, Any]:
    return {
        "solver_id": 1,
        "search_timelimit": int(round(float(timelimit_s) * 1000.0)),
        "timelimit": float(timelimit_s),
        "use_nigh_nn": True,
        "cost_delta_factor": 1,
        "smooth_traj": True,
        "motionsFile": str(motion_file),
        "num_primitives_0": 400,
        "delta_0": 0.5,
        "delta": 0.5,
        "max_motions_primitives": 20_000,
        "max_it": 3,
        "new_schedule": True,
        "add_primitives_opt": True,
        "max_iter": 100,
        "weight_goal": 200,
        "control_bounds": True,
        "use_warmstart": True,
        "fix_seed": True,
        "seed": int(seed),
    }


def parse_traj_solution(traj_file: Path) -> ParsedTrajectory:
    payload = yaml.safe_load(traj_file.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Trajectory YAML root must be an object: {traj_file}")
    states = payload.get("states")
    if not isinstance(states, list) or not states:
        raise ValueError(f"Trajectory has no states: {traj_file}")
    xy = [(float(state[0]), float(state[1])) for state in states]
    times = payload.get("times")
    if isinstance(times, list) and times:
        duration_s = float(times[-1])
    elif "cost" in payload:
        duration_s = float(payload["cost"])
    else:
        duration_s = float(max(0, len(states) - 1))
    return ParsedTrajectory(xy=xy, duration_s=duration_s, state_count=len(states))


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"YAML root must be an object: {path}")
    return payload


def render_problem_plot(
    *,
    env_file: Path,
    xy: list[tuple[float, float]],
    output_png: Path,
    title: str,
) -> None:
    env = _load_yaml(env_file)
    environment = env.get("environment", {})
    robots = env.get("robots", [])
    if not isinstance(environment, dict) or not isinstance(robots, list) or not robots:
        raise ValueError(f"Invalid Dynobench environment file: {env_file}")

    fig, ax = plt.subplots(figsize=(7.0, 5.0), dpi=160)
    for obstacle in environment.get("obstacles", []):
        if not isinstance(obstacle, dict) or obstacle.get("type") != "box":
            continue
        cx, cy = (float(v) for v in obstacle["center"])
        sx, sy = (float(v) for v in obstacle["size"])
        ax.add_patch(
            Rectangle(
                (cx - 0.5 * sx, cy - 0.5 * sy),
                sx,
                sy,
                facecolor="#555555",
                edgecolor="#222222",
                alpha=0.85,
            )
        )

    robot = robots[0]
    start = robot["start"]
    goal = robot["goal"]
    ax.scatter([float(start[0])], [float(start[1])], c="#1677b3", s=50, label="start", zorder=4)
    ax.scatter([float(goal[0])], [float(goal[1])], c="#d94a38", s=50, label="goal", zorder=4)
    if xy:
        xs, ys = zip(*xy)
        ax.plot(xs, ys, color="#f08a24", linewidth=2.2, label="official trajectory", zorder=3)
        ax.scatter([xs[-1]], [ys[-1]], c="#f08a24", s=28, zorder=5)

    bounds_min = environment.get("min", [0.0, 0.0])
    bounds_max = environment.get("max", [1.0, 1.0])
    ax.set_xlim(float(bounds_min[0]) - 0.2, float(bounds_max[0]) + 0.2)
    ax.set_ylim(float(bounds_min[1]) - 0.2, float(bounds_max[1]) + 0.2)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title(title)
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.grid(True, linewidth=0.4, alpha=0.35)
    ax.legend(loc="best", fontsize=8)
    output_png.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_png)
    plt.close(fig)


def _git_commit(path: Path) -> str:
    completed = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return "unknown"
    return completed.stdout.strip()


def _run_one_problem(
    *,
    dynoplan_root: Path,
    build_dir: Path,
    out_dir: Path,
    problem: str,
    timelimit_s: float,
    seed: int,
    motion_file: Path,
) -> dict[str, Any]:
    binary = build_dir / "main_idbastar"
    if not binary.is_file():
        raise FileNotFoundError(f"main_idbastar not found: {binary}")

    env_file = dynoplan_root / "dynobench" / "envs" / "car1_v0" / f"{problem}.yaml"
    if not env_file.is_file():
        raise FileNotFoundError(f"car1_v0 problem not found: {env_file}")

    raw_dir = out_dir / "raw" / problem
    raw_dir.mkdir(parents=True, exist_ok=True)
    cfg_file = raw_dir / "idbastar_car1.cfg.yaml"
    result_file = raw_dir / "idbastar_result.yaml"
    stdout_file = raw_dir / "stdout.txt"
    stderr_file = raw_dir / "stderr.txt"
    cfg_file.write_text(
        yaml.safe_dump(build_idbastar_cfg(motion_file=motion_file, timelimit_s=timelimit_s, seed=seed), sort_keys=False),
        encoding="utf-8",
    )

    cmd = [
        str(binary),
        "--env_file",
        str(env_file),
        "--models_base_path",
        str(dynoplan_root / "dynobench" / "models") + "/",
        "--results_file",
        str(result_file),
        "--cfg_file",
        str(cfg_file),
    ]

    started = time.perf_counter()
    completed = subprocess.run(
        cmd,
        cwd=str(build_dir),
        check=False,
        capture_output=True,
        text=True,
        timeout=max(10.0, float(timelimit_s) + 15.0),
    )
    runtime_s = time.perf_counter() - started
    stdout_file.write_text(completed.stdout, encoding="utf-8")
    stderr_file.write_text(completed.stderr, encoding="utf-8")

    traj_file = Path(str(result_file) + ".traj-sol.yaml")
    parsed: ParsedTrajectory | None = None
    image_file = out_dir / "figures" / f"car1_v0_{problem}_idbastar.png"
    parse_error = ""
    if traj_file.is_file():
        try:
            parsed = parse_traj_solution(traj_file)
            render_problem_plot(
                env_file=env_file,
                xy=parsed.xy,
                output_png=image_file,
                title=f"official Dynoplan car1_v0/{problem}",
            )
        except Exception as exc:  # pragma: no cover - recorded in RUN.md for external failures
            parse_error = f"{type(exc).__name__}: {exc}"

    reference_traj_file = env_file.parent / problem / "idbastar_v0_solution_v0.yaml"
    reference_image_file = out_dir / "figures" / f"car1_v0_{problem}_official_shipped_reference.png"
    reference_parsed: ParsedTrajectory | None = None
    reference_error = ""
    if reference_traj_file.is_file():
        try:
            reference_parsed = parse_traj_solution(reference_traj_file)
            render_problem_plot(
                env_file=env_file,
                xy=reference_parsed.xy,
                output_png=reference_image_file,
                title=f"official shipped car1_v0/{problem} reference",
            )
        except Exception as exc:  # pragma: no cover - recorded in RUN.md for external failures
            reference_error = f"{type(exc).__name__}: {exc}"

    return {
        "problem": f"car1_v0/{problem}",
        "algorithm": "main_idbastar",
        "returncode": int(completed.returncode),
        "success": bool(completed.returncode == 0 and parsed is not None),
        "runtime_s": f"{runtime_s:.6f}",
        "trajectory_duration_s": "" if parsed is None else f"{parsed.duration_s:.6f}",
        "state_count": "" if parsed is None else str(parsed.state_count),
        "env_file": str(env_file),
        "cfg_file": str(cfg_file),
        "result_file": str(result_file),
        "traj_file": str(traj_file) if traj_file.is_file() else "",
        "image_file": str(image_file) if image_file.is_file() else "",
        "stdout_file": str(stdout_file),
        "stderr_file": str(stderr_file),
        "parse_error": parse_error,
        "reference_traj_file": str(reference_traj_file) if reference_traj_file.is_file() else "",
        "reference_image_file": str(reference_image_file) if reference_image_file.is_file() else "",
        "reference_duration_s": "" if reference_parsed is None else f"{reference_parsed.duration_s:.6f}",
        "reference_state_count": "" if reference_parsed is None else str(reference_parsed.state_count),
        "reference_error": reference_error,
        "command": " ".join(cmd),
    }


def write_summary_csv(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "problem",
        "algorithm",
        "success",
        "returncode",
        "runtime_s",
        "trajectory_duration_s",
        "state_count",
        "image_file",
        "traj_file",
        "result_file",
        "parse_error",
        "reference_image_file",
        "reference_traj_file",
        "reference_duration_s",
        "reference_state_count",
        "reference_error",
        "command",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def write_run_md(
    *,
    out_dir: Path,
    dynoplan_root: Path,
    build_dir: Path,
    motion_file: Path,
    timelimit_s: float,
    seed: int,
    rows: list[dict[str, Any]],
) -> None:
    success_count = sum(1 for row in rows if row.get("success") is True)
    reference_count = sum(1 for row in rows if row.get("reference_image_file"))
    lines = [
        "# Official Dynoplan car1_v0 smoke",
        "",
        "## Scope",
        "",
        "This run uses the official Dynoplan executable and official Dynobench `car1_v0` problems.",
        "The model is `car_with_trailers`; local UGV parameters are not used.",
        "",
        "## Environment",
        "",
        f"- Dynoplan root: `{dynoplan_root}`",
        f"- Dynoplan commit: `{_git_commit(dynoplan_root)}`",
        f"- Build dir: `{build_dir}`",
        f"- Motion file: `{motion_file}`",
        f"- Time limit per problem: `{timelimit_s}` s",
        f"- Seed argument recorded by wrapper: `{seed}`",
        "",
        "## Results",
        "",
        f"- Success count: `{success_count}/{len(rows)}`",
        f"- Official shipped reference figures: `{reference_count}/{len(rows)}`",
        f"- Summary CSV: `{out_dir / 'summary.csv'}`",
        f"- Figures dir: `{out_dir / 'figures'}`",
        "",
        "| Problem | Computed success | Return code | Runtime s | Computed image | Shipped reference image |",
        "|---|---:|---:|---:|---|---|",
    ]
    for row in rows:
        image = row.get("image_file", "")
        image_text = f"`{image}`" if image else ""
        reference_image = row.get("reference_image_file", "")
        reference_image_text = f"`{reference_image}`" if reference_image else ""
        lines.append(
            "| {problem} | {success} | {returncode} | {runtime} | {image} | {reference_image} |".format(
                problem=row.get("problem", ""),
                success=row.get("success", ""),
                returncode=row.get("returncode", ""),
                runtime=row.get("runtime_s", ""),
                image=image_text,
                reference_image=reference_image_text,
            )
        )
    failed_rows = [row for row in rows if row.get("success") is not True]
    if failed_rows:
        lines += [
            "",
            "## Problems Encountered",
            "",
            "The official executable did not produce newly computed `car1_v0` trajectories in this run.",
            "Failed rows and raw stdout/stderr are kept under the ignored `raw/` directory for diagnosis.",
            "",
        ]
        for row in failed_rows:
            lines.append(
                "- `{problem}` returned `{returncode}`; stdout: `{stdout}`; stderr: `{stderr}`".format(
                    problem=row.get("problem", ""),
                    returncode=row.get("returncode", ""),
                    stdout=row.get("stdout_file", ""),
                    stderr=row.get("stderr_file", ""),
                )
            )
    lines += [
        "",
        "## Commands",
        "",
        "```bash",
        "bash 2_experiment/idb_rrt_strict_repro/scripts/run_official_car1_smoke.sh",
        "```",
        "",
        "Each row also records the exact `main_idbastar` command in `summary.csv`.",
        "",
        "## Notes",
        "",
        "- Official `main_idbastar` writes temporary debug trajectories under `/tmp/dynoplan` internally.",
        "- This smoke uses the small public `car1_v0` primitive bundle when the full Google Drive bundle is absent.",
        "- A successful row confirms the official car-with-trailer Dynobench problem ran; it does not validate a local UGV adapter.",
        "- Reference figures are rendered from solution YAML files shipped inside the official repository; they are not newly computed in this run.",
        "",
    ]
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "RUN.md").write_text("\n".join(lines), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dynoplan-root", type=Path, default=default_dynoplan_root())
    parser.add_argument("--build-dir", type=Path, default=None)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--timelimit-s", type=float, default=20.0)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--problems", nargs="+", default=list(DEFAULT_PROBLEMS))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    dynoplan_root = args.dynoplan_root.resolve()
    build_dir = (args.build_dir or dynoplan_root / "build-macos-conda-link-rpath").resolve()
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    motion_file = find_car1_motion_file(dynoplan_root).resolve()

    rows: list[dict[str, Any]] = []
    for problem in args.problems:
        rows.append(
            _run_one_problem(
                dynoplan_root=dynoplan_root,
                build_dir=build_dir,
                out_dir=out_dir,
                problem=problem,
                timelimit_s=float(args.timelimit_s),
                seed=int(args.seed),
                motion_file=motion_file,
            )
        )

    write_summary_csv(rows, out_dir / "summary.csv")
    write_run_md(
        out_dir=out_dir,
        dynoplan_root=dynoplan_root,
        build_dir=build_dir,
        motion_file=motion_file,
        timelimit_s=float(args.timelimit_s),
        seed=int(args.seed),
        rows=rows,
    )
    return 0 if all(row.get("success") is True for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
