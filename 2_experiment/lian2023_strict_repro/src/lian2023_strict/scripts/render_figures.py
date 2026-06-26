from __future__ import annotations

import argparse
from pathlib import Path

from ..config import load_algorithm_params, load_vehicle_params
from ..planner import PlannerMethod, plan_scene
from ..render import render_local_constraint, render_scene_result, render_velocity_profile
from ..scenes import build_scene, list_scene_names


def render_all(
    *,
    out_dir: Path,
    n_elements: int = 200,
    max_iterations: int = 10,
    ipopt_max_iterations: int = 30,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    print(
        "[render_figures] start "
        f"out_dir={out_dir} n_elements={n_elements} "
        f"max_iterations={max_iterations} ipopt_max_iterations={ipopt_max_iterations}",
        flush=True,
    )
    vehicle = load_vehicle_params()
    params = load_algorithm_params(
        n_elements=n_elements,
        max_iterations=max_iterations,
        ipopt_max_iterations=ipopt_max_iterations,
        enable_local_state_constraint=False,
    )
    results = []
    for scene_name in list_scene_names():
        scene = build_scene(scene_name)
        print(f"[render_figures] {scene_name} ours_eha_ipopt start", flush=True)
        result = plan_scene(scene, method=PlannerMethod.OURS_EHA_IPOPT, vehicle=vehicle, params=params)
        results.append(result)
        scene_path = out_dir / f"{scene_name}_ours.png"
        render_scene_result(scene, result, scene_path)
        print(
            f"[render_figures] {scene_name} status={result.status} "
            f"success={result.success} jinf={result.stats.get('jinf', '')} "
            f"output={scene_path}",
            flush=True,
        )
        if scene_name == "fig5b" and len(result.states) > 0:
            profile_path = out_dir / "fig7_velocity_controls.png"
            render_velocity_profile(result, profile_path)
            print(f"[render_figures] fig7 output={profile_path}", flush=True)
    scene = build_scene("fig5b")
    local_results = []
    for vmax in (2.0, 2.5, 3.0, 3.5):
        print(f"[render_figures] local constraint vmax={vmax} start", flush=True)
        result = plan_scene(
            scene,
            method=PlannerMethod.OURS_EHA_IPOPT,
            vehicle=vehicle,
            params=load_algorithm_params(
                n_elements=n_elements,
                max_iterations=max_iterations,
                ipopt_max_iterations=ipopt_max_iterations,
                enable_local_state_constraint=True,
                local_speed_bounds_m_s=(0.0, vmax),
            ),
        )
        local_results.append(result)
        print(
            f"[render_figures] local constraint vmax={vmax} "
            f"status={result.status} success={result.success} jinf={result.stats.get('jinf', '')}",
            flush=True,
        )
    local_path = out_dir / "fig9_fig10_local_state_constraint.png"
    render_local_constraint(scene, local_results, params, local_path)
    print(f"[render_figures] fig9_fig10 output={local_path}", flush=True)
    print("[render_figures] complete", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--n-elements", type=int, default=200)
    parser.add_argument("--max-iterations", type=int, default=10)
    parser.add_argument("--ipopt-max-iterations", type=int, default=30)
    args = parser.parse_args()
    render_all(
        out_dir=args.out_dir,
        n_elements=args.n_elements,
        max_iterations=args.max_iterations,
        ipopt_max_iterations=args.ipopt_max_iterations,
    )


if __name__ == "__main__":
    main()
