---
citation_key: Zhang2020World
arxiv_id: 2011.12491
arxiv_url: https://arxiv.org/abs/2011.12491
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:53:30Z
origin: ai+web
reviewed: false
---

# Introduction

An intelligent agent should be able to solve difficult problems by breaking them down into sequences of simpler problems. Classically, planning algorithms have been the tool of choice for endowing AI agents with the ability to reason over complex long-horizon problems [@doran1966experiments; @hart1968formal]. Recent years have seen an uptick in monographs examining the intersection of classical planning techniques -- which excel at temporal abstraction -- with deep reinforcement learning (RL) algorithms -- which excel at state abstraction. Perhaps the ripest fruit born of this relationship is the AlphaGo algorithm, wherein a model free policy is combined with a MCTS [@mcts] planning algorithm to achieve superhuman performance on the game of Go [@silver2016mastering].

In the field of robotics, progress on combining planning and reinforcement learning has been somewhat less rapid, although still resolute. Indeed, the laws of physics in the real world are vastly more complex than the simple rules of Go. Unlike board games such as chess and Go, which have deterministic and known dynamics and discrete action space, robots have to deal with a probabilistic and unpredictable world. Moreover, the action space for robotics is often continuous. As a result of these difficulties, planning in robotics presents a much harder problem. One general class of methods [@dyna] seeks to combine model-based planning and deep RL. These methods can be thought of as an extension of model-predictive control (MPC) algorithms, with the key difference being that the agent is trained over hypothetical experience in addition to the actually collected experience. The primary shortcoming of this class of methods is that, like MCTS in AlphaGo, they resort to planning with action sequences -- forcing the robot to plan for each action at every hundred milliseconds. Planning on the level of action sequences is fundamentally bottlenecked by the accuracy of the learned dynamics model and the horizon of a task, as the learned world model quickly diverges over a long horizon. This limitation shows that world models in the traditional Model-based RL (MBRL) setting often fail to deliver the promise of planning.

Another general class of methods, Hierarchical RL (HRL), introduces a higher-level learner to address the problem of planning [@feudal_hinton; @vezhnevets2017feudal; @hiro]. In this case, a goal-based RL agent serves as the worker, and a manager learns what sequences of goals it must set for the worker to achieve a complex task. While this is apparently a sound solution to the problem of planning, hierarchical learners neither explicitly learn a higher-level model of the world nor take advantage of the graph structure inherent to the problem of search.

