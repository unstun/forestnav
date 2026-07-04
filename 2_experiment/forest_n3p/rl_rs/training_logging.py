from __future__ import annotations

import csv
import hashlib
import json
import math
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import gymnasium as gym

from forest_n3p.rl_rs.reward import REWARD_TERM_NAMES

CSV_FIELDNAMES = (
    "episode_index",
    "curriculum_stage",
    "curriculum_source",
    "query_id",
    "difficulty_bucket",
    "profile_name",
    "map_seed",
    "query_seed",
    "reward_total",
    "reward_term_success",
    "reward_term_terminal",
    "reward_term_collision",
    "reward_term_progress",
    "reward_term_rs_progress",
    "reward_term_clearance",
    "reward_term_curvature",
    "reward_term_path_length",
    "reward_term_step",
    "terminated",
    "truncated",
    "terminal_rs_success",
    "collision",
    "failure_reason",
    "rollout_steps",
    "rollout_collision_checks",
    "rollout_length_m",
    "min_clearance_m",
    "mean_abs_curvature_delta",
    "mean_abs_curvature_rate",
    "nn_forward_time_s",
    "rollout_sample_time_s",
    "rollout_collision_time_s",
    "terminal_rs_time_s",
)


class RlRsEpisodeLoggingWrapper(gym.Wrapper):
    """Episode-level logging wrapper for RL-RS training runs."""

    def __init__(self, env: gym.Env, *, csv_path: str | Path, tensorboard_writer: Any | None = None) -> None:
        super().__init__(env)
        self.csv_path = Path(csv_path)
        self.tensorboard_writer = tensorboard_writer
        self.episode_index = 0
        self._reset_info: dict[str, Any] = {}
        self._reward_total = 0.0
        self._reward_terms = {name: 0.0 for name in REWARD_TERM_NAMES}
        self._step_infos: list[dict[str, Any]] = []
        self._nn_forward_time_s = 0.0

    def reset(self, **kwargs: Any):
        observation, info = self.env.reset(**kwargs)
        self._reset_info = dict(info)
        self._reward_total = 0.0
        self._reward_terms = {name: 0.0 for name in REWARD_TERM_NAMES}
        self._step_infos = []
        self._nn_forward_time_s = 0.0
        return observation, info

    def record_nn_forward_time(self, elapsed_s: float) -> None:
        elapsed = _optional_finite_float(elapsed_s)
        if elapsed is None or elapsed < 0.0:
            raise ValueError("elapsed_s must be a finite non-negative value")
        self._nn_forward_time_s += float(elapsed)

    def step(self, action: Any):
        observation, reward, terminated, truncated, info = self.env.step(action)
        step_info = dict(info)
        self._reward_total += float(reward)
        self._accumulate_reward_terms(step_info.get("reward_terms"))
        self._step_infos.append(step_info)
        if bool(terminated or truncated):
            record = self._build_episode_record(terminated=bool(terminated), truncated=bool(truncated))
            self._append_csv(record)
            self._write_tensorboard_scalars(record)
            self.episode_index += 1
        return observation, reward, terminated, truncated, info

    def close(self) -> None:
        writer = self.tensorboard_writer
        if writer is not None and hasattr(writer, "close"):
            writer.close()
        super().close()

    def _accumulate_reward_terms(self, terms: object) -> None:
        if not isinstance(terms, Mapping):
            return
        for name in REWARD_TERM_NAMES:
            self._reward_terms[name] += _finite_float(terms.get(name), default=0.0)

    def _build_episode_record(self, *, terminated: bool, truncated: bool) -> dict[str, Any]:
        curriculum = _mapping_or_empty(self._reset_info.get("curriculum"))
        context = self._reset_info.get("context")
        telemetry = _episode_telemetry_record(self.env)
        rollout_length_m = self._rollout_length_m(context=context, telemetry=telemetry)
        curvature_deltas = [_finite_float(info.get("curvature_delta_abs"), default=0.0) for info in self._step_infos]
        curvature_total = float(sum(abs(value) for value in curvature_deltas))
        mean_abs_curvature_delta = curvature_total / float(len(curvature_deltas)) if curvature_deltas else 0.0
        mean_abs_curvature_rate = curvature_total / rollout_length_m if rollout_length_m > 0.0 else 0.0
        clearances = [
            float(value)
            for info in self._step_infos
            if (value := _optional_finite_float(info.get("min_clearance_m"))) is not None
        ]
        min_clearance_m = min(clearances) if clearances else None

        return {
            "episode_index": int(self.episode_index),
            "curriculum_stage": curriculum.get("stage"),
            "curriculum_source": curriculum.get("source"),
            "query_id": curriculum.get("query_id"),
            "difficulty_bucket": curriculum.get("difficulty_bucket"),
            "profile_name": curriculum.get("profile_name"),
            "map_seed": curriculum.get("map_seed"),
            "query_seed": curriculum.get("query_seed"),
            "reward_total": float(self._reward_total),
            "reward_term_success": float(self._reward_terms["success"]),
            "reward_term_terminal": float(self._reward_terms["terminal"]),
            "reward_term_collision": float(self._reward_terms["collision"]),
            "reward_term_progress": float(self._reward_terms["progress"]),
            "reward_term_rs_progress": float(self._reward_terms["rs_progress"]),
            "reward_term_clearance": float(self._reward_terms["clearance"]),
            "reward_term_curvature": float(self._reward_terms["curvature"]),
            "reward_term_path_length": float(self._reward_terms["path_length"]),
            "reward_term_step": float(self._reward_terms["step"]),
            "terminated": bool(terminated),
            "truncated": bool(truncated),
            "terminal_rs_success": bool(telemetry.get("terminal_rs_success", False)),
            "collision": bool(telemetry.get("collided", False)),
            "failure_reason": telemetry.get("failure_reason"),
            "rollout_steps": int(telemetry.get("rollout_steps", len(self._step_infos))),
            "rollout_collision_checks": int(telemetry.get("rollout_collision_checks", 0)),
            "rollout_length_m": float(rollout_length_m),
            "min_clearance_m": min_clearance_m,
            "mean_abs_curvature_delta": float(mean_abs_curvature_delta),
            "mean_abs_curvature_rate": float(mean_abs_curvature_rate),
            "nn_forward_time_s": self._nn_forward_time_s + _finite_float(telemetry.get("nn_forward_time_s"), default=0.0),
            "rollout_sample_time_s": _finite_float(telemetry.get("rollout_sample_time_s"), default=0.0),
            "rollout_collision_time_s": _finite_float(telemetry.get("rollout_collision_time_s"), default=0.0),
            "terminal_rs_time_s": _finite_float(telemetry.get("terminal_rs_time_s"), default=0.0),
        }

    def _rollout_length_m(self, *, context: Any, telemetry: Mapping[str, Any]) -> float:
        raw_length = sum(_finite_float(info.get("rollout_path_length_m"), default=0.0) for info in self._step_infos)
        if raw_length > 0.0:
            return float(raw_length)
        action_step_m = _optional_finite_float(getattr(context, "action_step_m", None))
        if action_step_m is None:
            return 0.0
        return float(telemetry.get("rollout_steps", len(self._step_infos))) * action_step_m

    def _append_csv(self, record: Mapping[str, Any]) -> None:
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        write_header = not self.csv_path.exists() or self.csv_path.stat().st_size == 0
        with self.csv_path.open("a", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=CSV_FIELDNAMES)
            if write_header:
                writer.writeheader()
            writer.writerow({field: _csv_value(record.get(field)) for field in CSV_FIELDNAMES})

    def _write_tensorboard_scalars(self, record: Mapping[str, Any]) -> None:
        writer = self.tensorboard_writer
        if writer is None:
            return
        step = int(record["episode_index"])
        scalar_tags = {
            "episode/reward_total": record["reward_total"],
            "episode/terminal_rs_success": record["terminal_rs_success"],
            "episode/collision": record["collision"],
            "episode/truncated": record["truncated"],
            "episode/rollout_length_m": record["rollout_length_m"],
            "episode/min_clearance_m": record["min_clearance_m"],
            "episode/mean_abs_curvature_rate": record["mean_abs_curvature_rate"],
            "episode/rollout_collision_checks": record["rollout_collision_checks"],
            "timing/rollout_sample_time_s": record["rollout_sample_time_s"],
            "timing/rollout_collision_time_s": record["rollout_collision_time_s"],
            "timing/terminal_rs_time_s": record["terminal_rs_time_s"],
            "timing/nn_forward_time_s": record["nn_forward_time_s"],
        }
        for name in REWARD_TERM_NAMES:
            scalar_tags[f"episode/reward_term_{name}"] = record[f"reward_term_{name}"]
        for tag, value in scalar_tags.items():
            scalar_value = _optional_scalar_float(value)
            if scalar_value is not None:
                writer.add_scalar(tag, scalar_value, step)


