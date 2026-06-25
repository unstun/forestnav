---
citation_key: Zhang2023BiAMRRT
arxiv_id: 2301.11816
arxiv_url: https://arxiv.org/abs/2301.11816
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T15:51:28Z
origin: ai+web
reviewed: false
---

Shell *et al.*: Bi-AM-RRT\*: A Fast and Efficient Sampling-Based Motion Planning Algorithm in Dynamic Environments

::: IEEEkeywords
Mobile robot, motion planning, bidirectional search, rewiring
:::

# Introduction

Recent advances in robotics have prompted an increasing number of autonomous mobile robots to be used in various fields, such as transportation [@chen2023milestones], manufacturing [@zhao2022multimobile], rescue [@zhu2021novel], domestic service [@zhang2023semantic], and so on. As a fundamental task of mobile robots, motion planning aims to plan a feasible collision-free path from the starting point to the goal point for the robot in the working environment with static or dynamic obstacles [@zhang2022receding]. In such context, lots of research efforts have been conducted on the motion planning problem. For instance, based on the grid map, the Dijkstra [@dijkstra1959note] algorithm can derive a feasible trajectory by traversing the entire map. In order to save computing resources, A\* [@hart1968formal] and anytime repairing A\* (ARA\*)[@likhachev2003ara] use a heuristic search strategy to quickly obtain optimal solution. However, these methods are not suitable for high-dimensional environments or differential constraints. Moreover, to address dynamic obstacles, the D\* [@stentz1995focussed] and the anytime D\* [@likhachev2005anytime] are investigated to search for feasible solutions in dynamic environments. The methods above are grid-based algorithms that require discretization of the state space, which leads to an exponential growth in time spent and memory requirements with the increase of the state space dimension [@wang2022gmr]. To reduce the time cost and memory usage, diffusion map is employed [@coifman2006diffusion]. It is a non-linear dimensionality reduction technique, and seeks for a feasible solution by transforming each state on the map into a diffusion coordinate [@chen2016motion]. Nevertheless, this treatment tends to ignore some details in the environment, leading to poor planning performance or even getting into trap in complex dynamic environments.

For fast and high-quality motion planning in complex dynamic environments, sampling-based methods have attracted significant attention. Typically, the rapidly exploring random tree (RRT) algorithm [@lavalle1998rapidly] has been widely used and achieved great success due to its efficiency and low memory usage. To this end, many of its variants have been presented. For example, RRT-connect [@kuffner2000rrt] shortens the search time by exploiting goal bias and using two trees to search simultaneously. RRT\* [@karaman2011anytime] adds a rewiring process to shorten the path length. Extended-RRT [@li2012extended] re-searches for new collision-free path from the root when there are obstacles in the planned trajectory. But this practice is time-spending. Besides, the RT-RRT\*[@naderi2015rt] retains information about the whole tree from the robot's current position, and uses existing branches around obstacles to locally plan feasible paths. However, the growth of the whole tree takes more time. In such case, an extended RRT-based planning method with the assisting metric (AM) [@armstrong2021rrt] is investigated to guide the growth of the tree to shorten the path search time. Although the utilization of AM can accelerate the RRT exploration process, the search time and path length needs to be improved in dynamic environments.

In this paper, we propose a novel motion planning method based on bidirectional RRT and AM, namely Bi-AM-RRT\*, to reduce the search time and path length in dynamic environments. The presented Bi-AM-RRT\* exploits the trunk information of the reverse tree with the forward tree to efficiently generate a feasible path to the goal position. Based on this, the AM is used to improve the performance of motion planning in environments with obstacles. The AM can be any metric, such as Euclidean metric, diffusion metric, or geodesic metric. Besides, in order to optimize the search path, a new rewiring strategy based on the root and goal is presented to shorten the path length. The main contributions of this work include:

- an AM-based bidirectional search sampling framework for robot motion planning in dynamic environments;

- a novelly fast and efficient motion planning algorithm, namely Bi-AM-RRT\*, to improve the motion planning performance;

- a new rewiring strategy to accelerate the path optimization process to reduce the path length;

- evaluation and discussion on comparative experiments in different environments, which demonstrate the validity and efficiency of Bi-AM-RRT\*.

