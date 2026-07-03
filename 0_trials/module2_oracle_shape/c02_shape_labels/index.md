# C02 Oracle Shape Labels

本目录保存 C02.2 的首批代表样本可视化。它只标注 full oracle 中的关键机械类别, 还不是最终 Gate #2 判定。

| Case | Shape label | Query | Collides | A | B | Rendered B | Image |
|---|---|---|---|---|---|---|---|
| invalid_goal_complex | `invalid_goal_in_collision` | `complex_s00_q0007` exp=0 | state=False, goal=True | False:goal_in_collision | False:None | False | `invalid_goal_complex.png` |
| invalid_goal_extreme | `invalid_goal_in_collision` | `extreme_s00_q0006` exp=432 | state=False, goal=True | False:goal_in_collision | False:None | False | `invalid_goal_extreme.png` |
| invalid_start_extreme | `invalid_start_in_collision_goal_also_blocked` | `extreme_s00_q0006` exp=1024 | state=True, goal=True | False:start_in_collision | False:None | False | `invalid_start_extreme.png` |
| b_only_complex_timeout | `timeout_saved_by_goal_annulus` | `complex_s00_q0003` exp=4640 | state=False, goal=False | False:timeout | True:goal_annulus | True | `b_only_complex_timeout.png` |
| b_only_extreme_goal_annulus | `timeout_saved_by_goal_annulus` | `extreme_s00_q0003` exp=224 | state=False, goal=False | False:timeout | True:goal_annulus | True | `b_only_extreme_goal_annulus.png` |
| a_only_complex_conservative_b | `oracle_b_conservative_combined_collision_rejection` | `complex_s00_q0002` exp=3424 | state=False, goal=False | True:None | False:None | False | `a_only_complex_conservative_b.png` |
| a_only_extreme_conservative_b | `oracle_b_conservative_combined_collision_rejection` | `extreme_s00_q0003` exp=160 | state=False, goal=False | True:None | False:None | False | `a_only_extreme_conservative_b.png` |
