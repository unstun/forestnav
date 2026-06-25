---
citation_key: Li2025MultiAgent
arxiv_id: 2505.07779
arxiv_url: https://arxiv.org/abs/2505.07779
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T15:29:37Z
origin: ai+web
reviewed: false
---

# Introduction {#sec:introduction}

Modern logistics increasingly relies on large-scale automated warehouses and fulfillment centers, where thousands of mobile robots must *coordinate* in shared spaces to fulfill tasks efficiently. This paradigm shift promises transformative gains in throughput and flexibility, but also presents significant challenges [@wurman2008coordinating; @standley2010finding]. One of the core difficulties lies in [acr:mapf]{acronym-label="acr:mapf" acronym-form="singular+short"}, where robots must navigate from start to goal location on a network without colliding. The complexity of such planning problems grows *exponentially* with the number of agents [@silver2005cooperative], making even near-optimal solutions intractable at scale. In standard [acr:mapf]{acronym-label="acr:mapf" acronym-form="singular+short"}, each robot must avoid *vertex* and *edge* conflicts, i.e., occupying the same vertex or traversing the same edge simultaneously with another robot [@stern2019mapf].

**Existing Approaches** -- Numerous [acr:mapf]{acronym-label="acr:mapf" acronym-form="singular+short"} algorithms have been developed, but most are limited in ways that hinder their use in large-scale, real-time warehouse operations. A critical limitation is that many of these algorithms are *offline*, i.e., they require a complete, globally consistent plan before any robot can begin moving. This design prevents early execution of even the first steps, as plans may change due to backtracking, introducing significant delays in time-sensitive environments. [acr:mapf]{acronym-label="acr:mapf" acronym-form="singular+short"} algorithms also vary in their *performance guarantees*. Algorithms such as CBS [@sharon2015conflict], EECBS [@li2021eecbs], and M\* [@wagner2015subdimensional] provide optimal or bounded-suboptimal solutions but scale poorly due to the exponential growth of the joint search space and the inherent NP-hardness [@yu2013planning]. Faster alternatives, such as MAPF-LNS2 [@li2022mapf], LaCAM [@okumura2023lacam], and anytime variants such as MAPF-LNS [@li2021anytime], LaCAM\* [@okumura2023improving], and engineered LaCAM\* [@okumura2023engineering], improve feasibility but still suffer from offline computation and may yield subpar solution quality [@shen2023tracking]. Furthermore, despite recent progress [@lee2021parallel; @okumura2023engineering; @chan2024anytime], most [acr:mapf]{acronym-label="acr:mapf" acronym-form="singular+short"} planners are sequential, underutilizing modern parallelization techniques. These limitations motivate the need for *online*, *scalable*, and *parallelizable* planning tools to support real-time robot coordination at scale.

