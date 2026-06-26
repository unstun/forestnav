"""Lian 2023 EHA* paper baseline entry point.

This module keeps the benchmark-facing file name explicit.  The implementation
currently lives in ``paper_eha.py`` for backward compatibility with existing
tests and imports.
"""
from __future__ import annotations

from forest_n3p.baselines.lian2023.paper_eha import (
    Passage,
    classify_passages,
    extract_paper_boundary_points,
    plan_lian2023_eha_paper,
    run_classic_hybrid_astar_between_boundary_points,
)

__all__ = [
    "Passage",
    "classify_passages",
    "extract_paper_boundary_points",
    "plan_lian2023_eha_paper",
    "run_classic_hybrid_astar_between_boundary_points",
]

