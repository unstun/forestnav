import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch

from forest_n3p.scripts.train_bc_patch_policy import _build_patch_scalar_cnn, _runtime_error_reason


def test_patch_scalar_cnn_forward_shape_and_bounds():
    model = _build_patch_scalar_cnn(
        torch=torch,
        patch_channels=2,
        scalar_dim=8,
        cnn_channels=(4, 8),
        hidden_dims=(16,),
        max_steer=0.5,
    )

    output = model(torch.zeros((3, 2, 16, 16)), torch.zeros((3, 8)))

    assert output.shape == (3, 1)
    assert torch.all(output <= 0.5)
    assert torch.all(output >= -0.5)


def test_runtime_error_reason_keeps_exception_message():
    reason = _runtime_error_reason(ValueError("start state is in collision"))

    assert reason == "runtime_error:ValueError:start state is in collision"
