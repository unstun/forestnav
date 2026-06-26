"""iDb-RRT + trajectory optimization baseline entry point.

该文件把当前采用的 iDb-RRT TO baseline 暴露为独立模块，避免正式入口混在
`idb_rrt_local.py` 的本地适配实现中。

实现主体仍在 `idb_rrt_local.plan_idb_rrt_to`，便于保留已有测试和调参历史。
"""
from __future__ import annotations

from forest_n3p.baselines.idb_rrt_local import plan_idb_rrt_to

__all__ = ["plan_idb_rrt_to"]

