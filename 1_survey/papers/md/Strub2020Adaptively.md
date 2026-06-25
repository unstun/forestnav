---
citation_key: Strub2020Adaptively
arxiv_id: 2002.06599
arxiv_url: https://arxiv.org/abs/2002.06599
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:43:20Z
origin: ai+web
reviewed: false
---

# Introduction {#sec:introduction}

Path planning is the problem of finding a continuous sequence of valid states between a start and goal specification. Sampling-based planners, such as Probabilistic Roadmaps (PRM) [@kavraki1996], approximate the state space by sampling discrete states and connecting them with edges. The resulting structure can then be processed by graph-search algorithms to find a sequence of states that connects the start to the goal.

Informed graph-search algorithms, such as A\* [@hart1968], use knowledge about a problem domain to increase their efficiency. This knowledge is often captured in the form of a *heuristic function*, $\widehat{h}$, which estimates cost-to-go, i.e., the cost to go from any state in the state space to the goal.

The properties of this heuristic directly affect the performance of the search algorithms. An *admissible* heuristic never overestimates the actual cost-to-go. A *consistent* heuristic satisfies a triangle-inequality, such that for any two states, $\bm{\mathrm{x}}_{i}, \bm{\mathrm{x}}_{j}$, it satisfies $\widehat{h}\left(\bm{\mathrm{x}}_{i}\right) \leq p(\bm{\mathrm{x}}_{i}, \bm{\mathrm{x}}_{j}) + \widehat{h}\left(\bm{\mathrm{x}}_{j}\right)$, where $p(\bm{\mathrm{x}}_{i}, \bm{\mathrm{x}}_{j})$ is the best cost of any path from $\bm{\mathrm{x}}_{i}$ to $\bm{\mathrm{x}}_{j}$. Note that by definition all consistent heuristics are also admissible. A\* is guaranteed to find the optimal solution when provided with an admissible heuristic. If the provided heuristic is also consistent, then A\* expands the minimum number of states of any informed graph-search algorithm using that heuristic (i.e., it is *optimally efficient* [@hart1968]).

Improving the accuracy of a heuristic directly improves the performance of informed search algorithms [@korf1997; @culberson1998; @felner2004; @paden2017], and the search becomes trivial when a perfect heuristic is available.

Designing and selecting effective heuristics is difficult for many problem domains. This is because heuristics are most effective when they are both accurate and computationally inexpensive to evaluate. Heuristics that are applicable to an entire problem domain are often inexpensive to evaluate but may not be accurate for a specific problem instance. Accurate heuristics can be designed for a specific problem instance during the search, but this can be computationally expensive and may diminish the overall search performance.

