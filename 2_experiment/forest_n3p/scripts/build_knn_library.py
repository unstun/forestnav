from __future__ import annotations

import argparse
import sys
from pathlib import Path

from forest_n3p.inference import build_knn_library
from forest_n3p.training_data import source_head


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the T09 F-N3P KNN subgoal library.")
    parser.add_argument(
        "--dataset-dir",
        type=Path,
        default=Path("2_experiment/forest_n3p/datasets/t08_training_dataset"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("2_experiment/forest_n3p/models/t09_knn_library"),
    )
    parser.add_argument("--leaf-size", type=int, default=40)
    parser.add_argument("--zscore-epsilon", type=float, default=1e-6)
    parser.add_argument("--source-head", type=str, default=None)
    parser.add_argument("--command", type=str, default=None)
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args()
    command = args.command or " ".join(sys.argv)
    result = build_knn_library(
        args.dataset_dir,
        args.output_dir,
        leaf_size=int(args.leaf_size),
        zscore_epsilon=float(args.zscore_epsilon),
        source_head=args.source_head or source_head(),
        command=command,
    )
    print(result.metadata_path)
    print(result.tree_path)
    print(f"feature_shape={result.feature_shape}")
    print(f"label_shape={result.label_shape}")
    print(f"leaf_size={result.leaf_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