![MBRL versus $L^{3}P$(World Model as a Graph). MBRL does step-by-step virtual rollouts with the world model and quickly diverges from reality when the planning horizon increases. $L^{3}P$ models the world as a graph of sparse multi-step transitions, where the nodes are learned latent landmarks and the edges are reachability estimates. $L^{3}P$ succeeds at temporally extended reasoning. **Code** for $L^{3}P$ is available at: <https://github.com/LunjunZhang/world-model-as-a-graph>.](Zhang2020World_figs/L3P_paradigm_big.png){#fig:overview width="43%"}

To better combine classical planning and reinforcement learning, we propose to learn graph-structured world models composed of sparse multi-step transitions. To model the world as a graph, we borrow a concept from the navigation literature -- the idea of landmarks [@wang2008robot]. Landmarks are essentially states that an agent can navigate between in order to complete tasks. However, rather than simply using previously seen states as landmarks, as is traditionally done, we will instead develop a novel algorithm to learn the landmarks used for planning. Our key insight is that by mapping previously achieved goals into a latent space that captures the temporal distance between goals, we can perform clustering in the latent space to group together goals that are easily reachable from one another. Subsequently, we can then decode the latent centroids to obtain a set of goals scattered (in terms of reachability) across the goal space. Since our learned landmarks are obtained from latent clustering, we call them *latent landmarks*. The chief algorithmic contribution of this paper is a new method for planning over learned latent landmarks for high-dimensional continuous control domains, which we name Learning Latent Landmarks for Planning ($L^{3}P$).

The idea of reducing planning in RL to a graph search problem has enjoyed some attention recently [@sptm; @sorb; @mss; @Liu2019-mh; @yang2020plan2vec; @sgm]. A key difference between those works and $L^{3}P$ is that our use of *learned* latent landmarks allows us to substantially reduce the size of the search space. What's more, we make improvements to the graph search module and the online planning algorithm to improve the robustness and sample efficiency of our method. As a result of those decisions, our algorithm is able to achieve superior performance on a variety of robotics domains involving both navigation and manipulation. In addition to the results presented in Section [5](#sec:experiments){reference-type="ref" reference="sec:experiments"}, **videos** of our algorithm's performance and a more detailed analysis of the sub-tasks discovered by the latent landmarks can be found at: <https://sites.google.com/view/latent-landmarks/>.

:::: {#fig:overview .figure latex-placement="h"}
![](Zhang2020World_figs/L3P_diagram.png){width="75%"}

::: caption
An overview of $L^{3}P$, which learns a small number of latent landmarks for planning. The main components of our method are: learning reachability estimates (via Q-learning and regression), learning a latent space (via an auto-encoder with reachability constraints), learning latent landmarks (via clustering in the latent space), graph search on the world model and online planning.
:::
::::

# Related Works

The problem of learning landmarks to aid in robotics problems has a long and rich history [@gillner1998navigation; @wang2002human; @wang2008robot]. Prior art has been deeply rooted in the classical planning literature. For example, traditional methods would utilize [@dijkstra1959note] to plan over generated waypoints, SLAM [@durrant2006simultaneous] to simultaneously integrate mapping, or the RRT algorithm [@lavalle1998rapidly] for explicit path planning. The A\* algorithm [@hart1968formal] further improved the computational efficiency of Dijkstra. Those types of methods often heavily rely on a hand-crafted configuration space that provides prior knowledge.

Planning is intimately related to model-based RL (MBRL), as the core ideas underlying learned models and planners can enjoy considerable overlap. Perhaps the most clear instance of this overlap is Model Predictive Control (MPC), and the related Dyna algorithm [@dyna]. When combined with modern techniques [@me_trpo; @slbo; @mb_mf; @ha2018recurrent; @latent_dynamics; @exploring_mbrl; @mbpo], MBRL is able to achieve some level of success. [@state_tabulation] and [@hafner2020mastering] also learn a discrete latent representation of the environment in the MBRL framework. As discussed in the introduction, planning on action sequences will fundamentally struggle to scale in robotics.

Our method makes extensive use of a parametric goal-based RL agent to accomplish low-level navigation between states. This area has seen rapid progress recently, largely stemming from the success of Hindsight Experience Replay (HER) [@her]. Several improvements to HER augment the goal relabeling and sampling strategies to boost performance [@rig; @tdm; @skew-fit; @mep; @mega]. There have also been attempts at incorporating search as inductive biases within the value function [@Silver2016predictron; @tamar2016VIN; @Farquhar2017treeQN; @Racaniere2017I2A; @Lee2018gppn; @Srinivas2018UPN]. The focus of this line of work is to improve the low-level policy and is thus orthogonal to our work.

Recent work in Hierarchical RL (HRL) builds upon goal-based RL by learning a high-level parametric manager that feeds goals to the low-level goal-based agent [@feudal_hinton; @vezhnevets2017feudal; @hiro]. This can be viewed as a parametric alternative to classical planning, as discussed in the introduction. Recently, [@subgoal-trees; @long_plan] have derived HRL methods that are intimately tied to tree search algorithms. These papers are further connected to a recent trend in the literature wherein classical search methods are combined with parametric control [@sptm; @sorb; @mss; @Liu2019-mh; @yang2020plan2vec; @sgm]. Several of these articles will be discussed throughout this paper. LEAP [@leap] also considers the problem of proposing sub-goals for a goal-conditioned agent: it uses a VAE [@vae] and does CEM on the prior distribution to form the landmarks. Our method constrains the latent space with temporal reachability between goals, a concept previously explored in [@reachability], and uses latent clustering and graph search rather than sampling-based methods to learn and propose sub-goals.

# Background

We consider the problem of Multi-Goal RL under a Markov Decision Process (MDP) parameterized by $(S, A, \mathds P, G, \Psi, R, \rho_0)$. $S$ and $A$ are the state and action space. The probability distribution of the initial states is given by $\rho_0(s)$, and $\mathds P(s'\vert s, a)$ is the transition probability. $\Psi: S \mapsto G$ is a mapping from the state space to the goal space, which assumes that *every* state $s$ can be mapped to a corresponding *achieved* goal $g$. The reward function $R$ can be defined as $R(s,a,s', g) = -\mathds{1} \{\Psi(s') \neq g \}$. We further assume that each episode has a fixed horizon $T$.

A multi-goal policy is a probability distribution $\pi: S \times G \times A \rightarrow \mathbb{R}^{+}$, which gives rise to trajectory samples of the form $\tau = \{s_{0}, a_{0}, g, s_{1}, \cdots s_{T}\}$. The purpose of the policy $\pi$ is to learn how to reach the goals drawn from the goal distribution $p_{g}$. With a discount factor $\gamma \in (0, 1)$, it maximizes $\mathcal{J}(\pi) = \mathbb{E}_{g \sim p_{g}, \tau \sim \pi(g)}[\sum_{t=0}^{T-1} \gamma^{t} \cdot R(s_{t}, a_{t}, s_{t+1}, g) ]$. Q-learning provides a sample-efficient way to optimize the above objective by utilizing off-policy data stored in a replay buffer $B$. $Q(s,a,g)$ estimates the reward-to-go under the current policy $\pi$ conditioned upon the given goal. An additional technique, called Hindsight Experience Replay, or HER [@her], uses hindsight relabelling to drastically speed up training. This relabeling crucially relies upon the mapping $\Psi: S \mapsto G$ in the multi-goal MDP setting. We can write the the joint objective of multi-goal Q-learning with HER as minimizing (with $Q$ being the online network and $\widehat{Q}$ being the target network): $$\begin{align}
    \Big(Q(s_{t}, a_{t}, g) - \Big(R(s_{t+1}, g) + \gamma \cdot \widehat{Q}(s_{t+1}, a', g)\Big) \Big)^{2} \label{dqn-loss}
\end{align}$$ where $\tau \sim B, t\sim \{0\cdots T-1\}, (s_{t},a_{t},s_{t+1}) \sim \tau, k \sim \{t+1 \cdots T\} , g = \Psi(s_{k}) , a' \sim \pi(\cdot \mid s_{t+1}, g)$.

# The $L^{3}P$ Algorithm

Our overall objective in this section is to derive an algorithm that learns a small number of landmarks scattered across goal space in terms of reachability and use those learned landmarks for planning. There are three chief difficulties we must overcome when considering such an algorithm. First, how can we group together goals that are easily reachable from one another? The answer is to embed goals into a latent space, where the latent representation captures some notion of temporal distance between goals -- in the sense that goals that would take many timesteps to navigate between are further apart in latent space. Second, we need to find a way to learn a sparse set of landmarks used for planning. Our method performs clustering on the constrained latent space, and decodes the learned centroids as the landmarks we seek. Finally, we need to develop a non-parametric planning algorithm responsible for selecting sequences of landmarks the agent must traverse to accomplish its high-level goal. The proposed online planning algorithm is simple, scalable, and robust.

## Learning a Latent Space {#sec:latent-space}

Let us consider the following question: "How should we go about learning a latent space of goals where the metric reflects reachability?" Suppose we have an auto-encoder (AE) in the agent's goal space, with deterministic encoder $f_E$ and decoder $f_D$. As usual, the reconstruction loss is given by $\mathcal{L}_{rec}(g) = \Big\lVert f_{D} \big(f_{E}(g)\big) - g \Big\rVert_{2}^{2}$. We want to make sure that the distance between two latent codes would roughly correspond to the number of steps it would take the policy to go from one goal to another. Concretely, for any pair of goals $(g_{1}, g_{2})$, we optimize the following loss $\mathcal{L}_{latent}(g_{1}, g_{2})$: $$\begin{align}
    \label{eq:ae-loss}
    \Big( \big\lVert f_{E}(g_{1}) - f_{E}(g_{2}) \big\rVert_{2}^{2} - \dfrac{1}{2} \big(V(g_{1}, g_{2}) + V(g_{2}, g_{1})\big) \Big)^{2}
\end{align}$$ Where $V: G \times G \rightarrow \mathbb{R}^+$ is a mapping that estimates how many steps it would take the policy $\pi$ to go from one goal to another goal on average. By adding this constraint and solving a joint optimization $\mathcal{L}_{rec} + \lambda \cdot \mathcal{L}_{latent}$, the encoding-decoding mapping can no longer be arbitrary, giving more structure to the latent space. Goals that are close by in terms of reachability will be naturally clustered in the latent space, and interpolations between latent codes will lead to meaningful results.

Of course, the constraint in Equation [\[eq:ae-loss\]](#eq:ae-loss){reference-type="ref" reference="eq:ae-loss"} is quite meaningless if we do not have a way to estimate the mapping $V$. We will proceed towards this objective by noting the following interesting connection between multi-goal Q-functions and reachability. In the multi-goal RL framework considered in the background section, the reward is binary in nature. The agent receives a reward of $-1$ until it reaches the goal, and then $0$ when it reaches the desired goal. In this setting, the Q-function is implicitly estimating *the number of steps* it takes to reach the goal $g$ from the current state $s$ *after* the action $a$ is taken. Denote this quantity as $D(s,a,g)$, the Q-function can be re-written as: $$\begin{equation}
\begin{aligned}
    Q(s,a,g) &= \sum_{t=0}^{D(s,a,g) - 1} \gamma^{t} \cdot (-1) + \sum_{t=D(s,a,g)}^{T-1} \gamma^{t} \cdot 0 \\
    &= - \dfrac{1 - \gamma^{D(s,a,g)}}{1 - \gamma} \label{dis-function}
\end{aligned}
\end{equation}$$ Choosing to parameterize Q-functions in this way disentangles the effect of $\gamma$ on multi-goal Q-learning. It also provides us with access the direct distance estimation function $D(s,a,g)$. We note that this *distance* is not a mathematical distance in the sense of a metric. Instead, we use the word *distance* to refer to the number of steps the policy $\pi$ needs to take in the environment.

Given our tractable estimate of $D$, it is now a straightforward matter to estimate the desired quantity $V$, which approximates how many steps it takes the policy to transition between goals. To get the desired estimate, we regress $V$ towards $D$ by minimizing $$\begin{align}
    \min_{V} \Bigg( D\big(s_{t}, a_{t}, \Psi(s_{k})\big) - V\big(\Psi(s_{t+1}), \Psi(s_{k})\big) \Bigg)^{2}
\end{align}$$ with $\tau \sim B, t\sim \{0\cdots T-1\}, (s_{t},a_{t},s_{t+1}) \sim \tau, k \sim \{t+1 \cdots T\}$, and $\Psi$ being given by the environment to map the states to the goal space. One crucial detail is the use of $\Psi(s_{t+1})$ rather than $\Psi(s_{t})$ in the inputs to $V$. This is due to the fact that $D: S \times A \times G \rightarrow \mathbb{R}$ outputs the number of steps to go *after* an action is taken, when the state has transitioned into $s_{t+1}$. The objective above provides an unbiased estimate of the average number of steps between two goals.

The estimates $D$ and $V$ will prove useful beyond helping to optimize the auto-encoder in Equation [\[eq:ae-loss\]](#eq:ae-loss){reference-type="ref" reference="eq:ae-loss"}. They will prove essential in weighting and planning over latent landmark nodes in Section 4.3.

## Learning Latent Landmarks

Planning on a graph can be expensive, as the number of edges can grow quadratically with the number of nodes. To battle this issue in scalability, we use the constrained latent space to learn a sparse set of landmarks. A landmark can be thought of as a waypoint that the agent can pass through enroute to achieve a desired goal. Ideally, *goals that are easily reachable from one another should be grouped to form one single landmark*. Since our latent representation captures the temporal reachability between goals, this can be achieved by doing clustering in the latent space. The cluster centroids, when decoded from the decoder, will be precisely the latent landmarks we are seeking.

Clustering proceeds as follows. For $N$ clusters to be learned, we define a mixture of Gaussians in the latent space with $N$ trainable latent centroids, $\{\textbf{c}_{1} \cdots \textbf{c}_{N}\}$, and a shared trainable variance vector $\boldsymbol{\sigma}$. We maximize the evidence lower bound (ELBO) with a uniform prior $p(\textbf{c})$: $$\begin{equation}
\begin{aligned}
    &\log p\Big(z = f_{E}(g) \Big) \\
    & \geq \mathbb{E}_{q(\textbf{c} \mid z)}\Big[\log p(z \mid \textbf{c})\Big] - D_{KL}\Big(q(\textbf{c} \mid z) \parallel p(\textbf{c})\Big) \label{elbo_eq}
\end{aligned}
\end{equation}$$ Ideally, we would like each batch of data given to the latent clustering model to be representative of the whole replay buffer, such that the centroids will quickly learn to scatter out. To this end, we propose to use the Greedy Latent Sparsification (GLS) algorithm (see the Appendix) on each batch of data sampled from the replay before taking a gradient step with the batch. GLS is inspired by kmeans++ [@kmeans_plus_plus], with several key differences: this sparsification process is used for both training and initialization, it uses a neural metric for determining the distance between data points, and that it is compatible with mini-batch-style gradient-based training.

[]{#section-learning-latent-landmarks label="section-learning-latent-landmarks"}

## Planning with Latent Landmarks {#section-planning-with-latent-landmarks}

Having derived a latent encoding algorithm and an algorithm for learning latent landmarks, we at last turn our attention to search and planning. $L^{3}P$ is agnostic to the graph search algorithm being used. In practice, we use a variant of the Floyd algorithm, where our relaxation operations use a soft max rather than hard max for better stability (see the Appendix for more details). To construct a weight matrix that provides raw distance estimates between latent landmarks in the first place, we begin by decoding the learned centroids in the latent space into the nodes in the graph $\{f_{D}(\textbf{c}_{1}) \cdots f_{D}(\textbf{c}_{N})\}$. To build the graph, we add two edges directed in reverse orders for every pair of latent landmarks. For instance, for an edge going from $f_{D}(\textbf{c}_{i})$ to $f_{D}(\textbf{c}_{j})$, the weight on that edge is $w_{i,j} = -V(f_{D}(\textbf{c}_{i}), f_{D}(\textbf{c}_{j}))$. Notice that the distances are negated. At the start of an episode, the agent receives a goal $g$, and we construct matrix $W$: $$\begin{align}
    W = \begin{pmatrix} 
        0 & \dots & w_{1,N} & -V(f_{D}(\textbf{c}_{1}), g)\\ 
        \vdots & \ddots & \vdots & \vdots\\
        w_{N, 1} & \dots & 0 & -V(f_{D}(\textbf{c}_{N}), g) \\
        -\infty & \dots & -\infty & 0
    \end{pmatrix} \label{distance_matrix}
\end{align}$$

::::: minipage
:::: algorithm
**Given**: Environment `env`, initial state $s$, goal $g$.

::: algorithmic
`Cnt` = $0$. `SubG` = `None`. Solve for $\boldsymbol{d}_{\boldsymbol{c} \rightarrow g}$ with [**graph search**]{style="color: red"} using $W$. `Cnt` $=\texttt{Cnt}- 1$ Calculate $\boldsymbol{d}_{s\rightarrow \boldsymbol{c}}$. $\boldsymbol{d}$ $\leftarrow$ $\boldsymbol{d}_{s\rightarrow \boldsymbol{c}} + \boldsymbol{d}_{\boldsymbol{c} \rightarrow g}$ $\boldsymbol{d}[\texttt{SubG}] \leftarrow -\infty$ `SubG`, `Cnt` $\leftarrow \mathop{\mathrm{arg\,max}}\boldsymbol{d}$, $-\max \boldsymbol{d}$ $a \sim \pi(s, \texttt{SubG})$; $s \leftarrow$ `env.step(a)`.
:::

[]{#online_planning label="online_planning"}
::::
:::::

![We consider two environments involving a fetch robot, a block, and a box. In Box-Distractor-PickAndPlace, the fetch must learn to pick and place the block while avoiding collision with the box. In Place-Inside-Box, the fetch must pick the block and place it inside the box. We visualize the fetch states corresponding to learned landmarks in the second row of images. ](Zhang2020World_figs/place-landmarks.png){#fig:place-task width="40%"}

For online planning, when the agent receives a goal at the start of an episode, we use graph search to solve for $\boldsymbol{d}_{\boldsymbol{c}\rightarrow g}$ (which is fixed throughout an episode). For an observation state $s$, the algorithm calculates $\boldsymbol{d}_{s\rightarrow \boldsymbol{c}}$: $$\begin{align}
    \boldsymbol{d}_{s\rightarrow \boldsymbol{c}} &= \begin{pmatrix} 
        - D\big(s, \pi(s, f_{D}(\textbf{c}_{1})), f_{D}(\textbf{c}_{1})\big) \\ 
        \vdots \\
        - D\big(s, \pi(s, f_{D}(\textbf{c}_{N})), f_{D}(\textbf{c}_{N})\big) \\
        - D\big(s, \pi(s, g), g\big)
    \end{pmatrix} \label{state_to_landmarks}
\end{align}$$ The chosen landmark is $\texttt{subgoal} \leftarrow \mathop{\mathrm{arg\,max}}(\boldsymbol{d}_{s\rightarrow \boldsymbol{c}} + \boldsymbol{d}_{\boldsymbol{c} \rightarrow g})$. To further provide temporal abstraction and robustness, the agent will be asked to consistently pursue `subgoal` for $K=-\boldsymbol{d}_{s\rightarrow \boldsymbol{c}}[\texttt{subgoal}]$ number of steps, which is *how many steps it thinks it will need*. The proposed goal does **not** change during this period. In this way, $L^{3}P$ makes sure that the agent does not re-plan at every step, and this mechanism for temporal abstraction is crucial to its robustness. This mechanism is detailed in Algorithm [\[online_planning\]](#online_planning){reference-type="ref" reference="online_planning"}.

After this $K$ many steps, the agent will decide on the next landmark to pursue by re-calculating $\boldsymbol{d}_{s\rightarrow \boldsymbol{c}}$, but the *immediate* previous landmark will not be considered as a candidate landmark. The reason is that, if the agent has failed to reach a self-proposed landmark within the reachability limit it has set for itself, then the agent should try something new for the immediate next goal rather than stick to the immediate previous landmark for another round. We have found that this simple algorithm helps the agent avoid getting stuck and improves the overall robustness of the agent.

In summary, we have derived an algorithm that learns a sparse set of latent landmarks scattered across goal space in terms of reachability, and uses those learned landmarks for robust planning.

# Experiments and Evaluation {#sec:experiments}

We investigate the impact of $L^{3}P$ in a variety of robotic manipulation and navigation environments. These include standard benchmarks such as Fetch-PickAndPlace, and more difficult environments such as AntMaze-Hard and Place-Inside-Box that have been engineered to require test-time generalization. Videos of our algorithm in action are available at: <https://sites.google.com/view/latent-landmarks/>.

:::: {#fig:test_curves .figure latex-placement="h"}
![image](Zhang2020World_figs/plot3_2.png){width="90%"} []{#fig:test_curves label="fig:test_curves"}

::: caption
Test time success rate vs. total number of timesteps, on a variety of challenging robotic navigation and manipulation environments. $L^{3}P$ demonstrates better sample efficiency, higher asymptotic performance, and in some cases, the ability to generalize to longer horizons.
:::
::::

![For both Point and Ant, during training, the initialization state distribution and the goal proposal distribution are *uniform* around the maze. During test time, the agent is asked to traverse the longest path in the maze, which is not seen during training. Importantly, the map of the environment is not given to the agent at any given point; the agent has to learn the structure of the environment purely through interaction. The success rate during test is reported in Figure [4](#fig:test_curves){reference-type="ref" reference="fig:test_curves"}. This environment demonstrates $L^{3}P$'s ability to generalize to longer horizon goals during test time.](figures/TRAIN-TEST.png){#fig:mazes width="45%"}

![Visualizing the paths taken by SORB, MSS and $L^{3}P$ on AntMaze at test time. The [blue dots]{style="color: blue"} in the backgrounds are the learned landmarks using $L^{3}P$. The [orange dot]{style="color: orange"} is the starting location of the Ant. The [red dot]{style="color: red"} is the final goal. The [blue stars]{style="color: blue"} indicate the landmarks chosen by the planning algorithms. As illustrated in the figure above, $L^{3}P$ addresses two major failure modes of graph-based planning with RL. Firstly, graph-based methods tend to switch proposed subgoals too frequently and fall into a loop due to wormholes in distance estimates, whereas $L^{3}P$ leverages temporal abstraction in both landmark learning and online planning to avoid this pitfall. Secondly, when the agent pursues a subgoal unsuccessfully (due to obstacles, etc), other methods tend to get stuck by continuing proposing the same subgoal, whereas $L^{3}P$ can adapt to the encountered failure and propose different subgoals in the event of getting stuck. ](figures/l3p-compare.png){#fig:plan_visualize width="48%"}

## Baselines

We compare our method with a variety of baselines. HER [@her] is a model-free RL algorithm. SORB [@sorb] is a method that combines RL and graph search by using the entire replay buffer. Mapping State Space (MSS @mss) reduces the number of vertices by sub-sampling the replay buffer. $L^{3}P$, SORB, and MSS all use the same hindsight relabelling strategy proposed in HER. All of the domains are continuous control tasks, so we adopt DDPG [@ddpg] as the learning algorithm for the low-level actor.

## Generalization to Longer Horizons

The PointMaze-Hard and AntMaze-Hard environments introduced in Figure [6](#fig:plan_visualize){reference-type="ref" reference="fig:plan_visualize"} are designed to test an agent's ability to generalize to longer horizons. While PointMaze and AntMaze have been previously used in [@duan2016benchmarking; @mss; @mega], we make slight changes to those environments in order to increase their difficulty. We use a short, 200-timestep time horizon during training and a $\rho_0$ that is uniform in the maze. At test time, we always initialize the agent on one end of the maze, and set the goal on the other end. The horizon of the test environment is 500 steps. Crucially, no prior knowledge on the shape of the maze is given to the agent. We also set a much stricter threshold for determining whether an agent has reached the goal. In Figure [4](#fig:test_curves){reference-type="ref" reference="fig:test_curves"}, we see $L^{3}P$ is the only algorithm capable of solving AntMaze-Hard consistently.

We observe an interesting trend where the success rates for some of other graph search methods crash and then slowly recover after making some initial progress. We postulate this occurs because methods that are based on using the entire replay or sub-sampling the replay for landmark selection will struggle as the buffer size increases. For instance, in the AntMaze-Hard environment, MSS and SORB use 400 and tens of thousands of landmarks respectively, whereas $L^{3}P$ obtains a lean graph that only contain 50 learnable landmarks. The result suggests that *learning latent landmarks* is significantly more sample efficient and stable than either directly using or sub-sampling the replay buffer to build the graph. The online planning algorithm in $L^{3}P$, which effectively leverages temporal abstraction to improve robustness, also contributes to the asymptotic success rate. As explained in Figure [6](#fig:plan_visualize){reference-type="ref" reference="fig:plan_visualize"}, $L^{3}P$ successfully addresses the common failure modes of graph-based RL methods. The result convincingly shows that, at least on the navigation tasks considered, $L^{3}P$ is most effective at taking advantage of the problem's inherent graph structure (without any prior knowledge of the map or environment configurations) and generalizing to longer horizons during test time.

## Robotic Manipulation Tasks

We also benchmark challenging robotic manipulations tasks with a Fetch robot introduced in [@plappert2018multi; @her]. Besides the PickAndPlace task, we also evaluate our method on two additional Fetch tasks involving a box on a table, as illustrated in Figure [3](#fig:place-task){reference-type="ref" reference="fig:place-task"}. In Box-Distractor-PickAndPlace environment, the agent needs to perform the pick-and-place task with a box in the middle of the table serving as a distractor. The Place-Inside-Box environment aims to teach the agent to place an object with randomly initialized locations into the box and has a simple curriculum. During training, the goal distribution has 80% regular pick-and-place goals, enabling the agent to first learn how to fetch in general. Meanwhile, only 20% of the goals are inside the box, which is the harder part of the task. During testing, we evaluate the agent's ability to pick up the object from the table and place it inside the box. Our method achieves dominant performance in both learning speed and test-time generalization on those three robotic manipulation environments. We note that on those manipulation tasks considered, many prior planning methods *hurt* the performance of the model-free agent. $L^{3}P$ is the only method that is able to help the model-free agent learn faster and perform better on all three tasks.

## Understanding Model Choices in $L^{3}P$

We investigate $L^{3}P$'s sensitivity to different design choices and hyper-parameters via a set of ablation studies. More specifically, we study how the following four factors affect the performance of $L^{3}P$: the choice of graph search algorithms, and edge weight cutoff threshold in graph search (a key hyper-parameter in the graph search module); the choice of online planning algorithms, and the number of latent landmarks being learned (a key hyper-parameter in the planning module).

![](Zhang2020World_figs/ablation-graph-search.png){width="35%"}

![Ablation studies on the graph search module, including the choice of graph search algorithms and a key hyper-parameter in graph search: the edge weight cutoff threshold. ](Zhang2020World_figs/ablation-d-max.png){#fig:graph-ablation width="35%"}

While $L^{3}P$ is agnostic to the graph search algorithm being used, we study the effect of two possible choices: Floyd algorithm and a soft version of Floyd (soft Floyd). As shown in Figure [7](#fig:graph-ablation){reference-type="ref" reference="fig:graph-ablation"}, the choice seems to have a relatively small effect on learning. During the early phase of experimentation, we find that having a *soft* operation for relaxation in Floyd leads to better overall training stability. A hard version of relaxation helps the learning curve take off faster but suffers from greater instability during policy improvement. The likely reason is that neural distance estimates are not entirely accurate, and in the presence of occasional bad edges, using $\textit{softmax}$ rather than hard max improves robustness. We therefore use soft relaxation in $L^{3}P$.

![](Zhang2020World_figs/ablation-planner.png){width="34%"}

![Ablation studies on the online planning module, including the choice of planners and a key hyper-parameter in graph-based planning: the number of nodes (landmarks).](Zhang2020World_figs/ablation-n-landmark.png){#fig:ablation-planning width="35%"}

In the graph search module, a very sensitive hyper-parameter is the edge weight cutoff threshold, denoted as $d\_max$. This clipping threshold is commonly used in prior works such as [@sptm; @sorb; @mss; @sgm]. It essentially means that if the weight of an edge is bigger than $d\_max$, then it is set to be infinity during the graph search process. The motivation for introducing this common hyper-parameter is two-fold. Firstly, we only trust distance estimates when they are *local*, because value iterations are inherently local. Secondly, we want the next sub-goal to be relatively *nearby* in terms of reachability. The $d\_max$ value determines the maximum (perceived) distance from the current state to next proposed subgoal. As shown in Figure [7](#fig:graph-ablation){reference-type="ref" reference="fig:graph-ablation"}, our current approach is still quite sensitive to this hyper-parameter; changes to $d\_max$ can have a considerable impact on learning. As this weakness is common to this class of approaches, we believe that further research is required to discover more principled ways of encouraging the search results to be local.

For online planning, the $L^{3}P$ planner introduced in Algorithm [\[online_planning\]](#online_planning){reference-type="ref+label" reference="online_planning"} is essential to the success of $L^{3}P$. Our planning algorithm can take advantage of the temporal abstraction provided by the graph-structured world model. As previously shown in Figure [6](#fig:plan_visualize){reference-type="ref" reference="fig:plan_visualize"}, the design of $L^{3}P$ planner avoids many common pitfalls. It does not re-plan at every step, but instead uses the reachability estimates to dynamically decide when to re-plan, striking a balance between adaptability and consistency in planning. This planner is also more tolerant of errors: it removes the immediate previous landmark when it re-plans, so that the agent will be less prone to getting stuck. In Figure [8](#fig:ablation-planning){reference-type="ref" reference="fig:ablation-planning"}, we compare the $L^{3}P$ planner to a naive planner, which simply re-calculates the shortest path at every step. The result shows that our planning algorithm is crucial to the success of $L^{3}P$.

An important hyper-parameter in graph-based planning is the number of landmarks being used. Intuitively, since $L^{3}P$ is *learning* the nodes on the graph, it should be robust to the changes in the number of nodes (landmarks) being learned. In Figure [8](#fig:ablation-planning){reference-type="ref" reference="fig:ablation-planning"}, we show that this is indeed the case: $L^{3}P$ is robust to the number of latent landmarks. In contrast to prior methods, $L^{3}P$ is able to *learn* the nodes (landmarks) used for graph search from the agent's own experience. We vary this hyper-parameter in the challenging AntMaze-Hard environment, and we find that $L^{3}P$ is robust against a variety of values. This is expected, because the landmarks in the latent space of $L^{3}P$ will try to be equally scattered across the goal space according to the learned reachability metric. As the number of landmarks decreases, the learning procedure will automatically push the landmarks to be further away from one another.

# Closing Remarks

In this work, we introduce a way of learning graph-structured world models that endow agents with the ability to do temporally extended reasoning. The algorithm, $L^{3}P$, learns a set of latent landmarks scattered across the goal space to enable scalable planning. We demonstrate that $L^{3}P$ achieves significantly better sample efficiency, higher asymptotic performance, and generalization to longer horizons on a range of challenging robotic navigation and manipulation tasks. Here we briefly discuss two promising future directions. First, how can an agent quickly generate a set of plausible landmarks in a previously unseen environment? A lot of progress has been made on the topics of meta reinforcement learning and learning to explore; can $L^{3}P$ be combined with meta learning techniques for fast landmarks generation? Second, can we learn graph-structured world models from offline datasets? Batch RL is a more realistic setting for many RL applications, since online interaction can be expensive in the real world. Applying $L^{3}P$ to offline datasets might require a notion of uncertainty in different parts of the graph.

# Acknowledgements {#acknowledgements .unnumbered}

We thank the anonymous reviewers for providing helpful comments on the paper. Resources used in preparing this research were provided, in part, by the Province of Ontario, the Government of Canada through CIFAR, and companies sponsoring the Vector Institute for Artificial Intelligence ([www.vectorinstitute.ai/partners](www.vectorinstitute.ai/partners){.uri}).

# Appendix A: Greedy Latent Sparsification {#appendix-a-greedy-latent-sparsification .unnumbered}

::: {.figure latex-placement="h"}
![](Zhang2020World_figs/algorithm.png){width="50%"}
:::

The Greedy Latent Sparsification (GLS) algorithm sub-samples a large batch by sparsification. GLS first randomly selects a latent embedding from the batch, and then greedily chooses the next embedding that is furthest away from already selected embeddings. After collecting some *warm-up trajectories* before planning starts (see Table 1 below) during training, we first use GLS to initialize the latent centroids, and then continue to use it to sample the batches used to train the latent clusters. GLS is strongly inspired by [@kmeans_plus_plus], and this type of approach is known to improve clustering.

# Appendix B: Graph Search with Soft Relaxations {#appendix_sin .unnumbered}

In this paper, we employ a soft version of Floyd algorithm, which we find to empirically work well. Rather than simply using the $\min$ operation to do relaxation, the soft value iteration procedure uses a $soft\min$ operation when doing an update (note that, since we negated the distances to be negative in the weight matrix of the graph, the operations we use are actually max and softmax). The reason is that neural distances can be inconsistent and inaccurate at times, and using a soft operation makes the whole procedure more robust. More concretely, we repeat the following update on the weight matrix for $S$ steps with temperature $\beta$: $$\begin{align}
    w_{i,j} &\leftarrow \sum_{k=1}^{N+1} \dfrac{\exp \dfrac{1}{\beta}(w_{i, k} + w_{k, j})}{ \sum_{k'=1}^{N+1} \exp \dfrac{1}{\beta}(w_{i, k'} + w_{k', j}) } \Big( w_{i, k} + w_{k, j} \Big) %\label{sin}
\end{align}$$ Following the practice in [@sorb; @mss], we do the following initialization to the distance matrix: for entries smaller than the negative of $d\_max$, we penalize the entry by adding $-\infty$ to it (in this paper, we use $-10^{6}$ as the $-\infty$ value). The essential idea is that we only trust a neural estimate when it is *local*, and we rely on graph search to solve for *global*, longer-horizon distances. The $-\infty$ penalty effectively masks out those entries with large negative values in the softmax operation above. If we replace softmax with a hard max, we recover the original update in Floyd algorithm; we can interpolate between a hard Floyd and a soft Floyd by tuning the temperature $\beta$.

# Appendix C: Overall Training Procedure {#appendix-c-overall-training-procedure .unnumbered}

Here we provide an overall training procedure for $L^{3}P$ in **Algorithm 3**. Given an environment `env` and a training goal distribution $p(g)$, we initialize a replay buffer $B$ and the following **trainble modules**: policy $\pi$, distance function $D$, value function $V$, encoder $f_{E}$ and decoder $f_{D}$, latent centroids $\{\textbf{c}_{1} \cdots \textbf{c}_{N}\}$.

Every $K_{env}$ episodes of sampling, we take gradient steps for the above modules. The ratio between the number of environment steps and the number of gradient steps is a hyper-parameter.

::: {.figure latex-placement="h"}
![](Zhang2020World_figs/overall-training.png){width="50%"}
:::

# Appendix D: Implementation Details {#appendix-d-implementation-details .unnumbered}

- We find that having a centralized replay for all parallel workers is significantly more sample efficient than having separate replays for each worker and simply averaging the gradients across workers.

- For Ant-Maze environment, we do grad norm clipping by a value of $15.0$ for all networks. For Fetch tasks, we normalize the inputs by running means and standard deviations per input dimensions.

- Since $L^{3}P$ is able to decompose a long-horizon goal into many short-horizon goals, we shorten the range of future steps where we do hindsight relabelling; as a result, the agent can focus its optimization effort on more immediate goals. This corresponds to the hyper-parameter: hindsight relabelling range.

- During training, we collect $50\%$ of the data without the planning module, and the other $50\%$ of the data with planning. This corresponds to the hyper-parameter: probability of using search during train.

- At train time, to encourage exploration during planning, we temporarily add a small number of random landmarks from GLS (**Algorithm 2**) to the existing latent landmarks. A new set of random landmarks is selected for each episode before graph search starts (**Algorithm 1**). This corresponds to the hyper-parameter: random landmarks added during train.

- We find that collecting a certain number of *warm-up trajectories* for every worker before the planning procedure starts (during training) and before GLS (Algorithm 2) is used for initialization to help improve the planning results. This corresponds to the hyper-parameter: number of *warm-up trajectories*.

# Appendix E: Hyper-parameters {#app:hypers .unnumbered}

The first table below lists the common hyper-parameters across all environments. The second table below lists the hyper-parameters that differ across the environments.

::: {.figure latex-placement="h"}
![](Zhang2020World_figs/table_1.png){width="50%"}
:::

::: {.figure latex-placement="h"}
![](Zhang2020World_figs/table_2.png){width="50%"}
:::
