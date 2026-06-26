"""Formal Lian 2023 EHA*-NLP paper baseline with local 0.05 m margin."""
from __future__ import annotations

from typing import Any

from forest_n3p.baselines.common import PlannerResult
from forest_n3p.baselines.lian2023.eha_nlp_paper import plan_lian2023_eha_nlp_paper


def plan_lian2023_eha_nlp_paper_margin005(**kwargs: Any) -> PlannerResult:
    """Run the paper-structure Lian 2023 EHA*-NLP planner with 0.05 m margin.

    The margin is a local grid-safety setting used to avoid rectangle-footprint
    contact on the project realmap benchmark while preserving the Lian paper
    planner structure and local Ackermann vehicle parameters.
    """
    f_kwargs = dict(kwargs)
    f_kwargs["safety_margin_m"] = 0.05
    result = plan_lian2023_eha_nlp_paper(**f_kwargs)
    stats = dict(result.stats)
    stats["variant"] = "lian2023_eha_nlp_paper_margin005"
    stats["safety_margin_m"] = 0.05
    return PlannerResult(
        path_xy_cells=result.path_xy_cells,
        time_s=result.time_s,
        success=result.success,
        stats=stats,
    )
