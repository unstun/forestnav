---
citation_key: Gammell2014Informed
arxiv_id: 1404.2334
arxiv_url: https://arxiv.org/abs/1404.2334
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T17:15:26Z
origin: ai+web
reviewed: false
---

::: acronym
\[DoFs\]degrees-of-freedom

\[FOVs\]fields of view

\[i.i.d.\]independent and identically distributed

\[VT&R\]visual teach and repeat \[BIT\*\]Batch Informed Trees \[FMT\*\]fast marching tree \[LPA\*\]lifelong planning A\* \[MDPs\]Markov decision processes \[NRPs\]networks of reusable paths \[POMDPs\]partially-observable Markov decision processes \[PRM\*\]optimal [PRMs]{acronym-label="PRM" acronym-form="plural+short"} \[RRT\*\]optimal [RRT]{acronym-label="RRT" acronym-form="singular+abbrv"} \[RRTeh\*\][RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} with ellipsoidal heuristics
:::

::::::::::: spacing
0.965

1.5ex plus 1ex minus 0ex 0.7ex plus 0.5ex minus 0ex []{.smallcaps}Introduction[]{#sec:intro label="sec:intro"} The motion-planning problem is commonly solved by first discretizing the continuous state space with either a grid for graph-based searches or through random sampling for stochastic incremental searches. Graph-based searches, such as A\* [@hart_tssc68], are often *resolution complete* and *resolution optimal*. They are guaranteed to find the optimal solution, if a solution exists, and return failure otherwise (up to the resolution of the discretization). These graph-based algorithms do not scale well with problem size (e.g., state dimension or problem range).

Stochastic searches, such as [RRTs]{acronym-label="RRT" acronym-form="plural+short"} [@lavalle_ijrr01], [PRMs]{acronym-label="PRM" acronym-form="plural+short"} [@kavraki_tro96], and [ESTs]{acronym-label="EST" acronym-form="plural+short"} [@hsu_ijrr02], use sampling-based methods to avoid requiring a discretization of the state space. This allows them to scale more effectively with problem size and to directly consider kinodynamic constraints; however, the result is a less-strict completeness guarantee. [RRTs]{acronym-label="RRT" acronym-form="plural+short"} are *probabilistically complete*, guaranteeing that the probability of finding a solution, if one exists, approaches unity as the number of iterations approaches infinity.

Until recently, these sampling-based algorithms made no claims about the optimality of the solution. Urmson and Simmons [@urmson_iros03] had found that using a heuristic to bias sampling improved [RRT]{acronym-label="RRT" acronym-form="singular+short"} solutions, but did not formally quantify the effects. Ferguson and Stentz [@ferguson_iros06] recognized that the length of a solution bounds the possible improvements from above, and demonstrated an iterative anytime [RRT]{acronym-label="RRT" acronym-form="singular+short"} method to solve a series of subsequently smaller planning problems. Karaman and Frazzoli [@karaman_ijrr11] later showed that [RRTs]{acronym-label="RRT" acronym-form="plural+short"} return a suboptimal path with probability one, demonstrating that all [RRT]{acronym-label="RRT" acronym-form="singular+abbrv"}-based methods will almost surely be suboptimal and presented a new class of optimal planners. They named their optimal variants of [RRTs]{acronym-label="RRT" acronym-form="plural+short"} and [PRMs]{acronym-label="PRM" acronym-form="plural+short"}, [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} and [PRMstar]{acronym-label="PRMstar" acronym-form="singular+abbrv"}, respectively. These algorithms are shown to be *asymptotically optimal*, with the probability of finding the optimal solution approaching unity as the number of iterations approaches infinity.

:::: {#fig:randomWorld2 .figure latex-placement="t"}
![](Gammell2014Informed_figs/randomWorld2.png){width="\\columnwidth"}

::: caption
Solutions of equivalent cost found by [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} and Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} on a random world. After an initial solution is found, Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} focuses the search on an ellipsoidal informed subset of the state space, $X_{\widehat{f}}\subseteq X$, that contains all the states that can improve the current solution regardless of homotopy class. This allows Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} to find a better solution faster than [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} without requiring any additional user-tuned parameters.
:::
::::

:::: {#fig:randomWorld .figure latex-placement="t"}
![](Gammell2014Informed_figs/randomWorld.png){width="\\textwidth"}

::: caption
The solution cost versus computational time for [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} and Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} on a random world problem. Both planners were run until they found a solution of the same cost. Figs. (a, c) show the final result, while Fig. (b) shows the solution cost versus computational time. From Fig. (a), it can be observed that [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} spends significant computational resources exploring regions of the planning problem that cannot possibly improve the current solution, while Fig. (c) demonstrates how Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} focuses the search. .
:::
::::

[RRTs]{acronym-label="RRT" acronym-form="plural+short"} are not asymptotically optimal because the existing state graph biases future expansion. [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} overcomes this by introducing incremental rewiring of the graph. New states are not only added to a tree, but also considered as replacement parents for existing nearby states in the tree. With uniform global sampling, this results in an algorithm that asymptotically finds the optimal solution to the planning problem by *asymptotically finding the optimal paths from the initial state to every state in the problem domain*. This is inconsistent with their single-query nature and becomes expensive in high dimensions.

In this paper, we present the *focused* optimal planning problem as it relates to the minimization of path length in $\mathbb{R}^n$. For such problems, a necessary condition to improve the solution at any iteration is the addition of states from an ellipsoidal subset of the planning domain [@ferguson_iros06], [@gabriely_tro08; @gasilov_iete11; @otte_tro13]. We show that the probability of adding such states through uniform sampling becomes arbitrarily small as the size of the planning problem increases or the solution approaches the theoretical minimum, and present an exact method to sample the ellipsoidal subset directly. It is also shown that with strict assumptions (i.e., no obstacles) that this direct sampling results in linear convergence to the optimal solution.

