# Lian2023 Strict Reproduction

This directory is an independent Python reproduction workspace for:

J. Lian et al., "Trajectory Planning for Autonomous Valet Parking in Narrow Environments With Enhanced Hybrid A* Search and Nonlinear Optimization," IEEE TIV, 2023.

The implementation deliberately avoids importing `ugv_dqn`, local maps, or local UGV baseline code. The active scope is a paper-oriented reproduction attempt of Algorithm 1 and the main Fig.5/Table II style outputs using figure-reconstructed scenes.

## Current Status

- Table I constants are encoded in `configs/paper_params.yaml` and `src/lian2023_strict/config.py`.
- Four Fig.5-style scenes are reconstructed in `src/lian2023_strict/scenes.py`.
- A*, corridor construction, SWPS/SNPS-style grouping, boundary point selection, EHA-style connection, and IPOPT path smoothing are implemented.
- Non-paper fallbacks have been removed from the OURS route: failed boundary-point Hybrid A* segments now return `stage1_eha_fail`.
- The state-control IPOPT objective includes formula (16) and formula (23)/(24)-style soft penalties for formula (3), formula (7), and formula (15). Fig.5/Table II style runs disable formula (15), matching the paper text that local state constraints are temporarily removed for Fig.5.
- Formula (6) is represented as hard bounds on disk-center decision variables selected from the generated corridor boxes for `k = 0..n-1`. `jpenalty6` is reported as a post-solve diagnostic and is not part of `Jinf`.
- Strict success requires `Jinf <= Etol`. Current local n=200 runs use analytic gradients for formula (16), `Jpenalty(3)`, `Jpenalty(7)`, and `Jpenalty(15)`; 12 / 16 rows pass. OURS passes all four reconstructed Fig.5 scenes.

## Current n=200 Run

```bash
PYTHONPATH=2_experiment/lian2023_strict_repro/src \
python -m lian2023_strict.scripts.run_table2 \
  --out-dir 2_experiment/lian2023_strict_repro/outputs/2026-05-13_lian2023_paper_complete \
  --n-elements 200 \
  --max-iterations 10 \
  --ipopt-max-iterations 1000 \
  --timeout-s 1200
```

The current output directory is:

`outputs/2026-05-13_lian2023_paper_complete/`

This run uses the paper discretization size `n_elements=200` and the paper outer limit `Nmax=10`; local IPOPT is capped at `ipopt_max_iterations=1000` for each outer iteration because the paper does not report the solver's internal iteration cap. The recorded table reports 12 / 16 successful rows. The OURS rows pass fig5a (`Jinf=0.000059192`), fig5b (`Jinf=0.000066674`), fig5c (`Jinf=0.000000034`), and fig5d (`Jinf=0.000076362`).

Remaining gaps for author-code equivalence are exact Matlab scene geometry, private implementation details for T1/T2 corridor and `CorrectBoundaryPoints`, and the signed-velocity treatment needed for reverse Hybrid A* segments.

## Optional C++ OCP Callback

`src/lian2023_strict/ocp_fast.py` can load an optional C++ dynamic library for formula (16) + formula (23) objective / gradient callbacks.

Build it locally with:

```bash
PYTHONPATH=2_experiment/lian2023_strict_repro/src \
python 2_experiment/lian2023_strict_repro/scripts/build_ocp_fast.py
```

Enable it explicitly with:

```bash
LIAN2023_STRICT_USE_CPP=1
```

The default backend remains Python even if the library exists. This keeps paper-size records reproducible and prevents a local compiled artifact from silently changing IPOPT's floating-point trajectory.
