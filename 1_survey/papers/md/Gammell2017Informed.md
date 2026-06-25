---
citation_key: Gammell2017Informed
arxiv_id: 1706.06454
arxiv_url: https://arxiv.org/abs/1706.06454
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T17:02:55Z
origin: ai+web
reviewed: false
---

::: acronym
\[T-RO\]IEEE Transactions on Robotics

\[DOFs\]degrees-of-freedom

\[FOVs\]fields of view

\[i.i.d.\]independent and identically distributed \[a.a.s.\]asymptotically almost-surely \[2-pt BVP\]two-point [BVP]{acronym-label="BVP" acronym-form="singular+long"}

\[VT&R\]visual teach and repeat

\[AD\*\]Anytime D∗ \[ADA\*\]Anytime Dynamic A\* \[ARA\*\]Anytime Repairing A\* \[BIT\*\]Batch Informed Trees \[BIT\*\]Batch Informed Trees \[RABIT\*\]Regionally Accelerated [BITstar]{acronym-label="BITstar" acronym-form="singular+abbrv"} \[C-FOREST\]Coupled Forest of Random Engrafting Search Trees \[D\*\]Dynamic A∗ \[EST\]Expansive Space Trees \[FMT\*\]Fast Marching Tree \[FMT\*\]Fast Marching Trees \[LBT-RRT\]Lower Bound Tree [RRT]{acronym-label="RRT" acronym-form="singular+abbrv"} \[LPA\*\]Lifelong Planning A\* \[MDPs\]Markov decision processes \[NRPs\]networks of reusable paths \[POMDPs\]partially-observable Markov decision processes \[PRM\]Probabilistic Roadmaps \[PRM\*\]asymptotically optimal [PRM]{acronym-label="PRM" acronym-form="singular+abbrv"} \[PRM\*\]asymptotically optimal [PRMs]{acronym-label="PRM" acronym-form="plural+abbrv"} \[RA\*\]Randomized A\* \[RRG\]Rapidly exploring Random Graphs \[RRT\]Rapidly-exploring Random Trees \[RRT\*\]asymptotically optimal [RRT]{acronym-label="RRT" acronym-form="singular+abbrv"} \[RRT\*\]asymptotically optimal [RRTs]{acronym-label="RRT" acronym-form="plural+abbrv"} \[SBA\*\]Sampling-based A\* \[s-PRM\]simplified [PRM]{acronym-label="PRM" acronym-form="singular+abbrv"} \[sPRM\]simplified [PRMs]{acronym-label="PRM" acronym-form="plural+abbrv"} \[T-RRT\]Transition-based [RRT]{acronym-label="RRT" acronym-form="singular+abbrv"} \[T-RRT\*\]Transition-based [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} \[AT-RRT\]Anytime Transition-based [RRT]{acronym-label="RRT" acronym-form="singular+abbrv"}
:::

GAMMELL *ET AL.* : INFORMED SAMPLING FOR ASYMPTOTICALLY OPTIMAL PATH PLANNING (CONSOLIDATED VERSION)

::: IEEEkeywords
path planning, sampling-based planning, optimal path planning, informed sampling.
:::

# Introduction

are many powerful path planning techniques in robotics. Popular approaches include graph-based searches, such as Dijkstra's algorithm [@dijkstra_59] and A\* [@hart_tssc68], and sampling-based methods, such as [PRMs]{acronym-label="PRM" acronym-form="plural+short"} [@kavraki_tro96], [ESTs]{acronym-label="EST" acronym-form="plural+short"} [@hsu_ijrr02], and [RRTs]{acronym-label="RRT" acronym-form="plural+short"} [@lavalle_ijrr01]. While sampling-based methods avoid the challenges of *a priori* discretizations, their stochastic nature limits their formal performance. They are said to be *probabilistically complete* if the probability of finding a solution, if one exists, approaches unity with an infinite number of samples. They are also said to be *almost-surely asymptotically optimal* if the probability of converging asymptotically to the optimum, if one exists, approaches unity with an infinite number of samples (e.g., [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} [@karaman_ijrr11]).