:::: {#fig:finite_horizon_hierarchical_factorization .figure latex-placement="t"}
![](Li2025MultiAgent_figs/f2_model_0508.png){width="\\linewidth"}

::: caption
The algorithm plans in a receding-horizon fashion, computing and finalizing robot movements one timestep at a time. This online approach enables immediate execution of each computed step.
:::
::::

**Factorization for scalable multi-agent planning** -- *Factorization* has emerged as a powerful tool across domains such as game theory [@zanardi2022factorization] and motion planning [@zanardi2023factorization] to mitigate the curse of dimensionality by exploiting the *problem structure*. The core idea is to leverage *compositionality*[^1]: if subgroups of agents can be planned independently, their solutions can be composed, preserving feasibility and often optimality, withing the larger system. In [acr:mapf]{acronym-label="acr:mapf" acronym-form="singular+short"}, prior methods have pursued this via bottom-up strategies: assuming full independence, then merging agents that conflict [@wagner2015subdimensional; @standley2010finding; @lee2021parallel]. However, because these approaches consider the entire time horizon at once, independence is rare. As a result, agents are frequently replanned in overlapping groups, limiting scalability.

**Contribution** -- We propose a novel online algorithm for large-scale [acr:mapf]{acronym-label="acr:mapf" acronym-form="singular+short"} that combines finite-horizon hierarchical factorization with highly parallelizable planning. The proposed method leverages a uniform greedy optimal planner for individual agents and dynamically groups robots based on conflict and reachability within a finite horizon. Conflict resolution is handled efficiently using a PIBT-based, state-of-the-art routine [@okumura2022priority]. Our method enables immediate execution of each computed step, significantly reducing delay compared to offline methods. Experiments demonstrate faster execution onset and competitive solution quality across diverse scenarios.

# Finite-Horizon Hierarchical Factorization {#sec:finite_horizon_hierarchical_factorization}

[1](#fig:finite_horizon_hierarchical_factorization){reference-type="ref+label" reference="fig:finite_horizon_hierarchical_factorization"} illustrates the presented algorithm in parallelized stages. At each iteration, all robots first compute individual paths in parallel leveraging a balanced greedy planner based on backward BFS [@okumura2022priority] (). Conflicts over the next $H$ timesteps are then detected via spatial hashing, enabling a first-level factorization: conflict-free robots are finalized, while the rest replan while treating finalized robots as dynamic obstacles (). Next, conflicting robots are recursively grouped based on horizon-limited reachability () and replanned in parallel using an adapted PIBT algorithm (). If replanning fails, a congestion resolution module enlarges the group to allow for more spatio-temporal flexibility (). Finally, trajectories are merged, and only the first step is executed ().

The proposed algorithm is fast because both individual planning and groupwise replanning are parallelizable. In practice, many robots remain conflict-free within each horizon, allowing them to follow near-optimal paths while groupwise replanning ensures overall feasibility. This yields solution quality competitive with leading offline methods and significantly outperforms LaCAM\* [@okumura2023improving], the only known offline planner with comparable speed.

# Experimental Results {#sec:experiment_results}

**Experiment Setup** -- The experiments are conducted using [acr:mapf]{acronym-label="acr:mapf" acronym-form="singular+short"} benchmarks [@stern2019mapf][^2]. Due to space constraints, we report results on two challenging maps: the largest warehouse map `warehouse-20-40-10-2-2` and the random map `random-64-64-10`. Each experiment was run 200 times, and we report average performance with statistical attributes.

**Time needed before execution** -- To quantify the advantage of online algorithms, we report the time needed before execution (TNBE). [2](#fig:time_before_exe_warehouse){reference-type="ref+label" reference="fig:time_before_exe_warehouse"} shows the TNBE ratio between our method and the LaCAM\* baseline. While TNBE naturally increases with the number of robots, our algorithm consistently achieves substantial speedups, even at the longest planning horizon (20 steps). For instance, with 900 robots, we observe a 60% reduction in TNBE. Moreover, since each planning step in the proposed method completes in under 30 ms, even at scale, subsequent steps can be planned in parallel with execution, significantly outpacing real-world robot actuation times.

:::: {#fig:time_before_exe_warehouse .figure latex-placement="t"}
![](Li2025MultiAgent_figs/time_before_exe_warehouse_ratio_0507.png){width="\\linewidth"}

::: caption
The ratio of the TNBE between our algorithm and offline baselines; values below 1 indicate that our method achieves faster execution readiness.
:::
::::

:::: {#fig:performance_experiments .figure latex-placement="t"}
![](Li2025MultiAgent_figs/experiment_0507.png){width="\\linewidth"}

::: caption
Our algorithm consistently outperforms LaCAM\* in solution quality across all robot counts. In the warehouse map, performance improves monotonically as the planning horizon increases, while in the random map, the optimal planning horizon varies depending on the number of robots.
:::
::::

**Solution quality** -- Solution quality comparisons with LaCAM\* are shown in [3](#fig:performance_experiments){reference-type="ref+label" reference="fig:performance_experiments"}, using the sum of costs (SOC), i.e., the total travel time of all agents, measured relative to a lower bound that ignores conflicts [@okumura2023improving]. In our setup, LaCAM\* is allowed to continue refining its solution until our algorithm completes all planning steps. On the warehouse map, our method consistently yields higher-quality solutions across all robot counts and horizons. Longer horizons further improve performance by enabling better coordination. On the random map, our algorithm also outperforms LaCAM\*, though gains are not strictly monotonic in horizon length: excessively long horizons reduce the number of conflict-free agents, leading to more frequent and suboptimal groupwise replanning.

# Discussion and Conclusion {#sec:discussion_and_conclusion}

We introduced a scalable online algorithm for [acr:mapf]{acronym-label="acr:mapf" acronym-form="singular+short"} based on finite-horizon hierarchical factorization. By combining parallel individual planning with dynamic two-level grouping based on conflicts and reachability, as well as efficient on-the-fly conflict resolution, our method enables immediate execution and significantly reduces planning delays. Experiments confirm its strong performance both in speed and solution quality, making it a practical alternative to existing offline methods for real-time multi-robot coordination. Future work includes extending the approach to more general task assignment settings [@zardini2022analysis], lifelong MAPF [@ma2017lifelong], co-design with networks [@9963724], learning-enabled improvements [@tresca2025robo], and tighter guarantees.

**Acknowledgments** -- This work was supported by Prof. Zardini's grant from the MIT Amazon Science Hub, hosted in the Schwarzman College of Computing. We thank Dr. Federico Pecora, from Amazon Robotics, Movement Science, for the fruitful discussions and feedback.

[^1]: I.e., the "solution of the composition of problems" is the "composition of the solutions of problems".

[^2]: The experiments were performed on a MacBook Pro 2023 with a 12-core CPU and 36 GB of RAM. The parallel computation used 12 threads. A video of the experiments is available at [youtu.be/v3HfqYDTkGY](https://youtu.be/v3HfqYDTkGY).