This direct-sampling method allows for the creation of informed-sampling planners. Such a planner, Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"}, is presented to demonstrate the advantages of *informed* incremental search (Fig. [1](#fig:randomWorld2){reference-type="ref" reference="fig:randomWorld2"}). Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} behaves as [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} until a first solution is found, after which it only samples from the subset of states defined by an admissible heuristic to possibly improve the solution. This subset implicitly balances exploitation versus exploration and requires no additional tuning (i.e., there are no additional parameters) or assumptions (i.e., all relevant homotopy classes are searched). While heuristics may not always improve the search, their prominence in real-world planning demonstrates their practicality. In situations where they provide no additional information (e.g., when the informed subset includes the entire planning problem), Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} is equivalent to [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}.

Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} is a simple modification to [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} that demonstrates a clear improvement. In simulation, it performs as well as existing [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} algorithms on simple configurations, and demonstrates order-of-magnitude improvements as the configurations become more difficult (Fig. [2](#fig:randomWorld){reference-type="ref" reference="fig:randomWorld"}). As a result of its focused search, the algorithm has less dependence on the dimension and domain of the planning problem as well as the ability to find better topologically distinct paths sooner. It is also capable of finding solutions within tighter tolerances of the optimum than [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} with equivalent computation, and in the absence of obstacles can find the optimal solution to within machine zero in finite time (Fig. [3](#fig:machineZero){reference-type="ref" reference="fig:machineZero"}). It could also be used in combination with other algorithms, such as path-smoothing, to further reduce the search space.

The remainder of this paper is organized as follows. Section [\[sec:back\]](#sec:back){reference-type="ref" reference="sec:back"} presents a formal definition of the focused optimal planning problem and reviews the existing literature. Section [\[sec:ellipse\]](#sec:ellipse){reference-type="ref" reference="sec:ellipse"} presents a closed-form estimate of the subset of states that can improve a solution for problems seeking to minimize path length in $\mathbb{R}^n$ and analyzes the implications on [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}-style algorithms. Section [\[sec:sample\]](#sec:sample){reference-type="ref" reference="sec:sample"} presents a method to sample this subset directly. Section [\[sec:algorithm\]](#sec:algorithm){reference-type="ref" reference="sec:algorithm"} presents the Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} algorithm and Section [\[sec:sim\]](#sec:sim){reference-type="ref" reference="sec:sim"} presents simulation results comparing [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} and Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} on simple planning problems of various size and configuration and random problems of various dimension. Section [\[sec:end\]](#sec:end){reference-type="ref" reference="sec:end"} concludes the paper with a discussion of the technique and some related ongoing work.

:::: {#fig:machineZero .figure latex-placement="t"}
![](Gammell2014Informed_figs/machineZero.png)

::: caption
Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} converging to within machine zero of the optimum in the absence of obstacles. The start and goal states are shown as green and red, respectively, and are 100 units apart. The current solution is highlighted in magenta, and the ellipsoidal sampling domain, $X_{\widehat{f}}$, is shown as a grey dashed line for illustration. Improving the solution decreases the size of the sampling domain, creating a feedback effect that converges to within machine zero of the theoretical minimum. Fig. (a) shows the first solution at 59 iterations, (b) after 175 iterations, and (c), the final solution after 1142 iterations, at which point the ellipse has degenerated to a line between the start and goal.
:::
::::

1.5ex plus 1ex minus 0ex 0.7ex plus 0.5ex minus 0ex []{.smallcaps}Background[]{#sec:back label="sec:back"}

## Problem Definition {#sec:back:defn}

We define the optimal planning problem similarly to [@karaman_ijrr11]. Let $X\subseteq \mathbb{R}^n$ be the state space of the planning problem. Let $X_{\rm obs}\subsetneq X$ be the states in collision with obstacles and $X_{\rm free}= X\setminus X_{\rm obs}$ be the resulting set of permissible states. Let $\mathbf{x}_{\rm start}\in X_{\rm free}$ be the initial state and $\mathbf{x}_{\rm goal}\in X_{\rm free}$ be the desired final state. Let $\sigma: \; \left[0,1\right] \mapsto X$ be a sequence of states (a path) and $\Sigma$ be the set of all nontrivial paths.

The optimal planning problem is then formally defined as the search for the path, $\sigma^{*}$, that minimizes a given cost function, $c: \; \Sigma\mapsto \mathbb{R}_{\geq0}$, while connecting $\mathbf{x}_{\rm start}$ to $\mathbf{x}_{\rm goal}$ through free space, $$\begin{align*}
\sigma^{*}= \mathop{\mathrm{arg\,min}}_{\sigma\in \Sigma}\left\lbrace c\left(\sigma\right) \;\; \middle| \;\; \right. & \sigma(0) = \mathbf{x}_{\rm start},\, \sigma(1) = \mathbf{x}_{\rm goal},\\
& \;\;\; \left. \forall s \in \left[ 0,1 \right],\, \sigma\left(s\right) \in X_{\rm free}\right\rbrace,
\end{align*}$$ where $\mathbb{R}_{\geq0}$ is the set of non-negative real numbers.

Let $f\left(\mathbf{x}\right)$ be the cost of an optimal path from $\mathbf{x}_{\rm start}$ to $\mathbf{x}_{\rm goal}$ constrained to pass through $\mathbf{x}$. Then the subset of states that can improve the current solution, $X_{f}\subseteq X$, can be expressed in terms of the current solution cost, $c_{\rm best}$, $$\begin{align}
\label{eqn:fset}
    X_{f}= \left\lbrace \mathbf{x}\in X\;\; \middle| \;\; f\left(\mathbf{x}\right) < c_{\rm best}\right\rbrace.
\end{align}$$ The problem of focusing [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}'s search in order to increase the convergence rate is equivalent to increasing the probability of adding a random state from $X_{f}$.

As $f\left(\cdot\right)$ is generally unknown, a heuristic function, $\widehat{f}\left(\cdot\right)$, may be used as an estimate. This heuristic is referred to as *admissible* if it never overestimates the true cost of the path, i.e., $\forall \mathbf{x}\in X, \; \widehat{f}\left(\mathbf{x}\right) \leq f\left(\mathbf{x}\right)$. An estimate of $X_{f}$, $X_{\widehat{f}}$, can then be defined analogously to [\[eqn:fset\]](#eqn:fset){reference-type="eqref" reference="eqn:fset"}. For admissible heuristics, this estimate is guaranteed to completely contain the true set, $X_{\widehat{f}}\supseteq X_{f}$, and thus inclusion in the estimated set is also a necessary condition to improving the current solution.

## Prior Work {#sec:back:lit}

Prior work to focus [RRT]{acronym-label="RRT" acronym-form="singular+short"} and [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} has relied on sample biasing, heuristic-based sample rejection, heuristic-based graph pruning, and/or iterative searches.

### Sample Biasing {#sec:back:list:bias}

Sample biasing attempts to increase the frequency that states are sampled from $X_{f}$ by biasing the distribution of samples drawn from $X$. This continues to add states from outside of $X_{f}$ that cannot improve the solution. It also results in a nonuniform density over the problem being searched, violating a key [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} assumption.

#### Heuristic-biased Sampling {#sec:back:lit:bias:f}

Heuristic-biased sampling attempts to increase the probability of sampling $X_{f}$ by weighting the sampling of $X$ with a heuristic estimate of each state. It is used to improve the quality of a regular [RRT]{acronym-label="RRT" acronym-form="singular+short"} by Urmson and Simmons [@urmson_iros03] in the [hRRT]{acronym-label="hRRT" acronym-form="singular+short"} by selecting states with a probability inversely proportional to their heuristic cost. The [hRRT]{acronym-label="hRRT" acronym-form="singular+short"} was shown to find better solutions than [RRT]{acronym-label="RRT" acronym-form="singular+short"}; however, the use of RRTs means that the solution is almost surely suboptimal [@karaman_ijrr11].

Kiesel et al. [@kiesel_socs12] use a two-stage process to create an [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} heuristic in their *f-biasing* technique. A coarse abstraction of the planning problem is initially solved to provide a heuristic cost for each discrete state. [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} then samples new states by randomly selecting a discrete state and sampling inside it with a continuous uniform distribution. The discrete sampling is biased such that states belonging to the abstracted solution have the highest probability of selection. This technique provides a heuristic bias for the full duration of the [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} algorithm; however, to account for the discrete abstraction it maintains a nonzero probability of selecting every state. As a result, states that cannot improve the current solution are still sampled.

#### Path Biasing {#sec:back:lit:bias:path}

Path-biased sampling attempts to increase the frequency of sampling $X_{f}$ by sampling around the current solution path. This assumes that the current solution is either homotopic to the optimum or separated only by small obstacles. As this assumption is not generally true, path-biasing algorithms must also continue to sample globally to avoid local optima. The ratio of these two sampling methods is frequently a user-tuned parameter.

Alterovitz et al. [@alterovitz_icra11] use path biasing to develop the [RRM]{acronym-label="RRM" acronym-form="singular+short"}. Once an initial solution is found, each iteration of the [RRM]{acronym-label="RRM" acronym-form="singular+short"} either samples a new state or selects an existing state from the current solution and refines it. Path refinement occurs by connecting the selected state to its neighbours resulting in a graph instead of a tree.

Akgun and Stilman [@akgun_iros11] use path biasing in their dual-tree version of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}. Once an initial solution is found, the algorithm spends a user-specified percentage of its iterations refining the current solution. It does this by randomly selecting a state from the solution path and then explicitly sampling from its Voronoi region. This increases the probability of improving the current path at the expense of exploring other homotopy classes. Their algorithm also employs sample rejection in exploring the state space (Section [0.2.2](#sec:back:reject){reference-type="ref" reference="sec:back:reject"}).

Nasir et al. [@nasir_ijars13] combine path biasing with smoothing in their [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"}-Smart algorithm. When a solution is found, [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"}-Smart first smooths and reduces the path to its minimum number of states before using these states as biases for further sampling. This adds the complexity of a path-smoothing algorithm to the planner while still requiring global sampling to avoid local optima. While the path smoothing quickly reduces the cost of the current solution, it may also reduce the probability of finding a different homotopy class by removing the number of bias points about which samples are drawn and further violates the [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} assumption of uniform density.

Kim et al. [@kim_icra14] use a visibility analysis to generate an initial bias in their Cloud RRT\* algorithm. This bias is updated as a solution is found to further concentrate sampling near the path.

### Heuristic-based Sample Rejection {#sec:back:reject}

Heuristic-based sample rejection attempts to increase the real-time rate of sampling $X_{f}$ by using rejection sampling on $X$ to sample $X_{\widehat{f}}$. Samples drawn from a larger distribution are either kept or rejected based on their heuristic value. Akgun and Stilman [@akgun_iros11] use such a technique in their algorithm. While this is computationally inexpensive for a single iteration, the number of iterations necessary to find a single state in $X_{\widehat{f}}$ is proportional to its size relative to the sampling domain. This becomes nontrivial as the solution approaches the theoretical minimum or the planning domain grows.

Otte and Correll [@otte_tro13] draw samples from a subset of the planning domain in their parallelized C-FOREST algorithm. This subset is defined as the hyperrectangle that bounds the prolate hyperspheroidal informed subset. While this improves the performance of sample rejection, its utility decreases as the dimension of the problem increases (Remark [2](#rem:rect){reference-type="ref" reference="rem:rect"}).

### Graph Pruning {#sec:back:prune}

Graph pruning attempts to increase the real-time exploration of $X_{f}$ by using a heuristic function to limit the graph to $X_{\widehat{f}}$. States in the planning graph with a heuristic cost greater than the current solution are periodically removed while global sampling is continued. The space-filling nature of [RRTs]{acronym-label="RRT" acronym-form="plural+short"} biases the expansion of the pruned graph towards the perimeter of $X_{\widehat{f}}$. After the subset is filled, only samples from within $X_{\widehat{f}}$ itself can add new states to the graph. In this way, graph pruning becomes a rejection-sampling method after greedily filling the target subset. As adding a new state to an [RRT]{acronym-label="RRT" acronym-form="singular+short"} requires a call to a nearest-neighbour algorithm, graph pruning will be more computationally expensive than simple sample rejection while still suffering from the same probabilistic limitations.

Karaman et al. [@karaman_icra11] use graph pruning to implement an anytime version of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} that improves solutions during execution. They use the current vertex cost plus a heuristic estimate of the cost from the vertex to the goal to periodically remove states from the tree that cannot improve the current solution. As [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} asymptotically approaches the optimal cost of a vertex *from above*, this is an inadmissible heuristic for the cost of a solution through a vertex (Section [\[sec:ellipse\]](#sec:ellipse){reference-type="ref" reference="sec:ellipse"}). This can overestimate the heuristic cost of a vertex resulting in erroneous removal, especially early in the algorithm when the tree is coarse. Jordan and Perez [@jordan_tech13] use the same inadmissible heuristic in their bidirectional [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} algorithm.

Arslan and Tsiotras [@arslan_icra13] use a graph structure and [LPAstar]{acronym-label="LPAstar" acronym-form="singular+short"} [@koenig_ai04] techniques in the [RRT]{acronym-label="RRT" acronym-form="singular+abbrv"}\# algorithm to prune the existing graph. Each existing state is given a [LPAstar]{acronym-label="LPAstar" acronym-form="singular+short"}-style key that is updated after the addition of each new state. Only keys that are less than the current best solution are updated, and only up-to-date keys are available for connection with newly drawn samples.

### Anytime [RRTs]{acronym-label="RRT" acronym-form="plural+abbrv"}

Ferguson and Stentz [@ferguson_iros06] recognized that a solution bounds the subset of states that can provide further improvement from above. Their iterative [RRT]{acronym-label="RRT" acronym-form="singular+short"} method, Anytime [RRTs]{acronym-label="RRT" acronym-form="plural+abbrv"}, solves a series of independent planning problems whose domains are defined by the previous solution. They represent these domains as ellipses \[, Fig. 2\], but do not discuss how to generate samples. Restricting the planning domain encourages each [RRT]{acronym-label="RRT" acronym-form="singular+short"} to find a better solution than the previous; however, to do so they must discard the states already found in $X_{\widehat{f}}$.

The algorithm presented in this paper calculates $X_{\widehat{f}}$ explicitly and samples from it directly. Unlike path biasing it makes no assumptions about the homotopy class of the optimum and unlike heuristic biasing does not explore states that cannot improve the solution. As it is based on [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}, it is able to keep all states found in $X_{\widehat{f}}$ for the duration of the search, unlike Anytime [RRTs]{acronym-label="RRT" acronym-form="plural+abbrv"}. By sampling $X_{\widehat{f}}$ directly, it always samples potential improvements regardless of the relative size of $X_{\widehat{f}}$ to $X$. This allows it to work effectively regardless of the size of the planning problem or the relative cost of the current solution to the theoretical minimum, unlike sample rejection and graph pruning methods. In problems where the heuristic does not provide any additional information, it performs identically to [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}.

:::: {#fig:ellipse .figure latex-placement="tb"}
![](Gammell2014Informed_figs/ellipse_diagram.png)

::: caption
The heuristic sampling domain, $X_{\widehat{f}}$, for a $\mathbb{R}^2$ problem seeking to minimize path length is an ellipse with the initial state, $\mathbf{x}_{\rm start}$, and the goal state, $\mathbf{x}_{\rm goal}$ as focal points. The shape of the ellipse depends on both the initial and goal states, the theoretical minimum cost between the two, $c_{\rm min}$, and the cost of the best solution found to date, $c_{\rm best}$. The eccentricity of the ellipse is given by $c_{\rm min}/c_{\rm best}$.
:::
::::

1.5ex plus 1ex minus 0ex 0.7ex plus 0.5ex minus 0ex []{.smallcaps}Analysis of the Ellipsoidal Informed Subset[]{#sec:ellipse label="sec:ellipse"} Given a positive cost function, the cost of an optimal path from $\mathbf{x}_{\rm start}$ to $\mathbf{x}_{\rm goal}$ constrained to pass through $\mathbf{x}\in X$, $f\left(\mathbf{x}\right)$, is equal to the cost of the optimal path from $\mathbf{x}_{\rm start}$ to $\mathbf{x}$, $g\left(\mathbf{x}\right)$, plus the cost of the optimal path from $\mathbf{x}$ to $\mathbf{x}_{\rm goal}$, $h\left(\mathbf{x}\right)$. As [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}-based algorithms asymptotically approach the optimal path to every state *from above*, an admissible heuristic estimate, $\widehat{f}\left(\cdot\right)$, must estimate both these terms. A sufficient condition for admissibility is that the components, $\widehat{g}\left(\cdot\right)$ and $\widehat{h}\left(\cdot\right)$, are individually admissible heuristics of $g\left(\cdot\right)$ and $h\left(\cdot\right)$, respectively.

For problems seeking to minimize path length in $\mathbb{R}^n$, Euclidean distance is an admissible heuristic for both terms (even with motion constraints). This *informed* subset of states that may improve the current solution, $X_{\widehat{f}}\supseteq X_{f}$, can then be expressed in closed form in terms of the cost of the current solution, $c_{\rm best}$, as $$\begin{align*}
%
%
%
X_{\widehat{f}}= \left\lbrace \mathbf{x}\in X\;\; \middle| \;\; \left|\left| \mathbf{x}_{\rm start}- \mathbf{x} \right|\right|_{2} + \left|\left| \mathbf{x}- \mathbf{x}_{\rm goal} \right|\right|_{2} \leq c_{\rm best}\right\rbrace,
\end{align*}$$ which is the general equation of an $n$-dimensional prolate hyperspheroid (i.e., a special hyperellipsoid). The focal points are $\mathbf{x}_{\rm start}$ and $\mathbf{x}_{\rm goal}$, the transverse diameter is $c_{\rm best}$, and the conjugate diameters are $\sqrt{c_{\rm best}^2 - c_{\rm min}^2}$ (Fig. [4](#fig:ellipse){reference-type="ref" reference="fig:ellipse"}).

Admissibility of $\widehat{f}\left(\cdot\right)$ makes adding a state in $X_{\widehat{f}}$ a necessary condition to improve the solution. With the space-filling nature of [RRT]{acronym-label="RRT" acronym-form="singular+short"}, the probability of adding such a state quickly becomes the probability of sampling such a state. Thus, the probability of improving the solution at any iteration by uniformly sampling a larger subset, $\mathbf{x}^{i+1} \sim \mathcal{U}\left(X_{\rm s}\right),\, X_{\rm s}\supseteq X_{\widehat{f}}$, is less than or equal to the ratio of set measures $\lambda\left(\cdot\right)$, $$\begin{align}
\label{eqn:sampleProb}%
    P\left(c_{\rm best}^{i+1}<c_{\rm best}^i\right) &\leq P\left(\mathbf{x}^{i+1}\in X_{f}\right)\\
        &\leq P\left(\mathbf{x}^{i+1}\in X_{\widehat{f}}\right) = \tfrac{\lambda\left(X_{\widehat{f}}\right)}{\lambda\left(X_{\rm s}\right)}.\nonumber
\end{align}$$ Using the volume of a prolate hyperspheroid in $\mathbb{R}^n$ gives $$\begin{align}
\label{eqn:ellipseProb}%
    P\left(c_{\rm best}^{i+1}<c_{\rm best}^i\right) \leq \tfrac{c_{\rm best}^i \left( c_{\rm best}^{i^2} - c_{\rm min}^2 \right)^{\tfrac{n-1}{2}} \zeta_n}{2^n\lambda\left(X_{\rm s}\right)},
\end{align}$$ with $\zeta_n$ being the volume of a unit $n$-ball.

::: {#rem:rej .rem}
**Remark 1** (Rejection sampling). *From [\[eqn:ellipseProb\]](#eqn:ellipseProb){reference-type="eqref" reference="eqn:ellipseProb"} it can be observed that the probability of improving a solution through uniform sampling becomes arbitrarily small for large subsets (e.g., global sampling) or as the solution approaches the theoretical minimum.*
:::

::: {#rem:rect .rem}
**Remark 2** (Rectangular rejection sampling). *Let $X_{\rm s}$ be a hyperrectangle that tightly bounds the informed subset (i.e., the widths of each side correspond to the diameters of the prolate hyperspheroid) [@otte_tro13]. From [\[eqn:ellipseProb\]](#eqn:ellipseProb){reference-type="eqref" reference="eqn:ellipseProb"}, the probability that a sample drawn uniformly from $X_{\rm s}$ will be in $X_{\widehat{f}}$ is then $\frac{\zeta_n}{2^n}$, which decreases rapidly with $n$. For example, with $n=6$ this gives a maximum $8\%$ probability of improving a solution at each iteration through rejection sampling regardless of the specific solution, problem, or algorithm parameters.*
:::

::: {#thm:converge .thm}
**Theorem 1** (Obstacle-free linear convergence). *With uniform sampling of the informed subset, $\mathbf{x}\sim \mathcal{U}\left(X_{\widehat{f}}\right)$, the cost of the best solution, $c_{\rm best}$, converges linearly to the theoretical minimum, $c_{\rm min}$, in the absence of obstacles.*
:::

::: proof
*Proof.* The heuristic value of a state is equal to the transverse diameter of a prolate hyperspheroid that passes through the state and has focal points at $\mathbf{x}_{\rm start}$ and $\mathbf{x}_{\rm goal}$. With uniform sampling, the expectation is then [@gammell_arxiv14] $$\begin{align}
 \label{eqn:expect}%
    E\left[\widehat{f}\left(\mathbf{x}\right)\right] = \tfrac{nc_{\rm best}^2 + c_{\rm min}^2}{\left(n+1\right)c_{\rm best}}.
\end{align}$$ We assume that the [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} rewiring parameter is greater than the diameter of the informed subset, similarly to how the proof of the asymptotic optimality of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} assumes that $\eta$ is greater than the diameter of the planning problem [@karaman_ijrr11]. The expectation of the solution cost, $c_{\rm best}^{i}$, is then the expectation of the heuristic cost of a sample drawn from a prolate hyperspheroid of diameter $c_{\rm best}^{i-1}$, i.e., $E\left[c_{\rm best}^{i}\right] = E\left[\widehat{f}\left(\mathbf{x}^i\right)\right]$. From [\[eqn:expect\]](#eqn:expect){reference-type="eqref" reference="eqn:expect"} it follows that the solution cost converges linearly with a rate, $\mu$, that depends only on the state dimension [@gammell_arxiv14], $$\begin{align*}
%
    \mu =  \left. \tfrac{\partial E\left[c_{\rm best}^{i}\right]}{\partial c_{\rm best}^{i-1}} \right|_{c_{\rm best}^{i-1} = c_{\rm min}} = \tfrac{n - 1}{n+1}.
\end{align*}$$ ◻
:::

While the obstacle-free assumption is impractical, Thm. [1](#thm:converge){reference-type="ref" reference="thm:converge"} illustrates the fundamental effectiveness of direct informed sampling and provides possible insight for future work.

1.5ex plus 1ex minus 0ex 0.7ex plus 0.5ex minus 0ex []{.smallcaps}Direct Sampling of an Ellipsoidal Subset[]{#sec:sample label="sec:sample"} Uniformly distributed samples in a hyperellipsoid, $\mathbf{x}_{\rm ellipse}\sim \mathcal{U}\left(X_{\rm ellipse}\right)$, can be generated by transforming uniformly distributed samples from the unit $n$-ball, $\mathbf{x}_{\rm ball}\sim \mathcal{U}\left(X_{\rm ball}\right)$, $$\begin{align*}
%
    \mathbf{x}_{\rm ellipse}= \mathbf{L} \mathbf{x}_{\rm ball}+ \mathbf{x}_{\rm centre},
\end{align*}$$ where $\mathbf{x}_{\rm centre}= \left(\mathbf{x}_{f1}+ \mathbf{x}_{f2}\right)/2$ is the centre of the hyperellipsoid in terms of its two focal points, $\mathbf{x}_{f1}$ and $\mathbf{x}_{f2}$, and $X_{\rm ball}= \left\lbrace \mathbf{x}\in X\;\; \middle| \;\; \left|\left| \mathbf{x} \right|\right|_{2} \leq 1 \right\rbrace$ [@sun_fusion02].

This transformation can be calculated by Cholesky decomposition of the hyperellipsoid matrix, $\mathbf{S} \in \mathbb{R}^{n \times n}$, $$\begin{align*}
%
    \mathbf{L}\mathbf{L}^T \equiv \mathbf{S},
\end{align*}$$ where $$\begin{align*}
%
    \left( \mathbf{x}- \mathbf{x}_{\rm centre}\right)^T\mathbf{S}\left( \mathbf{x}- \mathbf{x}_{\rm centre}\right) = 1,
\end{align*}$$ with $\mathbf{S}$ having eigenvectors corresponding to the axes of the hyperellipsoid, $\left\lbrace \mathbf{a}_i \right\rbrace$, and eigenvalues corresponding to the squares of its radii, $\left\lbrace r_i^2 \right\rbrace$. The transformation, $\mathbf{L}$, maintains the uniform distribution in $X_{\rm ellipse}$ [@gammell_arxiv14b].

For prolate hyperspheroids, such as $X_{\widehat{f}}$, the transformation can be calculated from just the transverse axis and the radii. The hyperellipsoid matrix in a coordinate system aligned with the transverse axis is the diagonal matrix $$\begin{align*}
%
    \mathbf{S} = \mathop{\mathrm{diag}}\left\lbrace \tfrac{c_{\rm best}^2}{4}, \tfrac{c_{\rm best}^2 - c_{\rm min}^2}{4}, \ldots, \tfrac{c_{\rm best}^2 - c_{\rm min}^2}{4} \right\rbrace,
\end{align*}$$ with a resulting decomposition of $$\begin{align}
\label{eqn:finalL}%
    \mathbf{L} = \mathop{\mathrm{diag}}\left\lbrace \tfrac{c_{\rm best}}{2}, \tfrac{\sqrt{c_{\rm best}^2 - c_{\rm min}^2}}{2}, \ldots, \tfrac{\sqrt{c_{\rm best}^2 - c_{\rm min}^2}}{2} \right\rbrace,
\end{align}$$ where $\mathop{\mathrm{diag}}\left\lbrace\cdot\right\rbrace$ denotes a diagonal matrix.

The rotation from the hyperellipsoid frame to the world frame, $\mathbf{C} \in SO\left( n \right)$, can be solved directly as a general Wahba problem [@wahba_siam65]. It has been shown that a valid solution can be found even when the problem is underspecified [@ruiter_jgcs13]. The rotation matrix is given by $$\begin{align}
 \label{eqn:svd}%
    \mathbf{C} = \mathbf{U}\mathop{\mathrm{diag}}\left\lbrace 1, \ldots, 1, \det\left(\mathbf{U}\right) \det\left(\mathbf{V}\right) \right\rbrace \mathbf{V}^{T},
\end{align}$$ where $\det\left(\cdot\right)$ is the matrix determinant and $\mathbf{U} \in \mathbb{R}^{n\times n}$ and $\mathbf{V} \in \mathbb{R}^{n\times n}$ are unitary matrices such that $\mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^T \equiv \mathbf{M}$ via singular value decomposition. The matrix $\mathbf{M}$ is given by the outer product of the transverse axis in the world frame, $\mathbf{a}_1$, and the first column of the identity matrix, $\mathbf{1}_1$, $$\begin{align*}
%
    \mathbf{M} = \mathbf{a}_1\mathbf{1}_1^T,
\end{align*}$$ where $$\begin{align*}
%
    \mathbf{a}_{1} = \left( \mathbf{x}_{\rm goal}- \mathbf{x}_{\rm start}\right)/\left|\left| \mathbf{x}_{\rm goal}- \mathbf{x}_{\rm start} \right|\right|_{2}.
\end{align*}$$

A state uniformly distributed in the informed subset, $\mathbf{x}_{\widehat{f}}\sim \mathcal{U}\left(X_{\widehat{f}}\right)$, can thus be calculated from a sample drawn uniformly from a unit $n$-ball, $\mathbf{x}_{\rm ball}\sim \mathcal{U}\left(X_{\rm ball}\right)$, through a transformation [\[eqn:finalL\]](#eqn:finalL){reference-type="eqref" reference="eqn:finalL"}, rotation [\[eqn:svd\]](#eqn:svd){reference-type="eqref" reference="eqn:svd"}, and translation, $$\begin{align}
 \label{eqn:sample}
    \mathbf{x}_{\widehat{f}}= \mathbf{C}\mathbf{L}\mathbf{x}_{\rm ball}+ \mathbf{x}_{\rm centre}.
\end{align}$$ This procedure is presented algorithmically in Alg. [\[algo:sample\]](#algo:sample){reference-type="ref" reference="algo:sample"}.

::: algorithm
$V\gets \left\lbrace \mathbf{x}_{\rm start}\right\rbrace$ $E\gets \emptyset$ $X_{\rm soln}\gets \emptyset$ []{#algo:body:init label="algo:body:init"} $\mathcal{T}= \left( V, E\right)$

$c_{\rm best}\gets \min_{\mathbf{x}_{\rm soln}\in X_{\rm soln}}\left\lbrace \mathtt{Cost}\left( \mathbf{x}_{\rm soln}\right)\right\rbrace$ []{#algo:body:best label="algo:body:best"} $\mathbf{x}_{\rm rand}\gets \mathtt{Sample}\left(\mathbf{x}_{\rm start}, \mathbf{x}_{\rm goal}, c_{\rm best}\right)$ []{#algo:body:sample label="algo:body:sample"} $\mathbf{x}_{\rm nearest}\gets \mathtt{Nearest}\left(\mathcal{T}, \mathbf{x}_{\rm rand}\right)$ $\mathbf{x}_{\rm new}\gets \mathtt{Steer}\left(\mathbf{x}_{\rm nearest}, \mathbf{x}_{\rm rand}\right)$

$V\gets \cup \left\lbrace \mathbf{x}_{\rm new}\right\rbrace$ $X_{\rm near}\gets \mathtt{Near}\left(\mathcal{T}, \mathbf{x}_{\rm new}, r_{\mathrm{RRT}^*} \right)$ $\mathbf{x}_{\rm min}\gets \mathbf{x}_{\rm nearest}$ $c_{\rm min}\gets \mathtt{Cost}\left( \mathbf{x}_{\rm min}\right) + c\cdot\mathtt{Line}\left( \mathbf{x}_{\rm nearest}, \mathbf{x}_{\rm new}\right)$ $c_{\rm new}\gets \mathtt{Cost}\left( \mathbf{x}_{\rm near}\right) + c\cdot\mathtt{Line}\left( \mathbf{x}_{\rm near}, \mathbf{x}_{\rm new}\right)$ $\mathbf{x}_{\rm min}\gets \mathbf{x}_{\rm near}$ $c_{\rm min} \gets c_{\rm new}$ $E\gets E\cup \left\lbrace\left(\mathbf{x}_{\rm min}, \mathbf{x}_{\rm new}\right)\right\rbrace$

$c_{\rm near}\gets \mathtt{Cost}\left(\mathbf{x}_{\rm near}\right)$ $c_{\rm new}\gets \mathtt{Cost}\left( \mathbf{x}_{\rm new}\right) + c\cdot\mathtt{Line}\left( \mathbf{x}_{\rm new}, \mathbf{x}_{\rm near}\right)$ $\mathbf{x}_{\rm parent}\gets \mathtt{Parent}\left(\mathbf{x}_{\rm near}\right)$ $E\gets E\setminus \left\lbrace \left(\mathbf{x}_{\rm parent}, \mathbf{x}_{\rm near}\right) \right\rbrace$ $E\gets E\cup \left\lbrace \left( \mathbf{x}_{\rm new}, \mathbf{x}_{\rm near}\right)\right\rbrace$

$X_{\rm soln}\gets X_{\rm soln}\cup \left\lbrace \mathbf{x}_{\rm new}\right\rbrace$[]{#algo:body:goalEnd label="algo:body:goalEnd"}
:::

1.5ex plus 1ex minus 0ex 0.7ex plus 0.5ex minus 0ex []{.smallcaps}Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"}[]{#sec:algorithm label="sec:algorithm"} An example algorithm using direct informed sampling, Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"}, is presented in Algs. [\[algo:body\]](#algo:body){reference-type="ref" reference="algo:body"} and [\[algo:sample\]](#algo:sample){reference-type="ref" reference="algo:sample"}. It is identical to [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} as presented in [@karaman_ijrr11], with the addition of lines [\[algo:body:init\]](#algo:body:init){reference-type="ref" reference="algo:body:init"}, [\[algo:body:best\]](#algo:body:best){reference-type="ref" reference="algo:body:best"}, [\[algo:body:sample\]](#algo:body:sample){reference-type="ref" reference="algo:body:sample"}, [\[algo:body:goalStart\]](#algo:body:goalStart){reference-type="ref" reference="algo:body:goalStart"}, and [\[algo:body:goalEnd\]](#algo:body:goalEnd){reference-type="ref" reference="algo:body:goalEnd"}. Like [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}, it searches for the optimal path, $\sigma^{*}$, to a planning problem by incrementally building a tree in state space, $\mathcal{T}= \left( V, E\right)$, consisting of a set of vertices, $V\subseteq X_{\rm free}$, and edges, $E\subseteq X_{\rm free}\times X_{\rm free}$. New vertices are added by growing the graph in free space towards randomly selected states. The graph is rewired with each new vertex such that the cost of the nearby vertices are minimized.

The algorithm differs from [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} in that once a solution is found, it focuses the search on the part of the planning problem that can improve the solution. It does this through direct sampling of the ellipsoidal heuristic. As solutions are found (line [\[algo:body:goalStart\]](#algo:body:goalStart){reference-type="ref" reference="algo:body:goalStart"}), Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} adds them to a list of possible solutions (line [\[algo:body:goalEnd\]](#algo:body:goalEnd){reference-type="ref" reference="algo:body:goalEnd"}). It uses the minimum of this list (line [\[algo:body:best\]](#algo:body:best){reference-type="ref" reference="algo:body:best"}) to calculate and sample $X_{\widehat{f}}$ directly (line [\[algo:body:sample\]](#algo:body:sample){reference-type="ref" reference="algo:body:sample"}). As is conventional, we take the minimum of an empty set to be infinity. The new subfunctions are described below, while descriptions of subfunctions common to [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} can be found in [@karaman_ijrr11]:

`Sample`: Given two poses, $\mathbf{x}_{\rm from},\,\mathbf{x}_{\rm to}\in X_{\rm free}$ and a maximum heuristic value, $c_{\rm max}\in \mathbb{R}$, the function $\mathtt{Sample}\left( \mathbf{x}_{\rm from}, \mathbf{x}_{\rm to}, c_{\rm max}\right)$ returns [iid]{acronym-label="iid" acronym-form="singular+short"} samples from the state space, $\mathbf{x}_{\rm new}\in X$, such that the cost of an optimal path between $\mathbf{x}_{\rm from}$ and $\mathbf{x}_{\rm to}$ that is constrained to go through $\mathbf{x}_{\rm new}$ is less than $c_{\rm max}$ as described in Section [\[sec:ellipse\]](#sec:ellipse){reference-type="ref" reference="sec:ellipse"} and Alg. [\[algo:sample\]](#algo:sample){reference-type="ref" reference="algo:sample"}. In most planning problems, $\mathbf{x}_{\rm from}\equiv \mathbf{x}_{\rm start}$, $\mathbf{x}_{\rm to}\equiv \mathbf{x}_{\rm goal}$, and lines [\[algo:sample:start\]](#algo:sample:start){reference-type="ref" reference="algo:sample:start"} to [\[algo:sample:end\]](#algo:sample:end){reference-type="ref" reference="algo:sample:end"} of Alg. [\[algo:sample\]](#algo:sample){reference-type="ref" reference="algo:sample"} can be calculated once at the start of the problem.

`InGoalRegion`: Given a pose, $\mathbf{x}\in X_{\rm free}$, the function $\mathtt{InGoalRegion}\left(\mathbf{x}\right)$ returns $\mathtt{True}$ if and only if the state is in the goal region, $X_{\rm goal}$, as defined by the planning problem, otherwise it returns $\mathtt{False}$. One common goal region is a ball of radius $r_{\rm goal}$ centred about the goal, i.e., $$\begin{align*}
%
    X_{\rm goal}= \left\lbrace \mathbf{x}\in X_{\rm free}\;\; \middle| \;\; \left|\left| \mathbf{x}- \mathbf{x}_{\rm goal} \right|\right|_{2} \leq r_{\rm goal} \right\rbrace.
\end{align*}$$

`RotationToWorldFrame`: Given two poses as the focal points of a hyperellipsoid, $\mathbf{x}_{\rm from},\,\mathbf{x}_{\rm to}\in X$, the function $\mathtt{RotationToWorldFrame}\left(\mathbf{x}_{\rm from}, \mathbf{x}_{\rm to}\right)$ returns the rotation matrix, $\mathbf{C} \in SO\left( n \right)$, from the hyperellipsoid-aligned frame to the world frame as per [\[eqn:svd\]](#eqn:svd){reference-type="eqref" reference="eqn:svd"}. As previously discussed, in most planning problems this rotation matrix only needs to be calculated at the beginning of the problem.

`SampleUnitNBall`: The function, $\mathtt{SampleUnitNBall}$ returns a uniform sample from the volume of an $n$-ball of unit radius centred at the origin, i.e. $\mathbf{x}_{\rm ball}\sim \mathcal{U}\left(X_{\rm ball}\right)$.

::: algorithm
$c_{\rm min}\gets \left|\left| \mathbf{x}_{\rm goal}- \mathbf{x}_{\rm start} \right|\right|_{2}$ []{#algo:sample:start label="algo:sample:start"} $\mathbf{x}_{\rm centre}\gets \left(\mathbf{x}_{\rm start}+ \mathbf{x}_{\rm goal}\right)/2$ $\mathbf{C} \gets \mathtt{RotationToWorldFrame\left(\mathbf{x}_{\rm start}, \mathbf{x}_{\rm goal}\right)}$ []{#algo:sample:end label="algo:sample:end"} $r_{1} \gets c_{\rm max}/2$ $\left\lbrace r_i\right\rbrace_{i = 2,\ldots,n} \gets \left(\sqrt{c_{\rm max}^2 - c_{\rm min}^2}\right)/2$ $\mathbf{L} \gets \mathop{\mathrm{diag}}\left\lbrace r_1, r_2, \ldots, r_n\right\rbrace$ $\mathbf{x}_{\rm ball}\gets \mathtt{SampleUnitNBall}$ $\mathbf{x}_{\rm rand}\gets \left( \mathbf{C}\mathbf{L}\mathbf{x}_{\rm ball}+ \mathbf{x}_{\rm centre}\right) \cap X$ $\mathbf{x}_{\rm rand}\sim \mathcal{U}\left(X\right)$ ;
:::

## Calculating the Rewiring Radius {#sec:algorithm:rewire}

At each iteration, the rewiring radius, $r_{\mathrm{RRT}^*}$, must be large enough to guarantee almost-sure asymptotic convergence while being small enough to only generate a tractable number of rewiring candidates. Karaman and Frazzoli [@karaman_ijrr11] present a lower-bound for this rewiring radius in terms of the measure of the problem space and the number of vertices in the graph. Their expression assumes a uniform distribution of samples of a unit square. As Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} uniformly samples the *subset* of the planning problem that can improve the solution, a rewiring radius can be calculated from the measure of this informed subset and the related vertices inside it. This updated radius reduces the amount of rewiring necessary and further improves the performance of Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}. Ongoing work is focused on finding the exact form of this expression, but the radius provided by [@karaman_ijrr11] appears appropriate. There also exists a $k$-nearest neighbour version of this expression.

1.5ex plus 1ex minus 0ex 0.7ex plus 0.5ex minus 0ex []{.smallcaps}Simulations[]{#sec:sim label="sec:sim"} Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} was compared to [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} on a variety of simple planning problems (Figs. [5](#fig:probDefn){reference-type="ref" reference="fig:probDefn"} to [7](#fig:gapExample){reference-type="ref" reference="fig:gapExample"}) and randomly generated worlds (e.g., Figs. [1](#fig:randomWorld2){reference-type="ref" reference="fig:randomWorld2"}, [2](#fig:randomWorld){reference-type="ref" reference="fig:randomWorld"}). Simple problems were used to test specific challenges, while the random worlds were used to provide more challenging problems in a variety of state dimensions.

Fig. [5](#fig:probDefn){reference-type="ref" reference="fig:probDefn"}(a) was used to examine the effects of the problem range and the ability to find paths within a specified tolerance of the true optimum, with the width of the obstacle, $w$, selected randomly. Fig. [5](#fig:probDefn){reference-type="ref" reference="fig:probDefn"}(b) was used to demonstrate Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"}'s ability to find topologically distinct solutions, with the position of the narrow passage, $y_g$, selected randomly. For these toy problems, experiments were ended when the planner found a solution cost within the target tolerance of the optimum. Random worlds, as in Fig. [2](#fig:randomWorld){reference-type="ref" reference="fig:randomWorld"}, were used to test Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} on more complicated problems and in higher state dimensions by giving the algorithms $60$ seconds to improve their initial solutions. For each variation of every experiment, $100$ different runs of both [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} and Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} were performed with a common pseudo-random seed and map.

The algorithms share the same unoptimized code, allowing for the comparison of relative computational time. While further optimization would reduce the effect of graph size on the computational cost and reduce the difference between the two planners, as they have approximately the same cost per iteration it will not effect the order. To minimize the effects of the steer parameter on our results, we set it equal to the [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} rewiring radius at each iteration calculated from $\gamma_{\rm RRT} = 1.1\gamma_{\rm RRT}^*$, a choice we found improved the performance of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}. As discussed in Section [0.3](#sec:algorithm:rewire){reference-type="ref" reference="sec:algorithm:rewire"}, for Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} we calculated the rewiring radius for the subproblem defined by the current solution using the expression in [@karaman_ijrr11].

:::: {#fig:probDefn .figure latex-placement="tb"}
![](Gammell2014Informed_figs/probDefn.png)

::: caption
The two planning problems used in Section [\[sec:sim\]](#sec:sim){reference-type="ref" reference="sec:sim"}. The width of the obstacle, $w$, and the location of the gap, $y_g$, were selected randomly for each experimental run.
:::
::::

Experiments varying the width of the problem range, $l$, while keeping a fixed distance between the start and goal show that Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} finds a suitable solution in approximately the same time regardless of the relative size of the problem (Fig. [8](#fig:mapStudy){reference-type="ref" reference="fig:mapStudy"}). As a result of considering only the informed subset once an initial solution is found, the size of the search space is independent of the planning range (Fig. [6](#fig:convergeExample){reference-type="ref" reference="fig:convergeExample"}). In contrast, the time needed by [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} to find a similar solution increases as the problem range grows as proportionately more time is spent searching states that cannot improve the solution (Fig. [8](#fig:mapStudy){reference-type="ref" reference="fig:mapStudy"}).

Experiments varying the target solution cost show that Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} is capable of finding near-optimal solutions in significantly fewer iterations than [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} (Fig. [9](#fig:convergenceStudy){reference-type="ref" reference="fig:convergenceStudy"}). The direct sampling of the informed subset increases density around the optimal solution faster than global sampling and therefore increases the probability of improving the solution and further focusing the search. In contrast, [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} has uniform density across the entire planning domain and improving the solution actually *decreases* the probability of finding further improvements (Fig. [6](#fig:convergeExample){reference-type="ref" reference="fig:convergeExample"}).

Experiments varying the height of $h_g$ in Fig. [5](#fig:probDefn){reference-type="ref" reference="fig:probDefn"}(b) demonstrate that Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} finds difficult passages that improve the current solution, regardless of their homotopy class, quicker than [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} (Fig. [10](#fig:gapStudy){reference-type="ref" reference="fig:gapStudy"}). Once again, the result of considering only the informed subset is an increased state density in the region of the planning problem that includes the optimal solution. Compared to global sampling, this increases the probability of sampling within difficult passages, such as narrow gaps between obstacles, decreasing the time necessary to find such solutions (Fig. [7](#fig:gapExample){reference-type="ref" reference="fig:gapExample"}).

Finally, experiments on random worlds demonstrate that the improvements of Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} apply to a wide range of planning problems and state dimensions (Fig. [11](#fig:dimensionStudy){reference-type="ref" reference="fig:dimensionStudy"}).

:::: {#fig:convergeExample .figure latex-placement="t"}
![](Gammell2014Informed_figs/convergeExample.png){width="\\columnwidth"}

::: caption
An example of Fig. [5](#fig:probDefn){reference-type="ref" reference="fig:probDefn"}(a) after $5$ seconds for a problem with an optimal solution cost of $112.01$. Note that the presence of an obstacle provides a lower bound on the size of the ellipsoidal subset but that Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} still searches a significantly reduced domain than [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"}, increasing both the convergence rate and quality of final solution.
:::
::::

:::: {#fig:gapExample .figure latex-placement="t"}
![](Gammell2014Informed_figs/gapExample.png){width="\\columnwidth"}

::: caption
An example of Fig. [5](#fig:probDefn){reference-type="ref" reference="fig:probDefn"}(b) for a $3\%$ off-centre gap. By focusing the search space on the subset of states that may improve an initial solution flanking the obstacle, Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} is able to find a path through the narrow opening in $4.00$ seconds while [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} requires $12.32$ seconds.
:::
::::

:::: {#fig:mapStudy .figure latex-placement="t"}
![](Gammell2014Informed_figs/mapStudy.png){width="\\columnwidth"}

::: caption
The median computational time needed by [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} and Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} to find a path within 2% of the optimal cost in $\mathbb{R}^2$ for various map widths, $l$, for the problem in Fig. [5](#fig:probDefn){reference-type="ref" reference="fig:probDefn"}(a). Error bars denote a nonparametric $95\%$ confidence interval for the median number of iterations calculated from $100$ independent runs.
:::
::::

:::: {#fig:convergenceStudy .figure latex-placement="t"}
![](Gammell2014Informed_figs/convergenceStudy.png){width="\\columnwidth"}

::: caption
The median computational time needed by [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} and Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} to find a path within the specified tolerance of the optimal cost, $c^{*}$, in $\mathbb{R}^2$ for the problem in Fig. [5](#fig:probDefn){reference-type="ref" reference="fig:probDefn"}(a). Error bars denote a nonparametric $95\%$ confidence interval for the median number of iterations calculated from $100$ independent runs.
:::
::::

:::: {#fig:gapStudy .figure latex-placement="t"}
![](Gammell2014Informed_figs/gapStudy.png){width="\\columnwidth"}

::: caption
The median computational time needed by [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} and Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} to find a path cheaper than flanking the obstacle for various gap ratios, $h_g/h$ for the problem defined in Fig. [5](#fig:probDefn){reference-type="ref" reference="fig:probDefn"}(b). Error bars denote a nonparametric $95\%$ confidence interval for the median number of iterations calculated from $100$ independent runs.
:::
::::

:::: {#fig:dimensionStudy .figure latex-placement="t"}
![](Gammell2014Informed_figs/dimensionStudy.png){width="\\columnwidth"}

::: caption
The median performance of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} and Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} $60$ seconds after finding an initial solution for random worlds (e.g., Figs. [1](#fig:randomWorld2){reference-type="ref" reference="fig:randomWorld2"}, [2](#fig:randomWorld){reference-type="ref" reference="fig:randomWorld"}) in $\mathbb{R}^n$. Plotted as the relative difference in cost, $(c_{\rm best}^{\mbox{\tiny RRT*}} - c_{\rm best}^{\mbox{\tiny Informed RRT*}})/(c_{\rm best}^{\mbox{\tiny RRT*}})$. Error bars denote a nonparametric $95\%$ confidence interval for the median number of iterations calculated from $100$ independent runs.
:::
::::

1.5ex plus 1ex minus 0ex 0.7ex plus 0.5ex minus 0ex []{.smallcaps}Discussion & Conclusion[]{#sec:end label="sec:end"} In this paper, we discuss that a necessary condition for [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} algorithms to improve a solution is the addition of a state from a subset of the planning problem, $X_{f}\subseteq X$. For problems seeking to minimize path length in $\mathbb{R}^n$, this subset can be estimated, $X_{\widehat{f}}\supseteq X_{f}$, by a prolate hyperspheroid (a special type of hyperellipsoid) with the initial and goal states as focal points. It is shown that the probability of adding a new state from this subset through rejection sampling of a larger set becomes arbitrarily small as the dimension of the problem increases, the size of the sampled set increases, or the solution approaches the theoretical minimum. A simple method to sample $X_{\widehat{f}}$ directly is presented that allows for the creation of informed-sampling planners, such as Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"}. It is shown that Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} outperforms [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} in the ability to find near-optimal solutions in finite time regardless of state dimension without requiring any assumptions about the optimal homotopy class.

Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} uses heuristics to shrink the planning problem to subsets of the original domain. This makes it inherently dependent on the current solution cost, as it cannot focus the search when the associated prolate hyperspheroid is larger than the planning problem itself. Similarly, it can only shrink the subset down to the lower bound defined by the optimal solution. We are currently investigating techniques to focus the search without requiring an initial solution. These techniques, such as [BITstar]{acronym-label="BITstar" acronym-form="singular+short"} [@gammell_arxiv14c], incrementally *increase* the search subset. By doing so, they prioritize the initial search of low-cost solutions.

An [OMPL]{acronym-label="OMPL" acronym-form="singular+short"} implementation of Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} is described at [<http://asrl.utias.utoronto.ca/code>](http://asrl.utias.utoronto.ca/code).

1.5ex plus 1ex minus 0ex 0.7ex plus 0.5ex minus 0ex []{.smallcaps}\*Acknowledgment This research was funded by contributions from the [NSERC]{acronym-label="NSERC" acronym-form="singular+short"} through the [NCFRN]{acronym-label="NCFRN" acronym-form="singular+short"}, the Ontario Ministry of Research and Innovation's Early Researcher Award Program, and the [ONR]{acronym-label="ONR" acronym-form="singular+short"} Young Investigator Program.

:::: thebibliography
10

::: spacing
0.9 url@rmstyle

P. E. Hart, N. J. Nilsson, and B. Raphael, "A formal basis for the heuristic determination of minimum cost paths," *TSSC*, 4(2): 100--107, Jul. 1968

S. M. LaValle and J. J. Kuffner Jr., "Randomized kinodynamic planning," *IJRR*, 20(5): 378--400, 2001.

L. E. Kavraki, P. Švestka, J.-C. Latombe, and M. H. Overmars, "Probabilistic roadmaps for path planning in high-dimensional configuration spaces," *TRA*, 12(4): 566--580, 1996.

D. Hsu, R. Kindel, J.-C. Latombe, and S. Rock, "Randomized kinodynamic motion planning with moving obstacles," *IJRR*, 21(3): 233--255, 2002.

C. Urmson and R. Simmons, "Approaches for heuristically biasing RRT growth," *IROS*, 2: 1178--1183, 2003.

D. Ferguson and A. Stentz, "Anytime RRTs," *IROS*, 5369--5375, 2006.

S. Karaman and E. Frazzoli, "Sampling-based algorithms for optimal motion planning," *IJRR*, 30(7): 846--894, 2011.

M. Otte and N. Correll, "C-FOREST: Parallel shortest path planning with superlinear speedup," *TRO*, 29(3): 798--806, Jun. 2013

Y. Gabriely and E. Rimon, "CBUG: A quadratically competitive mobile robot navigation algorithm," *TRO*, 24(6): 1451--1457, Dec. 2008.

N. Gasilov, M. Dogan, and V. Arici, "Two-stage shortest path algorithm for solving optimal obstacle avoidance problem," *IETE Jour. of Research*, 57(3): 278--285, May 2011.

S. Kiesel, E. Burns, and W. Ruml, "Abstraction-guided sampling for motion planning," *SoCS*, 2012.

R. Alterovitz, S. Patil, and A. Derbakova, "Rapidly-exploring roadmaps: Weighing exploration vs. refinement in optimal motion planning," *ICRA*, 3706--3712, 2011.

B. Akgun and M. Stilman, "Sampling heuristics for optimal motion planning in high dimensions," *IROS*, 2640--2645, 2011.

J. Nasir, F. Islam, U. Malik, Y. Ayaz, O. Hasan, M. Khan, and M. S. Muhammad, "RRT\*-SMART: A rapid convergence implementation of RRT\*," *Int. Jour. of Adv. Robotic Systems*, 10, 2013.

D. Kim, J. Lee, and S. Yoon, "Cloud RRT\*: Sampling cloud based RRT\*," *ICRA*, 2014.

S. Karaman, M. R. Walter, A. Perez, E. Frazzoli, and S. Teller, "Anytime motion planning using the RRT\*," *ICRA*, 1478--1483, 2011.

M. Jordan and A. Perez, "Optimal bidirectional rapidly-exploring random trees," CSAIL, MIT, MIT-CSAIL-TR-2013-021, 2013.

O. Arslan and P. Tsiotras, "Use of relaxation methods in sampling-based algorithms for optimal motion planning," *ICRA*, 2013.

S. Koenig, M. Likhachev, and D. Furcy, "Lifelong planning A\*," *Artificial Intelligence*, 155(1--2): 93--146, 2004.

J. D. Gammell, S. S. Srinivasa, and T. D. Barfoot, "On recursive random prolate hyperspheroids," Autonomous Space Robotics Lab, University of Toronto, TR-2014-JDG002, 2014. [arXiv:1403.7664 \[math.ST\]](http://arxiv.org/abs/1403.7664)

H. Sun and M. Farooq, "Note on the generation of random points uniformly distributed in hyper-ellipsoids," in *Fifth Int. Conf. on Information Fusion*, 1: 489--496, 2002.

J. D. Gammell, and T. D. Barfoot, "The probability density function of a transformation-based hyperellipsoid sampling technique," Autonomous Space Robotics Lab, University of Toronto, TR-2014-JDG004, 2014. [arXiv:1404.1347 \[math.ST\]](http://arxiv.org/abs/1404.1347)

G. Wahba, "A least squares estimate of satellite attitude," *SIAM Review*, 7: 409, 1965.

A. H. J. de Ruiter and J. R. Forbes, "On the solution of Wahba's problem on SO(n)," *Jour. of the Astronautical Sciences*, 2014, to appear.

J. D. Gammell, S. S. Srinivasa, and T. D. Barfoot, "BIT\*: Batch informed trees for optimal sampling-based planning via dynamic programming on implicit random geometric graphs," Autonomous Space Robotics Lab, University of Toronto, TR-2014-JDG006, 2014. [arXiv:1405.5848 \[cs.RO\]](http://arxiv.org/abs/1405.5848)
:::
::::
:::::::::::

[^1]: $^1$ J. D. Gammell and T. D. Barfoot are with the Autonomous Space Robotics Lab at the University of Toronto Institute for Aerospace Studies, Toronto, Ontario, Canada. Email: `{jon.gammell, tim.barfoot}@utoronto.ca`

[^2]: $^2$ S. S. Srinivasa is with The Robotics Institute, Carnegie Mellon University, Pittsburgh, Pennsylvania, USA. Email: `siddh@cs.cmu.edu`
