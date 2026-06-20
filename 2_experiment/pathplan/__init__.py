"""Compatibility alias for the vendored F-N3P pathplan package."""

from __future__ import annotations

from importlib import import_module
import sys

_impl = import_module("forest_n3p.third_party.pathplan")
sys.modules[__name__] = _impl
