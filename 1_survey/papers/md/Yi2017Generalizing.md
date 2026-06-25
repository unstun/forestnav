---
citation_key: Yi2017Generalizing
arxiv_id: 1710.06092
arxiv_url: https://arxiv.org/abs/1710.06092
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T17:04:20Z
origin: ai+web
reviewed: false
---

# Introduction {#sec:intro}

Sampling-based motion-planning algorithms [@L06] have proven to be an effective tool at solving motion-planning problems. They search through a continuous state space $\ensuremath{\mathcal{X}}$ by sampling random states and maintaining a discrete graph $G$ called a *roadmap*. Vertices and edges in $G$ correspond to collision-free states and paths, respectively.

Roughly speaking, these algorithms iteratively sample new states. This is required to ensure that, as the number of samples tends to infinity, (i) a solution will be found and that (ii) given some optimization criteria, the quality of the solution will progressively converge to the quality of the optimal solution.

Initially, when a path has yet to be found, the samples are drawn from the entire state space $\ensuremath{\mathcal{X}}$. However, once a path $\gamma$ is produced, algorithms that seek *high-quality paths* can limit their sampling domain to a subset of $\ensuremath{\mathcal{X}}$ only containing states that may be used to produce higher-quality paths than $\gamma$. Following Gammell et al. [@GSB14], we call this subset the *informed subset* and denote it $\ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}$. In this work we address the problem of efficiently producing samples in informed subset for systems with arbitrary complex costs.

For Euclidean spaces optimizing for path length, $\ensuremath{\mathcal{X}}_{\rm {inf}}$ can be analytically expressed as a prolate hyperspheroid and can be sampled directly using a closed-form solution [@GSB14]. Indeed, directly sampling in $\ensuremath{\mathcal{X}}_{\rm {inf}}$ has been shown to dramatically improve computation time when compared to sampling in $\ensuremath{\mathcal{X}}$, especially in high dimensions.

Unfortunately, in more general settings, it is not clear how to directly sample $\ensuremath{\mathcal{X}}_{\rm {inf}}$. One approach to produce samples in $\ensuremath{\mathcal{X}}_{\rm {inf}}$ is via *rejection sampling*---sampling a state $x \in \ensuremath{\mathcal{X}}$ and testing if $x \in \ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}$. However, when the size of the informed space $\ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}$ is much smaller than entire state space $\ensuremath{\mathcal{X}}$, this procedure is highly inefficient, dominating the running time of the algorithm [@KTC16]. Recently, Kunz et al. [@KTC16] showed, under some technical assumptions, how to partially ameliorate this inefficiently by *Hierarchical rejection sampling* (HRS). Here, individual dimensions are sampled recursively and then combined. Rejection sampling is performed for these partial samples until a suitable sample has been produced. Unfortunately, HRS may still produce a large number of rejected samples especially in high-dimensional spaces [@KTC16]. This may cause the planning algorithm to spend most of its time trying to produces samples in $\ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}$ rather than explore it.

