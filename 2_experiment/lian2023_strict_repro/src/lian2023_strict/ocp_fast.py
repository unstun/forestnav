from __future__ import annotations

import ctypes
import os
import platform
from pathlib import Path
from typing import Any

import numpy as np


_DOUBLE_P = ctypes.POINTER(ctypes.c_double)
_INT64 = ctypes.c_int64
_LIB: ctypes.CDLL | None = None
_LOAD_ERROR: str = ""


def _shared_suffix() -> str:
    if platform.system() == "Darwin":
        return ".dylib"
    return ".so"


def _library_path() -> Path:
    return Path(__file__).resolve().with_name(f"_ocp_fast_lib{_shared_suffix()}")


def _load_library() -> ctypes.CDLL | None:
    global _LIB, _LOAD_ERROR
    if _LIB is not None:
        return _LIB
    path = _library_path()
    if not path.exists():
        _LOAD_ERROR = f"missing {path}"
        return None
    try:
        lib = ctypes.CDLL(str(path))
    except OSError as exc:
        _LOAD_ERROR = str(exc)
        return None
    _bind(lib)
    _LIB = lib
    _LOAD_ERROR = ""
    return _LIB


def _bind(lib: ctypes.CDLL) -> None:
    common_args = [
        _DOUBLE_P,
        _INT64,
        _DOUBLE_P,
        _INT64,
        _DOUBLE_P,
        _INT64,
        _DOUBLE_P,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_int,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
    ]
    lib.lian2023_formula23_penalty_value.argtypes = [*common_args, _DOUBLE_P]
    lib.lian2023_formula23_penalty_value.restype = ctypes.c_int
    lib.lian2023_formula23_penalty_gradient.argtypes = [*common_args, _DOUBLE_P, _DOUBLE_P, _DOUBLE_P, _DOUBLE_P]
    lib.lian2023_formula23_penalty_gradient.restype = ctypes.c_int
    packed_args = [
        _DOUBLE_P,
        _INT64,
        _INT64,
        _DOUBLE_P,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_int,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_double,
    ]
    lib.lian2023_packed_objective.argtypes = [*packed_args, _DOUBLE_P]
    lib.lian2023_packed_objective.restype = ctypes.c_int
    lib.lian2023_packed_gradient.argtypes = [*packed_args, _DOUBLE_P]
    lib.lian2023_packed_gradient.restype = ctypes.c_int


def load_error() -> str:
    _load_library()
    return _LOAD_ERROR


def is_available() -> bool:
    return _load_library() is not None


def is_enabled() -> bool:
    disabled = os.environ.get("LIAN2023_STRICT_DISABLE_CPP", "")
    if disabled.lower() in {"1", "true", "yes", "on"}:
        return False
    requested = os.environ.get("LIAN2023_STRICT_USE_CPP", "")
    return requested.lower() in {"1", "true", "yes", "on"} and is_available()


def formula23_penalty_value(
    states: np.ndarray,
    controls: np.ndarray,
    tf: float,
    vehicle: Any,
    params: Any,
    *,
    disk_centers: np.ndarray,
) -> float:
    lib = _load_library()
    if lib is None:
        raise RuntimeError(load_error())
    states_c = np.ascontiguousarray(states, dtype=np.float64)
    controls_c = np.ascontiguousarray(controls, dtype=np.float64)
    disks_c = np.ascontiguousarray(disk_centers, dtype=np.float64)
    offsets_c = np.ascontiguousarray(vehicle.disc_offsets_m, dtype=np.float64)
    _validate_shapes(states_c, controls_c, disks_c, offsets_c)
    out = ctypes.c_double(0.0)
    rc = lib.lian2023_formula23_penalty_value(
        states_c.ctypes.data_as(_DOUBLE_P),
        _INT64(states_c.shape[0]),
        controls_c.ctypes.data_as(_DOUBLE_P),
        _INT64(controls_c.shape[0]),
        disks_c.ctypes.data_as(_DOUBLE_P),
        _INT64(offsets_c.shape[0]),
        offsets_c.ctypes.data_as(_DOUBLE_P),
        ctypes.c_double(float(tf)),
        ctypes.c_double(float(vehicle.wheelbase_m)),
        ctypes.c_int(1 if params.enable_local_state_constraint else 0),
        ctypes.c_double(float(params.local_area[0])),
        ctypes.c_double(float(params.local_area[1])),
        ctypes.c_double(float(params.local_area[2])),
        ctypes.c_double(float(params.local_area[3])),
        ctypes.c_double(float(params.local_speed_bounds_m_s[0])),
        ctypes.c_double(float(params.local_speed_bounds_m_s[1])),
        ctypes.c_double(float(params.beta)),
        ctypes.byref(out),
    )
    if rc != 0:
        raise RuntimeError(f"C++ formula23 value failed with code {rc}")
    return float(out.value)