:::: {#fig:teaser .figure latex-placement="t"}
![](Strub2020Adaptively_figs/teaser0b.jpg){width="\\columnwidth"}

::: caption
AIT\* uses an asymmetric bidirectional search that is specialized for path planning problems with computationally expensive edge evaluations, such as those posed by NASA/JPL-Caltech's Axel Rover System [@nesnas2012].
:::
::::

Computational cost directly influences the real-world performance of planning algorithms. Sampling-based planners contain a number of computationally expensive basic operations, including state expansions and edge evaluations [@kleinbort2016]. State expansions often require nearest neighbor searches that increase in computational cost with the number of samples. Edge evaluations require local planning between two states and detecting collisions on the resulting path.

Lazy sampling-based planners, such as Lazy PRM [@bohlin2000], reduce this computational cost by avoiding the evaluation of every edge. These algorithms first perform an inexpensive search on a simplified approximation without collision detection. This allows them to only evaluate the edges that are believed to be on an optimal path, and reduce the number of evaluated edges. This improves performance, especially for problems with computationally expensive edge evaluations, such as those considered in this paper.

This paper presents Adaptively Informed Trees (AIT\*), a lazy, almost-surely asymptotically optimal sampling-based planner that uses an asymmetric bidirectional search to simultaneously estimate and exploit an accurate, problem-specific heuristic. AIT\* estimates this heuristic by performing a lazy reverse search on the current sampling-based approximation. This heuristic is then used to order the forward search of this approximation while considering complete edge evaluations. The results of the computationally expensive edge evaluations performed by this forward search inform the reverse search, which creates increasingly accurate heuristics. This allows AIT\* to efficiently share information between the two individual searches.

Efficiently estimating and exploiting a problem-specific heuristic allows AIT\* to outperform existing sampling-based planning algorithms when edge evaluations are expensive. AIT\* finds initial solutions to the tested problems at least as fast as RRT-Connect while still almost-surely converging to the optimal solution, which RRT-Connect does not.

# Background {#sec:background}

Creating and adapting heuristics to improve informed graph-search algorithms is an active area of research (Sec. [2.1](#sec:improved-heuristics-for-informed-search-algorithms){reference-type="ref" reference="sec:improved-heuristics-for-informed-search-algorithms"}). Heuristics are applied in sampling-based planning to reduce search effort by ordering the search and focus the approximation to the relevant region of the state space (Sec. [2.2](#sec:sampling-based-path-planning-with-heuristics){reference-type="ref" reference="sec:sampling-based-path-planning-with-heuristics"}). Lazy search algorithms separately focus on reducing search effort by avoiding collision detection (Sec. [2.3](#sec:sampling-based-path-planning-with-lazy-collision-detection){reference-type="ref" reference="sec:sampling-based-path-planning-with-lazy-collision-detection"}).

## Improved Heuristics for Informed Search Algorithms {#sec:improved-heuristics-for-informed-search-algorithms}

Improving the heuristic for informed graph-search algorithms has been shown to be effective for many problem domains, including path planning [@paden2017].

Pattern Databases [@culberson1998] are precomputed tables of exact solution costs to simplified subproblems of a problem domain. An informed algorithm can use this database during the search to create admissible heuristics. Additive Pattern Databases [@felner2004] extend this approach to combine database entries into more accurate heuristics that are still admissible. This approach speeds up the search of problems for which simplified subproblems can be created and solved, but requires creating databases for every problem domain *a priori* to the search.

Heuristic accuracy can alternatively be improved by using the error in the heuristic values of states as they are discovered. Thayer et al. [@thayer2011] use the error of each state expansion to update the heuristic during the search. This can be applied to any problem domain and does not require any preprocessing, but the resulting heuristic is not guaranteed to be admissible.

Adaptive A\* [@koenig2005; @koenig2006a] is an incremental search algorithm that updates its heuristic function based on the cost-to-come values of previous searches of similar problems. This results in ever more accurate and admissible heuristics but can not be used for the initial search of a graph.

Kaindl. et al [@kaindl1997] use the *Add method* to inform a forward search with a partial reverse search. The reverse search reveals errors in the heuristic values, the minimum of which is added to all unexpanded states. This results in a more informed but still admissible heuristic, but requires the user to specify how many states to expand during the reverse search and increases the heuristic uniformly for all unexpanded states. Wilt et al. [@wilt2013] present an updated version of this method which does not require a user-specified parameter.

Unlike these approaches, AIT\* does not need a predefined database, creates a consistent heuristic during the search, can be used on the initial search of a graph, and adaptively estimates the heuristic for each state individually.

## Sampling-Based Planning with Heuristics {#sec:sampling-based-path-planning-with-heuristics}

Heuristics have been used in sampling-based planning to guide the search and focus the approximation. RRT-Connect [@kuffner2000] builds on Rapidly-exploring Random Trees (RRT) [@lavalle2001] by incrementally growing two trees, one rooted in the start state and one in the goal state. These trees each explore the state space around them but are also guided towards each other by a *connect heuristic*. This approach can result in very fast initial solution times but is not almost-surely asymptotically optimal and does not improve the solution quality with more computational time.

Informed RRT\* [@gammell2018] incorporates an ellipsoidal heuristic into the almost-surely asymptotically optimal RRT\* [@karaman2011]. This improves the convergence rate by focusing the incremental approximation to the relevant region of the state space but does not guide the search.

Sakcak et al. [@sakcak2019a] incorporate a heuristic into a version of RRT\* which is based on motion-primitives [@sakcak2019b]. This can improve the performance for kinodynamic systems but requires preprocessing and relies on an *a priori* discretization which suffers from the *curse of dimensionality* [@bellman1957].

Batch Informed Trees (BIT\*) [@gammell2015; @gammell2020] samples batches of states and views these sampled states as an increasingly dense edge-implicit random geometric graph (RGG) [@penrose2003]. This allows BIT\* to use a series of informed graph-searches to process the states in order of potential solution quality. BIT\* efficiently reuses information from both previous searches and approximations by using incremental search techniques but does not update its heuristic during the search.

Unlike these approaches, AIT\* improves its solution quality with more computational time, uses its heuristic to guide the search, does not rely on an *a priori* discretization, and updates its heuristic during the search.

## Sampling-Based Planning with Lazy Collision Detection {#sec:sampling-based-path-planning-with-lazy-collision-detection}

Path planning algorithms employ lazy collision detection to avoid spending computational resources on edges that are unlikely to be on an optimal path. Lazy PRM [@bohlin2000] approximates the entire state space with an RGG without collision detection and searches this RGG for a path from the start state to a goal state. This path is then checked for collisions. If collisions are detected, then the corresponding edges and vertices are removed from the graph and a new search must be started from scratch. There also exist almost-surely asymptotically optimal variants of Lazy PRM [@hauser2015; @kim2018].

Lazy Shortest Path (LazySP) [@dellin2016] is a class of algorithms that reduces the number of edges checked for collisions. It first finds a path from the start to the goal using an inexpensive estimate of the edge costs. Once a path is found, it uses an *edge selector* function which determines the order in which these edges are checked for collision. An example of a LazySP algorithm is Lazy Receding Horizon A\* (LRHA\*) [@mandalika2018].

Unlike these approaches, AIT\* does not restart its search from scratch upon detecting collisions, and uses admissible heuristics to focus its approximation.

# Adaptively Informed Trees (AIT\*) {#sec:adaptively-informed-trees}

BIT\* is an almost-surely asymptotically optimal sampling-based planner that builds a discrete approximation of a state space by sampling batches of states. This approximation can be focused to the region of the state space that can possibly improve a current solution with informed sampling [@gammell2018].

BIT\* views the states it samples as an increasingly dense, edge-implicit RGG. It processes the implicit RGG edges in order of potential solution quality, similar to an edge-queue version of Lifelong Planning A\* (LPA\*) [@koenig2004]. The true edge costs are evaluated lazily by maintaining a queue ordered by the sum of the current cost-to-come from the start to the edge's parent state, a heuristic of the edge cost, and a heuristic of the cost-to-go from the edge's child state to the goal state. Full details of BIT\* are in [@gammell2017; @gammell2020].

AIT\* builds on BIT\* by improving the accuracy of the used heuristic, which improves performance on problems with expensive edge evaluations. It uses an asymmetric bidirectional search to efficiently estimate and exploit an accurate heuristic for each problem instance (Fig. [2](#fig:heuristic-visualization){reference-type="ref" reference="fig:heuristic-visualization"}). The forward search is the same as in BIT\* but uses the heuristic provided by a computationally inexpensive reverse search. This heuristic can be updated efficiently when the forward search reveals that it contains errors by using an incremental algorithm, such as LPA\*, on the reverse search. Algorithm [\[alg:conceptual\]](#alg:conceptual){reference-type="ref" reference="alg:conceptual"} presents a conceptual overview of BIT\* and AIT\*. The full algorithmic details are provided in Algorithms [\[alg:technical\]](#alg:technical){reference-type="ref" reference="alg:technical"}--[\[alg:updatestate\]](#alg:updatestate){reference-type="ref" reference="alg:updatestate"}.

Since BIT\* is almost-surely asymptotically optimal when given an admissible heuristic [@gammell2020] and the reverse search of AIT\* results in an admissible heuristic for each approximation, AIT\* is almost-surely asymptotically optimal as well.

:::::: {#fig:heuristic-visualization .figure latex-placement="t"}
::: minipage
[]{#fig:euclidean-heuristic label="fig:euclidean-heuristic"}
:::

::: minipage
[]{#fig:adaptive-heuristic label="fig:adaptive-heuristic"}
:::

::: caption
BIT\* approximates the state space of a problem by sampling batches of states (black dots), which define an RGG with implicit edges (dotted connections). These edges are processed in order of potential solution quality, according to a heuristic cost-to-go estimate (thick dashed lines). *A priori* heuristics are often not problem specific and provide poor estimates of the cost-to-go. The Euclidean norm assigns the lowest potential solution cost to the yellow edge despite the presence of the obstacle (). By using a lazy reverse search, AIT\* is instead able to provide a more accurate heuristic adapted to the current approximation of the specific problem ().
:::
::::::

## Notation {#sec:notation}

The state space of the planning problem is denoted by $X= {\mathbb{R}}^{n}, n \in \mathbb{N}$, the start by $\bm{\mathrm{x}}_{\mathrm{init}}\in X$, and the goals by $X_{\mathrm{goal}}\in X$. The sampled states are denoted by $X_{\mathrm{sampled}}$.

The forward and reverse search trees are denoted by $\mathcal{F}= (V_{\mathcal{F}}, E_{\mathcal{F}})$, and $\mathcal{R}= (V_{\mathcal{R}}, E_{\mathcal{R}})$, respectively. The vertices in these trees, denoted by $V_{\mathcal{F}}$ and $V_{\mathcal{R}}$, are associated with valid states. The edges in the forward tree, $E_{\mathcal{F}}\subseteq V_{\mathcal{F}}\times V_{\mathcal{F}}$, represent valid connections between states, while the edges in the reverse tree, $E_{\mathcal{R}}\subseteq V_{\mathcal{R}}\times V_{\mathcal{R}}$, can lead through invalid regions of the problem domain. An edge consists of a parent state, $\bm{\mathrm{x}}_{\mathrm{p}}$, and a child state, $\bm{\mathrm{x}}_{\mathrm{c}}$, and is denoted as $(\bm{\mathrm{x}}_{\mathrm{p}}, \bm{\mathrm{x}}_{\mathrm{c}})$.

Let $\mathbb{R}_{\geq 0}^{\infty}$ denote the union of the nonnegative real numbers with infinity. The function $\widehat{g}\colon X\to \mathbb{R}_{\geq 0}^{\infty}$ represents an admissible heuristic of the cost-to-come from the start to a state. The function $g_{\mathcal{F}}\colon X\to \mathbb{R}_{\geq 0}^{\infty}$ represents the cost-to-come from the start state to a state through the current forward tree. This cost is taken to be infinite for any state without an associated vertex in the forward tree.

The function $\widehat{h}\colon X\to \mathbb{R}_{\geq 0}^{\infty}$ represents an admissible heuristic of the cost-to-go from a state to a goal. The function $\widehat{f}\colon X\to \mathbb{R}_{\geq 0}^{\infty}$ represents an admissible estimate of the cost of a path from the start to a goal constrained to go through a state, e.g., $\widehat{f}\left(\bm{\mathrm{x}}\right) \vcentcolon=\widehat{g}\left(\bm{\mathrm{x}}\right) + \widehat{h}\left(\bm{\mathrm{x}}\right)$. This estimate defines the informed set of states that could provide a better solution, $X_{\widehat{f}}\vcentcolon=\set{ \bm{\mathrm{x}}\in X\widehat{f}\left(\bm{\mathrm{x}}\right) \leq c_{\mathrm{current}}}$, where $c_{\mathrm{current}}$ is the current solution cost. The function $c\colon X\times X\to \mathbb{R}_{\geq 0}^{\infty}$ denotes the true edge cost between two states. The function $\widehat{c}\colon X\times X\to \mathbb{R}_{\geq 0}^{\infty}$ is an admissible estimate of this cost.

Let $A$ be a set and let $B$, $C$ be subsets of $A$. The notation $B \overset{+}{\leftarrow} C$ is used for $B \leftarrow B \cup C$ and $B \overset{-}{\leftarrow} C$ for $B \leftarrow B \setminus C$. The number of states sampled per batch is denoted by $m$.

::: algorithm
` initialize search, queue, and approximation `**`update the heuristic`**` `
:::

## Approximation {#sec:approximation}

AIT\* samples batches of states to build a discrete approximation of the state space. It uses informed sampling to focus its approximation to the region of the state space that can possibly improve the current solution (Alg. [\[alg:technical\]](#alg:technical){reference-type="ref" reference="alg:technical"}, line [\[alg:technical:line:sampling\]](#alg:technical:line:sampling){reference-type="ref" reference="alg:technical:line:sampling"}).

States that are within a radius, $r$, of each other are treated as neighbors (Alg. [\[alg:neighbors\]](#alg:neighbors){reference-type="ref" reference="alg:neighbors"}, line [\[alg:neighbors:line:rgg\]](#alg:neighbors:line:rgg){reference-type="ref" reference="alg:neighbors:line:rgg"}). Graph complexity is limited as states are sampled by decreasing this radius as in [@karaman2011], using the measure of the informed set, as in [@gammell2018], $$\begin{align*}
  r(q) \vcentcolon=\eta {\left( 2 \left( 1 + \frac{1}{n} \right) \left( \frac{\lambda{\left(\ifblank{X_{\widehat{f}}}{\:\cdot\:}{X_{\widehat{f}}}\right)}}{\zeta_{n}} \right) \left( \frac{\log\left( q \right)}{q} \right) \right)}^{\frac{1}{n}},
\end{align*}$$ where $q$ is the number of sampled states in the informed set, $\eta > 1$ is a tuning parameter, and $\lambda(X_{\widehat{f}})$ and $\zeta_{n}$ are the Lebesgue measures of the informed set and an $n$-dimensional unit ball, respectively. Faster-decreasing radii are provided in [@janson2015; @janson2018] but are not used in AIT\* for fairer comparison to existing algorithms as they are presented in the literature.

AIT\* always includes the existing connections in both the forward and the reverse search trees in its approximation (Alg. [\[alg:neighbors\]](#alg:neighbors){reference-type="ref" reference="alg:neighbors"}, lines [\[alg:neighbors:line:rggextbegin\]](#alg:neighbors:line:rggextbegin){reference-type="ref" reference="alg:neighbors:line:rggextbegin"}, [\[alg:neighbors:line:rggextend\]](#alg:neighbors:line:rggextend){reference-type="ref" reference="alg:neighbors:line:rggextend"}), and removes invalid edges, regardless of the distance (Alg. [\[alg:updateheuristic\]](#alg:updateheuristic){reference-type="ref" reference="alg:updateheuristic"}, line [\[alg:updateheuristic:line:blacklist\]](#alg:updateheuristic:line:blacklist){reference-type="ref" reference="alg:updateheuristic:line:blacklist"}; Alg. [\[alg:neighbors\]](#alg:neighbors){reference-type="ref" reference="alg:neighbors"}, line [\[alg:neighbors:line:blacklist\]](#alg:neighbors:line:blacklist){reference-type="ref" reference="alg:neighbors:line:blacklist"}).

::: algorithm
` `$V_{\mathcal{F}}\leftarrow{}\bm{\mathrm{x}}_{\mathrm{init}}$`; `$E_{\mathcal{F}}\leftarrow{}\emptyset$`; `$\mathcal{F}\leftarrow{}(V_{\mathcal{F}}, E_{\mathcal{F}})$`; `$c_{\mathrm{current}} \leftarrow{}\infty$` `$X_{\mathrm{sampled}}\leftarrow{}X_{\mathrm{goal}}\cup \{ \bm{\mathrm{x}}_{\mathrm{init}}\}$`; `$\mathcal{Q}_{\mathrm{F}}\leftarrow{}\texttt{expand}\left(\bm{\mathrm{x}}_{\mathrm{init}}\right)$`;`

**$\texttt{update\_heuristic}\left(\right)$**[]{#alg:technical:line:initialize-heuristic label="alg:technical:line:initialize-heuristic"}
:::

::: algorithm
$E_{\mathrm{out}} \leftarrow{}\emptyset$
:::

::: algorithm
$V_{\mathrm{neighbors}} \leftarrow{}\set{ \bm{\mathrm{x}}_{i} \in X_{\mathrm{sampled}}\norm{\bm{\mathrm{x}}- \bm{\mathrm{x}}_{i}} \leq r\left( q \right) }$[]{#alg:neighbors:line:rgg label="alg:neighbors:line:rgg"} $V_{\mathrm{neighbors}} \overset{+}{\leftarrow}\texttt{parent}_{\mathcal{F}}\left(\bm{\mathrm{x}}\right)$; $V_{\mathrm{neighbors}} \overset{+}{\leftarrow}\texttt{parent}_{\mathcal{R}}\left(\bm{\mathrm{x}}\right)$[]{#alg:neighbors:line:rggextbegin label="alg:neighbors:line:rggextbegin"} $V_{\mathrm{neighbors}} \overset{+}{\leftarrow}\texttt{children}_{\mathcal{F}}\left(\bm{\mathrm{x}}\right)$; $V_{\mathrm{neighbors}} \overset{+}{\leftarrow}\texttt{children}_{\mathcal{R}}\left(\bm{\mathrm{x}}\right)$[]{#alg:neighbors:line:rggextend label="alg:neighbors:line:rggextend"}
:::

## Reverse Search {#sec:reverse-search}

AIT\* estimates a heuristic specific to the current approximation by performing a lazy reverse search with LPA\* (Alg. [\[alg:updateheuristic\]](#alg:updateheuristic){reference-type="ref" reference="alg:updateheuristic"} and Alg. [\[alg:updatestate\]](#alg:updatestate){reference-type="ref" reference="alg:updatestate"}). This search uses a vertex-queue, $\mathcal{Q}_{\mathrm{R}}$, which sorts states according to a lexicographical key, $$\begin{align*}
  \texttt{key}_{\mathrm{R}}(\bm{\mathrm{x}}) \vcentcolon=&\left(\min\left\{ \widehat{h}_{\mathrm{con}}\left[\bm{\mathrm{x}}\right], \widehat{h}_{\mathrm{exp}}\left[\bm{\mathrm{x}}\right] \right\} + \widehat{g}\left(\bm{\mathrm{x}}\right),\right.\\ &\phantom{\Big(}\left.\min\left\{ \widehat{h}_{\mathrm{con}}\left[\bm{\mathrm{x}}\right], \widehat{h}_{\mathrm{exp}}\left[\bm{\mathrm{x}}\right] \right\} \right),
\end{align*}$$ where $\widehat{h}_{\mathrm{con}}\left[\bm{\mathrm{x}}\right]$ denotes the cost-to-go of $\bm{\mathrm{x}}$ when it was last connected to the reverse tree and $\widehat{h}_{\mathrm{exp}}\left[\bm{\mathrm{x}}\right]$ denotes the cost-to-go of $\bm{\mathrm{x}}$ when it was last expanded in the reverse search. These are the $g$ and $v$ values in a forward LPA\* search [@aine2016].

If Algorithm [\[alg:updateheuristic\]](#alg:updateheuristic){reference-type="ref" reference="alg:updateheuristic"} is called without an argument (Alg. [\[alg:technical\]](#alg:technical){reference-type="ref" reference="alg:technical"}, lines [\[alg:technical:line:initialize-heuristic\]](#alg:technical:line:initialize-heuristic){reference-type="ref" reference="alg:technical:line:initialize-heuristic"}, [\[alg:technical:line:reinitialize-heuristic\]](#alg:technical:line:reinitialize-heuristic){reference-type="ref" reference="alg:technical:line:reinitialize-heuristic"}), it sets the $\widehat{h}_{\mathrm{con}}$ and $\widehat{h}_{\mathrm{exp}}$ values of all states except the goals to infinity and inserts the goal states into the queue (Alg. [\[alg:updateheuristic\]](#alg:updateheuristic){reference-type="ref" reference="alg:updateheuristic"}, lines [\[alg:updateheuristic:line:restart-begin\]](#alg:updateheuristic:line:restart-begin){reference-type="ref" reference="alg:updateheuristic:line:restart-begin"}--[\[alg:updateheuristic:line:restart-end\]](#alg:updateheuristic:line:restart-end){reference-type="ref" reference="alg:updateheuristic:line:restart-end"}). This restarts LPA\*, which is more efficient than repairing the search when large changes in the graph are expected [@likhachev2005; @likhachev2008; @aine2016]. LPA\*'s initial search is equivalent to A\* and results in a consistent and admissible estimate of the heuristic in the current approximation.

If Algorithm [\[alg:updateheuristic\]](#alg:updateheuristic){reference-type="ref" reference="alg:updateheuristic"} is called with an invalid edge (Alg. [\[alg:technical\]](#alg:technical){reference-type="ref" reference="alg:technical"}, line [\[alg:technical:line:update-heuristic\]](#alg:technical:line:update-heuristic){reference-type="ref" reference="alg:technical:line:update-heuristic"}), then it adds the edge to the set of invalid edges, $E_{\mathrm{invalid}}$, and updates the cost-to-go of the parent state (Alg. [\[alg:updateheuristic\]](#alg:updateheuristic){reference-type="ref" reference="alg:updateheuristic"}, lines [\[alg:updateheuristic:line:blacklist\]](#alg:updateheuristic:line:blacklist){reference-type="ref" reference="alg:updateheuristic:line:blacklist"}, [\[alg:updateheuristic:line:update-parent-state\]](#alg:updateheuristic:line:update-parent-state){reference-type="ref" reference="alg:updateheuristic:line:update-parent-state"}). LPA\* then repairs the reverse search tree and increases the cost-to-go values, $\widehat{h}_{\mathrm{con}}$, as necessary. This results in an updated heuristic which is still admissible for the current approximation and can be used by the forward search. Full details of LPA\* are available in [@koenig2004; @likhachev2005; @aine2016].

## Forward Search {#sec:forward-search}

The forward search of AIT\* uses an edge-queue, $\mathcal{Q}_{\mathrm{F}}$, which sorts edges according to a lexicographical key, $$\begin{align*}
  \texttt{key}_{\mathrm{F}}(\bm{\mathrm{x}}_{\mathrm{p}}, \bm{\mathrm{x}}_{\mathrm{c}}) \vcentcolon=&\left( g_{\mathcal{F}}\left(\bm{\mathrm{x}}_{\mathrm{p}}\right) + \widehat{c}\left(\bm{\mathrm{x}}_{\mathrm{p}}, \bm{\mathrm{x}}_{\mathrm{c}}\right) + \widehat{h}\left(\bm{\mathrm{x}}_{\mathrm{c}}\right),\right.\\ &\left.\phantom{\Big(}g_{\mathcal{F}}\left(\bm{\mathrm{x}}_{\mathrm{p}}\right) + \widehat{c}\left(\bm{\mathrm{x}}_{\mathrm{p}}, \bm{\mathrm{x}}_{\mathrm{c}}\right),\; g_{\mathcal{F}}\left(\bm{\mathrm{x}}_{\mathrm{p}}\right) \right),
\end{align*}$$ where the cost-to-go values from the reverse search are used as heuristic for the forward search, i.e., $\widehat{h}\left(\bm{\mathrm{x}}\right) \vcentcolon=\widehat{h}_{\mathrm{con}}\left[\bm{\mathrm{x}}\right]$.

::: algorithm
:::

::: algorithm
:::

An iteration begins by getting the best edge from the queue and checking whether it can possibly improve the current solution (Alg. [\[alg:technical\]](#alg:technical){reference-type="ref" reference="alg:technical"}, line [\[alg:technical:line:can-edge-possibly-improve-solution\]](#alg:technical:line:can-edge-possibly-improve-solution){reference-type="ref" reference="alg:technical:line:can-edge-possibly-improve-solution"}). If it can and is already part of the forward tree, its child state is expanded (Alg. [\[alg:technical\]](#alg:technical){reference-type="ref" reference="alg:technical"}, line [\[alg:technical:line:freebie\]](#alg:technical:line:freebie){reference-type="ref" reference="alg:technical:line:freebie"}).

If it is not in the forward tree but can possibly improve it (Alg. [\[alg:technical\]](#alg:technical){reference-type="ref" reference="alg:technical"}, line [\[alg:technical:line:can-edge-possibly-improve-tree\]](#alg:technical:line:can-edge-possibly-improve-tree){reference-type="ref" reference="alg:technical:line:can-edge-possibly-improve-tree"}), then the edge is checked for validity (Alg. [\[alg:technical\]](#alg:technical){reference-type="ref" reference="alg:technical"}, line [\[alg:technical:line:collision-detection\]](#alg:technical:line:collision-detection){reference-type="ref" reference="alg:technical:line:collision-detection"}). If the edge is invalid, then the heuristic is updated by the reverse search (Alg. [\[alg:technical\]](#alg:technical){reference-type="ref" reference="alg:technical"}, line [\[alg:technical:line:update-heuristic\]](#alg:technical:line:update-heuristic){reference-type="ref" reference="alg:technical:line:update-heuristic"}; Alg [\[alg:updateheuristic\]](#alg:updateheuristic){reference-type="ref" reference="alg:updateheuristic"}). If the edge is valid, then it is completely evaluated. The search then checks whether it can actually improve the current solution and the forward tree (Alg. [\[alg:technical\]](#alg:technical){reference-type="ref" reference="alg:technical"}, lines [\[alg:technical:line:can-edge-actually-improve-solution\]](#alg:technical:line:can-edge-actually-improve-solution){reference-type="ref" reference="alg:technical:line:can-edge-actually-improve-solution"}, [\[alg:technical:line:can-edge-actually-improve-tree\]](#alg:technical:line:can-edge-actually-improve-tree){reference-type="ref" reference="alg:technical:line:can-edge-actually-improve-tree"}).

The child state of a new edge that can improve the current solution and the forward tree is added to the tree if it is not already in the tree (Alg. [\[alg:technical\]](#alg:technical){reference-type="ref" reference="alg:technical"}, line [\[alg:technical:line:add-state-to-tree\]](#alg:technical:line:add-state-to-tree){reference-type="ref" reference="alg:technical:line:add-state-to-tree"}). If it is, then the new edge is a rewiring and the old edge is removed (Alg. [\[alg:technical\]](#alg:technical){reference-type="ref" reference="alg:technical"}, line [\[alg:technical:line:rewiring\]](#alg:technical:line:rewiring){reference-type="ref" reference="alg:technical:line:rewiring"}). The new edge is added to the tree and its child state is expanded in both cases (Alg. [\[alg:technical\]](#alg:technical){reference-type="ref" reference="alg:technical"}, lines [\[alg:technical:line:add-edge-to-tree\]](#alg:technical:line:add-edge-to-tree){reference-type="ref" reference="alg:technical:line:add-edge-to-tree"}, [\[alg:technical:line:expand-child-state\]](#alg:technical:line:expand-child-state){reference-type="ref" reference="alg:technical:line:expand-child-state"}).

The iteration finishes by updating the current solution cost (Alg. [\[alg:technical\]](#alg:technical){reference-type="ref" reference="alg:technical"}, line [\[alg:technical:line:update-solution-cost\]](#alg:technical:line:update-solution-cost){reference-type="ref" reference="alg:technical:line:update-solution-cost"}). In practice this is done efficiently by only checking the goal states in the forward search tree.

If the forward search processes an edge that can not possibly improve the current solution, then a new search on a refined approximation is started (Alg. [\[alg:technical\]](#alg:technical){reference-type="ref" reference="alg:technical"}, lines [\[alg:technical:line:can-edge-possibly-improve-solution\]](#alg:technical:line:can-edge-possibly-improve-solution){reference-type="ref" reference="alg:technical:line:can-edge-possibly-improve-solution"}, [\[alg:technical:line:sampling\]](#alg:technical:line:sampling){reference-type="ref" reference="alg:technical:line:sampling"}--[\[alg:technical:line:reinitialize-heuristic\]](#alg:technical:line:reinitialize-heuristic){reference-type="ref" reference="alg:technical:line:reinitialize-heuristic"}).

# Experimental Results {#sec:experimental-results}

:::::: {#fig:experiments .figure latex-placement="t"}
::: minipage
[]{#fig:experiment-wall-gap label="fig:experiment-wall-gap"}
:::

::: minipage
[]{#fig:experiment-goal-enclosure label="fig:experiment-goal-enclosure"}
:::

::: caption
Two dimensional illustrations of the experiments on which the planners were tested. The green () and red () dots represent the positions of the start and goal states, respectively. Grey regions represent invalid states. Each state space dimension was bounded to the interval \[0, 1\], which is illustrated by the black bounding boxes.
:::
::::::

AIT\* was compared against the Open Motion Planning Library (OMPL) [@sucan2012] implementations of RRT-Connect, RRT\*, RRT${}^{\#}$ [@arslan2013], and BIT\* on simulated problems[^2]. RRT\* and RRT${}^{\#}$ used a goal bias of 5% and RRT${}^{\#}$ used rejection sampling. All RRT-based algorithms used maximum edge lengths of 0.5, 1.25, and 3.0 in $\mathbb{R}^{4}, \mathbb{R}^{8}$, and $\mathbb{R}^{16}$, respectively. BIT\* and AIT\* sampled 100 states per batch regardless of dimension and used the Euclidean norm for all *a priori* heuristics. The RGG constant $\eta$ was 1.001 for all planners.

## Abstract Problems {#sec:abstract-problems}

The planners were tested on two abstract problems with different obstacle configurations in $\mathbb{R}^{4}, \mathbb{R}^{8}$, and $\mathbb{R}^{16}$ (Fig. [3](#fig:experiments){reference-type="ref" reference="fig:experiments"}). Each planner was run 100 times with different random seeds on each instantiation. Planners were given one second to solve problems in $\mathbb{R}^{4}$, ten seconds in $\mathbb{R}^{8}$, and 100 seconds in $\mathbb{R}^{16}$. The collision detection resolution was set to $10^{-6}$ to make evaluating edge costs computationally expensive. The optimization objective was path length. Figure [4](#fig:results){reference-type="ref" reference="fig:results"} shows the achieved preformances of all tested planners on all problems.

One abstract problem consisted of a wall with a narrow gap, such that in all dimensions only two homotopy classes exist (Fig. [\[fig:experiment-wall-gap\]](#fig:experiment-wall-gap){reference-type="ref" reference="fig:experiment-wall-gap"}). This shows AIT\*'s performance on a problem containing a hard-to-find optimal homotopy class (Figs. [\[fig:results-wall-gap-r4\]](#fig:results-wall-gap-r4){reference-type="ref" reference="fig:results-wall-gap-r4"}--).

The other abstract problem consisted of a hollow, axis-aligned hyperrectangle enclosing the goal state configured such that even in higher dimensions the goal can only be reached through the face of the hyperrectangle farthest from the start state (Fig. [\[fig:experiment-goal-enclosure\]](#fig:experiment-goal-enclosure){reference-type="ref" reference="fig:experiment-goal-enclosure"}). This problem is challenging for AIT\* because there are many invalid edges close to the root of the reverse search tree which means that often large parts of it must be repaired (Figs. [\[fig:results-goal-enclosure-r4\]](#fig:results-goal-enclosure-r4){reference-type="ref" reference="fig:results-goal-enclosure-r4"}--).

## Planning for Axel {#sec:planning-for-axel}

The benefits of AIT\*'s asymmetric bidirectional search were also tested on simulated planning problems for NASA/JPL-Caltech's Axel Rover System (Fig. [1](#fig:teaser){reference-type="ref" reference="fig:teaser"}), which is specialized for challenging terrain. These problems require sequences of $\mathrm{SE}(3)$ poses settled on the surface manifold of the terrain. This makes edge evaluations expensive, as every state along an edge has to be projected onto the manifold.

BIT\* and AIT\* were run 100 times to plan a path down a steep slope with a line-of-sight distance of 30.97 meters between the start and goal positions (Fig. [\[fig:results-axel-map\]](#fig:results-axel-map){reference-type="ref" reference="fig:results-axel-map"}). The linear and angular collision detection resolutions were set to 2 cm and 0.1 rad, respectively. BIT\* and AIT\* optimized for path length and roll. Figure [5](#fig:results-axel){reference-type="ref" reference="fig:results-axel"} shows the achieved performances.

::::::::::: {#fig:results .figure latex-placement="t"}
::: minipage
[]{#fig:results-wall-gap-r4 label="fig:results-wall-gap-r4"}
:::

::: minipage
[]{#fig:results-wall-gap-r8 label="fig:results-wall-gap-r8"}
:::

::: minipage
[]{#fig:results-wall-gap-r16 label="fig:results-wall-gap-r16"}
:::

\

::: minipage
[]{#fig:results-goal-enclosure-r4 label="fig:results-goal-enclosure-r4"}
:::

::: minipage
[]{#fig:results-goal-enclosure-r8 label="fig:results-goal-enclosure-r8"}
:::

::: minipage
[]{#fig:results-goal-enclosure-r16 label="fig:results-goal-enclosure-r16"}
:::

\

::: minipage
:::

::: caption
Planner performances on the abstract problems described in Section [4.1](#sec:abstract-problems){reference-type="ref" reference="sec:abstract-problems"}. Results from the wall gap experiments are presented in plots (), (), and (), and from the goal enclosure experiment in plots (), (), and (). The squares in the cost plots show the median times and costs of the initial solutions with a nonparametric 99% confidence interval. The lines show the median cost over time for almost-surely asymptotically optimal planners (unsuccessful runs were taken as infinite costs). Note that in plots (), (), (), and () less than 50 trials of RRT\* and RRT${}^{\#}$ were successful, so the median solution cost is infinite for these planners. AIT\* finds initial solutions faster than RRT-Connect on four out of six problems, always faster than BIT\* with the Euclidean heuristic, and around an order of magnitude faster than RRT\* and RRT${}^{\#}$. The goal enclosure is a challenging problem for AIT\*, because many states close to the goal are initially connected through invalid edges, which results in large updates of the reverse tree.
:::
:::::::::::

::::::::: {#fig:results-axel .figure latex-placement="t"}
::: minipage
[]{#fig:results-axel-map label="fig:results-axel-map"}
:::

::: minipage
[]{#fig:results-axel-success label="fig:results-axel-success"}
:::

::: minipage
[]{#fig:results-axel-initial-solution-time label="fig:results-axel-initial-solution-time"}
:::

::: minipage
[]{#fig:results-axel-initial-solution-cost label="fig:results-axel-initial-solution-cost"}
:::

::: minipage
[]{#fig:results-axel-final-solution-cost label="fig:results-axel-final-solution-cost"}
:::

::: caption
Results from 100 trials of BIT\* and AIT\* on a problem for NASA/JPL-Caltech's Axel. The challenge was to plan down a steep slope () from the green dot (top right) to the red dot (bottom left), through two narrow passages. The map is colored by elevation. The plot () shows the achieved success rates after running for 100 seconds. The plots (), (), and () show the medians with nonparametric 99% confidence intervals of the initial solution times, the initial solution costs, and the final solution costs, respectively. Unsuccessful runs were taken as infinite costs. AIT\* achieves a higher success rate and slighly faster initial solution times but higher initial solution costs than BIT\*. Both planners achieve similar final solution costs.
:::
:::::::::

# Discussion & Future Work {#sec:discussion-and-future-work}

AIT\* was designed for planning problems with expensive edge evaluations. These often occur when the search has to consider dynamic constraints (e.g., two-point boundary value problems) or complex robot and obstacle interactions (e.g., difficult collision detection) for each edge, as found on NASA/JPL-Caltech's Axel. In future work, Axel will consider tether-terrain interaction and physics-based stability checks based on the anchor history of the tether, which will further increase the edge evaluation cost.

These expensive edge evaluations were simulated in the abstract problems by increasing the collision detection resolution, providing a simple way to increase the edge evaluation cost and evaluate AIT\* on illustrative obstacle configurations.

The adaptive heuristic of AIT\* is less effective when the lazy reverse search connects many states through invalid edges, especially if these edges are near the root of the reverse search tree. This was illustrated with the goal enclosure experiment (Fig. [\[fig:experiment-goal-enclosure\]](#fig:experiment-goal-enclosure){reference-type="ref" reference="fig:experiment-goal-enclosure"}). Future work could use sparse collision detection on the reverse search to mitigate this problem.

The reverse search of AIT\* could also be used to estimate the search effort instead of the solution cost. The forward search could then be replaced with an anytime search that explicitly tries to minimize the time to the next solution, similar to [@thayer2012], which could speed up initial solution times.

Another way to speed up initial solution times of AIT\* would be to inflate the heuristic term in the key of the forward queue, as in Advanced BIT\* (ABIT\*) [@strub2020].

# Conclusion {#sec:conclusion}

Informed sampling-based algorithms use heuristic knowledge about a problem domain to improve their performance. Heuristics that are applicable to all problems in a domain are often simple to define and inexpensive to evaluate but seldom accurate for a specific problem instance. Problem-specific heuristics can be very accurate but the computational cost to estimate and/or evaluate them can often outweigh the improved search efficiency.

This paper presents AIT\*, an almost-surely asymptotically optimal sampling-based planner that simultaneously estimates and exploits an accurate heuristic specific to each problem instance. AIT\* uses an asymmetric bidirectional search to efficiently share information between the individual searches. The computationally inexpensive reverse search informs the expensive forward search by providing accurate heuristics specific to the current approximation of each problem instance. The forward search informs the reverse search by providing information about invalid edges, which results in ever more accurate heuristics. This is done efficiently by using LPA\* as the reverse search algorithm.

This approach is promising for path planning problems with expensive edge evaluations, such as those posed by NASA/JPL-Caltech's Axel. AIT\* outperforms existing sampling-based algorithms on the tested abstract problems by finding an initial solution quickly and converging to the optimum in an anytime manner. These problems show the robustness of AIT\* with respect to expensive edge evaluations and encourage more thorough evaluations of states which could be used in more advanced optimization objectives.

Information on the OMPL implementation of AIT\* is available at [`https://robotic-esp.com/code/`](https://robotic-esp.com/code/).

[^1]: $^{1}$M. P. Strub and J. D. Gammell are with the Estimation, Search, and Planning (ESP) Group of the Oxford Robotics Institute (ORI), University of Oxford, United Kingdom. `(mstrub|gammell)@robots.ox.ac.uk`

[^2]: The performances were measured with OMPL v1.4.1 on a laptop with 16 GB of RAM and an Intel i7-4910MQ processor running Ubuntu 18.04.
