---
citation_key: Gammell2020Asymptotically
arxiv_id: 2009.10484
arxiv_url: https://arxiv.org/abs/2009.10484
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:48:42Z
origin: ai+web
reviewed: false
---

::: acronym
\[BIT\*\]Batch Informed Trees \[BIT\*\]Batch Informed Trees \[FMT\*\]Fast Marching Tree \[PRM\*\]almost-surely asymptotically optimal [PRM]{acronym-label="PRM" acronym-form="singular+abbrv"} \[PRM\*\]almost-surely asymptotically optimal [PRMs]{acronym-label="PRM" acronym-form="plural+abbrv"} \[RRT\*\]almost-surely asymptotically optimal [RRT]{acronym-label="RRT" acronym-form="singular+abbrv"} \[RRT\*\]almost-surely asymptotically optimal [RRTs]{acronym-label="RRT" acronym-form="plural+abbrv"} \[s-PRM\]simplified [PRM]{acronym-label="PRM" acronym-form="singular+abbrv"} \[s-PRM\]simplified [PRMs]{acronym-label="PRM" acronym-form="plural+abbrv"}
:::

::: keywords
robotics, motion planning, robot motion planning, sampling-based planning, optimal motion planning, asymptotically optimal motion planning
:::

# INTRODUCTION {#sec:intro}

Planning is an important task in a number of fields, including computer science and robotics. It consists of finding a sequence of valid states (i.e., a path) between specified positions (i.e., a start and goal) in a search space. Many problems have multiple *feasible* solutions and applications often seek the feasible path that optimizes a cost function (i.e., the *optimal* solution). A feasible solution in robot motion planning is a path that avoids hazards in the environment (i.e., obstacles) and can be followed by the robot (e.g., is kinodynamically feasible). The optimal solution minimizes a user-specified path cost, such as actuator effort or path length.

Optimal planning is difficult because there are often a large number of states to consider and it can be computationally expensive to evaluate them. Graph-search algorithms, such as A\* [@hart_tssc68], can search discrete spaces (e.g., graphs) efficiently with strong formal guarantees. These techniques are guaranteed to find the optimal solution, if one exists, and otherwise return failure (i.e., they are *complete* and *optimal*). A\* is also guaranteed to expand no more states than any other optimal algorithm given the same information [i.e., it is *optimally efficient*; @hart_tssc68].

Robot motion planning search spaces are instead often continuously valued (i.e., infinite sets) since robots can be arbitrarily repositioned in the physical world. These spaces can be approximated with discrete representations and then searched with graph-search algorithms but the performance will depend on the chosen resolution. The resulting discrete solutions will only be resolution complete and resolution optimal relative to the continuous problem.

It can be difficult to select a 'correct' *a priori* discrete approximation in many continuously valued problems. Excessively sparse approximations may preclude finding a (suitable) solution but excessively dense ones can be prohibitively expensive to construct and search. These difficulties are common in robot motion planning where search spaces are often poorly bounded (e.g., planning outdoors), high dimensional (e.g., planning for manipulation), or otherwise expensive to discretize (e.g., kinodynamic systems).

Sampling-based planning algorithms, such as AC@PRM [PRM]{acronym-label="PRM" acronym-form="singular+abbrv"} [@kavraki_tra96] [PRM]{acronym-label="PRM" acronym-form="singular+long"} [[PRM]{acronym-label="PRM" acronym-form="singular+abbrv"}; @kavraki_tra96] , AC@EST [EST]{acronym-label="EST" acronym-form="singular+abbrv"} [@hsu_ijcga99] [EST]{acronym-label="EST" acronym-form="singular+long"} [[EST]{acronym-label="EST" acronym-form="singular+abbrv"}; @hsu_ijcga99] , and AC@RRT [RRT]{acronym-label="RRT" acronym-form="singular+abbrv"} [@lavalle_ijrr01] [RRT]{acronym-label="RRT" acronym-form="singular+long"} [[RRT]{acronym-label="RRT" acronym-form="singular+abbrv"}; @lavalle_ijrr01] , are designed to avoid *a priori* approximations of the search space. They instead use sampling to interleave aspects of approximation and search until a solution is found. This leads to better performance than graph-based methods on many problems but makes formal guarantees probabilistic and dependent on the sampling distribution. Given an appropriate distribution (e.g., uniform sampling), the probability that many of these techniques find a solution, if one exists, goes to one as the number of samples goes to infinity [i.e., they are *probabilistically complete*; @kavraki_tra98; @hsu_ijcga99; @lavalle_ijrr01]. Until recently, there were no equivalent formal statements about the quality of these solutions.

Karaman and Frazzoli [@karaman_ijrr11] present the first formal analysis of probabilistic solution quality in popular sampling-based planning algorithms. They prove that sampling potential states and statically connecting them to the nearest existing vertex, as in [RRT]{acronym-label="RRT" acronym-form="singular+short"}, gives a zero probability of finding the optimal solution, even with an infinite number of samples. They prove that algorithms that consider a higher number of connections, such as AC@sPRM [sPRM]{acronym-label="sPRM" acronym-form="singular+abbrv"} [@kavraki_tra98] [sPRM]{acronym-label="sPRM" acronym-form="singular+long"} [[sPRM]{acronym-label="sPRM" acronym-form="singular+abbrv"}; @kavraki_tra98] , can have a unity probability of asymptotically converging to the optimal solution, if one exists, as the number of samples goes to infinity (i.e., they are *almost-surely asymptotically optimal*). They present a series of algorithms specifically designed to consider a sufficient number of connections to achieve almost-sure asymptotic optimality efficiently: [PRMstar]{acronym-label="PRMstar" acronym-form="singular+short"}, [RRG]{acronym-label="RRG" acronym-form="singular+short"} and [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} [@karaman_ijrr11].

These results have motivated significant recent work on quality guarantees for sampling-based planning algorithms. These include refining the conditions necessary for popular approaches to converge asymptotically to the optimum and designing novel algorithms that find better initial solutions and/or converge faster. This survey summarizes results and algorithms from the field to present an introduction to this exciting work.

