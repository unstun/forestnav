---
origin: ai+local-source
reviewed: false
status: partial_blocked
created_at: 2026-06-25
---

# T14 9-method remote status

## Summary

The requested 9-method 50-query/bucket run is blocked only by the `idb_rrt`
Dynoplan binary. The Python-side implementation and remote deployment are in
place, and the 8-method run without `idb_rrt` completed on `gpu3070ti-relay`.

## Completed

- Removed the `md_dqn` evaluation entry from the official method set.
- Added `improved_ha`, `lo_ha`, `ss_rrt`, and `idb_rrt` registration.
- Added a fail-soft Dynoplan wrapper for `idb_rrt`.
- Synced code and Dynoplan upstream sources to `gpu3070ti-relay`.
- Remote 8-method smoke completed:
  - Path: `.pipeline/experiments/20260625_smoke_8method_1q_remote`
  - Records: 24
  - Exceptions: 0
- Remote 8-method 50q partial run completed:
  - Path: `.pipeline/experiments/20260625_t14_8method_50q_partial_no_idb`
  - Queries: 150
  - Records: 1200
  - Collision violations: 0
  - Method exceptions: 0
  - `official_methods_satisfied`: false
  - Missing official method: `idb_rrt`

## iDb-RRT blocker

Remote preflight for the full 9-method set failed with:

```text
idb_rrt unavailable: Dynoplan main_idbastar binary not found
```

Dynoplan source and `car1_v0_all.bin.sp.bin.small5000.msgpack` are present on
the remote host, but `main_idbastar` is not built. Building is blocked because
`gpu3070ti-relay` currently lacks the toolchain in PATH:

- `cmake`: missing
- `g++`: missing
- `make`: missing
- `sudo -n true`: fails because sudo requires a password

Dynoplan's top-level CMake requires Boost, OMPL, FCL, yaml-cpp, Crocoddyl,
Eigen3, and LZ4 before it can build `main_idbastar`.

## Boundary

The 8-method 50q output is a useful partial measurement, not a completed
9-method formal result. The verdict code now requires every official method to
be present before `formal_acceptance` can be true.

## Next unblock options

1. Provide sudo access on `gpu3070ti-relay` so the Dynoplan build dependencies
   can be installed.
2. Provide a Linux `main_idbastar` binary built against compatible Dynoplan
   dependencies.
3. Run the iDb-RRT leg on another Linux host that already has a C++17 build
   toolchain plus Dynoplan dependencies.
