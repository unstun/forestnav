"""Lian2023 EHA*-NLP EDT baseline entry point.

该文件把当前采用的 Lian2023 EHA*-NLP baseline 暴露为 `baselines` 第一层入口。
实现主体仍在 `lian2023/eha_nlp_edt.py`，这里仅作为正式 baseline 的清晰导出。
"""
from __future__ import annotations

from forest_n3p.baselines.lian2023.eha_nlp_edt import plan_lian2023_eha_nlp_edt

__all__ = ["plan_lian2023_eha_nlp_edt"]