def create_tensorboard_writer(log_dir: str | Path) -> Any:
    """Create a TensorBoard writer only when the caller explicitly asks for it."""

    try:
        from torch.utils.tensorboard import SummaryWriter
    except Exception as exc:  # pragma: no cover - depends on optional runtime packages.
        raise RuntimeError("TensorBoard logging requires torch.utils.tensorboard to import cleanly.") from exc
    return SummaryWriter(log_dir=str(log_dir))


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_training_manifest(
    output_dir: str | Path,
    *,
    config: Mapping[str, Any],
    source_hashes: Mapping[str, str],
    checkpoints: Sequence[Mapping[str, Any]],
    command: str | Sequence[str] | None = None,
) -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": 1,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "config": dict(config),
        "source_hashes": dict(source_hashes),
        "checkpoints": [dict(checkpoint) for checkpoint in checkpoints],
        "command": _command_record(command),
    }
    manifest_path = output_path / "training_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest_path


def _episode_telemetry_record(env: gym.Env) -> dict[str, Any]:
    planner_env = getattr(env, "planner_env", None)
    if planner_env is None:
        unwrapped = getattr(env, "unwrapped", None)
        planner_env = getattr(unwrapped, "planner_env", None)
    telemetry = getattr(planner_env, "telemetry", None)
    to_record = getattr(telemetry, "to_record", None)
    return dict(to_record()) if callable(to_record) else {}


def _mapping_or_empty(value: object) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _finite_float(value: object, *, default: float) -> float:
    parsed = _optional_finite_float(value)
    return float(default) if parsed is None else parsed


def _optional_finite_float(value: object) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    return parsed if math.isfinite(parsed) else None


def _optional_scalar_float(value: object) -> float | None:
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    return _optional_finite_float(value)


def _csv_value(value: object) -> object:
    return "" if value is None else value


def _command_record(command: str | Sequence[str] | None) -> str | list[str] | None:
    if command is None:
        return None
    if isinstance(command, str):
        return command
    return [str(part) for part in command]
