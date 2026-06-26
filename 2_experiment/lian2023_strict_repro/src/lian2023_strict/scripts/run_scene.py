from __future__ import annotations

import argparse
from pathlib import Path

from ..config import load_algorithm_params, load_vehicle_params
from ..planner import PlannerMethod, plan_scene
from ..render import render_scene_result, render_velocity_profile
from ..scenes import build_scene


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene", default="fig5c")
    parser.add_argument("--method", choices=[m.value for m in PlannerMethod], default=PlannerMethod.OURS_EHA_IPOPT.value)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--n-elements", type=int, default=200)
    parser.add_argument("--max-iterations", type=int, default=10)
    parser.add_argument("--ipopt-max-iterations", type=int, default=30)
    parser.add_argument("--timeout-s", type=float, default=30.0)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    scene = build_scene(args.scene)
    result = plan_scene(
        scene,
        method=PlannerMethod(args.method),
        vehicle=load_vehicle_params(),
        params=load_algorithm_params(
            n_elements=args.n_elements,
            max_iterations=args.max_iterations,
            ipopt_max_iterations=args.ipopt_max_iterations,
        ),
        timeout_s=args.timeout_s,
    )
    render_scene_result(scene, result, args.out_dir / f"{args.scene}_{args.method}.png")
    if result.success:
        render_velocity_profile(result, args.out_dir / f"{args.scene}_{args.method}_profiles.png")
    print(
        f"scene={result.scene} method={result.method.value} success={result.success} "
        f"status={result.status} total_time_s={float(result.stats.get('total_time_s', 0.0)):.3f}"
    )


if __name__ == "__main__":
    main()
