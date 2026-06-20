"""Configuration helpers for F-N3P experiments."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_CONFIG_PATH = Path(__file__).with_name("default.json")


def load_default_config() -> dict[str, Any]:
    """Load the default F-N3P configuration."""
    with DEFAULT_CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


DEFAULT_CONFIG = load_default_config()

__all__ = ["DEFAULT_CONFIG", "DEFAULT_CONFIG_PATH", "load_default_config"]
