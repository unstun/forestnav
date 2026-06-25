---
citation_key: Salzman2014AsymptoticallyOptimal
arxiv_id: 1403.7714
arxiv_url: https://arxiv.org/abs/1403.7714
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T17:15:19Z
origin: ai+web
reviewed: false
---

# Terminology and algorithmic background {#sec:background}

We begin by formally stating the motion-planning problem and introducing several We continue by reviewing the FMT\* algorithm.

## Problem definition and terminology

Let $\ensuremath{\mathcal{X}}$, $\ensuremath{\mathcal{X}}_{\rm free}$ denote the Euclidean[^3] C-space and free space, respectively, and $d$ the dimension of the C-space. Let $(\ensuremath{\ensuremath{\mathcal{X}}_{\rm free}}, x_{\text{init}}, \ensuremath{\mathcal{X}}_{\text{goal}})$ be the motion-planning problem where: $x_{\text{init}} \in \ensuremath{\ensuremath{\mathcal{X}}_{\rm free}}$ is the initial free configuration of the robot and $\ensuremath{\mathcal{X}}_{\text{goal}} \subseteq \ensuremath{\ensuremath{\mathcal{X}}_{\rm free}}$ is the goal region. We will make use of the following procedures: `sample_free`$(n)$, a procedure returning $n$ random configurations from $\ensuremath{\mathcal{X}}_{\rm free}$; `nearest_neighbors`$(x,V,r)$ is a procedure that returns all neighbors of $x$ with distance smaller than $r$ within the set $V$; `collision_free`$(x,y)$ tests whether the straight-line segment connecting $x$ and $y$ is contained in $\ensuremath{\mathcal{X}}_{\rm free}$; `cost`$(x,y)$ returns the cost of the straight-line path connecting $x$ and $y$, namely, in our case, the distance. We consider weighted graphs $\ensuremath{\mathcal{G}}= (V,E)$, where the weight of an edge $(x,y) \in E$ is $\texttt{cost}(x,y)$. Given such a graph $\mathcal{G}$, we denote by $\texttt{cost}_{\ensuremath{\mathcal{G}}}(x, y)$ the cost of the weighted shortest path from $x$ to $y$. Let $\texttt{cost-to-come}_{\ensuremath{\mathcal{G}}}(x)$ be $\texttt{cost}_{\ensuremath{\mathcal{G}}}(x_{\text{init}}, x)$ and $\texttt{cost-to-go}_{\ensuremath{\mathcal{G}}}(x)$ be the minimal $\texttt{cost}_{\ensuremath{\mathcal{G}}}(x, x_{\text{goal}})$ for $x_{goal} \in \ensuremath{\mathcal{X}}_{\text{goal}}$. Namely for every node $x$, $\texttt{cost-to-come}_{\ensuremath{\mathcal{G}}}(x)$ is the minimal cost to reach $x$ from $x_\text{init}$ and $\texttt{cost-to-go}_{\ensuremath{\mathcal{G}}}(x)$ is the minimal cost to reach $\ensuremath{\mathcal{X}}_{\text{goal}}$ from $x$. Additionally, let $B_{\ensuremath{\mathcal{G}}}(x_{\text{init}},r)$, $B_{\ensuremath{\mathcal{G}}}(\ensuremath{\mathcal{X}}_{\text{goal}},r)$ be the set of all nodes whose cost-to-come (respectively, cost-to-go) value on $\ensuremath{\mathcal{G}}$ is smaller than $r$. Finally, we denote by `Dijkstra`$(G, x, c)$ an implementation of Dijkstra's algorithm[^4] running on the graph $G$ from $x$ until a maximal cost of $c$ has been reached. The algorithm's implementation updates the cost to reach each node from $x$ and outputs the set of nodes traversed.

Given a set of samples $V$, and a radius $r$, we denote by $G(V,r)$ the *disk graph*,[^5] which is the graph whose set of vertices is $V$ and two vertices $x,y \in V$ are connected by an edge if the distance between $x$ and $y$ is less than $r$.

## Fast Marching Trees (FMT\*)

