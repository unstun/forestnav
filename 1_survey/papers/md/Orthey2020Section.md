---
citation_key: Orthey2020Section
arxiv_id: 2010.14524
arxiv_url: https://arxiv.org/abs/2010.14524
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:51:47Z
origin: ai+web
reviewed: false
---

# Introduction

![Efficient exploitation of admissible heuristics (stemming from solution to relaxed problem) using the triple step pattern. The triple step pattern is one of four section patterns we advocate to efficiently exploit admissible heuristics near narrow passages.](Orthey2020Section_figs/pullfigure.png){#fig:pullfigure width="95%"}

Sampling-based motion planning algorithms are a successful paradigm to automate robotic tasks [@lavalle_2006]. However, sampling-based algorithms do not perform well when the state space of the robot contains narrow passages [@Mainprice2020; @Szkandera2020; @Hsu2003; @Saha2005], which are low-measure regions which have to be traversed to reach a goal. Narrow passages are often occurring in tasks which are particularly important in robotic applications, like grasping, peg-in-hole, egress/ingress or long-horizon planning problems [@Fu2019; @Hartmann2020].

In previous work, we and other research teams have shown that we can often efficiently solve high-dimensional planning problems by using admissible lower-dimensional projections of the state space, a topic we refer to as multilevel motion planning [@Ferbach1997; @Bayazit2005; @Orthey2020IJRR; @Reid2020; @Vidal2019]. When using a multilevel motion planning framework, we can often use solutions to simplified planning stages as admissible heuristics for the original problem [@Pearl1984; @Aine2016]. To efficiently exploit those admissible heuristics, we can use biased sampling methods [@Orthey2020IJRR; @Reid2019], which we can combine with classical planning algorithms like the rapidly-exploring random tree algorithm [@Orthey2019], the probabilistic roadmap planner [@Orthey2018], its optimal star versions [@Orthey2020IJRR] or the fast marching tree planner [@Reid2019]. However, while showing promising runtimes, those algorithms are prone to get trapped when run on problems involving narrow passages.

In this work, we address narrow passages in multilevel motion planning problems by developing section patterns. Section patterns are methods to explicitly address problematic situations that occur when we exploit solutions to relaxed problems. We introduce four section patterns. First, we introduce the Manhattan pattern, which we use to compute solution paths which actuate the minimal amount of joints to reach a goal region, which is advantageous for high dimensional systems [@Cortes2008; @Orthey2020IJRR]. Second, we introduce the Wriggle pattern, which we use to make small random walk steps to traverse a narrow passage. Third, we introduce the Tunnel pattern, which we use to steer around small infeasible regions. Fourth, we introduce the Triple step pattern, which we use to backtrack in case the algorithm gets stuck. In Fig. [1](#fig:pullfigure){reference-type="ref" reference="fig:pullfigure"} the Triple step pattern is showcased for a $37$-degree of freedom (dof) robotic hand. We execute the pattern when a collision occurs (1). We first backstep (2), then sidestep (3) and finally we make a forward step (4) to reach a goal position. The details of this and the other patterns will be detailed later in this paper.

To coordinate the execution of the four section patterns, we develop a novel algorithm we call *pattern dance*. The pattern dance algorithm applies the section patterns sequentially by trying first a pattern which is easy to compute (Manhattan pattern) and reverting to the more complex pattern like Wriggle or Tunnel only if needed. If all those patterns fail, we revert to the Triple step pattern, which is the most computationally demanding pattern. We embed this pattern dance algorithm into four multilevel planners [@Orthey2020IJRR], namely the quotient space RRT (QRRT) [@Orthey2019], the quotient space roadmap planner (QMP) [@Orthey2018] and its optimal versions QRRT\* and QMP\* [@Orthey2020IJRR].

Our contributions are as follows.

1.  We develop section patterns to efficiently exploit base space paths (solutions to relaxed problems).

2.  To coordinate sections patterns, we develop the pattern dance algorithm.

3.  We combine the pattern dance algorithm with four multilevel planners (QRRT, QRRT\*, QMP, QMP\*) and compare against $36$ planners from the open motion planning library (OMPL) and a previous sidestepping algorithm [@Orthey2020IJRR] on $7$ challenging scenarios.

# Related Work

Let us review the literature by focusing on two topics. First, we focus on generating admissible heuristics [@Edelkamp2011] for motion planning problems involving continuous domains [@lavalle_2006]. We discuss sources of admissible heuristics like constraint relaxations, lazy search, informed trees and past experience. Second, given an admissible heuristic, we review methods to efficiently exploit the heuristic either using path section approaches, local minima avoidance or narrow passage handling.

## Generating Admissible Heuristics

Motion planning [@lavalle_2006] is a well studied topic which has been successfully applied to a wide range of problem domains [@Moll2015]. One of the most promising paradigms to solve motion planning problems are (asymptotically optimal) sampling-based planners [@Karaman2011; @Salzman2016; @Salzman2019; @Bekris2020; @Gammell2020Survey]. However, these planners might become inefficient in state spaces which are too high-dimensional [@Orthey2020IJRR], contain intricate constraints [@Jaillet2012] or narrow passages [@Lee2012]. We can, however, often solve such problems efficiently, if we use admissible heuristics [@Aine2016].

We believe there are three large sources of admissible heuristics. First, we can compute admissible heuristics as solutions to relaxed problems [@Pearl1984]. Early instances of this idea to motion planning can be found in the constraint relaxation frameworks by @Ferbach1997 [@Ferbach1997], @Sekhavat1998 [@Sekhavat1998] and @Bayazit2005 [@Bayazit2005]. Newer instances of this idea are putting the focus on different aspects like the specific type of projection [@Sucan2011; @Gochev2012] or the type of lower-dimensional space [@Orthey2018; @Brandao2020]. We refer to all those frameworks under the collective term multilevel motion planning [@Orthey2020IJRR]. We can apply multilevel frameworks both to holonomic [@Reid2019; @Reid2020] and nonholonomic planning problems [@Vidal2019; @Orthey2020IJRR]. To create multilevel abstraction, we can often remove links from a robot [@Bayazit2005; @Zhang2009], shrink links [@Baginski1996; @Saha2005] or approximate a robot by simpler geometries, either exact [@Orthey2018; @Grey2017] or approximate [@Brock2001; @Rickert2014; @tonneau_2018]. While most methods use prespecified levels of abstraction, we can also use workspace information to compute abstractions on the fly [@Yoshida2005; @Luna2020], adaptively switch between abstractions [@Styler2017] or learn useful abstractions for specific instances [@Brandao2020]. Our approach is similar, in that we also use a multilevel motion planning framework [@Orthey2020IJRR]. However, our work is complementary, in that we focus specifically on computing path sections in the presence of narrow passages in the state space.

A second source of admissible heuristics are lazy search [@Bohlin2000; @Haghtalab2017] and informed sets [@Gammell2014; @Joshi2020]. Instead of using relaxations, we can compute lazy paths (paths not checked for collisions), either forward from the start [@Hauser2014] or backwards from the goal [@Strub2020Adaptively], to create an efficient heuristic which we can exploit using dedicated algorithms [@Gammell2020]. Once a solution exists, we can also exploit informed sets, sets which exclude all states with provable higher cost-to-go [@Gammell2014; @Gammell2020]. Those methods are particularly important, since edge evaluations is one of the bottlenecks in motion planning [@Kleinbort2020]. It therefore makes sense to develop heuristics which evaluate edges as late as possible [@Mandalika2019; @Hou2020].

Third, inspired by pattern database approaches in discrete search [@Culberson1998; @Edelkamp2012; @Hu2019], we can also construct admissible heuristics by using past experience. We can achieve this by either precomputing motion primitives, like steering functions or controllers like linear quadratic regulators [@Sakcak2019Auto; @Sakcak2019]. Or, we can store previous solution paths directly and use them as heuristics in new environments [@Driess2020; @Qureshi2020]. Our work is complementary in that we assume a heuristic given and we focus on exploiting this heuristic as efficiently as possible.

## Exploiting Admissible Heuristic

Given an admissible heuristic, we can optimally exploit it by discretizing the state space [@Ferguson2005] and by using the A\* algorithm [@Hart1968; @Pearl1984; @Aine2016]. However, discretizing the state space usually does not scale well to higher dimensional state spaces [@Bungartz2004; @Persson2014; @Giles2015] and performance would be sensitive to the resolution used [@Du2020]. To avoid discretization, we found three categories of work which use continuous methods to exploit admissible heuristics.

First, we can use biased sampling methods. A straightforward way would be to represent the heuristic value of a state by the radius of a hypersphere around the state [@Littlefield2018]. We could then exploit this hypersphere using dynamic domain sampling [@Yershova2009]. Using such a scheme, we would expand states with higher heuristic values more often. Depending on the exact type of heuristic function used, we would obtain sampling distributions which would increase the probability to sample states which are near to restricted workspace geometries [@VanDenBerg2005; @Yang2005], to state space obstacles [@Amato1998] or to narrow passage [@Hsu2003]. Those sampling distributions could also be learned over time to improve sampling [@Luo2019; @Ichter2018]. Our approach is similar in that we also use sampling-based methods. We differ, however, in that we concentrate on designing efficient patterns complementary to biased sampling methods.

Given a solution to a relaxed problem, we can often use this solution as a guide path heuristic [@Zhang2009; @tonneau_2018] to quickly find a solution in the original state space. Using the parlance of fiber bundles, we call this the find section problem [@Orthey2020IJRR]. This problem requires a relaxed solution (a base path), which we can find by computing workspace regions [@Plaku2007], by using workspace graphs [@Denny2020; @Uwacu2020] or by using a simpler robot geometry [@tonneau_2018]. In more complex environments, it is often advantageous to use multiple base paths [@Vonasek2019; @Denny2020] which decompose the original problem into smaller subproblems [@pokorny_2016_ijrr; @bhattacharya_2018; @Orthey2020WAFR]. To exploit a base path, we can often use restriction sampling [@Palmieri2016; @Orthey2018], which is highly efficient in high-dimensional state spaces, where uniform sampling would most likely fail to find solutions in a reasonable time [@Grey2017]. Apart from biasing sampling, we can also explicitly search over the set of states which project onto the base path [@Zhang2009], which we call the path restriction. To find paths over path restrictions, we previously developed a sidestepping approach [@Orthey2020IJRR], where we propagate states along the path restriction and execute sidesteps when collision occur. However, as we show in Sec. [\[sec:sectionpatterns\]](#sec:sectionpatterns){reference-type="ref" reference="sec:sectionpatterns"}, sidesteps are often not beneficial for narrow passages. While we also search over path restrictions, we differ by developing dedicated patterns to more efficiently traverse narrow passages.

Path section approaches and other heuristic search methods often fail because they reach local minima. We define a local minimum as a region in state space where the heuristic is not or only weakly correlated with the true cost-to-go [@Vats2017]. To address local minima, we can choose one of two approaches. First, we could preemptively avoid local minima. If the environment is static, we can learn minima regions and use this information to update the heuristic function [@Vats2017]. Second, we could try to escape local minima. There exist several methods to escape local minima like deflating the heuristic value of states close to obstacles [@Du2019] or increasing the search resolution to prevent evaluation of closeby states [@Du2020]. A related idea is to utilize Tabu search [@Glover1998] to prevent sampling in previously visited regions.

It is important to make the distinction between local minima which trap the planner and regions which might look like local minima but which a planner can actually traverse. We call such regions narrow passages [@Salzman2013]. To verify the existence of narrow passages in low-dimensional state spaces, we can use exact infeasibility proofs [@Schweikard1998; @Basch2001], for example using geometrical shapes like alpha complices [@Mccarthy2012] or cell decomposition methods [@Zhang2008]. Because many state spaces have a local product structure, we can often use configuration space slices [@Lozano1987; @Sintov2020] to efficiently test for infeasibility [@Varava2020]. If the problem is feasible, we could then use the geometrical shapes to enumerate narrow passages [@Manak2019]. To exploit narrow passages, we could bias sampling to the most constricted areas [@Yang2005; @Szkandera2020]. We differ to those approaches by not explicitly modeling narrow passages or local minima, but we instead develop reactive measures to escape minima and to traverse narrow passages. We thereby avoid spending time on irrelevant narrow passages.

# Background[]{#sec:background label="sec:background"}

![ Left: Fiber bundle $\mathbb{R}^3 \rightarrow \mathbb{R}^2$ with base space $B$, total space $X$, fiber space $F$, mappings $\pi$, $\pi_F$ and fiber $F_b$ over base element $b$. Right: Path restriction $r(p)$ over base path $p$. Adapted from [@Orthey2020IJRR].[]{#fig:fiberbundle label="fig:fiberbundle"}](images/bundle/fiberbundle.pdf){#fig:fiberbundle width="\\linewidth"}

Let us describe the necessary background to follow the exposition of our algorithm in Sec. [\[sec:algorithm\]](#sec:algorithm){reference-type="ref" reference="sec:algorithm"} and Sec. [\[sec:sectionpatterns\]](#sec:sectionpatterns){reference-type="ref" reference="sec:sectionpatterns"}. We start by explaining multilevel motion planning, i.e. planning with sequences of relaxed subproblems. While several formulations exist, we believe the framework of fiber bundles [@Orthey2020IJRR] to be a good way to concisely model multilevel abstractions and describe our algorithms. We then describe the concepts of lift, path restriction and path section which are particularly important. Finally, we describe the notion of admissible heuristics, which is one of the fundamental concepts to exploit solutions to relaxed problems [@Pearl1984].

## Optimal Motion Planning

Let $X$ be the state space of the robot. To each state space we associate a constraint function $\phi: X\rightarrow \{0,1\}$ which evaluates to $0$ if a state is constraint-free and to $1$ otherwise. We use the constraint function to define the free state space $X_\textnormal{free}= \{ x \in X\mid \phi(x) = 0\}$. Together with an initial configuration $x_I\in X_\textnormal{free}$ and a goal configuration $x_G\in X_\textnormal{free}$, we define an optimal motion planning problem [@Karaman2011; @Salzman2019; @Bekris2020] as the tuple $(X_\textnormal{free}, x_I, x_G, c)$, whereby our task is to develop an algorithm which computes a path from $x_I$ to $x_G$ while staying in $X_\textnormal{free}$ and minimizing the cost functional $c$. In this work, we use a minimal-length cost functional, but other costs are also possible like minimal energy or maximum clearance.

## Multilevel Motion Planning[]{#sec:background:multilevel label="sec:background:multilevel"}

Since high-dimensional motion planning problems are often too computationally expensive to solve, we use a sequence of relaxed problems which we refer to as multilevel abstractions [@Orthey2020IJRR]. Given a state space $X$, let us denote a multilevel abstraction as the tuple $\{X_1, \cdots, X_K\}$ with $X_K = X$. To each state space $X_k$, we associate a constraint function $\phi_k$ and a projection $\pi_k$ from $X_k$ to $X_{k-1}$. We say that the projection $\pi_k$ is admissible (w.r.t. the constraint functions), if $\phi_{k-1}(\pi_k(x)) \leq \phi_k(x)$ for any $x$ in $X_k$. With admissibility, we basically guarantee that solutions are preserved under projections [@Orthey2019]. If we would allow inadmissible projections, we would potentially sacrifice solutions and thereby sacrifice (probabilistic) completeness.

## Fiber Bundle Formulation

When working with multilevel abstraction, we quickly stumble upon situations where we lack the appropriate vocabulary to describe solution strategies. As a remedy, we describe multilevel abstractions using the framework of fiber bundles [@steenrod_1951; @husemoller_1966; @lee_2003]. A fiber bundle is a tuple $(X_k, X_{k-1}, F_k, \pi_k, \pi_{F_k})$ consisting of a total space $X_k$, a base space $X_{k-1}$, a fiber space $F_k$, a projection mapping $\pi_k$ from total to base space and a fiber projection mapping $\pi_{F_k}$ from total to fiber space. We assume the projection mapping $\pi_k$ to be admissible. With a fiber bundle, we model product spaces which locally decompose as $X_k = X_{k-1} \times F_k$. The total space $X_k$ is a union of fiber spaces which are parameterized by the base space $X_{k-1}$. If the level $k$ is unimportant for the task as hand, we often refer to a fiber bundle as the tuple $(X, B, F, \pi, \pi_{F})$ with $X$ being the total, $B$ the base, $F$ the fiber space and $\pi$, $\pi_{F}$ the base and fiber projection, respectively. We visualize a prototypical fiber bundle in Fig. [2](#fig:fiberbundle){reference-type="ref" reference="fig:fiberbundle"} (left). For more details and motivation, we refer to our prior work [@Orthey2020IJRR]. For the purpose of this paper, we focus on the three concepts of lift, path restriction and path section, which we explain next.

## Lift

Let $(X, B, F, \pi, \pi_{F})$ be a fiber bundle and let $b \in B$ be a base space element. We often like to project the element $b$ back to the total space $X$. We call this operation a lift [@Roewekaemper2013; @Orthey2020IJRR]. We define a lift as a mapping $\textsc{Lift}: B \rightarrow X$. To uniquely select an element in $X$, we will overload this function as a mapping $\textsc{Lift}: B \times F \rightarrow X$ by providing a fiber space element $f$ in $F$. If $X$ is a product space, we define the lift as $\textsc{Lift}(b,f)=(b,f)$ [@Orthey2020IJRR].

## Path Restrictions

Let $p: I \rightarrow B$ with $I = [0,1]$ be a path on the base space (a base path). Given a base path, one of the most central sets which we use in this work are path restrictions. A path restriction is the set $r(p) = \{ x \in X\mid \pi(x) \in p[I]\}$, whereby $p[I] = \{ p(t): t \in I \}$ is the image of the base path in $B$ and $\pi$ is the projection from $X$ to $B$. We visualize this situation in Fig. [2](#fig:fiberbundle){reference-type="ref" reference="fig:fiberbundle"} (right), where we show the image of a base path on the disk-shaped base space and its associated path restriction on the total space.

## Path Sections

Given a path restriction, we are often interested in finding paths which are lying inside the path restriction. We call them path sections [@steenrod_1951]. A (smooth) path section w.r.t. a base path $p$ is a continuous mapping $s$ from base space $B$ to total space $X$ such that $\pi(s(u))=u$ for any $u$ in the image of $p$ [@lee_2003]. This means, for each base path element, we select a unique state from the path restriction---in a continuous manner.

## Admissible Heuristics

Our motivation to introduce path restrictions and path sections comes from the role they play in exploiting admissible heuristics. Given a goal state $x_G$, an admissible heuristic $h(x)$ for a state $x$ in $X$ is a lower-bound on the true cost-to-go (or value) function $h^{*}(x)$, which we define as the cost of the optimal path from $x$ to $x_G$ through $X_\textnormal{free}$. Formally, we write this condition as $h(x) \leq h^{*}(x)$ [@Pearl1984; @Aine2016; @Orthey2019].

Given an admissible heuristic, we can try to reach the goal $x_G$ by using locally optimal decisions [@Hart1968]. If we are at a state $x$, we can make an optimal decision by doing a two-step approach. First, we compute the $f$-value of all its neighbors, which is the sum of its heuristic value and its cost-to-come from the start state. We then expand the state (node) with the lowest $f$-value, because, under the admissible heuristic, it is our best guess to efficiently reach the goal [@Pearl1984].

However, in a continuous domain, we cannot straightforwardly compute all neighboring states. Instead, we imagine computing a small $\epsilon$-neighborhood around the state. To compute heuristic values, we project the complete neighborhood down onto the base space. To reach the goal, our best guess is to make a step into the direction of the current minimal-cost base path. The states which we would expand in that way are exactly the states on the path restriction. By searching a path section over this path restriction, we efficiently exploit the admissible heuristic given by the base path.

# Find Sections using Pattern Dance[]{#sec:algorithm label="sec:algorithm"}

Our goal is to develop an algorithm which solves the find section problem, the problem of finding a path section over a given path restriction. After we state the problem, we discuss how the problem fits into the more general framework of motion planning using multilevel abstractions [@Orthey2020IJRR]. Finally, we discuss the pattern dance algorithm, which coordinates four section patterns to efficiently find feasible path sections.

## Find Section Problem

Let $(X, B, F, \pi, \pi_{F})$ be a fiber bundle on $X$ (possibly in a sequence of fiber bundles) and let $p: I \to B$ be a base path on $B$ starting at $\pi(x_I)$ and ending at $\pi(x_G)$. Given the base path $p$ and its path restriction $r(p) \subseteq X$, our goal is to develop an algorithm to find a feasible path section, i.e. a path lying in the intersection of the path restriction $r(p)$ and the free state space $X_\textnormal{free}$ connecting $x_I$ to $x_G$. We call this problem the *find section problem*.

![Path restriction $r(p)$ on a total space $X$ over a base path $p$ from base space $B$, together with initial state $x_I$, goal state $x_G$, projection $\pi$ and head pointer with head pointer $\ensuremath{H}$, consisting of state $x$ and location $l$.[]{#fig:pathrestriction label="fig:pathrestriction"}](images/restriction/restriction.pdf){#fig:pathrestriction width="\\linewidth"}

To illustrate the find section problem, we visualize it in Fig. [3](#fig:pathrestriction){reference-type="ref" reference="fig:pathrestriction"}. The figure shows a base path $p$ on $B$ (bottom) and its restriction $r(p)$ on $X$ (top). Our goal is to connect $x_I$ to $x_G$ while staying inside $r(p)$. To efficiently solve the find section problem, we often need to track information along the path restriction. To track this information, we introduce the notion of a head pointer $\ensuremath{H}$ as the tuple $\ensuremath{H}=(x, l, r)$ consisting of a path restriction $r(p) \subseteq X$ over a base path $p$ in $B$, a current state $x$ in $r(p)$ and a location $l \in [0,1]$ defining the position along the base path. We think of the head pointer as a ruler which we move forward along the path restriction towards the goal state. In pseudocode, we refer to the current state as $\textsc{State}(\ensuremath{H})$ and its location as $\textsc{Location}(\ensuremath{H})$.

## Find Sections in Multilevel Planning[]{#sec:multilevelplanner label="sec:multilevelplanner"}

The find section problem is a subproblem of the more general multilevel motion planning problem (see Sec. [\[sec:background:multilevel\]](#sec:background:multilevel){reference-type="ref" reference="sec:background:multilevel"}). In previous works, we proposed to solve multilevel planning problems using a dedicated multilevel planner [@Orthey2020IJRR]. To clarify the role of finding sections, we describe this multilevel planner in Alg. [\[alg:bundleplanner\]](#alg:bundleplanner){reference-type="ref" reference="alg:bundleplanner"}. We initialize this algorithm with an initial state $x_I$, a goal state $x_G$ and a sequence of bundle spaces $X_1, \ldots, X_K$. To search for a feasible path, we first initialize a priority queue (Line 1), then we iteratively explore the bundle spaces (Line 2) by first trying to solve the find section problem (Line 3), then pushing the $k$-th bundle space into the priority queue (Line 4). We compute the importance of a bundle space by the sampling density of its associated graph [@Orthey2020IJRR] as $$\begin{equation}
\textsc{Importance}(X_k) = \dfrac{1}{|V_k|^{1/n_k}+1}
\end{equation}$$ with $|V_k|$ being the number of nodes in the graph $G_k$ on $X_k$ and $n_k$ is the dimensionality of $X_k$. We then go into a while loop which terminates if a planner terminate condition (PTC) of the $k$-th space is not fulfilled (Line 5). A PTC can be a timelimit, an iteration limit or a desired cost. We then pop the space with the highest importance from the queue (Line 6), execute one grow iteration for the selected bundle space (Line 7) and push the space back to the queue thereby updating its importance (Line 8). The planner terminates if the PTC of all bundle spaces is false and returns the graphs of all computed levels (Line 11). From those graphs, we can then compute the (optimal) solution path using a discrete A\* search [@Hart1968] (if one exists). All multilevel planner share this high-level structure. Multilevel planners differ by how the [Grow]{.smallcaps} function is implemented.

We previously developed four multilevel planners. First, the quotient-space roadmap planner (QMP), in which we implement [Grow]{.smallcaps} as a probabilistic roadmap (PRM) step [@Kavraki1996]. Second, the quotient-space rapidly-exploring random tree (QRRT), in which we implement [Grow]{.smallcaps} as an RRT step [@Kuffner2000]. Finally, we use the two asymptotically optimal versions QRRT\* and QMP\*, in which we implement a step of RRT\* and PRM\* [@Karaman2011], respectively. The algorithms also differ in how we compute the distance metric and how we implement sampling inside the grow function, as we detail in our previous publication [@Orthey2020IJRR].

The main contribution of our paper, the pattern dance algorithm, is an efficient method to solve the find section problem. The integration into the multilevel planner is shown in the [FindSection]{.smallcaps} method in Alg. [\[alg:findsection\]](#alg:findsection){reference-type="ref" reference="alg:findsection"}. First, we check if there exists a base space (Line 1). We then compute a base path $p$ from the underlying graph or tree on the base space (Line 2). We then build a path restriction $r$ from $p$ (Line 3) and create a head on the path restriction (Line 4). We then call the pattern dance algorithm with the head as input.

## Pattern Dance Algorithm

We depict the pseudocode of the pattern dance algorithm in Alg. [\[alg:patterndance\]](#alg:patterndance){reference-type="ref" reference="alg:patterndance"}. The input is a head over the path restriction and a recursion depth (initially set to zero). Inside the pattern dance algorithm, we coordinate the execution of four section patterns. The rational behind the coordination is to try less complex patterns first while we can successfully move the head forward along the path restriction. Only if no progress is made, we revert to more and more complex patterns to resolve the situation. We found this to be an efficient strategy to quickly find sections.

Those four section patterns are detailed in Sec. [\[sec:sectionpatterns\]](#sec:sectionpatterns){reference-type="ref" reference="sec:sectionpatterns"} and either move the head forward by controlling the lowest amount of joints possible ([ManhattanPattern]{.smallcaps}), execute random walk steps with forward bias ([WrigglePattern]{.smallcaps}), try to overcome small barriers using steps outside the path restriction ([TunnelPattern]{.smallcaps}) or use a dedicated backtracking procedure ([TripleStepPattern]{.smallcaps}) to efficiently find feasible path sections.

Before going into detail, we provide a brief summary and motivation. The algorithm iterates through all four patterns, starting with the computationally cheapest [ManhattanPattern]{.smallcaps} (Line 1). If the pattern succeeds, we successfully return (Line 2). Otherwise, we check if we reached the maximum recursion depth (Line 4) and return with failure (Line 5).

If the depth is below the maximum depth, we continue by executing first the [WrigglePattern]{.smallcaps} and the [TunnelPattern]{.smallcaps}(Line 7). If one pattern successfully terminates, we recursively call the pattern dance algorithm and we increase the recursion depth (Line 8). If no pattern successfully terminates, we backtrack using the [TripleStepPattern]{.smallcaps}. To execute the triple step pattern, we first interpolate a single step forward along the base path (Line 10, 11). We then attempt to find a valid fiber space element for a maximum of $\ensuremath{B_{\text{max}}}$ attempts (Line 12). This is done by first sampling a fiber state over the given base state (Line 13). We then lift the state to the path restriction (Line 14) to obtain a state $x$. If this state is valid and we *cannot* reach it from the head state (Line 16), we execute the triple step pattern with target $x$ (Line 17). If we successfully executed the pattern, we call the pattern dance algorithm again recursively. Note that the small forward step of $\ensuremath{\delta_{X_{k-1}}}$ (Line 10) is an essential component of our algorithm. If we would sample directly over the head base state, we often would sample symmetrical local minima (as an example, see state $p^{\prime}_1$ in Fig. [8](#fig:sectionpattern:triplestep){reference-type="ref" reference="fig:sectionpattern:triplestep"}). We found this to be particularly important for higher dimensional state spaces, where we often encounter infinitely many symmetrical local minima (consider the set of horizontal rotations of the cylinder before entering the opening in the Bugtrap scenario in Sec. [\[sec:evaluations\]](#sec:evaluations){reference-type="ref" reference="sec:evaluations"}).

To implement the section patterns and the pattern dance algorithm, we use the open motion planning library (OMPL) [@Sucan2012]. The algorithms are freely available and part of our multilevel motion planning extension of OMPL [@Orthey2020IJRR]. All code can be downloaded over github[^4]. All parameters used in the algorithms are shown in Table [1](#tab:parameters){reference-type="ref" reference="tab:parameters"}, including the values we use for the evaluations. The values for $\ensuremath{B_{\text{max}}}, \ensuremath{S_{\text{max}}}, \ensuremath{D_{\text{max}}}$ are chosen as large as possible to still give good performance on our hardware.

::: {#tab:parameters}
       Parameter                   Description                   Values used
  -------------------- ------------------------------------ ----------------------
    $D_{\text{max}}$      Maximum depth of pattern dance             $3$
    $B_{\text{max}}$    Maximum branching of pattern dance          $500$
    $S_{\text{max}}$        Maximum sampling attempts               $100$
   $\delta_{X_{k-1}}$        Step size on base space         $0.01 \mu_{X_{k-1}}$
    $\delta_{F_{k}}$         Step size on fiber space         $0.01 \mu_{F_{k}}$

  : Parameters used in algorithm. The variable $\mu_{X}$ refers to the measure (volume) of the state space $X$.
:::

# Section Patterns[]{#sec:sectionpatterns label="sec:sectionpatterns"}

The pattern dance algorithm relies on four section patterns, to which we like to provide more detail and motivation. Each of those section patterns is a particular approach to efficiently traverse narrow passages and escape local minima, whereby a local minimum is defined as a region where the heuristic cost is only weakly correlated with the true cost-to-go [@Vats2017]. Each section pattern takes as input a head pointer and tries to move this head pointer forward along the path restriction. Please also consult Fig. [3](#fig:pathrestriction){reference-type="ref" reference="fig:pathrestriction"} for visualization of the terminology used.

## Manhattan Pattern

Our first section pattern to propagate the head pointer $\ensuremath{H}$ is the Manhattan (MH) pattern. With the MH pattern, we interpolate a path between the head state and the goal state along the path restriction. To interpolate, we first interpolate along the base path while keeping the fiber element fixed. Once we reach the end of the base path, we interpolate along the fiber space to the goal state. This method is motivated by our desire to actuate the smallest number of joints at the same time, which is advantageous for high-dimensional systems [@Cortes2008].

We detail the MH pattern in Alg. [\[alg:L1pattern\]](#alg:L1pattern){reference-type="ref" reference="alg:L1pattern"}. We take as input a head pointer $\ensuremath{H}$ over a path restriction $r$ with base path $p$. We first project the head state onto the fiber (Line 1-2) by using the fiber projection $\pi_{F}$. We then take the location of the head pointer along the base path (Line 3) and step along the base path in increments of $\ensuremath{\delta_{X_{k-1}}}$ (Line 5-10) and add the states to the path $s$ (Line 4). This is done by computing the next base state (Line 6), lifting the base state into the total space (Line 7) and adding it to the path (Line 8). Once we reached the end of the base path, we add the goal state to the section (Line 11). The resulting path $s$ is schematically shown in Fig. [3](#fig:pathrestriction){reference-type="ref" reference="fig:pathrestriction"}. Finally, we evaluate the path by moving along until a constraint violation occurs or we reached the goal state (Line 12). The function $\textsc{CheckMotion}$ returns the last valid state which we use to update the head $\ensuremath{H}$. We then return true if the head has reached the goal and false otherwise.

:::: {#fig:geometrynarrowpassage .figure}
![image](Orthey2020Section_figs/03D_cylinder_env.png){width="55%"} ![image](Orthey2020Section_figs/03D_cylinder_statespace.png){width="40%"}

::: caption
Left: Rectangular rigid robot which has to traverse a narrow passage from a green start to a red goal state. Right: The geometry of its state spaces (darker colors are closer to start state).
:::
::::

:::: {#fig:pathrestrictionsnarrowpassages .figure}
![image](Orthey2020Section_figs/03D_cylinder_section.png){width="48%"} ![image](Orthey2020Section_figs/03D_cylinder_section_offset.png){width="48%"}

::: caption
Two path restrictions for the rectangular rigid robot near a narrow passage. Left: Robot moves along a straight base path. Right: Robot moves along a slanted base path.
:::
::::

## Interlude: The Geometry near Narrow Passages

The next three section patterns are tailor-made solutions to either traverse a narrow passage or to escape a local minimum. To motivate those patterns, we first study the geometry of state spaces near narrow passages. We use a simple toy example of a rigid rectangular body moving in the 2D plane. The state space of this rigid body is the special Euclidean group $SE(2)$, consisting of position and orientation. We assume that the body is located near to a narrow passages as shown in Fig. [4](#fig:geometrynarrowpassage){reference-type="ref" reference="fig:geometrynarrowpassage"} (left). We will further assume that our task is to move the rigid body through the narrow passage, from a start state (green) to a goal state (red). We will represent a state as $(x_0,x_1,x_2) \in SE(2)$, with $x_0, x_1$ being vertical and horizontal displacement and $x_2$ the orientation. We visualize a subset of the state space in Fig. [4](#fig:geometrynarrowpassage){reference-type="ref" reference="fig:geometrynarrowpassage"} (right), whereby points in collision are colored from dark red (low $x_1$ value, close to start) to bright blue (high $x_1$ value, close to goal).

To generate path restrictions, we first use a relaxation of the problem onto a circular disk as shown in Fig. [4](#fig:geometrynarrowpassage){reference-type="ref" reference="fig:geometrynarrowpassage"} (Left). We model this relaxation using the fiber bundle $SE(2) \rightarrow \mathbb{R}^2$ with base space $\mathbb{R}^2$ and total space $SE(2)$ [@Orthey2018]. Let us assume a base path $p: I \rightarrow \mathbb{R}^2$ for the disk to be given. This path induces a two-dimensional path restriction in $SE(2)$, two of which we visualize in Fig. [5](#fig:pathrestrictionsnarrowpassages){reference-type="ref" reference="fig:pathrestrictionsnarrowpassages"}. The left figure shows a path restriction for a base path going straight through the passage, as shown in Fig. [4](#fig:geometrynarrowpassage){reference-type="ref" reference="fig:geometrynarrowpassage"}. The right figure shows a path restriction for a base path which goes slanted through the passage. Both are also slices through the state space geometry shown in Fig. [4](#fig:geometrynarrowpassage){reference-type="ref" reference="fig:geometrynarrowpassage"} (right). From Fig. [5](#fig:pathrestrictionsnarrowpassages){reference-type="ref" reference="fig:pathrestrictionsnarrowpassages"}, we observe that there are at least three failure cases. Either, we reach a local minimum, we collide with constraints near a narrow passage or we get stuck in front of a small but infeasible region. For each case, we develop a dedicated section pattern to either advance or backtrack.

## Wriggle Pattern

![Wriggle pattern to traverse a narrow passage: Given a feasible state $p_1$, we make coordinated random walk steps along the fibers of the path restriction. The distance between fibers is determined by the base space step size parameter $\ensuremath{\delta_{X_{k-1}}}$.[]{#fig:wrigglepattern label="fig:wrigglepattern"}](images/sectionpatterns/wriggle/wrigglePattern.pdf){#fig:wrigglepattern width="\\linewidth"}

If we reach a local minimum, the triple step pattern is a way to backtrack to a narrow passage. However, we often might execute the triple step pattern prematurely, because we bumped into constraints near or in a narrow passage. To circumvent those situations, we use the wriggle pattern. With the wriggle pattern, we make coordinated random steps along the fibers of the path restriction and accept a step if it is valid, which is similar to retraction-based sampling [@Zhang2008Retraction]. We visualize this pattern in Fig. [6](#fig:wrigglepattern){reference-type="ref" reference="fig:wrigglepattern"}.

We show the pseudocode in Alg. [\[alg:wrigglepattern\]](#alg:wrigglepattern){reference-type="ref" reference="alg:wrigglepattern"}. We start by making one $\ensuremath{\delta_{X_{k-1}}}$ step forward from the head (Line 1). Until we have not reached the end (Line 3), we get the base state at location $l$ (Line 4), and get the fiber element of the head state (Line 6). We then sample for $\ensuremath{S_{\text{max}}}$ rounds (Line 8) by sampling a fiber state in the $\ensuremath{\delta_{F_{k}}}$ proximity of the head fiber state (Line 9). We then lift the base and fiber state (Line 10) and check if the state is valid (Line 11). If the state is valid, we check if the motion from the head to the new state is feasible (Line 12-17). We terminate if we could not expand the state (Line 21-23) or reach the end. We then return true if we made at least one step (Line 25).

## Tunnel Pattern

![Tunnel pattern to traverse a narrow passage: Given two feasible states $p_1$ and $p_2$, we connect them by momentarily leaving the path restriction to circumnavigate the infeasible region between them.[]{#fig:tunnelpattern label="fig:tunnelpattern"}](images/sectionpatterns/tunnel/tunnelPattern.pdf){#fig:tunnelpattern width="\\linewidth"}

While the wriggle pattern locally explores the neighborhood *inside* the path restriction, we often encounter situations where we find it advantageous to momentarily step *outside* the path restriction to overcome an infeasible region. From the perspective of the path restriction, we "tunnel" through the infeasible region, which we therefore refer to as the tunnel pattern. With the tunnel pattern, we assume to be located at a local minimum $p_1$ as shown in Fig. [7](#fig:tunnelpattern){reference-type="ref" reference="fig:tunnelpattern"}. To resolve this situation, we try to find the next valid state $p_2$ while keeping the fiber element constant. We then try to connect $p_1$ to $p_2$ by sampling valid states in a smoothly increasing neighborhood of the base space and a constant neighborhood in fiber space. While $p_2$ is not reached, we accept new states if they decrease the distance to $p_2$.

We show the pseudocode in Alg. [\[alg:tunnelpattern\]](#alg:tunnelpattern){reference-type="ref" reference="alg:tunnelpattern"}. We first search for a tunnel ending state $x_\text{End}$ at base path location $l_\text{End}$ (Line 1). To find the tunnel ending, we step forward along the base path without changing the fiber until we find a valid state. We then try to connect the head state $x_{\ensuremath{H}}$ to the tunnel ending state $x_\text{End}$. We use a while loop to move along the relevant base path segment from the head location $l$ to the tunnel end location $l_\text{End}$ (Line 6). We first check if we can connect the head state to the tunnel end state (Line 7). If true, we add a new edge into the graph (Line 8), set the head to the tunnel ending state (Line 9) and return true (Line 10). Otherwise, we step forward along the base path with step size $\ensuremath{\delta_{X_{k-1}}}$ (Line 12) and query the base state at $l$ (Line 13). Instead of using the base state exactly, we use a smoothly increasing neighborhood parameter $\epsilon$. The value of $\epsilon$ depends on the counter $\ensuremath{\text{ctr}}$ and smoothly interpolates between $0$ and $10 \ensuremath{\delta_{X_{k-1}}}$ using an Hermite polynomial [@De1987] (Line 14). We then attempt to make a step towards the tunnel ending for a maximum of $\ensuremath{S_{\text{max}}}$ attempts (Line 16). We do this by sampling a base space element (Line 17) and a fiber element (Line 18). We then lift the state (Line 19) and check for validity (Line 20). If the new state is valid, its distance is closer to the tunnel ending and we can connect it to the head state (Line 22), we add a new edge to the graph (Line 23), set the head state to the new state (Line 24) and continue forward (Line 25). If we fail to find a better sample for $\ensuremath{S_{\text{max}}}$ attempts, we return false (Line 30-32). We also return false if we reach the base path location $l_\text{End}$ without having a valid connection (Line 34).

## Triple Step Pattern

:::: {#fig:sectionpattern:triplestep .figure latex-placement="t"}
![](Orthey2020Section_figs/tripleStepPattern.png){width="\\linewidth"}

![At $p_1$ (after collision).](Orthey2020Section_figs/T1.png){width="\\linewidth"}

![At $p_2$ (after backstep).](Orthey2020Section_figs/T2.png){width="\\linewidth"}

![At $p_3$ (after sidestep).](Orthey2020Section_figs/T3.png){width="\\linewidth"}

![At $p_4$ (after forward step).](Orthey2020Section_figs/T4.png){width="\\linewidth"}

::: caption
Triple step pattern to traverse a narrow passage: We start at a state $p_1$ (a), backstep to a state $p_2$ (b), sidestep along the fiber to $p_3$ (c) and then step forward to reach a state $p_4$ (d). []{#fig:sectionpattern:triplestep label="fig:sectionpattern:triplestep"}
:::
::::

To escape a local minimum, we develop the triple step pattern. With the triple step pattern, we connect two states on the path restriction using a triple backtracking step.

The idea of the triple step pattern is to connect two states on (or near) the same fiber. Before explaining the pattern in detail, we first visualize the pattern in Fig. [8](#fig:sectionpattern:triplestep){reference-type="ref" reference="fig:sectionpattern:triplestep"}. You can see a rectangular rigid body in the plane, which is currently at state $p_1$ (Fig. [8](#fig:sectionpattern:triplestep){reference-type="ref" reference="fig:sectionpattern:triplestep"} (a)) and which we like to move to state $p_4$ (Fig. [8](#fig:sectionpattern:triplestep){reference-type="ref" reference="fig:sectionpattern:triplestep"} (d)). To connect those states, we first move backwards along the path restriction from $p_1$ to another state $p_2$ (Fig. [8](#fig:sectionpattern:triplestep){reference-type="ref" reference="fig:sectionpattern:triplestep"} (b)) while moving from $p_4$ to another state $p_3$ (Fig. [8](#fig:sectionpattern:triplestep){reference-type="ref" reference="fig:sectionpattern:triplestep"} (c)), respectively. We move backwards until we can connect $p_2$ and $p_3$ by a straight line segment. In that case we execute a backstep from $p_1$ to $p_2$, a sidestep (along the fiber marked) from $p_2$ to $p_3$ and a forward step from $p_3$ to $p_4$. Note that $p_4$ is slightly moved forward such that we avoid situations where we backtrack to a symmetric local minimum like $p'_1$ which would not improve our location along the path restriction.

We show the pseudocode for the triple step pattern in Alg. [\[alg:triplesteppattern\]](#alg:triplesteppattern){reference-type="ref" reference="alg:triplesteppattern"}. Our goal is to connect the head state to the given state $x$. We first compute a midpoint on the fiber space (Line 5) (to minimize the number of [CheckMotion]{.smallcaps} calls [@Mandalika2019]). We then move backwards along the base path while we are greater than the parameter $\ensuremath{\delta_{X_{k-1}}}$ (Line 6-7). For each location, we interpolate a base state (Line 8), lift the state using the fiber midpoint (Line 9) and check if this state is valid. If it is valid, we compute intermediate states $x_1$ and $x_2$ (Line 11, 12) and check if the motion between them is feasible (Line 13). If that is true, we additionally check if the backward and forward steps are feasible (Line 14, 15). If that is true, we add those edges to the graph (Line 16-18) and update the head to our new state $x$ (Line 19). In that case we return true (Line 20). If we fail to find such a triple step, we terminate once we reach the beginning of the base path location and return false (Line 27).

# Evaluations[]{#sec:evaluations label="sec:evaluations"}

:::: {#fig:scenarios .figure latex-placement="ht"}
![06D Bugtrap[]{#fig:scenarios:bugtrap label="fig:scenarios:bugtrap"}](images/evaluations/06D_Bugtrap.png){#fig:scenarios:bugtrap width="90%"}

![06D Double Lshape[]{#fig:scenarios:doubleLshape label="fig:scenarios:doubleLshape"}](images/evaluations/06D_DoubleL.png){#fig:scenarios:doubleLshape width="90%"}

![10D Chain Egress[]{#fig:scenarios:chainegress label="fig:scenarios:chainegress"}](images/evaluations/10D_ChainEgress.png){#fig:scenarios:chainegress width="90%"}

![37D ShadowHand Ball[]{#fig:scenarios:overhand label="fig:scenarios:overhand"}](images/evaluations/37D_overhand.png){#fig:scenarios:overhand width="\\linewidth"}

![37D ShadowHand Metal[]{#fig:scenarios:underhand label="fig:scenarios:underhand"}](images/evaluations/37D_underhand.png){#fig:scenarios:underhand width="\\linewidth"}

![37D ShadowHand Mug[]{#fig:scenarios:mug label="fig:scenarios:mug"}](images/evaluations/37D_singlefinger.png){#fig:scenarios:mug width="\\linewidth"}

![37D ShadowHand Scissor[]{#fig:scenarios:scissor label="fig:scenarios:scissor"}](images/evaluations/37D_doublefinger.png){#fig:scenarios:scissor width="\\linewidth"}

::: caption
Scenarios for evaluations. The task is to move the robot from the start state (green) to the goal state (red). Top Row (left to right): Bugtrap (6-dof), Double L Shape (6-dof) (goal configuration not shown) and Chain Egress (10-dof). Bottom Row: Overhand, Underhand, Single-Finger and Double-Finger Pregrasp (each 37-dof) (start configurations not shown).[]{#fig:scenarios label="fig:scenarios"}
:::
::::

:::: {#fig:simplifications .figure latex-placement="ht"}
![Shadow Hand Level 3 $\mathbb{R}^{37}$.[]{#fig:simplifications:hand3 label="fig:simplifications:hand3"}](images/multilevel/37D_level3.png){#fig:simplifications:hand3 width="\\linewidth"}

![Shadow Hand Level 2 $\mathbb{R}^{18}$.[]{#fig:simplifications:hand2 label="fig:simplifications:hand2"}](images/multilevel/37D_level2.png){#fig:simplifications:hand2 width="\\linewidth"}

![Shadow Hand Level 1 $\mathbb{R}^{13}$.[]{#fig:simplifications:hand1 label="fig:simplifications:hand1"}](images/multilevel/37D_level1.png){#fig:simplifications:hand1 width="\\linewidth"}

![Bugtrap Level 2 $SE(3)$.[]{#fig:simplifications:bugtrap2 label="fig:simplifications:bugtrap2"}](images/multilevel/06D_Bugtrap_level2.png){#fig:simplifications:bugtrap2 width="\\linewidth"}

![Double Lshape Level 2 $SE(3)$.[]{#fig:simplifications:dls2 label="fig:simplifications:dls2"}](images/multilevel/06D_DL_level2.png){#fig:simplifications:dls2 width="\\linewidth"}

![Articulated Chain Level 2 $SE(3) \times \mathbb{R}^6$.[]{#fig:simplifications:chain2 label="fig:simplifications:chain2"}](images/multilevel/10D_level2.png){#fig:simplifications:chain2 width="\\linewidth"}

![Bugtrap Level 1 $\mathbb{R}^3$.[]{#fig:simplifications:bugtrap1 label="fig:simplifications:bugtrap1"}](images/multilevel/06D_Bugtrap_level1.png){#fig:simplifications:bugtrap1 width="\\linewidth"}

![Double Lshape Level 1 $\mathbb{R}^3$.[]{#fig:simplifications:dls1 label="fig:simplifications:dls1"}](images/multilevel/06D_DL_level1.png){#fig:simplifications:dls1 width="\\linewidth"}

![Articulated Chain Level 1 $\mathbb{R}^3$.[]{#fig:simplifications:chain1 label="fig:simplifications:chain1"}](images/multilevel/10D_level1.png){#fig:simplifications:chain1 width="\\linewidth"}

::: caption
Multilevel abstraction using simplified models.[]{#fig:simplifications label="fig:simplifications"}
:::
::::

::: tabulary
\@LLCCCCCCC@ & & & & & & &\
& QRRT (**ours**) & 4.45 & 1.86 & **0.55** & 2.01 & 35.63 & 19.80 & 60.00\
2 & QRRT\* (**ours**) & 24.87 & 2.00 & 0.56 & 25.35 & 43.95 & 60.00 & 60.00\
3 & QMP (**ours**) & **0.51** & **1.27** & 1.91 & 0.86 & 18.98 & **1.20** & **14.52**\
4 & QMP\* (**ours**) & 0.90 & 1.63 & 7.29 & **0.86** & **1.94** & 1.63 & 37.27\
& RRT & 60.00 & 60.00 & 49.77 & 60.00 & 60.00 & 60.00 & 60.00\
6 & RRTConnect & 60.00 & 60.00 & 60.00 & *[1.70]{style="color: Mycolor1"}* & *[8.16]{style="color: Mycolor1"}* & 57.38 & 60.00\
7 & RRT# & 60.00 & 60.00 & 45.43 & 60.00 & 60.00 & 60.00 & 60.00\
8 & RRT\* & 60.00 & 60.00 & 51.74 & 60.00 & 60.00 & 60.00 & 60.00\
9 & RRTXstatic & 60.00 & 60.00 & 50.49 & 60.00 & 60.00 & 60.00 & 60.00\
10 & LazyRRT & 60.00 & 60.00 & 55.56 & 60.00 & 60.00 & 60.00 & 60.00\
11 & TRRT & 60.00 & 60.00 & *[0.81]{style="color: Mycolor1"}* & 42.08 & 60.00 & 60.00 & 60.00\
12 & BiTRRT & 11.54 & 54.30 & *[4.57]{style="color: Mycolor1"}* & 60.00 & 60.00 & 60.00 & 60.00\
13 & LBTRRT & 60.00 & 60.00 & 60.00 & 60.00 & 60.00 & 60.00 & 60.00\
14 & RLRT & 60.00 & 60.00 & 51.39 & *[3.68]{style="color: Mycolor1"}* & 28.47 & 60.00 & 60.00\
15 & BiRLRT & 60.00 & 57.40 & 60.00 & *[1.52]{style="color: Mycolor1"}* & 25.60 & 60.00 & 60.00\
16 & pRRT & 60.00 & 60.00 & 49.41 & 60.00 & 60.00 & 60.00 & 60.00\
17 & FMT & 60.00 & 60.00 & 60.00 & 60.00 & 60.00 & 60.00 & 60.00\
18 & BFMT & 60.00 & 50.34 & 60.00 & 60.00 & 60.00 & 60.00 & 60.00\
19 & PRM & 60.00 & 56.47 & 60.00 & 37.25 & 52.72 & 60.00 & 60.00\
20 & PRM\* & 60.00 & 57.80 & 60.00 & 34.24 & 50.04 & 60.00 & 60.00\
21 & LazyPRM & 60.00 & 60.00 & 60.00 & 60.00 & 60.00 & 60.00 & 60.00\
22 & LazyPRM\* & 60.00 & 60.00 & 60.00 & 54.06 & 60.00 & 60.00 & 60.00\
23 & SPARS & 60.00 & 59.73 & 60.00 & 60.00 & 60.00 & 60.00 & 60.00\
24 & SPARStwo & 60.00 & 54.69 & 60.00 & 60.00 & 60.00 & 60.00 & 60.00\
25 & SST & 60.00 & 60.00 & 60.00 & 60.00 & 60.00 & 60.00 & 60.00\
26 & EST & 60.00 & 60.00 & 50.46 & 24.96 & 45.64 & 60.00 & 60.00\
27 & BiEST & 60.00 & 60.00 & 59.85 & 29.79 & 33.36 & 60.00 & 60.00\
28 & InformedRRT\* & 60.00 & 60.00 & - & 60.00 & 60.00 & 60.00 & 60.00\
29 & SORRT\* & 60.00 & 60.00 & - & 60.00 & 60.00 & 60.00 & 60.00\
30 & kBIT\* & 60.00 & 60.00 & - & 34.17 & 46.44 & 60.00 & 60.00\
31 & kABIT\* & 60.00 & 60.00 & - & 50.28 & 44.56 & 60.00 & 60.00\
32 & AIT\* & 60.00 & 60.00 & - & 55.35 & 60.00 & 60.00 & 60.00\
33 & STRIDE & 60.00 & 60.00 & - & 29.58 & 48.98 & 60.00 & 60.00\
34 & ProjEST & 60.00 & 60.00 & - & 47.77 & 60.00 & 60.00 & 60.00\
35 & PDST & 60.00 & 60.00 & - & *[3.25]{style="color: Mycolor1"}* & 54.42 & 60.00 & 60.00\
36 & KPIECE1 & 60.00 & 60.00 & - & *[6.27]{style="color: Mycolor1"}* & 32.48 & 60.00 & 60.00\
37 & BKPIECE1 & 60.00 & 60.00 & - & 52.35 & 60.00 & 60.00 & 60.00\
38 & LBKPIECE1 & 60.00 & 49.79 & - & 60.00 & 60.00 & 60.00 & 60.00\
39 & SBL & 60.00 & 50.30 & - & 60.00 & 60.00 & 60.00 & 60.00\
40 & CForest & 60.00 & 60.00 & - & 60.00 & 60.00 & 60.00 & 60.00\
:::

::: tabulary
\@LLCCCCCCC@ & & & & & & &\
& QMP (**ours**) & **0.51** & **1.27** & **1.91** & **0.86** & **18.98** & **1.20** & **14.52**\
2 & QMP (SideStepping) & 60.00 & 26.08 & 60.00 & 1.07 & 55.37 & 6^a^ & 60.00\
& QMP\* (**ours**) & **0.90** & **1.63** & **7.29** & **0.86** & **1.94** & **1.63** & **37.27**\
4 & QMP\* (SideStepping) & 60.00 & 30.11 & 60.00 & 1.76 & 60.00 & 12^a^ & 60.00\
& QRRT (**ours**) & **4.45** & **1.86** & **0.55** & **2.01** & **35.63** & **19.80** & 60.00\
6 & QRRT (SideStepping) & 60.00 & 27.72 & 9.14 & 18.65 & 60.00 & 44^a^ & 60.00\
& QRRT\* (**ours**) & **24.87** & **2.00** & **0.56** & **25.35** & **43.95** & 60.00 & 60.00\
8 & QRRT\* (SideStepping) & 60.00 & 60.00 & 16.42 & 42.33 & 54.05 & **48**^a^ & 60.00\
:::

^a^ Taken from [@Orthey2020IJRR].

To evaluate our pattern dance algorithm, we integrate it into the multilevel planner QRRT, QRRT\*, QMP and QMP\*, as we discussed in Sec. [\[sec:multilevelplanner\]](#sec:multilevelplanner){reference-type="ref" reference="sec:multilevelplanner"}. We then conduct two comparisons. First, we compare our planner to $36$ available planning algorithms in the Open motion planning library (OMPL) [@Moll2015] on $7$ challenging environments as shown in Fig. [16](#fig:scenarios){reference-type="ref" reference="fig:scenarios"}. For each algorithm, we use the abbreviated name. For a full list of algorithms with full names and associated publication, see [@Orthey2020IJRR] and the OMPL documentation [@Sucan2012]. Second, we compare the multilevel planner with the pattern dance algorithm to an older version of the same multilevel planner, where we use a recursive sidestepping algorithm to quickly find sections [@Orthey2020IJRR].

## Evaluation Metric

To evaluate, we use a 8GB RAM 4-core 2.5GHz laptop running Ubuntu 16.04. For each experiment, we use a minimum length cost (for planner which support cost functions) and we let each planner run $10$ times with a cut-off time limit of $60$ seconds. We then report on the average runtime over those $10$ runs. We show the results in Table [\[table:eval1\]](#table:eval1){reference-type="ref" reference="table:eval1"}.

Concerning the results, there are two notes of caution. First, we let each OMPL planner run out-of-the-box without any parameter tuning. Further tuning of parameters could potentially improve results significantly. Second, due to the high number of planner and scenarios, we let each planner run only $10$ times and take the average. However, averaging over $10$ runs might exhibit more variance and thereby create more outliers.

## 06-dof Bugtrap

For the first evaluation, we use the Bugtrap scenario [@Lee2012] (Fig. [9](#fig:scenarios:bugtrap){reference-type="ref" reference="fig:scenarios:bugtrap"}). The lowest runtime we found in the literature is $22.17$s for a version of the Selective-Retraction-RRT [@Lee2012; @Zhang2008Retraction]. However, this runtime is not directly comparable due to different hardware, implementation, parameters and operating systems. To relax the problem, we use an inscribed sphere at the center of the cylindrical bug as shown in Fig. [23](#fig:simplifications:bugtrap1){reference-type="ref" reference="fig:simplifications:bugtrap1"} and Fig. [20](#fig:simplifications:bugtrap2){reference-type="ref" reference="fig:simplifications:bugtrap2"}.

We show the results of our evaluation in Fig. [\[table:eval1\]](#table:eval1){reference-type="ref" reference="table:eval1"}. The best performing planner is QMP (3rd planner in table) with $0.51$s followed by QMP\* (4) with $0.90$s and QRRT (1) with $4.45$s. We also see good performance of the BiTRRT (13) planner [@Jaillet2010] with $11.54$s. We note that the QRRT\* (2) algorithm requires $24.87$s, which we believe to be caused by the additional burden of rewiring the tree [@Salzman2016; @Orthey2020IJRR].

## 06-dof Double L shape

In the next evaluation, we like to show that the section patterns are not specific to the cylindrical geometry, but are more widely applicable to other rigid bodies. As demonstration, we use the double L-shape scenario [@VanDenBerg2005], where two L-shape bodies are connected to each other as shown in Fig. [10](#fig:scenarios:doubleLshape){reference-type="ref" reference="fig:scenarios:doubleLshape"}. The task is to move through a vertical wall with a small quadratic hole. We use a two-level relaxation by using an inscribed sphere as shown in Fig. [24](#fig:simplifications:dls1){reference-type="ref" reference="fig:simplifications:dls1"} and Fig. [21](#fig:simplifications:dls2){reference-type="ref" reference="fig:simplifications:dls2"}. To make our method more robust against base paths too close to obstacles, we increase the size of the sphere slightly to increase clearance from obstacles.

Our evaluation shows that QMP performs best with $1.27$s followed by QMP\* ($1.63$s), QRRT ($1.86$s) and QRRT\* ($2.00$s). The next best planner from OMPL is LBKPIECE1 (38) with $49.79$s.

## 10-dof Chain Egress

In the third evaluation, we like to increase the complexity by considering an articulated chain ($10$-dof) as shown in Fig. [11](#fig:scenarios:chainegress){reference-type="ref" reference="fig:scenarios:chainegress"}. The task is to remove the chain from a pipe, a typical egress scenario. Note that for such systems, we can find analytical feasible path sections if we assume the base path of the head to be curvature constrained [@Orthey2018RAS]. However, we will not make such assumption in this paper.

To relax the problem, we use an inscribed sphere in the head of the chain as shown in Fig. [25](#fig:simplifications:chain1){reference-type="ref" reference="fig:simplifications:chain1"} and Fig. [22](#fig:simplifications:chain2){reference-type="ref" reference="fig:simplifications:chain2"}. As in the case of the double L-shape, we slightly increase the size of the sphere to make our method more robust against base paths too close to obstacles.

In our evaluations, we show that QRRT performs best with $0.55$s followed by QRRT\* ($0.56$s). The next best planners are TRRT (11) ($0.81$s), QMP ($1.91$), BiTRRT (12) ($4.57$s) and QMP\* with $7.29$s. Note that there are $12$ OMPL planner which cannot address this problem, because they do not support compound state spaces or do not have dedicated projection functions for such spaces.

## 37-dof Pre-Grasp

For the next evaluations, we compute (pre-)grasping paths for a ShadowHand mounted on a KUKA LWR robot. The tasks are to compute an overhand grasp on a ball (Fig. [12](#fig:scenarios:overhand){reference-type="ref" reference="fig:scenarios:overhand"}), an underhand grasp on a metal piece (Fig. [13](#fig:scenarios:underhand){reference-type="ref" reference="fig:scenarios:underhand"}), a single-finger precision grasp on a mug (Fig. [14](#fig:scenarios:mug){reference-type="ref" reference="fig:scenarios:mug"}) and a double-finger precision grasp on a scissor (Fig. [15](#fig:scenarios:scissor){reference-type="ref" reference="fig:scenarios:scissor"}). The starting state for all scenarios is an upright position of the arm with hand being open, as shown in Fig. [17](#fig:simplifications:hand3){reference-type="ref" reference="fig:simplifications:hand3"}. To relax the problem, we use a three-level abstraction by first removing three fingers (Fig. [18](#fig:simplifications:hand2){reference-type="ref" reference="fig:simplifications:hand2"}) and subsequently removing the thumb (Fig. [19](#fig:simplifications:hand1){reference-type="ref" reference="fig:simplifications:hand1"}) of the hand.

Our evaluations show the following results. First, for the Ball scenario, we see that QMP and QMP\* perform best with $0.86$s. The next best planner is the OMPL planner BiRLRT (15) [@Luna2020] with $1.52$s, QRRT with $2.01$s and RRTConnect (6) with $1.70$s. We note that also the planner PDST (35) [@Ladd2004], RLRT (14) [@Luna2020] and KPIECE1 (36) [@Sucan2011] perform competively with $3.25$s, $3.68$s and $6.27$s, respectively. The planner QRRT\* does not perform well on this problem instance with $25.35$s, due to similar problems as on the Bugtrap scenario. Second, for the underhand grasp on the metal piece, we see that QMP\* performs best with $1.94$s followed by RRTConnect (6) with $8.16$s and QMP with $18.98$s. We will address the discrepancy between QMP and QMP\* further in Sec. [\[sec:limitations\]](#sec:limitations){reference-type="ref" reference="sec:limitations"}. Third, for the single-finger precision grasp on the mug, we observe that QMP performs best with $1.20$s followed by QMP\* with $1.63$s. While QRRT performs significantly worse ($19.80$s), QRRT\* was not able to solve this problem ($60.00$s). Fourth, for the double-finger precision grasp on the scissor, we observe that QMP performs best with $14.52$s followed by QMP\* with $37.27$s. No other planner is able to solve this problem. We will further discuss the high runtime of both QMP and QMP\* in detail in Sec. [\[sec:limitations\]](#sec:limitations){reference-type="ref" reference="sec:limitations"}.

# Limitations and Discussion[]{#sec:limitations label="sec:limitations"}

While our evaluations support the usage of section patterns for narrow passage planning problems, we also like to point out two limitations of our approach. To each limitation, we will discuss possible ways to eventually address and resolve the limitation.

:::: {#fig:limitations .figure latex-placement="ht"}
![](Orthey2020Section_figs/multimodal1.png){width="\\linewidth"}

![](Orthey2020Section_figs/multimodal2.png){width="\\linewidth"}

::: caption
Limitations of Section Pattern Approach. Base path does not admit a feasible path section. See text for clarification. []{#fig:limitations label="fig:limitations"}
:::
::::

::: tabulary
\@LCCCCCCCCCC@ Run & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 & 10\
\
QMP & 1.53 & 1.11 & 1.20 & 0.99 & 1.06 & 60.00 & 60.00 & 2.93 & 1.02 & 60.00\
QMP\* & 0.98 & 1.15 & 0.93 & 1.23 & 2.73 & 1.13 & 1.03 & 7.61 & 0.98 & 1.65\
\
QMP & 1.45 & 1.50 & 2.14 & 2.17 & 60.00 & 60.00 & 2.44 & 7.49 & 1.51 & 6.51\
QMP\* & 60.00 & 60.00 & 2.22 & 60.00 & 6.27 & 60.00 & 60.00 & 60.00 & 1.92 & 2.30\
:::

## Increased runtime on Metal and Scissor Scenario

The first limitation is the increased runtime of our planner on the 37D ShadowHand Scissor and the Metal scenario. We distinguish between two subproblems. First, we observe that QRRT and QRRT\* have a runtime of $60$s on the Scissor scenario. Both scenarios, however, are ingress scenarios, where the planner needs to find a narrow passage on the base space to enter the goal region, which is challenging for RRT-like algorithms [@Kuffner2000] and could be addressed using a bidirectional version of QRRT.

Second, we observe that QMP and QMP\* require $14.52$s and $37.27$s to solve the Scissor scenario and that QMP requires $18.98$s to solve the Metal scenario. To explain this rather large increase in runtime, we have a closer look at the individual runtimes, which we show in Table [\[table:limitations\]](#table:limitations){reference-type="ref" reference="table:limitations"}. We can observe that both planner exhibit one of two outputs. Either, they quickly return a solution (usually less than $3$s, always less than $10$s) or they fail and time out at $60$s (three/two times for QMP, zero/six times for QMP\*). To us, this indicates that both algorithms might be sensitive to the base space path. If the base path is not smooth enough, has kinks in it or is too close to obstacles, then we might not be able to solve it with the pattern dance algorithm. We could address this problem in the future by either additional smoothing of the base space path [@Vidal2019], by introducing conservative heuristics [@Chatterjee2019] or by switching to a different relaxed model [@Styler2017].

## Base path does not admit a feasible section

While all multilevel planner are probabilistically complete, we often need the pattern dance algorithm to efficiently solve a problem. However, we might encounter scenarios, where the base path does not admit a feasible path section. Such a situation is shown in Fig. [27](#fig:limitations){reference-type="ref" reference="fig:limitations"}. The scenario depicts an X-shape robot, which has to traverse a shape-sorter box with different openings, which we relax by inscribing a sphere (right). Planning for the spherical robot might produce a base path going through the wrong hole. Such a base path does not admit a feasible path section, meaning there are no paths along the path restriction of the base path to traverse towards the goal. While multilevel planner are probabilistically complete and would eventually resolve the situation, we would not be able to solve this situation using our pattern dance algorithm. To address such situations, we could either compute several base paths [@Orthey2020WAFR; @Ha2019; @Vonasek2019; @Osa2020; @bhattacharya_2018; @pokorny_2016_ijrr] and consider them as a multi-arm bandit problem over path restrictions [@Kurniawati2008] or we could automatically choose an alternative relaxation using either a meta-heuristic [@Brandao2020] or a brute-force search [@Orthey2019].

# Conclusion

We developed the pattern dance algorithm, which takes as input a base space path and efficiently searches for a feasible section in its path restriction using four dedicated section patterns, which we named Manhattan, Wriggle, Tunnel and Triple step. We showed in evaluations, that our pattern dance algorithm successfully coordinates section patterns and outperforms a similar sidestepping algorithm [@Orthey2020IJRR]. We then showed that multilevel motion planning algorithms using our pattern dance algorithm outperform classical planner from the OMPL library on challenging narrow passage scenarios including the Bugtrap, chain egress and precision grasping. With some exceptions, we often observed runtime improvements by one to two orders of magnitudes.

While we demonstrated to efficiently solve narrow passage problems, we also pointed out two limitations. First, we observe an increased runtime in some planning instances. We could address this problem by either optimizing the base path [@Zhang2009], by improved neighborhood modeling [@lacevic_2020] or by learning the section patterns themselves [@Ichter2018]. Second, we cannot handle cases where the base path does not admit a path section. We could address this problem by computing multiple base paths [@Orthey2020WAFR; @Osa2020; @Vonasek2019] or using more informed graph restriction sampling methods [@Orthey2019].

Despite limitations, we believe to have contributed a novel solution method which we can use to efficiently find sections over base path restrictions. We believe our method to be a promising tool to further probe, understand and efficiently exploit high-dimensional state spaces.

# Acknowledgement

Marc Toussaint thanks the Max Planck Institute for Intelligent Systems for the Max Planck Fellowship.

::: IEEEbiography
Andreas Orthey

is a postdoctoral researcher in computational robotics at the TU Berlin funded by the Max Planck Institute for Intelligent Systems (MPI-IS). Previously, he has been a Research Fellow with the Alexander von Humboldt Foundation (AvH) at the University of Stuttgart, the Japan Society for the Promotion of Science (JSPS) at the AIST in Tsukuba, Japan, a Postdoctoral Researcher at the Worcester Polytechnic Institute (WPI), MA, USA and a Doctoral Candidate at the LAAS-CNRS in Toulouse, France. He holds a PhD Degree from INP Toulouse and a Master's Degree with Honours from the TU Berlin. His research interest lies in optimization and planning for complex and high-dimensional robotic systems.
:::

::: IEEEbiography
Marc Toussaint is professor for Intelligent Systems at TU Berlin since March 2020 and Max Planck Fellow at the MPI for Intelligent Systems since November 2018. In 2017/18 he spend a year as visiting scholar at MIT, before that some months with Amazon Robotics, and was professor for Machine Learning and Robotics at the University of Stuttgart since 2012. In his view, a key in understanding and creating intelligence is the interplay of learning and reasoning, where learning becomes the enabler for strongly generalizing reasoning and acting in our physical world. His research therefore bridges between AI planning, machine learning, and robotics. His work was awarded best paper at R:SS'18 and ICMLA'07, and runner up at R:SS'12 and UAI'08.
:::

[^1]: $^{1}$Max Planck Institute for Intelligent Systems, Stuttgart, Germany. Marc Toussaint thanks the MPI-IS for the Max Planck Fellowship. `aorthey``@is.mpg.de`

[^2]: $^{2}$Technical University of Berlin, Germany

[^3]: ©2020 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or reuse of any copyrighted component of this work in other works.

[^4]: <https://github.com/aorthey/MotionExplorer/> and <https://github.com/aorthey/ompl/>.