:::: {#fig:alg .figure latex-placement="tb"}
![](Yi2017Generalizing_figs/alg.png){width="75%"}

::: caption
Algorithmic approach. Cost function is depicted using isocontours (darker shades reflect lower cost) while the boundary of the informed set is depicted in purple. The root-finding and MCMC algorithms are depicted in red and turquoise, respectively.
:::
::::

In this paper, we suggest an alternative approach to produce samples in the informed set $\ensuremath{\mathcal{X}}_{\rm {inf}}$ for a wide range of settings. **Our main insight is to recast this problem as one of sampling uniformly within the sub-level-set of an implicit non-convex function. This recasting enables us to apply Monte Carlo sampling methods, used very effectively in the Machine Learning and Optimization communities, to solve our problem.** Specifically, our approach, depicted in Fig [1](#fig:alg){reference-type="ref" reference="fig:alg"} consists of two stages: in the first, a random sample $x \in \ensuremath{\mathcal{X}}$ is retracted to the boundary of $\ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}$ by running a root-finding algorithm; in the second stage, this retracted sample is used to seed a Monte Carlo sampling chain which allows us to produce samples that (approximately) cover $\ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}$ uniformly.

While our approach can be used with any Markov Chain Monte Carlo (MCMC) method, it is especially suited to be used with Hit-and-Run [@KSZ11]. Roughly speaking, this is because Hit-and-Run (detailed in Sec [5](#sec:algorithm){reference-type="ref" reference="sec:algorithm"}) produces a series of one-dimensional rejection samples which are extremely fast to compute, even in high-dimensional spaces.

Our approach requires that the system has a solution to the two-point boundary value problem (2pBVP) [@L06] and that a gradient can be defined over the cost function. Indeed, we demonstrate the efficiency of our approach on a wide variety of systems and show that it enables reducing the planning time by several orders of magnitude when compared to algorithms using rejection sampling or HRS.

:::::: {#fig:motivation .figure latex-placement="t!"}
::: minipage
:::: {#fig:motivation:slow .figure}
![image](Yi2017Generalizing_figs/slow1.png){height="2.7cm"} ![image](Yi2017Generalizing_figs/slow2.png){height="2.7cm"} ![image](Yi2017Generalizing_figs/slow3.png){height="2.7cm"} ![image](Yi2017Generalizing_figs/slow4.png){height="2.7cm"}

::: caption
Both start velocity and goal velocity are zero.
:::
::::

:::: {#fig:motivation:fast .figure}
![image](Yi2017Generalizing_figs/fast1.png){height="2.7cm"} ![image](Yi2017Generalizing_figs/fast2.png){height="2.7cm"} ![image](Yi2017Generalizing_figs/fast3.png){height="2.7cm"} ![image](Yi2017Generalizing_figs/fast4.png){height="2.7cm"}

::: caption
Start velocity is zero but goal velocity is non-zero.
:::
::::
:::

::: minipage
![Phase plot of two trajectories of one of the joints.](Yi2017Generalizing_figs/phase_plot.png){#fig:motivation:phase_plot width="\\textwidth"}
:::

::: caption
HERB moves right arm from a start configuration to a goal configuration, which are in close proximity. When the goal velocity is non-zero, HERB needs to move right arm further away to accelerate.
:::
::::::

The rest of the paper is structured as follows: after describing related work in Sec. [2](#sec:related_work){reference-type="ref" reference="sec:related_work"}, we formally define our problem in Sec. [3](#sec:pdef){reference-type="ref" reference="sec:pdef"}. We then provide in Sec. [4](#sec:mtdi){reference-type="ref" reference="sec:mtdi"} an intuitive description of the challenges faced in sampling within the informed set for our planning domains. We continue in Sec. [5](#sec:algorithm){reference-type="ref" reference="sec:algorithm"} with a description of our algorithm and present experimental evaluations in Sec. [6](#sec:eval){reference-type="ref" reference="sec:eval"}. Finally, we conclude with a discussion in Sec. [7](#sec:future){reference-type="ref" reference="sec:future"}.

# Related work {#sec:related_work}

We start in Sec. [2.1](#subsec:planning){reference-type="ref" reference="subsec:planning"} by giving an overview of relevant sampling-based motion-planning algorithms. We then continue in Sec. [2.2](#subsec:sampling){reference-type="ref" reference="subsec:sampling"} to describe different approaches that can be used by these algorithms to sample $\ensuremath{\mathcal{X}}$. We conclude our literature review in Sec. [2.3](#subsec:mcmc){reference-type="ref" reference="subsec:mcmc"} with a brief overview of Markov Chain Monte Carlo methods.

## Sampling-based motion-planning algorithms {#subsec:planning}

Initial sampling-based algorithms such as RRT [@LK01] and PRM [@KSLO96] did not take into account the *quality* of a path, given some optimization criteria, and only guaranteed to asymptotically return *a* solution, if one exists. Karaman and Frazzoli [@KF11], presented variants of PRM and RRT, named PRM\* and RRT\*, respectively that were shown to produce paths who's cost converges asymptotically to the minimal-cost path. This was done by recognizing the underlying connections between stochastic sampling-based motion planning and the theory of random geometric graphs (see also [@SSH16]). Additional algorithms followed, increasing the converges rate by various techniques such as lazy dynamic programming [@GSB15; @SH15], relaxing optimality to near-optimality [@DB14; @SH16] and more.

Many of the algorithms mentioned require solving a two-point boundary value problem (2pBVP) to perform exact and optimal connections between vertices in the roadmap. For holonomic robots, these are simply straight lines in the configuration space, but for kinodynamic sytems with arbitrary cost functions, computing an optimal trajectory between two states is non-trivial in general.

Xie et al. [@XBPA15] use a variant of sequential quadratic programming (SQP) to solve 2pBVP and integrate it with BIT\* [@GSB15]. Webb and van den Berg [@WB13] use a fixed-final-state-free-final-time controller to solve the 2pBVP with respect to a cost function that allows for balancing between the duration of the trajectory and the expended control effort. Perez et al. [@PPKKL12] propose a variant of RRT\* that automatically defines a distance metric and node extension method by locally linearizing the domain dynamics and applying linear quadratic regulation (LQR).

Finally, we note that we are not the first to integrate Monte Carlo sampling into planning algorithms. T-RRT [@JCS10] and its variants [@DSC13] are inspired by Monte Carlo optimization techniques and use notions such as the Metropolis criterion [@CG95] to guide the exploration of the configuration space.

## State-space sampling {#subsec:sampling}

There is a rich body of literature on how to produce samples that increase the efficiency of a planner in terms of finding a solution or producing high-quality solutions. Heuristic approaches include sampling on the medial axis [@WAS99a; @YDLTA14], sampling near the boundary of the obstacles [@YTEA12], resampling along a given trajectory [@AS11] and more [@US03; @SWT09]. For planning under the differential constraints, reachability-guided sampling [@PLAEFRA17] focuses on sampling regions of the state space that are most likely to promote expansion for the given constraints.

Of specific interest to our work are approaches that produce samples in the informed set $\ensuremath{\mathcal{X}}_{\rm {inf}}$. As mentioned in Sec. [1](#sec:intro){reference-type="ref" reference="sec:intro"} Gammel et al. [@GSB14] describe an approach to sample uniformly in $\ensuremath{\mathcal{X}}_{\rm {inf}}$ for the specific case where $\ensuremath{\mathcal{X}}= \mathbb{R}^d$ and when optimizing for path length. To the best of our knowledge, the only method to produce samples in non-Euclidean spaces that can be applied to motion planning problems (other than rejection sampling) is HRS by Kunz et al. [@KTC16].

## Markov Chain Monte Carlo (MCMC) {#subsec:mcmc}

Monte Carlo simulation is a general sampling framework widely used in various domains. Roughly speaking, Monte Carlo simulation repeatedly samples a domain at random to approximate some value or function. One specific domain where Monte Carlo simulation is used which is relevant to this work is generating draws from a desired distribution which is hard to sample directly.

One of the popular classes of Monte Carlo simulation is *Markov Chain Monte Carlo* (MCMC) [@ADDJ03]. Here, the samples are drawn by generating a Markov chain such that the distribution of points on the chain converges to the desired distribution. One variant, which is of special interest to us is Hit-and-Run [@KSZ11]. Here, given the current point $x_i$ the next point $x_{i+1}$ in the Markov chain is produced by sampling a random direction $\theta$ on the surface of the unit sphere centered at $x_{i+1}$. This defines a ray $r_i$ rooted at $x_i$ and passing through $\theta$. The point $x_{i+1}$ is chosen by randomly sampling a point on $r_i$. This algorithm is considered to be one of the most efficient algorithms for generating an asymptotically uniform point if the set under consideration is convex [@LV06] and it can also be extended to sample points that converge to an arbitrary target distribution in total variation [@RS94].

The attractiveness of Hit-and-Run for our problem domain stems from the fact that it performs a series of one-dimensional rejection samples which are extremely fast to compute, even in high-dimensional spaces. Finally, it is worth noting that we are not the first to apply Hit-and-Run for motion-planning problems. Recently [@YPVA17] was used as an alternative to RRT to produce *feasible motions* (and not high-quality paths). Interestingly the paper concludes with the statement "*One drawback is that the sample paths for Hit-and-Run have no pruning and are therefore longer than the RRT paths. Hybrid approaches that yield short paths but also explore quickly are a promising future direction.*" Our paper can be seen as a hybrid approach marrying sampling-based planning with MCMC-based approaches.

# Problem definition {#sec:pdef}

Let $\ensuremath{\mathcal{X}}, \ensuremath{\mathcal{U}}$ denote the state and controls spaces, respectively and set $\ensuremath{\ensuremath{\mathcal{X}}_{\rm free}}\subset \ensuremath{\mathcal{X}}$ to be the set of states where the robot is collision free. A *trajectory* $\gamma$ is a timed path through $\ensuremath{\mathcal{X}}$ obtained by applying at time $t$ control $u(t) \in \ensuremath{\mathcal{U}}$ and satisfying the system dynamics $\dot{x}(t) = f( x(t) , u(t) )$. A trajectory is collision free if $\forall t,~\gamma(t) \in \ensuremath{\ensuremath{\mathcal{X}}_{\rm free}}$

Given a cost function $C : \ensuremath{\mathcal{X}}\times \ensuremath{\mathcal{U}}\rightarrow \mathbb{R}$, the cost of a trajectory $\gamma$ is the accumulated cost along the path $c(\gamma) = \int_0^{T} c( x(t), u(t) ) |\dot{\gamma}(t)|dt$, where $T$ is the duration of $\gamma$.

Given start and target states $x_s, x_g \in \ensuremath{\mathcal{X}}$, we wish to find a collision free trajectory $\gamma^*$ connecting $x_s$ to $x_g$ such that $c(\gamma^*) = \min_{\gamma \in \Gamma} c(\gamma)$, where $\Gamma$ is the set of all collision-free trajectories.

Given a trajectory $\gamma_{\rm best}$ with cost $\ensuremath{c_{\rm best}}= c(\gamma_{\rm best})$ the *informed set* $\ensuremath{\mathcal{X}}_{\rm {inf}}$ is defined to be all states $x$ which may be on trajectories with lower cost than $\ensuremath{c_{\rm best}}$. Specifically, $\ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}= \{ x \in \ensuremath{\mathcal{X}}\mid  
        c ( \gamma^*(x) ) < \ensuremath{c_{\rm best}}\}$ [@GSB14]. Here $\gamma^*(x)$ denotes the optimal trajectory from $x_s$ to $x_g$ constrained to pass through $x$. Notice that we do not require that $\gamma^*(x)$ is collision free.

In this work we consider the problem of efficiently producing samples within $\ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}$. These samples will be used within the informed RRT\* framework to efficiently and incrementally compute trajectories of decreasing cost, converging to the optimal trajectory.

# Motivation---$\ensuremath{\mathcal{X}}_{\rm {inf}}$ in kinodynamic state spaces {#sec:mtdi}

In this section we properly motivate this work. Specifically, we start by describing the differences in between planning in Euclidean configuration spaces (also called geometric planning) nd non-Euclidean state spaces.

## Geometric vs. Kinodynamic planning

Consider the problem depicted in Fig. [5](#fig:motivation){reference-type="ref" reference="fig:motivation"} where HERB is required to produce a large velocity at the end of its arm at the goal position. One approach to address this problem is to first plan in the geometric configuration space and then re-scale the trajectory in time. However, when the start and goal are in close proximity, a geometric planner will simply connect the two states (Fig. [3](#fig:motivation:fast){reference-type="ref" reference="fig:motivation:fast"}). On re-scaling this trajectory in time, reaching the goal velocity in such short distance will require large acceleration, which will not be feasible. Hence, it is required to move the arm back and then reach the goal, i.e. the trajectory returned by the kinodynamic planner shown in (Fig. [3](#fig:motivation:fast){reference-type="ref" reference="fig:motivation:fast"}). The difference between the two motions are shown in a phase plot in Fig. [4](#fig:motivation:phase_plot){reference-type="ref" reference="fig:motivation:phase_plot"}.

## Minimal Time Double Integrator

To understand why we resort to optimization-based methods and do not attempt to provide a closed-form solution to sample $\ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}$ we study the structure of the informed set for a simple yet important dynamical system---the double integrator minimizing time (MTDI). Here, we are given a one-dimensional point robot with bounded acceleration moving amid obstacles. We wish to compute the minimal-time trajectory between two states $x_s, x_g$. A state $x \in \ensuremath{\mathcal{X}}$ in this model is defined by the position $q \in \mathbb{R}$ and the velocity $\dot{q}\in \mathbb{R}$ of the robot. The system dynamics are described by: $$\begin{equation}
\begin{bmatrix}
    \dot{q} \\
    \ddot{q}
\end{bmatrix}
=
\begin{bmatrix}
    0 & 1 \\
    0 & 0
\end{bmatrix}
\begin{bmatrix}
    {q} \\
    \dot{q}
\end{bmatrix}
+
\begin{bmatrix}
    0 \\
    1
\end{bmatrix}
u.
\end{equation}$$ Here, the control $u \in [\underline{u}, \overline{u}]$ is the (bounded) acceleration.

Notice that (i) this is model can be seen as a simplified one-dimensional instance of a robot manipulator with many degrees of freedom and that (ii) closed-form solutions exist to the 2pBVP for this specific case (as well as the multi-dimensional setting) [@HN10; @KS14].

Recall that for Euclidean spaces minimizing path length, the informed set $\ensuremath{\mathcal{X}}_{\rm {inf}}$ is a prolate hyperspheroid [@GSB14]. Moreover, the size and shape of the hyperspheroid is defined only be the cost $\ensuremath{c_{\rm best}}$ of the current best solution and not by the location of the start $x_s$ and goal $x_g$.

For the case of a MTDI, this is not the case. Specifically, we have that (i) the structure of $\ensuremath{\mathcal{X}}_{\rm {inf}}$ changes not only with $\ensuremath{c_{\rm best}}$ but also according to the specific values of $x_s$ and $x_g$ and that (ii) the cost map that implicitly defines $\ensuremath{\mathcal{X}}_{\rm {inf}}$ can contain discontinuities (in contrast to Euclidean spaces minimizing path length where the cost map is continuous and differentiable at every point).

To understand the differences recall that optimal trajectories for MTDI follow a "bang-bang" controller [@HN10; @KS14]. Namely, we first apply maximal (or minimal) acceleration for some duration and then switch to applying minimal (or maximal, respectively) acceleration. It is straightforward to see that both the type and the amount of acceleration applied (and hence the structure of $\ensuremath{\mathcal{X}}_{\rm {inf}}$) depend on the specific values of $x_s$ and $x_g$. Fig [6](#fig:discont){reference-type="ref" reference="fig:discont"} depicts a simple example where the cost map is discontinuous.

To summarize, the structure of $\ensuremath{\mathcal{X}}_{\rm {inf}}$ can change given different start and goal states. Furthermore, its boundary may not be differentiable due to the aforementioned discontinuous.

:::: {#fig:discont .figure latex-placement="tb"}
![](Yi2017Generalizing_figs/cost_discontinuity.png){height="5.25cm"}

::: caption
Visualization of the discontinuity in the cost function of MTDI (right) related to the types of controls applied (left). Given state $x_s$ and fixed position $q_0$, we depict the cost (time) as a function of the velocity $\dot{q}$. The minimal cost is attained at $\dot{q}_{\min}$ by applying maximal acceleration (blue curves $(i), (ii)$). To reach states such as $\dot{q}_1$, where $\dot{q}_1 < \dot{q}_{\min}$ we need to apply maximal acceleration (curve $(i)$) followed by minimal acceleration (green curve $(iii)$), which result in a continuous increase in cost. However, for states such as $\dot{q}_2$, where $\dot{q}_2 > \dot{q}_{\min}$, we need to apply minimal acceleration followed by maximal acceleration (curves $(iv), (v)$), which result in the discontinuity.
:::
::::

# MCMC-based Informed Sampling {#sec:algorithm}

In this section we describe our approach to efficiently produce new samples in an informed set $\ensuremath{\mathcal{X}}_{\rm {inf}}$ given a specific cost $\ensuremath{c_{\rm best}}$ of trajectory $\gamma_{\rm best}(t)$. The samples follow a Markov Chain Monte Carlo, in which a new sample candidate is produced from a previous sample that also lies in the same informed set. Furthermore, the value $\ensuremath{c_{\rm best}}$ can decrease between consecutive iterations in the planning process of an informed RRT\* planner. This will occur if the search algorithm that uses the sampler finds a path to the goal whose cost is lower than $\ensuremath{c_{\rm best}}$.

The idea behind applying MCMC for informed sampling is to define a target distribution $\pi$ that has $p(x_{sample}\in\ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}) \ne 0 ~\&~ p(x_{sample})\notin\ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}= 0$. This is specially useful if we want to bias the samples based on our knowledge of the environment. However, we make no such assumption about the environment and use a uniform distribution over all points in $\ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}$. Our approach consists of two stages,

1.  finding an initial sample $x_0 \in \ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}$ which will serve as the start of a Markov chain. This is implemented using the function $\texttt{sample\_in\_informed\_space}( )$, and

2.  sampling a new sample $x_i \in \ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}$ given a previous sample $x_{i-1}$. This is implemented using the function $\texttt{MCMC\_sample} (x_{i-1}, \ensuremath{c_{\rm best}})$.

Our framework is described in Algorithm [\[alg:mcmc_informed_sampling\]](#alg:mcmc_informed_sampling){reference-type="ref" reference="alg:mcmc_informed_sampling"} and visualized in Fig. [1](#fig:alg){reference-type="ref" reference="fig:alg"}. We now continue to detail each of the algorithm's stages.

## Finding an initial sample in $\ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}$

In theory, MCMC methods converge to the desired distribution regardless of the initial sample used to seed the chain. In our setting, the probability distribution $\pi_{\hat{f}}$ is defined by having all points in $\ensuremath{\mathcal{X}}_{\rm {inf}}$ distributed uniformly while the probability of sampling any configuration $x \in \ensuremath{\mathcal{X}}\setminus \ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}$ is zero. A common practice to avoid starting biases in MCMC-type algorithm is to discard an initial set of samples (a process referred to as "burn-in") [@ADDJ03].

In our setting, we are only interested in points in $\ensuremath{\mathcal{X}}_{\rm {inf}}$, thus we suggest to start the Markov Chain in $\ensuremath{\mathcal{X}}_{\rm {inf}}$ and avoid this burn-in stage. We restart our process and generate a new Markov chain when (i) the cost of $\ensuremath{c_{\rm best}}$ is updated (i.e. a new solution is found by the planner) or (ii) the new sample on the existing Markov chain is outside $\ensuremath{\mathcal{X}}_{\rm {inf}}$.

We suggest several methods to produce an initial sample $x_0 \in \ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}$

- randomly returning either the start state or the goal state,

- randomly sampling a state $x_{\text rand} \in \ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}$ and using a gradient descent algorithm (e.g. Newton-Raphson Method [@RT06]) to find a sample in $\ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}$

- sampling from a pool of previous samples that are in the informed set $\ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}$ and

- applying rejection sampling until a sample in the informed set is found.

Each of the methods proposed has its own pros and cons. For example, a gradient-descent algorithm is usually efficient in finding a solution, but subject to only convex problems. Sampling from a pool of samples is algorithmic-free but biases new samples to be near previous samples.

## Generating a new sample in a Markov chain {#mcmc}

Our approach is general and can be applied to any MCMC algorithm (see Sec. [2](#sec:related_work){reference-type="ref" reference="sec:related_work"}). The process is demonstrated in Algorithm [\[alg:mcmc_informed_sampling\]](#alg:mcmc_informed_sampling){reference-type="ref" reference="alg:mcmc_informed_sampling"}. At the beginning of a Markov chain, `sample_in_informed_space`() is called to generate the first sample in an informed set. `MCMC_sample`() is called to generate a new sample based on a previous sample $x_{i-1}$ and a cost $\ensuremath{c_{\rm best}}$ that defines an informed set. We demonstrate how to instantiate it with two different algorithms *Metropolis-Hastings* and *Hit-and-Run*, which will be described in later subsections. If a generated new sample candidate is in the informed set, this candidate will be returned as a new sample. But if a generated new sample candidate is not in the informed set, it will go back to line 2. A new Markov chain will be initiated by calling `sample_in_informed_space`() to generate a new sample $x_0$.

:::: algorithm
::: algorithmic
[]{#alg:mcmc_informed_sampling:start label="alg:mcmc_informed_sampling:start"} $x_{0} \leftarrow \texttt{sample\_in\_informed\_space}( )$ $x_{i} \leftarrow \texttt{MCMC\_sample} (x_{i-1}, \ensuremath{c_{\rm best}})$ $i \leftarrow 0$; $x_{0} \leftarrow \varnothing$ **Goto** line [\[alg:mcmc_informed_sampling:start\]](#alg:mcmc_informed_sampling:start){reference-type="ref" reference="alg:mcmc_informed_sampling:start"} **return** $x_{i}$
:::
::::

### Metropolis-Hastings sampler

The Metropolis-Hastings algorithm is one of the most popular MCMC samplers [@CG95], because it provides a simple and parameter-free framework that guarantees the convergence of Markov chains to a target distribution. Our work adopts the general Metropolis-Hastings algorithm, as described in Algorithm [\[alg:mh_mcmc\]](#alg:mh_mcmc){reference-type="ref" reference="alg:mh_mcmc"}, We generate a new sample $x_{i}$ around the previous sample $x_{i-1}$ using a Gaussian distribution (line 1). We then check if the point lies in the informed set (lines 2-5) and if it does we return it. If not, we return the previous sample. An acceptance ratio $\alpha$ is used to keep the reversibility even if the target probability $\pi$ is asymmetric, which is needed to guarantee the convergence [@CG95].

:::: algorithm
::: algorithmic
$x'_{i} \leftarrow \texttt{sample\_normal}( q ( x \mid x_{i-1},\Sigma) )$ []{#start label="start"} $\alpha \leftarrow \frac{ q ( x_{i-1} \mid x'_{i},\Sigma) \pi( x'_{i} ) }{ q ( x'_{i} \mid x_{i-1},\Sigma) \pi( x_{i-1} ) }$ $x'_{i}$ $x_{i}$
:::
::::

In implementation, we use Newton-Raphson method as a gradient descent with random restart to find $x_0 \in \ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}$ as the start of a Markov chain.

### Hit-and-Run sampler

Hit-and-Run [@S84] sampler is known to efficiently generate uniform samples. Specifically, we use the Accelerated Hit-and-Run variant [@KSZ11] of the algorithm i.e. described in Algorithm [\[alg:hit_and_run_mcmc\]](#alg:hit_and_run_mcmc){reference-type="ref" reference="alg:hit_and_run_mcmc"}, which also supports the uniform sampling in both convex and non-convex state space [@KSZ11]. Given the previous sample $x_{i-1}$ it first samples a random direction on a unit sphere (line 1). This induces a line $L(\lambda)$ passing through $x_{i-1}$ in the direction sampled (line 2), parametrized by a scalar $\lambda$. We obtain upper and lower bounds on $\lambda$ (line 3) that are problem dependent. For example, if we have box constraints on joint limits of the robot and on maximum velocity, then bounds are given by $\lambda^{+} = -\lambda^{-} = l_{diag}$; where $l_{diag}$ is the length of the longest diagonal of the box. We then sample a point along $L(\lambda)$ by sampling a scalar $\lambda'$ within our bounds (line 5). This defines a point $x_{i}$ which is a candidate for the next sample along the Markov Chain (line 6). We then check if the point lies in the informed set (line 7) and if it does, we return it. If not, we update our bounds (lines 9-12) and repeat the process. The algorithm can be viewed as an efficient method that performs rejection sampling along a one-dimensional line passing through the previous sample parametrized by $\lambda$.

:::: algorithm
::: algorithmic
$d \leftarrow$ `sample_random_direction`$()$ $L(\lambda) = \{  x \mid x = x_{i-1} + \lambda d_i \}$ $\lambda^{+} \leftarrow \sup L(\lambda)$; $\lambda^{-} \leftarrow \inf L(\lambda)$

$\lambda' \leftarrow$ `sample_random`$(\lambda^{-} , \lambda^{+})$ $x_{i} \leftarrow x_{i-1} + \lambda'_{i} d_i$

$x_{i}$

$\lambda^{+} \leftarrow \lambda'$ $\lambda^{-} \leftarrow \lambda'$
:::
::::

For this algorithm, we continue sampling along a Markov Chain until either (i) the difference between the lower and upper bounds ($\lambda^-$ and $\lambda^+)$ that define our sampling domain is below a predefined threshold or (ii) a predefined number of samples was exceeded. We want to point out that a Hit-and-Run sampler only requires that a Markov chain starts in an informed set, and will not produce a sample outside of the informed set. Also, in our implementation, we pick the start or the goal state to find $x_0 \in \ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}$ as the start of a Markov chain.

## Asymptotic optimality

We note that our approach produces samples that cover the informed space. Namely, there is a non-zero probability to sample in any region of $\ensuremath{\ensuremath{\mathcal{X}}_{\rm {inf}}}$. A direct implication of the proof of optimality presented in [@KF11] is that our algorithm is asymptotic optimal:

::: {#prop:asym_opt .prop}
**Proposition 1**. *Informed RRT\* [@GSB14] running with MCMC-based informed sampling is asymptotic optimal.*
:::

# Evaluation {#sec:eval}

We evaluate the performance of proposed MCMC methods by comparing four types of samplers, which are Rejection Sampler (RS), Hierarchical Rejection Sampler (HRS), Metropolis-Hastings Sampler (MH), and Hit-and-Run Sampler (HNR). We use different samplers to generate a fixed number of samples in different informed sets to check the sampling efficiency. We then compare the quality of the samplers by evaluating how the samplers work with informed RRT\* [@GSB14].

## Sampling Efficiency

Fig. [7](#fig:sampling_efficiency:levelset){reference-type="ref" reference="fig:sampling_efficiency:levelset"} shows how the informed set volume ratio decreases as the informed set cost $\ensuremath{c_{\rm best}}$ becomes smaller in problems of different dimensions. In higher dimensions, the informed set volume ratio decreases much more quickly with decrease in the informed set cost $\ensuremath{c_{\rm best}}$, as new cheaper trajectories are found in the planning process.

Fig. [10](#fig:sampling_efficiency){reference-type="ref" reference="fig:sampling_efficiency"} shows the plot of the average time taken to generate one sample in the informed space vs. informed set volume ratio, i.e. the ratio of the volume of informed space to the volume of entire state space, for 5000 samples. The informed set volume ratio is estimated by the acceptance rate of rejection sampler. The informed set volume ratio is approximated by the ratio of the number of accepted to the total number of samples obtained while running rejection sampling. Fig. [10](#fig:sampling_efficiency){reference-type="ref" reference="fig:sampling_efficiency"} shows that MH and HNR have a better sampling efficiency compared to HRS and RS with decrease in informed set volume ratio or increase in dimensions.

:::: {#fig:sampling_efficiency .figure latex-placement="t!"}
![The informed set volume ratio decrease as $\ensuremath{c_{\rm best}}$ decreases in the planning process in different dimensions.](Yi2017Generalizing_figs/levelset.png){#fig:sampling_efficiency:levelset width="\\textwidth"}

![4-dimension sampling space.](Yi2017Generalizing_figs/sample_efficiency_2d.png){#fig:sampling_efficiency:2d width="\\linewidth"}

![12-dimension sampling space.](Yi2017Generalizing_figs/sample_efficiency_6d.png){#fig:sampling_efficiency:6d width="\\linewidth"}

::: caption
Average sampling time vs informed set volume ratio of four samplers (RS, HRS, MH and HNR) in state spaces of different dimensions. The X axis is the ratio of informed set volume to the entire sampling space. The Y axis is the average time per sample.
:::
::::

Metropolis-Hastings shows consistent sampling time when problems get harder. It takes the advantage of sampling a near state that generate samples in an informed set. However this does not reflect the quality of the samples, though all the samples are in the informed set. Recall in Algorithm [\[alg:mh_mcmc\]](#alg:mh_mcmc){reference-type="ref" reference="alg:mh_mcmc"}, a new sample candidate is obtained from a Gaussian distribution $q( x \mid x_{i-1}, \Sigma )$. The best covariance $\Sigma$ that generates faster convergence differs with problem setting. A small covariance tends to generate more samples near previous samples, while a large covariance has better exploration but is more likely to drive a Markov chain outside the informed set. In our next planning experiment setting, we use the same covariance for different problems.

When informed set volume ratio is relatively high, it is easy to generate samples in the informed set. All the samplers have close performances. It actually implies rejection sampler is the best because of its simplicity in implementation and minimum correlation between successive samples. The sampling time of all samplers except MH, increases as problems gets harder. Notice that the sampling efficiency of HNR scales better than HRS and HRS is scales than RS. Moving from a 4 dimension problem in Fig. [8](#fig:sampling_efficiency:2d){reference-type="ref" reference="fig:sampling_efficiency:2d"} to a 12 dimension problem in Fig. [9](#fig:sampling_efficiency:6d){reference-type="ref" reference="fig:sampling_efficiency:6d"}, sampling in an informed set becomes even harder, because the informed set volume ratio becomes smaller. Here, HNR and MH samplers show much better efficiency over the others.

We want to point out that efficiently sampling in an informed set is not sufficient for determining the performance of a sampler. For example, a sampler that constantly returns the same sample in a informed set might show the best sampling efficiency, however it is the worst sampler in a path planning problem. Ideally, we want generated samples to be uniformly distributed in an informed set to get the best exploration.

## Planning Efficiency

The quality of samples determines the efficiency of resulting planning algorithms. If a sampler could provide samples with same quality as others but generate samples in a much efficiency way, we would expect that an informed RRT\* with this sampler would show two properties.

- It shall converge faster in finding the optimal solution. Sampling in an informed set is gradually becoming harder as new better solution reduces $\ensuremath{c_{\rm best}}$ which reduces the informed set volume ratio.

- Its performance should not degrade significantly in high dimensional problems. As shown in Fig. [7](#fig:sampling_efficiency:levelset){reference-type="ref" reference="fig:sampling_efficiency:levelset"}, the informed set volume ratio decrease more significantly in a high-dimension state space. The advantage of a good informed sampler becomes evident.

To evaluate the planning efficiency of the samplers, we run them with the informed RRT\* planner [@GSB14] in position-velocity space with MTDI as steering function, on three different problems described below and shown in Fig. [14](#fig:problems){reference-type="ref" reference="fig:problems"}. For each problem the start and goal states (positions and velocities) are known in the joint space. Joint velocities at start and goal are calculated from desired end-effector velocities using inverse kinematics before starting the planning. Table [\[tab:params\]](#tab:params){reference-type="ref" reference="tab:params"} shows the parameters used in the problems.

::: table*
+-----------------------+---------+--------------------+---------+--------------------+----------+--------------------+---------+----------+---------+----------+---------+
| HERB Joint            | \[      | 2                  | \[      | 4                  | \[       | 6                  | \[      | \]       | \[      | \]       | \[      |
+======================:+========:+:========+=========:+:========+=========:+:=======:+=========:+:========+=========:+:========+=========:+:========+=========:+:========+
| Joint limits ($rad$)  | \[ 0.54 | 5.74 \] | \[ -2.00 | 2.00 \] | \[ -2.80 | 2.80 \] | \[ -0.90 | 3.10 \] | \[ -4.76 | 1.24 \] | \[ -1.60 | 1.60 \] | \[ -3.00 | 3.00 \] |
+-----------------------+---------+---------+----------+---------+----------+---------+----------+---------+----------+---------+----------+---------+----------+---------+
| $| v_{max} |~(rad/s)$ | \[      | 0.75               | \[      | 2.50               | \[       | 2.50               | \[      | \]       | \[      | \]       | \[      |
+-----------------------+---------+--------------------+---------+--------------------+----------+--------------------+---------+----------+---------+----------+---------+

          \[ \]
  ---------- ----------
    \[$-\pi$ $\pi$ \]
          \[ \]

          \[ \]
  ---------- ----------
    \[$-\pi$ $\pi$ \]
          \[ \]

. []{#tab:params label="tab:params"}
:::

### Problem 1: 6 Dimension - 3 DoF Planar Manipulator

The start and the goal states have zero velocities. Fig. [11](#fig:planning_efficiency:3dof:example){reference-type="ref" reference="fig:planning_efficiency:3dof:example"} shows the planned path.

### Problem 2: 12 Dimension - 6 DoF Snake Arm

The objective is to hammer the end-effector into the wall while starting with zero velocity. Fig. [12](#fig:planning_efficiency:6dof:example){reference-type="ref" reference="fig:planning_efficiency:6dof:example"} shows the planned path.

### Problem 3: 14 Dimension - 7 DoF WAM Arm

The objective is to quickly swing away a glass on a table using the right arm. Fig. [13](#fig:planning_efficiency:herb:example){reference-type="ref" reference="fig:planning_efficiency:herb:example"} shows a few steps of a planned path.

:::: {#fig:problems .figure latex-placement="t!"}
:::: {#fig:planning_efficiency:3dof:example .figure}
![image](Yi2017Generalizing_figs/3dof_1.png){height="2.45cm"} ![image](Yi2017Generalizing_figs/3dof_2.png){height="2.45cm"} ![image](Yi2017Generalizing_figs/3dof_3.png){height="2.45cm"} ![image](Yi2017Generalizing_figs/3dof_4.png){height="2.45cm"} ![image](Yi2017Generalizing_figs/3dof_5.png){height="2.45cm"}

::: caption
Problem 1 : 3DOF planar arm move from a start to a goal while starting and ending with zero velocities.
:::
::::

:::: {#fig:planning_efficiency:6dof:example .figure}
![image](Yi2017Generalizing_figs/6dof_1.png){height="3cm"} ![image](Yi2017Generalizing_figs/6dof_2.png){height="3cm"} ![image](Yi2017Generalizing_figs/6dof_3.png){height="3cm"} ![image](Yi2017Generalizing_figs/6dof_4.png){height="3cm"} ![image](Yi2017Generalizing_figs/6dof_5.png){height="3cm"}

::: caption
Problem 2 : 6DOF snake hammers the end-effector into the wall while starting with zero velocity.
:::
::::

:::: {#fig:planning_efficiency:herb:example .figure}
![image](Yi2017Generalizing_figs/herb_batting_1.png){height="2.7cm"} ![image](Yi2017Generalizing_figs/herb_batting_2.png){height="2.7cm"} ![image](Yi2017Generalizing_figs/herb_batting_3.png){height="2.7cm"} ![image](Yi2017Generalizing_figs/herb_batting_4.png){height="2.7cm"} ![image](Yi2017Generalizing_figs/herb_batting_5.png){height="2.7cm"}

::: caption
Problem 3 : HERB sweeps a cup on a table, in which the right arm starts with zero velocity and ends with non-zero velocity.
:::
::::

::: caption
Three problems are used to evaluate planning efficiency. These problems are defined in state spaces of different dimensions and subject to different kinodynamics.
:::
::::

:::: {#fig:planning_efficiency .figure latex-placement="t!"}
![Problem 1 - 6 Dimensions.](Yi2017Generalizing_figs/3dof_general.png){#fig:planning_efficiency:3dof:general width="\\linewidth"}

![Problem 2 - 12 Dimensions.](Yi2017Generalizing_figs/6dof_hammering.png){#fig:planning_efficiency:6dof:hammering width="\\linewidth"}

![Problem 3 - 14 Dimensions.](Yi2017Generalizing_figs/herb_batting_efficiency.png){#fig:planning_efficiency:herb:batting width="\\linewidth"}

::: caption
Planning Efficiency of four different samplers (RS, HRS, MH and HNR) in three problems. The X axis is the planning time. The Y axis is the ratio of the current best and the optimal $\ensuremath{c_{\rm best}}/ c^*_{\rm best}$.
:::
::::

As shown in in Fig. [18](#fig:planning_efficiency){reference-type="ref" reference="fig:planning_efficiency"}, MH has the worst performance in all three problems, especially when the dimension increases. Though theoretically samples converge to a target distribution only in the limit of infinite time. However, in practice the samples are to close to each other and don't explore the entire informed space. If the variance of transition distribution is too high, it will tend to move out of the informed set too frequently, and takes longer to converge as the rejection rate is too high.

HNR shows close performance with RS and HRS in a 6-dimension problem, as in Fig. [15](#fig:planning_efficiency:3dof:general){reference-type="ref" reference="fig:planning_efficiency:3dof:general"}. As shown in Fig. [16](#fig:planning_efficiency:6dof:hammering){reference-type="ref" reference="fig:planning_efficiency:6dof:hammering"} and [17](#fig:planning_efficiency:herb:batting){reference-type="ref" reference="fig:planning_efficiency:herb:batting"}, the advantages of HNR are clearly evident in higher dimensional problems. The cost of best solutions generated by planner with HNR sampler converges significantly faster to a cheaper to trajectory compared to others.

# Conclusion {#sec:future}

In this work we demonstrated the effectiveness of using MCMC algorithms to efficiently produce samples for asymptotically-optimal motion planning algorithms. Clearly, there are multiple other MCMC algorithms that can be used and it is interesting to see if alternative algorithms may produce better results. One drawback of these approaches is that they usually incur parameters that have to be tuned. Indeed, in this work we did not spend effort in tuning the parameters and did not change them across the range of scenarios we tested. There is a wealth of literature in the optimization community regarding this topic and integrating such tools is left for future work. Finally, we are interested in using this framework with alternative sampling-based algorithms such as BIT\* [@GSB15] or LBT-RRT [@SH16] and with alternative state spaces.

# Acknowledge

This work was (partially) funded by the National Science Foundation IIS ($\#1409003$), and the Office of Naval Research.

[^1]: $^{*}$Daqing Yi and Rohan Thakker contributed equally to this paper.

[^2]: $^{1}$Daqing Yi and Siddhartha Srinivasa are with Paul G. Allen School of Computer Science & Engineering, University of Washington. `{dqyi, siddh}@cs.washington.edu`

[^3]: $^{2}$ Rohan Thakker, Cole Gulino and Oren Salzman are with Robotics Institute, Carnegie Mellon University. `{rthakker, cgulino, osalzman} @andrew.cmu.edu`
