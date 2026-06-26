from __future__ import annotations

import argparse
import csv
import platform
from pathlib import Path

from ..config import load_algorithm_params, load_vehicle_params
from ..planner import PlannerMethod, plan_scene
from ..render import render_scene_result
from ..scenes import build_scene, list_scene_names


STAGE2_FIELDS = {
    "cpu_time_ii_s",
    "total_time_s",
    "terminal_error_m",
    "jinf",
    "jpenalty3",
    "jpenalty6",
    "jpenalty7",
    "jpenalty15",
    "outer_iterations",
    "ipopt_iterations",
    "final_penalty_weight",
}

TABLE2_FIELDS = [
    "scene",
    "method",
    "success",
    "status",
    "cpu_time_i_s",
    "cpu_time_ii_s",
    "total_time_s",
    "terminal_error_m",
    "jinf",
    "jpenalty3",
    "jpenalty6",
    "jpenalty7",
    "jpenalty15",
    "jinf_ok",
    "outer_iterations",
    "ipopt_iterations",
    "ipopt_max_iterations",
    "final_penalty_weight",
    "disc_corridors",
    "ipopt_status",
    "stage1_status",
    "passage_groups",
    "xbou_points",
    "note",
]


def _fmt_float(stats: dict, key: str, fmt: str = ".6f") -> str:
    if key in STAGE2_FIELDS and key not in stats:
        return ""
    return format(float(stats.get(key, 0.0)), fmt)


