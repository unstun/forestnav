from __future__ import annotations

import argparse
import json
from pathlib import Path

from ..config import load_algorithm_params, load_vehicle_params
from ..diagnostics import diagnose_stage1
from ..scenes import list_scene_names


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--scene", action="append", choices=list_scene_names())
    parser.add_argument("--n-elements", type=int, default=200)
    parser.add_argument("--max-iterations", type=int, default=10)
    parser.add_argument("--ipopt-max-iterations", type=int, default=240)
    parser.add_argument("--segment-timeout-s", type=float, default=30.0)
    args = parser.parse_args()

    vehicle = load_vehicle_params()
    params = load_algorithm_params(
        n_elements=args.n_elements,
        max_iterations=args.max_iterations,
        ipopt_max_iterations=args.ipopt_max_iterations,
        enable_local_state_constraint=False,
    )
    scene_names = tuple(args.scene) if args.scene else list_scene_names()
    results = [
        diagnose_stage1(scene_name, vehicle=vehicle, params=params, segment_timeout_s=args.segment_timeout_s)
        for scene_name in scene_names
    ]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    for item in results:
        seed = item.get("seed", {})
        print(
            f"[diagnose_stage1] {item['scene']} status={item['stage1_status']} "
            f"xbou={item.get('xbou_corrected_count', 0)} "
            f"seed_jinf={seed.get('jinf', '')} "
            f"seed_j3={seed.get('jpenalty3', '')} seed_j7={seed.get('jpenalty7', '')}",
            flush=True,
        )


if __name__ == "__main__":
    main()
