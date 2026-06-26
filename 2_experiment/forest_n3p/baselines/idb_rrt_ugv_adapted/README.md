# iDb-RRT-UGV adapted baseline

This package is a thin adapter around `forest_n3p.baselines.idb_rrt_paper`.

It keeps the project paper-oriented Db-RRT + control-shooting TO implementation
and replaces only the vehicle geometry and motion limits with the local UGV
parameters:

```text
length=0.924m
width=0.740m
wheelbase=0.600m
vmax=2.0m/s
amax=1.5m/s^2
max_steer=27deg
max_delta_dot=60deg/s
```

The adapter also runs a final collision audit with the shifted oriented
rectangle body model reconstructed from the local UGV footprint. A trajectory is
reported as successful only when the base planner succeeds and this full-body
collision audit passes.

Use this baseline as `iDb-RRT-UGV` in local `realmap_a` experiments. It is not
the original Dynoplan iDb-RRT implementation; the official-source smoke remains
in `2_experiment/idb_rrt_strict_repro/`.