def formula23_penalty_gradient(
    states: np.ndarray,
    controls: np.ndarray,
    disk_centers: np.ndarray,
    tf: float,
    vehicle: Any,
    params: Any,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    lib = _load_library()
    if lib is None:
        raise RuntimeError(load_error())
    states_c = np.ascontiguousarray(states, dtype=np.float64)
    controls_c = np.ascontiguousarray(controls, dtype=np.float64)
    disks_c = np.ascontiguousarray(disk_centers, dtype=np.float64)
    offsets_c = np.ascontiguousarray(vehicle.disc_offsets_m, dtype=np.float64)
    _validate_shapes(states_c, controls_c, disks_c, offsets_c)
    grad_states = np.zeros_like(states_c)
    grad_controls = np.zeros_like(controls_c)
    grad_disks = np.zeros_like(disks_c)
    grad_tf = ctypes.c_double(0.0)
    rc = lib.lian2023_formula23_penalty_gradient(
        states_c.ctypes.data_as(_DOUBLE_P),
        _INT64(states_c.shape[0]),
        controls_c.ctypes.data_as(_DOUBLE_P),
        _INT64(controls_c.shape[0]),
        disks_c.ctypes.data_as(_DOUBLE_P),
        _INT64(offsets_c.shape[0]),
        offsets_c.ctypes.data_as(_DOUBLE_P),
        ctypes.c_double(float(tf)),
        ctypes.c_double(float(vehicle.wheelbase_m)),
        ctypes.c_int(1 if params.enable_local_state_constraint else 0),
        ctypes.c_double(float(params.local_area[0])),
        ctypes.c_double(float(params.local_area[1])),
        ctypes.c_double(float(params.local_area[2])),
        ctypes.c_double(float(params.local_area[3])),
        ctypes.c_double(float(params.local_speed_bounds_m_s[0])),
        ctypes.c_double(float(params.local_speed_bounds_m_s[1])),
        ctypes.c_double(float(params.beta)),
        grad_states.ctypes.data_as(_DOUBLE_P),
        grad_controls.ctypes.data_as(_DOUBLE_P),
        grad_disks.ctypes.data_as(_DOUBLE_P),
        ctypes.byref(grad_tf),
    )
    if rc != 0:
        raise RuntimeError(f"C++ formula23 gradient failed with code {rc}")
    return grad_states, grad_controls, grad_disks, float(grad_tf.value)


def packed_objective(
    q: np.ndarray,
    *,
    n_controls: int,
    disc_count: int,
    vehicle: Any,
    params: Any,
    penalty_weight: float,
) -> float:
    lib = _load_library()
    if lib is None:
        raise RuntimeError(load_error())
    q_c = np.ascontiguousarray(q, dtype=np.float64)
    offsets_c = np.ascontiguousarray(vehicle.disc_offsets_m, dtype=np.float64)
    _validate_packed_shape(q_c, int(n_controls), int(disc_count), offsets_c)
    out = ctypes.c_double(0.0)
    rc = lib.lian2023_packed_objective(
        q_c.ctypes.data_as(_DOUBLE_P),
        _INT64(int(n_controls)),
        _INT64(int(disc_count)),
        offsets_c.ctypes.data_as(_DOUBLE_P),
        ctypes.c_double(float(penalty_weight)),
        ctypes.c_double(float(params.mu1)),
        ctypes.c_double(float(params.mu2)),
        ctypes.c_double(float(params.mu3)),
        ctypes.c_double(float(vehicle.wheelbase_m)),
        ctypes.c_int(1 if params.enable_local_state_constraint else 0),
        ctypes.c_double(float(params.local_area[0])),
        ctypes.c_double(float(params.local_area[1])),
        ctypes.c_double(float(params.local_area[2])),
        ctypes.c_double(float(params.local_area[3])),
        ctypes.c_double(float(params.local_speed_bounds_m_s[0])),
        ctypes.c_double(float(params.local_speed_bounds_m_s[1])),
        ctypes.c_double(float(params.beta)),
        ctypes.byref(out),
    )
    if rc != 0:
        raise RuntimeError(f"C++ packed objective failed with code {rc}")
    return float(out.value)


def packed_gradient(
    q: np.ndarray,
    *,
    n_controls: int,
    disc_count: int,
    vehicle: Any,
    params: Any,
    penalty_weight: float,
) -> np.ndarray:
    lib = _load_library()
    if lib is None:
        raise RuntimeError(load_error())
    q_c = np.ascontiguousarray(q, dtype=np.float64)
    offsets_c = np.ascontiguousarray(vehicle.disc_offsets_m, dtype=np.float64)
    _validate_packed_shape(q_c, int(n_controls), int(disc_count), offsets_c)
    grad = np.zeros_like(q_c)
    rc = lib.lian2023_packed_gradient(
        q_c.ctypes.data_as(_DOUBLE_P),
        _INT64(int(n_controls)),
        _INT64(int(disc_count)),
        offsets_c.ctypes.data_as(_DOUBLE_P),
        ctypes.c_double(float(penalty_weight)),
        ctypes.c_double(float(params.mu1)),
        ctypes.c_double(float(params.mu2)),
        ctypes.c_double(float(params.mu3)),
        ctypes.c_double(float(vehicle.wheelbase_m)),
        ctypes.c_int(1 if params.enable_local_state_constraint else 0),
        ctypes.c_double(float(params.local_area[0])),
        ctypes.c_double(float(params.local_area[1])),
        ctypes.c_double(float(params.local_area[2])),
        ctypes.c_double(float(params.local_area[3])),
        ctypes.c_double(float(params.local_speed_bounds_m_s[0])),
        ctypes.c_double(float(params.local_speed_bounds_m_s[1])),
        ctypes.c_double(float(params.beta)),
        grad.ctypes.data_as(_DOUBLE_P),
    )
    if rc != 0:
        raise RuntimeError(f"C++ packed gradient failed with code {rc}")
    return grad


def _validate_shapes(states: np.ndarray, controls: np.ndarray, disks: np.ndarray, offsets: np.ndarray) -> None:
    if states.ndim != 2 or states.shape[1] != 5:
        raise ValueError("states must have shape (n + 1, 5)")
    if controls.ndim != 2 or controls.shape[1] != 2:
        raise ValueError("controls must have shape (n, 2)")
    if states.shape[0] != controls.shape[0] + 1:
        raise ValueError("states must have exactly one more row than controls")
    if disks.ndim != 3 or disks.shape[0] != states.shape[0] or disks.shape[2] != 2:
        raise ValueError("disk_centers must have shape (n + 1, disc_count, 2)")
    if offsets.ndim != 1 or offsets.shape[0] != disks.shape[1]:
        raise ValueError("vehicle.disc_offsets_m must match disk_centers disc_count")


def _validate_packed_shape(q: np.ndarray, n_controls: int, disc_count: int, offsets: np.ndarray) -> None:
    expected = (n_controls + 1) * 5 + n_controls * 2 + (n_controls + 1) * disc_count * 2 + 1
    if q.ndim != 1 or q.shape[0] != expected:
        raise ValueError(f"q must have shape ({expected},)")
    if offsets.ndim != 1 or offsets.shape[0] != disc_count:
        raise ValueError("vehicle.disc_offsets_m must match disc_count")
