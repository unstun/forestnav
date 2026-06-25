# iDb-RRT Strict Official Experiment

This folder keeps the official Dynoplan/Dynobench experiment separate from the
local UGV adapters.

The first target is the official `car1_v0` benchmark family from Dynobench:
`parallelpark_0`, `kink_0`, and `bugtrap_0`. These are the vehicle-related
problems available in the public repository. They use Dynobench's
`car_with_trailers` model, not the local UGV parameters.

Official source is fetched into `upstream/dynoplan/`, which is ignored by the
outer Git repository.

## Commands

Fetch official source:

```bash
bash 2_experiment/idb_rrt_strict_repro/scripts/fetch_official_dynoplan.sh
```

Verify source identity:

```bash
bash 2_experiment/idb_rrt_strict_repro/scripts/verify_official_source.sh
```

Run the official `car1_v0` smoke experiment:

```bash
bash 2_experiment/idb_rrt_strict_repro/scripts/run_official_car1_smoke.sh
```