The remainder of this survey is organized as follows. Section [2](#sec:back){reference-type="ref" reference="sec:back"} introduces the asymptotically optimal planning problem with a focus on providing a common set of definitions and assumptions for the literature. Section [3](#sec:lit){reference-type="ref" reference="sec:lit"} presents an introductory survey of work in the field, including important theoretical results and effective algorithms. Section [4](#sec:fin){reference-type="ref" reference="sec:fin"} provides a closing summary that includes a discussion of ongoing areas of research interest.

# SAMPLING-BASED MOTION PLANNING {#sec:back}

The optimal planning problem requires solving the underlying feasible problem (**Figure [1](#fig:back:prob_defn){reference-type="ref" reference="fig:back:prob_defn"}**). Section [2.1](#sec:back:pdefn){reference-type="ref" reference="sec:back:pdefn"} presents formal definitions of the planning search space and the feasible and optimal problems. Section [2.2](#sec:back:anal){reference-type="ref" reference="sec:back:anal"} presents definitions of formal performance guarantees for sampling-based planning algorithms in the form of probabilistic statements on finding solutions to the feasible and optimal motion planning problems. Section [2.3](#sec:back:ass){reference-type="ref" reference="sec:back:ass"} summarizes common assumptions made to prove these properties for sampling-based planning algorithms.

:::: {#fig:back:prob_defn .figure latex-placement="tbp"}
![](Gammell2020Asymptotically_figs/prob_defn.png)

::: caption
An illustration of a simple motion planning problem, (a), defined by a search space, $X$, a start, $\mathbf{x}_{\rm start}\in X$, a goal region, $X_{\rm goal}\subset X$, and obstacles, $X_{\rm invalid}\subset X$. Solutions must pass solely through the set of states not in collision with an obstacle, $X_{\rm free}\coloneqq X\setminus X_{\rm invalid}$. For this problem there exists an infinite number of feasible solutions, (b), but only one optimal solution with respect to path length, (c).
:::
::::

## Problem Definitions {#sec:back:pdefn}

Planning problems are defined in a spatial representation of the system. There are a variety of common representations in robot motion planning, including actuator positions (i.e., configuration) and robot pose, possibly including dynamics (i.e., physical state). This survey refers to all robot representations, without loss of generality, as the search space, $X$.

::: marginnote
:::

A subset of the search space may be invalid for use in a solution, $X_{\rm invalid}\subset X$. This invalid set is not always expressible in closed form and for some problems it can only be defined by a noninvertible function, e.g., $X_{\rm invalid}\coloneqq \left\lbrace \mathbf{x}\in X\;\;\middle|\;\;\mathtt{IsInvalid}\left(\mathbf{x}\right)\right\rbrace$ where $\mathtt{IsInvalid}: X\to \left\lbrace \mathtt{true}, \mathtt{false}\right\rbrace$. Invalid states in robot motion planning include self collisions, collisions between the robot and the physical world, and other dangerous or undesirable outcomes. It is often easy to check these conditions for individual states but difficult to enumerate all invalid states, especially when evaluating validity requires mapping between the physical world and configuration space, as in manipulator arms.

The complement of the invalid states is the set of states permitted in a solution, $X_{\rm free}\coloneqq X\setminus X_{\rm invalid}$, where $\setminus$ is the set difference. A planning problem is defined by specifying a start state, $\mathbf{x}_{\rm start}\in X_{\rm free}$, and a goal state or region, $\mathbf{x}_{\rm goal}\in X_{\rm goal}\subset X_{\rm free}$, in this free space. In robot motion planning, the start is the initial robot configuration and the goal may be either an individual state (e.g., a mobile robot pose) or set of states (e.g., the set of arm joint angles for a desired end-effector position).

::: marginnote
:::

A path is a sequence of states through the search space that can be described by a continuous function with bounded variation (i.e., finite length), $$\begin{align*}
    \sigma: \left[ 0, T\right]\to X\;\; \text{s.t.} \;\;\mathrm{TV}\left(\sigma\right) < \infty,\;\; \forall t\in \left[ 0, T\right]\; \lim_{s\to t}\sigma\left(s\right) = \sigma\left(t\right),
\end{align*}$$ where $T\in\mathbb{R}_{>0}$ and $\mathrm{TV}\left(\cdot\right)$ is the total variation of the function [@karaman_ijrr11]. The set of paths passing solely through the free space of a problem is the set of free paths, $$\begin{align*}
    \varSigma_{\rm free}\coloneqq \left\lbrace \sigma\in\varSigma\;\;\middle|\;\;\forall t\in \left[ 0, T\right]\; \sigma\left(t\right) \in X_{\rm free}\right\rbrace,
\end{align*}$$ where $\varSigma$ is the set of all paths. The set of paths between the start and goal of a problem is the set of start-goal paths, $$\begin{align*}
    \varSigma_{\rm start\mhyphen{}goal}\coloneqq \left\lbrace \sigma\in\varSigma\;\;\middle|\;\;\sigma\left(0\right) = \mathbf{x}_{\rm start},\; \sigma\left(T\right) \in X_{\rm goal}\right\rbrace.
\end{align*}$$ The set of paths executable by the system is the set of followable paths, $\varSigma_{\rm follow}$. This followable set is equivalent to the set of all paths for unconstrained holonomic systems. Robotic systems can be unconstrained or subject to a variety of constraints and dynamics, such as in kinodynamic systems (Section [2.3.4](#sec:back:ass:kino){reference-type="ref" reference="sec:back:ass:kino"}).

::: marginnote
:::

A given problem has a solution if the set of feasible paths, $$\begin{align*}
    \varSigma_{\rm feasible}\coloneqq \varSigma_{\rm free}\cap \varSigma_{\rm start\mhyphen{}goal}\cap \varSigma_{\rm follow},
\end{align*}$$ is not empty, i.e., $\varSigma_{\rm feasible}\not= \emptyset$. The feasible motion planning problem is then formally defined as the search for a path from the feasible set (Definition [1](#defn:back:prob:feas){reference-type="ref" reference="defn:back:prob:feas"}).

::: marginnote
:::

::: {#defn:back:prob:feas .defn}
**Definition 1** (Feasible motion planning). *Let $X\subseteq \mathbb{R}^n$ be the $n$-dimensional search space of the planning problem, $X_{\rm invalid}\subset X$ be the set of invalid states, and $X_{\rm free}\coloneqq X\setminus X_{\rm invalid}$ be the resulting set of permissible states. Let $\mathbf{x}_{\rm start}\in X_{\rm free}$ be the initial state and $X_{\rm goal}\subset X_{\rm free}$ be the set of desired goal states. Let $\sigma: \left[ 0, T\right]\to X$ be a continuous function of bounded variation (i.e., a sequence of states) and $\varSigma_{\rm feasible}$ be the set of all such paths connecting the start and goal solely through free space that can be executed by the system.*

*The feasible motion planning problem is then formally defined as finding any feasible path, $\sigma'\in \varSigma_{\rm feasible}$, in the problem if a solution exists, i.e., $\varSigma_{\rm feasible}\not= \emptyset$, and otherwise returning failure.*
:::

There are often multiple feasible paths to a given problem (**Figure [1](#fig:back:prob_defn){reference-type="ref" reference="fig:back:prob_defn"}b**). In some applications, any such path is an appropriate solution but other situations require the path that optimizes a specified cost function (**Figure [1](#fig:back:prob_defn){reference-type="ref" reference="fig:back:prob_defn"}c**). The cost of all paths is assumed to be positive, $$\begin{align*}
    c: \varSigma\to \left[ 0, \infty\right) \;\; \text{s.t.} \;\;c\left(\sigma\right) = 0 \iff \forall t\in \left[ 0, T\right]\; \sigma\left(t\right) = \mathbf{x},
\end{align*}$$ such that all feasible solutions to nontrivial problems have finite and strictly positive costs, $$\begin{align*}
    \mathbf{x}_{\rm start}\not\in X_{\rm goal}\iff \forall \sigma\in \varSigma_{\rm feasible}\; c\left(\sigma\right) > 0.
\end{align*}$$ The optimal cost in a specified problem is then given by the infimum of feasible path costs, $$\begin{align*}
%
    c^{*}\coloneqq \inf\left\lbrace c\left(\sigma\right)\;\;\middle|\;\;\sigma\in\varSigma_{\rm feasible}\right\rbrace,
\end{align*}$$ which defines the set of all optimal paths as $$\begin{align*}
    \varSigma^{*}\coloneqq \left\lbrace \sigma\in\varSigma_{\rm feasible}\;\;\middle|\;\;c\left(\sigma\right) = c^{*}\right\rbrace.
\end{align*}$$ Common cost functions in robotics include path length, control effort, and obstacle clearance.

A given problem has an optimal solution if a feasible path exists with optimal cost, i.e., $\varSigma^{*}\not= \emptyset$. Problems may not have an optimal solution if the costs of feasible paths are an open set. The optimal motion planning problem is then formally defined as the search for a path from the optimal set (Definition [1](#defn:back:prob:opt){reference-type="ref" reference="defn:back:prob:opt"}).

::: marginnote
:::

::: marginnote
:::

::: {#defn:back:prob:opt .defn}
**Definition 1** (Optimal motion planning). *Let $X\subseteq \mathbb{R}^n$ be the $n$-dimensional search space of the planning problem, $X_{\rm invalid}\subset X$ be the set of invalid states, and $X_{\rm free}\coloneqq X\setminus X_{\rm invalid}$ be the resulting set of permissible states. Let $\mathbf{x}_{\rm start}\in X_{\rm free}$ be the initial state and $X_{\rm goal}\subset X_{\rm free}$ be the set of desired goal states. Let $\sigma: \left[ 0, T\right]\to X$ be a continuous function of bounded variation (i.e., a sequence of states) and $\varSigma_{\rm feasible}$ be the set of all such paths connecting the start and goal solely through free space that can be executed by the system. Let $c: \varSigma\to \left[ 0, \infty\right)$ be a cost function such that all nontrivial, feasible paths have finite and strictly positive costs. Let $\varSigma^{*}\coloneqq \left\lbrace \sigma\in \varSigma_{\rm feasible}\;\;\middle|\;\;c\left(\sigma\right) = c^{*}\right\rbrace$ be the set of all feasible paths with optimal cost, $c^{*}$.*

*The optimal motion planning problem is then formally defined as finding any feasible path, $\sigma'\in \varSigma_{\rm feasible}$, in the problem that has optimal cost, i.e., $\sigma'\in \varSigma^{*}$, if an optimal solution exists, i.e., $\varSigma^{*}\not= \emptyset$, and otherwise returning failure.*
:::

## Formal Analysis of Sampling-based Motion Planners {#sec:back:anal}

Sampling-based motion planners attempt to solve the feasible and optimal motion planning problems by sampling the search space. These samples are used to approximate and search the problem and can allow the algorithms to be applied to continuously valued spaces without *a priori* finite discretizations. They also make algorithm performance a function of the number and specific sequence of samples and weaken formal guarantees.

It is common to evaluate sampling-based planning performance as a function of the number of samples probabilistically over all possible realizations of a chosen sampling distribution. Algorithms with a probability of solving feasible motion planning problems that goes to one with infinite samples are described as probabilistically complete (Definition [1](#defn:back:anal:pc){reference-type="ref" reference="defn:back:anal:pc"}) in the sampling-based planning literature [e.g., @kavraki_tra98; @hsu_ijcga99; @lavalle_ijrr01; @karaman_ijrr11].

::: marginnote
:::

::: {#defn:back:anal:pc .defn}
**Definition 1** (Probabilistic completeness). *A sampling-based motion planning algorithm is said to be *probabilistically complete* if the probability it returns a feasible path, if such a path exists, goes to one as the number of samples goes to infinity, $$\begin{align*}
        \liminf_{q\to\infty} P\left(\varSigma_{q}\not= \emptyset\right) = 1,
\end{align*}$$ where $q$ is the number of samples and $\varSigma_{q}\subset\varSigma_{\rm feasible}$ is the set of feasible paths found by the planner from those samples. The probability is calculated over all possible runs of the algorithm, i.e., all realizations of the sampling distribution.*
:::

Karaman and Frazzoli [@karaman_ijrr11] extend the probabilistic analysis of sampling-based planning algorithms to consider asymptotic quality. They not only provide a definition of probabilistic convergence to the optimum but also show that [RRT]{acronym-label="RRT" acronym-form="singular+short"} and variants of [PRM]{acronym-label="PRM" acronym-form="singular+short"} have zero probability of doing so. They refer to algorithms that have unity probability of asymptotically converging towards an optimal solution with infinite samples as almost-surely asymptotic optimal (Definition [1](#defn:back:anal:asao){reference-type="ref" reference="defn:back:anal:asao"}) and show that variants of [sPRM]{acronym-label="sPRM" acronym-form="singular+short"} and the algorithms [PRMstar]{acronym-label="PRMstar" acronym-form="singular+short"}, [RRG]{acronym-label="RRG" acronym-form="singular+short"}, and [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} have this property. This work has since been refined and extended with new analysis (Section [3.1](#sec:lit:form){reference-type="ref" reference="sec:lit:form"}) and to the mathematically weaker concept of being asymptotically optimal in probability (Definition [1](#defn:back:anal:aop){reference-type="ref" reference="defn:back:anal:aop"}). Proving asymptotic optimality almost surely or in probability by definition implies probabilistic completeness.

::: marginnote
:::

::: {#defn:back:anal:asao .defn}
**Definition 1** (Almost-sure asymptotic optimality). *A sampling-based motion planning algorithm is said to converge asymptotically *almost surely* if it has unity probability of converging asymptotically to an optimal solution, if such a path exists, as the number of samples goes to infinity, $$\begin{align*}
        P\left(\limsup_{q\to\infty} \min_{\sigma\in\varSigma_{q}}\left\lbrace c\left(\sigma\right)\right\rbrace = c^{*}\right) = 1,
\end{align*}$$ where $q$ is the number of samples, $\varSigma_{q}\subset\varSigma_{\rm feasible}$ is the set of feasible paths found by the planner from those samples, $c: \varSigma\to \left[ 0, \infty\right)$ is the cost of a path, and $c^{*}$ is the optimal solution to the planning problem. The probability is calculated over all possible runs of the algorithm, i.e., all realizations of the sampling distribution.*
:::

::: marginnote
:::

::: {#defn:back:anal:aop .defn}
**Definition 1** (Asymptotic optimality in probability). *A sampling-based motion planning algorithm is said to converge asymptotically *in probability* if the probability that the best solution cost is more than any positive constant, $\epsilon > 0$, worse than the optimum, if such a path exists, goes to zero as the number of samples goes to infinity, $$\begin{align*}
        \forall \epsilon > 0,\;\; \limsup_{q\to \infty} P\left(\left(\min_{\sigma\in\varSigma_{q}}\left\lbrace c\left(\sigma\right)\right\rbrace - c^{*}\right) > \epsilon \right) = 0,
\end{align*}$$ where $q$ is the number of samples, $\varSigma_{q}\subset\varSigma_{\rm feasible}$ is the set of feasible paths found by the planner after those samples, $c: \varSigma\to \left[ 0, \infty\right)$ is the cost of a path, and $c^{*}$ is the optimal solution to the planning problem. The probability is calculated over all possible runs of the algorithm, i.e., all realizations of the sampling distribution.*
:::

Karaman and Frazzoli [@karaman_ijrr11] note that all planning algorithms are provably either asymptotically optimal with probability one or zero [i.e., almost surely or almost never; Lemma 25; @karaman_ijrr11],

::: extract
a sampling-based algorithm either converges to the optimal solution in almost all runs, or the convergence does not occur in almost all runs.
:::

A corollary of this lemma is that running a sequence of nonasymptotically optimal algorithms, as in Anytime [RRTs]{acronym-label="RRT" acronym-form="plural+abbrv"} [@ferguson_iros06], is not sufficient to achieve almost-sure asymptotically optimality. The set of optimal solutions in most practical planning problems has zero measure and therefore all sampling-based planning algorithms have zero probability of sampling an optimal solution in finite time [Lemma 28; @karaman_ijrr11],

::: extract
no sampling-based planning algorithm can find a solution to the optimality problem in a finite number of iterations.
:::

## Assumptions {#sec:back:ass}

Formal analysis of sampling-based planners requires making assumptions about the properties of the optimal motion planning problem. These commonly include aspects of the search space (Section [2.3.1](#sec:back:ass:space){reference-type="ref" reference="sec:back:ass:space"}), solutions (Section [2.3.2](#sec:back:ass:soln){reference-type="ref" reference="sec:back:ass:soln"}), and cost function (Section [2.3.3](#sec:back:ass:cost){reference-type="ref" reference="sec:back:ass:cost"}). These assumptions can also be modified and extended to provide formal analysis of planning performance for kinodynamic systems (Section [2.3.4](#sec:back:ass:kino){reference-type="ref" reference="sec:back:ass:kino"}).

### Search space assumptions {#sec:back:ass:space}

The search space is assumed in [@karaman_ijrr11] to be Euclidean and an open unit $n$-dimensional (hyper)cube, $X\coloneqq \left( 0, 1\right)^n$, as in works by Kavraki et al. [@kavraki_tra98] and others. Spaces that are not a unit cube and/or Euclidean must be scaled appropriately and/or behave locally as a Euclidean space. The free space is then taken as the closed complement of this search space and the invalid set, $X_{\rm free}\coloneqq \mathrm{cl}\left(X\setminus X_{\rm invalid}\right)$, where $\mathrm{cl}\left(\cdot\right)$ denotes the closure of a set. The closed free set ensures that a feasible path exists with optimal cost for all feasible planning problems, i.e., $\varSigma_{\rm feasible}\not= \emptyset \iff \varSigma^{*}\not= \emptyset$.

Janson et al. [@janson_ijrr15] refine these assumptions for planning problems to a goal region to ensure that samples can be drawn near the goal boundary with a nonzero probability. A goal region is described as $\xi$-regular if its boundary, $\partial X_{\rm goal}$, has bounded curvature everywhere. This is expressed by requiring that every state in the goal boundary also lies on the boundary of a $\xi$-radius subset of the goal region, $B\left(\mathbf{y}, \xi\right) \subseteq X_{\rm goal}$, where $\xi>0$, i.e., $$\begin{align}
    \forall \mathbf{x}\in \partial X_{\rm goal}\; \exists B\left(\mathbf{y}, \xi\right)\subseteq X_{\rm goal}\;\; \text{s.t.} \;\;\mathbf{x}\in \partial B\left(\mathbf{y}, \xi\right),\nonumber
%
    \shortintertext{where}%
%
    %
    B\left(\mathbf{y}\in X, r\in \mathbb{R}_{>0}\right) \coloneqq \left\lbrace \mathbf{z}\in X\;\;\middle|\;\;\left\| \mathbf{z}- \mathbf{y} \right\|_{2} \leq r\right\rbrace\label{eqn:back:ball}
\end{align}$$ is an $n$-dimensional ball of radius $r$ centred at $\mathbf{y}$ and $\partial$ denotes the boundary of the specified set.

### Solution assumptions {#sec:back:ass:soln}

The probability of sampling a state that could belong to a feasible path is proportional to the measure of the set of all feasible paths relative to that of the sampling domain. A sufficient condition for this probability to be nonzero when sampling uniformly is for there to exist a feasible path that remains a finite distance from obstacles for its entire length (**Figure [2](#fig:back:prob_assume){reference-type="ref" reference="fig:back:prob_assume"}a**). Such paths are described as having strong $\delta$-clearance and the set of all such paths is given by $$\begin{align*}
    \varSigma_{\delta\mhyphen\mathrm{clear}}\coloneqq \left\lbrace \sigma\in \varSigma_{\rm free}\;\;\middle|\;\;\exists \delta>0 \;\; \text{s.t.} \;\;\forall t\in \left[ 0, T\right]\; B\left(\sigma\left(t\right), \delta\right) \subseteq X_{\rm free}\right\rbrace
\end{align*}$$ where $B\left(\sigma\left(t\right), \delta\right)$ is a $\delta$-radius ball centred at $\sigma\left(t\right)$ as defined by Equation [\[eqn:back:ball\]](#eqn:back:ball){reference-type="ref" reference="eqn:back:ball"}.

::: marginnote
:::

A planning problem containing a feasible path with strong $\delta$-clearance is described as robustly feasible. Sampling-based motion planners have zero probability of solving problems where all solutions do not have strong $\delta$-clearance, i.e., problems that are not robustly feasible (**Figure [2](#fig:back:prob_assume){reference-type="ref" reference="fig:back:prob_assume"}c**).

:::: {#fig:back:prob_assume .figure latex-placement="tbp"}
![](Gammell2020Asymptotically_figs/prob_assume.png)

::: caption
An illustration of separate paths with strong $\delta$-clearance (a), weak $\delta$-clearance (b), and no $\delta$-clearance (c). Probabilistically complete sampling-based motion planners have a probability of finding a feasible path with strong $\delta$-clearance, e.g., $\sigma_{\mathrm{strong}\mhyphen\delta}$, that goes to one as the number of samples goes to infinity. Asymptotically optimal sampling-based motion planners have unity probability of converging to the optimal path with weak $\delta$-clearance, $\sigma_{\mathrm{weak}\mhyphen\delta}$, as the number of samples goes to infinity. Sampling-based motion planners have zero probability of solving problems where all solutions do not have $\delta$-clearance, $\sigma_{\mathrm{no}\mhyphen\delta}$.
:::
::::

The set of optimal solutions has zero measure and therefore zero probability of being sampled in most practical problems, even if the problem is robustly feasible. Asymptotically optimal sampling-based planning algorithms instead converge towards an optimal solution from suboptimal paths (**Figure [2](#fig:back:prob_assume){reference-type="ref" reference="fig:back:prob_assume"}b**). Optimal solutions often pass infinitely close to obstacles and are described as having weak $\delta$-clearance if they are homotopic to a strong $\delta$-clearance path, i.e., $$\begin{align*}
    \exists H: \left[ 0, 1\right] \to \varSigma_{\rm free}\;\; \text{s.t.} \;\;H\left(0\right) = \sigma^{*},\; H\left(1\right) = \sigma',\; \forall s\in \left( 0, 1\right]\; H\left(s\right) \in \varSigma_{\delta\mhyphen\mathrm{clear}},
\end{align*}$$ where $\sigma^{*}\in \varSigma_{\rm free}$ is an optimal solution, $\sigma'\in \varSigma_{\delta\mhyphen\mathrm{clear}}$ is a robustly feasible solution, and $H$ is a homotopic map between the two.

Janson et al. [@janson_ijrr15] note that this homotopy requirement can be "vacuously satisfied" (p. 886) and seek to refine the mathematical definition. They state the assumption as the existence of an infinite sequence of strong $\delta_i$-clearance paths, $\left(\sigma_{i}\right)_{i=1}^{\infty}$, such that the limit of this sequence has optimal cost, i.e., $$\begin{align*}
    \exists \left(\sigma_{i}\right)_{i=1}^{\infty} \;\; \text{s.t.} \;\;\lim_{i\to\infty} c\left(\sigma_{i}\right) = c^{*},\; \forall i\in \mathbb{N}\; \sigma_i\in \varSigma_{\delta_{i}\mhyphen\mathrm{clear}},
\end{align*}$$ where the sequence of clearances, $\left(\delta_{i}\right)_{i=1}^{\infty}$, is positive, $\forall i\in \mathbb{N}\;\; 0 < \delta_i\leq \delta$, and converges to zero, $\lim_{i\to\infty}\delta_i= 0$.

A planning problem with at least one optimal solution that can be continuously transformed to a strong $\delta$-clearance path is referred to as robustly optimal [@karaman_ijrr11] or $\delta$-robustly feasible [@janson_ijrr15]. Asymptotically optimal techniques cannot converge towards any other optima, i.e., cannot asymptotically solve optimal planning problems that are not robustly optimal or $\delta$-robustly feasible (**Figure** [2](#fig:back:prob_assume){reference-type="ref" reference="fig:back:prob_assume"}c).

Solovey and colleagues [@solovey_ijrr19; @solovey_icra20] define the robust optimum, $c^{*}_{\delta\mhyphen\mathrm{clear}}$, as the infimum of the $\delta$-clearance paths, $$\begin{align*}
    c^{*}_{\delta\mhyphen\mathrm{clear}}\coloneqq \inf\left\lbrace c\left(\sigma\right)\;\;\middle|\;\;\sigma\in\varSigma_{\delta\mhyphen\mathrm{clear}}\right\rbrace.
\end{align*}$$ This cost will be equivalent to the true optimum in problems that contain at least one optimal solution with weak $\delta$-clearance, i.e., one optimal solution that can be continuously transformed to a strong $\delta$-clearance path.

::: marginnote
:::

### Cost assumptions {#sec:back:ass:cost}

Asymptotic convergence towards the optimum requires a well-behaved cost function. While a variety of assumptions are made about the function in subsequent analysis, the most basic assumption is that it is bounded for paths in free space and monotonic such that the cost of any path cannot be smaller than its subpaths, $$\begin{align*}
    \forall \sigma_1,\sigma_2 \in \varSigma\;\quad c\left(\sigma_1\right) \leq c\left(\sigma_1 \middle| \sigma_2\right)\;\; \text{and}\;\; c\left(\sigma_2\right) \leq c\left(\sigma_1 \middle| \sigma_2\right),
\end{align*}$$ where $\left.\middle|\right.$ is the concatenation of two paths and is defined as $$\begin{align*}
    \forall t\in \left[ 0, T_{\sigma_1} + T_{\sigma_2}\right]\;\left.\sigma_1 \middle| \sigma_2\right. \coloneqq
      \begin{cases}
           \sigma_1\left(t\right),         & 0 \leq t\leq T_{\sigma_1}\\
           \sigma_2\left(t- T_{\sigma_1}\right),     & T_{\sigma_1} < t\leq T_{\sigma_1} + T_{\sigma_2}
      \end{cases},
\end{align*}$$ where $T_{\sigma_1}$ and $T_{\sigma_2}$ are the limits of the individual paths.

::: marginnote
:::

### Kinodynamic Systems {#sec:back:ass:kino}

The initial formal analysis of asymptotically optimal sampling-based motion planning algorithms focused on geometric motion planning in the absence of dynamics or constraints, i.e., $\varSigma_{\rm follow}= \varSigma$. This analysis has been extended to consider the dynamic systems often found in robotics. These systems are often described by a dynamical equation that relates the evolution of the state to control inputs (i.e., *kinodynamics*). This limits the set of followable paths to those that satisfy the differential equation of motion, $$\begin{align*}
    \varSigma_{\rm follow}\coloneqq \left\lbrace \sigma\in\varSigma\;\;\middle|\;\;\forall t\in\left[ 0, T\right],\;\; \exists\psi\in\varPsi\;\; \text{s.t.} \;\;\dot{\sigma}\left(t\right)=f\left(\sigma\left(t\right),\psi\left(t\right)\right)\right\rbrace.
\end{align*}$$ where $f\left(\cdot,\cdot\right)$ defines a time-invariant dynamical system and $\varPsi\coloneqq\left\lbrace \psi\right\rbrace$ is the set of all control sequences, $\psi: \left[ 0, T\right]\to U$, in the control space of the robot, $U\subseteq\mathbb{R}^m$. The path is fully defined by an initial state, $\sigma\left(0\right) = \mathbf{x}_{\rm start}$, and the control sequence, which makes kinodynamic motion planning the search for a sequence of controls, $\psi'\in\varPsi$, that solves the posed problem.

Optimal kinodynamic motion planning problems often seek to minimize the cost of the path and control effort in the form, $$\begin{align*}
    c\left(\sigma,\psi\right) \coloneqq \int_{0}^{T} \mathfrak{c}\left(\sigma\left(t\right),\psi\left(t\right)\right)dt,
\end{align*}$$ where the integrand, $\mathfrak{c}\left(\cdot,\cdot\right)$, is the *cost derivative* and maps from the search and control spaces to a cost, $$\begin{align*}
    \mathfrak{c}: X\times U\to \left[ 0, \infty\right).
\end{align*}$$

Formally analyzing the asymptotic optimality of kinodynamic motion planning algorithms requires additional assumptions that are not summarized here. These include statements about the controllability of the dynamical system, the nature of the cost function, and other properties of the problem, including whether the dynamical equation can be solved analytically for arbitrary end conditions (i.e., the existence of a 'steering' function). Kinodynamic motion planning is often considered in the presence of kinodynamic constraints (Section [3.3.3](#sec:lit:cnst:kino){reference-type="ref" reference="sec:lit:cnst:kino"}).

# ASYMPTOTICALLY OPTIMAL SAMPLING-BASED MOTION PLANNING {#sec:lit}

Asymptotically optimal sampling-based motion planning is a popular research topic. This section presents an introductory survey of approximately half of the more than 300 academic articles published since 2010, as necessitated by the limits of this article. While many of these works address multiple questions, general areas of research include refining and extending formal analysis (Section [3.1](#sec:lit:form){reference-type="ref" reference="sec:lit:form"}), improving practical performance (Section [3.2](#sec:lit:fast){reference-type="ref" reference="sec:lit:fast"}), supporting constraints and specifications (Section [3.3](#sec:lit:cnst){reference-type="ref" reference="sec:lit:cnst"}), and applying algorithms to a variety of problems in robotics (Section [3.4](#sec:lit:app){reference-type="ref" reference="sec:lit:app"}).

## Formal Analysis {#sec:lit:form}

A primary area of research interest is refining and extending the formal analysis of asymptotic optimality first presented in [@karaman_ijrr11]. This includes tightening the bounds that guarantee asymptotic optimality almost surely or in probability (Section [3.1.1](#sec:lit:form:bound){reference-type="ref" reference="sec:lit:form:bound"}), developing relaxed bounds for asymptotic convergence to *near optimal* solutions (Section [3.1.2](#sec:lit:form:near){reference-type="ref" reference="sec:lit:form:near"}), and extending analysis to evaluate rates of convergence (Section [3.1.3](#sec:lit:form:rate){reference-type="ref" reference="sec:lit:form:rate"}).

### Analytic Bounds {#sec:lit:form:bound}

The almost-sure asymptotic optimality presented in [@karaman_ijrr11] is a result of considering multiple connections per sample. The number of connections necessary are presented as a function of state measure (e.g., volume), state dimension, and the number of existing vertices. These expressions define either the minimum number of nearest vertices (e.g., $k$-nearest) or the maximum distance to consider (e.g., $r$-disc) when adding new samples.

The computational cost of sampling-based planning algorithms depends on the number of these connections required to be considered for each new sample. Significant research has worked to develop tighter bounds and/or alternative analysis for other algorithms to reduce the number of connections while maintaining asymptotic convergence to the optimum, sometimes by making more specific assumptions about the planning problem. Research has included addressing limitations in the original analysis [@solovey_icra20], relaxing asymptotic optimality to convergence in probability [@huynh_cdc14; @janson_ijrr15], and developing alternative analysis and refined expressions for connectivity, including with different sampling and graph models [@bera_isic13; @janson_ijrr18; @solovey_ijrr18; @solovey_ijrr19]. It has also investigated necessary conditions for asymptotic convergence when planning for kinodynamic systems [@li_ijrr16], including in an augmented state-cost search space [@hauser_tro16; @kleinbort_icra20], and integrated task and motion planning problems [@vegabrown_wafr20; @shome_wafr20]. These bounds are often also investigated as part of work focused on other aspects of the planning problem.

### Near Optimality {#sec:lit:form:near}

Asymptotically optimal algorithms converge towards an optimal solution as the number of samples increase but will almost surely not reach it in finite time [Lemma 28; @karaman_ijrr11]. Asymptotically *near-optimal* sampling-based algorithms improve practical performance by instead converging towards a solution that is within a user-specified factor of the optimum. This relaxed theoretical guarantee reduces computational effort and can result in algorithms that find better solutions faster in finite time and use less computational resources than required to maintain strict asymptotic optimality.

Asymptotic near optimality can be achieved in a variety of ways, including different connectivity expressions [@solovey_ijrr18; @solovey_ijrr19] and lazily evaluating or removing connections during or after the search [@marble_tro13; @wang_iros13; @dobson_ijrr14; @salzman_tro16].

### Convergence Rate {#sec:lit:form:rate}

Asymptotically optimal sampling-based planning algorithms converge with infinite samples but have no guarantees on their rate of convergence. Different rates can result in orders-of-magnitude differences in finite-time performance. Understanding the rates in different situations can help identify useful algorithms for practical problems and also design better planners.

Research includes developing probabilistic bounds on the length of a solution as a function of finite samples for [PRMstar]{acronym-label="PRMstar" acronym-form="singular+short"} [@dobson_iros13; @dobson_icra15] and AC@FMTstar [FMTstar]{acronym-label="FMTstar" acronym-form="singular+abbrv"} [@janson_ijrr15] [FMTstar]{acronym-label="FMTstar" acronym-form="singular+long"} [[FMTstar]{acronym-label="FMTstar" acronym-form="singular+abbrv"}; @janson_ijrr15] with both random and deterministic sampling [@janson_ijrr18; @tsao_icra20]. It also includes convergence rates for asymptotically near-optimal kinodynamic planners [@li_ijrr16] and asymptotically optimal kinodynamic planners built on feasible planning in a state-cost space [@hauser_tro16; @kleinbort_icra20]. It has also proven that naive [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} converges sublinearly (i.e., slower than linearly) in all possible problem or planner configurations when minimizing path length but that focused variants, such as Informed [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"}, can have linear convergence in some situations [@gammell_tro18].

## Practical Performance {#sec:lit:fast}

Another primary area of research is improving the practical ability of asymptotically optimal planning algorithms to find initial solutions quickly and converge rapidly towards the optimum. This work is important for real robotic systems and may also include formal analysis of the algorithmic improvements. Research in this area is wide ranging and difficult to classify but includes work on sampling (Section [3.2.1](#sec:lit:fast:samp){reference-type="ref" reference="sec:lit:fast:samp"}), heuristic search (Section [3.2.2](#sec:lit:fast:heur){reference-type="ref" reference="sec:lit:fast:heur"}), lazy computations (Section [3.2.3](#sec:lit:fast:lazy){reference-type="ref" reference="sec:lit:fast:lazy"}), hybrid search techniques (Section [3.2.4](#sec:lit:fast:hybrid){reference-type="ref" reference="sec:lit:fast:hybrid"}), bidirectional search techniques (Section [3.2.5](#sec:lit:fast:bi){reference-type="ref" reference="sec:lit:fast:bi"}), and a variety of other approaches (Section [3.2.6](#sec:lit:fast:misc){reference-type="ref" reference="sec:lit:fast:misc"}).

### Sampling {#sec:lit:fast:samp}

The performance of an individual instance of a sampling-based planning algorithm depends on the sequence of samples used in that specific run. Sequences may be deterministic [@janson_ijrr18; @palmieri_ral20; @tsao_icra20] or random but expected algorithm performance will depend on the underlying distribution. Many algorithms use a uniform distribution over the entire search space to ensure that all possible solutions can be found; however, performance can often be improved by increasing the likelihood of sampling (better) solutions.

Samples can be generated in a number of different ways that can reduce search effort, including sampling using motion primitives [@settimi_humanoids16], subspaces or simplified abstractions [@kiesel_socs12; @brunner_icra13; @reid_jfr19; @wang_tie20], potential functions [@qureshi_auro16], and gradient descent [@hauer_rss17]. Performance can also be improved by biasing sampling around approximations of free space [@bialkowski_iros13; @kim_icra14; @meng_robio17; @lai_icra19; @kang_iros19], with cross entropy [@kobilarov_ijrr12], machine-learning methods [@arslan_iros15; @iversen_iros16; @lehner_iros17; @ichter_icra18; @qureshi_iros18; @zhang_iros18; @kumar_iros19; @lai_ral20], and existing solutions [@akgun_iros11; @nasir_ijars13].

Existing solutions to a planning problem limit the search for improvements without loss of generality. The set of states that could belong to a better solution is the *omniscient set* and sampling it is a necessary condition to improve the solution for many algorithms [Lemma 5; @gammell_tro18]. Knowledge of the omniscient set is equivalent to solving a problem and it is often approximated as an *informed set* whose sampling is also necessary for improvement [Lemma 12; @gammell_tro18]. The utility of informed sets will depend on the precision and accuracy with which they approximate the omniscient set and they are often sampled approximately using heuristics and rejection sampling [@akgun_iros11; @perez_iros11; @otte_tro13; @arslan_icra15; @kunz_icra16; @littlefield_fsr18; @yi_icra18; @joshi_icra19].

An informed set applicable to all problems seeking to minimize path length is an $n$-dimensional ellipse defined by the $L^2$ (i.e., Euclidean) norm. It has been shown that the probability of sampling this set with rejection sampling goes to zero factorially (i.e., faster than exponentially) as state dimension increases [Theorem 14; @gammell_tro18]. This minimum-path-length curse of dimensionality can be avoided without loss of generality by directly sampling the $L^2$ informed set [@gammell_tro18].

### Heuristic Search {#sec:lit:fast:heur}

Graph-search algorithms use estimates of solution cost (i.e., heuristics) to order their search by potential solution quality. This allows them to prioritize high-quality solutions and avoid unnecessarily low-quality paths which improves both practical and theoretical performance. Heuristics can also be used to order asymptotically optimal sampling-based planning to find better initial solutions sooner, and converge towards the optimum faster, than uninformed approaches.

Heuristics can be used to order asymptotically optimal sampling-based planning probabilistically [@persson_ijrr14] and directly [@salzman_icra15a; @gammell_ijrr20]. AC@BITstar [BITstar]{acronym-label="BITstar" acronym-form="singular+abbrv"} [@gammell_ijrr20] [BITstar]{acronym-label="BITstar" acronym-form="singular+long"} [[BITstar]{acronym-label="BITstar" acronym-form="singular+abbrv"}; @gammell_ijrr20] separates approximation from search and uses heuristics to process batches of samples in order of potential solution quality. This not only searches problems quickly but also allows for extensions from the graph-search literature, including greedy searches [@holston_robio17], heuristic inflation and search truncation to balance exploration and exploitation [@strub_icra20a], and an asymmetric bidirectional search to adaptively estimate and use problem-specific heuristics [@strub_icra20b]. Research into estimating heuristics for motion planning also includes work on kinodynamic systems [@paden_ral17].

### Lazy Search {#sec:lit:fast:lazy}

Sampling-based planning algorithms search problems by sampling the free subspace and connecting samples with edges. These edges must also pass solely through free space and be followable by the robot (i.e., they must be feasible) for the algorithm to find valid solutions. Evaluating edge feasibility can be expensive in many problems, especially in the presence of constraints or obstacles that are defined by a noninvertible function of state.

Lazy algorithms reduce computational cost and improve real-time performance by delaying edge evaluations until necessary to find and/or improve a solution. Edges may be evaluated only when they belong to the best candidate solution [@hauser_icra15], in order of potential solution quality [@gammell_ijrr20], when necessary to satisfy optimality bounds [@salzman_tro16], or to estimate heuristics [@salzman_icra15a; @strub_icra20b]. Lazy collision checking can also be adapted as collision information is gathered to reduce false negatives [@kim_ur18].

### Hybrid Search {#sec:lit:fast:hybrid}

Asymptotically optimal sampling-based planning algorithms converge towards the global optimum but have a zero probability of finding it in finite time for most practical problems [Lemma 28; @karaman_ijrr11]. Local search methods, such as path simplification [@luna_icra13] or local optimization [@zucker_ijrr13], may find local minima in finite time but provide no global guarantees. Hybrid search algorithms improve the global convergence of sampling-based planning algorithms by including local optimization in the search.

The balance between global search and local optimization varies across hybrid algorithms. Some techniques apply optimizers to improve connections between samples [@choudhury_icra16; @suh_tro17; @kim_auro20] and/or minimize solutions [@nasir_ijars13; @kim_isr18; @kuntz_isrr20] during global search. Others are designed to use sampling-based exploration to explore homotopy classes as initial conditions for optimization methods [@kim_iros19].

### Bidirectional Search {#sec:lit:fast:bi}

Probabilistically complete bidirectional sampling-based planning algorithms, such as [RRT]{acronym-label="RRT" acronym-form="singular+abbrv"}-Connect [@kuffner_icra00], are effective techniques for feasible planning problems. Bidirectional variants of asymptotically optimal algorithms apply similar approaches to the optimal planning problem. This often finds initial solutions faster but incorporating bidirectional search into asymptotic convergence to the optimum can be more complex.

Bidirectional asymptotically optimal planning includes direct implementations of "[RRTstar]{acronym-label="RRTstar" acronym-form="singular+abbrv"}-Connect" [@akgun_iros11; @klemm_robio15] and modifications to improve asymptotic convergence by limiting the 'Connect' heuristic [@jordan_tech13; @qureshi_ras15] and using informed sampling [@burget_iros16]. They have also been used for manifold constraints [@jaillet_ras13], replanning in the presence of dynamic obstacles [@boardman_allerton14], and to estimate heuristics adaptively during search [@strub_icra20b]. A bidirectional [FMTstar]{acronym-label="FMTstar" acronym-form="singular+short"} also includes research on stopping conditions for bidirectional marching methods [@starek_iros15].

### Other Search Improvements {#sec:lit:fast:misc}

Not all methods to improve the practical performance of asymptotically optimal sampling-based planning algorithms fit neatly into the previous descriptions. A variety of other techniques to improve asymptotically optimal planning include switching between nonasymptotically optimal and asymptotically optimal algorithms [@alterovitz_icra11; @shan_iv14] and more thoroughly exploiting sampled information [@arslan_icra13; @arslan_icra15]. It also includes using computational resources more effectively, such as techniques designed for parallel computing [@otte_tro13; @arslan_cdc16].

## Constrained Planning Problems {#sec:lit:cnst}

Robot motion planning problems often require solutions that not only avoid obstacles but also satisfy other platform and/or task constraints. These can include manifold (Section [3.3.1](#sec:lit:cnst:man){reference-type="ref" reference="sec:lit:cnst:man"}), nonholonomic (Section [3.3.2](#sec:lit:cnst:noholo){reference-type="ref" reference="sec:lit:cnst:noholo"}), and kinodynamic (Section [3.3.3](#sec:lit:cnst:kino){reference-type="ref" reference="sec:lit:cnst:kino"}) constraints and high-level task specifications (Section [3.3.4](#sec:lit:cnst:form){reference-type="ref" reference="sec:lit:cnst:form"}).

### Manifold Constraints {#sec:lit:cnst:man}

Many robot motion planning problems require solutions to both avoid obstacles and satisfy geometric constraints, such as maintaining the orientation of a manipulator end effector. These kinematic or holonomic constraints are a function of state, e.g., $g\left(\mathbf{x}\right) = 0$, and limit solutions to a lower dimensional manifold of the original problem. This manifold has zero measure and therefore zero probability of being sampled from the full search space.

::: marginnote
:::

Problems that cannot be reparameterized onto the constraint manifold require planning techniques that can map their search to the implicit manifold. Research on asymptotically optimal algorithms to do so includes using continuation techniques [@jaillet_ras13] and decomposition into finite subspaces [@vegabrown_wafr20]. It also includes projection- and continuation-based methods that allow many types of general asymptotically optimal motion planners to be used directly on implicit manifold configuration spaces [@kingston_ijrr19].

### Nonholonomic Constraints {#sec:lit:cnst:noholo}

Many real-world robots have restrictions on their motion, such as skid-steer and Ackermann-steer wheeled robots that cannot move laterally. These nonholonomic constraints are an inseparable function of the state and its derivatives, e.g., $g\left(\mathbf{x}, \frac{d\mathbf{x}}{dt}, \frac{d^2\mathbf{x}}{dt^2}, \ldots\right) = 0$, and limit the connectivity of the search space. These problems can often be solved by treating the nonholonomic constraints as additional obstacles but better planning performance can be achieved by actively incorporating the constraints into the search. Many of these systems must also consider kinodynamic constraints (Section [3.3.3](#sec:lit:cnst:kino){reference-type="ref" reference="sec:lit:cnst:kino"}).

::: marginnote
:::

Research has developed distance functions for a variety of nonholonomic vehicles [@karaman_icra13; @park_iros15] and a general framework to assess asymptotically optimal planning for driftless systems [@schmerling_icra15]. It also includes work on asymptotically optimal feedback planning [@yershov_ijrr16], planning in vector flow fields [@palmieri_icra17], and deterministic sampling for driftless systems [@palmieri_ral20].

### Kinodynamic Constraints {#sec:lit:cnst:kino}

The motion of robots in the real world is governed by differential equations relating control inputs (e.g., forces) to accelerations (Section [2.3.4](#sec:back:ass:kino){reference-type="ref" reference="sec:back:ass:kino"}). These kinodynamics change the connectivity of the search space and any kinodynamic constraints that limit control inputs or rates of change, e.g., $\frac{d^2\mathbf{x}}{dt^2}<a_{\mathrm{max}}$, further reduce the set of feasible paths. This kinodynamic planning is further complicated for systems where the differential equations of motion cannot be solved in closed form for arbitrary end conditions. The absence of analytical solutions to these two-point [BVPs]{acronym-label="BVP" acronym-form="plural+short"} require additional considerations during asymptotically optimal planning, such as numerical approximations or shooting methods. Many of these systems must also consider nonholonomic constraints (Section [3.3.2](#sec:lit:cnst:noholo){reference-type="ref" reference="sec:lit:cnst:noholo"}).

::: marginnote
:::

This popular area of research includes analyzing kinodynamic asymptotic optimality [@karaman_cdc10; @schmerling_icra15; @schmerling_cdc15] and extending [RRTstar]{acronym-label="RRTstar" acronym-form="singular+short"} to kinodynamic systems [@jeon_cdc11; @perez_icra12; @karaman_icra13; @goretkin_icra13; @webb_icra13; @ha_cdc13; @arslan_icra17; @sakcak_auro19]. A wide variety of kinodynamic planning techniques exist, including solving two-point [BVPs]{acronym-label="BVP" acronym-form="plural+short"} with AC@LQR [LQRs]{acronym-label="LQR" acronym-form="plural+abbrv"} [@perez_icra12; @goretkin_icra13] [LQRs]{acronym-label="LQR" acronym-form="plural+long"} [[LQRs]{acronym-label="LQR" acronym-form="plural+abbrv"}; @perez_icra12; @goretkin_icra13] , fixed-final-state free-final-time controllers [@webb_icra13], successive approximation [@ha_cdc13], closed-loop prediction [@arslan_icra17], and precomputed motion primitives [@sakcak_auro19]. Other asymptotically optimal kinodynamic planning algorithms use [SQP]{acronym-label="SQP" acronym-form="singular+short"} with [BITstar]{acronym-label="BITstar" acronym-form="singular+short"} [@xie_icra15] and analytic steering solutions [@jeon_icra15] and numerical approximations [@yershov_ijrr16] with marching methods. Kinodynamic techniques have also been accelerated with heuristics and informed sampling [@kunz_icra16; @littlefield_fsr18; @littlefield_iros18; @yi_icra18].

Solving or approximating two-point [BVPs]{acronym-label="BVP" acronym-form="plural+short"} is impractical or impossible in some problems. Research on these applications has extended [RRT]{acronym-label="RRT" acronym-form="singular+abbrv"}-style shooting methods to asymptotically optimal kinodynamic planning [@abbasi-yadkori_iros10; @li_ijrr16], including with an augmented state-cost search space that does not require rewiring [@hauser_tro16; @kleinbort_icra20]. Two-point [BVPs]{acronym-label="BVP" acronym-form="plural+short"} can also be avoided with generalized label correcting methods [@paden_wafr20].

### High-level Task Specifications {#sec:lit:cnst:form}

Many motion planning problems require solutions to both avoid obstacles and satisfy a number of high-level or task-specific constraints. These may include the rules of the road for self-driving cars, a time-dependent sequence of tasks for a warehouse robot, or any number of other complex temporal relationships. These requirements are often defined in high-level specification languages and must be evaluated in parallel to searching for a collision-free path.

A number of different specification languages have been used with asymptotically optimal sampling-based planners, including $\mu$-calculus [@karaman_acc12], process algebra [@varricchio_icra14], AC@LTL [LTL]{acronym-label="LTL" acronym-form="singular+abbrv"} [@cho_ral17; @oh_cdc17; @zhang_ast20] [LTL]{acronym-label="LTL" acronym-form="singular+long"} [[LTL]{acronym-label="LTL" acronym-form="singular+abbrv"}; @cho_ral17; @oh_cdc17; @zhang_ast20] , finite [LTL]{acronym-label="LTL" acronym-form="singular+short"} [@reyescastro_cdc13], and AC@STL [STL]{acronym-label="STL" acronym-form="singular+abbrv"} [@vasile_iros17] [STL]{acronym-label="STL" acronym-form="singular+long"} [[STL]{acronym-label="STL" acronym-form="singular+abbrv"}; @vasile_iros17] . This research allows for algorithms to find paths that satisfy high-level constraints and, when no satisfying solution exists, find paths that reach the goal while violating a minimum number of specifications [@reyescastro_cdc13].

## Applications and Further Extensions {#sec:lit:app}

There are a number of interesting and challenging extensions of the motion planning problem in robotics. These include complex cost functions (Section [3.4.1](#sec:lit:app:cost){reference-type="ref" reference="sec:lit:app:cost"}) and planning for multirobot (Section [3.4.2](#sec:lit:app:mrobot){reference-type="ref" reference="sec:lit:app:mrobot"}) and multimodal (Section [3.4.3](#sec:lit:app:mmode){reference-type="ref" reference="sec:lit:app:mmode"}) systems. It also includes considering state and/or measurement uncertainty during planning (Section [3.4.4](#sec:lit:app:uncert){reference-type="ref" reference="sec:lit:app:uncert"}) and replanning when the environment changes or new information is available (Section [3.4.5](#sec:lit:app:replan){reference-type="ref" reference="sec:lit:app:replan"}).

Asymptotically optimal planning algorithms are also used in a variety of interesting applications. These include finding optimal solutions to the filtering [@chaudhari_cdc12] and stochastic control problems [@huynh_ijrr16; @huynh_cdc12; @chaudhari_acc13; @huynh_cdc14] and planning for a number of specific situations, including pursuit evasion games [@karaman_wafr10], simultaneous planning and execution [@karaman_icra11], moving goals [@liu_icma18], operating in vector flow fields [@palmieri_icra17; @to_icra20], autonomous driving at high speed [@jeon_acc13], autonomous driving for passenger comfort [@shin_iros18], cable-suspended parallel robots [@xiang_jmr20], to reduce radioactive exposure [@chao_net19], and very many more.

### Different Cost Functions and Objectives {#sec:lit:app:cost}

Many planning problems seek to optimize a more complex cost than path length, such as maximizing minimum clearance to obstacles, and objectives defined by cost maps or combinations of cost functions. These objective functions may not meet the assumptions used to first prove asymptotically optimality (Section [2.3](#sec:back:ass){reference-type="ref" reference="sec:back:ass"}) or the resulting refinements (Section [3.1.1](#sec:lit:form:bound){reference-type="ref" reference="sec:lit:form:bound"}).

Asymptotically optimal algorithms for these situations include planning on problems defined by cost maps [@devaurs_tase16], finding Pareto optimal solutions to multiobjective problems [@yi_ijcai15], and minimizing bottleneck (i.e., maximum state) cost [@solovey_ijrr19]. Specific applications include asymptotically optimal inspection in terms of path length and coverage [@fu_rss19] and planning for groups of vehicles to optimize connectivity, surveillance, and path length [@rahman_case16].

A reoccurring complex planning objective in robotics is information maximization. Informative path planning problems require systems to measure their environment while navigating to any specified goals. Asymptotically optimal algorithms have been developed and demonstrated for this problem in environmental monitoring [@hollinger_ijrr14; @jadidi_ijrr19] and mapping [@sayremccord_iros18].

### Multirobot Systems {#sec:lit:app:mrobot}

The complexity of path planning is directly related to the dimensionality of the search space. This dimensionality increases quickly in systems consisting of multiple robots. These problems can often be solved naively by treating each robot independently but this may preclude solutions to some problems that require coordination.

Research includes identifying conditions for multirobot asymptotic convergence and developing techniques to solve coupled multirobot problems with the tensor product of their individual spaces [@shome_auro20]. Applications also include groups of vehicles optimizing complex cost functions [@rahman_case16], two-arm manipulation [@shome_humanoids17], and cooperative aerial transport [@lee_tase18].

### Multimodal Systems {#sec:lit:app:mmode}

Some complex robotic systems have multiple configurations that are best represented as discrete modes (e.g., different legged-robot gaits). Planning problems for these multimodal systems have search spaces with both continuously valued and discrete dimensions. These problems can often be solved with general sampling-based planners but techniques designed to exploit the mixed nature of the search space can be more efficient.

Work to develop better asymptotically optimal planning algorithms for these situations includes extending roadmap planners to the multimodal configuration space of robot and object manipulation [@schmitt_icra17]. It also includes investigating the conditions for asymptotically optimal convergence in multimodal integrated task and motion planning problems [@shome_wafr20] and the application of multirobot techniques to this problem [@shome_mrs19].

### Uncertainty {#sec:lit:app:uncert}

Real-world robotic systems use noisy sensors to measure their environment. This creates uncertainty about their position relative to both obstacles and the goal and makes the feasible and optimal motion planning problems probabilistic. This *belief space planning* seeks a solution that safely reaches the goal with high probability given the system uncertainty.

Asymptotically optimal algorithms in belief space find the minimum cost path for a noisy system and/or in an uncertain environment that has a bounded probability of collision [i.e., chance constraint; @bry_icra11; @luders_gnc13; @bopardikar_ijrr16; @sun_isrr16; @virani_acc16; @yang_iros16] or is guaranteed to be safe [@luders_acc14]. Research has also studied the conditions required for optimality in belief space and shown that this property cannot be achieved for several cost functions [@shan_iros17] and investigated better distance functions to improve planning [@littlefield_isrr18].

### Unknown and/or Dynamic Environments {#sec:lit:app:replan}

Real-world robotic systems often operate in environments where the known presence and position of obstacles can change over time as a result of moving objects or sensor range limits. These changes may invalidate previously feasible solutions and require the system to solve an updated version of the original planning problem. This problem can be solved more efficiently with planning algorithms that reuse the previous search effort.

Asymptotically optimal techniques to replan efficiently when new information becomes available include using a bidirectional search to facilitate updates [@boardman_allerton14] and continuously refining and repairing a search during execution [@otte_ijrr16; @yang_iros16; @chen_auro19]. Work has also investigated achievable notions of optimality specific to incrementally revealed environments that result in policies guaranteed to be collision free [@janson_rss18].

# CONCLUSION {#sec:fin}

Sampling-based motion planning algorithms are powerful tools for searching continuously valued spaces, as often found in robotics. They use samples to approximate and search the space and many popular algorithms have a unity probability of finding a solution, if one exists, with an infinite number of samples (i.e., they are probabilistically complete; Definition [1](#defn:back:anal:pc){reference-type="ref" reference="defn:back:anal:pc"}). The quality of the solutions returned by these algorithms remained an open question until recently.

Karaman and Frazzoli [@karaman_ijrr11] analyze the quality of solutions found by popular sampling-based algorithms and prove that most have zero probability of finding an optimal solution, even with infinite samples. They provide efficient versions of these popular algorithms that instead converge asymptotically to the optimal solution with infinite samples almost surely over all realizations of a sampling distribution (i.e., they are almost-surely asymptotically optimal; Definition [1](#defn:back:anal:asao){reference-type="ref" reference="defn:back:anal:asao"}).

Most asymptotically optimal algorithms converge towards the optimal solution incrementally with additional samples. This anytime performance avoids the difficulties of approximating a continuously valued search space *a priori* to its search. The sampling instead interleaves approximation and search and the algorithms can be run for a given computational budget or until a suitable solution is found.

Extending asymptotically optimal planning has become an important and increasingly popular area of theoretical and practical research. Theoretical work has refined the necessary conditions for both asymptotic optimality almost surely and in probability (Definition [1](#defn:back:anal:aop){reference-type="ref" reference="defn:back:anal:aop"}), investigated asymptotic near-optimality, and analyzed rates of convergence. Practical work has developed a wide-variety of techniques to find better initial solutions sooner and converge towards the optimum faster.

Asymptotically optimal motion planning algorithms have been adopted and used on a number of robotic systems and problems. These include mobile ground robots, multirotor and fixed wing aerial vehicles, manipulator systems, and many others. These systems may operate independently or as part of a coordinated group and they may be unconstrained or have manifold, nonholonomic, kinodynamic, or high-level task constraints. The planning algorithms may need to optimize complex cost functions and account for unknown environments, moving obstacles, and measurement uncertainty in their plans.

Ongoing research will likely continue to expand the applicability and performance of these popular motion planning algorithms. This will include additional theoretical results, including perhaps further refinement to the necessary conditions for asymptotic optimality and investigations on the convergence rate of the resulting algorithms. It will also continue to include wide ranging efforts to improve practical search performance and applicability to real-world robotic problems.

::: summary
1.  Asymptotically optimal sampling-based planning algorithms are applicable to many optimal motion planning problems with continuously valued search spaces.

2.  These algorithms asymptotically converge to the optimal solution as the number of samples goes to infinity almost surely or in probability over all realizations of an appropriate sampling distribution.

3.  Many of these algorithms converge in an anytime manner that avoids the difficulty of selecting the correct approximation *a priori* to the search.

4.  These algorithms have been successfully applied to a number of important problems in robotics, including nonholonomic and kinodynamic systems, in unknown and dynamic environments, and in the presence of execution and measurement uncertainty.
:::

::: issues
1.  Research continues to refine the conditions necessary for asymptotic optimality for a wide range of problems and cost functions.

2.  There is a large amount of interest in improving practical search performance by finding and improving solutions quickly.

3.  Potential real-world applications continue to grow and include new challenging problems and environments.
:::

# DISCLOSURE STATEMENT {#disclosure-statement .unnumbered}

The authors are not aware of any affiliations, memberships, funding, or financial holdings that might be perceived as affecting the objectivity of this review.

# ACKNOWLEDGMENTS {#acknowledgments .unnumbered}

Work on this review was supported in part by the University of Oxford and [UKRI]{acronym-label="UKRI" acronym-form="singular+long"} and [EPSRC]{acronym-label="EPSRC" acronym-form="singular+abbrv"} through the "Robotics and Artificial Intelligence for Nuclear (RAIN)" research hub \[EP/R026084/1\] and the "ACE-OPS: From Autonomy to Cognitive assistance in Emergency OPerationS" international centre-to-centre research collaboration \[EP/S030832/1\].