:::: {#fig:intro:infsets .figure latex-placement="tb"}
![](Gammell2017Informed_figs/shrinking_sets_small.png){width="\\columnwidth"}

::: caption
An illustration of how the set of states that can improve solution length shrinks as better solutions are found. Common estimates of this *omniscient set* are illustrated as *informed sets*. The $L^2$ informed set always contains the entire omniscient set (i.e., $100\%$ recall) and shrinks along with it as a function of the current solution (i.e., high precision). It is exactly equal to the omniscient set in the absence of obstacles and constraints (i.e., $100\%$ recall *and* precision). This paper shows that direct sampling this $L^2$ informed set is a necessary condition for almost-surely asymptotically optimal planners to scale effectively to high state dimensions. This technique is demonstrated with Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"}.
:::
::::

[RRT]{acronym-label="RRT" acronym-form="singular+abbrv"} searches a planning problem by incrementally building a tree through free space. [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} extends this procedure to incrementally rewire the tree during its construction. This rewiring locally optimizes *every* vertex in the tree and allows the algorithm to almost-surely converge asymptotically to the optimal path to *every state* in the problem domain. This is an inefficient way to find the optimal solution to a single planning query.

The only states that need to be considered in single-query scenarios are those that can provide a better solution [@ferguson_iros06]. While exact knowledge of these states requires solving the planning problem, they can often be approximated with heuristics (Fig. [1](#fig:intro:infsets){reference-type="ref" reference="fig:intro:infsets"}). These heuristics have previously been used to focus almost-surely asymptotically optimal search [@akgun_iros11; @otte_tro13] but can also provide insight into the optimal planning problem.

This paper uses the set of states that can provide a better solution to analyze incremental almost-surely asymptotically optimal planning. It formally defines this shrinking set as the *omniscient set* and shows that sampling it is a necessary condition for [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"}-style planners to improve a solution. It defines estimates of this set as *informed sets* and provides metrics to quantify them in terms of their compactness (i.e., *precision*) and completeness (i.e., *recall*). It uses these results to bound the probability of improving a solution to a holonomic planning problem by the probability of sampling an informed set with $100\%$ recall.

The $L^2$ norm (i.e., Euclidean distance) is a well-known heuristic for problems seeking to minimize path length. It describes the omniscient set exactly in the absence of obstacles

and constraints (i.e., it is *sharp*) and always contains the omniscient set of a problem (i.e., it is *universally admissible*). This paper uses it to analyze the minimum-path-length problem and shows that existing focusing techniques (e.g., [@akgun_iros11; @otte_tro13]) are ineffective in high state dimensions. It is proven that these rejection-sampling approaches have a probability of improving a solution that goes to zero *factorially* (i.e., faster than exponentially) as state dimension increases.

This paper demonstrates how this minimum-path-length *curse of dimensionality* can be reduced by directly sampling the symmetric $n$-dimensional ellipse (i.e., prolate hyperspheroid), the $L^2$ informed set. The presented direct sampling approach always finds states that are believed to belong to a better solution regardless of the relative size of the $L^2$ informed set. It outperforms existing focusing techniques by orders of magnitude as state dimension increases.

The informed search approach is demonstrated with Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"}. This extension of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} uses direct informed sampling and admissible graph pruning to focus the search for improvements. It is shown analytically to outperform existing techniques in terms of convergence rate, especially in high state dimensions, and to result in linear convergence on some problems. It is probabilistically complete and almost-surely asymptotically optimal. When the $L^2$ heuristic does not provide additional information (e.g., small planning problems and/or large informed sets) it is identical to [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}. A version of Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} is publicly available in the [OMPL]{acronym-label="OMPL" acronym-form="singular+full"} [@ompl].

Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} is evaluated experimentally on abstract problems and on the [CMU]{acronym-label="CMU" acronym-form="singular+abbrv"} Personal Robotic Lab's [HERB]{acronym-label="HERB" acronym-form="singular+short"} [@herb], a 14-[DOF]{acronym-label="DOF" acronym-form="singular+short"} mobile manipulation platform. These experiments show that it outperforms existing focusing techniques as state dimension increases, especially in problems with large planning domains.

This paper is organized as follows. Section [2](#sec:omni_inf){reference-type="ref" reference="sec:omni_inf"} defines omniscient and informed sets and their associated precision and recall in preparation for the literature review presented in Section [3](#sec:lit){reference-type="ref" reference="sec:lit"}. Section [4](#sec:l2){reference-type="ref" reference="sec:l2"} presents a direct informed sampling technique for problems seeking to minimize path length which is demonstrated with Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} in Section [5](#sec:inf){reference-type="ref" reference="sec:inf"}. Section [6](#sec:rate){reference-type="ref" reference="sec:rate"} analyzes the expected convergence rate of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} algorithms and Section [7](#sec:exp){reference-type="ref" reference="sec:exp"} demonstrates the practical advantages of this improvement on abstract and simulated problems. Section [8](#sec:fin){reference-type="ref" reference="sec:fin"} finally presents a closing discussion and thoughts on future work.

## Statement of Contributions

This paper is a continuation of ideas first published in [@gammell_iros14] and associated technical reports [@gammell_arxiv14; @gammell_arxiv14b] and makes the following specific contributions:

- Formally defines omniscient and informed sets (Definitions [3](#defn:omni){reference-type="ref" reference="defn:omni"} and [7](#defn:informed){reference-type="ref" reference="defn:informed"}) and demonstrates how precision and recall can be used to quantify the performance of informed sampling (Definitions [8](#defn:precision){reference-type="ref" reference="defn:precision"} and [9](#defn:recall){reference-type="ref" reference="defn:recall"}).

- Provides upper bounds on the probability that an incremental sampling-based planner improves a solution to a holonomic planning problem (Theorems [6](#thm:necessary:exact:prob){reference-type="ref" reference="thm:necessary:exact:prob"} and [13](#thm:necessary:heuristic:prob){reference-type="ref" reference="thm:necessary:heuristic:prob"}).

- Bounds the expected next-iteration cost for [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} algorithms on any minimum-path-length planning problem (Lemma [17](#lem:conv:expect){reference-type="ref" reference="lem:conv:expect"}) and shows that existing formulations of these algorithms for holonomic planning have a probability of improving a solution that decreases factorially with state dimension (Theorem [14](#thm:curse){reference-type="ref" reference="thm:curse"}).

- Develops a method to reduce this minimum-path-length curse of dimensionality by directly sampling the ellipsoidal $L^2$ informed set defined by a goal or *countable set of goals* and the current solution (Algs. [\[algo:infset\]](#algo:infset){reference-type="ref" reference="algo:infset"}--[\[algo:randomKeep\]](#algo:randomKeep){reference-type="ref" reference="algo:randomKeep"}).

- Proves that a planning algorithm using this approach, Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"}, has better theoretical convergence (Theorems [18](#thm:conv:rrtstar){reference-type="ref" reference="thm:conv:rrtstar"}--[20](#thm:conv:informed){reference-type="ref" reference="thm:conv:informed"}) and experimental performance than existing focused planning algorithms on holonomic problems.

# Omniscient and Informed Sets {#sec:omni_inf}

A formal discussion of the optimal planning problem is presented in support of the literature review. It includes definitions of the states that can provide a better solution, the *omniscient set* (Definition [3](#defn:omni){reference-type="ref" reference="defn:omni"}), and estimates of this set, *informed sets*, quantified by *precision* and *recall* (Definitions [7](#defn:informed){reference-type="ref" reference="defn:informed"}--[10](#defn:admissible){reference-type="ref" reference="defn:admissible"}). These sets provide theoretical upper bounds on the probability of improving a solution to a holonomic problem that are used throughout the remainder of the paper (Theorems [6](#thm:necessary:exact:prob){reference-type="ref" reference="thm:necessary:exact:prob"} and [13](#thm:necessary:heuristic:prob){reference-type="ref" reference="thm:necessary:heuristic:prob"}).

Finding the optimal path from a start to a goal is formally defined as the optimal planning problem (Definition [1](#defn:opt){reference-type="ref" reference="defn:opt"}). The given definition is similar to [@karaman_ijrr11].

::: {#defn:opt .defn}
**Definition 1** (Optimal planning). *Let $X\subseteq \mathbb{R}^n$ be the state space of the planning problem, $X_{\rm obs}\subset X$ be the states in collision with obstacles, and $X_{\rm free}= \mathrm{cl}\left(X\setminus X_{\rm obs}\right)$ be the resulting set of permissible states, where $\mathrm{cl}\left(\cdot\right)$ represents the closure of a set. Let $\mathbf{x}_{\rm start}\in X_{\rm free}$ be the initial state and $X_{\rm goal}\subset X_{\rm free}$ be the set of desired goal states. Let $\sigma: \; \left[0,1\right] \to X_{\rm free}$ be a sequence of states through collision-free space that can be executed by the robot (i.e., a collision-free feasible path) and $\Sigma$ be the set of all such nontrivial paths.*

*The optimal planning problem is then formally defined as the search for a path, $\sigma^{*}\in\Sigma$, that minimizes a given cost function, $c: \; \Sigma\to \mathbb{R}_{\geq 0}$, while connecting $\mathbf{x}_{\rm start}$ to $\mathbf{x}_{\rm goal}\in X_{\rm goal}$, $$\begin{equation*}
        \sigma^{*}= \mathop{\mathrm{arg\,min}}_{\sigma\in \Sigma} \left\lbrace c\left(\sigma\right)\;\;\middle|\;\;\sigma\left(0\right) = \mathbf{x}_{\rm start},\, \sigma\left(1\right) \in X_{\rm goal}\right\rbrace,
\end{equation*}$$ where $\mathbb{R}_{\geq 0}$ is the set of non-negative real numbers.*
:::

Many sampling-based planners, such as [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}, probabilistically converge towards the optimum of these problems. Such planners are described as probabilistically complete and almost-surely asymptotically optimal (Definition [2](#defn:asao){reference-type="ref" reference="defn:asao"}).

::: {#defn:asao .defn}
**Definition 2** (Almost-sure asymptotic optimality). *A planner is said to be almost-surely asymptotically optimal if, with an infinite number of samples, the probability of converging asymptotically to the optimum (Definition [1](#defn:opt){reference-type="ref" reference="defn:opt"}), if one exists, is one, $$\begin{equation*}
        P\left(\limsup_{q\to \infty}c\left(\sigma_q\right) = c\left(\sigma^{*}\right)\right) = 1,
\end{equation*}$$ where $q$ is the number of samples, $\sigma_q$ is the path found by the planner from those samples, $\sigma^{*}$ is the optimal solution to the planning problem, and $c\left(\cdot\right)$ is the cost of a path.*
:::

Once *any* solution is found, the set of states that can provide a *better* solution can be defined as the omniscient set (Definition [3](#defn:omni){reference-type="ref" reference="defn:omni"}).

::: {#defn:omni .defn}
**Definition 3** (Omniscient set). *Let $g\left(\mathbf{x}\right)$ be the cost of the optimal path from the start to a state, $\mathbf{x}\in X_{\rm free}$, the *optimal cost-to-come*, $$\begin{equation*}
        g\left(\mathbf{x}\right) \coloneqq \min_{\sigma\in \Sigma} \left\lbrace c\left(\sigma\right)\;\;\middle|\;\;\sigma(0) = \mathbf{x}_{\rm start},\, \sigma(1) = \mathbf{x}\right\rbrace,
\end{equation*}$$ and $h\left(\mathbf{x}\right)$ be the cost of the optimal path from $\mathbf{x}$ to the goal region, the *optimal cost-to-go*, $$\begin{equation*}
        h\left(\mathbf{x}\right) \coloneqq \min_{\sigma\in \Sigma} \left\lbrace c\left(\sigma\right)\;\;\middle|\;\;\sigma(0) = \mathbf{x},\, \sigma(1) \in X_{\rm goal}\right\rbrace.
\end{equation*}$$ The cost of the optimal path from $\mathbf{x}_{\rm start}$ to $X_{\rm goal}$ constrained to pass through $\mathbf{x}$ is then given by $f\left(\mathbf{x}\right) \coloneqq g\left(\mathbf{x}\right) + h\left(\mathbf{x}\right)$. This defines the subset of states that can belong to a solution better than the current solution, $c_{i}$, as $$\begin{equation}
\label{eqn:fset}
        X_{f}\coloneqq \left\lbrace \mathbf{x}\in X_{\rm free}\;\;\middle|\;\;f\left(\mathbf{x}\right) < c_{i}\right\rbrace.
\end{equation}$$ Exact knowledge of $X_{f}$ requires exact knowledge of the entire planning problem so we refer to it as the *omniscient set*.*
:::

:::: {#fig:rrtstar:all .figure latex-placement="tb"}
![](Gammell2017Informed_figs/rrtstarConverge_small.png){width="\\columnwidth"}

::: caption
An example of how [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} almost-surely converges asymptotically to the optimum by incrementally building and rewiring a tree through the *entire* problem domain. [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} incrementally expands the tree into the problem domain and improve its connections. By continuing this process indefinitely, it almost-surely converges asymptotically to the optimal solution by asymptotically improving every path in the tree. This is inefficient in single-query planning scenarios.
:::
::::

[RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} builds a tree by incrementally adding states from the problem domain (Fig. [2](#fig:rrtstar:all){reference-type="ref" reference="fig:rrtstar:all"}). A necessary condition for it to improve a solution is that the newly added state belongs to the omniscient set (Lemma [4](#lem:necessary:exact){reference-type="ref" reference="lem:necessary:exact"}).

::: {#lem:necessary:exact .lem}
**Lemma 4** (The necessity of adding states in the omniscient set). *Adding a state from the omniscient set, $\mathbf{x}_{\rm new}\in X_{f}$, is a necessary condition for [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} to improve the current solution, $c_{i}$, $$\begin{equation*}
        c_{i+1}< c_{i}\implies \mathbf{x}_{\rm new}\in X_{f}.
\end{equation*}$$*

*This condition is necessary but not *sufficient* to improve the solution as the ability of states in $X_{f}$ to provide better solutions at any iteration depends on the structure of the tree (i.e., its optimality).*
:::

::: proof
*Proof.* The proof of Lemma [4](#lem:necessary:exact){reference-type="ref" reference="lem:necessary:exact"} from the supplementary online material appears in Appendix [9.1](#appx:necessary:exact){reference-type="ref" reference="appx:necessary:exact"}. ◻
:::

The state added by [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} at each iteration, $\mathbf{x}_{\rm new}$, is generated from a randomly sampled state, $\mathbf{x}_{\rm rand}$, and the nearest vertex in the existing tree, $$\begin{equation}
\label{eqn:back:nearest}
    \mathbf{v}_{\rm nearest}\coloneqq \mathop{\mathrm{arg\,min}}_{\mathbf{v}\in V}\left\lbrace  \left\| \mathbf{x}_{\rm rand}- \mathbf{v} \right\|_{2} \right\rbrace,
\end{equation}$$ through expansion and differential constraints (i.e., the $\mathtt{Steer}$ function). Absent any constraints (i.e., in holonomic planning) this takes the form $$\begin{equation}
\label{eqn:back:steer}
%
    \mathbf{x}_{\rm new}\coloneqq \mathop{\mathrm{arg\,min}}_{\mathbf{y}\in X}\left\lbrace \left\| \mathbf{x}_{\rm rand}- \mathbf{y} \right\|_{2}\;\;\middle|\;\;\left\| \mathbf{y}- \mathbf{v}_{\rm nearest} \right\|_{2} \leq \eta\right\rbrace,
\end{equation}$$ where $\eta$ is a user-selected maximum edge length.

The number of tree vertices in the problem domain increases indefinitely with [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} iterations. With an infinite number of iterations, eventually all reachable states will be no more than $\eta$ away from the nearest vertex in the tree. After these $\kappa$ iterations, *sampling* the omniscient set is a necessary condition to add a state from the omniscient set and improve the solution (Lemma [5](#lem:necessary:exact:sample){reference-type="ref" reference="lem:necessary:exact:sample"}).

::: {#lem:necessary:exact:sample .lem}
**Lemma 5** (The necessity of sampling states in the omniscient set in holonomic planning). *Sampling the omniscient set, $\mathbf{x}_{\rm rand}\in X_{f}$, is a necessary condition for [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} to improve the current solution to a holonomic problem, $c_{i}$, after an initial $\kappa$ iterations, $$\begin{equation*}
        \forall i\geq \kappa,\, c_{i+1}< c_{i}\implies \mathbf{x}_{\rm rand}\in X_{f},
\end{equation*}$$ for any sample distribution that maintains a nonzero probability over the entire omniscient set.*

*For simplicity, this statement is limited to holonomic planning but it can be extended to specific constraints with appropriate assumptions.*
:::

::: proof
*Proof.* The proof of Lemma [5](#lem:necessary:exact:sample){reference-type="ref" reference="lem:necessary:exact:sample"} from the supplementary online material appears in Appendix [9.2](#appx:necessary:sample){reference-type="ref" reference="appx:necessary:sample"}. ◻
:::

This result provides an upper limit on the probability of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} improving a solution at any iteration (Theorem [6](#thm:necessary:exact:prob){reference-type="ref" reference="thm:necessary:exact:prob"}).

::: {#thm:necessary:exact:prob .thm}
**Theorem 6** (An upper bound on the probability of improving a solution to a holonomic planning problem given knowledge of the omniscient set). *The probability that an iteration of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} improves the current solution to a holonomic problem, $c_{i}$, is bounded by the probability of sampling the omniscient set, $X_{f}$, $$\begin{equation*}
        \forall i\geq \kappa,\, P\left(c_{i+1}<c_{i}\right) \leq P\left(\mathbf{x}_{\rm rand}\in X_{f}\right),
\end{equation*}$$ for any iteration, $i$, after a sufficient vertex density is achieved in the initial $\kappa$ iterations.*

*For simplicity, this statement is limited to holonomic planning but it can be extended to specific constraints by expanding Lemma [5](#lem:necessary:exact:sample){reference-type="ref" reference="lem:necessary:exact:sample"}.*
:::

::: proof
*Proof.* Proof of Theorem [6](#thm:necessary:exact:prob){reference-type="ref" reference="thm:necessary:exact:prob"} follows directly from Lemma [5](#lem:necessary:exact:sample){reference-type="ref" reference="lem:necessary:exact:sample"}. Sampling a state in $X_{f}$ is a necessary but not sufficient condition to improve the solution after $\kappa$ iterations; therefore, the probability of sampling such a state bounds the probability of improving the solution. ◻
:::

Knowledge of an omniscient set requires solving the planning problem; however, these results can be extended to estimates of the omniscient set defined by solution cost heuristics (Definition [7](#defn:informed){reference-type="ref" reference="defn:informed"}).

::: {#defn:informed .defn}
**Definition 7** (Informed set). *Let $\widehat{f}\left(\mathbf{x}\right)$ represent a heuristic estimate of the solution cost constrained to go through a state, $\mathbf{x}\in X$. A heuristic estimate of the omniscient set can then be defined as $$\begin{equation*}
        X_{\widehat{f}}\coloneqq \left\lbrace \mathbf{x}\in X\;\;\middle|\;\;\widehat{f}\left(\mathbf{x}\right) < c_{i}\right\rbrace.
\end{equation*}$$ Such a set will be referred to as an *informed set*.*
:::

There are an infinite number of potential informed sets for any planning problem and choosing the 'best' set requires methods to quantify their performance. In binary classification, estimates are evaluated in terms of their precision and recall (Fig. [3](#fig:pr){reference-type="ref" reference="fig:pr"}). Analogue terms can be defined in sampling-based planning to quantify the ability of informed sets to estimate the omniscient set (Definitions [8](#defn:precision){reference-type="ref" reference="defn:precision"} and [9](#defn:recall){reference-type="ref" reference="defn:recall"}).

::: {#defn:precision .defn}
**Definition 8** (Precision). *The precision of an informed sampling technique is the probability that random samples drawn from the informed set could also be drawn from the omniscient set (e.g., the percentage of states drawn from the informed set, $X_{\widehat{f}}$, that belong to the omniscient set, $X_{f}$). For uniform sampling of an informed set, this is a ratio of measures, $$\begin{equation*}
        \mathrm{Precision}\left(X_{\widehat{f}}\right) \coloneqq \frac{\lambda\left(X_{\widehat{f}}\cap X_{f}\right)}{\lambda\left(X_{\widehat{f}}\right)}.
\end{equation*}$$ Any informed set with nonzero sampling probability that is a *subset* of the omniscient set will have $100\%$ precision.*
:::

::: {#defn:recall .defn}
**Definition 9** (Recall). *The recall of an informed sampling technique is the probability that random states drawn from the omniscient set could also be sampled from the informed set (e.g., the percentage of states that belong to the omniscient set, $X_{f}$, with a nonzero probability of being sampled from the informed set, $X_{\widehat{f}}$). For uniform sampling of an informed set, this is a ratio of measures, $$\begin{equation*}
        \mathrm{Recall}\left(X_{\widehat{f}}\right) \coloneqq \frac{\lambda\left(X_{\widehat{f}}\cap X_{f}\right)}{\lambda\left(X_{f}\right)}.
\end{equation*}$$ Any informed set with nonzero sampling probability that is a *superset* of the omniscient set will have $100\%$ recall.*
:::

:::: {#fig:pr .figure latex-placement="tb"}
![](Gammell2017Informed_figs/precision_recall.png){width="\\columnwidth"}

::: caption
An illustration of the *precision* and *recall* of estimating an oblong omniscient set, $X_{f}$, with a rectangular informed set, $X_{\widehat{f}}$. The informed set is coloured to highlight where it is correct (light grey) incorrect (dark grey) or missing the omniscient set (white). Precision is the likelihood of correctly sampling the omniscient set by sampling the informed set. Recall is the coverage of the omniscient set by the informed set. For uniform distributions, both these terms are ratios of Lebesgue measures.
:::
::::

Informed sets with $100\%$ recall (Definition [10](#defn:admissible){reference-type="ref" reference="defn:admissible"}) are important in almost-surely asymptotically optimal planning as less-than-perfect recall may exclude the optima to some problems.

::: {#defn:admissible .defn}
**Definition 10** (Admissible informed set). *A heuristic is said to be admissible if it never overestimates the true value of the function, $$\begin{equation*}
        \forall \mathbf{x}\in X, \; \widehat{f}\left(\mathbf{x}\right) \leq f\left(\mathbf{x}\right).
\end{equation*}$$ Any informed set defined by such an admissible heuristic will contain all possibly better solutions and have $100\%$ recall, i.e., $X_{\widehat{f}}\supseteq X_{f}.$*

*This set will be referred to as an *admissible* estimate of the omniscient set, or an *admissible informed set*. If the heuristic is an admissible estimate of the cost function for all possible problems then the set will be referred to as a *universally admissible informed set*.*
:::

These definitions allow the probability of improving a solution to a holonomic problem to be bounded by the probability of sampling any admissible informed set (Lemmas [11](#lem:necessary:heuristic){reference-type="ref" reference="lem:necessary:heuristic"} and [12](#lem:necessary:heuristic:sample){reference-type="ref" reference="lem:necessary:heuristic:sample"} and Theorem [13](#thm:necessary:heuristic:prob){reference-type="ref" reference="thm:necessary:heuristic:prob"}). The tightness of this bound will depend on the precision of the chosen estimate.

::: {#lem:necessary:heuristic .lem}
**Lemma 11** (The necessity of adding states in an admissible informed set). *Adding a state from an admissible informed set, $\mathbf{x}_{\rm new}\in X_{\widehat{f}}\supseteq X_{f}$, is a necessary condition for [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} to improve the current solution, $c_{i}$, $$\begin{equation*}
        c_{i+1}< c_{i}\implies \mathbf{x}_{\rm new}\in X_{\widehat{f}}\supseteq X_{f}.
\end{equation*}$$*
:::

::: proof
*Proof.* Lemma [11](#lem:necessary:heuristic){reference-type="ref" reference="lem:necessary:heuristic"} follows directly from Lemma [4](#lem:necessary:exact){reference-type="ref" reference="lem:necessary:exact"} given that $X_{\widehat{f}}\supseteq X_{f}$. ◻
:::

::: {#lem:necessary:heuristic:sample .lem}
**Lemma 12** (The necessity of sampling states in an admissible informed set in holonomic planning). *Sampling an admissible informed set, $\mathbf{x}_{\rm rand}\in X_{\widehat{f}}\supseteq X_{f}$, is a necessary condition for [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} to improve the current solution to a holonomic problem, $c_{i}$, after an initial $\kappa$ iterations, $$\begin{equation*}
        \forall i\geq \kappa,\, c_{i+1}< c_{i}\implies \mathbf{x}_{\rm rand}\in X_{\widehat{f}}\supseteq X_{f},
\end{equation*}$$ for any sample distribution that maintains a nonzero probability over the entire informed set.*

*For simplicity, this statement is limited to holonomic planning but it can be extended to specific constraints by expanding Lemma [5](#lem:necessary:exact:sample){reference-type="ref" reference="lem:necessary:exact:sample"}.*
:::

::: proof
*Proof.* Lemma [12](#lem:necessary:heuristic:sample){reference-type="ref" reference="lem:necessary:heuristic:sample"} follows directly from Lemma [5](#lem:necessary:exact:sample){reference-type="ref" reference="lem:necessary:exact:sample"} given that $X_{\widehat{f}}\supseteq X_{f}$. ◻
:::

::: {#thm:necessary:heuristic:prob .thm}
**Theorem 13** (An upper bound on the probability of improving a solution to a holonomic planning problem given knowledge of an admissible informed set). *The probability that an iteration of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} improves the current solution to a holonomic problem, $c_{i}$, is bounded by the probability of sampling an admissible informed set, $X_{\widehat{f}}\supseteq X_{f}$, $$\begin{equation*}
        \forall i\geq \kappa,\, P\left(c_{i+1}<c_{i}\right) \leq P\left(\mathbf{x}_{\rm rand}\in X_{f}\right)
                                                              \leq P\left(\mathbf{x}_{\rm rand}\in X_{\widehat{f}}\right),
\end{equation*}$$ for any iteration, $i$, after an initial $\kappa$ iterations.*

*For simplicity, this statement is limited to holonomic planning but it can be extended to specific constraints by expanding Lemma [5](#lem:necessary:exact:sample){reference-type="ref" reference="lem:necessary:exact:sample"}.*
:::

::: proof
*Proof.* Theorem [13](#thm:necessary:heuristic:prob){reference-type="ref" reference="thm:necessary:heuristic:prob"} follows directly from Theorem [6](#thm:necessary:exact:prob){reference-type="ref" reference="thm:necessary:exact:prob"} given that $X_{\widehat{f}}\supseteq X_{f}$. ◻
:::

# Prior Work Accelerating [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} Convergence {#sec:lit}

A review of previous work to improve the convergence rate of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} is presented using the results and terminology of Section [2](#sec:omni_inf){reference-type="ref" reference="sec:omni_inf"}. All these techniques attempt to increase the real-time rate of searching the omniscient set by exploiting additional information. Most can be viewed as versions of sample biasing, sample rejection, and/or graph pruning (Sections [3.1](#sec:lit:bias){reference-type="ref" reference="sec:lit:bias"}--[3.4](#sec:lit:other){reference-type="ref" reference="sec:lit:other"}).

## Sample Biasing {#sec:lit:bias}

Increasing the likelihood of sampling an informed set improves [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} performance. This sample biasing creates a nonuniform sample distribution that will increase exploration of the informed set but invalidates the assumptions used to prove almost-sure asymptotic optimality. One method to maintain these formal performance guarantees is to calculate the [RGG]{acronym-label="RGG" acronym-form="singular+short"} connection limit from a subset of samples that are uniformly distributed [@janson_ijrr15]. This maintains almost-sure asymptotic optimality but increases the required number of rewirings.

It is common to bias sampling around the current solution. This *path biasing* increases the likelihood of sampling a state that can improve the current solution but reduces the likelihood of finding solutions in other homotopy classes (i.e., it increases precision by decreasing recall; Fig [4](#fig:subsets){reference-type="ref" reference="fig:subsets"}a). The ratio of path biasing to global search is frequently a user-chosen parameter that must be tuned for each problem.

Akgun and Stilman [@akgun_iros11] use path biasing in their dual-tree version of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}. Once an initial solution is found the algorithm spends a user-specified percentage of iterations refining the current solution. It does this by explicitly sampling near a randomly selected state on the current path. This increases the probability of improvement at the expense of decreasing the exploration of other homotopy classes. Their algorithm also employs sample rejection in exploring the state space (see Section [3.2](#sec:lit:rej){reference-type="ref" reference="sec:lit:rej"}).

:::: {#fig:subsets .figure latex-placement="tb"}
![](Gammell2017Informed_figs/pr_examples_small.png)

::: caption
A illustration of the precision and recall of informed sampling techniques on the omniscient set depicted in Fig. [1](#fig:intro:infsets){reference-type="ref" reference="fig:intro:infsets"}(b). The informed sets are coloured to highlight where they are correct (light grey), incorrect (dark grey), or missing the omniscient set (white). Path biasing, (a), generally has high precision but low recall, especially in the presence of multiple homotopy classes Global or bounded sampling, (b), generally has full recall but low precision, especially in large relative planning problems or high state dimensions. Direct sampling of the $L^2$ informed set, (c), has full recall and high precision, regardless of the size of the omniscient set and is exactly equal to the omniscient set in the absence of obstacles and constraints.
:::
::::

Nasir et al. [@nasir_ijars13] combine path biasing with smoothing in their [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"}-Smart algorithm. Solution paths are simplified and then used as biases for further sampling around the solution. Their path smoothing rapidly improves the current solution but the path biasing decreases the likelihood of finding a solution in a different homotopy class.

Kiesel et al. [@kiesel_socs12] use a two-stage sampling process in their *f-biasing* technique. Samples are generated by randomly selecting a region of the planning problem and then uniformly sampling it. The probability of selecting a region is calculated by solving a simple discretization of the planning problem with Dijkstra's algorithm [@dijkstra_59]. The regions along the discrete solution are given a higher selection probability but all regions maintain a nonzero probability to compensate for the incompleteness of the discretization. This technique provides a sampling bias for the entire [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} search but once a solution is found it continues to sample states that cannot provide a better solution. It is stated that almost-sure asymptotic optimality is maintained but it is not discussed how to modify the rewiring neighbourhood to do so.

Kim et al. [@kim_icra14] also use a two-stage sampling process in their Cloud [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} algorithm. They generate uniform samples from a series of collision-free, possibly overlapping, spheres defined by a [GVG]{acronym-label="GVG" acronym-form="singular+long"} [@choset_icra95]. New spheres are added on solution paths and the probability of selecting them is updated so that samples from the homotopy class of the solution are biased around the path while maintaining the probability of sampling other homotopy classes. Cloud [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} successfully finds better solutions faster than other algorithms but continues to sample states that cannot improve the solution and its effect on almost-sure asymptotic optimality is not discussed.

Unlike sample biasing methods, the direct informed sampling used by Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} does not consider states that are known to be unable to improve a solution. It does result in a nonuniform sample distribution over the problem domain but it is still almost-surely asymptotically optimal as it has a uniform distribution in the informed set being searched.

## Sample Rejection {#sec:lit:rej}

Ignoring samples outside an informed set improves [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} performance. This sample rejection decreases the computational cost of states that cannot improve a solution but does not increase the probability of finding ones that can. If this probability is low (i.e., if the informed set is small relative to the sampling domain) then convergence will not be improved (Fig. [4](#fig:subsets){reference-type="ref" reference="fig:subsets"}b). It is shown that this probability decreases factorially with state dimension (i.e., faster than exponentially) in existing formulations of the holonomic minimum-path-length problem (Theorem [14](#thm:curse){reference-type="ref" reference="thm:curse"}).

Akgun and Stilman [@akgun_iros11] use global rejection sampling in addition to sample biasing in their dual-tree algorithm. As samples are drawn from the entire problem domain, performance will decrease rapidly as the solution improves and/or in large or high-dimensional planning problems.

Otte and Correll [@otte_tro13] use adaptive rejection sampling in their parallelized [CFOREST]{acronym-label="CFOREST" acronym-form="singular+short"} algorithm. Samples are generated from a rectangular subset of the planning domain that bounds the ellipsoidal $L^2$ informed set and rejected using the $L^2$ heuristic. This increases sampling precision and improves performance in large planning problems but its effectiveness still decreases factorially with state dimension (Theorem [14](#thm:curse){reference-type="ref" reference="thm:curse"}).

Unlike sample rejection methods, the direct informed sampling used by Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} maintains high precision and $100\%$ recall regardless of the relative sizes of the informed set and problem domain. It focuses its search in response to solution improvements and does not decrease in effectiveness in large planning domains. It scales more effectively than existing approaches to high-dimensional planning problems

## Graph Pruning {#sec:lit:prune}

Limiting the tree to an informed set improves [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} performance. This graph pruning removes states that can no longer improve the existing solution and reduces the computational cost of basic operations (e.g., nearest neighbour searches). It can also be used reject potential new states given their connection and any constraints, e.g., [\[eqn:back:steer\]](#eqn:back:steer){reference-type="eqref" reference="eqn:back:steer"}. After a sufficient number of iterations, this incremental pruning is equivalent in holonomic planning to rejection sampling with the same heuristic (Lemma [12](#lem:necessary:heuristic:sample){reference-type="ref" reference="lem:necessary:heuristic:sample"}) but with the additional computational costs of expanding towards the sample.

Karaman et al. [@karaman_icra11] use graph pruning to implement an online version of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} that improves solutions during path execution. They remove vertices whose *current* cost-to-come plus a heuristic estimate of cost-to-go is higher than the current solution. As current cost-to-come overestimates a vertex's optimal cost-to-come (i.e., it is an inadmissible heuristic), this approach may erroneously remove vertices that could provide a better solution.

Arslan and Tsiotras [@arslan_icra13; @arslan_icra15] combine incremental graph-pruning and incremental graph search techniques with [RRGs]{acronym-label="RRG" acronym-form="plural+short"} [@karaman_ijrr11] to reject samples in their [RRT]{acronym-label="RRT" acronym-form="singular+abbrv"}^\#^ algorithm. This incremental pruning focuses the search but its performance will also decrease rapidly as the solution improves or when used on large or high-dimensional planning problems. Some of the rejection criteria also use the current cost-to-come of vertices and may reject samples that could later improve the solution.

Unlike rejecting states with incremental graph pruning, the direct informed sampling used by Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} wastes no computational effort on states that are known to be unable to improve the solution. Its admissible graph pruning algorithm to remove unnecessary states also only removes vertices from the tree if doing so does not negatively affect the search.

## Other Techniques {#sec:lit:other}

Some techniques to improve [RRT]{acronym-label="RRT" acronym-form="singular+abbrv"}/[RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} performance do not fit neatly into the previous categories. Many of these methods could be further accelerated through direct informed sampling.

Urmson and Simmons [@urmson_iros03] uses rejection sampling to create a "probabilistic implementation of heuristic search concepts" in their [hRRT]{acronym-label="hRRT" acronym-form="singular+short"}. At each iteration, a uniformly distributed sample is probabilistically kept or rejected as a function of its heuristic value relative to the existing tree. This iteratively biases [RRT]{acronym-label="RRT" acronym-form="singular+short"} expansion towards regions of the problem domain believed to contain high-quality solutions and often finds better solutions than [RRT]{acronym-label="RRT" acronym-form="singular+short"}, especially on problems with continuous cost functions (e.g., path length [@urmson_iros03]); however, it results in nonuniform sample distributions.

Ferguson and Stentz [@ferguson_iros06] recognize that an existing solution defines the set of states that could provide better solutions. Their Anytime [RRTs]{acronym-label="RRT" acronym-form="plural+abbrv"}s algorithm attempts to incrementally find better solutions by searching a decreasing series of these ellipses. This shrinking search ignores some expensive solutions but does not guarantee better ones will be found.

Alterovitz et al. [@alterovitz_icra11] add path refinement to [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} in their [RRM]{acronym-label="RRM" acronym-form="singular+short"} algorithm. Once an initial solution is found, each iteration of [RRM]{acronym-label="RRM" acronym-form="singular+short"} either samples a new state or selects an existing state from the current solution and refines it. Path refinement connects the selected state to its neighbours and results in a graph instead of a tree. The ratio of refinement to exploration is a user-tuned parameter.

Shan et al. [@shan_iv14] find an initial solution with [RRT]{acronym-label="RRT" acronym-form="singular+short"}, simplify and rewire it using their [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}\_S algorithm, and then continue the search with [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}. This can find better solutions faster than [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} alone but the resulting search is not focused and continues to consider states that cannot provide better solutions.

Salzman and Halperin [@salzman_icra14] relax performance to asymptotic *near* optimality in their [LBTRRT]{acronym-label="LBTRRT" acronym-form="singular+short"}. Rewirings are only considered if they are required to maintain the desired tolerance to the optimum. This can reduce computational complexity but does not focus the search.

Devaurs et al. [@devaurs_afr15] use ideas from stochastic optimization to explore complex cost functions in their [TRRTstar]{acronym-label="TRRTstar" acronym-form="singular+short"} and [ATRRT]{acronym-label="ATRRT" acronym-form="singular+short"} algorithms. Transition tests accept or reject a potential new state depending on its cost relative to its parent. These tests help reduce the *integral* or *mechanical work* of the path in a cost space; however, for problems seeking to minimize path length are equivalent to graph pruning.

These algorithms, and those designed for more advanced purposes (e.g., [RRT]{acronym-label="RRT" acronym-form="singular+abbrv"}^X^ [@otte_ijrr16]), can be improved with the direct informed sampling and admissible graph pruning techniques illustrated in Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"}.

## Direct Informed Sampling for Path Length

This paper presents Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} as a demonstration of how direct sampling of $L^2$ informed sets increases the rate at which [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} improves solutions for problems seeking to minimize path length. Unlike sample biasing, this approach considers all homotopy classes that could provide better solutions (i.e., $100\%$ recall) while maintaining uniform sample distribution over a subplanning problem. Unlike sample rejection or graph pruning, it is effective regardless of the relative size of the informed set or the state dimension (i.e., high precision). In situations where the heuristic does not provide substantial information (i.e., small planning problems and/or large informed sets), it performs identically to [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}.

# The $L^2$ Informed Set {#sec:l2}

A universally admissible heuristic is well defined for problems seeking to minimize path length in $\mathbb{R}^n$ and is commonly used in sampling-based planners (e.g., [@ferguson_iros06; @akgun_iros11; @otte_tro13]). The cost of a solution constrained to pass through any state, $\mathbf{x}\in X$, is bounded from below by the $L^2$ norm (i.e., Euclidean distance) between it, the start, $\mathbf{x}_{\rm start}$, and the goal, $\mathbf{x}_{\rm goal}$, $$\begin{equation}
\label{eqn:fBelow}
    \widehat{f}\left(\mathbf{x}\right) = \left\| \mathbf{x}- \mathbf{x}_{\rm start} \right\|_{2} + \left\| \mathbf{x}_{\rm goal}- \mathbf{x} \right\|_{2}.
\end{equation}$$ The set of states that could provide a better solution than the current solution cost, $c_{i}$, can then be referred to as the $L^2$ informed set, $$\begin{equation*}
    X_{\widehat{f}}= \left\lbrace \mathbf{x}\in X_{\rm free}\;\;\middle|\;\;\left\| \mathbf{x}- \mathbf{x}_{\rm start} \right\|_{2} + \left\| \mathbf{x}_{\rm goal}- \mathbf{x} \right\|_{2} < c_{i}\right\rbrace.
\end{equation*}$$ This informed set is a universally admissible estimate of the omniscient set and is exact in the absence of obstacles and constraints (i.e., it is sharp over all minimum-path-length problems). The size of this informed set will decrease as solutions improve.

:::: {#fig:ellipse .figure latex-placement="tb"}
![](Gammell2017Informed_figs/ellipse_diagram.png)

::: caption
The $L^2$ informed set, $X_{\widehat{f}}$, for a $\mathbb{R}^2$ problem seeking to minimize path length is an ellipse with the initial state, $\mathbf{x}_{\rm start}$, and the goal state, $\mathbf{x}_{\rm goal}$, as focal points. The shape of the ellipse depends on both the initial and goal states, the theoretical minimum cost between the two, $c_{\rm min}$, and the cost of the best solution found to date, $c_{i}$. The eccentricity of the ellipse is given by $c_{\rm min}/c_{i}$.
:::
::::

The $L^2$ informed set is the intersection of the free space, $X_{\rm free}$, and a $n$-dimensional hyperellipsoid symmetric about its transverse axis (i.e., a prolate hyperspheroid), $$\begin{equation*}
    X_{\widehat{f}}= X_{\rm free}\cap X_{\rm PHS},
\end{equation*}$$ where $$\begin{equation*}
    X_{\rm PHS}\coloneqq \left\lbrace \mathbf{x}\in \mathbb{R}^n\;\;\middle|\;\;\left\| \mathbf{x}- \mathbf{x}_{\rm start} \right\|_{2} + \left\| \mathbf{x}_{\rm goal}- \mathbf{x} \right\|_{2} < c_{i}\right\rbrace.
\end{equation*}$$

The prolate hyperspheroid has focal points at $\mathbf{x}_{\rm start}$ and $\mathbf{x}_{\rm goal}$, a transverse diameter of $c_{i}$, and conjugate diameters of $\sqrt{c_{i}^2 - c_{\rm min}^2}$, where $$\begin{equation*}
    c_{\rm min}\coloneqq \left\| \mathbf{x}_{\rm goal}-\mathbf{x}_{\rm start} \right\|_{2},
\end{equation*}$$ is the theoretical minimum cost (Fig. [5](#fig:ellipse){reference-type="ref" reference="fig:ellipse"}). The Lebesgue measure of the informed set is $$\begin{equation}
\label{eqn:phsMeasure}
    \lambda\left(X_{\widehat{f}}\right) \leq \lambda\left(X_{\rm PHS}\right) = \frac{c_{i}\left( c_{i}^2 - c_{\rm min}^2 \right)^{\frac{n-1}{2}} \zeta_{n}}{2^n},
\end{equation}$$ where $\zeta_{n}$ is the Lebesgue measure of a $n$-dimensional unit ball, $$\begin{equation}
\label{eqn:ballMeasure}
    \zeta_{n} \coloneqq \frac{\pi^{\frac{n}{2}}}{\Gamma\left(\frac{n}{2} + 1\right)},
\end{equation}$$ and $\Gamma\left(\cdot\right)$ is the gamma function, an extension of factorials to real numbers [@gamma_function].

The probability of uniformly sampling this informed set by sampling any superset (e.g., a bounding box), $X_{\rm samp}\supseteq X_{\widehat{f}}$, can be written as a ratio of measures, $$\begin{align}
\label{eqn:sampleProb}
    &P\left(\mathbf{x}_{\rm rand}\in X_{\widehat{f}}\;\;\middle|\;\;\mathbf{x}_{\rm rand}\sim\mathcal{U}\left(X_{\rm samp}\right)\right)
    \leq \frac{\lambda\left(X_{\rm PHS}\right)}{\lambda\left(X_{\rm samp}\right)} \nonumber\\
    &\qquad\qquad\qquad\qquad\qquad\quad
    {}= \frac{\pi^{\frac{n}{2}} c_{i}\left( c_{i}^2 - c_{\rm min}^2 \right)^{\frac{n-1}{2}}}{2^n\Gamma\left(\frac{n}{2} + 1\right) \lambda\left(X_{\rm samp}\right)},
\end{align}$$ which can be combined with Theorem [13](#thm:necessary:heuristic:prob){reference-type="ref" reference="thm:necessary:heuristic:prob"} to bound the probability of improving a solution to a holonomic problem, $$\begin{align}
\label{eqn:betterProb}
    \forall i\geq \kappa,\, & P\left(c_{i+1}< c_{i}\;\;\middle|\;\;\mathbf{x}_{\rm rand}\sim\mathcal{U}\left(X_{\rm samp}\right)\right) \nonumber\\
    &\qquad\qquad\qquad\quad
    \leq \frac{\pi^{\frac{n}{2}} c_{i}\left( c_{i}^2 - c_{\rm min}^2 \right)^{\frac{n-1}{2}}}{2^n\Gamma\left(\frac{n}{2} + 1\right) \lambda\left(X_{\rm samp}\right)}.
\end{align}$$

:::: {#fig:sampleTheory .figure latex-placement="tb"}
![](Gammell2017Informed_figs/samplingTheory.png){width="\\textwidth"}

::: caption
An illustration of state dimension on problems seeking to minimize path length. The best case performance of an admissible rectangular sampling, e.g., [@otte_tro13], occurs when the rectangle tightly bounds the prolate hyperspheroid defined by the current solution cost, $X_{\rm rect}\supset X_{\rm PHS}\supseteq X_{\widehat{f}}$, (a). The probability of sampling this $L^2$ informed set (i.e., its relative measure) decreases *factorially* (i.e., faster than exponentially) with state dimension, $n$, (b), meaning that existing formulations of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} do not scale effectively to high state dimensions. Direct informed sampling, Alg. [\[algo:infset\]](#algo:infset){reference-type="ref" reference="algo:infset"}, scales more efficiently as illustrated by the average per-sample time versus state dimension, (c). Samples in the unit $n$-ball for Alg. [\[algo:phs\]](#algo:phs){reference-type="ref" reference="algo:phs"} were generated with Boost 1.58.
:::
::::

This probability becomes arbitrarily small for

::: inparaenum
costs, $c_{i}$, near the theoretical limit, $c_{\rm min}$,[]{#item:reject:cost label="item:reject:cost"}

large sampling domains, $\lambda\left(X_{\rm samp}\right)$, or[]{#item:reject:size label="item:reject:size"}

high state dimensions, $n$.[]{#item:reject:state label="item:reject:state"}
:::

While the solution cost and sampling domain size may vary during the search of a problem, the state dimension is constant throughout. This motivates investigating the effect of state dimension on existing formulations of the holonomic minimum-path-length planning problem (Theorem [14](#thm:curse){reference-type="ref" reference="thm:curse"}).

::: {#thm:curse .thm}
**Theorem 14** (The minimum-path-length curse of dimensionality). *The probability that [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} improves a solution to holonomic problems seeking to minimize path length decreases *factorially* (i.e., faster than exponentially) as state dimension increases, $$\begin{align}
\label{eqn:thm:curse}
        \forall i\geq \kappa,\, P\left(c_{i+1}<c_{i}\;\;\middle|\;\;\mathbf{x}_{\rm rand}\sim\mathcal{U}\left(X_{\rm rect}\right)\right) \leq& \frac{\pi^{\frac{n}{2}}}{2^n\Gamma\left(\frac{n}{2} + 1\right)},
\end{align}$$ when uniformly sampling a (hyper)rectangle bounding the $L^2$ informed set, $X_{\rm rect}\supset X_{\rm PHS}\supseteq X_{\widehat{f}}\supseteq X_{f}$.*

*For simplicity, this statement is limited to holonomic planning but it can be extended to specific constraints by expanding Lemma [5](#lem:necessary:exact:sample){reference-type="ref" reference="lem:necessary:exact:sample"}.*
:::

::: proof
*Proof.* Theorem [14](#thm:curse){reference-type="ref" reference="thm:curse"} is proven for [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} but holds for any algorithm for which an equivalent to Theorem [13](#thm:necessary:heuristic:prob){reference-type="ref" reference="thm:necessary:heuristic:prob"} exists.

The smallest possible $X_{\rm rect}$ that completely contains $X_{\rm PHS}$ is a (hyper)rectangle with widths corresponding to the diameters of the prolate hyperspheroid (Fig. [6](#fig:sampleTheory){reference-type="ref" reference="fig:sampleTheory"}a). The measure of any $X_{\rm rect}\supset X_{\rm PHS}$ is therefore bounded from below as $$\begin{equation}
\label{eqn:thm:curse:tightMeasure}
        \lambda\left(X_{\rm rect}\right) \geq c_{i}\left( c_{i}^2 - c_{\rm min}^2 \right)^{\frac{n-1}{2}}.
\end{equation}$$ When substituted into [\[eqn:betterProb\]](#eqn:betterProb){reference-type="eqref" reference="eqn:betterProb"} this gives $$\begin{equation*}
        \forall i\geq \kappa,\, P\left(c_{i+1}< c_{i}\;\;\middle|\;\;\mathbf{x}_{\rm rand}\sim\mathcal{U}\left(X_{\rm rect}\right)\right) \leq \frac{\pi^{\frac{n}{2}}}{2^n\Gamma\left(\frac{n}{2} + 1\right)},
\end{equation*}$$ proving Theorem [14](#thm:curse){reference-type="ref" reference="thm:curse"} for all rectangular sets, $X_{\rm rect}$, such that $X_{\rm rect}\supset X_{\rm PHS}\supseteq X_{\widehat{f}}\supseteq X_{f}$. ◻
:::

Theorem [14](#thm:curse){reference-type="ref" reference="thm:curse"} is an upper bound on the utility of rectangular rejection sampling in holonomic planning and is illustrated by plotting [\[eqn:thm:curse\]](#eqn:thm:curse){reference-type="eqref" reference="eqn:thm:curse"} versus state dimension (Fig. [6](#fig:sampleTheory){reference-type="ref" reference="fig:sampleTheory"}b). The results show that while rectangular rejection sampling may be $79\%$ successful in $\mathbb{R}^2$, its success decreases factorially as state dimension increases and is only $2\%$ in $\mathbb{R}^8$ and $4 \times 10^{-4}\%$ in $\mathbb{R}^{16}$. These numbers represent the *best-case* for rectangular rejection sampling and actual performance will depend on the size and orientation of the informed set relative to the sampling domain. This motivates a need for a direct method to sample the prolate hyperspheroid regardless of size, orientation, and state dimension.

## Direct Sampling {#sec:l2:sample}

A direct method to generate uniformly distributed samples in the $L^2$ informed set is adapted from techniques to sample hyperellipsoids [@sun_fusion02].

Let $\mathbf{S}\in\mathbb{R}^{n\times n}$ be a symmetric, positive-definite matrix (the hyperellipsoid matrix) such that the interior of a hyperellipsoid, $X_{\rm ellipse}$, is defined as $$\begin{equation}
\label{eqn:SDefn}
    X_{\rm ellipse}\coloneqq \left\lbrace \mathbf{x}\in \mathbb{R}^n\,\middle|\,\left( \mathbf{x}- \mathbf{x}_{\rm centre}\right)^T\mathbf{S}^{-1}\left( \mathbf{x}- \mathbf{x}_{\rm centre}\right) < 1\right\rbrace,
\end{equation}$$ where $\mathbf{x}_{\rm centre}$ is the centre point of the hyperellipsoid. Uniformly distributed samples in the hyperellipsoid, $\mathbf{x}_{\rm ellipse}\sim\mathcal{U}\left(X_{\rm ellipse}\right)$, can be generated from uniformly distributed samples in the interior of a unit $n$-dimensional ball, $\mathbf{x}_{\rm ball}\sim\mathcal{U}\left(X_{\rm ball}\right)$, by $$\begin{equation}
\label{eqn:transformDefn}
    \mathbf{x}_{\rm ellipse}= \mathbf{L} \mathbf{x}_{\rm ball}+ \mathbf{x}_{\rm centre},
\end{equation}$$ where $\mathbf{L}\in\mathbb{R}^{n\times n}$ is the lower-triangular Cholesky decomposition of the hyperellipsoid matrix such that $$\begin{equation*}
    \mathbf{L}\mathbf{L}^T \equiv \mathbf{S}
\end{equation*}$$ and $$\begin{equation*}
    X_{\rm ball}\coloneqq \left\lbrace \mathbf{x}\in\mathbb{R}^n\;\;\middle|\;\;\left\| \mathbf{x} \right\|_{2} < 1\right\rbrace.
\end{equation*}$$

For hyperellipsoids with orthogonal axes, there exists a coordinate frame in which the hyperellipsoid matrix is diagonal, $$\begin{equation*}
    \mathbf{S}' \coloneqq \mathop{\mathrm{diag}}\left( r_1^2, r_2^2, \ldots, r_n^2 \right),
\end{equation*}$$ where $r_j$ is the radius of $j$-th axis of the hyperellipsoid and $\mathop{\mathrm{diag}}\left(\cdot\right)$ constructs a diagonal matrix. A rotation from this hyperellipsoid-aligned frame to the world frame, $\mathbf{C}_{\rm we}\in SO\left(n\right)$, can be used to write [\[eqn:SDefn\]](#eqn:SDefn){reference-type="eqref" reference="eqn:SDefn"} in terms of $\mathbf{S}'$ as $$\begin{align}
\label{eqn:transformFinal}
%
    X_{\rm ellipse}\coloneqq &\left\lbrace\mathbf{x}\in \mathbb{R}^n\;\;\middle|
        \vphantom{\left( \mathbf{x}- \mathbf{x}_{\rm centre}\right)^T\mathbf{C}_{\rm we}\mathbf{S'}^{-1}\mathbf{C}_{\rm we}^T\left( \mathbf{x}- \mathbf{x}_{\rm centre}\right) < 1}\right.
        \nonumber\\
        &\;\left.\vphantom{\mathbf{x}\in \mathbb{R}^n}
    \left( \mathbf{x}- \mathbf{x}_{\rm centre}\right)^T\mathbf{C}_{\rm we}\mathbf{S'}^{-1}\mathbf{C}_{\rm we}^T\left( \mathbf{x}- \mathbf{x}_{\rm centre}\right) < 1\right\rbrace,\nonumber
\shortintertext{and \eqref{eqn:transformDefn} as}
    &\qquad\mathbf{x}_{\rm ellipse}= \mathbf{C}_{\rm we}\mathbf{L}' \mathbf{x}_{\rm ball}+ \mathbf{x}_{\rm centre},
\end{align}$$ given the orthogonality of rotation matrices, $\mathbf{C}_{\rm we}^{-1}\equiv\mathbf{C}_{\rm we}^T$, and that $\mathbf{L}'\mathbf{L}'^T \equiv \mathbf{S}'$.

The rotation between frames can be solved directly as a general Wahba problem [@wahba_siam65] even when underspecified [@ruiter_jas14]. Generally, the rotation matrix from one set of axes, $\left\lbrace \mathbf{a}_{j}\right\rbrace$, to another set of axes, $\left\lbrace \mathbf{b}_{j}\right\rbrace$, is given by $$\begin{equation}
 \label{eqn:svd}%
    \mathbf{C}_{\rm ba} = \mathbf{U}\boldsymbol{\Lambda}\mathbf{V}^{T},
\end{equation}$$ where $\boldsymbol{\Lambda}\in \mathbb{R}^{n\times n}$ is $$\begin{equation*}
    \boldsymbol{\Lambda} \coloneqq \mathop{\mathrm{diag}}\left( 1, \ldots, 1, \det\left(\mathbf{U}\right) \det\left(\mathbf{V}\right) \right),
\end{equation*}$$ and $\det\left(\cdot\right)$ is the matrix determinant. The terms $\mathbf{U} \in \mathbb{R}^{n\times n}$ and $\mathbf{V} \in \mathbb{R}^{n\times n}$ are unitary matrices such that $\mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^T \equiv \mathbf{M}$ via singular value decomposition and $\mathbf{M}\in\mathbb{R}^{n\times n}$ is given by the outer product of the $j\leq n$ corresponding axes, $$\begin{equation}
\label{eqn:MDefn}
    \mathbf{M} \coloneqq \left[\mathbf{a}_{1}, \mathbf{a}_{2}, \ldots, \mathbf{a}_{j} \right] \left[\mathbf{b}_{1}, \mathbf{b}_{2}, \ldots \mathbf{b}_{j}\right]^T.
\end{equation}$$

In problems seeking to minimize path length, the hyperellipsoid is a prolate hyperspheroid described by $$\begin{align}
    \mathbf{x}_{\rm centre}&\coloneqq \frac{\mathbf{x}_{\rm start}+ \mathbf{x}_{\rm goal}}{2},\label{eqn:phs:xcentre}\\
    \mathbf{S'} &\coloneqq \mathop{\mathrm{diag}}\left( \frac{c_{i}^2}{4}, \frac{c_{i}^2 - c_{\rm min}^2}{4}, \ldots, \frac{c_{i}^2 - c_{\rm min}^2}{4} \right),\nonumber\\
\shortintertext{and therefore,}
    \mathbf{L}' &= \mathop{\mathrm{diag}}\left( \frac{c_{i}}{2}, \frac{\sqrt{c_{i}^2 - c_{\rm min}^2}}{2}, \ldots, \frac{\sqrt{c_{i}^2 - c_{\rm min}^2}}{2} \right)\label{eqn:phs:L}.
\end{align}$$ Its local coordinate system is underspecified in the conjugate directions due to symmetry, making [\[eqn:MDefn\]](#eqn:MDefn){reference-type="eqref" reference="eqn:MDefn"} just $$\begin{equation}
\label{eqn:phs:M}%
    \mathbf{M} = \mathbf{a}_1\mathbf{1}_1^T,
\end{equation}$$ where $\mathbf{1}_1$ the first column of the identity matrix and the transverse axis in the world frame is $$\begin{equation*}
%
    \mathbf{a}_{1} = \left( \mathbf{x}_{\rm goal}- \mathbf{x}_{\rm start}\right)/\left\| \mathbf{x}_{\rm goal}- \mathbf{x}_{\rm start} \right\|_{2}.
\end{equation*}$$

Samples distributed uniformly in the $L^2$ informed set, $X_{\widehat{f}}=X_{\rm PHS}\cap X_{\rm free}$, can therefore be generated by using [\[eqn:transformFinal\]](#eqn:transformFinal){reference-type="eqref" reference="eqn:transformFinal"} to transform samples drawn uniformly from a unit $n$-ball. These samples are mapped to the prolate hyperspheroid through scaling, [\[eqn:phs:L\]](#eqn:phs:L){reference-type="eqref" reference="eqn:phs:L"}, rotation, [\[eqn:svd\]](#eqn:svd){reference-type="eqref" reference="eqn:svd"} and [\[eqn:phs:M\]](#eqn:phs:M){reference-type="eqref" reference="eqn:phs:M"}, and translation, [\[eqn:phs:xcentre\]](#eqn:phs:xcentre){reference-type="eqref" reference="eqn:phs:xcentre"}.

Sun and Farooq [@sun_fusion02] investigate various methods to generate samples in hyperellipsoids and provide the following lemma regarding the uniform sample density of this technique.

::: {#lem:uniform .lem}
**Lemma 15** (The uniform distribution of samples transformed into a hyperellipsoid from a unit $n$-ball. Originally Lemma 1 in [@sun_fusion02]). *If the random points distributed in a hyperellipsoid are generated from the random points uniformly distributed in a hypersphere through a linear invertible nonorthogonal transformation, then the random points distributed in the hyperellipsoid are also uniformly distributed.*
:::

::: proof
*Proof.* For brevity, [@sun_fusion02] only presents anecdotal proofs of Lemma [15](#lem:uniform){reference-type="ref" reference="lem:uniform"}. The full proof from the supplementary online material appears in Appendix [10](#appx:uniform){reference-type="ref" reference="appx:uniform"}. ◻
:::

::: algorithm
$\mathbf{x}_{\rm rand}\gets \mathtt{SamplePHS}\left(\mathbf{x}_{\rm start},\mathbf{x}_{\rm goal},c_{i}\right)$ $\mathbf{x}_{\rm rand}\gets \mathtt{SampleProblem}\left(X\right)$
:::

::: algorithm
$c_{\rm min}\gets \left\| \mathbf{x}_{\rm goal}- \mathbf{x}_{\rm start} \right\|_{2}$ []{#algo:phs:startStatic label="algo:phs:startStatic"} $\mathbf{x}_{\rm centre}\gets \left(\mathbf{x}_{\rm start}+ \mathbf{x}_{\rm goal}\right)/2$ $\mathbf{a}_1 \gets \left(\mathbf{x}_{\rm goal}- \mathbf{x}_{\rm start}\right)/c_{\rm min}$ $\left\lbrace \mathbf{U},\,\mathbf{V}\right\rbrace \gets \mathtt{SVD}\left(\mathbf{a}_1\mathbf{1}_1^T\right)$ $\boldsymbol{\Lambda} \gets \mathop{\mathrm{diag}}\left( 1, \ldots, 1, \det\left(\mathbf{U}\right) \det\left(\mathbf{V}\right) \right)$ $\mathbf{C}_{\rm we}\gets \mathbf{U}\boldsymbol{\Lambda}\mathbf{V}^{T}$ []{#algo:phs:endStatic label="algo:phs:endStatic"} $r_{1} \gets c_{i}/2$ $\left\lbrace r_j\right\rbrace_{j= 2,\ldots,n} \gets \left(\sqrt{c_{i}^2 - c_{\rm min}^2}\right)/2$ $\mathbf{L} \gets \mathop{\mathrm{diag}}\left(r_1, r_2, \ldots, r_n\right)$ $\mathbf{x}_{\rm ball}\gets \mathtt{SampleUnitBall}\left(n\right)$ $\mathbf{x}_{\rm rand}\gets \mathbf{C}_{\rm we}\mathbf{L}\mathbf{x}_{\rm ball}+ \mathbf{x}_{\rm centre}$
:::

### Algorithm {#sec:l2:sample:algo}

The $L^2$ informed set is an arbitrary intersection of the prolate hyperspheroid and the problem domain. It can be sampled efficiently by considering the relative measure of the two sets and sampling the smaller set until a sample belonging to both sets is found. These procedures are presented algorithmically in Algs. [\[algo:infset\]](#algo:infset){reference-type="ref" reference="algo:infset"} and [\[algo:phs\]](#algo:phs){reference-type="ref" reference="algo:phs"} and are publicly available in [OMPL]{acronym-label="OMPL" acronym-form="singular+short"}. Note that for most problems Alg. [\[algo:phs\]](#algo:phs){reference-type="ref" reference="algo:phs"}, Lines [\[algo:phs:startStatic\]](#algo:phs:startStatic){reference-type="ref" reference="algo:phs:startStatic"}--[\[algo:phs:endStatic\]](#algo:phs:endStatic){reference-type="ref" reference="algo:phs:endStatic"} are constant and only need to be calculated once.

The function $\mathtt{SVD}\left(\cdot\right)$ denotes the singular value decomposition of a matrix and $\mathtt{SampleUnitBall}\left(n\right)$ returns uniformly distributed samples from the interior of an $n$-dimensional unit ball. The measure of the prolate hyperspheroid, $\lambda\left(X_{\rm PHS}\right)$, is given by [\[eqn:phsMeasure\]](#eqn:phsMeasure){reference-type="eqref" reference="eqn:phsMeasure"} and `SampleProblem` returns samples uniformly distributed over the entire planning domain. Implementations of `SVD` and `SampleUnitBall` can be found in common C++ libraries.

### Practical Performance {#sec:l2:sample:exp}

Direct informed sampling (Alg. [\[algo:infset\]](#algo:infset){reference-type="ref" reference="algo:infset"}) is compared to the *best-case* performance of rectangular rejection sampling. The average computational time required to find a sample in the $L^2$ informed set is calculated by generating $10^6$ samples at each dimension (Fig. [6](#fig:sampleTheory){reference-type="ref" reference="fig:sampleTheory"}c). The results show that while rejection sampling may outperform direct informed sampling in low state dimensions (e.g., $\mathbb{R}^2$: $7.3\times10^{-8}$ vs. $3.5\times10^{-7}$ seconds), it becomes orders of magnitude slower as state dimension increases (e.g., $\mathbb{R}^{16}$: $4.0\times10^{-2}$ vs. $7.2\times10^{-7}$ seconds). These per-sample times are small but significant. Generating $10^5$ samples in $\mathbb{R}^{16}$ requires less than a second with direct informed sampling ($7.2\times10^{-2}$ seconds) but over an hour with rectangular rejection sampling ($3953$ seconds).

This experiment represents optimistic results for both constant (e.g., the problem domain) and adaptive (e.g., [@otte_tro13]) rectangular rejection sampling. Constant sampling domains rarely provide tight bounds on the informed set and will generally have higher rejection rates than the experiment. Adaptive sampling domains may tightly bound the informed set but must account for its alignment relative to the state space. This requires either a larger rectangular sampling domain or a rotation between frames that increases the rejection rate or computational cost compared to the experiment, respectively.

## Extension to Multiple Goals {#sec:l2:multi}

Many planning problems seek the minimum-length path that connects a start to any state in a goal region, $X_{\rm goal}$. In these situations the omniscient set is all states that could provide a better solution to *any* goal. The multigoal $L^2$ informed set is $$\begin{align*}
    X_{\widehat{f}}\coloneqq &\left\lbrace\mathbf{x}\in X_{\rm free}\;\;\middle|\;\;\left\| \mathbf{x}- \mathbf{x}_{\rm start} \right\|_{2} + \left\| \mathbf{x}_{{\rm goal},j}- \mathbf{x} \right\|_{2} < c_{i}
        \vphantom{\mbox{for any}\;\;\mathbf{x}_{{\rm goal},j}\in X_{\rm goal}}\right.\nonumber\\
        &\qquad\qquad\qquad\qquad\qquad\quad\left.\vphantom{\mathbf{x}\in X_{\rm free}\left\| \mathbf{x}- \mathbf{x}_{\rm start} \right\|_{2} + \left\| \mathbf{x}_{{\rm goal},j}- \mathbf{x} \right\|_{2}  < c_{i}}
    \mbox{for any}\;\;\mathbf{x}_{{\rm goal},j}\in X_{\rm goal}\right\rbrace.
\end{align*}$$

For a countable goal region, $X_{\rm goal}\coloneqq \left\lbrace \mathbf{x}_{{\rm goal},j}\right\rbrace_{j=1}^z$, this set is the union of the individual informed sets of each goal, $$\begin{equation*}
    X_{\widehat{f}}= \bigcup_{j=1}^zX_{\widehat{f},j},
\end{equation*}$$ where $z$ is the number of goals and $$\begin{equation*}
    X_{\widehat{f},j}\coloneqq \left\lbrace \mathbf{x}\in X_{\rm free}\hspace{-1pt}\;\;\middle|\;\;\hspace{-1pt}\left\| \mathbf{x}- \mathbf{x}_{\rm start} \right\|_{2} + \left\| \mathbf{x}_{{\rm goal},j}- \mathbf{x} \right\|_{2} < c_{i}\right\rbrace,
\end{equation*}$$ is the $L^2$ informed set of an individual $\left( \mathbf{x}_{\rm start}, \mathbf{x}_{{\rm goal},j}\right)$ pair. If the individual informed sets do not intersect, then a uniform sample distribution can be generated by randomly selecting an individual subset, $j$, in proportion to its relative measure, $$\begin{equation*}
    p\left(1\leq j\leq z\right)\coloneqq\frac{\lambda\left(X_{\widehat{f},j}\right)}{\sum_{k=1}^{z}\lambda\left(X_{\widehat{f},k}\right)},
\end{equation*}$$ and then generating a uniformly distributed sample inside the selected subset, $X_{\widehat{f},j}$.

::: algorithm
$\mathbf{x}_{{\rm goal},j}\gets \mathtt{RandomGoal}\left(\mathbf{x}_{\rm start}, X_{\rm goal}, c_{i}\right)$ $\mathbf{x}_{\rm rand}\gets \mathtt{SamplePHS}\left(\mathbf{x}_{\rm start}, {\color{BrickRed} \mathbf{x}_{{\rm goal},j}} ,c_{i}\right)$ $\mathbf{x}_{\rm rand}\gets \mathtt{SampleProblem}\left(X\right)$
:::

::: algorithm
$a \gets 0$ $a \gets a + \lambda\left(X_{{\rm PHS},k}\right)$ $p \gets \mathcal{U}\left[0,1\right]$ $j \gets 0$ $j \gets j + 1$ $p \gets p - \lambda\left(X_{{\rm PHS},j}\right)/a$
:::

If individual sets do intersect, then this approach will oversample states that belong to multiple sets (Fig. [7](#fig:multigoal){reference-type="ref" reference="fig:multigoal"}a). In these situations, uniform sample density can be maintained by probabilistically rejecting samples in proportion to their membership in individual sets. This creates a uniform sample distribution for multigoal $L^2$ informed sets defined by arbitrarily overlapping individual informed sets (Fig. [7](#fig:multigoal){reference-type="ref" reference="fig:multigoal"}b).

### Algorithm {#sec:l2:mult:algo}

The algorithm is described in Algs. [\[algo:multigoal\]](#algo:multigoal){reference-type="ref" reference="algo:multigoal"}--[\[algo:randomKeep\]](#algo:randomKeep){reference-type="ref" reference="algo:randomKeep"} as modifications to the sampling technique for a single-goal $L^2$ informed set, with changes highlighted in red (cf. Alg. [\[algo:infset\]](#algo:infset){reference-type="ref" reference="algo:infset"}). The measure of individual informed sets, $\lambda\left(X_{{\rm PHS},j}\right)$, is calculated from [\[eqn:phsMeasure\]](#eqn:phsMeasure){reference-type="eqref" reference="eqn:phsMeasure"} using the appropriate goal, $\mathbf{x}_{{\rm goal},j}$. This same technique can also be applied to problems with a countable start region.

::: algorithm
$a \gets 0$ $a \gets a + 1$ $p \gets \mathcal{U}\left[0,1\right]$
:::

:::: {#fig:multigoal .figure latex-placement="tp"}
![](Gammell2017Informed_figs/multigoal_sample.png){width="\\columnwidth"}

::: caption
An illustration of the multigoal $L^2$ informed set for a problem seeking to minimize path length from a start at $\left[0, 0\right]^T$, to any of three goals at $\left[ -0.75,\, 0 \right]^T$, $\left[ 0.25,\, 0 \right]^T$, and $\left[ 0.7,\, 0.7 \right]^T$, and a current solution cost of $c_{i}= 1.05$. Each ellipse illustrates the $L^2$ informed set for a start-goal pair. Combining the uniform distributions of these individuals (light grey) would result in a *nonuniform* distribution (dark grey), (a). By probabilistically rejecting samples in proportion to their individual membership, Alg. [\[algo:multigoal\]](#algo:multigoal){reference-type="ref" reference="algo:multigoal"} uniformly samples complex sets of arbitrary intersections, as illustrated with $2500$ random samples, (b).
:::
::::

# Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} {#sec:inf}

Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} is an extension of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} that demonstrates how informed sets can be used to improve anytime almost-surely asymptotically optimal planning. It performs the same as [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} until a solution is found after which the search is focused to the informed set through direct informed sampling and admissible graph pruning (Fig. [8](#fig:example){reference-type="ref" reference="fig:example"}). This increases the likelihood of sampling states that can improve the solution and increases the convergence rate towards the optimum regardless of the relative size of the informed set (e.g., near-minimum solutions or large problem domains) or the state dimension.

Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} uses direct informed sampling (Alg. [\[algo:multigoal\]](#algo:multigoal){reference-type="ref" reference="algo:multigoal"}), admissible graph pruning (Section [5.2](#sec:inf:prune){reference-type="ref" reference="sec:inf:prune"}), and an updated calculation of the rewiring neighbourhood (Section [5.3](#sec:inf:rewire){reference-type="ref" reference="sec:inf:rewire"}) to focus the search. The complete algorithm is presented in Algs. [\[algo:inf_rrtstar\]](#algo:inf_rrtstar){reference-type="ref" reference="algo:inf_rrtstar"} and [\[algo:prune\]](#algo:prune){reference-type="ref" reference="algo:prune"} as modifications to [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}, with changes highlighted in red. It can also be integrated into other sampling-based planners, such as [RRT]{acronym-label="RRT" acronym-form="singular+short"}^X^ [@otte_ijrr16] and [BITstar]{acronym-label="BITstar" acronym-form="singular+short"} [@gammell_icra15; @gammell_phd17; @gammell_ijrr18].

At each iteration, Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} calculates the current best solution (Alg. [\[algo:inf_rrtstar\]](#algo:inf_rrtstar){reference-type="ref" reference="algo:inf_rrtstar"}, Line [\[algo:inf_rrtstar:min\]](#algo:inf_rrtstar:min){reference-type="ref" reference="algo:inf_rrtstar:min"}) from the vertices in the goal region (Alg. [\[algo:inf_rrtstar\]](#algo:inf_rrtstar){reference-type="ref" reference="algo:inf_rrtstar"}, Lines [\[algo:inf_rrtstar:init\]](#algo:inf_rrtstar:init){reference-type="ref" reference="algo:inf_rrtstar:init"}, [\[algo:inf_rrtstar:goalStart\]](#algo:inf_rrtstar:goalStart){reference-type="ref" reference="algo:inf_rrtstar:goalStart"}--[\[algo:inf_rrtstar:goalEnd\]](#algo:inf_rrtstar:goalEnd){reference-type="ref" reference="algo:inf_rrtstar:goalEnd"}). This defines a shrinking $L^2$ informed set that is used to both focus sampling (Alg. [\[algo:inf_rrtstar\]](#algo:inf_rrtstar){reference-type="ref" reference="algo:inf_rrtstar"}, Line [\[algo:inf_rrtstar:sample\]](#algo:inf_rrtstar:sample){reference-type="ref" reference="algo:inf_rrtstar:sample"}; Alg. [\[algo:multigoal\]](#algo:multigoal){reference-type="ref" reference="algo:multigoal"}) and prune the graph (Alg. [\[algo:inf_rrtstar\]](#algo:inf_rrtstar){reference-type="ref" reference="algo:inf_rrtstar"}, Line [\[algo:inf_rrtstar:prune\]](#algo:inf_rrtstar:prune){reference-type="ref" reference="algo:inf_rrtstar:prune"}; Alg. [\[algo:prune\]](#algo:prune){reference-type="ref" reference="algo:prune"}). This process continues for as long as time allows or until a suitable solution is found.

Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} retains the probabilistic completeness and almost-sure asymptotically optimality of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}. It is probabilistically complete since it does not modify the search for an initial solution. It is almost-surely asymptotically optimal as it maintains a uniform sample distribution over a subset of the planning problem in which it uses a local rewiring neighbourhood that satisfies the bounds presented in [@karaman_ijrr11].

:::: {#fig:example .figure latex-placement="tbp"}
![](Gammell2017Informed_figs/exampleWorld.png){width="\\textwidth"}

::: caption
An example of how Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} uses the current solution to focus search to the $L^2$ informed set. After an unfocused search for an initial solution, (a), Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} prunes the graph of unnecessary states and redefines the search domain to the current $L^2$ informed set, (b). Samples are then generated directly from this informed set, avoiding those that are known to be unable to improve the current solution. This reduced search space increases the likelihood of finding an improved solution, which in turn further reduces the search space, (c). This results in an algorithm that focuses the search to the subproblem given by the current solution, shown enlarged in (d), even as the subproblem decreases with further improvement.
:::
::::

::: algorithm
$V\gets \left\lbrace \mathbf{x}_{\rm start}\right\rbrace;\;$ $E\gets \emptyset;\;$ $\mathcal{T}= \left( V, E\right)$ $V_{\mbox{\rm\scriptsize sol'n}}\gets \emptyset$ []{#algo:inf_rrtstar:init label="algo:inf_rrtstar:init"}

$c_{i}\gets \min_{\mathbf{v}_{\rm goal}\in V_{\mbox{\rm\scriptsize sol'n}}} \left\lbrace g_{\mathcal{T}}\left(\mathbf{v}_{\rm goal}\right)\right\rbrace$ []{#algo:inf_rrtstar:min label="algo:inf_rrtstar:min"} $\mathbf{x}_{\rm rand}\gets \mathtt{Sample}\left(\mathbf{x}_{\rm start}, X_{\rm goal}, c_{i}\right)$ []{#algo:inf_rrtstar:sample label="algo:inf_rrtstar:sample"} $\mathbf{v}_{\rm nearest}\gets \mathtt{Nearest}\left(V, \mathbf{x}_{\rm rand}\right)$ $\mathbf{x}_{\rm new}\gets \mathtt{Steer}\left(\mathbf{v}_{\rm nearest}, \mathbf{x}_{\rm rand}\right)$

$V_{\mbox{\rm\scriptsize sol'n}}\xleftarrow{\scriptscriptstyle +}\left\lbrace \mathbf{x}_{\rm new}\right\rbrace$[]{#algo:inf_rrtstar:goalEnd label="algo:inf_rrtstar:goalEnd"} $V\xleftarrow{\scriptscriptstyle +}\left\lbrace \mathbf{x}_{\rm new}\right\rbrace$ $V_{\rm near}\gets \mathtt{Near}\left(V, \mathbf{x}_{\rm new}, r_{\mathrm{rewire}}\right)$ $\mathbf{v}_{\rm min}\gets \mathbf{v}_{\rm nearest}$ $c_{\rm new}\gets g_{\mathcal{T}}\left(\mathbf{v}_{\rm near}\right) + c\left(\mathbf{v}_{\rm near},\mathbf{x}_{\rm new}\right)$ $\mathbf{v}_{\rm min}\gets \mathbf{v}_{\rm near}$ $E\xleftarrow{\scriptscriptstyle +}\left\lbrace\left(\mathbf{v}_{\rm min}, \mathbf{x}_{\rm new}\right)\right\rbrace$

$c_{\rm near}\gets g_{\mathcal{T}}\left(\mathbf{x}_{\rm new}\right) + c\left(\mathbf{x}_{\rm new},\mathbf{v}_{\rm near}\right)$ $\mathbf{v}_{\rm parent}\gets \mathtt{Parent}\left(\mathbf{v}_{\rm near}\right)$ $E\xleftarrow{\scriptscriptstyle -}\left\lbrace \left(\mathbf{v}_{\rm parent}, \mathbf{v}_{\rm near}\right) \right\rbrace$ $E\xleftarrow{\scriptscriptstyle +}\left\lbrace \left( \mathbf{x}_{\rm new}, \mathbf{v}_{\rm near}\right)\right\rbrace$ $\mathtt{Prune}\left(V, E, c_{i}\right)$[]{#algo:inf_rrtstar:prune label="algo:inf_rrtstar:prune"}
:::

## Notation {#sec:inf:note}

The tree, $\mathcal{T}\coloneqq \left( V, E\right)$, is defined by a set of vertices, $V\subset X_{\rm free}$, and edges, $E= \left\lbrace \left( \mathbf{v}, \mathbf{w}\right)\right\rbrace$, for some $\mathbf{v},\, \mathbf{w}\in V$. The function $g_{\mathcal{T}}\left(\mathbf{v}\right)$ represents the cost to reach a vertex, $\mathbf{v}\in V$, from the start given the current tree (the cost-to-come). The function $c\left(\mathbf{v},\mathbf{w}\right)$ represents the cost of a path connecting the states $\mathbf{v}, \mathbf{w}\in X_{\rm free}$, and corresponds to the edge cost between those two states if they are connected as vertices in the tree. The notation $X\xleftarrow{\scriptscriptstyle +}\left\lbrace \mathbf{x}\right\rbrace$ and $X\xleftarrow{\scriptscriptstyle -}\left\lbrace \mathbf{x}\right\rbrace$ is used to compactly represent the compounding set operations $X\gets X\cup \left\lbrace \mathbf{x}\right\rbrace$ and $X\gets X\setminus \left\lbrace \mathbf{x}\right\rbrace$, respectively. As is customary, the minimum of an empty set is taken to be infinity and a prolate hyperspheroid defined by an infinite transverse diameter is taken to have infinite measure.

## Graph Pruning (Alg. [\[algo:prune\]](#algo:prune){reference-type="ref" reference="algo:prune"}) {#sec:inf:prune}

Graph pruning simplifies a tree by removing unnecessary vertices. Vertices are often removed if their heuristic values are larger than the current solution (i.e., they do not belong to informed set). While this identifies vertices that cannot provide a better solution, it is not a *sufficient* condition to remove them without negatively affecting the search. Their descendants may still be capable of providing better solutions (i.e., they may belong to the informed set; Fig. [9](#fig:prune:defn){reference-type="ref" reference="fig:prune:defn"}) in which case their removal would negatively affect performance by decreasing vertex density in the search domain (i.e., the informed set; Fig. [10](#fig:prune:exp){reference-type="ref" reference="fig:prune:exp"}b).

An *admissible* pruning method that does not remove vertices from the informed set is presented in Alg. [\[algo:prune\]](#algo:prune){reference-type="ref" reference="algo:prune"}. It iteratively removes leaves of the tree that cannot provide a better solution until no such leaves exist. This only removes vertices if they *and all their descendants* cannot belong to a better solution (i.e., it only removes vertices from outside the informed set; Fig. [9](#fig:prune:defn){reference-type="ref" reference="fig:prune:defn"}). This retains all possibly beneficial vertices regardless of their current connections and does not alter the vertex distribution in areas being searched (Fig. [10](#fig:prune:exp){reference-type="ref" reference="fig:prune:exp"}c).

::: algorithm
$V_{\rm prune}\gets \left\lbrace \mathbf{v}\in V\;\;\middle|\;\;\widehat{f}\left(\mathbf{v}\right) > c_{i},\;\; \mathtt{and}\;\; \forall \mathbf{w}\in V,\; \left( \mathbf{v}, \mathbf{w}\right) \not\in E\right\rbrace$ $E\xleftarrow{\scriptscriptstyle -}\left\lbrace \left( \mathbf{u}, \mathbf{v}\right)\in E\;\;\middle|\;\;\mathbf{v}\in V_{\rm prune}\right\rbrace$ $V\xleftarrow{\scriptscriptstyle -}V_{\rm prune}$
:::

:::: {#fig:prune:defn .figure latex-placement="tbp"}
![](Gammell2017Informed_figs/pruning.png)

::: caption
An illustration of Alg. [\[algo:prune\]](#algo:prune){reference-type="ref" reference="algo:prune"} that shows the retained (black) and pruned (grey) vertices given the $L^2$ informed set (dashed grey line) defined by the current solution. Vertices are pruned if and only if they cannot improve the current solution (i.e., they are not members of the $L^2$ informed set) *and* neither can their descendants. This pruning condition avoids removing promising vertices (e.g., $\mathbf{v}$) simply because they are currently descendants of vertices outside the subset (e.g., $\mathbf{u}$) and maintains the vertex distribution of the $L^2$ informed set (Fig. [10](#fig:prune:exp){reference-type="ref" reference="fig:prune:exp"}).
:::
::::

## The Rewiring Neighbourhood {#sec:inf:rewire}

[RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} almost-surely converges asymptotically to the optimum by incrementally rewiring the tree around new states. In the $r$-disc variant this is the set of states within a radius, $r_{\mathrm{rewire}}$, of the new state, $$\begin{equation}
\label{eqn:back:rewire}
    r_{\mathrm{rewire}}\coloneqq \min\left\lbrace \eta, r_{\mathrm{RRT}^*}\right\rbrace,
\end{equation}$$ where $\eta$ is the maximum allowable edge length of the tree and $r_{\mathrm{RRT}^*}$ is a function of the problem measure and the number of vertices in the tree [@karaman_ijrr11]. Specifically, $$\begin{align}
\label{eqn:back:radius}
    r_{\mathrm{RRT}^*}&>  r_{\mathrm{RRT}^*}^*,\nonumber\\
    r_{\mathrm{RRT}^*}^*&\coloneqq \left(2 \left(1 + \frac{1}{n}\right)
    \left(\frac{\lambda\left(X\right)}{\zeta_{n}}\right)
    \left(\frac{\log\left(\left|V\right|\right)}{\left|V\right|}\right)\right)^{\frac{1}{n}},
\end{align}$$ where $\lambda\left(\cdot\right)$ is the Lebesgue measure of a set (e.g., the *volume*), $\zeta_{n}$ is the Lebesgue measure of an $n$-dimensional unit ball, i.e., [\[eqn:ballMeasure\]](#eqn:ballMeasure){reference-type="eqref" reference="eqn:ballMeasure"}, and $\left|\cdot\right|$ is the cardinality of a set.

The rewiring neighbourhood in the $k$-nearest variant is the $k_{\mathrm{RRT}^*}$-closest states to the new state, where $$\begin{align}
\label{eqn:back:knearest}
    k_{\mathrm{RRT}^*}&>  k_{\mathrm{RRT}^*}^*,\nonumber\\
    k_{\mathrm{RRT}^*}^*&\coloneqq e\left(1+\frac{1}{n}\right)\log\left(\left|V\right|\right).
\end{align}$$

Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} searches a subset of the original planning problem. The rewiring requirements to maintain almost-sure asymptotic optimality in this shrinking domain will be a function of the number of vertices in the informed set, $\left|V\cap X_{\widehat{f}}\right|$, and its measure, $\lambda\left(X_{\widehat{f}}\right)$. The $L^2$ informed set is not known in closed form (it is an intersection of a prolate hyperspheroid and free space) but its measure can be bounded from above by the minimum measure of the prolate hyperspheroid and the problem domain, $$\begin{equation*}
    \lambda\left(X_{\widehat{f}}\right)\leq\min\left\lbrace\lambda\left(X\right),\lambda\left(X_{\rm PHS}\right)\right\rbrace.
\end{equation*}$$

This updates [\[eqn:back:radius\]](#eqn:back:radius){reference-type="eqref" reference="eqn:back:radius"} and [\[eqn:back:knearest\]](#eqn:back:knearest){reference-type="eqref" reference="eqn:back:knearest"} to $$\begin{align}
\label{eqn:radius}
    r_{\mathrm{RRT}^*}^*&\leq \left(2 \left(1 + \frac{1}{n}\right)
    \left(\frac{\min\left\lbrace\lambda\left(X\right),\lambda\left(X_{\rm PHS}\right)\right\rbrace}{\zeta_{n}}\right)
        \vphantom{\left(\frac{\log\left(\left|V\cap X_{\widehat{f}}\right|\right)}{\left|V\cap X_{\widehat{f}}\right|}\right)}
        \right.\nonumber\\&\qquad\qquad\qquad\qquad\;\;\left.
        \vphantom{2 \left(1 + \frac{1}{n}\right)
        \left(\frac{\min\left\lbrace\lambda\left(X\right),\lambda\left(X_{\rm PHS}\right)\right\rbrace}{\zeta_{n}}\right)
        \left(\frac{\log\left(\left|V\cap X_{\widehat{f}}\right|\right)}{\left|V\cap X_{\widehat{f}}\right|}\right)}
    \left(\frac{\log\left(\left|V\cap X_{\widehat{f}}\right|\right)}{\left|V\cap X_{\widehat{f}}\right|}\right)\right)^{\frac{1}{n}}
\end{align}$$ and $$\begin{equation}
\label{eqn:knearest}
    k_{\mathrm{RRT}^*}^*= e\left(1+\frac{1}{n}\right)\log\left(\left|V\cap X_{\widehat{f}}\right|\right),
\end{equation}$$ where $\lambda\left(X_{\rm PHS}\right)$ is a function of the current solution, i.e., [\[eqn:phsMeasure\]](#eqn:phsMeasure){reference-type="eqref" reference="eqn:phsMeasure"}.

:::: {#fig:prune:exp .figure latex-placement="tbp"}
![](Gammell2017Informed_figs/pruningExample_small.png){width="\\columnwidth"}

::: caption
An illustration of pruning a graph found by [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}, (a), with both inadmissible, (b), and admissible, (c), methods. By removing all vertices that cannot belong to a better solution, the inadmissible method may greedily remove descendent vertices that will later provide a better solution once the graph is improved. By only removing vertices that cannot improve a solution if neither can their descendants, the admissible method (Alg. [\[algo:prune\]](#algo:prune){reference-type="ref" reference="algo:prune"}) maintains a uniform sample density in the entire informed set.
:::
::::

These rewiring neighbourhoods will be smaller than [\[eqn:back:radius\]](#eqn:back:radius){reference-type="eqref" reference="eqn:back:radius"} and [\[eqn:back:knearest\]](#eqn:back:knearest){reference-type="eqref" reference="eqn:back:knearest"} when they can contain fewer vertices (i.e., only those in the informed set) and/or a smaller problem measure (i.e., the measure of the informed set). Smaller rewiring neighbourhoods reduce the computational cost of rewiring at each iteration and improves the real-time performance of Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} while maintaining almost-sure asymptotic optimality.

# Rates of Convergence {#sec:rate}

Almost-sure asymptotic optimality provides no insight into the rate at which solutions are improved. Previous work has found probabilistic rates for [PRMstar]{acronym-label="PRMstar" acronym-form="singular+short"} [@dobson_icra15] and [FMTstar]{acronym-label="FMTstar" acronym-form="singular+short"} [@janson_ijrr15] and estimated the expected length of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} solutions as a function of computational time [@dobson_icra15].

Performance can be quantified analytically by evaluating the rate at which the sequence of solution costs converges to the optimum. This rate can be classified as sublinear, linear, or superlinear (Definition [16](#defn:conv){reference-type="ref" reference="defn:conv"}).

::: {#defn:conv .defn}
**Definition 16** (Rate of convergence). *A sequence of numbers, $\left(a_{i}\right)_{i=1}^{\infty}$, that monotonically and asymptotically approaches a limit, $a_\infty$, has a rate of convergence given by $$\begin{equation*}
        \mu\coloneqq \lim_{i\to\infty}\frac{\left|a_{i+1}-a_{\infty}\right|}{\left|a_{i}-a_{\infty}\right|}.
\end{equation*}$$ The sequence is said to converge *linearly* if the rate is in the range $0 < \mu< 1$, *superlinearly* (i.e., faster than linear) when $\mu=0$, and *sublinearly* (i.e., slower than linear) when $\mu=1$.*
:::

The expected convergence rate of an algorithm depends on its tuning and the planning problem. General rates can be calculated for holonomic minimum-path-length problems for [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} with and without sample rejection and Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} (Theorems [18](#thm:conv:rrtstar){reference-type="ref" reference="thm:conv:rrtstar"}--[20](#thm:conv:informed){reference-type="ref" reference="thm:conv:informed"}) by first calculating sharp bounds on the expected next-iteration cost (Lemma [17](#lem:conv:expect){reference-type="ref" reference="lem:conv:expect"}).

::: {#lem:conv:expect .lem}
**Lemma 17** (Expected next-iteration cost of minimum-path-length planning). *The expected value of the next solution to a minimum-path-length problem, $E\left[c_{i+1}\right]$, is bounded by $$\begin{equation}
\label{eqn:lem:conv:expect}
        p_{f}\frac{nc_{i}^2 + c_{\rm min}^2}{\left(n+ 1\right)c_{i}} + \left(1-p_{f}\right)c_{i}\leq E\left[c_{i+1}\right] \leq c_{i},
\end{equation}$$ where $c_{i}$ is the current solution cost, $c_{\rm min}$ is the theoretical minimum solution cost, $n$ is the state dimension of the planning problem, and $p_{f}= P\left(\mathbf{x}_{\rm new}\in X_{f}\right)$ is the probability of adding a state that is a member of the omniscient set (i.e., that can belong to a better solution). While not explicitly shown, the subset, $X_{f}$, and the probability of improving the solution, $p_{f}$, are generally functions of the current solution cost.*

*This lower bound is sharp over the set of all possible minimum-path-length planning problems and algorithm configurations and is exact for versions of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} with an infinite rewiring radius (i.e., $\eta=\infty$, and $r_{\mathrm{RRT}^*}=\infty$) searching an obstacle-free environment without constraints.*
:::

::: proof
*Proof.* The proof of Lemma [17](#lem:conv:expect){reference-type="ref" reference="lem:conv:expect"} from the supplementary online material appears in Appendix [11](#appx:infinite:expect){reference-type="ref" reference="appx:infinite:expect"}. ◻
:::

This result allows sharp bounds on the convergence rates of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} (with and without rejection sampling) and Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} to be calculated for any configuration or holonomic minimum-path-length planning problem. These bounds will be exact in problems without obstacles and constraints and with an infinite rewiring neighbourhood (i.e., $\eta=\infty$, and $r_{\mathrm{RRT}^*}=\infty$) and show that [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} *always* has sublinear convergence to the optimum (Theorem [18](#thm:conv:rrtstar){reference-type="ref" reference="thm:conv:rrtstar"}).

::: {#thm:conv:rrtstar .thm}
**Theorem 18** (Sublinear convergence of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} in holonomic minimum-path-length planning). *[RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} converges *sublinearly* towards the optimum of holonomic minimum-path-length planning problems, $$\begin{equation}
\label{eqn:thm:conv:rrtstar}
        E\left[\mu_{\mathrm{RRT}^*}\right] = 1.
\end{equation}$$*

*For simplicity, this statement is limited to holonomic planning but it can be extended to specific constraints by expanding Lemma [5](#lem:necessary:exact:sample){reference-type="ref" reference="lem:necessary:exact:sample"}.*
:::

::: proof
*Proof.* The proof of Theorem [18](#thm:conv:rrtstar){reference-type="ref" reference="thm:conv:rrtstar"} follows directly from Lemma [17](#lem:conv:expect){reference-type="ref" reference="lem:conv:expect"} when $p_{f}$ is given by [\[eqn:sampleProb\]](#eqn:sampleProb){reference-type="eqref" reference="eqn:sampleProb"} and appears from the supplementary online material in Appendix [12.1](#appx:infinite:rate:rrtstar){reference-type="ref" reference="appx:infinite:rate:rrtstar"}. ◻
:::

Rectangular rejection sampling improves the convergence rate of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}. This improvement is maximized by sampling a rectangle that tightly bounds the informed set (Fig. [6](#fig:sampleTheory){reference-type="ref" reference="fig:sampleTheory"}a). The resulting adaptive rectangular rejection sampling (e.g., [@otte_tro13]) allows [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} to converge linearly in the absence of obstacles and constraints and with an infinite rewiring neighbourhood (Theorem [19](#thm:conv:reject){reference-type="ref" reference="thm:conv:reject"}).

::: {#thm:conv:reject .thm}
**Theorem 19** (Linear convergence of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} with adaptive rectangular rejection sampling in holonomic minimum-path-length planning). *[RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} with adaptive rectangular rejection sampling converges at best *linearly* towards the optimum of holonomic minimum-path-length planning problems but factorially approaches sublinear convergence with increasing state dimension, $$\begin{equation}
\label{eqn:thm:conv:reject}
        1 - \frac{\pi^{\frac{n}{2}}}{\left(n+1\right)2^{n-1}\Gamma\left(\frac{n}{2}+1\right)} \leq E\left[\mu_{\mathrm{Rect}}\right] \leq 1.
\end{equation}$$*

*For simplicity, this statement is limited to holonomic planning but it can be extended to specific constraints by expanding Lemma [5](#lem:necessary:exact:sample){reference-type="ref" reference="lem:necessary:exact:sample"}.*
:::

::: proof
*Proof.* The proof of Theorem [19](#thm:conv:reject){reference-type="ref" reference="thm:conv:reject"} follows directly from Lemma [17](#lem:conv:expect){reference-type="ref" reference="lem:conv:expect"} when $p_{f}$ is calculated by substituting [\[eqn:thm:curse:tightMeasure\]](#eqn:thm:curse:tightMeasure){reference-type="eqref" reference="eqn:thm:curse:tightMeasure"} in [\[eqn:sampleProb\]](#eqn:sampleProb){reference-type="eqref" reference="eqn:sampleProb"} and appears from the supplementary online material in Appendix [12.2](#appx:infinite:rate:reject){reference-type="ref" reference="appx:infinite:rate:reject"}. ◻
:::

This convergence rate diminishes factorially (i.e., quickly) as state dimension increases due to the minimum-path-length curse of dimensionality. Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} avoids this limitation with direct informed sampling. It also converges linearly in the absence of obstacles and constraints and with an infinite rewiring neighbourhood but has a weaker dependence on state dimension (Theorem [20](#thm:conv:informed){reference-type="ref" reference="thm:conv:informed"}).

::: {#thm:conv:informed .thm}
**Theorem 20** (Linear convergence of Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} in holonomic minimum-path-length planning). *Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} converges at best *linearly* towards the optimum of holonomic minimum-path-length planning problems, $$\begin{equation}
\label{eqn:thm:conv:informed}
         \frac{n-1}{n+1} \leq E\left[\mu_{\mathrm{Inf}}\right] \leq 1,
\end{equation}$$ where the lower-bound occurs exactly with an infinite rewiring neighbourhood in the absence of obstacles and constraints.*

*For simplicity, this statement is limited to holonomic planning but it can be extended to specific constraints by expanding Lemma [5](#lem:necessary:exact:sample){reference-type="ref" reference="lem:necessary:exact:sample"}.*
:::

::: proof
*Proof.* The proof of Theorem [20](#thm:conv:informed){reference-type="ref" reference="thm:conv:informed"} follows directly from Lemma [17](#lem:conv:expect){reference-type="ref" reference="lem:conv:expect"} when $p_{f}=1$ and appears from the supplementary online material in Appendix [12.3](#appx:infinite:rate:informed){reference-type="ref" reference="appx:infinite:rate:informed"}. ◻
:::

:::: {#fig:conv:rates .figure latex-placement="tbp"}
![](Gammell2017Informed_figs/theoreticalRates.png){width="\\columnwidth"}

::: caption
An illustration of the lower-bounds on linearity, $E\left[1 - \mu^*\right]$, of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} with rejection sampling and Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} (Corollary [21](#cor:conv:always_better){reference-type="ref" reference="cor:conv:always_better"}). As predicted by Theorems [19](#thm:conv:reject){reference-type="ref" reference="thm:conv:reject"} and [20](#thm:conv:informed){reference-type="ref" reference="thm:conv:informed"}, the convergence rates bounds diverge as state dimensions increase, with rejection sampling factorially approaching sublinear convergence.
:::
::::

:::: {#fig:conv:exp:combo .figure latex-placement="tbp"}
![](Gammell2017Informed_figs/converge_combo.png){width="\\textwidth"}

::: caption
Experimental validation and extension of Lemma [17](#lem:conv:expect){reference-type="ref" reference="lem:conv:expect"} and Theorem [20](#thm:conv:informed){reference-type="ref" reference="thm:conv:informed"} in $\mathbb{R}^2$, $\mathbb{R}^4$ and $\mathbb{R}^8$. Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} was run from a common initial solution $10^4$ times in $\mathbb{R}^2$, $\mathbb{R}^4$ and $\mathbb{R}^8$ with different pseudo-random seeds. The error relative to the known optimum, $\log\left(c_{i}- c^*\right)$, was plotted for each instance at each iteration (cyan lines) along with the mean error (blue circles), a line of best fit (blue dashed line), and the lower-bound error predicted by Lemma [17](#lem:conv:expect){reference-type="ref" reference="lem:conv:expect"} (black line). The difference between the predicted lower bound and the mean errors (red lines), $\left|\left(c_{\mathrm{mean},i}-c_{\mathrm{theory},i}\right)/\left(c_{\mathrm{mean},i}-c^*\right)\right|$, with infinite rewiring neighbourhoods, (a)--(c), confirms experimentally that convergence is linear (Theorem [20](#thm:conv:informed){reference-type="ref" reference="thm:conv:informed"}). The mean error for a finite but *constant* rewiring neighbourhood, (d)--(f), shows experimentally that convergence is slower but possibly still linear. The mean error for a finite and *decreasing* rewiring neighbourhood, (g)--(i), shows experimentally that the is slower and sublinear. The results of (d)--(i) motivate further research on the effects of the [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} rewiring neighbourhood.
:::
::::

Theorems [18](#thm:conv:rrtstar){reference-type="ref" reference="thm:conv:rrtstar"}--[20](#thm:conv:informed){reference-type="ref" reference="thm:conv:informed"} result in the following corollary regarding the relative convergence rates of the algorithms.

::: {#cor:conv:always_better .cor}
**Corollary 21** (The faster convergence of Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} in holonomic minimum-path-length planning). *The best-case convergence rate of Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"}, $\mu_{\mathrm{Inf}}^*$, is always better than that of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}, with or without rejection sampling in holonomic minimum-path-length planning, $$\begin{equation*}
        \forall n \geq 2,\; \frac{n-1}{n+1} = E\left[\mu_{\mathrm{Inf}}^*\right] \leq E\left[\mu_{\mathrm{Rect}}^*\right] \leq E\left[\mu_{\mathrm{RRT}^*}^*\right] = 1.
\end{equation*}$$*

*For simplicity, this statement is limited to holonomic planning but it can be extended to specific constraints by expanding Lemma [5](#lem:necessary:exact:sample){reference-type="ref" reference="lem:necessary:exact:sample"}.*
:::

::: proof
*Proof.* The proof follows immediately from the lower bounds in [\[eqn:thm:conv:rrtstar\]](#eqn:thm:conv:rrtstar){reference-type="eqref" reference="eqn:thm:conv:rrtstar"}, [\[eqn:thm:conv:reject\]](#eqn:thm:conv:reject){reference-type="eqref" reference="eqn:thm:conv:reject"}, and [\[eqn:thm:conv:informed\]](#eqn:thm:conv:informed){reference-type="eqref" reference="eqn:thm:conv:informed"}. It is illustrated in Fig. [11](#fig:conv:rates){reference-type="ref" reference="fig:conv:rates"}. ◻
:::

## Experimental Validation and Extension {#sec:rate:exp}

Convergence rates are investigated experimentally for infinite, constant finite, and decreasing finite rewiring radii. To isolate the effects of the rewiring parameters, Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} was run on obstacle- and constraint-free problems in $\mathbb{R}^2$, $\mathbb{R}^4$, and $\mathbb{R}^8$ for $10^4$ trials of each configuration. Each trial started from the same initial solution but used different pseudo-random seeds to search for improvements. The logarithmic error relative to the known optimum, $\log\left(c_{i}- c^*\right)$, and the resulting mean were calculated at each iteration of each trial and used to validate Theorem [20](#thm:conv:informed){reference-type="ref" reference="thm:conv:informed"} and illustrate the effects of rewiring parameters on the convergence rate.

The experimental results for an infinite rewiring neighbourhood (i.e., $\eta=\infty$ and $r_{\mathrm{RRT}^*}=\infty$) show excellent agreement with the theoretical predictions in Theorem [20](#thm:conv:informed){reference-type="ref" reference="thm:conv:informed"} (Figs. [12](#fig:conv:exp:combo){reference-type="ref" reference="fig:conv:exp:combo"}a--c). The mean solution cost converges linearly towards the optimum and closely matches the lower-bound predicted by Lemma [17](#lem:conv:expect){reference-type="ref" reference="lem:conv:expect"}.

The experimental results for a *constant finite* rewiring neighbourhood (i.e., $\eta = 0.4$ and $r_{\mathrm{RRT}^*}=\infty$) show that the convergence rate is lower than predicted by Theorem [20](#thm:conv:informed){reference-type="ref" reference="thm:conv:informed"} (Figs. [12](#fig:conv:exp:combo){reference-type="ref" reference="fig:conv:exp:combo"}d--f). The convergence rate appears to be initially nonlinear but then become linear. It is hypothesized that this is related to the density of samples relative to the maximum edge length as reflected by $\kappa$ in Theorem [6](#thm:necessary:exact:prob){reference-type="ref" reference="thm:necessary:exact:prob"}.

The experimental results for a *decreasing finite* rewiring neighbourhood (i.e., $\eta = \infty$ and $r_{\mathrm{RRT}^*}=1.1r_{\mathrm{RRT}^*}^*$) show that the convergence rate appears to be sublinear (Figs. [12](#fig:conv:exp:combo){reference-type="ref" reference="fig:conv:exp:combo"}g--i). It is hypothesized that this is a result of the rewiring neighbourhood shrinking 'too' fast relative to the sample density.

These experiments suggest that further research is necessary to study the tradeoff between per-iteration cost and the number of iterations needed to find a solution. While a shrinking rewiring neighbourhood limits the number of rewirings, the apparent resulting sublinear convergence would require significantly more iterations to find high-quality solutions. Alternatively, while linear convergence needs fewer iterations to find equivalent solutions, the required constant radius would allow the number of rewirings to increase indefinitely.

# Experiments {#sec:exp}

Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} was evaluated on simulated problems in $\mathbb{R}^2$, $\mathbb{R}^4$, and $\mathbb{R}^8$ (Sections [7.1](#sec:exp:toy){reference-type="ref" reference="sec:exp:toy"} and [7.2](#sec:exp:grid){reference-type="ref" reference="sec:exp:grid"}) and for [HERB]{acronym-label="HERB" acronym-form="singular+short"} (Section [7.3](#sec:exp:herb){reference-type="ref" reference="sec:exp:herb"}) using [OMPL]{acronym-label="OMPL" acronym-form="singular+short"}. It was compared to the original [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} and versions that focus the search with graph pruning (e.g., Alg. [\[algo:prune\]](#algo:prune){reference-type="ref" reference="algo:prune"}), heuristic rejection on $\mathbf{x}_{\rm new}$, heuristic rejection on $\mathbf{x}_{\rm rand}$, and all three techniques combined.

All planners used the same tuning parameters and the ordered rewiring technique presented in [@perez_iros11]. Planners used a goal-sampling bias of $5\%$ and an [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} radius of $r_{\mathrm{RRT}^*}=2r_{\mathrm{RRT}^*}^*$. The maximum edge length was selected experimentally to reduce the time required to find an initial solution on a training problem, with values of $\eta=0.3$, $0.5$, $0.9$, and $1.3$ used in $\mathbb{R}^2$, $\mathbb{R}^4$, $\mathbb{R}^8$, and on [HERB]{acronym-label="HERB" acronym-form="singular+short"} ($\mathbb{R}^{14}$), respectively. Available planning time was limited for each state dimension to $3$, $30$, $150$, and $600$ seconds, respectively. Planners with heuristics used the $L^2$ norm as estimates of cost-to-come and cost-to-go while those with graph pruning delayed its application until solution cost changed by more than $5\%$.

These experiments were designed to investigate admissible methods to focus search. More advanced extensions of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} were not considered as they commonly include some combination of the investigated techniques.

## Toy Problems {#sec:exp:toy}

Two separate experiments were run in $\mathbb{R}^2$, $\mathbb{R}^4$, and $\mathbb{R}^8$ on randomized variants of the toy problem depicted in Fig. [13](#fig:exp:defn){reference-type="ref" reference="fig:exp:defn"}a to investigate the effects of obstacles on convergence.

The problem consists of a (hyper)cube of width $l$ with a single start and goal located at $\left[-0.5,0,\ldots,0\right]^T$ and $\left[0.5,0,\ldots,0\right]^T$, respectively. A single (hyper)cube obstacle of width $w\sim\mathcal{U}\left[0.25,0.5\right]$ sits between the start and goal in the centre of the problem domain.

The first experiment investigates finding near-optimal solutions in the presence of obstacles. The time required for each planner to find a solution within various fractions of the known optimum, $c^*$, was recorded over $100$ trials with different pseudo-random seeds for maps of width $l=2$. The percentage of trials that found a solution within the target tolerance of the optimum and the median time necessary to do so are presented for each planner in Figs. [14](#fig:exp){reference-type="ref" reference="fig:exp"}a--c. Trials that did not find a suitable solution were treated as having infinite time for the purpose of calculating the median. The results show that Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} performs equivalently to rejection sampling algorithms in low state dimensions but outperforms all existing techniques in higher dimensions.

The second experiment investigates finding near-optimal solutions in large planning problems. The time required for each planner to find a near-optimal solution was recorded over $100$ trials with different pseudo-random seeds for maps of increasing width, $l$. Planners sought a solution better than $1.01c^*$, $1.05c^*$, and $1.15c^*$ in $\mathbb{R}^2$, $\mathbb{R}^4$, and $\mathbb{R}^8$, respectively. The percentage of trials that found a sufficiently near-optimal solution and the median time necessary to do so are presented for each planner in Figs. [14](#fig:exp){reference-type="ref" reference="fig:exp"}d--f. Trials that did not find a suitable solution were treated as having infinite time for the purpose of calculating the median. The results show that Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} outperforms all existing techniques in large-domain planning problems and that the difference increases in higher state dimensions.

These experiments show that increasing problem size and state dimension decreases the ability of nondirect sampling methods to find near-optimal solutions, as predicted by [\[eqn:betterProb\]](#eqn:betterProb){reference-type="eqref" reference="eqn:betterProb"}. Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} limits these effects and outperforms existing techniques by efficiently focusing its search to the $L^2$ informed set using direct informed sampling.

## Worlds with Many Homotopy Classes {#sec:exp:grid}

The algorithms were tested on more complicated problems with many homotopy classes in $\mathbb{R}^2$, $\mathbb{R}^4$, and $\mathbb{R}^8$. The worlds consisted of a (hyper)cube of width $l=4$ with the start and goal located at $\left[-0.5,0,\ldots,0\right]^T$ and $\left[0.5,0,\ldots,0\right]^T$, respectively. The problem domain was filled with a regular pattern of axis-aligned (hyper)cube obstacles with a width such that the start and goal were $5$ 'columns' apart (Fig. [13](#fig:exp:defn){reference-type="ref" reference="fig:exp:defn"}b).

The planners were tested with $100$ different pseudo-random seeds on each world and state dimension. The solution cost of each planner was recorded every $1$ millisecond by a separate thread and the median was calculated from the $100$ trials by interpolating each trial at a period of $1$ millisecond. The absence of a solution was considered an infinite cost for the purpose of calculating the median.

The results are presented in Figs. [14](#fig:exp){reference-type="ref" reference="fig:exp"}g--i, where the percent of trials solved and the median solution cost are plotted versus run time. They demonstrate how Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} has better real-time convergence towards the optimum than existing techniques, especially in higher state dimensions.

:::: {#fig:exp:defn .figure latex-placement="tb"}
![](Gammell2017Informed_figs/probDefn.png){width="\\columnwidth"}

::: caption
Illustrations of the planning problems used for Sections [7.1](#sec:exp:toy){reference-type="ref" reference="sec:exp:toy"} and [7.2](#sec:exp:grid){reference-type="ref" reference="sec:exp:grid"} to study performance relative to a known optimum, the effect of map width, $l$, and performance in problems with many homotopy classes. The width of the obstacle in (a) is a random variable uniformly distributed over the range $\left[0.25,0.5\right]$. The regularly spaced obstacles in (b) are chosen in to scale efficiently to high dimensions and their width is such that the start and goal states are $5$ 'columns' apart.
:::
::::

:::: {#fig:exp .figure latex-placement="tbp"}
![](Gammell2017Informed_figs/experimental_results.png){width="\\textwidth"}

::: caption
Results for the experiments described in Sections [7.1](#sec:exp:toy){reference-type="ref" reference="sec:exp:toy"} and [7.2](#sec:exp:grid){reference-type="ref" reference="sec:exp:grid"}. Each planner was run $100$ different times in $\mathbb{R}^2$, $\mathbb{R}^4$, and $\mathbb{R}^8$ on each problem for $3$, $30$, and $150$ seconds, respectively. The percentage of trials that found the desired solution are plotted above and the median performance is plotted below for each experiment. Unsuccessful trials were assigned an infinite value for the purpose of calculating the median and the error bars denote a nonparamentric $99\%$ confidence interval on the median value. The times required to find different near-optimal solutions, $c_{i}<\gamma c^*$, for the problem illustrated in Fig. [13](#fig:exp:defn){reference-type="ref" reference="fig:exp:defn"}a with $l=2$ are presented in (a)--(c). The times required to find a solution within a fraction of the known optimum ($1.01c^*$, $1.05c^*$, and $1.15c^*$, respectively) for the problem illustrated in Fig. [13](#fig:exp:defn){reference-type="ref" reference="fig:exp:defn"}a for various map widths are presented in (d)--(f). Solution cost is plotted versus run time for the problem illustrated in Fig. [13](#fig:exp:defn){reference-type="ref" reference="fig:exp:defn"}b in (g)--(i). Taken together, these experiments demonstrate the benefits of direct informed sampling even in large or high-dimensional problems, with a high number of obstacles, and many homotopy classes.
:::
::::

## Motion Planning for [HERB]{acronym-label="HERB" acronym-form="singular+abbrv"} {#sec:exp:herb}

Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} was demonstrated on a high-dimensional problem using [HERB]{acronym-label="HERB" acronym-form="singular+short"}, a 14-[DOF]{acronym-label="DOF" acronym-form="singular+short"} mobile manipulation platform [@herb]. Poses were defined for the two arms to create a sequence of three planning problems (Fig. [15](#fig:exp:herb){reference-type="ref" reference="fig:exp:herb"}) inspired by [@ymca]. The objective of these problems was to find the minimum path length through a $14$-dimensional search space with strict limits (each joint has no more than $\pi$--$2\pi$ radians of travel). While path length is not a common cost function for manipulation, these experiments illustrate that direct informed sampling is beneficial in high-dimensional problem domains even with strict search limits.

[RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}, [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} with pruning and rejection, and Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} were each run for $50$ trials on each problem of the cycle. The resulting median path lengths are presented in Fig. [16](#fig:exp:herb:bars){reference-type="ref" reference="fig:exp:herb:bars"}. Trials that did not find a solution were considered to have infinite length for the purpose of calculating the median. This only occurred for the problem from (a) to (b), where the planners found a solution on $94\%$ of the trials.

[RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} with and without pruning and rejection sampling both fail to improve the initial solutions on all three planning problems but Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} is able to improve the path length by $3.9\%$, $7.9\%$, and $28.2\%$, respectively. The improvement for (a) to (b) is not statistically significant but (b) to (c) and (c) to (d) demonstrate the benefits of considering the relative sizes of the informed set and problem domain in high state dimensions.

# Discussion & Conclusion {#sec:fin}

[RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} almost-surely converges asymptotically to the optimum by asymptotically finding the optimal paths to every state in the problem domain. This is inefficient in single-query scenarios as, once a solution is found, searches only need to consider states that can belong to a better solution (i.e., the omniscient set; Definition [3](#defn:omni){reference-type="ref" reference="defn:omni"}, Lemma [4](#lem:necessary:exact){reference-type="ref" reference="lem:necessary:exact"}). Previous work has focused search to estimates of this set (i.e., informed sets; Definition [7](#defn:informed){reference-type="ref" reference="defn:informed"}) but has not used these estimates to analyze performance. This paper proves that for holonomic problems the probability of sampling an admissible informed set provides an upper bound on the probability of improving a solution (Theorem [13](#thm:necessary:heuristic:prob){reference-type="ref" reference="thm:necessary:heuristic:prob"}).

A popular admissible heuristic for problems seeking to minimize path length is the $L^2$ norm (i.e., Euclidean distance). This paper shows that existing techniques to exploit it are insufficient. The majority of approaches either reduce the ability to find solutions in other homotopy classes (i.e., reduce recall; Definition [9](#defn:recall){reference-type="ref" reference="defn:recall"}) or fail to account for the reduction of the $L^2$ informed set in response to solution improvement (i.e., have decreasing precision; Definition [8](#defn:precision){reference-type="ref" reference="defn:precision"}). Even existing adaptive techniques that address these problems (e.g., [@otte_tro13]) fail to account for its factorial decrease in measure with state dimension (i.e., the minimum-path-length curse of dimensionality; Theorem [14](#thm:curse){reference-type="ref" reference="thm:curse"}).

This paper presents a method to avoid these limitations through direct sampling of the $L^2$ informed set (Algs. [\[algo:infset\]](#algo:infset){reference-type="ref" reference="algo:infset"}--[\[algo:randomKeep\]](#algo:randomKeep){reference-type="ref" reference="algo:randomKeep"}; Section [4](#sec:l2){reference-type="ref" reference="sec:l2"}). This approach generates uniformly distributed samples in the informed set regardless of its size relative to the problem domain or the state dimension (i.e., it has $100\%$ recall and high precision). This paper presents Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} as a demonstration of how these techniques can be used in sampling-based planning (Algs. [\[algo:inf_rrtstar\]](#algo:inf_rrtstar){reference-type="ref" reference="algo:inf_rrtstar"} and [\[algo:prune\]](#algo:prune){reference-type="ref" reference="algo:prune"}; Section [5](#sec:inf){reference-type="ref" reference="sec:inf"}).

:::: {#fig:exp:herb .figure latex-placement="tbp"}
![](Gammell2017Informed_figs/herb_small.png){width="\\columnwidth"}

::: caption
A motion planning problem for [HERB]{acronym-label="HERB" acronym-form="singular+abbrv"} inspired by [@ymca]. Planners must find a collision-free path between each pair of subsequent poses, e.g., (a) to (b). [HERB]{acronym-label="HERB" acronym-form="singular+abbrv"}'s $14$ [DOFs]{acronym-label="DOF" acronym-form="plural+abbrv"} and large number of potential self-collisions make this a nontrivial planning problem for [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"}. The planners were given $600$ seconds for each phase of the planning problem and the results are presented in Fig [16](#fig:exp:herb:bars){reference-type="ref" reference="fig:exp:herb:bars"}.
:::
::::

Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} considers all homotopy classes that could provide a better solution (i.e., $100\%$ recall), unlike sample biasing techniques. It is effective regardless of the relative size of the informed set or the state dimension, unlike sample rejection or graph pruning. When the heuristic does not provide any information (e.g., small planning problems and/or large informed sets) it is identical to [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}.

This paper also uses the shape of the $L^2$ informed set to analyze the theoretical performance of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} on minimum-path-length problems (Section [6](#sec:rate){reference-type="ref" reference="sec:rate"}) by bounding the expected solution cost (Lemma [17](#lem:conv:expect){reference-type="ref" reference="lem:conv:expect"}) and convergence rates (Theorems [18](#thm:conv:rrtstar){reference-type="ref" reference="thm:conv:rrtstar"}--[20](#thm:conv:informed){reference-type="ref" reference="thm:conv:informed"}). The bounds are sharp over the set of all (Lemma [17](#lem:conv:expect){reference-type="ref" reference="lem:conv:expect"}) or all holonomic (Theorems [18](#thm:conv:rrtstar){reference-type="ref" reference="thm:conv:rrtstar"}--[20](#thm:conv:informed){reference-type="ref" reference="thm:conv:informed"}) minimum-path-length planning problems and algorithm configurations with the lower bounds exact for an infinite rewiring radius in the absence of obstacles and constraints. These results prove that [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} converges sublinearly (i.e., slower than linear) for all configurations and holonomic minimum-path-length problems and that focused variants (e.g., Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"}) can have linear convergence.

This analysis is extended experimentally to different configurations. The results confirm the theoretical findings and suggest that obstacle- and constraint-free convergence remains linear when the rewiring radius is constant but becomes sublinear when it decreases in the manner proposed by [@karaman_ijrr11]. As previous analysis of this radius has focused on per-iteration complexity, we believe this result motivates future research into the trade off between per-iteration cost and convergence rate.

The practical advantages of Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} are shown on a variety of planning problems (Section [7](#sec:exp){reference-type="ref" reference="sec:exp"}). These experiments demonstrate how its theoretical convergence rate corresponds to better performance on real planning problems. The amount of improvement depends on how efficiently the $L^2$ informed set decreases the search domain and may be limited in small problem domains and/or long circuitous solutions (e.g., the small/low-dimensional problems in Section [7.1](#sec:exp:toy){reference-type="ref" reference="sec:exp:toy"} and the first problem of Section [7.3](#sec:exp:herb){reference-type="ref" reference="sec:exp:herb"}). The design of Alg. [\[algo:multigoal\]](#algo:multigoal){reference-type="ref" reference="algo:multigoal"} assures that in these situations Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} performs no worse than other methods to exploit the $L^2$ heuristic (e.g., rejection sampling).

Designing these experiments highlighted the relationship between the maximum edge length, $\eta$, and algorithm performance. This user-selected value not only affected the time required to find an initial solution but, as a result of [\[eqn:back:rewire\]](#eqn:back:rewire){reference-type="eqref" reference="eqn:back:rewire"}, also the quality of the solution found in finite time. Specifically, large values of $\eta$ appeared to decrease the difference between algorithms; however, also resulted in order of magnitude increases in the time required to find initial solutions. When coupled with the results of Section [7](#sec:exp){reference-type="ref" reference="sec:exp"}, this result should further motivate more research into the effects of the [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} tuning parameters, $\eta$ and $r_{\mathrm{RRT}^*}$, on real-time performance. Given that anytime improvement of a solution is a major feature of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}, we tuned $\eta$ for these experiments to minimize the initial-solution time on a series of independent test problems.

We believe that defining precise and admissible informed sets is a fundamental challenge of using anytime almost-surely asymptotically optimal planners in real-world applications. The $L^2$ informed set is a sharp, uniformly admissible estimate of the omniscient set for problems seeking to minimize path length, even in the presence of constraints, and is exact in the absence of obstacles and constraints. This suggests that any informed set that is more precise must either

::: inparaenum
exploit additional information about the problem domain (e.g., obstacles, constraints), and/or

be inadmissible for some minimum-path-length planning problems.
:::

Finding ways to define new admissible heuristics from additional problem-specific information could potentially allow focused search algorithms to converge linearly in the presence of obstacles and/or constraints.

We ultimately believe that heuristics are a key component of successful planning algorithms. To this end, we are currently investigating methods to extend heuristics to entire sampling-based searches, similar to how A\* [@hart_tssc68] extends Dijkstra's algorithm [@dijkstra_59]. We accomplish this in [BITstar]{acronym-label="BITstar" acronym-form="singular+short"} [@gammell_icra15; @gammell_phd17; @gammell_ijrr18] by extending the ideas presented in this paper to batches of randomly generated samples. These samples are limited to informed sets and searched in order of potential solution quality. Information on [OMPL]{acronym-label="OMPL" acronym-form="singular+short"} implementations of both Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} and [BITstar]{acronym-label="BITstar" acronym-form="singular+short"} are available at [<http://asrl.utias.utoronto.ca/code>](http://asrl.utias.utoronto.ca/code).

:::: {#fig:exp:herb:bars .figure latex-placement="tbp"}
![](Gammell2017Informed_figs/herb_results.png){width="\\columnwidth"}

::: caption
Median path length results from the motion planning problems depicted in Fig. [15](#fig:exp:herb){reference-type="ref" reference="fig:exp:herb"}. Planners found a solution between each pose in every trial after $600$ seconds other than the transition from (a) to (b), where solutions were only found in $94\%$ of the $50$ trials. For the purpose of calculating the median, these unsolved trials were assigned an infinite cost. Error bars denote a nonparamentric $99\%$ confidence interval on the median value. The results show that even in the presence of strict state-space limits, Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} can outperform rejection sampling in high-dimensional problems.
:::
::::

# Proofs of Lemmas [4](#lem:necessary:exact){reference-type="ref" reference="lem:necessary:exact"} and [5](#lem:necessary:exact:sample){reference-type="ref" reference="lem:necessary:exact:sample"} {#appx:necessary}

This section restates and proves Lemmas [4](#lem:necessary:exact){reference-type="ref" reference="lem:necessary:exact"} and [5](#lem:necessary:exact:sample){reference-type="ref" reference="lem:necessary:exact:sample"}.

## Proof of Lemma [4](#lem:necessary:exact){reference-type="ref" reference="lem:necessary:exact"} {#appx:necessary:exact}

::: lem:exact
**Lemma [4](#lem:necessary:exact){reference-type="ref" reference="lem:necessary:exact"} 1** (The necessity of adding states in the omniscient set). *Adding a state from the omniscient set, $\mathbf{x}_{\rm new}\in X_{f}$, is a necessary condition for [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} to improve the current solution, $c_{i}$, $$\begin{equation*}
        c_{i+1}< c_{i}\implies \mathbf{x}_{\rm new}\in X_{f}.
\end{equation*}$$*

*This condition is necessary but not *sufficient* to improve the solution as the ability of states in $X_{f}$ to provide better solutions at any iteration depends on the structure of the tree (i.e., its optimality).*
:::

::: proof
*Proof.* At the end of iteration $i+1$, the cost of the best solution found by [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} will be the minimum of the previous best solution, $c_{i}$, and the best cost of any new or newly improved solutions, $c_{\rm new}$, $$\begin{equation}
\label{eqn:thm:nec:next}
        c_{i+1}= \min\left\lbrace c_{i},c_{\rm new}\right\rbrace.
\end{equation}$$ Each iteration of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} only adds connections to or from the newly added state, $\mathbf{x}_{\rm new}$, and therefore all new or modified paths pass through this new state. The cost of any of these new paths that extend to the goal region will be bounded from below by the cost of the optimal solution of a path through $\mathbf{x}_{\rm new}$, $$\begin{equation}
\label{eqn:thm:nec:improve}
        c_{\rm new}\geq f\left(\mathbf{x}_{\rm new}\right).
\end{equation}$$

Lemma [4](#lem:necessary:exact){reference-type="ref" reference="lem:necessary:exact"} is now proven by contradiction. Assume that [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} has a solution with cost $c_{i}$ after iteration $i$ and that it is improved at iteration $i+1$ by adding a state *not* in the omniscient set, $c_{i+1}< c_{i},\, \mathbf{x}_{\rm new}\not\in X_{f}$. By [\[eqn:fset\]](#eqn:fset){reference-type="eqref" reference="eqn:fset"}, the costs of solutions through any $\mathbf{x}_{\rm new}\not\in X_{f}$ are bounded from below by the current solution, $$\begin{equation*}
        f\left(\mathbf{x}_{\rm new}\right) \geq c_{i},
\end{equation*}$$ which by [\[eqn:thm:nec:improve\]](#eqn:thm:nec:improve){reference-type="eqref" reference="eqn:thm:nec:improve"} is also a bound on the cost of any new or modified solutions, $$\begin{equation*}
        c_{\rm new}\geq f\left(\mathbf{x}_{\rm new}\right) \geq c_{i}.
\end{equation*}$$ By [\[eqn:thm:nec:next\]](#eqn:thm:nec:next){reference-type="eqref" reference="eqn:thm:nec:next"}, the cost of the best solution found by [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} at the end of iteration $i+1$ must therefore be $c_{i}$. This contradicts the assumption that the solution was improved by a state not in the omniscient set and proves Lemma [4](#lem:necessary:exact){reference-type="ref" reference="lem:necessary:exact"}. ◻
:::

## Proof of Lemma [5](#lem:necessary:exact:sample){reference-type="ref" reference="lem:necessary:exact:sample"} {#appx:necessary:sample}

::: lem:sample
**Lemma [5](#lem:necessary:exact:sample){reference-type="ref" reference="lem:necessary:exact:sample"} 1** (The necessity of sampling states in the omniscient set in holonomic planning). *Sampling the omniscient set, $\mathbf{x}_{\rm rand}\in X_{f}$, is a necessary condition for [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} to improve the current solution to a holonomic problem, $c_{i}$, after an initial $\kappa$ iterations, $$\begin{equation*}
        \forall i\geq \kappa,\, c_{i+1}< c_{i}\implies \mathbf{x}_{\rm rand}\in X_{f},
\end{equation*}$$ for any sample distribution that maintains a nonzero probability over the entire omniscient set.*

*For simplicity, this statement is limited to holonomic planning but it can be extended to specific constraints with appropriate assumptions.*
:::

::: proof
*Proof.* In [RRT]{acronym-label="RRT" acronym-form="singular+short"} (and therefore [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}), the distribution of vertices in the graph approaches the sample distribution as the number of iterations approach infinity [@lavalle_tech98]. In the limit, all reachable regions of the problem domain with a nonzero sampling probability will therefore be sampled and the number of vertices in these regions will increase indefinitely with the number of iterations. This ever increasing number of vertices means that the worst-case distance between any state in a sampled subset and the nearest vertex in the graph will decrease indefinitely and monotonically.

Lemma [5](#lem:necessary:exact:sample){reference-type="ref" reference="lem:necessary:exact:sample"} is now proven by contradiction. Assume that by iteration $\kappa$ there are a sufficient number and distribution of vertices in the tree such that all possible states in $X_{f}$ are no further than $\eta$ from a vertex, $$\begin{equation}
\label{eqn:cor:dist}
        \forall \mathbf{x}\in X_{f},\, \exists \mathbf{v}\in V\;\; \mbox{s.t.} \;\;\left\| \mathbf{x}-\mathbf{v} \right\|_{2} < \eta,
\end{equation}$$ and that [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} has a solution with cost $c_{i}$ after iteration $i\geq\kappa$. Now assume that [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} improves the solution at iteration $i+1$ *without* *sampling* the omniscient set, $c_{i+1}< c_{i},\, \mathbf{x}_{\rm rand}\not\in X_{f}$.

As improving a solution requires *adding* a state from the omniscient set, $\mathbf{x}_{\rm new}\in X_{f}$, (Lemma [4](#lem:necessary:exact){reference-type="ref" reference="lem:necessary:exact"}) this implies that the state added to the graph is not the randomly sampled state, $\mathbf{x}_{\rm new}\not=\mathbf{x}_{\rm rand}$. These two states are related in holonomic planning by expansion constraints, [\[eqn:back:nearest\]](#eqn:back:nearest){reference-type="eqref" reference="eqn:back:nearest"} and [\[eqn:back:steer\]](#eqn:back:steer){reference-type="eqref" reference="eqn:back:steer"}, that find a new state as near as possible to $\mathbf{x}_{\rm rand}$ and no further than $\eta$ from the nearest vertex in the tree.

The triangle inequality implies that the nearest vertex to the sample, $\mathbf{v}_{\rm nearest}$, is also the nearest vertex to the proposed new state, $$\begin{equation*}
    \begin{aligned}
        \mathbf{v}_{\rm nearest}&\coloneqq \mathop{\mathrm{arg\,min}}_{\mathbf{v}\in V}\left\lbrace \left\| \mathbf{x}_{\rm rand}- \mathbf{v} \right\|_{2}\right\rbrace\\
                  &\equiv \mathop{\mathrm{arg\,min}}_{\mathbf{v}\in V}\left\lbrace \left\| \mathbf{x}_{\rm new}- \mathbf{v} \right\|_{2}\right\rbrace,
    \end{aligned}
\end{equation*}$$ which from [\[eqn:cor:dist\]](#eqn:cor:dist){reference-type="eqref" reference="eqn:cor:dist"} is bounded in its distance from $\mathbf{x}_{\rm new}$ by $$\begin{equation}
\label{eqn:cor:near_dist}
        \left\| \mathbf{x}_{\rm new}- \mathbf{v}_{\rm nearest} \right\|_{2} < \eta.
\end{equation}$$ Due to [\[eqn:back:steer\]](#eqn:back:steer){reference-type="eqref" reference="eqn:back:steer"}, the relationship in [\[eqn:cor:near_dist\]](#eqn:cor:near_dist){reference-type="eqref" reference="eqn:cor:near_dist"} is only satisfied in holonomic planning when $\mathbf{x}_{\rm new}\equiv\mathbf{x}_{\rm rand}$. As by assumption the random sample is not a member of the omniscient set, $\mathbf{x}_{\rm rand}\not\in X_{f}$, then therefore neither is the newly added state, $\mathbf{x}_{\rm new}\not\in X_{f}$, and by Lemma [4](#lem:necessary:exact){reference-type="ref" reference="lem:necessary:exact"} the solution is not improved, $c_{i+1}= c_{i}$. This contradicts the assumption that the solution was improved by sampling a state not in the omniscient set and proves Lemma [5](#lem:necessary:exact:sample){reference-type="ref" reference="lem:necessary:exact:sample"}. ◻
:::

# Proof of Lemma [15](#lem:uniform){reference-type="ref" reference="lem:uniform"} {#appx:uniform}

This section restates Lemma [15](#lem:uniform){reference-type="ref" reference="lem:uniform"} as presented by [@sun_fusion02] along with a full proof as presented in [@gammell_arxiv14b].

::: lem:uniform
**Lemma [15](#lem:uniform){reference-type="ref" reference="lem:uniform"} 1** (The uniform distribution of samples transformed into a hyperellipsoid from a unit $n$-ball. Originally Lemma 1 in [@sun_fusion02]). *If the random points distributed in a hyperellipsoid are generated from the random points uniformly distributed in a hypersphere through a linear invertible nonorthogonal transformation, then the random points distributed in the hyperellipsoid are also uniformly distributed.*
:::

::: proof
*Proof.* Let the sets $X_{\rm ball}\subset\mathbb{R}^n$ and $X_{\rm ellipse}\subset\mathbb{R}^n$ be the unit $n$-dimensional ball and a $n$-dimensional hyperellipsoid with radii $\left\lbrace r_{j}\right\rbrace_{j=1}^n$, respectively, having measures of $$\begin{align*}
        \lambda\left(X_{\rm ball}\right) &= \zeta_{n},\\
        \lambda\left(X_{\rm ellipse}\right) &= \zeta_{n}\prod_{j=1}^nr_j.
\end{align*}$$ Let $p_{\rm ball}\left(\cdot\right)$ be the probability density function of samples drawn uniformly from the unit $n$-ball such that, $$\begin{equation}
\label{eqn:ballPdf}
        p_{\rm ball}\left(\mathbf{x}\right) \coloneqq
        \begin{cases}
            \dfrac{1}{\zeta_{n}},& \forall\mathbf{x}\in X_{\rm ball}\\
            0,              & \text{otherwise}.
        \end{cases}
\end{equation}$$ Let $\tau\left(\cdot\right)$ be an invertible transformation from the unit $n$-ball to a hyperellipsoid such that, $$\begin{align*}
        \tau&: \; X_{\rm ball}\to X_{\rm ellipse},\\
        \tau^{-1} &: \; X_{\rm ellipse}\to X_{\rm ball}.
\end{align*}$$ By definition, the probability density function in the hyperellipsoid, $p_{\rm ellipse}\left(\cdot\right)$, resulting from applying this transformation to samples distributed in the unit $n$-ball is then $$\begin{equation}
\label{eqn:pdfDefn}
        p_{\rm ellipse}\left(\mathbf{x}\right) \coloneqq p_{\rm ball}\left(\tau^{-1}\left(\mathbf{x}\right)\right) \left|\det\left( \left.\frac{d\tau^{-1}}{d\mathbf{x}_{\rm ellipse}}\right|_{\mathbf{x}} \right) \right|.
\end{equation}$$

The proposed transformation in [\[eqn:transformDefn\]](#eqn:transformDefn){reference-type="eqref" reference="eqn:transformDefn"} has the inverse $$\begin{equation*}
        \tau^{-1}\left(\mathbf{x}_{\rm ellipse}\right) = \mathbf{L}^{-1}\left(\mathbf{x}_{\rm ellipse}- \mathbf{x}_{\rm centre}\right),
\end{equation*}$$ and the Jacobian $$\begin{equation}
\label{eqn:jacobian}
        \frac{d\tau^{-1}}{d\mathbf{x}_{\rm ellipse}} = \mathbf{L}^{-1}.
\end{equation}$$

Substituting [\[eqn:jacobian\]](#eqn:jacobian){reference-type="eqref" reference="eqn:jacobian"} and [\[eqn:ballPdf\]](#eqn:ballPdf){reference-type="eqref" reference="eqn:ballPdf"} into [\[eqn:pdfDefn\]](#eqn:pdfDefn){reference-type="eqref" reference="eqn:pdfDefn"} gives, $$\begin{equation}
\label{eqn:ellipsePdf}
        p_{\rm ellipse}\left(\mathbf{x}\right) \coloneqq 
        \begin{cases}
            \dfrac{1}{\zeta_{n}}\left|\det\left( \mathbf{L}^{-1} \right) \right|,& \forall \mathbf{x}\in X_{\rm ellipse}\\
            0,              & \text{otherwise},
        \end{cases}
\end{equation}$$ using the fact that $\tau^{-1}\left(\mathbf{x}\right) \in X_{\rm ball}\iff \mathbf{x}\in X_{\rm ellipse}$. As $p_{\rm ellipse}\left(\cdot\right)$ is constant for all $\mathbf{x}_{\rm ellipse}\in X_{\rm ellipse}$, this proves that using [\[eqn:transformDefn\]](#eqn:transformDefn){reference-type="eqref" reference="eqn:transformDefn"} to transform uniformly distributed samples in the unit $n$-ball results in a uniform distribution over the hyperellipsoid and proves Lemma [15](#lem:uniform){reference-type="ref" reference="lem:uniform"}.

For hyperellipsoids whose axes are orthogonal (e.g., a prolate hyperspheroid), [\[eqn:ellipsePdf\]](#eqn:ellipsePdf){reference-type="eqref" reference="eqn:ellipsePdf"} can be expressed in a more familiar and intuitive form. Using [\[eqn:transformFinal\]](#eqn:transformFinal){reference-type="eqref" reference="eqn:transformFinal"} for $\tau\left(\cdot\right)$ and the orthogonality of rotation matrices makes [\[eqn:ellipsePdf\]](#eqn:ellipsePdf){reference-type="eqref" reference="eqn:ellipsePdf"} $$\begin{equation}
\label{eqn:orthoPdfTemp}
        p_{\rm ellipse}\left(\mathbf{x}\right) \coloneqq 
        \begin{cases}
            \dfrac{1}{\zeta_{n}}\left|\det\left( \mathbf{L'}^{-1}\mathbf{C}_{\rm we}^T \right) \right|,& \forall \mathbf{x}\in X_{\rm ellipse}\\
            0,              & \text{otherwise}.
        \end{cases}
\end{equation}$$ where $\mathbf{L}' = \mathop{\mathrm{diag}}\left( r_1, r_2, \ldots, r_n \right)$ is a diagonal matrix which then simplifies [\[eqn:orthoPdfTemp\]](#eqn:orthoPdfTemp){reference-type="eqref" reference="eqn:orthoPdfTemp"} to $$\begin{equation}
\label{eqn:orthoPdf}
        p_{\rm ellipse}\left(\mathbf{x}\right) \coloneqq 
        \begin{cases}
            \dfrac{1}{\zeta_{n}\prod_{j=1}^nr_j},& \forall \mathbf{x}\in X_{\rm ellipse}\\
            0,              & \text{otherwise},
        \end{cases}
\end{equation}$$ since the determinant is a linear operator, all rotation matrices have a unity determinant, $\det\left(\mathbf{C}_{\rm we}\right) = 1$, and the determinant of a diagonal matrix is the product of its diagonal entries. As expected, [\[eqn:orthoPdf\]](#eqn:orthoPdf){reference-type="eqref" reference="eqn:orthoPdf"} is the inverse of the volume of an $n$-dimensional hyperellipsoid with radii $\left\lbrace r_j\right\rbrace_{j=1}^n$. ◻
:::

# Proof of Lemma [17](#lem:conv:expect){reference-type="ref" reference="lem:conv:expect"} {#appx:infinite:expect}

This section restates and proves Lemma [17](#lem:conv:expect){reference-type="ref" reference="lem:conv:expect"}, which is used in support of Theorems [18](#thm:conv:rrtstar){reference-type="ref" reference="thm:conv:rrtstar"}--[20](#thm:conv:informed){reference-type="ref" reference="thm:conv:informed"}. An earlier version of this proof appeared in [@gammell_arxiv14].

::: lem:expect
**Lemma [17](#lem:conv:expect){reference-type="ref" reference="lem:conv:expect"} 1** (Expected next-iteration cost of minimum-path-length planning). *The expected value of the next solution to a minimum-path-length problem, $E\left[c_{i+1}\right]$, is bounded by $$\begin{equation*}
        p_{f}\frac{nc_{i}^2 + c_{\rm min}^2}{\left(n+ 1\right)c_{i}} + \left(1-p_{f}\right)c_{i}\leq E\left[c_{i+1}\right] \leq c_{i},\tag{\ref{eqn:lem:conv:expect} redux}
\end{equation*}$$ where $c_{i}$ is the current solution cost, $c_{\rm min}$ is the theoretical minimum solution cost, $n$ is the state dimension of the planning problem, and $p_{f}= P\left(\mathbf{x}_{\rm new}\in X_{f}\right)$ is the probability of adding a state that is a member of the omniscient set (i.e., that can belong to a better solution). While not explicitly shown, the subset, $X_{f}$, and the probability of improving the solution, $p_{f}$, are generally functions of the current solution cost.*

*This lower bound is sharp over the set of all possible minimum-path-length planning problems and algorithm configurations and is exact for versions of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} with an infinite rewiring radius (i.e., $\eta=\infty$, and $r_{\mathrm{RRT}^*}=\infty$) searching an obstacle-free environment without constraints.*
:::

::: proof
*Proof.* Proof of the upper bound is trivial. [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} only accepts new solutions that improve its existing solution, assuring that the cost monotonically decreases, $$\begin{equation}
\label{eqn:lem:infinite:expect:upper} 
        c_{i+1}\leq c_{i}.
\end{equation}$$ Proof of the lower bound comes from finding an exact expression for the expected value of the solution cost found in the absence of obstacles and constraints with an infinite rewiring neighbourhood.

The expected solution cost of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} depends on the probability of sampling the omniscient set, $$\begin{align}
\label{eqn:lem:infinite:expect:expectDefn}
        E\left[c_{i+1}\right] ={} &p_{f}E\left[c_{i+1}\,\middle|\,\mathbf{x}_{\rm new}\in X_{f}\right]\nonumber\\
         &{}+ \left(1-p_{f}\right)E\left[c_{i+1}\,\middle|\,\mathbf{x}_{\rm new}\not\in X_{f}\right],
\end{align}$$ where $p_{f}= P\left(\mathbf{x}_{\rm new}\in X_{f}\right)$. Adding a state from the omniscient set, $X_{f}$, is a necessary condition to improve the solution (Lemma [4](#lem:necessary:exact){reference-type="ref" reference="lem:necessary:exact"}) and any other state will not change the solution cost, $E\left[c_{i+1}\,\middle|\,\mathbf{x}_{\rm new}\not\in X_{f}\right] = c_{i}$. This simplifies [\[eqn:lem:infinite:expect:expectDefn\]](#eqn:lem:infinite:expect:expectDefn){reference-type="eqref" reference="eqn:lem:infinite:expect:expectDefn"} to $$\begin{equation}
\label{eqn:lem:infinite:expect:simpleDefn}
        E\left[c_{i+1}\right] = p_{f}E\left[c_{i+1}\,\middle|\,\mathbf{x}_{\rm new}\in X_{f}\right] + \left(1-p_{f}\right)c_{i}.
\end{equation}$$ The costs of solutions found by adding states inside the omniscient are bounded from below by the optimal path through the newly added state, $$\begin{equation}
\label{eqn:lem:infinite:expect:expect1}
        E\left[c_{i+1}\,\middle|\,\mathbf{x}_{\rm new}\in X_{f}\right] \geq E\left[f\left(\mathbf{x}_{\rm new}\right)\,\middle|\,\mathbf{x}_{\rm new}\in X_{f}\right],
\end{equation}$$ where $f\left(\mathbf{x}\right)$ is the cost of the optimal path from the start to the goal constrained to pass through a state, $\mathbf{x}$. With a uniform sample distribution over $X_{f}$ the right-hand side of [\[eqn:lem:infinite:expect:expect1\]](#eqn:lem:infinite:expect:expect1){reference-type="eqref" reference="eqn:lem:infinite:expect:expect1"} becomes $$\begin{equation*}
        E\left[f\left(\mathbf{x}_{\rm new}\right)\,\middle|\,\mathbf{x}_{\rm new}\in X_{f}\right] = \frac{1}{\lambda\left(X_{f}\right)}\int_{X_{f}} f\left(\mathbf{x}_{\rm new}\right)dV.
\end{equation*}$$

When [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} uses an infinite rewiring radius it attempts connections between every new state and the start and goal. In the absence of obstacles and constraints these paths will be feasible and represent the optimal solutions using the state. This makes the expected value of this best-case configuration of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} equivalent to the expected optimal solution cost in the absence of obstacles, $$\begin{equation}
\label{eqn:lem:infinite:expect:expect2}
        E\left[c_{i+1}\,\middle|\,\mathbf{x}_{\rm new}\in X_{f}\right]^* \equiv E\left[f\left(\mathbf{x}_{\rm new}\right)\,\middle|\,\mathbf{x}_{\rm new}\in X_{f}\right].
\end{equation}$$ The lower bound provided by [\[eqn:lem:infinite:expect:expect1\]](#eqn:lem:infinite:expect:expect1){reference-type="eqref" reference="eqn:lem:infinite:expect:expect1"} is therefore sharp over the set of all possible planning problems and algorithm configurations.

In this absence of obstacles and constraints, the optimal solution using any state is given by [\[eqn:fBelow\]](#eqn:fBelow){reference-type="eqref" reference="eqn:fBelow"} and the omniscient set is the prolate hyperspheroid, $X_{f}\equiv X_{\widehat{f}}\equiv X_{\rm PHS}$. The measure of the omniscient set, $\lambda\left(X_{f}\right)=\lambda_{\rm PHS}$, is given by [\[eqn:phsMeasure\]](#eqn:phsMeasure){reference-type="eqref" reference="eqn:phsMeasure"}. This allows [\[eqn:lem:infinite:expect:expect2\]](#eqn:lem:infinite:expect:expect2){reference-type="eqref" reference="eqn:lem:infinite:expect:expect2"} to be written as $$\begin{align}
\label{eqn:lem:infinite:expect:expect3}
        E\left[c_{i+1}\,\middle|\,\mathbf{x}_{\rm new}\in X_{f}\right]^* = &\frac{1}{\lambda_{\rm PHS}}\int_{X_{\rm PHS}}\left( \left\| \mathbf{x}- \mathbf{x}_{\rm start} \right\|_{2}
                                                   \vphantom{+ \left\| \mathbf{x}_{\rm goal}- \mathbf{x} \right\|_{2}}\right.\nonumber\\
                                                  &\qquad\quad\;\; \left.\vphantom{\left\| \mathbf{x}- \mathbf{x}_{\rm start} \right\|_{2}}
                                                  {}+ \left\| \mathbf{x}_{\rm goal}- \mathbf{x} \right\|_{2}\right)dV.
\end{align}$$

The prolate hyperspheroidal coordinates, $\mu, \nu, \psi_1, \ldots, \psi_{n-2}$, $$\begin{align*}
        x_1 &= a\cosh\mu\cos\nu,\\
        x_2 &= a\sinh\mu\sin\nu\cos\psi_1,\nonumber\\
        x_3 &= a\sinh\mu\sin\nu\sin\psi_1\cos\psi_2,\nonumber\\
        &\vdots\nonumber\\
        x_{n-1} &= a\sinh\mu\sin\nu\sin\psi_1\sin\psi_2\ldots\sin\psi_{n-3}\cos\psi_{n-2},\nonumber\\
        x_{n} &= a\sinh\mu\sin\nu\sin\psi_1\sin\psi_2\ldots\sin\psi_{n-3}\sin\psi_{n-2},\nonumber
\end{align*}$$ and the parameterization $a = 0.5c_{\rm min}$, simplifies [\[eqn:fBelow\]](#eqn:fBelow){reference-type="eqref" reference="eqn:fBelow"} to $$\begin{equation}
\label{eqn:lem:infinite:expect:elliptical}
        f\left(\mathbf{x}\right) = c_{\rm min}\cosh{\mu}.
\end{equation}$$

Substituting [\[eqn:lem:infinite:expect:elliptical\]](#eqn:lem:infinite:expect:elliptical){reference-type="eqref" reference="eqn:lem:infinite:expect:elliptical"} and the prolate hyperspheroidal differential volume, $$\begin{align*}
        dV = a^n\left(\sinh^2\mu + \sin^2\nu\right)& \sinh^{n-2}\mu\sin^{n-2}\nu\sin^{n-3}\psi_1\ldots\\
        &\;\;\sin\psi_{n-3}\,d\mu\,d\nu\,d\psi_1\,\ldots\,d\psi_{n-2},
\end{align*}$$ into [\[eqn:lem:infinite:expect:expect3\]](#eqn:lem:infinite:expect:expect3){reference-type="eqref" reference="eqn:lem:infinite:expect:expect3"} results in $$\begin{align}
\label{eqn:lem:infinite:expect:expect4}
        E&\left[c_{i+1}\,\middle|\,\mathbf{x}_{\rm new}\in X_{f}\right]^* = \frac{c_{\rm min}^{n+1}}{2^n\lambda_{\rm PHS}}\int_{\mu = 0}^{\mu_i}\int_{\nu = 0}^{\pi}\int_{\psi_1 = 0}^{\pi}\nonumber\\
        &\qquad\ldots\int_{\psi_{n-3} = 0}^{\pi}\int_{\psi_{n-2} = 0}^{2\pi} \left(\sinh^2\mu + \sin^2\nu \right)\nonumber\\
        &\qquad\qquad\sinh^{n-2}\mu\cosh\mu\sin^{n-2}\nu\sin^{n-3}\psi_1\nonumber\\
        &\qquad\qquad\ldots \sin\psi_{n-3}\,d\mu\,d\nu\,d\psi_1,\ldots d\psi_{n-2},
\end{align}$$ where the integration limit for $\mu$ is derived from [\[eqn:lem:infinite:expect:elliptical\]](#eqn:lem:infinite:expect:elliptical){reference-type="eqref" reference="eqn:lem:infinite:expect:elliptical"} as $$\begin{equation}
\label{eqn:lem:infinite:expect:cosh_lim}
         \cosh\mu_i\coloneqq \frac{c_{i}}{c_{\rm min}}.
\end{equation}$$

Integrating [\[eqn:lem:infinite:expect:expect4\]](#eqn:lem:infinite:expect:expect4){reference-type="eqref" reference="eqn:lem:infinite:expect:expect4"} requires applying a series of identities, first $$\begin{align*}
        \left(n-1\right)\zeta_{n-1} \equiv \int_{\psi_1 = 0}^{\pi} \ldots &  \int_{\psi_{n-3} = 0}^{\pi} \int_{\psi_{n-2} = 0}^{2\pi}\sin^{n-3}\psi_1 \nonumber\\
        &\ldots \sin\psi_{n-3}\,d\psi_1 \ldots \,d\psi_{n-2},
\end{align*}$$ simplifies [\[eqn:lem:infinite:expect:expect4\]](#eqn:lem:infinite:expect:expect4){reference-type="eqref" reference="eqn:lem:infinite:expect:expect4"} to $$\begin{align}
\label{eqn:lem:infinite:expect:expect5}
        E\left[c_{i+1}\,\middle|\,\mathbf{x}_{\rm new}\in X_{f}\right]^*& = \frac{\left(n-1\right)c_{\rm min}^{n+1}\zeta_{n-1}}{2^n\lambda_{\rm PHS}}\nonumber\\
        &\int_{\mu = 0}^{\mu_i}\int_{\nu = 0}^{\pi}\left(\sinh^2\mu + \sin^2\nu \right)\nonumber\\
        &\sinh^{n-2}\mu\cosh\mu\sin^{n-2}\nu
        \,d\mu\,d\nu.
\end{align}$$ Next, the definite integral of the product of powers of $\sin$ and $\cos$, $$\begin{equation*}
        \int_0^\pi \sin^{2m-1}\theta \cos^{2n-1}\theta \,d\theta \equiv \mathrm{B}\left(m,n\right),
\end{equation*}$$ where $\mathrm{B}\left(\cdot,\cdot\right)$ is the beta function, $$\begin{equation*}
        \mathrm{B}\left(m,n\right) \coloneqq \int_{0}^{1}t^{m-1}\left(1 - t\right)^{n-1}\,dt,
\end{equation*}$$ is used to evaluate the integral over $\nu$ in [\[eqn:lem:infinite:expect:expect5\]](#eqn:lem:infinite:expect:expect5){reference-type="eqref" reference="eqn:lem:infinite:expect:expect5"}, giving $$\begin{align}
\label{eqn:lem:infinite:expect:expect6}
        E&\left[c_{i+1}\,\middle|\,\mathbf{x}_{\rm new}\in X_{f}\right]^* = \frac{\left(n-1\right)c_{\rm min}^{n+1}\zeta_{n-1}}{2^n\lambda_{\rm PHS}}\nonumber\\
        &\qquad\left(
            \mathrm{B}\left(\frac{n-1}{2},\frac{1}{2}\right)
            \int_{\mu = 0}^{\mu_i}
            \sinh^n\mu\cosh\mu
            \,d\mu\right.\nonumber\\
        &\qquad\left. {}+
            \mathrm{B}\left(\frac{n+1}{2},\frac{1}{2}\right)
            \int_{\mu = 0}^{\mu_i}
            \sinh^{n-2}\mu\cosh\mu
            \,d\mu
        \right).
\end{align}$$ The identity, $$\begin{equation*}
        \mathrm{B}\left(m+1,n\right) \equiv \frac{m}{m+n}\mathrm{B}\left(m,n\right),
\end{equation*}$$ and the recursive nature of the $n$-dimensional unit ball, $$\begin{equation*}
        \zeta_{n} \equiv \mathrm{B}\left(\frac{n+1}{2},\frac{1}{2}\right)\zeta_{n-1},
\end{equation*}$$ simplifies [\[eqn:lem:infinite:expect:expect6\]](#eqn:lem:infinite:expect:expect6){reference-type="eqref" reference="eqn:lem:infinite:expect:expect6"} to $$\begin{align}
\label{eqn:lem:infinite:expect:expect7}
        E&\left[c_{i+1}\,\middle|\,\mathbf{x}_{\rm new}\in X_{f}\right]^* \hspace{-0.25ex}=\hspace{-0.25ex} \frac{c_{\rm min}^{n+1}\zeta_{n}}{2^n\lambda_{\rm PHS}}\nonumber
        \left(
            n
            \int_{\mu = 0}^{\mu_i}
            \hspace{-0.5ex}\sinh^n\mu\cosh\mu
            \,d\mu\right.\nonumber\\
        &\quad\qquad\qquad\left. {}+
            \left(n-1\right)
            \int_{\mu = 0}^{\mu_i}
            \sinh^{n-2}\mu\cosh\mu
            \,d\mu
        \right).
\end{align}$$ The indefinite integral, $$\begin{equation*}
        \int\sinh^m\theta\cosh\theta\,d\theta \equiv \frac{\sinh^{m+1}\theta}{m+1},
\end{equation*}$$ is then used to evaluate [\[eqn:lem:infinite:expect:expect7\]](#eqn:lem:infinite:expect:expect7){reference-type="eqref" reference="eqn:lem:infinite:expect:expect7"}, giving $$\begin{align}
\label{eqn:lem:infinite:expect:expect8}
        E&\left[c_{i+1}\,\middle|\,\mathbf{x}_{\rm new}\in X_{f}\right]^* = \frac{c_{\rm min}^{n+1}\zeta_{n}}{2^n\lambda_{\rm PHS}}\nonumber\\
        &\qquad\qquad\qquad
        \left(
            \frac{n}{n+1}\sinh^{n+1}\mu_i
        +
            \sinh^{n-1}\mu_i
        \right).
\end{align}$$ Using [\[eqn:phsMeasure\]](#eqn:phsMeasure){reference-type="eqref" reference="eqn:phsMeasure"} to expand the measure $\lambda_{\rm PHS}$ in [\[eqn:lem:infinite:expect:expect8\]](#eqn:lem:infinite:expect:expect8){reference-type="eqref" reference="eqn:lem:infinite:expect:expect8"} cancels the measure of the unit $n$-ball, giving $$\begin{align}
\label{eqn:lem:infinite:expect:expect9}
        E&\left[c_{i+1}\,\middle|\,\mathbf{x}_{\rm new}\in X_{f}\right]^* = \frac{c_{\rm min}^{n+1}}{c_{i}\left(c_{i}^2 - c_{\rm min}^2\right)^{\frac{n- 1}{2}}}\nonumber\\
        &\qquad\qquad\qquad
        \left(
            \frac{n}{n+1}\sinh^{n+1}\mu_i
        +
            \sinh^{n-1}\mu_i
        \right).
\end{align}$$ Using the relationship $$\begin{equation*}
        \cosh{\mu} = b \iff \sinh{\mu} = \sqrt{b^2 - 1},
\end{equation*}$$ some algebraic manipulation, and [\[eqn:lem:infinite:expect:cosh_lim\]](#eqn:lem:infinite:expect:cosh_lim){reference-type="eqref" reference="eqn:lem:infinite:expect:cosh_lim"} finally simplifies [\[eqn:lem:infinite:expect:expect9\]](#eqn:lem:infinite:expect:expect9){reference-type="eqref" reference="eqn:lem:infinite:expect:expect9"} to $$\begin{equation*}
        E\left[c_{i+1}\,\middle|\,\mathbf{x}_{\rm new}\in X_{f}\right]^* = \frac{nc_{i}^2 + c_{\rm min}^2}{\left(n+1\right)c_{i}},
\end{equation*}$$ an exact value for the best-case expected solution cost of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}. This result allows [\[eqn:lem:infinite:expect:simpleDefn\]](#eqn:lem:infinite:expect:simpleDefn){reference-type="eqref" reference="eqn:lem:infinite:expect:simpleDefn"} to be written as the sharp bound, $$\begin{equation*}
        E\left[c_{i+1}\right] \geq p_{f}\frac{nc_{i}^2 + c_{\rm min}^2}{\left(n+ 1\right)c_{i}} + \left(1-p_{f}\right)c_{i},
\end{equation*}$$ which when combined with [\[eqn:lem:infinite:expect:upper\]](#eqn:lem:infinite:expect:upper){reference-type="eqref" reference="eqn:lem:infinite:expect:upper"} proves Lemma [17](#lem:conv:expect){reference-type="ref" reference="lem:conv:expect"}. ◻
:::

# Proofs of Theorems [18](#thm:conv:rrtstar){reference-type="ref" reference="thm:conv:rrtstar"}--[20](#thm:conv:informed){reference-type="ref" reference="thm:conv:informed"} {#appx:infinite:rate}

This section restates and proves Theorems [18](#thm:conv:rrtstar){reference-type="ref" reference="thm:conv:rrtstar"}--[20](#thm:conv:informed){reference-type="ref" reference="thm:conv:informed"}.

## Proof of Theorem [18](#thm:conv:rrtstar){reference-type="ref" reference="thm:conv:rrtstar"} {#appx:infinite:rate:rrtstar}

::: thm:conv_rrtstar
**Theorem [18](#thm:conv:rrtstar){reference-type="ref" reference="thm:conv:rrtstar"} 1** (Sublinear convergence of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} in holonomic minimum-path-length planning). *[RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} converges *sublinearly* towards the optimum of holonomic minimum-path-length planning problems, $$\begin{equation*}
        E\left[\mu_{\mathrm{RRT}^*}\right] = 1.\tag{\ref{eqn:thm:conv:rrtstar} redux}
\end{equation*}$$*

*For simplicity, this statement is limited to holonomic planning but it can be extended to specific constraints by expanding Lemma [5](#lem:necessary:exact:sample){reference-type="ref" reference="lem:necessary:exact:sample"}.*
:::

::: proof
*Proof.* The expected rate of convergence (Definition [16](#defn:conv){reference-type="ref" reference="defn:conv"}) of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} is $$\begin{equation}
\label{eqn:thm:conv:rrtstar:defn1}
        E\left[\mu_{\mathrm{RRT}^*}\right] = E\left[\lim_{i\to\infty}\frac{c_{i}- c^*}{c_{i-1}- c^*}\right],
\end{equation}$$ since $\forall i,\, c_{i}\geq c^*$. As [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} almost-surely converges asymptotically to the optimum, this sequence also almost-surely converges to a finite value, $0 \leq \mu_{\mathrm{RRT}^*}\leq 1$, $$\begin{equation*}
        P\left(\lim_{i\to\infty}\frac{c_{i}- c^*}{c_{i-1}- c^*} = \mu_{\mathrm{RRT}^*}\right) = 1.
\end{equation*}$$ By Lebesgue's dominated convergence theorem this allows the expectation operator to be brought inside the limit of [\[eqn:thm:conv:rrtstar:defn1\]](#eqn:thm:conv:rrtstar:defn1){reference-type="eqref" reference="eqn:thm:conv:rrtstar:defn1"}, giving $$\begin{equation}
\label{eqn:thm:conv:rrtstar:defn2}
        E\left[\mu_{\mathrm{RRT}^*}\right] = \lim_{i\to\infty}\frac{E\left[c_{i}\right] - c^*}{c_{i-1}- c^*},
\end{equation}$$ since $c_{i}$ is the only random variable at iteration $i$.

Lemma [17](#lem:conv:expect){reference-type="ref" reference="lem:conv:expect"} provides sharp bounds for the expected solution cost at any iteration, $E\left[c_{i}\right]$, with the lower-bound corresponding to an infinite rewiring radius in the absence of obstacles and constraints. Substituting this lower bound and that $c^*=c_{\rm min}$ in the absence of obstacles into [\[eqn:thm:conv:rrtstar:defn2\]](#eqn:thm:conv:rrtstar:defn2){reference-type="eqref" reference="eqn:thm:conv:rrtstar:defn2"} and simplifying gives an expression for the expected *best-case* convergence rate, $$\begin{equation*}
        E\left[\mu_{\mathrm{RRT}^*}^*\right] = 1 +  \frac{1}{\left(n+1\right)}
                                        \lim_{i\to\infty}\frac{
                                                            p_{f}\left(c_{\rm min}^2 - c_{i-1}^2\right)
                                                        }
                                                        {
                                                            \left(c_{i-1}^2 - c_{\rm min}c_{i-1}\right)
                                                        },
\end{equation*}$$ such that $E\left[\mu_{\mathrm{RRT}^*}^*\right] \leq E\left[\mu_{\mathrm{RRT}^*}\right]$ is a sharp bound over all possible planning problems and algorithm configurations. Applying l'Hôpital's rule [@hopitals_rule] with respect to $c_{i-1}$ gives $$\begin{align}
\label{eqn:thm:conv:rrtstar:lhopital}
        E\left[\mu_{\mathrm{RRT}^*}^*\right] = 1 &{}+ \frac{1}{\left(n+1\right)}\nonumber\\
                                        &\quad
                                        \lim_{i\to\infty}\frac{
                                                             \frac{\partial p_{f}}{\partial c_{i-1}}\left(c_{\rm min}^2 - c_{i-1}^2\right)
                                                               - 2p_{f}c_{i-1}
                                                        }
                                                        {
                                                           \left(2c_{i-1}-c_{\rm min}\right)
                                                        }.
\end{align}$$

As iterations go to infinity the probability of adding a sample in $X_{f}$ becomes the probability of sampling it (Lemma [5](#lem:necessary:exact:sample){reference-type="ref" reference="lem:necessary:exact:sample"}). The lower bound from Lemma [17](#lem:conv:expect){reference-type="ref" reference="lem:conv:expect"} is for an obstacle- and constraint-free problem and therefore the informed set is the omniscient set, $X_{f}\equiv X_{\widehat{f}}$, and the probability of sampling it is given by [\[eqn:sampleProb\]](#eqn:sampleProb){reference-type="eqref" reference="eqn:sampleProb"} with a partial derivative of $$\begin{align*}
        \frac{\partial p_{f}}{\partial c_{i-1}} = \frac{\pi^{\frac{n}{2}}}{2^n\Gamma\left(\frac{n}{2} + 1\right)\lambda\left(X_{\rm samp}\right)}
                                                              &\left(c_{i-1}^2 - c_{\rm min}^2\right)^{\frac{n-1}{2}}\\
                                                              &\left(1 + \frac{\left(n-1\right)c_{i-1}^2}{\left(c_{i-1}^2-c_{\rm min}^2\right)} \right).
\end{align*}$$

Almost-sure convergence to $c_{\rm min}$ implies $\lim_{i\to\infty}c_{i-1}=c_{\rm min}$ and therefore $\lim_{i\to\infty}p_{f}=0$ and $\lim_{i\to\infty}\frac{\partial p_{f}}{\partial c_{i-1}}=0$, making [\[eqn:thm:conv:rrtstar:lhopital\]](#eqn:thm:conv:rrtstar:lhopital){reference-type="eqref" reference="eqn:thm:conv:rrtstar:lhopital"}, $$\begin{equation*}
        E\left[\mu_{\mathrm{RRT}^*}^*\right] = 1.
\end{equation*}$$ As by definition the expected rate of convergence of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} is bounded by, $$\begin{equation*}
        E\left[\mu_{\mathrm{RRT}^*}^*\right] \leq E\left[\mu_{\mathrm{RRT}^*}\right] \leq 1,
\end{equation*}$$ this result proves Theorem [18](#thm:conv:rrtstar){reference-type="ref" reference="thm:conv:rrtstar"}. ◻
:::

## Proof of Theorem [19](#thm:conv:reject){reference-type="ref" reference="thm:conv:reject"} {#appx:infinite:rate:reject}

::: thm:conv_reject
**Theorem [19](#thm:conv:reject){reference-type="ref" reference="thm:conv:reject"} 1** (Linear convergence of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} with adaptive rectangular rejection sampling in holonomic minimum-path-length planning). *[RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} with adaptive rectangular rejection sampling converges at best *linearly* towards the optimum of holonomic minimum-path-length planning problems but factorially approaches sublinear convergence with increasing state dimension, $$\begin{equation*}
        1 - \frac{\pi^{\frac{n}{2}}}{\left(n+1\right)2^{n-1}\Gamma\left(\frac{n}{2}+1\right)} \leq E\left[\mu_{\mathrm{Rect}}\right] \leq 1. \tag{\ref{eqn:thm:conv:reject} redux}
\end{equation*}$$*

*For simplicity, this statement is limited to holonomic planning but it can be extended to specific constraints by expanding Lemma [5](#lem:necessary:exact:sample){reference-type="ref" reference="lem:necessary:exact:sample"}.*
:::

::: proof
*Proof.* Proof of Theorem [19](#thm:conv:reject){reference-type="ref" reference="thm:conv:reject"} follows that of Theorem [18](#thm:conv:rrtstar){reference-type="ref" reference="thm:conv:rrtstar"} but with the probability of adding a new state from $X_{f}$ instead calculated from [\[eqn:sampleProb\]](#eqn:sampleProb){reference-type="eqref" reference="eqn:sampleProb"} using [\[eqn:thm:curse:tightMeasure\]](#eqn:thm:curse:tightMeasure){reference-type="eqref" reference="eqn:thm:curse:tightMeasure"}, as $$\begin{equation}
\label{eqn:thm:conv:reject:pdf}
        p_{f} \leq \frac{\pi^{\frac{n}{2}}}{2^n\Gamma\left(\frac{n}{2} + 1\right)}.
\end{equation}$$ As $\frac{\partial p_{f}}{\partial c_{i-1}}=0$, [\[eqn:thm:conv:rrtstar:lhopital\]](#eqn:thm:conv:rrtstar:lhopital){reference-type="eqref" reference="eqn:thm:conv:rrtstar:lhopital"} becomes $$\begin{equation}
\label{eqn:thm:conv:reject:lhopital}
        E\left[\mu_{\mathrm{Rect}}^*\right]  = 1 - \frac{1}{\left(n+1\right)}
                                        \lim_{i\to\infty}\frac{
                                                          2p_{f}c_{i-1}
                                                       }
                                                       {
                                                          \left(2c_{i-1}-c_{\rm min}\right)
                                                       }.
\end{equation}$$ Noting that almost-sure convergence to $c_{\rm min}$ implies $\lim_{i\to\infty}c_{i-1}=c_{\rm min}$ and substituting [\[eqn:thm:conv:reject:pdf\]](#eqn:thm:conv:reject:pdf){reference-type="eqref" reference="eqn:thm:conv:reject:pdf"} into [\[eqn:thm:conv:reject:lhopital\]](#eqn:thm:conv:reject:lhopital){reference-type="eqref" reference="eqn:thm:conv:reject:lhopital"} results in $$\begin{align*}
        E\left[\mu_{\mathrm{Rect}}^*\right] &= 1 - \frac{2p_{f}}{\left(n+1\right)},\\
                             & \geq 1 - \frac{\pi^{\frac{n}{2}}}{\left(n+1\right)2^{n-1}\Gamma\left(\frac{n}{2} + 1\right)}.
\end{align*}$$ As by definition the expected rate of convergence of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} with rectangular rejection sampling is bounded by, $$\begin{equation*}
        E\left[\mu_{\mathrm{Rect}}^*\right] \leq E\left[\mu_{\mathrm{Rect}}\right] \leq 1.
\end{equation*}$$ This result proves Theorem [19](#thm:conv:reject){reference-type="ref" reference="thm:conv:reject"} with sharp bounds over all possible holonomic planning problems and algorithm configurations. ◻
:::

## Proof of Theorem [20](#thm:conv:informed){reference-type="ref" reference="thm:conv:informed"} {#appx:infinite:rate:informed}

::: thm:conv_informed
**Theorem [20](#thm:conv:informed){reference-type="ref" reference="thm:conv:informed"} 1** (Linear convergence of Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} in holonomic minimum-path-length planning). *Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} converges at best *linearly* towards the optimum of holonomic minimum-path-length planning problems, $$\begin{equation*}
         \frac{n-1}{n+1} \leq E\left[\mu_{\mathrm{Inf}}\right] \leq 1,\tag{\ref{eqn:thm:conv:informed} redux}
\end{equation*}$$ where the lower-bound occurs exactly with an infinite rewiring neighbourhood in the absence of obstacles and constraints.*

*For simplicity, this statement is limited to holonomic planning but it can be extended to specific constraints by expanding Lemma [5](#lem:necessary:exact:sample){reference-type="ref" reference="lem:necessary:exact:sample"}.*
:::

::: proof
*Proof.* Proof of Theorem [20](#thm:conv:informed){reference-type="ref" reference="thm:conv:informed"} follows that of Theorem [18](#thm:conv:rrtstar){reference-type="ref" reference="thm:conv:rrtstar"} but with a unity probability of adding a new state from $X_{f}$. From [\[eqn:thm:conv:rrtstar:lhopital\]](#eqn:thm:conv:rrtstar:lhopital){reference-type="eqref" reference="eqn:thm:conv:rrtstar:lhopital"}, the convergence rate of Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"} is then, $$\begin{equation*}
        E\left[\mu_{\mathrm{Inf}}^*\right] = 1 - \frac{1}{\left(n+1\right)}
                                        \lim_{i\to\infty}\frac{
                                                            2c_{i-1}
                                                       }
                                                       {
                                                            \left(2c_{i-1}-c_{\rm min}\right)
                                                       }.
\end{equation*}$$ As almost-sure convergence to $c_{\rm min}$ implies $\lim_{i\to\infty}c_{i-1}= c_{\rm min}$, this gives, $$\begin{equation*}
        E\left[\mu_{\mathrm{Inf}}^*\right] = \frac{n-1}{n+1}.
\end{equation*}$$ As by definition the expected rate of convergence of [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} with rectangular rejection sampling is bounded by, $$\begin{equation*}
        E\left[\mu_{\mathrm{Inf}}^*\right] \leq E\left[\mu_{\mathrm{Inf}}\right] \leq 1.
\end{equation*}$$ This result proves Theorem [20](#thm:conv:informed){reference-type="ref" reference="thm:conv:informed"} with sharp bounds over all possible holonomic planning problems and algorithm configurations. ◻
:::

# Acknowledgment {#acknowledgment .unnumbered}

The authors would like to thank the editorial board and reviewers for their helpful comments. We would also like to thank Laszlo-Peter Berczi for discussions on precision and recall, Christopher Dellin and Michael Koval for discussions and insight on the sampling of arbitrarily overlapping shapes, Jennifer King and Clinton Liddick for help running the [HERB]{acronym-label="HERB" acronym-form="singular+abbrv"} experiments, and Paul Newman for providing the time to finish this manuscript at the University of Oxford.

::: thebibliography
10 url@samestyle

E. W. Dijkstra, " l@English =l@English A note on two problems in connexion with graphs," *l@English =l@English Numerische Mathematik*, vol. 1, no. 1, pp. 269--271, 1959.

P. E. Hart, N. J. Nilsson, and B. Raphael, "A formal basis for the heuristic determination of minimum cost paths," *IEEE Transactions on Systems Science and Cybernetics*, vol. 4, no. 2, pp. 100--107, Jul. 1968.

L. E. Kavraki, P. Švestka, J.-C. Latombe, and M. H. Overmars, "Probabilistic roadmaps for path planning in high-dimensional configuration spaces," *IEEE Transactions on Robotics and Automation*, vol. 12, no. 4, pp. 566--580, 1996.

D. Hsu, R. Kindel, J.-C. Latombe, and S. Rock, "Randomized kinodynamic motion planning with moving obstacles," *The International Journal of Robotics Research*, vol. 21, no. 3, pp. 233--255, 2002.

S. M. LaValle and J. J. Kuffner Jr., "Randomized kinodynamic planning," *The International Journal of Robotics Research*, vol. 20, no. 5, pp. 378--400, 2001.

S. Karaman and E. Frazzoli, "Sampling-based algorithms for optimal motion planning," *The International Journal of Robotics Research*, vol. 30, no. 7, pp. 846--894, 2011.

D. Ferguson and A. Stentz, "Anytime RRTs," in *Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)*, 2006, pp. 5369--5375.

B. Akgun and M. Stilman, "Sampling heuristics for optimal motion planning in high dimensions," in *Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)*, 2011, pp. 2640--2645.

M. Otte and N. Correll, "C-FOREST: Parallel shortest path planning with superlinear speedup," *IEEE Transactions on Robotics (T-RO)*, vol. 29, no. 3, pp. 798--806, Jun. 2013.

I. A. Şucan, M. Moll, and L. E. Kavraki, "The Open Motion Planning Library," *IEEE Robotics & Automation Magazine*, vol. 19, no. 4, pp. 72--82, Dec. 2012, library available from http://ompl.kavrakilab.org.

S. Srinivasa, D. Berenson, M. Cakmak, A. Collet Romea, M. Dogar, A. Dragan, R. A. Knepper, T. D. Niemueller, K. Strabala, J. M. Vandeweghe, and J. Ziegler, "HERB 2.0: Lessons learned from developing a mobile manipulator for the home," *Proceedings of the IEEE*, vol. 100, no. 8, pp. 1--19, Jul. 2012.

J. D. Gammell, S. S. Srinivasa, and T. D. Barfoot, "Informed RRT\*: Optimal sampling-based path planning focused via direct sampling of an admissible ellipsoidal heuristic," in *Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)*, Chicago, Illinois, USA, 14--18 Sep. 2014, pp. 2997--3004.

------, "On recursive random prolate hyperspheroids," Autonomous Space Robotics Lab, University of Toronto, Tech. Rep. TR-2014-JDG002, Mar. 2014, [arXiv:1403.7664 \[math.ST\]](http://arxiv.org/abs/1403.7664).

J. D. Gammell and T. D. Barfoot, "The probability density function of a transformation-based hyperellipsoid sampling technique," Autonomous Space Robotics Lab, University of Toronto, Tech. Rep. TR-2014-JDG004, Apr. 2014, [arXiv:1404.1347 \[math.ST\]](http://arxiv.org/abs/1404.1347).

J. D. Gammell, T. D. Barfoot, and S. S. Srinivasa, "Informed sampling for asymptotically optimal path planning (consolidated version)," Autonomous Space Robotics Lab, University of Toronto, Tech. Rep., Jun. 2017, arXiv: [1706.06454 \[cs.RO\]](https://arxiv.org/abs/1706.06454).

L. Janson, E. Schmerling, A. Clark, and M. Pavone, "Fast marching tree: A fast marching sampling-based method for optimal motion planning in many dimensions," *The International Journal of Robotics Research (IJRR)*, vol. 34, no. 7, pp. 883--921, 2015.

J. Nasir, F. Islam, U. Malik, Y. Ayaz, O. Hasan, M. Khan, and M. S. Muhammad, "RRT\*-SMART: A rapid convergence implementation of RRT\*," *International Journal of Advanced Robotic Systems*, vol. 10, p. 299, 2013.

S. Kiesel, E. Burns, and W. Ruml, "Abstraction-guided sampling for motion planning," in *Proceedings of the Fifth Annual Symposium on Combinatorial Search (SoCS)*, 2012.

D. Kim, J. Lee, and S.-E. Yoon, "Cloud RRT\*: Sampling cloud based RRT\*," in *Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)*, May 2014, pp. 2519--2526.

H. Choset and J. Burdick, "Sensor based planning, part I: The generalized voronoi graph," in *Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)*, vol. 2, May 1995, pp. 1649--1655.

S. Karaman, M. R. Walter, A. Perez, E. Frazzoli, and S. Teller, "Anytime motion planning using the RRT\*," in *Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)*, 2011, pp. 1478--1483.

O. Arslan and P. Tsiotras, "Use of relaxation methods in sampling-based algorithms for optimal motion planning," in *Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)*, 2013.

------, "Dynamic programming guided exploration for sampling-based motion planning algorithms," in *Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)*, May 2015, pp. 4819--4826.

C. Urmson and R. Simmons, "Approaches for heuristically biasing RRT growth," in *Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)*, vol. 2, 2003, pp. 1178--1183.

R. Alterovitz, S. Patil, and A. Derbakova, "Rapidly-exploring roadmaps: Weighing exploration vs. refinement in optimal motion planning," in *Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)*, 2011, pp. 3706--3712.

Y. X. Shan, B. J. Li, J. Zhou, and Y. Zhang, "An approach to speed up RRT\*," in *Proceedings of the IEEE Intelligent Vehicles Symposium (IV)*, Jun. 2014, pp. 594--598.

O. Salzman and D. Halperin, "Asymptotically near-optimal RRT for fast, high-quality, motion planning," in *Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)*, May 2014, pp. 4680--4685.

D. Devaurs, T. Siméon, and J. Cortés, " l@English =l@English Efficient sampling-based approaches to optimal path planning in complex cost spaces," in *l@English =l@English Algorithmic Foundations of Robotics XI*, ser. Springer Tracts in Advanced Robotics, H. L. Akin, N. M. Amato, V. Isler, and A. F. van der Stappen, Eds. Springer International Publishing, 2015, vol. 107, pp. 143--159.

M. Otte and E. Frazzoli, "RRT^X^: Asymptotically optimal single-query sampling-based motion planning with quick replanning," *The International Journal of Robotics Research (IJRR)*, vol. 35, no. 7, pp. 797--822, 2016.

L. Euler, "De progressionibus transcendentibus seu quarum termini generales algebraice dari nequeunt," *Commentarii academiae scientiarum Petropolitanae*, vol. 5, pp. 36--57, 1738.

H. Sun and M. Farooq, "Note on the generation of random points uniformly distributed in hyper-ellipsoids," in *Proceedings of the Fifth International Conference on Information Fusion*, vol. 1, 2002, pp. 489--496.

G. Wahba, "A least squares estimate of satellite attitude," *Society for Industrial and Applied Mathematics (SIAM) Review*, vol. 7, p. 409, 1965.

A. H. J. de Ruiter and J. R. Forbes, " l@English =l@English On the solution of Wahba's problem on SO(n)," *l@English =l@English The Journal of the Astronautical Sciences*, vol. 60, no. 1, pp. 1--31, 2013.

J. D. Gammell, S. S. Srinivasa, and T. D. Barfoot, "Batch informed trees (BIT\*): Sampling-based optimal planning via the heuristically guided search of implicit random geometric graphs," in *Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)*, 2015, pp. 3067--3074.

J. D. Gammell, "Informed anytime search for continuous planning problems," Ph.D. dissertation, University of Toronto, Feb. 2017.

J. D. Gammell, T. D. Barfoot, and S. S. Srinivasa, "Informed asymptotically optimal anytime search," *The International Journal of Robotics Research (IJRR)*, 2018, manuscript #IJR-17-2980, in revision, arXiv: [1707.01888 \[cs.RO\]](https://arxiv.org/abs/1707.01888).

A. Dobson, G. V. Moustakides, and K. E. Bekris, "Geometric probability results for bounding path quality in sampling-based roadmaps after finite computation," in *Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)*, 2015, pp. 4180--4186.

A. Perez, S. Karaman, A. Shkolnik, E. Frazzoli, S. Teller, and M. R. Walter, "Asymptotically-optimal path planning for manipulation using incremental sampling-based algorithms," in *Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)*, 2011, pp. 4307--4313.

J. Morali and V. Willis, "Y.M.C.A." *Cruisin'*, Nov. 13 1978, Casablanca Records NBLP 7118.

J. D. Gammell, T. D. Barfoot, and S. S. Srinivasa, "Informed sampling for asymptotically optimal path planning," *IEEE Transactions on Robotics (T-RO)*, 2018.
:::

::: IEEEbiography
Jonathan D. Gammell is a Departmental Lecturer in Robotics with the Oxford Robotics Institute (ORI) at the University of Oxford, Oxford, United Kingdom. He performed this work at the Autonomous Space Robotics Lab at the University of Toronto, Toronto, Canada during his Ph. D. degree. He is interested in developing conceptually sound approaches to the fundamental problems of real-world autonomous robotics.
:::

::: IEEEbiography
Timothy D. Barfoot is a Professor at the University of Toronto Institute for Aerospace Studies (UTIAS). He holds the Canada Research Chair (Tier II) in Autonomous Space Robotics and works in the area of guidance, navigation, and control of mobile robots in a variety of applications. He is interested in developing methods to allow mobile robots to operate over long periods of time in large-scale, unstructured, three-dimensional environments, using rich onboard sensing (e.g., cameras and laser rangefinders) and computation.

Dr. Barfoot took up his position at UTIAS in May 2007, after spending four years at MDA Space Missions, where he developed autonomous vehicle navigation technologies for both planetary rovers and terrestrial applications such as underground mining. He sits on the editorial boards of the International Journal of Robotics Research and the Journal of Field Robotics. He recently served as the General Chair of Field and Service Robotics (FSR) 2015, which was held in Toronto.
:::

::: IEEEbiography
Siddhartha S. Srinivasa is the Boeing Endowed Professor at the School of Computer Science and Engineering, University of Washington. He works on robotic manipulation, with the goal of enabling robots to perform complex manipulation tasks under uncertainty and clutter, with and around people. To this end, he founded the Personal Robotics Lab in 2005. Dr. Srinivasa is also passionate about building end-to-end systems (HERB, ADA, HRP3, CHIMP, Andy, among others) that integrate perception, planning, and control in the real world. Understanding the interplay between system components has helped produce state of the art algorithms for robotic manipulation, motion planning, object recognition and pose estimation (MOPED), and dense 3D modelling (CHISEL, now used by Google Project Tango), and mathematical models for Human-Robot Collaboration.
:::

[^1]: J. D. Gammell performed this work as a member of the Autonomous Space Robotics Lab at the University of Toronto Institute for Aerospace Studies. He is now with the Oxford Robotics Institute at the University of Oxford, Oxford, United Kingdom. Email: `gammell@robots.ox.ac.uk`

[^2]: T. D. Barfoot is with the Autonomous Space Robotics Lab at the University of Toronto Institute for Aerospace Studies, Toronto, Ontario, Canada. Email: `tim.barfoot@utoronto.ca`

[^3]: S. S. Srinivasa is with the School of Computer Science and Engineering, University of Washington, Seattle, Washington, USA. Email: `siddh@cs.uw.edu`

[^4]: Manuscript submitted June 20, 2017.
