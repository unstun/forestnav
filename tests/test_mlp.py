from __future__ import annotations

import numpy as np
import torch

from forest_n3p.mlp import (
    MlpSubgoalPredictor,
    MlpTrainingConfig,
    SubgoalMlp,
    count_parameters,
    train_mlp_model,
)


def _write_dataset(root, features: np.ndarray, labels: np.ndarray) -> None:
    root.mkdir(parents=True, exist_ok=True)
    np.save(root / "features.npy", features.astype(np.float32))
    np.save(root / "labels.npy", labels.astype(np.float32))


def test_subgoal_mlp_uses_four_linear_layers() -> None:
    model = SubgoalMlp(input_dim=41, hidden_dims=(16, 8, 4), output_dim=3)
    linear_layers = [module for module in model.modules() if isinstance(module, torch.nn.Linear)]
    out = model(torch.zeros((2, 41), dtype=torch.float32))

    assert len(linear_layers) == 4
    assert out.shape == (2, 3)
    assert count_parameters(model) > 0


def test_train_mlp_model_writes_checkpoint_and_loaded_predictor_queries(tmp_path) -> None:
    rng = np.random.default_rng(123)
    features = rng.normal(size=(80, 41)).astype(np.float32)
    labels = np.stack(
        [
            0.5 * features[:, 0] + 0.1 * features[:, 1],
            -0.3 * features[:, 2],
            0.2 * features[:, 3],
        ],
        axis=1,
    ).astype(np.float32)
    dataset_dir = tmp_path / "dataset"
    output_dir = tmp_path / "model"
    _write_dataset(dataset_dir, features, labels)

    result = train_mlp_model(
        dataset_dir,
        output_dir,
        config=MlpTrainingConfig(
            seed=7,
            hidden_dims=(8, 8, 4),
            batch_size=16,
            epochs=3,
            patience=3,
            device="cpu",
        ),
        source_head="unit-test",
        execution_host="unit-test",
        command="unit-test",
    )
    predictor = MlpSubgoalPredictor.load(output_dir, device="cpu")
    prediction = predictor.query(features[0], current_pose=(1.0, 2.0, 0.0), k=5)[0]

    assert result.checkpoint_path.exists()
    assert result.metadata_path.exists()
    assert result.train_log_csv.exists()
    assert result.train_count == 72
    assert result.val_count == 8
    assert prediction.sample_index == -1
    assert np.all(np.isfinite(prediction.delta_body))
    assert np.all(np.isfinite(prediction.subgoal_pose))