The remainder of this paper is structured as follows. Section [2](#section2){reference-type="ref" reference="section2"} presents the related work. In Section [3](#section3){reference-type="ref" reference="section3"}, the problem definition and AM-RRT\* are introduced. Section [4](#section4){reference-type="ref" reference="section4"} elaborates the proposed Bi-AM-RRT\*. Section [5](#section5){reference-type="ref" reference="section5"} and Section [6](#section6){reference-type="ref" reference="section6"} describe the extensive experiments and discuss the results, respectively. Section [7](#section7){reference-type="ref" reference="section7"} concludes this paper.

# Related work {#section2}

Robot motion planning aims at planning a feasible path for robots, and has received significant attention over the years, especially in dynamic environments. Many algorithms have been proposed to address the motion planning problem.

To plan a feasible path, the artificial potential field algorithm was introduced for robot motion planning [@khatib1985real], which uses the direction of the fastest potential field decline as the moving direction of the robot. However, when in an environment with obstacles, such solution is prone to fall into local optimisation. In recent years, the learning-based motion planning strategies have been investigated. Everett *et al*. [@everett2018motion] proposed an obstacle avoidance method that trains in simulation with deep reinforcement learning (RL) without requiring any knowledge of other agents' dynamics. Similarly, Wang *et al*. [@wang2020mobile] designed an RL-based local planner, which adopts the global path as the guide path to adapt to the dynamic environment. To optimize the planner, Pérez-Higueras *et al*. [@perez2018teaching] combined inverse reinforcement learning with RRT\* to learn the cost function. The introduction of a machine learning improves the agent's path planning and obstacle avoidance performance in dynamic environments. Notably, these learning-based methods need to train the model in advance, which is time-spending. Moreover, in order to find the optimal trajectory, grid-based motion planning research efforts have been conducted extensively. For example, based on the grid map, A\*[@hart1968formal] was used to search for feasible solutions and gained great success. Koenig *et al*. presented D\*-lite for robot planning in unknown terrain based on the lifelong planning A\*. The performance is closely related to the degree of discretization of the state space. Although these grid-based approaches can always search for the optimal path (if one exists), they do not perform well as the scale of the problem increases, such as time-consuming and high memory consumption.

To improve planning performance, sampling-based methods are considered as a promising solution. In particular, RRT-based algorithms are widely popular due to their ability to efficiently search state spaces and have proven to be an effective way to plan a feasible path for robots [@wang2021survey]. For instance, Kuwata *et al*. [@kuwata2008motion] proposed CL-RRT for motion planning in complex environments. This method uses the input space of a closed-loop controller to select samples and combines effective techniques to reduce the computational complexity of constructing a state space. Based on the probabilist collision risk function, Fulgenzi *et al*. [@fulgenzi2010risk] introduced a Risk-RRT method. In this solution, a Gaussian prediction algorithm is used to actively predict the moving obstacles and the sampled trajectories to avoid collisions. To achieve dynamic obstacle avoidance, Naderi *et al*. [@naderi2015rt] designed a RT-RRT\* algorithm that interweaves path planning with tree growth and avoids waiting for the tree to be fully constructed by moving the tree root with the agent. Analogously, Armstrong *et al*. [@armstrong2021rrt] put forward an AM-RRT\* by using AM to accelerate the path planning process of RT-RRT\*. However, the planning performance is not satisfactory, especially in terms of search time. In order to reduce the search time, bidirectional search strategies are widely employed. As an early proposed bidirectional tree algorithm, RRT-connect [@kuffner2000rrt] uses a greedy heuristic to guide the growth of two trees, thereby shortening the search time. Subsequently, other variants such as Informed RRT\*-connect [@mashayekhi2020informed], B2U-RRT [@wang2021efficient], Bi-Risk-RRT [@ma2022bi], etc. were proposed. They all incorporate bidirectional search strategy and demonstrate the effectiveness of it. Inspired by AM-RRT\* and RRT-connect, a novel AM-based bidirectional search sampling framework for motion planning, i.e., Bi-AM-RRT\*, is proposed in this paper to further reduces the search time and the path length.

Additionally, it is necessary to obtain an optimal path while maintaining the speed of the planner to guarantee the quality of planning. To address the problem of path optimization, Karaman *et al*. [@karaman2010incremental] proposed RRT\* by using newly generated nodes to rewire adjacent vertices to ensure asymptotic optimality. But the convergence speed is slow. In order to accelerate the convergence speed, Yi *et al*. [@yi2018generalizing] suggested a sampling-based planning method with Markov Chain Monte Carlo for asymptotically-optimal motion planning. Chen *et al*. [@chen2018fast] designed DT-RRT to abandon the rewire process and add re-search parent based on the shortcut principle. Although this approach can speed up the convergence process, it tends to produce suboptimal paths. Analogously, Wang *et al*. [@xinyu2019bidirectional] presented a P-RRT\*-connect algorithm to accelerate the convergence of RRT\* using an artificial potential field method. Besides, based on the path optimization and intelligent sampling techniques, Islam *et al*. [@islam2012rrt] proposed RRT\*-Smart, which aims to obtain an optimum or near optimum solution. Gammell *et al*. [@gammell2014informed] investigated the optimal sampling-based path planning with a focused sampling method and presented Informed RRT\* to improve the covergence of RRT\*. However, these methods face challenges for the efficiency of motion planning in dynamic environments.

In this paper, based on bidirectional search sampling strategy, a novel motion planning method, namely Bi-AM-RRT\*, is proposed with a new rewiring scheme to reduce the path length and the search time for agent to find the goal in dynamic environments.

# Preliminaries {#section3}

In this section, the problem definition of motion planning and the programs on which the algorithm depends are introduced first, and then the sampling-based planning algorithm with AM, referred to as AM-RRT\*, is described.

## Motion Planning Problem Definition

Let us define the state space as *X $\in\mathbb{R}^{d}$*. *X$_{obs}\in$ X* denotes obstacles in the state space, while *X$_{free} = X/X_{obs}$* is the free space without obstacles. *x$_{agent} \in X_{free}$* is defined as the state of the mobile robot in the space, and the goal state is represented as *x$_{goal} \in X_{free}$*. In this paper, a search tree *T $\in X_{free}$* is used to generate a feasible collision-free path (i.e., points on the path *x$_{i} \in$ T*) from the start point *x$_{root}$* to the goal point *x$_{goal}$*. During exploration, the Bi-AM-RRT\* can grow both forward tree and reverse tree, which are denoted *T$_{f}$* and *T$_{r}$*, respectively. In addition, there are user-defined the maximum edge length *e$_{max}$* and the maximum number of nodes *n$_{max}$* in the circular domain with radius *e$_{max}$* to control the growth state of *T*. Let *t$_{exp}$* be the tree growth time. Meanwhile, the root rewiring time and goal rewiring time are denoted as *t$_{root}$* and *t$_{goal}$*, respectively. When the Euclidean distance is less than $\sigma$ and there is no obstacle between forward tree and reverse tree, two trees can be joined as one tree, where $\sigma$ represents the connecting distance of two trees.

In the presented method, AM *d$_{A}$* can be the Euclidean metric, the diffusion metric [@chen2016motion], and the geodesic metric [@owen2010fast], which are indicated as *d$_{E}$* , *d$_{D}$* , and *d$_{G}$*, respectively. These metrics are used to calculate the distance information of two states in the state space. Specifically, the Euclidean distance is expressed as $$\begin{equation}
\label{1}
    d_E(x_a, x_b) = \|x_a, x_b\|.
\end{equation}$$ The Euclidean distance between the two points is obtained based on the L2 norm of *x$_{a}$* and *x$_{b}$*. The diffusion distance is yielded by calculating the Euclidean distance of the approximate diffusion coordinates corresponding to each of the two states, and is described as $$\begin{equation}
\label{2}
    d_D(x_a, x_b) = \|h(g(x_a)), h(g(x_b))\|
\end{equation}$$ where *g($\cdot$)* refers to mapping a state $\cdot$ in the grid to the nearest point, and *h($\cdot$)* is mapping a state $\cdot$ to the diffuse coordinates. *d$_{D}$* can provide a good approximation when an obstacle is present. The geodesic distance is the use of the Dijkstra[@dijkstra1959note] method to generate a distance matrix from the connection matrix of discretization state space. It has the advantage of high precision, but is time-spending.

Next, the procedures on which the algorithm depends are described [@armstrong2021rrt]. *Cost(T, x)* refers to the length of the path from the root to *x* in *T* based on Euclidean distance. *Path(T, x)* refers to returning the sequence of path nodes from the root to *x* in *T*. *FreePath(x$_{a}$, x$_{b}$)* returns true when there are no obstacles between x$_{a}$ and x$_{b}$. *Nearest(T, x)* returns the nearest neighbor to *x* if there is no obstacle between *x* and its nearest neighbor. *RewireEllipse(T, x$_{goal}$)* is to return the state set within the rewire ellipse [@gammell2014informed]. *Enqueue(Q, x)* is the addition of *x* to the end of *Q*. *Dequeue(Q)* refers to removing and returning the first item in *Q*. *Push(S, x)* is to add *x* to the front of *S*. *Nearby(T,x)* returns the set of all nodes within E-distance e$_{max}$ of *x*. *Pop(S)* refers to deleting and returning the first item in *S*. *Second(S)* means that the second item in *S* is returned but not removed. *UpdateEdge(T, x$_{new}$, x$_{child}$)* replaces the edge *(x$_{parent}$, x$_{child}$)* with *(x$_{new}$, x$_{child}$)* in *T*, where *x$_{parent}$* is the parent of *x$_{child}$* in *T*. *Len(X)* returns the queue length of *X*.

## AM-RRT\*

AM-RRT\* is an informed sampling-based planning algorithm with AM [@armstrong2021rrt]. Typically, AM-RRT\* uses the diffusion distance as an AM, which is derived from the diffusion map [@coifman2006diffusion] and is also a kind of grid map. It utilizes a dimensional collapse method to reduce time and memory consumption. Although the diffusion distance alone performs poorly in complex environments, but it can achieve good performance as an AM of RRT\*, and can quickly find collision-free paths when obstacles appear. Fig. [1](#fig1){reference-type="ref" reference="fig1"} shows the obstacle avoidance performance with AM-RRT\*. When the obstacle appears on the path, AM-RRT\* does not regenerate the tree, but uses the information in the whole tree for obstacle avoidance action, especially the node information around the obstacle. As can be viewed in Fig. [1](#fig1){reference-type="ref" reference="fig1"}, when obstacles appear, with the help of diffusion metric, a feasible path can be quickly drawn based on node rewiring by using the branch information of the tree below the original path. During agent movement, the tree is maintained in real time. At the same time, the planned path is also rewired for optimization, and the path lengths are made approximately optimal by successive iterations. The whole process of tree growth is similar to RRT\* and its variants. In this process, the diffusion map only plays a leading role in guiding the tree to find the goal point quickly and cover the full space faster while maintaining its probabilistic completeness in a complex environment [@armstrong2021rrt].

:::: {#fig1 .figure}
::: caption
The obstacle avoidance process of AM-RRT\*. (a) The branch information (green circular area) is used for motion planning, and (b) obstacle avoidance when encountering a dynamic obstacle, where red represents the agent, blue represents the goal point, and black represents the obstacle.
:::
::::

# Proposed Bi-AM-RRT\* {#section4}

This paper proposes the Bi-AM-RRT\* for real-time optimal motion planning of mobile robots in dynamic environments. Generally, our proposed Bi-AM-RRT\* uses bidirectional trees (i.e., forward and reverse trees) for searching and accelerates the path optimization by a new rewiring process. In this section, the details of the of our Bi-AM-RRT\*, especially the proposed bidirectional search strategy and the new path rewiring strategy, are presented.

## Bidirectional Search Strategy for Bi-AM-RRT\*

For RRT-based motion planning, the use of a bidirectional search strategy is faster to plan feasible paths than unidirectional. Fig. [2](#fig2){reference-type="ref" reference="fig2"} illustrates the bidirectional tree growth rewiring process. First, the two trees grow simultaneously. When the forward tree and the reverse tree are meet, the forward tree uses the reverse tree to generate the path to the goal while the reverse tree stops growing and initializes. Finally, the forward tree continues to grow to the full map. In this process, the branch information of the forward tree is used for obstacle avoidance and path optimization (refer to Fig. [1](#fig1){reference-type="ref" reference="fig1"}).

:::: {#fig2 .figure}
::: caption
Bidirectional tree growth rewiring process. (a) The forward tree (in blue) and the reverse tree (in green) grow at the same time. (b) When the two trees are close enough to connect into one tree, the reverse tree stops growing and initializes.
:::
::::

Algorithm 1 describes the detail of Bi-AM-RRT\*. First, the forward tree and reverse tree information are initialized, and the map information is loaded (Lines 1$\sim$`<!-- -->`{=html}2). Then, the goal points are set and the *X$_{free}$* and *X$_{obs}$* information is continuously updated. The root state of the forward tree follows the position state of the agent, and the goal state is provided by someone. The root state of the reverse tree is set to the goal state, while the goal state is set to the initial state of the agent position and does not change as the agent position moves (Lines 3$\sim$`<!-- -->`{=html}6). When two trees are not connected (i.e., *x$_{goal\underline{~}f}$ $\in$ T$_{r}$, x$_{goal\underline{~}f}$ $\notin$ T$_{f}$*), they grow simultaneously. When two trees are connected successfully, only the forward tree continues to expand to the full map, generating more nodes to optimize the path to avoid obstacles or make the path shorter (Lines 8$\sim$`<!-- -->`{=html}11). The function *Meet*(*T$_{f}$*,*T$_{r}$*) denotes that true is returned when the Euclidean distance between *T$_{f}$* and *T$_{r}$* is less than the connection distance $\sigma$ and there is no obstacle blocking it. If true is returned, the information of the reverse tree is fused to the forward tree by the function *Swap*(*T$_{f}$*,*T$_{r}$*). Subsequently, the reverse tree stops expanding and initializes (Lines 12$\sim$`<!-- -->`{=html}14). And a collision-free path to the goal is generated, and finally, the agent moves along that path (Lines 15$\sim$`<!-- -->`{=html}16). When the agent reaches the goal, it waits for information about the next goal. The above steps are repeated once a new goal is given.

::: algorithm
*Path*$\leftarrow\phi$; *T$_f$*$\leftarrow\phi$; *T$_r$*$\leftarrow\phi$;\
**load()*$\leftarrow$*Map**;\

*load()$\leftarrow$X$_{free}$, X$_{obs}$*;\
*x$_{agent}$*$\leftarrow$*Agent*,*x$_{root\underline{~}f}$*$\leftarrow$*Agent*,*x$_{goal\underline{~}f}$*$\leftarrow$*Goal*;\
*x$_{root\underline{~}r}$*$\leftarrow$*Goal*, *x$_{goal\underline{~}r}$*$\leftarrow$*x$_{root\underline{~}f}$*(time=0);\
*start*$\leftarrow$*clock()*;\

*T$_{f}$*$\leftarrow$*Expend[ ]{.underline}f(T$_{f}$, Q[ ]{.underline}f$_{root}$, Q[ ]{.underline}f$_{goal}$, S[ ]{.underline}f$_{goal}$, x$_{goal\underline{~}f}$)*;\
*T$_{r}$*$\leftarrow$*Expend[ ]{.underline}r(T$_{r}$, Q[ ]{.underline}r$_{root}$, x$_{root\underline{~}r}$)*;\

*Swap(T$_{f}$,T$_{r}$)*;\
*T$_{r}$*$\leftarrow$*init()*;\
*Path=Path[ ]{.underline}f(T$_{f}$, Nearest(T$_{f}$, x$_{goal\underline{~}f}$))*;\
Move Agent towards *x$_{goal\underline{~}f}$*;
:::

The tree is grown in a way that maintains the probabilistic completeness of random sampling while using AM for guidance, which make the tree growth more aggressive and efficient. The growth of the forward tree is presented in Algorithm 2. When the goal point is given (Line 1), the forward tree actively grows toward the goal point under the guidance of the AM. The entire space is then covered by continuous sampling process using the function *SampleState*(T$_{f}$, x$_{goal\underline{~}f}$) (Line 2). *SampleState*(T$_{f}$, x$_{goal\underline{~}f}$) returns the sampling set *X$_{s}$*, which is defined as $$\begin{equation}
\label{3}
    \begin{split}
        X_{s}=\left\{
        \begin{array}{ll}
            \{x_{goal}\}                    &p>0.7{~}\rm{and}{~}\it x_{goal} \notin T\\
            X_{random} \in X_{free}     &p<0.5{~}\rm or{~}\it x_{goal} \notin T\\
            RewireEllipse(T, x_{goal}) &\rm otherwise \\
        \end{array}
        \right.
    \end{split}
    \nonumber
\end{equation}$$ where *p* $\in$ \[0,1). Afterwards, the root rewiring (see Algorithm 3) is performed to optimize the path (Line 3). In fact, the root rewiring process is always performed. When the goal is found, the rewiring of the goal point (see Algorithm 5) is then implemented to further optimize the path (Lines 4-5). In particular, the growth of the reverse tree is basically the same as that of the forward tree. Since the reverse tree does not need to reach its own goal, there is no goal rewiring step.

::: algorithm
*x$_{goal\underline{~}f}$*$\leftarrow$*Goal*;\
*T$_{f}$*$\leftarrow$*SampleState(T$_{f}$, x$_{goal\underline{~}f}$)*;\
*T$_{f}$*$\leftarrow$*RewireRoot(T$_{f}$, Q[ ]{.underline}f$_{root}$)*;\
*T$_{f}$*$\leftarrow$*RewireGoal(T$_{f}$, Q[ ]{.underline}f$_{root}$, S[ ]{.underline}f$_{goal}$, x$_{goal\underline{~}f}$)*;
:::

## Path Optimization With Rewiring Strategy

To optimize the path, a new rewiring method based on RRT\* is proposed, which re-searches the grandfather node instead of the parent node to speed up the convergence rate. Algorithm 3 provides the root rewiring process of the forward tree. *Q[ ]{.underline}f$_{root}$* is a reference queue used to find less costly points to update *T$_{f}$*. And the new *x$_{root\underline{~}f}$* is the first data of *Q[ ]{.underline}f$_{root}$*. When the root queue is empty, the information of the offset root is added and the root queue is reset (Lines 1$\sim$`<!-- -->`{=html}2). Then, *t$_{root}$* is used to limit the time of root rewiring (Lines 3$\sim$`<!-- -->`{=html}4). When the number of data in *Q[ ]{.underline}f$_{root}$* is greater than 0 and less than or equal to 2, the root rewiring of AM-RRT\* [@armstrong2021rrt] is used (Lines 5$\sim$`<!-- -->`{=html}6). When the number of data in *Q[ ]{.underline}f$_{root}$* is greater than 2, the proposed new rewiring method is executed for optimization (Lines 7$\sim$`<!-- -->`{=html}8). In such optimization process, the path length is reduced by re-searching for a point near the grandfather node that is less costly and has no obstacle between it and the child node as the new parent node, as shown Fig. [3](#fig3){reference-type="ref" reference="fig3"}, which is given in Algorithm 4. The combination of these two rewiring methods accelerates the convergence speed of path optimization and avoids the generation of suboptimal paths at the corners. Thus, the path length is shortened. The root rewiring process in the reverse tree expansion process is the same as that in the forward tree.

::: algorithm
*Enqueue(Q[ ]{.underline}f$_{root}$, x$_{root\underline{~}f}$)*;\
*start*$\leftarrow$*clock()*;\
*RewireRootFirst(T$_{f}$, Q[ ]{.underline}f$_{root}$)*; *RewireRootSecond(T$_{f}$, Q[ ]{.underline}f$_{root}$)*;
:::

![The path optimization process. The tree path is further optimized to A-B on the right when there is a less costly proximity point b around point C. Although the C-D path is better when there is a less costly proximity point a around point E, the path is not optimized due to the obstacle (black square) blocking it.](Zhang2023BiAMRRT_figs/33.png){#fig3 width="2.7in"}

Algorithm 4 summarizes the optimization process when *len(Q[ ]{.underline}f$_{root}$)\>2*. In this case, rewiring uses not just the information of *x$_{r1}$* but both *x$_{r1}$* and *x$_{r2}$* to speeds up the path optimization process and reduces the path length. *x$_{r1}$* and *x$_{r2}$* are dequeued in sequence and try to find the point in *x$_{r1}$* nearest neighbor that can reduce the path cost. If it exists, the *T$_{f}$* is updated (Lines 1$\sim$`<!-- -->`{=html}8). If *x$_{near}$* is not in reference queue *Q[ ]{.underline}f$_{root}$*, it is added to the *Q[ ]{.underline}f$_{root}$* (Lines 9$\sim$`<!-- -->`{=html}10).

::: algorithm
*x$_{r1}$*$\leftarrow$*Dequeue(Q[ ]{.underline}f$_{root}$)*;\
*x$_{r2}$*$\leftarrow$*Dequeue(Q[ ]{.underline}f$_{root}$)*;\
*c$_{old}$*$\leftarrow$*Cost(T$_{f}$, x$_{r1}$)*;\
*c$_{new}$*$\leftarrow$*Cost(T$_{f}$, x$_{r1}$)+d$_{E}$(x$_{r2}$, x$_{near}$)+d$_{E}$(x$_{r1}$, x$_{r2}$)*;\
*T$_{f}$*$\leftarrow$*UpdateEdge(T$_{f}$, x$_{near}$, x$_{r1}$)*;\
*Enqueue(Q[ ]{.underline}f$_{root}$, x$_{near}$)*;\
:::

When the goal point is in the tree, the goal rewiring method is performed, which is presented in Algorithm 5. In the algorithm, the reference data stack *S[ ]{.underline}f$_{goal}$* and reference queue *Q[ ]{.underline}f$_{goal}$* are used for path optimization, where *S[ ]{.underline}f$_{goal}$* stores the nodes of the current branch and *Q[ ]{.underline}f$_{goal}$* stores the nodes of the next branch. When both *S[ ]{.underline}f$_{goal}$* and *Q[ ]{.underline}f$_{goal}$* are empty, the root information of the real-time tree offset is pushed to *S[ ]{.underline}f$_{goal}$* (Lines 1$\sim$`<!-- -->`{=html}2). Here a two-step optimization approach is introduced in this paper: (1) when time is less than *t$_{goal}$* and there is a non-empty set of *len(Q[ ]{.underline}f$_{goal}$)* or *len(S[ ]{.underline}f$_{goal}$)*, the goal rewiring of AM-RRT\*[@armstrong2021rrt] is performed (Lines 4$\sim$`<!-- -->`{=html}6); and (2) when the time is less than twice *t$_{goal}$* and as long as there is a set *len(Q[ ]{.underline}f$_{goal}$)* or *len(S[ ]{.underline}f$_{goal}$)* longer than 2, the optimization strategy is performed according to Fig. [3](#fig3){reference-type="ref" reference="fig3"} (Lines 7$\sim$`<!-- -->`{=html}9), and the details can be found in Algorithm 6. The two-step optimization approach avoids suboptimal paths caused by obstacles, which reduce path length.

::: algorithm
*Push(S[ ]{.underline}f$_{goal}$, x$_{root\underline{~}f}$)*;\
*start*$\leftarrow$*clock()*;\
*RewireGoalFirst(T$_{f}$, Q[ ]{.underline}f$_{goal}$, S[ ]{.underline}f$_{goal}$, x$_{goal\underline{~}f}$)*; *RewireGoalSecond(T$_{f}$, Q[ ]{.underline}f$_{goal}$, S[ ]{.underline}f$_{goal}$, x$_{goal\underline{~}f}$)*;
:::

Algorithm 6 elaborates the second step of the optimization in Algorithm 5. This process uses the information from both points *x$_{r1}$* and *x$_{r2}$* to speed up the optimization process and reduce the path length. When the length of *S[ ]{.underline}f$_{goal}$* is greater than 2, *x$_{r1}$* and *x$_{r2}$* are popped in turn, otherwise they exit the queue in turn. (Lines 1$\sim$ 6). When *x$_{r1}$* is inside the rewire ellipse [@gammell2014informed] (nodes inside the ellipse are more likely to be utilized), the cost of each node within the *x$_{r1}$* radius of *e$_{max}$* is calculated. And if there is a point with a smaller cost, the rewiring optimization is performed (Lines 7$\sim$`<!-- -->`{=html}13). If the point is not in *S[ ]{.underline}f$_{goal}$*, it will be added to *S[ ]{.underline}f$_{goal}$* and *Q[ ]{.underline}f$_{goal}$*. Moreover, if the distance from the second node at the top in *S[ ]{.underline}f$_{goal}$* to the goal point is greater than the sum of the distance from *x$_{r1}$* to the goal point and the distance from *x$_{r1}$* to *x$_{r1}$*, the branch is discarded. Then the next iteration is continued (Lines 14$\sim$`<!-- -->`{=html}18).

::: algorithm
*x$_{r1}$=Pop(S[ ]{.underline}f$_{goal}$)*;\
*x$_{r2}$=Pop(S[ ]{.underline}f$_{goal}$)*;\
*x$_{r1}$=Dequeue(Q[ ]{.underline}f$_{goal}$)*;\
*x$_{r2}$=Dequeue(Q[ ]{.underline}f$_{goal}$)*;\
*c$_{old}$*$\leftarrow$*Cost(T$_{f}$, x$_{near}$)*;\
*c$_{new}$*$\leftarrow$*Cost(T$_{f}$, x$_{r2}$)+d$_{E}$(x$_{r1}$, x$_{near}$) +d$_{E}$(x$_{r1}$, x$_{r2}$)*;\
*T$_{f}$*$\leftarrow$*UpdateEdge(T$_{f}$, x$_{r2}$, x$_{near}$)*;\
*S[ ]{.underline}f$_{goal}$*$\leftarrow$*x$_{near}$}*;\
*Q[ ]{.underline}f$_{goal}$*$\leftarrow$*x$_{near}$}*;\
*S[ ]{.underline}f$_{goal}$=\[\]*
:::

The proposed Bi-AM-RRT\* can significantly reduce planning costs in both small simple environments and large complex environments with dynamic obstacles. The use of bidirectional tree shorten the time cost of finding the feasible path. During exploration, the suboptimal paths resulting from bidirectional tree connection are optimized by growing the entire path radially around. In addition, the use of the proposed root rewiring and goal rewiring methods accelerates path optimization and reduces the path length.

# Experiments and Results {#section5}

In order to prove the effectiveness and efficiency of the proposed method, extensive comparative experiments are carried out in different simulation environments. This section gives the experimental details, while the comparison and discussion of experimental results are provided.

## Experimental setting

The experiments are conducted in PyCharm 2021 on top of a Lenovo Y7000p laptop running Windows OS Intel i5-8300H CPU at 2.3 GHz having 16 GB of RAM. To demonstrate the validity and efficiency of the proposed method, our method is compared with RT-RRT\* [@naderi2015rt] and AM-RRT\* [@armstrong2021rrt]. Further, based on the bidirectional search sampling strategy and new rewiring strategy proposed in this work, extensive comparative experiments are designed using five state-of-the-art planners RT-RRT\*, RT-RRT\*(D), AM-RRT\*(E), AM-RRT\*(D) and AM-RRT\*(G) [@naderi2015rt; @armstrong2021rrt] to fully evaluate the performance of the Bi-AM-RRT\*. Specifically,

1.  based on five planners, only the bidirectional search strategy is used to design five types of planners, which are denoted as RT-RRT\*-1, RT-RRT\*(D)-1, AM-RRT\*(E)-1, AM-RRT\*(D)-1 and AM-RRT\*(G)-1.

2.  based on five planners, only the proposed rewiring strategy is used to design five types of planners, which are denoted as RT-RRT\*-2, RT-RRT\*(D)-2, AM-RRT\*(E)-2, AM-RRT\*(D)-2 and AM-RRT\*(G)-2.

3.  based on five planners, both the bidirectional search strategy and proposed rewiring strategy are used to design five types of planners, which are denoted as Bi-RT-RRT\*, Bi-RT-RRT\*(D), Bi-AM-RRT\*(E), Bi-AM-RRT\*(D) and Bi-AM-RRT\*(G).

As shown in Table [\[table1\]](#table1){reference-type="ref" reference="table1"}, a total of 20 planners are implemented for comparison. Moreover, experiments are carried out in three challenging scenarios to better demonstrate the robustness and applicability, namely Bug[ ]{.underline}trap, Maze, and Office (see Fig. [4](#fig5){reference-type="ref" reference="fig5"}), where the size of Bug[ ]{.underline}trap and Maze is 100$m$ $\times$ 100$m$, and the size of Office is 200$m$ $\times$ 200$m$. In the three scenarios, the parameter settings of planners are listed in Table [1](#table2){reference-type="ref" reference="table2"}. Note that the connection distance $\sigma$ used in bidirectional tree is set to 50$m$ in the Bug[ ]{.underline}trap scenario and 30$m$ in the other scenarios.

:::: table*
::: tabular
c c c c c c &\
Original & RT-RRT\* & RT-RRT\*(D) & AM-RRT\*(E) & AM-RRT\*(D) & AM-RRT\*(G)\
Bidirectional search-based & RT-RRT\*-1 & RT-RRT\*(D)-1 & AM-RRT\*(E)-1 & AM-RRT\*(D)-1 & AM-RRT\*(G)-1\
Proposed rewiring strategy-based & RT-RRT\*-2 & RT-RRT\*(D)-2 & AM-RRT\*(E)-2 & AM-RRT\*(D)-2 & AM-RRT\*(G)-2\
Bidirectional-and proposed rewiring strategy-based& Bi-RT-RRT\* & Bi-RT-RRT\*(D) & Bi-AM-RRT\*(E) & Bi-AM-RRT\*(D) & Bi-AM-RRT\*(G)\
:::
::::

:::: {#fig5 .figure}
::: caption
Experimental scenario: (a) Bug[ ]{.underline}trap, (b) Maze, and (c) Office, where the letters S and G represent the starting point and goal point, respectively. The sizes of the three scenarios are 100$m$ $\times$ 100$m$, 100$m$ $\times$ 100$m$, and 200$m$ $\times$ 200$m$, respectively.
:::
::::

::: {#table2}
                 *t$_{exp}$*/s   *t$_{root}$*/s   *t$_{goal}$*/s   *e$_{max}$*/m   *n$_{max}$*   *$\sigma$*/m
  ------------- --------------- ---------------- ---------------- --------------- ------------- --------------
  RT-RRT\*           0.15            0.003            0.003              5             12           30/50
  RT-RRT\*(D)        0.15            0.003            0.003              5             12           30/50
  AM-RRT\*(E)        0.15            0.002            0.004              5             20           30/50
  AM-RRT\*(D)        0.15            0.002            0.004              5             20           30/50
  AM-RRT\*(G)        0.15            0.002            0.004              5             20           30/50

  : Parameters setting of planner
:::

In the experiment, each planner is tested in a typical task where the agent needs to plan a feasible path to the goal point G from the starting point S in different scenarios with static obstacles, while recording the search time cost and path length of the agent's movement path from the start to the goal. To fairly evaluate the performance of the method, each experiment is repeated 25 times. The average of the 25 experiments is then used for an unbiased comparison of experimental results. In addition, we further verify the performance of the proposed method in the environment with dynamic obstacles, where dynamic obstacles are simulated by using black circles to block the robot's direction of motion (refer to Fig. [1](#fig1){reference-type="ref" reference="fig1"}).

## Results

### Scenario With Static Obstacles

According to the experimental setup, 20 different planners were implemented in three different scenarios. The experimental results are shown in Fig. [5](#fig6){reference-type="ref" reference="fig6"}. Fig. [5](#fig6){reference-type="ref" reference="fig6"}(a) presents the performance comparison comparison with and without the bidirectional search sampling strategy. Since suboptimal paths can be generated in bidirectional tree connections (see Fig. [6](#fig4){reference-type="ref" reference="fig4"}), the path length of the five planners based on bidirectional strategy increases, but only by 0.8%. Note that the search times are significantly improved with the use of the bidirectional search strategy. In the Bug[ ]{.underline}trap, Maze, and Office, the time costs are reduced by about 69%, 40.1%, and 41.7%, respectively. In particular, the search time of AM-RRT\*(E)-1 can be reduced by up to 75.6% in the Bug[ ]{.underline}trap scenario. Therefore, the results illustrate that the use of bidirectional search sampling strategy is effective.

![Comparison of experimental results. The average path length and search time required by different planners to find a feasible path from the starting point S to the goal point G in different scenarios, where (a) represents the results with (i.e., Modify) and without (i.e., Original) the bidirectional search sampling strategy, and (b) represents the results with (i.e., Modify) and without (i.e., Original) the proposed rewiring strategy, and (c) represents the results with (i.e., Modify) and without (i.e., Original) the bidirectional search sampling strategy and proposed rewiring strategy.](Zhang2023BiAMRRT_figs/6.png){#fig6 width="7in"}

:::: {#fig4 .figure}
::: caption
Path optimization process. (a) When a bidirectional tree connection produces a suboptimal path (red zone), (b) it can be optimized due to the continuous growth of the tree.
:::
::::

The results of Fig. [5](#fig6){reference-type="ref" reference="fig6"}(b) demonstrate that the combination of the original method and the proposed rewiring strategy can optimize the average performance of the path length and search time in the three scenarios to a certain extent. And the path length can be reduced by an average of about 2.2%. Especially for AM-RRT\*(D)-2, it can still shorten the path length by 3% and reduce the search time by 5.6% even in the large scenario (i.e., Office). Overall, the results demonstrate the effectiveness and generalizability of the proposed rewiring method of this paper.

Fig. [5](#fig6){reference-type="ref" reference="fig6"}(c) illustrates a comparison of the results between the solution presented in this paper (i.e., the strategy of fusing bidirectional search sampling strategy and proposed rewiring strategy) and the original solution. It can be seen that the proposed solution can achieve superior performance in terms of path length and search time, except for the slight increase in path length of Bi-RT-RRT\* and Bi-AM-RRT\*(E) planners in the Bug[ ]{.underline}trap scenario. The reason for this is that the bidirectional strategy and greater connection distance reduce the search time, but when the goal point is found, the number of nodes generated in the tree is insufficient, resulting in a lower degree of path optimization, which will be discussed in detail in Section [6](#section6){reference-type="ref" reference="section6"}. Besides, on average, Bi-AM-RRT\*(E) achieves the superior optimization performance in terms of search time, which can be reduced by 76.7%, but increased by 2.6%in terms of path length. It is worth noting that Bi-AM-RRT\*(D) obtains the most promising performance overall. In the three scenarios, Bi-AM-RRT\*(D) optimizes search time by 24.6%, 45.2% and 44.9%, respectively, and reduces path length by 1.4%, 0.7% and 2.8%, respectively.

::: {#table3}
                    Bug[ ]{.underline}trap   Maze   Office
  ---------------- ------------------------ ------ --------
  Bi-RT-RRT\*                 /               /       /
  Bi-RT-RRT\*(D)             1.5s            1.5s    5.6s
  Bi-AM-RRT\*(E)              /               /       /
  Bi-AM-RRT\*(D)             1.5s            1.5s    5.6s
  Bi-AM-RRT\*(G)             49s             49s     232s

  : Map processing time for each planner in different scenarios
:::

In addition, for Bi-RT-RRT\* and Bi-AM-RRT\*(E) planners, map processing time is not required. But for Bi-RT-RRT\*(D) and Bi-AM-RRT\*(D) planners, the diffusion maps are needed, while the geodesic metric is required for Bi-AM-RRT\*(G) planner. Table [2](#table3){reference-type="ref" reference="table3"} shows the map processing time for each planner in different scenarios. Although diffusion map processing takes time, the map processing time for Bug[ ]{.underline}trap and Maze scenarios is about 1.5$s$. Even for larger Office scenario, it only takes 5.6$s$. As tested in this work, the geodesic metric for Bug[ ]{.underline}trap and Maze scenarios take about 49$s$, while Office scenarios take about 232$s$. In this context, Bi-AM-RRT\*(D) outperforms other planners in terms of total search time (including map processing time) and path length. The reason behind this is that diffusion maps are a way to use dimensional collapse to reduce map processing time [@coifman2006diffusion; @chen2016motion], such that some details are ignored when processing larger and more complex maps. Therefore, in the Office scenario, the search time of Bi-RT-RRT\*(D) is still large, but it has less impact on planners based on AM. Although the comprehensive performance of Bi-RT-RRT\*(D) in small scenes is similar to that of Bi-AM-RRT\*(D), it is not suitable for larger scenarios. In conclusion, Bi-AM-RRT\*(D) is an excellent planner that further improves performance, and is suitable for both small and large scenarios. The results, then, further demonstrate the effectiveness and efficiency of our proposed strategy.

### Scenario With Dynamic Obstacles

In order to test the obstacle avoidance performance of the proposed method, the experiment is conducted in the Office scenario with the dynamic obstacle. The dynamic obstacle is simulated by using a solid black circle that can be added anywhere at any time to block the path of the robot. The experimental results are depicted in Fig. [7](#fig7){reference-type="ref" reference="fig7"}. When the goal point is given, both trees grow at the same time \[Fig. [7](#fig7){reference-type="ref" reference="fig7"}(a)\]. When the distance is close enough \[Fig. [7](#fig7){reference-type="ref" reference="fig7"}(b)\], the two paths are connected to one path at two green dots, and the reverse tree stops growing and initializes. The forward tree uses information from the reverse path to grow quickly to the goal point and to the whole map. During the navigation, when there is an obstacle in the path \[refer to Fig. [7](#fig7){reference-type="ref" reference="fig7"}(c)\], the forward tree uses the node information near the obstacle to quickly generate a feasible path to avoid the obstacle, allowing the agent to move along the planned path and safely reach the goal \[see Fig. [7](#fig7){reference-type="ref" reference="fig7"}(d)\]. Hence the results show that the proposed method can address the obstacle avoidance in dynamic environments.

:::: {#fig7 .figure}
::: caption
Obstacle avoidance performance of the proposed algorithm in the Office scenario. In (a) the blue line is the forward tree path and the green line is the reverse tree path. When two trees are close enough, they are connected into one tree through two green points (b). And when the black circle of obstacle appears in the path (c), a feasible path is quickly planned by using the information of nearby branches (d).
:::
::::

# Disscussion {#section6}

This section discusses the effect of the connection distance $\sigma$ on the obstacle avoidance performance and the number of nodes on the path optimization.

In this paper, the values of $\sigma$ are set to 30$m$ and 50$m$. This is very large for the connection distance between the two trees. While this makes it easier to connect the two trees, it also makes it easier to produce the suboptimal path, as shown in Fig. [6](#fig4){reference-type="ref" reference="fig4"}. For example, in the Bug[ ]{.underline}trap scenario, $\sigma$ is set to 50$m$ to allow the two trees of the Bi-RT-RRT\* and Bi-AM-RRT\*(E) planners to connect more easily, as illustrated in Fig. [8](#fig8){reference-type="ref" reference="fig8"}. Due to the guidance of Euclidean distance, the two trees are trapped at point A and point B in Fig. [8](#fig8){reference-type="ref" reference="fig8"}(a) for a long time, and the distance is far away. This is why the search times of these two planners are optimized by more than 50%, as shown in Fig. [5](#fig6){reference-type="ref" reference="fig6"}(a) and (c). When two trees are connected by the diffusion map or geodesic metric, the other three planners are connected basically in the upper left area of the Bug[ ]{.underline}trap scenario (see Fig. [2](#fig2){reference-type="ref" reference="fig2"}). Although $\sigma$ is set at 50$m$, it is not fully utilized, resulting in less optimization of the search time.

:::: {#fig8 .figure}
::: caption
Path planned by Bi-RT-RRT\* and Bi-AM-RRT\*(E) in the Bug[ ]{.underline}trap scenario. Since the Euclidean metric guides, the forward tree will be trapped in point A, and the reverse tree will be trapped in point B in (a) for a long time, so $\sigma$ is set to 50 for optimization. Although there is a longer suboptimal path after successful connection, but it has been gradually optimized before the agent arrives (b).
:::
::::

Also taking Bug[ ]{.underline}trap scenario as an example, it can be seen from Fig. [5](#fig6){reference-type="ref" reference="fig6"} that the search time using AM-RRT\*(E) is the longest, but the path length is shorter than that of RT-RRT\* and almost the same as that of AM-RRT\*(D). Since the agent starts moving when the planner finds the goal point, AM-RRT\*(E) can generate more nodes in the more search time. In other words, the path can be fully optimized by the time the agent starts moving. Although the tree grows in real time, RT-RRT\* does not have enough nodes to path optimization, as depicted in Fig. [9](#fig9){reference-type="ref" reference="fig9"}. In the experiment, when a feasible path to the goal point is found, RT-RRT\* generates an average of 445 nodes, AM-RRT\*(E) generates an average of 1062 nodes, and AM-RRT\*(D) generates only 76 nodes on average. After fusing the bidirectional strategy, Bi-RT-RRT\* and Bi-AM-RRT\*(E) can improve the efficiency of search time by more than 60%, but lead to a slight increase in path length. Although Bi-AM-RRT\*(G) achieves the shortest search time and path length, it requires a long map processing time. Bi-AM-RRT\*(D), on the other hand, completes the near-optimal path planning in a less time.

:::: {#fig9 .figure}
::: caption
Tree optimization process of the AM-RRT\*(E) (a) and RT-RRT\* (b).
:::
::::

In the Bug[ ]{.underline}trap scenario, $\sigma$ is set to 50$m$, and all planners can achieve obstacle avoidance performance. Although the three planners do not take full advantage of this large connection range, the Bi-RT-RRT\* and Bi-AM-RRT\*(E) can maintain path optimization and obstacle avoidance functions. This is due to the loopback path generated after the paths are connected, and there are more nodes available in this region to grow the tree and optimize the structure of the tree by rewiring before the agent arrives. In other scenarios, however, setting $\sigma$ to 50$m$ does not maintain rewiring and obstacle avoidance in some extreme connection situations, as shown in Fig. [10](#fig10){reference-type="ref" reference="fig10"}. To this end, the $\sigma$ setting of 30 is tested in the Office scenario, which shows that excellent performance can be maintained even under extreme connection conditions. For this purpose, the $\sigma$ is set to 30$m$ in experiments. The value of $\sigma$ should be determined based on factors such as the size of the scene map, the tree growth time *t$_{exp}$*, and the movement speed of the agent. In this paper, the values of $\sigma$ are not universal in different scenarios, but have certain reference value.

:::: {#fig10 .figure}
::: caption
The obstacle avoidance of Bi-AM-RRT\*(D) in the Office scenario when $\sigma$ is set to 50$m$. Although the two trees are successfully connected, there are no nodes between the two points A and B for tree growth (a). And the growth rate of the two points A and B, is not enough to maintain the path optimization and obstacle avoidance in that connected path when the agent arrives, resulting in the agent colliding with the obstacle (b).
:::
::::

# Conclusion {#section7}

In this paper, a novel motion planning approach, namely Bi-AM-RRT\*, has been proposed. Bi-AM-RRT\* uses a bidirectional search strategy and a new rewiring approach to reduce the search time and the path length. In the Bi-AM-RRT\*, two trees grow simultaneously when the goal point is not in the forward tree. Then they are connected as one tree when the distance is less than connection distance. In this case, the path to goal is generated by the forward tree while the reverse tree stops growing and initializes. The proposed rewiring method is used to reduce the path length. To this end, the shorter search time allows for faster generation of agent-to-goal paths, which in turn allows for more efficient tree growth by growing trees from points in the path to other regions. Extensive experiments have been carried out in three different scenarios for comparison. The results have demonstrated the validity of our proposal, and effectively improved the motion planning search time and path length. In particular, Bi-AM-RRT\*(D) has the best comprehensive performance, while optimizing the search time and path length. In addition, this paper has also discussed the influence of the value of the connection distance on the planner and shown the practicality and robustness of the presented approach.

It is worth noting that in the used bidirectional search strategy, the forward tree only uses the trunk information of the reverse tree, while its branch node information is discarded after a successful connection. In the future work, the use of branch information will be considered to further improve the path optimization and obstacle avoidance performance. And deploying our solution to mobile robots in real-world scenarios will also be investigated in future research.

[^1]: This work was supported in part by the National Natural Science Foundation of China under Grant No. 62203378, 62203377, U22A2050, in part by the Hebei Natural Science Foundation under Grant No. F2022203098, F2021203054, in part by the Science and Technology Research Plan for Colleges and Universities of Hebei Province under Grant No. QN2022077, and in part by the Hebei Innovation Capability Improvement Plan Project under Grant No. 22567619H. *(Corresponding author: Ying Zhang.)*

[^2]: Y. Zhang, H. Wang, M. Yin, and C. Hua are with the School of Electrical Engineering and the Key Laboratory of Intelligent Rehabilitation and Neromodulation of Hebei Province, Yanshan University, Qinhuangdao, 066004, China. (e-mail: yzhang@ysu.edu.cn; wtk0405@163.com; yin924431601@163.com; cch@ysu.edu.cn).

[^3]: J. Wang is with the Shenzhen Key Laboratory of Robotics Perception and Intelligence, Shenzhen 518055 China, and also with the Department of Electronic and Electrical Engineering, Southern University of Science and Technology, Shenzhen 518055, China (e-mail: wangjk@sustech.edu.cn).
