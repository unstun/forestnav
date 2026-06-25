---
citation_key: Strub2021AIT
arxiv_id: 2111.01877
arxiv_url: https://arxiv.org/abs/2111.01877
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:40:44Z
origin: ai+web
reviewed: false
---

# Introduction {#sec:introduction}

:::::: {#fig:evaluated-edges .figure latex-placement="t"}
::: center
Path length
:::

:::: {#fig:example-rrtstar-path-length .figure}
::: caption
RRT\*
:::
::::

:::: {#fig:example-fmtstar-path-length .figure}
::: caption
FMT\*
:::
::::

:::: {#fig:example-bitstar-path-length .figure}
::: caption
BIT\*
:::
::::

:::: {#fig:example-aitstar-path-length .figure}
::: caption
AIT\*
:::
::::

:::: {#fig:example-eitstar-path-length .figure}
::: caption
EIT\*
:::
::::

::: center
Obstacle clearance
:::

:::: {#fig:example-rrtstar-obstacle-clearance .figure}
::: caption
RRT\*
:::
::::

:::: {#fig:example-fmtstar-obstacle-clearance .figure}
::: caption
FMT\*
:::
::::

:::: {#fig:example-bitstar-obstacle-clearance .figure}
::: caption
BIT\*
:::
::::

:::: {#fig:example-aitstar-obstacle-clearance .figure}
::: caption
AIT\*
:::
::::

:::: {#fig:example-eitstar-obstacle-clearance .figure}
::: caption
EIT\*
:::
::::

::: caption
An illustration of the search trees constructed by [RRT\*]{acronym-label="RRT*" acronym-form="singular+abbrv"}, [FMT\*]{acronym-label="FMT*" acronym-form="singular+abbrv"}, [BIT\*]{acronym-label="BIT*" acronym-form="singular+abbrv"}, [AIT\*]{acronym-label="AIT*" acronym-form="singular+abbrv"}, and [EIT\*]{acronym-label="EIT*" acronym-form="singular+abbrv"} to find an initial solution when optimizing path length (--) and obstacle clearance (--). The start and goal are represented by a black dot (  ) and circle (  ), respectively. Sampled states are represented by small black dots (  ). State space obstacles are indicated with gray rectangles (  ). The initial solutions are shown in yellow (  ) and the search trees constructed to find them are shown in black (  ). Any edge in these search trees that is not part of the initial solution delayed finding it. [RRT\*]{acronym-label="RRT*" acronym-form="singular+abbrv"} randomly explores the state space and fully evaluates many edges that are not part of the initial solution for both objectives (, ). [FMT\*]{acronym-label="FMT*" acronym-form="singular+abbrv"} orders its search with increasing cost-to-come of the vertices and not only fully evaluates many edges that are not part of the initial solution for both objectives but also fails to find a solution when optimizing obstacle clearance because its connection strategy depends on edge cost (, ). [BIT\*]{acronym-label="BIT*" acronym-form="singular+abbrv"} orders its search on the total potential solution cost according to an admissible cost heuristic and evaluates fewer edges that are not part of the initial solution () but only if an informative admissible cost heuristic is available (). [AIT\*]{acronym-label="AIT*" acronym-form="singular+abbrv"} calculates and exploits a problem-specific heuristic and evaluates still fewer edges that are not part of the initial solution () but only when an informative admissible cost heuristic can be calculated for the optimization objective (). [EIT\*]{acronym-label="EIT*" acronym-form="singular+abbrv"} calculates and exploits cost and effort heuristics and evaluates few edges even when an admissible cost heuristic cannot be calculated for the objective (, ).
:::
::::::

Path planning algorithms aim to find a sequence of valid states, called a path, that connects a start to a goal. Sampling-based planners, such as AC@PRM [PRM]{acronym-label="PRM" acronym-form="singular+abbrv"} [@kavraki_tro1996] [PRM]{acronym-label="PRM" acronym-form="singular+long"} [[PRM]{acronym-label="PRM" acronym-form="singular+abbrv"}; @kavraki_tro1996] , find paths by randomly sampling valid states and connecting nearby states when these local connections are valid. The resulting structure can be viewed as a graph embedded in a state space, where each vertex represents a valid state and each edge a sequence of valid states connecting two vertices. Multiple planning problems can be solved by adding starts and goals to this embedded graph and then finding a path between them with a graph-search algorithm.

A single planning problem is often solved more efficiently with incremental sampling-based planners, such as AC@RRT [RRT]{acronym-label="RRT" acronym-form="singular+abbrv"} [@lavalle_icra1999; @lavalle_ijrr2001a] [RRT]{acronym-label="RRT" acronym-form="singular+long"} [[RRT]{acronym-label="RRT" acronym-form="singular+abbrv"}; @lavalle_icra1999; @lavalle_ijrr2001a] and its asymptotically optimal variant, [RRT\*]{acronym-label="RRT*" acronym-form="singular+abbrv"} [@karaman_rss2010; @karaman_ijrr2011]. These planners build a search tree of valid paths rooted at the start by incrementally sampling and connecting states when these local connections are valid. This avoids having to specify the sampling resolution *a priori*, but results in a randomly ordered search that spends computational effort on paths that are never part of a solution.

Best-first graph-search algorithms, such as Dijkstra's algorithm [@dijkstra_nm1959], can search problems more efficiently by ordering their search on *partial* solution cost. Informed graph-search algorithms, such as A\* [@hart_tssc1968], can further increase search efficiency by leveraging problem-specific information to order their search on *total* potential solution cost. This information is often expressed as a heuristic function that estimates the cost to connect any two vertices in a graph. A heuristic is called *admissible* if it never overestimates the true cost and *consistent* if it satisfies a specific triangle inequality. Given an admissible cost heuristic, A\* finds an optimal solution, and given a consistent cost heuristic, A\* does so optimally efficiently with respect to the number of expanded vertices [@hart_tssc1968].

The efficient search order of A\* is combined with the incremental sampling of [RRT\*]{acronym-label="RRT*" acronym-form="singular+short"} in informed sampling-based planners, such as AC@BIT\* [BIT\*]{acronym-label="BIT*" acronym-form="singular+abbrv"} [@gammell_icra2015; @gammell_ijrr2020] [BIT\*]{acronym-label="BIT*" acronym-form="singular+long"} [[BIT\*]{acronym-label="BIT*" acronym-form="singular+abbrv"}; @gammell_icra2015; @gammell_ijrr2020] . This improves planning performance, but only when effective cost heuristics are available. A heuristic is most effective when it is both accurate and computationally inexpensive to evaluate relative to other search operations. Such heuristics may not exist for some problems, because they are inaccurate for a given obstacle configuration or computationally expensive due to complex optimization objectives, or may not be admissible, which is often required for theoretical performance guarantees of informed planners.

Problem-specific information not expressible as admissible cost heuristics can be exploited by more advanced informed graph-search algorithms, such as AC@AEES [AEES]{acronym-label="AEES" acronym-form="singular+abbrv"} [@thayer_socs2012] [AEES]{acronym-label="AEES" acronym-form="singular+long"} [[AEES]{acronym-label="AEES" acronym-form="singular+abbrv"}; @thayer_socs2012] and AC@A-MHA\* [A-MHA\*]{acronym-label="A-MHA*" acronym-form="singular+abbrv"} [@natarajan_socs2019] [A-MHA\*]{acronym-label="A-MHA*" acronym-form="singular+long"} [[A-MHA\*]{acronym-label="A-MHA*" acronym-form="singular+abbrv"}; @natarajan_socs2019] . These algorithms decouple search order from solution quality guarantees, which allows them to balance search efficiency with anytime performance. This is especially important for robotic systems that operate under hard time constraints.

This paper presents techniques to inexpensively calculate accurate, admissible, and problem-specific heuristics and exploit them with sampling-based planning algorithms. This is achieved with an asymmetric bidirectional search that considers different information in the forward and reverse searches. These two searches continuously inform each other by sharing complementary information in both directions. Algorithm [\[alg:conceptual\]](#alg:conceptual){reference-type="ref" reference="alg:conceptual"} provides a conceptual overview of this approach.

The reverse search calculates heuristics for the current sampling-based approximation of a planning problem. It exploits problem-specific information implicit in the observed distribution of valid states by combining *a priori* heuristics between multiple states into more accurate heuristics between each state and the goal. The reverse search is computationally inexpensive because it only combines edge heuristics and avoids full collision detection and true edge cost evaluation.

The forward search finds valid paths in the current sampling-based approximation of a planning problem. It does this effectively by exploiting the accurate, problem-specific heuristics calculated by the reverse search. The forward search informs the reverse search when invalid edges were used to calculate the heuristic, causing the reverse search to update the heuristic. The forward search is computationally expensive because it performs full collision detection and edge cost evaluation, but focused on connections likely to yield a solution by the calculated heuristics (Figure [11](#fig:evaluated-edges){reference-type="ref" reference="fig:evaluated-edges"}).

This paper presents two almost-surely asymptotically optimal sampling-based planning algorithms informed by an asymmetric bidirectional search, [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"}. [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} calculates an increasingly accurate, admissible cost heuristic with its reverse search and exploits this heuristic with its forward search. This results in fast initial solution times even when the admissible cost heuristic available *a priori* is not accurate. The full details of [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} are presented in .

[EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} builds on [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} by calculating an additional cost and effort heuristic with its reverse search and exploiting all three heuristics with its forward search. This results in fast initial solution times even when no admissible cost heuristic is available. The full details of [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} are presented in .

The benefits of simultaneously calculating and exploiting adaptive heuristics are demonstrated on twelve problems in abstract, robotic, and biomedical domains in . All domains are tested with the path-length objective, where informative admissible heuristics are available *a priori*, and the obstacle-clearance objective, where informative admissible heuristics are not always available *a priori*. The results show that [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} outperforms all other asymptotically optimal planners on all problems in all domains when optimizing obstacle clearance. [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} also perform well when minimizing path length in comparison to the tested planners when considering success rates, median initial solution times, and median solution quality over time.

## Statement of Contributions {#sec:statement-of-contributions}

This paper expands on ideas first published as @strub_icra2020b. It makes the following specific contributions:

- Presents [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} as an extension of [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} to optimization objectives that are computationally expensive or difficult to approximate with an admissible *a priori* cost heuristic .

- Proves the almost-sure asymptotic optimality of these algorithms by building on results from the path-planning and graph-search literature .

- Demonstrates the effectiveness of these algorithms accross multiple domains and optimization objectives, including problems of robotic manipulation and problems with continuous goal regions .

# Background {#sec:background}

This section first formally defines the optimal path planning problem and then reviews related techniques from the literature on using heuristics in sampling-based planners and graph-search algorithms .

## Problem Definition {#sec:problem-definition}

There are two widely studied versions of the path planning problem. The *feasible* path planning problem is the task of finding a sequence of valid states, i.e., a path, that leads from a start to a goal. Many feasible problems have many solutions. The *optimal* path planning problem is the task of finding the best among these solutions, i.e., a valid path that is optimal with respect to a given optimization objective. Many optimal problems have a unique solution. The optimal path planning problem is formally defined in Definition [1](#def:optimal-planning){reference-type="ref" reference="def:optimal-planning"}.

::: {#def:optimal-planning .definition}
**Definition 1** (The Optimal Path Planning Problem [@karaman_ijrr2011]). *Let the state space of a planning problem be denoted by $X$, the subset of invalid states by $X_{\mathrm{invalid}} \subset X$, and the subset of valid states by $X_{\mathrm{valid}} \coloneqq \mathop{\mathrm{closure}} \left( X \setminus
    X_{\mathrm{invalid}} \right)$. Let the start state and the set of goal states be denoted by $\bm{\mathrm{x}}_{\mathrm{start}} \in X_{\mathrm{valid}}$ and $X_{\mathrm{goal}} \subset X_{\mathrm{valid}}$, respectively. Let $\sigma \colon [0, 1] \to X_{\mathrm{valid}}$ be a continuous function with bounded total variation, i.e., a valid path, and let the set of all valid paths be denoted by $\Sigma$. Let the optimization objective be defined by a cost function, $c \colon \Sigma \to [0, \infty)$, that maps each path to a nonnegative real number.*

*The optimal path planning problem is the task of finding a path, $\sigma^{*} \in \Sigma$, from the start to the goal with minimum cost, $$\begin{equation*}
    \sigma^{*} \coloneqq \mathop{\arg\min}_{\sigma \in \Sigma} \set*{ c(\sigma) \sigma(0) = \bm{\mathrm{x}}_{\mathrm{start}}, \sigma(1) \in X_{\mathrm{goal}}},
\end{equation*}$$ or reporting failure if no such path exists.*
:::

::: algorithm
` `
:::

Sampling-based planners are often evaluated probabilistically as a function of the number of samples over all possible realizations of a distribution. Algorithms whose probability of solving the feasible path planning problem approaches one as the number of samples approaches infinity are called *probabilistically complete*. Algorithms that asymptotically solve the optimal planning problem as the number of samples approaches infinity with a probability of one are called *almost-surely asymptotically optimal* [@karaman_ijrr2011]. Almost-sure asymptotic optimality implies probabilistic completeness and is formally defined in Definition [1](#def:asymptotic-optimality){reference-type="ref" reference="def:asymptotic-optimality"}.

::: {#def:asymptotic-optimality .definition}
**Definition 1** (Almost-sure asymptotic optimality [@karaman_ijrr2011]). *A sampling-based path planning algorithm is called *almost-surely asymptotically optimal* if it has a unity probability of asymptotically solving the optimal path planning problem as the number of samples approaches infinity (if an optimal solution exists), $$\begin{equation*}
    P\left( \adjustlimits{\mathop{\lim\,\sup}}_{{q \to \infty}}{\;\min}_{\;\sigma \in
        \Sigma_{q}} \{ c(\sigma) \} = c^{*} \right) = 1,
\end{equation*}$$ where $q$ is the number of samples, $\Sigma_{q} \subset \Sigma$ is the set of valid paths from the start to the goal found by the planner from those samples, $c \colon \Sigma \to [0, \infty)$ is the cost function, and $c^{*}$ is the optimal solution cost.*
:::

Sampling-based planners can also use deterministic sampling strategies [e.g., @branicky_icra2001; @lavalle_ijrr2004], which can result in deterministic optimality guarantees [@janson_ijrr2018]. The finite-time properties of asymptotically optimal planners are analyzed by @dobson_iros2013, @janson_ijrr2018, and @tsao_icra2020.

Formally analyzing sampling-based planners requires assumptions about the path planning problem [e.g., @gammell_arcras2021]. The analysis of [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} builds on the probabilistic results of @karaman_ijrr2011 and makes the same assumptions (Sections [2.1.1](#sec:state-space-assumptions){reference-type="ref" reference="sec:state-space-assumptions"}--[2.1.4](#sec:solution-assumptions){reference-type="ref" reference="sec:solution-assumptions"}).

### State Space Assumption {#sec:state-space-assumptions}

The state space of the planning problem is assumed to be an open, $n$-dimensional unit (hyper)cube, $X \coloneqq (0, 1)^{n}$, but problems with other state spaces can also be searched [@kleinbort_wafr2016; @kleinbort_afr2020].

### Cost Function Assumptions {#sec:cost-function-assumptions}

Let $\sigma_{1}, \sigma_{2} \in \Sigma$ be two paths such that $\sigma_{1}(1) = \sigma_{2}(0)$, and let $(\sigma_{1} | \sigma_{2}) \in \Sigma$ denote their concatenation, $$\begin{equation*}
  (\sigma_{1} | \sigma_{2})(t) \coloneqq
  \begin{cases}
    \sigma_{1}(2t) & \text{for } t \in \lbrack 0, \nicefrac{1}{2}
    \rbrack \\
    \sigma_{2}(2t - 1) & \text{for } t \in \lparen\nicefrac{1}{2}, 1\rbrack.
  \end{cases}
\end{equation*}$$ The cost of any path, $\sigma = ( \sigma_{1} | \sigma_{2} ) \in \Sigma$, is assumed to be lower bounded by the cost of any of its segments, $$\begin{equation*}
  \forall\; \sigma_{1}, \sigma_{2} \text{ s.t. } \sigma = (
  \sigma_{1} | \sigma_{2} ), \quad c(\sigma) \geq \max\{
c(\sigma_{1}), c(\sigma_{2}) \},
\end{equation*}$$ and upper bounded by a multiple of its total variation, $$\begin{equation*}
  \exists k \in [0, \infty), \quad c(\sigma) \leq k \mathop{\mathrm{TV}}(\sigma),
\end{equation*}$$ where $\mathrm{TV}(\sigma)$ denotes the total variation of the path $\sigma$ [@karaman_ijrr2011].

It is also assumed that only trivial paths consisting of a single state can have zero cost, $$\begin{equation*}
  c(\sigma) = 0 \iff \forall\; t \in [0, 1], \sigma(t) = \sigma(0).
\end{equation*}$$

### Obstacle Assumption {#sec:obstacle-assumptions}

The obstacle configuration of the optimal path planning problem is assumed to allow for a valid path from the start to the goal that remains a fixed distance, $\delta > 0$, from its nearest obstacles for its entire length, $$\begin{equation*}
  \exists\; \sigma \in \Sigma, \delta \in (0, \infty), \; \text{s.t. } \forall\; t \in [0,
  1], B_{\delta, n}(\sigma(t)) \subset X_{\mathrm{valid}},
\end{equation*}$$ where $B_{\delta, n}(\sigma(t))$ is an $n$-dimensional ball with radius $\delta$ centered at $\sigma(t)$, $$\begin{equation*}
  B_{\delta, n}(\bm{\mathrm{x}}) \coloneqq \left\{ \bm{\mathrm{x}}^{\prime} \in X
    \;\big|\; {\| \bm{\mathrm{x}} - \bm{\mathrm{x}}^{\prime} \|}_{2} \leq \delta \right\}.
\end{equation*}$$ Such a path is said to have *strong $\delta$-clearance*.

### Optimal Solution Assumption {#sec:solution-assumptions}

At least one solution of the optimal path planning problem, $\sigma^{*} \in \Sigma$, is assumed to be homotopic to a path, $\sigma_{\delta} \in \Sigma$, with strong $\delta$-clearance, $$\begin{equation*}
  \exists\; H \colon [0, 1] \to \Sigma, \quad H(0) = \sigma^{*}, H(1) = \sigma_{\delta},
\end{equation*}$$ where $H$ is a homotopic map whose image is the set of all valid paths from the start to the goal. Such a solution is said to have *weak $\delta$-clearance*.

## Literature Review {#sec:literature-review}

Almost-surely asymptotically optimal planning is a popular area of research [@gammell_arcras2021]. This section focuses on sampling-based and graph-search techniques to calculate and/or exploit heuristics to improve performance. Sampling-based planners that use heuristics to guide the sampling and/or order the search are reviewed in . Approaches that calculate and exploit accurate cost heuristics for graph-search algorithms are reviewed in and algorithms that use effort heuristics in . Using heuristics in sampling-based planning has parallels with lazy collision detection, which is reviewed in .

### Heuristics in Sampling-Based Planning {#sec:sampling-based-planning-with-heuristics}

Sampling-based planning algorithms can improve their performance by using heuristics to bias their sampling and guide their search.

[RRT]{acronym-label="RRT" acronym-form="singular+short"}-Connect [@kuffner_icra2000] builds on [RRT]{acronym-label="RRT" acronym-form="singular+short"} by growing two trees, one rooted in the start and one in the goal state. These trees each explore the state space around them, but are also guided towards each other with a *connect heuristic*. This approach can result in very fast initial solution times, but does not consider the solution cost and can consequently not improve the solution given more computational time. Almost-surely asymptotically optimal variants of [RRT]{acronym-label="RRT" acronym-form="singular+short"}-Connect exist [@akgun_iros2011; @jordan_tr2013; @klemm_robio2015; @qureshi_ras2015; @burget_iros2016] but the connect heuristic does not guide the search beyond finding an initial solution.

AC@hRRT [hRRT]{acronym-label="hRRT" acronym-form="singular+abbrv"} [@urmson_iros2003] [hRRT]{acronym-label="hRRT" acronym-form="singular+long"} [[hRRT]{acronym-label="hRRT" acronym-form="singular+abbrv"}; @urmson_iros2003] and AC@GBRRT [GBRRT]{acronym-label="GBRRT" acronym-form="singular+abbrv"} [@nayak_arxiv2021] [GBRRT]{acronym-label="GBRRT" acronym-form="singular+long"} [[GBRRT]{acronym-label="GBRRT" acronym-form="singular+abbrv"}; @nayak_arxiv2021] bias the growth of their trees with cost heuristics. [hRRT]{acronym-label="hRRT" acronym-form="singular+short"} uses *a priori* heuristics to weigh the Voronoi regions of [RRT]{acronym-label="RRT" acronym-form="singular+short"}. [GBRRT]{acronym-label="GBRRT" acronym-form="singular+short"} is a bidirectional version of [RRT]{acronym-label="RRT" acronym-form="singular+short"} that guides the forward tree with heuristics computed by the reverse tree. These algorithms have improved performance but do not provide any bounds on the quality of their solution.

Informed [RRT\*]{acronym-label="RRT*" acronym-form="singular+abbrv"} [@gammell_iros2014; @gammell_tro2018] builds on [RRT\*]{acronym-label="RRT*" acronym-form="singular+abbrv"} by using an admissible cost heuristic to ensure that only states that can improve the current solution are processed. This improves [RRT\*]{acronym-label="RRT*" acronym-form="singular+abbrv"}'s convergence rate and retains its almost-sure asymptotic optimality, but does not guide the search with the heuristic, does not improve the accuracy of the heuristic as the search progresses, and does not provide any benefits until an initial solution is found. @kunz_icra2016 and @yi_icra2018 extend informed sampling to kinodynamic systems. @joshi_icra2019 present a variant of Informed [RRT\*]{acronym-label="RRT*" acronym-form="singular+abbrv"} that uses previous collision detection results and available information in the graph structure to guide the search.

[RRTsharp]{acronym-label="RRTsharp" acronym-form="singular+abbrv"} [@arslan_icra2013; @arslan_icra2015] builds on [RRT\*]{acronym-label="RRT*" acronym-form="singular+abbrv"} by ensuring that all samples are optimally connected to the search tree after each iteration. It does this efficiently by using an admissible cost heuristic to update the connections of suboptimally connected samples in order of their total potential solution cost. This again improves [RRT\*]{acronym-label="RRT*" acronym-form="singular+abbrv"}'s convergence rate and retains its almost-sure asymptotic optimality, but can also not improve the accuracy of the heuristic as the search progresses and does not provide any benefits until an initial solution is found.

@sakcak_lcss2020 present a method that incorporates a heuristic into a version of RRT\* that is based on motion primitives [@sakcak_ar2019]. This can improve the performance on kinodynamic problems but uses a discretization of the state space that suffers from the *curse of dimensionality* [@bellman_book1957].

AC@IST [IST]{acronym-label="IST" acronym-form="singular+abbrv"} [@bekris_stair2008] [IST]{acronym-label="IST" acronym-form="singular+long"} [[IST]{acronym-label="IST" acronym-form="singular+abbrv"}; @bekris_stair2008] , A\*-RRT [@li_icra2011], the $f$-biasing method [@kiesel_socs2012], P-PRM [@le_iros2014], and AC@RIOT [RIOT]{acronym-label="RIOT" acronym-form="singular+abbrv"} [@westbrook_iros2020] [RIOT]{acronym-label="RIOT" acronym-form="singular+long"} [[RIOT]{acronym-label="RIOT" acronym-form="singular+abbrv"}; @westbrook_iros2020] all search a simplified approximation of the state space to calculate an accurate cost heuristic, which is then used to guide a sampling-based planner. These approaches improve planning performance but require a preprocessing step.

AC@BEAST [BEAST]{acronym-label="BEAST" acronym-form="singular+abbrv"} [@kiesel_iros2017] [BEAST]{acronym-label="BEAST" acronym-form="singular+long"} [[BEAST]{acronym-label="BEAST" acronym-form="singular+abbrv"}; @kiesel_iros2017] is similar to these methods in that it runs [PRM]{acronym-label="PRM" acronym-form="singular+short"} on a simplified abstraction of the problem and uses the resulting graph to calculate an effort heuristic for the samples in the simplified space. If searching the original space reveals that regions in the abstract space cannot easily be connected, then this effort heuristic is updated in a Bayesian manner. BEAST tends to find initial solutions faster than other planners but does not provide any guarantees on the quality of its solutions.

AC@QMP [QMP]{acronym-label="QMP" acronym-form="singular+abbrv"} [@orthey_iros2018] [QMP]{acronym-label="QMP" acronym-form="singular+long"} [[QMP]{acronym-label="QMP" acronym-form="singular+abbrv"}; @orthey_iros2018] ,  AC@QRRT [QRRT]{acronym-label="QRRT" acronym-form="singular+abbrv"} [@orthey_isrr2019] [QRRT]{acronym-label="QRRT" acronym-form="singular+long"} [[QRRT]{acronym-label="QRRT" acronym-form="singular+abbrv"}; @orthey_isrr2019] , and their asymptotically optimal variants [QMP]{acronym-label="QMP" acronym-form="singular+short"}\* and [QRRT]{acronym-label="QRRT" acronym-form="singular+short"}\* [@orthey_arxiv2020b] solve planning problems with sequences of admissible lower-dimensional simplifications of increasing dimensionality. Paths in lower-dimensional simplifications can guide the sampling of states in higher dimensional simplifications and can be seen as admissible heuristics. This can improve performance by orders of magnitude, especially for high-dimensional problems, but requires the user to manually specify the sequence of lower-dimensional simplifications for each problem.

AC@MPLB [MPLB]{acronym-label="MPLB" acronym-form="singular+abbrv"} [@salzman_icra2015b] [MPLB]{acronym-label="MPLB" acronym-form="singular+long"} [[MPLB]{acronym-label="MPLB" acronym-form="singular+abbrv"}; @salzman_icra2015b] is an anytime adaption of [FMT\*]{acronym-label="FMT*" acronym-form="singular+short"} [@janson_isrr2013; @janson_ijrr2015] that incorporates admissible cost heuristics. [MPLB]{acronym-label="MPLB" acronym-form="singular+short"} uses two passes of Dijkstra's algorithm to restrict the set of samples to be searched and another pass of Dijkstra's to calculate an admissible cost heuristic for these samples, all without detecting collisions. It then uses the resulting cost heuristic in a forward search with collision detection to find a path. This approach can result in accurate, admissible cost heuristics and requires few collision detections but does not update the heuristic when the forward search detects collisions on edges that were used to compute the heuristic.

[BIT\*]{acronym-label="BIT*" acronym-form="singular+short"} samples batches of states and views these states as an increasingly dense edge-implicit AC@RGG [RGG]{acronym-label="RGG" acronym-form="singular+abbrv"} [@penrose_book2003] [RGG]{acronym-label="RGG" acronym-form="singular+long"} [[RGG]{acronym-label="RGG" acronym-form="singular+abbrv"}; @penrose_book2003] . It uses an admissible cost heuristic to search this graph in order of potential solution quality with techniques similar to AC@LPA\* [LPA\*]{acronym-label="LPA*" acronym-form="singular+abbrv"} [@koenig_ai2004; @likhachev_icaps2005b; @aine_ai2016] [LPA\*]{acronym-label="LPA*" acronym-form="singular+long"} [[LPA\*]{acronym-label="LPA*" acronym-form="singular+abbrv"}; @koenig_ai2004; @likhachev_icaps2005b; @aine_ai2016] . AC@ABIT\* [ABIT\*]{acronym-label="ABIT*" acronym-form="singular+abbrv"} [@strub_icra2020a] [ABIT\*]{acronym-label="ABIT*" acronym-form="singular+long"} [[ABIT\*]{acronym-label="ABIT*" acronym-form="singular+abbrv"}; @strub_icra2020a] speeds up initial solution times by inflating its heuristic, similar to AC@ARA\* [ARA\*]{acronym-label="ARA*" acronym-form="singular+abbrv"} [@likhachev_nips2004] [ARA\*]{acronym-label="ARA*" acronym-form="singular+long"} [[ARA\*]{acronym-label="ARA*" acronym-form="singular+abbrv"}; @likhachev_nips2004] , and balances exploring the state space with exploiting the current [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation by truncating its search, similar to AC@TLPA\* [TLPA\*]{acronym-label="TLPA*" acronym-form="singular+abbrv"} [@aine_ai2016] [TLPA\*]{acronym-label="TLPA*" acronym-form="singular+long"} [[TLPA\*]{acronym-label="TLPA*" acronym-form="singular+abbrv"}; @aine_ai2016] . Both algorithms work best when the cost of a path correlates well with the computational effort required to validate it and when accurate cost heuristics are available *a priori*, but require that these heuristics are admissible and do not improve their accuracy as the search progresses.

Similar to [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"}, the methods in this section use heuristics to improve the performance of sampling-based planning algorithms. In contrast to [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"}, these methods either do not apply heuristics to all aspects of the search, do not provide any bounds on the quality of their solution, require a preprocessing step, do not calculate problem-specific heuristics, or do not improve the accuracy of the heuristic as the search progresses.

:::: {#fig:benefits-of-adaptive-heuristics .figure}
Path length Obstacle clearance\

:::: {#fig:euclidean-heuristic .figure}
::: caption
Euclidean cost heuristic
:::
::::

:::: {#fig:adaptive-cost-heuristic .figure}
::: caption
Calculated cost heuristic
:::
::::

:::: {#fig:zero-heuristic .figure}
::: caption
Trivial zero-cost heuristic
:::
::::

:::: {#fig:adaptive-effort-heuristic .figure}
::: caption
Calculated effort heuristic
:::
::::

::: caption
An illustration of how [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} leverage the observed distribution of valid states to calculate accurate, problem-specific heuristics. The start and goal are represented by a black dot (  ) and circle (  ), respectively. Sampled states are represented by small black dots (  ). The state space obstacle is indicated with a gray rectangle (  ). Euclidean distance is often used as a cost heuristic when optimizing path length (, ). It suggests the green and red edges are equally promising, even through the red edge leads to a dead end (). Calculating a problem-specific cost heuristic with a reverse search reveals that the green edge is more promising and can lead the forward search around the obstacle without evaluating many unnecessary edges (). Some optimization objectives may not easily allow for informative admissible heuristics, such as obstacle clearance (, ). Most informed search algorithms are ordered by cost-to-come in the absence of an informative heuristic, which again suggests that the green and red edges are equally promising (). Calculating a problem-specific effort heuristic with a reverse search again reveals that the green edge can lead to a solution faster than the red edge, even in the absence of an informative admissible cost heuristic ().
:::
::::

### Improved Heuristics in Graph-Search {#sec:improved-heuristics-for-informed-search}

Developing and exploiting accurate heuristics is an important area of research in informed graph-search algorithms. Techniques to calculate more accurate heuristics have improved performance in various problem domains, e.g., the 15-Puzzle [@culberson_cscsi1996], Rubik's Cube [@korf_ncai1997], and robot vacuum on a grid [@thayer_icaps2011b].

Pattern databases [@culberson_cscsi1996; @korf_ncai1997; @culberson_ci1998] are precomputed tables of exact solution costs to potentially simplified subproblems of a problem domain. The highest solution cost of any remaining subproblem in an ongoing search can be used as an accurate heuristic for an informed search. Additive pattern databases [@felner_jair2004] are constructed such that the heuristic remains admissible when the solution costs of all remaining subproblems are combined, which can result in more accurate heuristics. This increased accuracy can significantly improve performance, but is confined to problem domains for which pattern databases can be generated.

AC@HA\* [HA\*]{acronym-label="HA*" acronym-form="singular+abbrv"} [@holte_ncai1996] [HA\*]{acronym-label="HA*" acronym-form="singular+long"} [[HA\*]{acronym-label="HA*" acronym-form="singular+abbrv"}; @holte_ncai1996] uses homo­morphic transformations of the state space to create abstractions in which multiple states of the original space are mapped to a single state in abstract space. These abstractions are then searched to calculate a heuristic for the original state space. This can result in fewer expanded states, but the presented technique is only shown to work for graphs with uniform edge costs. AC@HCA\* [HCA\*]{acronym-label="HCA*" acronym-form="singular+abbrv"} [@silver_aiide2005] [HCA\*]{acronym-label="HCA*" acronym-form="singular+long"} [[HCA\*]{acronym-label="HCA*" acronym-form="singular+abbrv"}; @silver_aiide2005] and AC@WHCA\* [WHCA\*]{acronym-label="WHCA*" acronym-form="singular+abbrv"} [@silver_aiide2005] [WHCA\*]{acronym-label="WHCA*" acronym-form="singular+long"} [[WHCA\*]{acronym-label="WHCA*" acronym-form="singular+abbrv"}; @silver_aiide2005] are multiagent versions of [HA\*]{acronym-label="HA*" acronym-form="singular+short"} that use AC@RRA\* [RRA\*]{acronym-label="RRA*" acronym-form="singular+abbrv"} [@silver_aiide2005] [RRA\*]{acronym-label="RRA*" acronym-form="singular+long"} [[RRA\*]{acronym-label="RRA*" acronym-form="singular+abbrv"}; @silver_aiide2005] to search the abstraction from the goal to the start. The cost of the optimal paths to states from the goal in the abstract space is used as the heuristic for the corresponding states in the original space. If the search in the original space processes a state whose abstract representation has not been processed by [RRA\*]{acronym-label="RRA*" acronym-form="singular+short"}, then [RRA\*]{acronym-label="RRA*" acronym-form="singular+short"} is resumed until it finds the optimal path to an abstract state that corresponds to the state being processed by the search in the original space. This results in lower cost paths and better success rates than alternative multi-agent search algorithms, but cannot directly be applied to single-agent planning in continuous spaces.

AC@AA\* [AA\*]{acronym-label="AA*" acronym-form="singular+abbrv"} [@koenig_aamas2005; @sun_aamas2008] [AA\*]{acronym-label="AA*" acronym-form="singular+long"} [[AA\*]{acronym-label="AA*" acronym-form="singular+abbrv"}; @koenig_aamas2005; @sun_aamas2008] is an incremental search algorithm that calculates an increasingly accurate, admissible cost heuristic for subsequent searches of a graph with the same goal but different start states. After each search, the heuristic cost-to-go value of each closed state is updated to be the difference between the solution cost and the cost-to-come value of that state. This results in increasingly efficient searches of any problem domain but does not provide any benefits for the initial search of a graph.

The method in @thayer_icaps2011b also generates more accurate heuristics for any domain. It uses a relationship between the cost-to-go of a state and the cost-to-go of its best child to define a *single-step error* in the cost heuristic. The mean single-step error in this heuristic is then calculated either globally or per branch and used to adjust the heuristic accordingly. This approach can be used in the initial search but is not guaranteed to produce admissible heuristics.

The *Add method* [@kaindl_jair1997] uses a bidirectional search in which a partial reverse search generates heuristics that inform the forward search. The reverse search reveals errors in the heuristic values of the processed states, the minimum of which is added to the heuristic values of all unexpanded states in the forward search. This results in a more informed heuristic that remains admissible, but increases the heuristic value for all unexpanded states uniformly and requires a user-defined parameter that specifies how many states to expand in the reverse search. A version without this parameter is presented by @wilt_cai2013.

Similar to [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"}, the methods in this section generate increasingly accurate heuristics that result in increasingly efficient searches. In contrast to [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"}, these methods either require preprocessing, cannot be used for the initial search of a graph, result in inadmissible heuristics, or increase the heuristic value for all unexpanded states uniformly and only order by estimated solution cost.

### Effort Heuristics in Graph-Search {#sec:effort-and-distance-based-heuristics-in-informed-search}

Ordering the search based on (inflated) cost heuristics improves anytime performance the most when the cost of a path correlates well with the computational effort required to find it [@wilt_socs2012]. Directly ordering the search on the com­putational effort of a path can instead improve performance even when this is not the case. The graph-search literature often uses the number of states that must be expanded to find a solution as a proxy for the total search effort.

AC@DWA\* [DWA\*]{acronym-label="DWA*" acronym-form="singular+abbrv"} [@pohl_ijcai1973] [DWA\*]{acronym-label="DWA*" acronym-form="singular+long"} [[DWA\*]{acronym-label="DWA*" acronym-form="singular+abbrv"}; @pohl_ijcai1973] aims to improve performance by ordering its search in a manner that rewards progress away from the start. It multiplies an admissible cost heuristic by a weighting factor that decreases with increasing depth in the search tree. This is shown to reduce the number of expanded states on some problem domains, but requires an *a priori* estimate of the solution depth and implicitly assumes that every step away from the start is a step closer to the goal. Revised DWA\* [@thayer_icaps2009] removes this assumption, but still requires an *a priori* estimate of the solution depth.

A$_{\varepsilon}^{*}$ [@pearl_pami1982] aims to expand states that are as close to the goal as possible and could be part of a solution whose cost is within a user-specified factor of the optimal cost. It always expands the node with the least number of states left to be expanded, provided it could be part of a solution within the suboptimality bound according to an admissible cost heuristic. This works well if loose suboptimality bounds are acceptable or a very accurate cost heuristic is available, but otherwise forces the search to expand states with a large estimate of states left to be expanded just to increase the lower bound on the optimal solution cost.

AC@EES [EES]{acronym-label="EES" acronym-form="singular+abbrv"} [@thayer_icaps2011a] [EES]{acronym-label="EES" acronym-form="singular+long"} [[EES]{acronym-label="EES" acronym-form="singular+abbrv"}; @thayer_icaps2011a] aims to always expand the node which most quickly leads to a solution whose cost is within a user-specified bound of the optimal cost. It uses an admissible cost heuristic to guarantee the bound on the suboptimality and inadmissible cost and effort heuristics to guide its search. This significantly improves search performance in domains where solution cost and depth can differ, but introduces computational overhead and algorithmic complexity because [EES]{acronym-label="EES" acronym-form="singular+short"} must maintain three queues ordered on three different quantities. [AEES]{acronym-label="AEES" acronym-form="singular+short"} is an anytime version of EES and provides the foundation of the forward search of [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"}, which is discussed in .

Similar to [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"}, the methods in this section use estimates of the computational effort required to discover a solution to guide the search and improve performance. In contrast to [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"}, these methods do not increase the accuracy of their heuristics as the search progresses.

### Lazy Collision Detection {#sec:sampling-based-planning-with-lazy-collision-detection}

A byproduct of using heuristics in sampling-based planning to bias the sampling and guide the search is often that fewer edges have to be fully evaluated . This relates informed path planning algorithms to algorithms with lazy collision detection that explicitly aim to minimize the number of collision detections.

Lazy [PRM]{acronym-label="PRM" acronym-form="singular+short"} [@bohlin_icra2000] and Fuzzy [PRM]{acronym-label="PRM" acronym-form="singular+short"} [@nielsen_iros2000] take similar approaches to minimizing computational effort through lazy collision detection. Both algorithms initially connect samples without performing any collision detection on the edges. The resulting graph is processed with an informed graph-search algorithm to find a path that connects the start and goal states, and only checked for collision once a path is found. If collisions are detected, then the corresponding vertices and edges are removed from the graph and the updated graph is processed again to find a new path between the start and goal states. This results in few fully evaluated edges and improved planning performance, but Lazy [PRM]{acronym-label="PRM" acronym-form="singular+short"} and Fuzzy [PRM]{acronym-label="PRM" acronym-form="singular+short"} do not provide any guarantee on the quality of its solution and do not improve the accuracy of the heuristic used in their graph-search algorithm. Almost-surely asymptotically optimal variants of similar approaches exist [@hauser_icra2015; @kim_icra2018] but these algorithms also do not improve the accuracy of their heuristics as the search progresses.

The [SBL]{acronym-label="SBL" acronym-form="singular+short"} planner [@sanchez_rr2003] combines lazy collision detection with ideas from RRT-Connect. It grows two trees, similar to RRT-Connect, but only checks collisions on edges that it believes to be on a path connecting the start and goal states, like Lazy [PRM]{acronym-label="PRM" acronym-form="singular+short"} and Fuzzy [PRM]{acronym-label="PRM" acronym-form="singular+short"}. [SBL]{acronym-label="SBL" acronym-form="singular+short"} achieves fast solution times, but does also not provide any guarantees on the quality of its solution and does not improve its solution given more computational time.

AC@LBT-RRT [LBT-RRT]{acronym-label="LBT-RRT" acronym-form="singular+abbrv"} [@salzman_icra2014; @salzman_tro2016] [LBT-RRT]{acronym-label="LBT-RRT" acronym-form="singular+long"} [[LBT-RRT]{acronym-label="LBT-RRT" acronym-form="singular+abbrv"}; @salzman_icra2014; @salzman_tro2016] extends [RRT\*]{acronym-label="RRT*" acronym-form="singular+abbrv"} with a graph whose edges are not fully evaluated and uses this graph to determine which edges to evaluate next. [LBT-RRT]{acronym-label="LBT-RRT" acronym-form="singular+short"} is almost-surely asymptotically near-optimal and allows for continuous interpolation between [RRT]{acronym-label="RRT" acronym-form="singular+short"} and AC@RRG [RRG]{acronym-label="RRG" acronym-form="singular+abbrv"} [@karaman_ijrr2011] [RRG]{acronym-label="RRG" acronym-form="singular+long"} [[RRG]{acronym-label="RRG" acronym-form="singular+abbrv"}; @karaman_ijrr2011] by only rewiring states that are $\varepsilon$-inconsistent. A similar approach is used for replanning in dynamic environments in [RRTX]{acronym-label="RRTX" acronym-form="singular+abbrv"} [@otte_afr2015; @otte_ijrr2016]. Interpolating [LBT-RRT]{acronym-label="LBT-RRT" acronym-form="singular+short"} between [RRT]{acronym-label="RRT" acronym-form="singular+short"} and [RRG]{acronym-label="RRG" acronym-form="singular+short"} allows for balancing exploration with exploitation, but [LBT-RRT]{acronym-label="LBT-RRT" acronym-form="singular+short"} can only optimize path length.

The [LazySP]{acronym-label="LazySP" acronym-form="singular+short"} Framework [@dellin_icaps2016] explicitly aims to minimize the number of edges that are checked for collision. It first finds a path from the start to the goal using a heuristic for the edge cost and then uses an *edge selector* to determine the order in which the edges on the potential solution path are checked for collision. This often results in few fully evaluated edges, but is not asymptotically optimal and restarts the search every time an edge is found to be invalid. AC@GLS [GLS]{acronym-label="GLS" acronym-form="singular+abbrv"} [@mandalika_icaps2019] [GLS]{acronym-label="GLS" acronym-form="singular+long"} [[GLS]{acronym-label="GLS" acronym-form="singular+abbrv"}; @mandalika_icaps2019] builds on [LazySP]{acronym-label="LazySP" acronym-form="singular+short"} by presenting a framework that can algorithmically balance edge evaluation with continuing the search, but is also not asymptotically optimal. AC@LRHA\* [LRHA\*]{acronym-label="LRHA*" acronym-form="singular+abbrv"} [@mandalika_icaps2018] [LRHA\*]{acronym-label="LRHA*" acronym-form="singular+long"} [[LRHA\*]{acronym-label="LRHA*" acronym-form="singular+abbrv"}; @mandalika_icaps2018] is an example algorithm that fits within the [LazySP]{acronym-label="LazySP" acronym-form="singular+short"} and [GLS]{acronym-label="GLS" acronym-form="singular+short"} frameworks.

Similar to [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"}, the methods in this section improve performance by reducing the number of full edge evaluations. In contrast to [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"}, these methods either do not use heuristics, do not improve the accuracy of their heuristics, do not guarantee any bounds on the quality of their solution, do not improve their solution given more computation time, or can only optimize path length.

# [AIT\*]{acronym-label="AIT*" acronym-form="singular+abbrv"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+abbrv"} {#sec:algorithms}

::: table*
+-----------------------------+--------------------------------------------------------------------------+--------------------------------------------------------------------------+-----------------------------------------------------------------------+
| Component                   | [BIT\*]{acronym-label="BIT*" acronym-form="singular+short"}              | [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"}              | [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"}           |
+:===============+:===========+:=========================================================================+:=========================================================================+:======================================================================+
| Approximation               | Series of [RGG]{acronym-label="RGG" acronym-form="singular+short"}s      | Series of [RGG]{acronym-label="RGG" acronym-form="singular+short"}s      | Series of [RGG]{acronym-label="RGG" acronym-form="singular+short"}s   |
+----------------+------------+--------------------------------------------------------------------------+--------------------------------------------------------------------------+-----------------------------------------------------------------------+
| ::: sideways   | Purpose    | ---                                                                      | Calculate admissible cost heuristic                                      | Calculate in-/admissible cost & effort heuristics                     |
| Reverse search |            |                                                                          |                                                                          |                                                                       |
| :::            |            |                                                                          |                                                                          |                                                                       |
|                +------------+--------------------------------------------------------------------------+--------------------------------------------------------------------------+-----------------------------------------------------------------------+
|                | Algorithm  | ---                                                                      | Vertex-queue [LPA\*]{acronym-label="LPA*" acronym-form="singular+short"} | Edge-queue A\*                                                        |
|                +------------+--------------------------------------------------------------------------+--------------------------------------------------------------------------+-----------------------------------------------------------------------+
|                | Ordering   | ---                                                                      | *A priori* admissible solution cost                                      | *A priori* admissible solution cost & effort                          |
|                +------------+--------------------------------------------------------------------------+--------------------------------------------------------------------------+-----------------------------------------------------------------------+
|                | Validation | ---                                                                      | None                                                                     | Adaptive sparse collision detection                                   |
+----------------+------------+--------------------------------------------------------------------------+--------------------------------------------------------------------------+-----------------------------------------------------------------------+
| ::: sideways   | Purpose    | Find valid paths                                                         | Find valid paths                                                         | Find valid paths                                                      |
| Forward search |            |                                                                          |                                                                          |                                                                       |
| :::            |            |                                                                          |                                                                          |                                                                       |
|                +------------+--------------------------------------------------------------------------+--------------------------------------------------------------------------+-----------------------------------------------------------------------+
|                | Algorithm  | Edge-queue [TLPA\*]{acronym-label="TLPA*" acronym-form="singular+short"} | Edge-queue A\*                                                           | Edge-queue [AEES]{acronym-label="AEES" acronym-form="singular+short"} |
|                +------------+--------------------------------------------------------------------------+--------------------------------------------------------------------------+-----------------------------------------------------------------------+
|                | Ordering   | *A priori* admissible solution cost                                      | Calculated admissible solution cost                                      | Calculated in-/admissible solution cost & effort                      |
|                +------------+--------------------------------------------------------------------------+--------------------------------------------------------------------------+-----------------------------------------------------------------------+
|                | Validation | Dense collision detection                                                | Dense collision detection                                                | Dense collision detection                                             |
+----------------+------------+--------------------------------------------------------------------------+--------------------------------------------------------------------------+-----------------------------------------------------------------------+
:::

[AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} are almost-surely asymptotically optimal path planning algorithms that build on [BIT\*]{acronym-label="BIT*" acronym-form="singular+short"}. [BIT\*]{acronym-label="BIT*" acronym-form="singular+short"} approximates the state space with a batch of samples, which it views as an edge-implicit [RGG]{acronym-label="RGG" acronym-form="singular+short"}. [BIT\*]{acronym-label="BIT*" acronym-form="singular+short"} searches this [RGG]{acronym-label="RGG" acronym-form="singular+short"} in order of the total potential solution quality of its edges until it can guarantee that it has found the *resolution-optimal* solution, i.e., the optimal solution in the current approximation of the state space. Once the search is finished, [BIT\*]{acronym-label="BIT*" acronym-form="singular+short"} improves its [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation by adding a new batch of samples. In this way, [BIT\*]{acronym-label="BIT*" acronym-form="singular+short"} approximates and searches a continuously valued state space by building and searching a series of increasingly dense, edge-implicit [RGGs]{acronym-label="RGG" acronym-form="plural+short"}.

To find solutions, [BIT\*]{acronym-label="BIT*" acronym-form="singular+short"} processes the implicit edges of its current [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation in order of their total potential solution cost, using incremental search techniques similar to an edge-queue version of [TLPA\*]{acronym-label="TLPA*" acronym-form="singular+short"}. It estimates the total potential solution cost of an edge as the sum of the current cost to come to the source of the edge, a heuristic estimate of the edge cost, and a heuristic estimate of the cost to go from the target of the edge. The formal guarantees of [BIT\*]{acronym-label="BIT*" acronym-form="singular+short"} require that these cost heuristics are admissible.

[AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} extend [BIT\*]{acronym-label="BIT*" acronym-form="singular+short"} with an asymmetric bi­directional search that unifies many of the benefits reviewed in by leveraging information implicit in the observed distribution of valid states . The reverse searches of [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} calculate accurate heuristics which are exploited by their forward searches. The forward searches in turn inform the reverse searches if they used invalid edges to compute the heuristic. In this way, both searches continuously inform each other with complementary information.

The reverse searches of [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} evaluate edges approximately and are therefore computationally inexpensive. The forward searches of [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} evaluate edges fully and are therefore computationally expensive, but focused by the calculated problem-specific heuristics. This computational asymmetry avoids the inefficiency of naive symmetric bidirectional informed search, where frontiers of expensive searches pass each other [Section 10.2, @pohl_phd1969].

An overview of the search algorithms used in [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} is provided in . The rest of this section presents the notation used in this paper , the algorithmic details of [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} (Sections [3.2](#sec:adaptively-informed-trees){reference-type="ref" reference="sec:adaptively-informed-trees"} and [3.3](#sec:effort-informed-trees){reference-type="ref" reference="sec:effort-informed-trees"}), and the formal analysis of their asymptotic optimality .

## Notation {#sec:notation}

The state space is denoted by $X \subseteq \mathbb{R}^{n}, n \in \mathbb{N}$, the invalid states by $X_{\mathrm{invalid}} \subset X$, and the valid states by $X_{\mathrm{valid}} \coloneqq \mathop{\mathrm{closure}}\left( X \setminus
  X_{\mathrm{invalid}} \right)$. A single state is denoted by $\bm{\mathrm{x}} \in X$. The start and goal are denoted by $\bm{\mathrm{x}}_{\mathrm{start}} \in X_{\mathrm{valid}}$ and $X_{\mathrm{goal}} \subset X_{\mathrm{valid}}$, respectively. The set of sampled states underlying the [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation is denoted by $X_{\mathrm{sampled}} \subset X_{\mathrm{valid}}$.

The forward and reverse search trees are denoted by $\mathcal{F} = (V_{\mathcal{F}}, E_{\mathcal{F}})$ and $\mathcal{R} = (V_{\mathcal{R}}, E_{\mathcal{R}})$, respectively. All vertices in these trees, $V_{\mathcal{F}}$ and $V_{\mathcal{R}}$, are individually associated with a sampled state and are embedded in the valid region of the state space, $X_{\mathrm{valid}}$. Up to two vertices can be associated with a sample (one per search tree), but not every sample must be associated with a vertex in a tree. All edges in both trees, $E_{\mathcal{F}} \subset V_{\mathcal{F}} \times V_{\mathcal{F}}$ and $E_{\mathcal{R}} \subset V_{\mathcal{R}} \times V_{\mathcal{R}}$, are directed, defined by a source state, $\bm{\mathrm{x}}_{\mathrm{s}}$, and a target state, $\bm{\mathrm{x}}_{\mathrm{t}}$, and denoted by an ordered pair, $( \bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}} )$. The edges in the forward tree, $E_{\mathcal{F}}$, are embedded in the valid region of the state space and represent valid connections between sampled states. The edges in the reverse tree, $E_{\mathcal{R}}$, are not necessarily embedded in the valid region of the state space and may lead through invalid states.

The true connection cost between two states is denoted by the function $c \colon X \times X \to [0, \infty)$ and admissible estimates of this cost are denoted by the function $\hat{c} \colon X \times X \to [0, \infty)$, i.e., $\forall \bm{\mathrm{x}}_{i}, \bm{\mathrm{x}}_{j} \in X, \hat{c}\left(
  \bm{\mathrm{x}}_{i}, \bm{\mathrm{x}}_{j} \right) \leq c\left(
  \bm{\mathrm{x}}_{i}, \bm{\mathrm{x}}_{j} \right)$. Admissible cost heuristics to come to a specific state from the start are denoted by the function $\hat{g} \colon X \to [0, \infty)$ and often defined as $\hat{g}\left( \bm{\mathrm{x}} \right) \coloneqq \hat{c}\left(
  \bm{\mathrm{x}}_{\mathrm{start}}, \bm{\mathrm{x}} \right)$. Admissible cost heuristics to go from a specific state to a goal are denoted by the function $\hat{h} \colon X \to [0, \infty)$ and often defined as $\hat{h}\left( \bm{\mathrm{x}} \right) \coloneqq
\min_{\bm{\mathrm{x}}_{\mathrm{goal}} \in X_{\mathrm{goal}}} \left\{
  \hat{c}\left( \bm{\mathrm{x}}, \bm{\mathrm{x}}_{\mathrm{goal}} \right)
\right\}$.

The cost to come to a specific state from the start through the forward tree is denoted by the function $g_{\mathcal{F}} \colon X \to [0, \infty)$. It is well-defined for states that have an associated vertex in the forward tree and taken as infinity for states that do not.

Admissible estimates of the cost of a path from the start to a goal constrained to go through a specific state is denoted by the function $\hat{f} \colon X \to [0, \infty)$ and often defined as $\hat{f}(\bm{\mathrm{x}}) \coloneqq \hat{g}(\bm{\mathrm{x}}) +
\hat{h}(\bm{\mathrm{x}})$. This function defines the informed set, i.e., the set of states that can improve the current solution, $X_{\hat{f}} \coloneqq \{ \bm{\mathrm{x}} \in X \,|\,
\hat{f}(\bm{\mathrm{x}}) < c_{\mathrm{current}} \}$, where $c_{\mathrm{current}}$ is the cost of the current solution [@gammell_tro2018].

Square brackets denote a label, e.g., $l[\bm{\mathrm{x}}] \in \mathbb{R}$ refers to a real number, $l$, associated with the state $\bm{\mathrm{x}}$. Labels keep their values until they are updated, i.e., they are used in [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} similar to how $g$-values are used in A\*.

The compounding operations, $A \leftarrow A \cup B$ and $A \leftarrow A \setminus B$, are respectively denoted by $A \xleftarrow{\scriptscriptstyle +} B$ and $A \xleftarrow{\scriptscriptstyle -} B$, where $A$ and $B$ are subsets of a common set.

### [EIT\*]{acronym-label="EIT*" acronym-form="singular+abbrv"}-specific Notation {#sec:eit-notation}

Potentially inadmissible effort heuristics between two states are denoted by $\bar{e}\colon X \times X \to [0, \infty)$. These heuristics estimate the computational effort required to find and validate a path between two states, e.g., the number of necessary collision detections on the path. Potentially inadmissible effort heuristics between each state and the start are denoted by the function $\bar{d}\colon X \to [0, \infty)$ and often defined as $\bar{d}\left( \bm{\mathrm{x}} \right) \coloneqq
\bar{e}\left( \bm{\mathrm{x}}, \bm{\mathrm{x}}_{\mathrm{start}} \right)$. Potentially inadmissible cost heuristics between two states are denoted by the function $\bar{c}\colon X \times X \to [0, \infty)$. It is assumed that this estimate is never lower than its admissible counterpart, i.e., $\forall\; \bm{\mathrm{x}}_{1}, \bm{\mathrm{x}}_{2} \in X, \hat{c}\left(
  \bm{\mathrm{x}}_{1}, \bm{\mathrm{x}}_{2} \right) \leq \bar{c}\left(
  \bm{\mathrm{x}}_{1}, \bm{\mathrm{x}}_{2} \right)$.

## [AIT\*]{acronym-label="AIT*" acronym-form="singular+full"} {#sec:adaptively-informed-trees}

[AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} improves on [BIT\*]{acronym-label="BIT*" acronym-form="singular+short"} by using the same increasingly dense [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation but searching it with an asymmetric bidirectional search which calculates and exploits a more accurate cost heuristic that is specific to each [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation . This results in a more efficient search with fewer evaluated edges when an admissible cost heuristic is available *a priori* (Figures [3](#fig:example-bitstar-path-length){reference-type="ref" reference="fig:example-bitstar-path-length"}, , Extension 1), and can improve initial solution times and convergence rates.

[AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} consists of three high-level steps:

::: enumerate*
improving the [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation (sampling; )

updating the heuristic (reverse search; )

finding valid paths in the current [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation (forward search; ),
:::

as shown by Algorithm [\[alg:conceptual\]](#alg:conceptual){reference-type="ref" reference="alg:conceptual"}. The full technical details of [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} are given in Algorithms [\[alg:aitstar:technical\]](#alg:aitstar:technical){reference-type="ref" reference="alg:aitstar:technical"}--[\[alg:aitstar:prune\]](#alg:aitstar:prune){reference-type="ref" reference="alg:aitstar:prune"}.

The reverse search of [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} is a version of [LPA\*]{acronym-label="LPA*" acronym-form="singular+short"} that calculates accurate cost heuristics by combining an admissible cost heuristic between multiple states into a more accurate cost heuristic between each state and the goal. The calculated cost heuristic is admissible for the current [RGG]{acronym-label="RGG" acronym-form="singular+short"} and leverages information implicit in the observed distribution of valid states. This reverse search is computationally inexpensive because it does not perform collision detection on the edges.

If the reverse search finishes without reaching the start, then the start and goal are not in the same connected component of the current [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation. [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} skips the forward search in this case and directly improves the [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation. This ensures that [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} does not spend computational effort searching a graph that it knows cannot contain a solution.

The forward search of [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} is an edge-queue version of A\* which efficiently exploits the calculated heuristic and evaluates few edges that do not contribute to a solution when admissible cost heuristic are available *a priori*. If the forward search detects a collision on an edge in the reverse search tree, then [LPA\*]{acronym-label="LPA*" acronym-form="singular+short"} updates the heuristic by efficiently repairing this tree. The forward search then continues with the updated heuristic until the optimal solution on the current [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation is found or another collision is detected on an edge in the reverse search tree. This process is repeated as time allows to almost-surely asymptotically converge towards the optimal solution in an anytime manner .

:::: {#fig:aitstar-step-by-step .figure}
:::: {#fig:aitstar-step-1 .figure}
::: caption
:::
::::

:::: {#fig:aitstar-step-2 .figure}
::: caption
:::
::::

:::: {#fig:aitstar-step-3 .figure}
::: caption
:::
::::

:::: {#fig:aitstar-step-4 .figure}
::: caption
:::
::::

:::: {#fig:aitstar-step-5 .figure}
::: caption
:::
::::

::: caption
Five snapshots of AIT\*'s search when minimizing path length. The start and goal states are represented by a black dot (  ) and circle (  ), respectively. Sampled states are represented by small black dots (  ). State space obstacles are indicated with gray obstacles (  ). The forward search tree is shown with black lines (  ) and the reverse search tree with gray lines (  ). The current best solution is highlighted in yellow (  ). AIT\* starts by initializing the [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation and calculating an approximation-specific admissible cost heuristic with a reverse search without collision detection (). AIT\* exploits the calculated heuristic with its forward search and repairs the reverse search tree whenever the forward search reveals that it contains an invalid edge (). When the forward search finds the resolution-optimal solution, the [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation is improved by sampling and pruning and the heuristic is updated on this improved approximation (). This updated heuristic is again exploited with the next forward search and repaired when found to use invalid edges (). [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} repeats these steps until stopped and almost-surely asymptotically converges towards the optimal solution ().
:::
::::

### Approximation {#sec:ait-approximation}

[AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} incrementally approximates the state space by sampling batches of $m$ valid states (Alg. [\[alg:aitstar:technical\]](#alg:aitstar:technical){reference-type="ref" reference="alg:aitstar:technical"}, line [\[alg:aitstar:improve-approximation:sample\]](#alg:aitstar:improve-approximation:sample){reference-type="ref" reference="alg:aitstar:improve-approximation:sample"}). States are sampled uniformly in the informed set, using informed sampling [@gammell_tro2018] when possible. These samples are viewed as a series of increasingly dense, edge-implicit [RGG]{acronym-label="RGG" acronym-form="singular+short"}s where bidirectional edges are defined either by a connection radius, $r$, or by the *mutual* $k$-nearest neighbors [Alg. [\[alg:aitstar:neighbors\]](#alg:aitstar:neighbors){reference-type="ref" reference="alg:aitstar:neighbors"}, line [\[alg:aitstar:neighbors:nearest\]](#alg:aitstar:neighbors:nearest){reference-type="ref" reference="alg:aitstar:neighbors:nearest"}; mutual $k$-nearest as in @janson_ijrr2015]. The connection parameters, $r$ and $k$, scale as in [PRM\*]{acronym-label="PRM*" acronym-form="singular+abbrv"} [@karaman_ijrr2011], using the measure of the informed set as in @gammell_ijrr2020, $$\begin{align*}
  r(q) &\coloneqq 2 \eta {\left( 1 + \frac{1}{n} \right)}^{\frac{1}{n}} {\left(
         \frac{\min\left\{ \lambda\left( X \right), \lambda\left( X_{\hat{f}}
         \right) \right\}}{\lambda\left( B_{1, n} \right)} \right)}^{\frac{1}{n}} \\ &\qquad\quad{\left( \frac{\log\left( q \right)}{q} \right)}^{\frac{1}{n}} \\
  k(q) &\coloneqq \eta \, \mathrm{e} \left( 1 + \frac{1}{n} \right) \log\left( q \right),
\end{align*}$$ where $q$ is the number of sampled states in the informed set, $\eta > 1$ is a tuning parameter, $\lambda(\cdot)$ denotes the Lebesgue measure, and $B_{1, n}$ is the $n$-dimensional unit ball.

The $r$-disc strategy can result in better performance than the $k$-nearest version but the computation of the $r$-disc radius must be adjusted to the properties of the state space [@kleinbort_wafr2016; @kleinbort_afr2020]. Faster-decreasing radii are presented in @janson_ijrr2015 [@janson_ijrr2018], @solovey_ijrr2020, and @tsao_icra2020, but are not used in [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} for direct comparison to existing algorithms as they are presented in the literature.

[AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} considers the combination of both this [RGG]{acronym-label="RGG" acronym-form="singular+short"} definition and any existing connections in the forward search tree and ignores edges known to be invalid (Alg. [\[alg:aitstar:neighbors\]](#alg:aitstar:neighbors){reference-type="ref" reference="alg:aitstar:neighbors"}, lines [\[alg:aitstar:neighbors:forward-children\]](#alg:aitstar:neighbors:forward-children){reference-type="ref" reference="alg:aitstar:neighbors:forward-children"} and [\[alg:aitstar:neighbors:invalid\]](#alg:aitstar:neighbors:invalid){reference-type="ref" reference="alg:aitstar:neighbors:invalid"}). [RGG]{acronym-label="RGG" acronym-form="singular+short"} complexity is reduced by pruning samples that are not in the informed set (Alg. [\[alg:aitstar:technical\]](#alg:aitstar:technical){reference-type="ref" reference="alg:aitstar:technical"}, line [\[alg:aitstar:improve-approximation:prune\]](#alg:aitstar:improve-approximation:prune){reference-type="ref" reference="alg:aitstar:improve-approximation:prune"} and Alg. [\[alg:aitstar:prune\]](#alg:aitstar:prune){reference-type="ref" reference="alg:aitstar:prune"}).

### Reverse Search {#sec:ait-reverse-search}

[AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} calculates an accurate cost heuristic between each processed state and the goal that is admissible for the current [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation. It does this by calculating the *a priori* admissible cost heuristic, $\hat{c}\left( \,\cdot\,,\,\cdot\, \right)$, over the connectivity of this approximation.

This is achieved by processing the [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation with a version of [LPA\*]{acronym-label="LPA*" acronym-form="singular+short"} that is rooted at the goal and uses the admissible *a priori* cost heuristics, $\hat{c}\left( \,\cdot\,,\,\cdot\, \right)$, as edge costs without detecting collisions on the edges. The resulting reverse search tree can be updated efficiently because [LPA\*]{acronym-label="LPA*" acronym-form="singular+short"} stores the cost of a state when it was first connected or last rewired and when it was last expanded, denoted by $\hat{h}_{\mathrm{con}}[\bm{\mathrm{x}}]$ and $\hat{h}_{\mathrm{exp}}[\bm{\mathrm{x}}]$, respectively. These are the $g$ and $v$ values in a forward [LPA\*]{acronym-label="LPA*" acronym-form="singular+short"} search [@aine_ai2016].

The queue of the reverse [LPA\*]{acronym-label="LPA*" acronym-form="singular+short"} search in [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} is denoted by $\mathcal{Q}_{\mathcal{R}}$ and lexicographically ordered according to $$\begin{align*}
  \mathtt{key}_{\mathcal{R}}^{\text{AIT*}}(\bm{\mathrm{x}}) \coloneqq \Big( &\min\left\{ \hat{h}_{\mathrm{con}}[\bm{\mathrm{x}}],  \hat{h}_{\mathrm{exp}}[\bm{\mathrm{x}}] \right\} + \hat{g}(\bm{\mathrm{x}}), \\
  &\min\left\{ \hat{h}_{\mathrm{con}}[\bm{\mathrm{x}}],  \hat{h}_{\mathrm{exp}}[\bm{\mathrm{x}}] \right\}\Big),
\end{align*}$$ where $\hat{g}(\bm{\mathrm{x}})$ denotes an admissible *a priori* cost heuristic between a state, $\bm{\mathrm{x}}$, and the start. This key is used to extract the next edge from the reverse queue (Alg. [\[alg:aitstar:technical\]](#alg:aitstar:technical){reference-type="ref" reference="alg:aitstar:technical"}, lines [\[alg:aitstar:iterate-reverse-search:get-best-vertex\]](#alg:aitstar:iterate-reverse-search:get-best-vertex){reference-type="ref" reference="alg:aitstar:iterate-reverse-search:get-best-vertex"} and [\[alg:aitstar:iterate-reverse-search:pop-best-vertex\]](#alg:aitstar:iterate-reverse-search:pop-best-vertex){reference-type="ref" reference="alg:aitstar:iterate-reverse-search:pop-best-vertex"}).

An uninitialized LPA\* search is used to calculate the heuristic on the first batch of samples and after each new batch is added. This is more efficient than incrementally updating the heuristic with [LPA\*]{acronym-label="LPA*" acronym-form="singular+short"} for the large changes in the graph that result from increasing its resolution [@koenig_ai2004; @likhachev_icaps2005b; @aine_ai2016]. An uninitialized [LPA\*]{acronym-label="LPA*" acronym-form="singular+short"} search is started by clearing the reverse search tree (except for the goals), setting the $\hat{h}_{\mathrm{con}}$ and $\hat{h}_{\mathrm{exp}}$ values of all states to infinity (again, except for the goals), and inserting the goal states into the reverse queue (Alg. [\[alg:aitstar:technical\]](#alg:aitstar:technical){reference-type="ref" reference="alg:aitstar:technical"}, lines [\[alg:aitstar:technical:initialize-reverse\]](#alg:aitstar:technical:initialize-reverse){reference-type="ref" reference="alg:aitstar:technical:initialize-reverse"}, [\[alg:aitstar:technical:reinitialize-reverse-tree-begin\]](#alg:aitstar:technical:reinitialize-reverse-tree-begin){reference-type="ref" reference="alg:aitstar:technical:reinitialize-reverse-tree-begin"}, and [\[alg:aitstar:technical:reinitialize-reverse-tree-end\]](#alg:aitstar:technical:reinitialize-reverse-tree-end){reference-type="ref" reference="alg:aitstar:technical:reinitialize-reverse-tree-end"}).

The heuristic is updated whenever an edge in the reverse search tree is found to be invalid by removing this edge from the [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation and repairing the reverse search tree with [LPA\*]{acronym-label="LPA*" acronym-form="singular+short"}. This is accomplished by updating the cost-to-go of the source state of the invalid edge and then running [LPA\*]{acronym-label="LPA*" acronym-form="singular+short"} to update the cost of all affected states as necessary (Alg. [\[alg:aitstar:technical\]](#alg:aitstar:technical){reference-type="ref" reference="alg:aitstar:technical"}, lines [\[alg:aitstar:iterate-reverse-search:get-best-vertex\]](#alg:aitstar:iterate-reverse-search:get-best-vertex){reference-type="ref" reference="alg:aitstar:iterate-reverse-search:get-best-vertex"}--[\[alg:aitstar:iterate-reverse-search:end\]](#alg:aitstar:iterate-reverse-search:end){reference-type="ref" reference="alg:aitstar:iterate-reverse-search:end"} and [\[alg:aitstar:iterate-forward-search:blacklist\]](#alg:aitstar:iterate-forward-search:blacklist){reference-type="ref" reference="alg:aitstar:iterate-forward-search:blacklist"}--[\[alg:aitstar:iterate-forward-search:invalidate-reverse-branch\]](#alg:aitstar:iterate-forward-search:invalidate-reverse-branch){reference-type="ref" reference="alg:aitstar:iterate-forward-search:invalidate-reverse-branch"} and Alg. [\[alg:aitstar:invalidate-reverse-branch\]](#alg:aitstar:invalidate-reverse-branch){reference-type="ref" reference="alg:aitstar:invalidate-reverse-branch"}).

The reverse search is suspended when the total potential solution cost of the best state in the reverse queue is greater than or equal to that of the best edge in the forward queue and the target of the best edge in the forward queue is consistent (Alg. [\[alg:aitstar:technical\]](#alg:aitstar:technical){reference-type="ref" reference="alg:aitstar:technical"} lines [\[alg:aitstar:technical:continue-reverse-search-1\]](#alg:aitstar:technical:continue-reverse-search-1){reference-type="ref" reference="alg:aitstar:technical:continue-reverse-search-1"} and [\[alg:aitstar:technical:continue-reverse-search-2\]](#alg:aitstar:technical:continue-reverse-search-2){reference-type="ref" reference="alg:aitstar:technical:continue-reverse-search-2"}). This guarantees that no other edge in the forward queue would be better if the reverse search was continued [@strub_phd2021]. The reverse search is also suspended when the reverse or forward queue is empty or when all edges in the forward queue have consistent targets with a reverse-key value less than or equal to the minimum reverse-key in the reverse queue, but these conditions are omitted from Algorithm [\[alg:aitstar:technical\]](#alg:aitstar:technical){reference-type="ref" reference="alg:aitstar:technical"} for clearer structure.

::: algorithm
$\currentcost \leftarrow \infty$ $\sampledstates \leftarrow \goalstates \cup \{ \startstate \}$ $\fwdvertices \leftarrow \startstate$`;` $\fwdedges \leftarrow \emptyset$`;` $\fwdqueue \leftarrow
  \expandedge{\startstate}$[]{#alg:aitstar:technical:initialize-forward label="alg:aitstar:technical:initialize-forward"} $\revvertices \leftarrow \goalstates$`;` $\revedges \leftarrow \emptyset$`;` $\revqueue \leftarrow \goalstates$[]{#alg:aitstar:technical:initialize-reverse label="alg:aitstar:technical:initialize-reverse"} []{#alg:aitstar:technical:repeat-end label="alg:aitstar:technical:repeat-end"}
:::

### Forward Search {#sec:ait-forward-search}

[AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} finds solutions to a planning problem by building a search tree rooted at the start with an edge-queue version of A\* that uses the heuristic calculated by the reverse search. The edge-queue of the forward search is denoted by $\mathcal{Q}_{\mathcal{F}}$ and lexicographically ordered by $$\begin{align*}
  \mathtt{key}_{\mathcal{F}}^{\text{AIT*}}\left( \bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}} \right) \coloneqq \Big(&g_{\mathcal{F}}(\bm{\mathrm{x}}_{\mathrm{s}}) + \hat{c}(\bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}}) + \hat{h}_{\mathrm{con}}[\bm{\mathrm{x}}_{\mathrm{t}}],\\
  &g_{\mathcal{F}}(\bm{\mathrm{x}}_{\mathrm{s}}) + \hat{c}(\bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}}),\; g_{\mathcal{F}}(\bm{\mathrm{x}}_{\mathrm{s}})\Big),
\end{align*}$$ similar to how the edge-queue is ordered in [BIT\*]{acronym-label="BIT*" acronym-form="singular+short"}.

A forward search iteration begins by testing if the forward queue contains an edge that can possibly improve the current solution (Alg. [\[alg:aitstar:technical\]](#alg:aitstar:technical){reference-type="ref" reference="alg:aitstar:technical"}, line [\[alg:aitstar:technical:continue-forward-search\]](#alg:aitstar:technical:continue-forward-search){reference-type="ref" reference="alg:aitstar:technical:continue-forward-search"}). If it does, then the edge with the lowest $\mathtt{key}_{\mathcal{F}}^{\text{AIT*}}$-value is extracted from the forward queue (Alg. [\[alg:aitstar:technical\]](#alg:aitstar:technical){reference-type="ref" reference="alg:aitstar:technical"}, lines [\[alg:aitstar:iterate-forward-search:get-best-edge\]](#alg:aitstar:iterate-forward-search:get-best-edge){reference-type="ref" reference="alg:aitstar:iterate-forward-search:get-best-edge"} and [\[alg:aitstar:iterate-forward-search:pop-best-edge\]](#alg:aitstar:iterate-forward-search:pop-best-edge){reference-type="ref" reference="alg:aitstar:iterate-forward-search:pop-best-edge"}). If this edge is already in the forward tree, then its target is expanded into the forward queue and the iteration is complete (Alg. [\[alg:aitstar:technical\]](#alg:aitstar:technical){reference-type="ref" reference="alg:aitstar:technical"}, lines [\[alg:aitstar:iterate-forward-search:is-edge-in-tree\]](#alg:aitstar:iterate-forward-search:is-edge-in-tree){reference-type="ref" reference="alg:aitstar:iterate-forward-search:is-edge-in-tree"} and [\[alg:aitstar:iterate-forward-search:expand-edge-in-tree\]](#alg:aitstar:iterate-forward-search:expand-edge-in-tree){reference-type="ref" reference="alg:aitstar:iterate-forward-search:expand-edge-in-tree"}).

If the edge is not in the forward tree but can possibly improve it, then it is checked for validity which is computationally expensive (Alg. [\[alg:aitstar:technical\]](#alg:aitstar:technical){reference-type="ref" reference="alg:aitstar:technical"}, lines [\[alg:aitstar:iterate-forward-search:can-edge-possibly-improve-tree\]](#alg:aitstar:iterate-forward-search:can-edge-possibly-improve-tree){reference-type="ref" reference="alg:aitstar:iterate-forward-search:can-edge-possibly-improve-tree"} and [\[alg:aitstar:iterate-forward-search:collision-detection\]](#alg:aitstar:iterate-forward-search:collision-detection){reference-type="ref" reference="alg:aitstar:iterate-forward-search:collision-detection"}). If the edge is invalid, then it is added to the set of invalid edges (Alg. [\[alg:aitstar:technical\]](#alg:aitstar:technical){reference-type="ref" reference="alg:aitstar:technical"}, line [\[alg:aitstar:iterate-forward-search:blacklist\]](#alg:aitstar:iterate-forward-search:blacklist){reference-type="ref" reference="alg:aitstar:iterate-forward-search:blacklist"}) and if it is also part of the reverse tree, then the heuristic is updated with the reverse search (Alg. [\[alg:aitstar:technical\]](#alg:aitstar:technical){reference-type="ref" reference="alg:aitstar:technical"}, lines [\[alg:aitstar:iterate-reverse-search:get-best-vertex\]](#alg:aitstar:iterate-reverse-search:get-best-vertex){reference-type="ref" reference="alg:aitstar:iterate-reverse-search:get-best-vertex"}--[\[alg:aitstar:iterate-reverse-search:end\]](#alg:aitstar:iterate-reverse-search:end){reference-type="ref" reference="alg:aitstar:iterate-reverse-search:end"}, [\[alg:aitstar:iterate-forward-search:reverse-tree-check\]](#alg:aitstar:iterate-forward-search:reverse-tree-check){reference-type="ref" reference="alg:aitstar:iterate-forward-search:reverse-tree-check"}, [\[alg:aitstar:iterate-forward-search:invalidate-reverse-branch\]](#alg:aitstar:iterate-forward-search:invalidate-reverse-branch){reference-type="ref" reference="alg:aitstar:iterate-forward-search:invalidate-reverse-branch"}, and Alg. [\[alg:aitstar:invalidate-reverse-branch\]](#alg:aitstar:invalidate-reverse-branch){reference-type="ref" reference="alg:aitstar:invalidate-reverse-branch"}). If the edge is valid, then its true cost is evaluated which may also be computationally expensive and it is checked whether the edge can actually improve the current solution and forward tree (Alg. [\[alg:aitstar:technical\]](#alg:aitstar:technical){reference-type="ref" reference="alg:aitstar:technical"}, lines [\[alg:aitstar:iterate-forward-search:can-edge-actually-improve-solution\]](#alg:aitstar:iterate-forward-search:can-edge-actually-improve-solution){reference-type="ref" reference="alg:aitstar:iterate-forward-search:can-edge-actually-improve-solution"} and [\[alg:aitstar:iterate-forward-search:can-edge-actually-improve-tree\]](#alg:aitstar:iterate-forward-search:can-edge-actually-improve-tree){reference-type="ref" reference="alg:aitstar:iterate-forward-search:can-edge-actually-improve-tree"}).

If the edge can improve the current solution and forward search tree, then its target is added to this tree if it is not already in it (Alg. [\[alg:aitstar:technical\]](#alg:aitstar:technical){reference-type="ref" reference="alg:aitstar:technical"}, lines [\[alg:aitstar:iterate-forward-search:add-state-to-tree-begin\]](#alg:aitstar:iterate-forward-search:add-state-to-tree-begin){reference-type="ref" reference="alg:aitstar:iterate-forward-search:add-state-to-tree-begin"} and [\[alg:aitstar:iterate-forward-search:add-state-to-tree-end\]](#alg:aitstar:iterate-forward-search:add-state-to-tree-end){reference-type="ref" reference="alg:aitstar:iterate-forward-search:add-state-to-tree-end"}). If it is already in the forward search tree, then the new edge constitutes a rewiring and the old edge is removed from the tree (Alg. [\[alg:aitstar:technical\]](#alg:aitstar:technical){reference-type="ref" reference="alg:aitstar:technical"}, line [\[alg:aitstar:iterate-forward-search:rewiring\]](#alg:aitstar:iterate-forward-search:rewiring){reference-type="ref" reference="alg:aitstar:iterate-forward-search:rewiring"}). The new edge is added to the forward tree and its target is expanded regardless of whether the target was already in the tree or not (Alg. [\[alg:aitstar:technical\]](#alg:aitstar:technical){reference-type="ref" reference="alg:aitstar:technical"}, lines [\[alg:aitstar:iterate-forward-search:add-edge-to-tree\]](#alg:aitstar:iterate-forward-search:add-edge-to-tree){reference-type="ref" reference="alg:aitstar:iterate-forward-search:add-edge-to-tree"} and [\[alg:aitstar:iterate-forward-search:expand-child-state\]](#alg:aitstar:iterate-forward-search:expand-child-state){reference-type="ref" reference="alg:aitstar:iterate-forward-search:expand-child-state"}).

::: algorithm
$\outedges \leftarrow \emptyset$
:::

::: algorithm
:::

::: algorithm
$\sampledstates \leftarrow \set*{\state \in \sampledstates 
    \adsolcost{\state} \leq \currentcost}$ $\fwdvertices \leftarrow \set*{\state \in \fwdvertices 
    \adsolcost{\state} \leq \currentcost}$ $\fwdedges \leftarrow \set*{\edge{\sourcestate}{\targetstate} \in \fwdedges
  \max \set*{\adsolcost{\sourcestate}, \adsolcost{\targetstate}} \leq \currentcost}$
:::

A forward search iteration finishes by updating the current solution cost (Alg. [\[alg:aitstar:technical\]](#alg:aitstar:technical){reference-type="ref" reference="alg:aitstar:technical"}, line [\[alg:aitstar:iterate-forward-search:update-solution-cost\]](#alg:aitstar:iterate-forward-search:update-solution-cost){reference-type="ref" reference="alg:aitstar:iterate-forward-search:update-solution-cost"}). In practice this is done efficiently by only checking the goals in the forward tree.

The entire forward search terminates when it is guaranteed that the optimal solution in the current [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation is found. This occurs when no edge in the forward queue can possibly improve the current solution (Alg. [\[alg:aitstar:technical\]](#alg:aitstar:technical){reference-type="ref" reference="alg:aitstar:technical"}, ). The forward search also terminates when the start and goal are not in the same connected component of the [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation. This occurs when the reverse search tree does not reach any edge in the forward queue, but this condition is omitted from Algorithm [\[alg:aitstar:technical\]](#alg:aitstar:technical){reference-type="ref" reference="alg:aitstar:technical"} for clearer structure.

The three steps of [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"}, i.e., improving the [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation, updating the heuristic with the reverse search, and finding valid paths with the forward search, are repeated for as long as computational time allows or until a suitable solution is found. This results in increasingly accurate cost heuristics for increasingly efficient searches of increasingly accurate [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximations and will almost-surely asymptotically converge to the optimal solution in the limit of infinite samples .

## [EIT\*]{acronym-label="EIT*" acronym-form="singular+full"} {#sec:effort-informed-trees}

Informed planning algorithms guided by admissible cost heuristics, such as [BIT\*]{acronym-label="BIT*" acronym-form="singular+short"}, [ABIT\*]{acronym-label="ABIT*" acronym-form="singular+short"}, and [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"}, need effective *a priori* admissible cost heuristics to provide benefits over uninformed algorithms. Such heuristics may not exist because the available admissible cost heuristics may be too computationally expensive or too inaccurate to be effective, even for [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"}. [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} builds on [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} by exploiting problem-specific information in a way that leverages informative admissible cost heuristics when they are available but can still search problems effectively when they are not. It achieves this by leveraging additional types of problem-specific information, including information on the computational effort required to validate a path. This generalizes asymptotically optimal informed path planning algorithms to a broader class of problems that include those without effective *a priori* cost heuristics.

[EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} consists of the same three high-level steps as [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"}:

::: enumerate*
improving the [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation (sampling; )

updating the heuristics (reverse search; )

finding valid paths in the current [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation (forward search; ),
:::

as shown in Algorithm [\[alg:conceptual\]](#alg:conceptual){reference-type="ref" reference="alg:conceptual"}. Identically to [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"}, [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} also approximates the state space with a series of increasingly dense [RGG]{acronym-label="RGG" acronym-form="singular+short"}s and skips the forward search if the reverse search terminates without reaching the start. In contrast to [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"}, the reverse search of [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} includes adaptive sparse collision detection on the edges and calculates both problem-specific path-cost and search-effort heuristics which are exploited in an anytime manner by the forward search of [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"}. The full technical details of [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} are given in Algorithms [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"} and [\[alg:eitstar:get-best-forward-edge\]](#alg:eitstar:get-best-forward-edge){reference-type="ref" reference="alg:eitstar:get-best-forward-edge"} using the same $\neighborstates*{}$, $\expandstate*{}$, and $\prunestates*{}$ subroutines as [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} (Algs. [\[alg:aitstar:neighbors\]](#alg:aitstar:neighbors){reference-type="ref" reference="alg:aitstar:neighbors"}, [\[alg:aitstar:expand-edge\]](#alg:aitstar:expand-edge){reference-type="ref" reference="alg:aitstar:expand-edge"}, and [\[alg:aitstar:prune\]](#alg:aitstar:prune){reference-type="ref" reference="alg:aitstar:prune"}).

:::: {#fig:eitstar-step-by-step .figure}
:::: {#fig:eitstar-step-1 .figure}
::: caption
:::
::::

:::: {#fig:eitstar-step-2 .figure}
::: caption
:::
::::

:::: {#fig:eitstar-step-3 .figure}
::: caption
:::
::::

:::: {#fig:eitstar-step-4 .figure}
::: caption
:::
::::

:::: {#fig:eitstar-step-5 .figure}
::: caption
:::
::::

::: caption
Five snapshots of EIT\*'s search when optimizing obstacle clearance. The start and goal specifications are represented by a black dot (  ) and circle (  ), respectively. Sampled states are represented by small black dots (  ). State space obstacles are indicated with gray rectangles (  ). The forward search tree is shown with black lines (  ) and the reverse search tree with gray lines (  ). The current best solution is highlighted in yellow (  ). EIT\* starts by initializing the [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation and calculating approximation-specific cost and effort heuristics with a reverse search without collision detection (). EIT\* exploits the calculated heuristics to guide its forward search and repairs the reverse search tree whenever the forward search reveals that it contains an invalid edge. The forward search is initially ordered on the least calculated effort-to-go from a state to the goal, which results in fast initial solution times (). Once the initial solution is found, the forward search uses the calculated cost heuristics to find the resolution-optimal solution on the current [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation (). Having found the resolution optimal solution on an [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation, [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} improves this approximation, updates the heuristic, and aims to find the next best resolution-optimal solution with minimal computational effort (). This process is repeated until the algorithm is stopped and will almost-surely asymptotically converge towards the optimal solution ().
:::
::::

### Reverse Search {#sec:eit-reverse-search}

[EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} calculates an admissible cost heuristic, an inadmissible cost heuristic, and an inadmissible effort heuristic for each [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation. The calculated admissible cost heuristic is a lower bound on the optimal cost of a path from a state to the goal and is denoted by the label $\hat{h}[\,\cdot\,]$. The calculated inadmissible cost heuristic approximates the cost of an optimal path from a state to the goal and is denoted by the label $\bar{h}[\,\cdot\,]$. This inadmissible cost heuristic is often more accurate than its admissible analogue because it can capture more problem-specific knowledge, including information that may overestimate the true cost. The calculated inadmissible effort heuristic approximates the computational effort required to find and validate a path from a state to the goal and is denoted by the label $\bar{e}[\,\cdot\,]$. An example of such a heuristic is the number of collision checks required to validate a path, which is available and informative for all planning problems as it only depends on path length and collision detection resolution and not on the optimization objective.

These heuristics are computed as in [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} with a reverse search that combines *a priori* heuristics between multiple states into more accurate heuristics between each state and the goal. The calculated admissible cost heuristic, $\hat{h}[\,\cdot\,]$, is computed by combining *a priori* admissible cost heuristics, $\hat{c}(\,\cdot\,,\,\cdot\,)$, with a reverse search that preserves the admissibility of the heuristic between each state and the goal. The calculated inadmissible cost and effort heuristics, $\bar{h}[\,\cdot\,]$ and $\bar{e}[\,\cdot\,]$, are similarly computed with the inadmissible *a priori* cost and effort heuristics, $\bar{c}\left(\,\cdot\,,\,\cdot\,\right)$ and $\bar{e}\left(\,\cdot\,,\,\cdot\,\right)$. All three heuristics always have a value of zero for any goal state.

The reverse search of [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} is an edge-queue version of A\* with adaptive sparse collision detection. Collision detection is traditionally considered a computationally expensive operation in sampling-based planning [@hauser_icra2015; @kleinbort_afr2020] but this is due to the com­pu­tational cost of validating valid edges [@sanchez_rr2003]. Detecting invalid edges with sparse collision detection is computationally cheaper and was found to be of similar computational cost to other operations in the reverse search when solving the problems presented in .

The queue of the reverse A\* search in [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} is denoted by $\mathcal{Q}_{\mathcal{R}}$ and ordered lexicographically according to $$\begin{align*}
  \mathtt{key}_{\mathcal{R}}^{\text{EIT*}}\left( \bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}} \right) \coloneqq \Big( &\hat{h}\left[ \bm{\mathrm{x}}_{\mathrm{s}} \right] + \hat{c}\left( \bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}} \right) + \hat{g}\left( \bm{\mathrm{x}}_{\mathrm{t}} \right), \\
                                                                                                                     &\bar{e}\left[ \bm{\mathrm{x}}_{\mathrm{s}} \right] + \bar{e}\left( \bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}} \right) + \bar{d}\left( \bm{\mathrm{x}}_{\mathrm{t}} \right) \Big),
\end{align*}$$ where $\hat{g}(\bm{\mathrm{x}}_{\mathrm{t}})$ and $\bar{d}(\bm{\mathrm{x}}_{\mathrm{t}})$ denote admissible *a priori* cost and inadmissible *a priori* effort heuristics for a path from the target state, $\bm{\mathrm{x}}_{\mathrm{t}}$, to the start. The two parts of the key represent the total potential solution cost of a path through an edge and the total potential computational effort required to validate a path through an edge, respectively. The first part of the key ensures the admissibility of the calculated cost heuristic and the second part of the key ensures tiebreaks in favor of lower estimated effort, which is important if only the trivially admissible cost heuristic is available, i.e., $\forall \bm{\mathrm{x}}, \bm{\mathrm{x}}^{\prime} \in X,
\hat{c}(\bm{\mathrm{x}}, \bm{\mathrm{x}}^{\prime} ) \equiv \hat{g}(
\bm{\mathrm{x}} ) \equiv 0$.

New heuristics are calculated when the [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation is initialized or improved and updated when the forward search detects that the heuristics were calculated with an invalid edge. If the heuristics are calculated because of an initialized or improved approximation, then the resolution of the adaptive sparse collision detection is reset to a user-specified parameter (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, lines [\[alg:eitstar:technical:initialize-cd-resolution\]](#alg:eitstar:technical:initialize-cd-resolution){reference-type="ref" reference="alg:eitstar:technical:initialize-cd-resolution"} and [\[alg:eitstar:improve-approximation:reinitialize-cd-resolution\]](#alg:eitstar:improve-approximation:reinitialize-cd-resolution){reference-type="ref" reference="alg:eitstar:improve-approximation:reinitialize-cd-resolution"}). If they are updated because of an invalid edge, then the resolution of the sparse collision detection in the reverse search is increased (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, line [\[alg:eitstar:iterate-forward-search:update-cd-resolution\]](#alg:eitstar:iterate-forward-search:update-cd-resolution){reference-type="ref" reference="alg:eitstar:iterate-forward-search:update-cd-resolution"}).

Each iteration of the reverse search extracts the edge with the lowest $\mathtt{key}_{\mathcal{R}}^{\text{EIT*}}$-value from the reverse queue (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, lines [\[alg:eitstar:iterate-reverse-search:get-best-rev-edge\]](#alg:eitstar:iterate-reverse-search:get-best-rev-edge){reference-type="ref" reference="alg:eitstar:iterate-reverse-search:get-best-rev-edge"} and [\[alg:eitstar:iterate-reverse-search:remove-best-rev-edge\]](#alg:eitstar:iterate-reverse-search:remove-best-rev-edge){reference-type="ref" reference="alg:eitstar:iterate-reverse-search:remove-best-rev-edge"}) and checks $d$ evenly distributed states along this edge for collision (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, line [\[alg:eitstar:iterate-reverse-search:could-be-valid\]](#alg:eitstar:iterate-reverse-search:could-be-valid){reference-type="ref" reference="alg:eitstar:iterate-reverse-search:could-be-valid"}). If a collision is found, then the edge is added to the set of invalid edges (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, line [\[alg:eitstar:iterate-reverse-search:remember-invalid-edge\]](#alg:eitstar:iterate-reverse-search:remember-invalid-edge){reference-type="ref" reference="alg:eitstar:iterate-reverse-search:remember-invalid-edge"}), otherwise it is used to improve the inadmissible cost- and effort heuristics, if possible (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, lines [\[alg:eitstar:iterate-reverse-search:update-inad-cost\]](#alg:eitstar:iterate-reverse-search:update-inad-cost){reference-type="ref" reference="alg:eitstar:iterate-reverse-search:update-inad-cost"} and [\[alg:eitstar:iterate-reverse-search:update-inad-effort\]](#alg:eitstar:iterate-reverse-search:update-inad-effort){reference-type="ref" reference="alg:eitstar:iterate-reverse-search:update-inad-effort"}).

The edge is then checked if it can improve the admissible cost heuristic of its target (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, line [\[alg:eitstar:iterate-reverse-search:admissible-cost-test\]](#alg:eitstar:iterate-reverse-search:admissible-cost-test){reference-type="ref" reference="alg:eitstar:iterate-reverse-search:admissible-cost-test"}). If it can, then the heuristic is updated and the target is either rewired or added to the reverse search tree (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, lines [\[alg:eitstar:iterate-reverse-search:admissible-cost-update\]](#alg:eitstar:iterate-reverse-search:admissible-cost-update){reference-type="ref" reference="alg:eitstar:iterate-reverse-search:admissible-cost-update"}--[\[alg:eitstar:iterate-reverse-search:insert-state-in-tree\]](#alg:eitstar:iterate-reverse-search:insert-state-in-tree){reference-type="ref" reference="alg:eitstar:iterate-reverse-search:insert-state-in-tree"}). The reverse search iteration is completed by expanding the outgoing edges of the target into the reverse queue.

Similar to [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"}, the reverse search is suspended when the total potential solution cost of the best edge in the reverse queue is greater than or equal to that of the best edge in the forward queue and the target of the best edge in the forward queue is closed (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"} lines [\[alg:eitstar:technical:continue-reverse-search-1\]](#alg:eitstar:technical:continue-reverse-search-1){reference-type="ref" reference="alg:eitstar:technical:continue-reverse-search-1"} and [\[alg:eitstar:technical:continue-reverse-search-2\]](#alg:eitstar:technical:continue-reverse-search-2){reference-type="ref" reference="alg:eitstar:technical:continue-reverse-search-2"}). This guarantees that no other edge in the forward queue would be better if the reverse search was continued [@strub_phd2021]. The reverse search is also suspended when the reverse or forward queue is empty, when all edges in the forward queue have closed targets, or when the inflation factor is infinity and any edge in the forward queue has a target in the reverse tree, but these conditions are omitted from Algorithm [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"} for clearer structure.

### Forward Search {#sec:eit-forward-search}

The forward search of [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} is an edge-queue version of [AEES]{acronym-label="AEES" acronym-form="singular+short"} which exploits the cost and effort heuristics calculated by the reverse search of [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} in an anytime manner. It leverages problem-specific cost and effort information and results in effective searches with fast initial solution times even when no admissible cost heuristics are available *a priori* (, , Extension 2).

[AEES]{acronym-label="AEES" acronym-form="singular+short"} searches the same [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation multiple times with successively tighter suboptimality bounds. It initially prioritizes quickly finding any solution over efficiently finding the resolution-optimum, which improves anytime performance. [AEES]{acronym-label="AEES" acronym-form="singular+short"} is especially useful when no informative admissible cost heuristic is available *a priori* because it can exploit an effort heuristic to guide its search. Once an initial solution is found, [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} uses both the calculated admissible and inadmissible cost heuristics to improve the tree until it finds the resolution-optimum.

The forward search of [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} orders its queue by considering

::: enumerate*
a lower bound on the optimal solution cost

an estimate of the optimal solution cost

and an estimate of the minimum remaining effort to validate a solution within the current suboptimality bound.
:::

#### Optimal cost bound

A lower bound on the optimal solution cost in the current [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation is computed as $$\begin{align*}
  \mathop{\min}_{(\bm{\mathrm{x}}_{\mathrm{s}},
  \bm{\mathrm{x}}_{\mathrm{t}}) \in \mathcal{Q}_{\mathcal{F}}}
  \hat{s}\left( \bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}}
  \right)
\end{align*}$$ where $\hat{s} \colon X_{\mathrm{sampled}} \times X_{\mathrm{sampled}} \to [0, \infty)$ estimates the solution cost through an edge as $$\begin{align*}
\hat{s}\left( \bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}} \right) \coloneqq g_{\mathcal{F}}\left( \bm{\mathrm{x}}_{\mathrm{s}} \right) + \hat{c}\left( \bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}} \right) + \hat{h}\left[ \bm{\mathrm{x}}_{\mathrm{t}} \right],
\end{align*}$$ where $g_{\mathcal{F}}\left( \bm{\mathrm{x}}_{\mathrm{s}} \right)$ is the cost to come to the source of the edge, $\hat{c}\left( \bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}}
\right)$ is the admissible cost heuristic of the edge, and $\hat{h}\left[ \bm{\mathrm{x}}_{\mathrm{t}} \right]$ is the calculated admissible cost heuristic to go from the target of the edge. At least one edge in the forward queue has an optimally connected source state [Lemma 1, @hart_tssc1968]. The edge with the smallest $\hat{s}$-value in the queue is therefore a lower bound on the optimal solution cost in the current [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation. It is denoted as $$\begin{align*}
  (\bm{\mathrm{x}}_{\mathrm{s}}^{\hat{s}}, \bm{\mathrm{x}}_{\mathrm{t}}^{\hat{s}}) \coloneqq \mathop{\arg\min}_{(\bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}}) \in \mathcal{Q}_{\mathcal{F}}} \hat{s}\left( \bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}} \right).
\end{align*}$$

#### Optimal cost estimate

A more accurate, but possibly inadmissible, estimate of the optimal solution cost in the current [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation is computed as $$\begin{align*}
  \mathop{\min}_{(\bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}}) \in \mathcal{Q}_{\mathcal{F}}} \bar{s}\left( \bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}} \right),
\end{align*}$$ where $\bar{s} \colon X_{\mathrm{sampled}} \times X_{\mathrm{sampled}} \to [0, \infty)$ is also an estimate of the solution cost through an edge but with the inadmissible heuristics $\bar{c}$ and $\bar{h}$ instead of the admissible heuristics $\hat{c}$ and $\hat{h}$. It is defined as $$\begin{align*}
  \bar{s}\left( \bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}} \right) \coloneqq g_{\mathcal{F}}(\bm{\mathrm{x}}_{\mathrm{s}}) + \bar{c}\left( \bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}} \right) + \bar{h}\left[ \bm{\mathrm{x}}_{\mathrm{t}} \right].
\end{align*}$$ This estimate is often more accurate than the admissible lower bound because it can use information that may overestimate the true cost. The edge that leads to this possibly inadmissible estimate of optimal solution cost is denoted as $$\begin{align*}
  (\bm{\mathrm{x}}_{\mathrm{s}}^{\bar{s}},
  \bm{\mathrm{x}}_{\mathrm{t}}^{\bar{s}}) \coloneqq
  \mathop{\arg\min}_{(\bm{\mathrm{x}}_{\mathrm{s}},
  \bm{\mathrm{x}}_{\mathrm{t}}) \in \mathcal{Q}_{\mathcal{F}}} \bar{s}\left( \bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}} \right).
\end{align*}$$

::: algorithm
$\currentcost \leftarrow \infty$ $\sampledstates \leftarrow \goalstates \cup \{ \startstate \}$ $\fwdvertices \leftarrow \startstate$`;` $\fwdedges \leftarrow \emptyset$`;` $\fwdqueue \leftarrow \emptyset$ $\revvertices \leftarrow \goalstates$`;` $\closedrevvertices \leftarrow \emptyset$`;` $\revedges \leftarrow \emptyset$`;` $\revqueue \leftarrow \emptyset$[]{#alg:eitstar:technical:initialize-reverse-tree label="alg:eitstar:technical:initialize-reverse-tree"} $\inflationfactor \leftarrow \updateinflationfactor$[]{#alg:eitstar:technical:initialize-inflation-factor label="alg:eitstar:technical:initialize-inflation-factor"} $\cdresolution \leftarrow \updatecdresolution$[]{#alg:eitstar:technical:initialize-cd-resolution label="alg:eitstar:technical:initialize-cd-resolution"} $\fwdqueue \leftarrow \expandstate{\startstate}$`;` $\revqueue \leftarrow \expandstate{\goalstates}$[]{#alg:eitstar:initialize-queues:expand-start-and-goals label="alg:eitstar:initialize-queues:expand-start-and-goals"} []{#alg:eitstar:technical:repeat-end label="alg:eitstar:technical:repeat-end"}
:::

::: algorithm
$\displaystyle \edge{\inadremeffortsrc}{\inadremefforttgt} \leftarrow
  \mathop{\arg\,\min}_{\edge{\sourcestate}{\targetstate} \in \queue[\fwdsymbol][\inflationfactor\inadsolcostlabel*{}{}]} \set*{\inadedgeeffort{\sourcestate}{\targetstate} + \inadefforttogolabel{\targetstate}}$ $\displaystyle \edge{\inadsolcostsrc}{\inadsolcosttgt} \leftarrow
  \mathop{\arg\,\min}_{\edge{\sourcestate}{\targetstate} \in \fwdqueue} \set*{\fwdctc{\sourcestate} + \inadedgecost{\sourcestate}{\targetstate} + \inadctglabel{\targetstate}}$ $\displaystyle \edge{\adsolcostsrc}{\adsolcosttgt} \leftarrow
  \mathop{\arg\,\min}_{\edge{\sourcestate}{\targetstate} \in \fwdqueue} \set*{\fwdctc{\sourcestate} + \adedgecost{\sourcestate}{\targetstate} + \adctglabel{\targetstate}}$
:::

#### Minimum effort estimate

An estimate of the minimum remaining effort to validate a solution within the suboptimality bound is computed as $$\begin{align*}
  \mathop{\min}\limits_{(\bm{\mathrm{x}}_{\mathrm{s}},
  \bm{\mathrm{x}}_{\mathrm{t}}) \in \mathcal{Q}_{\mathcal{F}}^{w\bar{s}}}
  \bar{r}\left( \bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}} \right),
\end{align*}$$ where $\bar{r} \colon X_{\mathrm{sampled}} \times X_{\mathrm{sampled}} \to [0,
\infty)$ estimates the remaining effort to validate a solution through an edge as, $$\begin{align*}
  \bar{r}\left( \bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}}
  \right) \coloneqq \bar{e}\left( \bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}} \right) + \bar{e}\left[ \bm{\mathrm{x}}_{\mathrm{t}} \right],
\end{align*}$$ where $\bar{e}\left( \bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}}
\right)$ is the heuristic effort to validate the edge and $\bar{e}\left[ \bm{\mathrm{x}}_{\mathrm{t}} \right]$ is the calculated heuristic effort to validate a solution from the target of the edge. The minimum is taken only over the edges in the queue that are estimated to lead to a solution within the current suboptimality factor, $w$, $$\begin{align*}
  \mathcal{Q}_{\mathcal{F}}^{w\bar{s}} \coloneqq \set*{(\bm{\mathrm{x}}_{\mathrm{s}},  \bm{\mathrm{x}}_{\mathrm{t}}) \in \mathcal{Q}_{\mathcal{F}} \,\, \bar{s}(\bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}}) \leq w \bar{s}\left( \bm{\mathrm{x}}_{\mathrm{s}}^{\bar{s}}, \bm{\mathrm{x}}_{\mathrm{t}}^{\bar{s}} \right)}.
\end{align*}$$ The edge that results in this estimate of the minimum required effort remaining to find a solution within the current suboptimality bound is denoted as $$\begin{align*}
  (\bm{\mathrm{x}}_{\mathrm{s}}^{\bar{r}},
  \bm{\mathrm{x}}_{\mathrm{t}}^{\bar{r}}) \coloneqq
  \mathop{\arg\min}\limits_{(\bm{\mathrm{x}}_{\mathrm{s}},
  \bm{\mathrm{x}}_{\mathrm{t}}) \in \mathcal{Q}_{\mathcal{F}}^{w\bar{s}}}
  \bar{r}\left( \bm{\mathrm{x}}_{\mathrm{s}}, \bm{\mathrm{x}}_{\mathrm{t}} \right).
\end{align*}$$

[EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} first checks if the queue contains an edge that could improve the current solution (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, line [\[alg:eitstar:technical:continue-forward-search\]](#alg:eitstar:technical:continue-forward-search){reference-type="ref" reference="alg:eitstar:technical:continue-forward-search"}). If none of the edges in the forward queue can, then the [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation is improved by pruning states that are not in the informed set and sampling more states (Alg. [\[alg:aitstar:prune\]](#alg:aitstar:prune){reference-type="ref" reference="alg:aitstar:prune"} and Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, lines [\[alg:eitstar:improve-approximation:prune\]](#alg:eitstar:improve-approximation:prune){reference-type="ref" reference="alg:eitstar:improve-approximation:prune"} and [\[alg:eitstar:improve-approximation:sample\]](#alg:eitstar:improve-approximation:sample){reference-type="ref" reference="alg:eitstar:improve-approximation:sample"}). The reverse search tree and set of closed vertices are then reset (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, line [\[alg:eitstar:technical:reinitialize-reverse-tree\]](#alg:eitstar:technical:reinitialize-reverse-tree){reference-type="ref" reference="alg:eitstar:technical:reinitialize-reverse-tree"}) and the forward and reverse search queues are reinitialized by inserting the outgoing edges of the start and goals, respectively (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, line [\[alg:eitstar:reinitialize-queues:expand-start-and-goals\]](#alg:eitstar:reinitialize-queues:expand-start-and-goals){reference-type="ref" reference="alg:eitstar:reinitialize-queues:expand-start-and-goals"}).

If at least one edge in the forward queue could improve the current solution, then the edge that is estimated to lead to the fastest improvement of the current solution is extracted from the queue (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, lines [\[alg:eitstar:iterate-forward-search:get-best-edge\]](#alg:eitstar:iterate-forward-search:get-best-edge){reference-type="ref" reference="alg:eitstar:iterate-forward-search:get-best-edge"} and [\[alg:eitstar:iterate-forward-search:pop-best-edge\]](#alg:eitstar:iterate-forward-search:pop-best-edge){reference-type="ref" reference="alg:eitstar:iterate-forward-search:pop-best-edge"}, and Alg. [\[alg:eitstar:get-best-forward-edge\]](#alg:eitstar:get-best-forward-edge){reference-type="ref" reference="alg:eitstar:get-best-forward-edge"}). This edge is determined with the following steps:

1.  If the edge with the minimum remaining effort required to validate a solution, $\left( \bm{\mathrm{x}}_{\mathrm{s}}^{\bar{r}},
        \bm{\mathrm{x}}_{\mathrm{t}}^{\bar{r}} \right)$, can possibly lead to a solution within the current suboptimality bound, $$\begin{align*}
        \bar{s}\left( \bm{\mathrm{x}}_{\mathrm{s}}^{\bar{r}}, \bm{\mathrm{x}}_{\mathrm{t}}^{\bar{r}} \right) \leq w \hat{s}\left( \bm{\mathrm{x}}_{\mathrm{s}}^{\hat{s}}, \bm{\mathrm{x}}_{\mathrm{t}}^{\hat{s}} \right),
    \end{align*}$$ then it is selected (Alg. [\[alg:eitstar:get-best-forward-edge\]](#alg:eitstar:get-best-forward-edge){reference-type="ref" reference="alg:eitstar:get-best-forward-edge"}, lines [\[alg:eitstar:get-best-forward-edge:best-effort-test\]](#alg:eitstar:get-best-forward-edge:best-effort-test){reference-type="ref" reference="alg:eitstar:get-best-forward-edge:best-effort-test"} and [\[alg:eitstar:get-best-forward-edge:best-effort-return\]](#alg:eitstar:get-best-forward-edge:best-effort-return){reference-type="ref" reference="alg:eitstar:get-best-forward-edge:best-effort-return"}). This edge likely improves the current solution with the least amount of computational effort.

2.  If the edge that is estimated to be on the optimal solution path, $\left( \bm{\mathrm{x}}_{\mathrm{s}}^{\bar{s}},
        \bm{\mathrm{x}}_{\mathrm{t}}^{\bar{s}} \right)$, can possibly lead to a solution within the suboptimality bound, $$\begin{align*}
        \bar{s}\left( \bm{\mathrm{x}}_{\mathrm{s}}^{\bar{s}}, \bm{\mathrm{x}}_{\mathrm{t}}^{\bar{s}} \right) \leq w \hat{s}\left( \bm{\mathrm{x}}_{\mathrm{s}}^{\hat{s}}, \bm{\mathrm{x}}_{\mathrm{t}}^{\hat{s}} \right),
    \end{align*}$$ then it is selected (Alg. [\[alg:eitstar:get-best-forward-edge\]](#alg:eitstar:get-best-forward-edge){reference-type="ref" reference="alg:eitstar:get-best-forward-edge"}, lines [\[alg:eitstar:get-best-forward-edge:best-cost-test\]](#alg:eitstar:get-best-forward-edge:best-cost-test){reference-type="ref" reference="alg:eitstar:get-best-forward-edge:best-cost-test"} and [\[alg:eitstar:get-best-forward-edge:best-cost-return\]](#alg:eitstar:get-best-forward-edge:best-cost-return){reference-type="ref" reference="alg:eitstar:get-best-forward-edge:best-cost-return"}). This edge likely steps towards the resolution-optimal solution.

3.  Otherwise the edge that provides the lower bound on the optimal solution cost in the current [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation, $\left( \bm{\mathrm{x}}_{\mathrm{s}}^{\hat{s}},
        \bm{\mathrm{x}}_{\mathrm{t}}^{\hat{s}} \right)$, is selected. This raises the lower bound on the optimal solution cost in the current [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation and increases the number of candidates available to steps 1 and 2 in the next iteration (Alg. [\[alg:eitstar:get-best-forward-edge\]](#alg:eitstar:get-best-forward-edge){reference-type="ref" reference="alg:eitstar:get-best-forward-edge"}, lines [\[alg:eitstar:get-best-forward-edge:lower-bound-cost-else\]](#alg:eitstar:get-best-forward-edge:lower-bound-cost-else){reference-type="ref" reference="alg:eitstar:get-best-forward-edge:lower-bound-cost-else"} and [\[alg:eitstar:get-best-forward-edge:lower-bound-cost-return\]](#alg:eitstar:get-best-forward-edge:lower-bound-cost-return){reference-type="ref" reference="alg:eitstar:get-best-forward-edge:lower-bound-cost-return"}).

The forward search in [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} then proceeds similarly to [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"}. If the selected edge is in the forward search tree, then its target state is expanded and the forward search iteration is complete (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, lines [\[alg:eitstar:iterate-forward-search:is-edge-in-tree\]](#alg:eitstar:iterate-forward-search:is-edge-in-tree){reference-type="ref" reference="alg:eitstar:iterate-forward-search:is-edge-in-tree"} and [\[alg:eitstar:iterate-forward-search:expand-edge-in-tree\]](#alg:eitstar:iterate-forward-search:expand-edge-in-tree){reference-type="ref" reference="alg:eitstar:iterate-forward-search:expand-edge-in-tree"}). If the selected edge is not part of the forward search tree but can possibly improve it, then it is checked for collisions (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, lines [\[alg:eitstar:iterate-forward-search:can-edge-possibly-improve-tree\]](#alg:eitstar:iterate-forward-search:can-edge-possibly-improve-tree){reference-type="ref" reference="alg:eitstar:iterate-forward-search:can-edge-possibly-improve-tree"} and [\[alg:eitstar:iterate-forward-search:collision-detection\]](#alg:eitstar:iterate-forward-search:collision-detection){reference-type="ref" reference="alg:eitstar:iterate-forward-search:collision-detection"}).

If collisions are detected, then the edge is added to the invalid edges (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, line [\[alg:eitstar:iterate-forward-search:blacklist\]](#alg:eitstar:iterate-forward-search:blacklist){reference-type="ref" reference="alg:eitstar:iterate-forward-search:blacklist"}) and if it is in the reverse search tree, then the reverse search tree and queue are reset and the sparse collision detection resolution is updated, which will improve the accuracy of the heuristic computed by restarting the reverse search (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, lines [\[alg:eitstar:iterate-forward-search:reverse-tree-check\]](#alg:eitstar:iterate-forward-search:reverse-tree-check){reference-type="ref" reference="alg:eitstar:iterate-forward-search:reverse-tree-check"}--[\[alg:eitstar:iterate-forward-search:reexpand-goal-states\]](#alg:eitstar:iterate-forward-search:reexpand-goal-states){reference-type="ref" reference="alg:eitstar:iterate-forward-search:reexpand-goal-states"}). If no collisions are detected, then the true cost of the edge is evaluated to check whether it actually improves the current solution and forward search tree (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, lines [\[alg:eitstar:iterate-forward-search:can-edge-actually-improve-solution\]](#alg:eitstar:iterate-forward-search:can-edge-actually-improve-solution){reference-type="ref" reference="alg:eitstar:iterate-forward-search:can-edge-actually-improve-solution"} and [\[alg:eitstar:iterate-forward-search:can-edge-actually-improve-tree\]](#alg:eitstar:iterate-forward-search:can-edge-actually-improve-tree){reference-type="ref" reference="alg:eitstar:iterate-forward-search:can-edge-actually-improve-tree"}).

If the edge improves the current solution and forward search tree, then its target state is added to the tree if it is not already in it (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, lines [\[alg:eitstar:iterate-forward-search:forward-tree-check\]](#alg:eitstar:iterate-forward-search:forward-tree-check){reference-type="ref" reference="alg:eitstar:iterate-forward-search:forward-tree-check"} and [\[alg:eitstar:iterate-forward-search:add-state-to-tree\]](#alg:eitstar:iterate-forward-search:add-state-to-tree){reference-type="ref" reference="alg:eitstar:iterate-forward-search:add-state-to-tree"}). If the target state is already in the tree, then the edge causes a rewiring and the edge from the old parent is removed from the tree (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, lines [\[alg:eitstar:iterate-forward-search:rewiring-else\]](#alg:eitstar:iterate-forward-search:rewiring-else){reference-type="ref" reference="alg:eitstar:iterate-forward-search:rewiring-else"} and [\[alg:eitstar:iterate-forward-search:rewiring\]](#alg:eitstar:iterate-forward-search:rewiring){reference-type="ref" reference="alg:eitstar:iterate-forward-search:rewiring"}). The new edge is then added to the tree, its target state is expanded into the forward queue, and the solution cost is updated (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, lines [\[alg:eitstar:iterate-forward-search:add-edge-to-tree\]](#alg:eitstar:iterate-forward-search:add-edge-to-tree){reference-type="ref" reference="alg:eitstar:iterate-forward-search:add-edge-to-tree"}--[\[alg:eitstar:iterate-forward-search:update-solution-cost\]](#alg:eitstar:iterate-forward-search:update-solution-cost){reference-type="ref" reference="alg:eitstar:iterate-forward-search:update-solution-cost"}). If the edge results in an improved solution, then the suboptimality factor is changed according to a user-specified update policy (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, lines [\[alg:eitstar:iterate-forward-search:update-inflation-factor\]](#alg:eitstar:iterate-forward-search:update-inflation-factor){reference-type="ref" reference="alg:eitstar:iterate-forward-search:update-inflation-factor"}). Section [4](#sec:experimental-results){reference-type="ref" reference="sec:experimental-results"} presents the update policy used in the experimental evaluation of [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"}.

The entire forward search terminates when it is guaranteed that the optimal solution in the current [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation is found. This occurs when no edge in the forward queue can possibly improve the current solution (Alg. [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"}, ). The forward search also terminates when the start and goal are not in the same connected component of the [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation. This occurs when the reverse search tree does not reach any edge in the forward queue, but this condition is omitted from Algorithm [\[alg:eitstar:technical\]](#alg:eitstar:technical){reference-type="ref" reference="alg:eitstar:technical"} for clearer structure.

Similar to [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"}, the three steps of [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"}, i.e., improving the [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation, updating the heuristic with the reverse search, and finding valid paths with the forward search, are repeated for as long as computational time allows or until a suitable solution is found. This results in increasingly accurate cost and effort heuristics for increasingly efficient and effective searches of increasingly accurate approximations and will also almost-surely asymptotically converge to the optimal solution in the limit of infinite samples .

## Analysis {#sec:analysis}

Any path planning algorithm that processes a sampling-based approximation with a graph-search algorithm is almost-surely asymptotically optimal if the approximation almost-surely contains an asymptotically optimal solution and the graph-search algorithm is resolution-optimal. This is a sufficient but not necessary condition. The almost-sure asymptotic optimality of [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} follows from proven properties of their [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximations and graph-search algorithms.

### [AIT\*]{acronym-label="AIT*" acronym-form="singular+abbrv"} {#sec:ait-analysis}

The [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation constructed by [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} almost-surely contains an asymptotically optimal solution because it contains all the edges in [PRM\*]{acronym-label="PRM*" acronym-form="singular+abbrv"} for any set of samples and [PRM\*]{acronym-label="PRM*" acronym-form="singular+abbrv"} is almost-surely asymptotically optimal [@karaman_ijrr2011]. [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"}'s forward search is resolution-optimal because A\* is a resolution-optimal algorithm if it is provided with an admissible cost heuristic [@hart_tssc1968]. [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"}'s reverse search without collision detection results in an admissible cost-heuristic because [LPA\*]{acronym-label="LPA*" acronym-form="singular+short"} is also a resolution-optimal algorithm [@aine_ai2016] and because adding collision detection cannot decrease path cost. [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} is therefore almost-surely asymptotically optimal.

### [EIT\*]{acronym-label="EIT*" acronym-form="singular+abbrv"} {#sec:eit-analysis}

The [RGG]{acronym-label="RGG" acronym-form="singular+short"} approximation constructed by [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} almost-surely contains an asymptotically optimal solution because like [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} it also contains all the edges in [PRM\*]{acronym-label="PRM*" acronym-form="singular+abbrv"} and [PRM\*]{acronym-label="PRM*" acronym-form="singular+abbrv"} is almost-surely asymptotically optimal [@karaman_ijrr2011]. EIT\*'s forward search is resolution-optimal because [AEES]{acronym-label="AEES" acronym-form="singular+short"} is a resolution-optimal algorithm when the cost heuristic is admissible and the suboptimality factor is one [@thayer_icaps2011a]. EIT\*'s reverse search with sparse collision detection results in an admissible cost heuristic because denser collision detection cannot decrease path cost and A\* is a resolution-optimal graph-search algorithm when provided with an admissible cost heuristic [@hart_tssc1968]. [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} is therefore also almost-surely asymptotically optimal.

# Experimental Results {#sec:experimental-results}

The benefits of an asymmetric bidirectional search are shown on abstract, robotic manipulator, and knee replacement dislocation problems (Sections [4.1](#sec:abstract-problems){reference-type="ref" reference="sec:abstract-problems"}--[4.3](#sec:knee-implants){reference-type="ref" reference="sec:knee-implants"}). [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} were compared against the AC@OMPL [OMPL]{acronym-label="OMPL" acronym-form="singular+abbrv"} [@sucan_ram2012] [OMPL]{acronym-label="OMPL" acronym-form="singular+long"} [[OMPL]{acronym-label="OMPL" acronym-form="singular+abbrv"}; @sucan_ram2012] implementations of RRT, RRT-Connect, RRT\*, LBT-RRT, LazyPRM\*, FMT\*, BIT\*, and ABIT\*[^1].

The planners were tested when optimizing path length and obstacle clearance. Path length was optimized by minimizing the arc length of the path in state space. Obstacle clearance was optimized by minimizing the reciprocal of clearance integrated over the arc length of the path, $l$, $$\begin{align*}
  c(\sigma) &\coloneqq \int_{0}^{l} \frac{ 1 }{ \delta\left( \sigma(\nicefrac{s}{l}) \right) } \,\mathrm{d}s,
\end{align*}$$ where $\delta\colon X \to [10^{-6}, \infty)$ is the distance of a state to the nearest obstacle, limited to be no smaller than $10^{-6}$, $$\begin{align*}
  \delta\left( \bm{\mathrm{x}} \right) \coloneqq \max \left\{
  \mathop{\mathrm{clearance}}(\bm{\mathrm{x}}), 10^{-6} \right\}.
\end{align*}$$ The lower limit on $\delta$ ensures numerical stability and that the cost of a path is bounded by a multiple of its total variation as in . This optimization objective balances the clearance and length of a path and is similar to the objectives presented by @wein_ijrr2008 and @agarwal_ta2018.

The admissible cost heuristic, $\hat{c}$, used by informed planners was the Euclidean distance for path length and the trivial zero-heuristic for obstacle clearance. The possibly inadmissible cost heuristic, $\bar{c}$, used by [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} was again the Euclidean distance for path length and the reciprocal of the average clearance of the two end states for obstacle clearance, $$\begin{align*}
  \bar{c}\left( \bm{\mathrm{x}}_{i}, \bm{\mathrm{x}}_{j} \right) \coloneqq
  \frac{2}{\delta\left( \bm{\mathrm{x}}_{i} \right) + \delta\left(
  \bm{\mathrm{x}}_{j} \right) }.
\end{align*}$$ The effort heuristic, $\bar{e}(\,\cdot\,,\,\cdot\,)$, used by [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} was the number of collision checks required to validate a path for both objectives. It was computed by dividing the Euclidean distance between two states by the collision detection resolution.

The inflation factor update policy in [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} was configured to have an infinite inflation factor until the initial solution is found and then switch to a unity inflation factor. This results in fast initial solutions and efficient subsequent searches to improve them. The sparse collision detection resolution update policy used in [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} was configured to initially search each batch with a single collision check and then double the resolution if the forward search detects a collision on an edge used in the reverse search tree.

RRT-based planners used maximum edge lengths of 0.3, 0.9, 1.25, 1.25, 2.4, and 3.0 in $\mathbb{R}^{2}, \mathrm{SE}(3), \mathbb{R}^{7}, \mathbb{R}^{8}, \mathbb{R}^{14}$, and $\mathbb{R}^{16}$, respectively. RRT\* used informed sampling and [LBT-RRT]{acronym-label="LBT-RRT" acronym-form="singular+short"} used the default approximation factor of 0.4 but was not tested on obstacle clearance problems as it can only optimize path length. BIT\*-based planners used a batch size of $100$ samples and the $k$-nearest connection strategy with an [RGG]{acronym-label="RGG" acronym-form="singular+short"} connection parameter of $\eta = 1.001$ regardless of problem dimension.

FMT\* is not an anytime algorithm and requires the user to specify the number of samples in advance. All experiments presented in this section tested configurations of [FMT\*]{acronym-label="FMT*" acronym-form="singular+short"} with 10, 50, 100, 500, 1000, and 5000 samples. There are multiple lines for [FMT\*]{acronym-label="FMT*" acronym-form="singular+short"} in the presented plots because median solution times and costs were computed separately for each configuration and the results of all configurations that were able to solve a specific problem were plotted.

## Abstract Problem {#sec:abstract-problems}

State space obstacles have complex shapes even for relatively simple problems [e.g., Figure 1, @das_tro2020]. This complexity often makes it difficult to gain insight about the underlying reason for a planner's performance on a given problem. Directly designing abstract state space obstacles from basic geometries provides intuition on the performance of a planner for a given obstacle configuration and helps the algorithmic design process.

The basic geometries of these simple obstacle configurations make collision detection computationally much less expensive than in real-world problems. A simple way to simulate the more expensive collision detection of real-world problems in this abstract setting is to increase the collision detection resolution. The collision detection resolution was set to $5\cdot10^{-6}$, which on the tested hardware makes evaluating a valid edge in this abstract setting as computationally expensive as evaluating a valid edge on a dual-arm manipulation problem . While admissible cost heuristics exist for these abstract problems with clearance in state space [@strub_tr2021], such heuristics often do not exist for real-world problems with clearance in work space and therefore no heuristics were used for the clearance objective in these abstract problems either.

The abstract obstacle configuration on which the planners were tested consists of a wall with a narrow gap between the start and goal states . This obstacle configuration illustrates the speed with which planners find a hard-to-find optimal homotopy class when optimizing path length. When optimizing obstacle clearance, this configuration illustrates the challenges of searching in the absence of informative heuristics and ordering the search according to the total potential solution cost.

Three versions of the wall gap obstacle configuration in dimensions $\mathbb{R}^{2}, \mathbb{R}^{8}$, and $\mathbb{R}^{16}$ were tested for both objectives. The obstacle configuration shown in was adapted to higher dimensions by extending the obstacle such that only two homotopy classes exist for all problems.

shows the performance of all algorithms on all six instances of the problem when optimizing path length and obstacle clearance. When optimizing path length, [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} perform similarly to Lazy [PRM\*]{acronym-label="PRM*" acronym-form="singular+abbrv"}, [BIT\*]{acronym-label="BIT*" acronym-form="singular+short"}, and [ABIT\*]{acronym-label="ABIT*" acronym-form="singular+short"} and find initial solutions at least as fast as [RRT]{acronym-label="RRT" acronym-form="singular+short"}-Connect and significantly faster than [RRT\*]{acronym-label="RRT*" acronym-form="singular+abbrv"} and [LBT-RRT]{acronym-label="LBT-RRT" acronym-form="singular+short"} (Figures [30](#fig:results:wall-gap-path-length-r2){reference-type="ref" reference="fig:results:wall-gap-path-length-r2"}, , and ). When optimizing obstacle clearance, [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} outperforms all other tested asymptotically optimal planners, including [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"}, by again finding initial solutions as fast as [RRT]{acronym-label="RRT" acronym-form="singular+short"}-Connect, which has a computational advantage because it does not calculate path cost (e.g., obstacle clearance, Figures [31](#fig:results:wall-gap-clearance-r2){reference-type="ref" reference="fig:results:wall-gap-clearance-r2"}, , and ).

## Manipulator Problems {#sec:manipulator-arms}

The algorithms were also tested on path planning problems for Barrett [WAM]{acronym-label="WAM" acronym-form="singular+short"} arms in the AC@OpenRAVE [OpenRAVE]{acronym-label="OpenRAVE" acronym-form="singular+abbrv"} [@diankov_phd2010] [OpenRAVE]{acronym-label="OpenRAVE" acronym-form="singular+long"} [[OpenRAVE]{acronym-label="OpenRAVE" acronym-form="singular+abbrv"}; @diankov_phd2010] . [OpenRAVE]{acronym-label="OpenRAVE" acronym-form="singular+short"} was configured to use the AC@FCL [FCL]{acronym-label="FCL" acronym-form="singular+abbrv"} [@pan_icra2012] [FCL]{acronym-label="FCL" acronym-form="singular+long"} [[FCL]{acronym-label="FCL" acronym-form="singular+abbrv"}; @pan_icra2012] for collision detection and clearance computation, using AC@OBB [OBB]{acronym-label="OBB" acronym-form="singular+abbrv"} [@gottschalk_ccgit1996] [OBB]{acronym-label="OBB" acronym-form="singular+long"} [[OBB]{acronym-label="OBB" acronym-form="singular+abbrv"}; @gottschalk_ccgit1996] tree and AC@RSS [RSS]{acronym-label="RSS" acronym-form="singular+abbrv"} [@larsen_icra2000] [RSS]{acronym-label="RSS" acronym-form="singular+long"} [[RSS]{acronym-label="RSS" acronym-form="singular+abbrv"}; @larsen_icra2000]

volume representations, respectively. The collision detection and clearance computation resolution was set to $3.6 \cdot 10^{-3}$, which resulted in a 1% false-negative collision detection rate for invalid edges on representative problems.

### Single-Arm Manipulator Problem {#sec:single-arm-planning}

Robotic manipulator arms are commonly used in pick-and-place tasks. In the single-arm experiment, the algorithms were instructed to find paths for a Barret [WAM]{acronym-label="WAM" acronym-form="singular+short"} arm with seven degrees of freedom to place a small cube into a box .

shows the performance of all algorithms when optimizing path length and obstacle clearance. When optimizing path length, [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} perform similarly to Lazy [PRM\*]{acronym-label="PRM*" acronym-form="singular+abbrv"}, [BIT\*]{acronym-label="BIT*" acronym-form="singular+short"}, and [ABIT\*]{acronym-label="ABIT*" acronym-form="singular+short"}, which all find initial solutions nearly as fast as [RRT]{acronym-label="RRT" acronym-form="singular+short"}-Connect and significantly faster than [RRT\*]{acronym-label="RRT*" acronym-form="singular+short"} and [LBT-RRT]{acronym-label="LBT-RRT" acronym-form="singular+short"} . When optimizing obstacle clearance, [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} outperform all other tested asymptotically optimal planners but do not find initial solutions as fast as [RRT]{acronym-label="RRT" acronym-form="singular+short"}-Connect, which again has a computational advantage because it does not calculate path cost .

### Dual-Arm Manipulator Problem {#sec:dual-arm-planning}

In the dual-arm planning experiment, the algorithms were instructed to find paths for two Barret [WAM]{acronym-label="WAM" acronym-form="singular+short"} arms with a total of 14 degrees of freedom from a start configuration at the bottom shelf to a goal configuration at the top shelf .

shows the performance of all algorithms when optimizing path length and obstacle clearance. When optimizing path length, [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} performs similarly to [BIT\*]{acronym-label="BIT*" acronym-form="singular+short"} and [ABIT\*]{acronym-label="ABIT*" acronym-form="singular+short"} which perform better than Lazy [PRM\*]{acronym-label="PRM*" acronym-form="singular+abbrv"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} and find initial solutions nearly as fast as [RRT]{acronym-label="RRT" acronym-form="singular+short"}-Connect and significantly faster than [RRT\*]{acronym-label="RRT*" acronym-form="singular+short"} and [LBT-RRT]{acronym-label="LBT-RRT" acronym-form="singular+short"} . When optimizing obstacle clearance, [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} again outperform all tested asymptotically optimal planners but do not find initial solutions as fast as [RRT]{acronym-label="RRT" acronym-form="singular+short"}-Connect, which still has a computational advantage because it does not calculate path cost .

## Knee Replacement Dislocation Problem {#sec:knee-implants}

Calculating heuristics with an asymmetric bidirectional search can also improve performance on the feasible planning problem by guiding the search towards the goal. The knee replacement dislocation problem evaluates the potential of medial dislocation for the Oxford Domed Lateral [UKR]{acronym-label="UKR" acronym-form="singular+long"} [[UKR]{acronym-label="UKR" acronym-form="singular+abbrv"}; @pandit_knee2010 Figure [65](#fig:results:knee){reference-type="ref" reference="fig:results:knee"}][^2] by searching for a path to free the mobile bearing.

The Oxford Domed Lateral [UKR]{acronym-label="UKR" acronym-form="singular+short"} consists of metal femoral and ti­bial components which are fixed to the bone and a mobile polythylene bearing which separates the metal components [@gunther_knee1996]. Medial dislocation occurs when there is enough space between the tibial and femoral components for the mobile bearing to move onto the tibial-component wall where it may be trapped by the femoral component. The dislocation risk for different relative poses of the femoral and tibial components has been analyzed by using planning algorithms to search for paths that allow the bearing to reach a region representative of dislocation [@yang_caos2020; @yang_bors2021]. and  respectively illustrate the start state and goal region of the mobile bearing and the fixed poses of the tibial and femoral components used in this experiment. The state space of this problem is $\mathrm{SE}(3)$, and the mobile bearing is free to move and rotate in any direction not in collision with the fixed parts.

shows the performance of all planners when optimizing path length and obstacle clearance. When optimizing path length, [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} outperforms all other tested planners. [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} is the second best performing algorithm followed by [FMT\*]{acronym-label="FMT*" acronym-form="singular+short"}, [BIT\*]{acronym-label="BIT*" acronym-form="singular+short"}, and [ABIT\*]{acronym-label="ABIT*" acronym-form="singular+short"}. The [OMPL]{acronym-label="OMPL" acronym-form="singular+short"} implementations of [LBT-RRT]{acronym-label="LBT-RRT" acronym-form="singular+short"} and [RRT]{acronym-label="RRT" acronym-form="singular+short"}-Connect did not allow goals to be defined as a region and were replaced with [RRT]{acronym-label="RRT" acronym-form="singular+short"} for this experiment. When optimizing obstacle clearance, [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} again outperforms all other tested planners and is the only planner that achieved a success rate of 100%.

:::: {#fig:results:wall-gap .figure latex-placement="t"}
::: caption
A two-dimensional illustration of the wall gap experiment. The start and goal states are represented by a black dot (  ) and circle (  ), respectively. State space obstacles are indicated with gray rectangles (  ). Each state space dimension was bounded to the interval $[0, 1]$.
:::
::::

:::: {#fig:results:wall-gap-results .figure}
:::: {#fig:results:wall-gap-path-length-r2 .figure}
::: caption
Path length in $\mathbb{R}^{2}$
:::
::::

:::: {#fig:results:wall-gap-clearance-r2 .figure}
::: caption
Obstacle clearance in $\mathbb{R}^{2}$
:::
::::

\

:::: {#fig:results:wall-gap-path-length-r8 .figure}
::: caption
Path length in $\mathbb{R}^{8}$
:::
::::

:::: {#fig:results:wall-gap-clearance-r8 .figure}
::: caption
Obstacle clearance in $\mathbb{R}^{8}$
:::
::::

\

:::: {#fig:results:wall-gap-path-length-r16 .figure}
::: caption
Path length in $\mathbb{R}^{16}$
:::
::::

:::: {#fig:results:wall-gap-clearance-r16 .figure}
::: caption
Obstacle clearance in $\mathbb{R}^{16}$
:::
::::

\

::: figure
:::

::: caption
The planner performances on the wall gap experiments described in . The success plots show the percentages of successful runs over time. The cost plots show the median initial solution times and costs as squares and the median solution costs over time as thick lines, both with nonparametric 99% confidence intervals shown as error bars and shaded areas, respectively. Unsuccessful runs were taken as infinite costs. The results show that EIT\* outperforms all other tested asymptotically optimal planners for both objectives in terms of success rates, median initial solution times, and median solution quality over time.
:::
::::

:::: {#fig:results:one-manipulator-arm .figure}
![Start](Strub2021AIT_figs/one_arm_start_white.png){#fig:results:one-arm-start width="\\textwidth"}

![Start side view](Strub2021AIT_figs/one_arm_side_start_white.png){#fig:results:one-arm-back-start width="\\textwidth"}

![Start front view](Strub2021AIT_figs/one_arm_front_start_white.png){#fig:results:one-arm-side-start width="\\textwidth"}

![Start top view](Strub2021AIT_figs/one_arm_top_start_white.png){#fig:results:one-arm-top-start width="\\textwidth"}

\

![Goal](Strub2021AIT_figs/one_arm_goal_white.png){#fig:results:one-arm-goal width="\\textwidth"}

![Goal side view](Strub2021AIT_figs/one_arm_side_goal_white.png){#fig:results:one-arm-back-goal width="\\textwidth"}

![Goal front view](Strub2021AIT_figs/one_arm_front_goal_white.png){#fig:results:one-arm-side-goal width="\\textwidth"}

![Goal top view](Strub2021AIT_figs/one_arm_top_goal_white.png){#fig:results:one-arm-top-goal width="\\textwidth"}

::: caption
Illustrations of the single-arm manipulator problem. The top row shows the start configuration of the arm in position to pick up the red cube from the table (--). The bottom row shows the goal configuration of the arm in position to place a cube in the box (--).
:::
::::

:::: {#fig:results:one-arm-results .figure}
:::: {#fig:results:one-arm-path-length .figure}
::: caption
Path length
:::
::::

:::: {#fig:results:one-arm-clearance .figure}
::: caption
Obstacle clearance
:::
::::

\

::: figure
:::

::: caption
This figure shows the planner performances on the single-arm manipulator experiments described in . The success plots show the percentages of successful runs over time. The cost plots show the median initial solution times and costs as squares and the median solution costs over time as thick lines, both with nonparametric 99% confidence intervals shown as error bars and shaded areas, respectively. Unsuccessful runs were taken as infinite costs. The results show that for the path length version of this simple problem, [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} and [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} have near identical performances to Lazy [PRM]{acronym-label="PRM" acronym-form="singular+short"}\*, [FMT\*]{acronym-label="FMT*" acronym-form="singular+short"}, [BIT\*]{acronym-label="BIT*" acronym-form="singular+short"}, and [ABIT\*]{acronym-label="ABIT*" acronym-form="singular+short"}, which outperform [LBT-RRT]{acronym-label="LBT-RRT" acronym-form="singular+short"} and [RRT\*]{acronym-label="RRT*" acronym-form="singular+abbrv"} (). In the obstacle clearance version of the problem, [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} and [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} outperform all other almost-surely asymptotically optimal planners ().
:::
::::

:::: {#fig:results:two-manipulator-arms .figure}
![Start](Strub2021AIT_figs/two_arm_start_white.png){#fig:results:two-arm-start width="\\textwidth"}

![Start side view](Strub2021AIT_figs/two_arm_side_start_white.png){#fig:results:two-arm-back-start width="\\textwidth"}

![Start back view](Strub2021AIT_figs/two_arm_back_start_white.png){#fig:results:two-arm-side-start width="\\textwidth"}

![Start top view](Strub2021AIT_figs/two_arm_top_start_white.png){#fig:results:two-arm-top-start width="\\textwidth"}

\

![Goal](Strub2021AIT_figs/two_arm_goal_white.png){#fig:results:two-arm-goal width="\\textwidth"}

![Goal side view](Strub2021AIT_figs/two_arm_side_goal_white.png){#fig:results:two-arm-back-goal width="\\textwidth"}

![Goal back view](Strub2021AIT_figs/two_arm_back_goal_white.png){#fig:results:two-arm-side-goal width="\\textwidth"}

![Goal configuration top view](Strub2021AIT_figs/two_arm_top_goal_white.png){#fig:results:two-arm-top-goal width="\\textwidth"}

::: caption
Illustrations of the dual-arm manipulator problem. The top row shows the start configuration of the arms in position to pick up an object on the bottom shelf (--). The bottom row shows the goal configuration of the arms in position to place an object on the top shelf (--).
:::
::::

:::: {#fig:results:two-arm-results .figure}
:::: {#fig:results:two-arm-path-length .figure}
::: caption
Path length
:::
::::

:::: {#fig:results:two-arm-clearance .figure}
::: caption
Optimizing obstacle
:::
::::

\

::: figure
:::

::: caption
This figure shows the planner performances on the dual-arm manipulator experiments described in . The success plots show the percentages of successful runs over time. The cost plots show the median initial solution times and costs as squares and the median solution costs over time as thick lines, both with nonparametric 99% confidence intervals shown as error bars and shaded areas, respectively. Unsuccessful runs were taken as infinite costs. The results show when optimizing path length, [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} performs nearly identically to [BIT\*]{acronym-label="BIT*" acronym-form="singular+short"} and [ABIT\*]{acronym-label="ABIT*" acronym-form="singular+short"}, which all outperform Lazy [PRM]{acronym-label="PRM" acronym-form="singular+short"}\*, [FMT\*]{acronym-label="FMT*" acronym-form="singular+short"}, and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"}, and clearly outperform [LBT-RRT]{acronym-label="LBT-RRT" acronym-form="singular+short"} and [RRT\*]{acronym-label="RRT*" acronym-form="singular+short"} (). When optimizing obstacle clearance, [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} and [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} outperform all other almost-surely asymptotically optimal planners ().
:::
::::

:::: {#fig:results:knee .figure}
![Oxford Domed Lateral [UKR]{acronym-label="UKR" acronym-form="singular+abbrv"}\
[@pandit_knee2010]](figures/5-experimental-results/knee/cropped/original_border.png){#fig:results:knee-original width="\\textwidth"}

![Approximation used in experiments](Strub2021AIT_figs/approximation_white.png){#fig:results:knee-approximation width="\\textwidth"}

![Goal region used in experiments](Strub2021AIT_figs/goal_region_white.png){#fig:results:knee-goal-region width="\\textwidth"}

![Example goal configuration](Strub2021AIT_figs/goal_example_white.png){#fig:results:knee-goal-example width="\\textwidth"}

::: caption
A multiview illustration of the knee replacement dislocation experiment. The 3D model of the Oxford Domed Lateral [UKR]{acronym-label="UKR" acronym-form="singular+abbrv"} is reproduced from Figure 1 in @pandit_knee2010 (). The experiments presented in this paper used a simplified approximation of the Oxford Domed Lateral [UKR]{acronym-label="UKR" acronym-form="singular+abbrv"} (). The start state of the mobile bearing is between the two fixed parts () with the search space and goal region shown as red and green regions, respectively (). The goal region is the set of bearing positions in medial dislocation between the tibial and femoral components ().
:::
::::

:::: {#fig:results:knee-results .figure}
:::: {#fig:results:knee-path-length .figure}
::: caption
Path length
:::
::::

:::: {#fig:results:knee-clearance .figure}
::: caption
Obstacle clearance
:::
::::

\

::: figure
:::

::: caption
The planner performances on the knee replacement dislocation problem described in . The success plots show the percentages of successful runs over time. The cost plots show the median initial solution times and costs as squares and the median solution costs over time as thick lines, both with nonparametric 99% confidence intervals shown as error bars and shaded areas, respectively. Unsuccessful runs were taken as infinite costs. The results show that when optimizing path length, [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} and [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} outperform all other planners in terms of success rates, median initial solution times, and median solution quality over time. Lazy [PRM]{acronym-label="PRM" acronym-form="singular+short"}\* finds solutions as fast as [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} for some random sequences of samples, but reaches the time limit before finding any solution for other random sequences. When optimizing obstacle clearance, [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} again outperforms all other tested planners in terms of the above measures. [RRT]{acronym-label="RRT" acronym-form="singular+short"}-Connect and [LBT-RRT]{acronym-label="LBT-RRT" acronym-form="singular+short"} were not tested in this experiment, as their available OMPL implementations do not support goal regions.
:::
::::

# Discussion {#sec:discussion}

The experiments presented in demonstrate the benefits of sampling-based path planning with an asymmetric bidirectional search. This section discusses the results of these experiments, elaborates on the algorithmic differences between [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"}, and presents possible extensions to asymmetric bidirectional algorithms in sampling-based path planning and beyond.

shows the performance of [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"}, [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"}, and eight other sampling-based algorithms on a diverse set of twelve problems optimizing two objectives. When optimizing path length, the experiments show that [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} are competitive to the other tested planners in terms of initial solution times, success rates, and solution quality over time.

When optimizing obstacle clearance, the experiments show that [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} outperforms all other tested asymptotically optimal planners by finding initial solutions faster, reaching 100% success rates sooner, and providing the highest quality solution for most of the time. [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} is often the second-best performing planner on this objective and even competitive to [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} on the robotic arm experiments.

The batch size of [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} was kept constant for all presented experiments, while the performance of [RRT]{acronym-label="RRT" acronym-form="singular+short"}-based planners was tuned to the problem dimension by adjusting the maximum edge length. This shows that [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} can perform well without problem-specific batch sizes but can also motivate future research to investigate advanced batch-size calculations, including variable and adaptive batch sizes.

The experiments presented in keep the collision detection resolution constant within each problem. This resolution determines the false negative collision rate, i.e., the percentage of edges that are considered valid but in reality are not. What is considered an acceptable false negative collision rate depends on the application of the planning algorithm. Experiments not presented in this paper showed that the *relative* performance of [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} compared to other algorithms improves as edge evaluation becomes more computationally expensive, e.g., due to finer collision detection resolution or more complex analysis. This may be because [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} often fully evaluate fewer edges than other algorithms and their performance is therefore not as sensitive to the collision detection resolution. If edge evaluation is computationally inexpensive, e.g., due to coarse collision detection resolution, then the benefits of the accurate heuristics calculated in [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} may not justify the computational cost required to calculate them and other sampling-based planners may perform better in these cases.

Edge evaluation is also computationally expensive for systems with kinodynamic constraints, when full edge evaluation requires solving a two-point [BVP]{acronym-label="BVP" acronym-form="singular+short"}. The accurate heuristics calculated by [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} can reduce the number of [BVPs]{acronym-label="BVP" acronym-form="plural+short"} solved, but [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} require exact solutions to the [BVPs]{acronym-label="BVP" acronym-form="plural+short"}. Other almost-surely asymptotically optimal algorithms do not require exact [BVP]{acronym-label="BVP" acronym-form="singular+short"} solutions even for problems with kinodynamic constraints [@li_ijrr2016; @hauser_tro2016; @kleinbort_icra2020; @shome_icra2021].

[AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} use different algorithms for the reverse and forward searches of their asymmetric bidirectional search (Table [\[tbl:forward-and-reverse-searches\]](#tbl:forward-and-reverse-searches){reference-type="ref" reference="tbl:forward-and-reverse-searches"}). The change in forward search algorithms from A\* in [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} to [AEES]{acronym-label="AEES" acronym-form="singular+short"} in [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} is motivated by the benefits of effort heuristics, which cannot be exploited with A\*, and justify the computational overhead induced by the increased complexity of [AEES]{acronym-label="AEES" acronym-form="singular+short"}. The change in reverse search algorithms from [LPA\*]{acronym-label="LPA*" acronym-form="singular+short"} in [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} to A\* in [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} is motivated by the observations that repairing the reverse search tree with [LPA\*]{acronym-label="LPA*" acronym-form="singular+short"} is only more efficient than restarting A\* for small changes in the search tree [between 1% and 2%; Table 1, @aine_ai2016], and that detecting invalid edges with the forward search often results in larger changes in the reverse search tree. Implementing increasingly dense collision detection in an [LPA\*]{acronym-label="LPA*" acronym-form="singular+short"} reverse search would additionally require either further bookkeeping to keep track of which portion of the tree was checked with which resolution or result in duplicated collision detection effort on some of the edges.

The presented asymmetric bidirectional approach in which two searches inform each other with complementary information can potentially be beneficial in all problem domains where full edge evaluation is computationally expensive, e.g., because of computationally expensive true edge cost computation or complex collision detection. If this edge cost computation can inexpensively be approximated by a heuristic, then the reverse search can combine such heuristics between multiple states into more accurate heuristics between each state and the goal, similar to [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"}.

# Conclusion {#sec:conclusion}

Informed path planning algorithms can use problem-specific knowledge in the form of heuristics to improve their performance, but selecting appropriate heuristics is difficult. This is because heuristics are most effective when they are both accurate and computationally inexpensive to evaluate, which are often conflicting characteristics. Many informed planners additionally can only use problem-specific knowledge if it is expressible as admissible heuristics, which is not always possible for all optimization objectives.

This paper presents two almost-surely asymptotically optimal path planning algorithms that address these challenges by using asymmetric bidirectional searches that simultaneously calculate and exploit accurate, problem-specific heuristics. [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} uses an inexpensive reverse search to combine admissible *a priori* cost heuristics between two states into a more accurate but still admissible cost heuristic between each state and the goal. This heuristic is exploited to make [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"}'s forward search more efficient and repaired whenever the forward search detects that it uses invalid edges. In this way, information is passed between both directions of the bidirectional search, as each search informs the other.

[EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} builds on [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} by additionally calculating inadmissible cost and effort heuristics with its reverse search. This additional knowledge about the computational effort to validate a path can be calculated for any optimization objective and exploited by [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"}'s forward search to order its search in a solution-oriented manner. This improves anytime performance when the cost of a path does not correlate well with the computational effort required to validate it and allows [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} to find initial solutions quickly, even if an admissible cost heuristic is not available for an optimization objective.

The benefits of simultaneously calculating and exploiting ever more accurate heuristics through an asymmetric bidirectional search are demonstrated on twelve diverse problems in abstract, robotic, and biomedical domains. [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} outperforms all other tested asymptotically optimal planners when optimizing obstacle clearance and performs competitively when optimizing path length. [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} is often the second best performing asymptotically optimal planner when optimizing obstacle clearance and also performs competitively when optimizing path length.

Information on the [OMPL]{acronym-label="OMPL" acronym-form="singular+short"} implementations of [AIT\*]{acronym-label="AIT*" acronym-form="singular+short"} and [EIT\*]{acronym-label="EIT*" acronym-form="singular+short"} as well as the software framework for running the experiments and creating the corresponding plots will be available at <https://robotic-esp.com/code/>.

# Acknowledgments {#sec:acknowledgements}

This research was funded by UK Research and Innovation and EPSRC through Robotics and Artificial Intelligence for Nuclear (RAIN) \[EP/R026084/1\] and ACE-OPS: From Autonomy to Cognitive assistance in Emergency OPerationS \[EP/S030832/1\]. We thank Irene Yang and Stephen J. Mellon for discussions and guidance regarding medial dislocations of the Oxford Domed Lateral [UKR]{acronym-label="UKR" acronym-form="singular+short"} implant. We also thank the editorial board for considering this manuscript and our reviewers for their time and constructive criticism.

::: appendices
# Multimedia Extensions {#sec:multimedia-extensions}

A YouTube playlist that complements this article can be found at [`https://youtube.com/playlist?list= PLbaQBz4TuPczfN6PN6NkfmlnXpcf79Aq_`](https://youtube.com/playlist?list=PLbaQBz4TuPczfN6PN6NkfmlnXpcf79Aq_).

    Extension Type    Description
  ----------- ------- --------------------------------------------------------------------------
            1 Video   AIT\* compared to RRT\*, FMT\*, and BIT\*, optimizing path length
            2 Video   EIT\* compared to RRT\*, BIT\*, and AIT\*, optimizing obstacle clearance

  : Index to multimedia extensions.
:::

[^1]: ${}^{1}$Using [OMPL]{acronym-label="OMPL" acronym-form="singular+short"} v1.5.0 on a laptop with 16 GB of RAM and an Intel i7-4910MQ (2.9 GHz) processor running Ubuntu 18.04

[^2]: ${}^{2}$This experiment used an approximation of the Oxford Domed Lateral [UKR]{acronym-label="UKR" acronym-form="singular+long"} due to copyright restrictions.