FMT\*, outlined in Alg. [\[alg:fmt\]](#alg:fmt){reference-type="ref" reference="alg:fmt"}, performs a "lazy" dynamic programming recursion on a set of sampled configurations to grow a tree rooted at $x_{init}$ [@JP12]. The algorithm samples $n$ collision-free nodes $V$ (line 1). It searches for a path to $\ensuremath{\mathcal{X}}_{goal}$ by building a minimum-cost spanning tree growing in cost-to-come space (line 2 and detailed in Alg. [\[alg:search\]](#alg:search){reference-type="ref" reference="alg:search"}). As we explain in Section [3](#sec:alg){reference-type="ref" reference="sec:alg"}, the algorithm may benefit from using a heuristic function estimating the cost-to-go of a node and a bound on the maximal length of the path that should be found. As these are not part of the original formulation of FMT\*, we describe the search procedure of FMT\* using a cost-to-go estimation of zero for each node and an unbounded maximal path length (marked in red in Alg. [\[alg:fmt\]](#alg:fmt){reference-type="ref" reference="alg:fmt"} and [\[alg:search\]](#alg:search){reference-type="ref" reference="alg:search"}). This will allow us to use the same pseudo-code of Alg. [\[alg:search\]](#alg:search){reference-type="ref" reference="alg:search"} to explain the MPLB algorithm in Section [3](#sec:alg){reference-type="ref" reference="sec:alg"}.

The search-tree is built by maintaining two sets of nodes $H, W$ such that $H$ is the set of nodes added to the tree that may be expanded and $W$ is the set of nodes that have not yet been added to the tree (Alg. [\[alg:search\]](#alg:search){reference-type="ref" reference="alg:search"}, line 1). It then computes for each node the set of nearest neighbors[^6] of radius $r(n)$ (line 3). The algorithm repeats the following process: the node $z$ with the lowest cost-to-come value is chosen from $H$ (line 4 and 16). For each neighbor $x$ of $z$ that is not already in $H$, the algorithm finds its neighbor $y \in H$ such that the cost-to-come of $y$ added to the distance between $y$ and $x$ is minimal (lines 7-9). If the local path between $y$ and $x$ is free, $x$ is added to $H$ with $y$ as its parent (lines 10-12). At the end of each iteration $z$ is removed from $H$ (line 13). The algorithm runs until a solution is found or there are no more nodes to process.

To ensure AO, the radius $r(n)$ used by the algorithm is $$\begin{equation}
\label{eq:r}
r(n) = (1 + \eta) 
				\cdot 
				2 \left( \frac{1}{d}\right)^{\frac{1}{d}}
				\left( \frac{\mu (\ensuremath{\ensuremath{\mathcal{X}}_{\rm free}})}{\zeta_d}\right)^{\frac{1}{d}}
				\left( \frac{\log n}{n} \right)^{\frac{1}{d}},
\end{equation}$$ where $\eta > 0$ is some small constant, $\mu(\cdot)$ denotes the $d$-dimensional Lebesgue measure and $\zeta_d$ is the volume of the unit ball in the $d$-dimensional Euclidean space.

:::: algorithm
::: algorithmic
$V \leftarrow \ensuremath{\{ x_{\text{init}}\}} \cup \texttt{sample\_free}(n)$; $E \leftarrow \emptyset$; $\ensuremath{\mathcal{T}}\leftarrow (V,E)$ PATH $\leftarrow$ `search` $(\ensuremath{\mathcal{T}}, \ensuremath{\mathcal{X}}_{goal}, {\color{red} 0 , \infty})$ // See Alg. [\[alg:search\]](#alg:search){reference-type="ref" reference="alg:search"} PATH
:::
::::

:::: algorithm
::: algorithmic
$W \leftarrow V \setminus \ensuremath{\{ x_{\text{init}}\}}$; $H \leftarrow \ensuremath{\{ x_{\text{init}}\}}$ $N_v \leftarrow 
  					\texttt{nearest\_neighbors}(V \setminus \ensuremath{\{ v\}}, v, r(n))$

$z \leftarrow x_{\text{init}}$ $H_{\text{new}} \leftarrow \emptyset$; $X_{\text{near}} \leftarrow W \cap N_z$

$Y_{\text{near}} \leftarrow H \cap N_x$ $y_{\text{min}} \leftarrow \arg \min_{y \in Y_{\text{near}}} 
								\ensuremath{\{ \texttt{cost}_{\ensuremath{\mathcal{T}}}(y) + \texttt{dist}(y,x)\}}$

$\ensuremath{\mathcal{T}}.\texttt{parent}(x) \leftarrow y_{\text{min}}$ $H_{\text{new}} \leftarrow H_{\text{new}} \cup \ensuremath{\{ x\}}$; $W \leftarrow W \setminus \ensuremath{\{ x\}}$

$H \leftarrow (H \cup H_{\text{new}}) \setminus \ensuremath{\{ z\}}$ FAILURE

$z \leftarrow \arg \min_{y \in H}
								\ensuremath{\{ \texttt{cost$_{\ensuremath{\mathcal{T}}}$}(y) + 
											{\color{red}		\texttt{cost\_to\_go}(y)} \}}$ FAILURE

PATH
:::
::::

# Anytime FMT\* (aFMT\*) {#sec:aFMT}

An algorithm is said to be *anytime* if it yields meaningful results even after a short time and it improves the quality of the solution as more computation time is available. We outline a straightforward enhancement to FMT\* to make it anytime. As noted in previous work (see, e.g., [@WBC13]) one can turn a batch algorithm into an anytime one by the following general approach: choose an initial small number of samples $n=n_0$ and apply the algorithm. As long as time permits, double $n$ and repeat the process. The total running time is less than twice that of the running time for the largest $n$. Note that as FMT\* is AO, aFMT\* is also AO.

We can further speed up this method by reusing both existing samples and connections from previous iterations.

# Algorithmic framework {#sec:alg}

We are now ready to present our approach to exploiting lower bounds on cost in order to speed up sampling-based motion-planning algorithms.

Given a random infinite sequence of collision-free samples $S = s_1, s_2 \ldots$ denote by $V_i(S)$ the set of the first $2^i$ elements of $S$. Let $\ensuremath{\mathcal{G}}_i(S) = G(V_i(S), r(|V_i(S)|))$ and let $\ensuremath{\mathcal{H}}_i(S) \subseteq \ensuremath{\mathcal{G}}_i(S)$ be the subgraph containing collision-free edges only (here $r(n)$ is the radius defined in Eq. [\[eq:r\]](#eq:r){reference-type="ref" reference="eq:r"}). For brevity, we omit $S$ when referring to $V_i(S), \ensuremath{\mathcal{G}}_i(S)$ and $\ensuremath{\mathcal{H}}_i(S)$. Moreover, when we compare our algorithm to the aFMT\* algorithm, we do so for runs on the same random infinite sequence $S$. Clearly, for any two nodes $x, y \in V_i$, $\texttt{cost}_{\ensuremath{\mathcal{G}}_i}(x, y) 
	\leq  
\texttt{cost}_{\ensuremath{\mathcal{H}}_i}(x, y)$. Thus for any node $x \in V_i$, $\texttt{cost-to-go}_{\ensuremath{\mathcal{G}}_i}(x) \leq \texttt{cost-to-go}_{\ensuremath{\mathcal{H}}_i}(x).$ Namely, the cost-to-go computed using the disk graph $\ensuremath{\mathcal{G}}_i$ is a lower bound on the cost-to-go that may be obtained using $\ensuremath{\mathcal{H}}_i$. We call this the *lower bound property*. For an illustration, see Fig. [1](#fig:cspace){reference-type="ref" reference="fig:cspace"}.

:::: {#fig:cspace .figure latex-placement="t,b"}
::: caption
This figure demonstrates that the part of the tree expanded when searching in cost-to-come space (shaded blue region, Fig. (a)) is larger than the one expanded when searching in cost-to-come+cost-to-go space (shaded green region, Fig. (b)). Obstacles in the C-space are depicted in red, start location and goal region are depicted by a purple circle and a turquoise region, respectively. Edges of the disk graph $\ensuremath{\mathcal{G}}_i$ that are contained and not contained in $\ensuremath{\mathcal{H}}_i$ are depicted in black and dashed red, respectively. The figure is best viewed in color.
:::
::::

:::: algorithm
::: algorithmic
$V \leftarrow \ensuremath{\{ x_{\text{init}}\}}$; $n \leftarrow n_0$; $c_{prev} \leftarrow \infty$ $V \leftarrow V \cup \texttt{sample\_free}(n)$; $E \leftarrow \emptyset$; $\ensuremath{\mathcal{T}}\leftarrow (V,E)$ `estimate_cost_to_go`$(V, x_{init}, \ensuremath{\mathcal{X}}_{goal}, c_{prev})$ PATH $\leftarrow$ `search` $(\ensuremath{\mathcal{T}}, \ensuremath{\mathcal{X}}_{goal}, {\color{red} \texttt{cost\_to\_go} , c_{prev}})$ $n \leftarrow 2n$; $c_{prev} = \texttt{cost}$(PATH) PATH
:::
::::

:::: algorithm
::: algorithmic
$V_{\text{preproc}} \leftarrow \texttt{Dijkstra} 
			(G(V, r(|V|)), x_{init}, \frac{c}{2})$ $V_{\text{preproc}} \leftarrow V_{\text{preproc}} \cup \texttt{Dijkstra} 
			(G(V, r(|V|)), \ensuremath{\mathcal{X}}_{goal}, \frac{c}{2})$ cost_to_go$(x) \leftarrow \infty$ $\texttt{Dijkstra} 
	(G(V_{\text{preproc}}, r(|V_{\text{preproc}}|)), \ensuremath{\mathcal{X}}_{goal}, c)$
:::
::::

We present Motion Planning using Lower Bounds, or MPLB(outlined in Alg. [\[alg:MPLB\]](#alg:MPLB){reference-type="ref" reference="alg:MPLB"}). Similar to aFMT\*, the algorithm runs in iterations and at the $i$'th iteration, uses $V_i$ as its set of samples. Unlike aFMT\*, each iteration consists of a *preprocessing phase* (line 4) of computing a lower bound on the cost-to-go values and a *searching phase* (line 5) where a modified version of FMT\* is used.

Let $c_{i}(\text{ALG})$ denote the cost of the solution obtained by an algorithm ALG using $V_i$ as the set of samples (set $c_{0}(\text{ALG}) \leftarrow \infty$). We now show that only a subset of the nodes sampled in each iteration need to be considered. We then proceed to describe the two phases of MPLB.

## Promising nodes

We use the lower bound property to consider only a *subset* of $V_i$ that will be used in the $i$'th iteration. Intuitively, we only wish to consider nodes that may produce a solution that is better than the solution obtained in previous iterations. This leads us to the definition of promising nodes:

::: definition
**Definition 1**. *A node $x\!\in\!V_i$ is *promising* (at iteration $i$) if $$\texttt{cost-to-come}_{\ensuremath{\mathcal{H}}_i}(x) + \texttt{cost-to-go}_{\ensuremath{\mathcal{H}}_i}(x)\!<\!\ensuremath{c_{i-1}(\text{MPLB})}.$$*
:::

In the preprocessing phase, MPLB will traverse $\ensuremath{\mathcal{G}}_i$ (and not $\ensuremath{\mathcal{H}}_i$) to collect a set of nodes that contains all promising nodes (and possibly other nodes), compute a lower bound on their cost-to-go and use this set in the searching phase.

## Preprocessing phase: Estimating the cost-to-go

Recall that in the preprocessing phase, outlined in Alg. [\[alg:preproc\]](#alg:preproc){reference-type="ref" reference="alg:preproc"}, we wish to compute a lower bound on the cost-to-go for (a subset of) nodes $x \in V_i$. Specifically, the only nodes we wish to consider are *promising nodes*. This is done by collecting the set of nodes $V_{\text{preproc}} =  
B_{\ensuremath{\mathcal{G}}_i} \left( x_{\text{init}}, \frac{\ensuremath{c_{i-1}(\text{MPLB})}}{2} \right)
\cup
B_{\ensuremath{\mathcal{G}}_i} \left( \ensuremath{\mathcal{X}}_{\text{goal}}, \frac{\ensuremath{c_{i-1}(\text{MPLB})}}{2} \right)$. Namely, by performing one traversal from $x_{\text{init}}$ (line 1) and one traversal from $\ensuremath{\mathcal{X}}_{\text{goal}}$ (line 2), all nodes such that $\texttt{cost-to-come}_{\ensuremath{\mathcal{G}}_i} \leq \frac{\ensuremath{c_{i-1}(\text{MPLB})}}{2}$ or $\texttt{cost-to-go}_{\ensuremath{\mathcal{G}}_i} \leq \frac{\ensuremath{c_{i-1}(\text{MPLB})}}{2}$ are found. Clearly, any node *not* in either set is not promising (lines 3-4).

After collecting all nodes in $V_{\text{preproc}}$, MPLB computes the distance of every such node from $\ensuremath{\mathcal{X}}_{goal}$ (line 5). This is done by running a shortest paths algorithm on the graph $\ensuremath{\mathcal{G}}_i$ restricted to the nodes in $V_{\text{preproc}}$. This distance is stored for each node and will be used as a lower bound on the cost-to-go. We note that this preprocessing phase only uses NN calls and does not use any CD calls (as there are no LP calls).

## Searching phase: Using cost-to-go estimations

The lower bounds computed in the preprocessing phase allow for two algorithmic enhancements to the searching phase when compared to aFMT\*: (i) incorporating the cost-to-go estimation in the ordering scheme of the nodes and (ii) discarding nodes that are found to be not promising.

**Node ordering:** Recall that in aFMT\*, $H$ is the set of nodes added to the tree that may be expanded and that these nodes are ordered according to their cost-to-come value (Alg. [\[alg:search\]](#alg:search){reference-type="ref" reference="alg:search"}, line 16). Instead, we suggest using the cost-to-come added to the cost-to-go estimation to order the nodes in $H$. This follows exactly the formulation of A\* [@P84] which performs a Dijkstra-like search on a set of nodes. The nodes that were encountered but not processed yet ($H$ in our setting) are ordered according to a cost function $f() = g() + h()$. Here, $g(x)$ is the (computed) cost-to-come value of $x$ ($\texttt{cost-to-come}_{\ensuremath{\mathcal{H}}_i}(x)$ in our case) and $h$ is a lower bound on the cost-to-go of $x$ to the goal ($\texttt{cost-to-go}_{\ensuremath{\mathcal{G}}_i}(x)$ in our case). aFMT\* essentially uses the trivial heuristic $h = 0$. Instead, we suggest to use a much sharper bound to speed up the search towards the goal.

**Discarding nodes:** In the preprocessing stage MPLB computes a set of nodes that *may* be promising, though for each such node, the cost-to-come value was not computed. In the searching phase, once a node is added to the tree, its cost-to-come value will not change in the current iteration. Thus, every node $x$ added to the tree with $\texttt{cost-to-come}_{\ensuremath{\mathcal{H}}_i}(x) 
	 	+ 
	\texttt{cost-to-go}_{\ensuremath{\mathcal{G}}_i}(x) 	
		\geq
	\ensuremath{c_{i-1}(\text{MPLB})}$ is discarded as it cannot be promising. This implies that MPLB will terminate an iteration when it is evident that the previous iteration's solution cannot be improved (see Alg. [\[alg:search\]](#alg:search){reference-type="ref" reference="alg:search"}, lines 17-18).

In Section [5](#sec:eval){reference-type="ref" reference="sec:eval"} we demonstrate through various simulations that using lower bounds has a significant effect on the running time of the algorithm in practice. Ordering the nodes using a heuristic that tightly estimates the cost-to-go allows MPLB to expand a smaller portion of the nodes $V_i$ while discarding nodes allows to focus the search only on nodes that may potentially improve the existing solution.

# Comparative analysis and Discussion {#sec:analysis}

We compare aFMT\* and MPLB with respect to the size of the tree constructed in the searching phase and with respect to the primitive procedures, namely NN and LP. This is done by quantifying the number of NN and LP calls performed by both algorithms and allows us to discuss the fundamental differences between the two algorithms.

Let $\#_{\texttt{NN}, i}(\text{ALG})$, $\#_{\texttt{LP}, i}(\text{ALG})$ denote the number of NN and LP calls performed by an algorithm ALG in iteration $i$, respectively for a fixed sequence of samples $S$. Recall that when comparing the two algorithms, it is done for the same sequence $S$.

## Search-tree size

Let $V_i(\text{ALG}) \subseteq V_i$ denote the set of nodes in the tree in the $i$'th iteration of an algorithm $\text{ALG}$.

::: lem
**Lemma 1**. *At every iteration, the set of nodes traversed in MPLB's searching phase is not larger than that of aFMT\*.*
:::

::: proof
*Proof.* Every node $x$ in the tree of aFMT\* has cost-to-come not larger than $c_i(\text{aFMT}^*)$. Thus, the size of the search-tree of aFMT\* is: $|V_{i}(\text{aFMT*})| = \\
%							B_{\calH_i} (x_{\text{init}}, \cfmt)
%						=
							|\ensuremath{\{ 	x \in V_i \ | \ 
										\texttt{cost-to-come}_{\ensuremath{\mathcal{H}}_i}(x) \leq \ensuremath{c_i(\text{aFMT}^*)}
									\}}|.$

Similar to aFMT\*, each node $x$ traversed by MPLB in the searching phase has $\texttt{cost-to-come}_{\ensuremath{\mathcal{H}}_i}(x) +  \texttt{cost-to-go}_{\ensuremath{\mathcal{G}}_i}(x) \leq \ensuremath{c_i(\text{aFMT}^*)}$. Additionally, due to node discarding (see Section [3](#sec:alg){reference-type="ref" reference="sec:alg"}), $\texttt{cost-to-come}_{\ensuremath{\mathcal{H}}_i}(x) +  \texttt{cost-to-go}_{\ensuremath{\mathcal{G}}_i}(x) \leq \ensuremath{c_{i-1}(\text{MPLB})}$. Thus, the size of the search-tree of MPLB is: $|V_{i}(\text{MPLB})| = \\ 
	| \{	x \in V_i \ | \ 
									\texttt{cost-to-come}_{\ensuremath{\mathcal{H}}_i}(x) + \texttt{cost-to-go}_{\ensuremath{\mathcal{G}}_i}(x)$\
$\leq  
							\min \{ \ensuremath{c_{i-1}(\text{MPLB})}, \ensuremath{c_i(\text{aFMT}^*)}\}
								\}|.$\
Namely, $|V_{i}(\text{MPLB})| \leq |V_{i}(\text{aFMT*})|$. ◻
:::

## Nearest neighbor calls (NN)

## Local planning calls (LP)

will be called whenever either algorithm (aFMT\* or MPLB) attempts to insert a node to the search-tree (line 10 in Alg. [\[alg:search\]](#alg:search){reference-type="ref" reference="alg:search"}). Thus we can state the following lemma:

::: lem
**Lemma 2**. *If MPLB performs an LP call for the edge $(x, y)$ in the $i$'th iteration then aFMT\* will perform an LP call for the edge $(x, y)$ as well.*
:::

::: proof
*Proof.* The LP procedure will be called for every pair of nodes $x,y$ in the search tree such that: (i) $x,y$ are neighbors in $\ensuremath{\mathcal{G}}_i$ (namely their distance is less than $r(|V_i|)$), (ii) $\texttt{cost-to-come}_{\ensuremath{\mathcal{H}}_i}(x) < \texttt{cost-to-come}_{\ensuremath{\mathcal{H}}_i}(y)$ (namely $x$ is inserted to the tree before $y$), and

If MPLB performs an LP call for the edge $(x, y)$ then conditions (i),(ii) and (iii) hold for the samples $x, y$ in MPLB. To prove the lemma we show that they hold for the samples $x, y$ in aFMT\*. Condition (i) holds trivially as it is a property of the samples. Note that the cost-to-come of any node $z$ computed by both algorithms equals to $\texttt{cost-to-come}_{\ensuremath{\mathcal{H}}_i}(z)$. Using this observation and that $V_{\text{preproc}} \subseteq V_i$ (namely the nodes used by MPLB is a subset those used by aFMT\*), conditions (ii) and (iii) hold as well. ◻
:::

## Discussion

From the above analysis we conclude that MPLB will perform *no more* LP calls than aFMT\*. It *may* perform *more* NN calls than aFMT\*. As we demonstrate empirically in the Evaluation section, the number of NN calls that MPLB performs may actually be smaller than that of aFMT\*. Moreover, as the number of iterations increases, MPLB performs only a tiny fraction of the number of LP calls performed by aFMT\*.

# Evaluation {#sec:eval}

We present simulations evaluating the performance of MPLB as an anytime algorithm on 2, 3 and 6 dimensional C-spaces. All experiments were run on a 2.8GHz Intel Core i7 processor with 8GB of memory. The MPLB and aFMT\* implementations are based on the FMT\* implementation provided by Pavone's research group using the Open Motion Planning Library (OMPL 0.10.2) [@SMK12]. Each result is averaged over one hundred different runs. Scenarios and additional material are available at <http://acg.cs.tau.ac.il/projects/MPLB>.

The AO proof of FMT\* (and thus of aFMT\* and MPLB) relies on the fact that the C-space is Euclidean. Thus, we start by studying the motion of robots translating in the plane and in space (Fig. [\[fig:corr\]](#fig:corr){reference-type="ref" reference="fig:corr"} and [\[fig:grids\]](#fig:grids){reference-type="ref" reference="fig:grids"}). Next, we continue to examine the behavior of the algorithms in SE(3) (Fig. [\[fig:cubicles\]](#fig:cubicles){reference-type="ref" reference="fig:cubicles"}). Here the radius provided for FMT\* (Eq. [\[eq:r\]](#eq:r){reference-type="ref" reference="eq:r"}) is irrelevant due to the differences in the rotational and translational components of the C-space. Hence, for both aFMT\* and MPLB, we chose to connect each node to its $k$ NN, where $k(n)= 9 \log n$: Karaman and Frazzoli [@KF11] proposed a variant of RRG where each node is connected to its $k_{RRG}$ NN for $k_{RRG}(n) \geq 2e \log n$. Although this variant was analyzed for Euclidean spaces only, applying it to non-Euclidean spaces works well in practice (see, e.g. [@SH13]).

:::: {#fig:scenarios .figure latex-placement="t,b"}
::: caption
Scenarios used for the evaluation. (a) Two dimensional setting for a point robot. A low-cost path is easy to find yet in order to find a high-quality path, the robot needs to pass through two narrow passages. (b) Three-dimensional C-space for a translating robot in space. To find the shortest path the robot needs to pass through a three-dimensional grid. (c) Six-dimensional C-space for an L-shaped robot translating and rotating in space. Finding a path is relatively easy yet much time is needed to converge to the optimal path. Start and target configurations for (b) and (c) are depicted by green and red robots, respectively, The Home scenario is provided by the OMPL [@SMK12] distribution.
:::
::::

## Fast convergence to high-quality solutions

:::: {#fig:costs .figure latex-placement="t,b"}
::: caption
Average cost vs. time. Cost values are normalized such that a cost of one represents the cost of an optimal path. Low and high error bars denote the twentieth and eightieth percentile, respectively.
:::
::::

We start by comparing the cost of a solution obtained by aFMT\* and MPLB as a function of time (Fig [3](#fig:costs){reference-type="ref" reference="fig:costs"}). In all scenarios MPLB typically finds a solution of given cost between two to three times faster than aFMT\*. In the Corridors scenario (Fig. [\[fig:corr\]](#fig:corr){reference-type="ref" reference="fig:corr"}) the convergence rate can be sped up by using an approximation factor (see suggestion for future work in Section [6](#sec:future){reference-type="ref" reference="sec:future"}). Interestingly, as we will show, the speed-up achieved by MPLB is done while spending a smaller proportion of the time on LP compared to aFMT\*.

## Nearest Neighbors and Local Planning calls

:::: {#fig:profiler .figure latex-placement="t,b"}
![image](Salzman2014AsymptoticallyOptimal_figs/grids_profiler_results_no_legend.png){height="3 cm"} []{#fig:grid_profiler label="fig:grid_profiler"} ![image](Salzman2014AsymptoticallyOptimal_figs/profiler_legend.png){height="3 cm"} []{#fig:legend label="fig:legend"}

::: caption
Percentage of time spent for each of the main components in each iteration for both algorithms for the Grids Scenario. Each iteration is represented by the number of samples used. The left (right) bars of each iteration represent the result of aFMT\* (MPLB, respectively). Note that the time of each iteration for each algorithm is different.
:::
::::

We profiled aFMT\* and MPLB and collected the total time spent on CD for point sampling, LP for edges, NN calls and cost computations. Results for the Grids scenario are presented in Fig. [4](#fig:profiler){reference-type="ref" reference="fig:profiler"} (similar behavior was observed for the other scenarios as well). Clearly, CD computation time (due to sampling, not LP) is negligible for both algorithms and cost calculation plays a larger (but still small) role for MPLB. CD calls due to LP calls are the main bottleneck for aFMT\* (starting at around 65% and gradually decreasing to 45%). For MPLB they start as a main time consumer but as samples are added their percentage of the overall iteration time becomes quite small (around 2% for the last iteration). NN calls play an almost complementary role to the LP and for the last iteration take 40% of the total running time for the MPLB algorithm while taking less than 20% for aFMT\*.

::: wraptable
r4.9cm

  ------- --------------------------------------- ---------------------------------------
    $n$                  the ratio                               the ratio
           $\frac{\#_{\texttt{NN}}(\text{MPLB})}   $\frac{\#_{\texttt{LP}}(\text{MPLB})}
             		{\#_{\texttt{NN}}(\text{aFMT}^*)}$     		  {\#_{\texttt{LP}}(\text{aFMT}^*)}$
   1.6K                    0.71                                    0.38
   3.2K                    0.53                                    0.31
   6.4K                    0.68                                    0.33
   12.8K                   0.68                                    0.19
   25.6K                   0.69                                    0.20
   51.2K                   0.99                                    0.05
  ------- --------------------------------------- ---------------------------------------
:::

The table to the right reports on the ratio of NN and LP calls performed by MPLB and aFMT\* for the Grids scenario. The number of NN calls performed by MPLB is lower than those performed by aFMT\*. As expected, MPLB performs significantly less LP calls than aFMT\*.

# Conclusion and outlook {#sec:future}

In this work we show that by using effective lower bounds and with no compromise on the cost of paths produced by the algorithm, the weight of CD (via LP calls) may become almost negligible with respect to NN calls. This follows the ideas presented by Bialkowski et al. [@BKOF12] but uses different, more general, methods. Looking into NN computation, one can notice that AO algorithms such as sPRM\* [@KF11], FMT\* and MPLB rely on a specific type of NN computation: given a set $P$ of $n$ points, either compute for each point all its $k$ nearest neighbors, or all neighbors within distance $r$ from the point. In both cases, $P$ is known in advance and $k$ (or $r$) are parameters that do not change throughout the algorithm or throughout a single iteration of the algorithm.

# Acknowledgements

We wish to thank Marco Pavone and his co-workers for their advice and support regarding the FMT\* algorithm.

[^1]: $^*$ Blavatnik School of Computer Science, Tel-Aviv University, Israel

[^2]: This work has been supported in part by the Israel Science Foundation (grant no. 1102/11), by the German-Israeli Foundation (grant no. 1150-82.6/2011), and by the Hermann Minkowski--Minerva Center for Geometry at Tel Aviv University.

[^3]: Although we describe the algorithm for Euclidean spaces, by standard techniques the algorithm can be applied to non-Euclidean spaces such as SE3. However, the AO proof of FMT\*, presented in [@JP13], is shown only for Euclidean spaces.

[^4]: Any other algorithm that computes the shortest path from a single source to all nodes in a graph may be used.

[^5]: The disk graph is sometimes referred to as the the *neighborhood graph*.

[^6]: The nearest-neighbor computation can be delayed and performed only when a node is processed but we present the batched mode of computation to simplify the exposition.