def run_table2(
    *,
    out_dir: Path,
    n_elements: int = 200,
    max_iterations: int = 10,
    ipopt_max_iterations: int = 30,
    timeout_s: float = 30.0,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    vehicle = load_vehicle_params()
    params = load_algorithm_params(
        n_elements=n_elements,
        max_iterations=max_iterations,
        ipopt_max_iterations=ipopt_max_iterations,
        enable_local_state_constraint=False,
    )
    rows: list[dict[str, str]] = []
    csv_path = out_dir / "table2_local.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=TABLE2_FIELDS)
        writer.writeheader()
        f.flush()
        for scene_name in list_scene_names():
            scene = build_scene(scene_name)
            for method in PlannerMethod:
                row_no = len(rows) + 1
                print(f"[run_table2] {row_no:02d}/16 {scene_name} {method.value} start", flush=True)
                result = plan_scene(scene, method=method, vehicle=vehicle, params=params, timeout_s=timeout_s)
                if method == PlannerMethod.OURS_EHA_IPOPT:
                    render_scene_result(scene, result, out_dir / f"{scene_name}_ours.png")
                row = _row_from_result(scene_name, method, result)
                rows.append(row)
                writer.writerow(row)
                f.flush()
                print(
                    f"[run_table2] {row_no:02d}/16 {scene_name} {method.value} "
                    f"success={result.success} status={result.status} "
                    f"jinf={row['jinf']} total_time_s={row['total_time_s']}",
                    flush=True,
                )
    write_run_md(
        out_dir=out_dir,
        rows=rows,
        n_elements=n_elements,
        max_iterations=max_iterations,
        ipopt_max_iterations=ipopt_max_iterations,
        timeout_s=timeout_s,
    )


def _row_from_result(scene_name: str, method: PlannerMethod, result) -> dict[str, str]:
    return {
        "scene": scene_name,
        "method": method.value,
        "success": str(result.success),
        "status": result.status,
        "cpu_time_i_s": _fmt_float(result.stats, "cpu_time_i_s"),
        "cpu_time_ii_s": _fmt_float(result.stats, "cpu_time_ii_s"),
        "total_time_s": _fmt_float(result.stats, "total_time_s"),
        "terminal_error_m": _fmt_float(result.stats, "terminal_error_m"),
        "jinf": _fmt_float(result.stats, "jinf", ".9f"),
        "jpenalty3": _fmt_float(result.stats, "jpenalty3", ".9f"),
        "jpenalty6": _fmt_float(result.stats, "jpenalty6", ".9f"),
        "jpenalty7": _fmt_float(result.stats, "jpenalty7", ".9f"),
        "jpenalty15": _fmt_float(result.stats, "jpenalty15", ".9f"),
        "jinf_ok": str(result.stats.get("jinf_ok", "")),
        "outer_iterations": _fmt_float(result.stats, "outer_iterations", ".0f"),
        "ipopt_iterations": _fmt_float(result.stats, "ipopt_iterations", ".0f"),
        "ipopt_max_iterations": _fmt_float(result.stats, "ipopt_max_iterations", ".0f"),
        "final_penalty_weight": _fmt_float(result.stats, "final_penalty_weight", ".6g"),
        "disc_corridors": str(result.stats.get("disc_corridors", "")),
        "ipopt_status": str(result.stats.get("ipopt_status", "")),
        "stage1_status": str(result.stats.get("stage1_status", "")),
        "passage_groups": str(result.stats.get("passage_groups", "")),
        "xbou_points": str(result.stats.get("xbou_points", "")),
        "note": "local Python run; paper used Matlab R2021a and Intel i9-10850K",
    }


def write_run_md(
    *,
    out_dir: Path,
    rows: list[dict[str, str]],
    n_elements: int,
    max_iterations: int,
    ipopt_max_iterations: int,
    timeout_s: float,
) -> None:
    row_count = len(rows)
    total_count = len(list_scene_names()) * len(PlannerMethod)
    status_line = "complete" if row_count == total_count else f"partial ({row_count} / {total_count} rows)"
    (out_dir / "RUN.md").write_text(
        "\n".join(
            [
                "# Lian2023 Strict Reproduction Run",
                "",
                "## Command",
                "",
                "Table-style run:",
                "",
                (
                    "`PYTHONPATH=2_experiment/lian2023_strict_repro/src "
                    "python -m lian2023_strict.scripts.run_table2 "
                    f"--out-dir {out_dir} --n-elements {n_elements} "
                    f"--max-iterations {max_iterations} --ipopt-max-iterations {ipopt_max_iterations} "
                    f"--timeout-s {timeout_s}`"
                ),
                "",
                "Figure bundle run:",
                "",
                (
                    "`PYTHONPATH=2_experiment/lian2023_strict_repro/src "
                    "python -m lian2023_strict.scripts.render_figures "
                    f"--out-dir {out_dir / 'figures'} --n-elements {n_elements} "
                    f"--max-iterations {max_iterations} --ipopt-max-iterations {ipopt_max_iterations}`"
                ),
                "",
                "## Environment",
                "",
                f"- Python: {platform.python_version()}",
                f"- Platform: {platform.platform()}",
                "- Solver: `cyipopt.minimize_ipopt` is used for the state-control OCP stage.",
                "- Source paper: Lian et al., IEEE TIV 2023, Table I and Algorithm 1.",
                "- Performance note: analytic gradients are provided for formula (16), `Jpenalty(3)`, `Jpenalty(7)`, and `Jpenalty(15)`; this run records the exact requested `n-elements` and `max-iterations` values above.",
                "- Fig.5/Table II style runs set `enable_local_state_constraint=False`, matching the paper text that temporarily removes formula (15) for the four Fig.5 scenarios.",
                "- `table2_local.csv` is written incrementally after each row so interrupted long runs keep completed rows.",
                "",
                "## Checkpoints",
                "",
                f"- Vehicle and algorithm constants use Table I defaults, except `Wpenalty=1e6` follows Algorithm 1 line 38.",
                f"- Row status: {status_line}.",
                f"- Scenes: {', '.join(list_scene_names())}.",
                f"- Methods per scene: {', '.join(method.value for method in PlannerMethod)}.",
                f"- Successful rows: {sum(row['success'] == 'True' for row in rows)} / {row_count}.",
                f"- Rows satisfying `Jinf <= Etol`: {sum(row['jinf_ok'] == 'True' for row in rows)} / {row_count}.",
                "",
                "## Outputs",
                "",
                "- `table2_local.csv`: local timing and success table.",
                "- `fig5a_ours.png` ... `fig5d_ours.png`: Table-style run Fig.5 trajectory images.",
                "- `figures/fig5a_ours.png` ... `figures/fig5d_ours.png`: figure bundle copies regenerated by `render_figures`.",
                "- `figures/fig7_velocity_controls.png`: state/control profile if the Fig.5b OURS run reaches Stage 2.",
                "- `figures/fig9_fig10_local_state_constraint.png`: local state constraint diagnostic.",
                "",
                "## Known Differences",
                "",
                "- Scenes are figure-reconstructed from Lian et al. 2023 Fig. 5.",
                "- Current OCP uses formula (16) plus formula (23)/(24)-style penalties for kinematics, disk-center geometry, and local state constraints.",
                "- Formula (6) is represented as hard bounds on disk-center decision variables selected from the generated corridor boxes for `k = 0..n-1`.",
                "- `jpenalty6` is reported as a post-solve corridor violation diagnostic and is not included in `Jinf`.",
                "- `success=False, status=stage2_infeasible` means the solver produced a trajectory but did not reach the paper threshold `Jinf <= Etol`.",
                "- `success=False, status=stage1_eha_fail` means strict boundary-point Hybrid A* failed before OCP; Stage 2 fields are blank in `table2_local.csv`.",
                "- BP segment connection has no straight-line or grid-guided fallback; primitive Hybrid A* failure returns `stage1_eha_fail`.",
                f"- Paper-size diagnostic settings: table and figure runs use `n_elements={n_elements}, max_iterations={max_iterations}`.",
                f"- Local IPOPT cap: each outer iteration uses `ipopt_max_iterations={ipopt_max_iterations}` because the paper does not report IPOPT's internal iteration cap.",
                "- A paper-level numerical match requires all relevant rows to satisfy `Jinf <= 1e-4`; this diagnostic run records which rows fail that gate.",
                "- Local timing is measured on the current macOS/Python environment, while the paper used Matlab R2021a on Intel i9-10850K.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--n-elements", type=int, default=200)
    parser.add_argument("--max-iterations", type=int, default=10)
    parser.add_argument("--ipopt-max-iterations", type=int, default=30)
    parser.add_argument("--timeout-s", type=float, default=30.0)
    args = parser.parse_args()
    run_table2(
        out_dir=args.out_dir,
        n_elements=args.n_elements,
        max_iterations=args.max_iterations,
        ipopt_max_iterations=args.ipopt_max_iterations,
        timeout_s=args.timeout_s,
    )


if __name__ == "__main__":
    main()
